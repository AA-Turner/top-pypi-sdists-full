r'''
# `google_vmwareengine_cluster`

Refer to the Terraform Registry for docs: [`google_vmwareengine_cluster`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster).
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


class VmwareengineCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareengineCluster.VmwareengineCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster google_vmwareengine_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        parent: builtins.str,
        autoscaling_settings: typing.Optional[typing.Union["VmwareengineClusterAutoscalingSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        node_type_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VmwareengineClusterNodeTypeConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["VmwareengineClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster google_vmwareengine_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The ID of the Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#name VmwareengineCluster#name}
        :param parent: The resource name of the private cloud to create a new cluster in. Resource names are schemeless URIs that follow the conventions in https://cloud.google.com/apis/design/resource_names. For example: projects/my-project/locations/us-west1-a/privateClouds/my-cloud Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#parent VmwareengineCluster#parent}
        :param autoscaling_settings: autoscaling_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#autoscaling_settings VmwareengineCluster#autoscaling_settings}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#id VmwareengineCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param node_type_configs: node_type_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#node_type_configs VmwareengineCluster#node_type_configs}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#timeouts VmwareengineCluster#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec59fac37670f356047b837130a2e57f7298727b62beba4a3efda8ea657450cf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VmwareengineClusterConfig(
            name=name,
            parent=parent,
            autoscaling_settings=autoscaling_settings,
            id=id,
            node_type_configs=node_type_configs,
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
        '''Generates CDKTF code for importing a VmwareengineCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VmwareengineCluster to import.
        :param import_from_id: The id of the existing VmwareengineCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VmwareengineCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__357f64cd22e55cbf90b54ef11938276ca3c19474255214329f35c64103a103da)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAutoscalingSettings")
    def put_autoscaling_settings(
        self,
        *,
        autoscaling_policies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VmwareengineClusterAutoscalingSettingsAutoscalingPolicies", typing.Dict[builtins.str, typing.Any]]]],
        cool_down_period: typing.Optional[builtins.str] = None,
        max_cluster_node_count: typing.Optional[jsii.Number] = None,
        min_cluster_node_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param autoscaling_policies: autoscaling_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#autoscaling_policies VmwareengineCluster#autoscaling_policies}
        :param cool_down_period: The minimum duration between consecutive autoscale operations. It starts once addition or removal of nodes is fully completed. Minimum cool down period is 30m. Cool down period must be in whole minutes (for example, 30m, 31m, 50m). Mandatory for successful addition of autoscaling settings in cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#cool_down_period VmwareengineCluster#cool_down_period}
        :param max_cluster_node_count: Maximum number of nodes of any type in a cluster. Mandatory for successful addition of autoscaling settings in cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#max_cluster_node_count VmwareengineCluster#max_cluster_node_count}
        :param min_cluster_node_count: Minimum number of nodes of any type in a cluster. Mandatory for successful addition of autoscaling settings in cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#min_cluster_node_count VmwareengineCluster#min_cluster_node_count}
        '''
        value = VmwareengineClusterAutoscalingSettings(
            autoscaling_policies=autoscaling_policies,
            cool_down_period=cool_down_period,
            max_cluster_node_count=max_cluster_node_count,
            min_cluster_node_count=min_cluster_node_count,
        )

        return typing.cast(None, jsii.invoke(self, "putAutoscalingSettings", [value]))

    @jsii.member(jsii_name="putNodeTypeConfigs")
    def put_node_type_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VmwareengineClusterNodeTypeConfigs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1002d8990a89bd4f17af5fc2c962b636b0ad99490d6fd80119c756ecc20c7d91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNodeTypeConfigs", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#create VmwareengineCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#delete VmwareengineCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#update VmwareengineCluster#update}.
        '''
        value = VmwareengineClusterTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAutoscalingSettings")
    def reset_autoscaling_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscalingSettings", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNodeTypeConfigs")
    def reset_node_type_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeTypeConfigs", []))

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
    @jsii.member(jsii_name="autoscalingSettings")
    def autoscaling_settings(
        self,
    ) -> "VmwareengineClusterAutoscalingSettingsOutputReference":
        return typing.cast("VmwareengineClusterAutoscalingSettingsOutputReference", jsii.get(self, "autoscalingSettings"))

    @builtins.property
    @jsii.member(jsii_name="management")
    def management(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "management"))

    @builtins.property
    @jsii.member(jsii_name="nodeTypeConfigs")
    def node_type_configs(self) -> "VmwareengineClusterNodeTypeConfigsList":
        return typing.cast("VmwareengineClusterNodeTypeConfigsList", jsii.get(self, "nodeTypeConfigs"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "VmwareengineClusterTimeoutsOutputReference":
        return typing.cast("VmwareengineClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingSettingsInput")
    def autoscaling_settings_input(
        self,
    ) -> typing.Optional["VmwareengineClusterAutoscalingSettings"]:
        return typing.cast(typing.Optional["VmwareengineClusterAutoscalingSettings"], jsii.get(self, "autoscalingSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeTypeConfigsInput")
    def node_type_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmwareengineClusterNodeTypeConfigs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmwareengineClusterNodeTypeConfigs"]]], jsii.get(self, "nodeTypeConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="parentInput")
    def parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VmwareengineClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VmwareengineClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a6be2d8e44774009d1a145aedd4399eba9989a31d258d2e3f2b9174793ba87c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d021b87d3963195add2eb878447922e1fa29ba4a0652547f28d857e89369342)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66a67c6fa9ff0f1f64dea5534f3bb0a7ccf5992591ba1a44ed18bba1f8689c46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vmwareengineCluster.VmwareengineClusterAutoscalingSettings",
    jsii_struct_bases=[],
    name_mapping={
        "autoscaling_policies": "autoscalingPolicies",
        "cool_down_period": "coolDownPeriod",
        "max_cluster_node_count": "maxClusterNodeCount",
        "min_cluster_node_count": "minClusterNodeCount",
    },
)
class VmwareengineClusterAutoscalingSettings:
    def __init__(
        self,
        *,
        autoscaling_policies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VmwareengineClusterAutoscalingSettingsAutoscalingPolicies", typing.Dict[builtins.str, typing.Any]]]],
        cool_down_period: typing.Optional[builtins.str] = None,
        max_cluster_node_count: typing.Optional[jsii.Number] = None,
        min_cluster_node_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param autoscaling_policies: autoscaling_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#autoscaling_policies VmwareengineCluster#autoscaling_policies}
        :param cool_down_period: The minimum duration between consecutive autoscale operations. It starts once addition or removal of nodes is fully completed. Minimum cool down period is 30m. Cool down period must be in whole minutes (for example, 30m, 31m, 50m). Mandatory for successful addition of autoscaling settings in cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#cool_down_period VmwareengineCluster#cool_down_period}
        :param max_cluster_node_count: Maximum number of nodes of any type in a cluster. Mandatory for successful addition of autoscaling settings in cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#max_cluster_node_count VmwareengineCluster#max_cluster_node_count}
        :param min_cluster_node_count: Minimum number of nodes of any type in a cluster. Mandatory for successful addition of autoscaling settings in cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#min_cluster_node_count VmwareengineCluster#min_cluster_node_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3ed31e75e258ea44b4e47131de64c6bc645e073ada612fd8e8609be5d623330)
            check_type(argname="argument autoscaling_policies", value=autoscaling_policies, expected_type=type_hints["autoscaling_policies"])
            check_type(argname="argument cool_down_period", value=cool_down_period, expected_type=type_hints["cool_down_period"])
            check_type(argname="argument max_cluster_node_count", value=max_cluster_node_count, expected_type=type_hints["max_cluster_node_count"])
            check_type(argname="argument min_cluster_node_count", value=min_cluster_node_count, expected_type=type_hints["min_cluster_node_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "autoscaling_policies": autoscaling_policies,
        }
        if cool_down_period is not None:
            self._values["cool_down_period"] = cool_down_period
        if max_cluster_node_count is not None:
            self._values["max_cluster_node_count"] = max_cluster_node_count
        if min_cluster_node_count is not None:
            self._values["min_cluster_node_count"] = min_cluster_node_count

    @builtins.property
    def autoscaling_policies(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmwareengineClusterAutoscalingSettingsAutoscalingPolicies"]]:
        '''autoscaling_policies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#autoscaling_policies VmwareengineCluster#autoscaling_policies}
        '''
        result = self._values.get("autoscaling_policies")
        assert result is not None, "Required property 'autoscaling_policies' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmwareengineClusterAutoscalingSettingsAutoscalingPolicies"]], result)

    @builtins.property
    def cool_down_period(self) -> typing.Optional[builtins.str]:
        '''The minimum duration between consecutive autoscale operations.

        It starts once addition or removal of nodes is fully completed.
        Minimum cool down period is 30m.
        Cool down period must be in whole minutes (for example, 30m, 31m, 50m).
        Mandatory for successful addition of autoscaling settings in cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#cool_down_period VmwareengineCluster#cool_down_period}
        '''
        result = self._values.get("cool_down_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_cluster_node_count(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of nodes of any type in a cluster. Mandatory for successful addition of autoscaling settings in cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#max_cluster_node_count VmwareengineCluster#max_cluster_node_count}
        '''
        result = self._values.get("max_cluster_node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_cluster_node_count(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of nodes of any type in a cluster. Mandatory for successful addition of autoscaling settings in cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#min_cluster_node_count VmwareengineCluster#min_cluster_node_count}
        '''
        result = self._values.get("min_cluster_node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmwareengineClusterAutoscalingSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vmwareengineCluster.VmwareengineClusterAutoscalingSettingsAutoscalingPolicies",
    jsii_struct_bases=[],
    name_mapping={
        "autoscale_policy_id": "autoscalePolicyId",
        "node_type_id": "nodeTypeId",
        "scale_out_size": "scaleOutSize",
        "consumed_memory_thresholds": "consumedMemoryThresholds",
        "cpu_thresholds": "cpuThresholds",
        "storage_thresholds": "storageThresholds",
    },
)
class VmwareengineClusterAutoscalingSettingsAutoscalingPolicies:
    def __init__(
        self,
        *,
        autoscale_policy_id: builtins.str,
        node_type_id: builtins.str,
        scale_out_size: jsii.Number,
        consumed_memory_thresholds: typing.Optional[typing.Union["VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds", typing.Dict[builtins.str, typing.Any]]] = None,
        cpu_thresholds: typing.Optional[typing.Union["VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_thresholds: typing.Optional[typing.Union["VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param autoscale_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#autoscale_policy_id VmwareengineCluster#autoscale_policy_id}.
        :param node_type_id: The canonical identifier of the node type to add or remove. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#node_type_id VmwareengineCluster#node_type_id}
        :param scale_out_size: Number of nodes to add to a cluster during a scale-out operation. Must be divisible by 2 for stretched clusters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#scale_out_size VmwareengineCluster#scale_out_size}
        :param consumed_memory_thresholds: consumed_memory_thresholds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#consumed_memory_thresholds VmwareengineCluster#consumed_memory_thresholds}
        :param cpu_thresholds: cpu_thresholds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#cpu_thresholds VmwareengineCluster#cpu_thresholds}
        :param storage_thresholds: storage_thresholds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#storage_thresholds VmwareengineCluster#storage_thresholds}
        '''
        if isinstance(consumed_memory_thresholds, dict):
            consumed_memory_thresholds = VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds(**consumed_memory_thresholds)
        if isinstance(cpu_thresholds, dict):
            cpu_thresholds = VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds(**cpu_thresholds)
        if isinstance(storage_thresholds, dict):
            storage_thresholds = VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds(**storage_thresholds)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1eee777c6d706b3ed67349da0e387acb0d3438239b403a54bd910aec07ce382)
            check_type(argname="argument autoscale_policy_id", value=autoscale_policy_id, expected_type=type_hints["autoscale_policy_id"])
            check_type(argname="argument node_type_id", value=node_type_id, expected_type=type_hints["node_type_id"])
            check_type(argname="argument scale_out_size", value=scale_out_size, expected_type=type_hints["scale_out_size"])
            check_type(argname="argument consumed_memory_thresholds", value=consumed_memory_thresholds, expected_type=type_hints["consumed_memory_thresholds"])
            check_type(argname="argument cpu_thresholds", value=cpu_thresholds, expected_type=type_hints["cpu_thresholds"])
            check_type(argname="argument storage_thresholds", value=storage_thresholds, expected_type=type_hints["storage_thresholds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "autoscale_policy_id": autoscale_policy_id,
            "node_type_id": node_type_id,
            "scale_out_size": scale_out_size,
        }
        if consumed_memory_thresholds is not None:
            self._values["consumed_memory_thresholds"] = consumed_memory_thresholds
        if cpu_thresholds is not None:
            self._values["cpu_thresholds"] = cpu_thresholds
        if storage_thresholds is not None:
            self._values["storage_thresholds"] = storage_thresholds

    @builtins.property
    def autoscale_policy_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#autoscale_policy_id VmwareengineCluster#autoscale_policy_id}.'''
        result = self._values.get("autoscale_policy_id")
        assert result is not None, "Required property 'autoscale_policy_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def node_type_id(self) -> builtins.str:
        '''The canonical identifier of the node type to add or remove.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#node_type_id VmwareengineCluster#node_type_id}
        '''
        result = self._values.get("node_type_id")
        assert result is not None, "Required property 'node_type_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scale_out_size(self) -> jsii.Number:
        '''Number of nodes to add to a cluster during a scale-out operation. Must be divisible by 2 for stretched clusters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#scale_out_size VmwareengineCluster#scale_out_size}
        '''
        result = self._values.get("scale_out_size")
        assert result is not None, "Required property 'scale_out_size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def consumed_memory_thresholds(
        self,
    ) -> typing.Optional["VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds"]:
        '''consumed_memory_thresholds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#consumed_memory_thresholds VmwareengineCluster#consumed_memory_thresholds}
        '''
        result = self._values.get("consumed_memory_thresholds")
        return typing.cast(typing.Optional["VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds"], result)

    @builtins.property
    def cpu_thresholds(
        self,
    ) -> typing.Optional["VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds"]:
        '''cpu_thresholds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#cpu_thresholds VmwareengineCluster#cpu_thresholds}
        '''
        result = self._values.get("cpu_thresholds")
        return typing.cast(typing.Optional["VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds"], result)

    @builtins.property
    def storage_thresholds(
        self,
    ) -> typing.Optional["VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds"]:
        '''storage_thresholds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#storage_thresholds VmwareengineCluster#storage_thresholds}
        '''
        result = self._values.get("storage_thresholds")
        return typing.cast(typing.Optional["VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmwareengineClusterAutoscalingSettingsAutoscalingPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vmwareengineCluster.VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds",
    jsii_struct_bases=[],
    name_mapping={"scale_in": "scaleIn", "scale_out": "scaleOut"},
)
class VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds:
    def __init__(self, *, scale_in: jsii.Number, scale_out: jsii.Number) -> None:
        '''
        :param scale_in: The utilization triggering the scale-in operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#scale_in VmwareengineCluster#scale_in}
        :param scale_out: The utilization triggering the scale-out operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#scale_out VmwareengineCluster#scale_out}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ff2762651e204fc01dbf0fb7622735d10a89742213c22545476ef155bc27110)
            check_type(argname="argument scale_in", value=scale_in, expected_type=type_hints["scale_in"])
            check_type(argname="argument scale_out", value=scale_out, expected_type=type_hints["scale_out"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "scale_in": scale_in,
            "scale_out": scale_out,
        }

    @builtins.property
    def scale_in(self) -> jsii.Number:
        '''The utilization triggering the scale-in operation in percent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#scale_in VmwareengineCluster#scale_in}
        '''
        result = self._values.get("scale_in")
        assert result is not None, "Required property 'scale_in' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def scale_out(self) -> jsii.Number:
        '''The utilization triggering the scale-out operation in percent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#scale_out VmwareengineCluster#scale_out}
        '''
        result = self._values.get("scale_out")
        assert result is not None, "Required property 'scale_out' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholdsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareengineCluster.VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholdsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1505700b985495d5f8e53269d850b2c4b1d3fc7af0dbb677aa41c15ca6b2fa1a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="scaleInInput")
    def scale_in_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scaleInInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleOutInput")
    def scale_out_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scaleOutInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleIn")
    def scale_in(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scaleIn"))

    @scale_in.setter
    def scale_in(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87d64e86fc26af5e61bb41aba05dcf23d568b17108645a40a50d973a41edb3d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleIn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scaleOut")
    def scale_out(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scaleOut"))

    @scale_out.setter
    def scale_out(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6daebdf7d3ec1af066e4640bfa84de3f8c59735642526f56823620a078d5e0bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleOut", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds]:
        return typing.cast(typing.Optional[VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11cfd9426cdab03eeda1e60972ec2ed0c3e9bb9df0195bbcbbdf92ea3fac43a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vmwareengineCluster.VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds",
    jsii_struct_bases=[],
    name_mapping={"scale_in": "scaleIn", "scale_out": "scaleOut"},
)
class VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds:
    def __init__(self, *, scale_in: jsii.Number, scale_out: jsii.Number) -> None:
        '''
        :param scale_in: The utilization triggering the scale-in operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#scale_in VmwareengineCluster#scale_in}
        :param scale_out: The utilization triggering the scale-out operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#scale_out VmwareengineCluster#scale_out}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff4e64af07a898e3961deca75d201d658748bce448ba33afe0cdc00b20e73994)
            check_type(argname="argument scale_in", value=scale_in, expected_type=type_hints["scale_in"])
            check_type(argname="argument scale_out", value=scale_out, expected_type=type_hints["scale_out"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "scale_in": scale_in,
            "scale_out": scale_out,
        }

    @builtins.property
    def scale_in(self) -> jsii.Number:
        '''The utilization triggering the scale-in operation in percent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#scale_in VmwareengineCluster#scale_in}
        '''
        result = self._values.get("scale_in")
        assert result is not None, "Required property 'scale_in' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def scale_out(self) -> jsii.Number:
        '''The utilization triggering the scale-out operation in percent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#scale_out VmwareengineCluster#scale_out}
        '''
        result = self._values.get("scale_out")
        assert result is not None, "Required property 'scale_out' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholdsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareengineCluster.VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholdsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8724f1ed67b14706ecbab33d9a015d9e02ec2bf3e336526110c83e251516772)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="scaleInInput")
    def scale_in_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scaleInInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleOutInput")
    def scale_out_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scaleOutInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleIn")
    def scale_in(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scaleIn"))

    @scale_in.setter
    def scale_in(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fb8021663beda1d44a74c27b579e409dd5004c37a11a36a446eba7f2aff7acf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleIn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scaleOut")
    def scale_out(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scaleOut"))

    @scale_out.setter
    def scale_out(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac9a43d83b03bbc12210d4dd6bcfc525cbc2a5a0b88b5b9f63deae4f8641702d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleOut", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds]:
        return typing.cast(typing.Optional[VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b5d50dbe80a3909e1b62617f9f6a847c3996d3d7af8956b99414b40fde45bea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareengineCluster.VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__851f4f1fcf98af1b6d67d30675e300541b01c717b724b0b6bc82233d54eae462)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d30e27f7138e9a28b00ce8b927c9afc46f2403462f700ad8ee5d887336e053c4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__907e43ede104fe71fd1e560a9d4bc7596e330056bd270f1192717820255e63c0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ee0af15a75289f91f31dabb05484739e7ac2d652a0f6b5f225a72bbd247dc24)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c9c8b24f195c006570602e60cf90820266cc1d8768b35fa961e5bfdcdabbf7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmwareengineClusterAutoscalingSettingsAutoscalingPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmwareengineClusterAutoscalingSettingsAutoscalingPolicies]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmwareengineClusterAutoscalingSettingsAutoscalingPolicies]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c120b613564639d9a191c23ccd286521b09660b95da7b3e6b72046f41a860f9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareengineCluster.VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c73001c8ebdd82be78e07c9be14400fd6f472b4ea8dc4864690a676045c370c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putConsumedMemoryThresholds")
    def put_consumed_memory_thresholds(
        self,
        *,
        scale_in: jsii.Number,
        scale_out: jsii.Number,
    ) -> None:
        '''
        :param scale_in: The utilization triggering the scale-in operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#scale_in VmwareengineCluster#scale_in}
        :param scale_out: The utilization triggering the scale-out operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#scale_out VmwareengineCluster#scale_out}
        '''
        value = VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds(
            scale_in=scale_in, scale_out=scale_out
        )

        return typing.cast(None, jsii.invoke(self, "putConsumedMemoryThresholds", [value]))

    @jsii.member(jsii_name="putCpuThresholds")
    def put_cpu_thresholds(
        self,
        *,
        scale_in: jsii.Number,
        scale_out: jsii.Number,
    ) -> None:
        '''
        :param scale_in: The utilization triggering the scale-in operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#scale_in VmwareengineCluster#scale_in}
        :param scale_out: The utilization triggering the scale-out operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#scale_out VmwareengineCluster#scale_out}
        '''
        value = VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds(
            scale_in=scale_in, scale_out=scale_out
        )

        return typing.cast(None, jsii.invoke(self, "putCpuThresholds", [value]))

    @jsii.member(jsii_name="putStorageThresholds")
    def put_storage_thresholds(
        self,
        *,
        scale_in: jsii.Number,
        scale_out: jsii.Number,
    ) -> None:
        '''
        :param scale_in: The utilization triggering the scale-in operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#scale_in VmwareengineCluster#scale_in}
        :param scale_out: The utilization triggering the scale-out operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#scale_out VmwareengineCluster#scale_out}
        '''
        value = VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds(
            scale_in=scale_in, scale_out=scale_out
        )

        return typing.cast(None, jsii.invoke(self, "putStorageThresholds", [value]))

    @jsii.member(jsii_name="resetConsumedMemoryThresholds")
    def reset_consumed_memory_thresholds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsumedMemoryThresholds", []))

    @jsii.member(jsii_name="resetCpuThresholds")
    def reset_cpu_thresholds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuThresholds", []))

    @jsii.member(jsii_name="resetStorageThresholds")
    def reset_storage_thresholds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageThresholds", []))

    @builtins.property
    @jsii.member(jsii_name="consumedMemoryThresholds")
    def consumed_memory_thresholds(
        self,
    ) -> VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholdsOutputReference:
        return typing.cast(VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholdsOutputReference, jsii.get(self, "consumedMemoryThresholds"))

    @builtins.property
    @jsii.member(jsii_name="cpuThresholds")
    def cpu_thresholds(
        self,
    ) -> VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholdsOutputReference:
        return typing.cast(VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholdsOutputReference, jsii.get(self, "cpuThresholds"))

    @builtins.property
    @jsii.member(jsii_name="storageThresholds")
    def storage_thresholds(
        self,
    ) -> "VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholdsOutputReference":
        return typing.cast("VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholdsOutputReference", jsii.get(self, "storageThresholds"))

    @builtins.property
    @jsii.member(jsii_name="autoscalePolicyIdInput")
    def autoscale_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoscalePolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="consumedMemoryThresholdsInput")
    def consumed_memory_thresholds_input(
        self,
    ) -> typing.Optional[VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds]:
        return typing.cast(typing.Optional[VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds], jsii.get(self, "consumedMemoryThresholdsInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuThresholdsInput")
    def cpu_thresholds_input(
        self,
    ) -> typing.Optional[VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds]:
        return typing.cast(typing.Optional[VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds], jsii.get(self, "cpuThresholdsInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeTypeIdInput")
    def node_type_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeTypeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleOutSizeInput")
    def scale_out_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scaleOutSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="storageThresholdsInput")
    def storage_thresholds_input(
        self,
    ) -> typing.Optional["VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds"]:
        return typing.cast(typing.Optional["VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds"], jsii.get(self, "storageThresholdsInput"))

    @builtins.property
    @jsii.member(jsii_name="autoscalePolicyId")
    def autoscale_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoscalePolicyId"))

    @autoscale_policy_id.setter
    def autoscale_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3ddbb8d649daf4ea4072ec9510dba823924ebfed9b8c5285254c6df978921a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoscalePolicyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeTypeId")
    def node_type_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeTypeId"))

    @node_type_id.setter
    def node_type_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d79af7c18d2003ac3631ab27d190a91fd82bb5fc423cba6e13a678e867b090f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeTypeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scaleOutSize")
    def scale_out_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scaleOutSize"))

    @scale_out_size.setter
    def scale_out_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acb972dd5fc21e431b8a0832c7db0e9e6e0abd4eddb038a7482302d9f8b1896f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleOutSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareengineClusterAutoscalingSettingsAutoscalingPolicies]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareengineClusterAutoscalingSettingsAutoscalingPolicies]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareengineClusterAutoscalingSettingsAutoscalingPolicies]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ab99ce4c659b8077c04fbf37b5fce2a9d8149f67fb76d784cba281809aad28f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vmwareengineCluster.VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds",
    jsii_struct_bases=[],
    name_mapping={"scale_in": "scaleIn", "scale_out": "scaleOut"},
)
class VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds:
    def __init__(self, *, scale_in: jsii.Number, scale_out: jsii.Number) -> None:
        '''
        :param scale_in: The utilization triggering the scale-in operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#scale_in VmwareengineCluster#scale_in}
        :param scale_out: The utilization triggering the scale-out operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#scale_out VmwareengineCluster#scale_out}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b086c4ce4a5c772d87404055b8740a3a3de570a31e179f8189a477d0004c2621)
            check_type(argname="argument scale_in", value=scale_in, expected_type=type_hints["scale_in"])
            check_type(argname="argument scale_out", value=scale_out, expected_type=type_hints["scale_out"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "scale_in": scale_in,
            "scale_out": scale_out,
        }

    @builtins.property
    def scale_in(self) -> jsii.Number:
        '''The utilization triggering the scale-in operation in percent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#scale_in VmwareengineCluster#scale_in}
        '''
        result = self._values.get("scale_in")
        assert result is not None, "Required property 'scale_in' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def scale_out(self) -> jsii.Number:
        '''The utilization triggering the scale-out operation in percent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#scale_out VmwareengineCluster#scale_out}
        '''
        result = self._values.get("scale_out")
        assert result is not None, "Required property 'scale_out' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholdsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareengineCluster.VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholdsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__31076be447f0aca3ad13a1d47af2a72b5445b3f5a25f49140f139bd9bec66d8f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="scaleInInput")
    def scale_in_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scaleInInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleOutInput")
    def scale_out_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scaleOutInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleIn")
    def scale_in(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scaleIn"))

    @scale_in.setter
    def scale_in(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85837bd3040f34b6d653343603a0ab48f002a418485703dc41e8118e682fece5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleIn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scaleOut")
    def scale_out(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scaleOut"))

    @scale_out.setter
    def scale_out(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4f38d46c86d5904120f0177b1e5f2ce524ff7276b298dd2587bddade47e7f26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleOut", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds]:
        return typing.cast(typing.Optional[VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85217ddadebaf837e9d2976c7ce502e3fc5232d338fd49f0e51ad6226fa72bd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VmwareengineClusterAutoscalingSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareengineCluster.VmwareengineClusterAutoscalingSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__40e808928e762c1ab153de6c6d8bb14bd2663bfbdeb23c4737753d14475ef93f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutoscalingPolicies")
    def put_autoscaling_policies(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmwareengineClusterAutoscalingSettingsAutoscalingPolicies, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aa6ea4655e43845f4754f0b19d3ab3e30619352cdf1f70d00a172cbe3dc6139)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAutoscalingPolicies", [value]))

    @jsii.member(jsii_name="resetCoolDownPeriod")
    def reset_cool_down_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCoolDownPeriod", []))

    @jsii.member(jsii_name="resetMaxClusterNodeCount")
    def reset_max_cluster_node_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxClusterNodeCount", []))

    @jsii.member(jsii_name="resetMinClusterNodeCount")
    def reset_min_cluster_node_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinClusterNodeCount", []))

    @builtins.property
    @jsii.member(jsii_name="autoscalingPolicies")
    def autoscaling_policies(
        self,
    ) -> VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesList:
        return typing.cast(VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesList, jsii.get(self, "autoscalingPolicies"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingPoliciesInput")
    def autoscaling_policies_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmwareengineClusterAutoscalingSettingsAutoscalingPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmwareengineClusterAutoscalingSettingsAutoscalingPolicies]]], jsii.get(self, "autoscalingPoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="coolDownPeriodInput")
    def cool_down_period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "coolDownPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="maxClusterNodeCountInput")
    def max_cluster_node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxClusterNodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="minClusterNodeCountInput")
    def min_cluster_node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minClusterNodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="coolDownPeriod")
    def cool_down_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "coolDownPeriod"))

    @cool_down_period.setter
    def cool_down_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa4e0e9d0a71f557fa3da3b020b202a71f7450474cdf8915c4b58fd017889705)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coolDownPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxClusterNodeCount")
    def max_cluster_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxClusterNodeCount"))

    @max_cluster_node_count.setter
    def max_cluster_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d54efa78cfe51e2f1057e55e7c11b42584c97c91aa19cad85ffd8e7ec18b92a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxClusterNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minClusterNodeCount")
    def min_cluster_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minClusterNodeCount"))

    @min_cluster_node_count.setter
    def min_cluster_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2943e7363db2429b48ce956e93b1f86955c8d12c2cd81f3e2178880959b04374)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minClusterNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VmwareengineClusterAutoscalingSettings]:
        return typing.cast(typing.Optional[VmwareengineClusterAutoscalingSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VmwareengineClusterAutoscalingSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a667ce6bfe73076c243bdb7f1cec8ba02e96ae600dcda658fe8d2a0d672264a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vmwareengineCluster.VmwareengineClusterConfig",
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
        "parent": "parent",
        "autoscaling_settings": "autoscalingSettings",
        "id": "id",
        "node_type_configs": "nodeTypeConfigs",
        "timeouts": "timeouts",
    },
)
class VmwareengineClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        parent: builtins.str,
        autoscaling_settings: typing.Optional[typing.Union[VmwareengineClusterAutoscalingSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        node_type_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VmwareengineClusterNodeTypeConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["VmwareengineClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The ID of the Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#name VmwareengineCluster#name}
        :param parent: The resource name of the private cloud to create a new cluster in. Resource names are schemeless URIs that follow the conventions in https://cloud.google.com/apis/design/resource_names. For example: projects/my-project/locations/us-west1-a/privateClouds/my-cloud Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#parent VmwareengineCluster#parent}
        :param autoscaling_settings: autoscaling_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#autoscaling_settings VmwareengineCluster#autoscaling_settings}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#id VmwareengineCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param node_type_configs: node_type_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#node_type_configs VmwareengineCluster#node_type_configs}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#timeouts VmwareengineCluster#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(autoscaling_settings, dict):
            autoscaling_settings = VmwareengineClusterAutoscalingSettings(**autoscaling_settings)
        if isinstance(timeouts, dict):
            timeouts = VmwareengineClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a10cc83340504cab685017b4874759cc7cf617dba1ba08fe3aca25a461c608d7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument autoscaling_settings", value=autoscaling_settings, expected_type=type_hints["autoscaling_settings"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument node_type_configs", value=node_type_configs, expected_type=type_hints["node_type_configs"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "parent": parent,
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
        if autoscaling_settings is not None:
            self._values["autoscaling_settings"] = autoscaling_settings
        if id is not None:
            self._values["id"] = id
        if node_type_configs is not None:
            self._values["node_type_configs"] = node_type_configs
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
    def name(self) -> builtins.str:
        '''The ID of the Cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#name VmwareengineCluster#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parent(self) -> builtins.str:
        '''The resource name of the private cloud to create a new cluster in.

        Resource names are schemeless URIs that follow the conventions in https://cloud.google.com/apis/design/resource_names.
        For example: projects/my-project/locations/us-west1-a/privateClouds/my-cloud

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#parent VmwareengineCluster#parent}
        '''
        result = self._values.get("parent")
        assert result is not None, "Required property 'parent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def autoscaling_settings(
        self,
    ) -> typing.Optional[VmwareengineClusterAutoscalingSettings]:
        '''autoscaling_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#autoscaling_settings VmwareengineCluster#autoscaling_settings}
        '''
        result = self._values.get("autoscaling_settings")
        return typing.cast(typing.Optional[VmwareengineClusterAutoscalingSettings], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#id VmwareengineCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_type_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmwareengineClusterNodeTypeConfigs"]]]:
        '''node_type_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#node_type_configs VmwareengineCluster#node_type_configs}
        '''
        result = self._values.get("node_type_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VmwareengineClusterNodeTypeConfigs"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["VmwareengineClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#timeouts VmwareengineCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["VmwareengineClusterTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmwareengineClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vmwareengineCluster.VmwareengineClusterNodeTypeConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "node_count": "nodeCount",
        "node_type_id": "nodeTypeId",
        "custom_core_count": "customCoreCount",
    },
)
class VmwareengineClusterNodeTypeConfigs:
    def __init__(
        self,
        *,
        node_count: jsii.Number,
        node_type_id: builtins.str,
        custom_core_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param node_count: The number of nodes of this type in the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#node_count VmwareengineCluster#node_count}
        :param node_type_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#node_type_id VmwareengineCluster#node_type_id}.
        :param custom_core_count: Customized number of cores available to each node of the type. This number must always be one of 'nodeType.availableCustomCoreCounts'. If zero is provided max value from 'nodeType.availableCustomCoreCounts' will be used. Once the customer is created then corecount cannot be changed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#custom_core_count VmwareengineCluster#custom_core_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9e8436a0c2af498bab3da727e7ac830a8f6e9f73ffa89b73ee5205d29a75d56)
            check_type(argname="argument node_count", value=node_count, expected_type=type_hints["node_count"])
            check_type(argname="argument node_type_id", value=node_type_id, expected_type=type_hints["node_type_id"])
            check_type(argname="argument custom_core_count", value=custom_core_count, expected_type=type_hints["custom_core_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "node_count": node_count,
            "node_type_id": node_type_id,
        }
        if custom_core_count is not None:
            self._values["custom_core_count"] = custom_core_count

    @builtins.property
    def node_count(self) -> jsii.Number:
        '''The number of nodes of this type in the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#node_count VmwareengineCluster#node_count}
        '''
        result = self._values.get("node_count")
        assert result is not None, "Required property 'node_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def node_type_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#node_type_id VmwareengineCluster#node_type_id}.'''
        result = self._values.get("node_type_id")
        assert result is not None, "Required property 'node_type_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_core_count(self) -> typing.Optional[jsii.Number]:
        '''Customized number of cores available to each node of the type.

        This number must always be one of 'nodeType.availableCustomCoreCounts'.
        If zero is provided max value from 'nodeType.availableCustomCoreCounts' will be used.
        Once the customer is created then corecount cannot be changed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#custom_core_count VmwareengineCluster#custom_core_count}
        '''
        result = self._values.get("custom_core_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmwareengineClusterNodeTypeConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VmwareengineClusterNodeTypeConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareengineCluster.VmwareengineClusterNodeTypeConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b75b6806acefba58a6e46202d677d7b875968ff8e8e9881fd90f8c0d3b8abfde)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VmwareengineClusterNodeTypeConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d78c879b500e1d9d2a50e797e7a27ff787f161048bc65f8f60cc494361e6fc4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VmwareengineClusterNodeTypeConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f49e2fe3089a79aee79d6fd66c1db54b002c7a66249dacde69e92001b663567)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9be61d8f572715c2cd074746d4fd197915e149977fb39de2e14421c729480d5f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__60c9b996d1aa2a4b39bdcb7c35b69f52c48929a757cbe6371a1524c1d68d548c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmwareengineClusterNodeTypeConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmwareengineClusterNodeTypeConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmwareengineClusterNodeTypeConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a85b2fd399529775235d46da8f1b423ec731cc07a658e57633d429fb6894affd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VmwareengineClusterNodeTypeConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareengineCluster.VmwareengineClusterNodeTypeConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e44c6ed7959876efb03194eaed2c5a557bc97038c381046f5909c8b1a4c9221c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCustomCoreCount")
    def reset_custom_core_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomCoreCount", []))

    @builtins.property
    @jsii.member(jsii_name="customCoreCountInput")
    def custom_core_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "customCoreCountInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeCountInput")
    def node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeTypeIdInput")
    def node_type_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeTypeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="customCoreCount")
    def custom_core_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "customCoreCount"))

    @custom_core_count.setter
    def custom_core_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0da3f408aeb6f9e0787d64bbabbd5ad3989caaa2decf248f79f5a7b61b106a8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customCoreCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeCount")
    def node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodeCount"))

    @node_count.setter
    def node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8673f44ced85a24a20cdee914d9ca95878122ed6cbcefbd2960c242335fb7bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeTypeId")
    def node_type_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeTypeId"))

    @node_type_id.setter
    def node_type_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__963cb8eccedc6765b2b28c1ddeb21a8d399435b8145c36012ba210aa77d995e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeTypeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareengineClusterNodeTypeConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareengineClusterNodeTypeConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareengineClusterNodeTypeConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__892a5851f44f5add26c5deb3f7a8f7f8c22b6048d13a3da4cf1f05d768f4a958)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vmwareengineCluster.VmwareengineClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class VmwareengineClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#create VmwareengineCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#delete VmwareengineCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#update VmwareengineCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4cdeafba0e5a76f0c31e01e4dc419d5f81c4cab14ecc379d2e428ab65215a9f)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#create VmwareengineCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#delete VmwareengineCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vmwareengine_cluster#update VmwareengineCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VmwareengineClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VmwareengineClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vmwareengineCluster.VmwareengineClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__181cef034111cbb24705856588d5e753b21cb99760acfd92568ac0381331345d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__95726fb26c21d13f822fa2780ee4114e2428e2aa9fb8292fa87c725c0d686b92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a35158cf458b7f17dce91b08c1769234ba8fb7ff32b20cc570f505c40b7e0710)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18e8040da2a588a31102e32ea4fc6a78c7dbd498d7beab028581d90ca8875620)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareengineClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareengineClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareengineClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b546522ef59b35cdf6373fd12994f2776e3152653889a7e2d9437d44051cb6d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "VmwareengineCluster",
    "VmwareengineClusterAutoscalingSettings",
    "VmwareengineClusterAutoscalingSettingsAutoscalingPolicies",
    "VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds",
    "VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholdsOutputReference",
    "VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds",
    "VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholdsOutputReference",
    "VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesList",
    "VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesOutputReference",
    "VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds",
    "VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholdsOutputReference",
    "VmwareengineClusterAutoscalingSettingsOutputReference",
    "VmwareengineClusterConfig",
    "VmwareengineClusterNodeTypeConfigs",
    "VmwareengineClusterNodeTypeConfigsList",
    "VmwareengineClusterNodeTypeConfigsOutputReference",
    "VmwareengineClusterTimeouts",
    "VmwareengineClusterTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__ec59fac37670f356047b837130a2e57f7298727b62beba4a3efda8ea657450cf(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    parent: builtins.str,
    autoscaling_settings: typing.Optional[typing.Union[VmwareengineClusterAutoscalingSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    node_type_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmwareengineClusterNodeTypeConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[VmwareengineClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__357f64cd22e55cbf90b54ef11938276ca3c19474255214329f35c64103a103da(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1002d8990a89bd4f17af5fc2c962b636b0ad99490d6fd80119c756ecc20c7d91(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmwareengineClusterNodeTypeConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a6be2d8e44774009d1a145aedd4399eba9989a31d258d2e3f2b9174793ba87c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d021b87d3963195add2eb878447922e1fa29ba4a0652547f28d857e89369342(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66a67c6fa9ff0f1f64dea5534f3bb0a7ccf5992591ba1a44ed18bba1f8689c46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3ed31e75e258ea44b4e47131de64c6bc645e073ada612fd8e8609be5d623330(
    *,
    autoscaling_policies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmwareengineClusterAutoscalingSettingsAutoscalingPolicies, typing.Dict[builtins.str, typing.Any]]]],
    cool_down_period: typing.Optional[builtins.str] = None,
    max_cluster_node_count: typing.Optional[jsii.Number] = None,
    min_cluster_node_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1eee777c6d706b3ed67349da0e387acb0d3438239b403a54bd910aec07ce382(
    *,
    autoscale_policy_id: builtins.str,
    node_type_id: builtins.str,
    scale_out_size: jsii.Number,
    consumed_memory_thresholds: typing.Optional[typing.Union[VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds, typing.Dict[builtins.str, typing.Any]]] = None,
    cpu_thresholds: typing.Optional[typing.Union[VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_thresholds: typing.Optional[typing.Union[VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ff2762651e204fc01dbf0fb7622735d10a89742213c22545476ef155bc27110(
    *,
    scale_in: jsii.Number,
    scale_out: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1505700b985495d5f8e53269d850b2c4b1d3fc7af0dbb677aa41c15ca6b2fa1a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87d64e86fc26af5e61bb41aba05dcf23d568b17108645a40a50d973a41edb3d3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6daebdf7d3ec1af066e4640bfa84de3f8c59735642526f56823620a078d5e0bd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11cfd9426cdab03eeda1e60972ec2ed0c3e9bb9df0195bbcbbdf92ea3fac43a5(
    value: typing.Optional[VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff4e64af07a898e3961deca75d201d658748bce448ba33afe0cdc00b20e73994(
    *,
    scale_in: jsii.Number,
    scale_out: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8724f1ed67b14706ecbab33d9a015d9e02ec2bf3e336526110c83e251516772(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fb8021663beda1d44a74c27b579e409dd5004c37a11a36a446eba7f2aff7acf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac9a43d83b03bbc12210d4dd6bcfc525cbc2a5a0b88b5b9f63deae4f8641702d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b5d50dbe80a3909e1b62617f9f6a847c3996d3d7af8956b99414b40fde45bea(
    value: typing.Optional[VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__851f4f1fcf98af1b6d67d30675e300541b01c717b724b0b6bc82233d54eae462(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d30e27f7138e9a28b00ce8b927c9afc46f2403462f700ad8ee5d887336e053c4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__907e43ede104fe71fd1e560a9d4bc7596e330056bd270f1192717820255e63c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ee0af15a75289f91f31dabb05484739e7ac2d652a0f6b5f225a72bbd247dc24(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c9c8b24f195c006570602e60cf90820266cc1d8768b35fa961e5bfdcdabbf7f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c120b613564639d9a191c23ccd286521b09660b95da7b3e6b72046f41a860f9c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmwareengineClusterAutoscalingSettingsAutoscalingPolicies]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c73001c8ebdd82be78e07c9be14400fd6f472b4ea8dc4864690a676045c370c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3ddbb8d649daf4ea4072ec9510dba823924ebfed9b8c5285254c6df978921a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d79af7c18d2003ac3631ab27d190a91fd82bb5fc423cba6e13a678e867b090f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acb972dd5fc21e431b8a0832c7db0e9e6e0abd4eddb038a7482302d9f8b1896f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ab99ce4c659b8077c04fbf37b5fce2a9d8149f67fb76d784cba281809aad28f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareengineClusterAutoscalingSettingsAutoscalingPolicies]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b086c4ce4a5c772d87404055b8740a3a3de570a31e179f8189a477d0004c2621(
    *,
    scale_in: jsii.Number,
    scale_out: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31076be447f0aca3ad13a1d47af2a72b5445b3f5a25f49140f139bd9bec66d8f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85837bd3040f34b6d653343603a0ab48f002a418485703dc41e8118e682fece5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4f38d46c86d5904120f0177b1e5f2ce524ff7276b298dd2587bddade47e7f26(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85217ddadebaf837e9d2976c7ce502e3fc5232d338fd49f0e51ad6226fa72bd1(
    value: typing.Optional[VmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40e808928e762c1ab153de6c6d8bb14bd2663bfbdeb23c4737753d14475ef93f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aa6ea4655e43845f4754f0b19d3ab3e30619352cdf1f70d00a172cbe3dc6139(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmwareengineClusterAutoscalingSettingsAutoscalingPolicies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa4e0e9d0a71f557fa3da3b020b202a71f7450474cdf8915c4b58fd017889705(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d54efa78cfe51e2f1057e55e7c11b42584c97c91aa19cad85ffd8e7ec18b92a9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2943e7363db2429b48ce956e93b1f86955c8d12c2cd81f3e2178880959b04374(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a667ce6bfe73076c243bdb7f1cec8ba02e96ae600dcda658fe8d2a0d672264a0(
    value: typing.Optional[VmwareengineClusterAutoscalingSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a10cc83340504cab685017b4874759cc7cf617dba1ba08fe3aca25a461c608d7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    parent: builtins.str,
    autoscaling_settings: typing.Optional[typing.Union[VmwareengineClusterAutoscalingSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    node_type_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VmwareengineClusterNodeTypeConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[VmwareengineClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9e8436a0c2af498bab3da727e7ac830a8f6e9f73ffa89b73ee5205d29a75d56(
    *,
    node_count: jsii.Number,
    node_type_id: builtins.str,
    custom_core_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b75b6806acefba58a6e46202d677d7b875968ff8e8e9881fd90f8c0d3b8abfde(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d78c879b500e1d9d2a50e797e7a27ff787f161048bc65f8f60cc494361e6fc4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f49e2fe3089a79aee79d6fd66c1db54b002c7a66249dacde69e92001b663567(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9be61d8f572715c2cd074746d4fd197915e149977fb39de2e14421c729480d5f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60c9b996d1aa2a4b39bdcb7c35b69f52c48929a757cbe6371a1524c1d68d548c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a85b2fd399529775235d46da8f1b423ec731cc07a658e57633d429fb6894affd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VmwareengineClusterNodeTypeConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e44c6ed7959876efb03194eaed2c5a557bc97038c381046f5909c8b1a4c9221c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0da3f408aeb6f9e0787d64bbabbd5ad3989caaa2decf248f79f5a7b61b106a8f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8673f44ced85a24a20cdee914d9ca95878122ed6cbcefbd2960c242335fb7bf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__963cb8eccedc6765b2b28c1ddeb21a8d399435b8145c36012ba210aa77d995e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__892a5851f44f5add26c5deb3f7a8f7f8c22b6048d13a3da4cf1f05d768f4a958(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareengineClusterNodeTypeConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4cdeafba0e5a76f0c31e01e4dc419d5f81c4cab14ecc379d2e428ab65215a9f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__181cef034111cbb24705856588d5e753b21cb99760acfd92568ac0381331345d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95726fb26c21d13f822fa2780ee4114e2428e2aa9fb8292fa87c725c0d686b92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a35158cf458b7f17dce91b08c1769234ba8fb7ff32b20cc570f505c40b7e0710(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18e8040da2a588a31102e32ea4fc6a78c7dbd498d7beab028581d90ca8875620(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b546522ef59b35cdf6373fd12994f2776e3152653889a7e2d9437d44051cb6d7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VmwareengineClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
