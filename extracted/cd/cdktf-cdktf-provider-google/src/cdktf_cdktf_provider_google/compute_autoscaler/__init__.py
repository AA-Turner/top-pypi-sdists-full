r'''
# `google_compute_autoscaler`

Refer to the Terraform Registry for docs: [`google_compute_autoscaler`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler).
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


class ComputeAutoscaler(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeAutoscaler.ComputeAutoscaler",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler google_compute_autoscaler}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        autoscaling_policy: typing.Union["ComputeAutoscalerAutoscalingPolicy", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        target: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ComputeAutoscalerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        zone: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler google_compute_autoscaler} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param autoscaling_policy: autoscaling_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#autoscaling_policy ComputeAutoscaler#autoscaling_policy}
        :param name: Name of the resource. The name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#name ComputeAutoscaler#name}
        :param target: URL of the managed instance group that this autoscaler will scale. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#target ComputeAutoscaler#target}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#description ComputeAutoscaler#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#id ComputeAutoscaler#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#project ComputeAutoscaler#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#timeouts ComputeAutoscaler#timeouts}
        :param zone: URL of the zone where the instance group resides. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#zone ComputeAutoscaler#zone}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c944c4f9c9040efc4daa5a0c3eac7ff2033f7c5f1607b0b2a2b458a8dd45c718)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeAutoscalerConfig(
            autoscaling_policy=autoscaling_policy,
            name=name,
            target=target,
            description=description,
            id=id,
            project=project,
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
        '''Generates CDKTF code for importing a ComputeAutoscaler resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeAutoscaler to import.
        :param import_from_id: The id of the existing ComputeAutoscaler that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeAutoscaler to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd6497cf6f40f0be8306eed35a816a092e28de6534bfabca12ae9e8abc3ecb1c)
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
        cpu_utilization: typing.Optional[typing.Union["ComputeAutoscalerAutoscalingPolicyCpuUtilization", typing.Dict[builtins.str, typing.Any]]] = None,
        load_balancing_utilization: typing.Optional[typing.Union["ComputeAutoscalerAutoscalingPolicyLoadBalancingUtilization", typing.Dict[builtins.str, typing.Any]]] = None,
        metric: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeAutoscalerAutoscalingPolicyMetric", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mode: typing.Optional[builtins.str] = None,
        scale_in_control: typing.Optional[typing.Union["ComputeAutoscalerAutoscalingPolicyScaleInControl", typing.Dict[builtins.str, typing.Any]]] = None,
        scaling_schedules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeAutoscalerAutoscalingPolicyScalingSchedules", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param max_replicas: The maximum number of instances that the autoscaler can scale up to. This is required when creating or updating an autoscaler. The maximum number of replicas should not be lower than minimal number of replicas. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#max_replicas ComputeAutoscaler#max_replicas}
        :param min_replicas: The minimum number of replicas that the autoscaler can scale down to. This cannot be less than 0. If not provided, autoscaler will choose a default value depending on maximum number of instances allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#min_replicas ComputeAutoscaler#min_replicas}
        :param cooldown_period: The number of seconds that the autoscaler should wait before it starts collecting information from a new instance. This prevents the autoscaler from collecting information when the instance is initializing, during which the collected usage would not be reliable. The default time autoscaler waits is 60 seconds. Virtual machine initialization times might vary because of numerous factors. We recommend that you test how long an instance may take to initialize. To do this, create an instance and time the startup process. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#cooldown_period ComputeAutoscaler#cooldown_period}
        :param cpu_utilization: cpu_utilization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#cpu_utilization ComputeAutoscaler#cpu_utilization}
        :param load_balancing_utilization: load_balancing_utilization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#load_balancing_utilization ComputeAutoscaler#load_balancing_utilization}
        :param metric: metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#metric ComputeAutoscaler#metric}
        :param mode: Defines operating mode for this policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#mode ComputeAutoscaler#mode}
        :param scale_in_control: scale_in_control block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#scale_in_control ComputeAutoscaler#scale_in_control}
        :param scaling_schedules: scaling_schedules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#scaling_schedules ComputeAutoscaler#scaling_schedules}
        '''
        value = ComputeAutoscalerAutoscalingPolicy(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#create ComputeAutoscaler#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#delete ComputeAutoscaler#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#update ComputeAutoscaler#update}.
        '''
        value = ComputeAutoscalerTimeouts(create=create, delete=delete, update=update)

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
    def autoscaling_policy(self) -> "ComputeAutoscalerAutoscalingPolicyOutputReference":
        return typing.cast("ComputeAutoscalerAutoscalingPolicyOutputReference", jsii.get(self, "autoscalingPolicy"))

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
    def timeouts(self) -> "ComputeAutoscalerTimeoutsOutputReference":
        return typing.cast("ComputeAutoscalerTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingPolicyInput")
    def autoscaling_policy_input(
        self,
    ) -> typing.Optional["ComputeAutoscalerAutoscalingPolicy"]:
        return typing.cast(typing.Optional["ComputeAutoscalerAutoscalingPolicy"], jsii.get(self, "autoscalingPolicyInput"))

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
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeAutoscalerTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeAutoscalerTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__4ba0702c25783cf7f4cfa37a8d267f9109d129303053c997b86861ab1be8f725)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1bd621335279e6df74c52a001824ba799741ea8da4696f367a6b78310f7b012)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7db042de54be229b55f9b3e4bd587b5adf43d15dd601fe3a09aa29ab55b37a32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b842fa7791a579d8f78c28ac9e878ba3cea9d2fa5974960896813af124eb8f89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e02b40789766310e7fcaf1a858806be0ea69d2fb2a0c158e18eed4b4c4d2824f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd81be4c4f44d2b571321fd0908d63e5168e4e088c2e6fd394a4ecef08d82baa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeAutoscaler.ComputeAutoscalerAutoscalingPolicy",
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
class ComputeAutoscalerAutoscalingPolicy:
    def __init__(
        self,
        *,
        max_replicas: jsii.Number,
        min_replicas: jsii.Number,
        cooldown_period: typing.Optional[jsii.Number] = None,
        cpu_utilization: typing.Optional[typing.Union["ComputeAutoscalerAutoscalingPolicyCpuUtilization", typing.Dict[builtins.str, typing.Any]]] = None,
        load_balancing_utilization: typing.Optional[typing.Union["ComputeAutoscalerAutoscalingPolicyLoadBalancingUtilization", typing.Dict[builtins.str, typing.Any]]] = None,
        metric: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeAutoscalerAutoscalingPolicyMetric", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mode: typing.Optional[builtins.str] = None,
        scale_in_control: typing.Optional[typing.Union["ComputeAutoscalerAutoscalingPolicyScaleInControl", typing.Dict[builtins.str, typing.Any]]] = None,
        scaling_schedules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeAutoscalerAutoscalingPolicyScalingSchedules", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param max_replicas: The maximum number of instances that the autoscaler can scale up to. This is required when creating or updating an autoscaler. The maximum number of replicas should not be lower than minimal number of replicas. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#max_replicas ComputeAutoscaler#max_replicas}
        :param min_replicas: The minimum number of replicas that the autoscaler can scale down to. This cannot be less than 0. If not provided, autoscaler will choose a default value depending on maximum number of instances allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#min_replicas ComputeAutoscaler#min_replicas}
        :param cooldown_period: The number of seconds that the autoscaler should wait before it starts collecting information from a new instance. This prevents the autoscaler from collecting information when the instance is initializing, during which the collected usage would not be reliable. The default time autoscaler waits is 60 seconds. Virtual machine initialization times might vary because of numerous factors. We recommend that you test how long an instance may take to initialize. To do this, create an instance and time the startup process. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#cooldown_period ComputeAutoscaler#cooldown_period}
        :param cpu_utilization: cpu_utilization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#cpu_utilization ComputeAutoscaler#cpu_utilization}
        :param load_balancing_utilization: load_balancing_utilization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#load_balancing_utilization ComputeAutoscaler#load_balancing_utilization}
        :param metric: metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#metric ComputeAutoscaler#metric}
        :param mode: Defines operating mode for this policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#mode ComputeAutoscaler#mode}
        :param scale_in_control: scale_in_control block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#scale_in_control ComputeAutoscaler#scale_in_control}
        :param scaling_schedules: scaling_schedules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#scaling_schedules ComputeAutoscaler#scaling_schedules}
        '''
        if isinstance(cpu_utilization, dict):
            cpu_utilization = ComputeAutoscalerAutoscalingPolicyCpuUtilization(**cpu_utilization)
        if isinstance(load_balancing_utilization, dict):
            load_balancing_utilization = ComputeAutoscalerAutoscalingPolicyLoadBalancingUtilization(**load_balancing_utilization)
        if isinstance(scale_in_control, dict):
            scale_in_control = ComputeAutoscalerAutoscalingPolicyScaleInControl(**scale_in_control)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abbc6799206835ee89755b54b8f53ef5962ddd0a7ce52afaa184409daaf9da00)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#max_replicas ComputeAutoscaler#max_replicas}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#min_replicas ComputeAutoscaler#min_replicas}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#cooldown_period ComputeAutoscaler#cooldown_period}
        '''
        result = self._values.get("cooldown_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cpu_utilization(
        self,
    ) -> typing.Optional["ComputeAutoscalerAutoscalingPolicyCpuUtilization"]:
        '''cpu_utilization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#cpu_utilization ComputeAutoscaler#cpu_utilization}
        '''
        result = self._values.get("cpu_utilization")
        return typing.cast(typing.Optional["ComputeAutoscalerAutoscalingPolicyCpuUtilization"], result)

    @builtins.property
    def load_balancing_utilization(
        self,
    ) -> typing.Optional["ComputeAutoscalerAutoscalingPolicyLoadBalancingUtilization"]:
        '''load_balancing_utilization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#load_balancing_utilization ComputeAutoscaler#load_balancing_utilization}
        '''
        result = self._values.get("load_balancing_utilization")
        return typing.cast(typing.Optional["ComputeAutoscalerAutoscalingPolicyLoadBalancingUtilization"], result)

    @builtins.property
    def metric(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeAutoscalerAutoscalingPolicyMetric"]]]:
        '''metric block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#metric ComputeAutoscaler#metric}
        '''
        result = self._values.get("metric")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeAutoscalerAutoscalingPolicyMetric"]]], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Defines operating mode for this policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#mode ComputeAutoscaler#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scale_in_control(
        self,
    ) -> typing.Optional["ComputeAutoscalerAutoscalingPolicyScaleInControl"]:
        '''scale_in_control block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#scale_in_control ComputeAutoscaler#scale_in_control}
        '''
        result = self._values.get("scale_in_control")
        return typing.cast(typing.Optional["ComputeAutoscalerAutoscalingPolicyScaleInControl"], result)

    @builtins.property
    def scaling_schedules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeAutoscalerAutoscalingPolicyScalingSchedules"]]]:
        '''scaling_schedules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#scaling_schedules ComputeAutoscaler#scaling_schedules}
        '''
        result = self._values.get("scaling_schedules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeAutoscalerAutoscalingPolicyScalingSchedules"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeAutoscalerAutoscalingPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeAutoscaler.ComputeAutoscalerAutoscalingPolicyCpuUtilization",
    jsii_struct_bases=[],
    name_mapping={"target": "target", "predictive_method": "predictiveMethod"},
)
class ComputeAutoscalerAutoscalingPolicyCpuUtilization:
    def __init__(
        self,
        *,
        target: jsii.Number,
        predictive_method: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target: The target CPU utilization that the autoscaler should maintain. Must be a float value in the range (0, 1]. If not specified, the default is 0.6. If the CPU level is below the target utilization, the autoscaler scales down the number of instances until it reaches the minimum number of instances you specified or until the average CPU of your instances reaches the target utilization. If the average CPU is above the target utilization, the autoscaler scales up until it reaches the maximum number of instances you specified or until the average utilization reaches the target utilization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#target ComputeAutoscaler#target}
        :param predictive_method: Indicates whether predictive autoscaling based on CPU metric is enabled. Valid values are:. - NONE (default). No predictive method is used. The autoscaler scales the group to meet current demand based on real-time metrics. - OPTIMIZE_AVAILABILITY. Predictive autoscaling improves availability by monitoring daily and weekly load patterns and scaling out ahead of anticipated demand. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#predictive_method ComputeAutoscaler#predictive_method}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c736170ebd225e5a151cc447e73b3a5002af737667c1e31b35ca051db5a76a0a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#target ComputeAutoscaler#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def predictive_method(self) -> typing.Optional[builtins.str]:
        '''Indicates whether predictive autoscaling based on CPU metric is enabled. Valid values are:.

        - NONE (default). No predictive method is used. The autoscaler scales the group to meet current demand based on real-time metrics.
        - OPTIMIZE_AVAILABILITY. Predictive autoscaling improves availability by monitoring daily and weekly load patterns and scaling out ahead of anticipated demand.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#predictive_method ComputeAutoscaler#predictive_method}
        '''
        result = self._values.get("predictive_method")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeAutoscalerAutoscalingPolicyCpuUtilization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeAutoscalerAutoscalingPolicyCpuUtilizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeAutoscaler.ComputeAutoscalerAutoscalingPolicyCpuUtilizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb35a4fd48b3a12ece36b97e16c6167abd6700bec4b6c12a9fcfef37f3466899)
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
            type_hints = typing.get_type_hints(_typecheckingstub__11d571411a3f67344f6029c9ec7ba9c754320c13abe48c66cd3945af32a3c2c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "predictiveMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "target"))

    @target.setter
    def target(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aec8afd2ffe299581036e52a15d3716beb2d7a26ed4026b09c396a88c7a642bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeAutoscalerAutoscalingPolicyCpuUtilization]:
        return typing.cast(typing.Optional[ComputeAutoscalerAutoscalingPolicyCpuUtilization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeAutoscalerAutoscalingPolicyCpuUtilization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e69c75afdd540c138deadd8dc28fa052e83e3c2ff88e46ea89bb382293abf7bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeAutoscaler.ComputeAutoscalerAutoscalingPolicyLoadBalancingUtilization",
    jsii_struct_bases=[],
    name_mapping={"target": "target"},
)
class ComputeAutoscalerAutoscalingPolicyLoadBalancingUtilization:
    def __init__(self, *, target: jsii.Number) -> None:
        '''
        :param target: Fraction of backend capacity utilization (set in HTTP(s) load balancing configuration) that autoscaler should maintain. Must be a positive float value. If not defined, the default is 0.8. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#target ComputeAutoscaler#target}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0b5f1359092d6644afc8f2033cbb16e49fb566fad7b779e96bbc8fa6f8e164e)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target": target,
        }

    @builtins.property
    def target(self) -> jsii.Number:
        '''Fraction of backend capacity utilization (set in HTTP(s) load balancing configuration) that autoscaler should maintain.

        Must
        be a positive float value. If not defined, the default is 0.8.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#target ComputeAutoscaler#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeAutoscalerAutoscalingPolicyLoadBalancingUtilization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeAutoscalerAutoscalingPolicyLoadBalancingUtilizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeAutoscaler.ComputeAutoscalerAutoscalingPolicyLoadBalancingUtilizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7d05f0241096e653b221910fb397ef30562c197696f2f53eb120d1a94c79886)
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
            type_hints = typing.get_type_hints(_typecheckingstub__383d254bfdcbf0dba800b6344e69afcb67d52daff89f58db4fb2bdc40ad6bda2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeAutoscalerAutoscalingPolicyLoadBalancingUtilization]:
        return typing.cast(typing.Optional[ComputeAutoscalerAutoscalingPolicyLoadBalancingUtilization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeAutoscalerAutoscalingPolicyLoadBalancingUtilization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c825cba1932c5dd39b6dcddf4b3d9098ae087652c70c0d58db36384fefd34151)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeAutoscaler.ComputeAutoscalerAutoscalingPolicyMetric",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "filter": "filter",
        "single_instance_assignment": "singleInstanceAssignment",
        "target": "target",
        "type": "type",
    },
)
class ComputeAutoscalerAutoscalingPolicyMetric:
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
        :param name: The identifier (type) of the Stackdriver Monitoring metric. The metric cannot have negative values. The metric must have a value type of INT64 or DOUBLE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#name ComputeAutoscaler#name}
        :param filter: A filter string to be used as the filter string for a Stackdriver Monitoring TimeSeries.list API call. This filter is used to select a specific TimeSeries for the purpose of autoscaling and to determine whether the metric is exporting per-instance or per-group data. You can only use the AND operator for joining selectors. You can only use direct equality comparison operator (=) without any functions for each selector. You can specify the metric in both the filter string and in the metric field. However, if specified in both places, the metric must be identical. The monitored resource type determines what kind of values are expected for the metric. If it is a gce_instance, the autoscaler expects the metric to include a separate TimeSeries for each instance in a group. In such a case, you cannot filter on resource labels. If the resource type is any other value, the autoscaler expects this metric to contain values that apply to the entire autoscaled instance group and resource label filtering can be performed to point autoscaler at the correct TimeSeries to scale upon. This is called a per-group metric for the purpose of autoscaling. If not specified, the type defaults to gce_instance. You should provide a filter that is selective enough to pick just one TimeSeries for the autoscaled group or for each of the instances (if you are using gce_instance resource type). If multiple TimeSeries are returned upon the query execution, the autoscaler will sum their respective values to obtain its scaling value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#filter ComputeAutoscaler#filter}
        :param single_instance_assignment: If scaling is based on a per-group metric value that represents the total amount of work to be done or resource usage, set this value to an amount assigned for a single instance of the scaled group. The autoscaler will keep the number of instances proportional to the value of this metric, the metric itself should not change value due to group resizing. For example, a good metric to use with the target is 'pubsub.googleapis.com/subscription/num_undelivered_messages' or a custom metric exporting the total number of requests coming to your instances. A bad example would be a metric exporting an average or median latency, since this value can't include a chunk assignable to a single instance, it could be better used with utilization_target instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#single_instance_assignment ComputeAutoscaler#single_instance_assignment}
        :param target: The target value of the metric that autoscaler should maintain. This must be a positive value. A utilization metric scales number of virtual machines handling requests to increase or decrease proportionally to the metric. For example, a good metric to use as a utilizationTarget is www.googleapis.com/compute/instance/network/received_bytes_count. The autoscaler will work to keep this value constant for each of the instances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#target ComputeAutoscaler#target}
        :param type: Defines how target utilization value is expressed for a Stackdriver Monitoring metric. Possible values: ["GAUGE", "DELTA_PER_SECOND", "DELTA_PER_MINUTE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#type ComputeAutoscaler#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5531a24a9547b0eedb1c11c8cd2dc2f4e2427bdb549c035636e192b732ba1e21)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#name ComputeAutoscaler#name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#filter ComputeAutoscaler#filter}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#single_instance_assignment ComputeAutoscaler#single_instance_assignment}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#target ComputeAutoscaler#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Defines how target utilization value is expressed for a Stackdriver Monitoring metric. Possible values: ["GAUGE", "DELTA_PER_SECOND", "DELTA_PER_MINUTE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#type ComputeAutoscaler#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeAutoscalerAutoscalingPolicyMetric(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeAutoscalerAutoscalingPolicyMetricList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeAutoscaler.ComputeAutoscalerAutoscalingPolicyMetricList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f611854357b8f9e8cb1c47e2dee6ac38a01b49cb8a7ed2e3e4457ee596bb496d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeAutoscalerAutoscalingPolicyMetricOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09fdf97dda89423dac11d73fd778a6959a192f1cb07308b849c79b86d03509d8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeAutoscalerAutoscalingPolicyMetricOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__703631f6494e4b205c38484a82bfc424eab31b4df3fe9c051fcd2196126aac89)
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
            type_hints = typing.get_type_hints(_typecheckingstub__afce9ac8aeaab066ba71675ad77d2918d953321a0c74868c665d08f19be63304)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4087cd5e06e718c51fc510076cf7fa2404ca2eeab6043a08e6879b71d8d907d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeAutoscalerAutoscalingPolicyMetric]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeAutoscalerAutoscalingPolicyMetric]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeAutoscalerAutoscalingPolicyMetric]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59ef24ae1abdc16689d8e36b069a0cea559ef0a6dc40adb09bafde164d6c74c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeAutoscalerAutoscalingPolicyMetricOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeAutoscaler.ComputeAutoscalerAutoscalingPolicyMetricOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__95e4de9fd6bdf4dcf072a60c418841607472ce2b014df6b77fe984b8fdeb2d8d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0103fef0f4952cd44047ad7fd390da6ed8c12cf37e202532678009ae70f7404e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b631eea38e23694a015cc1ec9185e44f79065d295dc930fb294a9e2602dadb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="singleInstanceAssignment")
    def single_instance_assignment(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "singleInstanceAssignment"))

    @single_instance_assignment.setter
    def single_instance_assignment(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__520a2d50e4fc23e185f2795f96969e1692fc5a55b92f2020b2671880cfb23152)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "singleInstanceAssignment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "target"))

    @target.setter
    def target(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__142878c0cee319f932a6b25a7654a94ceeae3a380aaf6515dfb376483a631f69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85bb99f2d320c98aa4699a10c602175fe6a7a1c79e6e5fba0a81569f65bdc72b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeAutoscalerAutoscalingPolicyMetric]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeAutoscalerAutoscalingPolicyMetric]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeAutoscalerAutoscalingPolicyMetric]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9019ef0e0061133aff260955b60fc6faeaef0455336a4843b8f13abec13a51b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeAutoscalerAutoscalingPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeAutoscaler.ComputeAutoscalerAutoscalingPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__14d5248ca777b823be7e9723dfb626fd826b2f9490cc1aacb70cb2778ca8330f)
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
        :param target: The target CPU utilization that the autoscaler should maintain. Must be a float value in the range (0, 1]. If not specified, the default is 0.6. If the CPU level is below the target utilization, the autoscaler scales down the number of instances until it reaches the minimum number of instances you specified or until the average CPU of your instances reaches the target utilization. If the average CPU is above the target utilization, the autoscaler scales up until it reaches the maximum number of instances you specified or until the average utilization reaches the target utilization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#target ComputeAutoscaler#target}
        :param predictive_method: Indicates whether predictive autoscaling based on CPU metric is enabled. Valid values are:. - NONE (default). No predictive method is used. The autoscaler scales the group to meet current demand based on real-time metrics. - OPTIMIZE_AVAILABILITY. Predictive autoscaling improves availability by monitoring daily and weekly load patterns and scaling out ahead of anticipated demand. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#predictive_method ComputeAutoscaler#predictive_method}
        '''
        value = ComputeAutoscalerAutoscalingPolicyCpuUtilization(
            target=target, predictive_method=predictive_method
        )

        return typing.cast(None, jsii.invoke(self, "putCpuUtilization", [value]))

    @jsii.member(jsii_name="putLoadBalancingUtilization")
    def put_load_balancing_utilization(self, *, target: jsii.Number) -> None:
        '''
        :param target: Fraction of backend capacity utilization (set in HTTP(s) load balancing configuration) that autoscaler should maintain. Must be a positive float value. If not defined, the default is 0.8. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#target ComputeAutoscaler#target}
        '''
        value = ComputeAutoscalerAutoscalingPolicyLoadBalancingUtilization(
            target=target
        )

        return typing.cast(None, jsii.invoke(self, "putLoadBalancingUtilization", [value]))

    @jsii.member(jsii_name="putMetric")
    def put_metric(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeAutoscalerAutoscalingPolicyMetric, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__960e065c9c457d03a68b456b5adecd1814223880a0aaab9e9fd4fb624cbdfc07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMetric", [value]))

    @jsii.member(jsii_name="putScaleInControl")
    def put_scale_in_control(
        self,
        *,
        max_scaled_in_replicas: typing.Optional[typing.Union["ComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas", typing.Dict[builtins.str, typing.Any]]] = None,
        time_window_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_scaled_in_replicas: max_scaled_in_replicas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#max_scaled_in_replicas ComputeAutoscaler#max_scaled_in_replicas}
        :param time_window_sec: How long back autoscaling should look when computing recommendations to include directives regarding slower scale down, as described above. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#time_window_sec ComputeAutoscaler#time_window_sec}
        '''
        value = ComputeAutoscalerAutoscalingPolicyScaleInControl(
            max_scaled_in_replicas=max_scaled_in_replicas,
            time_window_sec=time_window_sec,
        )

        return typing.cast(None, jsii.invoke(self, "putScaleInControl", [value]))

    @jsii.member(jsii_name="putScalingSchedules")
    def put_scaling_schedules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeAutoscalerAutoscalingPolicyScalingSchedules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9c8e662a9b35c39510dbd28a9eb825c79300ef2a474b9d8543e1ab7de6c8b5e)
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
    ) -> ComputeAutoscalerAutoscalingPolicyCpuUtilizationOutputReference:
        return typing.cast(ComputeAutoscalerAutoscalingPolicyCpuUtilizationOutputReference, jsii.get(self, "cpuUtilization"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancingUtilization")
    def load_balancing_utilization(
        self,
    ) -> ComputeAutoscalerAutoscalingPolicyLoadBalancingUtilizationOutputReference:
        return typing.cast(ComputeAutoscalerAutoscalingPolicyLoadBalancingUtilizationOutputReference, jsii.get(self, "loadBalancingUtilization"))

    @builtins.property
    @jsii.member(jsii_name="metric")
    def metric(self) -> ComputeAutoscalerAutoscalingPolicyMetricList:
        return typing.cast(ComputeAutoscalerAutoscalingPolicyMetricList, jsii.get(self, "metric"))

    @builtins.property
    @jsii.member(jsii_name="scaleInControl")
    def scale_in_control(
        self,
    ) -> "ComputeAutoscalerAutoscalingPolicyScaleInControlOutputReference":
        return typing.cast("ComputeAutoscalerAutoscalingPolicyScaleInControlOutputReference", jsii.get(self, "scaleInControl"))

    @builtins.property
    @jsii.member(jsii_name="scalingSchedules")
    def scaling_schedules(
        self,
    ) -> "ComputeAutoscalerAutoscalingPolicyScalingSchedulesList":
        return typing.cast("ComputeAutoscalerAutoscalingPolicyScalingSchedulesList", jsii.get(self, "scalingSchedules"))

    @builtins.property
    @jsii.member(jsii_name="cooldownPeriodInput")
    def cooldown_period_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cooldownPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuUtilizationInput")
    def cpu_utilization_input(
        self,
    ) -> typing.Optional[ComputeAutoscalerAutoscalingPolicyCpuUtilization]:
        return typing.cast(typing.Optional[ComputeAutoscalerAutoscalingPolicyCpuUtilization], jsii.get(self, "cpuUtilizationInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancingUtilizationInput")
    def load_balancing_utilization_input(
        self,
    ) -> typing.Optional[ComputeAutoscalerAutoscalingPolicyLoadBalancingUtilization]:
        return typing.cast(typing.Optional[ComputeAutoscalerAutoscalingPolicyLoadBalancingUtilization], jsii.get(self, "loadBalancingUtilizationInput"))

    @builtins.property
    @jsii.member(jsii_name="maxReplicasInput")
    def max_replicas_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxReplicasInput"))

    @builtins.property
    @jsii.member(jsii_name="metricInput")
    def metric_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeAutoscalerAutoscalingPolicyMetric]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeAutoscalerAutoscalingPolicyMetric]]], jsii.get(self, "metricInput"))

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
    ) -> typing.Optional["ComputeAutoscalerAutoscalingPolicyScaleInControl"]:
        return typing.cast(typing.Optional["ComputeAutoscalerAutoscalingPolicyScaleInControl"], jsii.get(self, "scaleInControlInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingSchedulesInput")
    def scaling_schedules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeAutoscalerAutoscalingPolicyScalingSchedules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeAutoscalerAutoscalingPolicyScalingSchedules"]]], jsii.get(self, "scalingSchedulesInput"))

    @builtins.property
    @jsii.member(jsii_name="cooldownPeriod")
    def cooldown_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cooldownPeriod"))

    @cooldown_period.setter
    def cooldown_period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2427c47dc19a01b1a9c8a189a90326114c6883a53f2e7ec5f8d9f58dd0889b85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cooldownPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxReplicas")
    def max_replicas(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxReplicas"))

    @max_replicas.setter
    def max_replicas(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bf8636e2207435741af21cd27ac8f0e4df07f4941bf4734d58d2a089dbc5a61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxReplicas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minReplicas")
    def min_replicas(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minReplicas"))

    @min_replicas.setter
    def min_replicas(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__debaa0433ee89694004486068d1a959eb9b0b0dc1f71e87287ea49f30781cb16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minReplicas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0abacae6052425bd04693bbad823a53c387b25f968e3f4d12b11b70b66ee6484)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeAutoscalerAutoscalingPolicy]:
        return typing.cast(typing.Optional[ComputeAutoscalerAutoscalingPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeAutoscalerAutoscalingPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a27c32ec9a2e9524fb9108dfc182820f7f4cdb8309f9da60ad28dd45351396f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeAutoscaler.ComputeAutoscalerAutoscalingPolicyScaleInControl",
    jsii_struct_bases=[],
    name_mapping={
        "max_scaled_in_replicas": "maxScaledInReplicas",
        "time_window_sec": "timeWindowSec",
    },
)
class ComputeAutoscalerAutoscalingPolicyScaleInControl:
    def __init__(
        self,
        *,
        max_scaled_in_replicas: typing.Optional[typing.Union["ComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas", typing.Dict[builtins.str, typing.Any]]] = None,
        time_window_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_scaled_in_replicas: max_scaled_in_replicas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#max_scaled_in_replicas ComputeAutoscaler#max_scaled_in_replicas}
        :param time_window_sec: How long back autoscaling should look when computing recommendations to include directives regarding slower scale down, as described above. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#time_window_sec ComputeAutoscaler#time_window_sec}
        '''
        if isinstance(max_scaled_in_replicas, dict):
            max_scaled_in_replicas = ComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas(**max_scaled_in_replicas)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__891bddecddf6e4b8ffcf43108ef67720a7f1f472a6bdb8b717c13a3a9d124564)
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
    ) -> typing.Optional["ComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas"]:
        '''max_scaled_in_replicas block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#max_scaled_in_replicas ComputeAutoscaler#max_scaled_in_replicas}
        '''
        result = self._values.get("max_scaled_in_replicas")
        return typing.cast(typing.Optional["ComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas"], result)

    @builtins.property
    def time_window_sec(self) -> typing.Optional[jsii.Number]:
        '''How long back autoscaling should look when computing recommendations to include directives regarding slower scale down, as described above.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#time_window_sec ComputeAutoscaler#time_window_sec}
        '''
        result = self._values.get("time_window_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeAutoscalerAutoscalingPolicyScaleInControl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeAutoscaler.ComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas",
    jsii_struct_bases=[],
    name_mapping={"fixed": "fixed", "percent": "percent"},
)
class ComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas:
    def __init__(
        self,
        *,
        fixed: typing.Optional[jsii.Number] = None,
        percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fixed: Specifies a fixed number of VM instances. This must be a positive integer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#fixed ComputeAutoscaler#fixed}
        :param percent: Specifies a percentage of instances between 0 to 100%, inclusive. For example, specify 80 for 80%. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#percent ComputeAutoscaler#percent}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f596228190b816e4515aa6ff62d0791ec2107f1213c1b46e7b09ea7e8c31aae0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#fixed ComputeAutoscaler#fixed}
        '''
        result = self._values.get("fixed")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def percent(self) -> typing.Optional[jsii.Number]:
        '''Specifies a percentage of instances between 0 to 100%, inclusive. For example, specify 80 for 80%.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#percent ComputeAutoscaler#percent}
        '''
        result = self._values.get("percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicasOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeAutoscaler.ComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicasOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c6def0a48dd5041189fdca4124e74b995c21f8f8c5f32b5e2cd12b5ab20ede1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2f11801246b22d6ba41a365d232a9c85abc384350a4f5fc8ee5b3a2f9f6b30d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="percent")
    def percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percent"))

    @percent.setter
    def percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ccaf375218b9917a1923392d3a99f86dba390cef71a0afd70ec7a85a27fc1c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas]:
        return typing.cast(typing.Optional[ComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3c0ea43a99d6f28c2fc1c907a67305b3b3d42990fe13fa857b9a24760f913d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeAutoscalerAutoscalingPolicyScaleInControlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeAutoscaler.ComputeAutoscalerAutoscalingPolicyScaleInControlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9db3acbdccc1e4c5f454bdfef02d3456d6056b38bdb49a0dc6ef6e2e54d8e796)
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
        :param fixed: Specifies a fixed number of VM instances. This must be a positive integer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#fixed ComputeAutoscaler#fixed}
        :param percent: Specifies a percentage of instances between 0 to 100%, inclusive. For example, specify 80 for 80%. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#percent ComputeAutoscaler#percent}
        '''
        value = ComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas(
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
    ) -> ComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicasOutputReference:
        return typing.cast(ComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicasOutputReference, jsii.get(self, "maxScaledInReplicas"))

    @builtins.property
    @jsii.member(jsii_name="maxScaledInReplicasInput")
    def max_scaled_in_replicas_input(
        self,
    ) -> typing.Optional[ComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas]:
        return typing.cast(typing.Optional[ComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas], jsii.get(self, "maxScaledInReplicasInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__8cfceafb0726ae5943ef4ec9f83634a325cc1a48e5d99560176b6d8954a85f28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeWindowSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeAutoscalerAutoscalingPolicyScaleInControl]:
        return typing.cast(typing.Optional[ComputeAutoscalerAutoscalingPolicyScaleInControl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeAutoscalerAutoscalingPolicyScaleInControl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dad9eb3f728300a327d06e51c0fd38cbca9b6bb1a87593edcf1e6ebdc0832bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeAutoscaler.ComputeAutoscalerAutoscalingPolicyScalingSchedules",
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
class ComputeAutoscalerAutoscalingPolicyScalingSchedules:
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
        :param duration_sec: The duration of time intervals (in seconds) for which this scaling schedule will be running. The minimum allowed value is 300. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#duration_sec ComputeAutoscaler#duration_sec}
        :param min_required_replicas: Minimum number of VM instances that autoscaler will recommend in time intervals starting according to schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#min_required_replicas ComputeAutoscaler#min_required_replicas}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#name ComputeAutoscaler#name}.
        :param schedule: The start timestamps of time intervals when this scaling schedule should provide a scaling signal. This field uses the extended cron format (with an optional year field). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#schedule ComputeAutoscaler#schedule}
        :param description: A description of a scaling schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#description ComputeAutoscaler#description}
        :param disabled: A boolean value that specifies if a scaling schedule can influence autoscaler recommendations. If set to true, then a scaling schedule has no effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#disabled ComputeAutoscaler#disabled}
        :param time_zone: The time zone to be used when interpreting the schedule. The value of this field must be a time zone name from the tz database: http://en.wikipedia.org/wiki/Tz_database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#time_zone ComputeAutoscaler#time_zone}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79c0ecbffbc008de74deea02047d9f251cbabf7adc2c6ec7633d5d55de7547e9)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#duration_sec ComputeAutoscaler#duration_sec}
        '''
        result = self._values.get("duration_sec")
        assert result is not None, "Required property 'duration_sec' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def min_required_replicas(self) -> jsii.Number:
        '''Minimum number of VM instances that autoscaler will recommend in time intervals starting according to schedule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#min_required_replicas ComputeAutoscaler#min_required_replicas}
        '''
        result = self._values.get("min_required_replicas")
        assert result is not None, "Required property 'min_required_replicas' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#name ComputeAutoscaler#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schedule(self) -> builtins.str:
        '''The start timestamps of time intervals when this scaling schedule should provide a scaling signal.

        This field uses the extended cron format (with an optional year field).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#schedule ComputeAutoscaler#schedule}
        '''
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of a scaling schedule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#description ComputeAutoscaler#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A boolean value that specifies if a scaling schedule can influence autoscaler recommendations.

        If set to true, then a scaling schedule has no effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#disabled ComputeAutoscaler#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[builtins.str]:
        '''The time zone to be used when interpreting the schedule.

        The value of this field must be a time zone name from the tz database: http://en.wikipedia.org/wiki/Tz_database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#time_zone ComputeAutoscaler#time_zone}
        '''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeAutoscalerAutoscalingPolicyScalingSchedules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeAutoscalerAutoscalingPolicyScalingSchedulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeAutoscaler.ComputeAutoscalerAutoscalingPolicyScalingSchedulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__270138a7abfa4d34d65f107d3b85f60041fcd1cf289c64a969e33d14a780f4bb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeAutoscalerAutoscalingPolicyScalingSchedulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a269af2e3b3497585e2f4640f46870a3333db8201d78d85efb69df5cc53048b3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeAutoscalerAutoscalingPolicyScalingSchedulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__211e3ec40928a7c1f450167b2d3121f67e4636147e2104560726a900e78d1e45)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e72c164b80fd9e3231f653ec9ff79c68753255cce70dd868029175b675f89475)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9df4fcba790cf6816f352cfeb803c4ccbf8b3954d50f73d89ed92ae8b4788c0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeAutoscalerAutoscalingPolicyScalingSchedules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeAutoscalerAutoscalingPolicyScalingSchedules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeAutoscalerAutoscalingPolicyScalingSchedules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3567d1c7062f71b6ac732e5c94c692ab88c515cc4ace7ca8b76d070794864479)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeAutoscalerAutoscalingPolicyScalingSchedulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeAutoscaler.ComputeAutoscalerAutoscalingPolicyScalingSchedulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6f99e6d374c5612d1bc18123ee792c2614ccaec049a519616c2bb6dbe93e09a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__95513b1cba2ca623721744df0efe3fdd5de8c8e005dcab1b8b76d67682c6c0e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d35e1aa8accd6792c63a5e1f7ba3a8c270295c1e13e2af4529103f78eae7ef00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="durationSec")
    def duration_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "durationSec"))

    @duration_sec.setter
    def duration_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e13416dcfcd23a153d0f8d5b20cee1ab882cc1fbfb08e4814505ddfcb81037f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "durationSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minRequiredReplicas")
    def min_required_replicas(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minRequiredReplicas"))

    @min_required_replicas.setter
    def min_required_replicas(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bb977e4d400c01f39ecc1b2d3783a29e9c3cc53e90e8cc134ac0184de33a4d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minRequiredReplicas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a6bea9e16f8df1b376183b7698483be7900ee9a22de0fcc37c459416674b59c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedule"))

    @schedule.setter
    def schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f29738ea792cf7705ec536e2939640a79547c2a2a15631f7989db4b78cd4da50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec1a1854854f8f5f6e9e387a8e9787ebbb853a3865e6fbaf89df1e06b1151713)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeAutoscalerAutoscalingPolicyScalingSchedules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeAutoscalerAutoscalingPolicyScalingSchedules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeAutoscalerAutoscalingPolicyScalingSchedules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7392b4a9ebbee2a29e03aaa8891d6e41d09d5100946d825c380e13fa77a8f1fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeAutoscaler.ComputeAutoscalerConfig",
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
        "timeouts": "timeouts",
        "zone": "zone",
    },
)
class ComputeAutoscalerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        autoscaling_policy: typing.Union[ComputeAutoscalerAutoscalingPolicy, typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        target: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ComputeAutoscalerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param autoscaling_policy: autoscaling_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#autoscaling_policy ComputeAutoscaler#autoscaling_policy}
        :param name: Name of the resource. The name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#name ComputeAutoscaler#name}
        :param target: URL of the managed instance group that this autoscaler will scale. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#target ComputeAutoscaler#target}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#description ComputeAutoscaler#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#id ComputeAutoscaler#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#project ComputeAutoscaler#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#timeouts ComputeAutoscaler#timeouts}
        :param zone: URL of the zone where the instance group resides. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#zone ComputeAutoscaler#zone}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(autoscaling_policy, dict):
            autoscaling_policy = ComputeAutoscalerAutoscalingPolicy(**autoscaling_policy)
        if isinstance(timeouts, dict):
            timeouts = ComputeAutoscalerTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__103c2db01d2e1004c9b323e1e65efcaa0aeb94ba889ebf82260edf9963200b6b)
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
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
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
    def autoscaling_policy(self) -> ComputeAutoscalerAutoscalingPolicy:
        '''autoscaling_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#autoscaling_policy ComputeAutoscaler#autoscaling_policy}
        '''
        result = self._values.get("autoscaling_policy")
        assert result is not None, "Required property 'autoscaling_policy' is missing"
        return typing.cast(ComputeAutoscalerAutoscalingPolicy, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the resource.

        The name must be 1-63 characters long and match
        the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the
        first character must be a lowercase letter, and all following
        characters must be a dash, lowercase letter, or digit, except the last
        character, which cannot be a dash.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#name ComputeAutoscaler#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> builtins.str:
        '''URL of the managed instance group that this autoscaler will scale.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#target ComputeAutoscaler#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#description ComputeAutoscaler#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#id ComputeAutoscaler#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#project ComputeAutoscaler#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeAutoscalerTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#timeouts ComputeAutoscaler#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeAutoscalerTimeouts"], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''URL of the zone where the instance group resides.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#zone ComputeAutoscaler#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeAutoscalerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeAutoscaler.ComputeAutoscalerTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeAutoscalerTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#create ComputeAutoscaler#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#delete ComputeAutoscaler#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#update ComputeAutoscaler#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cacadf6d4f44f8495f0cda59dcee137a1f0f87b4af87ff5224783212d60c7828)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#create ComputeAutoscaler#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#delete ComputeAutoscaler#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_autoscaler#update ComputeAutoscaler#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeAutoscalerTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeAutoscalerTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeAutoscaler.ComputeAutoscalerTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ff35ee013e16835b6168870f3f22c8488540442e56abaa7334afa98d9a524be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a937e0a2576194f9da32f316a6b5bc377f95625328d4196400984b474faa701)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__189c8fc77f66d43ae22be5a08e64060c79aad61f05d569d60463557798104151)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2f26dc3c61bd3d433126cca4ccc50d230f3296eb7be0cc9424d46894cbd71bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeAutoscalerTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeAutoscalerTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeAutoscalerTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed003fdccfa0a7639c2d700b259c0fdecfac7cf07edb44833f038e32079cc93e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeAutoscaler",
    "ComputeAutoscalerAutoscalingPolicy",
    "ComputeAutoscalerAutoscalingPolicyCpuUtilization",
    "ComputeAutoscalerAutoscalingPolicyCpuUtilizationOutputReference",
    "ComputeAutoscalerAutoscalingPolicyLoadBalancingUtilization",
    "ComputeAutoscalerAutoscalingPolicyLoadBalancingUtilizationOutputReference",
    "ComputeAutoscalerAutoscalingPolicyMetric",
    "ComputeAutoscalerAutoscalingPolicyMetricList",
    "ComputeAutoscalerAutoscalingPolicyMetricOutputReference",
    "ComputeAutoscalerAutoscalingPolicyOutputReference",
    "ComputeAutoscalerAutoscalingPolicyScaleInControl",
    "ComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas",
    "ComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicasOutputReference",
    "ComputeAutoscalerAutoscalingPolicyScaleInControlOutputReference",
    "ComputeAutoscalerAutoscalingPolicyScalingSchedules",
    "ComputeAutoscalerAutoscalingPolicyScalingSchedulesList",
    "ComputeAutoscalerAutoscalingPolicyScalingSchedulesOutputReference",
    "ComputeAutoscalerConfig",
    "ComputeAutoscalerTimeouts",
    "ComputeAutoscalerTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c944c4f9c9040efc4daa5a0c3eac7ff2033f7c5f1607b0b2a2b458a8dd45c718(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    autoscaling_policy: typing.Union[ComputeAutoscalerAutoscalingPolicy, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    target: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ComputeAutoscalerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__fd6497cf6f40f0be8306eed35a816a092e28de6534bfabca12ae9e8abc3ecb1c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ba0702c25783cf7f4cfa37a8d267f9109d129303053c997b86861ab1be8f725(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1bd621335279e6df74c52a001824ba799741ea8da4696f367a6b78310f7b012(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7db042de54be229b55f9b3e4bd587b5adf43d15dd601fe3a09aa29ab55b37a32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b842fa7791a579d8f78c28ac9e878ba3cea9d2fa5974960896813af124eb8f89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e02b40789766310e7fcaf1a858806be0ea69d2fb2a0c158e18eed4b4c4d2824f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd81be4c4f44d2b571321fd0908d63e5168e4e088c2e6fd394a4ecef08d82baa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abbc6799206835ee89755b54b8f53ef5962ddd0a7ce52afaa184409daaf9da00(
    *,
    max_replicas: jsii.Number,
    min_replicas: jsii.Number,
    cooldown_period: typing.Optional[jsii.Number] = None,
    cpu_utilization: typing.Optional[typing.Union[ComputeAutoscalerAutoscalingPolicyCpuUtilization, typing.Dict[builtins.str, typing.Any]]] = None,
    load_balancing_utilization: typing.Optional[typing.Union[ComputeAutoscalerAutoscalingPolicyLoadBalancingUtilization, typing.Dict[builtins.str, typing.Any]]] = None,
    metric: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeAutoscalerAutoscalingPolicyMetric, typing.Dict[builtins.str, typing.Any]]]]] = None,
    mode: typing.Optional[builtins.str] = None,
    scale_in_control: typing.Optional[typing.Union[ComputeAutoscalerAutoscalingPolicyScaleInControl, typing.Dict[builtins.str, typing.Any]]] = None,
    scaling_schedules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeAutoscalerAutoscalingPolicyScalingSchedules, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c736170ebd225e5a151cc447e73b3a5002af737667c1e31b35ca051db5a76a0a(
    *,
    target: jsii.Number,
    predictive_method: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb35a4fd48b3a12ece36b97e16c6167abd6700bec4b6c12a9fcfef37f3466899(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11d571411a3f67344f6029c9ec7ba9c754320c13abe48c66cd3945af32a3c2c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aec8afd2ffe299581036e52a15d3716beb2d7a26ed4026b09c396a88c7a642bd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e69c75afdd540c138deadd8dc28fa052e83e3c2ff88e46ea89bb382293abf7bf(
    value: typing.Optional[ComputeAutoscalerAutoscalingPolicyCpuUtilization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0b5f1359092d6644afc8f2033cbb16e49fb566fad7b779e96bbc8fa6f8e164e(
    *,
    target: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7d05f0241096e653b221910fb397ef30562c197696f2f53eb120d1a94c79886(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__383d254bfdcbf0dba800b6344e69afcb67d52daff89f58db4fb2bdc40ad6bda2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c825cba1932c5dd39b6dcddf4b3d9098ae087652c70c0d58db36384fefd34151(
    value: typing.Optional[ComputeAutoscalerAutoscalingPolicyLoadBalancingUtilization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5531a24a9547b0eedb1c11c8cd2dc2f4e2427bdb549c035636e192b732ba1e21(
    *,
    name: builtins.str,
    filter: typing.Optional[builtins.str] = None,
    single_instance_assignment: typing.Optional[jsii.Number] = None,
    target: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f611854357b8f9e8cb1c47e2dee6ac38a01b49cb8a7ed2e3e4457ee596bb496d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09fdf97dda89423dac11d73fd778a6959a192f1cb07308b849c79b86d03509d8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__703631f6494e4b205c38484a82bfc424eab31b4df3fe9c051fcd2196126aac89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afce9ac8aeaab066ba71675ad77d2918d953321a0c74868c665d08f19be63304(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4087cd5e06e718c51fc510076cf7fa2404ca2eeab6043a08e6879b71d8d907d9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59ef24ae1abdc16689d8e36b069a0cea559ef0a6dc40adb09bafde164d6c74c6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeAutoscalerAutoscalingPolicyMetric]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95e4de9fd6bdf4dcf072a60c418841607472ce2b014df6b77fe984b8fdeb2d8d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0103fef0f4952cd44047ad7fd390da6ed8c12cf37e202532678009ae70f7404e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b631eea38e23694a015cc1ec9185e44f79065d295dc930fb294a9e2602dadb7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__520a2d50e4fc23e185f2795f96969e1692fc5a55b92f2020b2671880cfb23152(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__142878c0cee319f932a6b25a7654a94ceeae3a380aaf6515dfb376483a631f69(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85bb99f2d320c98aa4699a10c602175fe6a7a1c79e6e5fba0a81569f65bdc72b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9019ef0e0061133aff260955b60fc6faeaef0455336a4843b8f13abec13a51b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeAutoscalerAutoscalingPolicyMetric]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14d5248ca777b823be7e9723dfb626fd826b2f9490cc1aacb70cb2778ca8330f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__960e065c9c457d03a68b456b5adecd1814223880a0aaab9e9fd4fb624cbdfc07(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeAutoscalerAutoscalingPolicyMetric, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9c8e662a9b35c39510dbd28a9eb825c79300ef2a474b9d8543e1ab7de6c8b5e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeAutoscalerAutoscalingPolicyScalingSchedules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2427c47dc19a01b1a9c8a189a90326114c6883a53f2e7ec5f8d9f58dd0889b85(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bf8636e2207435741af21cd27ac8f0e4df07f4941bf4734d58d2a089dbc5a61(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__debaa0433ee89694004486068d1a959eb9b0b0dc1f71e87287ea49f30781cb16(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0abacae6052425bd04693bbad823a53c387b25f968e3f4d12b11b70b66ee6484(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a27c32ec9a2e9524fb9108dfc182820f7f4cdb8309f9da60ad28dd45351396f(
    value: typing.Optional[ComputeAutoscalerAutoscalingPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__891bddecddf6e4b8ffcf43108ef67720a7f1f472a6bdb8b717c13a3a9d124564(
    *,
    max_scaled_in_replicas: typing.Optional[typing.Union[ComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas, typing.Dict[builtins.str, typing.Any]]] = None,
    time_window_sec: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f596228190b816e4515aa6ff62d0791ec2107f1213c1b46e7b09ea7e8c31aae0(
    *,
    fixed: typing.Optional[jsii.Number] = None,
    percent: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c6def0a48dd5041189fdca4124e74b995c21f8f8c5f32b5e2cd12b5ab20ede1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2f11801246b22d6ba41a365d232a9c85abc384350a4f5fc8ee5b3a2f9f6b30d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ccaf375218b9917a1923392d3a99f86dba390cef71a0afd70ec7a85a27fc1c2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3c0ea43a99d6f28c2fc1c907a67305b3b3d42990fe13fa857b9a24760f913d9(
    value: typing.Optional[ComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9db3acbdccc1e4c5f454bdfef02d3456d6056b38bdb49a0dc6ef6e2e54d8e796(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cfceafb0726ae5943ef4ec9f83634a325cc1a48e5d99560176b6d8954a85f28(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dad9eb3f728300a327d06e51c0fd38cbca9b6bb1a87593edcf1e6ebdc0832bb(
    value: typing.Optional[ComputeAutoscalerAutoscalingPolicyScaleInControl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79c0ecbffbc008de74deea02047d9f251cbabf7adc2c6ec7633d5d55de7547e9(
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

def _typecheckingstub__270138a7abfa4d34d65f107d3b85f60041fcd1cf289c64a969e33d14a780f4bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a269af2e3b3497585e2f4640f46870a3333db8201d78d85efb69df5cc53048b3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__211e3ec40928a7c1f450167b2d3121f67e4636147e2104560726a900e78d1e45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e72c164b80fd9e3231f653ec9ff79c68753255cce70dd868029175b675f89475(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9df4fcba790cf6816f352cfeb803c4ccbf8b3954d50f73d89ed92ae8b4788c0f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3567d1c7062f71b6ac732e5c94c692ab88c515cc4ace7ca8b76d070794864479(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeAutoscalerAutoscalingPolicyScalingSchedules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6f99e6d374c5612d1bc18123ee792c2614ccaec049a519616c2bb6dbe93e09a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95513b1cba2ca623721744df0efe3fdd5de8c8e005dcab1b8b76d67682c6c0e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d35e1aa8accd6792c63a5e1f7ba3a8c270295c1e13e2af4529103f78eae7ef00(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e13416dcfcd23a153d0f8d5b20cee1ab882cc1fbfb08e4814505ddfcb81037f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bb977e4d400c01f39ecc1b2d3783a29e9c3cc53e90e8cc134ac0184de33a4d9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a6bea9e16f8df1b376183b7698483be7900ee9a22de0fcc37c459416674b59c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f29738ea792cf7705ec536e2939640a79547c2a2a15631f7989db4b78cd4da50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec1a1854854f8f5f6e9e387a8e9787ebbb853a3865e6fbaf89df1e06b1151713(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7392b4a9ebbee2a29e03aaa8891d6e41d09d5100946d825c380e13fa77a8f1fc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeAutoscalerAutoscalingPolicyScalingSchedules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__103c2db01d2e1004c9b323e1e65efcaa0aeb94ba889ebf82260edf9963200b6b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    autoscaling_policy: typing.Union[ComputeAutoscalerAutoscalingPolicy, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    target: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ComputeAutoscalerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cacadf6d4f44f8495f0cda59dcee137a1f0f87b4af87ff5224783212d60c7828(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ff35ee013e16835b6168870f3f22c8488540442e56abaa7334afa98d9a524be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a937e0a2576194f9da32f316a6b5bc377f95625328d4196400984b474faa701(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__189c8fc77f66d43ae22be5a08e64060c79aad61f05d569d60463557798104151(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2f26dc3c61bd3d433126cca4ccc50d230f3296eb7be0cc9424d46894cbd71bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed003fdccfa0a7639c2d700b259c0fdecfac7cf07edb44833f038e32079cc93e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeAutoscalerTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
