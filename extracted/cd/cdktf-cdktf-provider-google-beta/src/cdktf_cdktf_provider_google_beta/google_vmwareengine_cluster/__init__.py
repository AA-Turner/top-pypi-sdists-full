r'''
# `google_vmwareengine_cluster`

Refer to the Terraform Registry for docs: [`google_vmwareengine_cluster`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster).
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


class GoogleVmwareengineCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVmwareengineCluster.GoogleVmwareengineCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster google_vmwareengine_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        parent: builtins.str,
        autoscaling_settings: typing.Optional[typing.Union["GoogleVmwareengineClusterAutoscalingSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        node_type_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleVmwareengineClusterNodeTypeConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleVmwareengineClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster google_vmwareengine_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The ID of the Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#name GoogleVmwareengineCluster#name}
        :param parent: The resource name of the private cloud to create a new cluster in. Resource names are schemeless URIs that follow the conventions in https://cloud.google.com/apis/design/resource_names. For example: projects/my-project/locations/us-west1-a/privateClouds/my-cloud Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#parent GoogleVmwareengineCluster#parent}
        :param autoscaling_settings: autoscaling_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#autoscaling_settings GoogleVmwareengineCluster#autoscaling_settings}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#id GoogleVmwareengineCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param node_type_configs: node_type_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#node_type_configs GoogleVmwareengineCluster#node_type_configs}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#timeouts GoogleVmwareengineCluster#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__509c0f04532297955459e2765e2d2c046999ea2b2f75fd38974ec54c07453a10)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleVmwareengineClusterConfig(
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
        '''Generates CDKTF code for importing a GoogleVmwareengineCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleVmwareengineCluster to import.
        :param import_from_id: The id of the existing GoogleVmwareengineCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleVmwareengineCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfcfd58fea41363fbb8895f679a408f0524a82c8ea3e75507e2b8a9888ad4895)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAutoscalingSettings")
    def put_autoscaling_settings(
        self,
        *,
        autoscaling_policies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPolicies", typing.Dict[builtins.str, typing.Any]]]],
        cool_down_period: typing.Optional[builtins.str] = None,
        max_cluster_node_count: typing.Optional[jsii.Number] = None,
        min_cluster_node_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param autoscaling_policies: autoscaling_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#autoscaling_policies GoogleVmwareengineCluster#autoscaling_policies}
        :param cool_down_period: The minimum duration between consecutive autoscale operations. It starts once addition or removal of nodes is fully completed. Minimum cool down period is 30m. Cool down period must be in whole minutes (for example, 30m, 31m, 50m). Mandatory for successful addition of autoscaling settings in cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#cool_down_period GoogleVmwareengineCluster#cool_down_period}
        :param max_cluster_node_count: Maximum number of nodes of any type in a cluster. Mandatory for successful addition of autoscaling settings in cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#max_cluster_node_count GoogleVmwareengineCluster#max_cluster_node_count}
        :param min_cluster_node_count: Minimum number of nodes of any type in a cluster. Mandatory for successful addition of autoscaling settings in cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#min_cluster_node_count GoogleVmwareengineCluster#min_cluster_node_count}
        '''
        value = GoogleVmwareengineClusterAutoscalingSettings(
            autoscaling_policies=autoscaling_policies,
            cool_down_period=cool_down_period,
            max_cluster_node_count=max_cluster_node_count,
            min_cluster_node_count=min_cluster_node_count,
        )

        return typing.cast(None, jsii.invoke(self, "putAutoscalingSettings", [value]))

    @jsii.member(jsii_name="putNodeTypeConfigs")
    def put_node_type_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleVmwareengineClusterNodeTypeConfigs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81377ad7c41ab0008b3cae2abec527107ded766b178fed46158ec221b850013f)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#create GoogleVmwareengineCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#delete GoogleVmwareengineCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#update GoogleVmwareengineCluster#update}.
        '''
        value = GoogleVmwareengineClusterTimeouts(
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
    ) -> "GoogleVmwareengineClusterAutoscalingSettingsOutputReference":
        return typing.cast("GoogleVmwareengineClusterAutoscalingSettingsOutputReference", jsii.get(self, "autoscalingSettings"))

    @builtins.property
    @jsii.member(jsii_name="management")
    def management(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "management"))

    @builtins.property
    @jsii.member(jsii_name="nodeTypeConfigs")
    def node_type_configs(self) -> "GoogleVmwareengineClusterNodeTypeConfigsList":
        return typing.cast("GoogleVmwareengineClusterNodeTypeConfigsList", jsii.get(self, "nodeTypeConfigs"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleVmwareengineClusterTimeoutsOutputReference":
        return typing.cast("GoogleVmwareengineClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingSettingsInput")
    def autoscaling_settings_input(
        self,
    ) -> typing.Optional["GoogleVmwareengineClusterAutoscalingSettings"]:
        return typing.cast(typing.Optional["GoogleVmwareengineClusterAutoscalingSettings"], jsii.get(self, "autoscalingSettingsInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVmwareengineClusterNodeTypeConfigs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVmwareengineClusterNodeTypeConfigs"]]], jsii.get(self, "nodeTypeConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="parentInput")
    def parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleVmwareengineClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleVmwareengineClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__664fbd8fcbfa16f7a34d13d72513936b35a69b24978b60fd476ac09f4700dc3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__441590dca8ddcc11bf9c65a7460b4cc198de45a0ee9c2555df80c1bfc7b4268b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73e9816cb41e82d96bef02ea6ce611e6f6f319eb9f63dea59ef35df4c20b2a42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVmwareengineCluster.GoogleVmwareengineClusterAutoscalingSettings",
    jsii_struct_bases=[],
    name_mapping={
        "autoscaling_policies": "autoscalingPolicies",
        "cool_down_period": "coolDownPeriod",
        "max_cluster_node_count": "maxClusterNodeCount",
        "min_cluster_node_count": "minClusterNodeCount",
    },
)
class GoogleVmwareengineClusterAutoscalingSettings:
    def __init__(
        self,
        *,
        autoscaling_policies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPolicies", typing.Dict[builtins.str, typing.Any]]]],
        cool_down_period: typing.Optional[builtins.str] = None,
        max_cluster_node_count: typing.Optional[jsii.Number] = None,
        min_cluster_node_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param autoscaling_policies: autoscaling_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#autoscaling_policies GoogleVmwareengineCluster#autoscaling_policies}
        :param cool_down_period: The minimum duration between consecutive autoscale operations. It starts once addition or removal of nodes is fully completed. Minimum cool down period is 30m. Cool down period must be in whole minutes (for example, 30m, 31m, 50m). Mandatory for successful addition of autoscaling settings in cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#cool_down_period GoogleVmwareengineCluster#cool_down_period}
        :param max_cluster_node_count: Maximum number of nodes of any type in a cluster. Mandatory for successful addition of autoscaling settings in cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#max_cluster_node_count GoogleVmwareengineCluster#max_cluster_node_count}
        :param min_cluster_node_count: Minimum number of nodes of any type in a cluster. Mandatory for successful addition of autoscaling settings in cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#min_cluster_node_count GoogleVmwareengineCluster#min_cluster_node_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7b9c55e112f0b13135710b144f382671b98b9bbf848d13d247d0b575b620ff4)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPolicies"]]:
        '''autoscaling_policies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#autoscaling_policies GoogleVmwareengineCluster#autoscaling_policies}
        '''
        result = self._values.get("autoscaling_policies")
        assert result is not None, "Required property 'autoscaling_policies' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPolicies"]], result)

    @builtins.property
    def cool_down_period(self) -> typing.Optional[builtins.str]:
        '''The minimum duration between consecutive autoscale operations.

        It starts once addition or removal of nodes is fully completed.
        Minimum cool down period is 30m.
        Cool down period must be in whole minutes (for example, 30m, 31m, 50m).
        Mandatory for successful addition of autoscaling settings in cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#cool_down_period GoogleVmwareengineCluster#cool_down_period}
        '''
        result = self._values.get("cool_down_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_cluster_node_count(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of nodes of any type in a cluster. Mandatory for successful addition of autoscaling settings in cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#max_cluster_node_count GoogleVmwareengineCluster#max_cluster_node_count}
        '''
        result = self._values.get("max_cluster_node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_cluster_node_count(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of nodes of any type in a cluster. Mandatory for successful addition of autoscaling settings in cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#min_cluster_node_count GoogleVmwareengineCluster#min_cluster_node_count}
        '''
        result = self._values.get("min_cluster_node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVmwareengineClusterAutoscalingSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVmwareengineCluster.GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPolicies",
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
class GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPolicies:
    def __init__(
        self,
        *,
        autoscale_policy_id: builtins.str,
        node_type_id: builtins.str,
        scale_out_size: jsii.Number,
        consumed_memory_thresholds: typing.Optional[typing.Union["GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds", typing.Dict[builtins.str, typing.Any]]] = None,
        cpu_thresholds: typing.Optional[typing.Union["GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_thresholds: typing.Optional[typing.Union["GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param autoscale_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#autoscale_policy_id GoogleVmwareengineCluster#autoscale_policy_id}.
        :param node_type_id: The canonical identifier of the node type to add or remove. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#node_type_id GoogleVmwareengineCluster#node_type_id}
        :param scale_out_size: Number of nodes to add to a cluster during a scale-out operation. Must be divisible by 2 for stretched clusters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#scale_out_size GoogleVmwareengineCluster#scale_out_size}
        :param consumed_memory_thresholds: consumed_memory_thresholds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#consumed_memory_thresholds GoogleVmwareengineCluster#consumed_memory_thresholds}
        :param cpu_thresholds: cpu_thresholds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#cpu_thresholds GoogleVmwareengineCluster#cpu_thresholds}
        :param storage_thresholds: storage_thresholds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#storage_thresholds GoogleVmwareengineCluster#storage_thresholds}
        '''
        if isinstance(consumed_memory_thresholds, dict):
            consumed_memory_thresholds = GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds(**consumed_memory_thresholds)
        if isinstance(cpu_thresholds, dict):
            cpu_thresholds = GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds(**cpu_thresholds)
        if isinstance(storage_thresholds, dict):
            storage_thresholds = GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds(**storage_thresholds)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aecd97865948f6ff144d9cda8b9a170a38d3e960c98ccf3432830e6dd977ba0)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#autoscale_policy_id GoogleVmwareengineCluster#autoscale_policy_id}.'''
        result = self._values.get("autoscale_policy_id")
        assert result is not None, "Required property 'autoscale_policy_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def node_type_id(self) -> builtins.str:
        '''The canonical identifier of the node type to add or remove.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#node_type_id GoogleVmwareengineCluster#node_type_id}
        '''
        result = self._values.get("node_type_id")
        assert result is not None, "Required property 'node_type_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scale_out_size(self) -> jsii.Number:
        '''Number of nodes to add to a cluster during a scale-out operation. Must be divisible by 2 for stretched clusters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#scale_out_size GoogleVmwareengineCluster#scale_out_size}
        '''
        result = self._values.get("scale_out_size")
        assert result is not None, "Required property 'scale_out_size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def consumed_memory_thresholds(
        self,
    ) -> typing.Optional["GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds"]:
        '''consumed_memory_thresholds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#consumed_memory_thresholds GoogleVmwareengineCluster#consumed_memory_thresholds}
        '''
        result = self._values.get("consumed_memory_thresholds")
        return typing.cast(typing.Optional["GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds"], result)

    @builtins.property
    def cpu_thresholds(
        self,
    ) -> typing.Optional["GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds"]:
        '''cpu_thresholds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#cpu_thresholds GoogleVmwareengineCluster#cpu_thresholds}
        '''
        result = self._values.get("cpu_thresholds")
        return typing.cast(typing.Optional["GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds"], result)

    @builtins.property
    def storage_thresholds(
        self,
    ) -> typing.Optional["GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds"]:
        '''storage_thresholds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#storage_thresholds GoogleVmwareengineCluster#storage_thresholds}
        '''
        result = self._values.get("storage_thresholds")
        return typing.cast(typing.Optional["GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVmwareengineCluster.GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds",
    jsii_struct_bases=[],
    name_mapping={"scale_in": "scaleIn", "scale_out": "scaleOut"},
)
class GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds:
    def __init__(self, *, scale_in: jsii.Number, scale_out: jsii.Number) -> None:
        '''
        :param scale_in: The utilization triggering the scale-in operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#scale_in GoogleVmwareengineCluster#scale_in}
        :param scale_out: The utilization triggering the scale-out operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#scale_out GoogleVmwareengineCluster#scale_out}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd80e3cac4e7017dff89c197b5957f6f06c002b0cfcb29479f14fc610772a293)
            check_type(argname="argument scale_in", value=scale_in, expected_type=type_hints["scale_in"])
            check_type(argname="argument scale_out", value=scale_out, expected_type=type_hints["scale_out"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "scale_in": scale_in,
            "scale_out": scale_out,
        }

    @builtins.property
    def scale_in(self) -> jsii.Number:
        '''The utilization triggering the scale-in operation in percent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#scale_in GoogleVmwareengineCluster#scale_in}
        '''
        result = self._values.get("scale_in")
        assert result is not None, "Required property 'scale_in' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def scale_out(self) -> jsii.Number:
        '''The utilization triggering the scale-out operation in percent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#scale_out GoogleVmwareengineCluster#scale_out}
        '''
        result = self._values.get("scale_out")
        assert result is not None, "Required property 'scale_out' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholdsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVmwareengineCluster.GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholdsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__827a19e4d406add6d50a960f49459e5111739ed6feb92ed38edb3445a0ce74a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__81e5902cf39396f0450d4e6ad213f622f9911450fb110b607637e108ac874aeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleIn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scaleOut")
    def scale_out(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scaleOut"))

    @scale_out.setter
    def scale_out(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66456d9594f7c8f0ae5627bba7ba7e595799087b1295ca4dfb7c6e0a29946cb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleOut", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds]:
        return typing.cast(typing.Optional[GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b901af917820dbde784155768ee6efa6ac55d8551aca459540d5f9f453717e4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVmwareengineCluster.GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds",
    jsii_struct_bases=[],
    name_mapping={"scale_in": "scaleIn", "scale_out": "scaleOut"},
)
class GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds:
    def __init__(self, *, scale_in: jsii.Number, scale_out: jsii.Number) -> None:
        '''
        :param scale_in: The utilization triggering the scale-in operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#scale_in GoogleVmwareengineCluster#scale_in}
        :param scale_out: The utilization triggering the scale-out operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#scale_out GoogleVmwareengineCluster#scale_out}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__377ddf08ee4dbdd48f80bcc30a4ee5c2a23c5df89730b7c800c354b9a1ce29e3)
            check_type(argname="argument scale_in", value=scale_in, expected_type=type_hints["scale_in"])
            check_type(argname="argument scale_out", value=scale_out, expected_type=type_hints["scale_out"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "scale_in": scale_in,
            "scale_out": scale_out,
        }

    @builtins.property
    def scale_in(self) -> jsii.Number:
        '''The utilization triggering the scale-in operation in percent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#scale_in GoogleVmwareengineCluster#scale_in}
        '''
        result = self._values.get("scale_in")
        assert result is not None, "Required property 'scale_in' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def scale_out(self) -> jsii.Number:
        '''The utilization triggering the scale-out operation in percent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#scale_out GoogleVmwareengineCluster#scale_out}
        '''
        result = self._values.get("scale_out")
        assert result is not None, "Required property 'scale_out' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholdsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVmwareengineCluster.GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholdsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f461afc50c7ce8a8dd412450453fcc1eeff1360a68d92fa69032a1ac43c6467)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f699032548474ad2449c8cba0325bb9d652debf750fa57c0ff7a509ab72af9e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleIn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scaleOut")
    def scale_out(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scaleOut"))

    @scale_out.setter
    def scale_out(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f78e7e459704bc2d47cc0b782cf3f65d8ae9ffad2882cfb13e44c4bd0ed209f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleOut", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds]:
        return typing.cast(typing.Optional[GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb924513b691442d0a793a929e7eb30dee0d925df03b10f5dc0d91d5d58e4073)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVmwareengineCluster.GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e723531fa447d26d565f5a9643e02e32a2600dda21c238bf5c54996b1602459a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a414b2d991098d11db1baf3d81a6efdde4bea0b00cb88e7944eeb5bbf00e0616)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__558dc5a8832e40b18fbd5713cbbccec6fc255534ca1fd01d8bc1b25fcdf152ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc788ff89f6d13594e47077f661da6ebfe27aa1868c867e6add66589149c2acb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f388c9760b89f639e1fcbb04a9610df9488053d1029f32c3a0057a54e136ecef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPolicies]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPolicies]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00ed9ee8badf73bf0f0c2e584aa7e0e88c475f172eb439b3a8431e671e61ab1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVmwareengineCluster.GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3699946c8751af4644bba79ecc5c592a6e2dd3c1f2b4153e12e34d2b7050e3eb)
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
        :param scale_in: The utilization triggering the scale-in operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#scale_in GoogleVmwareengineCluster#scale_in}
        :param scale_out: The utilization triggering the scale-out operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#scale_out GoogleVmwareengineCluster#scale_out}
        '''
        value = GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds(
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
        :param scale_in: The utilization triggering the scale-in operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#scale_in GoogleVmwareengineCluster#scale_in}
        :param scale_out: The utilization triggering the scale-out operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#scale_out GoogleVmwareengineCluster#scale_out}
        '''
        value = GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds(
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
        :param scale_in: The utilization triggering the scale-in operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#scale_in GoogleVmwareengineCluster#scale_in}
        :param scale_out: The utilization triggering the scale-out operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#scale_out GoogleVmwareengineCluster#scale_out}
        '''
        value = GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds(
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
    ) -> GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholdsOutputReference:
        return typing.cast(GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholdsOutputReference, jsii.get(self, "consumedMemoryThresholds"))

    @builtins.property
    @jsii.member(jsii_name="cpuThresholds")
    def cpu_thresholds(
        self,
    ) -> GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholdsOutputReference:
        return typing.cast(GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholdsOutputReference, jsii.get(self, "cpuThresholds"))

    @builtins.property
    @jsii.member(jsii_name="storageThresholds")
    def storage_thresholds(
        self,
    ) -> "GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholdsOutputReference":
        return typing.cast("GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholdsOutputReference", jsii.get(self, "storageThresholds"))

    @builtins.property
    @jsii.member(jsii_name="autoscalePolicyIdInput")
    def autoscale_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoscalePolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="consumedMemoryThresholdsInput")
    def consumed_memory_thresholds_input(
        self,
    ) -> typing.Optional[GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds]:
        return typing.cast(typing.Optional[GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds], jsii.get(self, "consumedMemoryThresholdsInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuThresholdsInput")
    def cpu_thresholds_input(
        self,
    ) -> typing.Optional[GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds]:
        return typing.cast(typing.Optional[GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds], jsii.get(self, "cpuThresholdsInput"))

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
    ) -> typing.Optional["GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds"]:
        return typing.cast(typing.Optional["GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds"], jsii.get(self, "storageThresholdsInput"))

    @builtins.property
    @jsii.member(jsii_name="autoscalePolicyId")
    def autoscale_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoscalePolicyId"))

    @autoscale_policy_id.setter
    def autoscale_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c054753197eaf89f547ca2d8d3f5fcab2c0d84f485cf824b66a1d54602eac30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoscalePolicyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeTypeId")
    def node_type_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeTypeId"))

    @node_type_id.setter
    def node_type_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__725ed3442f9435fd683382332f46d240e3ad9936d8dec576dc373b11db07cf0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeTypeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scaleOutSize")
    def scale_out_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scaleOutSize"))

    @scale_out_size.setter
    def scale_out_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__768ffd94896d59dc1c0bcb5498936eea809795c31348830d4612c7e35a9f4944)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleOutSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPolicies]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPolicies]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPolicies]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2d2ecef13a44ebb0c02f10869b0212be0ffeb334c1248af7ec852778489f13e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVmwareengineCluster.GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds",
    jsii_struct_bases=[],
    name_mapping={"scale_in": "scaleIn", "scale_out": "scaleOut"},
)
class GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds:
    def __init__(self, *, scale_in: jsii.Number, scale_out: jsii.Number) -> None:
        '''
        :param scale_in: The utilization triggering the scale-in operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#scale_in GoogleVmwareengineCluster#scale_in}
        :param scale_out: The utilization triggering the scale-out operation in percent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#scale_out GoogleVmwareengineCluster#scale_out}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__739cdad21afeab096f3eb3734f67a2a3a7d133471fe7a21270eb70ab7ee08496)
            check_type(argname="argument scale_in", value=scale_in, expected_type=type_hints["scale_in"])
            check_type(argname="argument scale_out", value=scale_out, expected_type=type_hints["scale_out"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "scale_in": scale_in,
            "scale_out": scale_out,
        }

    @builtins.property
    def scale_in(self) -> jsii.Number:
        '''The utilization triggering the scale-in operation in percent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#scale_in GoogleVmwareengineCluster#scale_in}
        '''
        result = self._values.get("scale_in")
        assert result is not None, "Required property 'scale_in' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def scale_out(self) -> jsii.Number:
        '''The utilization triggering the scale-out operation in percent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#scale_out GoogleVmwareengineCluster#scale_out}
        '''
        result = self._values.get("scale_out")
        assert result is not None, "Required property 'scale_out' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholdsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVmwareengineCluster.GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholdsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce0ca4420a34c19cb110c0d40e59c60ff706fa9cb052dce9f38df90cf4c2c3b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__954948701a86455091e829a3043e5b1b2a6c119f54fa081661fa4ca2232f02eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleIn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scaleOut")
    def scale_out(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scaleOut"))

    @scale_out.setter
    def scale_out(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__043d8aa42aec206cbd6bd47c4a63fc4d3082b67e75b128883a7ff6e0b0b6c50a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleOut", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds]:
        return typing.cast(typing.Optional[GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e572ad698ada37e082d4c3e965779faa6e2b96541fecc821ed4803d998682e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVmwareengineClusterAutoscalingSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVmwareengineCluster.GoogleVmwareengineClusterAutoscalingSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e580a8ba554daf6f35d3d36545b8594b77e5d2a0e623e345f9e1a0bcfe9c856)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutoscalingPolicies")
    def put_autoscaling_policies(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPolicies, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cf5765d4949a5f46d7814d35195c45a724ddee7f991dcbcb14659b65477969a)
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
    ) -> GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesList:
        return typing.cast(GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesList, jsii.get(self, "autoscalingPolicies"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingPoliciesInput")
    def autoscaling_policies_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPolicies]]], jsii.get(self, "autoscalingPoliciesInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__4f0f38bf668d7b284ab5082f5c7da5866e9ce03d29b9ba99da4bbc7951bceb28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coolDownPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxClusterNodeCount")
    def max_cluster_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxClusterNodeCount"))

    @max_cluster_node_count.setter
    def max_cluster_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31bc4783b5e2b18e49ebe2cef6da7686677ac03aa0e094ea123d3b557256834a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxClusterNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minClusterNodeCount")
    def min_cluster_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minClusterNodeCount"))

    @min_cluster_node_count.setter
    def min_cluster_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cfbefd376ec2d72ab6a9088328a4b9214a14865c7bbbadcd3c843040369db74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minClusterNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVmwareengineClusterAutoscalingSettings]:
        return typing.cast(typing.Optional[GoogleVmwareengineClusterAutoscalingSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVmwareengineClusterAutoscalingSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc51f1f3056d678a758a062b772a19461b7ee29d96e64d28d96a8c0cc70eb47a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVmwareengineCluster.GoogleVmwareengineClusterConfig",
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
class GoogleVmwareengineClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        autoscaling_settings: typing.Optional[typing.Union[GoogleVmwareengineClusterAutoscalingSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        node_type_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleVmwareengineClusterNodeTypeConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleVmwareengineClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The ID of the Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#name GoogleVmwareengineCluster#name}
        :param parent: The resource name of the private cloud to create a new cluster in. Resource names are schemeless URIs that follow the conventions in https://cloud.google.com/apis/design/resource_names. For example: projects/my-project/locations/us-west1-a/privateClouds/my-cloud Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#parent GoogleVmwareengineCluster#parent}
        :param autoscaling_settings: autoscaling_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#autoscaling_settings GoogleVmwareengineCluster#autoscaling_settings}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#id GoogleVmwareengineCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param node_type_configs: node_type_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#node_type_configs GoogleVmwareengineCluster#node_type_configs}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#timeouts GoogleVmwareengineCluster#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(autoscaling_settings, dict):
            autoscaling_settings = GoogleVmwareengineClusterAutoscalingSettings(**autoscaling_settings)
        if isinstance(timeouts, dict):
            timeouts = GoogleVmwareengineClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da355844def8d4c362b86513656a55f324e700dcb8c30a1dc6fe98c41a9b5aa4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#name GoogleVmwareengineCluster#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parent(self) -> builtins.str:
        '''The resource name of the private cloud to create a new cluster in.

        Resource names are schemeless URIs that follow the conventions in https://cloud.google.com/apis/design/resource_names.
        For example: projects/my-project/locations/us-west1-a/privateClouds/my-cloud

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#parent GoogleVmwareengineCluster#parent}
        '''
        result = self._values.get("parent")
        assert result is not None, "Required property 'parent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def autoscaling_settings(
        self,
    ) -> typing.Optional[GoogleVmwareengineClusterAutoscalingSettings]:
        '''autoscaling_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#autoscaling_settings GoogleVmwareengineCluster#autoscaling_settings}
        '''
        result = self._values.get("autoscaling_settings")
        return typing.cast(typing.Optional[GoogleVmwareengineClusterAutoscalingSettings], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#id GoogleVmwareengineCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_type_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVmwareengineClusterNodeTypeConfigs"]]]:
        '''node_type_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#node_type_configs GoogleVmwareengineCluster#node_type_configs}
        '''
        result = self._values.get("node_type_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVmwareengineClusterNodeTypeConfigs"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleVmwareengineClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#timeouts GoogleVmwareengineCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleVmwareengineClusterTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVmwareengineClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVmwareengineCluster.GoogleVmwareengineClusterNodeTypeConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "node_count": "nodeCount",
        "node_type_id": "nodeTypeId",
        "custom_core_count": "customCoreCount",
    },
)
class GoogleVmwareengineClusterNodeTypeConfigs:
    def __init__(
        self,
        *,
        node_count: jsii.Number,
        node_type_id: builtins.str,
        custom_core_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param node_count: The number of nodes of this type in the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#node_count GoogleVmwareengineCluster#node_count}
        :param node_type_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#node_type_id GoogleVmwareengineCluster#node_type_id}.
        :param custom_core_count: Customized number of cores available to each node of the type. This number must always be one of 'nodeType.availableCustomCoreCounts'. If zero is provided max value from 'nodeType.availableCustomCoreCounts' will be used. Once the customer is created then corecount cannot be changed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#custom_core_count GoogleVmwareengineCluster#custom_core_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d8adfa3dd7dd71228c2e500b1159ae56df2992f99ef521aeb515b9171e13d4c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#node_count GoogleVmwareengineCluster#node_count}
        '''
        result = self._values.get("node_count")
        assert result is not None, "Required property 'node_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def node_type_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#node_type_id GoogleVmwareengineCluster#node_type_id}.'''
        result = self._values.get("node_type_id")
        assert result is not None, "Required property 'node_type_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_core_count(self) -> typing.Optional[jsii.Number]:
        '''Customized number of cores available to each node of the type.

        This number must always be one of 'nodeType.availableCustomCoreCounts'.
        If zero is provided max value from 'nodeType.availableCustomCoreCounts' will be used.
        Once the customer is created then corecount cannot be changed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#custom_core_count GoogleVmwareengineCluster#custom_core_count}
        '''
        result = self._values.get("custom_core_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVmwareengineClusterNodeTypeConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVmwareengineClusterNodeTypeConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVmwareengineCluster.GoogleVmwareengineClusterNodeTypeConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__82ed458ca0769a2219f2a8940db904ec498ad24bef373bd7e079d349359441f8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleVmwareengineClusterNodeTypeConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaa9c832a832b8b1518b77854a67fa3bb930cf1ac2abd9ec4ed398631da3d156)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleVmwareengineClusterNodeTypeConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbf56fb3bc7bc7108566ac18c86e434b804592d290a4141f9aa966fd97c8a76a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9db4409ac6e4ad43e7fa7f6c82b5f8ffabc544a129e063fecf4a033b53339134)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5844489aa9a5099b0070efcbf5cc7e21d6b6a97fc2cae1afe540224bc59928ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVmwareengineClusterNodeTypeConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVmwareengineClusterNodeTypeConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVmwareengineClusterNodeTypeConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94fa71b010467a304f4650bf9531e826b7d46051436aaf114b42c55689383953)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVmwareengineClusterNodeTypeConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVmwareengineCluster.GoogleVmwareengineClusterNodeTypeConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e49e615fcc2e57f871b5c2765482dd0b480548d3f4d5b029bf3fe2d1cc538159)
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
            type_hints = typing.get_type_hints(_typecheckingstub__68f35b48e5d64aab597e98acfa6180ebe6e29c6a39dfc785c8b29c3eb45388c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customCoreCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeCount")
    def node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodeCount"))

    @node_count.setter
    def node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc008e2c269497c1d124de712be0eee843fb091c859f425fa30966e5e7470b18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeTypeId")
    def node_type_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeTypeId"))

    @node_type_id.setter
    def node_type_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24c5a24e6cdf04a94d7e58409b98c04c204eae0c8c6f001626b4d10b1df1be7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeTypeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVmwareengineClusterNodeTypeConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVmwareengineClusterNodeTypeConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVmwareengineClusterNodeTypeConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43b88a1a879cbf77683d262784dd45410e98d78310f735500ef63eb216f2f13b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVmwareengineCluster.GoogleVmwareengineClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleVmwareengineClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#create GoogleVmwareengineCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#delete GoogleVmwareengineCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#update GoogleVmwareengineCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f64ad92e8d3414c26c06dd1c382c06bf2365491a7ca3bf92ad149f3383bffa4)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#create GoogleVmwareengineCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#delete GoogleVmwareengineCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vmwareengine_cluster#update GoogleVmwareengineCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVmwareengineClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVmwareengineClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVmwareengineCluster.GoogleVmwareengineClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc2747c1bc32d163960c39f3b04c0a9a6dfc0a4b995877de7ebd1b065d2eee5b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62bf69049505418d44e62e78295809f03454e8f900d459236cf8f0cb0394dfae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac14b827fd0578ea834d10ea71b80493de0dbbdfdb3620c1c6ead9ea12b3f018)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a52081bb33aef9e40aacaa99a32bfc2a3342fdd19550b8be5ac2919df3831dea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVmwareengineClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVmwareengineClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVmwareengineClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acfbf8e29277310a8ade015f039d6165f573ed55b84c3d2c537e54be7b17f3b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleVmwareengineCluster",
    "GoogleVmwareengineClusterAutoscalingSettings",
    "GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPolicies",
    "GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds",
    "GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholdsOutputReference",
    "GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds",
    "GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholdsOutputReference",
    "GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesList",
    "GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesOutputReference",
    "GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds",
    "GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholdsOutputReference",
    "GoogleVmwareengineClusterAutoscalingSettingsOutputReference",
    "GoogleVmwareengineClusterConfig",
    "GoogleVmwareengineClusterNodeTypeConfigs",
    "GoogleVmwareengineClusterNodeTypeConfigsList",
    "GoogleVmwareengineClusterNodeTypeConfigsOutputReference",
    "GoogleVmwareengineClusterTimeouts",
    "GoogleVmwareengineClusterTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__509c0f04532297955459e2765e2d2c046999ea2b2f75fd38974ec54c07453a10(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    parent: builtins.str,
    autoscaling_settings: typing.Optional[typing.Union[GoogleVmwareengineClusterAutoscalingSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    node_type_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVmwareengineClusterNodeTypeConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleVmwareengineClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__cfcfd58fea41363fbb8895f679a408f0524a82c8ea3e75507e2b8a9888ad4895(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81377ad7c41ab0008b3cae2abec527107ded766b178fed46158ec221b850013f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVmwareengineClusterNodeTypeConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__664fbd8fcbfa16f7a34d13d72513936b35a69b24978b60fd476ac09f4700dc3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__441590dca8ddcc11bf9c65a7460b4cc198de45a0ee9c2555df80c1bfc7b4268b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73e9816cb41e82d96bef02ea6ce611e6f6f319eb9f63dea59ef35df4c20b2a42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7b9c55e112f0b13135710b144f382671b98b9bbf848d13d247d0b575b620ff4(
    *,
    autoscaling_policies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPolicies, typing.Dict[builtins.str, typing.Any]]]],
    cool_down_period: typing.Optional[builtins.str] = None,
    max_cluster_node_count: typing.Optional[jsii.Number] = None,
    min_cluster_node_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aecd97865948f6ff144d9cda8b9a170a38d3e960c98ccf3432830e6dd977ba0(
    *,
    autoscale_policy_id: builtins.str,
    node_type_id: builtins.str,
    scale_out_size: jsii.Number,
    consumed_memory_thresholds: typing.Optional[typing.Union[GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds, typing.Dict[builtins.str, typing.Any]]] = None,
    cpu_thresholds: typing.Optional[typing.Union[GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_thresholds: typing.Optional[typing.Union[GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd80e3cac4e7017dff89c197b5957f6f06c002b0cfcb29479f14fc610772a293(
    *,
    scale_in: jsii.Number,
    scale_out: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__827a19e4d406add6d50a960f49459e5111739ed6feb92ed38edb3445a0ce74a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81e5902cf39396f0450d4e6ad213f622f9911450fb110b607637e108ac874aeb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66456d9594f7c8f0ae5627bba7ba7e595799087b1295ca4dfb7c6e0a29946cb8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b901af917820dbde784155768ee6efa6ac55d8551aca459540d5f9f453717e4d(
    value: typing.Optional[GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesConsumedMemoryThresholds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__377ddf08ee4dbdd48f80bcc30a4ee5c2a23c5df89730b7c800c354b9a1ce29e3(
    *,
    scale_in: jsii.Number,
    scale_out: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f461afc50c7ce8a8dd412450453fcc1eeff1360a68d92fa69032a1ac43c6467(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f699032548474ad2449c8cba0325bb9d652debf750fa57c0ff7a509ab72af9e8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f78e7e459704bc2d47cc0b782cf3f65d8ae9ffad2882cfb13e44c4bd0ed209f0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb924513b691442d0a793a929e7eb30dee0d925df03b10f5dc0d91d5d58e4073(
    value: typing.Optional[GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesCpuThresholds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e723531fa447d26d565f5a9643e02e32a2600dda21c238bf5c54996b1602459a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a414b2d991098d11db1baf3d81a6efdde4bea0b00cb88e7944eeb5bbf00e0616(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__558dc5a8832e40b18fbd5713cbbccec6fc255534ca1fd01d8bc1b25fcdf152ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc788ff89f6d13594e47077f661da6ebfe27aa1868c867e6add66589149c2acb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f388c9760b89f639e1fcbb04a9610df9488053d1029f32c3a0057a54e136ecef(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00ed9ee8badf73bf0f0c2e584aa7e0e88c475f172eb439b3a8431e671e61ab1a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPolicies]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3699946c8751af4644bba79ecc5c592a6e2dd3c1f2b4153e12e34d2b7050e3eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c054753197eaf89f547ca2d8d3f5fcab2c0d84f485cf824b66a1d54602eac30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__725ed3442f9435fd683382332f46d240e3ad9936d8dec576dc373b11db07cf0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__768ffd94896d59dc1c0bcb5498936eea809795c31348830d4612c7e35a9f4944(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2d2ecef13a44ebb0c02f10869b0212be0ffeb334c1248af7ec852778489f13e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPolicies]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__739cdad21afeab096f3eb3734f67a2a3a7d133471fe7a21270eb70ab7ee08496(
    *,
    scale_in: jsii.Number,
    scale_out: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce0ca4420a34c19cb110c0d40e59c60ff706fa9cb052dce9f38df90cf4c2c3b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__954948701a86455091e829a3043e5b1b2a6c119f54fa081661fa4ca2232f02eb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__043d8aa42aec206cbd6bd47c4a63fc4d3082b67e75b128883a7ff6e0b0b6c50a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e572ad698ada37e082d4c3e965779faa6e2b96541fecc821ed4803d998682e9(
    value: typing.Optional[GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPoliciesStorageThresholds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e580a8ba554daf6f35d3d36545b8594b77e5d2a0e623e345f9e1a0bcfe9c856(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cf5765d4949a5f46d7814d35195c45a724ddee7f991dcbcb14659b65477969a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVmwareengineClusterAutoscalingSettingsAutoscalingPolicies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f0f38bf668d7b284ab5082f5c7da5866e9ce03d29b9ba99da4bbc7951bceb28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31bc4783b5e2b18e49ebe2cef6da7686677ac03aa0e094ea123d3b557256834a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cfbefd376ec2d72ab6a9088328a4b9214a14865c7bbbadcd3c843040369db74(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc51f1f3056d678a758a062b772a19461b7ee29d96e64d28d96a8c0cc70eb47a(
    value: typing.Optional[GoogleVmwareengineClusterAutoscalingSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da355844def8d4c362b86513656a55f324e700dcb8c30a1dc6fe98c41a9b5aa4(
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
    autoscaling_settings: typing.Optional[typing.Union[GoogleVmwareengineClusterAutoscalingSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    node_type_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVmwareengineClusterNodeTypeConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleVmwareengineClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d8adfa3dd7dd71228c2e500b1159ae56df2992f99ef521aeb515b9171e13d4c(
    *,
    node_count: jsii.Number,
    node_type_id: builtins.str,
    custom_core_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82ed458ca0769a2219f2a8940db904ec498ad24bef373bd7e079d349359441f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaa9c832a832b8b1518b77854a67fa3bb930cf1ac2abd9ec4ed398631da3d156(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbf56fb3bc7bc7108566ac18c86e434b804592d290a4141f9aa966fd97c8a76a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9db4409ac6e4ad43e7fa7f6c82b5f8ffabc544a129e063fecf4a033b53339134(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5844489aa9a5099b0070efcbf5cc7e21d6b6a97fc2cae1afe540224bc59928ed(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94fa71b010467a304f4650bf9531e826b7d46051436aaf114b42c55689383953(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVmwareengineClusterNodeTypeConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e49e615fcc2e57f871b5c2765482dd0b480548d3f4d5b029bf3fe2d1cc538159(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68f35b48e5d64aab597e98acfa6180ebe6e29c6a39dfc785c8b29c3eb45388c6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc008e2c269497c1d124de712be0eee843fb091c859f425fa30966e5e7470b18(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24c5a24e6cdf04a94d7e58409b98c04c204eae0c8c6f001626b4d10b1df1be7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43b88a1a879cbf77683d262784dd45410e98d78310f735500ef63eb216f2f13b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVmwareengineClusterNodeTypeConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f64ad92e8d3414c26c06dd1c382c06bf2365491a7ca3bf92ad149f3383bffa4(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc2747c1bc32d163960c39f3b04c0a9a6dfc0a4b995877de7ebd1b065d2eee5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62bf69049505418d44e62e78295809f03454e8f900d459236cf8f0cb0394dfae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac14b827fd0578ea834d10ea71b80493de0dbbdfdb3620c1c6ead9ea12b3f018(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a52081bb33aef9e40aacaa99a32bfc2a3342fdd19550b8be5ac2919df3831dea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acfbf8e29277310a8ade015f039d6165f573ed55b84c3d2c537e54be7b17f3b2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVmwareengineClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
