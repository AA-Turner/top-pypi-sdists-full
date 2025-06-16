r'''
# `google_container_aws_node_pool`

Refer to the Terraform Registry for docs: [`google_container_aws_node_pool`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool).
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


class GoogleContainerAwsNodePool(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsNodePool.GoogleContainerAwsNodePool",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool google_container_aws_node_pool}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        autoscaling: typing.Union["GoogleContainerAwsNodePoolAutoscaling", typing.Dict[builtins.str, typing.Any]],
        cluster: builtins.str,
        config: typing.Union["GoogleContainerAwsNodePoolConfigA", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        max_pods_constraint: typing.Union["GoogleContainerAwsNodePoolMaxPodsConstraint", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        subnet_id: builtins.str,
        version: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        kubelet_config: typing.Optional[typing.Union["GoogleContainerAwsNodePoolKubeletConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        management: typing.Optional[typing.Union["GoogleContainerAwsNodePoolManagement", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleContainerAwsNodePoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        update_settings: typing.Optional[typing.Union["GoogleContainerAwsNodePoolUpdateSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool google_container_aws_node_pool} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param autoscaling: autoscaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#autoscaling GoogleContainerAwsNodePool#autoscaling}
        :param cluster: The awsCluster for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#cluster GoogleContainerAwsNodePool#cluster}
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#config GoogleContainerAwsNodePool#config}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#location GoogleContainerAwsNodePool#location}
        :param max_pods_constraint: max_pods_constraint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#max_pods_constraint GoogleContainerAwsNodePool#max_pods_constraint}
        :param name: The name of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#name GoogleContainerAwsNodePool#name}
        :param subnet_id: The subnet where the node pool node run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#subnet_id GoogleContainerAwsNodePool#subnet_id}
        :param version: The Kubernetes version to run on this node pool (e.g. ``1.19.10-gke.1000``). You can list all supported versions on a given Google Cloud region by calling GetAwsServerConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#version GoogleContainerAwsNodePool#version}
        :param annotations: Optional. Annotations on the node pool. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Key can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field ``effective_annotations`` for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#annotations GoogleContainerAwsNodePool#annotations}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#id GoogleContainerAwsNodePool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kubelet_config: kubelet_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#kubelet_config GoogleContainerAwsNodePool#kubelet_config}
        :param management: management block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#management GoogleContainerAwsNodePool#management}
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#project GoogleContainerAwsNodePool#project}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#timeouts GoogleContainerAwsNodePool#timeouts}
        :param update_settings: update_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#update_settings GoogleContainerAwsNodePool#update_settings}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73268889630ec5b4031758b2c1d6456cac78ae83b91587693542dfc7ce1f1c98)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config_ = GoogleContainerAwsNodePoolConfig(
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
        '''Generates CDKTF code for importing a GoogleContainerAwsNodePool resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleContainerAwsNodePool to import.
        :param import_from_id: The id of the existing GoogleContainerAwsNodePool that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleContainerAwsNodePool to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35c9c515416140be74e3fca3551a5c9615e094a62cf19e040233d2dc6c1bf355)
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
        :param max_node_count: Maximum number of nodes in the NodePool. Must be >= min_node_count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#max_node_count GoogleContainerAwsNodePool#max_node_count}
        :param min_node_count: Minimum number of nodes in the NodePool. Must be >= 1 and <= max_node_count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#min_node_count GoogleContainerAwsNodePool#min_node_count}
        '''
        value = GoogleContainerAwsNodePoolAutoscaling(
            max_node_count=max_node_count, min_node_count=min_node_count
        )

        return typing.cast(None, jsii.invoke(self, "putAutoscaling", [value]))

    @jsii.member(jsii_name="putConfig")
    def put_config(
        self,
        *,
        config_encryption: typing.Union["GoogleContainerAwsNodePoolConfigConfigEncryption", typing.Dict[builtins.str, typing.Any]],
        iam_instance_profile: builtins.str,
        autoscaling_metrics_collection: typing.Optional[typing.Union["GoogleContainerAwsNodePoolConfigAutoscalingMetricsCollection", typing.Dict[builtins.str, typing.Any]]] = None,
        image_type: typing.Optional[builtins.str] = None,
        instance_placement: typing.Optional[typing.Union["GoogleContainerAwsNodePoolConfigInstancePlacement", typing.Dict[builtins.str, typing.Any]]] = None,
        instance_type: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        proxy_config: typing.Optional[typing.Union["GoogleContainerAwsNodePoolConfigProxyConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        root_volume: typing.Optional[typing.Union["GoogleContainerAwsNodePoolConfigRootVolume", typing.Dict[builtins.str, typing.Any]]] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        spot_config: typing.Optional[typing.Union["GoogleContainerAwsNodePoolConfigSpotConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ssh_config: typing.Optional[typing.Union["GoogleContainerAwsNodePoolConfigSshConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleContainerAwsNodePoolConfigTaints", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param config_encryption: config_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#config_encryption GoogleContainerAwsNodePool#config_encryption}
        :param iam_instance_profile: The name of the AWS IAM role assigned to nodes in the pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#iam_instance_profile GoogleContainerAwsNodePool#iam_instance_profile}
        :param autoscaling_metrics_collection: autoscaling_metrics_collection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#autoscaling_metrics_collection GoogleContainerAwsNodePool#autoscaling_metrics_collection}
        :param image_type: The OS image type to use on node pool instances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#image_type GoogleContainerAwsNodePool#image_type}
        :param instance_placement: instance_placement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#instance_placement GoogleContainerAwsNodePool#instance_placement}
        :param instance_type: Optional. The AWS instance type. When unspecified, it defaults to ``m5.large``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#instance_type GoogleContainerAwsNodePool#instance_type}
        :param labels: Optional. The initial labels assigned to nodes of this node pool. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#labels GoogleContainerAwsNodePool#labels}
        :param proxy_config: proxy_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#proxy_config GoogleContainerAwsNodePool#proxy_config}
        :param root_volume: root_volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#root_volume GoogleContainerAwsNodePool#root_volume}
        :param security_group_ids: Optional. The IDs of additional security groups to add to nodes in this pool. The manager will automatically create security groups with minimum rules needed for a functioning cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#security_group_ids GoogleContainerAwsNodePool#security_group_ids}
        :param spot_config: spot_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#spot_config GoogleContainerAwsNodePool#spot_config}
        :param ssh_config: ssh_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#ssh_config GoogleContainerAwsNodePool#ssh_config}
        :param tags: Optional. Key/value metadata to assign to each underlying AWS resource. Specify at most 50 pairs containing alphanumerics, spaces, and symbols (.+-=_:@/). Keys can be up to 127 Unicode characters. Values can be up to 255 Unicode characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#tags GoogleContainerAwsNodePool#tags}
        :param taints: taints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#taints GoogleContainerAwsNodePool#taints}
        '''
        value = GoogleContainerAwsNodePoolConfigA(
            config_encryption=config_encryption,
            iam_instance_profile=iam_instance_profile,
            autoscaling_metrics_collection=autoscaling_metrics_collection,
            image_type=image_type,
            instance_placement=instance_placement,
            instance_type=instance_type,
            labels=labels,
            proxy_config=proxy_config,
            root_volume=root_volume,
            security_group_ids=security_group_ids,
            spot_config=spot_config,
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
        :param cpu_cfs_quota: Whether or not to enable CPU CFS quota. Defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#cpu_cfs_quota GoogleContainerAwsNodePool#cpu_cfs_quota}
        :param cpu_cfs_quota_period: Optional. The CPU CFS quota period to use for the node. Defaults to "100ms". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#cpu_cfs_quota_period GoogleContainerAwsNodePool#cpu_cfs_quota_period}
        :param cpu_manager_policy: The CpuManagerPolicy to use for the node. Defaults to "none". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#cpu_manager_policy GoogleContainerAwsNodePool#cpu_manager_policy}
        :param pod_pids_limit: Optional. The maximum number of PIDs in each pod running on the node. The limit scales automatically based on underlying machine size if left unset. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#pod_pids_limit GoogleContainerAwsNodePool#pod_pids_limit}
        '''
        value = GoogleContainerAwsNodePoolKubeletConfig(
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
        :param auto_repair: Optional. Whether or not the nodes will be automatically repaired. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#auto_repair GoogleContainerAwsNodePool#auto_repair}
        '''
        value = GoogleContainerAwsNodePoolManagement(auto_repair=auto_repair)

        return typing.cast(None, jsii.invoke(self, "putManagement", [value]))

    @jsii.member(jsii_name="putMaxPodsConstraint")
    def put_max_pods_constraint(self, *, max_pods_per_node: jsii.Number) -> None:
        '''
        :param max_pods_per_node: The maximum number of pods to schedule on a single node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#max_pods_per_node GoogleContainerAwsNodePool#max_pods_per_node}
        '''
        value = GoogleContainerAwsNodePoolMaxPodsConstraint(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#create GoogleContainerAwsNodePool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#delete GoogleContainerAwsNodePool#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#update GoogleContainerAwsNodePool#update}.
        '''
        value = GoogleContainerAwsNodePoolTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putUpdateSettings")
    def put_update_settings(
        self,
        *,
        surge_settings: typing.Optional[typing.Union["GoogleContainerAwsNodePoolUpdateSettingsSurgeSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param surge_settings: surge_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#surge_settings GoogleContainerAwsNodePool#surge_settings}
        '''
        value = GoogleContainerAwsNodePoolUpdateSettings(surge_settings=surge_settings)

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
    def autoscaling(self) -> "GoogleContainerAwsNodePoolAutoscalingOutputReference":
        return typing.cast("GoogleContainerAwsNodePoolAutoscalingOutputReference", jsii.get(self, "autoscaling"))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> "GoogleContainerAwsNodePoolConfigAOutputReference":
        return typing.cast("GoogleContainerAwsNodePoolConfigAOutputReference", jsii.get(self, "config"))

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
    def kubelet_config(
        self,
    ) -> "GoogleContainerAwsNodePoolKubeletConfigOutputReference":
        return typing.cast("GoogleContainerAwsNodePoolKubeletConfigOutputReference", jsii.get(self, "kubeletConfig"))

    @builtins.property
    @jsii.member(jsii_name="management")
    def management(self) -> "GoogleContainerAwsNodePoolManagementOutputReference":
        return typing.cast("GoogleContainerAwsNodePoolManagementOutputReference", jsii.get(self, "management"))

    @builtins.property
    @jsii.member(jsii_name="maxPodsConstraint")
    def max_pods_constraint(
        self,
    ) -> "GoogleContainerAwsNodePoolMaxPodsConstraintOutputReference":
        return typing.cast("GoogleContainerAwsNodePoolMaxPodsConstraintOutputReference", jsii.get(self, "maxPodsConstraint"))

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
    def timeouts(self) -> "GoogleContainerAwsNodePoolTimeoutsOutputReference":
        return typing.cast("GoogleContainerAwsNodePoolTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateSettings")
    def update_settings(
        self,
    ) -> "GoogleContainerAwsNodePoolUpdateSettingsOutputReference":
        return typing.cast("GoogleContainerAwsNodePoolUpdateSettingsOutputReference", jsii.get(self, "updateSettings"))

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
    def autoscaling_input(
        self,
    ) -> typing.Optional["GoogleContainerAwsNodePoolAutoscaling"]:
        return typing.cast(typing.Optional["GoogleContainerAwsNodePoolAutoscaling"], jsii.get(self, "autoscalingInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterInput")
    def cluster_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterInput"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(self) -> typing.Optional["GoogleContainerAwsNodePoolConfigA"]:
        return typing.cast(typing.Optional["GoogleContainerAwsNodePoolConfigA"], jsii.get(self, "configInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kubeletConfigInput")
    def kubelet_config_input(
        self,
    ) -> typing.Optional["GoogleContainerAwsNodePoolKubeletConfig"]:
        return typing.cast(typing.Optional["GoogleContainerAwsNodePoolKubeletConfig"], jsii.get(self, "kubeletConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="managementInput")
    def management_input(
        self,
    ) -> typing.Optional["GoogleContainerAwsNodePoolManagement"]:
        return typing.cast(typing.Optional["GoogleContainerAwsNodePoolManagement"], jsii.get(self, "managementInput"))

    @builtins.property
    @jsii.member(jsii_name="maxPodsConstraintInput")
    def max_pods_constraint_input(
        self,
    ) -> typing.Optional["GoogleContainerAwsNodePoolMaxPodsConstraint"]:
        return typing.cast(typing.Optional["GoogleContainerAwsNodePoolMaxPodsConstraint"], jsii.get(self, "maxPodsConstraintInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleContainerAwsNodePoolTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleContainerAwsNodePoolTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="updateSettingsInput")
    def update_settings_input(
        self,
    ) -> typing.Optional["GoogleContainerAwsNodePoolUpdateSettings"]:
        return typing.cast(typing.Optional["GoogleContainerAwsNodePoolUpdateSettings"], jsii.get(self, "updateSettingsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__883fb559698c2eee78a4b89d5204b6a31a740a4cb0845868e6737489df035920)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cluster"))

    @cluster.setter
    def cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f8c0c771d2fb88b6b02916ab8eedf52a031736ad723affcf4f281fc116f699b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18b45b3fced8214e8c62ff3a4efe1d342950659ae20d2b1e87ca4dc8be98d19f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40c97904e5372247d234f0c93fb3aff8f75f3f32551d3ee09001e0bba5438504)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00d2128ac593c3291157343ec6e55c1579693ddccbf452f947db0f46c0e8cfb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfadb76dc755a180864f38024f923cda11b4112a0a0364a584434b251489ad85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afd79c50160434b57f71aa6e7e5ee6c1385f20d5bcc73ab71078a80fdfa20c2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1d7a6ebbda3398a895e7e4a89f1827204e3ecff1adcc3b71dacae9aabb78fd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsNodePool.GoogleContainerAwsNodePoolAutoscaling",
    jsii_struct_bases=[],
    name_mapping={"max_node_count": "maxNodeCount", "min_node_count": "minNodeCount"},
)
class GoogleContainerAwsNodePoolAutoscaling:
    def __init__(
        self,
        *,
        max_node_count: jsii.Number,
        min_node_count: jsii.Number,
    ) -> None:
        '''
        :param max_node_count: Maximum number of nodes in the NodePool. Must be >= min_node_count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#max_node_count GoogleContainerAwsNodePool#max_node_count}
        :param min_node_count: Minimum number of nodes in the NodePool. Must be >= 1 and <= max_node_count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#min_node_count GoogleContainerAwsNodePool#min_node_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd9ebde0d630ce4b5d4c12505bfce75c8a94b2425ed454c175b0281ec8b9838b)
            check_type(argname="argument max_node_count", value=max_node_count, expected_type=type_hints["max_node_count"])
            check_type(argname="argument min_node_count", value=min_node_count, expected_type=type_hints["min_node_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_node_count": max_node_count,
            "min_node_count": min_node_count,
        }

    @builtins.property
    def max_node_count(self) -> jsii.Number:
        '''Maximum number of nodes in the NodePool. Must be >= min_node_count.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#max_node_count GoogleContainerAwsNodePool#max_node_count}
        '''
        result = self._values.get("max_node_count")
        assert result is not None, "Required property 'max_node_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def min_node_count(self) -> jsii.Number:
        '''Minimum number of nodes in the NodePool. Must be >= 1 and <= max_node_count.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#min_node_count GoogleContainerAwsNodePool#min_node_count}
        '''
        result = self._values.get("min_node_count")
        assert result is not None, "Required property 'min_node_count' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsNodePoolAutoscaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAwsNodePoolAutoscalingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsNodePool.GoogleContainerAwsNodePoolAutoscalingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bf1e49f248e13374a8810770ee58bc7bdb84fb5b1280414afa4a1b2922fd8b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44e6865a72c154904711e904eb93d33cbcc9ee1654b73f38834a288013e77eca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minNodeCount")
    def min_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minNodeCount"))

    @min_node_count.setter
    def min_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc5b3bc0c7483038e5cab8d5ad02811d3d9ef3c607941114521b04f279185fc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleContainerAwsNodePoolAutoscaling]:
        return typing.cast(typing.Optional[GoogleContainerAwsNodePoolAutoscaling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAwsNodePoolAutoscaling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4e3221d2f834b30f72dc0b1455b98f90897b282d43d414460683c859fd063e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsNodePool.GoogleContainerAwsNodePoolConfig",
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
class GoogleContainerAwsNodePoolConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        autoscaling: typing.Union[GoogleContainerAwsNodePoolAutoscaling, typing.Dict[builtins.str, typing.Any]],
        cluster: builtins.str,
        config: typing.Union["GoogleContainerAwsNodePoolConfigA", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        max_pods_constraint: typing.Union["GoogleContainerAwsNodePoolMaxPodsConstraint", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        subnet_id: builtins.str,
        version: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        kubelet_config: typing.Optional[typing.Union["GoogleContainerAwsNodePoolKubeletConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        management: typing.Optional[typing.Union["GoogleContainerAwsNodePoolManagement", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleContainerAwsNodePoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        update_settings: typing.Optional[typing.Union["GoogleContainerAwsNodePoolUpdateSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param autoscaling: autoscaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#autoscaling GoogleContainerAwsNodePool#autoscaling}
        :param cluster: The awsCluster for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#cluster GoogleContainerAwsNodePool#cluster}
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#config GoogleContainerAwsNodePool#config}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#location GoogleContainerAwsNodePool#location}
        :param max_pods_constraint: max_pods_constraint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#max_pods_constraint GoogleContainerAwsNodePool#max_pods_constraint}
        :param name: The name of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#name GoogleContainerAwsNodePool#name}
        :param subnet_id: The subnet where the node pool node run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#subnet_id GoogleContainerAwsNodePool#subnet_id}
        :param version: The Kubernetes version to run on this node pool (e.g. ``1.19.10-gke.1000``). You can list all supported versions on a given Google Cloud region by calling GetAwsServerConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#version GoogleContainerAwsNodePool#version}
        :param annotations: Optional. Annotations on the node pool. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Key can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field ``effective_annotations`` for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#annotations GoogleContainerAwsNodePool#annotations}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#id GoogleContainerAwsNodePool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kubelet_config: kubelet_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#kubelet_config GoogleContainerAwsNodePool#kubelet_config}
        :param management: management block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#management GoogleContainerAwsNodePool#management}
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#project GoogleContainerAwsNodePool#project}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#timeouts GoogleContainerAwsNodePool#timeouts}
        :param update_settings: update_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#update_settings GoogleContainerAwsNodePool#update_settings}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(autoscaling, dict):
            autoscaling = GoogleContainerAwsNodePoolAutoscaling(**autoscaling)
        if isinstance(config, dict):
            config = GoogleContainerAwsNodePoolConfigA(**config)
        if isinstance(max_pods_constraint, dict):
            max_pods_constraint = GoogleContainerAwsNodePoolMaxPodsConstraint(**max_pods_constraint)
        if isinstance(kubelet_config, dict):
            kubelet_config = GoogleContainerAwsNodePoolKubeletConfig(**kubelet_config)
        if isinstance(management, dict):
            management = GoogleContainerAwsNodePoolManagement(**management)
        if isinstance(timeouts, dict):
            timeouts = GoogleContainerAwsNodePoolTimeouts(**timeouts)
        if isinstance(update_settings, dict):
            update_settings = GoogleContainerAwsNodePoolUpdateSettings(**update_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1cdad113338b09deb183284d28c9b5083f150881d6eb4e850555a3eadff602b)
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
    def autoscaling(self) -> GoogleContainerAwsNodePoolAutoscaling:
        '''autoscaling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#autoscaling GoogleContainerAwsNodePool#autoscaling}
        '''
        result = self._values.get("autoscaling")
        assert result is not None, "Required property 'autoscaling' is missing"
        return typing.cast(GoogleContainerAwsNodePoolAutoscaling, result)

    @builtins.property
    def cluster(self) -> builtins.str:
        '''The awsCluster for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#cluster GoogleContainerAwsNodePool#cluster}
        '''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def config(self) -> "GoogleContainerAwsNodePoolConfigA":
        '''config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#config GoogleContainerAwsNodePool#config}
        '''
        result = self._values.get("config")
        assert result is not None, "Required property 'config' is missing"
        return typing.cast("GoogleContainerAwsNodePoolConfigA", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#location GoogleContainerAwsNodePool#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def max_pods_constraint(self) -> "GoogleContainerAwsNodePoolMaxPodsConstraint":
        '''max_pods_constraint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#max_pods_constraint GoogleContainerAwsNodePool#max_pods_constraint}
        '''
        result = self._values.get("max_pods_constraint")
        assert result is not None, "Required property 'max_pods_constraint' is missing"
        return typing.cast("GoogleContainerAwsNodePoolMaxPodsConstraint", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#name GoogleContainerAwsNodePool#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''The subnet where the node pool node run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#subnet_id GoogleContainerAwsNodePool#subnet_id}
        '''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''The Kubernetes version to run on this node pool (e.g. ``1.19.10-gke.1000``). You can list all supported versions on a given Google Cloud region by calling GetAwsServerConfig.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#version GoogleContainerAwsNodePool#version}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#annotations GoogleContainerAwsNodePool#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#id GoogleContainerAwsNodePool#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kubelet_config(
        self,
    ) -> typing.Optional["GoogleContainerAwsNodePoolKubeletConfig"]:
        '''kubelet_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#kubelet_config GoogleContainerAwsNodePool#kubelet_config}
        '''
        result = self._values.get("kubelet_config")
        return typing.cast(typing.Optional["GoogleContainerAwsNodePoolKubeletConfig"], result)

    @builtins.property
    def management(self) -> typing.Optional["GoogleContainerAwsNodePoolManagement"]:
        '''management block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#management GoogleContainerAwsNodePool#management}
        '''
        result = self._values.get("management")
        return typing.cast(typing.Optional["GoogleContainerAwsNodePoolManagement"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The project for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#project GoogleContainerAwsNodePool#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleContainerAwsNodePoolTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#timeouts GoogleContainerAwsNodePool#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleContainerAwsNodePoolTimeouts"], result)

    @builtins.property
    def update_settings(
        self,
    ) -> typing.Optional["GoogleContainerAwsNodePoolUpdateSettings"]:
        '''update_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#update_settings GoogleContainerAwsNodePool#update_settings}
        '''
        result = self._values.get("update_settings")
        return typing.cast(typing.Optional["GoogleContainerAwsNodePoolUpdateSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsNodePoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsNodePool.GoogleContainerAwsNodePoolConfigA",
    jsii_struct_bases=[],
    name_mapping={
        "config_encryption": "configEncryption",
        "iam_instance_profile": "iamInstanceProfile",
        "autoscaling_metrics_collection": "autoscalingMetricsCollection",
        "image_type": "imageType",
        "instance_placement": "instancePlacement",
        "instance_type": "instanceType",
        "labels": "labels",
        "proxy_config": "proxyConfig",
        "root_volume": "rootVolume",
        "security_group_ids": "securityGroupIds",
        "spot_config": "spotConfig",
        "ssh_config": "sshConfig",
        "tags": "tags",
        "taints": "taints",
    },
)
class GoogleContainerAwsNodePoolConfigA:
    def __init__(
        self,
        *,
        config_encryption: typing.Union["GoogleContainerAwsNodePoolConfigConfigEncryption", typing.Dict[builtins.str, typing.Any]],
        iam_instance_profile: builtins.str,
        autoscaling_metrics_collection: typing.Optional[typing.Union["GoogleContainerAwsNodePoolConfigAutoscalingMetricsCollection", typing.Dict[builtins.str, typing.Any]]] = None,
        image_type: typing.Optional[builtins.str] = None,
        instance_placement: typing.Optional[typing.Union["GoogleContainerAwsNodePoolConfigInstancePlacement", typing.Dict[builtins.str, typing.Any]]] = None,
        instance_type: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        proxy_config: typing.Optional[typing.Union["GoogleContainerAwsNodePoolConfigProxyConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        root_volume: typing.Optional[typing.Union["GoogleContainerAwsNodePoolConfigRootVolume", typing.Dict[builtins.str, typing.Any]]] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        spot_config: typing.Optional[typing.Union["GoogleContainerAwsNodePoolConfigSpotConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ssh_config: typing.Optional[typing.Union["GoogleContainerAwsNodePoolConfigSshConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleContainerAwsNodePoolConfigTaints", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param config_encryption: config_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#config_encryption GoogleContainerAwsNodePool#config_encryption}
        :param iam_instance_profile: The name of the AWS IAM role assigned to nodes in the pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#iam_instance_profile GoogleContainerAwsNodePool#iam_instance_profile}
        :param autoscaling_metrics_collection: autoscaling_metrics_collection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#autoscaling_metrics_collection GoogleContainerAwsNodePool#autoscaling_metrics_collection}
        :param image_type: The OS image type to use on node pool instances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#image_type GoogleContainerAwsNodePool#image_type}
        :param instance_placement: instance_placement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#instance_placement GoogleContainerAwsNodePool#instance_placement}
        :param instance_type: Optional. The AWS instance type. When unspecified, it defaults to ``m5.large``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#instance_type GoogleContainerAwsNodePool#instance_type}
        :param labels: Optional. The initial labels assigned to nodes of this node pool. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#labels GoogleContainerAwsNodePool#labels}
        :param proxy_config: proxy_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#proxy_config GoogleContainerAwsNodePool#proxy_config}
        :param root_volume: root_volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#root_volume GoogleContainerAwsNodePool#root_volume}
        :param security_group_ids: Optional. The IDs of additional security groups to add to nodes in this pool. The manager will automatically create security groups with minimum rules needed for a functioning cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#security_group_ids GoogleContainerAwsNodePool#security_group_ids}
        :param spot_config: spot_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#spot_config GoogleContainerAwsNodePool#spot_config}
        :param ssh_config: ssh_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#ssh_config GoogleContainerAwsNodePool#ssh_config}
        :param tags: Optional. Key/value metadata to assign to each underlying AWS resource. Specify at most 50 pairs containing alphanumerics, spaces, and symbols (.+-=_:@/). Keys can be up to 127 Unicode characters. Values can be up to 255 Unicode characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#tags GoogleContainerAwsNodePool#tags}
        :param taints: taints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#taints GoogleContainerAwsNodePool#taints}
        '''
        if isinstance(config_encryption, dict):
            config_encryption = GoogleContainerAwsNodePoolConfigConfigEncryption(**config_encryption)
        if isinstance(autoscaling_metrics_collection, dict):
            autoscaling_metrics_collection = GoogleContainerAwsNodePoolConfigAutoscalingMetricsCollection(**autoscaling_metrics_collection)
        if isinstance(instance_placement, dict):
            instance_placement = GoogleContainerAwsNodePoolConfigInstancePlacement(**instance_placement)
        if isinstance(proxy_config, dict):
            proxy_config = GoogleContainerAwsNodePoolConfigProxyConfig(**proxy_config)
        if isinstance(root_volume, dict):
            root_volume = GoogleContainerAwsNodePoolConfigRootVolume(**root_volume)
        if isinstance(spot_config, dict):
            spot_config = GoogleContainerAwsNodePoolConfigSpotConfig(**spot_config)
        if isinstance(ssh_config, dict):
            ssh_config = GoogleContainerAwsNodePoolConfigSshConfig(**ssh_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1954e141c98bcaf9353b75ace200e5b3741e9a1e038db6b8c4cbad9f6efe1513)
            check_type(argname="argument config_encryption", value=config_encryption, expected_type=type_hints["config_encryption"])
            check_type(argname="argument iam_instance_profile", value=iam_instance_profile, expected_type=type_hints["iam_instance_profile"])
            check_type(argname="argument autoscaling_metrics_collection", value=autoscaling_metrics_collection, expected_type=type_hints["autoscaling_metrics_collection"])
            check_type(argname="argument image_type", value=image_type, expected_type=type_hints["image_type"])
            check_type(argname="argument instance_placement", value=instance_placement, expected_type=type_hints["instance_placement"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument proxy_config", value=proxy_config, expected_type=type_hints["proxy_config"])
            check_type(argname="argument root_volume", value=root_volume, expected_type=type_hints["root_volume"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument spot_config", value=spot_config, expected_type=type_hints["spot_config"])
            check_type(argname="argument ssh_config", value=ssh_config, expected_type=type_hints["ssh_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument taints", value=taints, expected_type=type_hints["taints"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "config_encryption": config_encryption,
            "iam_instance_profile": iam_instance_profile,
        }
        if autoscaling_metrics_collection is not None:
            self._values["autoscaling_metrics_collection"] = autoscaling_metrics_collection
        if image_type is not None:
            self._values["image_type"] = image_type
        if instance_placement is not None:
            self._values["instance_placement"] = instance_placement
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
        if spot_config is not None:
            self._values["spot_config"] = spot_config
        if ssh_config is not None:
            self._values["ssh_config"] = ssh_config
        if tags is not None:
            self._values["tags"] = tags
        if taints is not None:
            self._values["taints"] = taints

    @builtins.property
    def config_encryption(self) -> "GoogleContainerAwsNodePoolConfigConfigEncryption":
        '''config_encryption block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#config_encryption GoogleContainerAwsNodePool#config_encryption}
        '''
        result = self._values.get("config_encryption")
        assert result is not None, "Required property 'config_encryption' is missing"
        return typing.cast("GoogleContainerAwsNodePoolConfigConfigEncryption", result)

    @builtins.property
    def iam_instance_profile(self) -> builtins.str:
        '''The name of the AWS IAM role assigned to nodes in the pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#iam_instance_profile GoogleContainerAwsNodePool#iam_instance_profile}
        '''
        result = self._values.get("iam_instance_profile")
        assert result is not None, "Required property 'iam_instance_profile' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def autoscaling_metrics_collection(
        self,
    ) -> typing.Optional["GoogleContainerAwsNodePoolConfigAutoscalingMetricsCollection"]:
        '''autoscaling_metrics_collection block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#autoscaling_metrics_collection GoogleContainerAwsNodePool#autoscaling_metrics_collection}
        '''
        result = self._values.get("autoscaling_metrics_collection")
        return typing.cast(typing.Optional["GoogleContainerAwsNodePoolConfigAutoscalingMetricsCollection"], result)

    @builtins.property
    def image_type(self) -> typing.Optional[builtins.str]:
        '''The OS image type to use on node pool instances.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#image_type GoogleContainerAwsNodePool#image_type}
        '''
        result = self._values.get("image_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_placement(
        self,
    ) -> typing.Optional["GoogleContainerAwsNodePoolConfigInstancePlacement"]:
        '''instance_placement block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#instance_placement GoogleContainerAwsNodePool#instance_placement}
        '''
        result = self._values.get("instance_placement")
        return typing.cast(typing.Optional["GoogleContainerAwsNodePoolConfigInstancePlacement"], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''Optional. The AWS instance type. When unspecified, it defaults to ``m5.large``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#instance_type GoogleContainerAwsNodePool#instance_type}
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        The initial labels assigned to nodes of this node pool. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#labels GoogleContainerAwsNodePool#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def proxy_config(
        self,
    ) -> typing.Optional["GoogleContainerAwsNodePoolConfigProxyConfig"]:
        '''proxy_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#proxy_config GoogleContainerAwsNodePool#proxy_config}
        '''
        result = self._values.get("proxy_config")
        return typing.cast(typing.Optional["GoogleContainerAwsNodePoolConfigProxyConfig"], result)

    @builtins.property
    def root_volume(
        self,
    ) -> typing.Optional["GoogleContainerAwsNodePoolConfigRootVolume"]:
        '''root_volume block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#root_volume GoogleContainerAwsNodePool#root_volume}
        '''
        result = self._values.get("root_volume")
        return typing.cast(typing.Optional["GoogleContainerAwsNodePoolConfigRootVolume"], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        The IDs of additional security groups to add to nodes in this pool. The manager will automatically create security groups with minimum rules needed for a functioning cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#security_group_ids GoogleContainerAwsNodePool#security_group_ids}
        '''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def spot_config(
        self,
    ) -> typing.Optional["GoogleContainerAwsNodePoolConfigSpotConfig"]:
        '''spot_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#spot_config GoogleContainerAwsNodePool#spot_config}
        '''
        result = self._values.get("spot_config")
        return typing.cast(typing.Optional["GoogleContainerAwsNodePoolConfigSpotConfig"], result)

    @builtins.property
    def ssh_config(
        self,
    ) -> typing.Optional["GoogleContainerAwsNodePoolConfigSshConfig"]:
        '''ssh_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#ssh_config GoogleContainerAwsNodePool#ssh_config}
        '''
        result = self._values.get("ssh_config")
        return typing.cast(typing.Optional["GoogleContainerAwsNodePoolConfigSshConfig"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        Key/value metadata to assign to each underlying AWS resource. Specify at most 50 pairs containing alphanumerics, spaces, and symbols (.+-=_:@/). Keys can be up to 127 Unicode characters. Values can be up to 255 Unicode characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#tags GoogleContainerAwsNodePool#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def taints(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerAwsNodePoolConfigTaints"]]]:
        '''taints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#taints GoogleContainerAwsNodePool#taints}
        '''
        result = self._values.get("taints")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerAwsNodePoolConfigTaints"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsNodePoolConfigA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAwsNodePoolConfigAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsNodePool.GoogleContainerAwsNodePoolConfigAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d20f7bcb74e6f5f124e61208f1ddafc5b08e342a4b9d5add903c3888bcea7007)
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
        :param granularity: The frequency at which EC2 Auto Scaling sends aggregated data to AWS CloudWatch. The only valid value is "1Minute". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#granularity GoogleContainerAwsNodePool#granularity}
        :param metrics: The metrics to enable. For a list of valid metrics, see https://docs.aws.amazon.com/autoscaling/ec2/APIReference/API_EnableMetricsCollection.html. If you specify granularity and don't specify any metrics, all metrics are enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#metrics GoogleContainerAwsNodePool#metrics}
        '''
        value = GoogleContainerAwsNodePoolConfigAutoscalingMetricsCollection(
            granularity=granularity, metrics=metrics
        )

        return typing.cast(None, jsii.invoke(self, "putAutoscalingMetricsCollection", [value]))

    @jsii.member(jsii_name="putConfigEncryption")
    def put_config_encryption(self, *, kms_key_arn: builtins.str) -> None:
        '''
        :param kms_key_arn: The ARN of the AWS KMS key used to encrypt node pool configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#kms_key_arn GoogleContainerAwsNodePool#kms_key_arn}
        '''
        value = GoogleContainerAwsNodePoolConfigConfigEncryption(
            kms_key_arn=kms_key_arn
        )

        return typing.cast(None, jsii.invoke(self, "putConfigEncryption", [value]))

    @jsii.member(jsii_name="putInstancePlacement")
    def put_instance_placement(
        self,
        *,
        tenancy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param tenancy: The tenancy for the instance. Possible values: TENANCY_UNSPECIFIED, DEFAULT, DEDICATED, HOST. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#tenancy GoogleContainerAwsNodePool#tenancy}
        '''
        value = GoogleContainerAwsNodePoolConfigInstancePlacement(tenancy=tenancy)

        return typing.cast(None, jsii.invoke(self, "putInstancePlacement", [value]))

    @jsii.member(jsii_name="putProxyConfig")
    def put_proxy_config(
        self,
        *,
        secret_arn: builtins.str,
        secret_version: builtins.str,
    ) -> None:
        '''
        :param secret_arn: The ARN of the AWS Secret Manager secret that contains the HTTP(S) proxy configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#secret_arn GoogleContainerAwsNodePool#secret_arn}
        :param secret_version: The version string of the AWS Secret Manager secret that contains the HTTP(S) proxy configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#secret_version GoogleContainerAwsNodePool#secret_version}
        '''
        value = GoogleContainerAwsNodePoolConfigProxyConfig(
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
        :param iops: Optional. The number of I/O operations per second (IOPS) to provision for GP3 volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#iops GoogleContainerAwsNodePool#iops}
        :param kms_key_arn: Optional. The Amazon Resource Name (ARN) of the Customer Managed Key (CMK) used to encrypt AWS EBS volumes. If not specified, the default Amazon managed key associated to the AWS region where this cluster runs will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#kms_key_arn GoogleContainerAwsNodePool#kms_key_arn}
        :param size_gib: Optional. The size of the volume, in GiBs. When unspecified, a default value is provided. See the specific reference in the parent resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#size_gib GoogleContainerAwsNodePool#size_gib}
        :param throughput: Optional. The throughput to provision for the volume, in MiB/s. Only valid if the volume type is GP3. If volume type is gp3 and throughput is not specified, the throughput will defaults to 125. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#throughput GoogleContainerAwsNodePool#throughput}
        :param volume_type: Optional. Type of the EBS volume. When unspecified, it defaults to GP2 volume. Possible values: VOLUME_TYPE_UNSPECIFIED, GP2, GP3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#volume_type GoogleContainerAwsNodePool#volume_type}
        '''
        value = GoogleContainerAwsNodePoolConfigRootVolume(
            iops=iops,
            kms_key_arn=kms_key_arn,
            size_gib=size_gib,
            throughput=throughput,
            volume_type=volume_type,
        )

        return typing.cast(None, jsii.invoke(self, "putRootVolume", [value]))

    @jsii.member(jsii_name="putSpotConfig")
    def put_spot_config(self, *, instance_types: typing.Sequence[builtins.str]) -> None:
        '''
        :param instance_types: List of AWS EC2 instance types for creating a spot node pool's nodes. The specified instance types must have the same number of CPUs and memory. You can use the Amazon EC2 Instance Selector tool (https://github.com/aws/amazon-ec2-instance-selector) to choose instance types with matching CPU and memory Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#instance_types GoogleContainerAwsNodePool#instance_types}
        '''
        value = GoogleContainerAwsNodePoolConfigSpotConfig(
            instance_types=instance_types
        )

        return typing.cast(None, jsii.invoke(self, "putSpotConfig", [value]))

    @jsii.member(jsii_name="putSshConfig")
    def put_ssh_config(self, *, ec2_key_pair: builtins.str) -> None:
        '''
        :param ec2_key_pair: The name of the EC2 key pair used to login into cluster machines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#ec2_key_pair GoogleContainerAwsNodePool#ec2_key_pair}
        '''
        value = GoogleContainerAwsNodePoolConfigSshConfig(ec2_key_pair=ec2_key_pair)

        return typing.cast(None, jsii.invoke(self, "putSshConfig", [value]))

    @jsii.member(jsii_name="putTaints")
    def put_taints(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleContainerAwsNodePoolConfigTaints", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f27817ad1bb1e6dd6515aafda1d873d2d8532a8f90da9c6a1e32212349c8de5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTaints", [value]))

    @jsii.member(jsii_name="resetAutoscalingMetricsCollection")
    def reset_autoscaling_metrics_collection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscalingMetricsCollection", []))

    @jsii.member(jsii_name="resetImageType")
    def reset_image_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageType", []))

    @jsii.member(jsii_name="resetInstancePlacement")
    def reset_instance_placement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstancePlacement", []))

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

    @jsii.member(jsii_name="resetSpotConfig")
    def reset_spot_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpotConfig", []))

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
    ) -> "GoogleContainerAwsNodePoolConfigAutoscalingMetricsCollectionOutputReference":
        return typing.cast("GoogleContainerAwsNodePoolConfigAutoscalingMetricsCollectionOutputReference", jsii.get(self, "autoscalingMetricsCollection"))

    @builtins.property
    @jsii.member(jsii_name="configEncryption")
    def config_encryption(
        self,
    ) -> "GoogleContainerAwsNodePoolConfigConfigEncryptionOutputReference":
        return typing.cast("GoogleContainerAwsNodePoolConfigConfigEncryptionOutputReference", jsii.get(self, "configEncryption"))

    @builtins.property
    @jsii.member(jsii_name="instancePlacement")
    def instance_placement(
        self,
    ) -> "GoogleContainerAwsNodePoolConfigInstancePlacementOutputReference":
        return typing.cast("GoogleContainerAwsNodePoolConfigInstancePlacementOutputReference", jsii.get(self, "instancePlacement"))

    @builtins.property
    @jsii.member(jsii_name="proxyConfig")
    def proxy_config(
        self,
    ) -> "GoogleContainerAwsNodePoolConfigProxyConfigOutputReference":
        return typing.cast("GoogleContainerAwsNodePoolConfigProxyConfigOutputReference", jsii.get(self, "proxyConfig"))

    @builtins.property
    @jsii.member(jsii_name="rootVolume")
    def root_volume(
        self,
    ) -> "GoogleContainerAwsNodePoolConfigRootVolumeOutputReference":
        return typing.cast("GoogleContainerAwsNodePoolConfigRootVolumeOutputReference", jsii.get(self, "rootVolume"))

    @builtins.property
    @jsii.member(jsii_name="spotConfig")
    def spot_config(
        self,
    ) -> "GoogleContainerAwsNodePoolConfigSpotConfigOutputReference":
        return typing.cast("GoogleContainerAwsNodePoolConfigSpotConfigOutputReference", jsii.get(self, "spotConfig"))

    @builtins.property
    @jsii.member(jsii_name="sshConfig")
    def ssh_config(self) -> "GoogleContainerAwsNodePoolConfigSshConfigOutputReference":
        return typing.cast("GoogleContainerAwsNodePoolConfigSshConfigOutputReference", jsii.get(self, "sshConfig"))

    @builtins.property
    @jsii.member(jsii_name="taints")
    def taints(self) -> "GoogleContainerAwsNodePoolConfigTaintsList":
        return typing.cast("GoogleContainerAwsNodePoolConfigTaintsList", jsii.get(self, "taints"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingMetricsCollectionInput")
    def autoscaling_metrics_collection_input(
        self,
    ) -> typing.Optional["GoogleContainerAwsNodePoolConfigAutoscalingMetricsCollection"]:
        return typing.cast(typing.Optional["GoogleContainerAwsNodePoolConfigAutoscalingMetricsCollection"], jsii.get(self, "autoscalingMetricsCollectionInput"))

    @builtins.property
    @jsii.member(jsii_name="configEncryptionInput")
    def config_encryption_input(
        self,
    ) -> typing.Optional["GoogleContainerAwsNodePoolConfigConfigEncryption"]:
        return typing.cast(typing.Optional["GoogleContainerAwsNodePoolConfigConfigEncryption"], jsii.get(self, "configEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="iamInstanceProfileInput")
    def iam_instance_profile_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamInstanceProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="imageTypeInput")
    def image_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="instancePlacementInput")
    def instance_placement_input(
        self,
    ) -> typing.Optional["GoogleContainerAwsNodePoolConfigInstancePlacement"]:
        return typing.cast(typing.Optional["GoogleContainerAwsNodePoolConfigInstancePlacement"], jsii.get(self, "instancePlacementInput"))

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
    ) -> typing.Optional["GoogleContainerAwsNodePoolConfigProxyConfig"]:
        return typing.cast(typing.Optional["GoogleContainerAwsNodePoolConfigProxyConfig"], jsii.get(self, "proxyConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="rootVolumeInput")
    def root_volume_input(
        self,
    ) -> typing.Optional["GoogleContainerAwsNodePoolConfigRootVolume"]:
        return typing.cast(typing.Optional["GoogleContainerAwsNodePoolConfigRootVolume"], jsii.get(self, "rootVolumeInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIdsInput")
    def security_group_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="spotConfigInput")
    def spot_config_input(
        self,
    ) -> typing.Optional["GoogleContainerAwsNodePoolConfigSpotConfig"]:
        return typing.cast(typing.Optional["GoogleContainerAwsNodePoolConfigSpotConfig"], jsii.get(self, "spotConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="sshConfigInput")
    def ssh_config_input(
        self,
    ) -> typing.Optional["GoogleContainerAwsNodePoolConfigSshConfig"]:
        return typing.cast(typing.Optional["GoogleContainerAwsNodePoolConfigSshConfig"], jsii.get(self, "sshConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="taintsInput")
    def taints_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerAwsNodePoolConfigTaints"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerAwsNodePoolConfigTaints"]]], jsii.get(self, "taintsInput"))

    @builtins.property
    @jsii.member(jsii_name="iamInstanceProfile")
    def iam_instance_profile(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "iamInstanceProfile"))

    @iam_instance_profile.setter
    def iam_instance_profile(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10d7eea0deb11451b3439245afa548b8618b5c8181ea5fd09ea1d4ce744bb975)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iamInstanceProfile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageType")
    def image_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageType"))

    @image_type.setter
    def image_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78d5200c536860eccc2b7b372ce5f7a37010c38942cc7faf15b0f07281dee559)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45d93ed7803d2bab3c4a3d021b90e9f817922e52286a5df62795d10695e934ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eccbb82f6c6cb64a091b8f50297b61bc2db2ffda4163b7070a4d49c100f30279)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b95375da2c91603ab85cea7af3a6af7943aed35d14964efaa1f143fdc7de5cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f71799343a12d6198b6f2f54ea06344ca1085d4938a28100faec8ccd44dbebec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleContainerAwsNodePoolConfigA]:
        return typing.cast(typing.Optional[GoogleContainerAwsNodePoolConfigA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAwsNodePoolConfigA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55fa44756d6d54609eee0b7c42be928711f8f68f51afd767ed324de293fc92fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsNodePool.GoogleContainerAwsNodePoolConfigAutoscalingMetricsCollection",
    jsii_struct_bases=[],
    name_mapping={"granularity": "granularity", "metrics": "metrics"},
)
class GoogleContainerAwsNodePoolConfigAutoscalingMetricsCollection:
    def __init__(
        self,
        *,
        granularity: builtins.str,
        metrics: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param granularity: The frequency at which EC2 Auto Scaling sends aggregated data to AWS CloudWatch. The only valid value is "1Minute". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#granularity GoogleContainerAwsNodePool#granularity}
        :param metrics: The metrics to enable. For a list of valid metrics, see https://docs.aws.amazon.com/autoscaling/ec2/APIReference/API_EnableMetricsCollection.html. If you specify granularity and don't specify any metrics, all metrics are enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#metrics GoogleContainerAwsNodePool#metrics}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c6a310a222e5c2443827c7e940d1a6c61b9695aca4c46f65b959326db10f6b0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#granularity GoogleContainerAwsNodePool#granularity}
        '''
        result = self._values.get("granularity")
        assert result is not None, "Required property 'granularity' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metrics(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The metrics to enable.

        For a list of valid metrics, see https://docs.aws.amazon.com/autoscaling/ec2/APIReference/API_EnableMetricsCollection.html. If you specify granularity and don't specify any metrics, all metrics are enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#metrics GoogleContainerAwsNodePool#metrics}
        '''
        result = self._values.get("metrics")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsNodePoolConfigAutoscalingMetricsCollection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAwsNodePoolConfigAutoscalingMetricsCollectionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsNodePool.GoogleContainerAwsNodePoolConfigAutoscalingMetricsCollectionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__19b11fb890112a243cbfac2b5a3dee4dd90c44c33f5b00a1d68797ae00ae6f46)
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
            type_hints = typing.get_type_hints(_typecheckingstub__34efaf0f40d436cd562753296d04b13d455215c8bde0fcab9d6a56d5bf7997f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "granularity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metrics")
    def metrics(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "metrics"))

    @metrics.setter
    def metrics(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb7cedb254878f2b36d00dfecbb206294507b764d66f5cf805d4568d89911cdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metrics", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAwsNodePoolConfigAutoscalingMetricsCollection]:
        return typing.cast(typing.Optional[GoogleContainerAwsNodePoolConfigAutoscalingMetricsCollection], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAwsNodePoolConfigAutoscalingMetricsCollection],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab971127488106a2c22cbb6ee986c45719706d0153cddac31452af82a52808f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsNodePool.GoogleContainerAwsNodePoolConfigConfigEncryption",
    jsii_struct_bases=[],
    name_mapping={"kms_key_arn": "kmsKeyArn"},
)
class GoogleContainerAwsNodePoolConfigConfigEncryption:
    def __init__(self, *, kms_key_arn: builtins.str) -> None:
        '''
        :param kms_key_arn: The ARN of the AWS KMS key used to encrypt node pool configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#kms_key_arn GoogleContainerAwsNodePool#kms_key_arn}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44751e06a51234bdb9ec07a2c29c75399e5a80e5621f21810c17595e77018ae5)
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key_arn": kms_key_arn,
        }

    @builtins.property
    def kms_key_arn(self) -> builtins.str:
        '''The ARN of the AWS KMS key used to encrypt node pool configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#kms_key_arn GoogleContainerAwsNodePool#kms_key_arn}
        '''
        result = self._values.get("kms_key_arn")
        assert result is not None, "Required property 'kms_key_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsNodePoolConfigConfigEncryption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAwsNodePoolConfigConfigEncryptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsNodePool.GoogleContainerAwsNodePoolConfigConfigEncryptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7dfd49ab0622eb369d31ac171c3b2e20a82b35aa7b4ef1ffe8de69171d4a02ce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc6ee7c6a1b9a2bc86d800b180f83118c08047a92a74c47d93f080acd1d5a0df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAwsNodePoolConfigConfigEncryption]:
        return typing.cast(typing.Optional[GoogleContainerAwsNodePoolConfigConfigEncryption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAwsNodePoolConfigConfigEncryption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74ccf81958a90abecb4af31e22ebd358a912105afa782810aa3b2d91dea2e8f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsNodePool.GoogleContainerAwsNodePoolConfigInstancePlacement",
    jsii_struct_bases=[],
    name_mapping={"tenancy": "tenancy"},
)
class GoogleContainerAwsNodePoolConfigInstancePlacement:
    def __init__(self, *, tenancy: typing.Optional[builtins.str] = None) -> None:
        '''
        :param tenancy: The tenancy for the instance. Possible values: TENANCY_UNSPECIFIED, DEFAULT, DEDICATED, HOST. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#tenancy GoogleContainerAwsNodePool#tenancy}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65743764906c4739267ad2b9273d92c269ad96d06169c1b359810066533c638f)
            check_type(argname="argument tenancy", value=tenancy, expected_type=type_hints["tenancy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if tenancy is not None:
            self._values["tenancy"] = tenancy

    @builtins.property
    def tenancy(self) -> typing.Optional[builtins.str]:
        '''The tenancy for the instance. Possible values: TENANCY_UNSPECIFIED, DEFAULT, DEDICATED, HOST.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#tenancy GoogleContainerAwsNodePool#tenancy}
        '''
        result = self._values.get("tenancy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsNodePoolConfigInstancePlacement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAwsNodePoolConfigInstancePlacementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsNodePool.GoogleContainerAwsNodePoolConfigInstancePlacementOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6345203dedef3a64a16e825ce847d6aa5db85214fade93337fda066b0a2b4ee5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTenancy")
    def reset_tenancy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTenancy", []))

    @builtins.property
    @jsii.member(jsii_name="tenancyInput")
    def tenancy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenancyInput"))

    @builtins.property
    @jsii.member(jsii_name="tenancy")
    def tenancy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenancy"))

    @tenancy.setter
    def tenancy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c953a7d5f6a80dda3888daaa1b6b4be27dc4207379a46a3855f3d1b2e0c4d59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenancy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAwsNodePoolConfigInstancePlacement]:
        return typing.cast(typing.Optional[GoogleContainerAwsNodePoolConfigInstancePlacement], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAwsNodePoolConfigInstancePlacement],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2dbde65605453b4613f67ea17f1a7f41db7b553554858161e70f973edb432a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsNodePool.GoogleContainerAwsNodePoolConfigProxyConfig",
    jsii_struct_bases=[],
    name_mapping={"secret_arn": "secretArn", "secret_version": "secretVersion"},
)
class GoogleContainerAwsNodePoolConfigProxyConfig:
    def __init__(
        self,
        *,
        secret_arn: builtins.str,
        secret_version: builtins.str,
    ) -> None:
        '''
        :param secret_arn: The ARN of the AWS Secret Manager secret that contains the HTTP(S) proxy configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#secret_arn GoogleContainerAwsNodePool#secret_arn}
        :param secret_version: The version string of the AWS Secret Manager secret that contains the HTTP(S) proxy configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#secret_version GoogleContainerAwsNodePool#secret_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb3e9d54afbcdabc01ad27c5984aecfeea65de82810286fcae1c5f7f3fd6a3e6)
            check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_arn": secret_arn,
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_arn(self) -> builtins.str:
        '''The ARN of the AWS Secret Manager secret that contains the HTTP(S) proxy configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#secret_arn GoogleContainerAwsNodePool#secret_arn}
        '''
        result = self._values.get("secret_arn")
        assert result is not None, "Required property 'secret_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''The version string of the AWS Secret Manager secret that contains the HTTP(S) proxy configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#secret_version GoogleContainerAwsNodePool#secret_version}
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsNodePoolConfigProxyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAwsNodePoolConfigProxyConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsNodePool.GoogleContainerAwsNodePoolConfigProxyConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbee8e39ca8d1bef1ad96b935a02123eda6264864103a2559f746a61ced40f21)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b090503af96be3ee2466245793edf1da47fc2c75f17cfea534190f0165cfbb1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretVersion")
    def secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersion"))

    @secret_version.setter
    def secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d7867aa830fa74383574a799e17182c7c9e98bc7329bf25ed6999959dbc678c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAwsNodePoolConfigProxyConfig]:
        return typing.cast(typing.Optional[GoogleContainerAwsNodePoolConfigProxyConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAwsNodePoolConfigProxyConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34ba60ebc8a2d9a98ef8238bc7c387a7580f25df44e7de73151d4a4b7aced411)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsNodePool.GoogleContainerAwsNodePoolConfigRootVolume",
    jsii_struct_bases=[],
    name_mapping={
        "iops": "iops",
        "kms_key_arn": "kmsKeyArn",
        "size_gib": "sizeGib",
        "throughput": "throughput",
        "volume_type": "volumeType",
    },
)
class GoogleContainerAwsNodePoolConfigRootVolume:
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
        :param iops: Optional. The number of I/O operations per second (IOPS) to provision for GP3 volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#iops GoogleContainerAwsNodePool#iops}
        :param kms_key_arn: Optional. The Amazon Resource Name (ARN) of the Customer Managed Key (CMK) used to encrypt AWS EBS volumes. If not specified, the default Amazon managed key associated to the AWS region where this cluster runs will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#kms_key_arn GoogleContainerAwsNodePool#kms_key_arn}
        :param size_gib: Optional. The size of the volume, in GiBs. When unspecified, a default value is provided. See the specific reference in the parent resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#size_gib GoogleContainerAwsNodePool#size_gib}
        :param throughput: Optional. The throughput to provision for the volume, in MiB/s. Only valid if the volume type is GP3. If volume type is gp3 and throughput is not specified, the throughput will defaults to 125. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#throughput GoogleContainerAwsNodePool#throughput}
        :param volume_type: Optional. Type of the EBS volume. When unspecified, it defaults to GP2 volume. Possible values: VOLUME_TYPE_UNSPECIFIED, GP2, GP3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#volume_type GoogleContainerAwsNodePool#volume_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__783c91779958eeeabecd7f9f1458dc78903e4d826e84b7335a42a68a33a80a1f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#iops GoogleContainerAwsNodePool#iops}
        '''
        result = self._values.get("iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The Amazon Resource Name (ARN) of the Customer Managed Key (CMK) used to encrypt AWS EBS volumes. If not specified, the default Amazon managed key associated to the AWS region where this cluster runs will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#kms_key_arn GoogleContainerAwsNodePool#kms_key_arn}
        '''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def size_gib(self) -> typing.Optional[jsii.Number]:
        '''Optional.

        The size of the volume, in GiBs. When unspecified, a default value is provided. See the specific reference in the parent resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#size_gib GoogleContainerAwsNodePool#size_gib}
        '''
        result = self._values.get("size_gib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def throughput(self) -> typing.Optional[jsii.Number]:
        '''Optional.

        The throughput to provision for the volume, in MiB/s. Only valid if the volume type is GP3. If volume type is gp3 and throughput is not specified, the throughput will defaults to 125.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#throughput GoogleContainerAwsNodePool#throughput}
        '''
        result = self._values.get("throughput")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def volume_type(self) -> typing.Optional[builtins.str]:
        '''Optional. Type of the EBS volume. When unspecified, it defaults to GP2 volume. Possible values: VOLUME_TYPE_UNSPECIFIED, GP2, GP3.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#volume_type GoogleContainerAwsNodePool#volume_type}
        '''
        result = self._values.get("volume_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsNodePoolConfigRootVolume(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAwsNodePoolConfigRootVolumeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsNodePool.GoogleContainerAwsNodePoolConfigRootVolumeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d552b90bf4cd3b8cdf940c5cf4751da34b5cd6ca54be28026430ccc608a818e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b912a8e9ce863a8e10c8cfcda45e67bf9517b59025eb8fb1e42e75f042ada064)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iops", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArn")
    def kms_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyArn"))

    @kms_key_arn.setter
    def kms_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bc364273c4ecbcb6542296f8dc246e44ff4d26daedcdd27039907bb65b78ead)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sizeGib")
    def size_gib(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeGib"))

    @size_gib.setter
    def size_gib(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__872b6bce32a1598d675eb81a19efc2f8d468a73e91fa184c34e5440695013207)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeGib", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="throughput")
    def throughput(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "throughput"))

    @throughput.setter
    def throughput(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ac241a88b7920cb6143dc457c378b630fc8ef067e5631277a8e519053c752aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throughput", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeType")
    def volume_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeType"))

    @volume_type.setter
    def volume_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9993fbb8645f816d4cbde0585a4fd06a40b4c87f10552baa851cc683f2efa751)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAwsNodePoolConfigRootVolume]:
        return typing.cast(typing.Optional[GoogleContainerAwsNodePoolConfigRootVolume], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAwsNodePoolConfigRootVolume],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dcfd05727fb071c581731dad22ec5b3c1f4fba7aaa050e74c2c99f910e2548c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsNodePool.GoogleContainerAwsNodePoolConfigSpotConfig",
    jsii_struct_bases=[],
    name_mapping={"instance_types": "instanceTypes"},
)
class GoogleContainerAwsNodePoolConfigSpotConfig:
    def __init__(self, *, instance_types: typing.Sequence[builtins.str]) -> None:
        '''
        :param instance_types: List of AWS EC2 instance types for creating a spot node pool's nodes. The specified instance types must have the same number of CPUs and memory. You can use the Amazon EC2 Instance Selector tool (https://github.com/aws/amazon-ec2-instance-selector) to choose instance types with matching CPU and memory Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#instance_types GoogleContainerAwsNodePool#instance_types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d79acb0bda8c99e380c7b8b96c86d9ad804c703c3deb0a0b68f28b5227dc9222)
            check_type(argname="argument instance_types", value=instance_types, expected_type=type_hints["instance_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_types": instance_types,
        }

    @builtins.property
    def instance_types(self) -> typing.List[builtins.str]:
        '''List of AWS EC2 instance types for creating a spot node pool's nodes.

        The specified instance types must have the same number of CPUs and memory. You can use the Amazon EC2 Instance Selector tool (https://github.com/aws/amazon-ec2-instance-selector) to choose instance types with matching CPU and memory

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#instance_types GoogleContainerAwsNodePool#instance_types}
        '''
        result = self._values.get("instance_types")
        assert result is not None, "Required property 'instance_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsNodePoolConfigSpotConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAwsNodePoolConfigSpotConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsNodePool.GoogleContainerAwsNodePoolConfigSpotConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__817322f813ccfcb8355e9544d6b03db12415513d590b93116717d18b2a64bd70)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="instanceTypesInput")
    def instance_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "instanceTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceTypes")
    def instance_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "instanceTypes"))

    @instance_types.setter
    def instance_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dd48adfa8cbe193f8f39123ba8fdb0246ca9e770f0f40d51ad5fcaebc6e7b31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAwsNodePoolConfigSpotConfig]:
        return typing.cast(typing.Optional[GoogleContainerAwsNodePoolConfigSpotConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAwsNodePoolConfigSpotConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7730e81627e5c875b5991bb0762cc8b62b98b2088fc38eab7c49206f40e3b945)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsNodePool.GoogleContainerAwsNodePoolConfigSshConfig",
    jsii_struct_bases=[],
    name_mapping={"ec2_key_pair": "ec2KeyPair"},
)
class GoogleContainerAwsNodePoolConfigSshConfig:
    def __init__(self, *, ec2_key_pair: builtins.str) -> None:
        '''
        :param ec2_key_pair: The name of the EC2 key pair used to login into cluster machines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#ec2_key_pair GoogleContainerAwsNodePool#ec2_key_pair}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21c9fe029acee88e648e56328f9ba639331dffc730a10469319b3840cb614134)
            check_type(argname="argument ec2_key_pair", value=ec2_key_pair, expected_type=type_hints["ec2_key_pair"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ec2_key_pair": ec2_key_pair,
        }

    @builtins.property
    def ec2_key_pair(self) -> builtins.str:
        '''The name of the EC2 key pair used to login into cluster machines.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#ec2_key_pair GoogleContainerAwsNodePool#ec2_key_pair}
        '''
        result = self._values.get("ec2_key_pair")
        assert result is not None, "Required property 'ec2_key_pair' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsNodePoolConfigSshConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAwsNodePoolConfigSshConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsNodePool.GoogleContainerAwsNodePoolConfigSshConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d09774ac5f5f43352fc8640fc91474c0ead1b1c407a66c5aced0ed9cc148e950)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e7d60c6f8c36473add4cf4faf3d94427f20f8fbb802c93945dd466b103e546d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ec2KeyPair", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAwsNodePoolConfigSshConfig]:
        return typing.cast(typing.Optional[GoogleContainerAwsNodePoolConfigSshConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAwsNodePoolConfigSshConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7222bb1c71c8569d8bccd3cf9e79d74f7dcc730f96e50fb55127040bcf016a16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsNodePool.GoogleContainerAwsNodePoolConfigTaints",
    jsii_struct_bases=[],
    name_mapping={"effect": "effect", "key": "key", "value": "value"},
)
class GoogleContainerAwsNodePoolConfigTaints:
    def __init__(
        self,
        *,
        effect: builtins.str,
        key: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param effect: The taint effect. Possible values: EFFECT_UNSPECIFIED, NO_SCHEDULE, PREFER_NO_SCHEDULE, NO_EXECUTE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#effect GoogleContainerAwsNodePool#effect}
        :param key: Key for the taint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#key GoogleContainerAwsNodePool#key}
        :param value: Value for the taint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#value GoogleContainerAwsNodePool#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1137e3fe11dfea2a29f80250a138b8d4262116bc0ed19fd78032bd7e4bf1368a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#effect GoogleContainerAwsNodePool#effect}
        '''
        result = self._values.get("effect")
        assert result is not None, "Required property 'effect' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''Key for the taint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#key GoogleContainerAwsNodePool#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Value for the taint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#value GoogleContainerAwsNodePool#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsNodePoolConfigTaints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAwsNodePoolConfigTaintsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsNodePool.GoogleContainerAwsNodePoolConfigTaintsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6760f7c7a8c2a5e637f57164a409bb542bc1c7a87c18f6a2be06338ca0e9eed2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleContainerAwsNodePoolConfigTaintsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a26fd21857fafcb528b0f85ba1500433b879b32e9f8c9a0dec4257feab4184c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleContainerAwsNodePoolConfigTaintsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__964b5f48dfbaa679ec8057a66f3b913ba1fdd955cdbea11542989ee61ee94e79)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2316d7c5b85e15962bb597b1ec996169db41791ef904b9ef7c7007344eb3a7cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aaec36b9ae18f811e1668240237f9c02d82cb44385bc4831b1cbb41a0fb34a2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerAwsNodePoolConfigTaints]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerAwsNodePoolConfigTaints]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerAwsNodePoolConfigTaints]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6946782c3fb36619152e148682a8486004ae5375cecb1854635913be7752d614)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleContainerAwsNodePoolConfigTaintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsNodePool.GoogleContainerAwsNodePoolConfigTaintsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2dcc67ffacd036731c278914d9a47515ac58f4c97c742c57c69aae1fd4a006f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__410bd0ba9646e6a2ac79c18ca03dd15e727ec821b20fe8c61147640fc0a75efa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b6ac5ccc21646234f5f31ec4fbc240c0687f1ddbedfafd3957cc4d633390ea8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5f028450ae4a109981369c92b0b09f53fb562d2ac19a675ab4003dbd483e23e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAwsNodePoolConfigTaints]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAwsNodePoolConfigTaints]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAwsNodePoolConfigTaints]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5718aa5890e80d446f2ccf47d2290613812bf18d7a88c78b08674a74a354215b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsNodePool.GoogleContainerAwsNodePoolKubeletConfig",
    jsii_struct_bases=[],
    name_mapping={
        "cpu_cfs_quota": "cpuCfsQuota",
        "cpu_cfs_quota_period": "cpuCfsQuotaPeriod",
        "cpu_manager_policy": "cpuManagerPolicy",
        "pod_pids_limit": "podPidsLimit",
    },
)
class GoogleContainerAwsNodePoolKubeletConfig:
    def __init__(
        self,
        *,
        cpu_cfs_quota: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cpu_cfs_quota_period: typing.Optional[builtins.str] = None,
        cpu_manager_policy: typing.Optional[builtins.str] = None,
        pod_pids_limit: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cpu_cfs_quota: Whether or not to enable CPU CFS quota. Defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#cpu_cfs_quota GoogleContainerAwsNodePool#cpu_cfs_quota}
        :param cpu_cfs_quota_period: Optional. The CPU CFS quota period to use for the node. Defaults to "100ms". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#cpu_cfs_quota_period GoogleContainerAwsNodePool#cpu_cfs_quota_period}
        :param cpu_manager_policy: The CpuManagerPolicy to use for the node. Defaults to "none". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#cpu_manager_policy GoogleContainerAwsNodePool#cpu_manager_policy}
        :param pod_pids_limit: Optional. The maximum number of PIDs in each pod running on the node. The limit scales automatically based on underlying machine size if left unset. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#pod_pids_limit GoogleContainerAwsNodePool#pod_pids_limit}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c6fcba6a683011c7dc5e198ea33a26a3d595cd88be0d03ba6d0031c23550b3b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#cpu_cfs_quota GoogleContainerAwsNodePool#cpu_cfs_quota}
        '''
        result = self._values.get("cpu_cfs_quota")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def cpu_cfs_quota_period(self) -> typing.Optional[builtins.str]:
        '''Optional. The CPU CFS quota period to use for the node. Defaults to "100ms".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#cpu_cfs_quota_period GoogleContainerAwsNodePool#cpu_cfs_quota_period}
        '''
        result = self._values.get("cpu_cfs_quota_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu_manager_policy(self) -> typing.Optional[builtins.str]:
        '''The CpuManagerPolicy to use for the node. Defaults to "none".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#cpu_manager_policy GoogleContainerAwsNodePool#cpu_manager_policy}
        '''
        result = self._values.get("cpu_manager_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pod_pids_limit(self) -> typing.Optional[jsii.Number]:
        '''Optional.

        The maximum number of PIDs in each pod running on the node. The limit scales automatically based on underlying machine size if left unset.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#pod_pids_limit GoogleContainerAwsNodePool#pod_pids_limit}
        '''
        result = self._values.get("pod_pids_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsNodePoolKubeletConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAwsNodePoolKubeletConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsNodePool.GoogleContainerAwsNodePoolKubeletConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c85e7e0df00dd252272638dfe8d02d8ad756fda72417db857dcd935e4b7f13f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca50f687626a2e8e8c0a0cf4e53c52113adc0bea082b7d4b16033a82e6e3db6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuCfsQuota", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpuCfsQuotaPeriod")
    def cpu_cfs_quota_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpuCfsQuotaPeriod"))

    @cpu_cfs_quota_period.setter
    def cpu_cfs_quota_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c90db0c1ec64fea935b7a9a7f4e71a99593f307c8e9a6843af505b84ac700f7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuCfsQuotaPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpuManagerPolicy")
    def cpu_manager_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpuManagerPolicy"))

    @cpu_manager_policy.setter
    def cpu_manager_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0688de8ddef32ec14ff3f79cba419b782d6b20c9d4a3085691fc8be257eb2ce6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuManagerPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="podPidsLimit")
    def pod_pids_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "podPidsLimit"))

    @pod_pids_limit.setter
    def pod_pids_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10f819e7f04ce173244f3e9ae32f90e7cfa346082735940091c021eba6f38b9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podPidsLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAwsNodePoolKubeletConfig]:
        return typing.cast(typing.Optional[GoogleContainerAwsNodePoolKubeletConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAwsNodePoolKubeletConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a02b5f3220839127f536de7a5381b55fa8487fc57bb25c1b3dfb5fde370724f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsNodePool.GoogleContainerAwsNodePoolManagement",
    jsii_struct_bases=[],
    name_mapping={"auto_repair": "autoRepair"},
)
class GoogleContainerAwsNodePoolManagement:
    def __init__(
        self,
        *,
        auto_repair: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param auto_repair: Optional. Whether or not the nodes will be automatically repaired. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#auto_repair GoogleContainerAwsNodePool#auto_repair}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d41c51def1c9b9cb772c4c052e00d510c1e67a2968853b5642dad11e378cdaa)
            check_type(argname="argument auto_repair", value=auto_repair, expected_type=type_hints["auto_repair"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_repair is not None:
            self._values["auto_repair"] = auto_repair

    @builtins.property
    def auto_repair(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. Whether or not the nodes will be automatically repaired.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#auto_repair GoogleContainerAwsNodePool#auto_repair}
        '''
        result = self._values.get("auto_repair")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsNodePoolManagement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAwsNodePoolManagementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsNodePool.GoogleContainerAwsNodePoolManagementOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8aaaa71ac955bd6fff5433c7970484df49bc01df931abce39eb021b8799d693f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e947df660188d2c9962c03beef7d81a71235c7c0141020dfcfccf8a1429c8c21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoRepair", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleContainerAwsNodePoolManagement]:
        return typing.cast(typing.Optional[GoogleContainerAwsNodePoolManagement], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAwsNodePoolManagement],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2b763afebc62fa4b16a53b684dbb42e9e13d21ea807e5de1c9fd4fd96131140)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsNodePool.GoogleContainerAwsNodePoolMaxPodsConstraint",
    jsii_struct_bases=[],
    name_mapping={"max_pods_per_node": "maxPodsPerNode"},
)
class GoogleContainerAwsNodePoolMaxPodsConstraint:
    def __init__(self, *, max_pods_per_node: jsii.Number) -> None:
        '''
        :param max_pods_per_node: The maximum number of pods to schedule on a single node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#max_pods_per_node GoogleContainerAwsNodePool#max_pods_per_node}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4045f177bea59651dfba41675eaf4e4a27f91275fb185b764a840e29d81fc61a)
            check_type(argname="argument max_pods_per_node", value=max_pods_per_node, expected_type=type_hints["max_pods_per_node"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_pods_per_node": max_pods_per_node,
        }

    @builtins.property
    def max_pods_per_node(self) -> jsii.Number:
        '''The maximum number of pods to schedule on a single node.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#max_pods_per_node GoogleContainerAwsNodePool#max_pods_per_node}
        '''
        result = self._values.get("max_pods_per_node")
        assert result is not None, "Required property 'max_pods_per_node' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsNodePoolMaxPodsConstraint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAwsNodePoolMaxPodsConstraintOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsNodePool.GoogleContainerAwsNodePoolMaxPodsConstraintOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d73552b932b4328e5d2560ec2793b2570500c56168dd17ea839e2d414363508)
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
            type_hints = typing.get_type_hints(_typecheckingstub__02d017cad1ecce9ee2f61ddf21665407ccf88dba96b0f8d2e7fba77dfaf42088)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPodsPerNode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAwsNodePoolMaxPodsConstraint]:
        return typing.cast(typing.Optional[GoogleContainerAwsNodePoolMaxPodsConstraint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAwsNodePoolMaxPodsConstraint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba3b43a7e2947222e3cd47ef2b0b942dd84e341a6e311db490c1c6edaae54e09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsNodePool.GoogleContainerAwsNodePoolTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleContainerAwsNodePoolTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#create GoogleContainerAwsNodePool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#delete GoogleContainerAwsNodePool#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#update GoogleContainerAwsNodePool#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aa7371b68cd6d6f48d6c825ee9f8cb2257ff97a262864aa56a422d3a7c339f9)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#create GoogleContainerAwsNodePool#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#delete GoogleContainerAwsNodePool#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#update GoogleContainerAwsNodePool#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsNodePoolTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAwsNodePoolTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsNodePool.GoogleContainerAwsNodePoolTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7526e4f6dbf8e9674fcccb52177ab0c6c0e2984e790367c253166ae43d590e42)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ab609eb1ef5229f03e8896133456f27c6a4440518f225c6679040a16f6ae777)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d04206865d8a984c13a71e5d12f7a0d050da4841b39f9666c993c8e8b224435d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__388b87d149a60ec0d04d3ef8467722d4e00eaa1d33829e3a2d096245d63aae29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAwsNodePoolTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAwsNodePoolTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAwsNodePoolTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d904f89d36fd7cd975f7aea1f392768de5e4acc8f82c52a4d7a4447d84460143)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsNodePool.GoogleContainerAwsNodePoolUpdateSettings",
    jsii_struct_bases=[],
    name_mapping={"surge_settings": "surgeSettings"},
)
class GoogleContainerAwsNodePoolUpdateSettings:
    def __init__(
        self,
        *,
        surge_settings: typing.Optional[typing.Union["GoogleContainerAwsNodePoolUpdateSettingsSurgeSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param surge_settings: surge_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#surge_settings GoogleContainerAwsNodePool#surge_settings}
        '''
        if isinstance(surge_settings, dict):
            surge_settings = GoogleContainerAwsNodePoolUpdateSettingsSurgeSettings(**surge_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efda28a0dfe089277543fbf7b71f93cb26258e384ab3eec1552651ab16055f61)
            check_type(argname="argument surge_settings", value=surge_settings, expected_type=type_hints["surge_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if surge_settings is not None:
            self._values["surge_settings"] = surge_settings

    @builtins.property
    def surge_settings(
        self,
    ) -> typing.Optional["GoogleContainerAwsNodePoolUpdateSettingsSurgeSettings"]:
        '''surge_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#surge_settings GoogleContainerAwsNodePool#surge_settings}
        '''
        result = self._values.get("surge_settings")
        return typing.cast(typing.Optional["GoogleContainerAwsNodePoolUpdateSettingsSurgeSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsNodePoolUpdateSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAwsNodePoolUpdateSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsNodePool.GoogleContainerAwsNodePoolUpdateSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5842edb2440cde6f9d7feddd8aa224b8b92193b5e17c0dd2242cd8982809753a)
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
        :param max_surge: Optional. The maximum number of nodes that can be created beyond the current size of the node pool during the update process. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#max_surge GoogleContainerAwsNodePool#max_surge}
        :param max_unavailable: Optional. The maximum number of nodes that can be simultaneously unavailable during the update process. A node is considered unavailable if its status is not Ready. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#max_unavailable GoogleContainerAwsNodePool#max_unavailable}
        '''
        value = GoogleContainerAwsNodePoolUpdateSettingsSurgeSettings(
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
    ) -> "GoogleContainerAwsNodePoolUpdateSettingsSurgeSettingsOutputReference":
        return typing.cast("GoogleContainerAwsNodePoolUpdateSettingsSurgeSettingsOutputReference", jsii.get(self, "surgeSettings"))

    @builtins.property
    @jsii.member(jsii_name="surgeSettingsInput")
    def surge_settings_input(
        self,
    ) -> typing.Optional["GoogleContainerAwsNodePoolUpdateSettingsSurgeSettings"]:
        return typing.cast(typing.Optional["GoogleContainerAwsNodePoolUpdateSettingsSurgeSettings"], jsii.get(self, "surgeSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAwsNodePoolUpdateSettings]:
        return typing.cast(typing.Optional[GoogleContainerAwsNodePoolUpdateSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAwsNodePoolUpdateSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d6087764d3b86e6a7caf76ffbdf7ba8c617d958588528a70117f387db1857f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsNodePool.GoogleContainerAwsNodePoolUpdateSettingsSurgeSettings",
    jsii_struct_bases=[],
    name_mapping={"max_surge": "maxSurge", "max_unavailable": "maxUnavailable"},
)
class GoogleContainerAwsNodePoolUpdateSettingsSurgeSettings:
    def __init__(
        self,
        *,
        max_surge: typing.Optional[jsii.Number] = None,
        max_unavailable: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_surge: Optional. The maximum number of nodes that can be created beyond the current size of the node pool during the update process. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#max_surge GoogleContainerAwsNodePool#max_surge}
        :param max_unavailable: Optional. The maximum number of nodes that can be simultaneously unavailable during the update process. A node is considered unavailable if its status is not Ready. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#max_unavailable GoogleContainerAwsNodePool#max_unavailable}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__604266ffa6c56f9acedd4928001ede1b48b16674e76ef92c41e5e7629c638f75)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#max_surge GoogleContainerAwsNodePool#max_surge}
        '''
        result = self._values.get("max_surge")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_unavailable(self) -> typing.Optional[jsii.Number]:
        '''Optional.

        The maximum number of nodes that can be simultaneously unavailable during the update process. A node is considered unavailable if its status is not Ready.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_node_pool#max_unavailable GoogleContainerAwsNodePool#max_unavailable}
        '''
        result = self._values.get("max_unavailable")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsNodePoolUpdateSettingsSurgeSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAwsNodePoolUpdateSettingsSurgeSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsNodePool.GoogleContainerAwsNodePoolUpdateSettingsSurgeSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f5a331494ec7cff0acaa3119578d6a28de04d449af04ce97c27b00a1e5c5fcf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7539e6f113e9833d5553740ccece13b0ae63fc6f7a5bfe37677110e9f2517c41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxSurge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxUnavailable")
    def max_unavailable(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxUnavailable"))

    @max_unavailable.setter
    def max_unavailable(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98f7e8785ed54234f17e692501200000e037c673cb89b771e6d01e69ebcd28fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxUnavailable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAwsNodePoolUpdateSettingsSurgeSettings]:
        return typing.cast(typing.Optional[GoogleContainerAwsNodePoolUpdateSettingsSurgeSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAwsNodePoolUpdateSettingsSurgeSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18d7f6ad04a3b1cc295cb2ed49f675ce50c3fbc45c1a4668f6af32025f16a684)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleContainerAwsNodePool",
    "GoogleContainerAwsNodePoolAutoscaling",
    "GoogleContainerAwsNodePoolAutoscalingOutputReference",
    "GoogleContainerAwsNodePoolConfig",
    "GoogleContainerAwsNodePoolConfigA",
    "GoogleContainerAwsNodePoolConfigAOutputReference",
    "GoogleContainerAwsNodePoolConfigAutoscalingMetricsCollection",
    "GoogleContainerAwsNodePoolConfigAutoscalingMetricsCollectionOutputReference",
    "GoogleContainerAwsNodePoolConfigConfigEncryption",
    "GoogleContainerAwsNodePoolConfigConfigEncryptionOutputReference",
    "GoogleContainerAwsNodePoolConfigInstancePlacement",
    "GoogleContainerAwsNodePoolConfigInstancePlacementOutputReference",
    "GoogleContainerAwsNodePoolConfigProxyConfig",
    "GoogleContainerAwsNodePoolConfigProxyConfigOutputReference",
    "GoogleContainerAwsNodePoolConfigRootVolume",
    "GoogleContainerAwsNodePoolConfigRootVolumeOutputReference",
    "GoogleContainerAwsNodePoolConfigSpotConfig",
    "GoogleContainerAwsNodePoolConfigSpotConfigOutputReference",
    "GoogleContainerAwsNodePoolConfigSshConfig",
    "GoogleContainerAwsNodePoolConfigSshConfigOutputReference",
    "GoogleContainerAwsNodePoolConfigTaints",
    "GoogleContainerAwsNodePoolConfigTaintsList",
    "GoogleContainerAwsNodePoolConfigTaintsOutputReference",
    "GoogleContainerAwsNodePoolKubeletConfig",
    "GoogleContainerAwsNodePoolKubeletConfigOutputReference",
    "GoogleContainerAwsNodePoolManagement",
    "GoogleContainerAwsNodePoolManagementOutputReference",
    "GoogleContainerAwsNodePoolMaxPodsConstraint",
    "GoogleContainerAwsNodePoolMaxPodsConstraintOutputReference",
    "GoogleContainerAwsNodePoolTimeouts",
    "GoogleContainerAwsNodePoolTimeoutsOutputReference",
    "GoogleContainerAwsNodePoolUpdateSettings",
    "GoogleContainerAwsNodePoolUpdateSettingsOutputReference",
    "GoogleContainerAwsNodePoolUpdateSettingsSurgeSettings",
    "GoogleContainerAwsNodePoolUpdateSettingsSurgeSettingsOutputReference",
]

publication.publish()

def _typecheckingstub__73268889630ec5b4031758b2c1d6456cac78ae83b91587693542dfc7ce1f1c98(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    autoscaling: typing.Union[GoogleContainerAwsNodePoolAutoscaling, typing.Dict[builtins.str, typing.Any]],
    cluster: builtins.str,
    config: typing.Union[GoogleContainerAwsNodePoolConfigA, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    max_pods_constraint: typing.Union[GoogleContainerAwsNodePoolMaxPodsConstraint, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    subnet_id: builtins.str,
    version: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    kubelet_config: typing.Optional[typing.Union[GoogleContainerAwsNodePoolKubeletConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    management: typing.Optional[typing.Union[GoogleContainerAwsNodePoolManagement, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleContainerAwsNodePoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    update_settings: typing.Optional[typing.Union[GoogleContainerAwsNodePoolUpdateSettings, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__35c9c515416140be74e3fca3551a5c9615e094a62cf19e040233d2dc6c1bf355(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__883fb559698c2eee78a4b89d5204b6a31a740a4cb0845868e6737489df035920(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f8c0c771d2fb88b6b02916ab8eedf52a031736ad723affcf4f281fc116f699b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18b45b3fced8214e8c62ff3a4efe1d342950659ae20d2b1e87ca4dc8be98d19f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40c97904e5372247d234f0c93fb3aff8f75f3f32551d3ee09001e0bba5438504(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00d2128ac593c3291157343ec6e55c1579693ddccbf452f947db0f46c0e8cfb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfadb76dc755a180864f38024f923cda11b4112a0a0364a584434b251489ad85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afd79c50160434b57f71aa6e7e5ee6c1385f20d5bcc73ab71078a80fdfa20c2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1d7a6ebbda3398a895e7e4a89f1827204e3ecff1adcc3b71dacae9aabb78fd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd9ebde0d630ce4b5d4c12505bfce75c8a94b2425ed454c175b0281ec8b9838b(
    *,
    max_node_count: jsii.Number,
    min_node_count: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bf1e49f248e13374a8810770ee58bc7bdb84fb5b1280414afa4a1b2922fd8b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44e6865a72c154904711e904eb93d33cbcc9ee1654b73f38834a288013e77eca(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc5b3bc0c7483038e5cab8d5ad02811d3d9ef3c607941114521b04f279185fc5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4e3221d2f834b30f72dc0b1455b98f90897b282d43d414460683c859fd063e1(
    value: typing.Optional[GoogleContainerAwsNodePoolAutoscaling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1cdad113338b09deb183284d28c9b5083f150881d6eb4e850555a3eadff602b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    autoscaling: typing.Union[GoogleContainerAwsNodePoolAutoscaling, typing.Dict[builtins.str, typing.Any]],
    cluster: builtins.str,
    config: typing.Union[GoogleContainerAwsNodePoolConfigA, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    max_pods_constraint: typing.Union[GoogleContainerAwsNodePoolMaxPodsConstraint, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    subnet_id: builtins.str,
    version: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    kubelet_config: typing.Optional[typing.Union[GoogleContainerAwsNodePoolKubeletConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    management: typing.Optional[typing.Union[GoogleContainerAwsNodePoolManagement, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleContainerAwsNodePoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    update_settings: typing.Optional[typing.Union[GoogleContainerAwsNodePoolUpdateSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1954e141c98bcaf9353b75ace200e5b3741e9a1e038db6b8c4cbad9f6efe1513(
    *,
    config_encryption: typing.Union[GoogleContainerAwsNodePoolConfigConfigEncryption, typing.Dict[builtins.str, typing.Any]],
    iam_instance_profile: builtins.str,
    autoscaling_metrics_collection: typing.Optional[typing.Union[GoogleContainerAwsNodePoolConfigAutoscalingMetricsCollection, typing.Dict[builtins.str, typing.Any]]] = None,
    image_type: typing.Optional[builtins.str] = None,
    instance_placement: typing.Optional[typing.Union[GoogleContainerAwsNodePoolConfigInstancePlacement, typing.Dict[builtins.str, typing.Any]]] = None,
    instance_type: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    proxy_config: typing.Optional[typing.Union[GoogleContainerAwsNodePoolConfigProxyConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    root_volume: typing.Optional[typing.Union[GoogleContainerAwsNodePoolConfigRootVolume, typing.Dict[builtins.str, typing.Any]]] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    spot_config: typing.Optional[typing.Union[GoogleContainerAwsNodePoolConfigSpotConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ssh_config: typing.Optional[typing.Union[GoogleContainerAwsNodePoolConfigSshConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerAwsNodePoolConfigTaints, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d20f7bcb74e6f5f124e61208f1ddafc5b08e342a4b9d5add903c3888bcea7007(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f27817ad1bb1e6dd6515aafda1d873d2d8532a8f90da9c6a1e32212349c8de5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerAwsNodePoolConfigTaints, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10d7eea0deb11451b3439245afa548b8618b5c8181ea5fd09ea1d4ce744bb975(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78d5200c536860eccc2b7b372ce5f7a37010c38942cc7faf15b0f07281dee559(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45d93ed7803d2bab3c4a3d021b90e9f817922e52286a5df62795d10695e934ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eccbb82f6c6cb64a091b8f50297b61bc2db2ffda4163b7070a4d49c100f30279(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b95375da2c91603ab85cea7af3a6af7943aed35d14964efaa1f143fdc7de5cc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f71799343a12d6198b6f2f54ea06344ca1085d4938a28100faec8ccd44dbebec(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55fa44756d6d54609eee0b7c42be928711f8f68f51afd767ed324de293fc92fc(
    value: typing.Optional[GoogleContainerAwsNodePoolConfigA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c6a310a222e5c2443827c7e940d1a6c61b9695aca4c46f65b959326db10f6b0(
    *,
    granularity: builtins.str,
    metrics: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19b11fb890112a243cbfac2b5a3dee4dd90c44c33f5b00a1d68797ae00ae6f46(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34efaf0f40d436cd562753296d04b13d455215c8bde0fcab9d6a56d5bf7997f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb7cedb254878f2b36d00dfecbb206294507b764d66f5cf805d4568d89911cdd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab971127488106a2c22cbb6ee986c45719706d0153cddac31452af82a52808f3(
    value: typing.Optional[GoogleContainerAwsNodePoolConfigAutoscalingMetricsCollection],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44751e06a51234bdb9ec07a2c29c75399e5a80e5621f21810c17595e77018ae5(
    *,
    kms_key_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dfd49ab0622eb369d31ac171c3b2e20a82b35aa7b4ef1ffe8de69171d4a02ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc6ee7c6a1b9a2bc86d800b180f83118c08047a92a74c47d93f080acd1d5a0df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74ccf81958a90abecb4af31e22ebd358a912105afa782810aa3b2d91dea2e8f1(
    value: typing.Optional[GoogleContainerAwsNodePoolConfigConfigEncryption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65743764906c4739267ad2b9273d92c269ad96d06169c1b359810066533c638f(
    *,
    tenancy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6345203dedef3a64a16e825ce847d6aa5db85214fade93337fda066b0a2b4ee5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c953a7d5f6a80dda3888daaa1b6b4be27dc4207379a46a3855f3d1b2e0c4d59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2dbde65605453b4613f67ea17f1a7f41db7b553554858161e70f973edb432a7(
    value: typing.Optional[GoogleContainerAwsNodePoolConfigInstancePlacement],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb3e9d54afbcdabc01ad27c5984aecfeea65de82810286fcae1c5f7f3fd6a3e6(
    *,
    secret_arn: builtins.str,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbee8e39ca8d1bef1ad96b935a02123eda6264864103a2559f746a61ced40f21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b090503af96be3ee2466245793edf1da47fc2c75f17cfea534190f0165cfbb1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d7867aa830fa74383574a799e17182c7c9e98bc7329bf25ed6999959dbc678c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34ba60ebc8a2d9a98ef8238bc7c387a7580f25df44e7de73151d4a4b7aced411(
    value: typing.Optional[GoogleContainerAwsNodePoolConfigProxyConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__783c91779958eeeabecd7f9f1458dc78903e4d826e84b7335a42a68a33a80a1f(
    *,
    iops: typing.Optional[jsii.Number] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    size_gib: typing.Optional[jsii.Number] = None,
    throughput: typing.Optional[jsii.Number] = None,
    volume_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d552b90bf4cd3b8cdf940c5cf4751da34b5cd6ca54be28026430ccc608a818e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b912a8e9ce863a8e10c8cfcda45e67bf9517b59025eb8fb1e42e75f042ada064(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bc364273c4ecbcb6542296f8dc246e44ff4d26daedcdd27039907bb65b78ead(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__872b6bce32a1598d675eb81a19efc2f8d468a73e91fa184c34e5440695013207(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ac241a88b7920cb6143dc457c378b630fc8ef067e5631277a8e519053c752aa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9993fbb8645f816d4cbde0585a4fd06a40b4c87f10552baa851cc683f2efa751(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dcfd05727fb071c581731dad22ec5b3c1f4fba7aaa050e74c2c99f910e2548c(
    value: typing.Optional[GoogleContainerAwsNodePoolConfigRootVolume],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d79acb0bda8c99e380c7b8b96c86d9ad804c703c3deb0a0b68f28b5227dc9222(
    *,
    instance_types: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__817322f813ccfcb8355e9544d6b03db12415513d590b93116717d18b2a64bd70(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dd48adfa8cbe193f8f39123ba8fdb0246ca9e770f0f40d51ad5fcaebc6e7b31(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7730e81627e5c875b5991bb0762cc8b62b98b2088fc38eab7c49206f40e3b945(
    value: typing.Optional[GoogleContainerAwsNodePoolConfigSpotConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21c9fe029acee88e648e56328f9ba639331dffc730a10469319b3840cb614134(
    *,
    ec2_key_pair: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d09774ac5f5f43352fc8640fc91474c0ead1b1c407a66c5aced0ed9cc148e950(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e7d60c6f8c36473add4cf4faf3d94427f20f8fbb802c93945dd466b103e546d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7222bb1c71c8569d8bccd3cf9e79d74f7dcc730f96e50fb55127040bcf016a16(
    value: typing.Optional[GoogleContainerAwsNodePoolConfigSshConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1137e3fe11dfea2a29f80250a138b8d4262116bc0ed19fd78032bd7e4bf1368a(
    *,
    effect: builtins.str,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6760f7c7a8c2a5e637f57164a409bb542bc1c7a87c18f6a2be06338ca0e9eed2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a26fd21857fafcb528b0f85ba1500433b879b32e9f8c9a0dec4257feab4184c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__964b5f48dfbaa679ec8057a66f3b913ba1fdd955cdbea11542989ee61ee94e79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2316d7c5b85e15962bb597b1ec996169db41791ef904b9ef7c7007344eb3a7cf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaec36b9ae18f811e1668240237f9c02d82cb44385bc4831b1cbb41a0fb34a2f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6946782c3fb36619152e148682a8486004ae5375cecb1854635913be7752d614(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerAwsNodePoolConfigTaints]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2dcc67ffacd036731c278914d9a47515ac58f4c97c742c57c69aae1fd4a006f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__410bd0ba9646e6a2ac79c18ca03dd15e727ec821b20fe8c61147640fc0a75efa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b6ac5ccc21646234f5f31ec4fbc240c0687f1ddbedfafd3957cc4d633390ea8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5f028450ae4a109981369c92b0b09f53fb562d2ac19a675ab4003dbd483e23e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5718aa5890e80d446f2ccf47d2290613812bf18d7a88c78b08674a74a354215b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAwsNodePoolConfigTaints]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c6fcba6a683011c7dc5e198ea33a26a3d595cd88be0d03ba6d0031c23550b3b(
    *,
    cpu_cfs_quota: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cpu_cfs_quota_period: typing.Optional[builtins.str] = None,
    cpu_manager_policy: typing.Optional[builtins.str] = None,
    pod_pids_limit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c85e7e0df00dd252272638dfe8d02d8ad756fda72417db857dcd935e4b7f13f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca50f687626a2e8e8c0a0cf4e53c52113adc0bea082b7d4b16033a82e6e3db6e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c90db0c1ec64fea935b7a9a7f4e71a99593f307c8e9a6843af505b84ac700f7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0688de8ddef32ec14ff3f79cba419b782d6b20c9d4a3085691fc8be257eb2ce6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10f819e7f04ce173244f3e9ae32f90e7cfa346082735940091c021eba6f38b9b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a02b5f3220839127f536de7a5381b55fa8487fc57bb25c1b3dfb5fde370724f8(
    value: typing.Optional[GoogleContainerAwsNodePoolKubeletConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d41c51def1c9b9cb772c4c052e00d510c1e67a2968853b5642dad11e378cdaa(
    *,
    auto_repair: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aaaa71ac955bd6fff5433c7970484df49bc01df931abce39eb021b8799d693f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e947df660188d2c9962c03beef7d81a71235c7c0141020dfcfccf8a1429c8c21(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2b763afebc62fa4b16a53b684dbb42e9e13d21ea807e5de1c9fd4fd96131140(
    value: typing.Optional[GoogleContainerAwsNodePoolManagement],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4045f177bea59651dfba41675eaf4e4a27f91275fb185b764a840e29d81fc61a(
    *,
    max_pods_per_node: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d73552b932b4328e5d2560ec2793b2570500c56168dd17ea839e2d414363508(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02d017cad1ecce9ee2f61ddf21665407ccf88dba96b0f8d2e7fba77dfaf42088(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba3b43a7e2947222e3cd47ef2b0b942dd84e341a6e311db490c1c6edaae54e09(
    value: typing.Optional[GoogleContainerAwsNodePoolMaxPodsConstraint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aa7371b68cd6d6f48d6c825ee9f8cb2257ff97a262864aa56a422d3a7c339f9(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7526e4f6dbf8e9674fcccb52177ab0c6c0e2984e790367c253166ae43d590e42(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ab609eb1ef5229f03e8896133456f27c6a4440518f225c6679040a16f6ae777(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d04206865d8a984c13a71e5d12f7a0d050da4841b39f9666c993c8e8b224435d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__388b87d149a60ec0d04d3ef8467722d4e00eaa1d33829e3a2d096245d63aae29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d904f89d36fd7cd975f7aea1f392768de5e4acc8f82c52a4d7a4447d84460143(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAwsNodePoolTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efda28a0dfe089277543fbf7b71f93cb26258e384ab3eec1552651ab16055f61(
    *,
    surge_settings: typing.Optional[typing.Union[GoogleContainerAwsNodePoolUpdateSettingsSurgeSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5842edb2440cde6f9d7feddd8aa224b8b92193b5e17c0dd2242cd8982809753a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d6087764d3b86e6a7caf76ffbdf7ba8c617d958588528a70117f387db1857f6(
    value: typing.Optional[GoogleContainerAwsNodePoolUpdateSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__604266ffa6c56f9acedd4928001ede1b48b16674e76ef92c41e5e7629c638f75(
    *,
    max_surge: typing.Optional[jsii.Number] = None,
    max_unavailable: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f5a331494ec7cff0acaa3119578d6a28de04d449af04ce97c27b00a1e5c5fcf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7539e6f113e9833d5553740ccece13b0ae63fc6f7a5bfe37677110e9f2517c41(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98f7e8785ed54234f17e692501200000e037c673cb89b771e6d01e69ebcd28fd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18d7f6ad04a3b1cc295cb2ed49f675ce50c3fbc45c1a4668f6af32025f16a684(
    value: typing.Optional[GoogleContainerAwsNodePoolUpdateSettingsSurgeSettings],
) -> None:
    """Type checking stubs"""
    pass
