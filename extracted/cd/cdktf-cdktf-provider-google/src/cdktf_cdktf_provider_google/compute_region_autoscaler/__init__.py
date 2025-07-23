r'''
# `google_compute_region_autoscaler`

Refer to the Terraform Registry for docs: [`google_compute_region_autoscaler`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler).
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


class ComputeRegionAutoscaler(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionAutoscaler.ComputeRegionAutoscaler",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler google_compute_region_autoscaler}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        autoscaling_policy: typing.Union["ComputeRegionAutoscalerAutoscalingPolicy", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        target: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ComputeRegionAutoscalerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler google_compute_region_autoscaler} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param autoscaling_policy: autoscaling_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#autoscaling_policy ComputeRegionAutoscaler#autoscaling_policy}
        :param name: Name of the resource. The name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#name ComputeRegionAutoscaler#name}
        :param target: URL of the managed instance group that this autoscaler will scale. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#target ComputeRegionAutoscaler#target}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#description ComputeRegionAutoscaler#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#id ComputeRegionAutoscaler#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#project ComputeRegionAutoscaler#project}.
        :param region: URL of the region where the instance group resides. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#region ComputeRegionAutoscaler#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#timeouts ComputeRegionAutoscaler#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__828887e7583dfed0abc41643793d0493042a3ef3a284c4356f699d3c700f438c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeRegionAutoscalerConfig(
            autoscaling_policy=autoscaling_policy,
            name=name,
            target=target,
            description=description,
            id=id,
            project=project,
            region=region,
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
        '''Generates CDKTF code for importing a ComputeRegionAutoscaler resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeRegionAutoscaler to import.
        :param import_from_id: The id of the existing ComputeRegionAutoscaler that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeRegionAutoscaler to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__730a6b91cfe0da4465cf92cca081cb6f37613d210ff5e85031a7d14428e80267)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAutoscalingPolicy")
    def put_autoscaling_policy(
        self,
        *,
        max_replicas: jsii.Number,
        min_replicas: jsii.Number,
        cooldown_period: typing.Optional[jsii.Number] = None,
        cpu_utilization: typing.Optional[typing.Union["ComputeRegionAutoscalerAutoscalingPolicyCpuUtilization", typing.Dict[builtins.str, typing.Any]]] = None,
        load_balancing_utilization: typing.Optional[typing.Union["ComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilization", typing.Dict[builtins.str, typing.Any]]] = None,
        metric: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionAutoscalerAutoscalingPolicyMetric", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mode: typing.Optional[builtins.str] = None,
        scale_in_control: typing.Optional[typing.Union["ComputeRegionAutoscalerAutoscalingPolicyScaleInControl", typing.Dict[builtins.str, typing.Any]]] = None,
        scaling_schedules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionAutoscalerAutoscalingPolicyScalingSchedules", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param max_replicas: The maximum number of instances that the autoscaler can scale up to. This is required when creating or updating an autoscaler. The maximum number of replicas should not be lower than minimal number of replicas. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#max_replicas ComputeRegionAutoscaler#max_replicas}
        :param min_replicas: The minimum number of replicas that the autoscaler can scale down to. This cannot be less than 0. If not provided, autoscaler will choose a default value depending on maximum number of instances allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#min_replicas ComputeRegionAutoscaler#min_replicas}
        :param cooldown_period: The number of seconds that the autoscaler should wait before it starts collecting information from a new instance. This prevents the autoscaler from collecting information when the instance is initializing, during which the collected usage would not be reliable. The default time autoscaler waits is 60 seconds. Virtual machine initialization times might vary because of numerous factors. We recommend that you test how long an instance may take to initialize. To do this, create an instance and time the startup process. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#cooldown_period ComputeRegionAutoscaler#cooldown_period}
        :param cpu_utilization: cpu_utilization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#cpu_utilization ComputeRegionAutoscaler#cpu_utilization}
        :param load_balancing_utilization: load_balancing_utilization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#load_balancing_utilization ComputeRegionAutoscaler#load_balancing_utilization}
        :param metric: metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#metric ComputeRegionAutoscaler#metric}
        :param mode: Defines operating mode for this policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#mode ComputeRegionAutoscaler#mode}
        :param scale_in_control: scale_in_control block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#scale_in_control ComputeRegionAutoscaler#scale_in_control}
        :param scaling_schedules: scaling_schedules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#scaling_schedules ComputeRegionAutoscaler#scaling_schedules}
        '''
        value = ComputeRegionAutoscalerAutoscalingPolicy(
            max_replicas=max_replicas,
            min_replicas=min_replicas,
            cooldown_period=cooldown_period,
            cpu_utilization=cpu_utilization,
            load_balancing_utilization=load_balancing_utilization,
            metric=metric,
            mode=mode,
            scale_in_control=scale_in_control,
            scaling_schedules=scaling_schedules,
        )

        return typing.cast(None, jsii.invoke(self, "putAutoscalingPolicy", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#create ComputeRegionAutoscaler#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#delete ComputeRegionAutoscaler#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#update ComputeRegionAutoscaler#update}.
        '''
        value = ComputeRegionAutoscalerTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

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
    @jsii.member(jsii_name="autoscalingPolicy")
    def autoscaling_policy(
        self,
    ) -> "ComputeRegionAutoscalerAutoscalingPolicyOutputReference":
        return typing.cast("ComputeRegionAutoscalerAutoscalingPolicyOutputReference", jsii.get(self, "autoscalingPolicy"))

    @builtins.property
    @jsii.member(jsii_name="creationTimestamp")
    def creation_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeRegionAutoscalerTimeoutsOutputReference":
        return typing.cast("ComputeRegionAutoscalerTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingPolicyInput")
    def autoscaling_policy_input(
        self,
    ) -> typing.Optional["ComputeRegionAutoscalerAutoscalingPolicy"]:
        return typing.cast(typing.Optional["ComputeRegionAutoscalerAutoscalingPolicy"], jsii.get(self, "autoscalingPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeRegionAutoscalerTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeRegionAutoscalerTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__759d5989bab54b5ff3bae115e863a2052caf50c092bf0f0b8a1b0ccf23ea7529)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fec393026c05e20e37ef3bd634b3ae9a1dcb6771d094b14944fc7b52ac013d31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0adebc5dfe19c8673a221fffa878688744c20f7655b8bcf3bbbcae8bd6e8e2d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8db967cffe16c69dbbe89126dd7fa586a2d6064c581e21d00220ce2b415f8e0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa634cddb658b8a4cb5ca0d17a305cffbeabca908b422148bae865c479f89677)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c322571e9ca8e40e708222ea97de12e20fff2fa03af4446e1bcb364753953302)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionAutoscaler.ComputeRegionAutoscalerAutoscalingPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "max_replicas": "maxReplicas",
        "min_replicas": "minReplicas",
        "cooldown_period": "cooldownPeriod",
        "cpu_utilization": "cpuUtilization",
        "load_balancing_utilization": "loadBalancingUtilization",
        "metric": "metric",
        "mode": "mode",
        "scale_in_control": "scaleInControl",
        "scaling_schedules": "scalingSchedules",
    },
)
class ComputeRegionAutoscalerAutoscalingPolicy:
    def __init__(
        self,
        *,
        max_replicas: jsii.Number,
        min_replicas: jsii.Number,
        cooldown_period: typing.Optional[jsii.Number] = None,
        cpu_utilization: typing.Optional[typing.Union["ComputeRegionAutoscalerAutoscalingPolicyCpuUtilization", typing.Dict[builtins.str, typing.Any]]] = None,
        load_balancing_utilization: typing.Optional[typing.Union["ComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilization", typing.Dict[builtins.str, typing.Any]]] = None,
        metric: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionAutoscalerAutoscalingPolicyMetric", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mode: typing.Optional[builtins.str] = None,
        scale_in_control: typing.Optional[typing.Union["ComputeRegionAutoscalerAutoscalingPolicyScaleInControl", typing.Dict[builtins.str, typing.Any]]] = None,
        scaling_schedules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionAutoscalerAutoscalingPolicyScalingSchedules", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param max_replicas: The maximum number of instances that the autoscaler can scale up to. This is required when creating or updating an autoscaler. The maximum number of replicas should not be lower than minimal number of replicas. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#max_replicas ComputeRegionAutoscaler#max_replicas}
        :param min_replicas: The minimum number of replicas that the autoscaler can scale down to. This cannot be less than 0. If not provided, autoscaler will choose a default value depending on maximum number of instances allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#min_replicas ComputeRegionAutoscaler#min_replicas}
        :param cooldown_period: The number of seconds that the autoscaler should wait before it starts collecting information from a new instance. This prevents the autoscaler from collecting information when the instance is initializing, during which the collected usage would not be reliable. The default time autoscaler waits is 60 seconds. Virtual machine initialization times might vary because of numerous factors. We recommend that you test how long an instance may take to initialize. To do this, create an instance and time the startup process. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#cooldown_period ComputeRegionAutoscaler#cooldown_period}
        :param cpu_utilization: cpu_utilization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#cpu_utilization ComputeRegionAutoscaler#cpu_utilization}
        :param load_balancing_utilization: load_balancing_utilization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#load_balancing_utilization ComputeRegionAutoscaler#load_balancing_utilization}
        :param metric: metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#metric ComputeRegionAutoscaler#metric}
        :param mode: Defines operating mode for this policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#mode ComputeRegionAutoscaler#mode}
        :param scale_in_control: scale_in_control block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#scale_in_control ComputeRegionAutoscaler#scale_in_control}
        :param scaling_schedules: scaling_schedules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#scaling_schedules ComputeRegionAutoscaler#scaling_schedules}
        '''
        if isinstance(cpu_utilization, dict):
            cpu_utilization = ComputeRegionAutoscalerAutoscalingPolicyCpuUtilization(**cpu_utilization)
        if isinstance(load_balancing_utilization, dict):
            load_balancing_utilization = ComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilization(**load_balancing_utilization)
        if isinstance(scale_in_control, dict):
            scale_in_control = ComputeRegionAutoscalerAutoscalingPolicyScaleInControl(**scale_in_control)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c64633fa9d59f4b7998a1168a2bea5597fac450d332b5f2165e0658d112693d)
            check_type(argname="argument max_replicas", value=max_replicas, expected_type=type_hints["max_replicas"])
            check_type(argname="argument min_replicas", value=min_replicas, expected_type=type_hints["min_replicas"])
            check_type(argname="argument cooldown_period", value=cooldown_period, expected_type=type_hints["cooldown_period"])
            check_type(argname="argument cpu_utilization", value=cpu_utilization, expected_type=type_hints["cpu_utilization"])
            check_type(argname="argument load_balancing_utilization", value=load_balancing_utilization, expected_type=type_hints["load_balancing_utilization"])
            check_type(argname="argument metric", value=metric, expected_type=type_hints["metric"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument scale_in_control", value=scale_in_control, expected_type=type_hints["scale_in_control"])
            check_type(argname="argument scaling_schedules", value=scaling_schedules, expected_type=type_hints["scaling_schedules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_replicas": max_replicas,
            "min_replicas": min_replicas,
        }
        if cooldown_period is not None:
            self._values["cooldown_period"] = cooldown_period
        if cpu_utilization is not None:
            self._values["cpu_utilization"] = cpu_utilization
        if load_balancing_utilization is not None:
            self._values["load_balancing_utilization"] = load_balancing_utilization
        if metric is not None:
            self._values["metric"] = metric
        if mode is not None:
            self._values["mode"] = mode
        if scale_in_control is not None:
            self._values["scale_in_control"] = scale_in_control
        if scaling_schedules is not None:
            self._values["scaling_schedules"] = scaling_schedules

    @builtins.property
    def max_replicas(self) -> jsii.Number:
        '''The maximum number of instances that the autoscaler can scale up to.

        This is required when creating or updating an autoscaler. The
        maximum number of replicas should not be lower than minimal number
        of replicas.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#max_replicas ComputeRegionAutoscaler#max_replicas}
        '''
        result = self._values.get("max_replicas")
        assert result is not None, "Required property 'max_replicas' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def min_replicas(self) -> jsii.Number:
        '''The minimum number of replicas that the autoscaler can scale down to.

        This cannot be less than 0. If not provided, autoscaler will
        choose a default value depending on maximum number of instances
        allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#min_replicas ComputeRegionAutoscaler#min_replicas}
        '''
        result = self._values.get("min_replicas")
        assert result is not None, "Required property 'min_replicas' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def cooldown_period(self) -> typing.Optional[jsii.Number]:
        '''The number of seconds that the autoscaler should wait before it starts collecting information from a new instance.

        This prevents
        the autoscaler from collecting information when the instance is
        initializing, during which the collected usage would not be
        reliable. The default time autoscaler waits is 60 seconds.

        Virtual machine initialization times might vary because of
        numerous factors. We recommend that you test how long an
        instance may take to initialize. To do this, create an instance
        and time the startup process.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#cooldown_period ComputeRegionAutoscaler#cooldown_period}
        '''
        result = self._values.get("cooldown_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cpu_utilization(
        self,
    ) -> typing.Optional["ComputeRegionAutoscalerAutoscalingPolicyCpuUtilization"]:
        '''cpu_utilization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#cpu_utilization ComputeRegionAutoscaler#cpu_utilization}
        '''
        result = self._values.get("cpu_utilization")
        return typing.cast(typing.Optional["ComputeRegionAutoscalerAutoscalingPolicyCpuUtilization"], result)

    @builtins.property
    def load_balancing_utilization(
        self,
    ) -> typing.Optional["ComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilization"]:
        '''load_balancing_utilization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#load_balancing_utilization ComputeRegionAutoscaler#load_balancing_utilization}
        '''
        result = self._values.get("load_balancing_utilization")
        return typing.cast(typing.Optional["ComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilization"], result)

    @builtins.property
    def metric(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionAutoscalerAutoscalingPolicyMetric"]]]:
        '''metric block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#metric ComputeRegionAutoscaler#metric}
        '''
        result = self._values.get("metric")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionAutoscalerAutoscalingPolicyMetric"]]], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Defines operating mode for this policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#mode ComputeRegionAutoscaler#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scale_in_control(
        self,
    ) -> typing.Optional["ComputeRegionAutoscalerAutoscalingPolicyScaleInControl"]:
        '''scale_in_control block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#scale_in_control ComputeRegionAutoscaler#scale_in_control}
        '''
        result = self._values.get("scale_in_control")
        return typing.cast(typing.Optional["ComputeRegionAutoscalerAutoscalingPolicyScaleInControl"], result)

    @builtins.property
    def scaling_schedules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionAutoscalerAutoscalingPolicyScalingSchedules"]]]:
        '''scaling_schedules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#scaling_schedules ComputeRegionAutoscaler#scaling_schedules}
        '''
        result = self._values.get("scaling_schedules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionAutoscalerAutoscalingPolicyScalingSchedules"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionAutoscalerAutoscalingPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionAutoscaler.ComputeRegionAutoscalerAutoscalingPolicyCpuUtilization",
    jsii_struct_bases=[],
    name_mapping={"target": "target", "predictive_method": "predictiveMethod"},
)
class ComputeRegionAutoscalerAutoscalingPolicyCpuUtilization:
    def __init__(
        self,
        *,
        target: jsii.Number,
        predictive_method: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target: The target CPU utilization that the autoscaler should maintain. Must be a float value in the range (0, 1]. If not specified, the default is 0.6. If the CPU level is below the target utilization, the autoscaler scales down the number of instances until it reaches the minimum number of instances you specified or until the average CPU of your instances reaches the target utilization. If the average CPU is above the target utilization, the autoscaler scales up until it reaches the maximum number of instances you specified or until the average utilization reaches the target utilization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#target ComputeRegionAutoscaler#target}
        :param predictive_method: Indicates whether predictive autoscaling based on CPU metric is enabled. Valid values are:. - NONE (default). No predictive method is used. The autoscaler scales the group to meet current demand based on real-time metrics. - OPTIMIZE_AVAILABILITY. Predictive autoscaling improves availability by monitoring daily and weekly load patterns and scaling out ahead of anticipated demand. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#predictive_method ComputeRegionAutoscaler#predictive_method}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b3f60ceae0a2d22dc098b278e31079650d46d111dc789b92d5b905da17798b0)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument predictive_method", value=predictive_method, expected_type=type_hints["predictive_method"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target": target,
        }
        if predictive_method is not None:
            self._values["predictive_method"] = predictive_method

    @builtins.property
    def target(self) -> jsii.Number:
        '''The target CPU utilization that the autoscaler should maintain.

        Must be a float value in the range (0, 1]. If not specified, the
        default is 0.6.

        If the CPU level is below the target utilization, the autoscaler
        scales down the number of instances until it reaches the minimum
        number of instances you specified or until the average CPU of
        your instances reaches the target utilization.

        If the average CPU is above the target utilization, the autoscaler
        scales up until it reaches the maximum number of instances you
        specified or until the average utilization reaches the target
        utilization.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#target ComputeRegionAutoscaler#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def predictive_method(self) -> typing.Optional[builtins.str]:
        '''Indicates whether predictive autoscaling based on CPU metric is enabled. Valid values are:.

        - NONE (default). No predictive method is used. The autoscaler scales the group to meet current demand based on real-time metrics.
        - OPTIMIZE_AVAILABILITY. Predictive autoscaling improves availability by monitoring daily and weekly load patterns and scaling out ahead of anticipated demand.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#predictive_method ComputeRegionAutoscaler#predictive_method}
        '''
        result = self._values.get("predictive_method")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionAutoscalerAutoscalingPolicyCpuUtilization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionAutoscalerAutoscalingPolicyCpuUtilizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionAutoscaler.ComputeRegionAutoscalerAutoscalingPolicyCpuUtilizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dbcc8d731d469ae8eceb686cde1b4c941245c7ecde88da4e23063eedbbca46f5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPredictiveMethod")
    def reset_predictive_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPredictiveMethod", []))

    @builtins.property
    @jsii.member(jsii_name="predictiveMethodInput")
    def predictive_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "predictiveMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="predictiveMethod")
    def predictive_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "predictiveMethod"))

    @predictive_method.setter
    def predictive_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d92bc396304657163ac7445e5560cdee8fd17ded2e9a3f1d5cf2cf66e88168e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "predictiveMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "target"))

    @target.setter
    def target(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a456d2c88020718b624e51f5058a31a493757c6e6ebaf82ded469a44271fc37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionAutoscalerAutoscalingPolicyCpuUtilization]:
        return typing.cast(typing.Optional[ComputeRegionAutoscalerAutoscalingPolicyCpuUtilization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionAutoscalerAutoscalingPolicyCpuUtilization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c48243c8420aa504fba481ffcfd6dd18d0db0e4920f7f069bd9d0f6c68d174c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionAutoscaler.ComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilization",
    jsii_struct_bases=[],
    name_mapping={"target": "target"},
)
class ComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilization:
    def __init__(self, *, target: jsii.Number) -> None:
        '''
        :param target: Fraction of backend capacity utilization (set in HTTP(s) load balancing configuration) that autoscaler should maintain. Must be a positive float value. If not defined, the default is 0.8. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#target ComputeRegionAutoscaler#target}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ebac9df426a8b6710a2b0bcd489fb7af4e3fbb7d4475e0ad4e319ae68d036e6)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target": target,
        }

    @builtins.property
    def target(self) -> jsii.Number:
        '''Fraction of backend capacity utilization (set in HTTP(s) load balancing configuration) that autoscaler should maintain.

        Must
        be a positive float value. If not defined, the default is 0.8.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#target ComputeRegionAutoscaler#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionAutoscaler.ComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__13e972367427273e31b71a69ea2e2d72f7a636d4acec98c0970eca57f86dd66e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "target"))

    @target.setter
    def target(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbf8474d7202a234171a1f1d78f3a0604b08e2c5211c7a26a345dd27e2041a3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilization]:
        return typing.cast(typing.Optional[ComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16d9d5f39d4eb2d1f385aabe4f19a1d185471e769a717d0a4bc59d15d924025b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionAutoscaler.ComputeRegionAutoscalerAutoscalingPolicyMetric",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "filter": "filter",
        "single_instance_assignment": "singleInstanceAssignment",
        "target": "target",
        "type": "type",
    },
)
class ComputeRegionAutoscalerAutoscalingPolicyMetric:
    def __init__(
        self,
        *,
        name: builtins.str,
        filter: typing.Optional[builtins.str] = None,
        single_instance_assignment: typing.Optional[jsii.Number] = None,
        target: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The identifier (type) of the Stackdriver Monitoring metric. The metric cannot have negative values. The metric must have a value type of INT64 or DOUBLE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#name ComputeRegionAutoscaler#name}
        :param filter: A filter string to be used as the filter string for a Stackdriver Monitoring TimeSeries.list API call. This filter is used to select a specific TimeSeries for the purpose of autoscaling and to determine whether the metric is exporting per-instance or per-group data. You can only use the AND operator for joining selectors. You can only use direct equality comparison operator (=) without any functions for each selector. You can specify the metric in both the filter string and in the metric field. However, if specified in both places, the metric must be identical. The monitored resource type determines what kind of values are expected for the metric. If it is a gce_instance, the autoscaler expects the metric to include a separate TimeSeries for each instance in a group. In such a case, you cannot filter on resource labels. If the resource type is any other value, the autoscaler expects this metric to contain values that apply to the entire autoscaled instance group and resource label filtering can be performed to point autoscaler at the correct TimeSeries to scale upon. This is called a per-group metric for the purpose of autoscaling. If not specified, the type defaults to gce_instance. You should provide a filter that is selective enough to pick just one TimeSeries for the autoscaled group or for each of the instances (if you are using gce_instance resource type). If multiple TimeSeries are returned upon the query execution, the autoscaler will sum their respective values to obtain its scaling value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#filter ComputeRegionAutoscaler#filter}
        :param single_instance_assignment: If scaling is based on a per-group metric value that represents the total amount of work to be done or resource usage, set this value to an amount assigned for a single instance of the scaled group. The autoscaler will keep the number of instances proportional to the value of this metric, the metric itself should not change value due to group resizing. For example, a good metric to use with the target is 'pubsub.googleapis.com/subscription/num_undelivered_messages' or a custom metric exporting the total number of requests coming to your instances. A bad example would be a metric exporting an average or median latency, since this value can't include a chunk assignable to a single instance, it could be better used with utilization_target instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#single_instance_assignment ComputeRegionAutoscaler#single_instance_assignment}
        :param target: The target value of the metric that autoscaler should maintain. This must be a positive value. A utilization metric scales number of virtual machines handling requests to increase or decrease proportionally to the metric. For example, a good metric to use as a utilizationTarget is www.googleapis.com/compute/instance/network/received_bytes_count. The autoscaler will work to keep this value constant for each of the instances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#target ComputeRegionAutoscaler#target}
        :param type: Defines how target utilization value is expressed for a Stackdriver Monitoring metric. Possible values: ["GAUGE", "DELTA_PER_SECOND", "DELTA_PER_MINUTE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#type ComputeRegionAutoscaler#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f20292978fc6562a2fa634e1ca44d457f2df7e255d26b9050d6c0ddf7c1ac43a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument single_instance_assignment", value=single_instance_assignment, expected_type=type_hints["single_instance_assignment"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if filter is not None:
            self._values["filter"] = filter
        if single_instance_assignment is not None:
            self._values["single_instance_assignment"] = single_instance_assignment
        if target is not None:
            self._values["target"] = target
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def name(self) -> builtins.str:
        '''The identifier (type) of the Stackdriver Monitoring metric. The metric cannot have negative values.

        The metric must have a value type of INT64 or DOUBLE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#name ComputeRegionAutoscaler#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filter(self) -> typing.Optional[builtins.str]:
        '''A filter string to be used as the filter string for a Stackdriver Monitoring TimeSeries.list API call. This filter is used to select a specific TimeSeries for the purpose of autoscaling and to determine whether the metric is exporting per-instance or per-group data.

        You can only use the AND operator for joining selectors.
        You can only use direct equality comparison operator (=) without
        any functions for each selector.
        You can specify the metric in both the filter string and in the
        metric field. However, if specified in both places, the metric must
        be identical.

        The monitored resource type determines what kind of values are
        expected for the metric. If it is a gce_instance, the autoscaler
        expects the metric to include a separate TimeSeries for each
        instance in a group. In such a case, you cannot filter on resource
        labels.

        If the resource type is any other value, the autoscaler expects
        this metric to contain values that apply to the entire autoscaled
        instance group and resource label filtering can be performed to
        point autoscaler at the correct TimeSeries to scale upon.
        This is called a per-group metric for the purpose of autoscaling.

        If not specified, the type defaults to gce_instance.

        You should provide a filter that is selective enough to pick just
        one TimeSeries for the autoscaled group or for each of the instances
        (if you are using gce_instance resource type). If multiple
        TimeSeries are returned upon the query execution, the autoscaler
        will sum their respective values to obtain its scaling value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#filter ComputeRegionAutoscaler#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def single_instance_assignment(self) -> typing.Optional[jsii.Number]:
        '''If scaling is based on a per-group metric value that represents the total amount of work to be done or resource usage, set this value to an amount assigned for a single instance of the scaled group.

        The autoscaler will keep the number of instances proportional to the
        value of this metric, the metric itself should not change value due
        to group resizing.

        For example, a good metric to use with the target is
        'pubsub.googleapis.com/subscription/num_undelivered_messages'
        or a custom metric exporting the total number of requests coming to
        your instances.

        A bad example would be a metric exporting an average or median
        latency, since this value can't include a chunk assignable to a
        single instance, it could be better used with utilization_target
        instead.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#single_instance_assignment ComputeRegionAutoscaler#single_instance_assignment}
        '''
        result = self._values.get("single_instance_assignment")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target(self) -> typing.Optional[jsii.Number]:
        '''The target value of the metric that autoscaler should maintain.

        This must be a positive value. A utilization
        metric scales number of virtual machines handling requests
        to increase or decrease proportionally to the metric.

        For example, a good metric to use as a utilizationTarget is
        www.googleapis.com/compute/instance/network/received_bytes_count.
        The autoscaler will work to keep this value constant for each
        of the instances.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#target ComputeRegionAutoscaler#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Defines how target utilization value is expressed for a Stackdriver Monitoring metric. Possible values: ["GAUGE", "DELTA_PER_SECOND", "DELTA_PER_MINUTE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#type ComputeRegionAutoscaler#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionAutoscalerAutoscalingPolicyMetric(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionAutoscalerAutoscalingPolicyMetricList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionAutoscaler.ComputeRegionAutoscalerAutoscalingPolicyMetricList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__032a56967a454e60b9b9deb7dcab1419b518f0a36ae2a0d9f1ee86d01fbd9844)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionAutoscalerAutoscalingPolicyMetricOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dda195a1e7f06cd5d4cb7664b8bb01e739d368dab5db52cbeab75c3c3fdc7d3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionAutoscalerAutoscalingPolicyMetricOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de6b581df1b2f7ca65736906590cdf8222ea7b63f8c45ef0f29cbf6d9510dae3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d11a955ff93a19bae2a56ec91bf86eff7b4ba2e83d44971cb51d130029fca936)
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
            type_hints = typing.get_type_hints(_typecheckingstub__19183805ed3922745567f51e5546760731cbcc91934e9ab899eec7fa0d31c680)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionAutoscalerAutoscalingPolicyMetric]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionAutoscalerAutoscalingPolicyMetric]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionAutoscalerAutoscalingPolicyMetric]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80cd28636d4c48a760445329ff1a7054f39caef6ec88f8e6c26e9ed6feb39a48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionAutoscalerAutoscalingPolicyMetricOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionAutoscaler.ComputeRegionAutoscalerAutoscalingPolicyMetricOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e33ec3c9133fdbc6df4b93030bd565d70756abbf52b639222e1b5d78d0e42e1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

    @jsii.member(jsii_name="resetSingleInstanceAssignment")
    def reset_single_instance_assignment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSingleInstanceAssignment", []))

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="singleInstanceAssignmentInput")
    def single_instance_assignment_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "singleInstanceAssignmentInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filter"))

    @filter.setter
    def filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5aeabe1d809ac2d5962b865c5f1bc8381d0d8e1e8ae7c3d75d9890e4a423756d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3750b56a9f5f5adc1f82b9ce75c8d1cbf5481e7d3e0c6369b17ba8f8eafab8f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="singleInstanceAssignment")
    def single_instance_assignment(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "singleInstanceAssignment"))

    @single_instance_assignment.setter
    def single_instance_assignment(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f51a761e367091972fee12085bc080464afcf8ccac9ab658479b441d87a35ca9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "singleInstanceAssignment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "target"))

    @target.setter
    def target(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99d3ae5e3f362ff9f12e74aac6b93628c170b8464afb6946f7cde432b5ca2a91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83ba9c3465f8fc4990a3da9ba745edb64b7c26389c70a58c5efebb2bb75cb7ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionAutoscalerAutoscalingPolicyMetric]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionAutoscalerAutoscalingPolicyMetric]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionAutoscalerAutoscalingPolicyMetric]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c25edd6d3caa57070f1a6e61113a6a825c5242889dedb896c37319b26af545b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionAutoscalerAutoscalingPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionAutoscaler.ComputeRegionAutoscalerAutoscalingPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f4319c478bf4014d7b61e25fc746063eece384ce259b4e318e5b781ce82e35f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCpuUtilization")
    def put_cpu_utilization(
        self,
        *,
        target: jsii.Number,
        predictive_method: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target: The target CPU utilization that the autoscaler should maintain. Must be a float value in the range (0, 1]. If not specified, the default is 0.6. If the CPU level is below the target utilization, the autoscaler scales down the number of instances until it reaches the minimum number of instances you specified or until the average CPU of your instances reaches the target utilization. If the average CPU is above the target utilization, the autoscaler scales up until it reaches the maximum number of instances you specified or until the average utilization reaches the target utilization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#target ComputeRegionAutoscaler#target}
        :param predictive_method: Indicates whether predictive autoscaling based on CPU metric is enabled. Valid values are:. - NONE (default). No predictive method is used. The autoscaler scales the group to meet current demand based on real-time metrics. - OPTIMIZE_AVAILABILITY. Predictive autoscaling improves availability by monitoring daily and weekly load patterns and scaling out ahead of anticipated demand. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#predictive_method ComputeRegionAutoscaler#predictive_method}
        '''
        value = ComputeRegionAutoscalerAutoscalingPolicyCpuUtilization(
            target=target, predictive_method=predictive_method
        )

        return typing.cast(None, jsii.invoke(self, "putCpuUtilization", [value]))

    @jsii.member(jsii_name="putLoadBalancingUtilization")
    def put_load_balancing_utilization(self, *, target: jsii.Number) -> None:
        '''
        :param target: Fraction of backend capacity utilization (set in HTTP(s) load balancing configuration) that autoscaler should maintain. Must be a positive float value. If not defined, the default is 0.8. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#target ComputeRegionAutoscaler#target}
        '''
        value = ComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilization(
            target=target
        )

        return typing.cast(None, jsii.invoke(self, "putLoadBalancingUtilization", [value]))

    @jsii.member(jsii_name="putMetric")
    def put_metric(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionAutoscalerAutoscalingPolicyMetric, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bed7be26d6a19648c218f601b7528c7fac17dea33d15742fb4b6f7d792e02e8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMetric", [value]))

    @jsii.member(jsii_name="putScaleInControl")
    def put_scale_in_control(
        self,
        *,
        max_scaled_in_replicas: typing.Optional[typing.Union["ComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas", typing.Dict[builtins.str, typing.Any]]] = None,
        time_window_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_scaled_in_replicas: max_scaled_in_replicas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#max_scaled_in_replicas ComputeRegionAutoscaler#max_scaled_in_replicas}
        :param time_window_sec: How long back autoscaling should look when computing recommendations to include directives regarding slower scale down, as described above. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#time_window_sec ComputeRegionAutoscaler#time_window_sec}
        '''
        value = ComputeRegionAutoscalerAutoscalingPolicyScaleInControl(
            max_scaled_in_replicas=max_scaled_in_replicas,
            time_window_sec=time_window_sec,
        )

        return typing.cast(None, jsii.invoke(self, "putScaleInControl", [value]))

    @jsii.member(jsii_name="putScalingSchedules")
    def put_scaling_schedules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionAutoscalerAutoscalingPolicyScalingSchedules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__546be3397322c6914fc30a34a224264b062ee1afc502780419af74604bd49280)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putScalingSchedules", [value]))

    @jsii.member(jsii_name="resetCooldownPeriod")
    def reset_cooldown_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCooldownPeriod", []))

    @jsii.member(jsii_name="resetCpuUtilization")
    def reset_cpu_utilization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuUtilization", []))

    @jsii.member(jsii_name="resetLoadBalancingUtilization")
    def reset_load_balancing_utilization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancingUtilization", []))

    @jsii.member(jsii_name="resetMetric")
    def reset_metric(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetric", []))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetScaleInControl")
    def reset_scale_in_control(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScaleInControl", []))

    @jsii.member(jsii_name="resetScalingSchedules")
    def reset_scaling_schedules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScalingSchedules", []))

    @builtins.property
    @jsii.member(jsii_name="cpuUtilization")
    def cpu_utilization(
        self,
    ) -> ComputeRegionAutoscalerAutoscalingPolicyCpuUtilizationOutputReference:
        return typing.cast(ComputeRegionAutoscalerAutoscalingPolicyCpuUtilizationOutputReference, jsii.get(self, "cpuUtilization"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancingUtilization")
    def load_balancing_utilization(
        self,
    ) -> ComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilizationOutputReference:
        return typing.cast(ComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilizationOutputReference, jsii.get(self, "loadBalancingUtilization"))

    @builtins.property
    @jsii.member(jsii_name="metric")
    def metric(self) -> ComputeRegionAutoscalerAutoscalingPolicyMetricList:
        return typing.cast(ComputeRegionAutoscalerAutoscalingPolicyMetricList, jsii.get(self, "metric"))

    @builtins.property
    @jsii.member(jsii_name="scaleInControl")
    def scale_in_control(
        self,
    ) -> "ComputeRegionAutoscalerAutoscalingPolicyScaleInControlOutputReference":
        return typing.cast("ComputeRegionAutoscalerAutoscalingPolicyScaleInControlOutputReference", jsii.get(self, "scaleInControl"))

    @builtins.property
    @jsii.member(jsii_name="scalingSchedules")
    def scaling_schedules(
        self,
    ) -> "ComputeRegionAutoscalerAutoscalingPolicyScalingSchedulesList":
        return typing.cast("ComputeRegionAutoscalerAutoscalingPolicyScalingSchedulesList", jsii.get(self, "scalingSchedules"))

    @builtins.property
    @jsii.member(jsii_name="cooldownPeriodInput")
    def cooldown_period_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cooldownPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuUtilizationInput")
    def cpu_utilization_input(
        self,
    ) -> typing.Optional[ComputeRegionAutoscalerAutoscalingPolicyCpuUtilization]:
        return typing.cast(typing.Optional[ComputeRegionAutoscalerAutoscalingPolicyCpuUtilization], jsii.get(self, "cpuUtilizationInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancingUtilizationInput")
    def load_balancing_utilization_input(
        self,
    ) -> typing.Optional[ComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilization]:
        return typing.cast(typing.Optional[ComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilization], jsii.get(self, "loadBalancingUtilizationInput"))

    @builtins.property
    @jsii.member(jsii_name="maxReplicasInput")
    def max_replicas_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxReplicasInput"))

    @builtins.property
    @jsii.member(jsii_name="metricInput")
    def metric_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionAutoscalerAutoscalingPolicyMetric]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionAutoscalerAutoscalingPolicyMetric]]], jsii.get(self, "metricInput"))

    @builtins.property
    @jsii.member(jsii_name="minReplicasInput")
    def min_replicas_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minReplicasInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleInControlInput")
    def scale_in_control_input(
        self,
    ) -> typing.Optional["ComputeRegionAutoscalerAutoscalingPolicyScaleInControl"]:
        return typing.cast(typing.Optional["ComputeRegionAutoscalerAutoscalingPolicyScaleInControl"], jsii.get(self, "scaleInControlInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingSchedulesInput")
    def scaling_schedules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionAutoscalerAutoscalingPolicyScalingSchedules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionAutoscalerAutoscalingPolicyScalingSchedules"]]], jsii.get(self, "scalingSchedulesInput"))

    @builtins.property
    @jsii.member(jsii_name="cooldownPeriod")
    def cooldown_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cooldownPeriod"))

    @cooldown_period.setter
    def cooldown_period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f477025412ad92f154014d917d444f6d300e2da9c7eee4af22efefc7ec24d5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cooldownPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxReplicas")
    def max_replicas(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxReplicas"))

    @max_replicas.setter
    def max_replicas(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0496c5e746fbb2ddab5f7cc0a2e16e201a5e6ff5c1c89d264954a2c55eaf524)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxReplicas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minReplicas")
    def min_replicas(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minReplicas"))

    @min_replicas.setter
    def min_replicas(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2affda891dbcdf55a2dc7874e5fa2938059d78e13a8e41f0b4753a1824e1d1ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minReplicas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2523f95c1db3119d17db74576cb6bc70d0515e3ea071243459d5f2e9a3230eb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionAutoscalerAutoscalingPolicy]:
        return typing.cast(typing.Optional[ComputeRegionAutoscalerAutoscalingPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionAutoscalerAutoscalingPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__031b3ac6e83cdf1dec5f1b4690d841531aedffb9de14265be60eb7db18d8ea1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionAutoscaler.ComputeRegionAutoscalerAutoscalingPolicyScaleInControl",
    jsii_struct_bases=[],
    name_mapping={
        "max_scaled_in_replicas": "maxScaledInReplicas",
        "time_window_sec": "timeWindowSec",
    },
)
class ComputeRegionAutoscalerAutoscalingPolicyScaleInControl:
    def __init__(
        self,
        *,
        max_scaled_in_replicas: typing.Optional[typing.Union["ComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas", typing.Dict[builtins.str, typing.Any]]] = None,
        time_window_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_scaled_in_replicas: max_scaled_in_replicas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#max_scaled_in_replicas ComputeRegionAutoscaler#max_scaled_in_replicas}
        :param time_window_sec: How long back autoscaling should look when computing recommendations to include directives regarding slower scale down, as described above. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#time_window_sec ComputeRegionAutoscaler#time_window_sec}
        '''
        if isinstance(max_scaled_in_replicas, dict):
            max_scaled_in_replicas = ComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas(**max_scaled_in_replicas)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79e35adef032acd4f4ec7719c2ec2acecba56bd16ef77fb8e0cbfad82873a7eb)
            check_type(argname="argument max_scaled_in_replicas", value=max_scaled_in_replicas, expected_type=type_hints["max_scaled_in_replicas"])
            check_type(argname="argument time_window_sec", value=time_window_sec, expected_type=type_hints["time_window_sec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_scaled_in_replicas is not None:
            self._values["max_scaled_in_replicas"] = max_scaled_in_replicas
        if time_window_sec is not None:
            self._values["time_window_sec"] = time_window_sec

    @builtins.property
    def max_scaled_in_replicas(
        self,
    ) -> typing.Optional["ComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas"]:
        '''max_scaled_in_replicas block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#max_scaled_in_replicas ComputeRegionAutoscaler#max_scaled_in_replicas}
        '''
        result = self._values.get("max_scaled_in_replicas")
        return typing.cast(typing.Optional["ComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas"], result)

    @builtins.property
    def time_window_sec(self) -> typing.Optional[jsii.Number]:
        '''How long back autoscaling should look when computing recommendations to include directives regarding slower scale down, as described above.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#time_window_sec ComputeRegionAutoscaler#time_window_sec}
        '''
        result = self._values.get("time_window_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionAutoscalerAutoscalingPolicyScaleInControl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionAutoscaler.ComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas",
    jsii_struct_bases=[],
    name_mapping={"fixed": "fixed", "percent": "percent"},
)
class ComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas:
    def __init__(
        self,
        *,
        fixed: typing.Optional[jsii.Number] = None,
        percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fixed: Specifies a fixed number of VM instances. This must be a positive integer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#fixed ComputeRegionAutoscaler#fixed}
        :param percent: Specifies a percentage of instances between 0 to 100%, inclusive. For example, specify 80 for 80%. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#percent ComputeRegionAutoscaler#percent}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78b93ce2da3e166bb8c7145e4a7d720c6cad673bb4f95663493f3d65a8d2f686)
            check_type(argname="argument fixed", value=fixed, expected_type=type_hints["fixed"])
            check_type(argname="argument percent", value=percent, expected_type=type_hints["percent"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fixed is not None:
            self._values["fixed"] = fixed
        if percent is not None:
            self._values["percent"] = percent

    @builtins.property
    def fixed(self) -> typing.Optional[jsii.Number]:
        '''Specifies a fixed number of VM instances. This must be a positive integer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#fixed ComputeRegionAutoscaler#fixed}
        '''
        result = self._values.get("fixed")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def percent(self) -> typing.Optional[jsii.Number]:
        '''Specifies a percentage of instances between 0 to 100%, inclusive. For example, specify 80 for 80%.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#percent ComputeRegionAutoscaler#percent}
        '''
        result = self._values.get("percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicasOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionAutoscaler.ComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicasOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27dc34180d42191e71dfc26f165bff7dfee6957035f2c3e3b2afef5fc95b2040)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFixed")
    def reset_fixed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFixed", []))

    @jsii.member(jsii_name="resetPercent")
    def reset_percent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPercent", []))

    @builtins.property
    @jsii.member(jsii_name="fixedInput")
    def fixed_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "fixedInput"))

    @builtins.property
    @jsii.member(jsii_name="percentInput")
    def percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "percentInput"))

    @builtins.property
    @jsii.member(jsii_name="fixed")
    def fixed(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "fixed"))

    @fixed.setter
    def fixed(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16f7f960848dde14d7dd6022526dc1f4ee9a5bc537d6d127da318ff221805345)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="percent")
    def percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percent"))

    @percent.setter
    def percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__583ea2eb7a4c8436e4c358d9ad89d28c2003a101fd7bf9b32e6b6436be1b2bf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas]:
        return typing.cast(typing.Optional[ComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c27b640520965c2c7bc2d0700f9f3218fcf06eb45662a74789246ef26f71d7b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionAutoscalerAutoscalingPolicyScaleInControlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionAutoscaler.ComputeRegionAutoscalerAutoscalingPolicyScaleInControlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac965d1958469b8079978366414892ddfd6277be0925f8fd9fbfc084e1699501)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMaxScaledInReplicas")
    def put_max_scaled_in_replicas(
        self,
        *,
        fixed: typing.Optional[jsii.Number] = None,
        percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fixed: Specifies a fixed number of VM instances. This must be a positive integer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#fixed ComputeRegionAutoscaler#fixed}
        :param percent: Specifies a percentage of instances between 0 to 100%, inclusive. For example, specify 80 for 80%. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#percent ComputeRegionAutoscaler#percent}
        '''
        value = ComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas(
            fixed=fixed, percent=percent
        )

        return typing.cast(None, jsii.invoke(self, "putMaxScaledInReplicas", [value]))

    @jsii.member(jsii_name="resetMaxScaledInReplicas")
    def reset_max_scaled_in_replicas(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxScaledInReplicas", []))

    @jsii.member(jsii_name="resetTimeWindowSec")
    def reset_time_window_sec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeWindowSec", []))

    @builtins.property
    @jsii.member(jsii_name="maxScaledInReplicas")
    def max_scaled_in_replicas(
        self,
    ) -> ComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicasOutputReference:
        return typing.cast(ComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicasOutputReference, jsii.get(self, "maxScaledInReplicas"))

    @builtins.property
    @jsii.member(jsii_name="maxScaledInReplicasInput")
    def max_scaled_in_replicas_input(
        self,
    ) -> typing.Optional[ComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas]:
        return typing.cast(typing.Optional[ComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas], jsii.get(self, "maxScaledInReplicasInput"))

    @builtins.property
    @jsii.member(jsii_name="timeWindowSecInput")
    def time_window_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeWindowSecInput"))

    @builtins.property
    @jsii.member(jsii_name="timeWindowSec")
    def time_window_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeWindowSec"))

    @time_window_sec.setter
    def time_window_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7ba8ed1d9e83ae8f787f11de65a8cbb25dcb3bfe3710437e880a24055f20d94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeWindowSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionAutoscalerAutoscalingPolicyScaleInControl]:
        return typing.cast(typing.Optional[ComputeRegionAutoscalerAutoscalingPolicyScaleInControl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionAutoscalerAutoscalingPolicyScaleInControl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7405f2e929b3286bc837689af2ae0525437a300abba7e0fd3591694d2ffaeca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionAutoscaler.ComputeRegionAutoscalerAutoscalingPolicyScalingSchedules",
    jsii_struct_bases=[],
    name_mapping={
        "duration_sec": "durationSec",
        "min_required_replicas": "minRequiredReplicas",
        "name": "name",
        "schedule": "schedule",
        "description": "description",
        "disabled": "disabled",
        "time_zone": "timeZone",
    },
)
class ComputeRegionAutoscalerAutoscalingPolicyScalingSchedules:
    def __init__(
        self,
        *,
        duration_sec: jsii.Number,
        min_required_replicas: jsii.Number,
        name: builtins.str,
        schedule: builtins.str,
        description: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        time_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param duration_sec: The duration of time intervals (in seconds) for which this scaling schedule will be running. The minimum allowed value is 300. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#duration_sec ComputeRegionAutoscaler#duration_sec}
        :param min_required_replicas: Minimum number of VM instances that autoscaler will recommend in time intervals starting according to schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#min_required_replicas ComputeRegionAutoscaler#min_required_replicas}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#name ComputeRegionAutoscaler#name}.
        :param schedule: The start timestamps of time intervals when this scaling schedule should provide a scaling signal. This field uses the extended cron format (with an optional year field). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#schedule ComputeRegionAutoscaler#schedule}
        :param description: A description of a scaling schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#description ComputeRegionAutoscaler#description}
        :param disabled: A boolean value that specifies if a scaling schedule can influence autoscaler recommendations. If set to true, then a scaling schedule has no effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#disabled ComputeRegionAutoscaler#disabled}
        :param time_zone: The time zone to be used when interpreting the schedule. The value of this field must be a time zone name from the tz database: http://en.wikipedia.org/wiki/Tz_database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#time_zone ComputeRegionAutoscaler#time_zone}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dc36400f995df895c2f745c86a492ade72505f249baeed5b3dbd45fca444dd5)
            check_type(argname="argument duration_sec", value=duration_sec, expected_type=type_hints["duration_sec"])
            check_type(argname="argument min_required_replicas", value=min_required_replicas, expected_type=type_hints["min_required_replicas"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "duration_sec": duration_sec,
            "min_required_replicas": min_required_replicas,
            "name": name,
            "schedule": schedule,
        }
        if description is not None:
            self._values["description"] = description
        if disabled is not None:
            self._values["disabled"] = disabled
        if time_zone is not None:
            self._values["time_zone"] = time_zone

    @builtins.property
    def duration_sec(self) -> jsii.Number:
        '''The duration of time intervals (in seconds) for which this scaling schedule will be running.

        The minimum allowed value is 300.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#duration_sec ComputeRegionAutoscaler#duration_sec}
        '''
        result = self._values.get("duration_sec")
        assert result is not None, "Required property 'duration_sec' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def min_required_replicas(self) -> jsii.Number:
        '''Minimum number of VM instances that autoscaler will recommend in time intervals starting according to schedule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#min_required_replicas ComputeRegionAutoscaler#min_required_replicas}
        '''
        result = self._values.get("min_required_replicas")
        assert result is not None, "Required property 'min_required_replicas' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#name ComputeRegionAutoscaler#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schedule(self) -> builtins.str:
        '''The start timestamps of time intervals when this scaling schedule should provide a scaling signal.

        This field uses the extended cron format (with an optional year field).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#schedule ComputeRegionAutoscaler#schedule}
        '''
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of a scaling schedule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#description ComputeRegionAutoscaler#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A boolean value that specifies if a scaling schedule can influence autoscaler recommendations.

        If set to true, then a scaling schedule has no effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#disabled ComputeRegionAutoscaler#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[builtins.str]:
        '''The time zone to be used when interpreting the schedule.

        The value of this field must be a time zone name from the tz database: http://en.wikipedia.org/wiki/Tz_database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#time_zone ComputeRegionAutoscaler#time_zone}
        '''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionAutoscalerAutoscalingPolicyScalingSchedules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionAutoscalerAutoscalingPolicyScalingSchedulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionAutoscaler.ComputeRegionAutoscalerAutoscalingPolicyScalingSchedulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__493b454d9dc1bfa8060e057d64bb09b06fa8fe7ec69c72ab5a7c61d9bc77cb4d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionAutoscalerAutoscalingPolicyScalingSchedulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__862aaec2130f8409d7dceac00e02e9951ef6a7309d38c45c70735d0ddb91c218)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionAutoscalerAutoscalingPolicyScalingSchedulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b415bcc77ffba17b52f8a5bd8c23601ef58e73e652b6e44de05d28b0d9c36dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad50c7d7e09a8ada125eebbc2987ff9fcd97a4fb7f88a872c8e20a0100166492)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cbe15a73ab3f2584587d5637f2a66169b6ef6110faf603560a528e5b6f2d1907)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionAutoscalerAutoscalingPolicyScalingSchedules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionAutoscalerAutoscalingPolicyScalingSchedules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionAutoscalerAutoscalingPolicyScalingSchedules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2bd61bbdc335d5406571eb9a2532c2810c496ee3bc09d6252d159ce6de9342c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionAutoscalerAutoscalingPolicyScalingSchedulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionAutoscaler.ComputeRegionAutoscalerAutoscalingPolicyScalingSchedulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc58b5831473f8e46fcc2339f0222f13cfa0444a102c5cc371a470a28364722e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisabled")
    def reset_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabled", []))

    @jsii.member(jsii_name="resetTimeZone")
    def reset_time_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeZone", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="disabledInput")
    def disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disabledInput"))

    @builtins.property
    @jsii.member(jsii_name="durationSecInput")
    def duration_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "durationSecInput"))

    @builtins.property
    @jsii.member(jsii_name="minRequiredReplicasInput")
    def min_required_replicas_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minRequiredReplicasInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15437af29cc78606fcd87eec9d176c55df049b8788e12da3934ae2ca0df01e81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disabled")
    def disabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disabled"))

    @disabled.setter
    def disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__968d4e5a3215abbc926b3eaed1ca4893f66888336b0a361298685f9b7c9283a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="durationSec")
    def duration_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "durationSec"))

    @duration_sec.setter
    def duration_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__370c3d13d1fa4cdfe5523efe752a7b004b9c6f2eb0bdb0f19b72fceb7368ba5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "durationSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minRequiredReplicas")
    def min_required_replicas(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minRequiredReplicas"))

    @min_required_replicas.setter
    def min_required_replicas(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a41a626eeacd181d0c8f88e2a3abc43fe5554137ae6d3b9517274ce45e5a64ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minRequiredReplicas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95270b26674f3885fc7f1e2d0b6e3647d3f15f2292a5b150e565f8fd16abf5b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedule"))

    @schedule.setter
    def schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f154806c45bb59f09d1e46b53eb551d61ff7e849b0b78fac9cadd131f75da75b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4ceff085a961e972891d797539a21053113e23acc9ff445a3d887faaa1f2907)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionAutoscalerAutoscalingPolicyScalingSchedules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionAutoscalerAutoscalingPolicyScalingSchedules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionAutoscalerAutoscalingPolicyScalingSchedules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4226f2a479ad314bea1836443dbc7cff31f2f2626eca9a4c9c27bfae0c72e3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionAutoscaler.ComputeRegionAutoscalerConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "autoscaling_policy": "autoscalingPolicy",
        "name": "name",
        "target": "target",
        "description": "description",
        "id": "id",
        "project": "project",
        "region": "region",
        "timeouts": "timeouts",
    },
)
class ComputeRegionAutoscalerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        autoscaling_policy: typing.Union[ComputeRegionAutoscalerAutoscalingPolicy, typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        target: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ComputeRegionAutoscalerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param autoscaling_policy: autoscaling_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#autoscaling_policy ComputeRegionAutoscaler#autoscaling_policy}
        :param name: Name of the resource. The name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#name ComputeRegionAutoscaler#name}
        :param target: URL of the managed instance group that this autoscaler will scale. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#target ComputeRegionAutoscaler#target}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#description ComputeRegionAutoscaler#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#id ComputeRegionAutoscaler#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#project ComputeRegionAutoscaler#project}.
        :param region: URL of the region where the instance group resides. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#region ComputeRegionAutoscaler#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#timeouts ComputeRegionAutoscaler#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(autoscaling_policy, dict):
            autoscaling_policy = ComputeRegionAutoscalerAutoscalingPolicy(**autoscaling_policy)
        if isinstance(timeouts, dict):
            timeouts = ComputeRegionAutoscalerTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a15216cab526287c2b03fcca0d0e4366e22b85dc55a565f18ba9b8009de6a35)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument autoscaling_policy", value=autoscaling_policy, expected_type=type_hints["autoscaling_policy"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "autoscaling_policy": autoscaling_policy,
            "name": name,
            "target": target,
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
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
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
    def autoscaling_policy(self) -> ComputeRegionAutoscalerAutoscalingPolicy:
        '''autoscaling_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#autoscaling_policy ComputeRegionAutoscaler#autoscaling_policy}
        '''
        result = self._values.get("autoscaling_policy")
        assert result is not None, "Required property 'autoscaling_policy' is missing"
        return typing.cast(ComputeRegionAutoscalerAutoscalingPolicy, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the resource.

        The name must be 1-63 characters long and match
        the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the
        first character must be a lowercase letter, and all following
        characters must be a dash, lowercase letter, or digit, except the last
        character, which cannot be a dash.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#name ComputeRegionAutoscaler#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> builtins.str:
        '''URL of the managed instance group that this autoscaler will scale.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#target ComputeRegionAutoscaler#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#description ComputeRegionAutoscaler#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#id ComputeRegionAutoscaler#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#project ComputeRegionAutoscaler#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''URL of the region where the instance group resides.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#region ComputeRegionAutoscaler#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeRegionAutoscalerTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#timeouts ComputeRegionAutoscaler#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeRegionAutoscalerTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionAutoscalerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionAutoscaler.ComputeRegionAutoscalerTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeRegionAutoscalerTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#create ComputeRegionAutoscaler#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#delete ComputeRegionAutoscaler#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#update ComputeRegionAutoscaler#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcf9653a06a363522c7f880573986428c7c034dec3206736df5840149a4108a8)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#create ComputeRegionAutoscaler#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#delete ComputeRegionAutoscaler#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_autoscaler#update ComputeRegionAutoscaler#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionAutoscalerTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionAutoscalerTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionAutoscaler.ComputeRegionAutoscalerTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__34188c48da12b84a190a93216eedc1c288d84619cec979f4fc5d66de96efd76e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b0df43573c6b503020f03de5ae2e68614c139c0f918f7d138327467279da083)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d208549257e0dbc90c0e2c21858db3aa2e82560b1b54faf94db8241bf3ff3e0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b02826843e4c5adb5488bfca876af85a7e896675f4616588012003b4fe130f3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionAutoscalerTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionAutoscalerTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionAutoscalerTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efdf5b05ea15d91f582640703654d7cc338bb7fa2710abf8e1c8cc26009a821a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeRegionAutoscaler",
    "ComputeRegionAutoscalerAutoscalingPolicy",
    "ComputeRegionAutoscalerAutoscalingPolicyCpuUtilization",
    "ComputeRegionAutoscalerAutoscalingPolicyCpuUtilizationOutputReference",
    "ComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilization",
    "ComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilizationOutputReference",
    "ComputeRegionAutoscalerAutoscalingPolicyMetric",
    "ComputeRegionAutoscalerAutoscalingPolicyMetricList",
    "ComputeRegionAutoscalerAutoscalingPolicyMetricOutputReference",
    "ComputeRegionAutoscalerAutoscalingPolicyOutputReference",
    "ComputeRegionAutoscalerAutoscalingPolicyScaleInControl",
    "ComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas",
    "ComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicasOutputReference",
    "ComputeRegionAutoscalerAutoscalingPolicyScaleInControlOutputReference",
    "ComputeRegionAutoscalerAutoscalingPolicyScalingSchedules",
    "ComputeRegionAutoscalerAutoscalingPolicyScalingSchedulesList",
    "ComputeRegionAutoscalerAutoscalingPolicyScalingSchedulesOutputReference",
    "ComputeRegionAutoscalerConfig",
    "ComputeRegionAutoscalerTimeouts",
    "ComputeRegionAutoscalerTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__828887e7583dfed0abc41643793d0493042a3ef3a284c4356f699d3c700f438c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    autoscaling_policy: typing.Union[ComputeRegionAutoscalerAutoscalingPolicy, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    target: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ComputeRegionAutoscalerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__730a6b91cfe0da4465cf92cca081cb6f37613d210ff5e85031a7d14428e80267(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__759d5989bab54b5ff3bae115e863a2052caf50c092bf0f0b8a1b0ccf23ea7529(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fec393026c05e20e37ef3bd634b3ae9a1dcb6771d094b14944fc7b52ac013d31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0adebc5dfe19c8673a221fffa878688744c20f7655b8bcf3bbbcae8bd6e8e2d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8db967cffe16c69dbbe89126dd7fa586a2d6064c581e21d00220ce2b415f8e0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa634cddb658b8a4cb5ca0d17a305cffbeabca908b422148bae865c479f89677(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c322571e9ca8e40e708222ea97de12e20fff2fa03af4446e1bcb364753953302(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c64633fa9d59f4b7998a1168a2bea5597fac450d332b5f2165e0658d112693d(
    *,
    max_replicas: jsii.Number,
    min_replicas: jsii.Number,
    cooldown_period: typing.Optional[jsii.Number] = None,
    cpu_utilization: typing.Optional[typing.Union[ComputeRegionAutoscalerAutoscalingPolicyCpuUtilization, typing.Dict[builtins.str, typing.Any]]] = None,
    load_balancing_utilization: typing.Optional[typing.Union[ComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilization, typing.Dict[builtins.str, typing.Any]]] = None,
    metric: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionAutoscalerAutoscalingPolicyMetric, typing.Dict[builtins.str, typing.Any]]]]] = None,
    mode: typing.Optional[builtins.str] = None,
    scale_in_control: typing.Optional[typing.Union[ComputeRegionAutoscalerAutoscalingPolicyScaleInControl, typing.Dict[builtins.str, typing.Any]]] = None,
    scaling_schedules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionAutoscalerAutoscalingPolicyScalingSchedules, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b3f60ceae0a2d22dc098b278e31079650d46d111dc789b92d5b905da17798b0(
    *,
    target: jsii.Number,
    predictive_method: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbcc8d731d469ae8eceb686cde1b4c941245c7ecde88da4e23063eedbbca46f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d92bc396304657163ac7445e5560cdee8fd17ded2e9a3f1d5cf2cf66e88168e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a456d2c88020718b624e51f5058a31a493757c6e6ebaf82ded469a44271fc37(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c48243c8420aa504fba481ffcfd6dd18d0db0e4920f7f069bd9d0f6c68d174c(
    value: typing.Optional[ComputeRegionAutoscalerAutoscalingPolicyCpuUtilization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ebac9df426a8b6710a2b0bcd489fb7af4e3fbb7d4475e0ad4e319ae68d036e6(
    *,
    target: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13e972367427273e31b71a69ea2e2d72f7a636d4acec98c0970eca57f86dd66e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbf8474d7202a234171a1f1d78f3a0604b08e2c5211c7a26a345dd27e2041a3c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16d9d5f39d4eb2d1f385aabe4f19a1d185471e769a717d0a4bc59d15d924025b(
    value: typing.Optional[ComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f20292978fc6562a2fa634e1ca44d457f2df7e255d26b9050d6c0ddf7c1ac43a(
    *,
    name: builtins.str,
    filter: typing.Optional[builtins.str] = None,
    single_instance_assignment: typing.Optional[jsii.Number] = None,
    target: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__032a56967a454e60b9b9deb7dcab1419b518f0a36ae2a0d9f1ee86d01fbd9844(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dda195a1e7f06cd5d4cb7664b8bb01e739d368dab5db52cbeab75c3c3fdc7d3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de6b581df1b2f7ca65736906590cdf8222ea7b63f8c45ef0f29cbf6d9510dae3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d11a955ff93a19bae2a56ec91bf86eff7b4ba2e83d44971cb51d130029fca936(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19183805ed3922745567f51e5546760731cbcc91934e9ab899eec7fa0d31c680(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80cd28636d4c48a760445329ff1a7054f39caef6ec88f8e6c26e9ed6feb39a48(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionAutoscalerAutoscalingPolicyMetric]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e33ec3c9133fdbc6df4b93030bd565d70756abbf52b639222e1b5d78d0e42e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aeabe1d809ac2d5962b865c5f1bc8381d0d8e1e8ae7c3d75d9890e4a423756d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3750b56a9f5f5adc1f82b9ce75c8d1cbf5481e7d3e0c6369b17ba8f8eafab8f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f51a761e367091972fee12085bc080464afcf8ccac9ab658479b441d87a35ca9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99d3ae5e3f362ff9f12e74aac6b93628c170b8464afb6946f7cde432b5ca2a91(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83ba9c3465f8fc4990a3da9ba745edb64b7c26389c70a58c5efebb2bb75cb7ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c25edd6d3caa57070f1a6e61113a6a825c5242889dedb896c37319b26af545b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionAutoscalerAutoscalingPolicyMetric]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f4319c478bf4014d7b61e25fc746063eece384ce259b4e318e5b781ce82e35f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bed7be26d6a19648c218f601b7528c7fac17dea33d15742fb4b6f7d792e02e8e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionAutoscalerAutoscalingPolicyMetric, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__546be3397322c6914fc30a34a224264b062ee1afc502780419af74604bd49280(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionAutoscalerAutoscalingPolicyScalingSchedules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f477025412ad92f154014d917d444f6d300e2da9c7eee4af22efefc7ec24d5d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0496c5e746fbb2ddab5f7cc0a2e16e201a5e6ff5c1c89d264954a2c55eaf524(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2affda891dbcdf55a2dc7874e5fa2938059d78e13a8e41f0b4753a1824e1d1ad(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2523f95c1db3119d17db74576cb6bc70d0515e3ea071243459d5f2e9a3230eb2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__031b3ac6e83cdf1dec5f1b4690d841531aedffb9de14265be60eb7db18d8ea1a(
    value: typing.Optional[ComputeRegionAutoscalerAutoscalingPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79e35adef032acd4f4ec7719c2ec2acecba56bd16ef77fb8e0cbfad82873a7eb(
    *,
    max_scaled_in_replicas: typing.Optional[typing.Union[ComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas, typing.Dict[builtins.str, typing.Any]]] = None,
    time_window_sec: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78b93ce2da3e166bb8c7145e4a7d720c6cad673bb4f95663493f3d65a8d2f686(
    *,
    fixed: typing.Optional[jsii.Number] = None,
    percent: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27dc34180d42191e71dfc26f165bff7dfee6957035f2c3e3b2afef5fc95b2040(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16f7f960848dde14d7dd6022526dc1f4ee9a5bc537d6d127da318ff221805345(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__583ea2eb7a4c8436e4c358d9ad89d28c2003a101fd7bf9b32e6b6436be1b2bf2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c27b640520965c2c7bc2d0700f9f3218fcf06eb45662a74789246ef26f71d7b4(
    value: typing.Optional[ComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac965d1958469b8079978366414892ddfd6277be0925f8fd9fbfc084e1699501(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7ba8ed1d9e83ae8f787f11de65a8cbb25dcb3bfe3710437e880a24055f20d94(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7405f2e929b3286bc837689af2ae0525437a300abba7e0fd3591694d2ffaeca(
    value: typing.Optional[ComputeRegionAutoscalerAutoscalingPolicyScaleInControl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dc36400f995df895c2f745c86a492ade72505f249baeed5b3dbd45fca444dd5(
    *,
    duration_sec: jsii.Number,
    min_required_replicas: jsii.Number,
    name: builtins.str,
    schedule: builtins.str,
    description: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    time_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__493b454d9dc1bfa8060e057d64bb09b06fa8fe7ec69c72ab5a7c61d9bc77cb4d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__862aaec2130f8409d7dceac00e02e9951ef6a7309d38c45c70735d0ddb91c218(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b415bcc77ffba17b52f8a5bd8c23601ef58e73e652b6e44de05d28b0d9c36dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad50c7d7e09a8ada125eebbc2987ff9fcd97a4fb7f88a872c8e20a0100166492(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbe15a73ab3f2584587d5637f2a66169b6ef6110faf603560a528e5b6f2d1907(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2bd61bbdc335d5406571eb9a2532c2810c496ee3bc09d6252d159ce6de9342c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionAutoscalerAutoscalingPolicyScalingSchedules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc58b5831473f8e46fcc2339f0222f13cfa0444a102c5cc371a470a28364722e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15437af29cc78606fcd87eec9d176c55df049b8788e12da3934ae2ca0df01e81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__968d4e5a3215abbc926b3eaed1ca4893f66888336b0a361298685f9b7c9283a8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__370c3d13d1fa4cdfe5523efe752a7b004b9c6f2eb0bdb0f19b72fceb7368ba5d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a41a626eeacd181d0c8f88e2a3abc43fe5554137ae6d3b9517274ce45e5a64ee(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95270b26674f3885fc7f1e2d0b6e3647d3f15f2292a5b150e565f8fd16abf5b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f154806c45bb59f09d1e46b53eb551d61ff7e849b0b78fac9cadd131f75da75b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4ceff085a961e972891d797539a21053113e23acc9ff445a3d887faaa1f2907(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4226f2a479ad314bea1836443dbc7cff31f2f2626eca9a4c9c27bfae0c72e3d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionAutoscalerAutoscalingPolicyScalingSchedules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a15216cab526287c2b03fcca0d0e4366e22b85dc55a565f18ba9b8009de6a35(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    autoscaling_policy: typing.Union[ComputeRegionAutoscalerAutoscalingPolicy, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    target: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ComputeRegionAutoscalerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf9653a06a363522c7f880573986428c7c034dec3206736df5840149a4108a8(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34188c48da12b84a190a93216eedc1c288d84619cec979f4fc5d66de96efd76e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b0df43573c6b503020f03de5ae2e68614c139c0f918f7d138327467279da083(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d208549257e0dbc90c0e2c21858db3aa2e82560b1b54faf94db8241bf3ff3e0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b02826843e4c5adb5488bfca876af85a7e896675f4616588012003b4fe130f3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efdf5b05ea15d91f582640703654d7cc338bb7fa2710abf8e1c8cc26009a821a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionAutoscalerTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
