r'''
# `azurerm_cosmosdb_sql_container`

Refer to the Terraform Registry for docs: [`azurerm_cosmosdb_sql_container`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container).
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


class CosmosdbSqlContainer(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbSqlContainer.CosmosdbSqlContainer",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container azurerm_cosmosdb_sql_container}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        account_name: builtins.str,
        database_name: builtins.str,
        name: builtins.str,
        partition_key_paths: typing.Sequence[builtins.str],
        resource_group_name: builtins.str,
        analytical_storage_ttl: typing.Optional[jsii.Number] = None,
        autoscale_settings: typing.Optional[typing.Union["CosmosdbSqlContainerAutoscaleSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        conflict_resolution_policy: typing.Optional[typing.Union["CosmosdbSqlContainerConflictResolutionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        default_ttl: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        indexing_policy: typing.Optional[typing.Union["CosmosdbSqlContainerIndexingPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        partition_key_kind: typing.Optional[builtins.str] = None,
        partition_key_version: typing.Optional[jsii.Number] = None,
        throughput: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["CosmosdbSqlContainerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        unique_key: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CosmosdbSqlContainerUniqueKey", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container azurerm_cosmosdb_sql_container} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#account_name CosmosdbSqlContainer#account_name}.
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#database_name CosmosdbSqlContainer#database_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#name CosmosdbSqlContainer#name}.
        :param partition_key_paths: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#partition_key_paths CosmosdbSqlContainer#partition_key_paths}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#resource_group_name CosmosdbSqlContainer#resource_group_name}.
        :param analytical_storage_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#analytical_storage_ttl CosmosdbSqlContainer#analytical_storage_ttl}.
        :param autoscale_settings: autoscale_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#autoscale_settings CosmosdbSqlContainer#autoscale_settings}
        :param conflict_resolution_policy: conflict_resolution_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#conflict_resolution_policy CosmosdbSqlContainer#conflict_resolution_policy}
        :param default_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#default_ttl CosmosdbSqlContainer#default_ttl}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#id CosmosdbSqlContainer#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param indexing_policy: indexing_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#indexing_policy CosmosdbSqlContainer#indexing_policy}
        :param partition_key_kind: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#partition_key_kind CosmosdbSqlContainer#partition_key_kind}.
        :param partition_key_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#partition_key_version CosmosdbSqlContainer#partition_key_version}.
        :param throughput: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#throughput CosmosdbSqlContainer#throughput}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#timeouts CosmosdbSqlContainer#timeouts}
        :param unique_key: unique_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#unique_key CosmosdbSqlContainer#unique_key}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1691175d9fcd6444a4a57af57c106b2060e117b60a7a1655c8091f666361ce97)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CosmosdbSqlContainerConfig(
            account_name=account_name,
            database_name=database_name,
            name=name,
            partition_key_paths=partition_key_paths,
            resource_group_name=resource_group_name,
            analytical_storage_ttl=analytical_storage_ttl,
            autoscale_settings=autoscale_settings,
            conflict_resolution_policy=conflict_resolution_policy,
            default_ttl=default_ttl,
            id=id,
            indexing_policy=indexing_policy,
            partition_key_kind=partition_key_kind,
            partition_key_version=partition_key_version,
            throughput=throughput,
            timeouts=timeouts,
            unique_key=unique_key,
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
        '''Generates CDKTF code for importing a CosmosdbSqlContainer resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CosmosdbSqlContainer to import.
        :param import_from_id: The id of the existing CosmosdbSqlContainer that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CosmosdbSqlContainer to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b68cabe42ccec21112609347115d4bde59410546b08b47b5856f2f610eb7b3b6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAutoscaleSettings")
    def put_autoscale_settings(
        self,
        *,
        max_throughput: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_throughput: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#max_throughput CosmosdbSqlContainer#max_throughput}.
        '''
        value = CosmosdbSqlContainerAutoscaleSettings(max_throughput=max_throughput)

        return typing.cast(None, jsii.invoke(self, "putAutoscaleSettings", [value]))

    @jsii.member(jsii_name="putConflictResolutionPolicy")
    def put_conflict_resolution_policy(
        self,
        *,
        mode: builtins.str,
        conflict_resolution_path: typing.Optional[builtins.str] = None,
        conflict_resolution_procedure: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#mode CosmosdbSqlContainer#mode}.
        :param conflict_resolution_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#conflict_resolution_path CosmosdbSqlContainer#conflict_resolution_path}.
        :param conflict_resolution_procedure: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#conflict_resolution_procedure CosmosdbSqlContainer#conflict_resolution_procedure}.
        '''
        value = CosmosdbSqlContainerConflictResolutionPolicy(
            mode=mode,
            conflict_resolution_path=conflict_resolution_path,
            conflict_resolution_procedure=conflict_resolution_procedure,
        )

        return typing.cast(None, jsii.invoke(self, "putConflictResolutionPolicy", [value]))

    @jsii.member(jsii_name="putIndexingPolicy")
    def put_indexing_policy(
        self,
        *,
        composite_index: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CosmosdbSqlContainerIndexingPolicyCompositeIndex", typing.Dict[builtins.str, typing.Any]]]]] = None,
        excluded_path: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CosmosdbSqlContainerIndexingPolicyExcludedPath", typing.Dict[builtins.str, typing.Any]]]]] = None,
        included_path: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CosmosdbSqlContainerIndexingPolicyIncludedPath", typing.Dict[builtins.str, typing.Any]]]]] = None,
        indexing_mode: typing.Optional[builtins.str] = None,
        spatial_index: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CosmosdbSqlContainerIndexingPolicySpatialIndex", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param composite_index: composite_index block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#composite_index CosmosdbSqlContainer#composite_index}
        :param excluded_path: excluded_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#excluded_path CosmosdbSqlContainer#excluded_path}
        :param included_path: included_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#included_path CosmosdbSqlContainer#included_path}
        :param indexing_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#indexing_mode CosmosdbSqlContainer#indexing_mode}.
        :param spatial_index: spatial_index block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#spatial_index CosmosdbSqlContainer#spatial_index}
        '''
        value = CosmosdbSqlContainerIndexingPolicy(
            composite_index=composite_index,
            excluded_path=excluded_path,
            included_path=included_path,
            indexing_mode=indexing_mode,
            spatial_index=spatial_index,
        )

        return typing.cast(None, jsii.invoke(self, "putIndexingPolicy", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#create CosmosdbSqlContainer#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#delete CosmosdbSqlContainer#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#read CosmosdbSqlContainer#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#update CosmosdbSqlContainer#update}.
        '''
        value = CosmosdbSqlContainerTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putUniqueKey")
    def put_unique_key(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CosmosdbSqlContainerUniqueKey", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3f6a87ff4f959b63dcd5b06004f8978acda405c798e502532debb8494745e2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUniqueKey", [value]))

    @jsii.member(jsii_name="resetAnalyticalStorageTtl")
    def reset_analytical_storage_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnalyticalStorageTtl", []))

    @jsii.member(jsii_name="resetAutoscaleSettings")
    def reset_autoscale_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscaleSettings", []))

    @jsii.member(jsii_name="resetConflictResolutionPolicy")
    def reset_conflict_resolution_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConflictResolutionPolicy", []))

    @jsii.member(jsii_name="resetDefaultTtl")
    def reset_default_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultTtl", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIndexingPolicy")
    def reset_indexing_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIndexingPolicy", []))

    @jsii.member(jsii_name="resetPartitionKeyKind")
    def reset_partition_key_kind(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartitionKeyKind", []))

    @jsii.member(jsii_name="resetPartitionKeyVersion")
    def reset_partition_key_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartitionKeyVersion", []))

    @jsii.member(jsii_name="resetThroughput")
    def reset_throughput(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThroughput", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUniqueKey")
    def reset_unique_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUniqueKey", []))

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
    @jsii.member(jsii_name="autoscaleSettings")
    def autoscale_settings(
        self,
    ) -> "CosmosdbSqlContainerAutoscaleSettingsOutputReference":
        return typing.cast("CosmosdbSqlContainerAutoscaleSettingsOutputReference", jsii.get(self, "autoscaleSettings"))

    @builtins.property
    @jsii.member(jsii_name="conflictResolutionPolicy")
    def conflict_resolution_policy(
        self,
    ) -> "CosmosdbSqlContainerConflictResolutionPolicyOutputReference":
        return typing.cast("CosmosdbSqlContainerConflictResolutionPolicyOutputReference", jsii.get(self, "conflictResolutionPolicy"))

    @builtins.property
    @jsii.member(jsii_name="indexingPolicy")
    def indexing_policy(self) -> "CosmosdbSqlContainerIndexingPolicyOutputReference":
        return typing.cast("CosmosdbSqlContainerIndexingPolicyOutputReference", jsii.get(self, "indexingPolicy"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CosmosdbSqlContainerTimeoutsOutputReference":
        return typing.cast("CosmosdbSqlContainerTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uniqueKey")
    def unique_key(self) -> "CosmosdbSqlContainerUniqueKeyList":
        return typing.cast("CosmosdbSqlContainerUniqueKeyList", jsii.get(self, "uniqueKey"))

    @builtins.property
    @jsii.member(jsii_name="accountNameInput")
    def account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="analyticalStorageTtlInput")
    def analytical_storage_ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "analyticalStorageTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="autoscaleSettingsInput")
    def autoscale_settings_input(
        self,
    ) -> typing.Optional["CosmosdbSqlContainerAutoscaleSettings"]:
        return typing.cast(typing.Optional["CosmosdbSqlContainerAutoscaleSettings"], jsii.get(self, "autoscaleSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="conflictResolutionPolicyInput")
    def conflict_resolution_policy_input(
        self,
    ) -> typing.Optional["CosmosdbSqlContainerConflictResolutionPolicy"]:
        return typing.cast(typing.Optional["CosmosdbSqlContainerConflictResolutionPolicy"], jsii.get(self, "conflictResolutionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseNameInput")
    def database_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseNameInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultTtlInput")
    def default_ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="indexingPolicyInput")
    def indexing_policy_input(
        self,
    ) -> typing.Optional["CosmosdbSqlContainerIndexingPolicy"]:
        return typing.cast(typing.Optional["CosmosdbSqlContainerIndexingPolicy"], jsii.get(self, "indexingPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="partitionKeyKindInput")
    def partition_key_kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "partitionKeyKindInput"))

    @builtins.property
    @jsii.member(jsii_name="partitionKeyPathsInput")
    def partition_key_paths_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "partitionKeyPathsInput"))

    @builtins.property
    @jsii.member(jsii_name="partitionKeyVersionInput")
    def partition_key_version_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "partitionKeyVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="throughputInput")
    def throughput_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "throughputInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CosmosdbSqlContainerTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CosmosdbSqlContainerTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="uniqueKeyInput")
    def unique_key_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbSqlContainerUniqueKey"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbSqlContainerUniqueKey"]]], jsii.get(self, "uniqueKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="accountName")
    def account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountName"))

    @account_name.setter
    def account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c46e26fe6f30291d853218242bc8054d551d3ed476c6028011c37e63f8ed346c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="analyticalStorageTtl")
    def analytical_storage_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "analyticalStorageTtl"))

    @analytical_storage_ttl.setter
    def analytical_storage_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a169dcb767ba5a07c21a19eb62551df68d82012f10e834d210c5385f4d9c30de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "analyticalStorageTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @database_name.setter
    def database_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8369e6c29838d61c72a4b18459e73f11d64190910299ff0cc3f1bde2b885ec98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultTtl")
    def default_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultTtl"))

    @default_ttl.setter
    def default_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d98250c76db8ba7723d1da91edfc78469b683b6e8d09abff6fccd8578a32df6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e5f1255dd9ba8c42d84358b6069ce92279c0c3d852f9f2c50a5b8cf96707d21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__591778811afa82d42f7b5da39c9b96df47b12c0d4bf922d1e96896127f0b5e02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partitionKeyKind")
    def partition_key_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "partitionKeyKind"))

    @partition_key_kind.setter
    def partition_key_kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5661973cddbf8cee1c991ee156fc51222fcd8e7cab4c4b0251217d5ac6a34151)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partitionKeyKind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partitionKeyPaths")
    def partition_key_paths(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "partitionKeyPaths"))

    @partition_key_paths.setter
    def partition_key_paths(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a207f3c84492a96cba7bf52c1d5a8a6ce64a95120a3622709275573e5608c19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partitionKeyPaths", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partitionKeyVersion")
    def partition_key_version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "partitionKeyVersion"))

    @partition_key_version.setter
    def partition_key_version(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d91c53d13fed196a585b75cd078a7094657f4b938fa25a614ac0a79064ba4b6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partitionKeyVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fc56e44f61315f9af2927d136caa8e511c87d4bdae283b48dc9a30979315324)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="throughput")
    def throughput(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "throughput"))

    @throughput.setter
    def throughput(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63cd43e9713ff1c8c91638f866c5c2816413fe9e78992628690601f8b90120d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throughput", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbSqlContainer.CosmosdbSqlContainerAutoscaleSettings",
    jsii_struct_bases=[],
    name_mapping={"max_throughput": "maxThroughput"},
)
class CosmosdbSqlContainerAutoscaleSettings:
    def __init__(self, *, max_throughput: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param max_throughput: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#max_throughput CosmosdbSqlContainer#max_throughput}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bee75d56aa51ee460c2a7e690e9bfa3273f16c339b03af7cc1f1c4726999630)
            check_type(argname="argument max_throughput", value=max_throughput, expected_type=type_hints["max_throughput"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_throughput is not None:
            self._values["max_throughput"] = max_throughput

    @builtins.property
    def max_throughput(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#max_throughput CosmosdbSqlContainer#max_throughput}.'''
        result = self._values.get("max_throughput")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbSqlContainerAutoscaleSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CosmosdbSqlContainerAutoscaleSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbSqlContainer.CosmosdbSqlContainerAutoscaleSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c701f39df6bfe17bf2bb3713d55e31305427d0ac632030c84a6c198537d4979)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxThroughput")
    def reset_max_throughput(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxThroughput", []))

    @builtins.property
    @jsii.member(jsii_name="maxThroughputInput")
    def max_throughput_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxThroughputInput"))

    @builtins.property
    @jsii.member(jsii_name="maxThroughput")
    def max_throughput(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxThroughput"))

    @max_throughput.setter
    def max_throughput(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__844eecfe91c74f36fd32b2cf03e3ba57e2c71aaa1cbfe27aef4301550adbf0b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxThroughput", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CosmosdbSqlContainerAutoscaleSettings]:
        return typing.cast(typing.Optional[CosmosdbSqlContainerAutoscaleSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CosmosdbSqlContainerAutoscaleSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b784386436ddae1a8b899378555125ffa84b1c3e3073d89b5fdab350002626e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbSqlContainer.CosmosdbSqlContainerConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "account_name": "accountName",
        "database_name": "databaseName",
        "name": "name",
        "partition_key_paths": "partitionKeyPaths",
        "resource_group_name": "resourceGroupName",
        "analytical_storage_ttl": "analyticalStorageTtl",
        "autoscale_settings": "autoscaleSettings",
        "conflict_resolution_policy": "conflictResolutionPolicy",
        "default_ttl": "defaultTtl",
        "id": "id",
        "indexing_policy": "indexingPolicy",
        "partition_key_kind": "partitionKeyKind",
        "partition_key_version": "partitionKeyVersion",
        "throughput": "throughput",
        "timeouts": "timeouts",
        "unique_key": "uniqueKey",
    },
)
class CosmosdbSqlContainerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        account_name: builtins.str,
        database_name: builtins.str,
        name: builtins.str,
        partition_key_paths: typing.Sequence[builtins.str],
        resource_group_name: builtins.str,
        analytical_storage_ttl: typing.Optional[jsii.Number] = None,
        autoscale_settings: typing.Optional[typing.Union[CosmosdbSqlContainerAutoscaleSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        conflict_resolution_policy: typing.Optional[typing.Union["CosmosdbSqlContainerConflictResolutionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        default_ttl: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        indexing_policy: typing.Optional[typing.Union["CosmosdbSqlContainerIndexingPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        partition_key_kind: typing.Optional[builtins.str] = None,
        partition_key_version: typing.Optional[jsii.Number] = None,
        throughput: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["CosmosdbSqlContainerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        unique_key: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CosmosdbSqlContainerUniqueKey", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#account_name CosmosdbSqlContainer#account_name}.
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#database_name CosmosdbSqlContainer#database_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#name CosmosdbSqlContainer#name}.
        :param partition_key_paths: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#partition_key_paths CosmosdbSqlContainer#partition_key_paths}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#resource_group_name CosmosdbSqlContainer#resource_group_name}.
        :param analytical_storage_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#analytical_storage_ttl CosmosdbSqlContainer#analytical_storage_ttl}.
        :param autoscale_settings: autoscale_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#autoscale_settings CosmosdbSqlContainer#autoscale_settings}
        :param conflict_resolution_policy: conflict_resolution_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#conflict_resolution_policy CosmosdbSqlContainer#conflict_resolution_policy}
        :param default_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#default_ttl CosmosdbSqlContainer#default_ttl}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#id CosmosdbSqlContainer#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param indexing_policy: indexing_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#indexing_policy CosmosdbSqlContainer#indexing_policy}
        :param partition_key_kind: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#partition_key_kind CosmosdbSqlContainer#partition_key_kind}.
        :param partition_key_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#partition_key_version CosmosdbSqlContainer#partition_key_version}.
        :param throughput: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#throughput CosmosdbSqlContainer#throughput}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#timeouts CosmosdbSqlContainer#timeouts}
        :param unique_key: unique_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#unique_key CosmosdbSqlContainer#unique_key}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(autoscale_settings, dict):
            autoscale_settings = CosmosdbSqlContainerAutoscaleSettings(**autoscale_settings)
        if isinstance(conflict_resolution_policy, dict):
            conflict_resolution_policy = CosmosdbSqlContainerConflictResolutionPolicy(**conflict_resolution_policy)
        if isinstance(indexing_policy, dict):
            indexing_policy = CosmosdbSqlContainerIndexingPolicy(**indexing_policy)
        if isinstance(timeouts, dict):
            timeouts = CosmosdbSqlContainerTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c50580e4f0fcc4711e98010e7212aa4e423970a36dfc78f03d029d353091e452)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument account_name", value=account_name, expected_type=type_hints["account_name"])
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument partition_key_paths", value=partition_key_paths, expected_type=type_hints["partition_key_paths"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument analytical_storage_ttl", value=analytical_storage_ttl, expected_type=type_hints["analytical_storage_ttl"])
            check_type(argname="argument autoscale_settings", value=autoscale_settings, expected_type=type_hints["autoscale_settings"])
            check_type(argname="argument conflict_resolution_policy", value=conflict_resolution_policy, expected_type=type_hints["conflict_resolution_policy"])
            check_type(argname="argument default_ttl", value=default_ttl, expected_type=type_hints["default_ttl"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument indexing_policy", value=indexing_policy, expected_type=type_hints["indexing_policy"])
            check_type(argname="argument partition_key_kind", value=partition_key_kind, expected_type=type_hints["partition_key_kind"])
            check_type(argname="argument partition_key_version", value=partition_key_version, expected_type=type_hints["partition_key_version"])
            check_type(argname="argument throughput", value=throughput, expected_type=type_hints["throughput"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument unique_key", value=unique_key, expected_type=type_hints["unique_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_name": account_name,
            "database_name": database_name,
            "name": name,
            "partition_key_paths": partition_key_paths,
            "resource_group_name": resource_group_name,
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
        if analytical_storage_ttl is not None:
            self._values["analytical_storage_ttl"] = analytical_storage_ttl
        if autoscale_settings is not None:
            self._values["autoscale_settings"] = autoscale_settings
        if conflict_resolution_policy is not None:
            self._values["conflict_resolution_policy"] = conflict_resolution_policy
        if default_ttl is not None:
            self._values["default_ttl"] = default_ttl
        if id is not None:
            self._values["id"] = id
        if indexing_policy is not None:
            self._values["indexing_policy"] = indexing_policy
        if partition_key_kind is not None:
            self._values["partition_key_kind"] = partition_key_kind
        if partition_key_version is not None:
            self._values["partition_key_version"] = partition_key_version
        if throughput is not None:
            self._values["throughput"] = throughput
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if unique_key is not None:
            self._values["unique_key"] = unique_key

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
    def account_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#account_name CosmosdbSqlContainer#account_name}.'''
        result = self._values.get("account_name")
        assert result is not None, "Required property 'account_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def database_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#database_name CosmosdbSqlContainer#database_name}.'''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#name CosmosdbSqlContainer#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def partition_key_paths(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#partition_key_paths CosmosdbSqlContainer#partition_key_paths}.'''
        result = self._values.get("partition_key_paths")
        assert result is not None, "Required property 'partition_key_paths' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#resource_group_name CosmosdbSqlContainer#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def analytical_storage_ttl(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#analytical_storage_ttl CosmosdbSqlContainer#analytical_storage_ttl}.'''
        result = self._values.get("analytical_storage_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def autoscale_settings(
        self,
    ) -> typing.Optional[CosmosdbSqlContainerAutoscaleSettings]:
        '''autoscale_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#autoscale_settings CosmosdbSqlContainer#autoscale_settings}
        '''
        result = self._values.get("autoscale_settings")
        return typing.cast(typing.Optional[CosmosdbSqlContainerAutoscaleSettings], result)

    @builtins.property
    def conflict_resolution_policy(
        self,
    ) -> typing.Optional["CosmosdbSqlContainerConflictResolutionPolicy"]:
        '''conflict_resolution_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#conflict_resolution_policy CosmosdbSqlContainer#conflict_resolution_policy}
        '''
        result = self._values.get("conflict_resolution_policy")
        return typing.cast(typing.Optional["CosmosdbSqlContainerConflictResolutionPolicy"], result)

    @builtins.property
    def default_ttl(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#default_ttl CosmosdbSqlContainer#default_ttl}.'''
        result = self._values.get("default_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#id CosmosdbSqlContainer#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def indexing_policy(self) -> typing.Optional["CosmosdbSqlContainerIndexingPolicy"]:
        '''indexing_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#indexing_policy CosmosdbSqlContainer#indexing_policy}
        '''
        result = self._values.get("indexing_policy")
        return typing.cast(typing.Optional["CosmosdbSqlContainerIndexingPolicy"], result)

    @builtins.property
    def partition_key_kind(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#partition_key_kind CosmosdbSqlContainer#partition_key_kind}.'''
        result = self._values.get("partition_key_kind")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def partition_key_version(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#partition_key_version CosmosdbSqlContainer#partition_key_version}.'''
        result = self._values.get("partition_key_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def throughput(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#throughput CosmosdbSqlContainer#throughput}.'''
        result = self._values.get("throughput")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CosmosdbSqlContainerTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#timeouts CosmosdbSqlContainer#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CosmosdbSqlContainerTimeouts"], result)

    @builtins.property
    def unique_key(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbSqlContainerUniqueKey"]]]:
        '''unique_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#unique_key CosmosdbSqlContainer#unique_key}
        '''
        result = self._values.get("unique_key")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbSqlContainerUniqueKey"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbSqlContainerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbSqlContainer.CosmosdbSqlContainerConflictResolutionPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "mode": "mode",
        "conflict_resolution_path": "conflictResolutionPath",
        "conflict_resolution_procedure": "conflictResolutionProcedure",
    },
)
class CosmosdbSqlContainerConflictResolutionPolicy:
    def __init__(
        self,
        *,
        mode: builtins.str,
        conflict_resolution_path: typing.Optional[builtins.str] = None,
        conflict_resolution_procedure: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#mode CosmosdbSqlContainer#mode}.
        :param conflict_resolution_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#conflict_resolution_path CosmosdbSqlContainer#conflict_resolution_path}.
        :param conflict_resolution_procedure: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#conflict_resolution_procedure CosmosdbSqlContainer#conflict_resolution_procedure}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e38501b4e73d56c5a7081e91269068a3e8a67f1de74faf33dd9880a32d4ca3d6)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument conflict_resolution_path", value=conflict_resolution_path, expected_type=type_hints["conflict_resolution_path"])
            check_type(argname="argument conflict_resolution_procedure", value=conflict_resolution_procedure, expected_type=type_hints["conflict_resolution_procedure"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
        }
        if conflict_resolution_path is not None:
            self._values["conflict_resolution_path"] = conflict_resolution_path
        if conflict_resolution_procedure is not None:
            self._values["conflict_resolution_procedure"] = conflict_resolution_procedure

    @builtins.property
    def mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#mode CosmosdbSqlContainer#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def conflict_resolution_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#conflict_resolution_path CosmosdbSqlContainer#conflict_resolution_path}.'''
        result = self._values.get("conflict_resolution_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def conflict_resolution_procedure(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#conflict_resolution_procedure CosmosdbSqlContainer#conflict_resolution_procedure}.'''
        result = self._values.get("conflict_resolution_procedure")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbSqlContainerConflictResolutionPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CosmosdbSqlContainerConflictResolutionPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbSqlContainer.CosmosdbSqlContainerConflictResolutionPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ebf018f3dd4240f2fb0bbc66b97d653210138a45be9ebe2c3632f2365bd3626)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetConflictResolutionPath")
    def reset_conflict_resolution_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConflictResolutionPath", []))

    @jsii.member(jsii_name="resetConflictResolutionProcedure")
    def reset_conflict_resolution_procedure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConflictResolutionProcedure", []))

    @builtins.property
    @jsii.member(jsii_name="conflictResolutionPathInput")
    def conflict_resolution_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conflictResolutionPathInput"))

    @builtins.property
    @jsii.member(jsii_name="conflictResolutionProcedureInput")
    def conflict_resolution_procedure_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conflictResolutionProcedureInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="conflictResolutionPath")
    def conflict_resolution_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "conflictResolutionPath"))

    @conflict_resolution_path.setter
    def conflict_resolution_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d281b96b2a97cc0c8ccff26dbcfb9a5c963615a6dffa05afd46585667e6c5ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "conflictResolutionPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="conflictResolutionProcedure")
    def conflict_resolution_procedure(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "conflictResolutionProcedure"))

    @conflict_resolution_procedure.setter
    def conflict_resolution_procedure(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f903d82c96257c6eef2513d665ca3ff028396897b007be2f694b0a00f1ac9c7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "conflictResolutionProcedure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__234c2cb7140206d1e860e32e3abe5eba98f145ad819e5cf45e2fb00812b59e71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CosmosdbSqlContainerConflictResolutionPolicy]:
        return typing.cast(typing.Optional[CosmosdbSqlContainerConflictResolutionPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CosmosdbSqlContainerConflictResolutionPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c1ff42a92ac609afa7de098a3f3bb3d1305159b000e4baa6e5e05c8fd1089db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbSqlContainer.CosmosdbSqlContainerIndexingPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "composite_index": "compositeIndex",
        "excluded_path": "excludedPath",
        "included_path": "includedPath",
        "indexing_mode": "indexingMode",
        "spatial_index": "spatialIndex",
    },
)
class CosmosdbSqlContainerIndexingPolicy:
    def __init__(
        self,
        *,
        composite_index: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CosmosdbSqlContainerIndexingPolicyCompositeIndex", typing.Dict[builtins.str, typing.Any]]]]] = None,
        excluded_path: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CosmosdbSqlContainerIndexingPolicyExcludedPath", typing.Dict[builtins.str, typing.Any]]]]] = None,
        included_path: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CosmosdbSqlContainerIndexingPolicyIncludedPath", typing.Dict[builtins.str, typing.Any]]]]] = None,
        indexing_mode: typing.Optional[builtins.str] = None,
        spatial_index: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CosmosdbSqlContainerIndexingPolicySpatialIndex", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param composite_index: composite_index block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#composite_index CosmosdbSqlContainer#composite_index}
        :param excluded_path: excluded_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#excluded_path CosmosdbSqlContainer#excluded_path}
        :param included_path: included_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#included_path CosmosdbSqlContainer#included_path}
        :param indexing_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#indexing_mode CosmosdbSqlContainer#indexing_mode}.
        :param spatial_index: spatial_index block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#spatial_index CosmosdbSqlContainer#spatial_index}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a8187b691f4e3654041b4fd239de88c7a1ca4dce0388aeb5aaf27cd973d679a)
            check_type(argname="argument composite_index", value=composite_index, expected_type=type_hints["composite_index"])
            check_type(argname="argument excluded_path", value=excluded_path, expected_type=type_hints["excluded_path"])
            check_type(argname="argument included_path", value=included_path, expected_type=type_hints["included_path"])
            check_type(argname="argument indexing_mode", value=indexing_mode, expected_type=type_hints["indexing_mode"])
            check_type(argname="argument spatial_index", value=spatial_index, expected_type=type_hints["spatial_index"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if composite_index is not None:
            self._values["composite_index"] = composite_index
        if excluded_path is not None:
            self._values["excluded_path"] = excluded_path
        if included_path is not None:
            self._values["included_path"] = included_path
        if indexing_mode is not None:
            self._values["indexing_mode"] = indexing_mode
        if spatial_index is not None:
            self._values["spatial_index"] = spatial_index

    @builtins.property
    def composite_index(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbSqlContainerIndexingPolicyCompositeIndex"]]]:
        '''composite_index block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#composite_index CosmosdbSqlContainer#composite_index}
        '''
        result = self._values.get("composite_index")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbSqlContainerIndexingPolicyCompositeIndex"]]], result)

    @builtins.property
    def excluded_path(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbSqlContainerIndexingPolicyExcludedPath"]]]:
        '''excluded_path block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#excluded_path CosmosdbSqlContainer#excluded_path}
        '''
        result = self._values.get("excluded_path")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbSqlContainerIndexingPolicyExcludedPath"]]], result)

    @builtins.property
    def included_path(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbSqlContainerIndexingPolicyIncludedPath"]]]:
        '''included_path block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#included_path CosmosdbSqlContainer#included_path}
        '''
        result = self._values.get("included_path")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbSqlContainerIndexingPolicyIncludedPath"]]], result)

    @builtins.property
    def indexing_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#indexing_mode CosmosdbSqlContainer#indexing_mode}.'''
        result = self._values.get("indexing_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spatial_index(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbSqlContainerIndexingPolicySpatialIndex"]]]:
        '''spatial_index block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#spatial_index CosmosdbSqlContainer#spatial_index}
        '''
        result = self._values.get("spatial_index")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbSqlContainerIndexingPolicySpatialIndex"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbSqlContainerIndexingPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbSqlContainer.CosmosdbSqlContainerIndexingPolicyCompositeIndex",
    jsii_struct_bases=[],
    name_mapping={"index": "index"},
)
class CosmosdbSqlContainerIndexingPolicyCompositeIndex:
    def __init__(
        self,
        *,
        index: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CosmosdbSqlContainerIndexingPolicyCompositeIndexIndex", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param index: index block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#index CosmosdbSqlContainer#index}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__387be593a2c88da8e3518c52c7a9231c75ee0ff65d296d27394f342768895851)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "index": index,
        }

    @builtins.property
    def index(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbSqlContainerIndexingPolicyCompositeIndexIndex"]]:
        '''index block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#index CosmosdbSqlContainer#index}
        '''
        result = self._values.get("index")
        assert result is not None, "Required property 'index' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbSqlContainerIndexingPolicyCompositeIndexIndex"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbSqlContainerIndexingPolicyCompositeIndex(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbSqlContainer.CosmosdbSqlContainerIndexingPolicyCompositeIndexIndex",
    jsii_struct_bases=[],
    name_mapping={"order": "order", "path": "path"},
)
class CosmosdbSqlContainerIndexingPolicyCompositeIndexIndex:
    def __init__(self, *, order: builtins.str, path: builtins.str) -> None:
        '''
        :param order: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#order CosmosdbSqlContainer#order}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#path CosmosdbSqlContainer#path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e3574ce32168bbbab5c5f0883e328d37bc2c40eca17d406019e4d42a7aa1cac)
            check_type(argname="argument order", value=order, expected_type=type_hints["order"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "order": order,
            "path": path,
        }

    @builtins.property
    def order(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#order CosmosdbSqlContainer#order}.'''
        result = self._values.get("order")
        assert result is not None, "Required property 'order' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#path CosmosdbSqlContainer#path}.'''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbSqlContainerIndexingPolicyCompositeIndexIndex(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CosmosdbSqlContainerIndexingPolicyCompositeIndexIndexList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbSqlContainer.CosmosdbSqlContainerIndexingPolicyCompositeIndexIndexList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__29395d6763f5ae615c784858c8210fb8f3f11c6bace64cb86a8d249973f41329)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CosmosdbSqlContainerIndexingPolicyCompositeIndexIndexOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdbcdebdae19e01df1acbd0dbd59cff0a4f685087ea67daa85a387013fb274e4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CosmosdbSqlContainerIndexingPolicyCompositeIndexIndexOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c656e7177bedb84a0ee1a981a97cfd96f0dc843d2804beea634ee5ccd79a5dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__adb49d459146d9678993f64880d6dd3d7171b166e828970d77f8fc85311514a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1030d4b0cbb4271568fc2eda0f07a556b2e1bdeb93aff63611a2f8a2ad32d73d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbSqlContainerIndexingPolicyCompositeIndexIndex]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbSqlContainerIndexingPolicyCompositeIndexIndex]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbSqlContainerIndexingPolicyCompositeIndexIndex]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76a1953a39adcafb9e4b2951bb68eac2df60c85cc0f9257ed0b2645a8abfba18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CosmosdbSqlContainerIndexingPolicyCompositeIndexIndexOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbSqlContainer.CosmosdbSqlContainerIndexingPolicyCompositeIndexIndexOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e31f95455d810c169bf73a285392f65e8f8a5785dc1a8be85a8829c70cee397)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="orderInput")
    def order_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orderInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="order")
    def order(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "order"))

    @order.setter
    def order(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c2a40e77a65788ecbef7ab69cf34dc1e6028cf105d204b4ff87fd0d3a935b43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "order", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54ef96628a003f3770693be58cf93235d043b80180ebdf5da245b0e1f11be008)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbSqlContainerIndexingPolicyCompositeIndexIndex]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbSqlContainerIndexingPolicyCompositeIndexIndex]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbSqlContainerIndexingPolicyCompositeIndexIndex]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4c1f49fb7e14c4ee5c901991015668423b4b0a2e9a3d1f65ba643f117332d18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CosmosdbSqlContainerIndexingPolicyCompositeIndexList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbSqlContainer.CosmosdbSqlContainerIndexingPolicyCompositeIndexList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__947e41f37f3ba1cbb027a7320c46ba6d03a876b8d0bd44493664aee439ebc793)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CosmosdbSqlContainerIndexingPolicyCompositeIndexOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9998414ff611278c3f8683c57ea0d8496d02afb65c34329dfb0673227a79c53c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CosmosdbSqlContainerIndexingPolicyCompositeIndexOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__220c287f567b130562a9d9b072efff76e1ce15af425544dc634a3f4d6686fccf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__22594fc0bf365e080da724c3652c5dcb29fd61b599e653c4b461a01b310a5c6f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__257bb2a1251701af872c06a0deeae74d9e6ff3f0ba87acad4a18dfb8e297e90f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbSqlContainerIndexingPolicyCompositeIndex]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbSqlContainerIndexingPolicyCompositeIndex]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbSqlContainerIndexingPolicyCompositeIndex]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5db702ef1955ca67df7b2a87f1d5bf384f410fb0b9d139a188e58aa0b9fce6af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CosmosdbSqlContainerIndexingPolicyCompositeIndexOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbSqlContainer.CosmosdbSqlContainerIndexingPolicyCompositeIndexOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c97b84f2d4f864c9bdbe5bb29c93fba412cd677769c1003e73be99ccbc9ef66f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putIndex")
    def put_index(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbSqlContainerIndexingPolicyCompositeIndexIndex, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0827ba14329c0fa31107da981ae0dfb4fd9acd2ed5c226142804b9a177e52392)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIndex", [value]))

    @builtins.property
    @jsii.member(jsii_name="index")
    def index(self) -> CosmosdbSqlContainerIndexingPolicyCompositeIndexIndexList:
        return typing.cast(CosmosdbSqlContainerIndexingPolicyCompositeIndexIndexList, jsii.get(self, "index"))

    @builtins.property
    @jsii.member(jsii_name="indexInput")
    def index_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbSqlContainerIndexingPolicyCompositeIndexIndex]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbSqlContainerIndexingPolicyCompositeIndexIndex]]], jsii.get(self, "indexInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbSqlContainerIndexingPolicyCompositeIndex]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbSqlContainerIndexingPolicyCompositeIndex]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbSqlContainerIndexingPolicyCompositeIndex]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__750450d6511aa78b249b6ea8d7bd8f09aa9851d7456ab735d8af9464f4de1129)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbSqlContainer.CosmosdbSqlContainerIndexingPolicyExcludedPath",
    jsii_struct_bases=[],
    name_mapping={"path": "path"},
)
class CosmosdbSqlContainerIndexingPolicyExcludedPath:
    def __init__(self, *, path: builtins.str) -> None:
        '''
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#path CosmosdbSqlContainer#path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b706a1babf899e5d022e18fd8c0083455123af373201efd610ca0c47cae33a9a)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
        }

    @builtins.property
    def path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#path CosmosdbSqlContainer#path}.'''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbSqlContainerIndexingPolicyExcludedPath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CosmosdbSqlContainerIndexingPolicyExcludedPathList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbSqlContainer.CosmosdbSqlContainerIndexingPolicyExcludedPathList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__31c927ba725391bd49aa6e49aa8ae92a4551d3faa9133b0c274806031aebd2a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CosmosdbSqlContainerIndexingPolicyExcludedPathOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f7467cc35bb607596dbfd2c621a77ca539d5f31c9fc1ccd4f11bdf06709d7bd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CosmosdbSqlContainerIndexingPolicyExcludedPathOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__236b0b3d6eacd1e768281e13f797e5b43a7a3a300fafff330b7aa30fb901f7f7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa414c18db063d29b69a03cee15ca6b598dda9860f5666797af0b58302ae0a05)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f38ab7782771f3d2953a37973fd036a287adbf3db757e847977671347d892cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbSqlContainerIndexingPolicyExcludedPath]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbSqlContainerIndexingPolicyExcludedPath]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbSqlContainerIndexingPolicyExcludedPath]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7a9be46fd2bae79ad69932758401d84fcd67e570b63b32aebb1bf27a4ea66b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CosmosdbSqlContainerIndexingPolicyExcludedPathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbSqlContainer.CosmosdbSqlContainerIndexingPolicyExcludedPathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9af0d649cea33b2d3af1e8881a9cb555dd0217738caa73b529e2d048bde496c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__549e4342ebefd48f08723c7784f12d412f008f2f020bc6dd21cb4e94d39ca55f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbSqlContainerIndexingPolicyExcludedPath]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbSqlContainerIndexingPolicyExcludedPath]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbSqlContainerIndexingPolicyExcludedPath]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0694bd34c2bc465a352db9a10cf21a7bd7333f3df3bb5a2d9df994adf528a9ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbSqlContainer.CosmosdbSqlContainerIndexingPolicyIncludedPath",
    jsii_struct_bases=[],
    name_mapping={"path": "path"},
)
class CosmosdbSqlContainerIndexingPolicyIncludedPath:
    def __init__(self, *, path: builtins.str) -> None:
        '''
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#path CosmosdbSqlContainer#path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe1cb58441b468cfd6eb4a3a1092cd2c77ad8add51555d674e23843a4a6930dd)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
        }

    @builtins.property
    def path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#path CosmosdbSqlContainer#path}.'''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbSqlContainerIndexingPolicyIncludedPath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CosmosdbSqlContainerIndexingPolicyIncludedPathList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbSqlContainer.CosmosdbSqlContainerIndexingPolicyIncludedPathList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b15c3011257360679ca8bf8de56670cb22e3a150132341e7b9cefeda6f979606)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CosmosdbSqlContainerIndexingPolicyIncludedPathOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69f251a571e2312fc614f056eda9e547c6d0d6455f3ed6b376bd6a4dcbc561f6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CosmosdbSqlContainerIndexingPolicyIncludedPathOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4d86e44c8ea9be7285973e656421671abc1d7b355ab3d10ef23ba46bd24af46)
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
            type_hints = typing.get_type_hints(_typecheckingstub__79afb4639e0dfba5b73a75b16bc55a22ec96107a646cd4d872d82a5c0cc2006c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8f508e0ad3a925fa32dcca1e09074e9d3bbb99d8f8ce06797748909949370b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbSqlContainerIndexingPolicyIncludedPath]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbSqlContainerIndexingPolicyIncludedPath]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbSqlContainerIndexingPolicyIncludedPath]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32ba727199ddeae8ee0d5d3f2c0e69527ed997397be1f4c18d8cce4b76e19522)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CosmosdbSqlContainerIndexingPolicyIncludedPathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbSqlContainer.CosmosdbSqlContainerIndexingPolicyIncludedPathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7000f5a7989b921b477b8328d3cef356985c1f683b9762f3a39e2fadc5d69ede)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0333018750a7f68292b5fafd88033753abc27a5882a81f4aacfc38eacad1afc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbSqlContainerIndexingPolicyIncludedPath]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbSqlContainerIndexingPolicyIncludedPath]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbSqlContainerIndexingPolicyIncludedPath]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b571fd487f86e74a13ad135ab8ffd6d79c795c2373eb2d2a50d9cba96f5392a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CosmosdbSqlContainerIndexingPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbSqlContainer.CosmosdbSqlContainerIndexingPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b6669dd5ba54a5adc775c1d7f0bbe120a6ec08ba5b93126df051503af672b36)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCompositeIndex")
    def put_composite_index(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbSqlContainerIndexingPolicyCompositeIndex, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df3a607f17573953b5ed5866f30e01a03e6307faeaa13dac0ad816e3d26b4b43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCompositeIndex", [value]))

    @jsii.member(jsii_name="putExcludedPath")
    def put_excluded_path(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbSqlContainerIndexingPolicyExcludedPath, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5465878d83fee2913170a4d332ebfae16a073ce3b7e46bfe8afd31d5fac4099)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExcludedPath", [value]))

    @jsii.member(jsii_name="putIncludedPath")
    def put_included_path(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbSqlContainerIndexingPolicyIncludedPath, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b12e16f0bb78fed6b94dd19c8285aa45a018ba4b5d3cd5bd1979d4d7c67a12d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIncludedPath", [value]))

    @jsii.member(jsii_name="putSpatialIndex")
    def put_spatial_index(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CosmosdbSqlContainerIndexingPolicySpatialIndex", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92a8739867b6148ad49a074eab5dbe0cdbac4cfaed3c0224a40c994659b3a1d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSpatialIndex", [value]))

    @jsii.member(jsii_name="resetCompositeIndex")
    def reset_composite_index(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompositeIndex", []))

    @jsii.member(jsii_name="resetExcludedPath")
    def reset_excluded_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedPath", []))

    @jsii.member(jsii_name="resetIncludedPath")
    def reset_included_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludedPath", []))

    @jsii.member(jsii_name="resetIndexingMode")
    def reset_indexing_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIndexingMode", []))

    @jsii.member(jsii_name="resetSpatialIndex")
    def reset_spatial_index(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpatialIndex", []))

    @builtins.property
    @jsii.member(jsii_name="compositeIndex")
    def composite_index(self) -> CosmosdbSqlContainerIndexingPolicyCompositeIndexList:
        return typing.cast(CosmosdbSqlContainerIndexingPolicyCompositeIndexList, jsii.get(self, "compositeIndex"))

    @builtins.property
    @jsii.member(jsii_name="excludedPath")
    def excluded_path(self) -> CosmosdbSqlContainerIndexingPolicyExcludedPathList:
        return typing.cast(CosmosdbSqlContainerIndexingPolicyExcludedPathList, jsii.get(self, "excludedPath"))

    @builtins.property
    @jsii.member(jsii_name="includedPath")
    def included_path(self) -> CosmosdbSqlContainerIndexingPolicyIncludedPathList:
        return typing.cast(CosmosdbSqlContainerIndexingPolicyIncludedPathList, jsii.get(self, "includedPath"))

    @builtins.property
    @jsii.member(jsii_name="spatialIndex")
    def spatial_index(self) -> "CosmosdbSqlContainerIndexingPolicySpatialIndexList":
        return typing.cast("CosmosdbSqlContainerIndexingPolicySpatialIndexList", jsii.get(self, "spatialIndex"))

    @builtins.property
    @jsii.member(jsii_name="compositeIndexInput")
    def composite_index_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbSqlContainerIndexingPolicyCompositeIndex]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbSqlContainerIndexingPolicyCompositeIndex]]], jsii.get(self, "compositeIndexInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedPathInput")
    def excluded_path_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbSqlContainerIndexingPolicyExcludedPath]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbSqlContainerIndexingPolicyExcludedPath]]], jsii.get(self, "excludedPathInput"))

    @builtins.property
    @jsii.member(jsii_name="includedPathInput")
    def included_path_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbSqlContainerIndexingPolicyIncludedPath]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbSqlContainerIndexingPolicyIncludedPath]]], jsii.get(self, "includedPathInput"))

    @builtins.property
    @jsii.member(jsii_name="indexingModeInput")
    def indexing_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "indexingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="spatialIndexInput")
    def spatial_index_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbSqlContainerIndexingPolicySpatialIndex"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbSqlContainerIndexingPolicySpatialIndex"]]], jsii.get(self, "spatialIndexInput"))

    @builtins.property
    @jsii.member(jsii_name="indexingMode")
    def indexing_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "indexingMode"))

    @indexing_mode.setter
    def indexing_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8d37cdbd497762feb17c33580da4e4e5bca2fbb8b839fa59751b4c1ae0e30e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indexingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CosmosdbSqlContainerIndexingPolicy]:
        return typing.cast(typing.Optional[CosmosdbSqlContainerIndexingPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CosmosdbSqlContainerIndexingPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bd421269aa00a09853dd222dcf038775ad1f43b7aca4be1d1276151b49ef641)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbSqlContainer.CosmosdbSqlContainerIndexingPolicySpatialIndex",
    jsii_struct_bases=[],
    name_mapping={"path": "path"},
)
class CosmosdbSqlContainerIndexingPolicySpatialIndex:
    def __init__(self, *, path: builtins.str) -> None:
        '''
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#path CosmosdbSqlContainer#path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e8f4b592e25af754c823abf1109a228dba402ae8e5b73d60b79247e8a7e712d)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
        }

    @builtins.property
    def path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#path CosmosdbSqlContainer#path}.'''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbSqlContainerIndexingPolicySpatialIndex(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CosmosdbSqlContainerIndexingPolicySpatialIndexList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbSqlContainer.CosmosdbSqlContainerIndexingPolicySpatialIndexList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eeb1b17c208f99e30e6f308090a8092ac19999916ee741b9814e7f7e320eed28)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CosmosdbSqlContainerIndexingPolicySpatialIndexOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76bc3c1f2302a1d90c8d885a1aa7b5ba49e5c8942dcf24ea2113e9fc3ff4ee22)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CosmosdbSqlContainerIndexingPolicySpatialIndexOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__573900b4a10316917c8a1cc5d13a9c59351ccca3257e6d679532da235087ec84)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4f0f6b17b9e7f01980364235d36be824e8ce0ce05b8572118520f27f6a84bf1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b63382ad411d87054f37e1e6bc5258f59bbc75caa332ed1a8e9a8228b6622de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbSqlContainerIndexingPolicySpatialIndex]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbSqlContainerIndexingPolicySpatialIndex]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbSqlContainerIndexingPolicySpatialIndex]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8665304726be19774f62c57ae3a5a0d01de0a9569599848462717b6cd7738f19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CosmosdbSqlContainerIndexingPolicySpatialIndexOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbSqlContainer.CosmosdbSqlContainerIndexingPolicySpatialIndexOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b84742d55e08686f3dcb5633c5aafac394124673361c09615507844c69df081f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="types")
    def types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "types"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43e582a71d25908088540dffd10542db861505feb34b26ae357dcebc041ee867)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbSqlContainerIndexingPolicySpatialIndex]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbSqlContainerIndexingPolicySpatialIndex]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbSqlContainerIndexingPolicySpatialIndex]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80b1c313068c441f5bf9f7cca5e76d84a4c055d9a7814c04c91c3ddcd02bce5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbSqlContainer.CosmosdbSqlContainerTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class CosmosdbSqlContainerTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#create CosmosdbSqlContainer#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#delete CosmosdbSqlContainer#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#read CosmosdbSqlContainer#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#update CosmosdbSqlContainer#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__580c293af6c2d11a301c58423814b60f27ccd4ea410592d848b219fceb17a27f)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#create CosmosdbSqlContainer#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#delete CosmosdbSqlContainer#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#read CosmosdbSqlContainer#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#update CosmosdbSqlContainer#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbSqlContainerTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CosmosdbSqlContainerTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbSqlContainer.CosmosdbSqlContainerTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0374b8ef5a6bede1d5dfd96f86e215aec2e19247d5bb4fe028b1463c609d5ac0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__822c44e3e968e1459e1f06817b52d85923759d6840cb18d54a191a72b2a6a89a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__881dbfdd13767a9deeee846d645e9481cfcb234829a287a9675c1796cf164731)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e1c06e43c191a6184598875e693862ee407a71b5d773d8b77814329b737675c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee1852e21c443d4348b808264d6c7fb0383826f96a7e278b3002196f8a582887)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbSqlContainerTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbSqlContainerTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbSqlContainerTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ef1229204dcbf40f06fe872ae0ec34dfbdeed262ed809e02d3636d046cd329d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbSqlContainer.CosmosdbSqlContainerUniqueKey",
    jsii_struct_bases=[],
    name_mapping={"paths": "paths"},
)
class CosmosdbSqlContainerUniqueKey:
    def __init__(self, *, paths: typing.Sequence[builtins.str]) -> None:
        '''
        :param paths: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#paths CosmosdbSqlContainer#paths}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75d410881730045b380744b0d43cdfed1bda204638bc5ce7107e343dcd3e38d1)
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "paths": paths,
        }

    @builtins.property
    def paths(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_sql_container#paths CosmosdbSqlContainer#paths}.'''
        result = self._values.get("paths")
        assert result is not None, "Required property 'paths' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbSqlContainerUniqueKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CosmosdbSqlContainerUniqueKeyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbSqlContainer.CosmosdbSqlContainerUniqueKeyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d97134e78c9bff283a3fbdfdc7e5e1500404ff9a53412975fc69ae3cfab15150)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CosmosdbSqlContainerUniqueKeyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6da9bc7b7da1b17bbd0b728de962c818a2a37f86ab7880ed21b97c7e6770b87)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CosmosdbSqlContainerUniqueKeyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9d58ff0544095750a32aa261a05b8d1f45c75e466e70f3fd913e8548ba54c8b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__581ab2b84740fef1e34714d4efc1287eb39f66b0213bf4e00a007b7f7fe7a03e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__328fb0c1d09f43b53245bea0ba6c4be383f16b3aefa5aafd5bf9651b641c6764)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbSqlContainerUniqueKey]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbSqlContainerUniqueKey]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbSqlContainerUniqueKey]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd7cc3b56e245688402e11ae8e3a5a9e4bdcf1d1c25fdfb2a17ce1db75ae17bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CosmosdbSqlContainerUniqueKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbSqlContainer.CosmosdbSqlContainerUniqueKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb1420d47dddb4d1439e1f5268aeae7ce8b1907550e95868207d48b2e22fc397)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="pathsInput")
    def paths_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "pathsInput"))

    @builtins.property
    @jsii.member(jsii_name="paths")
    def paths(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "paths"))

    @paths.setter
    def paths(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fabbbe00dd5237a57bc7f82b12bceabaca8c479cc18c253802ee0c7b20ff8e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "paths", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbSqlContainerUniqueKey]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbSqlContainerUniqueKey]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbSqlContainerUniqueKey]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__375ba0275e7a8fb0a0ce94eee745bddea73b0e01c6cf72541fb89ca454592169)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CosmosdbSqlContainer",
    "CosmosdbSqlContainerAutoscaleSettings",
    "CosmosdbSqlContainerAutoscaleSettingsOutputReference",
    "CosmosdbSqlContainerConfig",
    "CosmosdbSqlContainerConflictResolutionPolicy",
    "CosmosdbSqlContainerConflictResolutionPolicyOutputReference",
    "CosmosdbSqlContainerIndexingPolicy",
    "CosmosdbSqlContainerIndexingPolicyCompositeIndex",
    "CosmosdbSqlContainerIndexingPolicyCompositeIndexIndex",
    "CosmosdbSqlContainerIndexingPolicyCompositeIndexIndexList",
    "CosmosdbSqlContainerIndexingPolicyCompositeIndexIndexOutputReference",
    "CosmosdbSqlContainerIndexingPolicyCompositeIndexList",
    "CosmosdbSqlContainerIndexingPolicyCompositeIndexOutputReference",
    "CosmosdbSqlContainerIndexingPolicyExcludedPath",
    "CosmosdbSqlContainerIndexingPolicyExcludedPathList",
    "CosmosdbSqlContainerIndexingPolicyExcludedPathOutputReference",
    "CosmosdbSqlContainerIndexingPolicyIncludedPath",
    "CosmosdbSqlContainerIndexingPolicyIncludedPathList",
    "CosmosdbSqlContainerIndexingPolicyIncludedPathOutputReference",
    "CosmosdbSqlContainerIndexingPolicyOutputReference",
    "CosmosdbSqlContainerIndexingPolicySpatialIndex",
    "CosmosdbSqlContainerIndexingPolicySpatialIndexList",
    "CosmosdbSqlContainerIndexingPolicySpatialIndexOutputReference",
    "CosmosdbSqlContainerTimeouts",
    "CosmosdbSqlContainerTimeoutsOutputReference",
    "CosmosdbSqlContainerUniqueKey",
    "CosmosdbSqlContainerUniqueKeyList",
    "CosmosdbSqlContainerUniqueKeyOutputReference",
]

