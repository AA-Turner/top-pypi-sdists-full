r'''
# `google_vertex_ai_feature_online_store_featureview`

Refer to the Terraform Registry for docs: [`google_vertex_ai_feature_online_store_featureview`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview).
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


class GoogleVertexAiFeatureOnlineStoreFeatureview(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeatureOnlineStoreFeatureview.GoogleVertexAiFeatureOnlineStoreFeatureview",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview google_vertex_ai_feature_online_store_featureview}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        feature_online_store: builtins.str,
        big_query_source: typing.Optional[typing.Union["GoogleVertexAiFeatureOnlineStoreFeatureviewBigQuerySource", typing.Dict[builtins.str, typing.Any]]] = None,
        feature_registry_source: typing.Optional[typing.Union["GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySource", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        sync_config: typing.Optional[typing.Union["GoogleVertexAiFeatureOnlineStoreFeatureviewSyncConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleVertexAiFeatureOnlineStoreFeatureviewTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        vector_search_config: typing.Optional[typing.Union["GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview google_vertex_ai_feature_online_store_featureview} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param feature_online_store: The name of the FeatureOnlineStore to use for the featureview. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#feature_online_store GoogleVertexAiFeatureOnlineStoreFeatureview#feature_online_store}
        :param big_query_source: big_query_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#big_query_source GoogleVertexAiFeatureOnlineStoreFeatureview#big_query_source}
        :param feature_registry_source: feature_registry_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#feature_registry_source GoogleVertexAiFeatureOnlineStoreFeatureview#feature_registry_source}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#id GoogleVertexAiFeatureOnlineStoreFeatureview#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: A set of key/value label pairs to assign to this FeatureView. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#labels GoogleVertexAiFeatureOnlineStoreFeatureview#labels}
        :param name: Name of the FeatureView. This value may be up to 60 characters, and valid characters are [a-z0-9_]. The first character cannot be a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#name GoogleVertexAiFeatureOnlineStoreFeatureview#name}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#project GoogleVertexAiFeatureOnlineStoreFeatureview#project}.
        :param region: The region for the resource. It should be the same as the featureonlinestore region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#region GoogleVertexAiFeatureOnlineStoreFeatureview#region}
        :param sync_config: sync_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#sync_config GoogleVertexAiFeatureOnlineStoreFeatureview#sync_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#timeouts GoogleVertexAiFeatureOnlineStoreFeatureview#timeouts}
        :param vector_search_config: vector_search_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#vector_search_config GoogleVertexAiFeatureOnlineStoreFeatureview#vector_search_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18384ef55b8963fe5e1663993536da6a86ac8e92e3661ae3c379e46432f227bf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleVertexAiFeatureOnlineStoreFeatureviewConfig(
            feature_online_store=feature_online_store,
            big_query_source=big_query_source,
            feature_registry_source=feature_registry_source,
            id=id,
            labels=labels,
            name=name,
            project=project,
            region=region,
            sync_config=sync_config,
            timeouts=timeouts,
            vector_search_config=vector_search_config,
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
        '''Generates CDKTF code for importing a GoogleVertexAiFeatureOnlineStoreFeatureview resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleVertexAiFeatureOnlineStoreFeatureview to import.
        :param import_from_id: The id of the existing GoogleVertexAiFeatureOnlineStoreFeatureview that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleVertexAiFeatureOnlineStoreFeatureview to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e85bd3e7cfe1f08ef5446a16680f4c08f65a7e3ef271240ccfa9a8c5e75e9d50)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBigQuerySource")
    def put_big_query_source(
        self,
        *,
        entity_id_columns: typing.Sequence[builtins.str],
        uri: builtins.str,
    ) -> None:
        '''
        :param entity_id_columns: Columns to construct entityId / row keys. Start by supporting 1 only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#entity_id_columns GoogleVertexAiFeatureOnlineStoreFeatureview#entity_id_columns}
        :param uri: The BigQuery view URI that will be materialized on each sync trigger based on FeatureView.SyncConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#uri GoogleVertexAiFeatureOnlineStoreFeatureview#uri}
        '''
        value = GoogleVertexAiFeatureOnlineStoreFeatureviewBigQuerySource(
            entity_id_columns=entity_id_columns, uri=uri
        )

        return typing.cast(None, jsii.invoke(self, "putBigQuerySource", [value]))

    @jsii.member(jsii_name="putFeatureRegistrySource")
    def put_feature_registry_source(
        self,
        *,
        feature_groups: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups", typing.Dict[builtins.str, typing.Any]]]],
        project_number: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param feature_groups: feature_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#feature_groups GoogleVertexAiFeatureOnlineStoreFeatureview#feature_groups}
        :param project_number: The project number of the parent project of the feature Groups. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#project_number GoogleVertexAiFeatureOnlineStoreFeatureview#project_number}
        '''
        value = GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySource(
            feature_groups=feature_groups, project_number=project_number
        )

        return typing.cast(None, jsii.invoke(self, "putFeatureRegistrySource", [value]))

    @jsii.member(jsii_name="putSyncConfig")
    def put_sync_config(self, *, cron: typing.Optional[builtins.str] = None) -> None:
        '''
        :param cron: Cron schedule (https://en.wikipedia.org/wiki/Cron) to launch scheduled runs. To explicitly set a timezone to the cron tab, apply a prefix in the cron tab: "CRON_TZ=${IANA_TIME_ZONE}" or "TZ=${IANA_TIME_ZONE}". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#cron GoogleVertexAiFeatureOnlineStoreFeatureview#cron}
        '''
        value = GoogleVertexAiFeatureOnlineStoreFeatureviewSyncConfig(cron=cron)

        return typing.cast(None, jsii.invoke(self, "putSyncConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#create GoogleVertexAiFeatureOnlineStoreFeatureview#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#delete GoogleVertexAiFeatureOnlineStoreFeatureview#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#update GoogleVertexAiFeatureOnlineStoreFeatureview#update}.
        '''
        value = GoogleVertexAiFeatureOnlineStoreFeatureviewTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVectorSearchConfig")
    def put_vector_search_config(
        self,
        *,
        embedding_column: builtins.str,
        brute_force_config: typing.Optional[typing.Union["GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigBruteForceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        crowding_column: typing.Optional[builtins.str] = None,
        distance_measure_type: typing.Optional[builtins.str] = None,
        embedding_dimension: typing.Optional[jsii.Number] = None,
        filter_columns: typing.Optional[typing.Sequence[builtins.str]] = None,
        tree_ah_config: typing.Optional[typing.Union["GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigTreeAhConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param embedding_column: Column of embedding. This column contains the source data to create index for vector search. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#embedding_column GoogleVertexAiFeatureOnlineStoreFeatureview#embedding_column}
        :param brute_force_config: brute_force_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#brute_force_config GoogleVertexAiFeatureOnlineStoreFeatureview#brute_force_config}
        :param crowding_column: Column of crowding. This column contains crowding attribute which is a constraint on a neighbor list produced by nearest neighbor search requiring that no more than some value k' of the k neighbors returned have the same value of crowdingAttribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#crowding_column GoogleVertexAiFeatureOnlineStoreFeatureview#crowding_column}
        :param distance_measure_type: The distance measure used in nearest neighbor search. For details on allowed values, see the `API documentation <https://cloud.google.com/vertex-ai/docs/reference/rest/v1beta1/projects.locations.featureOnlineStores.featureViews#DistanceMeasureType>`_. Possible values: ["SQUARED_L2_DISTANCE", "COSINE_DISTANCE", "DOT_PRODUCT_DISTANCE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#distance_measure_type GoogleVertexAiFeatureOnlineStoreFeatureview#distance_measure_type}
        :param embedding_dimension: The number of dimensions of the input embedding. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#embedding_dimension GoogleVertexAiFeatureOnlineStoreFeatureview#embedding_dimension}
        :param filter_columns: Columns of features that are used to filter vector search results. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#filter_columns GoogleVertexAiFeatureOnlineStoreFeatureview#filter_columns}
        :param tree_ah_config: tree_ah_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#tree_ah_config GoogleVertexAiFeatureOnlineStoreFeatureview#tree_ah_config}
        '''
        value = GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfig(
            embedding_column=embedding_column,
            brute_force_config=brute_force_config,
            crowding_column=crowding_column,
            distance_measure_type=distance_measure_type,
            embedding_dimension=embedding_dimension,
            filter_columns=filter_columns,
            tree_ah_config=tree_ah_config,
        )

        return typing.cast(None, jsii.invoke(self, "putVectorSearchConfig", [value]))

    @jsii.member(jsii_name="resetBigQuerySource")
    def reset_big_query_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBigQuerySource", []))

    @jsii.member(jsii_name="resetFeatureRegistrySource")
    def reset_feature_registry_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFeatureRegistrySource", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSyncConfig")
    def reset_sync_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncConfig", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVectorSearchConfig")
    def reset_vector_search_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVectorSearchConfig", []))

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
    @jsii.member(jsii_name="bigQuerySource")
    def big_query_source(
        self,
    ) -> "GoogleVertexAiFeatureOnlineStoreFeatureviewBigQuerySourceOutputReference":
        return typing.cast("GoogleVertexAiFeatureOnlineStoreFeatureviewBigQuerySourceOutputReference", jsii.get(self, "bigQuerySource"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="featureRegistrySource")
    def feature_registry_source(
        self,
    ) -> "GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceOutputReference":
        return typing.cast("GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceOutputReference", jsii.get(self, "featureRegistrySource"))

    @builtins.property
    @jsii.member(jsii_name="syncConfig")
    def sync_config(
        self,
    ) -> "GoogleVertexAiFeatureOnlineStoreFeatureviewSyncConfigOutputReference":
        return typing.cast("GoogleVertexAiFeatureOnlineStoreFeatureviewSyncConfigOutputReference", jsii.get(self, "syncConfig"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "GoogleVertexAiFeatureOnlineStoreFeatureviewTimeoutsOutputReference":
        return typing.cast("GoogleVertexAiFeatureOnlineStoreFeatureviewTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="vectorSearchConfig")
    def vector_search_config(
        self,
    ) -> "GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigOutputReference":
        return typing.cast("GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigOutputReference", jsii.get(self, "vectorSearchConfig"))

    @builtins.property
    @jsii.member(jsii_name="bigQuerySourceInput")
    def big_query_source_input(
        self,
    ) -> typing.Optional["GoogleVertexAiFeatureOnlineStoreFeatureviewBigQuerySource"]:
        return typing.cast(typing.Optional["GoogleVertexAiFeatureOnlineStoreFeatureviewBigQuerySource"], jsii.get(self, "bigQuerySourceInput"))

    @builtins.property
    @jsii.member(jsii_name="featureOnlineStoreInput")
    def feature_online_store_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "featureOnlineStoreInput"))

    @builtins.property
    @jsii.member(jsii_name="featureRegistrySourceInput")
    def feature_registry_source_input(
        self,
    ) -> typing.Optional["GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySource"]:
        return typing.cast(typing.Optional["GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySource"], jsii.get(self, "featureRegistrySourceInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

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
    @jsii.member(jsii_name="syncConfigInput")
    def sync_config_input(
        self,
    ) -> typing.Optional["GoogleVertexAiFeatureOnlineStoreFeatureviewSyncConfig"]:
        return typing.cast(typing.Optional["GoogleVertexAiFeatureOnlineStoreFeatureviewSyncConfig"], jsii.get(self, "syncConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleVertexAiFeatureOnlineStoreFeatureviewTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleVertexAiFeatureOnlineStoreFeatureviewTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="vectorSearchConfigInput")
    def vector_search_config_input(
        self,
    ) -> typing.Optional["GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfig"]:
        return typing.cast(typing.Optional["GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfig"], jsii.get(self, "vectorSearchConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="featureOnlineStore")
    def feature_online_store(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "featureOnlineStore"))

    @feature_online_store.setter
    def feature_online_store(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__415e030426cd7768069730abec76295eb8b58f4facaf7175ec66f6020f39959d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "featureOnlineStore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2843084426a5342b5c3097d0b454d0486f8476dee7707e8db6ae501015cac5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1e3988ca7684db6bc2dd0833a108e726e8b31ce3567c347e26e6bd6c88f4089)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__341733b85047216bae965f0fbb48e5e4cd4e07cd7871ca6d033ae4fafa771bf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d624ecce79f003318814d3d52f2b97e416aa75ce881a42105b20b346283a972b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c47d25119f4ec3cf09f3fe79dff7e7d9b1cac8373fa1764f196c45ac42658b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeatureOnlineStoreFeatureview.GoogleVertexAiFeatureOnlineStoreFeatureviewBigQuerySource",
    jsii_struct_bases=[],
    name_mapping={"entity_id_columns": "entityIdColumns", "uri": "uri"},
)
class GoogleVertexAiFeatureOnlineStoreFeatureviewBigQuerySource:
    def __init__(
        self,
        *,
        entity_id_columns: typing.Sequence[builtins.str],
        uri: builtins.str,
    ) -> None:
        '''
        :param entity_id_columns: Columns to construct entityId / row keys. Start by supporting 1 only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#entity_id_columns GoogleVertexAiFeatureOnlineStoreFeatureview#entity_id_columns}
        :param uri: The BigQuery view URI that will be materialized on each sync trigger based on FeatureView.SyncConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#uri GoogleVertexAiFeatureOnlineStoreFeatureview#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c9f8f7e10da98e222c330fceaaa6d0f2409fbaf486bf0512f2e7664d6ee7574)
            check_type(argname="argument entity_id_columns", value=entity_id_columns, expected_type=type_hints["entity_id_columns"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "entity_id_columns": entity_id_columns,
            "uri": uri,
        }

    @builtins.property
    def entity_id_columns(self) -> typing.List[builtins.str]:
        '''Columns to construct entityId / row keys. Start by supporting 1 only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#entity_id_columns GoogleVertexAiFeatureOnlineStoreFeatureview#entity_id_columns}
        '''
        result = self._values.get("entity_id_columns")
        assert result is not None, "Required property 'entity_id_columns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def uri(self) -> builtins.str:
        '''The BigQuery view URI that will be materialized on each sync trigger based on FeatureView.SyncConfig.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#uri GoogleVertexAiFeatureOnlineStoreFeatureview#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiFeatureOnlineStoreFeatureviewBigQuerySource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiFeatureOnlineStoreFeatureviewBigQuerySourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeatureOnlineStoreFeatureview.GoogleVertexAiFeatureOnlineStoreFeatureviewBigQuerySourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e76a2ee98b9bb6564f87906b902b8bf67759ea2df59ff5f39200597502b6b2bd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="entityIdColumnsInput")
    def entity_id_columns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "entityIdColumnsInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="entityIdColumns")
    def entity_id_columns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "entityIdColumns"))

    @entity_id_columns.setter
    def entity_id_columns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__458dfdfaf81d661398b4158d00889381b3a836240d8f3cf775039581f11c9e0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entityIdColumns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c153ae2463a0ecec947598c0d3d4cc5c87f9a72ad9ee638545042d1aa317b63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiFeatureOnlineStoreFeatureviewBigQuerySource]:
        return typing.cast(typing.Optional[GoogleVertexAiFeatureOnlineStoreFeatureviewBigQuerySource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiFeatureOnlineStoreFeatureviewBigQuerySource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3fa9504cb181cfb2799adf7a5d89ffb77c1cb0c92f5453ec2f614f8e7bed781)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeatureOnlineStoreFeatureview.GoogleVertexAiFeatureOnlineStoreFeatureviewConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "feature_online_store": "featureOnlineStore",
        "big_query_source": "bigQuerySource",
        "feature_registry_source": "featureRegistrySource",
        "id": "id",
        "labels": "labels",
        "name": "name",
        "project": "project",
        "region": "region",
        "sync_config": "syncConfig",
        "timeouts": "timeouts",
        "vector_search_config": "vectorSearchConfig",
    },
)
class GoogleVertexAiFeatureOnlineStoreFeatureviewConfig(
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
        feature_online_store: builtins.str,
        big_query_source: typing.Optional[typing.Union[GoogleVertexAiFeatureOnlineStoreFeatureviewBigQuerySource, typing.Dict[builtins.str, typing.Any]]] = None,
        feature_registry_source: typing.Optional[typing.Union["GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySource", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        sync_config: typing.Optional[typing.Union["GoogleVertexAiFeatureOnlineStoreFeatureviewSyncConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleVertexAiFeatureOnlineStoreFeatureviewTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        vector_search_config: typing.Optional[typing.Union["GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param feature_online_store: The name of the FeatureOnlineStore to use for the featureview. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#feature_online_store GoogleVertexAiFeatureOnlineStoreFeatureview#feature_online_store}
        :param big_query_source: big_query_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#big_query_source GoogleVertexAiFeatureOnlineStoreFeatureview#big_query_source}
        :param feature_registry_source: feature_registry_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#feature_registry_source GoogleVertexAiFeatureOnlineStoreFeatureview#feature_registry_source}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#id GoogleVertexAiFeatureOnlineStoreFeatureview#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: A set of key/value label pairs to assign to this FeatureView. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#labels GoogleVertexAiFeatureOnlineStoreFeatureview#labels}
        :param name: Name of the FeatureView. This value may be up to 60 characters, and valid characters are [a-z0-9_]. The first character cannot be a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#name GoogleVertexAiFeatureOnlineStoreFeatureview#name}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#project GoogleVertexAiFeatureOnlineStoreFeatureview#project}.
        :param region: The region for the resource. It should be the same as the featureonlinestore region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#region GoogleVertexAiFeatureOnlineStoreFeatureview#region}
        :param sync_config: sync_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#sync_config GoogleVertexAiFeatureOnlineStoreFeatureview#sync_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#timeouts GoogleVertexAiFeatureOnlineStoreFeatureview#timeouts}
        :param vector_search_config: vector_search_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#vector_search_config GoogleVertexAiFeatureOnlineStoreFeatureview#vector_search_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(big_query_source, dict):
            big_query_source = GoogleVertexAiFeatureOnlineStoreFeatureviewBigQuerySource(**big_query_source)
        if isinstance(feature_registry_source, dict):
            feature_registry_source = GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySource(**feature_registry_source)
        if isinstance(sync_config, dict):
            sync_config = GoogleVertexAiFeatureOnlineStoreFeatureviewSyncConfig(**sync_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleVertexAiFeatureOnlineStoreFeatureviewTimeouts(**timeouts)
        if isinstance(vector_search_config, dict):
            vector_search_config = GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfig(**vector_search_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2771584a12631ac838047e05d25fc66f9c74a4930200caa57390b3d9523ccb6b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument feature_online_store", value=feature_online_store, expected_type=type_hints["feature_online_store"])
            check_type(argname="argument big_query_source", value=big_query_source, expected_type=type_hints["big_query_source"])
            check_type(argname="argument feature_registry_source", value=feature_registry_source, expected_type=type_hints["feature_registry_source"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument sync_config", value=sync_config, expected_type=type_hints["sync_config"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument vector_search_config", value=vector_search_config, expected_type=type_hints["vector_search_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "feature_online_store": feature_online_store,
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
        if big_query_source is not None:
            self._values["big_query_source"] = big_query_source
        if feature_registry_source is not None:
            self._values["feature_registry_source"] = feature_registry_source
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if name is not None:
            self._values["name"] = name
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
        if sync_config is not None:
            self._values["sync_config"] = sync_config
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if vector_search_config is not None:
            self._values["vector_search_config"] = vector_search_config

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
    def feature_online_store(self) -> builtins.str:
        '''The name of the FeatureOnlineStore to use for the featureview.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#feature_online_store GoogleVertexAiFeatureOnlineStoreFeatureview#feature_online_store}
        '''
        result = self._values.get("feature_online_store")
        assert result is not None, "Required property 'feature_online_store' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def big_query_source(
        self,
    ) -> typing.Optional[GoogleVertexAiFeatureOnlineStoreFeatureviewBigQuerySource]:
        '''big_query_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#big_query_source GoogleVertexAiFeatureOnlineStoreFeatureview#big_query_source}
        '''
        result = self._values.get("big_query_source")
        return typing.cast(typing.Optional[GoogleVertexAiFeatureOnlineStoreFeatureviewBigQuerySource], result)

    @builtins.property
    def feature_registry_source(
        self,
    ) -> typing.Optional["GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySource"]:
        '''feature_registry_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#feature_registry_source GoogleVertexAiFeatureOnlineStoreFeatureview#feature_registry_source}
        '''
        result = self._values.get("feature_registry_source")
        return typing.cast(typing.Optional["GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySource"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#id GoogleVertexAiFeatureOnlineStoreFeatureview#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A set of key/value label pairs to assign to this FeatureView.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#labels GoogleVertexAiFeatureOnlineStoreFeatureview#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the FeatureView.

        This value may be up to 60 characters, and valid characters are [a-z0-9_]. The first character cannot be a number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#name GoogleVertexAiFeatureOnlineStoreFeatureview#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#project GoogleVertexAiFeatureOnlineStoreFeatureview#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region for the resource. It should be the same as the featureonlinestore region.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#region GoogleVertexAiFeatureOnlineStoreFeatureview#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_config(
        self,
    ) -> typing.Optional["GoogleVertexAiFeatureOnlineStoreFeatureviewSyncConfig"]:
        '''sync_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#sync_config GoogleVertexAiFeatureOnlineStoreFeatureview#sync_config}
        '''
        result = self._values.get("sync_config")
        return typing.cast(typing.Optional["GoogleVertexAiFeatureOnlineStoreFeatureviewSyncConfig"], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleVertexAiFeatureOnlineStoreFeatureviewTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#timeouts GoogleVertexAiFeatureOnlineStoreFeatureview#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleVertexAiFeatureOnlineStoreFeatureviewTimeouts"], result)

    @builtins.property
    def vector_search_config(
        self,
    ) -> typing.Optional["GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfig"]:
        '''vector_search_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#vector_search_config GoogleVertexAiFeatureOnlineStoreFeatureview#vector_search_config}
        '''
        result = self._values.get("vector_search_config")
        return typing.cast(typing.Optional["GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiFeatureOnlineStoreFeatureviewConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeatureOnlineStoreFeatureview.GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySource",
    jsii_struct_bases=[],
    name_mapping={
        "feature_groups": "featureGroups",
        "project_number": "projectNumber",
    },
)
class GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySource:
    def __init__(
        self,
        *,
        feature_groups: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups", typing.Dict[builtins.str, typing.Any]]]],
        project_number: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param feature_groups: feature_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#feature_groups GoogleVertexAiFeatureOnlineStoreFeatureview#feature_groups}
        :param project_number: The project number of the parent project of the feature Groups. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#project_number GoogleVertexAiFeatureOnlineStoreFeatureview#project_number}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b89ee9848d297de866dde872beaa853657098e15399171236e0e3182d479aa5)
            check_type(argname="argument feature_groups", value=feature_groups, expected_type=type_hints["feature_groups"])
            check_type(argname="argument project_number", value=project_number, expected_type=type_hints["project_number"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "feature_groups": feature_groups,
        }
        if project_number is not None:
            self._values["project_number"] = project_number

    @builtins.property
    def feature_groups(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups"]]:
        '''feature_groups block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#feature_groups GoogleVertexAiFeatureOnlineStoreFeatureview#feature_groups}
        '''
        result = self._values.get("feature_groups")
        assert result is not None, "Required property 'feature_groups' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups"]], result)

    @builtins.property
    def project_number(self) -> typing.Optional[builtins.str]:
        '''The project number of the parent project of the feature Groups.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#project_number GoogleVertexAiFeatureOnlineStoreFeatureview#project_number}
        '''
        result = self._values.get("project_number")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeatureOnlineStoreFeatureview.GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups",
    jsii_struct_bases=[],
    name_mapping={"feature_group_id": "featureGroupId", "feature_ids": "featureIds"},
)
class GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups:
    def __init__(
        self,
        *,
        feature_group_id: builtins.str,
        feature_ids: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param feature_group_id: Identifier of the feature group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#feature_group_id GoogleVertexAiFeatureOnlineStoreFeatureview#feature_group_id}
        :param feature_ids: Identifiers of features under the feature group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#feature_ids GoogleVertexAiFeatureOnlineStoreFeatureview#feature_ids}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__661556a5f0258a513e5f0cc100fab60491a105467764f3ad51f876cc2f205130)
            check_type(argname="argument feature_group_id", value=feature_group_id, expected_type=type_hints["feature_group_id"])
            check_type(argname="argument feature_ids", value=feature_ids, expected_type=type_hints["feature_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "feature_group_id": feature_group_id,
            "feature_ids": feature_ids,
        }

    @builtins.property
    def feature_group_id(self) -> builtins.str:
        '''Identifier of the feature group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#feature_group_id GoogleVertexAiFeatureOnlineStoreFeatureview#feature_group_id}
        '''
        result = self._values.get("feature_group_id")
        assert result is not None, "Required property 'feature_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def feature_ids(self) -> typing.List[builtins.str]:
        '''Identifiers of features under the feature group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#feature_ids GoogleVertexAiFeatureOnlineStoreFeatureview#feature_ids}
        '''
        result = self._values.get("feature_ids")
        assert result is not None, "Required property 'feature_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroupsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeatureOnlineStoreFeatureview.GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroupsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eddfbee0a1f8d56515596db20a807ffc0a0c2b6c80903283f05c71afeac12a0e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroupsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff19d46221c0a2812fc2db10e138965933f142921b844338bd9c976db4b0a4b5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroupsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__054d8e5fa95a9c0fe02fea7f426e50acac28a1862050b4201bebb4ae81db1359)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0479229f8969aa400d2f757d54f208379ae0960122306d957d6367e57d2e9767)
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
            type_hints = typing.get_type_hints(_typecheckingstub__47df1ce9f7200e1d0beb03a67acaa42c9a628c07163a979d38ec294f910abe44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8677f55718e0d991aa7846f87c87f7227a9cc06c5c936736b92ea45315065d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroupsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeatureOnlineStoreFeatureview.GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroupsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__173a501a0b2563547a37f466ec8c3b376b6c0bf2ec3037124a348021821fc24f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="featureGroupIdInput")
    def feature_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "featureGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="featureIdsInput")
    def feature_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "featureIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="featureGroupId")
    def feature_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "featureGroupId"))

    @feature_group_id.setter
    def feature_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16fa1b7a4ed5c0d79db59ff2179223892272c4d20a03a6f41ac2b95ca2012b87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "featureGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="featureIds")
    def feature_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "featureIds"))

    @feature_ids.setter
    def feature_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68119c506e8690ff8c1ddc849e780b086dd25a483dd6979ae3e3ac9434623e4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "featureIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d444debffe177133dff849dbd8a5fd28d85b241119b75b0c89c804bea79d447a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeatureOnlineStoreFeatureview.GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__255da47835584e51a822e00d37c6c24c71d2a2ccb8438543775d697883942f31)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFeatureGroups")
    def put_feature_groups(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96eb58be46afec73b51dd333b2737926f299f63dec24fe71ffc21905b0799740)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFeatureGroups", [value]))

    @jsii.member(jsii_name="resetProjectNumber")
    def reset_project_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectNumber", []))

    @builtins.property
    @jsii.member(jsii_name="featureGroups")
    def feature_groups(
        self,
    ) -> GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroupsList:
        return typing.cast(GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroupsList, jsii.get(self, "featureGroups"))

    @builtins.property
    @jsii.member(jsii_name="featureGroupsInput")
    def feature_groups_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups]]], jsii.get(self, "featureGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="projectNumberInput")
    def project_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="projectNumber")
    def project_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectNumber"))

    @project_number.setter
    def project_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3bddf82bde71243db7db153c87846fbbe87f8fc32ffb867033401c79354e645)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySource]:
        return typing.cast(typing.Optional[GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b28bf73b2cb86e094e3a498fe8fd43a9c95c00828e9b6627f1ae4851565b3027)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeatureOnlineStoreFeatureview.GoogleVertexAiFeatureOnlineStoreFeatureviewSyncConfig",
    jsii_struct_bases=[],
    name_mapping={"cron": "cron"},
)
class GoogleVertexAiFeatureOnlineStoreFeatureviewSyncConfig:
    def __init__(self, *, cron: typing.Optional[builtins.str] = None) -> None:
        '''
        :param cron: Cron schedule (https://en.wikipedia.org/wiki/Cron) to launch scheduled runs. To explicitly set a timezone to the cron tab, apply a prefix in the cron tab: "CRON_TZ=${IANA_TIME_ZONE}" or "TZ=${IANA_TIME_ZONE}". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#cron GoogleVertexAiFeatureOnlineStoreFeatureview#cron}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2671b35151e94baa712a726d6b09d5e5585ce8c19c6f04cde59952810fb991d6)
            check_type(argname="argument cron", value=cron, expected_type=type_hints["cron"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cron is not None:
            self._values["cron"] = cron

    @builtins.property
    def cron(self) -> typing.Optional[builtins.str]:
        '''Cron schedule (https://en.wikipedia.org/wiki/Cron) to launch scheduled runs. To explicitly set a timezone to the cron tab, apply a prefix in the cron tab: "CRON_TZ=${IANA_TIME_ZONE}" or "TZ=${IANA_TIME_ZONE}".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#cron GoogleVertexAiFeatureOnlineStoreFeatureview#cron}
        '''
        result = self._values.get("cron")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiFeatureOnlineStoreFeatureviewSyncConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiFeatureOnlineStoreFeatureviewSyncConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeatureOnlineStoreFeatureview.GoogleVertexAiFeatureOnlineStoreFeatureviewSyncConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5170ddc4616edcd5aba68c0beb0086ea96eb3bdf043526aebe10b72135b8930)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCron")
    def reset_cron(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCron", []))

    @builtins.property
    @jsii.member(jsii_name="cronInput")
    def cron_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cronInput"))

    @builtins.property
    @jsii.member(jsii_name="cron")
    def cron(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cron"))

    @cron.setter
    def cron(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf83759966f841ea8168dfb494ad62b57ba2b844aaa424f7f6cdfae64c0cf978)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cron", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiFeatureOnlineStoreFeatureviewSyncConfig]:
        return typing.cast(typing.Optional[GoogleVertexAiFeatureOnlineStoreFeatureviewSyncConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiFeatureOnlineStoreFeatureviewSyncConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__881bc182dcbaadf8db1b760468f22ec196eec793d1cc8eb2e9bcf7bf36cb4b79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeatureOnlineStoreFeatureview.GoogleVertexAiFeatureOnlineStoreFeatureviewTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleVertexAiFeatureOnlineStoreFeatureviewTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#create GoogleVertexAiFeatureOnlineStoreFeatureview#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#delete GoogleVertexAiFeatureOnlineStoreFeatureview#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#update GoogleVertexAiFeatureOnlineStoreFeatureview#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76a7d34ff1969fb2de639dff425e36f1574ab919b544b5af720b63e051bf4d1b)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#create GoogleVertexAiFeatureOnlineStoreFeatureview#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#delete GoogleVertexAiFeatureOnlineStoreFeatureview#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#update GoogleVertexAiFeatureOnlineStoreFeatureview#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiFeatureOnlineStoreFeatureviewTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiFeatureOnlineStoreFeatureviewTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeatureOnlineStoreFeatureview.GoogleVertexAiFeatureOnlineStoreFeatureviewTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__65d2ec1356a3daba95cc042984a516d991e9c22c1e6f4b61fa493d5f70677830)
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
            type_hints = typing.get_type_hints(_typecheckingstub__36ad8dcf7cb4bc8914961e07fd495d3699e0b492d545c83a2061f161663d9edf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08dd34fc4b1151a0d8b84bd93f42bfa09e342e3efe390550ff30e2d14130ac1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8291f590189e87fd2b19b741daeaca635fb35a892d924d471f63c1055c3dce8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiFeatureOnlineStoreFeatureviewTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiFeatureOnlineStoreFeatureviewTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiFeatureOnlineStoreFeatureviewTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__536d73888f12cf4355d69dd45507bc5418aebe610bc20abfc86c92b9ff916972)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeatureOnlineStoreFeatureview.GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfig",
    jsii_struct_bases=[],
    name_mapping={
        "embedding_column": "embeddingColumn",
        "brute_force_config": "bruteForceConfig",
        "crowding_column": "crowdingColumn",
        "distance_measure_type": "distanceMeasureType",
        "embedding_dimension": "embeddingDimension",
        "filter_columns": "filterColumns",
        "tree_ah_config": "treeAhConfig",
    },
)
class GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfig:
    def __init__(
        self,
        *,
        embedding_column: builtins.str,
        brute_force_config: typing.Optional[typing.Union["GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigBruteForceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        crowding_column: typing.Optional[builtins.str] = None,
        distance_measure_type: typing.Optional[builtins.str] = None,
        embedding_dimension: typing.Optional[jsii.Number] = None,
        filter_columns: typing.Optional[typing.Sequence[builtins.str]] = None,
        tree_ah_config: typing.Optional[typing.Union["GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigTreeAhConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param embedding_column: Column of embedding. This column contains the source data to create index for vector search. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#embedding_column GoogleVertexAiFeatureOnlineStoreFeatureview#embedding_column}
        :param brute_force_config: brute_force_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#brute_force_config GoogleVertexAiFeatureOnlineStoreFeatureview#brute_force_config}
        :param crowding_column: Column of crowding. This column contains crowding attribute which is a constraint on a neighbor list produced by nearest neighbor search requiring that no more than some value k' of the k neighbors returned have the same value of crowdingAttribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#crowding_column GoogleVertexAiFeatureOnlineStoreFeatureview#crowding_column}
        :param distance_measure_type: The distance measure used in nearest neighbor search. For details on allowed values, see the `API documentation <https://cloud.google.com/vertex-ai/docs/reference/rest/v1beta1/projects.locations.featureOnlineStores.featureViews#DistanceMeasureType>`_. Possible values: ["SQUARED_L2_DISTANCE", "COSINE_DISTANCE", "DOT_PRODUCT_DISTANCE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#distance_measure_type GoogleVertexAiFeatureOnlineStoreFeatureview#distance_measure_type}
        :param embedding_dimension: The number of dimensions of the input embedding. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#embedding_dimension GoogleVertexAiFeatureOnlineStoreFeatureview#embedding_dimension}
        :param filter_columns: Columns of features that are used to filter vector search results. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#filter_columns GoogleVertexAiFeatureOnlineStoreFeatureview#filter_columns}
        :param tree_ah_config: tree_ah_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#tree_ah_config GoogleVertexAiFeatureOnlineStoreFeatureview#tree_ah_config}
        '''
        if isinstance(brute_force_config, dict):
            brute_force_config = GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigBruteForceConfig(**brute_force_config)
        if isinstance(tree_ah_config, dict):
            tree_ah_config = GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigTreeAhConfig(**tree_ah_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9df1e5504221b652560d6bd80908056fa34aa814ce445bd93a18f05373fcf816)
            check_type(argname="argument embedding_column", value=embedding_column, expected_type=type_hints["embedding_column"])
            check_type(argname="argument brute_force_config", value=brute_force_config, expected_type=type_hints["brute_force_config"])
            check_type(argname="argument crowding_column", value=crowding_column, expected_type=type_hints["crowding_column"])
            check_type(argname="argument distance_measure_type", value=distance_measure_type, expected_type=type_hints["distance_measure_type"])
            check_type(argname="argument embedding_dimension", value=embedding_dimension, expected_type=type_hints["embedding_dimension"])
            check_type(argname="argument filter_columns", value=filter_columns, expected_type=type_hints["filter_columns"])
            check_type(argname="argument tree_ah_config", value=tree_ah_config, expected_type=type_hints["tree_ah_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "embedding_column": embedding_column,
        }
        if brute_force_config is not None:
            self._values["brute_force_config"] = brute_force_config
        if crowding_column is not None:
            self._values["crowding_column"] = crowding_column
        if distance_measure_type is not None:
            self._values["distance_measure_type"] = distance_measure_type
        if embedding_dimension is not None:
            self._values["embedding_dimension"] = embedding_dimension
        if filter_columns is not None:
            self._values["filter_columns"] = filter_columns
        if tree_ah_config is not None:
            self._values["tree_ah_config"] = tree_ah_config

    @builtins.property
    def embedding_column(self) -> builtins.str:
        '''Column of embedding. This column contains the source data to create index for vector search.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#embedding_column GoogleVertexAiFeatureOnlineStoreFeatureview#embedding_column}
        '''
        result = self._values.get("embedding_column")
        assert result is not None, "Required property 'embedding_column' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def brute_force_config(
        self,
    ) -> typing.Optional["GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigBruteForceConfig"]:
        '''brute_force_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#brute_force_config GoogleVertexAiFeatureOnlineStoreFeatureview#brute_force_config}
        '''
        result = self._values.get("brute_force_config")
        return typing.cast(typing.Optional["GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigBruteForceConfig"], result)

    @builtins.property
    def crowding_column(self) -> typing.Optional[builtins.str]:
        '''Column of crowding.

        This column contains crowding attribute which is a constraint on a neighbor list produced by nearest neighbor search requiring that no more than some value k' of the k neighbors returned have the same value of crowdingAttribute.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#crowding_column GoogleVertexAiFeatureOnlineStoreFeatureview#crowding_column}
        '''
        result = self._values.get("crowding_column")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def distance_measure_type(self) -> typing.Optional[builtins.str]:
        '''The distance measure used in nearest neighbor search.

        For details on allowed values, see the `API documentation <https://cloud.google.com/vertex-ai/docs/reference/rest/v1beta1/projects.locations.featureOnlineStores.featureViews#DistanceMeasureType>`_. Possible values: ["SQUARED_L2_DISTANCE", "COSINE_DISTANCE", "DOT_PRODUCT_DISTANCE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#distance_measure_type GoogleVertexAiFeatureOnlineStoreFeatureview#distance_measure_type}
        '''
        result = self._values.get("distance_measure_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def embedding_dimension(self) -> typing.Optional[jsii.Number]:
        '''The number of dimensions of the input embedding.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#embedding_dimension GoogleVertexAiFeatureOnlineStoreFeatureview#embedding_dimension}
        '''
        result = self._values.get("embedding_dimension")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def filter_columns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Columns of features that are used to filter vector search results.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#filter_columns GoogleVertexAiFeatureOnlineStoreFeatureview#filter_columns}
        '''
        result = self._values.get("filter_columns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tree_ah_config(
        self,
    ) -> typing.Optional["GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigTreeAhConfig"]:
        '''tree_ah_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#tree_ah_config GoogleVertexAiFeatureOnlineStoreFeatureview#tree_ah_config}
        '''
        result = self._values.get("tree_ah_config")
        return typing.cast(typing.Optional["GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigTreeAhConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeatureOnlineStoreFeatureview.GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigBruteForceConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigBruteForceConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigBruteForceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigBruteForceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeatureOnlineStoreFeatureview.GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigBruteForceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3589c3baea2da293637b619b29a4dd64c2e0cc49466075c213be50f321a233e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigBruteForceConfig]:
        return typing.cast(typing.Optional[GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigBruteForceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigBruteForceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__376597c43863a9baa27b759d105de8b7fb1f6f7081cc16b9cd75b2fb64146178)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeatureOnlineStoreFeatureview.GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__17b7c7378112a591e5cc67cec0408acb151f42b3b98b56740f3febfb0fea857b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBruteForceConfig")
    def put_brute_force_config(self) -> None:
        value = GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigBruteForceConfig()

        return typing.cast(None, jsii.invoke(self, "putBruteForceConfig", [value]))

    @jsii.member(jsii_name="putTreeAhConfig")
    def put_tree_ah_config(
        self,
        *,
        leaf_node_embedding_count: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param leaf_node_embedding_count: Number of embeddings on each leaf node. The default value is 1000 if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#leaf_node_embedding_count GoogleVertexAiFeatureOnlineStoreFeatureview#leaf_node_embedding_count}
        '''
        value = GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigTreeAhConfig(
            leaf_node_embedding_count=leaf_node_embedding_count
        )

        return typing.cast(None, jsii.invoke(self, "putTreeAhConfig", [value]))

    @jsii.member(jsii_name="resetBruteForceConfig")
    def reset_brute_force_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBruteForceConfig", []))

    @jsii.member(jsii_name="resetCrowdingColumn")
    def reset_crowding_column(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrowdingColumn", []))

    @jsii.member(jsii_name="resetDistanceMeasureType")
    def reset_distance_measure_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDistanceMeasureType", []))

    @jsii.member(jsii_name="resetEmbeddingDimension")
    def reset_embedding_dimension(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmbeddingDimension", []))

    @jsii.member(jsii_name="resetFilterColumns")
    def reset_filter_columns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterColumns", []))

    @jsii.member(jsii_name="resetTreeAhConfig")
    def reset_tree_ah_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTreeAhConfig", []))

    @builtins.property
    @jsii.member(jsii_name="bruteForceConfig")
    def brute_force_config(
        self,
    ) -> GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigBruteForceConfigOutputReference:
        return typing.cast(GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigBruteForceConfigOutputReference, jsii.get(self, "bruteForceConfig"))

    @builtins.property
    @jsii.member(jsii_name="treeAhConfig")
    def tree_ah_config(
        self,
    ) -> "GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigTreeAhConfigOutputReference":
        return typing.cast("GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigTreeAhConfigOutputReference", jsii.get(self, "treeAhConfig"))

    @builtins.property
    @jsii.member(jsii_name="bruteForceConfigInput")
    def brute_force_config_input(
        self,
    ) -> typing.Optional[GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigBruteForceConfig]:
        return typing.cast(typing.Optional[GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigBruteForceConfig], jsii.get(self, "bruteForceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="crowdingColumnInput")
    def crowding_column_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "crowdingColumnInput"))

    @builtins.property
    @jsii.member(jsii_name="distanceMeasureTypeInput")
    def distance_measure_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "distanceMeasureTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="embeddingColumnInput")
    def embedding_column_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "embeddingColumnInput"))

    @builtins.property
    @jsii.member(jsii_name="embeddingDimensionInput")
    def embedding_dimension_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "embeddingDimensionInput"))

    @builtins.property
    @jsii.member(jsii_name="filterColumnsInput")
    def filter_columns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "filterColumnsInput"))

    @builtins.property
    @jsii.member(jsii_name="treeAhConfigInput")
    def tree_ah_config_input(
        self,
    ) -> typing.Optional["GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigTreeAhConfig"]:
        return typing.cast(typing.Optional["GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigTreeAhConfig"], jsii.get(self, "treeAhConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="crowdingColumn")
    def crowding_column(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "crowdingColumn"))

    @crowding_column.setter
    def crowding_column(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58460928cd4c35a143404ea40c5fe0e7954290bc6e5d0230cf2e4f28b06ed785)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crowdingColumn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="distanceMeasureType")
    def distance_measure_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "distanceMeasureType"))

    @distance_measure_type.setter
    def distance_measure_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f271f0f735b5f835f0b9ffa5f79b947a44b247903a0a3ddb55fe82d464eb4bd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "distanceMeasureType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="embeddingColumn")
    def embedding_column(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "embeddingColumn"))

    @embedding_column.setter
    def embedding_column(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83958b309ddf40d3c800688342c38242523fa776e1799cbdfe6b7d4d1764b7de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "embeddingColumn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="embeddingDimension")
    def embedding_dimension(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "embeddingDimension"))

    @embedding_dimension.setter
    def embedding_dimension(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dca039cb4beb84584145a5ba011c597ad5c06ffac05f2c0f53f2843a360e30cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "embeddingDimension", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filterColumns")
    def filter_columns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "filterColumns"))

    @filter_columns.setter
    def filter_columns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4959214756ab35b0bd5998ac162b606909764c68c7f7e1d75922d5e6a411eb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterColumns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfig]:
        return typing.cast(typing.Optional[GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e34b7eaf11ae0f63cde74f575e4ebef2009c56efdce10512d4aa064e97d7b42d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeatureOnlineStoreFeatureview.GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigTreeAhConfig",
    jsii_struct_bases=[],
    name_mapping={"leaf_node_embedding_count": "leafNodeEmbeddingCount"},
)
class GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigTreeAhConfig:
    def __init__(
        self,
        *,
        leaf_node_embedding_count: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param leaf_node_embedding_count: Number of embeddings on each leaf node. The default value is 1000 if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#leaf_node_embedding_count GoogleVertexAiFeatureOnlineStoreFeatureview#leaf_node_embedding_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0978a97a4780969a833cf2feac9d9564d87cc1c160bb0f0f532c0d3a155964dc)
            check_type(argname="argument leaf_node_embedding_count", value=leaf_node_embedding_count, expected_type=type_hints["leaf_node_embedding_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if leaf_node_embedding_count is not None:
            self._values["leaf_node_embedding_count"] = leaf_node_embedding_count

    @builtins.property
    def leaf_node_embedding_count(self) -> typing.Optional[builtins.str]:
        '''Number of embeddings on each leaf node. The default value is 1000 if not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store_featureview#leaf_node_embedding_count GoogleVertexAiFeatureOnlineStoreFeatureview#leaf_node_embedding_count}
        '''
        result = self._values.get("leaf_node_embedding_count")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigTreeAhConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigTreeAhConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeatureOnlineStoreFeatureview.GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigTreeAhConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d7425f0ecd180cd0143ff65f40cc087c8a5161d25f78a83929ff9e2233b5bc1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLeafNodeEmbeddingCount")
    def reset_leaf_node_embedding_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLeafNodeEmbeddingCount", []))

    @builtins.property
    @jsii.member(jsii_name="leafNodeEmbeddingCountInput")
    def leaf_node_embedding_count_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "leafNodeEmbeddingCountInput"))

    @builtins.property
    @jsii.member(jsii_name="leafNodeEmbeddingCount")
    def leaf_node_embedding_count(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "leafNodeEmbeddingCount"))

    @leaf_node_embedding_count.setter
    def leaf_node_embedding_count(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40b7fd2bec409cf4137c55a068c858a92e5f243090b341733f1b82af957e3572)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "leafNodeEmbeddingCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigTreeAhConfig]:
        return typing.cast(typing.Optional[GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigTreeAhConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigTreeAhConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59a7d7a35c1821279f714bd10ad6a967a53adb11ca615d6291377eded147abd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleVertexAiFeatureOnlineStoreFeatureview",
    "GoogleVertexAiFeatureOnlineStoreFeatureviewBigQuerySource",
    "GoogleVertexAiFeatureOnlineStoreFeatureviewBigQuerySourceOutputReference",
    "GoogleVertexAiFeatureOnlineStoreFeatureviewConfig",
    "GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySource",
    "GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups",
    "GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroupsList",
    "GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroupsOutputReference",
    "GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceOutputReference",
    "GoogleVertexAiFeatureOnlineStoreFeatureviewSyncConfig",
    "GoogleVertexAiFeatureOnlineStoreFeatureviewSyncConfigOutputReference",
    "GoogleVertexAiFeatureOnlineStoreFeatureviewTimeouts",
    "GoogleVertexAiFeatureOnlineStoreFeatureviewTimeoutsOutputReference",
    "GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfig",
    "GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigBruteForceConfig",
    "GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigBruteForceConfigOutputReference",
    "GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigOutputReference",
    "GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigTreeAhConfig",
    "GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigTreeAhConfigOutputReference",
]

publication.publish()

def _typecheckingstub__18384ef55b8963fe5e1663993536da6a86ac8e92e3661ae3c379e46432f227bf(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    feature_online_store: builtins.str,
    big_query_source: typing.Optional[typing.Union[GoogleVertexAiFeatureOnlineStoreFeatureviewBigQuerySource, typing.Dict[builtins.str, typing.Any]]] = None,
    feature_registry_source: typing.Optional[typing.Union[GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySource, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    sync_config: typing.Optional[typing.Union[GoogleVertexAiFeatureOnlineStoreFeatureviewSyncConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleVertexAiFeatureOnlineStoreFeatureviewTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    vector_search_config: typing.Optional[typing.Union[GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e85bd3e7cfe1f08ef5446a16680f4c08f65a7e3ef271240ccfa9a8c5e75e9d50(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__415e030426cd7768069730abec76295eb8b58f4facaf7175ec66f6020f39959d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2843084426a5342b5c3097d0b454d0486f8476dee7707e8db6ae501015cac5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1e3988ca7684db6bc2dd0833a108e726e8b31ce3567c347e26e6bd6c88f4089(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__341733b85047216bae965f0fbb48e5e4cd4e07cd7871ca6d033ae4fafa771bf9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d624ecce79f003318814d3d52f2b97e416aa75ce881a42105b20b346283a972b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c47d25119f4ec3cf09f3fe79dff7e7d9b1cac8373fa1764f196c45ac42658b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c9f8f7e10da98e222c330fceaaa6d0f2409fbaf486bf0512f2e7664d6ee7574(
    *,
    entity_id_columns: typing.Sequence[builtins.str],
    uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e76a2ee98b9bb6564f87906b902b8bf67759ea2df59ff5f39200597502b6b2bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__458dfdfaf81d661398b4158d00889381b3a836240d8f3cf775039581f11c9e0d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c153ae2463a0ecec947598c0d3d4cc5c87f9a72ad9ee638545042d1aa317b63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3fa9504cb181cfb2799adf7a5d89ffb77c1cb0c92f5453ec2f614f8e7bed781(
    value: typing.Optional[GoogleVertexAiFeatureOnlineStoreFeatureviewBigQuerySource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2771584a12631ac838047e05d25fc66f9c74a4930200caa57390b3d9523ccb6b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    feature_online_store: builtins.str,
    big_query_source: typing.Optional[typing.Union[GoogleVertexAiFeatureOnlineStoreFeatureviewBigQuerySource, typing.Dict[builtins.str, typing.Any]]] = None,
    feature_registry_source: typing.Optional[typing.Union[GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySource, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    sync_config: typing.Optional[typing.Union[GoogleVertexAiFeatureOnlineStoreFeatureviewSyncConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleVertexAiFeatureOnlineStoreFeatureviewTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    vector_search_config: typing.Optional[typing.Union[GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b89ee9848d297de866dde872beaa853657098e15399171236e0e3182d479aa5(
    *,
    feature_groups: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups, typing.Dict[builtins.str, typing.Any]]]],
    project_number: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__661556a5f0258a513e5f0cc100fab60491a105467764f3ad51f876cc2f205130(
    *,
    feature_group_id: builtins.str,
    feature_ids: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eddfbee0a1f8d56515596db20a807ffc0a0c2b6c80903283f05c71afeac12a0e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff19d46221c0a2812fc2db10e138965933f142921b844338bd9c976db4b0a4b5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__054d8e5fa95a9c0fe02fea7f426e50acac28a1862050b4201bebb4ae81db1359(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0479229f8969aa400d2f757d54f208379ae0960122306d957d6367e57d2e9767(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47df1ce9f7200e1d0beb03a67acaa42c9a628c07163a979d38ec294f910abe44(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8677f55718e0d991aa7846f87c87f7227a9cc06c5c936736b92ea45315065d7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__173a501a0b2563547a37f466ec8c3b376b6c0bf2ec3037124a348021821fc24f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16fa1b7a4ed5c0d79db59ff2179223892272c4d20a03a6f41ac2b95ca2012b87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68119c506e8690ff8c1ddc849e780b086dd25a483dd6979ae3e3ac9434623e4e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d444debffe177133dff849dbd8a5fd28d85b241119b75b0c89c804bea79d447a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__255da47835584e51a822e00d37c6c24c71d2a2ccb8438543775d697883942f31(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96eb58be46afec73b51dd333b2737926f299f63dec24fe71ffc21905b0799740(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3bddf82bde71243db7db153c87846fbbe87f8fc32ffb867033401c79354e645(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b28bf73b2cb86e094e3a498fe8fd43a9c95c00828e9b6627f1ae4851565b3027(
    value: typing.Optional[GoogleVertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2671b35151e94baa712a726d6b09d5e5585ce8c19c6f04cde59952810fb991d6(
    *,
    cron: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5170ddc4616edcd5aba68c0beb0086ea96eb3bdf043526aebe10b72135b8930(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf83759966f841ea8168dfb494ad62b57ba2b844aaa424f7f6cdfae64c0cf978(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__881bc182dcbaadf8db1b760468f22ec196eec793d1cc8eb2e9bcf7bf36cb4b79(
    value: typing.Optional[GoogleVertexAiFeatureOnlineStoreFeatureviewSyncConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76a7d34ff1969fb2de639dff425e36f1574ab919b544b5af720b63e051bf4d1b(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65d2ec1356a3daba95cc042984a516d991e9c22c1e6f4b61fa493d5f70677830(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36ad8dcf7cb4bc8914961e07fd495d3699e0b492d545c83a2061f161663d9edf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08dd34fc4b1151a0d8b84bd93f42bfa09e342e3efe390550ff30e2d14130ac1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8291f590189e87fd2b19b741daeaca635fb35a892d924d471f63c1055c3dce8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__536d73888f12cf4355d69dd45507bc5418aebe610bc20abfc86c92b9ff916972(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiFeatureOnlineStoreFeatureviewTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9df1e5504221b652560d6bd80908056fa34aa814ce445bd93a18f05373fcf816(
    *,
    embedding_column: builtins.str,
    brute_force_config: typing.Optional[typing.Union[GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigBruteForceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    crowding_column: typing.Optional[builtins.str] = None,
    distance_measure_type: typing.Optional[builtins.str] = None,
    embedding_dimension: typing.Optional[jsii.Number] = None,
    filter_columns: typing.Optional[typing.Sequence[builtins.str]] = None,
    tree_ah_config: typing.Optional[typing.Union[GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigTreeAhConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3589c3baea2da293637b619b29a4dd64c2e0cc49466075c213be50f321a233e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__376597c43863a9baa27b759d105de8b7fb1f6f7081cc16b9cd75b2fb64146178(
    value: typing.Optional[GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigBruteForceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17b7c7378112a591e5cc67cec0408acb151f42b3b98b56740f3febfb0fea857b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58460928cd4c35a143404ea40c5fe0e7954290bc6e5d0230cf2e4f28b06ed785(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f271f0f735b5f835f0b9ffa5f79b947a44b247903a0a3ddb55fe82d464eb4bd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83958b309ddf40d3c800688342c38242523fa776e1799cbdfe6b7d4d1764b7de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dca039cb4beb84584145a5ba011c597ad5c06ffac05f2c0f53f2843a360e30cc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4959214756ab35b0bd5998ac162b606909764c68c7f7e1d75922d5e6a411eb8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e34b7eaf11ae0f63cde74f575e4ebef2009c56efdce10512d4aa064e97d7b42d(
    value: typing.Optional[GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0978a97a4780969a833cf2feac9d9564d87cc1c160bb0f0f532c0d3a155964dc(
    *,
    leaf_node_embedding_count: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d7425f0ecd180cd0143ff65f40cc087c8a5161d25f78a83929ff9e2233b5bc1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40b7fd2bec409cf4137c55a068c858a92e5f243090b341733f1b82af957e3572(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59a7d7a35c1821279f714bd10ad6a967a53adb11ca615d6291377eded147abd8(
    value: typing.Optional[GoogleVertexAiFeatureOnlineStoreFeatureviewVectorSearchConfigTreeAhConfig],
) -> None:
    """Type checking stubs"""
    pass
