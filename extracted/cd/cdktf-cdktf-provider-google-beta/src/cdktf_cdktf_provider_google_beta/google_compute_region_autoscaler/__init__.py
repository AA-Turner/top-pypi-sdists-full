r'''
# `google_compute_region_autoscaler`

Refer to the Terraform Registry for docs: [`google_compute_region_autoscaler`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler).
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


class GoogleComputeRegionAutoscaler(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionAutoscaler.GoogleComputeRegionAutoscaler",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler google_compute_region_autoscaler}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        autoscaling_policy: typing.Union["GoogleComputeRegionAutoscalerAutoscalingPolicy", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        target: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeRegionAutoscalerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler google_compute_region_autoscaler} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param autoscaling_policy: autoscaling_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#autoscaling_policy GoogleComputeRegionAutoscaler#autoscaling_policy}
        :param name: Name of the resource. The name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#name GoogleComputeRegionAutoscaler#name}
        :param target: URL of the managed instance group that this autoscaler will scale. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#target GoogleComputeRegionAutoscaler#target}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#description GoogleComputeRegionAutoscaler#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#id GoogleComputeRegionAutoscaler#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#project GoogleComputeRegionAutoscaler#project}.
        :param region: URL of the region where the instance group resides. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#region GoogleComputeRegionAutoscaler#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#timeouts GoogleComputeRegionAutoscaler#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43d3963a5ed830be20adf5076b34cc616450ddad621de77f87318b664bd6329b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleComputeRegionAutoscalerConfig(
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
        '''Generates CDKTF code for importing a GoogleComputeRegionAutoscaler resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleComputeRegionAutoscaler to import.
        :param import_from_id: The id of the existing GoogleComputeRegionAutoscaler that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleComputeRegionAutoscaler to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e7b183c6f74ff003b4e7231f54c5905f38daf944f2de54dd66d8979ff62825d)
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
        cpu_utilization: typing.Optional[typing.Union["GoogleComputeRegionAutoscalerAutoscalingPolicyCpuUtilization", typing.Dict[builtins.str, typing.Any]]] = None,
        load_balancing_utilization: typing.Optional[typing.Union["GoogleComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilization", typing.Dict[builtins.str, typing.Any]]] = None,
        metric: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRegionAutoscalerAutoscalingPolicyMetric", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mode: typing.Optional[builtins.str] = None,
        scale_down_control: typing.Optional[typing.Union["GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControl", typing.Dict[builtins.str, typing.Any]]] = None,
        scale_in_control: typing.Optional[typing.Union["GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControl", typing.Dict[builtins.str, typing.Any]]] = None,
        scaling_schedules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRegionAutoscalerAutoscalingPolicyScalingSchedules", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param max_replicas: The maximum number of instances that the autoscaler can scale up to. This is required when creating or updating an autoscaler. The maximum number of replicas should not be lower than minimal number of replicas. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#max_replicas GoogleComputeRegionAutoscaler#max_replicas}
        :param min_replicas: The minimum number of replicas that the autoscaler can scale down to. This cannot be less than 0. If not provided, autoscaler will choose a default value depending on maximum number of instances allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#min_replicas GoogleComputeRegionAutoscaler#min_replicas}
        :param cooldown_period: The number of seconds that the autoscaler should wait before it starts collecting information from a new instance. This prevents the autoscaler from collecting information when the instance is initializing, during which the collected usage would not be reliable. The default time autoscaler waits is 60 seconds. Virtual machine initialization times might vary because of numerous factors. We recommend that you test how long an instance may take to initialize. To do this, create an instance and time the startup process. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#cooldown_period GoogleComputeRegionAutoscaler#cooldown_period}
        :param cpu_utilization: cpu_utilization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#cpu_utilization GoogleComputeRegionAutoscaler#cpu_utilization}
        :param load_balancing_utilization: load_balancing_utilization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#load_balancing_utilization GoogleComputeRegionAutoscaler#load_balancing_utilization}
        :param metric: metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#metric GoogleComputeRegionAutoscaler#metric}
        :param mode: Defines operating mode for this policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#mode GoogleComputeRegionAutoscaler#mode}
        :param scale_down_control: scale_down_control block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#scale_down_control GoogleComputeRegionAutoscaler#scale_down_control}
        :param scale_in_control: scale_in_control block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#scale_in_control GoogleComputeRegionAutoscaler#scale_in_control}
        :param scaling_schedules: scaling_schedules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#scaling_schedules GoogleComputeRegionAutoscaler#scaling_schedules}
        '''
        value = GoogleComputeRegionAutoscalerAutoscalingPolicy(
            max_replicas=max_replicas,
            min_replicas=min_replicas,
            cooldown_period=cooldown_period,
            cpu_utilization=cpu_utilization,
            load_balancing_utilization=load_balancing_utilization,
            metric=metric,
            mode=mode,
            scale_down_control=scale_down_control,
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#create GoogleComputeRegionAutoscaler#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#delete GoogleComputeRegionAutoscaler#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#update GoogleComputeRegionAutoscaler#update}.
        '''
        value = GoogleComputeRegionAutoscalerTimeouts(
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
    ) -> "GoogleComputeRegionAutoscalerAutoscalingPolicyOutputReference":
        return typing.cast("GoogleComputeRegionAutoscalerAutoscalingPolicyOutputReference", jsii.get(self, "autoscalingPolicy"))

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
    def timeouts(self) -> "GoogleComputeRegionAutoscalerTimeoutsOutputReference":
        return typing.cast("GoogleComputeRegionAutoscalerTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingPolicyInput")
    def autoscaling_policy_input(
        self,
    ) -> typing.Optional["GoogleComputeRegionAutoscalerAutoscalingPolicy"]:
        return typing.cast(typing.Optional["GoogleComputeRegionAutoscalerAutoscalingPolicy"], jsii.get(self, "autoscalingPolicyInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeRegionAutoscalerTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeRegionAutoscalerTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6058414ffd4581009a2ef2c4a050c7bc037f261eff3e9213f1e5d37ea49f79e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc2a77b9e6760543adcfee6b82b6019506c51250bf145f9f98e556255ff3e2d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b84011ba6d5bceafebaa0ee53269219340612168abbf9aa75d96d8251ca2c23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5864410e590d209ee927766e8f3b71775c08c21ce80c860e5e9db58c716799e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__306f1535be2fe55d0e92424b04563135a1cb0651d163dd114cab98a6897cb036)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__471d2640c6ab7c995a7f9df7befb745d74cc667e3ff34631fcc88a7499f31ff3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionAutoscaler.GoogleComputeRegionAutoscalerAutoscalingPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "max_replicas": "maxReplicas",
        "min_replicas": "minReplicas",
        "cooldown_period": "cooldownPeriod",
        "cpu_utilization": "cpuUtilization",
        "load_balancing_utilization": "loadBalancingUtilization",
        "metric": "metric",
        "mode": "mode",
        "scale_down_control": "scaleDownControl",
        "scale_in_control": "scaleInControl",
        "scaling_schedules": "scalingSchedules",
    },
)
class GoogleComputeRegionAutoscalerAutoscalingPolicy:
    def __init__(
        self,
        *,
        max_replicas: jsii.Number,
        min_replicas: jsii.Number,
        cooldown_period: typing.Optional[jsii.Number] = None,
        cpu_utilization: typing.Optional[typing.Union["GoogleComputeRegionAutoscalerAutoscalingPolicyCpuUtilization", typing.Dict[builtins.str, typing.Any]]] = None,
        load_balancing_utilization: typing.Optional[typing.Union["GoogleComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilization", typing.Dict[builtins.str, typing.Any]]] = None,
        metric: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRegionAutoscalerAutoscalingPolicyMetric", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mode: typing.Optional[builtins.str] = None,
        scale_down_control: typing.Optional[typing.Union["GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControl", typing.Dict[builtins.str, typing.Any]]] = None,
        scale_in_control: typing.Optional[typing.Union["GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControl", typing.Dict[builtins.str, typing.Any]]] = None,
        scaling_schedules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRegionAutoscalerAutoscalingPolicyScalingSchedules", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param max_replicas: The maximum number of instances that the autoscaler can scale up to. This is required when creating or updating an autoscaler. The maximum number of replicas should not be lower than minimal number of replicas. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#max_replicas GoogleComputeRegionAutoscaler#max_replicas}
        :param min_replicas: The minimum number of replicas that the autoscaler can scale down to. This cannot be less than 0. If not provided, autoscaler will choose a default value depending on maximum number of instances allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#min_replicas GoogleComputeRegionAutoscaler#min_replicas}
        :param cooldown_period: The number of seconds that the autoscaler should wait before it starts collecting information from a new instance. This prevents the autoscaler from collecting information when the instance is initializing, during which the collected usage would not be reliable. The default time autoscaler waits is 60 seconds. Virtual machine initialization times might vary because of numerous factors. We recommend that you test how long an instance may take to initialize. To do this, create an instance and time the startup process. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#cooldown_period GoogleComputeRegionAutoscaler#cooldown_period}
        :param cpu_utilization: cpu_utilization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#cpu_utilization GoogleComputeRegionAutoscaler#cpu_utilization}
        :param load_balancing_utilization: load_balancing_utilization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#load_balancing_utilization GoogleComputeRegionAutoscaler#load_balancing_utilization}
        :param metric: metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#metric GoogleComputeRegionAutoscaler#metric}
        :param mode: Defines operating mode for this policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#mode GoogleComputeRegionAutoscaler#mode}
        :param scale_down_control: scale_down_control block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#scale_down_control GoogleComputeRegionAutoscaler#scale_down_control}
        :param scale_in_control: scale_in_control block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#scale_in_control GoogleComputeRegionAutoscaler#scale_in_control}
        :param scaling_schedules: scaling_schedules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#scaling_schedules GoogleComputeRegionAutoscaler#scaling_schedules}
        '''
        if isinstance(cpu_utilization, dict):
            cpu_utilization = GoogleComputeRegionAutoscalerAutoscalingPolicyCpuUtilization(**cpu_utilization)
        if isinstance(load_balancing_utilization, dict):
            load_balancing_utilization = GoogleComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilization(**load_balancing_utilization)
        if isinstance(scale_down_control, dict):
            scale_down_control = GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControl(**scale_down_control)
        if isinstance(scale_in_control, dict):
            scale_in_control = GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControl(**scale_in_control)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ea6040ef0d109d3c3d2fcdc3452a061b039f009e672d8d3254ca9825a403f5c)
            check_type(argname="argument max_replicas", value=max_replicas, expected_type=type_hints["max_replicas"])
            check_type(argname="argument min_replicas", value=min_replicas, expected_type=type_hints["min_replicas"])
            check_type(argname="argument cooldown_period", value=cooldown_period, expected_type=type_hints["cooldown_period"])
            check_type(argname="argument cpu_utilization", value=cpu_utilization, expected_type=type_hints["cpu_utilization"])
            check_type(argname="argument load_balancing_utilization", value=load_balancing_utilization, expected_type=type_hints["load_balancing_utilization"])
            check_type(argname="argument metric", value=metric, expected_type=type_hints["metric"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument scale_down_control", value=scale_down_control, expected_type=type_hints["scale_down_control"])
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
        if scale_down_control is not None:
            self._values["scale_down_control"] = scale_down_control
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#max_replicas GoogleComputeRegionAutoscaler#max_replicas}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#min_replicas GoogleComputeRegionAutoscaler#min_replicas}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#cooldown_period GoogleComputeRegionAutoscaler#cooldown_period}
        '''
        result = self._values.get("cooldown_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cpu_utilization(
        self,
    ) -> typing.Optional["GoogleComputeRegionAutoscalerAutoscalingPolicyCpuUtilization"]:
        '''cpu_utilization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#cpu_utilization GoogleComputeRegionAutoscaler#cpu_utilization}
        '''
        result = self._values.get("cpu_utilization")
        return typing.cast(typing.Optional["GoogleComputeRegionAutoscalerAutoscalingPolicyCpuUtilization"], result)

    @builtins.property
    def load_balancing_utilization(
        self,
    ) -> typing.Optional["GoogleComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilization"]:
        '''load_balancing_utilization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#load_balancing_utilization GoogleComputeRegionAutoscaler#load_balancing_utilization}
        '''
        result = self._values.get("load_balancing_utilization")
        return typing.cast(typing.Optional["GoogleComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilization"], result)

    @builtins.property
    def metric(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionAutoscalerAutoscalingPolicyMetric"]]]:
        '''metric block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#metric GoogleComputeRegionAutoscaler#metric}
        '''
        result = self._values.get("metric")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionAutoscalerAutoscalingPolicyMetric"]]], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Defines operating mode for this policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#mode GoogleComputeRegionAutoscaler#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scale_down_control(
        self,
    ) -> typing.Optional["GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControl"]:
        '''scale_down_control block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#scale_down_control GoogleComputeRegionAutoscaler#scale_down_control}
        '''
        result = self._values.get("scale_down_control")
        return typing.cast(typing.Optional["GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControl"], result)

    @builtins.property
    def scale_in_control(
        self,
    ) -> typing.Optional["GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControl"]:
        '''scale_in_control block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#scale_in_control GoogleComputeRegionAutoscaler#scale_in_control}
        '''
        result = self._values.get("scale_in_control")
        return typing.cast(typing.Optional["GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControl"], result)

    @builtins.property
    def scaling_schedules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionAutoscalerAutoscalingPolicyScalingSchedules"]]]:
        '''scaling_schedules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#scaling_schedules GoogleComputeRegionAutoscaler#scaling_schedules}
        '''
        result = self._values.get("scaling_schedules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionAutoscalerAutoscalingPolicyScalingSchedules"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionAutoscalerAutoscalingPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionAutoscaler.GoogleComputeRegionAutoscalerAutoscalingPolicyCpuUtilization",
    jsii_struct_bases=[],
    name_mapping={"target": "target", "predictive_method": "predictiveMethod"},
)
class GoogleComputeRegionAutoscalerAutoscalingPolicyCpuUtilization:
    def __init__(
        self,
        *,
        target: jsii.Number,
        predictive_method: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target: The target CPU utilization that the autoscaler should maintain. Must be a float value in the range (0, 1]. If not specified, the default is 0.6. If the CPU level is below the target utilization, the autoscaler scales down the number of instances until it reaches the minimum number of instances you specified or until the average CPU of your instances reaches the target utilization. If the average CPU is above the target utilization, the autoscaler scales up until it reaches the maximum number of instances you specified or until the average utilization reaches the target utilization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#target GoogleComputeRegionAutoscaler#target}
        :param predictive_method: Indicates whether predictive autoscaling based on CPU metric is enabled. Valid values are:. - NONE (default). No predictive method is used. The autoscaler scales the group to meet current demand based on real-time metrics. - OPTIMIZE_AVAILABILITY. Predictive autoscaling improves availability by monitoring daily and weekly load patterns and scaling out ahead of anticipated demand. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#predictive_method GoogleComputeRegionAutoscaler#predictive_method}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b3faa7953f374ae9c7385e4d4abce6621b43855d5795e1df0800d08b7047093)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#target GoogleComputeRegionAutoscaler#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def predictive_method(self) -> typing.Optional[builtins.str]:
        '''Indicates whether predictive autoscaling based on CPU metric is enabled. Valid values are:.

        - NONE (default). No predictive method is used. The autoscaler scales the group to meet current demand based on real-time metrics.
        - OPTIMIZE_AVAILABILITY. Predictive autoscaling improves availability by monitoring daily and weekly load patterns and scaling out ahead of anticipated demand.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#predictive_method GoogleComputeRegionAutoscaler#predictive_method}
        '''
        result = self._values.get("predictive_method")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionAutoscalerAutoscalingPolicyCpuUtilization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionAutoscalerAutoscalingPolicyCpuUtilizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionAutoscaler.GoogleComputeRegionAutoscalerAutoscalingPolicyCpuUtilizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__159de316292aa693ffe550128d5a3ffe7c901dae483f6a1982e0aad85c4c8111)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ef4180a1a6e95641b4dc06ec33d0b5aeec2544eb0c6f0eeba22344bc341e831)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "predictiveMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "target"))

    @target.setter
    def target(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a97066c298a34d87aca4570ce23ecdf997399ea5bafb6f78d0937823bd0df888)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionAutoscalerAutoscalingPolicyCpuUtilization]:
        return typing.cast(typing.Optional[GoogleComputeRegionAutoscalerAutoscalingPolicyCpuUtilization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionAutoscalerAutoscalingPolicyCpuUtilization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db991e462ae6c23e16ce25d2ca71a8fa8feeea024130daad542f155ed5942f98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionAutoscaler.GoogleComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilization",
    jsii_struct_bases=[],
    name_mapping={"target": "target"},
)
class GoogleComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilization:
    def __init__(self, *, target: jsii.Number) -> None:
        '''
        :param target: Fraction of backend capacity utilization (set in HTTP(s) load balancing configuration) that autoscaler should maintain. Must be a positive float value. If not defined, the default is 0.8. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#target GoogleComputeRegionAutoscaler#target}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9314a8e6c68c104f9da843ca37ef09ad6c96dc344d1d57446583b7556aa0c48e)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target": target,
        }

    @builtins.property
    def target(self) -> jsii.Number:
        '''Fraction of backend capacity utilization (set in HTTP(s) load balancing configuration) that autoscaler should maintain.

        Must
        be a positive float value. If not defined, the default is 0.8.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#target GoogleComputeRegionAutoscaler#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionAutoscaler.GoogleComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d98e6f1d4b2269bf530cca1fe5d3cd069990fc880fb959279c5a0aa77617720)
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
            type_hints = typing.get_type_hints(_typecheckingstub__01d284c8db7a41efeb62a9d5b506330fd56f36472c2a2a3c33c3c54891d2d9d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilization]:
        return typing.cast(typing.Optional[GoogleComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3544aa376aaec1dd80962b84f6736232f6e72f12239e0580e7016c6b5db0849c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionAutoscaler.GoogleComputeRegionAutoscalerAutoscalingPolicyMetric",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "filter": "filter",
        "single_instance_assignment": "singleInstanceAssignment",
        "target": "target",
        "type": "type",
    },
)
class GoogleComputeRegionAutoscalerAutoscalingPolicyMetric:
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
        :param name: The identifier (type) of the Stackdriver Monitoring metric. The metric cannot have negative values. The metric must have a value type of INT64 or DOUBLE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#name GoogleComputeRegionAutoscaler#name}
        :param filter: A filter string to be used as the filter string for a Stackdriver Monitoring TimeSeries.list API call. This filter is used to select a specific TimeSeries for the purpose of autoscaling and to determine whether the metric is exporting per-instance or per-group data. You can only use the AND operator for joining selectors. You can only use direct equality comparison operator (=) without any functions for each selector. You can specify the metric in both the filter string and in the metric field. However, if specified in both places, the metric must be identical. The monitored resource type determines what kind of values are expected for the metric. If it is a gce_instance, the autoscaler expects the metric to include a separate TimeSeries for each instance in a group. In such a case, you cannot filter on resource labels. If the resource type is any other value, the autoscaler expects this metric to contain values that apply to the entire autoscaled instance group and resource label filtering can be performed to point autoscaler at the correct TimeSeries to scale upon. This is called a per-group metric for the purpose of autoscaling. If not specified, the type defaults to gce_instance. You should provide a filter that is selective enough to pick just one TimeSeries for the autoscaled group or for each of the instances (if you are using gce_instance resource type). If multiple TimeSeries are returned upon the query execution, the autoscaler will sum their respective values to obtain its scaling value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#filter GoogleComputeRegionAutoscaler#filter}
        :param single_instance_assignment: If scaling is based on a per-group metric value that represents the total amount of work to be done or resource usage, set this value to an amount assigned for a single instance of the scaled group. The autoscaler will keep the number of instances proportional to the value of this metric, the metric itself should not change value due to group resizing. For example, a good metric to use with the target is 'pubsub.googleapis.com/subscription/num_undelivered_messages' or a custom metric exporting the total number of requests coming to your instances. A bad example would be a metric exporting an average or median latency, since this value can't include a chunk assignable to a single instance, it could be better used with utilization_target instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#single_instance_assignment GoogleComputeRegionAutoscaler#single_instance_assignment}
        :param target: The target value of the metric that autoscaler should maintain. This must be a positive value. A utilization metric scales number of virtual machines handling requests to increase or decrease proportionally to the metric. For example, a good metric to use as a utilizationTarget is www.googleapis.com/compute/instance/network/received_bytes_count. The autoscaler will work to keep this value constant for each of the instances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#target GoogleComputeRegionAutoscaler#target}
        :param type: Defines how target utilization value is expressed for a Stackdriver Monitoring metric. Possible values: ["GAUGE", "DELTA_PER_SECOND", "DELTA_PER_MINUTE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#type GoogleComputeRegionAutoscaler#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a1ebe788840a0b4a72c168b19c69d45f61db2ce1855f21e721d2176e680c945)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#name GoogleComputeRegionAutoscaler#name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#filter GoogleComputeRegionAutoscaler#filter}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#single_instance_assignment GoogleComputeRegionAutoscaler#single_instance_assignment}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#target GoogleComputeRegionAutoscaler#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Defines how target utilization value is expressed for a Stackdriver Monitoring metric. Possible values: ["GAUGE", "DELTA_PER_SECOND", "DELTA_PER_MINUTE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#type GoogleComputeRegionAutoscaler#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionAutoscalerAutoscalingPolicyMetric(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionAutoscalerAutoscalingPolicyMetricList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionAutoscaler.GoogleComputeRegionAutoscalerAutoscalingPolicyMetricList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__53afd30460c6ea83ed1a21c67eb6e3b0448219a065eb6e764324f94070b134a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeRegionAutoscalerAutoscalingPolicyMetricOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d55ff1a2cbbe581510ccd984137cbcb331f5f5b27e16d669a66fd508b656111)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeRegionAutoscalerAutoscalingPolicyMetricOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca077246f3c7f465845445d618ee7593bcee2933953da702cca4f84ec62a12e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__42dea22963975b11474cd576494747aea7140634703b638f5f97b29bffb5b302)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b41fa7845034f381979c902f767d64ba7a8182ee46931760e38c88cfca8c2488)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionAutoscalerAutoscalingPolicyMetric]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionAutoscalerAutoscalingPolicyMetric]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionAutoscalerAutoscalingPolicyMetric]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12de7f80a56761edd6c1cb2bde1ed17b906ded9ce21b866b82ac14b0588fab9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeRegionAutoscalerAutoscalingPolicyMetricOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionAutoscaler.GoogleComputeRegionAutoscalerAutoscalingPolicyMetricOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf349c1be5f0565e4160ed9bb2ee52e30e4478b33db71db9eaf313cf4cd6baaa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a4e6570f121855f7454ec0026f042c8822679502d2fb88249c00de4fb3867d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45b6eb26b26670e62de290cc52551dd35c5863fb1a08b712f239cff28b27fdc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="singleInstanceAssignment")
    def single_instance_assignment(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "singleInstanceAssignment"))

    @single_instance_assignment.setter
    def single_instance_assignment(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfcfbc096c030a0aac5f98dce8aabfcaa427ac9f68a61da21af46d92ddb9efb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "singleInstanceAssignment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "target"))

    @target.setter
    def target(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9254e582ad7bf991d131ebc723ec4546b6d1dcf4a42b5badee75426f5b697418)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe655e287a65c32b488959722b692697de7d595b791c7a2dbbbab221ba1ebcae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionAutoscalerAutoscalingPolicyMetric]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionAutoscalerAutoscalingPolicyMetric]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionAutoscalerAutoscalingPolicyMetric]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cc8c39405353c46f6709265c62c9d268786e5cd69b7315a0e527c21a0814196)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeRegionAutoscalerAutoscalingPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionAutoscaler.GoogleComputeRegionAutoscalerAutoscalingPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb45a03e3af9b18d93711915618e361bb3618f6d707a66e4e0a979ee2e336076)
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
        :param target: The target CPU utilization that the autoscaler should maintain. Must be a float value in the range (0, 1]. If not specified, the default is 0.6. If the CPU level is below the target utilization, the autoscaler scales down the number of instances until it reaches the minimum number of instances you specified or until the average CPU of your instances reaches the target utilization. If the average CPU is above the target utilization, the autoscaler scales up until it reaches the maximum number of instances you specified or until the average utilization reaches the target utilization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#target GoogleComputeRegionAutoscaler#target}
        :param predictive_method: Indicates whether predictive autoscaling based on CPU metric is enabled. Valid values are:. - NONE (default). No predictive method is used. The autoscaler scales the group to meet current demand based on real-time metrics. - OPTIMIZE_AVAILABILITY. Predictive autoscaling improves availability by monitoring daily and weekly load patterns and scaling out ahead of anticipated demand. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#predictive_method GoogleComputeRegionAutoscaler#predictive_method}
        '''
        value = GoogleComputeRegionAutoscalerAutoscalingPolicyCpuUtilization(
            target=target, predictive_method=predictive_method
        )

        return typing.cast(None, jsii.invoke(self, "putCpuUtilization", [value]))

    @jsii.member(jsii_name="putLoadBalancingUtilization")
    def put_load_balancing_utilization(self, *, target: jsii.Number) -> None:
        '''
        :param target: Fraction of backend capacity utilization (set in HTTP(s) load balancing configuration) that autoscaler should maintain. Must be a positive float value. If not defined, the default is 0.8. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#target GoogleComputeRegionAutoscaler#target}
        '''
        value = GoogleComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilization(
            target=target
        )

        return typing.cast(None, jsii.invoke(self, "putLoadBalancingUtilization", [value]))

    @jsii.member(jsii_name="putMetric")
    def put_metric(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRegionAutoscalerAutoscalingPolicyMetric, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfa2e640cd18c8e829490ddd17309a891cd38688511a86a8015ea951b0650d5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMetric", [value]))

    @jsii.member(jsii_name="putScaleDownControl")
    def put_scale_down_control(
        self,
        *,
        max_scaled_down_replicas: typing.Optional[typing.Union["GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicas", typing.Dict[builtins.str, typing.Any]]] = None,
        time_window_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_scaled_down_replicas: max_scaled_down_replicas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#max_scaled_down_replicas GoogleComputeRegionAutoscaler#max_scaled_down_replicas}
        :param time_window_sec: How long back autoscaling should look when computing recommendations to include directives regarding slower scale down, as described above. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#time_window_sec GoogleComputeRegionAutoscaler#time_window_sec}
        '''
        value = GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControl(
            max_scaled_down_replicas=max_scaled_down_replicas,
            time_window_sec=time_window_sec,
        )

        return typing.cast(None, jsii.invoke(self, "putScaleDownControl", [value]))

    @jsii.member(jsii_name="putScaleInControl")
    def put_scale_in_control(
        self,
        *,
        max_scaled_in_replicas: typing.Optional[typing.Union["GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas", typing.Dict[builtins.str, typing.Any]]] = None,
        time_window_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_scaled_in_replicas: max_scaled_in_replicas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#max_scaled_in_replicas GoogleComputeRegionAutoscaler#max_scaled_in_replicas}
        :param time_window_sec: How long back autoscaling should look when computing recommendations to include directives regarding slower scale down, as described above. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#time_window_sec GoogleComputeRegionAutoscaler#time_window_sec}
        '''
        value = GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControl(
            max_scaled_in_replicas=max_scaled_in_replicas,
            time_window_sec=time_window_sec,
        )

        return typing.cast(None, jsii.invoke(self, "putScaleInControl", [value]))

    @jsii.member(jsii_name="putScalingSchedules")
    def put_scaling_schedules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRegionAutoscalerAutoscalingPolicyScalingSchedules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9120b1ae40b1cc0b23e5004d71b83795b00d703f8350bc7f7ab4fc13ed9f5d96)
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

    @jsii.member(jsii_name="resetScaleDownControl")
    def reset_scale_down_control(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScaleDownControl", []))

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
    ) -> GoogleComputeRegionAutoscalerAutoscalingPolicyCpuUtilizationOutputReference:
        return typing.cast(GoogleComputeRegionAutoscalerAutoscalingPolicyCpuUtilizationOutputReference, jsii.get(self, "cpuUtilization"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancingUtilization")
    def load_balancing_utilization(
        self,
    ) -> GoogleComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilizationOutputReference:
        return typing.cast(GoogleComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilizationOutputReference, jsii.get(self, "loadBalancingUtilization"))

    @builtins.property
    @jsii.member(jsii_name="metric")
    def metric(self) -> GoogleComputeRegionAutoscalerAutoscalingPolicyMetricList:
        return typing.cast(GoogleComputeRegionAutoscalerAutoscalingPolicyMetricList, jsii.get(self, "metric"))

    @builtins.property
    @jsii.member(jsii_name="scaleDownControl")
    def scale_down_control(
        self,
    ) -> "GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControlOutputReference":
        return typing.cast("GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControlOutputReference", jsii.get(self, "scaleDownControl"))

    @builtins.property
    @jsii.member(jsii_name="scaleInControl")
    def scale_in_control(
        self,
    ) -> "GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControlOutputReference":
        return typing.cast("GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControlOutputReference", jsii.get(self, "scaleInControl"))

    @builtins.property
    @jsii.member(jsii_name="scalingSchedules")
    def scaling_schedules(
        self,
    ) -> "GoogleComputeRegionAutoscalerAutoscalingPolicyScalingSchedulesList":
        return typing.cast("GoogleComputeRegionAutoscalerAutoscalingPolicyScalingSchedulesList", jsii.get(self, "scalingSchedules"))

    @builtins.property
    @jsii.member(jsii_name="cooldownPeriodInput")
    def cooldown_period_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cooldownPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuUtilizationInput")
    def cpu_utilization_input(
        self,
    ) -> typing.Optional[GoogleComputeRegionAutoscalerAutoscalingPolicyCpuUtilization]:
        return typing.cast(typing.Optional[GoogleComputeRegionAutoscalerAutoscalingPolicyCpuUtilization], jsii.get(self, "cpuUtilizationInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancingUtilizationInput")
    def load_balancing_utilization_input(
        self,
    ) -> typing.Optional[GoogleComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilization]:
        return typing.cast(typing.Optional[GoogleComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilization], jsii.get(self, "loadBalancingUtilizationInput"))

    @builtins.property
    @jsii.member(jsii_name="maxReplicasInput")
    def max_replicas_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxReplicasInput"))

    @builtins.property
    @jsii.member(jsii_name="metricInput")
    def metric_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionAutoscalerAutoscalingPolicyMetric]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionAutoscalerAutoscalingPolicyMetric]]], jsii.get(self, "metricInput"))

    @builtins.property
    @jsii.member(jsii_name="minReplicasInput")
    def min_replicas_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minReplicasInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleDownControlInput")
    def scale_down_control_input(
        self,
    ) -> typing.Optional["GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControl"]:
        return typing.cast(typing.Optional["GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControl"], jsii.get(self, "scaleDownControlInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleInControlInput")
    def scale_in_control_input(
        self,
    ) -> typing.Optional["GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControl"]:
        return typing.cast(typing.Optional["GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControl"], jsii.get(self, "scaleInControlInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingSchedulesInput")
    def scaling_schedules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionAutoscalerAutoscalingPolicyScalingSchedules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionAutoscalerAutoscalingPolicyScalingSchedules"]]], jsii.get(self, "scalingSchedulesInput"))

    @builtins.property
    @jsii.member(jsii_name="cooldownPeriod")
    def cooldown_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cooldownPeriod"))

    @cooldown_period.setter
    def cooldown_period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d85b9a8202653c6bdfdf2d39d99703587554fb05b927af5bff8682a0f68be00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cooldownPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxReplicas")
    def max_replicas(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxReplicas"))

    @max_replicas.setter
    def max_replicas(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c166459ee6ed395fdb562e434bede16593b953967d4aefbc0d9088455cc4f847)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxReplicas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minReplicas")
    def min_replicas(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minReplicas"))

    @min_replicas.setter
    def min_replicas(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe4fb4ebca429b29ac59c641bb1561cd7071abe1838dec039d9be728c698ef21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minReplicas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d89090ab00b42243fb656be3a53d8d1dc196ceff39b91ad2b3d11509909d83a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionAutoscalerAutoscalingPolicy]:
        return typing.cast(typing.Optional[GoogleComputeRegionAutoscalerAutoscalingPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionAutoscalerAutoscalingPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__734553d7cde02e6537d235fe451e9d0451d24d72b76764f859069fdc378bc8af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionAutoscaler.GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControl",
    jsii_struct_bases=[],
    name_mapping={
        "max_scaled_down_replicas": "maxScaledDownReplicas",
        "time_window_sec": "timeWindowSec",
    },
)
class GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControl:
    def __init__(
        self,
        *,
        max_scaled_down_replicas: typing.Optional[typing.Union["GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicas", typing.Dict[builtins.str, typing.Any]]] = None,
        time_window_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_scaled_down_replicas: max_scaled_down_replicas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#max_scaled_down_replicas GoogleComputeRegionAutoscaler#max_scaled_down_replicas}
        :param time_window_sec: How long back autoscaling should look when computing recommendations to include directives regarding slower scale down, as described above. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#time_window_sec GoogleComputeRegionAutoscaler#time_window_sec}
        '''
        if isinstance(max_scaled_down_replicas, dict):
            max_scaled_down_replicas = GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicas(**max_scaled_down_replicas)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98d29c519a7c583cd4387ac10f6632b9af98634a857711a0140481575f71fb11)
            check_type(argname="argument max_scaled_down_replicas", value=max_scaled_down_replicas, expected_type=type_hints["max_scaled_down_replicas"])
            check_type(argname="argument time_window_sec", value=time_window_sec, expected_type=type_hints["time_window_sec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_scaled_down_replicas is not None:
            self._values["max_scaled_down_replicas"] = max_scaled_down_replicas
        if time_window_sec is not None:
            self._values["time_window_sec"] = time_window_sec

    @builtins.property
    def max_scaled_down_replicas(
        self,
    ) -> typing.Optional["GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicas"]:
        '''max_scaled_down_replicas block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#max_scaled_down_replicas GoogleComputeRegionAutoscaler#max_scaled_down_replicas}
        '''
        result = self._values.get("max_scaled_down_replicas")
        return typing.cast(typing.Optional["GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicas"], result)

    @builtins.property
    def time_window_sec(self) -> typing.Optional[jsii.Number]:
        '''How long back autoscaling should look when computing recommendations to include directives regarding slower scale down, as described above.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#time_window_sec GoogleComputeRegionAutoscaler#time_window_sec}
        '''
        result = self._values.get("time_window_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionAutoscaler.GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicas",
    jsii_struct_bases=[],
    name_mapping={"fixed": "fixed", "percent": "percent"},
)
class GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicas:
    def __init__(
        self,
        *,
        fixed: typing.Optional[jsii.Number] = None,
        percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fixed: Specifies a fixed number of VM instances. This must be a positive integer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#fixed GoogleComputeRegionAutoscaler#fixed}
        :param percent: Specifies a percentage of instances between 0 to 100%, inclusive. For example, specify 80 for 80%. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#percent GoogleComputeRegionAutoscaler#percent}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58bed10fcb8e130cd7ac779305dae0855a35f905ddae42781b41d87e2eefb15c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#fixed GoogleComputeRegionAutoscaler#fixed}
        '''
        result = self._values.get("fixed")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def percent(self) -> typing.Optional[jsii.Number]:
        '''Specifies a percentage of instances between 0 to 100%, inclusive. For example, specify 80 for 80%.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#percent GoogleComputeRegionAutoscaler#percent}
        '''
        result = self._values.get("percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicas(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicasOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionAutoscaler.GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicasOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c308268a57916b6596bc641e8740efb6675635b8af5d7a2813fe1bfb41f25d6d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__12988a39b34d242258a85980bc57b55cb15e1790a62790a3a241e8c3510fd7d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="percent")
    def percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percent"))

    @percent.setter
    def percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__421bd105208eb4f34bad4a29f30a16387327bb200aee2396cbb1e15aeef5633d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicas]:
        return typing.cast(typing.Optional[GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicas], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicas],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__356cddca41a94ff6e4cbef90fcbee4d6c51047379b26aa4f76d8b2166c641d33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionAutoscaler.GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d788a74f5f54ed224bb77d2539cc920b9bf74b366f36660715c7cf8c8e44f1ac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMaxScaledDownReplicas")
    def put_max_scaled_down_replicas(
        self,
        *,
        fixed: typing.Optional[jsii.Number] = None,
        percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fixed: Specifies a fixed number of VM instances. This must be a positive integer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#fixed GoogleComputeRegionAutoscaler#fixed}
        :param percent: Specifies a percentage of instances between 0 to 100%, inclusive. For example, specify 80 for 80%. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#percent GoogleComputeRegionAutoscaler#percent}
        '''
        value = GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicas(
            fixed=fixed, percent=percent
        )

        return typing.cast(None, jsii.invoke(self, "putMaxScaledDownReplicas", [value]))

    @jsii.member(jsii_name="resetMaxScaledDownReplicas")
    def reset_max_scaled_down_replicas(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxScaledDownReplicas", []))

    @jsii.member(jsii_name="resetTimeWindowSec")
    def reset_time_window_sec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeWindowSec", []))

    @builtins.property
    @jsii.member(jsii_name="maxScaledDownReplicas")
    def max_scaled_down_replicas(
        self,
    ) -> GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicasOutputReference:
        return typing.cast(GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicasOutputReference, jsii.get(self, "maxScaledDownReplicas"))

    @builtins.property
    @jsii.member(jsii_name="maxScaledDownReplicasInput")
    def max_scaled_down_replicas_input(
        self,
    ) -> typing.Optional[GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicas]:
        return typing.cast(typing.Optional[GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicas], jsii.get(self, "maxScaledDownReplicasInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__33f93863e23d6a3e5dfa5e60c1d03685950720b635a7e0e6ccefed5bc09bd011)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeWindowSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControl]:
        return typing.cast(typing.Optional[GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__963b06e23f34811e8b8ea523bc511a2a49cf5c26c5619b170817ef2ba32b35a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionAutoscaler.GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControl",
    jsii_struct_bases=[],
    name_mapping={
        "max_scaled_in_replicas": "maxScaledInReplicas",
        "time_window_sec": "timeWindowSec",
    },
)
class GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControl:
    def __init__(
        self,
        *,
        max_scaled_in_replicas: typing.Optional[typing.Union["GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas", typing.Dict[builtins.str, typing.Any]]] = None,
        time_window_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_scaled_in_replicas: max_scaled_in_replicas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#max_scaled_in_replicas GoogleComputeRegionAutoscaler#max_scaled_in_replicas}
        :param time_window_sec: How long back autoscaling should look when computing recommendations to include directives regarding slower scale down, as described above. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#time_window_sec GoogleComputeRegionAutoscaler#time_window_sec}
        '''
        if isinstance(max_scaled_in_replicas, dict):
            max_scaled_in_replicas = GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas(**max_scaled_in_replicas)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f4c562c9ae9b04b783186677fd0c39f92f6b9bcb44aab90e118fb57afb14ded)
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
    ) -> typing.Optional["GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas"]:
        '''max_scaled_in_replicas block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#max_scaled_in_replicas GoogleComputeRegionAutoscaler#max_scaled_in_replicas}
        '''
        result = self._values.get("max_scaled_in_replicas")
        return typing.cast(typing.Optional["GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas"], result)

    @builtins.property
    def time_window_sec(self) -> typing.Optional[jsii.Number]:
        '''How long back autoscaling should look when computing recommendations to include directives regarding slower scale down, as described above.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#time_window_sec GoogleComputeRegionAutoscaler#time_window_sec}
        '''
        result = self._values.get("time_window_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionAutoscaler.GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas",
    jsii_struct_bases=[],
    name_mapping={"fixed": "fixed", "percent": "percent"},
)
class GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas:
    def __init__(
        self,
        *,
        fixed: typing.Optional[jsii.Number] = None,
        percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fixed: Specifies a fixed number of VM instances. This must be a positive integer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#fixed GoogleComputeRegionAutoscaler#fixed}
        :param percent: Specifies a percentage of instances between 0 to 100%, inclusive. For example, specify 80 for 80%. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#percent GoogleComputeRegionAutoscaler#percent}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f477c222b9d27b0ac4228d94808f8d1fa0f04c2976dba57dd0e7cab519f0eec)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#fixed GoogleComputeRegionAutoscaler#fixed}
        '''
        result = self._values.get("fixed")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def percent(self) -> typing.Optional[jsii.Number]:
        '''Specifies a percentage of instances between 0 to 100%, inclusive. For example, specify 80 for 80%.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#percent GoogleComputeRegionAutoscaler#percent}
        '''
        result = self._values.get("percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicasOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionAutoscaler.GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicasOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6426f30e8f7572d62dbc05bc0435d0e8cff8835aa5bc988682b5ff27c785f73)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fd35909166ec1444b435106d900ec8db0993baa219ead258f7359cff761b566)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="percent")
    def percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percent"))

    @percent.setter
    def percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f95cf5bba5b8e563b64adac3e07e4ace02b1ec7694ef8f95b8cd44b1c4730fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas]:
        return typing.cast(typing.Optional[GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__340a179858fb72547bf64dbe792c43b5b562dba809938ea15a7d3182a63148da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionAutoscaler.GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b5baa30ae3d9ecfde0a90c2522f35489c183fffc64366bd158e40c8634b52be)
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
        :param fixed: Specifies a fixed number of VM instances. This must be a positive integer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#fixed GoogleComputeRegionAutoscaler#fixed}
        :param percent: Specifies a percentage of instances between 0 to 100%, inclusive. For example, specify 80 for 80%. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#percent GoogleComputeRegionAutoscaler#percent}
        '''
        value = GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas(
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
    ) -> GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicasOutputReference:
        return typing.cast(GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicasOutputReference, jsii.get(self, "maxScaledInReplicas"))

    @builtins.property
    @jsii.member(jsii_name="maxScaledInReplicasInput")
    def max_scaled_in_replicas_input(
        self,
    ) -> typing.Optional[GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas]:
        return typing.cast(typing.Optional[GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas], jsii.get(self, "maxScaledInReplicasInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ba71a1b85e160aca92e9869c9f2d6b8e62e120713d4b9037dd88bac40ebd732a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeWindowSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControl]:
        return typing.cast(typing.Optional[GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__235c2846889a9c148b2068f9f8ce7c444ec501fba8040ff9a94e082f9fd380ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionAutoscaler.GoogleComputeRegionAutoscalerAutoscalingPolicyScalingSchedules",
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
class GoogleComputeRegionAutoscalerAutoscalingPolicyScalingSchedules:
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
        :param duration_sec: The duration of time intervals (in seconds) for which this scaling schedule will be running. The minimum allowed value is 300. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#duration_sec GoogleComputeRegionAutoscaler#duration_sec}
        :param min_required_replicas: Minimum number of VM instances that autoscaler will recommend in time intervals starting according to schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#min_required_replicas GoogleComputeRegionAutoscaler#min_required_replicas}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#name GoogleComputeRegionAutoscaler#name}.
        :param schedule: The start timestamps of time intervals when this scaling schedule should provide a scaling signal. This field uses the extended cron format (with an optional year field). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#schedule GoogleComputeRegionAutoscaler#schedule}
        :param description: A description of a scaling schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#description GoogleComputeRegionAutoscaler#description}
        :param disabled: A boolean value that specifies if a scaling schedule can influence autoscaler recommendations. If set to true, then a scaling schedule has no effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#disabled GoogleComputeRegionAutoscaler#disabled}
        :param time_zone: The time zone to be used when interpreting the schedule. The value of this field must be a time zone name from the tz database: http://en.wikipedia.org/wiki/Tz_database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#time_zone GoogleComputeRegionAutoscaler#time_zone}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c197b1e3857035187596b5c69068403482f87108f7343900aadd816580a2aed7)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#duration_sec GoogleComputeRegionAutoscaler#duration_sec}
        '''
        result = self._values.get("duration_sec")
        assert result is not None, "Required property 'duration_sec' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def min_required_replicas(self) -> jsii.Number:
        '''Minimum number of VM instances that autoscaler will recommend in time intervals starting according to schedule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#min_required_replicas GoogleComputeRegionAutoscaler#min_required_replicas}
        '''
        result = self._values.get("min_required_replicas")
        assert result is not None, "Required property 'min_required_replicas' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#name GoogleComputeRegionAutoscaler#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schedule(self) -> builtins.str:
        '''The start timestamps of time intervals when this scaling schedule should provide a scaling signal.

        This field uses the extended cron format (with an optional year field).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#schedule GoogleComputeRegionAutoscaler#schedule}
        '''
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of a scaling schedule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#description GoogleComputeRegionAutoscaler#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A boolean value that specifies if a scaling schedule can influence autoscaler recommendations.

        If set to true, then a scaling schedule has no effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#disabled GoogleComputeRegionAutoscaler#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[builtins.str]:
        '''The time zone to be used when interpreting the schedule.

        The value of this field must be a time zone name from the tz database: http://en.wikipedia.org/wiki/Tz_database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#time_zone GoogleComputeRegionAutoscaler#time_zone}
        '''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionAutoscalerAutoscalingPolicyScalingSchedules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionAutoscalerAutoscalingPolicyScalingSchedulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionAutoscaler.GoogleComputeRegionAutoscalerAutoscalingPolicyScalingSchedulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f5fc5dce1f77ab79303c0545e48193d4c561ab58207195063bdd1c74a6c1bd0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeRegionAutoscalerAutoscalingPolicyScalingSchedulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__697101fa96fdde1cf391c6a623ea2bb39ca114530a31e403609eac88838dcc2b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeRegionAutoscalerAutoscalingPolicyScalingSchedulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acf7871fce99aeb3557cd22b7a863df4f02b64b57ec75d7283fe9afc9e9e25cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bf22b10f8e9d5f0935f5245a25abcbda629236679b41befdd72a84de5a27077)
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
            type_hints = typing.get_type_hints(_typecheckingstub__08b263e394039d34e913a6ca290d81bd92be3f680a4366fbfe8cb6bd69b45bab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionAutoscalerAutoscalingPolicyScalingSchedules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionAutoscalerAutoscalingPolicyScalingSchedules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionAutoscalerAutoscalingPolicyScalingSchedules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe80e11f459155fcc29958e91702300f366b3f8ab0f6eb94cff629a2d914764b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeRegionAutoscalerAutoscalingPolicyScalingSchedulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionAutoscaler.GoogleComputeRegionAutoscalerAutoscalingPolicyScalingSchedulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f75fbfc001d13420f19ad09949c2e3ccd00f70d7beaebd5a1c0d9f4d5334bee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40432f6e7a4755c03307e40f3492cff3a7f9e40ef73c9be988ca1efec81a6a06)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b4fdb01c8446211febf348af9546f01b7ff1d77949aa3c0b2378cbfde4ee38c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="durationSec")
    def duration_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "durationSec"))

    @duration_sec.setter
    def duration_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccfec37df22513e538a291e95e05a6a0a79e91fb9b3a84817026af8b9b269516)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "durationSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minRequiredReplicas")
    def min_required_replicas(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minRequiredReplicas"))

    @min_required_replicas.setter
    def min_required_replicas(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2352da74c25b4953b364face72bd845c3df0aefce49ea0db35a6af112ee2c875)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minRequiredReplicas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdb1685409482fd97501de8684826e815e30aac901fd45261e50716e90ccf0ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedule"))

    @schedule.setter
    def schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43c6b74f02c75fb8c8d1c79d8661a93f7021d8771a267750ad6b0dfdffa76413)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d944a471e5d36d589cc3a1623cf3ec99f91ab1a7bb0f46c144378f0d337ddc86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionAutoscalerAutoscalingPolicyScalingSchedules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionAutoscalerAutoscalingPolicyScalingSchedules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionAutoscalerAutoscalingPolicyScalingSchedules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54f9592e53523e2ecbc5a4472d47b9594d5b5ab4a74968705382cd76b0bd1a4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionAutoscaler.GoogleComputeRegionAutoscalerConfig",
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
class GoogleComputeRegionAutoscalerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        autoscaling_policy: typing.Union[GoogleComputeRegionAutoscalerAutoscalingPolicy, typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        target: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeRegionAutoscalerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param autoscaling_policy: autoscaling_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#autoscaling_policy GoogleComputeRegionAutoscaler#autoscaling_policy}
        :param name: Name of the resource. The name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#name GoogleComputeRegionAutoscaler#name}
        :param target: URL of the managed instance group that this autoscaler will scale. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#target GoogleComputeRegionAutoscaler#target}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#description GoogleComputeRegionAutoscaler#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#id GoogleComputeRegionAutoscaler#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#project GoogleComputeRegionAutoscaler#project}.
        :param region: URL of the region where the instance group resides. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#region GoogleComputeRegionAutoscaler#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#timeouts GoogleComputeRegionAutoscaler#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(autoscaling_policy, dict):
            autoscaling_policy = GoogleComputeRegionAutoscalerAutoscalingPolicy(**autoscaling_policy)
        if isinstance(timeouts, dict):
            timeouts = GoogleComputeRegionAutoscalerTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0d23ac7c84075f5667474bfa10879d50308790600a7e8365a6fbbf93625e4b8)
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
    def autoscaling_policy(self) -> GoogleComputeRegionAutoscalerAutoscalingPolicy:
        '''autoscaling_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#autoscaling_policy GoogleComputeRegionAutoscaler#autoscaling_policy}
        '''
        result = self._values.get("autoscaling_policy")
        assert result is not None, "Required property 'autoscaling_policy' is missing"
        return typing.cast(GoogleComputeRegionAutoscalerAutoscalingPolicy, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the resource.

        The name must be 1-63 characters long and match
        the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the
        first character must be a lowercase letter, and all following
        characters must be a dash, lowercase letter, or digit, except the last
        character, which cannot be a dash.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#name GoogleComputeRegionAutoscaler#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> builtins.str:
        '''URL of the managed instance group that this autoscaler will scale.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#target GoogleComputeRegionAutoscaler#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#description GoogleComputeRegionAutoscaler#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#id GoogleComputeRegionAutoscaler#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#project GoogleComputeRegionAutoscaler#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''URL of the region where the instance group resides.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#region GoogleComputeRegionAutoscaler#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleComputeRegionAutoscalerTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#timeouts GoogleComputeRegionAutoscaler#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleComputeRegionAutoscalerTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionAutoscalerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionAutoscaler.GoogleComputeRegionAutoscalerTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleComputeRegionAutoscalerTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#create GoogleComputeRegionAutoscaler#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#delete GoogleComputeRegionAutoscaler#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#update GoogleComputeRegionAutoscaler#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8239c6a46c1012be04747de5cece4538c8e6e2f3da90deea1b3d861bbaa5ba8c)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#create GoogleComputeRegionAutoscaler#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#delete GoogleComputeRegionAutoscaler#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_autoscaler#update GoogleComputeRegionAutoscaler#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionAutoscalerTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionAutoscalerTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionAutoscaler.GoogleComputeRegionAutoscalerTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a51388f6c45546e9f5081d83738e239ef4c4214df6b77de12d4688536c4b0b70)
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
            type_hints = typing.get_type_hints(_typecheckingstub__defe2b96b54410f83f9aad4361076b6be56272da9aa0512365e24cd5cf731a2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9cf56ae9e8c72545bc1328dd6ee5af810625ff7e72580cf2a13b448aa8f0c9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50b7200f0fc4305fa03611efefdaafb8f72696fe9efbad4c5f1add925652c709)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionAutoscalerTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionAutoscalerTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionAutoscalerTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aa0859db498679ee2efbf6d0c8534aeb12c025e4d56d3d71a3c781913003107)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleComputeRegionAutoscaler",
    "GoogleComputeRegionAutoscalerAutoscalingPolicy",
    "GoogleComputeRegionAutoscalerAutoscalingPolicyCpuUtilization",
    "GoogleComputeRegionAutoscalerAutoscalingPolicyCpuUtilizationOutputReference",
    "GoogleComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilization",
    "GoogleComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilizationOutputReference",
    "GoogleComputeRegionAutoscalerAutoscalingPolicyMetric",
    "GoogleComputeRegionAutoscalerAutoscalingPolicyMetricList",
    "GoogleComputeRegionAutoscalerAutoscalingPolicyMetricOutputReference",
    "GoogleComputeRegionAutoscalerAutoscalingPolicyOutputReference",
    "GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControl",
    "GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicas",
    "GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicasOutputReference",
    "GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControlOutputReference",
    "GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControl",
    "GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas",
    "GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicasOutputReference",
    "GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControlOutputReference",
    "GoogleComputeRegionAutoscalerAutoscalingPolicyScalingSchedules",
    "GoogleComputeRegionAutoscalerAutoscalingPolicyScalingSchedulesList",
    "GoogleComputeRegionAutoscalerAutoscalingPolicyScalingSchedulesOutputReference",
    "GoogleComputeRegionAutoscalerConfig",
    "GoogleComputeRegionAutoscalerTimeouts",
    "GoogleComputeRegionAutoscalerTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__43d3963a5ed830be20adf5076b34cc616450ddad621de77f87318b664bd6329b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    autoscaling_policy: typing.Union[GoogleComputeRegionAutoscalerAutoscalingPolicy, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    target: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeRegionAutoscalerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__3e7b183c6f74ff003b4e7231f54c5905f38daf944f2de54dd66d8979ff62825d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6058414ffd4581009a2ef2c4a050c7bc037f261eff3e9213f1e5d37ea49f79e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc2a77b9e6760543adcfee6b82b6019506c51250bf145f9f98e556255ff3e2d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b84011ba6d5bceafebaa0ee53269219340612168abbf9aa75d96d8251ca2c23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5864410e590d209ee927766e8f3b71775c08c21ce80c860e5e9db58c716799e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__306f1535be2fe55d0e92424b04563135a1cb0651d163dd114cab98a6897cb036(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__471d2640c6ab7c995a7f9df7befb745d74cc667e3ff34631fcc88a7499f31ff3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ea6040ef0d109d3c3d2fcdc3452a061b039f009e672d8d3254ca9825a403f5c(
    *,
    max_replicas: jsii.Number,
    min_replicas: jsii.Number,
    cooldown_period: typing.Optional[jsii.Number] = None,
    cpu_utilization: typing.Optional[typing.Union[GoogleComputeRegionAutoscalerAutoscalingPolicyCpuUtilization, typing.Dict[builtins.str, typing.Any]]] = None,
    load_balancing_utilization: typing.Optional[typing.Union[GoogleComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilization, typing.Dict[builtins.str, typing.Any]]] = None,
    metric: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRegionAutoscalerAutoscalingPolicyMetric, typing.Dict[builtins.str, typing.Any]]]]] = None,
    mode: typing.Optional[builtins.str] = None,
    scale_down_control: typing.Optional[typing.Union[GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControl, typing.Dict[builtins.str, typing.Any]]] = None,
    scale_in_control: typing.Optional[typing.Union[GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControl, typing.Dict[builtins.str, typing.Any]]] = None,
    scaling_schedules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRegionAutoscalerAutoscalingPolicyScalingSchedules, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b3faa7953f374ae9c7385e4d4abce6621b43855d5795e1df0800d08b7047093(
    *,
    target: jsii.Number,
    predictive_method: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__159de316292aa693ffe550128d5a3ffe7c901dae483f6a1982e0aad85c4c8111(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ef4180a1a6e95641b4dc06ec33d0b5aeec2544eb0c6f0eeba22344bc341e831(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a97066c298a34d87aca4570ce23ecdf997399ea5bafb6f78d0937823bd0df888(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db991e462ae6c23e16ce25d2ca71a8fa8feeea024130daad542f155ed5942f98(
    value: typing.Optional[GoogleComputeRegionAutoscalerAutoscalingPolicyCpuUtilization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9314a8e6c68c104f9da843ca37ef09ad6c96dc344d1d57446583b7556aa0c48e(
    *,
    target: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d98e6f1d4b2269bf530cca1fe5d3cd069990fc880fb959279c5a0aa77617720(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01d284c8db7a41efeb62a9d5b506330fd56f36472c2a2a3c33c3c54891d2d9d5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3544aa376aaec1dd80962b84f6736232f6e72f12239e0580e7016c6b5db0849c(
    value: typing.Optional[GoogleComputeRegionAutoscalerAutoscalingPolicyLoadBalancingUtilization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a1ebe788840a0b4a72c168b19c69d45f61db2ce1855f21e721d2176e680c945(
    *,
    name: builtins.str,
    filter: typing.Optional[builtins.str] = None,
    single_instance_assignment: typing.Optional[jsii.Number] = None,
    target: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53afd30460c6ea83ed1a21c67eb6e3b0448219a065eb6e764324f94070b134a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d55ff1a2cbbe581510ccd984137cbcb331f5f5b27e16d669a66fd508b656111(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca077246f3c7f465845445d618ee7593bcee2933953da702cca4f84ec62a12e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42dea22963975b11474cd576494747aea7140634703b638f5f97b29bffb5b302(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b41fa7845034f381979c902f767d64ba7a8182ee46931760e38c88cfca8c2488(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12de7f80a56761edd6c1cb2bde1ed17b906ded9ce21b866b82ac14b0588fab9a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionAutoscalerAutoscalingPolicyMetric]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf349c1be5f0565e4160ed9bb2ee52e30e4478b33db71db9eaf313cf4cd6baaa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a4e6570f121855f7454ec0026f042c8822679502d2fb88249c00de4fb3867d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45b6eb26b26670e62de290cc52551dd35c5863fb1a08b712f239cff28b27fdc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfcfbc096c030a0aac5f98dce8aabfcaa427ac9f68a61da21af46d92ddb9efb1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9254e582ad7bf991d131ebc723ec4546b6d1dcf4a42b5badee75426f5b697418(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe655e287a65c32b488959722b692697de7d595b791c7a2dbbbab221ba1ebcae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cc8c39405353c46f6709265c62c9d268786e5cd69b7315a0e527c21a0814196(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionAutoscalerAutoscalingPolicyMetric]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb45a03e3af9b18d93711915618e361bb3618f6d707a66e4e0a979ee2e336076(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfa2e640cd18c8e829490ddd17309a891cd38688511a86a8015ea951b0650d5a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRegionAutoscalerAutoscalingPolicyMetric, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9120b1ae40b1cc0b23e5004d71b83795b00d703f8350bc7f7ab4fc13ed9f5d96(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRegionAutoscalerAutoscalingPolicyScalingSchedules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d85b9a8202653c6bdfdf2d39d99703587554fb05b927af5bff8682a0f68be00(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c166459ee6ed395fdb562e434bede16593b953967d4aefbc0d9088455cc4f847(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe4fb4ebca429b29ac59c641bb1561cd7071abe1838dec039d9be728c698ef21(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d89090ab00b42243fb656be3a53d8d1dc196ceff39b91ad2b3d11509909d83a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__734553d7cde02e6537d235fe451e9d0451d24d72b76764f859069fdc378bc8af(
    value: typing.Optional[GoogleComputeRegionAutoscalerAutoscalingPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98d29c519a7c583cd4387ac10f6632b9af98634a857711a0140481575f71fb11(
    *,
    max_scaled_down_replicas: typing.Optional[typing.Union[GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicas, typing.Dict[builtins.str, typing.Any]]] = None,
    time_window_sec: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58bed10fcb8e130cd7ac779305dae0855a35f905ddae42781b41d87e2eefb15c(
    *,
    fixed: typing.Optional[jsii.Number] = None,
    percent: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c308268a57916b6596bc641e8740efb6675635b8af5d7a2813fe1bfb41f25d6d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12988a39b34d242258a85980bc57b55cb15e1790a62790a3a241e8c3510fd7d2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__421bd105208eb4f34bad4a29f30a16387327bb200aee2396cbb1e15aeef5633d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__356cddca41a94ff6e4cbef90fcbee4d6c51047379b26aa4f76d8b2166c641d33(
    value: typing.Optional[GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicas],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d788a74f5f54ed224bb77d2539cc920b9bf74b366f36660715c7cf8c8e44f1ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33f93863e23d6a3e5dfa5e60c1d03685950720b635a7e0e6ccefed5bc09bd011(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__963b06e23f34811e8b8ea523bc511a2a49cf5c26c5619b170817ef2ba32b35a7(
    value: typing.Optional[GoogleComputeRegionAutoscalerAutoscalingPolicyScaleDownControl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f4c562c9ae9b04b783186677fd0c39f92f6b9bcb44aab90e118fb57afb14ded(
    *,
    max_scaled_in_replicas: typing.Optional[typing.Union[GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas, typing.Dict[builtins.str, typing.Any]]] = None,
    time_window_sec: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f477c222b9d27b0ac4228d94808f8d1fa0f04c2976dba57dd0e7cab519f0eec(
    *,
    fixed: typing.Optional[jsii.Number] = None,
    percent: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6426f30e8f7572d62dbc05bc0435d0e8cff8835aa5bc988682b5ff27c785f73(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fd35909166ec1444b435106d900ec8db0993baa219ead258f7359cff761b566(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f95cf5bba5b8e563b64adac3e07e4ace02b1ec7694ef8f95b8cd44b1c4730fb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__340a179858fb72547bf64dbe792c43b5b562dba809938ea15a7d3182a63148da(
    value: typing.Optional[GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b5baa30ae3d9ecfde0a90c2522f35489c183fffc64366bd158e40c8634b52be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba71a1b85e160aca92e9869c9f2d6b8e62e120713d4b9037dd88bac40ebd732a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__235c2846889a9c148b2068f9f8ce7c444ec501fba8040ff9a94e082f9fd380ba(
    value: typing.Optional[GoogleComputeRegionAutoscalerAutoscalingPolicyScaleInControl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c197b1e3857035187596b5c69068403482f87108f7343900aadd816580a2aed7(
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

def _typecheckingstub__2f5fc5dce1f77ab79303c0545e48193d4c561ab58207195063bdd1c74a6c1bd0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__697101fa96fdde1cf391c6a623ea2bb39ca114530a31e403609eac88838dcc2b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acf7871fce99aeb3557cd22b7a863df4f02b64b57ec75d7283fe9afc9e9e25cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bf22b10f8e9d5f0935f5245a25abcbda629236679b41befdd72a84de5a27077(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08b263e394039d34e913a6ca290d81bd92be3f680a4366fbfe8cb6bd69b45bab(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe80e11f459155fcc29958e91702300f366b3f8ab0f6eb94cff629a2d914764b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionAutoscalerAutoscalingPolicyScalingSchedules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f75fbfc001d13420f19ad09949c2e3ccd00f70d7beaebd5a1c0d9f4d5334bee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40432f6e7a4755c03307e40f3492cff3a7f9e40ef73c9be988ca1efec81a6a06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b4fdb01c8446211febf348af9546f01b7ff1d77949aa3c0b2378cbfde4ee38c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccfec37df22513e538a291e95e05a6a0a79e91fb9b3a84817026af8b9b269516(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2352da74c25b4953b364face72bd845c3df0aefce49ea0db35a6af112ee2c875(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdb1685409482fd97501de8684826e815e30aac901fd45261e50716e90ccf0ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43c6b74f02c75fb8c8d1c79d8661a93f7021d8771a267750ad6b0dfdffa76413(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d944a471e5d36d589cc3a1623cf3ec99f91ab1a7bb0f46c144378f0d337ddc86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54f9592e53523e2ecbc5a4472d47b9594d5b5ab4a74968705382cd76b0bd1a4b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionAutoscalerAutoscalingPolicyScalingSchedules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0d23ac7c84075f5667474bfa10879d50308790600a7e8365a6fbbf93625e4b8(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    autoscaling_policy: typing.Union[GoogleComputeRegionAutoscalerAutoscalingPolicy, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    target: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeRegionAutoscalerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8239c6a46c1012be04747de5cece4538c8e6e2f3da90deea1b3d861bbaa5ba8c(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a51388f6c45546e9f5081d83738e239ef4c4214df6b77de12d4688536c4b0b70(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__defe2b96b54410f83f9aad4361076b6be56272da9aa0512365e24cd5cf731a2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9cf56ae9e8c72545bc1328dd6ee5af810625ff7e72580cf2a13b448aa8f0c9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50b7200f0fc4305fa03611efefdaafb8f72696fe9efbad4c5f1add925652c709(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aa0859db498679ee2efbf6d0c8534aeb12c025e4d56d3d71a3c781913003107(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionAutoscalerTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
