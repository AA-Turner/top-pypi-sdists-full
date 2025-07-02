r'''
# `azurerm_cosmosdb_gremlin_graph`

Refer to the Terraform Registry for docs: [`azurerm_cosmosdb_gremlin_graph`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph).
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


class CosmosdbGremlinGraph(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbGremlinGraph.CosmosdbGremlinGraph",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph azurerm_cosmosdb_gremlin_graph}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        account_name: builtins.str,
        database_name: builtins.str,
        name: builtins.str,
        partition_key_path: builtins.str,
        resource_group_name: builtins.str,
        analytical_storage_ttl: typing.Optional[jsii.Number] = None,
        autoscale_settings: typing.Optional[typing.Union["CosmosdbGremlinGraphAutoscaleSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        conflict_resolution_policy: typing.Optional[typing.Union["CosmosdbGremlinGraphConflictResolutionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        default_ttl: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        index_policy: typing.Optional[typing.Union["CosmosdbGremlinGraphIndexPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        partition_key_version: typing.Optional[jsii.Number] = None,
        throughput: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["CosmosdbGremlinGraphTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        unique_key: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CosmosdbGremlinGraphUniqueKey", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph azurerm_cosmosdb_gremlin_graph} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#account_name CosmosdbGremlinGraph#account_name}.
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#database_name CosmosdbGremlinGraph#database_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#name CosmosdbGremlinGraph#name}.
        :param partition_key_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#partition_key_path CosmosdbGremlinGraph#partition_key_path}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#resource_group_name CosmosdbGremlinGraph#resource_group_name}.
        :param analytical_storage_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#analytical_storage_ttl CosmosdbGremlinGraph#analytical_storage_ttl}.
        :param autoscale_settings: autoscale_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#autoscale_settings CosmosdbGremlinGraph#autoscale_settings}
        :param conflict_resolution_policy: conflict_resolution_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#conflict_resolution_policy CosmosdbGremlinGraph#conflict_resolution_policy}
        :param default_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#default_ttl CosmosdbGremlinGraph#default_ttl}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#id CosmosdbGremlinGraph#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param index_policy: index_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#index_policy CosmosdbGremlinGraph#index_policy}
        :param partition_key_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#partition_key_version CosmosdbGremlinGraph#partition_key_version}.
        :param throughput: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#throughput CosmosdbGremlinGraph#throughput}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#timeouts CosmosdbGremlinGraph#timeouts}
        :param unique_key: unique_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#unique_key CosmosdbGremlinGraph#unique_key}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa8df528db5a92495231e27e05430d15be1440b51c76d79041a6439eff382bce)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CosmosdbGremlinGraphConfig(
            account_name=account_name,
            database_name=database_name,
            name=name,
            partition_key_path=partition_key_path,
            resource_group_name=resource_group_name,
            analytical_storage_ttl=analytical_storage_ttl,
            autoscale_settings=autoscale_settings,
            conflict_resolution_policy=conflict_resolution_policy,
            default_ttl=default_ttl,
            id=id,
            index_policy=index_policy,
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
        '''Generates CDKTF code for importing a CosmosdbGremlinGraph resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CosmosdbGremlinGraph to import.
        :param import_from_id: The id of the existing CosmosdbGremlinGraph that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CosmosdbGremlinGraph to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__530621025cf5da2138c68af9eb8e615e5f463236a6773848f0dc1072a7236e40)
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
        :param max_throughput: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#max_throughput CosmosdbGremlinGraph#max_throughput}.
        '''
        value = CosmosdbGremlinGraphAutoscaleSettings(max_throughput=max_throughput)

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
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#mode CosmosdbGremlinGraph#mode}.
        :param conflict_resolution_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#conflict_resolution_path CosmosdbGremlinGraph#conflict_resolution_path}.
        :param conflict_resolution_procedure: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#conflict_resolution_procedure CosmosdbGremlinGraph#conflict_resolution_procedure}.
        '''
        value = CosmosdbGremlinGraphConflictResolutionPolicy(
            mode=mode,
            conflict_resolution_path=conflict_resolution_path,
            conflict_resolution_procedure=conflict_resolution_procedure,
        )

        return typing.cast(None, jsii.invoke(self, "putConflictResolutionPolicy", [value]))

    @jsii.member(jsii_name="putIndexPolicy")
    def put_index_policy(
        self,
        *,
        indexing_mode: builtins.str,
        automatic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        composite_index: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CosmosdbGremlinGraphIndexPolicyCompositeIndex", typing.Dict[builtins.str, typing.Any]]]]] = None,
        excluded_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        spatial_index: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CosmosdbGremlinGraphIndexPolicySpatialIndex", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param indexing_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#indexing_mode CosmosdbGremlinGraph#indexing_mode}.
        :param automatic: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#automatic CosmosdbGremlinGraph#automatic}.
        :param composite_index: composite_index block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#composite_index CosmosdbGremlinGraph#composite_index}
        :param excluded_paths: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#excluded_paths CosmosdbGremlinGraph#excluded_paths}.
        :param included_paths: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#included_paths CosmosdbGremlinGraph#included_paths}.
        :param spatial_index: spatial_index block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#spatial_index CosmosdbGremlinGraph#spatial_index}
        '''
        value = CosmosdbGremlinGraphIndexPolicy(
            indexing_mode=indexing_mode,
            automatic=automatic,
            composite_index=composite_index,
            excluded_paths=excluded_paths,
            included_paths=included_paths,
            spatial_index=spatial_index,
        )

        return typing.cast(None, jsii.invoke(self, "putIndexPolicy", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#create CosmosdbGremlinGraph#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#delete CosmosdbGremlinGraph#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#read CosmosdbGremlinGraph#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#update CosmosdbGremlinGraph#update}.
        '''
        value = CosmosdbGremlinGraphTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putUniqueKey")
    def put_unique_key(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CosmosdbGremlinGraphUniqueKey", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc175b3a8f18c49a1d21538ddbf7812e2c3a35ae1f43e408eabeb75e776ba9b9)
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

    @jsii.member(jsii_name="resetIndexPolicy")
    def reset_index_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIndexPolicy", []))

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
    ) -> "CosmosdbGremlinGraphAutoscaleSettingsOutputReference":
        return typing.cast("CosmosdbGremlinGraphAutoscaleSettingsOutputReference", jsii.get(self, "autoscaleSettings"))

    @builtins.property
    @jsii.member(jsii_name="conflictResolutionPolicy")
    def conflict_resolution_policy(
        self,
    ) -> "CosmosdbGremlinGraphConflictResolutionPolicyOutputReference":
        return typing.cast("CosmosdbGremlinGraphConflictResolutionPolicyOutputReference", jsii.get(self, "conflictResolutionPolicy"))

    @builtins.property
    @jsii.member(jsii_name="indexPolicy")
    def index_policy(self) -> "CosmosdbGremlinGraphIndexPolicyOutputReference":
        return typing.cast("CosmosdbGremlinGraphIndexPolicyOutputReference", jsii.get(self, "indexPolicy"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CosmosdbGremlinGraphTimeoutsOutputReference":
        return typing.cast("CosmosdbGremlinGraphTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uniqueKey")
    def unique_key(self) -> "CosmosdbGremlinGraphUniqueKeyList":
        return typing.cast("CosmosdbGremlinGraphUniqueKeyList", jsii.get(self, "uniqueKey"))

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
    ) -> typing.Optional["CosmosdbGremlinGraphAutoscaleSettings"]:
        return typing.cast(typing.Optional["CosmosdbGremlinGraphAutoscaleSettings"], jsii.get(self, "autoscaleSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="conflictResolutionPolicyInput")
    def conflict_resolution_policy_input(
        self,
    ) -> typing.Optional["CosmosdbGremlinGraphConflictResolutionPolicy"]:
        return typing.cast(typing.Optional["CosmosdbGremlinGraphConflictResolutionPolicy"], jsii.get(self, "conflictResolutionPolicyInput"))

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
    @jsii.member(jsii_name="indexPolicyInput")
    def index_policy_input(self) -> typing.Optional["CosmosdbGremlinGraphIndexPolicy"]:
        return typing.cast(typing.Optional["CosmosdbGremlinGraphIndexPolicy"], jsii.get(self, "indexPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="partitionKeyPathInput")
    def partition_key_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "partitionKeyPathInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CosmosdbGremlinGraphTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CosmosdbGremlinGraphTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="uniqueKeyInput")
    def unique_key_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbGremlinGraphUniqueKey"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbGremlinGraphUniqueKey"]]], jsii.get(self, "uniqueKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="accountName")
    def account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountName"))

    @account_name.setter
    def account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f4527ec5ae39df17385c5940eed8232a4950d223a5a934fb1eb0fd2435a1806)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="analyticalStorageTtl")
    def analytical_storage_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "analyticalStorageTtl"))

    @analytical_storage_ttl.setter
    def analytical_storage_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d49576cf2e7ea685b8e3ca55b26b50528d66fc84cf75b2f996c727fc25fdbe50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "analyticalStorageTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @database_name.setter
    def database_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e13680cb8d8e7a25929ce1b00a8951270e968212ecb42d51745f160822e44ae4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultTtl")
    def default_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultTtl"))

    @default_ttl.setter
    def default_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3603de9891566be9777cce580f1085b023f188fb7e3b7c3ac2e0fec7115bb7ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69d65542b503c26d005febb777440e585184e77eda3183d8e60fe8f3773f4a05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d02995186389d3211b2696432d7e82dcd57b8025f9ddc0ba3d21161ba8067f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partitionKeyPath")
    def partition_key_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "partitionKeyPath"))

    @partition_key_path.setter
    def partition_key_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0af7d73eca5d69ede92f87b4c7b41cc13b67ee74efc3e4acb9d0fb1c06e535a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partitionKeyPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partitionKeyVersion")
    def partition_key_version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "partitionKeyVersion"))

    @partition_key_version.setter
    def partition_key_version(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ccff9a5f98ea20fee8bd6e47bf5c80c9066b3cbe2a9cd1edb24c12f630255d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partitionKeyVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c15a39f6ff81205e6275ca8f3e90fa069f963b4504e703d1991ae477cdc2490)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="throughput")
    def throughput(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "throughput"))

    @throughput.setter
    def throughput(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7dd3dbb8ee5d9e6bd24bf618fb4b5d091e3b6b324ebda3cd00b00b90c84d29a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throughput", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbGremlinGraph.CosmosdbGremlinGraphAutoscaleSettings",
    jsii_struct_bases=[],
    name_mapping={"max_throughput": "maxThroughput"},
)
class CosmosdbGremlinGraphAutoscaleSettings:
    def __init__(self, *, max_throughput: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param max_throughput: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#max_throughput CosmosdbGremlinGraph#max_throughput}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e249108c67b8a5767dd17395bc6d13168a951c63e126a30d3e1db4d700e9332)
            check_type(argname="argument max_throughput", value=max_throughput, expected_type=type_hints["max_throughput"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_throughput is not None:
            self._values["max_throughput"] = max_throughput

    @builtins.property
    def max_throughput(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#max_throughput CosmosdbGremlinGraph#max_throughput}.'''
        result = self._values.get("max_throughput")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbGremlinGraphAutoscaleSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CosmosdbGremlinGraphAutoscaleSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbGremlinGraph.CosmosdbGremlinGraphAutoscaleSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8ee708e5e861bc663a638ec73b57a033349fe6ce321c6c25fb3974c09fd2eee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ab99c4d01d546b441208bc35dcd53f28b372517bd5db70db2dcf7cc486b94c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxThroughput", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CosmosdbGremlinGraphAutoscaleSettings]:
        return typing.cast(typing.Optional[CosmosdbGremlinGraphAutoscaleSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CosmosdbGremlinGraphAutoscaleSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c93c45e9eb0a11415c172f43672ebca957e9aaac2f0815be691e4a13818cc46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbGremlinGraph.CosmosdbGremlinGraphConfig",
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
        "partition_key_path": "partitionKeyPath",
        "resource_group_name": "resourceGroupName",
        "analytical_storage_ttl": "analyticalStorageTtl",
        "autoscale_settings": "autoscaleSettings",
        "conflict_resolution_policy": "conflictResolutionPolicy",
        "default_ttl": "defaultTtl",
        "id": "id",
        "index_policy": "indexPolicy",
        "partition_key_version": "partitionKeyVersion",
        "throughput": "throughput",
        "timeouts": "timeouts",
        "unique_key": "uniqueKey",
    },
)
class CosmosdbGremlinGraphConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        partition_key_path: builtins.str,
        resource_group_name: builtins.str,
        analytical_storage_ttl: typing.Optional[jsii.Number] = None,
        autoscale_settings: typing.Optional[typing.Union[CosmosdbGremlinGraphAutoscaleSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        conflict_resolution_policy: typing.Optional[typing.Union["CosmosdbGremlinGraphConflictResolutionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        default_ttl: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        index_policy: typing.Optional[typing.Union["CosmosdbGremlinGraphIndexPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        partition_key_version: typing.Optional[jsii.Number] = None,
        throughput: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["CosmosdbGremlinGraphTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        unique_key: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CosmosdbGremlinGraphUniqueKey", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#account_name CosmosdbGremlinGraph#account_name}.
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#database_name CosmosdbGremlinGraph#database_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#name CosmosdbGremlinGraph#name}.
        :param partition_key_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#partition_key_path CosmosdbGremlinGraph#partition_key_path}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#resource_group_name CosmosdbGremlinGraph#resource_group_name}.
        :param analytical_storage_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#analytical_storage_ttl CosmosdbGremlinGraph#analytical_storage_ttl}.
        :param autoscale_settings: autoscale_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#autoscale_settings CosmosdbGremlinGraph#autoscale_settings}
        :param conflict_resolution_policy: conflict_resolution_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#conflict_resolution_policy CosmosdbGremlinGraph#conflict_resolution_policy}
        :param default_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#default_ttl CosmosdbGremlinGraph#default_ttl}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#id CosmosdbGremlinGraph#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param index_policy: index_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#index_policy CosmosdbGremlinGraph#index_policy}
        :param partition_key_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#partition_key_version CosmosdbGremlinGraph#partition_key_version}.
        :param throughput: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#throughput CosmosdbGremlinGraph#throughput}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#timeouts CosmosdbGremlinGraph#timeouts}
        :param unique_key: unique_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#unique_key CosmosdbGremlinGraph#unique_key}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(autoscale_settings, dict):
            autoscale_settings = CosmosdbGremlinGraphAutoscaleSettings(**autoscale_settings)
        if isinstance(conflict_resolution_policy, dict):
            conflict_resolution_policy = CosmosdbGremlinGraphConflictResolutionPolicy(**conflict_resolution_policy)
        if isinstance(index_policy, dict):
            index_policy = CosmosdbGremlinGraphIndexPolicy(**index_policy)
        if isinstance(timeouts, dict):
            timeouts = CosmosdbGremlinGraphTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0a443e7e7fb8e321936f079a44cd50a0af028bd528e3bc64f584943032c5686)
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
            check_type(argname="argument partition_key_path", value=partition_key_path, expected_type=type_hints["partition_key_path"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument analytical_storage_ttl", value=analytical_storage_ttl, expected_type=type_hints["analytical_storage_ttl"])
            check_type(argname="argument autoscale_settings", value=autoscale_settings, expected_type=type_hints["autoscale_settings"])
            check_type(argname="argument conflict_resolution_policy", value=conflict_resolution_policy, expected_type=type_hints["conflict_resolution_policy"])
            check_type(argname="argument default_ttl", value=default_ttl, expected_type=type_hints["default_ttl"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument index_policy", value=index_policy, expected_type=type_hints["index_policy"])
            check_type(argname="argument partition_key_version", value=partition_key_version, expected_type=type_hints["partition_key_version"])
            check_type(argname="argument throughput", value=throughput, expected_type=type_hints["throughput"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument unique_key", value=unique_key, expected_type=type_hints["unique_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_name": account_name,
            "database_name": database_name,
            "name": name,
            "partition_key_path": partition_key_path,
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
        if index_policy is not None:
            self._values["index_policy"] = index_policy
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#account_name CosmosdbGremlinGraph#account_name}.'''
        result = self._values.get("account_name")
        assert result is not None, "Required property 'account_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def database_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#database_name CosmosdbGremlinGraph#database_name}.'''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#name CosmosdbGremlinGraph#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def partition_key_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#partition_key_path CosmosdbGremlinGraph#partition_key_path}.'''
        result = self._values.get("partition_key_path")
        assert result is not None, "Required property 'partition_key_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#resource_group_name CosmosdbGremlinGraph#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def analytical_storage_ttl(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#analytical_storage_ttl CosmosdbGremlinGraph#analytical_storage_ttl}.'''
        result = self._values.get("analytical_storage_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def autoscale_settings(
        self,
    ) -> typing.Optional[CosmosdbGremlinGraphAutoscaleSettings]:
        '''autoscale_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#autoscale_settings CosmosdbGremlinGraph#autoscale_settings}
        '''
        result = self._values.get("autoscale_settings")
        return typing.cast(typing.Optional[CosmosdbGremlinGraphAutoscaleSettings], result)

    @builtins.property
    def conflict_resolution_policy(
        self,
    ) -> typing.Optional["CosmosdbGremlinGraphConflictResolutionPolicy"]:
        '''conflict_resolution_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#conflict_resolution_policy CosmosdbGremlinGraph#conflict_resolution_policy}
        '''
        result = self._values.get("conflict_resolution_policy")
        return typing.cast(typing.Optional["CosmosdbGremlinGraphConflictResolutionPolicy"], result)

    @builtins.property
    def default_ttl(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#default_ttl CosmosdbGremlinGraph#default_ttl}.'''
        result = self._values.get("default_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#id CosmosdbGremlinGraph#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def index_policy(self) -> typing.Optional["CosmosdbGremlinGraphIndexPolicy"]:
        '''index_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#index_policy CosmosdbGremlinGraph#index_policy}
        '''
        result = self._values.get("index_policy")
        return typing.cast(typing.Optional["CosmosdbGremlinGraphIndexPolicy"], result)

    @builtins.property
    def partition_key_version(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#partition_key_version CosmosdbGremlinGraph#partition_key_version}.'''
        result = self._values.get("partition_key_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def throughput(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#throughput CosmosdbGremlinGraph#throughput}.'''
        result = self._values.get("throughput")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CosmosdbGremlinGraphTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#timeouts CosmosdbGremlinGraph#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CosmosdbGremlinGraphTimeouts"], result)

    @builtins.property
    def unique_key(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbGremlinGraphUniqueKey"]]]:
        '''unique_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#unique_key CosmosdbGremlinGraph#unique_key}
        '''
        result = self._values.get("unique_key")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbGremlinGraphUniqueKey"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbGremlinGraphConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbGremlinGraph.CosmosdbGremlinGraphConflictResolutionPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "mode": "mode",
        "conflict_resolution_path": "conflictResolutionPath",
        "conflict_resolution_procedure": "conflictResolutionProcedure",
    },
)
class CosmosdbGremlinGraphConflictResolutionPolicy:
    def __init__(
        self,
        *,
        mode: builtins.str,
        conflict_resolution_path: typing.Optional[builtins.str] = None,
        conflict_resolution_procedure: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#mode CosmosdbGremlinGraph#mode}.
        :param conflict_resolution_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#conflict_resolution_path CosmosdbGremlinGraph#conflict_resolution_path}.
        :param conflict_resolution_procedure: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#conflict_resolution_procedure CosmosdbGremlinGraph#conflict_resolution_procedure}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__507f7bd2a7316c811ece87ce17b3c60be9c75616295a8e36d4aa5947a903d2ff)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#mode CosmosdbGremlinGraph#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def conflict_resolution_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#conflict_resolution_path CosmosdbGremlinGraph#conflict_resolution_path}.'''
        result = self._values.get("conflict_resolution_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def conflict_resolution_procedure(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#conflict_resolution_procedure CosmosdbGremlinGraph#conflict_resolution_procedure}.'''
        result = self._values.get("conflict_resolution_procedure")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbGremlinGraphConflictResolutionPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CosmosdbGremlinGraphConflictResolutionPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbGremlinGraph.CosmosdbGremlinGraphConflictResolutionPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2efa00d8553c027c6004ce91fe602b2432711f8f21d598ad234701197362dfbc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__59ab6de226a19a858e99936adfdb006771632d8c792211592d891e5c13e304a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "conflictResolutionPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="conflictResolutionProcedure")
    def conflict_resolution_procedure(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "conflictResolutionProcedure"))

    @conflict_resolution_procedure.setter
    def conflict_resolution_procedure(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad4492e123c64e479f2ae8239543a4e2684672cf833d0790e2ba594e8a645d21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "conflictResolutionProcedure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8c5d878ba44db345463c966263cb9b97a7930e4de2798eedd8c49c420ae3fd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CosmosdbGremlinGraphConflictResolutionPolicy]:
        return typing.cast(typing.Optional[CosmosdbGremlinGraphConflictResolutionPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CosmosdbGremlinGraphConflictResolutionPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4547a2848349a03cba200da17bb49a8bc29f2c6ac13774377c99b8bb0e49a108)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbGremlinGraph.CosmosdbGremlinGraphIndexPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "indexing_mode": "indexingMode",
        "automatic": "automatic",
        "composite_index": "compositeIndex",
        "excluded_paths": "excludedPaths",
        "included_paths": "includedPaths",
        "spatial_index": "spatialIndex",
    },
)
class CosmosdbGremlinGraphIndexPolicy:
    def __init__(
        self,
        *,
        indexing_mode: builtins.str,
        automatic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        composite_index: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CosmosdbGremlinGraphIndexPolicyCompositeIndex", typing.Dict[builtins.str, typing.Any]]]]] = None,
        excluded_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        spatial_index: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CosmosdbGremlinGraphIndexPolicySpatialIndex", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param indexing_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#indexing_mode CosmosdbGremlinGraph#indexing_mode}.
        :param automatic: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#automatic CosmosdbGremlinGraph#automatic}.
        :param composite_index: composite_index block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#composite_index CosmosdbGremlinGraph#composite_index}
        :param excluded_paths: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#excluded_paths CosmosdbGremlinGraph#excluded_paths}.
        :param included_paths: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#included_paths CosmosdbGremlinGraph#included_paths}.
        :param spatial_index: spatial_index block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#spatial_index CosmosdbGremlinGraph#spatial_index}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7d58904ebd53750ee409475ca9d026254112c550e93f89dbc90468fec069b21)
            check_type(argname="argument indexing_mode", value=indexing_mode, expected_type=type_hints["indexing_mode"])
            check_type(argname="argument automatic", value=automatic, expected_type=type_hints["automatic"])
            check_type(argname="argument composite_index", value=composite_index, expected_type=type_hints["composite_index"])
            check_type(argname="argument excluded_paths", value=excluded_paths, expected_type=type_hints["excluded_paths"])
            check_type(argname="argument included_paths", value=included_paths, expected_type=type_hints["included_paths"])
            check_type(argname="argument spatial_index", value=spatial_index, expected_type=type_hints["spatial_index"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "indexing_mode": indexing_mode,
        }
        if automatic is not None:
            self._values["automatic"] = automatic
        if composite_index is not None:
            self._values["composite_index"] = composite_index
        if excluded_paths is not None:
            self._values["excluded_paths"] = excluded_paths
        if included_paths is not None:
            self._values["included_paths"] = included_paths
        if spatial_index is not None:
            self._values["spatial_index"] = spatial_index

    @builtins.property
    def indexing_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#indexing_mode CosmosdbGremlinGraph#indexing_mode}.'''
        result = self._values.get("indexing_mode")
        assert result is not None, "Required property 'indexing_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def automatic(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#automatic CosmosdbGremlinGraph#automatic}.'''
        result = self._values.get("automatic")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def composite_index(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbGremlinGraphIndexPolicyCompositeIndex"]]]:
        '''composite_index block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#composite_index CosmosdbGremlinGraph#composite_index}
        '''
        result = self._values.get("composite_index")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbGremlinGraphIndexPolicyCompositeIndex"]]], result)

    @builtins.property
    def excluded_paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#excluded_paths CosmosdbGremlinGraph#excluded_paths}.'''
        result = self._values.get("excluded_paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def included_paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#included_paths CosmosdbGremlinGraph#included_paths}.'''
        result = self._values.get("included_paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def spatial_index(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbGremlinGraphIndexPolicySpatialIndex"]]]:
        '''spatial_index block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#spatial_index CosmosdbGremlinGraph#spatial_index}
        '''
        result = self._values.get("spatial_index")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbGremlinGraphIndexPolicySpatialIndex"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbGremlinGraphIndexPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbGremlinGraph.CosmosdbGremlinGraphIndexPolicyCompositeIndex",
    jsii_struct_bases=[],
    name_mapping={"index": "index"},
)
class CosmosdbGremlinGraphIndexPolicyCompositeIndex:
    def __init__(
        self,
        *,
        index: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CosmosdbGremlinGraphIndexPolicyCompositeIndexIndex", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param index: index block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#index CosmosdbGremlinGraph#index}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__813c7635e577eee7812bba84d4f5e16411e15fb2ecc27d421d5269ef7c1937e8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "index": index,
        }

    @builtins.property
    def index(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbGremlinGraphIndexPolicyCompositeIndexIndex"]]:
        '''index block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#index CosmosdbGremlinGraph#index}
        '''
        result = self._values.get("index")
        assert result is not None, "Required property 'index' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbGremlinGraphIndexPolicyCompositeIndexIndex"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbGremlinGraphIndexPolicyCompositeIndex(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbGremlinGraph.CosmosdbGremlinGraphIndexPolicyCompositeIndexIndex",
    jsii_struct_bases=[],
    name_mapping={"order": "order", "path": "path"},
)
class CosmosdbGremlinGraphIndexPolicyCompositeIndexIndex:
    def __init__(self, *, order: builtins.str, path: builtins.str) -> None:
        '''
        :param order: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#order CosmosdbGremlinGraph#order}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#path CosmosdbGremlinGraph#path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7f7bf77f5212ddce73ecd2d1510de085470babea0e3624e7f47f4731c6b1df3)
            check_type(argname="argument order", value=order, expected_type=type_hints["order"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "order": order,
            "path": path,
        }

    @builtins.property
    def order(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#order CosmosdbGremlinGraph#order}.'''
        result = self._values.get("order")
        assert result is not None, "Required property 'order' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#path CosmosdbGremlinGraph#path}.'''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbGremlinGraphIndexPolicyCompositeIndexIndex(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CosmosdbGremlinGraphIndexPolicyCompositeIndexIndexList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbGremlinGraph.CosmosdbGremlinGraphIndexPolicyCompositeIndexIndexList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9df7ae22209477e757ddaf15a9fab43215474b996925699edec59db97669c36)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CosmosdbGremlinGraphIndexPolicyCompositeIndexIndexOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2390f23f66de0b1307dc645c8bbc97243381992061f7cf5048b0ac918feb6fbf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CosmosdbGremlinGraphIndexPolicyCompositeIndexIndexOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30d20b0224199fcdc67d6fd5043e915af369ee907f2e1036e38ecf01e3dfb824)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5faf97db75199dde192f5f3cd9724df44277870c64fc0562f22d820dc9841935)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5640aa58ebe424580134ce6daf3f8d329839ff16b317063b2fa302c9d22c8b5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbGremlinGraphIndexPolicyCompositeIndexIndex]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbGremlinGraphIndexPolicyCompositeIndexIndex]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbGremlinGraphIndexPolicyCompositeIndexIndex]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adf5fa2295b2d8338af1d2d83356c8ee3b31140236fa75e1131d06a3fac01911)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CosmosdbGremlinGraphIndexPolicyCompositeIndexIndexOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbGremlinGraph.CosmosdbGremlinGraphIndexPolicyCompositeIndexIndexOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__594a6b9c27be046e01ad84d13dcd3ba73ab0866223dfffa59fd5224d7d41e7e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e38332c5a94363ac57d8fb0687f405962dcfb99ba619cc4a615f7df2c2a673e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "order", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ff6a464dabe2a27c41deb16b56e5111315c04ea50b1170a63e8ce186382c420)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbGremlinGraphIndexPolicyCompositeIndexIndex]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbGremlinGraphIndexPolicyCompositeIndexIndex]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbGremlinGraphIndexPolicyCompositeIndexIndex]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97d1f44cabec9c5f9355623e75af224caaf53c14ff8020194caece1c5d235352)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CosmosdbGremlinGraphIndexPolicyCompositeIndexList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbGremlinGraph.CosmosdbGremlinGraphIndexPolicyCompositeIndexList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3118b995bbab835a8354debdf0458bfa62d13c6db563ce773a383509e5f2c28a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CosmosdbGremlinGraphIndexPolicyCompositeIndexOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f614a49389e09c05e3ecad2dd2ed426bde63e94937430dc1e6c5690514fa1fd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CosmosdbGremlinGraphIndexPolicyCompositeIndexOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f55cfa398fb38025e3b8ccae3e0cb74fcc782e30552a870fc7cff0fd8993ab6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bdabf9f0970f571172c091c54f23fc770d076aef4d89c727615d6db6958ab0c2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7908e4a126cd3f1f8c57cb5a99177391468fb073af2d9635fa7d585073fa476a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbGremlinGraphIndexPolicyCompositeIndex]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbGremlinGraphIndexPolicyCompositeIndex]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbGremlinGraphIndexPolicyCompositeIndex]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d48e28e17b01c91c92623c134bdba81e61def5de7cf73039a3638b56ec08da0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CosmosdbGremlinGraphIndexPolicyCompositeIndexOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbGremlinGraph.CosmosdbGremlinGraphIndexPolicyCompositeIndexOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__47727f2cf96c2ef7c87fb5bf2a6c80922c6bc72bfb045a67e1a8c9cee74ba286)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putIndex")
    def put_index(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbGremlinGraphIndexPolicyCompositeIndexIndex, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7c27d50fc2462b8c0dd42ec027c240f6147d9153fbe828c0068697256440528)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIndex", [value]))

    @builtins.property
    @jsii.member(jsii_name="index")
    def index(self) -> CosmosdbGremlinGraphIndexPolicyCompositeIndexIndexList:
        return typing.cast(CosmosdbGremlinGraphIndexPolicyCompositeIndexIndexList, jsii.get(self, "index"))

    @builtins.property
    @jsii.member(jsii_name="indexInput")
    def index_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbGremlinGraphIndexPolicyCompositeIndexIndex]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbGremlinGraphIndexPolicyCompositeIndexIndex]]], jsii.get(self, "indexInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbGremlinGraphIndexPolicyCompositeIndex]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbGremlinGraphIndexPolicyCompositeIndex]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbGremlinGraphIndexPolicyCompositeIndex]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11b18c76bf1cd98ebd99370e930de8bbd34d4d44dea4910f6c33477e402c883e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CosmosdbGremlinGraphIndexPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbGremlinGraph.CosmosdbGremlinGraphIndexPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a949e7f59fd84aaa2171401cdaf6b32c17385becf9af9cae9a6249f0592945f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCompositeIndex")
    def put_composite_index(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbGremlinGraphIndexPolicyCompositeIndex, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83bc2fc0fdbdf34c1f051bfa3e3077c119f193f3b9a935f3250666d5ffa9fed9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCompositeIndex", [value]))

    @jsii.member(jsii_name="putSpatialIndex")
    def put_spatial_index(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CosmosdbGremlinGraphIndexPolicySpatialIndex", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7982914ec0a96788a43f83d1aceec8bc0eb827fb61af9b23591f2c83e237805f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSpatialIndex", [value]))

    @jsii.member(jsii_name="resetAutomatic")
    def reset_automatic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutomatic", []))

    @jsii.member(jsii_name="resetCompositeIndex")
    def reset_composite_index(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompositeIndex", []))

    @jsii.member(jsii_name="resetExcludedPaths")
    def reset_excluded_paths(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedPaths", []))

    @jsii.member(jsii_name="resetIncludedPaths")
    def reset_included_paths(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludedPaths", []))

    @jsii.member(jsii_name="resetSpatialIndex")
    def reset_spatial_index(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpatialIndex", []))

    @builtins.property
    @jsii.member(jsii_name="compositeIndex")
    def composite_index(self) -> CosmosdbGremlinGraphIndexPolicyCompositeIndexList:
        return typing.cast(CosmosdbGremlinGraphIndexPolicyCompositeIndexList, jsii.get(self, "compositeIndex"))

    @builtins.property
    @jsii.member(jsii_name="spatialIndex")
    def spatial_index(self) -> "CosmosdbGremlinGraphIndexPolicySpatialIndexList":
        return typing.cast("CosmosdbGremlinGraphIndexPolicySpatialIndexList", jsii.get(self, "spatialIndex"))

    @builtins.property
    @jsii.member(jsii_name="automaticInput")
    def automatic_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "automaticInput"))

    @builtins.property
    @jsii.member(jsii_name="compositeIndexInput")
    def composite_index_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbGremlinGraphIndexPolicyCompositeIndex]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbGremlinGraphIndexPolicyCompositeIndex]]], jsii.get(self, "compositeIndexInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedPathsInput")
    def excluded_paths_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludedPathsInput"))

    @builtins.property
    @jsii.member(jsii_name="includedPathsInput")
    def included_paths_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includedPathsInput"))

    @builtins.property
    @jsii.member(jsii_name="indexingModeInput")
    def indexing_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "indexingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="spatialIndexInput")
    def spatial_index_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbGremlinGraphIndexPolicySpatialIndex"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbGremlinGraphIndexPolicySpatialIndex"]]], jsii.get(self, "spatialIndexInput"))

    @builtins.property
    @jsii.member(jsii_name="automatic")
    def automatic(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "automatic"))

    @automatic.setter
    def automatic(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3efd8eb74f9c04b41be0b14608c21527ed1284f25a716263b76455218077e998)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "automatic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludedPaths")
    def excluded_paths(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedPaths"))

    @excluded_paths.setter
    def excluded_paths(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d5125ee20635d649f51625d4ab68891b5bc9500a93eb2881004665021da5160)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedPaths", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includedPaths")
    def included_paths(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includedPaths"))

    @included_paths.setter
    def included_paths(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9de1396f4d24f924236ab53ce9e8833170e7b50f6ac2ad2318f87ceca1916755)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedPaths", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="indexingMode")
    def indexing_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "indexingMode"))

    @indexing_mode.setter
    def indexing_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dca4758d1a3a0e8c7a7ad0a6ecfcf1d9f5e5268f471b36004cac33a9bbcc3e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indexingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CosmosdbGremlinGraphIndexPolicy]:
        return typing.cast(typing.Optional[CosmosdbGremlinGraphIndexPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CosmosdbGremlinGraphIndexPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75e4aeec0d83ff66df619b2b3fc0842984613f27dfca60e065afec62abd2eab3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbGremlinGraph.CosmosdbGremlinGraphIndexPolicySpatialIndex",
    jsii_struct_bases=[],
    name_mapping={"path": "path"},
)
class CosmosdbGremlinGraphIndexPolicySpatialIndex:
    def __init__(self, *, path: builtins.str) -> None:
        '''
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#path CosmosdbGremlinGraph#path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cec3e2c64f9738aaee5289101d744b45eb00eb8c30d18d53a24590b89af4a0a)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
        }

    @builtins.property
    def path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#path CosmosdbGremlinGraph#path}.'''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbGremlinGraphIndexPolicySpatialIndex(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CosmosdbGremlinGraphIndexPolicySpatialIndexList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbGremlinGraph.CosmosdbGremlinGraphIndexPolicySpatialIndexList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__40018b4a03020f2ed272b653c38d3de88d6b71facd7d637bd172a402babdc4de)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CosmosdbGremlinGraphIndexPolicySpatialIndexOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60427c2b64d973a4e809b2f98f4d4b6a8bedfc7d54d4860520ab8433b1ffad83)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CosmosdbGremlinGraphIndexPolicySpatialIndexOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22e7232fa305dce145d0360d3738629ac9bae7e7b1b244e4edc0d7d3269bd467)
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
            type_hints = typing.get_type_hints(_typecheckingstub__51851d2ae3e5f378a1d9bb189cb85b22bd0b1c4c7a72470d49e7c1eabd47d24c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__99b8a67cc8edb6a1abbc1e5d489fb20bd974f47d178484b2290a8bc019bd6bc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbGremlinGraphIndexPolicySpatialIndex]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbGremlinGraphIndexPolicySpatialIndex]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbGremlinGraphIndexPolicySpatialIndex]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17600cd07a70ee481a7e81283bfc156a9f3f5ed7eb6c95e8c4c1b2c0d38b90bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CosmosdbGremlinGraphIndexPolicySpatialIndexOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbGremlinGraph.CosmosdbGremlinGraphIndexPolicySpatialIndexOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__826b89254f2a1708a40639de15d4f6ac6ae9b743ba06e52175ec5fbee5ab733d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a571a9f16becc466cc2fcadf59fd4828dd5b49f5013557f055ced75978c0d45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbGremlinGraphIndexPolicySpatialIndex]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbGremlinGraphIndexPolicySpatialIndex]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbGremlinGraphIndexPolicySpatialIndex]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69c49349608a256b5120d48daca6a2306e307f94d1f22b7f40fad4c03b179397)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbGremlinGraph.CosmosdbGremlinGraphTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class CosmosdbGremlinGraphTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#create CosmosdbGremlinGraph#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#delete CosmosdbGremlinGraph#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#read CosmosdbGremlinGraph#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#update CosmosdbGremlinGraph#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db48a9583de3846038051a1e9b11117ac7716a9db021340f2eb68aa7078c27e4)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#create CosmosdbGremlinGraph#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#delete CosmosdbGremlinGraph#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#read CosmosdbGremlinGraph#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#update CosmosdbGremlinGraph#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbGremlinGraphTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CosmosdbGremlinGraphTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbGremlinGraph.CosmosdbGremlinGraphTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e5df424cb9700e9d3a4b6b677d73637cdb7bbc76652699e4d766aeb7973b12c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd4db59e9607abd11b947042f3ca459a0bc8c13e3a57ba7117946f014aa1b21d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d5d8bf9d4be6a082025d633b53561ce1ba9018d2f6800cb95a5bab0598cb3e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26b201a3a1e9a8ce9a5cb077fb57ddd62cd7af5cf203dc28dd3e32f68757dbbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6463adc83b0c4123fbff6be31e5e5b5cef376c66824aeac2eb96dfb0780c3f7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbGremlinGraphTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbGremlinGraphTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbGremlinGraphTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae05c0e3503445e648310c7bef2d00d05ebffa3e69da8e7418e6fc23b53dd358)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbGremlinGraph.CosmosdbGremlinGraphUniqueKey",
    jsii_struct_bases=[],
    name_mapping={"paths": "paths"},
)
class CosmosdbGremlinGraphUniqueKey:
    def __init__(self, *, paths: typing.Sequence[builtins.str]) -> None:
        '''
        :param paths: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#paths CosmosdbGremlinGraph#paths}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f16a44dce92fafa572dd83bfea9cf5831670bd94118f7e079ff7be15ad1af034)
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "paths": paths,
        }

    @builtins.property
    def paths(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_gremlin_graph#paths CosmosdbGremlinGraph#paths}.'''
        result = self._values.get("paths")
        assert result is not None, "Required property 'paths' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbGremlinGraphUniqueKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CosmosdbGremlinGraphUniqueKeyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbGremlinGraph.CosmosdbGremlinGraphUniqueKeyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7fa185fa953d1c212e9966f312a1aef704ca869ac11755bb88a0e2fce31e331)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CosmosdbGremlinGraphUniqueKeyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63f1e1eb52de48cdcc9b077aa0e0225c921770be565c80437d59d2fa226b9639)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CosmosdbGremlinGraphUniqueKeyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7e4c8dd2920908f365da050ef9fba141f6a83ec09a73c537c36b812b56badba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54c1efe910742630e5b17f74d6002c61118a5c9ea81bb3e441dfe28184356308)
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
            type_hints = typing.get_type_hints(_typecheckingstub__408a850e438f0db75c7a60a118dcb265eeacaf1d58a68b02e841de856b03ac86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbGremlinGraphUniqueKey]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbGremlinGraphUniqueKey]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbGremlinGraphUniqueKey]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc2bb8eee2303b3e19a49ca5667cd29959c2efbc3ac3a2dfc9fd7145c0c9c176)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CosmosdbGremlinGraphUniqueKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbGremlinGraph.CosmosdbGremlinGraphUniqueKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__282d5a8a9e634721e935621e056f6452cdb0ea8db0b41f7f4a22df2136835b39)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e7fce78a2c083a792a8a6bc17b7de184e9f67424eed02c28e2cc68213c26725)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "paths", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbGremlinGraphUniqueKey]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbGremlinGraphUniqueKey]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbGremlinGraphUniqueKey]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5239ddefa2be54d8030cb8a93ce3cb4e01e005470408ab448b3260a0aa862ea5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CosmosdbGremlinGraph",
    "CosmosdbGremlinGraphAutoscaleSettings",
    "CosmosdbGremlinGraphAutoscaleSettingsOutputReference",
    "CosmosdbGremlinGraphConfig",
    "CosmosdbGremlinGraphConflictResolutionPolicy",
    "CosmosdbGremlinGraphConflictResolutionPolicyOutputReference",
    "CosmosdbGremlinGraphIndexPolicy",
    "CosmosdbGremlinGraphIndexPolicyCompositeIndex",
    "CosmosdbGremlinGraphIndexPolicyCompositeIndexIndex",
    "CosmosdbGremlinGraphIndexPolicyCompositeIndexIndexList",
    "CosmosdbGremlinGraphIndexPolicyCompositeIndexIndexOutputReference",
    "CosmosdbGremlinGraphIndexPolicyCompositeIndexList",
    "CosmosdbGremlinGraphIndexPolicyCompositeIndexOutputReference",
    "CosmosdbGremlinGraphIndexPolicyOutputReference",
    "CosmosdbGremlinGraphIndexPolicySpatialIndex",
    "CosmosdbGremlinGraphIndexPolicySpatialIndexList",
    "CosmosdbGremlinGraphIndexPolicySpatialIndexOutputReference",
    "CosmosdbGremlinGraphTimeouts",
    "CosmosdbGremlinGraphTimeoutsOutputReference",
    "CosmosdbGremlinGraphUniqueKey",
    "CosmosdbGremlinGraphUniqueKeyList",
    "CosmosdbGremlinGraphUniqueKeyOutputReference",
]

