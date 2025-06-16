r'''
# `google_compute_autoscaler`

Refer to the Terraform Registry for docs: [`google_compute_autoscaler`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler).
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


class GoogleComputeAutoscaler(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeAutoscaler.GoogleComputeAutoscaler",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler google_compute_autoscaler}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        autoscaling_policy: typing.Union["GoogleComputeAutoscalerAutoscalingPolicy", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        target: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeAutoscalerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        zone: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler google_compute_autoscaler} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param autoscaling_policy: autoscaling_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#autoscaling_policy GoogleComputeAutoscaler#autoscaling_policy}
        :param name: Name of the resource. The name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#name GoogleComputeAutoscaler#name}
        :param target: URL of the managed instance group that this autoscaler will scale. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#target GoogleComputeAutoscaler#target}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#description GoogleComputeAutoscaler#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#id GoogleComputeAutoscaler#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#project GoogleComputeAutoscaler#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#timeouts GoogleComputeAutoscaler#timeouts}
        :param zone: URL of the zone where the instance group resides. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#zone GoogleComputeAutoscaler#zone}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35cfbded27894277e07f097818258aa0e14afb0a66ff7496f4a68e6934ba69d8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleComputeAutoscalerConfig(
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
        '''Generates CDKTF code for importing a GoogleComputeAutoscaler resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleComputeAutoscaler to import.
        :param import_from_id: The id of the existing GoogleComputeAutoscaler that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleComputeAutoscaler to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78a8409fdd65732c56db0ac7a5af0d0cbfce6565b01096cf979c042c9eb3f25e)
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
        cpu_utilization: typing.Optional[typing.Union["GoogleComputeAutoscalerAutoscalingPolicyCpuUtilization", typing.Dict[builtins.str, typing.Any]]] = None,
        load_balancing_utilization: typing.Optional[typing.Union["GoogleComputeAutoscalerAutoscalingPolicyLoadBalancingUtilization", typing.Dict[builtins.str, typing.Any]]] = None,
        metric: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeAutoscalerAutoscalingPolicyMetric", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mode: typing.Optional[builtins.str] = None,
        scale_down_control: typing.Optional[typing.Union["GoogleComputeAutoscalerAutoscalingPolicyScaleDownControl", typing.Dict[builtins.str, typing.Any]]] = None,
        scale_in_control: typing.Optional[typing.Union["GoogleComputeAutoscalerAutoscalingPolicyScaleInControl", typing.Dict[builtins.str, typing.Any]]] = None,
        scaling_schedules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeAutoscalerAutoscalingPolicyScalingSchedules", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param max_replicas: The maximum number of instances that the autoscaler can scale up to. This is required when creating or updating an autoscaler. The maximum number of replicas should not be lower than minimal number of replicas. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#max_replicas GoogleComputeAutoscaler#max_replicas}
        :param min_replicas: The minimum number of replicas that the autoscaler can scale down to. This cannot be less than 0. If not provided, autoscaler will choose a default value depending on maximum number of instances allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#min_replicas GoogleComputeAutoscaler#min_replicas}
        :param cooldown_period: The number of seconds that the autoscaler should wait before it starts collecting information from a new instance. This prevents the autoscaler from collecting information when the instance is initializing, during which the collected usage would not be reliable. The default time autoscaler waits is 60 seconds. Virtual machine initialization times might vary because of numerous factors. We recommend that you test how long an instance may take to initialize. To do this, create an instance and time the startup process. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#cooldown_period GoogleComputeAutoscaler#cooldown_period}
        :param cpu_utilization: cpu_utilization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#cpu_utilization GoogleComputeAutoscaler#cpu_utilization}
        :param load_balancing_utilization: load_balancing_utilization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#load_balancing_utilization GoogleComputeAutoscaler#load_balancing_utilization}
        :param metric: metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#metric GoogleComputeAutoscaler#metric}
        :param mode: Defines operating mode for this policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#mode GoogleComputeAutoscaler#mode}
        :param scale_down_control: scale_down_control block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#scale_down_control GoogleComputeAutoscaler#scale_down_control}
        :param scale_in_control: scale_in_control block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#scale_in_control GoogleComputeAutoscaler#scale_in_control}
        :param scaling_schedules: scaling_schedules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#scaling_schedules GoogleComputeAutoscaler#scaling_schedules}
        '''
        value = GoogleComputeAutoscalerAutoscalingPolicy(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#create GoogleComputeAutoscaler#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#delete GoogleComputeAutoscaler#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#update GoogleComputeAutoscaler#update}.
        '''
        value = GoogleComputeAutoscalerTimeouts(
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
    def autoscaling_policy(
        self,
    ) -> "GoogleComputeAutoscalerAutoscalingPolicyOutputReference":
        return typing.cast("GoogleComputeAutoscalerAutoscalingPolicyOutputReference", jsii.get(self, "autoscalingPolicy"))

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
    def timeouts(self) -> "GoogleComputeAutoscalerTimeoutsOutputReference":
        return typing.cast("GoogleComputeAutoscalerTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingPolicyInput")
    def autoscaling_policy_input(
        self,
    ) -> typing.Optional["GoogleComputeAutoscalerAutoscalingPolicy"]:
        return typing.cast(typing.Optional["GoogleComputeAutoscalerAutoscalingPolicy"], jsii.get(self, "autoscalingPolicyInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeAutoscalerTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeAutoscalerTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c5103d4e65778950bf463d20f40cadad7e3f40c98e7ceaa28184290e04de43b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d489135bb540b32a0906068e2bffa6e32cb004ea3292702d3afe6b10dc62d3fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4140dbadbb8d3f116a41d2d692d6b9f20e572b04e353dd129355a9094760637)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aec26b02355648d1c9f89dbc847c01bcec611c5614d3e621625a1efa6398cc9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9890252bad29b39fb1b60df36312356c1a2685669b9e44d8e3098ab46786fa3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8fc9556f106774a89192987fe594bfe1203a3d70c4b1f65faabb999267a690d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeAutoscaler.GoogleComputeAutoscalerAutoscalingPolicy",
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
class GoogleComputeAutoscalerAutoscalingPolicy:
    def __init__(
        self,
        *,
        max_replicas: jsii.Number,
        min_replicas: jsii.Number,
        cooldown_period: typing.Optional[jsii.Number] = None,
        cpu_utilization: typing.Optional[typing.Union["GoogleComputeAutoscalerAutoscalingPolicyCpuUtilization", typing.Dict[builtins.str, typing.Any]]] = None,
        load_balancing_utilization: typing.Optional[typing.Union["GoogleComputeAutoscalerAutoscalingPolicyLoadBalancingUtilization", typing.Dict[builtins.str, typing.Any]]] = None,
        metric: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeAutoscalerAutoscalingPolicyMetric", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mode: typing.Optional[builtins.str] = None,
        scale_down_control: typing.Optional[typing.Union["GoogleComputeAutoscalerAutoscalingPolicyScaleDownControl", typing.Dict[builtins.str, typing.Any]]] = None,
        scale_in_control: typing.Optional[typing.Union["GoogleComputeAutoscalerAutoscalingPolicyScaleInControl", typing.Dict[builtins.str, typing.Any]]] = None,
        scaling_schedules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeAutoscalerAutoscalingPolicyScalingSchedules", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param max_replicas: The maximum number of instances that the autoscaler can scale up to. This is required when creating or updating an autoscaler. The maximum number of replicas should not be lower than minimal number of replicas. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#max_replicas GoogleComputeAutoscaler#max_replicas}
        :param min_replicas: The minimum number of replicas that the autoscaler can scale down to. This cannot be less than 0. If not provided, autoscaler will choose a default value depending on maximum number of instances allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#min_replicas GoogleComputeAutoscaler#min_replicas}
        :param cooldown_period: The number of seconds that the autoscaler should wait before it starts collecting information from a new instance. This prevents the autoscaler from collecting information when the instance is initializing, during which the collected usage would not be reliable. The default time autoscaler waits is 60 seconds. Virtual machine initialization times might vary because of numerous factors. We recommend that you test how long an instance may take to initialize. To do this, create an instance and time the startup process. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#cooldown_period GoogleComputeAutoscaler#cooldown_period}
        :param cpu_utilization: cpu_utilization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#cpu_utilization GoogleComputeAutoscaler#cpu_utilization}
        :param load_balancing_utilization: load_balancing_utilization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#load_balancing_utilization GoogleComputeAutoscaler#load_balancing_utilization}
        :param metric: metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#metric GoogleComputeAutoscaler#metric}
        :param mode: Defines operating mode for this policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#mode GoogleComputeAutoscaler#mode}
        :param scale_down_control: scale_down_control block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#scale_down_control GoogleComputeAutoscaler#scale_down_control}
        :param scale_in_control: scale_in_control block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#scale_in_control GoogleComputeAutoscaler#scale_in_control}
        :param scaling_schedules: scaling_schedules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#scaling_schedules GoogleComputeAutoscaler#scaling_schedules}
        '''
        if isinstance(cpu_utilization, dict):
            cpu_utilization = GoogleComputeAutoscalerAutoscalingPolicyCpuUtilization(**cpu_utilization)
        if isinstance(load_balancing_utilization, dict):
            load_balancing_utilization = GoogleComputeAutoscalerAutoscalingPolicyLoadBalancingUtilization(**load_balancing_utilization)
        if isinstance(scale_down_control, dict):
            scale_down_control = GoogleComputeAutoscalerAutoscalingPolicyScaleDownControl(**scale_down_control)
        if isinstance(scale_in_control, dict):
            scale_in_control = GoogleComputeAutoscalerAutoscalingPolicyScaleInControl(**scale_in_control)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55d24525b45015d95cb55e37957a924ee50a56bf8ea33511b51c578b11f8ce79)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#max_replicas GoogleComputeAutoscaler#max_replicas}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#min_replicas GoogleComputeAutoscaler#min_replicas}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#cooldown_period GoogleComputeAutoscaler#cooldown_period}
        '''
        result = self._values.get("cooldown_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cpu_utilization(
        self,
    ) -> typing.Optional["GoogleComputeAutoscalerAutoscalingPolicyCpuUtilization"]:
        '''cpu_utilization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#cpu_utilization GoogleComputeAutoscaler#cpu_utilization}
        '''
        result = self._values.get("cpu_utilization")
        return typing.cast(typing.Optional["GoogleComputeAutoscalerAutoscalingPolicyCpuUtilization"], result)

    @builtins.property
    def load_balancing_utilization(
        self,
    ) -> typing.Optional["GoogleComputeAutoscalerAutoscalingPolicyLoadBalancingUtilization"]:
        '''load_balancing_utilization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#load_balancing_utilization GoogleComputeAutoscaler#load_balancing_utilization}
        '''
        result = self._values.get("load_balancing_utilization")
        return typing.cast(typing.Optional["GoogleComputeAutoscalerAutoscalingPolicyLoadBalancingUtilization"], result)

    @builtins.property
    def metric(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeAutoscalerAutoscalingPolicyMetric"]]]:
        '''metric block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#metric GoogleComputeAutoscaler#metric}
        '''
        result = self._values.get("metric")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeAutoscalerAutoscalingPolicyMetric"]]], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Defines operating mode for this policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#mode GoogleComputeAutoscaler#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scale_down_control(
        self,
    ) -> typing.Optional["GoogleComputeAutoscalerAutoscalingPolicyScaleDownControl"]:
        '''scale_down_control block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#scale_down_control GoogleComputeAutoscaler#scale_down_control}
        '''
        result = self._values.get("scale_down_control")
        return typing.cast(typing.Optional["GoogleComputeAutoscalerAutoscalingPolicyScaleDownControl"], result)

    @builtins.property
    def scale_in_control(
        self,
    ) -> typing.Optional["GoogleComputeAutoscalerAutoscalingPolicyScaleInControl"]:
        '''scale_in_control block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#scale_in_control GoogleComputeAutoscaler#scale_in_control}
        '''
        result = self._values.get("scale_in_control")
        return typing.cast(typing.Optional["GoogleComputeAutoscalerAutoscalingPolicyScaleInControl"], result)

    @builtins.property
    def scaling_schedules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeAutoscalerAutoscalingPolicyScalingSchedules"]]]:
        '''scaling_schedules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#scaling_schedules GoogleComputeAutoscaler#scaling_schedules}
        '''
        result = self._values.get("scaling_schedules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeAutoscalerAutoscalingPolicyScalingSchedules"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeAutoscalerAutoscalingPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeAutoscaler.GoogleComputeAutoscalerAutoscalingPolicyCpuUtilization",
    jsii_struct_bases=[],
    name_mapping={"target": "target", "predictive_method": "predictiveMethod"},
)
class GoogleComputeAutoscalerAutoscalingPolicyCpuUtilization:
    def __init__(
        self,
        *,
        target: jsii.Number,
        predictive_method: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target: The target CPU utilization that the autoscaler should maintain. Must be a float value in the range (0, 1]. If not specified, the default is 0.6. If the CPU level is below the target utilization, the autoscaler scales down the number of instances until it reaches the minimum number of instances you specified or until the average CPU of your instances reaches the target utilization. If the average CPU is above the target utilization, the autoscaler scales up until it reaches the maximum number of instances you specified or until the average utilization reaches the target utilization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#target GoogleComputeAutoscaler#target}
        :param predictive_method: Indicates whether predictive autoscaling based on CPU metric is enabled. Valid values are:. - NONE (default). No predictive method is used. The autoscaler scales the group to meet current demand based on real-time metrics. - OPTIMIZE_AVAILABILITY. Predictive autoscaling improves availability by monitoring daily and weekly load patterns and scaling out ahead of anticipated demand. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#predictive_method GoogleComputeAutoscaler#predictive_method}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c60eba81dcaf226575edc1561d1da97e5eed2d8124422e4df9d6ec2f2e42a4c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#target GoogleComputeAutoscaler#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def predictive_method(self) -> typing.Optional[builtins.str]:
        '''Indicates whether predictive autoscaling based on CPU metric is enabled. Valid values are:.

        - NONE (default). No predictive method is used. The autoscaler scales the group to meet current demand based on real-time metrics.
        - OPTIMIZE_AVAILABILITY. Predictive autoscaling improves availability by monitoring daily and weekly load patterns and scaling out ahead of anticipated demand.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#predictive_method GoogleComputeAutoscaler#predictive_method}
        '''
        result = self._values.get("predictive_method")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeAutoscalerAutoscalingPolicyCpuUtilization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeAutoscalerAutoscalingPolicyCpuUtilizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeAutoscaler.GoogleComputeAutoscalerAutoscalingPolicyCpuUtilizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cae74129c409a0e1aecc2ac49d4809f7eac42876465443d52ab64d455cd61923)
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
            type_hints = typing.get_type_hints(_typecheckingstub__96268fcaacb41b5eddc892ffa7edfd1d17529ca9fa0c7bcacbe63a72d0c12ed0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "predictiveMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "target"))

    @target.setter
    def target(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c22e215740840dfca5b9929ed920558ad91883d732badeb02855ffc88859d09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeAutoscalerAutoscalingPolicyCpuUtilization]:
        return typing.cast(typing.Optional[GoogleComputeAutoscalerAutoscalingPolicyCpuUtilization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeAutoscalerAutoscalingPolicyCpuUtilization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f028144fc365ac513b39bffb7b934268c09920c252b599d5a1b03b9a057e573a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeAutoscaler.GoogleComputeAutoscalerAutoscalingPolicyLoadBalancingUtilization",
    jsii_struct_bases=[],
    name_mapping={"target": "target"},
)
class GoogleComputeAutoscalerAutoscalingPolicyLoadBalancingUtilization:
    def __init__(self, *, target: jsii.Number) -> None:
        '''
        :param target: Fraction of backend capacity utilization (set in HTTP(s) load balancing configuration) that autoscaler should maintain. Must be a positive float value. If not defined, the default is 0.8. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#target GoogleComputeAutoscaler#target}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e21469fc21ddc38cb1d2efe7615091c9f825b853385aef01bdd6663983c434ff)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target": target,
        }

    @builtins.property
    def target(self) -> jsii.Number:
        '''Fraction of backend capacity utilization (set in HTTP(s) load balancing configuration) that autoscaler should maintain.

        Must
        be a positive float value. If not defined, the default is 0.8.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#target GoogleComputeAutoscaler#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeAutoscalerAutoscalingPolicyLoadBalancingUtilization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeAutoscalerAutoscalingPolicyLoadBalancingUtilizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeAutoscaler.GoogleComputeAutoscalerAutoscalingPolicyLoadBalancingUtilizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__653535b6b3dcd84e3faebec1eb361f8a031cb7b91359720b0cd42436fdb00ab3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea97fbd446c58c29108e569eba01c4bf25ba24b10ac0e1dce6a2e66b3eba1f73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeAutoscalerAutoscalingPolicyLoadBalancingUtilization]:
        return typing.cast(typing.Optional[GoogleComputeAutoscalerAutoscalingPolicyLoadBalancingUtilization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeAutoscalerAutoscalingPolicyLoadBalancingUtilization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23022660bf3fc0b5f84188e86a0817578a2d4e59bd88ae048aacb32023996295)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeAutoscaler.GoogleComputeAutoscalerAutoscalingPolicyMetric",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "filter": "filter",
        "single_instance_assignment": "singleInstanceAssignment",
        "target": "target",
        "type": "type",
    },
)
class GoogleComputeAutoscalerAutoscalingPolicyMetric:
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
        :param name: The identifier (type) of the Stackdriver Monitoring metric. The metric cannot have negative values. The metric must have a value type of INT64 or DOUBLE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#name GoogleComputeAutoscaler#name}
        :param filter: A filter string to be used as the filter string for a Stackdriver Monitoring TimeSeries.list API call. This filter is used to select a specific TimeSeries for the purpose of autoscaling and to determine whether the metric is exporting per-instance or per-group data. You can only use the AND operator for joining selectors. You can only use direct equality comparison operator (=) without any functions for each selector. You can specify the metric in both the filter string and in the metric field. However, if specified in both places, the metric must be identical. The monitored resource type determines what kind of values are expected for the metric. If it is a gce_instance, the autoscaler expects the metric to include a separate TimeSeries for each instance in a group. In such a case, you cannot filter on resource labels. If the resource type is any other value, the autoscaler expects this metric to contain values that apply to the entire autoscaled instance group and resource label filtering can be performed to point autoscaler at the correct TimeSeries to scale upon. This is called a per-group metric for the purpose of autoscaling. If not specified, the type defaults to gce_instance. You should provide a filter that is selective enough to pick just one TimeSeries for the autoscaled group or for each of the instances (if you are using gce_instance resource type). If multiple TimeSeries are returned upon the query execution, the autoscaler will sum their respective values to obtain its scaling value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#filter GoogleComputeAutoscaler#filter}
        :param single_instance_assignment: If scaling is based on a per-group metric value that represents the total amount of work to be done or resource usage, set this value to an amount assigned for a single instance of the scaled group. The autoscaler will keep the number of instances proportional to the value of this metric, the metric itself should not change value due to group resizing. For example, a good metric to use with the target is 'pubsub.googleapis.com/subscription/num_undelivered_messages' or a custom metric exporting the total number of requests coming to your instances. A bad example would be a metric exporting an average or median latency, since this value can't include a chunk assignable to a single instance, it could be better used with utilization_target instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#single_instance_assignment GoogleComputeAutoscaler#single_instance_assignment}
        :param target: The target value of the metric that autoscaler should maintain. This must be a positive value. A utilization metric scales number of virtual machines handling requests to increase or decrease proportionally to the metric. For example, a good metric to use as a utilizationTarget is www.googleapis.com/compute/instance/network/received_bytes_count. The autoscaler will work to keep this value constant for each of the instances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#target GoogleComputeAutoscaler#target}
        :param type: Defines how target utilization value is expressed for a Stackdriver Monitoring metric. Possible values: ["GAUGE", "DELTA_PER_SECOND", "DELTA_PER_MINUTE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#type GoogleComputeAutoscaler#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5aedf0959c220caf65320498af60bc14b1898dcacefd87e1f983cb73094f71b1)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#name GoogleComputeAutoscaler#name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#filter GoogleComputeAutoscaler#filter}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#single_instance_assignment GoogleComputeAutoscaler#single_instance_assignment}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#target GoogleComputeAutoscaler#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Defines how target utilization value is expressed for a Stackdriver Monitoring metric. Possible values: ["GAUGE", "DELTA_PER_SECOND", "DELTA_PER_MINUTE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#type GoogleComputeAutoscaler#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeAutoscalerAutoscalingPolicyMetric(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeAutoscalerAutoscalingPolicyMetricList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeAutoscaler.GoogleComputeAutoscalerAutoscalingPolicyMetricList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bacdde8d0c88f53ed1a0e2a5011b2385e7997cc5941c0a0f70e28b56d480edb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeAutoscalerAutoscalingPolicyMetricOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1ed1e651a3eb7e88e6a061f6391f008a13a13d3d090e7e4e50b593e9448de42)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeAutoscalerAutoscalingPolicyMetricOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27513c31ecbc0d4ce04a08d14797056fffa3e4cdfddbb6211fc445597e54fafb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be58e08f709659eb1c4e957eb4a0ddaa634da7c5bb30ed1bdec4bc365cbe28ed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4acacd5b404af0aca0575d55726de17e494e51dbd1fdde298cbf2120e94bbf6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeAutoscalerAutoscalingPolicyMetric]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeAutoscalerAutoscalingPolicyMetric]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeAutoscalerAutoscalingPolicyMetric]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__288fef0e1bd19c5f10faef2d9dd17d08ee805645cba286c9fba9e41f715c976f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeAutoscalerAutoscalingPolicyMetricOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeAutoscaler.GoogleComputeAutoscalerAutoscalingPolicyMetricOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7a81e99b5c9956c6473c1bca112d1651046dbe3412d2c3545fa4a81cce634cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__891c4a390d922706eeb7fc3a9af2869c09f45a07174721620a3a6f356fb78729)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c27bf916234d5fa18d4b50da96ed194af12cb6d0074930193e5b8dca9e7ad3a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="singleInstanceAssignment")
    def single_instance_assignment(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "singleInstanceAssignment"))

    @single_instance_assignment.setter
    def single_instance_assignment(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc28001472c752e4cd2176c9fde6139f09b78b7d9ba1febbe8d4e1aee291ed7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "singleInstanceAssignment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "target"))

    @target.setter
    def target(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a9348bf636dc14188387e6b9e0ef65e37671aa24c7ab81595cd73c8cbe00bcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6e276dd98faec36c028bbc292f002cd33ba1d80164223ee45a467de162f9da0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeAutoscalerAutoscalingPolicyMetric]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeAutoscalerAutoscalingPolicyMetric]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeAutoscalerAutoscalingPolicyMetric]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b51eafbb59a2df2026614987f3b5f8f39576b8c020c011b0322c832f354bf05d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeAutoscalerAutoscalingPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeAutoscaler.GoogleComputeAutoscalerAutoscalingPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1aebc62227187737793587d5e0c05af0f48001f52ea312179e059f4ab66c05ce)
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
        :param target: The target CPU utilization that the autoscaler should maintain. Must be a float value in the range (0, 1]. If not specified, the default is 0.6. If the CPU level is below the target utilization, the autoscaler scales down the number of instances until it reaches the minimum number of instances you specified or until the average CPU of your instances reaches the target utilization. If the average CPU is above the target utilization, the autoscaler scales up until it reaches the maximum number of instances you specified or until the average utilization reaches the target utilization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#target GoogleComputeAutoscaler#target}
        :param predictive_method: Indicates whether predictive autoscaling based on CPU metric is enabled. Valid values are:. - NONE (default). No predictive method is used. The autoscaler scales the group to meet current demand based on real-time metrics. - OPTIMIZE_AVAILABILITY. Predictive autoscaling improves availability by monitoring daily and weekly load patterns and scaling out ahead of anticipated demand. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#predictive_method GoogleComputeAutoscaler#predictive_method}
        '''
        value = GoogleComputeAutoscalerAutoscalingPolicyCpuUtilization(
            target=target, predictive_method=predictive_method
        )

        return typing.cast(None, jsii.invoke(self, "putCpuUtilization", [value]))

    @jsii.member(jsii_name="putLoadBalancingUtilization")
    def put_load_balancing_utilization(self, *, target: jsii.Number) -> None:
        '''
        :param target: Fraction of backend capacity utilization (set in HTTP(s) load balancing configuration) that autoscaler should maintain. Must be a positive float value. If not defined, the default is 0.8. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#target GoogleComputeAutoscaler#target}
        '''
        value = GoogleComputeAutoscalerAutoscalingPolicyLoadBalancingUtilization(
            target=target
        )

        return typing.cast(None, jsii.invoke(self, "putLoadBalancingUtilization", [value]))

    @jsii.member(jsii_name="putMetric")
    def put_metric(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeAutoscalerAutoscalingPolicyMetric, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__039a41627ed4c24f94ac9fdae7fb7cad70bdd7a1f741aa0ab6b8e463fd689e67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMetric", [value]))

    @jsii.member(jsii_name="putScaleDownControl")
    def put_scale_down_control(
        self,
        *,
        max_scaled_down_replicas: typing.Optional[typing.Union["GoogleComputeAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicas", typing.Dict[builtins.str, typing.Any]]] = None,
        time_window_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_scaled_down_replicas: max_scaled_down_replicas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#max_scaled_down_replicas GoogleComputeAutoscaler#max_scaled_down_replicas}
        :param time_window_sec: How long back autoscaling should look when computing recommendations to include directives regarding slower scale down, as described above. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#time_window_sec GoogleComputeAutoscaler#time_window_sec}
        '''
        value = GoogleComputeAutoscalerAutoscalingPolicyScaleDownControl(
            max_scaled_down_replicas=max_scaled_down_replicas,
            time_window_sec=time_window_sec,
        )

        return typing.cast(None, jsii.invoke(self, "putScaleDownControl", [value]))

    @jsii.member(jsii_name="putScaleInControl")
    def put_scale_in_control(
        self,
        *,
        max_scaled_in_replicas: typing.Optional[typing.Union["GoogleComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas", typing.Dict[builtins.str, typing.Any]]] = None,
        time_window_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_scaled_in_replicas: max_scaled_in_replicas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#max_scaled_in_replicas GoogleComputeAutoscaler#max_scaled_in_replicas}
        :param time_window_sec: How long back autoscaling should look when computing recommendations to include directives regarding slower scale down, as described above. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#time_window_sec GoogleComputeAutoscaler#time_window_sec}
        '''
        value = GoogleComputeAutoscalerAutoscalingPolicyScaleInControl(
            max_scaled_in_replicas=max_scaled_in_replicas,
            time_window_sec=time_window_sec,
        )

        return typing.cast(None, jsii.invoke(self, "putScaleInControl", [value]))

    @jsii.member(jsii_name="putScalingSchedules")
    def put_scaling_schedules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeAutoscalerAutoscalingPolicyScalingSchedules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__741b6de70d4b27bdd8245711113deac40c06a70d457367f2c43c87421ddc755a)
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
    ) -> GoogleComputeAutoscalerAutoscalingPolicyCpuUtilizationOutputReference:
        return typing.cast(GoogleComputeAutoscalerAutoscalingPolicyCpuUtilizationOutputReference, jsii.get(self, "cpuUtilization"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancingUtilization")
    def load_balancing_utilization(
        self,
    ) -> GoogleComputeAutoscalerAutoscalingPolicyLoadBalancingUtilizationOutputReference:
        return typing.cast(GoogleComputeAutoscalerAutoscalingPolicyLoadBalancingUtilizationOutputReference, jsii.get(self, "loadBalancingUtilization"))

    @builtins.property
    @jsii.member(jsii_name="metric")
    def metric(self) -> GoogleComputeAutoscalerAutoscalingPolicyMetricList:
        return typing.cast(GoogleComputeAutoscalerAutoscalingPolicyMetricList, jsii.get(self, "metric"))

    @builtins.property
    @jsii.member(jsii_name="scaleDownControl")
    def scale_down_control(
        self,
    ) -> "GoogleComputeAutoscalerAutoscalingPolicyScaleDownControlOutputReference":
        return typing.cast("GoogleComputeAutoscalerAutoscalingPolicyScaleDownControlOutputReference", jsii.get(self, "scaleDownControl"))

    @builtins.property
    @jsii.member(jsii_name="scaleInControl")
    def scale_in_control(
        self,
    ) -> "GoogleComputeAutoscalerAutoscalingPolicyScaleInControlOutputReference":
        return typing.cast("GoogleComputeAutoscalerAutoscalingPolicyScaleInControlOutputReference", jsii.get(self, "scaleInControl"))

    @builtins.property
    @jsii.member(jsii_name="scalingSchedules")
    def scaling_schedules(
        self,
    ) -> "GoogleComputeAutoscalerAutoscalingPolicyScalingSchedulesList":
        return typing.cast("GoogleComputeAutoscalerAutoscalingPolicyScalingSchedulesList", jsii.get(self, "scalingSchedules"))

    @builtins.property
    @jsii.member(jsii_name="cooldownPeriodInput")
    def cooldown_period_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cooldownPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuUtilizationInput")
    def cpu_utilization_input(
        self,
    ) -> typing.Optional[GoogleComputeAutoscalerAutoscalingPolicyCpuUtilization]:
        return typing.cast(typing.Optional[GoogleComputeAutoscalerAutoscalingPolicyCpuUtilization], jsii.get(self, "cpuUtilizationInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancingUtilizationInput")
    def load_balancing_utilization_input(
        self,
    ) -> typing.Optional[GoogleComputeAutoscalerAutoscalingPolicyLoadBalancingUtilization]:
        return typing.cast(typing.Optional[GoogleComputeAutoscalerAutoscalingPolicyLoadBalancingUtilization], jsii.get(self, "loadBalancingUtilizationInput"))

    @builtins.property
    @jsii.member(jsii_name="maxReplicasInput")
    def max_replicas_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxReplicasInput"))

    @builtins.property
    @jsii.member(jsii_name="metricInput")
    def metric_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeAutoscalerAutoscalingPolicyMetric]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeAutoscalerAutoscalingPolicyMetric]]], jsii.get(self, "metricInput"))

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
    ) -> typing.Optional["GoogleComputeAutoscalerAutoscalingPolicyScaleDownControl"]:
        return typing.cast(typing.Optional["GoogleComputeAutoscalerAutoscalingPolicyScaleDownControl"], jsii.get(self, "scaleDownControlInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleInControlInput")
    def scale_in_control_input(
        self,
    ) -> typing.Optional["GoogleComputeAutoscalerAutoscalingPolicyScaleInControl"]:
        return typing.cast(typing.Optional["GoogleComputeAutoscalerAutoscalingPolicyScaleInControl"], jsii.get(self, "scaleInControlInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingSchedulesInput")
    def scaling_schedules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeAutoscalerAutoscalingPolicyScalingSchedules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeAutoscalerAutoscalingPolicyScalingSchedules"]]], jsii.get(self, "scalingSchedulesInput"))

    @builtins.property
    @jsii.member(jsii_name="cooldownPeriod")
    def cooldown_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cooldownPeriod"))

    @cooldown_period.setter
    def cooldown_period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__454155838a535945ae57e13de6b8fd613283de97ea18d2acbe4cd35f2a120eed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cooldownPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxReplicas")
    def max_replicas(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxReplicas"))

    @max_replicas.setter
    def max_replicas(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9a6dfe8d30db0371b479d197e5bccf2fee7d0ef14e88e709905a2b0fc9ccf3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxReplicas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minReplicas")
    def min_replicas(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minReplicas"))

    @min_replicas.setter
    def min_replicas(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c82b15c7a268075c331091521f10f6a1d7ac8128df3fa8f5c852b2c4ddda5d84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minReplicas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51a3de3af710840bdb68843b3019214447fb2dede53403bf5db77e5a4399aa76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeAutoscalerAutoscalingPolicy]:
        return typing.cast(typing.Optional[GoogleComputeAutoscalerAutoscalingPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeAutoscalerAutoscalingPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2166e52db1119ffaea83adb9f09d94dd3bcbcfe7f2a224bc347376bcf15f934)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeAutoscaler.GoogleComputeAutoscalerAutoscalingPolicyScaleDownControl",
    jsii_struct_bases=[],
    name_mapping={
        "max_scaled_down_replicas": "maxScaledDownReplicas",
        "time_window_sec": "timeWindowSec",
    },
)
class GoogleComputeAutoscalerAutoscalingPolicyScaleDownControl:
    def __init__(
        self,
        *,
        max_scaled_down_replicas: typing.Optional[typing.Union["GoogleComputeAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicas", typing.Dict[builtins.str, typing.Any]]] = None,
        time_window_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_scaled_down_replicas: max_scaled_down_replicas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#max_scaled_down_replicas GoogleComputeAutoscaler#max_scaled_down_replicas}
        :param time_window_sec: How long back autoscaling should look when computing recommendations to include directives regarding slower scale down, as described above. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#time_window_sec GoogleComputeAutoscaler#time_window_sec}
        '''
        if isinstance(max_scaled_down_replicas, dict):
            max_scaled_down_replicas = GoogleComputeAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicas(**max_scaled_down_replicas)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a87bd626d1b45aa55a44539339ef3c0b8adb8b93d7c931ed5053f6aa0b21de73)
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
    ) -> typing.Optional["GoogleComputeAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicas"]:
        '''max_scaled_down_replicas block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#max_scaled_down_replicas GoogleComputeAutoscaler#max_scaled_down_replicas}
        '''
        result = self._values.get("max_scaled_down_replicas")
        return typing.cast(typing.Optional["GoogleComputeAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicas"], result)

    @builtins.property
    def time_window_sec(self) -> typing.Optional[jsii.Number]:
        '''How long back autoscaling should look when computing recommendations to include directives regarding slower scale down, as described above.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#time_window_sec GoogleComputeAutoscaler#time_window_sec}
        '''
        result = self._values.get("time_window_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeAutoscalerAutoscalingPolicyScaleDownControl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeAutoscaler.GoogleComputeAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicas",
    jsii_struct_bases=[],
    name_mapping={"fixed": "fixed", "percent": "percent"},
)
class GoogleComputeAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicas:
    def __init__(
        self,
        *,
        fixed: typing.Optional[jsii.Number] = None,
        percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fixed: Specifies a fixed number of VM instances. This must be a positive integer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#fixed GoogleComputeAutoscaler#fixed}
        :param percent: Specifies a percentage of instances between 0 to 100%, inclusive. For example, specify 80 for 80%. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#percent GoogleComputeAutoscaler#percent}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d792c1fce78f734b0d2b9cffb1395e93246544541d3600659e58f872df78a78)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#fixed GoogleComputeAutoscaler#fixed}
        '''
        result = self._values.get("fixed")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def percent(self) -> typing.Optional[jsii.Number]:
        '''Specifies a percentage of instances between 0 to 100%, inclusive. For example, specify 80 for 80%.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#percent GoogleComputeAutoscaler#percent}
        '''
        result = self._values.get("percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicas(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicasOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeAutoscaler.GoogleComputeAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicasOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3c3432f8774c66b5ca73836d39a45626f798bcd979d5c8141dccee63274fc6d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f91212b2559f127749340e2049438f4f1225cb3e63d920d739430fc3b1c2446b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="percent")
    def percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percent"))

    @percent.setter
    def percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8d1b393405a01d37b5b321f97a2c8cda5306f067b360e7b2593c01e8fbc1e59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicas]:
        return typing.cast(typing.Optional[GoogleComputeAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicas], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicas],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70a3d08f04ab4c3631ddc48e10054c05f84524e0949dd6895381f6f657206c3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeAutoscalerAutoscalingPolicyScaleDownControlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeAutoscaler.GoogleComputeAutoscalerAutoscalingPolicyScaleDownControlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ddb2fee3dc8200556ceacf3ef1f0628a11acc144124981c8e8faea42e725945)
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
        :param fixed: Specifies a fixed number of VM instances. This must be a positive integer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#fixed GoogleComputeAutoscaler#fixed}
        :param percent: Specifies a percentage of instances between 0 to 100%, inclusive. For example, specify 80 for 80%. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#percent GoogleComputeAutoscaler#percent}
        '''
        value = GoogleComputeAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicas(
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
    ) -> GoogleComputeAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicasOutputReference:
        return typing.cast(GoogleComputeAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicasOutputReference, jsii.get(self, "maxScaledDownReplicas"))

    @builtins.property
    @jsii.member(jsii_name="maxScaledDownReplicasInput")
    def max_scaled_down_replicas_input(
        self,
    ) -> typing.Optional[GoogleComputeAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicas]:
        return typing.cast(typing.Optional[GoogleComputeAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicas], jsii.get(self, "maxScaledDownReplicasInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__3ef23a73a6d57be778696f00ba0c2836ff066105fc219e1e98da77ff2dbd6760)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeWindowSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeAutoscalerAutoscalingPolicyScaleDownControl]:
        return typing.cast(typing.Optional[GoogleComputeAutoscalerAutoscalingPolicyScaleDownControl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeAutoscalerAutoscalingPolicyScaleDownControl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb40e227a675da4a3accc8a30965b5a2689ed1eaa3c55625e2c087611746e018)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeAutoscaler.GoogleComputeAutoscalerAutoscalingPolicyScaleInControl",
    jsii_struct_bases=[],
    name_mapping={
        "max_scaled_in_replicas": "maxScaledInReplicas",
        "time_window_sec": "timeWindowSec",
    },
)
class GoogleComputeAutoscalerAutoscalingPolicyScaleInControl:
    def __init__(
        self,
        *,
        max_scaled_in_replicas: typing.Optional[typing.Union["GoogleComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas", typing.Dict[builtins.str, typing.Any]]] = None,
        time_window_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_scaled_in_replicas: max_scaled_in_replicas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#max_scaled_in_replicas GoogleComputeAutoscaler#max_scaled_in_replicas}
        :param time_window_sec: How long back autoscaling should look when computing recommendations to include directives regarding slower scale down, as described above. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#time_window_sec GoogleComputeAutoscaler#time_window_sec}
        '''
        if isinstance(max_scaled_in_replicas, dict):
            max_scaled_in_replicas = GoogleComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas(**max_scaled_in_replicas)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__856210422d42e0298f48054ae19fc199bb263b8343a90bc88077371180632cb5)
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
    ) -> typing.Optional["GoogleComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas"]:
        '''max_scaled_in_replicas block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#max_scaled_in_replicas GoogleComputeAutoscaler#max_scaled_in_replicas}
        '''
        result = self._values.get("max_scaled_in_replicas")
        return typing.cast(typing.Optional["GoogleComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas"], result)

    @builtins.property
    def time_window_sec(self) -> typing.Optional[jsii.Number]:
        '''How long back autoscaling should look when computing recommendations to include directives regarding slower scale down, as described above.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#time_window_sec GoogleComputeAutoscaler#time_window_sec}
        '''
        result = self._values.get("time_window_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeAutoscalerAutoscalingPolicyScaleInControl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeAutoscaler.GoogleComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas",
    jsii_struct_bases=[],
    name_mapping={"fixed": "fixed", "percent": "percent"},
)
class GoogleComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas:
    def __init__(
        self,
        *,
        fixed: typing.Optional[jsii.Number] = None,
        percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fixed: Specifies a fixed number of VM instances. This must be a positive integer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#fixed GoogleComputeAutoscaler#fixed}
        :param percent: Specifies a percentage of instances between 0 to 100%, inclusive. For example, specify 80 for 80%. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#percent GoogleComputeAutoscaler#percent}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f23b08231924397cf89e89722acba64f0a1cdcb66e421a9c2e15ba7e6a89a49e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#fixed GoogleComputeAutoscaler#fixed}
        '''
        result = self._values.get("fixed")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def percent(self) -> typing.Optional[jsii.Number]:
        '''Specifies a percentage of instances between 0 to 100%, inclusive. For example, specify 80 for 80%.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#percent GoogleComputeAutoscaler#percent}
        '''
        result = self._values.get("percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicasOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeAutoscaler.GoogleComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicasOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3018f2c2e0f834a01d712b8f16739a4c78ff1ea6fc875a1ceed5bea08182794)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6930ee13a6431573470c0389813a49b48cc5318ddd10ce69a8de56fb862d81e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="percent")
    def percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percent"))

    @percent.setter
    def percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2d5b1284e1fc16650b6670fc06e440b46547c41663d100c26fc0ecbf1d370c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas]:
        return typing.cast(typing.Optional[GoogleComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d282e93a709cdb0144184e087dfd7232a36a570639f2a7ad08a68fe20d502d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeAutoscalerAutoscalingPolicyScaleInControlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeAutoscaler.GoogleComputeAutoscalerAutoscalingPolicyScaleInControlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__16a999dddd4dfd8dc10c2fd02a79cc83c47e35ae29206aa322c683708d754e55)
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
        :param fixed: Specifies a fixed number of VM instances. This must be a positive integer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#fixed GoogleComputeAutoscaler#fixed}
        :param percent: Specifies a percentage of instances between 0 to 100%, inclusive. For example, specify 80 for 80%. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#percent GoogleComputeAutoscaler#percent}
        '''
        value = GoogleComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas(
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
    ) -> GoogleComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicasOutputReference:
        return typing.cast(GoogleComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicasOutputReference, jsii.get(self, "maxScaledInReplicas"))

    @builtins.property
    @jsii.member(jsii_name="maxScaledInReplicasInput")
    def max_scaled_in_replicas_input(
        self,
    ) -> typing.Optional[GoogleComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas]:
        return typing.cast(typing.Optional[GoogleComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas], jsii.get(self, "maxScaledInReplicasInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__5968713439dfe35c519de75bdc4c6844f2c97819724f00d478c5fb45fc872983)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeWindowSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeAutoscalerAutoscalingPolicyScaleInControl]:
        return typing.cast(typing.Optional[GoogleComputeAutoscalerAutoscalingPolicyScaleInControl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeAutoscalerAutoscalingPolicyScaleInControl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67ee285225b169eabbe9428050b166c7862dc2c29e3e0e840fcb7fb95769656e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeAutoscaler.GoogleComputeAutoscalerAutoscalingPolicyScalingSchedules",
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
class GoogleComputeAutoscalerAutoscalingPolicyScalingSchedules:
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
        :param duration_sec: The duration of time intervals (in seconds) for which this scaling schedule will be running. The minimum allowed value is 300. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#duration_sec GoogleComputeAutoscaler#duration_sec}
        :param min_required_replicas: Minimum number of VM instances that autoscaler will recommend in time intervals starting according to schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#min_required_replicas GoogleComputeAutoscaler#min_required_replicas}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#name GoogleComputeAutoscaler#name}.
        :param schedule: The start timestamps of time intervals when this scaling schedule should provide a scaling signal. This field uses the extended cron format (with an optional year field). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#schedule GoogleComputeAutoscaler#schedule}
        :param description: A description of a scaling schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#description GoogleComputeAutoscaler#description}
        :param disabled: A boolean value that specifies if a scaling schedule can influence autoscaler recommendations. If set to true, then a scaling schedule has no effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#disabled GoogleComputeAutoscaler#disabled}
        :param time_zone: The time zone to be used when interpreting the schedule. The value of this field must be a time zone name from the tz database: http://en.wikipedia.org/wiki/Tz_database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#time_zone GoogleComputeAutoscaler#time_zone}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__312fbf791abdf4edf897c804a6a5581bdb471020396b632032b6e9f16c161048)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#duration_sec GoogleComputeAutoscaler#duration_sec}
        '''
        result = self._values.get("duration_sec")
        assert result is not None, "Required property 'duration_sec' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def min_required_replicas(self) -> jsii.Number:
        '''Minimum number of VM instances that autoscaler will recommend in time intervals starting according to schedule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#min_required_replicas GoogleComputeAutoscaler#min_required_replicas}
        '''
        result = self._values.get("min_required_replicas")
        assert result is not None, "Required property 'min_required_replicas' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#name GoogleComputeAutoscaler#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schedule(self) -> builtins.str:
        '''The start timestamps of time intervals when this scaling schedule should provide a scaling signal.

        This field uses the extended cron format (with an optional year field).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#schedule GoogleComputeAutoscaler#schedule}
        '''
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of a scaling schedule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#description GoogleComputeAutoscaler#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A boolean value that specifies if a scaling schedule can influence autoscaler recommendations.

        If set to true, then a scaling schedule has no effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#disabled GoogleComputeAutoscaler#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[builtins.str]:
        '''The time zone to be used when interpreting the schedule.

        The value of this field must be a time zone name from the tz database: http://en.wikipedia.org/wiki/Tz_database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#time_zone GoogleComputeAutoscaler#time_zone}
        '''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeAutoscalerAutoscalingPolicyScalingSchedules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeAutoscalerAutoscalingPolicyScalingSchedulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeAutoscaler.GoogleComputeAutoscalerAutoscalingPolicyScalingSchedulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__217aac2e4c601d084221484495ebae7f931aaf2a0efc51bb211bb1820f30e325)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeAutoscalerAutoscalingPolicyScalingSchedulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__675c53c0b80b574a6b81cfa3983e56b5fd88a33f54105ed18b19d12656a3e95e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeAutoscalerAutoscalingPolicyScalingSchedulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4554705bb95a2fe02d3aceb2a1e60a1680c6b8fc0b387c1661bd0fc3e3365ece)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b8fc9f2b39d4b024c2ef1460edc43904fffda3b03ea863723bdf446a6b74509)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a7f7a07ede59090fb013d8c11dbbc0f9bc53d0cb8aad9d0cdfeec128b791991)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeAutoscalerAutoscalingPolicyScalingSchedules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeAutoscalerAutoscalingPolicyScalingSchedules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeAutoscalerAutoscalingPolicyScalingSchedules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fd66ad6cc2514a23c7cc8586f2f9475e144ca5098f9340205e9226fd66c1ab9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeAutoscalerAutoscalingPolicyScalingSchedulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeAutoscaler.GoogleComputeAutoscalerAutoscalingPolicyScalingSchedulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0439ef034f608ef3fcf86f9055126ca127fda3eaa2d88687d6c271c6a1b73e11)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bad20085ce408a7d4260de1f2aa1ebccf262ffaff48fdb0938d11d09634e5cfc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a169f2d7ae6f4ce9d875252e52dfae83d1024204695046852a6d859bd6f66ab7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="durationSec")
    def duration_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "durationSec"))

    @duration_sec.setter
    def duration_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b60ed0d3441f86f3b2ec8b45c8870f0df8a09915d1009440a9f1df3cade7f925)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "durationSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minRequiredReplicas")
    def min_required_replicas(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minRequiredReplicas"))

    @min_required_replicas.setter
    def min_required_replicas(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28ea68145952931af46c99a05005bdb2d5735c5229ddc41ec88fadff87b9a0be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minRequiredReplicas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92f4754cb1cb6b2a26116bb71f17dd94bd5adf16ae80a766be535b3df2ee86f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedule"))

    @schedule.setter
    def schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c97985354d58cf9ab104a9a01ec4e8338b01eb032a012688a11bd892e6251ffa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb3faea2d660dbe3f3a1665be420e702046daf442fc820421f306caa3da8f3d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeAutoscalerAutoscalingPolicyScalingSchedules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeAutoscalerAutoscalingPolicyScalingSchedules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeAutoscalerAutoscalingPolicyScalingSchedules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6154f73d8835e04b4a644fc2044061742a9d247762dcbb35f4f9db6340375587)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeAutoscaler.GoogleComputeAutoscalerConfig",
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
class GoogleComputeAutoscalerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        autoscaling_policy: typing.Union[GoogleComputeAutoscalerAutoscalingPolicy, typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        target: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeAutoscalerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param autoscaling_policy: autoscaling_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#autoscaling_policy GoogleComputeAutoscaler#autoscaling_policy}
        :param name: Name of the resource. The name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#name GoogleComputeAutoscaler#name}
        :param target: URL of the managed instance group that this autoscaler will scale. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#target GoogleComputeAutoscaler#target}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#description GoogleComputeAutoscaler#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#id GoogleComputeAutoscaler#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#project GoogleComputeAutoscaler#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#timeouts GoogleComputeAutoscaler#timeouts}
        :param zone: URL of the zone where the instance group resides. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#zone GoogleComputeAutoscaler#zone}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(autoscaling_policy, dict):
            autoscaling_policy = GoogleComputeAutoscalerAutoscalingPolicy(**autoscaling_policy)
        if isinstance(timeouts, dict):
            timeouts = GoogleComputeAutoscalerTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__685dd9d5d2bfce9a7db62e536b71c4907e06c2a5744021a511ad08f80902d166)
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
    def autoscaling_policy(self) -> GoogleComputeAutoscalerAutoscalingPolicy:
        '''autoscaling_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#autoscaling_policy GoogleComputeAutoscaler#autoscaling_policy}
        '''
        result = self._values.get("autoscaling_policy")
        assert result is not None, "Required property 'autoscaling_policy' is missing"
        return typing.cast(GoogleComputeAutoscalerAutoscalingPolicy, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the resource.

        The name must be 1-63 characters long and match
        the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the
        first character must be a lowercase letter, and all following
        characters must be a dash, lowercase letter, or digit, except the last
        character, which cannot be a dash.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#name GoogleComputeAutoscaler#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> builtins.str:
        '''URL of the managed instance group that this autoscaler will scale.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#target GoogleComputeAutoscaler#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#description GoogleComputeAutoscaler#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#id GoogleComputeAutoscaler#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#project GoogleComputeAutoscaler#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleComputeAutoscalerTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#timeouts GoogleComputeAutoscaler#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleComputeAutoscalerTimeouts"], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''URL of the zone where the instance group resides.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#zone GoogleComputeAutoscaler#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeAutoscalerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeAutoscaler.GoogleComputeAutoscalerTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleComputeAutoscalerTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#create GoogleComputeAutoscaler#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#delete GoogleComputeAutoscaler#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#update GoogleComputeAutoscaler#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd75a15ce9bb3723ffd94af95754b74e0a043938dce7ccca3d5ca31124d1fcdd)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#create GoogleComputeAutoscaler#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#delete GoogleComputeAutoscaler#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_autoscaler#update GoogleComputeAutoscaler#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeAutoscalerTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeAutoscalerTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeAutoscaler.GoogleComputeAutoscalerTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f00a10e2ede0249479ec1d5aa8be71d437ae6478a11f54e77066dfbf37274e41)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f4c4dc92cc606bafd3b961149a8e53bce361e841f22c9e5819827d7e26708a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a46df158867f3d42819168139e5ae86ac92cb12c7286a0b71348aea028b02c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68f39c45b2a7b50d1ff673f8694e5c2d8ddb023ea2f7fa9021825a95c1543027)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeAutoscalerTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeAutoscalerTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeAutoscalerTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd2c1b7b97bc25073a9538d43ef1ee82b87e9e98777bdaba25f2bade0b881bb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleComputeAutoscaler",
    "GoogleComputeAutoscalerAutoscalingPolicy",
    "GoogleComputeAutoscalerAutoscalingPolicyCpuUtilization",
    "GoogleComputeAutoscalerAutoscalingPolicyCpuUtilizationOutputReference",
    "GoogleComputeAutoscalerAutoscalingPolicyLoadBalancingUtilization",
    "GoogleComputeAutoscalerAutoscalingPolicyLoadBalancingUtilizationOutputReference",
    "GoogleComputeAutoscalerAutoscalingPolicyMetric",
    "GoogleComputeAutoscalerAutoscalingPolicyMetricList",
    "GoogleComputeAutoscalerAutoscalingPolicyMetricOutputReference",
    "GoogleComputeAutoscalerAutoscalingPolicyOutputReference",
    "GoogleComputeAutoscalerAutoscalingPolicyScaleDownControl",
    "GoogleComputeAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicas",
    "GoogleComputeAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicasOutputReference",
    "GoogleComputeAutoscalerAutoscalingPolicyScaleDownControlOutputReference",
    "GoogleComputeAutoscalerAutoscalingPolicyScaleInControl",
    "GoogleComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas",
    "GoogleComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicasOutputReference",
    "GoogleComputeAutoscalerAutoscalingPolicyScaleInControlOutputReference",
    "GoogleComputeAutoscalerAutoscalingPolicyScalingSchedules",
    "GoogleComputeAutoscalerAutoscalingPolicyScalingSchedulesList",
    "GoogleComputeAutoscalerAutoscalingPolicyScalingSchedulesOutputReference",
    "GoogleComputeAutoscalerConfig",
    "GoogleComputeAutoscalerTimeouts",
    "GoogleComputeAutoscalerTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__35cfbded27894277e07f097818258aa0e14afb0a66ff7496f4a68e6934ba69d8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    autoscaling_policy: typing.Union[GoogleComputeAutoscalerAutoscalingPolicy, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    target: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeAutoscalerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__78a8409fdd65732c56db0ac7a5af0d0cbfce6565b01096cf979c042c9eb3f25e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5103d4e65778950bf463d20f40cadad7e3f40c98e7ceaa28184290e04de43b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d489135bb540b32a0906068e2bffa6e32cb004ea3292702d3afe6b10dc62d3fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4140dbadbb8d3f116a41d2d692d6b9f20e572b04e353dd129355a9094760637(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aec26b02355648d1c9f89dbc847c01bcec611c5614d3e621625a1efa6398cc9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9890252bad29b39fb1b60df36312356c1a2685669b9e44d8e3098ab46786fa3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8fc9556f106774a89192987fe594bfe1203a3d70c4b1f65faabb999267a690d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55d24525b45015d95cb55e37957a924ee50a56bf8ea33511b51c578b11f8ce79(
    *,
    max_replicas: jsii.Number,
    min_replicas: jsii.Number,
    cooldown_period: typing.Optional[jsii.Number] = None,
    cpu_utilization: typing.Optional[typing.Union[GoogleComputeAutoscalerAutoscalingPolicyCpuUtilization, typing.Dict[builtins.str, typing.Any]]] = None,
    load_balancing_utilization: typing.Optional[typing.Union[GoogleComputeAutoscalerAutoscalingPolicyLoadBalancingUtilization, typing.Dict[builtins.str, typing.Any]]] = None,
    metric: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeAutoscalerAutoscalingPolicyMetric, typing.Dict[builtins.str, typing.Any]]]]] = None,
    mode: typing.Optional[builtins.str] = None,
    scale_down_control: typing.Optional[typing.Union[GoogleComputeAutoscalerAutoscalingPolicyScaleDownControl, typing.Dict[builtins.str, typing.Any]]] = None,
    scale_in_control: typing.Optional[typing.Union[GoogleComputeAutoscalerAutoscalingPolicyScaleInControl, typing.Dict[builtins.str, typing.Any]]] = None,
    scaling_schedules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeAutoscalerAutoscalingPolicyScalingSchedules, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c60eba81dcaf226575edc1561d1da97e5eed2d8124422e4df9d6ec2f2e42a4c(
    *,
    target: jsii.Number,
    predictive_method: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cae74129c409a0e1aecc2ac49d4809f7eac42876465443d52ab64d455cd61923(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96268fcaacb41b5eddc892ffa7edfd1d17529ca9fa0c7bcacbe63a72d0c12ed0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c22e215740840dfca5b9929ed920558ad91883d732badeb02855ffc88859d09(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f028144fc365ac513b39bffb7b934268c09920c252b599d5a1b03b9a057e573a(
    value: typing.Optional[GoogleComputeAutoscalerAutoscalingPolicyCpuUtilization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e21469fc21ddc38cb1d2efe7615091c9f825b853385aef01bdd6663983c434ff(
    *,
    target: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__653535b6b3dcd84e3faebec1eb361f8a031cb7b91359720b0cd42436fdb00ab3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea97fbd446c58c29108e569eba01c4bf25ba24b10ac0e1dce6a2e66b3eba1f73(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23022660bf3fc0b5f84188e86a0817578a2d4e59bd88ae048aacb32023996295(
    value: typing.Optional[GoogleComputeAutoscalerAutoscalingPolicyLoadBalancingUtilization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aedf0959c220caf65320498af60bc14b1898dcacefd87e1f983cb73094f71b1(
    *,
    name: builtins.str,
    filter: typing.Optional[builtins.str] = None,
    single_instance_assignment: typing.Optional[jsii.Number] = None,
    target: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bacdde8d0c88f53ed1a0e2a5011b2385e7997cc5941c0a0f70e28b56d480edb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1ed1e651a3eb7e88e6a061f6391f008a13a13d3d090e7e4e50b593e9448de42(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27513c31ecbc0d4ce04a08d14797056fffa3e4cdfddbb6211fc445597e54fafb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be58e08f709659eb1c4e957eb4a0ddaa634da7c5bb30ed1bdec4bc365cbe28ed(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4acacd5b404af0aca0575d55726de17e494e51dbd1fdde298cbf2120e94bbf6f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__288fef0e1bd19c5f10faef2d9dd17d08ee805645cba286c9fba9e41f715c976f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeAutoscalerAutoscalingPolicyMetric]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7a81e99b5c9956c6473c1bca112d1651046dbe3412d2c3545fa4a81cce634cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__891c4a390d922706eeb7fc3a9af2869c09f45a07174721620a3a6f356fb78729(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c27bf916234d5fa18d4b50da96ed194af12cb6d0074930193e5b8dca9e7ad3a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc28001472c752e4cd2176c9fde6139f09b78b7d9ba1febbe8d4e1aee291ed7d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a9348bf636dc14188387e6b9e0ef65e37671aa24c7ab81595cd73c8cbe00bcc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6e276dd98faec36c028bbc292f002cd33ba1d80164223ee45a467de162f9da0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b51eafbb59a2df2026614987f3b5f8f39576b8c020c011b0322c832f354bf05d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeAutoscalerAutoscalingPolicyMetric]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aebc62227187737793587d5e0c05af0f48001f52ea312179e059f4ab66c05ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__039a41627ed4c24f94ac9fdae7fb7cad70bdd7a1f741aa0ab6b8e463fd689e67(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeAutoscalerAutoscalingPolicyMetric, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__741b6de70d4b27bdd8245711113deac40c06a70d457367f2c43c87421ddc755a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeAutoscalerAutoscalingPolicyScalingSchedules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__454155838a535945ae57e13de6b8fd613283de97ea18d2acbe4cd35f2a120eed(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9a6dfe8d30db0371b479d197e5bccf2fee7d0ef14e88e709905a2b0fc9ccf3b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c82b15c7a268075c331091521f10f6a1d7ac8128df3fa8f5c852b2c4ddda5d84(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51a3de3af710840bdb68843b3019214447fb2dede53403bf5db77e5a4399aa76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2166e52db1119ffaea83adb9f09d94dd3bcbcfe7f2a224bc347376bcf15f934(
    value: typing.Optional[GoogleComputeAutoscalerAutoscalingPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a87bd626d1b45aa55a44539339ef3c0b8adb8b93d7c931ed5053f6aa0b21de73(
    *,
    max_scaled_down_replicas: typing.Optional[typing.Union[GoogleComputeAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicas, typing.Dict[builtins.str, typing.Any]]] = None,
    time_window_sec: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d792c1fce78f734b0d2b9cffb1395e93246544541d3600659e58f872df78a78(
    *,
    fixed: typing.Optional[jsii.Number] = None,
    percent: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3c3432f8774c66b5ca73836d39a45626f798bcd979d5c8141dccee63274fc6d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f91212b2559f127749340e2049438f4f1225cb3e63d920d739430fc3b1c2446b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8d1b393405a01d37b5b321f97a2c8cda5306f067b360e7b2593c01e8fbc1e59(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70a3d08f04ab4c3631ddc48e10054c05f84524e0949dd6895381f6f657206c3e(
    value: typing.Optional[GoogleComputeAutoscalerAutoscalingPolicyScaleDownControlMaxScaledDownReplicas],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ddb2fee3dc8200556ceacf3ef1f0628a11acc144124981c8e8faea42e725945(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ef23a73a6d57be778696f00ba0c2836ff066105fc219e1e98da77ff2dbd6760(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb40e227a675da4a3accc8a30965b5a2689ed1eaa3c55625e2c087611746e018(
    value: typing.Optional[GoogleComputeAutoscalerAutoscalingPolicyScaleDownControl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__856210422d42e0298f48054ae19fc199bb263b8343a90bc88077371180632cb5(
    *,
    max_scaled_in_replicas: typing.Optional[typing.Union[GoogleComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas, typing.Dict[builtins.str, typing.Any]]] = None,
    time_window_sec: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f23b08231924397cf89e89722acba64f0a1cdcb66e421a9c2e15ba7e6a89a49e(
    *,
    fixed: typing.Optional[jsii.Number] = None,
    percent: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3018f2c2e0f834a01d712b8f16739a4c78ff1ea6fc875a1ceed5bea08182794(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6930ee13a6431573470c0389813a49b48cc5318ddd10ce69a8de56fb862d81e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2d5b1284e1fc16650b6670fc06e440b46547c41663d100c26fc0ecbf1d370c6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d282e93a709cdb0144184e087dfd7232a36a570639f2a7ad08a68fe20d502d8(
    value: typing.Optional[GoogleComputeAutoscalerAutoscalingPolicyScaleInControlMaxScaledInReplicas],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16a999dddd4dfd8dc10c2fd02a79cc83c47e35ae29206aa322c683708d754e55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5968713439dfe35c519de75bdc4c6844f2c97819724f00d478c5fb45fc872983(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67ee285225b169eabbe9428050b166c7862dc2c29e3e0e840fcb7fb95769656e(
    value: typing.Optional[GoogleComputeAutoscalerAutoscalingPolicyScaleInControl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__312fbf791abdf4edf897c804a6a5581bdb471020396b632032b6e9f16c161048(
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

def _typecheckingstub__217aac2e4c601d084221484495ebae7f931aaf2a0efc51bb211bb1820f30e325(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__675c53c0b80b574a6b81cfa3983e56b5fd88a33f54105ed18b19d12656a3e95e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4554705bb95a2fe02d3aceb2a1e60a1680c6b8fc0b387c1661bd0fc3e3365ece(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b8fc9f2b39d4b024c2ef1460edc43904fffda3b03ea863723bdf446a6b74509(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a7f7a07ede59090fb013d8c11dbbc0f9bc53d0cb8aad9d0cdfeec128b791991(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fd66ad6cc2514a23c7cc8586f2f9475e144ca5098f9340205e9226fd66c1ab9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeAutoscalerAutoscalingPolicyScalingSchedules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0439ef034f608ef3fcf86f9055126ca127fda3eaa2d88687d6c271c6a1b73e11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bad20085ce408a7d4260de1f2aa1ebccf262ffaff48fdb0938d11d09634e5cfc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a169f2d7ae6f4ce9d875252e52dfae83d1024204695046852a6d859bd6f66ab7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b60ed0d3441f86f3b2ec8b45c8870f0df8a09915d1009440a9f1df3cade7f925(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28ea68145952931af46c99a05005bdb2d5735c5229ddc41ec88fadff87b9a0be(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92f4754cb1cb6b2a26116bb71f17dd94bd5adf16ae80a766be535b3df2ee86f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c97985354d58cf9ab104a9a01ec4e8338b01eb032a012688a11bd892e6251ffa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb3faea2d660dbe3f3a1665be420e702046daf442fc820421f306caa3da8f3d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6154f73d8835e04b4a644fc2044061742a9d247762dcbb35f4f9db6340375587(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeAutoscalerAutoscalingPolicyScalingSchedules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__685dd9d5d2bfce9a7db62e536b71c4907e06c2a5744021a511ad08f80902d166(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    autoscaling_policy: typing.Union[GoogleComputeAutoscalerAutoscalingPolicy, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    target: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeAutoscalerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd75a15ce9bb3723ffd94af95754b74e0a043938dce7ccca3d5ca31124d1fcdd(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f00a10e2ede0249479ec1d5aa8be71d437ae6478a11f54e77066dfbf37274e41(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f4c4dc92cc606bafd3b961149a8e53bce361e841f22c9e5819827d7e26708a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a46df158867f3d42819168139e5ae86ac92cb12c7286a0b71348aea028b02c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68f39c45b2a7b50d1ff673f8694e5c2d8ddb023ea2f7fa9021825a95c1543027(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd2c1b7b97bc25073a9538d43ef1ee82b87e9e98777bdaba25f2bade0b881bb9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeAutoscalerTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
