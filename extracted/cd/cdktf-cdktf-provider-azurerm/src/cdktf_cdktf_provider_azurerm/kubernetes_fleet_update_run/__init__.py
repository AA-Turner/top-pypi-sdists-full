r'''
# `azurerm_kubernetes_fleet_update_run`

Refer to the Terraform Registry for docs: [`azurerm_kubernetes_fleet_update_run`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run).
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


class KubernetesFleetUpdateRun(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesFleetUpdateRun.KubernetesFleetUpdateRun",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run azurerm_kubernetes_fleet_update_run}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        kubernetes_fleet_manager_id: builtins.str,
        managed_cluster_update: typing.Union["KubernetesFleetUpdateRunManagedClusterUpdate", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        fleet_update_strategy_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        stage: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KubernetesFleetUpdateRunStage", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["KubernetesFleetUpdateRunTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run azurerm_kubernetes_fleet_update_run} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param kubernetes_fleet_manager_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#kubernetes_fleet_manager_id KubernetesFleetUpdateRun#kubernetes_fleet_manager_id}.
        :param managed_cluster_update: managed_cluster_update block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#managed_cluster_update KubernetesFleetUpdateRun#managed_cluster_update}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#name KubernetesFleetUpdateRun#name}.
        :param fleet_update_strategy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#fleet_update_strategy_id KubernetesFleetUpdateRun#fleet_update_strategy_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#id KubernetesFleetUpdateRun#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param stage: stage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#stage KubernetesFleetUpdateRun#stage}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#timeouts KubernetesFleetUpdateRun#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a86fa10b826b21a6ad3212994134577119d960bc644a19c209858636010cc7e7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = KubernetesFleetUpdateRunConfig(
            kubernetes_fleet_manager_id=kubernetes_fleet_manager_id,
            managed_cluster_update=managed_cluster_update,
            name=name,
            fleet_update_strategy_id=fleet_update_strategy_id,
            id=id,
            stage=stage,
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
        '''Generates CDKTF code for importing a KubernetesFleetUpdateRun resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the KubernetesFleetUpdateRun to import.
        :param import_from_id: The id of the existing KubernetesFleetUpdateRun that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the KubernetesFleetUpdateRun to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__908cd0571a5b2491d427c143cb3aae3dc6e5d9347075f3621504d1a182157671)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putManagedClusterUpdate")
    def put_managed_cluster_update(
        self,
        *,
        upgrade: typing.Union["KubernetesFleetUpdateRunManagedClusterUpdateUpgrade", typing.Dict[builtins.str, typing.Any]],
        node_image_selection: typing.Optional[typing.Union["KubernetesFleetUpdateRunManagedClusterUpdateNodeImageSelection", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param upgrade: upgrade block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#upgrade KubernetesFleetUpdateRun#upgrade}
        :param node_image_selection: node_image_selection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#node_image_selection KubernetesFleetUpdateRun#node_image_selection}
        '''
        value = KubernetesFleetUpdateRunManagedClusterUpdate(
            upgrade=upgrade, node_image_selection=node_image_selection
        )

        return typing.cast(None, jsii.invoke(self, "putManagedClusterUpdate", [value]))

    @jsii.member(jsii_name="putStage")
    def put_stage(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KubernetesFleetUpdateRunStage", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30a83144863778d7d475dbd03c88337edea6878179fdd7ac31e264fc0c895ec2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStage", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#create KubernetesFleetUpdateRun#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#delete KubernetesFleetUpdateRun#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#read KubernetesFleetUpdateRun#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#update KubernetesFleetUpdateRun#update}.
        '''
        value = KubernetesFleetUpdateRunTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetFleetUpdateStrategyId")
    def reset_fleet_update_strategy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFleetUpdateStrategyId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetStage")
    def reset_stage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStage", []))

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
    @jsii.member(jsii_name="managedClusterUpdate")
    def managed_cluster_update(
        self,
    ) -> "KubernetesFleetUpdateRunManagedClusterUpdateOutputReference":
        return typing.cast("KubernetesFleetUpdateRunManagedClusterUpdateOutputReference", jsii.get(self, "managedClusterUpdate"))

    @builtins.property
    @jsii.member(jsii_name="stage")
    def stage(self) -> "KubernetesFleetUpdateRunStageList":
        return typing.cast("KubernetesFleetUpdateRunStageList", jsii.get(self, "stage"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "KubernetesFleetUpdateRunTimeoutsOutputReference":
        return typing.cast("KubernetesFleetUpdateRunTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="fleetUpdateStrategyIdInput")
    def fleet_update_strategy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fleetUpdateStrategyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesFleetManagerIdInput")
    def kubernetes_fleet_manager_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kubernetesFleetManagerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="managedClusterUpdateInput")
    def managed_cluster_update_input(
        self,
    ) -> typing.Optional["KubernetesFleetUpdateRunManagedClusterUpdate"]:
        return typing.cast(typing.Optional["KubernetesFleetUpdateRunManagedClusterUpdate"], jsii.get(self, "managedClusterUpdateInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="stageInput")
    def stage_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KubernetesFleetUpdateRunStage"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KubernetesFleetUpdateRunStage"]]], jsii.get(self, "stageInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "KubernetesFleetUpdateRunTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "KubernetesFleetUpdateRunTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="fleetUpdateStrategyId")
    def fleet_update_strategy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fleetUpdateStrategyId"))

    @fleet_update_strategy_id.setter
    def fleet_update_strategy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40c7a644ba4d877f686ba4e0b8635af6858c74b3b836d1f252c713ab8f5d923f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fleetUpdateStrategyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0ea0dcdd8716abbc947422aad16a80146b22b82e9e410b7941bc5b2ad210355)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kubernetesFleetManagerId")
    def kubernetes_fleet_manager_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kubernetesFleetManagerId"))

    @kubernetes_fleet_manager_id.setter
    def kubernetes_fleet_manager_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__519bda9e0117599c56daec7731959dfd2d1ec009a6536da4df4a1ec6e9b532da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kubernetesFleetManagerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0c060d7539c9c88f32bc0ea7cc5a06655116d357f80eab06eba5d4fab91610a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesFleetUpdateRun.KubernetesFleetUpdateRunConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "kubernetes_fleet_manager_id": "kubernetesFleetManagerId",
        "managed_cluster_update": "managedClusterUpdate",
        "name": "name",
        "fleet_update_strategy_id": "fleetUpdateStrategyId",
        "id": "id",
        "stage": "stage",
        "timeouts": "timeouts",
    },
)
class KubernetesFleetUpdateRunConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        kubernetes_fleet_manager_id: builtins.str,
        managed_cluster_update: typing.Union["KubernetesFleetUpdateRunManagedClusterUpdate", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        fleet_update_strategy_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        stage: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KubernetesFleetUpdateRunStage", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["KubernetesFleetUpdateRunTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param kubernetes_fleet_manager_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#kubernetes_fleet_manager_id KubernetesFleetUpdateRun#kubernetes_fleet_manager_id}.
        :param managed_cluster_update: managed_cluster_update block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#managed_cluster_update KubernetesFleetUpdateRun#managed_cluster_update}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#name KubernetesFleetUpdateRun#name}.
        :param fleet_update_strategy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#fleet_update_strategy_id KubernetesFleetUpdateRun#fleet_update_strategy_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#id KubernetesFleetUpdateRun#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param stage: stage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#stage KubernetesFleetUpdateRun#stage}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#timeouts KubernetesFleetUpdateRun#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(managed_cluster_update, dict):
            managed_cluster_update = KubernetesFleetUpdateRunManagedClusterUpdate(**managed_cluster_update)
        if isinstance(timeouts, dict):
            timeouts = KubernetesFleetUpdateRunTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d92a66721c6c2a2e756831b668eb07978117c736d44f19d4b8ef6eb5bafaba5)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument kubernetes_fleet_manager_id", value=kubernetes_fleet_manager_id, expected_type=type_hints["kubernetes_fleet_manager_id"])
            check_type(argname="argument managed_cluster_update", value=managed_cluster_update, expected_type=type_hints["managed_cluster_update"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument fleet_update_strategy_id", value=fleet_update_strategy_id, expected_type=type_hints["fleet_update_strategy_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kubernetes_fleet_manager_id": kubernetes_fleet_manager_id,
            "managed_cluster_update": managed_cluster_update,
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
        if fleet_update_strategy_id is not None:
            self._values["fleet_update_strategy_id"] = fleet_update_strategy_id
        if id is not None:
            self._values["id"] = id
        if stage is not None:
            self._values["stage"] = stage
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
    def kubernetes_fleet_manager_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#kubernetes_fleet_manager_id KubernetesFleetUpdateRun#kubernetes_fleet_manager_id}.'''
        result = self._values.get("kubernetes_fleet_manager_id")
        assert result is not None, "Required property 'kubernetes_fleet_manager_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def managed_cluster_update(self) -> "KubernetesFleetUpdateRunManagedClusterUpdate":
        '''managed_cluster_update block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#managed_cluster_update KubernetesFleetUpdateRun#managed_cluster_update}
        '''
        result = self._values.get("managed_cluster_update")
        assert result is not None, "Required property 'managed_cluster_update' is missing"
        return typing.cast("KubernetesFleetUpdateRunManagedClusterUpdate", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#name KubernetesFleetUpdateRun#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fleet_update_strategy_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#fleet_update_strategy_id KubernetesFleetUpdateRun#fleet_update_strategy_id}.'''
        result = self._values.get("fleet_update_strategy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#id KubernetesFleetUpdateRun#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stage(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KubernetesFleetUpdateRunStage"]]]:
        '''stage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#stage KubernetesFleetUpdateRun#stage}
        '''
        result = self._values.get("stage")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KubernetesFleetUpdateRunStage"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["KubernetesFleetUpdateRunTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#timeouts KubernetesFleetUpdateRun#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["KubernetesFleetUpdateRunTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesFleetUpdateRunConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesFleetUpdateRun.KubernetesFleetUpdateRunManagedClusterUpdate",
    jsii_struct_bases=[],
    name_mapping={"upgrade": "upgrade", "node_image_selection": "nodeImageSelection"},
)
class KubernetesFleetUpdateRunManagedClusterUpdate:
    def __init__(
        self,
        *,
        upgrade: typing.Union["KubernetesFleetUpdateRunManagedClusterUpdateUpgrade", typing.Dict[builtins.str, typing.Any]],
        node_image_selection: typing.Optional[typing.Union["KubernetesFleetUpdateRunManagedClusterUpdateNodeImageSelection", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param upgrade: upgrade block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#upgrade KubernetesFleetUpdateRun#upgrade}
        :param node_image_selection: node_image_selection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#node_image_selection KubernetesFleetUpdateRun#node_image_selection}
        '''
        if isinstance(upgrade, dict):
            upgrade = KubernetesFleetUpdateRunManagedClusterUpdateUpgrade(**upgrade)
        if isinstance(node_image_selection, dict):
            node_image_selection = KubernetesFleetUpdateRunManagedClusterUpdateNodeImageSelection(**node_image_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__696cc603b8ddd0eb9ea80269ccc85d66b070d7afc1ffc23810b27eaab05323a0)
            check_type(argname="argument upgrade", value=upgrade, expected_type=type_hints["upgrade"])
            check_type(argname="argument node_image_selection", value=node_image_selection, expected_type=type_hints["node_image_selection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "upgrade": upgrade,
        }
        if node_image_selection is not None:
            self._values["node_image_selection"] = node_image_selection

    @builtins.property
    def upgrade(self) -> "KubernetesFleetUpdateRunManagedClusterUpdateUpgrade":
        '''upgrade block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#upgrade KubernetesFleetUpdateRun#upgrade}
        '''
        result = self._values.get("upgrade")
        assert result is not None, "Required property 'upgrade' is missing"
        return typing.cast("KubernetesFleetUpdateRunManagedClusterUpdateUpgrade", result)

    @builtins.property
    def node_image_selection(
        self,
    ) -> typing.Optional["KubernetesFleetUpdateRunManagedClusterUpdateNodeImageSelection"]:
        '''node_image_selection block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#node_image_selection KubernetesFleetUpdateRun#node_image_selection}
        '''
        result = self._values.get("node_image_selection")
        return typing.cast(typing.Optional["KubernetesFleetUpdateRunManagedClusterUpdateNodeImageSelection"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesFleetUpdateRunManagedClusterUpdate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesFleetUpdateRun.KubernetesFleetUpdateRunManagedClusterUpdateNodeImageSelection",
    jsii_struct_bases=[],
    name_mapping={"type": "type"},
)
class KubernetesFleetUpdateRunManagedClusterUpdateNodeImageSelection:
    def __init__(self, *, type: builtins.str) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#type KubernetesFleetUpdateRun#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb9bb715caeffba2372bd264b099e92f783065aa86e8cb5bda6e506d61a2eea6)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#type KubernetesFleetUpdateRun#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesFleetUpdateRunManagedClusterUpdateNodeImageSelection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesFleetUpdateRunManagedClusterUpdateNodeImageSelectionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesFleetUpdateRun.KubernetesFleetUpdateRunManagedClusterUpdateNodeImageSelectionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__36d11aab2cac17884b9530c5621f230f72fcfde18c781e1c1c2a06581594056b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec3a882b6e38bacd1029b9ce6739494abc4841213a3509a342fe8eeae6f09664)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KubernetesFleetUpdateRunManagedClusterUpdateNodeImageSelection]:
        return typing.cast(typing.Optional[KubernetesFleetUpdateRunManagedClusterUpdateNodeImageSelection], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesFleetUpdateRunManagedClusterUpdateNodeImageSelection],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4494a89f5f146e4722b871dd98bd7bfbb75e9bc57b071f1a26b533b5aaa15d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KubernetesFleetUpdateRunManagedClusterUpdateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesFleetUpdateRun.KubernetesFleetUpdateRunManagedClusterUpdateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7ffe26c74fe69676616657eeb5d79e63874a010c639dd40d41235f888b47d40)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNodeImageSelection")
    def put_node_image_selection(self, *, type: builtins.str) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#type KubernetesFleetUpdateRun#type}.
        '''
        value = KubernetesFleetUpdateRunManagedClusterUpdateNodeImageSelection(
            type=type
        )

        return typing.cast(None, jsii.invoke(self, "putNodeImageSelection", [value]))

    @jsii.member(jsii_name="putUpgrade")
    def put_upgrade(
        self,
        *,
        type: builtins.str,
        kubernetes_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#type KubernetesFleetUpdateRun#type}.
        :param kubernetes_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#kubernetes_version KubernetesFleetUpdateRun#kubernetes_version}.
        '''
        value = KubernetesFleetUpdateRunManagedClusterUpdateUpgrade(
            type=type, kubernetes_version=kubernetes_version
        )

        return typing.cast(None, jsii.invoke(self, "putUpgrade", [value]))

    @jsii.member(jsii_name="resetNodeImageSelection")
    def reset_node_image_selection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeImageSelection", []))

    @builtins.property
    @jsii.member(jsii_name="nodeImageSelection")
    def node_image_selection(
        self,
    ) -> KubernetesFleetUpdateRunManagedClusterUpdateNodeImageSelectionOutputReference:
        return typing.cast(KubernetesFleetUpdateRunManagedClusterUpdateNodeImageSelectionOutputReference, jsii.get(self, "nodeImageSelection"))

    @builtins.property
    @jsii.member(jsii_name="upgrade")
    def upgrade(
        self,
    ) -> "KubernetesFleetUpdateRunManagedClusterUpdateUpgradeOutputReference":
        return typing.cast("KubernetesFleetUpdateRunManagedClusterUpdateUpgradeOutputReference", jsii.get(self, "upgrade"))

    @builtins.property
    @jsii.member(jsii_name="nodeImageSelectionInput")
    def node_image_selection_input(
        self,
    ) -> typing.Optional[KubernetesFleetUpdateRunManagedClusterUpdateNodeImageSelection]:
        return typing.cast(typing.Optional[KubernetesFleetUpdateRunManagedClusterUpdateNodeImageSelection], jsii.get(self, "nodeImageSelectionInput"))

    @builtins.property
    @jsii.member(jsii_name="upgradeInput")
    def upgrade_input(
        self,
    ) -> typing.Optional["KubernetesFleetUpdateRunManagedClusterUpdateUpgrade"]:
        return typing.cast(typing.Optional["KubernetesFleetUpdateRunManagedClusterUpdateUpgrade"], jsii.get(self, "upgradeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KubernetesFleetUpdateRunManagedClusterUpdate]:
        return typing.cast(typing.Optional[KubernetesFleetUpdateRunManagedClusterUpdate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesFleetUpdateRunManagedClusterUpdate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__225a75dc366ebfb2143e9cc62cb9ec3cd145527ab913af2aacc1ebc2fbebcbfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesFleetUpdateRun.KubernetesFleetUpdateRunManagedClusterUpdateUpgrade",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "kubernetes_version": "kubernetesVersion"},
)
class KubernetesFleetUpdateRunManagedClusterUpdateUpgrade:
    def __init__(
        self,
        *,
        type: builtins.str,
        kubernetes_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#type KubernetesFleetUpdateRun#type}.
        :param kubernetes_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#kubernetes_version KubernetesFleetUpdateRun#kubernetes_version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a812607486946f656f8ead09369ef0288449868344bb6d0399be574c85306d2e)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument kubernetes_version", value=kubernetes_version, expected_type=type_hints["kubernetes_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if kubernetes_version is not None:
            self._values["kubernetes_version"] = kubernetes_version

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#type KubernetesFleetUpdateRun#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kubernetes_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#kubernetes_version KubernetesFleetUpdateRun#kubernetes_version}.'''
        result = self._values.get("kubernetes_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesFleetUpdateRunManagedClusterUpdateUpgrade(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesFleetUpdateRunManagedClusterUpdateUpgradeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesFleetUpdateRun.KubernetesFleetUpdateRunManagedClusterUpdateUpgradeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9aabcbdd4ac3d322c1b1caa0e091392232561e49b191b06fb798fbd1443a340e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKubernetesVersion")
    def reset_kubernetes_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKubernetesVersion", []))

    @builtins.property
    @jsii.member(jsii_name="kubernetesVersionInput")
    def kubernetes_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kubernetesVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesVersion")
    def kubernetes_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kubernetesVersion"))

    @kubernetes_version.setter
    def kubernetes_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05d04bfea541fab8129de148315993ede22f2c665cbb2299b8ab3c467b28d33a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kubernetesVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1bc6df5e51c715ec8d4810870713f10f2b3ca7353f4652fd701dddcc737ed3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KubernetesFleetUpdateRunManagedClusterUpdateUpgrade]:
        return typing.cast(typing.Optional[KubernetesFleetUpdateRunManagedClusterUpdateUpgrade], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesFleetUpdateRunManagedClusterUpdateUpgrade],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7937b2bd888ebc61dece0b9678af9efd0447a677b2d5e1957be42025c810acc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesFleetUpdateRun.KubernetesFleetUpdateRunStage",
    jsii_struct_bases=[],
    name_mapping={
        "group": "group",
        "name": "name",
        "after_stage_wait_in_seconds": "afterStageWaitInSeconds",
    },
)
class KubernetesFleetUpdateRunStage:
    def __init__(
        self,
        *,
        group: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KubernetesFleetUpdateRunStageGroup", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        after_stage_wait_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param group: group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#group KubernetesFleetUpdateRun#group}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#name KubernetesFleetUpdateRun#name}.
        :param after_stage_wait_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#after_stage_wait_in_seconds KubernetesFleetUpdateRun#after_stage_wait_in_seconds}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__466b8b65f52b8e4908bd923601f2212cd95e11d9f065d7aec55dd68a0378f73c)
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument after_stage_wait_in_seconds", value=after_stage_wait_in_seconds, expected_type=type_hints["after_stage_wait_in_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group": group,
            "name": name,
        }
        if after_stage_wait_in_seconds is not None:
            self._values["after_stage_wait_in_seconds"] = after_stage_wait_in_seconds

    @builtins.property
    def group(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KubernetesFleetUpdateRunStageGroup"]]:
        '''group block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#group KubernetesFleetUpdateRun#group}
        '''
        result = self._values.get("group")
        assert result is not None, "Required property 'group' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KubernetesFleetUpdateRunStageGroup"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#name KubernetesFleetUpdateRun#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def after_stage_wait_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#after_stage_wait_in_seconds KubernetesFleetUpdateRun#after_stage_wait_in_seconds}.'''
        result = self._values.get("after_stage_wait_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesFleetUpdateRunStage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesFleetUpdateRun.KubernetesFleetUpdateRunStageGroup",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class KubernetesFleetUpdateRunStageGroup:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#name KubernetesFleetUpdateRun#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f3948055684e36817945dd97cd9fe21319fb8a739a149299f05659fcab2a6e8)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#name KubernetesFleetUpdateRun#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesFleetUpdateRunStageGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesFleetUpdateRunStageGroupList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesFleetUpdateRun.KubernetesFleetUpdateRunStageGroupList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__343a17a3835516aee530329db466c973023675b1fcb733b929234a08408be292)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KubernetesFleetUpdateRunStageGroupOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54a526544d281c432b685395840c267e21d3afb67e993fcfcebc024588e55f26)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KubernetesFleetUpdateRunStageGroupOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49e3159881048fbb6ce556d2dd29ec44d400baaadc5e733db659d1c1c1f0b412)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae16b75ccde5059043162a659e9d362cdad2389bea7192b1638fec34bed6f841)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fef819fd4111be01b471b33dfa3bc80d6570d1b654d8101b4e378593dfbcf96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KubernetesFleetUpdateRunStageGroup]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KubernetesFleetUpdateRunStageGroup]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KubernetesFleetUpdateRunStageGroup]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__245d2c38ce0b5f24adc20c58fc5c065115da6a944e141b634e870d41fb2a298f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KubernetesFleetUpdateRunStageGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesFleetUpdateRun.KubernetesFleetUpdateRunStageGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f8d6c2c6dc6c32806214249f50da9c1396bb8ca39f3cac718d1cf1315a5d592)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90c14fef318ec005cb708a3ce9393da0588da89a25e37d95398a18e4f6551727)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KubernetesFleetUpdateRunStageGroup]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KubernetesFleetUpdateRunStageGroup]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KubernetesFleetUpdateRunStageGroup]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5ffc06bd251d1bb5b1603db2716f8847474149abbbdfbaa0786c6437aca46aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KubernetesFleetUpdateRunStageList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesFleetUpdateRun.KubernetesFleetUpdateRunStageList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a33c6f3e97233616fe799d684e3150504bd0a594bc4121ab62026a0a81e2ca3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "KubernetesFleetUpdateRunStageOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d7a78ca8a23ec516c1a297525ccebc9dbbbf760211b9ca5f05f13bdd408a89f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KubernetesFleetUpdateRunStageOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8c41cf3b50d542e93feaa8a4e9a43c53b3724e5878f8253a9db32dce7531af5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__932abdb502354f0e5722f2865f502a4ee5895358406cd48ff4a817c0559f3e01)
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
            type_hints = typing.get_type_hints(_typecheckingstub__63c73a14dcbcaead8c3980bcfced395a65f7c8144a03d6ddb06f7e23127537a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KubernetesFleetUpdateRunStage]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KubernetesFleetUpdateRunStage]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KubernetesFleetUpdateRunStage]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e944bf7f2369a598caf3f749646c55c6dfb4c8ce3f740f306cdc4aeec2f3c1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KubernetesFleetUpdateRunStageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesFleetUpdateRun.KubernetesFleetUpdateRunStageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d667e36e47d110b8dfcafc06e536bf2386abc91855c915e1f2417475ad6fd4c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putGroup")
    def put_group(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KubernetesFleetUpdateRunStageGroup, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7940e855bf1201fa6f6979469f72db6207a36805be59c25abb593b3e37ba55a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGroup", [value]))

    @jsii.member(jsii_name="resetAfterStageWaitInSeconds")
    def reset_after_stage_wait_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAfterStageWaitInSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="group")
    def group(self) -> KubernetesFleetUpdateRunStageGroupList:
        return typing.cast(KubernetesFleetUpdateRunStageGroupList, jsii.get(self, "group"))

    @builtins.property
    @jsii.member(jsii_name="afterStageWaitInSecondsInput")
    def after_stage_wait_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "afterStageWaitInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="groupInput")
    def group_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KubernetesFleetUpdateRunStageGroup]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KubernetesFleetUpdateRunStageGroup]]], jsii.get(self, "groupInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="afterStageWaitInSeconds")
    def after_stage_wait_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "afterStageWaitInSeconds"))

    @after_stage_wait_in_seconds.setter
    def after_stage_wait_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7711ae478242eec510a8ba2366c98ddfc7f9bbf4d841e98fd06af5d0ecfe9a94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "afterStageWaitInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5bc2d34b5a785c370db27c60e6ac1200012c4c5e03bffaee7ee632c44105024)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KubernetesFleetUpdateRunStage]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KubernetesFleetUpdateRunStage]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KubernetesFleetUpdateRunStage]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2f2c79358fce6ce0f784d7f3a8016285792928cc06714e70ae23deaf8d8cf77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesFleetUpdateRun.KubernetesFleetUpdateRunTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class KubernetesFleetUpdateRunTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#create KubernetesFleetUpdateRun#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#delete KubernetesFleetUpdateRun#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#read KubernetesFleetUpdateRun#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#update KubernetesFleetUpdateRun#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a35c857a4c48ab82d4bc3af60a8f524df872f39a882b2f7ef15b767cd90755b)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#create KubernetesFleetUpdateRun#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#delete KubernetesFleetUpdateRun#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#read KubernetesFleetUpdateRun#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kubernetes_fleet_update_run#update KubernetesFleetUpdateRun#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesFleetUpdateRunTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesFleetUpdateRunTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesFleetUpdateRun.KubernetesFleetUpdateRunTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2fd05f2f57e6cbe64887040c89ba6efdbca9cb1a71ddda9651868c7664316dae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

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
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ffb5223761562cebdf71010c1c0f2316151ebf1d17a3a89237fa4f13c7e610bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7bbe6bb23717633da7bbc527865a22f2eb1355b7e1337c1495810433b820550)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cd9898492875bdec9333e9ae0f256b26a3d86ec7959d77ebde8d81eb093a905)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1101e2e9782753736fd010c6088f35b36cd0f96effc5ed597cab853972cede9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KubernetesFleetUpdateRunTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KubernetesFleetUpdateRunTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KubernetesFleetUpdateRunTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04c898dffbd9205607b6b5c3076f5b31e54a690cae7ac64046858ba0567971c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "KubernetesFleetUpdateRun",
    "KubernetesFleetUpdateRunConfig",
    "KubernetesFleetUpdateRunManagedClusterUpdate",
    "KubernetesFleetUpdateRunManagedClusterUpdateNodeImageSelection",
    "KubernetesFleetUpdateRunManagedClusterUpdateNodeImageSelectionOutputReference",
    "KubernetesFleetUpdateRunManagedClusterUpdateOutputReference",
    "KubernetesFleetUpdateRunManagedClusterUpdateUpgrade",
    "KubernetesFleetUpdateRunManagedClusterUpdateUpgradeOutputReference",
    "KubernetesFleetUpdateRunStage",
    "KubernetesFleetUpdateRunStageGroup",
    "KubernetesFleetUpdateRunStageGroupList",
    "KubernetesFleetUpdateRunStageGroupOutputReference",
    "KubernetesFleetUpdateRunStageList",
    "KubernetesFleetUpdateRunStageOutputReference",
    "KubernetesFleetUpdateRunTimeouts",
    "KubernetesFleetUpdateRunTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__a86fa10b826b21a6ad3212994134577119d960bc644a19c209858636010cc7e7(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    kubernetes_fleet_manager_id: builtins.str,
    managed_cluster_update: typing.Union[KubernetesFleetUpdateRunManagedClusterUpdate, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    fleet_update_strategy_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    stage: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KubernetesFleetUpdateRunStage, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[KubernetesFleetUpdateRunTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__908cd0571a5b2491d427c143cb3aae3dc6e5d9347075f3621504d1a182157671(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30a83144863778d7d475dbd03c88337edea6878179fdd7ac31e264fc0c895ec2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KubernetesFleetUpdateRunStage, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40c7a644ba4d877f686ba4e0b8635af6858c74b3b836d1f252c713ab8f5d923f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0ea0dcdd8716abbc947422aad16a80146b22b82e9e410b7941bc5b2ad210355(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__519bda9e0117599c56daec7731959dfd2d1ec009a6536da4df4a1ec6e9b532da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c060d7539c9c88f32bc0ea7cc5a06655116d357f80eab06eba5d4fab91610a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d92a66721c6c2a2e756831b668eb07978117c736d44f19d4b8ef6eb5bafaba5(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    kubernetes_fleet_manager_id: builtins.str,
    managed_cluster_update: typing.Union[KubernetesFleetUpdateRunManagedClusterUpdate, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    fleet_update_strategy_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    stage: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KubernetesFleetUpdateRunStage, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[KubernetesFleetUpdateRunTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__696cc603b8ddd0eb9ea80269ccc85d66b070d7afc1ffc23810b27eaab05323a0(
    *,
    upgrade: typing.Union[KubernetesFleetUpdateRunManagedClusterUpdateUpgrade, typing.Dict[builtins.str, typing.Any]],
    node_image_selection: typing.Optional[typing.Union[KubernetesFleetUpdateRunManagedClusterUpdateNodeImageSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb9bb715caeffba2372bd264b099e92f783065aa86e8cb5bda6e506d61a2eea6(
    *,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36d11aab2cac17884b9530c5621f230f72fcfde18c781e1c1c2a06581594056b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec3a882b6e38bacd1029b9ce6739494abc4841213a3509a342fe8eeae6f09664(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4494a89f5f146e4722b871dd98bd7bfbb75e9bc57b071f1a26b533b5aaa15d2(
    value: typing.Optional[KubernetesFleetUpdateRunManagedClusterUpdateNodeImageSelection],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7ffe26c74fe69676616657eeb5d79e63874a010c639dd40d41235f888b47d40(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__225a75dc366ebfb2143e9cc62cb9ec3cd145527ab913af2aacc1ebc2fbebcbfc(
    value: typing.Optional[KubernetesFleetUpdateRunManagedClusterUpdate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a812607486946f656f8ead09369ef0288449868344bb6d0399be574c85306d2e(
    *,
    type: builtins.str,
    kubernetes_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aabcbdd4ac3d322c1b1caa0e091392232561e49b191b06fb798fbd1443a340e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05d04bfea541fab8129de148315993ede22f2c665cbb2299b8ab3c467b28d33a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1bc6df5e51c715ec8d4810870713f10f2b3ca7353f4652fd701dddcc737ed3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7937b2bd888ebc61dece0b9678af9efd0447a677b2d5e1957be42025c810acc4(
    value: typing.Optional[KubernetesFleetUpdateRunManagedClusterUpdateUpgrade],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__466b8b65f52b8e4908bd923601f2212cd95e11d9f065d7aec55dd68a0378f73c(
    *,
    group: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KubernetesFleetUpdateRunStageGroup, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    after_stage_wait_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f3948055684e36817945dd97cd9fe21319fb8a739a149299f05659fcab2a6e8(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__343a17a3835516aee530329db466c973023675b1fcb733b929234a08408be292(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54a526544d281c432b685395840c267e21d3afb67e993fcfcebc024588e55f26(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49e3159881048fbb6ce556d2dd29ec44d400baaadc5e733db659d1c1c1f0b412(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae16b75ccde5059043162a659e9d362cdad2389bea7192b1638fec34bed6f841(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fef819fd4111be01b471b33dfa3bc80d6570d1b654d8101b4e378593dfbcf96(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__245d2c38ce0b5f24adc20c58fc5c065115da6a944e141b634e870d41fb2a298f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KubernetesFleetUpdateRunStageGroup]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f8d6c2c6dc6c32806214249f50da9c1396bb8ca39f3cac718d1cf1315a5d592(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90c14fef318ec005cb708a3ce9393da0588da89a25e37d95398a18e4f6551727(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5ffc06bd251d1bb5b1603db2716f8847474149abbbdfbaa0786c6437aca46aa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KubernetesFleetUpdateRunStageGroup]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a33c6f3e97233616fe799d684e3150504bd0a594bc4121ab62026a0a81e2ca3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d7a78ca8a23ec516c1a297525ccebc9dbbbf760211b9ca5f05f13bdd408a89f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8c41cf3b50d542e93feaa8a4e9a43c53b3724e5878f8253a9db32dce7531af5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__932abdb502354f0e5722f2865f502a4ee5895358406cd48ff4a817c0559f3e01(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63c73a14dcbcaead8c3980bcfced395a65f7c8144a03d6ddb06f7e23127537a2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e944bf7f2369a598caf3f749646c55c6dfb4c8ce3f740f306cdc4aeec2f3c1e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KubernetesFleetUpdateRunStage]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d667e36e47d110b8dfcafc06e536bf2386abc91855c915e1f2417475ad6fd4c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7940e855bf1201fa6f6979469f72db6207a36805be59c25abb593b3e37ba55a3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KubernetesFleetUpdateRunStageGroup, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7711ae478242eec510a8ba2366c98ddfc7f9bbf4d841e98fd06af5d0ecfe9a94(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5bc2d34b5a785c370db27c60e6ac1200012c4c5e03bffaee7ee632c44105024(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2f2c79358fce6ce0f784d7f3a8016285792928cc06714e70ae23deaf8d8cf77(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KubernetesFleetUpdateRunStage]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a35c857a4c48ab82d4bc3af60a8f524df872f39a882b2f7ef15b767cd90755b(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fd05f2f57e6cbe64887040c89ba6efdbca9cb1a71ddda9651868c7664316dae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffb5223761562cebdf71010c1c0f2316151ebf1d17a3a89237fa4f13c7e610bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7bbe6bb23717633da7bbc527865a22f2eb1355b7e1337c1495810433b820550(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cd9898492875bdec9333e9ae0f256b26a3d86ec7959d77ebde8d81eb093a905(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1101e2e9782753736fd010c6088f35b36cd0f96effc5ed597cab853972cede9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c898dffbd9205607b6b5c3076f5b31e54a690cae7ac64046858ba0567971c2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KubernetesFleetUpdateRunTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
