r'''
# `azurerm_data_protection_backup_instance_kubernetes_cluster`

Refer to the Terraform Registry for docs: [`azurerm_data_protection_backup_instance_kubernetes_cluster`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster).
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


class DataProtectionBackupInstanceKubernetesCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupInstanceKubernetesCluster.DataProtectionBackupInstanceKubernetesCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster azurerm_data_protection_backup_instance_kubernetes_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        backup_policy_id: builtins.str,
        kubernetes_cluster_id: builtins.str,
        location: builtins.str,
        name: builtins.str,
        snapshot_resource_group_name: builtins.str,
        vault_id: builtins.str,
        backup_datasource_parameters: typing.Optional[typing.Union["DataProtectionBackupInstanceKubernetesClusterBackupDatasourceParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataProtectionBackupInstanceKubernetesClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster azurerm_data_protection_backup_instance_kubernetes_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param backup_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#backup_policy_id DataProtectionBackupInstanceKubernetesCluster#backup_policy_id}.
        :param kubernetes_cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#kubernetes_cluster_id DataProtectionBackupInstanceKubernetesCluster#kubernetes_cluster_id}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#location DataProtectionBackupInstanceKubernetesCluster#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#name DataProtectionBackupInstanceKubernetesCluster#name}.
        :param snapshot_resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#snapshot_resource_group_name DataProtectionBackupInstanceKubernetesCluster#snapshot_resource_group_name}.
        :param vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#vault_id DataProtectionBackupInstanceKubernetesCluster#vault_id}.
        :param backup_datasource_parameters: backup_datasource_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#backup_datasource_parameters DataProtectionBackupInstanceKubernetesCluster#backup_datasource_parameters}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#id DataProtectionBackupInstanceKubernetesCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#timeouts DataProtectionBackupInstanceKubernetesCluster#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__930db50115f0747be0e563b05480904a4993a503cba4e1a4cee0dedc82486277)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataProtectionBackupInstanceKubernetesClusterConfig(
            backup_policy_id=backup_policy_id,
            kubernetes_cluster_id=kubernetes_cluster_id,
            location=location,
            name=name,
            snapshot_resource_group_name=snapshot_resource_group_name,
            vault_id=vault_id,
            backup_datasource_parameters=backup_datasource_parameters,
            id=id,
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
        '''Generates CDKTF code for importing a DataProtectionBackupInstanceKubernetesCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataProtectionBackupInstanceKubernetesCluster to import.
        :param import_from_id: The id of the existing DataProtectionBackupInstanceKubernetesCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataProtectionBackupInstanceKubernetesCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6f301f9022c38961b12314646b785d1ac0e3400c0de4024edc8a656685a03c4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBackupDatasourceParameters")
    def put_backup_datasource_parameters(
        self,
        *,
        cluster_scoped_resources_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        excluded_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
        excluded_resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        label_selectors: typing.Optional[typing.Sequence[builtins.str]] = None,
        volume_snapshot_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cluster_scoped_resources_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#cluster_scoped_resources_enabled DataProtectionBackupInstanceKubernetesCluster#cluster_scoped_resources_enabled}.
        :param excluded_namespaces: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#excluded_namespaces DataProtectionBackupInstanceKubernetesCluster#excluded_namespaces}.
        :param excluded_resource_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#excluded_resource_types DataProtectionBackupInstanceKubernetesCluster#excluded_resource_types}.
        :param included_namespaces: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#included_namespaces DataProtectionBackupInstanceKubernetesCluster#included_namespaces}.
        :param included_resource_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#included_resource_types DataProtectionBackupInstanceKubernetesCluster#included_resource_types}.
        :param label_selectors: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#label_selectors DataProtectionBackupInstanceKubernetesCluster#label_selectors}.
        :param volume_snapshot_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#volume_snapshot_enabled DataProtectionBackupInstanceKubernetesCluster#volume_snapshot_enabled}.
        '''
        value = DataProtectionBackupInstanceKubernetesClusterBackupDatasourceParameters(
            cluster_scoped_resources_enabled=cluster_scoped_resources_enabled,
            excluded_namespaces=excluded_namespaces,
            excluded_resource_types=excluded_resource_types,
            included_namespaces=included_namespaces,
            included_resource_types=included_resource_types,
            label_selectors=label_selectors,
            volume_snapshot_enabled=volume_snapshot_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putBackupDatasourceParameters", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#create DataProtectionBackupInstanceKubernetesCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#delete DataProtectionBackupInstanceKubernetesCluster#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#read DataProtectionBackupInstanceKubernetesCluster#read}.
        '''
        value = DataProtectionBackupInstanceKubernetesClusterTimeouts(
            create=create, delete=delete, read=read
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetBackupDatasourceParameters")
    def reset_backup_datasource_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupDatasourceParameters", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="backupDatasourceParameters")
    def backup_datasource_parameters(
        self,
    ) -> "DataProtectionBackupInstanceKubernetesClusterBackupDatasourceParametersOutputReference":
        return typing.cast("DataProtectionBackupInstanceKubernetesClusterBackupDatasourceParametersOutputReference", jsii.get(self, "backupDatasourceParameters"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "DataProtectionBackupInstanceKubernetesClusterTimeoutsOutputReference":
        return typing.cast("DataProtectionBackupInstanceKubernetesClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="backupDatasourceParametersInput")
    def backup_datasource_parameters_input(
        self,
    ) -> typing.Optional["DataProtectionBackupInstanceKubernetesClusterBackupDatasourceParameters"]:
        return typing.cast(typing.Optional["DataProtectionBackupInstanceKubernetesClusterBackupDatasourceParameters"], jsii.get(self, "backupDatasourceParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="backupPolicyIdInput")
    def backup_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backupPolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesClusterIdInput")
    def kubernetes_cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kubernetesClusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotResourceGroupNameInput")
    def snapshot_resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snapshotResourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataProtectionBackupInstanceKubernetesClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataProtectionBackupInstanceKubernetesClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="vaultIdInput")
    def vault_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vaultIdInput"))

    @builtins.property
    @jsii.member(jsii_name="backupPolicyId")
    def backup_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backupPolicyId"))

    @backup_policy_id.setter
    def backup_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50af5c61410ffd92f0080f8f40aa34d2798f17518f1eee429ac5be1130eb38e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupPolicyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f423e3748f49567556244a253b92986a3a1862a271db3c6c264ef2630414b81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kubernetesClusterId")
    def kubernetes_cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kubernetesClusterId"))

    @kubernetes_cluster_id.setter
    def kubernetes_cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb857aaa1176d6f143fd93e02c739f4ded89dceff82c89caae1757199433be01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kubernetesClusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7432bac5f6c9b363711ee796129f062dfd7353c0014208c7042fa9528d6d2c32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b567e503ed734db1449237d098efd0d4eaf891f0f90f2642f9a5870bd29f9a35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snapshotResourceGroupName")
    def snapshot_resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snapshotResourceGroupName"))

    @snapshot_resource_group_name.setter
    def snapshot_resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae0c51b90694505c046f55d53427d0468348387759d38a29d88953ef45c210c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotResourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vaultId")
    def vault_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vaultId"))

    @vault_id.setter
    def vault_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90a508cbba22cadf4cda8bc9e6f60d988e1686a2450dc0d268ba0f0499c31fef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vaultId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupInstanceKubernetesCluster.DataProtectionBackupInstanceKubernetesClusterBackupDatasourceParameters",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_scoped_resources_enabled": "clusterScopedResourcesEnabled",
        "excluded_namespaces": "excludedNamespaces",
        "excluded_resource_types": "excludedResourceTypes",
        "included_namespaces": "includedNamespaces",
        "included_resource_types": "includedResourceTypes",
        "label_selectors": "labelSelectors",
        "volume_snapshot_enabled": "volumeSnapshotEnabled",
    },
)
class DataProtectionBackupInstanceKubernetesClusterBackupDatasourceParameters:
    def __init__(
        self,
        *,
        cluster_scoped_resources_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        excluded_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
        excluded_resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        label_selectors: typing.Optional[typing.Sequence[builtins.str]] = None,
        volume_snapshot_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cluster_scoped_resources_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#cluster_scoped_resources_enabled DataProtectionBackupInstanceKubernetesCluster#cluster_scoped_resources_enabled}.
        :param excluded_namespaces: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#excluded_namespaces DataProtectionBackupInstanceKubernetesCluster#excluded_namespaces}.
        :param excluded_resource_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#excluded_resource_types DataProtectionBackupInstanceKubernetesCluster#excluded_resource_types}.
        :param included_namespaces: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#included_namespaces DataProtectionBackupInstanceKubernetesCluster#included_namespaces}.
        :param included_resource_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#included_resource_types DataProtectionBackupInstanceKubernetesCluster#included_resource_types}.
        :param label_selectors: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#label_selectors DataProtectionBackupInstanceKubernetesCluster#label_selectors}.
        :param volume_snapshot_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#volume_snapshot_enabled DataProtectionBackupInstanceKubernetesCluster#volume_snapshot_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b7c9c28a89a421f845fd320c36891da36a8b1e802a508da2b475dbc127029bf)
            check_type(argname="argument cluster_scoped_resources_enabled", value=cluster_scoped_resources_enabled, expected_type=type_hints["cluster_scoped_resources_enabled"])
            check_type(argname="argument excluded_namespaces", value=excluded_namespaces, expected_type=type_hints["excluded_namespaces"])
            check_type(argname="argument excluded_resource_types", value=excluded_resource_types, expected_type=type_hints["excluded_resource_types"])
            check_type(argname="argument included_namespaces", value=included_namespaces, expected_type=type_hints["included_namespaces"])
            check_type(argname="argument included_resource_types", value=included_resource_types, expected_type=type_hints["included_resource_types"])
            check_type(argname="argument label_selectors", value=label_selectors, expected_type=type_hints["label_selectors"])
            check_type(argname="argument volume_snapshot_enabled", value=volume_snapshot_enabled, expected_type=type_hints["volume_snapshot_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cluster_scoped_resources_enabled is not None:
            self._values["cluster_scoped_resources_enabled"] = cluster_scoped_resources_enabled
        if excluded_namespaces is not None:
            self._values["excluded_namespaces"] = excluded_namespaces
        if excluded_resource_types is not None:
            self._values["excluded_resource_types"] = excluded_resource_types
        if included_namespaces is not None:
            self._values["included_namespaces"] = included_namespaces
        if included_resource_types is not None:
            self._values["included_resource_types"] = included_resource_types
        if label_selectors is not None:
            self._values["label_selectors"] = label_selectors
        if volume_snapshot_enabled is not None:
            self._values["volume_snapshot_enabled"] = volume_snapshot_enabled

    @builtins.property
    def cluster_scoped_resources_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#cluster_scoped_resources_enabled DataProtectionBackupInstanceKubernetesCluster#cluster_scoped_resources_enabled}.'''
        result = self._values.get("cluster_scoped_resources_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def excluded_namespaces(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#excluded_namespaces DataProtectionBackupInstanceKubernetesCluster#excluded_namespaces}.'''
        result = self._values.get("excluded_namespaces")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def excluded_resource_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#excluded_resource_types DataProtectionBackupInstanceKubernetesCluster#excluded_resource_types}.'''
        result = self._values.get("excluded_resource_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def included_namespaces(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#included_namespaces DataProtectionBackupInstanceKubernetesCluster#included_namespaces}.'''
        result = self._values.get("included_namespaces")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def included_resource_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#included_resource_types DataProtectionBackupInstanceKubernetesCluster#included_resource_types}.'''
        result = self._values.get("included_resource_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def label_selectors(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#label_selectors DataProtectionBackupInstanceKubernetesCluster#label_selectors}.'''
        result = self._values.get("label_selectors")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def volume_snapshot_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#volume_snapshot_enabled DataProtectionBackupInstanceKubernetesCluster#volume_snapshot_enabled}.'''
        result = self._values.get("volume_snapshot_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProtectionBackupInstanceKubernetesClusterBackupDatasourceParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataProtectionBackupInstanceKubernetesClusterBackupDatasourceParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupInstanceKubernetesCluster.DataProtectionBackupInstanceKubernetesClusterBackupDatasourceParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a9b188b3e37d91657371b996239e6a255db5b01e277653db5e3b5fb77acc52c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClusterScopedResourcesEnabled")
    def reset_cluster_scoped_resources_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterScopedResourcesEnabled", []))

    @jsii.member(jsii_name="resetExcludedNamespaces")
    def reset_excluded_namespaces(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedNamespaces", []))

    @jsii.member(jsii_name="resetExcludedResourceTypes")
    def reset_excluded_resource_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedResourceTypes", []))

    @jsii.member(jsii_name="resetIncludedNamespaces")
    def reset_included_namespaces(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludedNamespaces", []))

    @jsii.member(jsii_name="resetIncludedResourceTypes")
    def reset_included_resource_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludedResourceTypes", []))

    @jsii.member(jsii_name="resetLabelSelectors")
    def reset_label_selectors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabelSelectors", []))

    @jsii.member(jsii_name="resetVolumeSnapshotEnabled")
    def reset_volume_snapshot_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeSnapshotEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="clusterScopedResourcesEnabledInput")
    def cluster_scoped_resources_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "clusterScopedResourcesEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedNamespacesInput")
    def excluded_namespaces_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludedNamespacesInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedResourceTypesInput")
    def excluded_resource_types_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludedResourceTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="includedNamespacesInput")
    def included_namespaces_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includedNamespacesInput"))

    @builtins.property
    @jsii.member(jsii_name="includedResourceTypesInput")
    def included_resource_types_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includedResourceTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="labelSelectorsInput")
    def label_selectors_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "labelSelectorsInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeSnapshotEnabledInput")
    def volume_snapshot_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "volumeSnapshotEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterScopedResourcesEnabled")
    def cluster_scoped_resources_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "clusterScopedResourcesEnabled"))

    @cluster_scoped_resources_enabled.setter
    def cluster_scoped_resources_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e9cba83ea59ef89f01ec482cb84951c7536559c8e5583a436a5a69444f5f059)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterScopedResourcesEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludedNamespaces")
    def excluded_namespaces(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedNamespaces"))

    @excluded_namespaces.setter
    def excluded_namespaces(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__126412799a8a1e7f331769552005c753dd34397e8db10f7b648f94cf1d10192c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedNamespaces", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludedResourceTypes")
    def excluded_resource_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedResourceTypes"))

    @excluded_resource_types.setter
    def excluded_resource_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56daec80e0a17e9925a1029bb6ce3da0a2ee5ef127ef307aedd1ffe230fdabec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedResourceTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includedNamespaces")
    def included_namespaces(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includedNamespaces"))

    @included_namespaces.setter
    def included_namespaces(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46ad8c2a291a4c42bfef16c8205dcf5085d48ac963a958be0fd9e21d4826e486)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedNamespaces", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includedResourceTypes")
    def included_resource_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includedResourceTypes"))

    @included_resource_types.setter
    def included_resource_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03f510d3bf00aa9168fe5f2d3a2f69b9f558efaf4e42349adf93a52112fb4e69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedResourceTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labelSelectors")
    def label_selectors(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "labelSelectors"))

    @label_selectors.setter
    def label_selectors(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__287d903d4c36ed89c20b6ebc2eb120441e56a2c3dc07d7c6107992ac35999e70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labelSelectors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeSnapshotEnabled")
    def volume_snapshot_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "volumeSnapshotEnabled"))

    @volume_snapshot_enabled.setter
    def volume_snapshot_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e1bb5c7474167a95fa85cedc91faf4f36b909042f4780ce89693e08d814314c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeSnapshotEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataProtectionBackupInstanceKubernetesClusterBackupDatasourceParameters]:
        return typing.cast(typing.Optional[DataProtectionBackupInstanceKubernetesClusterBackupDatasourceParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataProtectionBackupInstanceKubernetesClusterBackupDatasourceParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbc38860251f20531b6c0752970350063940daa0b881cde5cfd169c7639479f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupInstanceKubernetesCluster.DataProtectionBackupInstanceKubernetesClusterConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "backup_policy_id": "backupPolicyId",
        "kubernetes_cluster_id": "kubernetesClusterId",
        "location": "location",
        "name": "name",
        "snapshot_resource_group_name": "snapshotResourceGroupName",
        "vault_id": "vaultId",
        "backup_datasource_parameters": "backupDatasourceParameters",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class DataProtectionBackupInstanceKubernetesClusterConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        backup_policy_id: builtins.str,
        kubernetes_cluster_id: builtins.str,
        location: builtins.str,
        name: builtins.str,
        snapshot_resource_group_name: builtins.str,
        vault_id: builtins.str,
        backup_datasource_parameters: typing.Optional[typing.Union[DataProtectionBackupInstanceKubernetesClusterBackupDatasourceParameters, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataProtectionBackupInstanceKubernetesClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param backup_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#backup_policy_id DataProtectionBackupInstanceKubernetesCluster#backup_policy_id}.
        :param kubernetes_cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#kubernetes_cluster_id DataProtectionBackupInstanceKubernetesCluster#kubernetes_cluster_id}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#location DataProtectionBackupInstanceKubernetesCluster#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#name DataProtectionBackupInstanceKubernetesCluster#name}.
        :param snapshot_resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#snapshot_resource_group_name DataProtectionBackupInstanceKubernetesCluster#snapshot_resource_group_name}.
        :param vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#vault_id DataProtectionBackupInstanceKubernetesCluster#vault_id}.
        :param backup_datasource_parameters: backup_datasource_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#backup_datasource_parameters DataProtectionBackupInstanceKubernetesCluster#backup_datasource_parameters}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#id DataProtectionBackupInstanceKubernetesCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#timeouts DataProtectionBackupInstanceKubernetesCluster#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(backup_datasource_parameters, dict):
            backup_datasource_parameters = DataProtectionBackupInstanceKubernetesClusterBackupDatasourceParameters(**backup_datasource_parameters)
        if isinstance(timeouts, dict):
            timeouts = DataProtectionBackupInstanceKubernetesClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e91464ad2793a7b3a41e407f1ca6efaa6b14ce42dd14fdbbdd260b3a9e5cb05e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument backup_policy_id", value=backup_policy_id, expected_type=type_hints["backup_policy_id"])
            check_type(argname="argument kubernetes_cluster_id", value=kubernetes_cluster_id, expected_type=type_hints["kubernetes_cluster_id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument snapshot_resource_group_name", value=snapshot_resource_group_name, expected_type=type_hints["snapshot_resource_group_name"])
            check_type(argname="argument vault_id", value=vault_id, expected_type=type_hints["vault_id"])
            check_type(argname="argument backup_datasource_parameters", value=backup_datasource_parameters, expected_type=type_hints["backup_datasource_parameters"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "backup_policy_id": backup_policy_id,
            "kubernetes_cluster_id": kubernetes_cluster_id,
            "location": location,
            "name": name,
            "snapshot_resource_group_name": snapshot_resource_group_name,
            "vault_id": vault_id,
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
        if backup_datasource_parameters is not None:
            self._values["backup_datasource_parameters"] = backup_datasource_parameters
        if id is not None:
            self._values["id"] = id
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
    def backup_policy_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#backup_policy_id DataProtectionBackupInstanceKubernetesCluster#backup_policy_id}.'''
        result = self._values.get("backup_policy_id")
        assert result is not None, "Required property 'backup_policy_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kubernetes_cluster_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#kubernetes_cluster_id DataProtectionBackupInstanceKubernetesCluster#kubernetes_cluster_id}.'''
        result = self._values.get("kubernetes_cluster_id")
        assert result is not None, "Required property 'kubernetes_cluster_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#location DataProtectionBackupInstanceKubernetesCluster#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#name DataProtectionBackupInstanceKubernetesCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def snapshot_resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#snapshot_resource_group_name DataProtectionBackupInstanceKubernetesCluster#snapshot_resource_group_name}.'''
        result = self._values.get("snapshot_resource_group_name")
        assert result is not None, "Required property 'snapshot_resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vault_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#vault_id DataProtectionBackupInstanceKubernetesCluster#vault_id}.'''
        result = self._values.get("vault_id")
        assert result is not None, "Required property 'vault_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backup_datasource_parameters(
        self,
    ) -> typing.Optional[DataProtectionBackupInstanceKubernetesClusterBackupDatasourceParameters]:
        '''backup_datasource_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#backup_datasource_parameters DataProtectionBackupInstanceKubernetesCluster#backup_datasource_parameters}
        '''
        result = self._values.get("backup_datasource_parameters")
        return typing.cast(typing.Optional[DataProtectionBackupInstanceKubernetesClusterBackupDatasourceParameters], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#id DataProtectionBackupInstanceKubernetesCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["DataProtectionBackupInstanceKubernetesClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#timeouts DataProtectionBackupInstanceKubernetesCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataProtectionBackupInstanceKubernetesClusterTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProtectionBackupInstanceKubernetesClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupInstanceKubernetesCluster.DataProtectionBackupInstanceKubernetesClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "read": "read"},
)
class DataProtectionBackupInstanceKubernetesClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#create DataProtectionBackupInstanceKubernetesCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#delete DataProtectionBackupInstanceKubernetesCluster#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#read DataProtectionBackupInstanceKubernetesCluster#read}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da50df3c0270d8737e18915af4661c6257e03feaee3da51cafe5e2dc3950df53)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#create DataProtectionBackupInstanceKubernetesCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#delete DataProtectionBackupInstanceKubernetesCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_protection_backup_instance_kubernetes_cluster#read DataProtectionBackupInstanceKubernetesCluster#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProtectionBackupInstanceKubernetesClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataProtectionBackupInstanceKubernetesClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupInstanceKubernetesCluster.DataProtectionBackupInstanceKubernetesClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dde03f7829583d2a82f349d4d53ae663009f85f1f9abc0affe39e50edc8ef1c7)
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
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71de95bfffea8cc7116c71c9a98bfc5b0f6cda3cbe5a1076b2591bea26216032)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d73e85e97b9ebf01a0d0f963bbf1affa995d0494c1c1e2380beef4a81571ae6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66c81b7ed52f645c8642778076d44999b3e757b4a0b2dc92010057949ca50e2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupInstanceKubernetesClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupInstanceKubernetesClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupInstanceKubernetesClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6f06d57823959bdf8fa491faa0b0c6032c5d6b89940b9305b364fb26539ae83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataProtectionBackupInstanceKubernetesCluster",
    "DataProtectionBackupInstanceKubernetesClusterBackupDatasourceParameters",
    "DataProtectionBackupInstanceKubernetesClusterBackupDatasourceParametersOutputReference",
    "DataProtectionBackupInstanceKubernetesClusterConfig",
    "DataProtectionBackupInstanceKubernetesClusterTimeouts",
    "DataProtectionBackupInstanceKubernetesClusterTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__930db50115f0747be0e563b05480904a4993a503cba4e1a4cee0dedc82486277(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    backup_policy_id: builtins.str,
    kubernetes_cluster_id: builtins.str,
    location: builtins.str,
    name: builtins.str,
    snapshot_resource_group_name: builtins.str,
    vault_id: builtins.str,
    backup_datasource_parameters: typing.Optional[typing.Union[DataProtectionBackupInstanceKubernetesClusterBackupDatasourceParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataProtectionBackupInstanceKubernetesClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__d6f301f9022c38961b12314646b785d1ac0e3400c0de4024edc8a656685a03c4(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50af5c61410ffd92f0080f8f40aa34d2798f17518f1eee429ac5be1130eb38e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f423e3748f49567556244a253b92986a3a1862a271db3c6c264ef2630414b81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb857aaa1176d6f143fd93e02c739f4ded89dceff82c89caae1757199433be01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7432bac5f6c9b363711ee796129f062dfd7353c0014208c7042fa9528d6d2c32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b567e503ed734db1449237d098efd0d4eaf891f0f90f2642f9a5870bd29f9a35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae0c51b90694505c046f55d53427d0468348387759d38a29d88953ef45c210c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90a508cbba22cadf4cda8bc9e6f60d988e1686a2450dc0d268ba0f0499c31fef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b7c9c28a89a421f845fd320c36891da36a8b1e802a508da2b475dbc127029bf(
    *,
    cluster_scoped_resources_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    excluded_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
    excluded_resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    included_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
    included_resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    label_selectors: typing.Optional[typing.Sequence[builtins.str]] = None,
    volume_snapshot_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a9b188b3e37d91657371b996239e6a255db5b01e277653db5e3b5fb77acc52c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e9cba83ea59ef89f01ec482cb84951c7536559c8e5583a436a5a69444f5f059(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__126412799a8a1e7f331769552005c753dd34397e8db10f7b648f94cf1d10192c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56daec80e0a17e9925a1029bb6ce3da0a2ee5ef127ef307aedd1ffe230fdabec(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46ad8c2a291a4c42bfef16c8205dcf5085d48ac963a958be0fd9e21d4826e486(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03f510d3bf00aa9168fe5f2d3a2f69b9f558efaf4e42349adf93a52112fb4e69(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__287d903d4c36ed89c20b6ebc2eb120441e56a2c3dc07d7c6107992ac35999e70(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e1bb5c7474167a95fa85cedc91faf4f36b909042f4780ce89693e08d814314c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbc38860251f20531b6c0752970350063940daa0b881cde5cfd169c7639479f5(
    value: typing.Optional[DataProtectionBackupInstanceKubernetesClusterBackupDatasourceParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e91464ad2793a7b3a41e407f1ca6efaa6b14ce42dd14fdbbdd260b3a9e5cb05e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    backup_policy_id: builtins.str,
    kubernetes_cluster_id: builtins.str,
    location: builtins.str,
    name: builtins.str,
    snapshot_resource_group_name: builtins.str,
    vault_id: builtins.str,
    backup_datasource_parameters: typing.Optional[typing.Union[DataProtectionBackupInstanceKubernetesClusterBackupDatasourceParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataProtectionBackupInstanceKubernetesClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da50df3c0270d8737e18915af4661c6257e03feaee3da51cafe5e2dc3950df53(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dde03f7829583d2a82f349d4d53ae663009f85f1f9abc0affe39e50edc8ef1c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71de95bfffea8cc7116c71c9a98bfc5b0f6cda3cbe5a1076b2591bea26216032(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d73e85e97b9ebf01a0d0f963bbf1affa995d0494c1c1e2380beef4a81571ae6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66c81b7ed52f645c8642778076d44999b3e757b4a0b2dc92010057949ca50e2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6f06d57823959bdf8fa491faa0b0c6032c5d6b89940b9305b364fb26539ae83(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataProtectionBackupInstanceKubernetesClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