publication.publish()

def _typecheckingstub__1691175d9fcd6444a4a57af57c106b2060e117b60a7a1655c8091f666361ce97(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    account_name: builtins.str,
    database_name: builtins.str,
    name: builtins.str,
    partition_key_paths: typing.Sequence[builtins.str],
    resource_group_name: builtins.str,
    analytical_storage_ttl: typing.Optional[jsii.Number] = None,
    autoscale_settings: typing.Optional[typing.Union[CosmosdbSqlContainerAutoscaleSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    conflict_resolution_policy: typing.Optional[typing.Union[CosmosdbSqlContainerConflictResolutionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    default_ttl: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    indexing_policy: typing.Optional[typing.Union[CosmosdbSqlContainerIndexingPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    partition_key_kind: typing.Optional[builtins.str] = None,
    partition_key_version: typing.Optional[jsii.Number] = None,
    throughput: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[CosmosdbSqlContainerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    unique_key: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbSqlContainerUniqueKey, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__b68cabe42ccec21112609347115d4bde59410546b08b47b5856f2f610eb7b3b6(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3f6a87ff4f959b63dcd5b06004f8978acda405c798e502532debb8494745e2a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbSqlContainerUniqueKey, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c46e26fe6f30291d853218242bc8054d551d3ed476c6028011c37e63f8ed346c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a169dcb767ba5a07c21a19eb62551df68d82012f10e834d210c5385f4d9c30de(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8369e6c29838d61c72a4b18459e73f11d64190910299ff0cc3f1bde2b885ec98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d98250c76db8ba7723d1da91edfc78469b683b6e8d09abff6fccd8578a32df6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e5f1255dd9ba8c42d84358b6069ce92279c0c3d852f9f2c50a5b8cf96707d21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__591778811afa82d42f7b5da39c9b96df47b12c0d4bf922d1e96896127f0b5e02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5661973cddbf8cee1c991ee156fc51222fcd8e7cab4c4b0251217d5ac6a34151(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a207f3c84492a96cba7bf52c1d5a8a6ce64a95120a3622709275573e5608c19(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d91c53d13fed196a585b75cd078a7094657f4b938fa25a614ac0a79064ba4b6e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fc56e44f61315f9af2927d136caa8e511c87d4bdae283b48dc9a30979315324(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63cd43e9713ff1c8c91638f866c5c2816413fe9e78992628690601f8b90120d9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bee75d56aa51ee460c2a7e690e9bfa3273f16c339b03af7cc1f1c4726999630(
    *,
    max_throughput: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c701f39df6bfe17bf2bb3713d55e31305427d0ac632030c84a6c198537d4979(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__844eecfe91c74f36fd32b2cf03e3ba57e2c71aaa1cbfe27aef4301550adbf0b2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b784386436ddae1a8b899378555125ffa84b1c3e3073d89b5fdab350002626e(
    value: typing.Optional[CosmosdbSqlContainerAutoscaleSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c50580e4f0fcc4711e98010e7212aa4e423970a36dfc78f03d029d353091e452(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    account_name: builtins.str,
    database_name: builtins.str,
    name: builtins.str,
    partition_key_paths: typing.Sequence[builtins.str],
    resource_group_name: builtins.str,
    analytical_storage_ttl: typing.Optional[jsii.Number] = None,
    autoscale_settings: typing.Optional[typing.Union[CosmosdbSqlContainerAutoscaleSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    conflict_resolution_policy: typing.Optional[typing.Union[CosmosdbSqlContainerConflictResolutionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    default_ttl: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    indexing_policy: typing.Optional[typing.Union[CosmosdbSqlContainerIndexingPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    partition_key_kind: typing.Optional[builtins.str] = None,
    partition_key_version: typing.Optional[jsii.Number] = None,
    throughput: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[CosmosdbSqlContainerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    unique_key: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbSqlContainerUniqueKey, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e38501b4e73d56c5a7081e91269068a3e8a67f1de74faf33dd9880a32d4ca3d6(
    *,
    mode: builtins.str,
    conflict_resolution_path: typing.Optional[builtins.str] = None,
    conflict_resolution_procedure: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ebf018f3dd4240f2fb0bbc66b97d653210138a45be9ebe2c3632f2365bd3626(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d281b96b2a97cc0c8ccff26dbcfb9a5c963615a6dffa05afd46585667e6c5ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f903d82c96257c6eef2513d665ca3ff028396897b007be2f694b0a00f1ac9c7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__234c2cb7140206d1e860e32e3abe5eba98f145ad819e5cf45e2fb00812b59e71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c1ff42a92ac609afa7de098a3f3bb3d1305159b000e4baa6e5e05c8fd1089db(
    value: typing.Optional[CosmosdbSqlContainerConflictResolutionPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a8187b691f4e3654041b4fd239de88c7a1ca4dce0388aeb5aaf27cd973d679a(
    *,
    composite_index: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbSqlContainerIndexingPolicyCompositeIndex, typing.Dict[builtins.str, typing.Any]]]]] = None,
    excluded_path: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbSqlContainerIndexingPolicyExcludedPath, typing.Dict[builtins.str, typing.Any]]]]] = None,
    included_path: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbSqlContainerIndexingPolicyIncludedPath, typing.Dict[builtins.str, typing.Any]]]]] = None,
    indexing_mode: typing.Optional[builtins.str] = None,
    spatial_index: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbSqlContainerIndexingPolicySpatialIndex, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__387be593a2c88da8e3518c52c7a9231c75ee0ff65d296d27394f342768895851(
    *,
    index: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbSqlContainerIndexingPolicyCompositeIndexIndex, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e3574ce32168bbbab5c5f0883e328d37bc2c40eca17d406019e4d42a7aa1cac(
    *,
    order: builtins.str,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29395d6763f5ae615c784858c8210fb8f3f11c6bace64cb86a8d249973f41329(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdbcdebdae19e01df1acbd0dbd59cff0a4f685087ea67daa85a387013fb274e4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c656e7177bedb84a0ee1a981a97cfd96f0dc843d2804beea634ee5ccd79a5dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adb49d459146d9678993f64880d6dd3d7171b166e828970d77f8fc85311514a2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1030d4b0cbb4271568fc2eda0f07a556b2e1bdeb93aff63611a2f8a2ad32d73d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76a1953a39adcafb9e4b2951bb68eac2df60c85cc0f9257ed0b2645a8abfba18(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbSqlContainerIndexingPolicyCompositeIndexIndex]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e31f95455d810c169bf73a285392f65e8f8a5785dc1a8be85a8829c70cee397(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c2a40e77a65788ecbef7ab69cf34dc1e6028cf105d204b4ff87fd0d3a935b43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54ef96628a003f3770693be58cf93235d043b80180ebdf5da245b0e1f11be008(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4c1f49fb7e14c4ee5c901991015668423b4b0a2e9a3d1f65ba643f117332d18(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbSqlContainerIndexingPolicyCompositeIndexIndex]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__947e41f37f3ba1cbb027a7320c46ba6d03a876b8d0bd44493664aee439ebc793(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9998414ff611278c3f8683c57ea0d8496d02afb65c34329dfb0673227a79c53c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__220c287f567b130562a9d9b072efff76e1ce15af425544dc634a3f4d6686fccf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22594fc0bf365e080da724c3652c5dcb29fd61b599e653c4b461a01b310a5c6f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__257bb2a1251701af872c06a0deeae74d9e6ff3f0ba87acad4a18dfb8e297e90f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5db702ef1955ca67df7b2a87f1d5bf384f410fb0b9d139a188e58aa0b9fce6af(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbSqlContainerIndexingPolicyCompositeIndex]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c97b84f2d4f864c9bdbe5bb29c93fba412cd677769c1003e73be99ccbc9ef66f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0827ba14329c0fa31107da981ae0dfb4fd9acd2ed5c226142804b9a177e52392(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbSqlContainerIndexingPolicyCompositeIndexIndex, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__750450d6511aa78b249b6ea8d7bd8f09aa9851d7456ab735d8af9464f4de1129(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbSqlContainerIndexingPolicyCompositeIndex]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b706a1babf899e5d022e18fd8c0083455123af373201efd610ca0c47cae33a9a(
    *,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31c927ba725391bd49aa6e49aa8ae92a4551d3faa9133b0c274806031aebd2a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f7467cc35bb607596dbfd2c621a77ca539d5f31c9fc1ccd4f11bdf06709d7bd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__236b0b3d6eacd1e768281e13f797e5b43a7a3a300fafff330b7aa30fb901f7f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa414c18db063d29b69a03cee15ca6b598dda9860f5666797af0b58302ae0a05(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f38ab7782771f3d2953a37973fd036a287adbf3db757e847977671347d892cf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7a9be46fd2bae79ad69932758401d84fcd67e570b63b32aebb1bf27a4ea66b7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbSqlContainerIndexingPolicyExcludedPath]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9af0d649cea33b2d3af1e8881a9cb555dd0217738caa73b529e2d048bde496c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__549e4342ebefd48f08723c7784f12d412f008f2f020bc6dd21cb4e94d39ca55f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0694bd34c2bc465a352db9a10cf21a7bd7333f3df3bb5a2d9df994adf528a9ff(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbSqlContainerIndexingPolicyExcludedPath]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe1cb58441b468cfd6eb4a3a1092cd2c77ad8add51555d674e23843a4a6930dd(
    *,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b15c3011257360679ca8bf8de56670cb22e3a150132341e7b9cefeda6f979606(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69f251a571e2312fc614f056eda9e547c6d0d6455f3ed6b376bd6a4dcbc561f6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4d86e44c8ea9be7285973e656421671abc1d7b355ab3d10ef23ba46bd24af46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79afb4639e0dfba5b73a75b16bc55a22ec96107a646cd4d872d82a5c0cc2006c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8f508e0ad3a925fa32dcca1e09074e9d3bbb99d8f8ce06797748909949370b1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32ba727199ddeae8ee0d5d3f2c0e69527ed997397be1f4c18d8cce4b76e19522(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbSqlContainerIndexingPolicyIncludedPath]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7000f5a7989b921b477b8328d3cef356985c1f683b9762f3a39e2fadc5d69ede(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0333018750a7f68292b5fafd88033753abc27a5882a81f4aacfc38eacad1afc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b571fd487f86e74a13ad135ab8ffd6d79c795c2373eb2d2a50d9cba96f5392a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbSqlContainerIndexingPolicyIncludedPath]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b6669dd5ba54a5adc775c1d7f0bbe120a6ec08ba5b93126df051503af672b36(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df3a607f17573953b5ed5866f30e01a03e6307faeaa13dac0ad816e3d26b4b43(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbSqlContainerIndexingPolicyCompositeIndex, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5465878d83fee2913170a4d332ebfae16a073ce3b7e46bfe8afd31d5fac4099(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbSqlContainerIndexingPolicyExcludedPath, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b12e16f0bb78fed6b94dd19c8285aa45a018ba4b5d3cd5bd1979d4d7c67a12d3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbSqlContainerIndexingPolicyIncludedPath, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92a8739867b6148ad49a074eab5dbe0cdbac4cfaed3c0224a40c994659b3a1d8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbSqlContainerIndexingPolicySpatialIndex, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8d37cdbd497762feb17c33580da4e4e5bca2fbb8b839fa59751b4c1ae0e30e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bd421269aa00a09853dd222dcf038775ad1f43b7aca4be1d1276151b49ef641(
    value: typing.Optional[CosmosdbSqlContainerIndexingPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e8f4b592e25af754c823abf1109a228dba402ae8e5b73d60b79247e8a7e712d(
    *,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeb1b17c208f99e30e6f308090a8092ac19999916ee741b9814e7f7e320eed28(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76bc3c1f2302a1d90c8d885a1aa7b5ba49e5c8942dcf24ea2113e9fc3ff4ee22(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__573900b4a10316917c8a1cc5d13a9c59351ccca3257e6d679532da235087ec84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4f0f6b17b9e7f01980364235d36be824e8ce0ce05b8572118520f27f6a84bf1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b63382ad411d87054f37e1e6bc5258f59bbc75caa332ed1a8e9a8228b6622de(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8665304726be19774f62c57ae3a5a0d01de0a9569599848462717b6cd7738f19(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbSqlContainerIndexingPolicySpatialIndex]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b84742d55e08686f3dcb5633c5aafac394124673361c09615507844c69df081f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43e582a71d25908088540dffd10542db861505feb34b26ae357dcebc041ee867(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80b1c313068c441f5bf9f7cca5e76d84a4c055d9a7814c04c91c3ddcd02bce5a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbSqlContainerIndexingPolicySpatialIndex]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__580c293af6c2d11a301c58423814b60f27ccd4ea410592d848b219fceb17a27f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0374b8ef5a6bede1d5dfd96f86e215aec2e19247d5bb4fe028b1463c609d5ac0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__822c44e3e968e1459e1f06817b52d85923759d6840cb18d54a191a72b2a6a89a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__881dbfdd13767a9deeee846d645e9481cfcb234829a287a9675c1796cf164731(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e1c06e43c191a6184598875e693862ee407a71b5d773d8b77814329b737675c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee1852e21c443d4348b808264d6c7fb0383826f96a7e278b3002196f8a582887(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ef1229204dcbf40f06fe872ae0ec34dfbdeed262ed809e02d3636d046cd329d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbSqlContainerTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75d410881730045b380744b0d43cdfed1bda204638bc5ce7107e343dcd3e38d1(
    *,
    paths: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d97134e78c9bff283a3fbdfdc7e5e1500404ff9a53412975fc69ae3cfab15150(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6da9bc7b7da1b17bbd0b728de962c818a2a37f86ab7880ed21b97c7e6770b87(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9d58ff0544095750a32aa261a05b8d1f45c75e466e70f3fd913e8548ba54c8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__581ab2b84740fef1e34714d4efc1287eb39f66b0213bf4e00a007b7f7fe7a03e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__328fb0c1d09f43b53245bea0ba6c4be383f16b3aefa5aafd5bf9651b641c6764(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd7cc3b56e245688402e11ae8e3a5a9e4bdcf1d1c25fdfb2a17ce1db75ae17bc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbSqlContainerUniqueKey]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb1420d47dddb4d1439e1f5268aeae7ce8b1907550e95868207d48b2e22fc397(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fabbbe00dd5237a57bc7f82b12bceabaca8c479cc18c253802ee0c7b20ff8e3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__375ba0275e7a8fb0a0ce94eee745bddea73b0e01c6cf72541fb89ca454592169(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbSqlContainerUniqueKey]],
) -> None:
    """Type checking stubs"""
    pass