publication.publish()

def _typecheckingstub__fa8df528db5a92495231e27e05430d15be1440b51c76d79041a6439eff382bce(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    account_name: builtins.str,
    database_name: builtins.str,
    name: builtins.str,
    partition_key_path: builtins.str,
    resource_group_name: builtins.str,
    analytical_storage_ttl: typing.Optional[jsii.Number] = None,
    autoscale_settings: typing.Optional[typing.Union[CosmosdbGremlinGraphAutoscaleSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    conflict_resolution_policy: typing.Optional[typing.Union[CosmosdbGremlinGraphConflictResolutionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    default_ttl: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    index_policy: typing.Optional[typing.Union[CosmosdbGremlinGraphIndexPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    partition_key_version: typing.Optional[jsii.Number] = None,
    throughput: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[CosmosdbGremlinGraphTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    unique_key: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbGremlinGraphUniqueKey, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__530621025cf5da2138c68af9eb8e615e5f463236a6773848f0dc1072a7236e40(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc175b3a8f18c49a1d21538ddbf7812e2c3a35ae1f43e408eabeb75e776ba9b9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbGremlinGraphUniqueKey, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f4527ec5ae39df17385c5940eed8232a4950d223a5a934fb1eb0fd2435a1806(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d49576cf2e7ea685b8e3ca55b26b50528d66fc84cf75b2f996c727fc25fdbe50(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e13680cb8d8e7a25929ce1b00a8951270e968212ecb42d51745f160822e44ae4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3603de9891566be9777cce580f1085b023f188fb7e3b7c3ac2e0fec7115bb7ae(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69d65542b503c26d005febb777440e585184e77eda3183d8e60fe8f3773f4a05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d02995186389d3211b2696432d7e82dcd57b8025f9ddc0ba3d21161ba8067f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0af7d73eca5d69ede92f87b4c7b41cc13b67ee74efc3e4acb9d0fb1c06e535a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ccff9a5f98ea20fee8bd6e47bf5c80c9066b3cbe2a9cd1edb24c12f630255d1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c15a39f6ff81205e6275ca8f3e90fa069f963b4504e703d1991ae477cdc2490(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7dd3dbb8ee5d9e6bd24bf618fb4b5d091e3b6b324ebda3cd00b00b90c84d29a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e249108c67b8a5767dd17395bc6d13168a951c63e126a30d3e1db4d700e9332(
    *,
    max_throughput: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8ee708e5e861bc663a638ec73b57a033349fe6ce321c6c25fb3974c09fd2eee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ab99c4d01d546b441208bc35dcd53f28b372517bd5db70db2dcf7cc486b94c6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c93c45e9eb0a11415c172f43672ebca957e9aaac2f0815be691e4a13818cc46(
    value: typing.Optional[CosmosdbGremlinGraphAutoscaleSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0a443e7e7fb8e321936f079a44cd50a0af028bd528e3bc64f584943032c5686(
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
    partition_key_path: builtins.str,
    resource_group_name: builtins.str,
    analytical_storage_ttl: typing.Optional[jsii.Number] = None,
    autoscale_settings: typing.Optional[typing.Union[CosmosdbGremlinGraphAutoscaleSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    conflict_resolution_policy: typing.Optional[typing.Union[CosmosdbGremlinGraphConflictResolutionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    default_ttl: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    index_policy: typing.Optional[typing.Union[CosmosdbGremlinGraphIndexPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    partition_key_version: typing.Optional[jsii.Number] = None,
    throughput: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[CosmosdbGremlinGraphTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    unique_key: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbGremlinGraphUniqueKey, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__507f7bd2a7316c811ece87ce17b3c60be9c75616295a8e36d4aa5947a903d2ff(
    *,
    mode: builtins.str,
    conflict_resolution_path: typing.Optional[builtins.str] = None,
    conflict_resolution_procedure: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2efa00d8553c027c6004ce91fe602b2432711f8f21d598ad234701197362dfbc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59ab6de226a19a858e99936adfdb006771632d8c792211592d891e5c13e304a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad4492e123c64e479f2ae8239543a4e2684672cf833d0790e2ba594e8a645d21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8c5d878ba44db345463c966263cb9b97a7930e4de2798eedd8c49c420ae3fd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4547a2848349a03cba200da17bb49a8bc29f2c6ac13774377c99b8bb0e49a108(
    value: typing.Optional[CosmosdbGremlinGraphConflictResolutionPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7d58904ebd53750ee409475ca9d026254112c550e93f89dbc90468fec069b21(
    *,
    indexing_mode: builtins.str,
    automatic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    composite_index: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbGremlinGraphIndexPolicyCompositeIndex, typing.Dict[builtins.str, typing.Any]]]]] = None,
    excluded_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    included_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    spatial_index: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbGremlinGraphIndexPolicySpatialIndex, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__813c7635e577eee7812bba84d4f5e16411e15fb2ecc27d421d5269ef7c1937e8(
    *,
    index: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbGremlinGraphIndexPolicyCompositeIndexIndex, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7f7bf77f5212ddce73ecd2d1510de085470babea0e3624e7f47f4731c6b1df3(
    *,
    order: builtins.str,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9df7ae22209477e757ddaf15a9fab43215474b996925699edec59db97669c36(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2390f23f66de0b1307dc645c8bbc97243381992061f7cf5048b0ac918feb6fbf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30d20b0224199fcdc67d6fd5043e915af369ee907f2e1036e38ecf01e3dfb824(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5faf97db75199dde192f5f3cd9724df44277870c64fc0562f22d820dc9841935(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5640aa58ebe424580134ce6daf3f8d329839ff16b317063b2fa302c9d22c8b5e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adf5fa2295b2d8338af1d2d83356c8ee3b31140236fa75e1131d06a3fac01911(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbGremlinGraphIndexPolicyCompositeIndexIndex]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__594a6b9c27be046e01ad84d13dcd3ba73ab0866223dfffa59fd5224d7d41e7e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e38332c5a94363ac57d8fb0687f405962dcfb99ba619cc4a615f7df2c2a673e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ff6a464dabe2a27c41deb16b56e5111315c04ea50b1170a63e8ce186382c420(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97d1f44cabec9c5f9355623e75af224caaf53c14ff8020194caece1c5d235352(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbGremlinGraphIndexPolicyCompositeIndexIndex]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3118b995bbab835a8354debdf0458bfa62d13c6db563ce773a383509e5f2c28a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f614a49389e09c05e3ecad2dd2ed426bde63e94937430dc1e6c5690514fa1fd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f55cfa398fb38025e3b8ccae3e0cb74fcc782e30552a870fc7cff0fd8993ab6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdabf9f0970f571172c091c54f23fc770d076aef4d89c727615d6db6958ab0c2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7908e4a126cd3f1f8c57cb5a99177391468fb073af2d9635fa7d585073fa476a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d48e28e17b01c91c92623c134bdba81e61def5de7cf73039a3638b56ec08da0a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbGremlinGraphIndexPolicyCompositeIndex]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47727f2cf96c2ef7c87fb5bf2a6c80922c6bc72bfb045a67e1a8c9cee74ba286(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7c27d50fc2462b8c0dd42ec027c240f6147d9153fbe828c0068697256440528(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbGremlinGraphIndexPolicyCompositeIndexIndex, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11b18c76bf1cd98ebd99370e930de8bbd34d4d44dea4910f6c33477e402c883e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbGremlinGraphIndexPolicyCompositeIndex]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a949e7f59fd84aaa2171401cdaf6b32c17385becf9af9cae9a6249f0592945f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83bc2fc0fdbdf34c1f051bfa3e3077c119f193f3b9a935f3250666d5ffa9fed9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbGremlinGraphIndexPolicyCompositeIndex, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7982914ec0a96788a43f83d1aceec8bc0eb827fb61af9b23591f2c83e237805f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbGremlinGraphIndexPolicySpatialIndex, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3efd8eb74f9c04b41be0b14608c21527ed1284f25a716263b76455218077e998(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d5125ee20635d649f51625d4ab68891b5bc9500a93eb2881004665021da5160(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9de1396f4d24f924236ab53ce9e8833170e7b50f6ac2ad2318f87ceca1916755(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dca4758d1a3a0e8c7a7ad0a6ecfcf1d9f5e5268f471b36004cac33a9bbcc3e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75e4aeec0d83ff66df619b2b3fc0842984613f27dfca60e065afec62abd2eab3(
    value: typing.Optional[CosmosdbGremlinGraphIndexPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cec3e2c64f9738aaee5289101d744b45eb00eb8c30d18d53a24590b89af4a0a(
    *,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40018b4a03020f2ed272b653c38d3de88d6b71facd7d637bd172a402babdc4de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60427c2b64d973a4e809b2f98f4d4b6a8bedfc7d54d4860520ab8433b1ffad83(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22e7232fa305dce145d0360d3738629ac9bae7e7b1b244e4edc0d7d3269bd467(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51851d2ae3e5f378a1d9bb189cb85b22bd0b1c4c7a72470d49e7c1eabd47d24c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99b8a67cc8edb6a1abbc1e5d489fb20bd974f47d178484b2290a8bc019bd6bc6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17600cd07a70ee481a7e81283bfc156a9f3f5ed7eb6c95e8c4c1b2c0d38b90bf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbGremlinGraphIndexPolicySpatialIndex]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__826b89254f2a1708a40639de15d4f6ac6ae9b743ba06e52175ec5fbee5ab733d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a571a9f16becc466cc2fcadf59fd4828dd5b49f5013557f055ced75978c0d45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69c49349608a256b5120d48daca6a2306e307f94d1f22b7f40fad4c03b179397(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbGremlinGraphIndexPolicySpatialIndex]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db48a9583de3846038051a1e9b11117ac7716a9db021340f2eb68aa7078c27e4(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e5df424cb9700e9d3a4b6b677d73637cdb7bbc76652699e4d766aeb7973b12c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd4db59e9607abd11b947042f3ca459a0bc8c13e3a57ba7117946f014aa1b21d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d5d8bf9d4be6a082025d633b53561ce1ba9018d2f6800cb95a5bab0598cb3e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26b201a3a1e9a8ce9a5cb077fb57ddd62cd7af5cf203dc28dd3e32f68757dbbb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6463adc83b0c4123fbff6be31e5e5b5cef376c66824aeac2eb96dfb0780c3f7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae05c0e3503445e648310c7bef2d00d05ebffa3e69da8e7418e6fc23b53dd358(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbGremlinGraphTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f16a44dce92fafa572dd83bfea9cf5831670bd94118f7e079ff7be15ad1af034(
    *,
    paths: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7fa185fa953d1c212e9966f312a1aef704ca869ac11755bb88a0e2fce31e331(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63f1e1eb52de48cdcc9b077aa0e0225c921770be565c80437d59d2fa226b9639(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7e4c8dd2920908f365da050ef9fba141f6a83ec09a73c537c36b812b56badba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54c1efe910742630e5b17f74d6002c61118a5c9ea81bb3e441dfe28184356308(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__408a850e438f0db75c7a60a118dcb265eeacaf1d58a68b02e841de856b03ac86(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc2bb8eee2303b3e19a49ca5667cd29959c2efbc3ac3a2dfc9fd7145c0c9c176(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbGremlinGraphUniqueKey]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__282d5a8a9e634721e935621e056f6452cdb0ea8db0b41f7f4a22df2136835b39(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e7fce78a2c083a792a8a6bc17b7de184e9f67424eed02c28e2cc68213c26725(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5239ddefa2be54d8030cb8a93ce3cb4e01e005470408ab448b3260a0aa862ea5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbGremlinGraphUniqueKey]],
) -> None:
    """Type checking stubs"""
    pass
