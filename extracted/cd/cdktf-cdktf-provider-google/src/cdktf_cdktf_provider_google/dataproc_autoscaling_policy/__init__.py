r'''
# `google_dataproc_autoscaling_policy`

Refer to the Terraform Registry for docs: [`google_dataproc_autoscaling_policy`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy).
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


class DataprocAutoscalingPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocAutoscalingPolicy.DataprocAutoscalingPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy google_dataproc_autoscaling_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        policy_id: builtins.str,
        basic_algorithm: typing.Optional[typing.Union["DataprocAutoscalingPolicyBasicAlgorithm", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        secondary_worker_config: typing.Optional[typing.Union["DataprocAutoscalingPolicySecondaryWorkerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["DataprocAutoscalingPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        worker_config: typing.Optional[typing.Union["DataprocAutoscalingPolicyWorkerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy google_dataproc_autoscaling_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param policy_id: The policy id. The id must contain only letters (a-z, A-Z), numbers (0-9), underscores (_), and hyphens (-). Cannot begin or end with underscore or hyphen. Must consist of between 3 and 50 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#policy_id DataprocAutoscalingPolicy#policy_id}
        :param basic_algorithm: basic_algorithm block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#basic_algorithm DataprocAutoscalingPolicy#basic_algorithm}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#id DataprocAutoscalingPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param location: The location where the autoscaling policy should reside. The default value is 'global'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#location DataprocAutoscalingPolicy#location}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#project DataprocAutoscalingPolicy#project}.
        :param secondary_worker_config: secondary_worker_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#secondary_worker_config DataprocAutoscalingPolicy#secondary_worker_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#timeouts DataprocAutoscalingPolicy#timeouts}
        :param worker_config: worker_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#worker_config DataprocAutoscalingPolicy#worker_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__717fa8e0d07b277bd5cdb2d8946aff06d41f02d9adda1f746a14fb12c30bc3b7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataprocAutoscalingPolicyConfig(
            policy_id=policy_id,
            basic_algorithm=basic_algorithm,
            id=id,
            location=location,
            project=project,
            secondary_worker_config=secondary_worker_config,
            timeouts=timeouts,
            worker_config=worker_config,
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
        '''Generates CDKTF code for importing a DataprocAutoscalingPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataprocAutoscalingPolicy to import.
        :param import_from_id: The id of the existing DataprocAutoscalingPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataprocAutoscalingPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__700082d80b45d1c0a47d01001b282a0997069422433002f0e5f54ab851787a78)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBasicAlgorithm")
    def put_basic_algorithm(
        self,
        *,
        yarn_config: typing.Union["DataprocAutoscalingPolicyBasicAlgorithmYarnConfig", typing.Dict[builtins.str, typing.Any]],
        cooldown_period: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param yarn_config: yarn_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#yarn_config DataprocAutoscalingPolicy#yarn_config}
        :param cooldown_period: Duration between scaling events. A scaling period starts after the update operation from the previous event has completed. Bounds: [2m, 1d]. Default: 2m. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#cooldown_period DataprocAutoscalingPolicy#cooldown_period}
        '''
        value = DataprocAutoscalingPolicyBasicAlgorithm(
            yarn_config=yarn_config, cooldown_period=cooldown_period
        )

        return typing.cast(None, jsii.invoke(self, "putBasicAlgorithm", [value]))

    @jsii.member(jsii_name="putSecondaryWorkerConfig")
    def put_secondary_worker_config(
        self,
        *,
        max_instances: typing.Optional[jsii.Number] = None,
        min_instances: typing.Optional[jsii.Number] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_instances: Maximum number of instances for this group. Note that by default, clusters will not use secondary workers. Required for secondary workers if the minimum secondary instances is set. Bounds: [minInstances, ). Defaults to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#max_instances DataprocAutoscalingPolicy#max_instances}
        :param min_instances: Minimum number of instances for this group. Bounds: [0, maxInstances]. Defaults to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#min_instances DataprocAutoscalingPolicy#min_instances}
        :param weight: Weight for the instance group, which is used to determine the fraction of total workers in the cluster from this instance group. For example, if primary workers have weight 2, and secondary workers have weight 1, the cluster will have approximately 2 primary workers for each secondary worker. The cluster may not reach the specified balance if constrained by min/max bounds or other autoscaling settings. For example, if maxInstances for secondary workers is 0, then only primary workers will be added. The cluster can also be out of balance when created. If weight is not set on any instance group, the cluster will default to equal weight for all groups: the cluster will attempt to maintain an equal number of workers in each group within the configured size bounds for each group. If weight is set for one group only, the cluster will default to zero weight on the unset group. For example if weight is set only on primary workers, the cluster will use primary workers only and no secondary workers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#weight DataprocAutoscalingPolicy#weight}
        '''
        value = DataprocAutoscalingPolicySecondaryWorkerConfig(
            max_instances=max_instances, min_instances=min_instances, weight=weight
        )

        return typing.cast(None, jsii.invoke(self, "putSecondaryWorkerConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#create DataprocAutoscalingPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#delete DataprocAutoscalingPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#update DataprocAutoscalingPolicy#update}.
        '''
        value = DataprocAutoscalingPolicyTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putWorkerConfig")
    def put_worker_config(
        self,
        *,
        max_instances: jsii.Number,
        min_instances: typing.Optional[jsii.Number] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_instances: Maximum number of instances for this group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#max_instances DataprocAutoscalingPolicy#max_instances}
        :param min_instances: Minimum number of instances for this group. Bounds: [2, maxInstances]. Defaults to 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#min_instances DataprocAutoscalingPolicy#min_instances}
        :param weight: Weight for the instance group, which is used to determine the fraction of total workers in the cluster from this instance group. For example, if primary workers have weight 2, and secondary workers have weight 1, the cluster will have approximately 2 primary workers for each secondary worker. The cluster may not reach the specified balance if constrained by min/max bounds or other autoscaling settings. For example, if maxInstances for secondary workers is 0, then only primary workers will be added. The cluster can also be out of balance when created. If weight is not set on any instance group, the cluster will default to equal weight for all groups: the cluster will attempt to maintain an equal number of workers in each group within the configured size bounds for each group. If weight is set for one group only, the cluster will default to zero weight on the unset group. For example if weight is set only on primary workers, the cluster will use primary workers only and no secondary workers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#weight DataprocAutoscalingPolicy#weight}
        '''
        value = DataprocAutoscalingPolicyWorkerConfig(
            max_instances=max_instances, min_instances=min_instances, weight=weight
        )

        return typing.cast(None, jsii.invoke(self, "putWorkerConfig", [value]))

    @jsii.member(jsii_name="resetBasicAlgorithm")
    def reset_basic_algorithm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBasicAlgorithm", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetSecondaryWorkerConfig")
    def reset_secondary_worker_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecondaryWorkerConfig", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetWorkerConfig")
    def reset_worker_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkerConfig", []))

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
    @jsii.member(jsii_name="basicAlgorithm")
    def basic_algorithm(
        self,
    ) -> "DataprocAutoscalingPolicyBasicAlgorithmOutputReference":
        return typing.cast("DataprocAutoscalingPolicyBasicAlgorithmOutputReference", jsii.get(self, "basicAlgorithm"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="secondaryWorkerConfig")
    def secondary_worker_config(
        self,
    ) -> "DataprocAutoscalingPolicySecondaryWorkerConfigOutputReference":
        return typing.cast("DataprocAutoscalingPolicySecondaryWorkerConfigOutputReference", jsii.get(self, "secondaryWorkerConfig"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DataprocAutoscalingPolicyTimeoutsOutputReference":
        return typing.cast("DataprocAutoscalingPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="workerConfig")
    def worker_config(self) -> "DataprocAutoscalingPolicyWorkerConfigOutputReference":
        return typing.cast("DataprocAutoscalingPolicyWorkerConfigOutputReference", jsii.get(self, "workerConfig"))

    @builtins.property
    @jsii.member(jsii_name="basicAlgorithmInput")
    def basic_algorithm_input(
        self,
    ) -> typing.Optional["DataprocAutoscalingPolicyBasicAlgorithm"]:
        return typing.cast(typing.Optional["DataprocAutoscalingPolicyBasicAlgorithm"], jsii.get(self, "basicAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="policyIdInput")
    def policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="secondaryWorkerConfigInput")
    def secondary_worker_config_input(
        self,
    ) -> typing.Optional["DataprocAutoscalingPolicySecondaryWorkerConfig"]:
        return typing.cast(typing.Optional["DataprocAutoscalingPolicySecondaryWorkerConfig"], jsii.get(self, "secondaryWorkerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataprocAutoscalingPolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataprocAutoscalingPolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="workerConfigInput")
    def worker_config_input(
        self,
    ) -> typing.Optional["DataprocAutoscalingPolicyWorkerConfig"]:
        return typing.cast(typing.Optional["DataprocAutoscalingPolicyWorkerConfig"], jsii.get(self, "workerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45602e0f0ff2e3fbcd534709ab2b9084e64901d3d1d48b87e4203284d132d59a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__131416a252572784a29504897b2efc6f75f95bb9d57efa3d8461b77dd9c53c12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyId")
    def policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyId"))

    @policy_id.setter
    def policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a15882f11d3d0ec18898a143b1cf2f46e317f9794dcbb8a3e2ec6784474ba1b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__518a796e9f8051d587ca837b9e246718841f230b3043cc08582605dbb1b7561a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocAutoscalingPolicy.DataprocAutoscalingPolicyBasicAlgorithm",
    jsii_struct_bases=[],
    name_mapping={"yarn_config": "yarnConfig", "cooldown_period": "cooldownPeriod"},
)
class DataprocAutoscalingPolicyBasicAlgorithm:
    def __init__(
        self,
        *,
        yarn_config: typing.Union["DataprocAutoscalingPolicyBasicAlgorithmYarnConfig", typing.Dict[builtins.str, typing.Any]],
        cooldown_period: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param yarn_config: yarn_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#yarn_config DataprocAutoscalingPolicy#yarn_config}
        :param cooldown_period: Duration between scaling events. A scaling period starts after the update operation from the previous event has completed. Bounds: [2m, 1d]. Default: 2m. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#cooldown_period DataprocAutoscalingPolicy#cooldown_period}
        '''
        if isinstance(yarn_config, dict):
            yarn_config = DataprocAutoscalingPolicyBasicAlgorithmYarnConfig(**yarn_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0392426022d332921971a8c20288eb32c7040946068fc4e480dbfa209175813e)
            check_type(argname="argument yarn_config", value=yarn_config, expected_type=type_hints["yarn_config"])
            check_type(argname="argument cooldown_period", value=cooldown_period, expected_type=type_hints["cooldown_period"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "yarn_config": yarn_config,
        }
        if cooldown_period is not None:
            self._values["cooldown_period"] = cooldown_period

    @builtins.property
    def yarn_config(self) -> "DataprocAutoscalingPolicyBasicAlgorithmYarnConfig":
        '''yarn_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#yarn_config DataprocAutoscalingPolicy#yarn_config}
        '''
        result = self._values.get("yarn_config")
        assert result is not None, "Required property 'yarn_config' is missing"
        return typing.cast("DataprocAutoscalingPolicyBasicAlgorithmYarnConfig", result)

    @builtins.property
    def cooldown_period(self) -> typing.Optional[builtins.str]:
        '''Duration between scaling events. A scaling period starts after the update operation from the previous event has completed.

        Bounds: [2m, 1d]. Default: 2m.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#cooldown_period DataprocAutoscalingPolicy#cooldown_period}
        '''
        result = self._values.get("cooldown_period")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocAutoscalingPolicyBasicAlgorithm(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocAutoscalingPolicyBasicAlgorithmOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocAutoscalingPolicy.DataprocAutoscalingPolicyBasicAlgorithmOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2c2e397c3afea0672b4d66cac87fc2291e3d19d79beb4b08c47555ca40fb430)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putYarnConfig")
    def put_yarn_config(
        self,
        *,
        graceful_decommission_timeout: builtins.str,
        scale_down_factor: jsii.Number,
        scale_up_factor: jsii.Number,
        scale_down_min_worker_fraction: typing.Optional[jsii.Number] = None,
        scale_up_min_worker_fraction: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param graceful_decommission_timeout: Timeout for YARN graceful decommissioning of Node Managers. Specifies the duration to wait for jobs to complete before forcefully removing workers (and potentially interrupting jobs). Only applicable to downscaling operations. Bounds: [0s, 1d]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#graceful_decommission_timeout DataprocAutoscalingPolicy#graceful_decommission_timeout}
        :param scale_down_factor: Fraction of average pending memory in the last cooldown period for which to remove workers. A scale-down factor of 1 will result in scaling down so that there is no available memory remaining after the update (more aggressive scaling). A scale-down factor of 0 disables removing workers, which can be beneficial for autoscaling a single job. Bounds: [0.0, 1.0]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#scale_down_factor DataprocAutoscalingPolicy#scale_down_factor}
        :param scale_up_factor: Fraction of average pending memory in the last cooldown period for which to add workers. A scale-up factor of 1.0 will result in scaling up so that there is no pending memory remaining after the update (more aggressive scaling). A scale-up factor closer to 0 will result in a smaller magnitude of scaling up (less aggressive scaling). Bounds: [0.0, 1.0]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#scale_up_factor DataprocAutoscalingPolicy#scale_up_factor}
        :param scale_down_min_worker_fraction: Minimum scale-down threshold as a fraction of total cluster size before scaling occurs. For example, in a 20-worker cluster, a threshold of 0.1 means the autoscaler must recommend at least a 2 worker scale-down for the cluster to scale. A threshold of 0 means the autoscaler will scale down on any recommended change. Bounds: [0.0, 1.0]. Default: 0.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#scale_down_min_worker_fraction DataprocAutoscalingPolicy#scale_down_min_worker_fraction}
        :param scale_up_min_worker_fraction: Minimum scale-up threshold as a fraction of total cluster size before scaling occurs. For example, in a 20-worker cluster, a threshold of 0.1 means the autoscaler must recommend at least a 2-worker scale-up for the cluster to scale. A threshold of 0 means the autoscaler will scale up on any recommended change. Bounds: [0.0, 1.0]. Default: 0.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#scale_up_min_worker_fraction DataprocAutoscalingPolicy#scale_up_min_worker_fraction}
        '''
        value = DataprocAutoscalingPolicyBasicAlgorithmYarnConfig(
            graceful_decommission_timeout=graceful_decommission_timeout,
            scale_down_factor=scale_down_factor,
            scale_up_factor=scale_up_factor,
            scale_down_min_worker_fraction=scale_down_min_worker_fraction,
            scale_up_min_worker_fraction=scale_up_min_worker_fraction,
        )

        return typing.cast(None, jsii.invoke(self, "putYarnConfig", [value]))

    @jsii.member(jsii_name="resetCooldownPeriod")
    def reset_cooldown_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCooldownPeriod", []))

    @builtins.property
    @jsii.member(jsii_name="yarnConfig")
    def yarn_config(
        self,
    ) -> "DataprocAutoscalingPolicyBasicAlgorithmYarnConfigOutputReference":
        return typing.cast("DataprocAutoscalingPolicyBasicAlgorithmYarnConfigOutputReference", jsii.get(self, "yarnConfig"))

    @builtins.property
    @jsii.member(jsii_name="cooldownPeriodInput")
    def cooldown_period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cooldownPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="yarnConfigInput")
    def yarn_config_input(
        self,
    ) -> typing.Optional["DataprocAutoscalingPolicyBasicAlgorithmYarnConfig"]:
        return typing.cast(typing.Optional["DataprocAutoscalingPolicyBasicAlgorithmYarnConfig"], jsii.get(self, "yarnConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="cooldownPeriod")
    def cooldown_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cooldownPeriod"))

    @cooldown_period.setter
    def cooldown_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e653a3bd680c31d7ae90ebc13e887fc10f3f545b88972a856fa6433fc890489f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cooldownPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocAutoscalingPolicyBasicAlgorithm]:
        return typing.cast(typing.Optional[DataprocAutoscalingPolicyBasicAlgorithm], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocAutoscalingPolicyBasicAlgorithm],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a60070352094a2f836c67fc5215201a0504c2572bd81899940ecdc50288ec42b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocAutoscalingPolicy.DataprocAutoscalingPolicyBasicAlgorithmYarnConfig",
    jsii_struct_bases=[],
    name_mapping={
        "graceful_decommission_timeout": "gracefulDecommissionTimeout",
        "scale_down_factor": "scaleDownFactor",
        "scale_up_factor": "scaleUpFactor",
        "scale_down_min_worker_fraction": "scaleDownMinWorkerFraction",
        "scale_up_min_worker_fraction": "scaleUpMinWorkerFraction",
    },
)
class DataprocAutoscalingPolicyBasicAlgorithmYarnConfig:
    def __init__(
        self,
        *,
        graceful_decommission_timeout: builtins.str,
        scale_down_factor: jsii.Number,
        scale_up_factor: jsii.Number,
        scale_down_min_worker_fraction: typing.Optional[jsii.Number] = None,
        scale_up_min_worker_fraction: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param graceful_decommission_timeout: Timeout for YARN graceful decommissioning of Node Managers. Specifies the duration to wait for jobs to complete before forcefully removing workers (and potentially interrupting jobs). Only applicable to downscaling operations. Bounds: [0s, 1d]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#graceful_decommission_timeout DataprocAutoscalingPolicy#graceful_decommission_timeout}
        :param scale_down_factor: Fraction of average pending memory in the last cooldown period for which to remove workers. A scale-down factor of 1 will result in scaling down so that there is no available memory remaining after the update (more aggressive scaling). A scale-down factor of 0 disables removing workers, which can be beneficial for autoscaling a single job. Bounds: [0.0, 1.0]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#scale_down_factor DataprocAutoscalingPolicy#scale_down_factor}
        :param scale_up_factor: Fraction of average pending memory in the last cooldown period for which to add workers. A scale-up factor of 1.0 will result in scaling up so that there is no pending memory remaining after the update (more aggressive scaling). A scale-up factor closer to 0 will result in a smaller magnitude of scaling up (less aggressive scaling). Bounds: [0.0, 1.0]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#scale_up_factor DataprocAutoscalingPolicy#scale_up_factor}
        :param scale_down_min_worker_fraction: Minimum scale-down threshold as a fraction of total cluster size before scaling occurs. For example, in a 20-worker cluster, a threshold of 0.1 means the autoscaler must recommend at least a 2 worker scale-down for the cluster to scale. A threshold of 0 means the autoscaler will scale down on any recommended change. Bounds: [0.0, 1.0]. Default: 0.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#scale_down_min_worker_fraction DataprocAutoscalingPolicy#scale_down_min_worker_fraction}
        :param scale_up_min_worker_fraction: Minimum scale-up threshold as a fraction of total cluster size before scaling occurs. For example, in a 20-worker cluster, a threshold of 0.1 means the autoscaler must recommend at least a 2-worker scale-up for the cluster to scale. A threshold of 0 means the autoscaler will scale up on any recommended change. Bounds: [0.0, 1.0]. Default: 0.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#scale_up_min_worker_fraction DataprocAutoscalingPolicy#scale_up_min_worker_fraction}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aec7cf3b001899243f1688d83c3a18d9dd5bbb4da4e6348dd5baf6f34053f2c)
            check_type(argname="argument graceful_decommission_timeout", value=graceful_decommission_timeout, expected_type=type_hints["graceful_decommission_timeout"])
            check_type(argname="argument scale_down_factor", value=scale_down_factor, expected_type=type_hints["scale_down_factor"])
            check_type(argname="argument scale_up_factor", value=scale_up_factor, expected_type=type_hints["scale_up_factor"])
            check_type(argname="argument scale_down_min_worker_fraction", value=scale_down_min_worker_fraction, expected_type=type_hints["scale_down_min_worker_fraction"])
            check_type(argname="argument scale_up_min_worker_fraction", value=scale_up_min_worker_fraction, expected_type=type_hints["scale_up_min_worker_fraction"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "graceful_decommission_timeout": graceful_decommission_timeout,
            "scale_down_factor": scale_down_factor,
            "scale_up_factor": scale_up_factor,
        }
        if scale_down_min_worker_fraction is not None:
            self._values["scale_down_min_worker_fraction"] = scale_down_min_worker_fraction
        if scale_up_min_worker_fraction is not None:
            self._values["scale_up_min_worker_fraction"] = scale_up_min_worker_fraction

    @builtins.property
    def graceful_decommission_timeout(self) -> builtins.str:
        '''Timeout for YARN graceful decommissioning of Node Managers.

        Specifies the
        duration to wait for jobs to complete before forcefully removing workers
        (and potentially interrupting jobs). Only applicable to downscaling operations.

        Bounds: [0s, 1d].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#graceful_decommission_timeout DataprocAutoscalingPolicy#graceful_decommission_timeout}
        '''
        result = self._values.get("graceful_decommission_timeout")
        assert result is not None, "Required property 'graceful_decommission_timeout' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scale_down_factor(self) -> jsii.Number:
        '''Fraction of average pending memory in the last cooldown period for which to remove workers.

        A scale-down factor of 1 will result in scaling down so that there
        is no available memory remaining after the update (more aggressive scaling).
        A scale-down factor of 0 disables removing workers, which can be beneficial for
        autoscaling a single job.

        Bounds: [0.0, 1.0].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#scale_down_factor DataprocAutoscalingPolicy#scale_down_factor}
        '''
        result = self._values.get("scale_down_factor")
        assert result is not None, "Required property 'scale_down_factor' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def scale_up_factor(self) -> jsii.Number:
        '''Fraction of average pending memory in the last cooldown period for which to add workers.

        A scale-up factor of 1.0 will result in scaling up so that there
        is no pending memory remaining after the update (more aggressive scaling).
        A scale-up factor closer to 0 will result in a smaller magnitude of scaling up
        (less aggressive scaling).

        Bounds: [0.0, 1.0].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#scale_up_factor DataprocAutoscalingPolicy#scale_up_factor}
        '''
        result = self._values.get("scale_up_factor")
        assert result is not None, "Required property 'scale_up_factor' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def scale_down_min_worker_fraction(self) -> typing.Optional[jsii.Number]:
        '''Minimum scale-down threshold as a fraction of total cluster size before scaling occurs.

        For example, in a 20-worker cluster, a threshold of 0.1 means the autoscaler must
        recommend at least a 2 worker scale-down for the cluster to scale. A threshold of 0
        means the autoscaler will scale down on any recommended change.

        Bounds: [0.0, 1.0]. Default: 0.0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#scale_down_min_worker_fraction DataprocAutoscalingPolicy#scale_down_min_worker_fraction}
        '''
        result = self._values.get("scale_down_min_worker_fraction")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def scale_up_min_worker_fraction(self) -> typing.Optional[jsii.Number]:
        '''Minimum scale-up threshold as a fraction of total cluster size before scaling occurs.

        For example, in a 20-worker cluster, a threshold of 0.1 means the autoscaler
        must recommend at least a 2-worker scale-up for the cluster to scale. A threshold of
        0 means the autoscaler will scale up on any recommended change.

        Bounds: [0.0, 1.0]. Default: 0.0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#scale_up_min_worker_fraction DataprocAutoscalingPolicy#scale_up_min_worker_fraction}
        '''
        result = self._values.get("scale_up_min_worker_fraction")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocAutoscalingPolicyBasicAlgorithmYarnConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocAutoscalingPolicyBasicAlgorithmYarnConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocAutoscalingPolicy.DataprocAutoscalingPolicyBasicAlgorithmYarnConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f01fbdd3249def503929d2f07d18ed808842a1283f8dd66f3c0e59bfb782aba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetScaleDownMinWorkerFraction")
    def reset_scale_down_min_worker_fraction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScaleDownMinWorkerFraction", []))

    @jsii.member(jsii_name="resetScaleUpMinWorkerFraction")
    def reset_scale_up_min_worker_fraction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScaleUpMinWorkerFraction", []))

    @builtins.property
    @jsii.member(jsii_name="gracefulDecommissionTimeoutInput")
    def graceful_decommission_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gracefulDecommissionTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleDownFactorInput")
    def scale_down_factor_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scaleDownFactorInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleDownMinWorkerFractionInput")
    def scale_down_min_worker_fraction_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scaleDownMinWorkerFractionInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleUpFactorInput")
    def scale_up_factor_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scaleUpFactorInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleUpMinWorkerFractionInput")
    def scale_up_min_worker_fraction_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scaleUpMinWorkerFractionInput"))

    @builtins.property
    @jsii.member(jsii_name="gracefulDecommissionTimeout")
    def graceful_decommission_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gracefulDecommissionTimeout"))

    @graceful_decommission_timeout.setter
    def graceful_decommission_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51342c37c8fc0d023e1443c199f9b724e9bdba191b67000777c569326a346fde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gracefulDecommissionTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scaleDownFactor")
    def scale_down_factor(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scaleDownFactor"))

    @scale_down_factor.setter
    def scale_down_factor(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4533f767b23b52dccdf8770f758b2b945e14d98211da8219d6deac00cb9e5074)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleDownFactor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scaleDownMinWorkerFraction")
    def scale_down_min_worker_fraction(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scaleDownMinWorkerFraction"))

    @scale_down_min_worker_fraction.setter
    def scale_down_min_worker_fraction(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__841b911741960bd8d57edf5712d88bc596bc4700b8ba598ec7e2d771aff057ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleDownMinWorkerFraction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scaleUpFactor")
    def scale_up_factor(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scaleUpFactor"))

    @scale_up_factor.setter
    def scale_up_factor(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__624da08f53c8c83ace5d90b6fd77cc21e6e68e767a16353feb1fbb5d8479b84e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleUpFactor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scaleUpMinWorkerFraction")
    def scale_up_min_worker_fraction(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scaleUpMinWorkerFraction"))

    @scale_up_min_worker_fraction.setter
    def scale_up_min_worker_fraction(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__439e1b02574b0ea726c48fc6b8b611cd5d7117976312130f8274d0f8606227b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleUpMinWorkerFraction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocAutoscalingPolicyBasicAlgorithmYarnConfig]:
        return typing.cast(typing.Optional[DataprocAutoscalingPolicyBasicAlgorithmYarnConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocAutoscalingPolicyBasicAlgorithmYarnConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9295f4008fad47589a759ea05e8df59a6d1a0dafac87cc517856b3b82d9664a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocAutoscalingPolicy.DataprocAutoscalingPolicyConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "policy_id": "policyId",
        "basic_algorithm": "basicAlgorithm",
        "id": "id",
        "location": "location",
        "project": "project",
        "secondary_worker_config": "secondaryWorkerConfig",
        "timeouts": "timeouts",
        "worker_config": "workerConfig",
    },
)
class DataprocAutoscalingPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        policy_id: builtins.str,
        basic_algorithm: typing.Optional[typing.Union[DataprocAutoscalingPolicyBasicAlgorithm, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        secondary_worker_config: typing.Optional[typing.Union["DataprocAutoscalingPolicySecondaryWorkerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["DataprocAutoscalingPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        worker_config: typing.Optional[typing.Union["DataprocAutoscalingPolicyWorkerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param policy_id: The policy id. The id must contain only letters (a-z, A-Z), numbers (0-9), underscores (_), and hyphens (-). Cannot begin or end with underscore or hyphen. Must consist of between 3 and 50 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#policy_id DataprocAutoscalingPolicy#policy_id}
        :param basic_algorithm: basic_algorithm block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#basic_algorithm DataprocAutoscalingPolicy#basic_algorithm}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#id DataprocAutoscalingPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param location: The location where the autoscaling policy should reside. The default value is 'global'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#location DataprocAutoscalingPolicy#location}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#project DataprocAutoscalingPolicy#project}.
        :param secondary_worker_config: secondary_worker_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#secondary_worker_config DataprocAutoscalingPolicy#secondary_worker_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#timeouts DataprocAutoscalingPolicy#timeouts}
        :param worker_config: worker_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#worker_config DataprocAutoscalingPolicy#worker_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(basic_algorithm, dict):
            basic_algorithm = DataprocAutoscalingPolicyBasicAlgorithm(**basic_algorithm)
        if isinstance(secondary_worker_config, dict):
            secondary_worker_config = DataprocAutoscalingPolicySecondaryWorkerConfig(**secondary_worker_config)
        if isinstance(timeouts, dict):
            timeouts = DataprocAutoscalingPolicyTimeouts(**timeouts)
        if isinstance(worker_config, dict):
            worker_config = DataprocAutoscalingPolicyWorkerConfig(**worker_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__653c6f7659619ec60a5deaf669cb2b15091e4f4685ef4795f1265396bcf30d30)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument policy_id", value=policy_id, expected_type=type_hints["policy_id"])
            check_type(argname="argument basic_algorithm", value=basic_algorithm, expected_type=type_hints["basic_algorithm"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument secondary_worker_config", value=secondary_worker_config, expected_type=type_hints["secondary_worker_config"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument worker_config", value=worker_config, expected_type=type_hints["worker_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy_id": policy_id,
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
        if basic_algorithm is not None:
            self._values["basic_algorithm"] = basic_algorithm
        if id is not None:
            self._values["id"] = id
        if location is not None:
            self._values["location"] = location
        if project is not None:
            self._values["project"] = project
        if secondary_worker_config is not None:
            self._values["secondary_worker_config"] = secondary_worker_config
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if worker_config is not None:
            self._values["worker_config"] = worker_config

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
    def policy_id(self) -> builtins.str:
        '''The policy id.

        The id must contain only letters (a-z, A-Z), numbers (0-9), underscores (_),
        and hyphens (-). Cannot begin or end with underscore or hyphen. Must consist of between
        3 and 50 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#policy_id DataprocAutoscalingPolicy#policy_id}
        '''
        result = self._values.get("policy_id")
        assert result is not None, "Required property 'policy_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def basic_algorithm(
        self,
    ) -> typing.Optional[DataprocAutoscalingPolicyBasicAlgorithm]:
        '''basic_algorithm block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#basic_algorithm DataprocAutoscalingPolicy#basic_algorithm}
        '''
        result = self._values.get("basic_algorithm")
        return typing.cast(typing.Optional[DataprocAutoscalingPolicyBasicAlgorithm], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#id DataprocAutoscalingPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The  location where the autoscaling policy should reside. The default value is 'global'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#location DataprocAutoscalingPolicy#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#project DataprocAutoscalingPolicy#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secondary_worker_config(
        self,
    ) -> typing.Optional["DataprocAutoscalingPolicySecondaryWorkerConfig"]:
        '''secondary_worker_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#secondary_worker_config DataprocAutoscalingPolicy#secondary_worker_config}
        '''
        result = self._values.get("secondary_worker_config")
        return typing.cast(typing.Optional["DataprocAutoscalingPolicySecondaryWorkerConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DataprocAutoscalingPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#timeouts DataprocAutoscalingPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataprocAutoscalingPolicyTimeouts"], result)

    @builtins.property
    def worker_config(self) -> typing.Optional["DataprocAutoscalingPolicyWorkerConfig"]:
        '''worker_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#worker_config DataprocAutoscalingPolicy#worker_config}
        '''
        result = self._values.get("worker_config")
        return typing.cast(typing.Optional["DataprocAutoscalingPolicyWorkerConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocAutoscalingPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocAutoscalingPolicy.DataprocAutoscalingPolicySecondaryWorkerConfig",
    jsii_struct_bases=[],
    name_mapping={
        "max_instances": "maxInstances",
        "min_instances": "minInstances",
        "weight": "weight",
    },
)
class DataprocAutoscalingPolicySecondaryWorkerConfig:
    def __init__(
        self,
        *,
        max_instances: typing.Optional[jsii.Number] = None,
        min_instances: typing.Optional[jsii.Number] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_instances: Maximum number of instances for this group. Note that by default, clusters will not use secondary workers. Required for secondary workers if the minimum secondary instances is set. Bounds: [minInstances, ). Defaults to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#max_instances DataprocAutoscalingPolicy#max_instances}
        :param min_instances: Minimum number of instances for this group. Bounds: [0, maxInstances]. Defaults to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#min_instances DataprocAutoscalingPolicy#min_instances}
        :param weight: Weight for the instance group, which is used to determine the fraction of total workers in the cluster from this instance group. For example, if primary workers have weight 2, and secondary workers have weight 1, the cluster will have approximately 2 primary workers for each secondary worker. The cluster may not reach the specified balance if constrained by min/max bounds or other autoscaling settings. For example, if maxInstances for secondary workers is 0, then only primary workers will be added. The cluster can also be out of balance when created. If weight is not set on any instance group, the cluster will default to equal weight for all groups: the cluster will attempt to maintain an equal number of workers in each group within the configured size bounds for each group. If weight is set for one group only, the cluster will default to zero weight on the unset group. For example if weight is set only on primary workers, the cluster will use primary workers only and no secondary workers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#weight DataprocAutoscalingPolicy#weight}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77440b6cbc4b682b619754068df639a51f6f97508151ad861ebd2f10693ad46f)
            check_type(argname="argument max_instances", value=max_instances, expected_type=type_hints["max_instances"])
            check_type(argname="argument min_instances", value=min_instances, expected_type=type_hints["min_instances"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_instances is not None:
            self._values["max_instances"] = max_instances
        if min_instances is not None:
            self._values["min_instances"] = min_instances
        if weight is not None:
            self._values["weight"] = weight

    @builtins.property
    def max_instances(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of instances for this group.

        Note that by default, clusters will not use
        secondary workers. Required for secondary workers if the minimum secondary instances is set.
        Bounds: [minInstances, ). Defaults to 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#max_instances DataprocAutoscalingPolicy#max_instances}
        '''
        result = self._values.get("max_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_instances(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of instances for this group. Bounds: [0, maxInstances]. Defaults to 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#min_instances DataprocAutoscalingPolicy#min_instances}
        '''
        result = self._values.get("min_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''Weight for the instance group, which is used to determine the fraction of total workers in the cluster from this instance group.

        For example, if primary workers have weight 2,
        and secondary workers have weight 1, the cluster will have approximately 2 primary workers
        for each secondary worker.

        The cluster may not reach the specified balance if constrained by min/max bounds or other
        autoscaling settings. For example, if maxInstances for secondary workers is 0, then only
        primary workers will be added. The cluster can also be out of balance when created.

        If weight is not set on any instance group, the cluster will default to equal weight for
        all groups: the cluster will attempt to maintain an equal number of workers in each group
        within the configured size bounds for each group. If weight is set for one group only,
        the cluster will default to zero weight on the unset group. For example if weight is set
        only on primary workers, the cluster will use primary workers only and no secondary workers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#weight DataprocAutoscalingPolicy#weight}
        '''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocAutoscalingPolicySecondaryWorkerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocAutoscalingPolicySecondaryWorkerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocAutoscalingPolicy.DataprocAutoscalingPolicySecondaryWorkerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81ae9b7451f434d8ec60dc305fd0d720891d6361c660c6832a30487b87eee88d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxInstances")
    def reset_max_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxInstances", []))

    @jsii.member(jsii_name="resetMinInstances")
    def reset_min_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinInstances", []))

    @jsii.member(jsii_name="resetWeight")
    def reset_weight(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeight", []))

    @builtins.property
    @jsii.member(jsii_name="maxInstancesInput")
    def max_instances_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="minInstancesInput")
    def min_instances_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="weightInput")
    def weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weightInput"))

    @builtins.property
    @jsii.member(jsii_name="maxInstances")
    def max_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxInstances"))

    @max_instances.setter
    def max_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9882f9504a7af82aa3caa9afa1cced44ccec857df99e784a729207dece6d75c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minInstances")
    def min_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minInstances"))

    @min_instances.setter
    def min_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fc0d68c9e2e9c9a3ed98888485dfd27d741f81c950054e6e7fb5b83eb39d651)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @weight.setter
    def weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b191c90fade70c08b54d3869791ce3224e448ab5e5a9d8a613066ced53c5a22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weight", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocAutoscalingPolicySecondaryWorkerConfig]:
        return typing.cast(typing.Optional[DataprocAutoscalingPolicySecondaryWorkerConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocAutoscalingPolicySecondaryWorkerConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__150973b886a0a67ee12a5a4072460d7a037672dab3ff21966b86bd89ff12c142)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocAutoscalingPolicy.DataprocAutoscalingPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DataprocAutoscalingPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#create DataprocAutoscalingPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#delete DataprocAutoscalingPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#update DataprocAutoscalingPolicy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b07cfaab691739dce8f8d8585bc17d20871f563076bce1ac590abe173b6cf9a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#create DataprocAutoscalingPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#delete DataprocAutoscalingPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#update DataprocAutoscalingPolicy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocAutoscalingPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocAutoscalingPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocAutoscalingPolicy.DataprocAutoscalingPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a52acb20b17c3c7c20b08e5a362d0f3a394f78f1bbd70722e834fe093c4554d9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6d4ded8e6bec26e7b987d6e40f3dc4533bae10745e41c959d231752c67e0113)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2416a05e1660fdb460c9f4a83370e8d245ee037631907370dc5b59e15b6e2d87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f73c451238a111abc5cb29511debf481ca6c0bb54c461a8c160cbbf1a7213053)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocAutoscalingPolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocAutoscalingPolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocAutoscalingPolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32a0f393d13c610277670a05452e55503a23bff9554970c16c45f8aa8308f618)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocAutoscalingPolicy.DataprocAutoscalingPolicyWorkerConfig",
    jsii_struct_bases=[],
    name_mapping={
        "max_instances": "maxInstances",
        "min_instances": "minInstances",
        "weight": "weight",
    },
)
class DataprocAutoscalingPolicyWorkerConfig:
    def __init__(
        self,
        *,
        max_instances: jsii.Number,
        min_instances: typing.Optional[jsii.Number] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_instances: Maximum number of instances for this group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#max_instances DataprocAutoscalingPolicy#max_instances}
        :param min_instances: Minimum number of instances for this group. Bounds: [2, maxInstances]. Defaults to 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#min_instances DataprocAutoscalingPolicy#min_instances}
        :param weight: Weight for the instance group, which is used to determine the fraction of total workers in the cluster from this instance group. For example, if primary workers have weight 2, and secondary workers have weight 1, the cluster will have approximately 2 primary workers for each secondary worker. The cluster may not reach the specified balance if constrained by min/max bounds or other autoscaling settings. For example, if maxInstances for secondary workers is 0, then only primary workers will be added. The cluster can also be out of balance when created. If weight is not set on any instance group, the cluster will default to equal weight for all groups: the cluster will attempt to maintain an equal number of workers in each group within the configured size bounds for each group. If weight is set for one group only, the cluster will default to zero weight on the unset group. For example if weight is set only on primary workers, the cluster will use primary workers only and no secondary workers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#weight DataprocAutoscalingPolicy#weight}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1de8d1c35bc0a9c972ffc3ee6595263e88a372f5792b9b510c82ab746fe6bc6b)
            check_type(argname="argument max_instances", value=max_instances, expected_type=type_hints["max_instances"])
            check_type(argname="argument min_instances", value=min_instances, expected_type=type_hints["min_instances"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_instances": max_instances,
        }
        if min_instances is not None:
            self._values["min_instances"] = min_instances
        if weight is not None:
            self._values["weight"] = weight

    @builtins.property
    def max_instances(self) -> jsii.Number:
        '''Maximum number of instances for this group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#max_instances DataprocAutoscalingPolicy#max_instances}
        '''
        result = self._values.get("max_instances")
        assert result is not None, "Required property 'max_instances' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def min_instances(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of instances for this group. Bounds: [2, maxInstances]. Defaults to 2.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#min_instances DataprocAutoscalingPolicy#min_instances}
        '''
        result = self._values.get("min_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''Weight for the instance group, which is used to determine the fraction of total workers in the cluster from this instance group.

        For example, if primary workers have weight 2,
        and secondary workers have weight 1, the cluster will have approximately 2 primary workers
        for each secondary worker.

        The cluster may not reach the specified balance if constrained by min/max bounds or other
        autoscaling settings. For example, if maxInstances for secondary workers is 0, then only
        primary workers will be added. The cluster can also be out of balance when created.

        If weight is not set on any instance group, the cluster will default to equal weight for
        all groups: the cluster will attempt to maintain an equal number of workers in each group
        within the configured size bounds for each group. If weight is set for one group only,
        the cluster will default to zero weight on the unset group. For example if weight is set
        only on primary workers, the cluster will use primary workers only and no secondary workers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_autoscaling_policy#weight DataprocAutoscalingPolicy#weight}
        '''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocAutoscalingPolicyWorkerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocAutoscalingPolicyWorkerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocAutoscalingPolicy.DataprocAutoscalingPolicyWorkerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec0c50516fcdebbfb81f5b8d49660d04cda44367745357d9ceae234f5d53331f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMinInstances")
    def reset_min_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinInstances", []))

    @jsii.member(jsii_name="resetWeight")
    def reset_weight(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeight", []))

    @builtins.property
    @jsii.member(jsii_name="maxInstancesInput")
    def max_instances_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="minInstancesInput")
    def min_instances_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="weightInput")
    def weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weightInput"))

    @builtins.property
    @jsii.member(jsii_name="maxInstances")
    def max_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxInstances"))

    @max_instances.setter
    def max_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0c6c25d019351d0975fd0dfee42ade2df2d481e74ba8db7f2594bb423e87284)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minInstances")
    def min_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minInstances"))

    @min_instances.setter
    def min_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a06db920c179e7031ff24fbc9fc2a17bf9fd530840e3e53fe04cad515c97fbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @weight.setter
    def weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80dd763c87946840d48fd45bd497f54ba5fb488e2e35d5b092b7021a5e36c826)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weight", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocAutoscalingPolicyWorkerConfig]:
        return typing.cast(typing.Optional[DataprocAutoscalingPolicyWorkerConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocAutoscalingPolicyWorkerConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19f57a3329378a6d0be8b7624340c888f1cb36af0c2ce2e851671dc6639a4c9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataprocAutoscalingPolicy",
    "DataprocAutoscalingPolicyBasicAlgorithm",
    "DataprocAutoscalingPolicyBasicAlgorithmOutputReference",
    "DataprocAutoscalingPolicyBasicAlgorithmYarnConfig",
    "DataprocAutoscalingPolicyBasicAlgorithmYarnConfigOutputReference",
    "DataprocAutoscalingPolicyConfig",
    "DataprocAutoscalingPolicySecondaryWorkerConfig",
    "DataprocAutoscalingPolicySecondaryWorkerConfigOutputReference",
    "DataprocAutoscalingPolicyTimeouts",
    "DataprocAutoscalingPolicyTimeoutsOutputReference",
    "DataprocAutoscalingPolicyWorkerConfig",
    "DataprocAutoscalingPolicyWorkerConfigOutputReference",
]

publication.publish()

def _typecheckingstub__717fa8e0d07b277bd5cdb2d8946aff06d41f02d9adda1f746a14fb12c30bc3b7(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    policy_id: builtins.str,
    basic_algorithm: typing.Optional[typing.Union[DataprocAutoscalingPolicyBasicAlgorithm, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    secondary_worker_config: typing.Optional[typing.Union[DataprocAutoscalingPolicySecondaryWorkerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[DataprocAutoscalingPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    worker_config: typing.Optional[typing.Union[DataprocAutoscalingPolicyWorkerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__700082d80b45d1c0a47d01001b282a0997069422433002f0e5f54ab851787a78(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45602e0f0ff2e3fbcd534709ab2b9084e64901d3d1d48b87e4203284d132d59a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__131416a252572784a29504897b2efc6f75f95bb9d57efa3d8461b77dd9c53c12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a15882f11d3d0ec18898a143b1cf2f46e317f9794dcbb8a3e2ec6784474ba1b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__518a796e9f8051d587ca837b9e246718841f230b3043cc08582605dbb1b7561a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0392426022d332921971a8c20288eb32c7040946068fc4e480dbfa209175813e(
    *,
    yarn_config: typing.Union[DataprocAutoscalingPolicyBasicAlgorithmYarnConfig, typing.Dict[builtins.str, typing.Any]],
    cooldown_period: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2c2e397c3afea0672b4d66cac87fc2291e3d19d79beb4b08c47555ca40fb430(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e653a3bd680c31d7ae90ebc13e887fc10f3f545b88972a856fa6433fc890489f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a60070352094a2f836c67fc5215201a0504c2572bd81899940ecdc50288ec42b(
    value: typing.Optional[DataprocAutoscalingPolicyBasicAlgorithm],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aec7cf3b001899243f1688d83c3a18d9dd5bbb4da4e6348dd5baf6f34053f2c(
    *,
    graceful_decommission_timeout: builtins.str,
    scale_down_factor: jsii.Number,
    scale_up_factor: jsii.Number,
    scale_down_min_worker_fraction: typing.Optional[jsii.Number] = None,
    scale_up_min_worker_fraction: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f01fbdd3249def503929d2f07d18ed808842a1283f8dd66f3c0e59bfb782aba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51342c37c8fc0d023e1443c199f9b724e9bdba191b67000777c569326a346fde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4533f767b23b52dccdf8770f758b2b945e14d98211da8219d6deac00cb9e5074(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__841b911741960bd8d57edf5712d88bc596bc4700b8ba598ec7e2d771aff057ff(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__624da08f53c8c83ace5d90b6fd77cc21e6e68e767a16353feb1fbb5d8479b84e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__439e1b02574b0ea726c48fc6b8b611cd5d7117976312130f8274d0f8606227b5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9295f4008fad47589a759ea05e8df59a6d1a0dafac87cc517856b3b82d9664a7(
    value: typing.Optional[DataprocAutoscalingPolicyBasicAlgorithmYarnConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__653c6f7659619ec60a5deaf669cb2b15091e4f4685ef4795f1265396bcf30d30(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    policy_id: builtins.str,
    basic_algorithm: typing.Optional[typing.Union[DataprocAutoscalingPolicyBasicAlgorithm, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    secondary_worker_config: typing.Optional[typing.Union[DataprocAutoscalingPolicySecondaryWorkerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[DataprocAutoscalingPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    worker_config: typing.Optional[typing.Union[DataprocAutoscalingPolicyWorkerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77440b6cbc4b682b619754068df639a51f6f97508151ad861ebd2f10693ad46f(
    *,
    max_instances: typing.Optional[jsii.Number] = None,
    min_instances: typing.Optional[jsii.Number] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81ae9b7451f434d8ec60dc305fd0d720891d6361c660c6832a30487b87eee88d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9882f9504a7af82aa3caa9afa1cced44ccec857df99e784a729207dece6d75c7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fc0d68c9e2e9c9a3ed98888485dfd27d741f81c950054e6e7fb5b83eb39d651(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b191c90fade70c08b54d3869791ce3224e448ab5e5a9d8a613066ced53c5a22(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__150973b886a0a67ee12a5a4072460d7a037672dab3ff21966b86bd89ff12c142(
    value: typing.Optional[DataprocAutoscalingPolicySecondaryWorkerConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b07cfaab691739dce8f8d8585bc17d20871f563076bce1ac590abe173b6cf9a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a52acb20b17c3c7c20b08e5a362d0f3a394f78f1bbd70722e834fe093c4554d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6d4ded8e6bec26e7b987d6e40f3dc4533bae10745e41c959d231752c67e0113(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2416a05e1660fdb460c9f4a83370e8d245ee037631907370dc5b59e15b6e2d87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f73c451238a111abc5cb29511debf481ca6c0bb54c461a8c160cbbf1a7213053(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32a0f393d13c610277670a05452e55503a23bff9554970c16c45f8aa8308f618(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocAutoscalingPolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1de8d1c35bc0a9c972ffc3ee6595263e88a372f5792b9b510c82ab746fe6bc6b(
    *,
    max_instances: jsii.Number,
    min_instances: typing.Optional[jsii.Number] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec0c50516fcdebbfb81f5b8d49660d04cda44367745357d9ceae234f5d53331f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c6c25d019351d0975fd0dfee42ade2df2d481e74ba8db7f2594bb423e87284(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a06db920c179e7031ff24fbc9fc2a17bf9fd530840e3e53fe04cad515c97fbc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80dd763c87946840d48fd45bd497f54ba5fb488e2e35d5b092b7021a5e36c826(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19f57a3329378a6d0be8b7624340c888f1cb36af0c2ce2e851671dc6639a4c9a(
    value: typing.Optional[DataprocAutoscalingPolicyWorkerConfig],
) -> None:
    """Type checking stubs"""
    pass
