r'''
# `aws_ecs_capacity_provider`

Refer to the Terraform Registry for docs: [`aws_ecs_capacity_provider`](https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider).
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


class EcsCapacityProvider(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ecsCapacityProvider.EcsCapacityProvider",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider aws_ecs_capacity_provider}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        auto_scaling_group_provider: typing.Optional[typing.Union["EcsCapacityProviderAutoScalingGroupProvider", typing.Dict[builtins.str, typing.Any]]] = None,
        cluster: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        managed_instances_provider: typing.Optional[typing.Union["EcsCapacityProviderManagedInstancesProvider", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider aws_ecs_capacity_provider} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#name EcsCapacityProvider#name}.
        :param auto_scaling_group_provider: auto_scaling_group_provider block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#auto_scaling_group_provider EcsCapacityProvider#auto_scaling_group_provider}
        :param cluster: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#cluster EcsCapacityProvider#cluster}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#id EcsCapacityProvider#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param managed_instances_provider: managed_instances_provider block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#managed_instances_provider EcsCapacityProvider#managed_instances_provider}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#region EcsCapacityProvider#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#tags EcsCapacityProvider#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#tags_all EcsCapacityProvider#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3bf2746c14ee596c69de0470d6191b36f92644c677e4720667d230d8ba01a7e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = EcsCapacityProviderConfig(
            name=name,
            auto_scaling_group_provider=auto_scaling_group_provider,
            cluster=cluster,
            id=id,
            managed_instances_provider=managed_instances_provider,
            region=region,
            tags=tags,
            tags_all=tags_all,
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
        '''Generates CDKTF code for importing a EcsCapacityProvider resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the EcsCapacityProvider to import.
        :param import_from_id: The id of the existing EcsCapacityProvider that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the EcsCapacityProvider to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f77e654120b74a191b7418a905ced4e81536a19d86fa1cf932836fb21e393f4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAutoScalingGroupProvider")
    def put_auto_scaling_group_provider(
        self,
        *,
        auto_scaling_group_arn: builtins.str,
        managed_draining: typing.Optional[builtins.str] = None,
        managed_scaling: typing.Optional[typing.Union["EcsCapacityProviderAutoScalingGroupProviderManagedScaling", typing.Dict[builtins.str, typing.Any]]] = None,
        managed_termination_protection: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auto_scaling_group_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#auto_scaling_group_arn EcsCapacityProvider#auto_scaling_group_arn}.
        :param managed_draining: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#managed_draining EcsCapacityProvider#managed_draining}.
        :param managed_scaling: managed_scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#managed_scaling EcsCapacityProvider#managed_scaling}
        :param managed_termination_protection: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#managed_termination_protection EcsCapacityProvider#managed_termination_protection}.
        '''
        value = EcsCapacityProviderAutoScalingGroupProvider(
            auto_scaling_group_arn=auto_scaling_group_arn,
            managed_draining=managed_draining,
            managed_scaling=managed_scaling,
            managed_termination_protection=managed_termination_protection,
        )

        return typing.cast(None, jsii.invoke(self, "putAutoScalingGroupProvider", [value]))

    @jsii.member(jsii_name="putManagedInstancesProvider")
    def put_managed_instances_provider(
        self,
        *,
        infrastructure_role_arn: builtins.str,
        instance_launch_template: typing.Union["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplate", typing.Dict[builtins.str, typing.Any]],
        infrastructure_optimization: typing.Optional[typing.Union["EcsCapacityProviderManagedInstancesProviderInfrastructureOptimization", typing.Dict[builtins.str, typing.Any]]] = None,
        propagate_tags: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param infrastructure_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#infrastructure_role_arn EcsCapacityProvider#infrastructure_role_arn}.
        :param instance_launch_template: instance_launch_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#instance_launch_template EcsCapacityProvider#instance_launch_template}
        :param infrastructure_optimization: infrastructure_optimization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#infrastructure_optimization EcsCapacityProvider#infrastructure_optimization}
        :param propagate_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#propagate_tags EcsCapacityProvider#propagate_tags}.
        '''
        value = EcsCapacityProviderManagedInstancesProvider(
            infrastructure_role_arn=infrastructure_role_arn,
            instance_launch_template=instance_launch_template,
            infrastructure_optimization=infrastructure_optimization,
            propagate_tags=propagate_tags,
        )

        return typing.cast(None, jsii.invoke(self, "putManagedInstancesProvider", [value]))

    @jsii.member(jsii_name="resetAutoScalingGroupProvider")
    def reset_auto_scaling_group_provider(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoScalingGroupProvider", []))

    @jsii.member(jsii_name="resetCluster")
    def reset_cluster(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCluster", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetManagedInstancesProvider")
    def reset_managed_instances_provider(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedInstancesProvider", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

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
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="autoScalingGroupProvider")
    def auto_scaling_group_provider(
        self,
    ) -> "EcsCapacityProviderAutoScalingGroupProviderOutputReference":
        return typing.cast("EcsCapacityProviderAutoScalingGroupProviderOutputReference", jsii.get(self, "autoScalingGroupProvider"))

    @builtins.property
    @jsii.member(jsii_name="managedInstancesProvider")
    def managed_instances_provider(
        self,
    ) -> "EcsCapacityProviderManagedInstancesProviderOutputReference":
        return typing.cast("EcsCapacityProviderManagedInstancesProviderOutputReference", jsii.get(self, "managedInstancesProvider"))

    @builtins.property
    @jsii.member(jsii_name="autoScalingGroupProviderInput")
    def auto_scaling_group_provider_input(
        self,
    ) -> typing.Optional["EcsCapacityProviderAutoScalingGroupProvider"]:
        return typing.cast(typing.Optional["EcsCapacityProviderAutoScalingGroupProvider"], jsii.get(self, "autoScalingGroupProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterInput")
    def cluster_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="managedInstancesProviderInput")
    def managed_instances_provider_input(
        self,
    ) -> typing.Optional["EcsCapacityProviderManagedInstancesProvider"]:
        return typing.cast(typing.Optional["EcsCapacityProviderManagedInstancesProvider"], jsii.get(self, "managedInstancesProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsAllInput")
    def tags_all_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsAllInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cluster"))

    @cluster.setter
    def cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bee01a8ebfa3cdb0c37cfb46929f3f2fc1ff777ddfdec739fe139f379ee88a78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__817aaea4449db5ba8429963a71ae12db12fe851bbae3abbd427b3280985bd6e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79b514b296517015c6728dc6c41eee1d740d62c016b895b782f499ca8d820f22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1853ac1235a23ba19310129de7eba9d8dac52dd964c3ab01f1274a165af4eeb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a64ed14430dac70c950aa828f0feaef8411717b5dceb1eb11bd56241e53cb96f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69aa72aeda7db743c7eb86a3ea47bbce101ad26ddc96703cd38a29b97f13423e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ecsCapacityProvider.EcsCapacityProviderAutoScalingGroupProvider",
    jsii_struct_bases=[],
    name_mapping={
        "auto_scaling_group_arn": "autoScalingGroupArn",
        "managed_draining": "managedDraining",
        "managed_scaling": "managedScaling",
        "managed_termination_protection": "managedTerminationProtection",
    },
)
class EcsCapacityProviderAutoScalingGroupProvider:
    def __init__(
        self,
        *,
        auto_scaling_group_arn: builtins.str,
        managed_draining: typing.Optional[builtins.str] = None,
        managed_scaling: typing.Optional[typing.Union["EcsCapacityProviderAutoScalingGroupProviderManagedScaling", typing.Dict[builtins.str, typing.Any]]] = None,
        managed_termination_protection: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auto_scaling_group_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#auto_scaling_group_arn EcsCapacityProvider#auto_scaling_group_arn}.
        :param managed_draining: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#managed_draining EcsCapacityProvider#managed_draining}.
        :param managed_scaling: managed_scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#managed_scaling EcsCapacityProvider#managed_scaling}
        :param managed_termination_protection: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#managed_termination_protection EcsCapacityProvider#managed_termination_protection}.
        '''
        if isinstance(managed_scaling, dict):
            managed_scaling = EcsCapacityProviderAutoScalingGroupProviderManagedScaling(**managed_scaling)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__798d40ce0c9fb092567831846c9439a51ff85fe90e6898e9a8d6cc6e7bd58d7d)
            check_type(argname="argument auto_scaling_group_arn", value=auto_scaling_group_arn, expected_type=type_hints["auto_scaling_group_arn"])
            check_type(argname="argument managed_draining", value=managed_draining, expected_type=type_hints["managed_draining"])
            check_type(argname="argument managed_scaling", value=managed_scaling, expected_type=type_hints["managed_scaling"])
            check_type(argname="argument managed_termination_protection", value=managed_termination_protection, expected_type=type_hints["managed_termination_protection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auto_scaling_group_arn": auto_scaling_group_arn,
        }
        if managed_draining is not None:
            self._values["managed_draining"] = managed_draining
        if managed_scaling is not None:
            self._values["managed_scaling"] = managed_scaling
        if managed_termination_protection is not None:
            self._values["managed_termination_protection"] = managed_termination_protection

    @builtins.property
    def auto_scaling_group_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#auto_scaling_group_arn EcsCapacityProvider#auto_scaling_group_arn}.'''
        result = self._values.get("auto_scaling_group_arn")
        assert result is not None, "Required property 'auto_scaling_group_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def managed_draining(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#managed_draining EcsCapacityProvider#managed_draining}.'''
        result = self._values.get("managed_draining")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_scaling(
        self,
    ) -> typing.Optional["EcsCapacityProviderAutoScalingGroupProviderManagedScaling"]:
        '''managed_scaling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#managed_scaling EcsCapacityProvider#managed_scaling}
        '''
        result = self._values.get("managed_scaling")
        return typing.cast(typing.Optional["EcsCapacityProviderAutoScalingGroupProviderManagedScaling"], result)

    @builtins.property
    def managed_termination_protection(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#managed_termination_protection EcsCapacityProvider#managed_termination_protection}.'''
        result = self._values.get("managed_termination_protection")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsCapacityProviderAutoScalingGroupProvider(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ecsCapacityProvider.EcsCapacityProviderAutoScalingGroupProviderManagedScaling",
    jsii_struct_bases=[],
    name_mapping={
        "instance_warmup_period": "instanceWarmupPeriod",
        "maximum_scaling_step_size": "maximumScalingStepSize",
        "minimum_scaling_step_size": "minimumScalingStepSize",
        "status": "status",
        "target_capacity": "targetCapacity",
    },
)
class EcsCapacityProviderAutoScalingGroupProviderManagedScaling:
    def __init__(
        self,
        *,
        instance_warmup_period: typing.Optional[jsii.Number] = None,
        maximum_scaling_step_size: typing.Optional[jsii.Number] = None,
        minimum_scaling_step_size: typing.Optional[jsii.Number] = None,
        status: typing.Optional[builtins.str] = None,
        target_capacity: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param instance_warmup_period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#instance_warmup_period EcsCapacityProvider#instance_warmup_period}.
        :param maximum_scaling_step_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#maximum_scaling_step_size EcsCapacityProvider#maximum_scaling_step_size}.
        :param minimum_scaling_step_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#minimum_scaling_step_size EcsCapacityProvider#minimum_scaling_step_size}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#status EcsCapacityProvider#status}.
        :param target_capacity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#target_capacity EcsCapacityProvider#target_capacity}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aea398c383aa653974f99a5f3193fefbbe0d0aedfc884333a70643b231a3a8e1)
            check_type(argname="argument instance_warmup_period", value=instance_warmup_period, expected_type=type_hints["instance_warmup_period"])
            check_type(argname="argument maximum_scaling_step_size", value=maximum_scaling_step_size, expected_type=type_hints["maximum_scaling_step_size"])
            check_type(argname="argument minimum_scaling_step_size", value=minimum_scaling_step_size, expected_type=type_hints["minimum_scaling_step_size"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument target_capacity", value=target_capacity, expected_type=type_hints["target_capacity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_warmup_period is not None:
            self._values["instance_warmup_period"] = instance_warmup_period
        if maximum_scaling_step_size is not None:
            self._values["maximum_scaling_step_size"] = maximum_scaling_step_size
        if minimum_scaling_step_size is not None:
            self._values["minimum_scaling_step_size"] = minimum_scaling_step_size
        if status is not None:
            self._values["status"] = status
        if target_capacity is not None:
            self._values["target_capacity"] = target_capacity

    @builtins.property
    def instance_warmup_period(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#instance_warmup_period EcsCapacityProvider#instance_warmup_period}.'''
        result = self._values.get("instance_warmup_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_scaling_step_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#maximum_scaling_step_size EcsCapacityProvider#maximum_scaling_step_size}.'''
        result = self._values.get("maximum_scaling_step_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minimum_scaling_step_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#minimum_scaling_step_size EcsCapacityProvider#minimum_scaling_step_size}.'''
        result = self._values.get("minimum_scaling_step_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#status EcsCapacityProvider#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_capacity(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#target_capacity EcsCapacityProvider#target_capacity}.'''
        result = self._values.get("target_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsCapacityProviderAutoScalingGroupProviderManagedScaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EcsCapacityProviderAutoScalingGroupProviderManagedScalingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ecsCapacityProvider.EcsCapacityProviderAutoScalingGroupProviderManagedScalingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9125a61629fe561ef7eb37c07c25ddcd12dc95c448210a868e992572b45b5535)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInstanceWarmupPeriod")
    def reset_instance_warmup_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceWarmupPeriod", []))

    @jsii.member(jsii_name="resetMaximumScalingStepSize")
    def reset_maximum_scaling_step_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumScalingStepSize", []))

    @jsii.member(jsii_name="resetMinimumScalingStepSize")
    def reset_minimum_scaling_step_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimumScalingStepSize", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetTargetCapacity")
    def reset_target_capacity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetCapacity", []))

    @builtins.property
    @jsii.member(jsii_name="instanceWarmupPeriodInput")
    def instance_warmup_period_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "instanceWarmupPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumScalingStepSizeInput")
    def maximum_scaling_step_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumScalingStepSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumScalingStepSizeInput")
    def minimum_scaling_step_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minimumScalingStepSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="targetCapacityInput")
    def target_capacity_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetCapacityInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceWarmupPeriod")
    def instance_warmup_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "instanceWarmupPeriod"))

    @instance_warmup_period.setter
    def instance_warmup_period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9e129789c8e6c678c7ef0e4f10f5b03301b05658da08e20a62036f125bb0a9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceWarmupPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumScalingStepSize")
    def maximum_scaling_step_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumScalingStepSize"))

    @maximum_scaling_step_size.setter
    def maximum_scaling_step_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ae7799fb416a40882e83a1509d08e78b56227826943b342e972bce6b0650b24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumScalingStepSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimumScalingStepSize")
    def minimum_scaling_step_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minimumScalingStepSize"))

    @minimum_scaling_step_size.setter
    def minimum_scaling_step_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60dc4970a8ab39096418bf3f408bed39e6bb061e4e49c7a60dc945f82ce3333c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumScalingStepSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5018b2e3685ad5f14413e3a4ee7d20e3e9d4883557f10a2da94335a55258347)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetCapacity")
    def target_capacity(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetCapacity"))

    @target_capacity.setter
    def target_capacity(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9ad1b45bdf0d46b8247f18438ee6fb041eac910adfdfeaeb908872e0b8002aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetCapacity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EcsCapacityProviderAutoScalingGroupProviderManagedScaling]:
        return typing.cast(typing.Optional[EcsCapacityProviderAutoScalingGroupProviderManagedScaling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EcsCapacityProviderAutoScalingGroupProviderManagedScaling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52f0e4572a3a8ef9c664d724de42af387beab98d668c4de4474fcb45610d0cb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EcsCapacityProviderAutoScalingGroupProviderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ecsCapacityProvider.EcsCapacityProviderAutoScalingGroupProviderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a65009d21d48c359041b0ad6c8b66b5277bef39bdcf56d7b84929831f4a93baf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putManagedScaling")
    def put_managed_scaling(
        self,
        *,
        instance_warmup_period: typing.Optional[jsii.Number] = None,
        maximum_scaling_step_size: typing.Optional[jsii.Number] = None,
        minimum_scaling_step_size: typing.Optional[jsii.Number] = None,
        status: typing.Optional[builtins.str] = None,
        target_capacity: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param instance_warmup_period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#instance_warmup_period EcsCapacityProvider#instance_warmup_period}.
        :param maximum_scaling_step_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#maximum_scaling_step_size EcsCapacityProvider#maximum_scaling_step_size}.
        :param minimum_scaling_step_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#minimum_scaling_step_size EcsCapacityProvider#minimum_scaling_step_size}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#status EcsCapacityProvider#status}.
        :param target_capacity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#target_capacity EcsCapacityProvider#target_capacity}.
        '''
        value = EcsCapacityProviderAutoScalingGroupProviderManagedScaling(
            instance_warmup_period=instance_warmup_period,
            maximum_scaling_step_size=maximum_scaling_step_size,
            minimum_scaling_step_size=minimum_scaling_step_size,
            status=status,
            target_capacity=target_capacity,
        )

        return typing.cast(None, jsii.invoke(self, "putManagedScaling", [value]))

    @jsii.member(jsii_name="resetManagedDraining")
    def reset_managed_draining(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedDraining", []))

    @jsii.member(jsii_name="resetManagedScaling")
    def reset_managed_scaling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedScaling", []))

    @jsii.member(jsii_name="resetManagedTerminationProtection")
    def reset_managed_termination_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedTerminationProtection", []))

    @builtins.property
    @jsii.member(jsii_name="managedScaling")
    def managed_scaling(
        self,
    ) -> EcsCapacityProviderAutoScalingGroupProviderManagedScalingOutputReference:
        return typing.cast(EcsCapacityProviderAutoScalingGroupProviderManagedScalingOutputReference, jsii.get(self, "managedScaling"))

    @builtins.property
    @jsii.member(jsii_name="autoScalingGroupArnInput")
    def auto_scaling_group_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoScalingGroupArnInput"))

    @builtins.property
    @jsii.member(jsii_name="managedDrainingInput")
    def managed_draining_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managedDrainingInput"))

    @builtins.property
    @jsii.member(jsii_name="managedScalingInput")
    def managed_scaling_input(
        self,
    ) -> typing.Optional[EcsCapacityProviderAutoScalingGroupProviderManagedScaling]:
        return typing.cast(typing.Optional[EcsCapacityProviderAutoScalingGroupProviderManagedScaling], jsii.get(self, "managedScalingInput"))

    @builtins.property
    @jsii.member(jsii_name="managedTerminationProtectionInput")
    def managed_termination_protection_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managedTerminationProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="autoScalingGroupArn")
    def auto_scaling_group_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoScalingGroupArn"))

    @auto_scaling_group_arn.setter
    def auto_scaling_group_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b10e0ed8c35de902dd0b3fd7f91267d7099c20d79467bb967f9c8ef36efbd4b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoScalingGroupArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="managedDraining")
    def managed_draining(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managedDraining"))

    @managed_draining.setter
    def managed_draining(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__129ece76b9b3c5fab80a87f0fa74f84281c6e6909507d9d0aecefbf8c28d97fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedDraining", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="managedTerminationProtection")
    def managed_termination_protection(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managedTerminationProtection"))

    @managed_termination_protection.setter
    def managed_termination_protection(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87bf4f64228b4b171c4443902514addf8ef44c6b9079900312d7d6d0eb98f766)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedTerminationProtection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EcsCapacityProviderAutoScalingGroupProvider]:
        return typing.cast(typing.Optional[EcsCapacityProviderAutoScalingGroupProvider], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EcsCapacityProviderAutoScalingGroupProvider],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3465647231626f313b67cd1d547910204175a86a7fe528730e6a8659bcee889)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ecsCapacityProvider.EcsCapacityProviderConfig",
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
        "auto_scaling_group_provider": "autoScalingGroupProvider",
        "cluster": "cluster",
        "id": "id",
        "managed_instances_provider": "managedInstancesProvider",
        "region": "region",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class EcsCapacityProviderConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        auto_scaling_group_provider: typing.Optional[typing.Union[EcsCapacityProviderAutoScalingGroupProvider, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        managed_instances_provider: typing.Optional[typing.Union["EcsCapacityProviderManagedInstancesProvider", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#name EcsCapacityProvider#name}.
        :param auto_scaling_group_provider: auto_scaling_group_provider block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#auto_scaling_group_provider EcsCapacityProvider#auto_scaling_group_provider}
        :param cluster: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#cluster EcsCapacityProvider#cluster}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#id EcsCapacityProvider#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param managed_instances_provider: managed_instances_provider block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#managed_instances_provider EcsCapacityProvider#managed_instances_provider}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#region EcsCapacityProvider#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#tags EcsCapacityProvider#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#tags_all EcsCapacityProvider#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(auto_scaling_group_provider, dict):
            auto_scaling_group_provider = EcsCapacityProviderAutoScalingGroupProvider(**auto_scaling_group_provider)
        if isinstance(managed_instances_provider, dict):
            managed_instances_provider = EcsCapacityProviderManagedInstancesProvider(**managed_instances_provider)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f7825bd6e506de5febb6f3031cd2775abf009027e7e62d89ca20a4223d69734)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument auto_scaling_group_provider", value=auto_scaling_group_provider, expected_type=type_hints["auto_scaling_group_provider"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument managed_instances_provider", value=managed_instances_provider, expected_type=type_hints["managed_instances_provider"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
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
        if auto_scaling_group_provider is not None:
            self._values["auto_scaling_group_provider"] = auto_scaling_group_provider
        if cluster is not None:
            self._values["cluster"] = cluster
        if id is not None:
            self._values["id"] = id
        if managed_instances_provider is not None:
            self._values["managed_instances_provider"] = managed_instances_provider
        if region is not None:
            self._values["region"] = region
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all

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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#name EcsCapacityProvider#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_scaling_group_provider(
        self,
    ) -> typing.Optional[EcsCapacityProviderAutoScalingGroupProvider]:
        '''auto_scaling_group_provider block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#auto_scaling_group_provider EcsCapacityProvider#auto_scaling_group_provider}
        '''
        result = self._values.get("auto_scaling_group_provider")
        return typing.cast(typing.Optional[EcsCapacityProviderAutoScalingGroupProvider], result)

    @builtins.property
    def cluster(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#cluster EcsCapacityProvider#cluster}.'''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#id EcsCapacityProvider#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_instances_provider(
        self,
    ) -> typing.Optional["EcsCapacityProviderManagedInstancesProvider"]:
        '''managed_instances_provider block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#managed_instances_provider EcsCapacityProvider#managed_instances_provider}
        '''
        result = self._values.get("managed_instances_provider")
        return typing.cast(typing.Optional["EcsCapacityProviderManagedInstancesProvider"], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#region EcsCapacityProvider#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#tags EcsCapacityProvider#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#tags_all EcsCapacityProvider#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsCapacityProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ecsCapacityProvider.EcsCapacityProviderManagedInstancesProvider",
    jsii_struct_bases=[],
    name_mapping={
        "infrastructure_role_arn": "infrastructureRoleArn",
        "instance_launch_template": "instanceLaunchTemplate",
        "infrastructure_optimization": "infrastructureOptimization",
        "propagate_tags": "propagateTags",
    },
)
class EcsCapacityProviderManagedInstancesProvider:
    def __init__(
        self,
        *,
        infrastructure_role_arn: builtins.str,
        instance_launch_template: typing.Union["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplate", typing.Dict[builtins.str, typing.Any]],
        infrastructure_optimization: typing.Optional[typing.Union["EcsCapacityProviderManagedInstancesProviderInfrastructureOptimization", typing.Dict[builtins.str, typing.Any]]] = None,
        propagate_tags: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param infrastructure_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#infrastructure_role_arn EcsCapacityProvider#infrastructure_role_arn}.
        :param instance_launch_template: instance_launch_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#instance_launch_template EcsCapacityProvider#instance_launch_template}
        :param infrastructure_optimization: infrastructure_optimization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#infrastructure_optimization EcsCapacityProvider#infrastructure_optimization}
        :param propagate_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#propagate_tags EcsCapacityProvider#propagate_tags}.
        '''
        if isinstance(instance_launch_template, dict):
            instance_launch_template = EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplate(**instance_launch_template)
        if isinstance(infrastructure_optimization, dict):
            infrastructure_optimization = EcsCapacityProviderManagedInstancesProviderInfrastructureOptimization(**infrastructure_optimization)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ff67e3d8e7c6ba486856d32a9da9fb01e59d07bfc04a71d1a38469c409f7584)
            check_type(argname="argument infrastructure_role_arn", value=infrastructure_role_arn, expected_type=type_hints["infrastructure_role_arn"])
            check_type(argname="argument instance_launch_template", value=instance_launch_template, expected_type=type_hints["instance_launch_template"])
            check_type(argname="argument infrastructure_optimization", value=infrastructure_optimization, expected_type=type_hints["infrastructure_optimization"])
            check_type(argname="argument propagate_tags", value=propagate_tags, expected_type=type_hints["propagate_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "infrastructure_role_arn": infrastructure_role_arn,
            "instance_launch_template": instance_launch_template,
        }
        if infrastructure_optimization is not None:
            self._values["infrastructure_optimization"] = infrastructure_optimization
        if propagate_tags is not None:
            self._values["propagate_tags"] = propagate_tags

    @builtins.property
    def infrastructure_role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#infrastructure_role_arn EcsCapacityProvider#infrastructure_role_arn}.'''
        result = self._values.get("infrastructure_role_arn")
        assert result is not None, "Required property 'infrastructure_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_launch_template(
        self,
    ) -> "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplate":
        '''instance_launch_template block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#instance_launch_template EcsCapacityProvider#instance_launch_template}
        '''
        result = self._values.get("instance_launch_template")
        assert result is not None, "Required property 'instance_launch_template' is missing"
        return typing.cast("EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplate", result)

    @builtins.property
    def infrastructure_optimization(
        self,
    ) -> typing.Optional["EcsCapacityProviderManagedInstancesProviderInfrastructureOptimization"]:
        '''infrastructure_optimization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#infrastructure_optimization EcsCapacityProvider#infrastructure_optimization}
        '''
        result = self._values.get("infrastructure_optimization")
        return typing.cast(typing.Optional["EcsCapacityProviderManagedInstancesProviderInfrastructureOptimization"], result)

    @builtins.property
    def propagate_tags(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#propagate_tags EcsCapacityProvider#propagate_tags}.'''
        result = self._values.get("propagate_tags")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsCapacityProviderManagedInstancesProvider(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ecsCapacityProvider.EcsCapacityProviderManagedInstancesProviderInfrastructureOptimization",
    jsii_struct_bases=[],
    name_mapping={"scale_in_after": "scaleInAfter"},
)
class EcsCapacityProviderManagedInstancesProviderInfrastructureOptimization:
    def __init__(self, *, scale_in_after: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param scale_in_after: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#scale_in_after EcsCapacityProvider#scale_in_after}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__762d04c1174465946f3d933a88452bbb823b03b6f91d8c972349b74f75962b05)
            check_type(argname="argument scale_in_after", value=scale_in_after, expected_type=type_hints["scale_in_after"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if scale_in_after is not None:
            self._values["scale_in_after"] = scale_in_after

    @builtins.property
    def scale_in_after(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#scale_in_after EcsCapacityProvider#scale_in_after}.'''
        result = self._values.get("scale_in_after")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsCapacityProviderManagedInstancesProviderInfrastructureOptimization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EcsCapacityProviderManagedInstancesProviderInfrastructureOptimizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ecsCapacityProvider.EcsCapacityProviderManagedInstancesProviderInfrastructureOptimizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__88f79b01c75bded40867fbb1f29992c8adb5cebc002cd28e123fe7b9906f8dbe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetScaleInAfter")
    def reset_scale_in_after(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScaleInAfter", []))

    @builtins.property
    @jsii.member(jsii_name="scaleInAfterInput")
    def scale_in_after_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scaleInAfterInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleInAfter")
    def scale_in_after(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scaleInAfter"))

    @scale_in_after.setter
    def scale_in_after(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4396b0bdd8098ad9fa956fcc867f942c7ab5488792819a9c5b8e90a55b16e70b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleInAfter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EcsCapacityProviderManagedInstancesProviderInfrastructureOptimization]:
        return typing.cast(typing.Optional[EcsCapacityProviderManagedInstancesProviderInfrastructureOptimization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EcsCapacityProviderManagedInstancesProviderInfrastructureOptimization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1560a46fe69cdd210eb07e971e1b8c1c904f4ca510bee86f9b06f67afe6a9fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ecsCapacityProvider.EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplate",
    jsii_struct_bases=[],
    name_mapping={
        "ec2_instance_profile_arn": "ec2InstanceProfileArn",
        "network_configuration": "networkConfiguration",
        "instance_requirements": "instanceRequirements",
        "monitoring": "monitoring",
        "storage_configuration": "storageConfiguration",
    },
)
class EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplate:
    def __init__(
        self,
        *,
        ec2_instance_profile_arn: builtins.str,
        network_configuration: typing.Union["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateNetworkConfiguration", typing.Dict[builtins.str, typing.Any]],
        instance_requirements: typing.Optional[typing.Union["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirements", typing.Dict[builtins.str, typing.Any]]] = None,
        monitoring: typing.Optional[builtins.str] = None,
        storage_configuration: typing.Optional[typing.Union["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateStorageConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ec2_instance_profile_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#ec2_instance_profile_arn EcsCapacityProvider#ec2_instance_profile_arn}.
        :param network_configuration: network_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#network_configuration EcsCapacityProvider#network_configuration}
        :param instance_requirements: instance_requirements block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#instance_requirements EcsCapacityProvider#instance_requirements}
        :param monitoring: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#monitoring EcsCapacityProvider#monitoring}.
        :param storage_configuration: storage_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#storage_configuration EcsCapacityProvider#storage_configuration}
        '''
        if isinstance(network_configuration, dict):
            network_configuration = EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateNetworkConfiguration(**network_configuration)
        if isinstance(instance_requirements, dict):
            instance_requirements = EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirements(**instance_requirements)
        if isinstance(storage_configuration, dict):
            storage_configuration = EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateStorageConfiguration(**storage_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c38acd0ab05c5b80cbf9cbade9a35dd2df9693b561e856d23f16dd247c09313)
            check_type(argname="argument ec2_instance_profile_arn", value=ec2_instance_profile_arn, expected_type=type_hints["ec2_instance_profile_arn"])
            check_type(argname="argument network_configuration", value=network_configuration, expected_type=type_hints["network_configuration"])
            check_type(argname="argument instance_requirements", value=instance_requirements, expected_type=type_hints["instance_requirements"])
            check_type(argname="argument monitoring", value=monitoring, expected_type=type_hints["monitoring"])
            check_type(argname="argument storage_configuration", value=storage_configuration, expected_type=type_hints["storage_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ec2_instance_profile_arn": ec2_instance_profile_arn,
            "network_configuration": network_configuration,
        }
        if instance_requirements is not None:
            self._values["instance_requirements"] = instance_requirements
        if monitoring is not None:
            self._values["monitoring"] = monitoring
        if storage_configuration is not None:
            self._values["storage_configuration"] = storage_configuration

    @builtins.property
    def ec2_instance_profile_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#ec2_instance_profile_arn EcsCapacityProvider#ec2_instance_profile_arn}.'''
        result = self._values.get("ec2_instance_profile_arn")
        assert result is not None, "Required property 'ec2_instance_profile_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_configuration(
        self,
    ) -> "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateNetworkConfiguration":
        '''network_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#network_configuration EcsCapacityProvider#network_configuration}
        '''
        result = self._values.get("network_configuration")
        assert result is not None, "Required property 'network_configuration' is missing"
        return typing.cast("EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateNetworkConfiguration", result)

    @builtins.property
    def instance_requirements(
        self,
    ) -> typing.Optional["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirements"]:
        '''instance_requirements block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#instance_requirements EcsCapacityProvider#instance_requirements}
        '''
        result = self._values.get("instance_requirements")
        return typing.cast(typing.Optional["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirements"], result)

    @builtins.property
    def monitoring(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#monitoring EcsCapacityProvider#monitoring}.'''
        result = self._values.get("monitoring")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_configuration(
        self,
    ) -> typing.Optional["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateStorageConfiguration"]:
        '''storage_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#storage_configuration EcsCapacityProvider#storage_configuration}
        '''
        result = self._values.get("storage_configuration")
        return typing.cast(typing.Optional["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateStorageConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ecsCapacityProvider.EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirements",
    jsii_struct_bases=[],
    name_mapping={
        "memory_mib": "memoryMib",
        "vcpu_count": "vcpuCount",
        "accelerator_count": "acceleratorCount",
        "accelerator_manufacturers": "acceleratorManufacturers",
        "accelerator_names": "acceleratorNames",
        "accelerator_total_memory_mib": "acceleratorTotalMemoryMib",
        "accelerator_types": "acceleratorTypes",
        "allowed_instance_types": "allowedInstanceTypes",
        "bare_metal": "bareMetal",
        "baseline_ebs_bandwidth_mbps": "baselineEbsBandwidthMbps",
        "burstable_performance": "burstablePerformance",
        "cpu_manufacturers": "cpuManufacturers",
        "excluded_instance_types": "excludedInstanceTypes",
        "instance_generations": "instanceGenerations",
        "local_storage": "localStorage",
        "local_storage_types": "localStorageTypes",
        "max_spot_price_as_percentage_of_optimal_on_demand_price": "maxSpotPriceAsPercentageOfOptimalOnDemandPrice",
        "memory_gib_per_vcpu": "memoryGibPerVcpu",
        "network_bandwidth_gbps": "networkBandwidthGbps",
        "network_interface_count": "networkInterfaceCount",
        "on_demand_max_price_percentage_over_lowest_price": "onDemandMaxPricePercentageOverLowestPrice",
        "require_hibernate_support": "requireHibernateSupport",
        "spot_max_price_percentage_over_lowest_price": "spotMaxPricePercentageOverLowestPrice",
        "total_local_storage_gb": "totalLocalStorageGb",
    },
)
class EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirements:
    def __init__(
        self,
        *,
        memory_mib: typing.Union["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryMib", typing.Dict[builtins.str, typing.Any]],
        vcpu_count: typing.Union["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsVcpuCount", typing.Dict[builtins.str, typing.Any]],
        accelerator_count: typing.Optional[typing.Union["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorCount", typing.Dict[builtins.str, typing.Any]]] = None,
        accelerator_manufacturers: typing.Optional[typing.Sequence[builtins.str]] = None,
        accelerator_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        accelerator_total_memory_mib: typing.Optional[typing.Union["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorTotalMemoryMib", typing.Dict[builtins.str, typing.Any]]] = None,
        accelerator_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        bare_metal: typing.Optional[builtins.str] = None,
        baseline_ebs_bandwidth_mbps: typing.Optional[typing.Union["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsBaselineEbsBandwidthMbps", typing.Dict[builtins.str, typing.Any]]] = None,
        burstable_performance: typing.Optional[builtins.str] = None,
        cpu_manufacturers: typing.Optional[typing.Sequence[builtins.str]] = None,
        excluded_instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        instance_generations: typing.Optional[typing.Sequence[builtins.str]] = None,
        local_storage: typing.Optional[builtins.str] = None,
        local_storage_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_spot_price_as_percentage_of_optimal_on_demand_price: typing.Optional[jsii.Number] = None,
        memory_gib_per_vcpu: typing.Optional[typing.Union["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryGibPerVcpu", typing.Dict[builtins.str, typing.Any]]] = None,
        network_bandwidth_gbps: typing.Optional[typing.Union["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkBandwidthGbps", typing.Dict[builtins.str, typing.Any]]] = None,
        network_interface_count: typing.Optional[typing.Union["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkInterfaceCount", typing.Dict[builtins.str, typing.Any]]] = None,
        on_demand_max_price_percentage_over_lowest_price: typing.Optional[jsii.Number] = None,
        require_hibernate_support: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        spot_max_price_percentage_over_lowest_price: typing.Optional[jsii.Number] = None,
        total_local_storage_gb: typing.Optional[typing.Union["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsTotalLocalStorageGb", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param memory_mib: memory_mib block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#memory_mib EcsCapacityProvider#memory_mib}
        :param vcpu_count: vcpu_count block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#vcpu_count EcsCapacityProvider#vcpu_count}
        :param accelerator_count: accelerator_count block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#accelerator_count EcsCapacityProvider#accelerator_count}
        :param accelerator_manufacturers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#accelerator_manufacturers EcsCapacityProvider#accelerator_manufacturers}.
        :param accelerator_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#accelerator_names EcsCapacityProvider#accelerator_names}.
        :param accelerator_total_memory_mib: accelerator_total_memory_mib block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#accelerator_total_memory_mib EcsCapacityProvider#accelerator_total_memory_mib}
        :param accelerator_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#accelerator_types EcsCapacityProvider#accelerator_types}.
        :param allowed_instance_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#allowed_instance_types EcsCapacityProvider#allowed_instance_types}.
        :param bare_metal: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#bare_metal EcsCapacityProvider#bare_metal}.
        :param baseline_ebs_bandwidth_mbps: baseline_ebs_bandwidth_mbps block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#baseline_ebs_bandwidth_mbps EcsCapacityProvider#baseline_ebs_bandwidth_mbps}
        :param burstable_performance: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#burstable_performance EcsCapacityProvider#burstable_performance}.
        :param cpu_manufacturers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#cpu_manufacturers EcsCapacityProvider#cpu_manufacturers}.
        :param excluded_instance_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#excluded_instance_types EcsCapacityProvider#excluded_instance_types}.
        :param instance_generations: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#instance_generations EcsCapacityProvider#instance_generations}.
        :param local_storage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#local_storage EcsCapacityProvider#local_storage}.
        :param local_storage_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#local_storage_types EcsCapacityProvider#local_storage_types}.
        :param max_spot_price_as_percentage_of_optimal_on_demand_price: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#max_spot_price_as_percentage_of_optimal_on_demand_price EcsCapacityProvider#max_spot_price_as_percentage_of_optimal_on_demand_price}.
        :param memory_gib_per_vcpu: memory_gib_per_vcpu block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#memory_gib_per_vcpu EcsCapacityProvider#memory_gib_per_vcpu}
        :param network_bandwidth_gbps: network_bandwidth_gbps block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#network_bandwidth_gbps EcsCapacityProvider#network_bandwidth_gbps}
        :param network_interface_count: network_interface_count block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#network_interface_count EcsCapacityProvider#network_interface_count}
        :param on_demand_max_price_percentage_over_lowest_price: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#on_demand_max_price_percentage_over_lowest_price EcsCapacityProvider#on_demand_max_price_percentage_over_lowest_price}.
        :param require_hibernate_support: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#require_hibernate_support EcsCapacityProvider#require_hibernate_support}.
        :param spot_max_price_percentage_over_lowest_price: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#spot_max_price_percentage_over_lowest_price EcsCapacityProvider#spot_max_price_percentage_over_lowest_price}.
        :param total_local_storage_gb: total_local_storage_gb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#total_local_storage_gb EcsCapacityProvider#total_local_storage_gb}
        '''
        if isinstance(memory_mib, dict):
            memory_mib = EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryMib(**memory_mib)
        if isinstance(vcpu_count, dict):
            vcpu_count = EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsVcpuCount(**vcpu_count)
        if isinstance(accelerator_count, dict):
            accelerator_count = EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorCount(**accelerator_count)
        if isinstance(accelerator_total_memory_mib, dict):
            accelerator_total_memory_mib = EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorTotalMemoryMib(**accelerator_total_memory_mib)
        if isinstance(baseline_ebs_bandwidth_mbps, dict):
            baseline_ebs_bandwidth_mbps = EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsBaselineEbsBandwidthMbps(**baseline_ebs_bandwidth_mbps)
        if isinstance(memory_gib_per_vcpu, dict):
            memory_gib_per_vcpu = EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryGibPerVcpu(**memory_gib_per_vcpu)
        if isinstance(network_bandwidth_gbps, dict):
            network_bandwidth_gbps = EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkBandwidthGbps(**network_bandwidth_gbps)
        if isinstance(network_interface_count, dict):
            network_interface_count = EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkInterfaceCount(**network_interface_count)
        if isinstance(total_local_storage_gb, dict):
            total_local_storage_gb = EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsTotalLocalStorageGb(**total_local_storage_gb)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dba9a05eace9f830f932846ce21f33d8ffc562ba825477521917ce9f7f28e072)
            check_type(argname="argument memory_mib", value=memory_mib, expected_type=type_hints["memory_mib"])
            check_type(argname="argument vcpu_count", value=vcpu_count, expected_type=type_hints["vcpu_count"])
            check_type(argname="argument accelerator_count", value=accelerator_count, expected_type=type_hints["accelerator_count"])
            check_type(argname="argument accelerator_manufacturers", value=accelerator_manufacturers, expected_type=type_hints["accelerator_manufacturers"])
            check_type(argname="argument accelerator_names", value=accelerator_names, expected_type=type_hints["accelerator_names"])
            check_type(argname="argument accelerator_total_memory_mib", value=accelerator_total_memory_mib, expected_type=type_hints["accelerator_total_memory_mib"])
            check_type(argname="argument accelerator_types", value=accelerator_types, expected_type=type_hints["accelerator_types"])
            check_type(argname="argument allowed_instance_types", value=allowed_instance_types, expected_type=type_hints["allowed_instance_types"])
            check_type(argname="argument bare_metal", value=bare_metal, expected_type=type_hints["bare_metal"])
            check_type(argname="argument baseline_ebs_bandwidth_mbps", value=baseline_ebs_bandwidth_mbps, expected_type=type_hints["baseline_ebs_bandwidth_mbps"])
            check_type(argname="argument burstable_performance", value=burstable_performance, expected_type=type_hints["burstable_performance"])
            check_type(argname="argument cpu_manufacturers", value=cpu_manufacturers, expected_type=type_hints["cpu_manufacturers"])
            check_type(argname="argument excluded_instance_types", value=excluded_instance_types, expected_type=type_hints["excluded_instance_types"])
            check_type(argname="argument instance_generations", value=instance_generations, expected_type=type_hints["instance_generations"])
            check_type(argname="argument local_storage", value=local_storage, expected_type=type_hints["local_storage"])
            check_type(argname="argument local_storage_types", value=local_storage_types, expected_type=type_hints["local_storage_types"])
            check_type(argname="argument max_spot_price_as_percentage_of_optimal_on_demand_price", value=max_spot_price_as_percentage_of_optimal_on_demand_price, expected_type=type_hints["max_spot_price_as_percentage_of_optimal_on_demand_price"])
            check_type(argname="argument memory_gib_per_vcpu", value=memory_gib_per_vcpu, expected_type=type_hints["memory_gib_per_vcpu"])
            check_type(argname="argument network_bandwidth_gbps", value=network_bandwidth_gbps, expected_type=type_hints["network_bandwidth_gbps"])
            check_type(argname="argument network_interface_count", value=network_interface_count, expected_type=type_hints["network_interface_count"])
            check_type(argname="argument on_demand_max_price_percentage_over_lowest_price", value=on_demand_max_price_percentage_over_lowest_price, expected_type=type_hints["on_demand_max_price_percentage_over_lowest_price"])
            check_type(argname="argument require_hibernate_support", value=require_hibernate_support, expected_type=type_hints["require_hibernate_support"])
            check_type(argname="argument spot_max_price_percentage_over_lowest_price", value=spot_max_price_percentage_over_lowest_price, expected_type=type_hints["spot_max_price_percentage_over_lowest_price"])
            check_type(argname="argument total_local_storage_gb", value=total_local_storage_gb, expected_type=type_hints["total_local_storage_gb"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "memory_mib": memory_mib,
            "vcpu_count": vcpu_count,
        }
        if accelerator_count is not None:
            self._values["accelerator_count"] = accelerator_count
        if accelerator_manufacturers is not None:
            self._values["accelerator_manufacturers"] = accelerator_manufacturers
        if accelerator_names is not None:
            self._values["accelerator_names"] = accelerator_names
        if accelerator_total_memory_mib is not None:
            self._values["accelerator_total_memory_mib"] = accelerator_total_memory_mib
        if accelerator_types is not None:
            self._values["accelerator_types"] = accelerator_types
        if allowed_instance_types is not None:
            self._values["allowed_instance_types"] = allowed_instance_types
        if bare_metal is not None:
            self._values["bare_metal"] = bare_metal
        if baseline_ebs_bandwidth_mbps is not None:
            self._values["baseline_ebs_bandwidth_mbps"] = baseline_ebs_bandwidth_mbps
        if burstable_performance is not None:
            self._values["burstable_performance"] = burstable_performance
        if cpu_manufacturers is not None:
            self._values["cpu_manufacturers"] = cpu_manufacturers
        if excluded_instance_types is not None:
            self._values["excluded_instance_types"] = excluded_instance_types
        if instance_generations is not None:
            self._values["instance_generations"] = instance_generations
        if local_storage is not None:
            self._values["local_storage"] = local_storage
        if local_storage_types is not None:
            self._values["local_storage_types"] = local_storage_types
        if max_spot_price_as_percentage_of_optimal_on_demand_price is not None:
            self._values["max_spot_price_as_percentage_of_optimal_on_demand_price"] = max_spot_price_as_percentage_of_optimal_on_demand_price
        if memory_gib_per_vcpu is not None:
            self._values["memory_gib_per_vcpu"] = memory_gib_per_vcpu
        if network_bandwidth_gbps is not None:
            self._values["network_bandwidth_gbps"] = network_bandwidth_gbps
        if network_interface_count is not None:
            self._values["network_interface_count"] = network_interface_count
        if on_demand_max_price_percentage_over_lowest_price is not None:
            self._values["on_demand_max_price_percentage_over_lowest_price"] = on_demand_max_price_percentage_over_lowest_price
        if require_hibernate_support is not None:
            self._values["require_hibernate_support"] = require_hibernate_support
        if spot_max_price_percentage_over_lowest_price is not None:
            self._values["spot_max_price_percentage_over_lowest_price"] = spot_max_price_percentage_over_lowest_price
        if total_local_storage_gb is not None:
            self._values["total_local_storage_gb"] = total_local_storage_gb

    @builtins.property
    def memory_mib(
        self,
    ) -> "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryMib":
        '''memory_mib block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#memory_mib EcsCapacityProvider#memory_mib}
        '''
        result = self._values.get("memory_mib")
        assert result is not None, "Required property 'memory_mib' is missing"
        return typing.cast("EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryMib", result)

    @builtins.property
    def vcpu_count(
        self,
    ) -> "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsVcpuCount":
        '''vcpu_count block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#vcpu_count EcsCapacityProvider#vcpu_count}
        '''
        result = self._values.get("vcpu_count")
        assert result is not None, "Required property 'vcpu_count' is missing"
        return typing.cast("EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsVcpuCount", result)

    @builtins.property
    def accelerator_count(
        self,
    ) -> typing.Optional["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorCount"]:
        '''accelerator_count block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#accelerator_count EcsCapacityProvider#accelerator_count}
        '''
        result = self._values.get("accelerator_count")
        return typing.cast(typing.Optional["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorCount"], result)

    @builtins.property
    def accelerator_manufacturers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#accelerator_manufacturers EcsCapacityProvider#accelerator_manufacturers}.'''
        result = self._values.get("accelerator_manufacturers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def accelerator_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#accelerator_names EcsCapacityProvider#accelerator_names}.'''
        result = self._values.get("accelerator_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def accelerator_total_memory_mib(
        self,
    ) -> typing.Optional["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorTotalMemoryMib"]:
        '''accelerator_total_memory_mib block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#accelerator_total_memory_mib EcsCapacityProvider#accelerator_total_memory_mib}
        '''
        result = self._values.get("accelerator_total_memory_mib")
        return typing.cast(typing.Optional["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorTotalMemoryMib"], result)

    @builtins.property
    def accelerator_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#accelerator_types EcsCapacityProvider#accelerator_types}.'''
        result = self._values.get("accelerator_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allowed_instance_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#allowed_instance_types EcsCapacityProvider#allowed_instance_types}.'''
        result = self._values.get("allowed_instance_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def bare_metal(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#bare_metal EcsCapacityProvider#bare_metal}.'''
        result = self._values.get("bare_metal")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def baseline_ebs_bandwidth_mbps(
        self,
    ) -> typing.Optional["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsBaselineEbsBandwidthMbps"]:
        '''baseline_ebs_bandwidth_mbps block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#baseline_ebs_bandwidth_mbps EcsCapacityProvider#baseline_ebs_bandwidth_mbps}
        '''
        result = self._values.get("baseline_ebs_bandwidth_mbps")
        return typing.cast(typing.Optional["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsBaselineEbsBandwidthMbps"], result)

    @builtins.property
    def burstable_performance(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#burstable_performance EcsCapacityProvider#burstable_performance}.'''
        result = self._values.get("burstable_performance")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu_manufacturers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#cpu_manufacturers EcsCapacityProvider#cpu_manufacturers}.'''
        result = self._values.get("cpu_manufacturers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def excluded_instance_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#excluded_instance_types EcsCapacityProvider#excluded_instance_types}.'''
        result = self._values.get("excluded_instance_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def instance_generations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#instance_generations EcsCapacityProvider#instance_generations}.'''
        result = self._values.get("instance_generations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def local_storage(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#local_storage EcsCapacityProvider#local_storage}.'''
        result = self._values.get("local_storage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_storage_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#local_storage_types EcsCapacityProvider#local_storage_types}.'''
        result = self._values.get("local_storage_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def max_spot_price_as_percentage_of_optimal_on_demand_price(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#max_spot_price_as_percentage_of_optimal_on_demand_price EcsCapacityProvider#max_spot_price_as_percentage_of_optimal_on_demand_price}.'''
        result = self._values.get("max_spot_price_as_percentage_of_optimal_on_demand_price")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_gib_per_vcpu(
        self,
    ) -> typing.Optional["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryGibPerVcpu"]:
        '''memory_gib_per_vcpu block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#memory_gib_per_vcpu EcsCapacityProvider#memory_gib_per_vcpu}
        '''
        result = self._values.get("memory_gib_per_vcpu")
        return typing.cast(typing.Optional["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryGibPerVcpu"], result)

    @builtins.property
    def network_bandwidth_gbps(
        self,
    ) -> typing.Optional["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkBandwidthGbps"]:
        '''network_bandwidth_gbps block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#network_bandwidth_gbps EcsCapacityProvider#network_bandwidth_gbps}
        '''
        result = self._values.get("network_bandwidth_gbps")
        return typing.cast(typing.Optional["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkBandwidthGbps"], result)

    @builtins.property
    def network_interface_count(
        self,
    ) -> typing.Optional["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkInterfaceCount"]:
        '''network_interface_count block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#network_interface_count EcsCapacityProvider#network_interface_count}
        '''
        result = self._values.get("network_interface_count")
        return typing.cast(typing.Optional["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkInterfaceCount"], result)

    @builtins.property
    def on_demand_max_price_percentage_over_lowest_price(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#on_demand_max_price_percentage_over_lowest_price EcsCapacityProvider#on_demand_max_price_percentage_over_lowest_price}.'''
        result = self._values.get("on_demand_max_price_percentage_over_lowest_price")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def require_hibernate_support(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#require_hibernate_support EcsCapacityProvider#require_hibernate_support}.'''
        result = self._values.get("require_hibernate_support")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def spot_max_price_percentage_over_lowest_price(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#spot_max_price_percentage_over_lowest_price EcsCapacityProvider#spot_max_price_percentage_over_lowest_price}.'''
        result = self._values.get("spot_max_price_percentage_over_lowest_price")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def total_local_storage_gb(
        self,
    ) -> typing.Optional["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsTotalLocalStorageGb"]:
        '''total_local_storage_gb block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#total_local_storage_gb EcsCapacityProvider#total_local_storage_gb}
        '''
        result = self._values.get("total_local_storage_gb")
        return typing.cast(typing.Optional["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsTotalLocalStorageGb"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirements(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ecsCapacityProvider.EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorCount",
    jsii_struct_bases=[],
    name_mapping={"max": "max", "min": "min"},
)
class EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorCount:
    def __init__(
        self,
        *,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#max EcsCapacityProvider#max}.
        :param min: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#min EcsCapacityProvider#min}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fc2e2db80ab936900e89f399d127bc6f2db9141715c8a27627f525da80e9703)
            check_type(argname="argument max", value=max, expected_type=type_hints["max"])
            check_type(argname="argument min", value=min, expected_type=type_hints["min"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max is not None:
            self._values["max"] = max
        if min is not None:
            self._values["min"] = min

    @builtins.property
    def max(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#max EcsCapacityProvider#max}.'''
        result = self._values.get("max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#min EcsCapacityProvider#min}.'''
        result = self._values.get("min")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorCount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorCountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ecsCapacityProvider.EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorCountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c398b01eb8a3793e3a05677ba271081a559ed4aab27a96a6b8d04c4fe691e37d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMax")
    def reset_max(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMax", []))

    @jsii.member(jsii_name="resetMin")
    def reset_min(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMin", []))

    @builtins.property
    @jsii.member(jsii_name="maxInput")
    def max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInput"))

    @builtins.property
    @jsii.member(jsii_name="minInput")
    def min_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minInput"))

    @builtins.property
    @jsii.member(jsii_name="max")
    def max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "max"))

    @max.setter
    def max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d22ac9e7144535e1feae157e3de7a1cf817a70c30bfb973f8727bd287aee1df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "max", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="min")
    def min(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "min"))

    @min.setter
    def min(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd4e5006e9a497dc89518d2b9358cf126f5b66adeb05aae1398eaba9a64d5301)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "min", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorCount]:
        return typing.cast(typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorCount], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorCount],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21d58051bbfd6e375f3f2b0f2e41ab72ade1a2f4ab504efd83ac1afb3ede1cf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ecsCapacityProvider.EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorTotalMemoryMib",
    jsii_struct_bases=[],
    name_mapping={"max": "max", "min": "min"},
)
class EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorTotalMemoryMib:
    def __init__(
        self,
        *,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#max EcsCapacityProvider#max}.
        :param min: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#min EcsCapacityProvider#min}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d6921dc97e3372977efe5ca7210a816f8b69fad31672fe4fb9a42971eb4f291)
            check_type(argname="argument max", value=max, expected_type=type_hints["max"])
            check_type(argname="argument min", value=min, expected_type=type_hints["min"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max is not None:
            self._values["max"] = max
        if min is not None:
            self._values["min"] = min

    @builtins.property
    def max(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#max EcsCapacityProvider#max}.'''
        result = self._values.get("max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#min EcsCapacityProvider#min}.'''
        result = self._values.get("min")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorTotalMemoryMib(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorTotalMemoryMibOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ecsCapacityProvider.EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorTotalMemoryMibOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c6bbd504db7a896fb6ded2dd79e0c12be2f5758c4f85e1708cc17c2f2c42226)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMax")
    def reset_max(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMax", []))

    @jsii.member(jsii_name="resetMin")
    def reset_min(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMin", []))

    @builtins.property
    @jsii.member(jsii_name="maxInput")
    def max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInput"))

    @builtins.property
    @jsii.member(jsii_name="minInput")
    def min_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minInput"))

    @builtins.property
    @jsii.member(jsii_name="max")
    def max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "max"))

    @max.setter
    def max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f542231d03fcd974dc7aba200ce10b1c84e73aa13139209bc73c5b3bc30cf33e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "max", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="min")
    def min(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "min"))

    @min.setter
    def min(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26371a43f5e7845939acafc61b0d35f0c28ca0314b105409775913317288cc2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "min", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorTotalMemoryMib]:
        return typing.cast(typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorTotalMemoryMib], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorTotalMemoryMib],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2934502a4e6eec57c1c848b969cc9811aa6471e790fc170c86b3e4bbb78aa0b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ecsCapacityProvider.EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsBaselineEbsBandwidthMbps",
    jsii_struct_bases=[],
    name_mapping={"max": "max", "min": "min"},
)
class EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsBaselineEbsBandwidthMbps:
    def __init__(
        self,
        *,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#max EcsCapacityProvider#max}.
        :param min: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#min EcsCapacityProvider#min}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfc1141436a18faa21e805273af12061da8063e284f40a21dff92cc31656b86f)
            check_type(argname="argument max", value=max, expected_type=type_hints["max"])
            check_type(argname="argument min", value=min, expected_type=type_hints["min"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max is not None:
            self._values["max"] = max
        if min is not None:
            self._values["min"] = min

    @builtins.property
    def max(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#max EcsCapacityProvider#max}.'''
        result = self._values.get("max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#min EcsCapacityProvider#min}.'''
        result = self._values.get("min")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsBaselineEbsBandwidthMbps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsBaselineEbsBandwidthMbpsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ecsCapacityProvider.EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsBaselineEbsBandwidthMbpsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__821feb9ed75a2532bfab4c43b387a206215c7dc8f7e0b022e0b428c0dd1f1dc8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMax")
    def reset_max(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMax", []))

    @jsii.member(jsii_name="resetMin")
    def reset_min(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMin", []))

    @builtins.property
    @jsii.member(jsii_name="maxInput")
    def max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInput"))

    @builtins.property
    @jsii.member(jsii_name="minInput")
    def min_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minInput"))

    @builtins.property
    @jsii.member(jsii_name="max")
    def max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "max"))

    @max.setter
    def max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a32aeec5ddbd807b84eb4f1bec0a901f74944f038ad908d35312b84ad37dcffc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "max", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="min")
    def min(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "min"))

    @min.setter
    def min(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d4fa03cfc29a7d92241f28a8cc52d6ff0b71a2b74051266d5dc6222ba5abfb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "min", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsBaselineEbsBandwidthMbps]:
        return typing.cast(typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsBaselineEbsBandwidthMbps], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsBaselineEbsBandwidthMbps],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb677a218b5a287367835a9981ea8549500fab3ab66f838ba43e1dcb2b09b56e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ecsCapacityProvider.EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryGibPerVcpu",
    jsii_struct_bases=[],
    name_mapping={"max": "max", "min": "min"},
)
class EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryGibPerVcpu:
    def __init__(
        self,
        *,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#max EcsCapacityProvider#max}.
        :param min: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#min EcsCapacityProvider#min}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07f29562b56306ce48de558c8c865c07b70fd9cfbed342caa046cb360ed1b3e0)
            check_type(argname="argument max", value=max, expected_type=type_hints["max"])
            check_type(argname="argument min", value=min, expected_type=type_hints["min"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max is not None:
            self._values["max"] = max
        if min is not None:
            self._values["min"] = min

    @builtins.property
    def max(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#max EcsCapacityProvider#max}.'''
        result = self._values.get("max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#min EcsCapacityProvider#min}.'''
        result = self._values.get("min")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryGibPerVcpu(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryGibPerVcpuOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ecsCapacityProvider.EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryGibPerVcpuOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a670a40d91564fe67235630de19aa7d4a30d236087135426b5b021dd470cbf0f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMax")
    def reset_max(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMax", []))

    @jsii.member(jsii_name="resetMin")
    def reset_min(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMin", []))

    @builtins.property
    @jsii.member(jsii_name="maxInput")
    def max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInput"))

    @builtins.property
    @jsii.member(jsii_name="minInput")
    def min_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minInput"))

    @builtins.property
    @jsii.member(jsii_name="max")
    def max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "max"))

    @max.setter
    def max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__181941a5ba3683311863c38bf78988ff6d871a1001a005dbe76cfdcd9d314d07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "max", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="min")
    def min(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "min"))

    @min.setter
    def min(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f67582e54d090781b8bd18e9c69d52437f31cbe6de42ebdb6779e205cf77721)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "min", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryGibPerVcpu]:
        return typing.cast(typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryGibPerVcpu], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryGibPerVcpu],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34452b0a3600302473035476ff5345164d30841efaa690fe4bd4187fcff1c27b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ecsCapacityProvider.EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryMib",
    jsii_struct_bases=[],
    name_mapping={"min": "min", "max": "max"},
)
class EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryMib:
    def __init__(
        self,
        *,
        min: jsii.Number,
        max: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param min: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#min EcsCapacityProvider#min}.
        :param max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#max EcsCapacityProvider#max}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dff2390a950f57403298193f518f81f22f1e37044132107afbec470e076c9dbf)
            check_type(argname="argument min", value=min, expected_type=type_hints["min"])
            check_type(argname="argument max", value=max, expected_type=type_hints["max"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "min": min,
        }
        if max is not None:
            self._values["max"] = max

    @builtins.property
    def min(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#min EcsCapacityProvider#min}.'''
        result = self._values.get("min")
        assert result is not None, "Required property 'min' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def max(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#max EcsCapacityProvider#max}.'''
        result = self._values.get("max")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryMib(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryMibOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ecsCapacityProvider.EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryMibOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b5f35870f1da6e103d67b04d11931f19a8895b4d614b8af706723c0f2096c0e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMax")
    def reset_max(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMax", []))

    @builtins.property
    @jsii.member(jsii_name="maxInput")
    def max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInput"))

    @builtins.property
    @jsii.member(jsii_name="minInput")
    def min_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minInput"))

    @builtins.property
    @jsii.member(jsii_name="max")
    def max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "max"))

    @max.setter
    def max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b2e611baf423c23db945f438d3a6d44fbca231e3f15982307359ff30ca0bd95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "max", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="min")
    def min(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "min"))

    @min.setter
    def min(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31bb47bfb24cdf0b16e31e6b1c35cb05b6950996c8d3d6719dd4f4368cf1abe0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "min", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryMib]:
        return typing.cast(typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryMib], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryMib],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99c4bd79c52b66a678a6a393edcb24c9a85eb13b3dbdde795dc2d5eb13d95a42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ecsCapacityProvider.EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkBandwidthGbps",
    jsii_struct_bases=[],
    name_mapping={"max": "max", "min": "min"},
)
class EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkBandwidthGbps:
    def __init__(
        self,
        *,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#max EcsCapacityProvider#max}.
        :param min: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#min EcsCapacityProvider#min}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7be8a679ff022aaa01cfc4e7a71a00d2363b224f610c898ec7996d387fd2068)
            check_type(argname="argument max", value=max, expected_type=type_hints["max"])
            check_type(argname="argument min", value=min, expected_type=type_hints["min"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max is not None:
            self._values["max"] = max
        if min is not None:
            self._values["min"] = min

    @builtins.property
    def max(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#max EcsCapacityProvider#max}.'''
        result = self._values.get("max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#min EcsCapacityProvider#min}.'''
        result = self._values.get("min")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkBandwidthGbps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkBandwidthGbpsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ecsCapacityProvider.EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkBandwidthGbpsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c177a1614b013172efbc02438bbedf6685f92c276cf83ba361bbc630300575f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMax")
    def reset_max(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMax", []))

    @jsii.member(jsii_name="resetMin")
    def reset_min(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMin", []))

    @builtins.property
    @jsii.member(jsii_name="maxInput")
    def max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInput"))

    @builtins.property
    @jsii.member(jsii_name="minInput")
    def min_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minInput"))

    @builtins.property
    @jsii.member(jsii_name="max")
    def max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "max"))

    @max.setter
    def max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdf5bfdf245d7a6568ed1534429d932da04e43b70a929356a13d2e2be6e89d95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "max", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="min")
    def min(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "min"))

    @min.setter
    def min(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9fb0c764f58b69fcfa702ec9c35deec25ae701a876cd6c118cc4a84265f4a6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "min", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkBandwidthGbps]:
        return typing.cast(typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkBandwidthGbps], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkBandwidthGbps],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80364ca30661a260db6d8c16621c80c6f1f5f3bb54ee27716a96fa6c6fbf90f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ecsCapacityProvider.EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkInterfaceCount",
    jsii_struct_bases=[],
    name_mapping={"max": "max", "min": "min"},
)
class EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkInterfaceCount:
    def __init__(
        self,
        *,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#max EcsCapacityProvider#max}.
        :param min: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#min EcsCapacityProvider#min}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f86c1f14860f34f13e17c06d1a96e87fca3ffa174fd4cebff0ac7700232309b)
            check_type(argname="argument max", value=max, expected_type=type_hints["max"])
            check_type(argname="argument min", value=min, expected_type=type_hints["min"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max is not None:
            self._values["max"] = max
        if min is not None:
            self._values["min"] = min

    @builtins.property
    def max(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#max EcsCapacityProvider#max}.'''
        result = self._values.get("max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#min EcsCapacityProvider#min}.'''
        result = self._values.get("min")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkInterfaceCount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkInterfaceCountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ecsCapacityProvider.EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkInterfaceCountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81e9d579b60a209045a8ca9890d2b3e56252ccbba743f5b8d6e618d81b754e9d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMax")
    def reset_max(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMax", []))

    @jsii.member(jsii_name="resetMin")
    def reset_min(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMin", []))

    @builtins.property
    @jsii.member(jsii_name="maxInput")
    def max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInput"))

    @builtins.property
    @jsii.member(jsii_name="minInput")
    def min_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minInput"))

    @builtins.property
    @jsii.member(jsii_name="max")
    def max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "max"))

    @max.setter
    def max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a98bfb532ac715c63696328b5b93ba5e5dee69bd126c0d5656ce6bdb97f298a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "max", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="min")
    def min(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "min"))

    @min.setter
    def min(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56330915157340e0259d61105ae3ec9ff9c841bcc1942849c374cc4f996dd55e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "min", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkInterfaceCount]:
        return typing.cast(typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkInterfaceCount], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkInterfaceCount],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__021f76a03625da2163cf518a61971a4b4f2c5277d935abbd37de721aef77674b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ecsCapacityProvider.EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3866b4b5166d923ef52c2b33d476d80b02d7986492280c654ad258df582e0442)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAcceleratorCount")
    def put_accelerator_count(
        self,
        *,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#max EcsCapacityProvider#max}.
        :param min: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#min EcsCapacityProvider#min}.
        '''
        value = EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorCount(
            max=max, min=min
        )

        return typing.cast(None, jsii.invoke(self, "putAcceleratorCount", [value]))

    @jsii.member(jsii_name="putAcceleratorTotalMemoryMib")
    def put_accelerator_total_memory_mib(
        self,
        *,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#max EcsCapacityProvider#max}.
        :param min: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#min EcsCapacityProvider#min}.
        '''
        value = EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorTotalMemoryMib(
            max=max, min=min
        )

        return typing.cast(None, jsii.invoke(self, "putAcceleratorTotalMemoryMib", [value]))

    @jsii.member(jsii_name="putBaselineEbsBandwidthMbps")
    def put_baseline_ebs_bandwidth_mbps(
        self,
        *,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#max EcsCapacityProvider#max}.
        :param min: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#min EcsCapacityProvider#min}.
        '''
        value = EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsBaselineEbsBandwidthMbps(
            max=max, min=min
        )

        return typing.cast(None, jsii.invoke(self, "putBaselineEbsBandwidthMbps", [value]))

    @jsii.member(jsii_name="putMemoryGibPerVcpu")
    def put_memory_gib_per_vcpu(
        self,
        *,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#max EcsCapacityProvider#max}.
        :param min: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#min EcsCapacityProvider#min}.
        '''
        value = EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryGibPerVcpu(
            max=max, min=min
        )

        return typing.cast(None, jsii.invoke(self, "putMemoryGibPerVcpu", [value]))

    @jsii.member(jsii_name="putMemoryMib")
    def put_memory_mib(
        self,
        *,
        min: jsii.Number,
        max: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param min: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#min EcsCapacityProvider#min}.
        :param max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#max EcsCapacityProvider#max}.
        '''
        value = EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryMib(
            min=min, max=max
        )

        return typing.cast(None, jsii.invoke(self, "putMemoryMib", [value]))

    @jsii.member(jsii_name="putNetworkBandwidthGbps")
    def put_network_bandwidth_gbps(
        self,
        *,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#max EcsCapacityProvider#max}.
        :param min: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#min EcsCapacityProvider#min}.
        '''
        value = EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkBandwidthGbps(
            max=max, min=min
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkBandwidthGbps", [value]))

    @jsii.member(jsii_name="putNetworkInterfaceCount")
    def put_network_interface_count(
        self,
        *,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#max EcsCapacityProvider#max}.
        :param min: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#min EcsCapacityProvider#min}.
        '''
        value = EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkInterfaceCount(
            max=max, min=min
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkInterfaceCount", [value]))

    @jsii.member(jsii_name="putTotalLocalStorageGb")
    def put_total_local_storage_gb(
        self,
        *,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#max EcsCapacityProvider#max}.
        :param min: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#min EcsCapacityProvider#min}.
        '''
        value = EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsTotalLocalStorageGb(
            max=max, min=min
        )

        return typing.cast(None, jsii.invoke(self, "putTotalLocalStorageGb", [value]))

    @jsii.member(jsii_name="putVcpuCount")
    def put_vcpu_count(
        self,
        *,
        min: jsii.Number,
        max: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param min: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#min EcsCapacityProvider#min}.
        :param max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#max EcsCapacityProvider#max}.
        '''
        value = EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsVcpuCount(
            min=min, max=max
        )

        return typing.cast(None, jsii.invoke(self, "putVcpuCount", [value]))

    @jsii.member(jsii_name="resetAcceleratorCount")
    def reset_accelerator_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceleratorCount", []))

    @jsii.member(jsii_name="resetAcceleratorManufacturers")
    def reset_accelerator_manufacturers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceleratorManufacturers", []))

    @jsii.member(jsii_name="resetAcceleratorNames")
    def reset_accelerator_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceleratorNames", []))

    @jsii.member(jsii_name="resetAcceleratorTotalMemoryMib")
    def reset_accelerator_total_memory_mib(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceleratorTotalMemoryMib", []))

    @jsii.member(jsii_name="resetAcceleratorTypes")
    def reset_accelerator_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceleratorTypes", []))

    @jsii.member(jsii_name="resetAllowedInstanceTypes")
    def reset_allowed_instance_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedInstanceTypes", []))

    @jsii.member(jsii_name="resetBareMetal")
    def reset_bare_metal(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBareMetal", []))

    @jsii.member(jsii_name="resetBaselineEbsBandwidthMbps")
    def reset_baseline_ebs_bandwidth_mbps(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBaselineEbsBandwidthMbps", []))

    @jsii.member(jsii_name="resetBurstablePerformance")
    def reset_burstable_performance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBurstablePerformance", []))

    @jsii.member(jsii_name="resetCpuManufacturers")
    def reset_cpu_manufacturers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuManufacturers", []))

    @jsii.member(jsii_name="resetExcludedInstanceTypes")
    def reset_excluded_instance_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedInstanceTypes", []))

    @jsii.member(jsii_name="resetInstanceGenerations")
    def reset_instance_generations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceGenerations", []))

    @jsii.member(jsii_name="resetLocalStorage")
    def reset_local_storage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalStorage", []))

    @jsii.member(jsii_name="resetLocalStorageTypes")
    def reset_local_storage_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalStorageTypes", []))

    @jsii.member(jsii_name="resetMaxSpotPriceAsPercentageOfOptimalOnDemandPrice")
    def reset_max_spot_price_as_percentage_of_optimal_on_demand_price(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxSpotPriceAsPercentageOfOptimalOnDemandPrice", []))

    @jsii.member(jsii_name="resetMemoryGibPerVcpu")
    def reset_memory_gib_per_vcpu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemoryGibPerVcpu", []))

    @jsii.member(jsii_name="resetNetworkBandwidthGbps")
    def reset_network_bandwidth_gbps(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkBandwidthGbps", []))

    @jsii.member(jsii_name="resetNetworkInterfaceCount")
    def reset_network_interface_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkInterfaceCount", []))

    @jsii.member(jsii_name="resetOnDemandMaxPricePercentageOverLowestPrice")
    def reset_on_demand_max_price_percentage_over_lowest_price(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnDemandMaxPricePercentageOverLowestPrice", []))

    @jsii.member(jsii_name="resetRequireHibernateSupport")
    def reset_require_hibernate_support(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireHibernateSupport", []))

    @jsii.member(jsii_name="resetSpotMaxPricePercentageOverLowestPrice")
    def reset_spot_max_price_percentage_over_lowest_price(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpotMaxPricePercentageOverLowestPrice", []))

    @jsii.member(jsii_name="resetTotalLocalStorageGb")
    def reset_total_local_storage_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTotalLocalStorageGb", []))

    @builtins.property
    @jsii.member(jsii_name="acceleratorCount")
    def accelerator_count(
        self,
    ) -> EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorCountOutputReference:
        return typing.cast(EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorCountOutputReference, jsii.get(self, "acceleratorCount"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorTotalMemoryMib")
    def accelerator_total_memory_mib(
        self,
    ) -> EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorTotalMemoryMibOutputReference:
        return typing.cast(EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorTotalMemoryMibOutputReference, jsii.get(self, "acceleratorTotalMemoryMib"))

    @builtins.property
    @jsii.member(jsii_name="baselineEbsBandwidthMbps")
    def baseline_ebs_bandwidth_mbps(
        self,
    ) -> EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsBaselineEbsBandwidthMbpsOutputReference:
        return typing.cast(EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsBaselineEbsBandwidthMbpsOutputReference, jsii.get(self, "baselineEbsBandwidthMbps"))

    @builtins.property
    @jsii.member(jsii_name="memoryGibPerVcpu")
    def memory_gib_per_vcpu(
        self,
    ) -> EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryGibPerVcpuOutputReference:
        return typing.cast(EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryGibPerVcpuOutputReference, jsii.get(self, "memoryGibPerVcpu"))

    @builtins.property
    @jsii.member(jsii_name="memoryMib")
    def memory_mib(
        self,
    ) -> EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryMibOutputReference:
        return typing.cast(EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryMibOutputReference, jsii.get(self, "memoryMib"))

    @builtins.property
    @jsii.member(jsii_name="networkBandwidthGbps")
    def network_bandwidth_gbps(
        self,
    ) -> EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkBandwidthGbpsOutputReference:
        return typing.cast(EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkBandwidthGbpsOutputReference, jsii.get(self, "networkBandwidthGbps"))

    @builtins.property
    @jsii.member(jsii_name="networkInterfaceCount")
    def network_interface_count(
        self,
    ) -> EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkInterfaceCountOutputReference:
        return typing.cast(EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkInterfaceCountOutputReference, jsii.get(self, "networkInterfaceCount"))

    @builtins.property
    @jsii.member(jsii_name="totalLocalStorageGb")
    def total_local_storage_gb(
        self,
    ) -> "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsTotalLocalStorageGbOutputReference":
        return typing.cast("EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsTotalLocalStorageGbOutputReference", jsii.get(self, "totalLocalStorageGb"))

    @builtins.property
    @jsii.member(jsii_name="vcpuCount")
    def vcpu_count(
        self,
    ) -> "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsVcpuCountOutputReference":
        return typing.cast("EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsVcpuCountOutputReference", jsii.get(self, "vcpuCount"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorCountInput")
    def accelerator_count_input(
        self,
    ) -> typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorCount]:
        return typing.cast(typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorCount], jsii.get(self, "acceleratorCountInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorManufacturersInput")
    def accelerator_manufacturers_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "acceleratorManufacturersInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorNamesInput")
    def accelerator_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "acceleratorNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorTotalMemoryMibInput")
    def accelerator_total_memory_mib_input(
        self,
    ) -> typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorTotalMemoryMib]:
        return typing.cast(typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorTotalMemoryMib], jsii.get(self, "acceleratorTotalMemoryMibInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorTypesInput")
    def accelerator_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "acceleratorTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedInstanceTypesInput")
    def allowed_instance_types_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedInstanceTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="bareMetalInput")
    def bare_metal_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bareMetalInput"))

    @builtins.property
    @jsii.member(jsii_name="baselineEbsBandwidthMbpsInput")
    def baseline_ebs_bandwidth_mbps_input(
        self,
    ) -> typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsBaselineEbsBandwidthMbps]:
        return typing.cast(typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsBaselineEbsBandwidthMbps], jsii.get(self, "baselineEbsBandwidthMbpsInput"))

    @builtins.property
    @jsii.member(jsii_name="burstablePerformanceInput")
    def burstable_performance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "burstablePerformanceInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuManufacturersInput")
    def cpu_manufacturers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "cpuManufacturersInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedInstanceTypesInput")
    def excluded_instance_types_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludedInstanceTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceGenerationsInput")
    def instance_generations_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "instanceGenerationsInput"))

    @builtins.property
    @jsii.member(jsii_name="localStorageInput")
    def local_storage_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localStorageInput"))

    @builtins.property
    @jsii.member(jsii_name="localStorageTypesInput")
    def local_storage_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "localStorageTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="maxSpotPriceAsPercentageOfOptimalOnDemandPriceInput")
    def max_spot_price_as_percentage_of_optimal_on_demand_price_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxSpotPriceAsPercentageOfOptimalOnDemandPriceInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryGibPerVcpuInput")
    def memory_gib_per_vcpu_input(
        self,
    ) -> typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryGibPerVcpu]:
        return typing.cast(typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryGibPerVcpu], jsii.get(self, "memoryGibPerVcpuInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryMibInput")
    def memory_mib_input(
        self,
    ) -> typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryMib]:
        return typing.cast(typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryMib], jsii.get(self, "memoryMibInput"))

    @builtins.property
    @jsii.member(jsii_name="networkBandwidthGbpsInput")
    def network_bandwidth_gbps_input(
        self,
    ) -> typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkBandwidthGbps]:
        return typing.cast(typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkBandwidthGbps], jsii.get(self, "networkBandwidthGbpsInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInterfaceCountInput")
    def network_interface_count_input(
        self,
    ) -> typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkInterfaceCount]:
        return typing.cast(typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkInterfaceCount], jsii.get(self, "networkInterfaceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="onDemandMaxPricePercentageOverLowestPriceInput")
    def on_demand_max_price_percentage_over_lowest_price_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "onDemandMaxPricePercentageOverLowestPriceInput"))

    @builtins.property
    @jsii.member(jsii_name="requireHibernateSupportInput")
    def require_hibernate_support_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireHibernateSupportInput"))

    @builtins.property
    @jsii.member(jsii_name="spotMaxPricePercentageOverLowestPriceInput")
    def spot_max_price_percentage_over_lowest_price_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "spotMaxPricePercentageOverLowestPriceInput"))

    @builtins.property
    @jsii.member(jsii_name="totalLocalStorageGbInput")
    def total_local_storage_gb_input(
        self,
    ) -> typing.Optional["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsTotalLocalStorageGb"]:
        return typing.cast(typing.Optional["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsTotalLocalStorageGb"], jsii.get(self, "totalLocalStorageGbInput"))

    @builtins.property
    @jsii.member(jsii_name="vcpuCountInput")
    def vcpu_count_input(
        self,
    ) -> typing.Optional["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsVcpuCount"]:
        return typing.cast(typing.Optional["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsVcpuCount"], jsii.get(self, "vcpuCountInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorManufacturers")
    def accelerator_manufacturers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "acceleratorManufacturers"))

    @accelerator_manufacturers.setter
    def accelerator_manufacturers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__738c880c2d93fb7308199246425dfa8a62844bb0dd674c0604ba1ed256007e12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorManufacturers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="acceleratorNames")
    def accelerator_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "acceleratorNames"))

    @accelerator_names.setter
    def accelerator_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1398d278957a60bf6f1c6fc6f7817962adfda89b1c046fd084b51b41091ba235)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="acceleratorTypes")
    def accelerator_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "acceleratorTypes"))

    @accelerator_types.setter
    def accelerator_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04384363f7e2404c7e890474b4176c2d0c5c00277bd37b2e026400b1df0628f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedInstanceTypes")
    def allowed_instance_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedInstanceTypes"))

    @allowed_instance_types.setter
    def allowed_instance_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9512341032ac4720fc079aa9a05edd2a6807d9d3e71bfd8756584bd69fbe4eaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedInstanceTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bareMetal")
    def bare_metal(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bareMetal"))

    @bare_metal.setter
    def bare_metal(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea0b052727736ead76877ef10f88ac479f9129363fe1465ebf27b95032cdec32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bareMetal", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="burstablePerformance")
    def burstable_performance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "burstablePerformance"))

    @burstable_performance.setter
    def burstable_performance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a39f10e56748313679fa39249dd0c775ffab5cd6da0cb52c51b52f918a0c56bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "burstablePerformance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpuManufacturers")
    def cpu_manufacturers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "cpuManufacturers"))

    @cpu_manufacturers.setter
    def cpu_manufacturers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59f6a9f05177ade8863ccec6172355c4e4c96adb2ae54363abc2dcf40c8a50b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuManufacturers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludedInstanceTypes")
    def excluded_instance_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedInstanceTypes"))

    @excluded_instance_types.setter
    def excluded_instance_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b9867916aef2a6012c5c51f98b44ed3aceb64512b17d335419415909c29cfda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedInstanceTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceGenerations")
    def instance_generations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "instanceGenerations"))

    @instance_generations.setter
    def instance_generations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a70ea2757b8a01c8f218e626b503a495d64f85eb1c31fa07d016bfaee5baf09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceGenerations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localStorage")
    def local_storage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localStorage"))

    @local_storage.setter
    def local_storage(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3089072a523f6840bfe20209971bc936acb620ecaa4b89b094eca9b3182f6bdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localStorage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localStorageTypes")
    def local_storage_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "localStorageTypes"))

    @local_storage_types.setter
    def local_storage_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f13921038d3472d29dc48db0d2e0cecbf04cf59848b4e9798f792b91d7b44236)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localStorageTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxSpotPriceAsPercentageOfOptimalOnDemandPrice")
    def max_spot_price_as_percentage_of_optimal_on_demand_price(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxSpotPriceAsPercentageOfOptimalOnDemandPrice"))

    @max_spot_price_as_percentage_of_optimal_on_demand_price.setter
    def max_spot_price_as_percentage_of_optimal_on_demand_price(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a777fdc31fcd642a9f505f03478900d6d2099b3b64dcd55c1e224d66d2dfb68c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxSpotPriceAsPercentageOfOptimalOnDemandPrice", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onDemandMaxPricePercentageOverLowestPrice")
    def on_demand_max_price_percentage_over_lowest_price(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "onDemandMaxPricePercentageOverLowestPrice"))

    @on_demand_max_price_percentage_over_lowest_price.setter
    def on_demand_max_price_percentage_over_lowest_price(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff60ef8cf9efc7cd05c39b635b03fb538dd6faf79d55df06f6054541aee5fba6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onDemandMaxPricePercentageOverLowestPrice", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireHibernateSupport")
    def require_hibernate_support(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireHibernateSupport"))

    @require_hibernate_support.setter
    def require_hibernate_support(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4daf9e5932bf85c230025484ac267bdc779f52b59f912163d858659016c0e848)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireHibernateSupport", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="spotMaxPricePercentageOverLowestPrice")
    def spot_max_price_percentage_over_lowest_price(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "spotMaxPricePercentageOverLowestPrice"))

    @spot_max_price_percentage_over_lowest_price.setter
    def spot_max_price_percentage_over_lowest_price(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8332eea65b37d3f4ceb9cd1175f665d44b12d7e0c7eb10a0da8bfc0f0f65cda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spotMaxPricePercentageOverLowestPrice", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirements]:
        return typing.cast(typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirements], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirements],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41276741f6cbf98e73367dff3faef2adbc8115f9be2f6a70fb8f70d1968491bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ecsCapacityProvider.EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsTotalLocalStorageGb",
    jsii_struct_bases=[],
    name_mapping={"max": "max", "min": "min"},
)
class EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsTotalLocalStorageGb:
    def __init__(
        self,
        *,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#max EcsCapacityProvider#max}.
        :param min: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#min EcsCapacityProvider#min}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e4cf1afb2a2773ece7f1819bdab1bd4b0026a55fae2080b2db45a32062f568a)
            check_type(argname="argument max", value=max, expected_type=type_hints["max"])
            check_type(argname="argument min", value=min, expected_type=type_hints["min"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max is not None:
            self._values["max"] = max
        if min is not None:
            self._values["min"] = min

    @builtins.property
    def max(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#max EcsCapacityProvider#max}.'''
        result = self._values.get("max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#min EcsCapacityProvider#min}.'''
        result = self._values.get("min")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsTotalLocalStorageGb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsTotalLocalStorageGbOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ecsCapacityProvider.EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsTotalLocalStorageGbOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__618b51e4e13937bb806e7c0f9c0bfdd533fbed7db57ae66adc3bd9622f5863cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMax")
    def reset_max(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMax", []))

    @jsii.member(jsii_name="resetMin")
    def reset_min(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMin", []))

    @builtins.property
    @jsii.member(jsii_name="maxInput")
    def max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInput"))

    @builtins.property
    @jsii.member(jsii_name="minInput")
    def min_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minInput"))

    @builtins.property
    @jsii.member(jsii_name="max")
    def max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "max"))

    @max.setter
    def max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c4c5c12d2e5cc0b2d34164cc9c8776498149bed97fbc457e75928a08a14c8b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "max", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="min")
    def min(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "min"))

    @min.setter
    def min(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c053d913b40aef1d8357e4ca16aef526ff0833b8e653ecd06033ce493f18a0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "min", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsTotalLocalStorageGb]:
        return typing.cast(typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsTotalLocalStorageGb], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsTotalLocalStorageGb],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93dd01f9f88e8a383deca9c53e1b6f5e6997bd5adbd7ea78f9c898d01525d7d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ecsCapacityProvider.EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsVcpuCount",
    jsii_struct_bases=[],
    name_mapping={"min": "min", "max": "max"},
)
class EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsVcpuCount:
    def __init__(
        self,
        *,
        min: jsii.Number,
        max: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param min: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#min EcsCapacityProvider#min}.
        :param max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#max EcsCapacityProvider#max}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33ea3d776668fd4b7af7df16701c869748bf366d010ac5c7ce2e57d2ddbff28d)
            check_type(argname="argument min", value=min, expected_type=type_hints["min"])
            check_type(argname="argument max", value=max, expected_type=type_hints["max"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "min": min,
        }
        if max is not None:
            self._values["max"] = max

    @builtins.property
    def min(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#min EcsCapacityProvider#min}.'''
        result = self._values.get("min")
        assert result is not None, "Required property 'min' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def max(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#max EcsCapacityProvider#max}.'''
        result = self._values.get("max")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsVcpuCount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsVcpuCountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ecsCapacityProvider.EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsVcpuCountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a383bafc6dd177dd61e7eb7ec34058ae0a5f56ecd2e1d4f4995db9c2a22b904)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMax")
    def reset_max(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMax", []))

    @builtins.property
    @jsii.member(jsii_name="maxInput")
    def max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInput"))

    @builtins.property
    @jsii.member(jsii_name="minInput")
    def min_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minInput"))

    @builtins.property
    @jsii.member(jsii_name="max")
    def max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "max"))

    @max.setter
    def max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cfc3741d75d6b5a7584c39401c92dcf72990b4eb5690de80dc1ff013a352c57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "max", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="min")
    def min(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "min"))

    @min.setter
    def min(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30520cae8850eb923b10bf0f587ff199aa7708c1b0357c63e3db8eefe92a21c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "min", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsVcpuCount]:
        return typing.cast(typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsVcpuCount], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsVcpuCount],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b39bdaf2c7700c2327a7aa775a994b9045bd527c1a80701d092e60b376571d0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ecsCapacityProvider.EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateNetworkConfiguration",
    jsii_struct_bases=[],
    name_mapping={"subnets": "subnets", "security_groups": "securityGroups"},
)
class EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateNetworkConfiguration:
    def __init__(
        self,
        *,
        subnets: typing.Sequence[builtins.str],
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param subnets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#subnets EcsCapacityProvider#subnets}.
        :param security_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#security_groups EcsCapacityProvider#security_groups}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfdd5ebcd2a135c8f321f6e05a2a604eb17cda247327544d5ebe7ae034f0af67)
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subnets": subnets,
        }
        if security_groups is not None:
            self._values["security_groups"] = security_groups

    @builtins.property
    def subnets(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#subnets EcsCapacityProvider#subnets}.'''
        result = self._values.get("subnets")
        assert result is not None, "Required property 'subnets' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#security_groups EcsCapacityProvider#security_groups}.'''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateNetworkConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateNetworkConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ecsCapacityProvider.EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateNetworkConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4f4ba64c74d21d3bfa808c3ada5de22ece3e2b6e92ecf23f5acd5b098e226d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSecurityGroups")
    def reset_security_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroups", []))

    @builtins.property
    @jsii.member(jsii_name="securityGroupsInput")
    def security_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetsInput")
    def subnets_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetsInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroups"))

    @security_groups.setter
    def security_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88b7b3a1fb831b7febe94c05ed1cc6fa6204bb8d2d01b899856a3ec79e99eb25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnets")
    def subnets(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnets"))

    @subnets.setter
    def subnets(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce5ed876424d170550a127c6a54ea578d45ce9f8ddae8d98d89548e0a873ea79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateNetworkConfiguration]:
        return typing.cast(typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateNetworkConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateNetworkConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5dd38156173c40f665a36d4119cb309a786f21e5ba4f6b774cac60073dc8418)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ecsCapacityProvider.EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c99925d65d012c89b709939ad820ffd6a4d53730d47df7a75600330e362417f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInstanceRequirements")
    def put_instance_requirements(
        self,
        *,
        memory_mib: typing.Union[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryMib, typing.Dict[builtins.str, typing.Any]],
        vcpu_count: typing.Union[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsVcpuCount, typing.Dict[builtins.str, typing.Any]],
        accelerator_count: typing.Optional[typing.Union[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorCount, typing.Dict[builtins.str, typing.Any]]] = None,
        accelerator_manufacturers: typing.Optional[typing.Sequence[builtins.str]] = None,
        accelerator_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        accelerator_total_memory_mib: typing.Optional[typing.Union[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorTotalMemoryMib, typing.Dict[builtins.str, typing.Any]]] = None,
        accelerator_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        bare_metal: typing.Optional[builtins.str] = None,
        baseline_ebs_bandwidth_mbps: typing.Optional[typing.Union[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsBaselineEbsBandwidthMbps, typing.Dict[builtins.str, typing.Any]]] = None,
        burstable_performance: typing.Optional[builtins.str] = None,
        cpu_manufacturers: typing.Optional[typing.Sequence[builtins.str]] = None,
        excluded_instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        instance_generations: typing.Optional[typing.Sequence[builtins.str]] = None,
        local_storage: typing.Optional[builtins.str] = None,
        local_storage_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_spot_price_as_percentage_of_optimal_on_demand_price: typing.Optional[jsii.Number] = None,
        memory_gib_per_vcpu: typing.Optional[typing.Union[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryGibPerVcpu, typing.Dict[builtins.str, typing.Any]]] = None,
        network_bandwidth_gbps: typing.Optional[typing.Union[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkBandwidthGbps, typing.Dict[builtins.str, typing.Any]]] = None,
        network_interface_count: typing.Optional[typing.Union[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkInterfaceCount, typing.Dict[builtins.str, typing.Any]]] = None,
        on_demand_max_price_percentage_over_lowest_price: typing.Optional[jsii.Number] = None,
        require_hibernate_support: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        spot_max_price_percentage_over_lowest_price: typing.Optional[jsii.Number] = None,
        total_local_storage_gb: typing.Optional[typing.Union[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsTotalLocalStorageGb, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param memory_mib: memory_mib block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#memory_mib EcsCapacityProvider#memory_mib}
        :param vcpu_count: vcpu_count block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#vcpu_count EcsCapacityProvider#vcpu_count}
        :param accelerator_count: accelerator_count block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#accelerator_count EcsCapacityProvider#accelerator_count}
        :param accelerator_manufacturers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#accelerator_manufacturers EcsCapacityProvider#accelerator_manufacturers}.
        :param accelerator_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#accelerator_names EcsCapacityProvider#accelerator_names}.
        :param accelerator_total_memory_mib: accelerator_total_memory_mib block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#accelerator_total_memory_mib EcsCapacityProvider#accelerator_total_memory_mib}
        :param accelerator_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#accelerator_types EcsCapacityProvider#accelerator_types}.
        :param allowed_instance_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#allowed_instance_types EcsCapacityProvider#allowed_instance_types}.
        :param bare_metal: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#bare_metal EcsCapacityProvider#bare_metal}.
        :param baseline_ebs_bandwidth_mbps: baseline_ebs_bandwidth_mbps block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#baseline_ebs_bandwidth_mbps EcsCapacityProvider#baseline_ebs_bandwidth_mbps}
        :param burstable_performance: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#burstable_performance EcsCapacityProvider#burstable_performance}.
        :param cpu_manufacturers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#cpu_manufacturers EcsCapacityProvider#cpu_manufacturers}.
        :param excluded_instance_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#excluded_instance_types EcsCapacityProvider#excluded_instance_types}.
        :param instance_generations: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#instance_generations EcsCapacityProvider#instance_generations}.
        :param local_storage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#local_storage EcsCapacityProvider#local_storage}.
        :param local_storage_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#local_storage_types EcsCapacityProvider#local_storage_types}.
        :param max_spot_price_as_percentage_of_optimal_on_demand_price: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#max_spot_price_as_percentage_of_optimal_on_demand_price EcsCapacityProvider#max_spot_price_as_percentage_of_optimal_on_demand_price}.
        :param memory_gib_per_vcpu: memory_gib_per_vcpu block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#memory_gib_per_vcpu EcsCapacityProvider#memory_gib_per_vcpu}
        :param network_bandwidth_gbps: network_bandwidth_gbps block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#network_bandwidth_gbps EcsCapacityProvider#network_bandwidth_gbps}
        :param network_interface_count: network_interface_count block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#network_interface_count EcsCapacityProvider#network_interface_count}
        :param on_demand_max_price_percentage_over_lowest_price: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#on_demand_max_price_percentage_over_lowest_price EcsCapacityProvider#on_demand_max_price_percentage_over_lowest_price}.
        :param require_hibernate_support: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#require_hibernate_support EcsCapacityProvider#require_hibernate_support}.
        :param spot_max_price_percentage_over_lowest_price: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#spot_max_price_percentage_over_lowest_price EcsCapacityProvider#spot_max_price_percentage_over_lowest_price}.
        :param total_local_storage_gb: total_local_storage_gb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#total_local_storage_gb EcsCapacityProvider#total_local_storage_gb}
        '''
        value = EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirements(
            memory_mib=memory_mib,
            vcpu_count=vcpu_count,
            accelerator_count=accelerator_count,
            accelerator_manufacturers=accelerator_manufacturers,
            accelerator_names=accelerator_names,
            accelerator_total_memory_mib=accelerator_total_memory_mib,
            accelerator_types=accelerator_types,
            allowed_instance_types=allowed_instance_types,
            bare_metal=bare_metal,
            baseline_ebs_bandwidth_mbps=baseline_ebs_bandwidth_mbps,
            burstable_performance=burstable_performance,
            cpu_manufacturers=cpu_manufacturers,
            excluded_instance_types=excluded_instance_types,
            instance_generations=instance_generations,
            local_storage=local_storage,
            local_storage_types=local_storage_types,
            max_spot_price_as_percentage_of_optimal_on_demand_price=max_spot_price_as_percentage_of_optimal_on_demand_price,
            memory_gib_per_vcpu=memory_gib_per_vcpu,
            network_bandwidth_gbps=network_bandwidth_gbps,
            network_interface_count=network_interface_count,
            on_demand_max_price_percentage_over_lowest_price=on_demand_max_price_percentage_over_lowest_price,
            require_hibernate_support=require_hibernate_support,
            spot_max_price_percentage_over_lowest_price=spot_max_price_percentage_over_lowest_price,
            total_local_storage_gb=total_local_storage_gb,
        )

        return typing.cast(None, jsii.invoke(self, "putInstanceRequirements", [value]))

    @jsii.member(jsii_name="putNetworkConfiguration")
    def put_network_configuration(
        self,
        *,
        subnets: typing.Sequence[builtins.str],
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param subnets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#subnets EcsCapacityProvider#subnets}.
        :param security_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#security_groups EcsCapacityProvider#security_groups}.
        '''
        value = EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateNetworkConfiguration(
            subnets=subnets, security_groups=security_groups
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkConfiguration", [value]))

    @jsii.member(jsii_name="putStorageConfiguration")
    def put_storage_configuration(self, *, storage_size_gib: jsii.Number) -> None:
        '''
        :param storage_size_gib: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#storage_size_gib EcsCapacityProvider#storage_size_gib}.
        '''
        value = EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateStorageConfiguration(
            storage_size_gib=storage_size_gib
        )

        return typing.cast(None, jsii.invoke(self, "putStorageConfiguration", [value]))

    @jsii.member(jsii_name="resetInstanceRequirements")
    def reset_instance_requirements(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceRequirements", []))

    @jsii.member(jsii_name="resetMonitoring")
    def reset_monitoring(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitoring", []))

    @jsii.member(jsii_name="resetStorageConfiguration")
    def reset_storage_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="instanceRequirements")
    def instance_requirements(
        self,
    ) -> EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsOutputReference:
        return typing.cast(EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsOutputReference, jsii.get(self, "instanceRequirements"))

    @builtins.property
    @jsii.member(jsii_name="networkConfiguration")
    def network_configuration(
        self,
    ) -> EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateNetworkConfigurationOutputReference:
        return typing.cast(EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateNetworkConfigurationOutputReference, jsii.get(self, "networkConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="storageConfiguration")
    def storage_configuration(
        self,
    ) -> "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateStorageConfigurationOutputReference":
        return typing.cast("EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateStorageConfigurationOutputReference", jsii.get(self, "storageConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="ec2InstanceProfileArnInput")
    def ec2_instance_profile_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ec2InstanceProfileArnInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceRequirementsInput")
    def instance_requirements_input(
        self,
    ) -> typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirements]:
        return typing.cast(typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirements], jsii.get(self, "instanceRequirementsInput"))

    @builtins.property
    @jsii.member(jsii_name="monitoringInput")
    def monitoring_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "monitoringInput"))

    @builtins.property
    @jsii.member(jsii_name="networkConfigurationInput")
    def network_configuration_input(
        self,
    ) -> typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateNetworkConfiguration]:
        return typing.cast(typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateNetworkConfiguration], jsii.get(self, "networkConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="storageConfigurationInput")
    def storage_configuration_input(
        self,
    ) -> typing.Optional["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateStorageConfiguration"]:
        return typing.cast(typing.Optional["EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateStorageConfiguration"], jsii.get(self, "storageConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="ec2InstanceProfileArn")
    def ec2_instance_profile_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ec2InstanceProfileArn"))

    @ec2_instance_profile_arn.setter
    def ec2_instance_profile_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca886ce6b3ccd0407087735a5704a53cf422d08baaec12cfd5899cc39d199228)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ec2InstanceProfileArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="monitoring")
    def monitoring(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "monitoring"))

    @monitoring.setter
    def monitoring(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b1a3b68a427e493dcaa9523503314b3450364963dbb461cafd745f581a7a414)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitoring", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplate]:
        return typing.cast(typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51bcb1999453a80182fe5a14a6fdc6126fec482b665552c4b7f6b2f45fd76db5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ecsCapacityProvider.EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateStorageConfiguration",
    jsii_struct_bases=[],
    name_mapping={"storage_size_gib": "storageSizeGib"},
)
class EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateStorageConfiguration:
    def __init__(self, *, storage_size_gib: jsii.Number) -> None:
        '''
        :param storage_size_gib: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#storage_size_gib EcsCapacityProvider#storage_size_gib}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca3feb68490a7ba072e79232c0e10ec44a78203817284465c3fea291cbea8ad7)
            check_type(argname="argument storage_size_gib", value=storage_size_gib, expected_type=type_hints["storage_size_gib"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "storage_size_gib": storage_size_gib,
        }

    @builtins.property
    def storage_size_gib(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#storage_size_gib EcsCapacityProvider#storage_size_gib}.'''
        result = self._values.get("storage_size_gib")
        assert result is not None, "Required property 'storage_size_gib' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateStorageConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateStorageConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ecsCapacityProvider.EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateStorageConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cbb087ccbd3af95f5298c0aad5d6d2dfac2c573bd04d35031c98e523888fe41e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="storageSizeGibInput")
    def storage_size_gib_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "storageSizeGibInput"))

    @builtins.property
    @jsii.member(jsii_name="storageSizeGib")
    def storage_size_gib(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "storageSizeGib"))

    @storage_size_gib.setter
    def storage_size_gib(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ee334605a75fed4a246a4fef3025c33c4bfc49728d80ae624e5627ec47be604)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageSizeGib", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateStorageConfiguration]:
        return typing.cast(typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateStorageConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateStorageConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a00311790f7206103f91dff4a815cc501ca932cdcab31a78c63b9332f9c05319)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EcsCapacityProviderManagedInstancesProviderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ecsCapacityProvider.EcsCapacityProviderManagedInstancesProviderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b43f678844d9387e8c84704473fe5593ea0133301df3e346737bd06ec204e146)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInfrastructureOptimization")
    def put_infrastructure_optimization(
        self,
        *,
        scale_in_after: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param scale_in_after: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#scale_in_after EcsCapacityProvider#scale_in_after}.
        '''
        value = EcsCapacityProviderManagedInstancesProviderInfrastructureOptimization(
            scale_in_after=scale_in_after
        )

        return typing.cast(None, jsii.invoke(self, "putInfrastructureOptimization", [value]))

    @jsii.member(jsii_name="putInstanceLaunchTemplate")
    def put_instance_launch_template(
        self,
        *,
        ec2_instance_profile_arn: builtins.str,
        network_configuration: typing.Union[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateNetworkConfiguration, typing.Dict[builtins.str, typing.Any]],
        instance_requirements: typing.Optional[typing.Union[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirements, typing.Dict[builtins.str, typing.Any]]] = None,
        monitoring: typing.Optional[builtins.str] = None,
        storage_configuration: typing.Optional[typing.Union[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateStorageConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ec2_instance_profile_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#ec2_instance_profile_arn EcsCapacityProvider#ec2_instance_profile_arn}.
        :param network_configuration: network_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#network_configuration EcsCapacityProvider#network_configuration}
        :param instance_requirements: instance_requirements block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#instance_requirements EcsCapacityProvider#instance_requirements}
        :param monitoring: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#monitoring EcsCapacityProvider#monitoring}.
        :param storage_configuration: storage_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/ecs_capacity_provider#storage_configuration EcsCapacityProvider#storage_configuration}
        '''
        value = EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplate(
            ec2_instance_profile_arn=ec2_instance_profile_arn,
            network_configuration=network_configuration,
            instance_requirements=instance_requirements,
            monitoring=monitoring,
            storage_configuration=storage_configuration,
        )

        return typing.cast(None, jsii.invoke(self, "putInstanceLaunchTemplate", [value]))

    @jsii.member(jsii_name="resetInfrastructureOptimization")
    def reset_infrastructure_optimization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInfrastructureOptimization", []))

    @jsii.member(jsii_name="resetPropagateTags")
    def reset_propagate_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPropagateTags", []))

    @builtins.property
    @jsii.member(jsii_name="infrastructureOptimization")
    def infrastructure_optimization(
        self,
    ) -> EcsCapacityProviderManagedInstancesProviderInfrastructureOptimizationOutputReference:
        return typing.cast(EcsCapacityProviderManagedInstancesProviderInfrastructureOptimizationOutputReference, jsii.get(self, "infrastructureOptimization"))

    @builtins.property
    @jsii.member(jsii_name="instanceLaunchTemplate")
    def instance_launch_template(
        self,
    ) -> EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateOutputReference:
        return typing.cast(EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateOutputReference, jsii.get(self, "instanceLaunchTemplate"))

    @builtins.property
    @jsii.member(jsii_name="infrastructureOptimizationInput")
    def infrastructure_optimization_input(
        self,
    ) -> typing.Optional[EcsCapacityProviderManagedInstancesProviderInfrastructureOptimization]:
        return typing.cast(typing.Optional[EcsCapacityProviderManagedInstancesProviderInfrastructureOptimization], jsii.get(self, "infrastructureOptimizationInput"))

    @builtins.property
    @jsii.member(jsii_name="infrastructureRoleArnInput")
    def infrastructure_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "infrastructureRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceLaunchTemplateInput")
    def instance_launch_template_input(
        self,
    ) -> typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplate]:
        return typing.cast(typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplate], jsii.get(self, "instanceLaunchTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="propagateTagsInput")
    def propagate_tags_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "propagateTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="infrastructureRoleArn")
    def infrastructure_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "infrastructureRoleArn"))

    @infrastructure_role_arn.setter
    def infrastructure_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f55aa4c084ec89976e5f3b5d68bf8d7911c0d39145805f7136fb4de067a9cc3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "infrastructureRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="propagateTags")
    def propagate_tags(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "propagateTags"))

    @propagate_tags.setter
    def propagate_tags(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2075d5847f4002d4390e3b1a6c7aa6a562f051be812293b1fa2ac64a2e5b8eca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "propagateTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EcsCapacityProviderManagedInstancesProvider]:
        return typing.cast(typing.Optional[EcsCapacityProviderManagedInstancesProvider], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EcsCapacityProviderManagedInstancesProvider],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__724419b16d7c1317967d972aad3cbdfdc520cdb0a4643087a5c2d26862b17dfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "EcsCapacityProvider",
    "EcsCapacityProviderAutoScalingGroupProvider",
    "EcsCapacityProviderAutoScalingGroupProviderManagedScaling",
    "EcsCapacityProviderAutoScalingGroupProviderManagedScalingOutputReference",
    "EcsCapacityProviderAutoScalingGroupProviderOutputReference",
    "EcsCapacityProviderConfig",
    "EcsCapacityProviderManagedInstancesProvider",
    "EcsCapacityProviderManagedInstancesProviderInfrastructureOptimization",
    "EcsCapacityProviderManagedInstancesProviderInfrastructureOptimizationOutputReference",
    "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplate",
    "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirements",
    "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorCount",
    "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorCountOutputReference",
    "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorTotalMemoryMib",
    "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorTotalMemoryMibOutputReference",
    "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsBaselineEbsBandwidthMbps",
    "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsBaselineEbsBandwidthMbpsOutputReference",
    "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryGibPerVcpu",
    "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryGibPerVcpuOutputReference",
    "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryMib",
    "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryMibOutputReference",
    "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkBandwidthGbps",
    "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkBandwidthGbpsOutputReference",
    "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkInterfaceCount",
    "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkInterfaceCountOutputReference",
    "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsOutputReference",
    "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsTotalLocalStorageGb",
    "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsTotalLocalStorageGbOutputReference",
    "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsVcpuCount",
    "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsVcpuCountOutputReference",
    "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateNetworkConfiguration",
    "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateNetworkConfigurationOutputReference",
    "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateOutputReference",
    "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateStorageConfiguration",
    "EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateStorageConfigurationOutputReference",
    "EcsCapacityProviderManagedInstancesProviderOutputReference",
]

publication.publish()

def _typecheckingstub__f3bf2746c14ee596c69de0470d6191b36f92644c677e4720667d230d8ba01a7e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    auto_scaling_group_provider: typing.Optional[typing.Union[EcsCapacityProviderAutoScalingGroupProvider, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    managed_instances_provider: typing.Optional[typing.Union[EcsCapacityProviderManagedInstancesProvider, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__1f77e654120b74a191b7418a905ced4e81536a19d86fa1cf932836fb21e393f4(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bee01a8ebfa3cdb0c37cfb46929f3f2fc1ff777ddfdec739fe139f379ee88a78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__817aaea4449db5ba8429963a71ae12db12fe851bbae3abbd427b3280985bd6e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79b514b296517015c6728dc6c41eee1d740d62c016b895b782f499ca8d820f22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1853ac1235a23ba19310129de7eba9d8dac52dd964c3ab01f1274a165af4eeb7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a64ed14430dac70c950aa828f0feaef8411717b5dceb1eb11bd56241e53cb96f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69aa72aeda7db743c7eb86a3ea47bbce101ad26ddc96703cd38a29b97f13423e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__798d40ce0c9fb092567831846c9439a51ff85fe90e6898e9a8d6cc6e7bd58d7d(
    *,
    auto_scaling_group_arn: builtins.str,
    managed_draining: typing.Optional[builtins.str] = None,
    managed_scaling: typing.Optional[typing.Union[EcsCapacityProviderAutoScalingGroupProviderManagedScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    managed_termination_protection: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aea398c383aa653974f99a5f3193fefbbe0d0aedfc884333a70643b231a3a8e1(
    *,
    instance_warmup_period: typing.Optional[jsii.Number] = None,
    maximum_scaling_step_size: typing.Optional[jsii.Number] = None,
    minimum_scaling_step_size: typing.Optional[jsii.Number] = None,
    status: typing.Optional[builtins.str] = None,
    target_capacity: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9125a61629fe561ef7eb37c07c25ddcd12dc95c448210a868e992572b45b5535(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9e129789c8e6c678c7ef0e4f10f5b03301b05658da08e20a62036f125bb0a9f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ae7799fb416a40882e83a1509d08e78b56227826943b342e972bce6b0650b24(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60dc4970a8ab39096418bf3f408bed39e6bb061e4e49c7a60dc945f82ce3333c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5018b2e3685ad5f14413e3a4ee7d20e3e9d4883557f10a2da94335a55258347(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9ad1b45bdf0d46b8247f18438ee6fb041eac910adfdfeaeb908872e0b8002aa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52f0e4572a3a8ef9c664d724de42af387beab98d668c4de4474fcb45610d0cb3(
    value: typing.Optional[EcsCapacityProviderAutoScalingGroupProviderManagedScaling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a65009d21d48c359041b0ad6c8b66b5277bef39bdcf56d7b84929831f4a93baf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b10e0ed8c35de902dd0b3fd7f91267d7099c20d79467bb967f9c8ef36efbd4b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__129ece76b9b3c5fab80a87f0fa74f84281c6e6909507d9d0aecefbf8c28d97fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87bf4f64228b4b171c4443902514addf8ef44c6b9079900312d7d6d0eb98f766(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3465647231626f313b67cd1d547910204175a86a7fe528730e6a8659bcee889(
    value: typing.Optional[EcsCapacityProviderAutoScalingGroupProvider],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f7825bd6e506de5febb6f3031cd2775abf009027e7e62d89ca20a4223d69734(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    auto_scaling_group_provider: typing.Optional[typing.Union[EcsCapacityProviderAutoScalingGroupProvider, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    managed_instances_provider: typing.Optional[typing.Union[EcsCapacityProviderManagedInstancesProvider, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ff67e3d8e7c6ba486856d32a9da9fb01e59d07bfc04a71d1a38469c409f7584(
    *,
    infrastructure_role_arn: builtins.str,
    instance_launch_template: typing.Union[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplate, typing.Dict[builtins.str, typing.Any]],
    infrastructure_optimization: typing.Optional[typing.Union[EcsCapacityProviderManagedInstancesProviderInfrastructureOptimization, typing.Dict[builtins.str, typing.Any]]] = None,
    propagate_tags: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__762d04c1174465946f3d933a88452bbb823b03b6f91d8c972349b74f75962b05(
    *,
    scale_in_after: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88f79b01c75bded40867fbb1f29992c8adb5cebc002cd28e123fe7b9906f8dbe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4396b0bdd8098ad9fa956fcc867f942c7ab5488792819a9c5b8e90a55b16e70b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1560a46fe69cdd210eb07e971e1b8c1c904f4ca510bee86f9b06f67afe6a9fe(
    value: typing.Optional[EcsCapacityProviderManagedInstancesProviderInfrastructureOptimization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c38acd0ab05c5b80cbf9cbade9a35dd2df9693b561e856d23f16dd247c09313(
    *,
    ec2_instance_profile_arn: builtins.str,
    network_configuration: typing.Union[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateNetworkConfiguration, typing.Dict[builtins.str, typing.Any]],
    instance_requirements: typing.Optional[typing.Union[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirements, typing.Dict[builtins.str, typing.Any]]] = None,
    monitoring: typing.Optional[builtins.str] = None,
    storage_configuration: typing.Optional[typing.Union[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateStorageConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dba9a05eace9f830f932846ce21f33d8ffc562ba825477521917ce9f7f28e072(
    *,
    memory_mib: typing.Union[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryMib, typing.Dict[builtins.str, typing.Any]],
    vcpu_count: typing.Union[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsVcpuCount, typing.Dict[builtins.str, typing.Any]],
    accelerator_count: typing.Optional[typing.Union[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorCount, typing.Dict[builtins.str, typing.Any]]] = None,
    accelerator_manufacturers: typing.Optional[typing.Sequence[builtins.str]] = None,
    accelerator_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    accelerator_total_memory_mib: typing.Optional[typing.Union[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorTotalMemoryMib, typing.Dict[builtins.str, typing.Any]]] = None,
    accelerator_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    bare_metal: typing.Optional[builtins.str] = None,
    baseline_ebs_bandwidth_mbps: typing.Optional[typing.Union[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsBaselineEbsBandwidthMbps, typing.Dict[builtins.str, typing.Any]]] = None,
    burstable_performance: typing.Optional[builtins.str] = None,
    cpu_manufacturers: typing.Optional[typing.Sequence[builtins.str]] = None,
    excluded_instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    instance_generations: typing.Optional[typing.Sequence[builtins.str]] = None,
    local_storage: typing.Optional[builtins.str] = None,
    local_storage_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_spot_price_as_percentage_of_optimal_on_demand_price: typing.Optional[jsii.Number] = None,
    memory_gib_per_vcpu: typing.Optional[typing.Union[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryGibPerVcpu, typing.Dict[builtins.str, typing.Any]]] = None,
    network_bandwidth_gbps: typing.Optional[typing.Union[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkBandwidthGbps, typing.Dict[builtins.str, typing.Any]]] = None,
    network_interface_count: typing.Optional[typing.Union[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkInterfaceCount, typing.Dict[builtins.str, typing.Any]]] = None,
    on_demand_max_price_percentage_over_lowest_price: typing.Optional[jsii.Number] = None,
    require_hibernate_support: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    spot_max_price_percentage_over_lowest_price: typing.Optional[jsii.Number] = None,
    total_local_storage_gb: typing.Optional[typing.Union[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsTotalLocalStorageGb, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fc2e2db80ab936900e89f399d127bc6f2db9141715c8a27627f525da80e9703(
    *,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c398b01eb8a3793e3a05677ba271081a559ed4aab27a96a6b8d04c4fe691e37d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d22ac9e7144535e1feae157e3de7a1cf817a70c30bfb973f8727bd287aee1df(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd4e5006e9a497dc89518d2b9358cf126f5b66adeb05aae1398eaba9a64d5301(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21d58051bbfd6e375f3f2b0f2e41ab72ade1a2f4ab504efd83ac1afb3ede1cf8(
    value: typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorCount],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d6921dc97e3372977efe5ca7210a816f8b69fad31672fe4fb9a42971eb4f291(
    *,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c6bbd504db7a896fb6ded2dd79e0c12be2f5758c4f85e1708cc17c2f2c42226(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f542231d03fcd974dc7aba200ce10b1c84e73aa13139209bc73c5b3bc30cf33e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26371a43f5e7845939acafc61b0d35f0c28ca0314b105409775913317288cc2e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2934502a4e6eec57c1c848b969cc9811aa6471e790fc170c86b3e4bbb78aa0b1(
    value: typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsAcceleratorTotalMemoryMib],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfc1141436a18faa21e805273af12061da8063e284f40a21dff92cc31656b86f(
    *,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__821feb9ed75a2532bfab4c43b387a206215c7dc8f7e0b022e0b428c0dd1f1dc8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a32aeec5ddbd807b84eb4f1bec0a901f74944f038ad908d35312b84ad37dcffc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d4fa03cfc29a7d92241f28a8cc52d6ff0b71a2b74051266d5dc6222ba5abfb4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb677a218b5a287367835a9981ea8549500fab3ab66f838ba43e1dcb2b09b56e(
    value: typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsBaselineEbsBandwidthMbps],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07f29562b56306ce48de558c8c865c07b70fd9cfbed342caa046cb360ed1b3e0(
    *,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a670a40d91564fe67235630de19aa7d4a30d236087135426b5b021dd470cbf0f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__181941a5ba3683311863c38bf78988ff6d871a1001a005dbe76cfdcd9d314d07(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f67582e54d090781b8bd18e9c69d52437f31cbe6de42ebdb6779e205cf77721(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34452b0a3600302473035476ff5345164d30841efaa690fe4bd4187fcff1c27b(
    value: typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryGibPerVcpu],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dff2390a950f57403298193f518f81f22f1e37044132107afbec470e076c9dbf(
    *,
    min: jsii.Number,
    max: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b5f35870f1da6e103d67b04d11931f19a8895b4d614b8af706723c0f2096c0e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b2e611baf423c23db945f438d3a6d44fbca231e3f15982307359ff30ca0bd95(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31bb47bfb24cdf0b16e31e6b1c35cb05b6950996c8d3d6719dd4f4368cf1abe0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99c4bd79c52b66a678a6a393edcb24c9a85eb13b3dbdde795dc2d5eb13d95a42(
    value: typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsMemoryMib],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7be8a679ff022aaa01cfc4e7a71a00d2363b224f610c898ec7996d387fd2068(
    *,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c177a1614b013172efbc02438bbedf6685f92c276cf83ba361bbc630300575f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdf5bfdf245d7a6568ed1534429d932da04e43b70a929356a13d2e2be6e89d95(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9fb0c764f58b69fcfa702ec9c35deec25ae701a876cd6c118cc4a84265f4a6d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80364ca30661a260db6d8c16621c80c6f1f5f3bb54ee27716a96fa6c6fbf90f3(
    value: typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkBandwidthGbps],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f86c1f14860f34f13e17c06d1a96e87fca3ffa174fd4cebff0ac7700232309b(
    *,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81e9d579b60a209045a8ca9890d2b3e56252ccbba743f5b8d6e618d81b754e9d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a98bfb532ac715c63696328b5b93ba5e5dee69bd126c0d5656ce6bdb97f298a9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56330915157340e0259d61105ae3ec9ff9c841bcc1942849c374cc4f996dd55e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__021f76a03625da2163cf518a61971a4b4f2c5277d935abbd37de721aef77674b(
    value: typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsNetworkInterfaceCount],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3866b4b5166d923ef52c2b33d476d80b02d7986492280c654ad258df582e0442(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__738c880c2d93fb7308199246425dfa8a62844bb0dd674c0604ba1ed256007e12(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1398d278957a60bf6f1c6fc6f7817962adfda89b1c046fd084b51b41091ba235(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04384363f7e2404c7e890474b4176c2d0c5c00277bd37b2e026400b1df0628f3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9512341032ac4720fc079aa9a05edd2a6807d9d3e71bfd8756584bd69fbe4eaa(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea0b052727736ead76877ef10f88ac479f9129363fe1465ebf27b95032cdec32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a39f10e56748313679fa39249dd0c775ffab5cd6da0cb52c51b52f918a0c56bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59f6a9f05177ade8863ccec6172355c4e4c96adb2ae54363abc2dcf40c8a50b8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b9867916aef2a6012c5c51f98b44ed3aceb64512b17d335419415909c29cfda(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a70ea2757b8a01c8f218e626b503a495d64f85eb1c31fa07d016bfaee5baf09(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3089072a523f6840bfe20209971bc936acb620ecaa4b89b094eca9b3182f6bdc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f13921038d3472d29dc48db0d2e0cecbf04cf59848b4e9798f792b91d7b44236(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a777fdc31fcd642a9f505f03478900d6d2099b3b64dcd55c1e224d66d2dfb68c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff60ef8cf9efc7cd05c39b635b03fb538dd6faf79d55df06f6054541aee5fba6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4daf9e5932bf85c230025484ac267bdc779f52b59f912163d858659016c0e848(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8332eea65b37d3f4ceb9cd1175f665d44b12d7e0c7eb10a0da8bfc0f0f65cda(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41276741f6cbf98e73367dff3faef2adbc8115f9be2f6a70fb8f70d1968491bb(
    value: typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirements],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e4cf1afb2a2773ece7f1819bdab1bd4b0026a55fae2080b2db45a32062f568a(
    *,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__618b51e4e13937bb806e7c0f9c0bfdd533fbed7db57ae66adc3bd9622f5863cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c4c5c12d2e5cc0b2d34164cc9c8776498149bed97fbc457e75928a08a14c8b4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c053d913b40aef1d8357e4ca16aef526ff0833b8e653ecd06033ce493f18a0f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93dd01f9f88e8a383deca9c53e1b6f5e6997bd5adbd7ea78f9c898d01525d7d5(
    value: typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsTotalLocalStorageGb],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33ea3d776668fd4b7af7df16701c869748bf366d010ac5c7ce2e57d2ddbff28d(
    *,
    min: jsii.Number,
    max: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a383bafc6dd177dd61e7eb7ec34058ae0a5f56ecd2e1d4f4995db9c2a22b904(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cfc3741d75d6b5a7584c39401c92dcf72990b4eb5690de80dc1ff013a352c57(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30520cae8850eb923b10bf0f587ff199aa7708c1b0357c63e3db8eefe92a21c0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b39bdaf2c7700c2327a7aa775a994b9045bd527c1a80701d092e60b376571d0e(
    value: typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateInstanceRequirementsVcpuCount],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfdd5ebcd2a135c8f321f6e05a2a604eb17cda247327544d5ebe7ae034f0af67(
    *,
    subnets: typing.Sequence[builtins.str],
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4f4ba64c74d21d3bfa808c3ada5de22ece3e2b6e92ecf23f5acd5b098e226d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88b7b3a1fb831b7febe94c05ed1cc6fa6204bb8d2d01b899856a3ec79e99eb25(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce5ed876424d170550a127c6a54ea578d45ce9f8ddae8d98d89548e0a873ea79(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5dd38156173c40f665a36d4119cb309a786f21e5ba4f6b774cac60073dc8418(
    value: typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateNetworkConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c99925d65d012c89b709939ad820ffd6a4d53730d47df7a75600330e362417f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca886ce6b3ccd0407087735a5704a53cf422d08baaec12cfd5899cc39d199228(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b1a3b68a427e493dcaa9523503314b3450364963dbb461cafd745f581a7a414(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51bcb1999453a80182fe5a14a6fdc6126fec482b665552c4b7f6b2f45fd76db5(
    value: typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca3feb68490a7ba072e79232c0e10ec44a78203817284465c3fea291cbea8ad7(
    *,
    storage_size_gib: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbb087ccbd3af95f5298c0aad5d6d2dfac2c573bd04d35031c98e523888fe41e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ee334605a75fed4a246a4fef3025c33c4bfc49728d80ae624e5627ec47be604(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a00311790f7206103f91dff4a815cc501ca932cdcab31a78c63b9332f9c05319(
    value: typing.Optional[EcsCapacityProviderManagedInstancesProviderInstanceLaunchTemplateStorageConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b43f678844d9387e8c84704473fe5593ea0133301df3e346737bd06ec204e146(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f55aa4c084ec89976e5f3b5d68bf8d7911c0d39145805f7136fb4de067a9cc3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2075d5847f4002d4390e3b1a6c7aa6a562f051be812293b1fa2ac64a2e5b8eca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__724419b16d7c1317967d972aad3cbdfdc520cdb0a4643087a5c2d26862b17dfd(
    value: typing.Optional[EcsCapacityProviderManagedInstancesProvider],
) -> None:
    """Type checking stubs"""
    pass
