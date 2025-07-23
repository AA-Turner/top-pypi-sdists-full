r'''
# `google_vertex_ai_feature_online_store_featureview`

Refer to the Terraform Registry for docs: [`google_vertex_ai_feature_online_store_featureview`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview).
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


class VertexAiFeatureOnlineStoreFeatureview(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiFeatureOnlineStoreFeatureview.VertexAiFeatureOnlineStoreFeatureview",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview google_vertex_ai_feature_online_store_featureview}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        feature_online_store: builtins.str,
        big_query_source: typing.Optional[typing.Union["VertexAiFeatureOnlineStoreFeatureviewBigQuerySource", typing.Dict[builtins.str, typing.Any]]] = None,
        feature_registry_source: typing.Optional[typing.Union["VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySource", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        sync_config: typing.Optional[typing.Union["VertexAiFeatureOnlineStoreFeatureviewSyncConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["VertexAiFeatureOnlineStoreFeatureviewTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview google_vertex_ai_feature_online_store_featureview} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param feature_online_store: The name of the FeatureOnlineStore to use for the featureview. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#feature_online_store VertexAiFeatureOnlineStoreFeatureview#feature_online_store}
        :param big_query_source: big_query_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#big_query_source VertexAiFeatureOnlineStoreFeatureview#big_query_source}
        :param feature_registry_source: feature_registry_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#feature_registry_source VertexAiFeatureOnlineStoreFeatureview#feature_registry_source}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#id VertexAiFeatureOnlineStoreFeatureview#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: A set of key/value label pairs to assign to this FeatureView. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#labels VertexAiFeatureOnlineStoreFeatureview#labels}
        :param name: Name of the FeatureView. This value may be up to 60 characters, and valid characters are [a-z0-9_]. The first character cannot be a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#name VertexAiFeatureOnlineStoreFeatureview#name}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#project VertexAiFeatureOnlineStoreFeatureview#project}.
        :param region: The region for the resource. It should be the same as the featureonlinestore region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#region VertexAiFeatureOnlineStoreFeatureview#region}
        :param sync_config: sync_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#sync_config VertexAiFeatureOnlineStoreFeatureview#sync_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#timeouts VertexAiFeatureOnlineStoreFeatureview#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5d75bde2b6b8eb81e32d1afd6615bfaaf05d8285708800840d5e73936c491af)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VertexAiFeatureOnlineStoreFeatureviewConfig(
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
        '''Generates CDKTF code for importing a VertexAiFeatureOnlineStoreFeatureview resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VertexAiFeatureOnlineStoreFeatureview to import.
        :param import_from_id: The id of the existing VertexAiFeatureOnlineStoreFeatureview that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VertexAiFeatureOnlineStoreFeatureview to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cb23c2fe2dc327bb82680e8b78cabe51545c0870bdd1b9e0c861794837d2bff)
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
        :param entity_id_columns: Columns to construct entityId / row keys. Start by supporting 1 only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#entity_id_columns VertexAiFeatureOnlineStoreFeatureview#entity_id_columns}
        :param uri: The BigQuery view URI that will be materialized on each sync trigger based on FeatureView.SyncConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#uri VertexAiFeatureOnlineStoreFeatureview#uri}
        '''
        value = VertexAiFeatureOnlineStoreFeatureviewBigQuerySource(
            entity_id_columns=entity_id_columns, uri=uri
        )

        return typing.cast(None, jsii.invoke(self, "putBigQuerySource", [value]))

    @jsii.member(jsii_name="putFeatureRegistrySource")
    def put_feature_registry_source(
        self,
        *,
        feature_groups: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups", typing.Dict[builtins.str, typing.Any]]]],
        project_number: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param feature_groups: feature_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#feature_groups VertexAiFeatureOnlineStoreFeatureview#feature_groups}
        :param project_number: The project number of the parent project of the feature Groups. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#project_number VertexAiFeatureOnlineStoreFeatureview#project_number}
        '''
        value = VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySource(
            feature_groups=feature_groups, project_number=project_number
        )

        return typing.cast(None, jsii.invoke(self, "putFeatureRegistrySource", [value]))

    @jsii.member(jsii_name="putSyncConfig")
    def put_sync_config(self, *, cron: typing.Optional[builtins.str] = None) -> None:
        '''
        :param cron: Cron schedule (https://en.wikipedia.org/wiki/Cron) to launch scheduled runs. To explicitly set a timezone to the cron tab, apply a prefix in the cron tab: "CRON_TZ=${IANA_TIME_ZONE}" or "TZ=${IANA_TIME_ZONE}". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#cron VertexAiFeatureOnlineStoreFeatureview#cron}
        '''
        value = VertexAiFeatureOnlineStoreFeatureviewSyncConfig(cron=cron)

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#create VertexAiFeatureOnlineStoreFeatureview#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#delete VertexAiFeatureOnlineStoreFeatureview#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#update VertexAiFeatureOnlineStoreFeatureview#update}.
        '''
        value = VertexAiFeatureOnlineStoreFeatureviewTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

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
    ) -> "VertexAiFeatureOnlineStoreFeatureviewBigQuerySourceOutputReference":
        return typing.cast("VertexAiFeatureOnlineStoreFeatureviewBigQuerySourceOutputReference", jsii.get(self, "bigQuerySource"))

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
    ) -> "VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceOutputReference":
        return typing.cast("VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceOutputReference", jsii.get(self, "featureRegistrySource"))

    @builtins.property
    @jsii.member(jsii_name="syncConfig")
    def sync_config(
        self,
    ) -> "VertexAiFeatureOnlineStoreFeatureviewSyncConfigOutputReference":
        return typing.cast("VertexAiFeatureOnlineStoreFeatureviewSyncConfigOutputReference", jsii.get(self, "syncConfig"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "VertexAiFeatureOnlineStoreFeatureviewTimeoutsOutputReference":
        return typing.cast("VertexAiFeatureOnlineStoreFeatureviewTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="bigQuerySourceInput")
    def big_query_source_input(
        self,
    ) -> typing.Optional["VertexAiFeatureOnlineStoreFeatureviewBigQuerySource"]:
        return typing.cast(typing.Optional["VertexAiFeatureOnlineStoreFeatureviewBigQuerySource"], jsii.get(self, "bigQuerySourceInput"))

    @builtins.property
    @jsii.member(jsii_name="featureOnlineStoreInput")
    def feature_online_store_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "featureOnlineStoreInput"))

    @builtins.property
    @jsii.member(jsii_name="featureRegistrySourceInput")
    def feature_registry_source_input(
        self,
    ) -> typing.Optional["VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySource"]:
        return typing.cast(typing.Optional["VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySource"], jsii.get(self, "featureRegistrySourceInput"))

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
    ) -> typing.Optional["VertexAiFeatureOnlineStoreFeatureviewSyncConfig"]:
        return typing.cast(typing.Optional["VertexAiFeatureOnlineStoreFeatureviewSyncConfig"], jsii.get(self, "syncConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VertexAiFeatureOnlineStoreFeatureviewTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VertexAiFeatureOnlineStoreFeatureviewTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="featureOnlineStore")
    def feature_online_store(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "featureOnlineStore"))

    @feature_online_store.setter
    def feature_online_store(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d1334daf6bec856172af5e94d420bbd3181e6fa9ecb4ccfe7b824f9d4a3d4aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "featureOnlineStore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1de18896d6bf7bd23904803afadc7128f8d89070bed6e263d5ce3682a5b615bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb47a7aa7aae1fa448604493c863512f44ea2972d167aa05330f5abaa8390d4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd160f5a5829e936b40901ce89fdf4b96766234006c2558129d6d27e1896a9ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c35fd63bea9927ee33361613017915decc88b637dd39f3be0b8b7a9fdda23930)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48118afa4abb59c3ff268bfc661033a97838ce35180bc75001fc63d49350c2b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiFeatureOnlineStoreFeatureview.VertexAiFeatureOnlineStoreFeatureviewBigQuerySource",
    jsii_struct_bases=[],
    name_mapping={"entity_id_columns": "entityIdColumns", "uri": "uri"},
)
class VertexAiFeatureOnlineStoreFeatureviewBigQuerySource:
    def __init__(
        self,
        *,
        entity_id_columns: typing.Sequence[builtins.str],
        uri: builtins.str,
    ) -> None:
        '''
        :param entity_id_columns: Columns to construct entityId / row keys. Start by supporting 1 only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#entity_id_columns VertexAiFeatureOnlineStoreFeatureview#entity_id_columns}
        :param uri: The BigQuery view URI that will be materialized on each sync trigger based on FeatureView.SyncConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#uri VertexAiFeatureOnlineStoreFeatureview#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c2708e0d2a0b0033eddfca405772819fdb20c094ae06c611bc045ad79f7db3f)
            check_type(argname="argument entity_id_columns", value=entity_id_columns, expected_type=type_hints["entity_id_columns"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "entity_id_columns": entity_id_columns,
            "uri": uri,
        }

    @builtins.property
    def entity_id_columns(self) -> typing.List[builtins.str]:
        '''Columns to construct entityId / row keys. Start by supporting 1 only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#entity_id_columns VertexAiFeatureOnlineStoreFeatureview#entity_id_columns}
        '''
        result = self._values.get("entity_id_columns")
        assert result is not None, "Required property 'entity_id_columns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def uri(self) -> builtins.str:
        '''The BigQuery view URI that will be materialized on each sync trigger based on FeatureView.SyncConfig.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#uri VertexAiFeatureOnlineStoreFeatureview#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiFeatureOnlineStoreFeatureviewBigQuerySource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiFeatureOnlineStoreFeatureviewBigQuerySourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiFeatureOnlineStoreFeatureview.VertexAiFeatureOnlineStoreFeatureviewBigQuerySourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e2ebeba2dba28cebe605faece429394891b72016664145e6d5aa94203f34122)
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
            type_hints = typing.get_type_hints(_typecheckingstub__71f5b1cfdb8dea9f1d98e4d377102dbff8a812f4c9f3a194834cbc96a922c77e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entityIdColumns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43fa74627bc03969b5fef6aef3082e467811a66364849d2b3023089cd3a6908b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiFeatureOnlineStoreFeatureviewBigQuerySource]:
        return typing.cast(typing.Optional[VertexAiFeatureOnlineStoreFeatureviewBigQuerySource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiFeatureOnlineStoreFeatureviewBigQuerySource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__351db6976037b8d901b50b9b2fa328379dfeb95193366abdf8672da04bc05bb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiFeatureOnlineStoreFeatureview.VertexAiFeatureOnlineStoreFeatureviewConfig",
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
    },
)
class VertexAiFeatureOnlineStoreFeatureviewConfig(
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
        big_query_source: typing.Optional[typing.Union[VertexAiFeatureOnlineStoreFeatureviewBigQuerySource, typing.Dict[builtins.str, typing.Any]]] = None,
        feature_registry_source: typing.Optional[typing.Union["VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySource", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        sync_config: typing.Optional[typing.Union["VertexAiFeatureOnlineStoreFeatureviewSyncConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["VertexAiFeatureOnlineStoreFeatureviewTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param feature_online_store: The name of the FeatureOnlineStore to use for the featureview. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#feature_online_store VertexAiFeatureOnlineStoreFeatureview#feature_online_store}
        :param big_query_source: big_query_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#big_query_source VertexAiFeatureOnlineStoreFeatureview#big_query_source}
        :param feature_registry_source: feature_registry_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#feature_registry_source VertexAiFeatureOnlineStoreFeatureview#feature_registry_source}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#id VertexAiFeatureOnlineStoreFeatureview#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: A set of key/value label pairs to assign to this FeatureView. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#labels VertexAiFeatureOnlineStoreFeatureview#labels}
        :param name: Name of the FeatureView. This value may be up to 60 characters, and valid characters are [a-z0-9_]. The first character cannot be a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#name VertexAiFeatureOnlineStoreFeatureview#name}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#project VertexAiFeatureOnlineStoreFeatureview#project}.
        :param region: The region for the resource. It should be the same as the featureonlinestore region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#region VertexAiFeatureOnlineStoreFeatureview#region}
        :param sync_config: sync_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#sync_config VertexAiFeatureOnlineStoreFeatureview#sync_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#timeouts VertexAiFeatureOnlineStoreFeatureview#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(big_query_source, dict):
            big_query_source = VertexAiFeatureOnlineStoreFeatureviewBigQuerySource(**big_query_source)
        if isinstance(feature_registry_source, dict):
            feature_registry_source = VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySource(**feature_registry_source)
        if isinstance(sync_config, dict):
            sync_config = VertexAiFeatureOnlineStoreFeatureviewSyncConfig(**sync_config)
        if isinstance(timeouts, dict):
            timeouts = VertexAiFeatureOnlineStoreFeatureviewTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6f53f720df0cd74d8f73770872bc7757f9246ff2a6b56449ec8b1d987cf21da)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#feature_online_store VertexAiFeatureOnlineStoreFeatureview#feature_online_store}
        '''
        result = self._values.get("feature_online_store")
        assert result is not None, "Required property 'feature_online_store' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def big_query_source(
        self,
    ) -> typing.Optional[VertexAiFeatureOnlineStoreFeatureviewBigQuerySource]:
        '''big_query_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#big_query_source VertexAiFeatureOnlineStoreFeatureview#big_query_source}
        '''
        result = self._values.get("big_query_source")
        return typing.cast(typing.Optional[VertexAiFeatureOnlineStoreFeatureviewBigQuerySource], result)

    @builtins.property
    def feature_registry_source(
        self,
    ) -> typing.Optional["VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySource"]:
        '''feature_registry_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#feature_registry_source VertexAiFeatureOnlineStoreFeatureview#feature_registry_source}
        '''
        result = self._values.get("feature_registry_source")
        return typing.cast(typing.Optional["VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySource"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#id VertexAiFeatureOnlineStoreFeatureview#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#labels VertexAiFeatureOnlineStoreFeatureview#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the FeatureView.

        This value may be up to 60 characters, and valid characters are [a-z0-9_]. The first character cannot be a number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#name VertexAiFeatureOnlineStoreFeatureview#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#project VertexAiFeatureOnlineStoreFeatureview#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region for the resource. It should be the same as the featureonlinestore region.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#region VertexAiFeatureOnlineStoreFeatureview#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_config(
        self,
    ) -> typing.Optional["VertexAiFeatureOnlineStoreFeatureviewSyncConfig"]:
        '''sync_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#sync_config VertexAiFeatureOnlineStoreFeatureview#sync_config}
        '''
        result = self._values.get("sync_config")
        return typing.cast(typing.Optional["VertexAiFeatureOnlineStoreFeatureviewSyncConfig"], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["VertexAiFeatureOnlineStoreFeatureviewTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#timeouts VertexAiFeatureOnlineStoreFeatureview#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["VertexAiFeatureOnlineStoreFeatureviewTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiFeatureOnlineStoreFeatureviewConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiFeatureOnlineStoreFeatureview.VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySource",
    jsii_struct_bases=[],
    name_mapping={
        "feature_groups": "featureGroups",
        "project_number": "projectNumber",
    },
)
class VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySource:
    def __init__(
        self,
        *,
        feature_groups: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups", typing.Dict[builtins.str, typing.Any]]]],
        project_number: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param feature_groups: feature_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#feature_groups VertexAiFeatureOnlineStoreFeatureview#feature_groups}
        :param project_number: The project number of the parent project of the feature Groups. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#project_number VertexAiFeatureOnlineStoreFeatureview#project_number}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__494c0f1bd08d79366002235b1f30172737330ada6749b066e4f8541582269ca3)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups"]]:
        '''feature_groups block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#feature_groups VertexAiFeatureOnlineStoreFeatureview#feature_groups}
        '''
        result = self._values.get("feature_groups")
        assert result is not None, "Required property 'feature_groups' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups"]], result)

    @builtins.property
    def project_number(self) -> typing.Optional[builtins.str]:
        '''The project number of the parent project of the feature Groups.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#project_number VertexAiFeatureOnlineStoreFeatureview#project_number}
        '''
        result = self._values.get("project_number")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiFeatureOnlineStoreFeatureview.VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups",
    jsii_struct_bases=[],
    name_mapping={"feature_group_id": "featureGroupId", "feature_ids": "featureIds"},
)
class VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups:
    def __init__(
        self,
        *,
        feature_group_id: builtins.str,
        feature_ids: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param feature_group_id: Identifier of the feature group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#feature_group_id VertexAiFeatureOnlineStoreFeatureview#feature_group_id}
        :param feature_ids: Identifiers of features under the feature group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#feature_ids VertexAiFeatureOnlineStoreFeatureview#feature_ids}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17d01ca7a836fbe7dc3952040e0ecb9ba731718cf8e91d02a3f114d9804c0df5)
            check_type(argname="argument feature_group_id", value=feature_group_id, expected_type=type_hints["feature_group_id"])
            check_type(argname="argument feature_ids", value=feature_ids, expected_type=type_hints["feature_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "feature_group_id": feature_group_id,
            "feature_ids": feature_ids,
        }

    @builtins.property
    def feature_group_id(self) -> builtins.str:
        '''Identifier of the feature group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#feature_group_id VertexAiFeatureOnlineStoreFeatureview#feature_group_id}
        '''
        result = self._values.get("feature_group_id")
        assert result is not None, "Required property 'feature_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def feature_ids(self) -> typing.List[builtins.str]:
        '''Identifiers of features under the feature group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#feature_ids VertexAiFeatureOnlineStoreFeatureview#feature_ids}
        '''
        result = self._values.get("feature_ids")
        assert result is not None, "Required property 'feature_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroupsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiFeatureOnlineStoreFeatureview.VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroupsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7f15dc0d8245d86e38122f782e4da390063d99faca631ba505946a5acdae9ad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroupsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5320c3d783c37171c4f43eee9b6a32a49b282ec462bd79419999104ed1da7e99)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroupsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__690123fe4f9083233a08a1570dd6ae3fdc0c575399b82a958d2f5c880f33f6bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fae8dee314ccc7b2a1523d8e0206a6890fb65defbe9d07cea5048221a08721a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d27e720c60d6ad6ffba207bbc74a38a3d26de61183048bbdf3a8c16c5aa87651)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a4f0cca1dd5c600036b86622d36225ed70252a0ce86ce5c4f0a96a57eda6b24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroupsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiFeatureOnlineStoreFeatureview.VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroupsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__53587917d95525da7fe05d26a5b63fca4e6265540a75e429e07451dcad818597)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d01d04bb6b473772a2a85c748e465131b026b0f61cee6bfb19223e04e1dfe04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "featureGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="featureIds")
    def feature_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "featureIds"))

    @feature_ids.setter
    def feature_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2735e35400d749fa43a6e7831905513760e4883be57c8114187e5e40470016cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "featureIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a018cd6099e8f6ccb3ed83fa555f77b62dccfe8b6ef66309e79b4e3a17ab6b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiFeatureOnlineStoreFeatureview.VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b23e5e198b4dd3466f378e875f775ef40808fae2c54ac49b13abd9c5a60fb786)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFeatureGroups")
    def put_feature_groups(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b09946f9c06ec6b8da41c9b275d3924b549905aaba3d6e4e2fd44378a5f50d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFeatureGroups", [value]))

    @jsii.member(jsii_name="resetProjectNumber")
    def reset_project_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectNumber", []))

    @builtins.property
    @jsii.member(jsii_name="featureGroups")
    def feature_groups(
        self,
    ) -> VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroupsList:
        return typing.cast(VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroupsList, jsii.get(self, "featureGroups"))

    @builtins.property
    @jsii.member(jsii_name="featureGroupsInput")
    def feature_groups_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups]]], jsii.get(self, "featureGroupsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__12eff6388fd5ac9a8fb99681bd377df81df363d057b91cdbdbf264d3529e9efa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySource]:
        return typing.cast(typing.Optional[VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5402e27e42a11a6836b7f79c800ef6cdadd17dbbebfb9d196605426b6fdf93d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiFeatureOnlineStoreFeatureview.VertexAiFeatureOnlineStoreFeatureviewSyncConfig",
    jsii_struct_bases=[],
    name_mapping={"cron": "cron"},
)
class VertexAiFeatureOnlineStoreFeatureviewSyncConfig:
    def __init__(self, *, cron: typing.Optional[builtins.str] = None) -> None:
        '''
        :param cron: Cron schedule (https://en.wikipedia.org/wiki/Cron) to launch scheduled runs. To explicitly set a timezone to the cron tab, apply a prefix in the cron tab: "CRON_TZ=${IANA_TIME_ZONE}" or "TZ=${IANA_TIME_ZONE}". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#cron VertexAiFeatureOnlineStoreFeatureview#cron}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25676f7a243a7ee3816357586bbeffb86aa0e07b55ef70ed3c1a9e2ef0795d52)
            check_type(argname="argument cron", value=cron, expected_type=type_hints["cron"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cron is not None:
            self._values["cron"] = cron

    @builtins.property
    def cron(self) -> typing.Optional[builtins.str]:
        '''Cron schedule (https://en.wikipedia.org/wiki/Cron) to launch scheduled runs. To explicitly set a timezone to the cron tab, apply a prefix in the cron tab: "CRON_TZ=${IANA_TIME_ZONE}" or "TZ=${IANA_TIME_ZONE}".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#cron VertexAiFeatureOnlineStoreFeatureview#cron}
        '''
        result = self._values.get("cron")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiFeatureOnlineStoreFeatureviewSyncConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiFeatureOnlineStoreFeatureviewSyncConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiFeatureOnlineStoreFeatureview.VertexAiFeatureOnlineStoreFeatureviewSyncConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f056d23e802062d0a07f1f331e6f49d05b577ecf7a72043116ba9992fc0a323)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4aba912f9afb2980fea551fda499fda2b51ffd3a9a831b15554145e8d2867b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cron", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiFeatureOnlineStoreFeatureviewSyncConfig]:
        return typing.cast(typing.Optional[VertexAiFeatureOnlineStoreFeatureviewSyncConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiFeatureOnlineStoreFeatureviewSyncConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__494c59770722afdb6b65c114e557920d54c27bbe1a58e3365e32aa4231eba379)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiFeatureOnlineStoreFeatureview.VertexAiFeatureOnlineStoreFeatureviewTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class VertexAiFeatureOnlineStoreFeatureviewTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#create VertexAiFeatureOnlineStoreFeatureview#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#delete VertexAiFeatureOnlineStoreFeatureview#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#update VertexAiFeatureOnlineStoreFeatureview#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b71c204bea8254fdd64a1ebebd8941d472e08ba22066b1082dd265c2d4bd473)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#create VertexAiFeatureOnlineStoreFeatureview#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#delete VertexAiFeatureOnlineStoreFeatureview#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store_featureview#update VertexAiFeatureOnlineStoreFeatureview#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiFeatureOnlineStoreFeatureviewTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiFeatureOnlineStoreFeatureviewTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiFeatureOnlineStoreFeatureview.VertexAiFeatureOnlineStoreFeatureviewTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b11ddb17c0c645bb304b5d4a0d78bb594d273297348120b0b4b2234471a09f7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__47e738a7517918e32a20b04e236357f76697a1bd33d231e6e2bc7a7a3b035091)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b422ec1bc622797503f4617aab67ea3e719e1138435cca3a99065435a443b943)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41dd84e7a9bbf9187b4f95772012c008fba5e99bd41bc8c256f2efc54c97e5be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiFeatureOnlineStoreFeatureviewTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiFeatureOnlineStoreFeatureviewTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiFeatureOnlineStoreFeatureviewTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__452058adf4b11db0d3ce7f4eeb8a4e9448fb372bd010a2fb5a27741df73e7f91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "VertexAiFeatureOnlineStoreFeatureview",
    "VertexAiFeatureOnlineStoreFeatureviewBigQuerySource",
    "VertexAiFeatureOnlineStoreFeatureviewBigQuerySourceOutputReference",
    "VertexAiFeatureOnlineStoreFeatureviewConfig",
    "VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySource",
    "VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups",
    "VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroupsList",
    "VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroupsOutputReference",
    "VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceOutputReference",
    "VertexAiFeatureOnlineStoreFeatureviewSyncConfig",
    "VertexAiFeatureOnlineStoreFeatureviewSyncConfigOutputReference",
    "VertexAiFeatureOnlineStoreFeatureviewTimeouts",
    "VertexAiFeatureOnlineStoreFeatureviewTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__d5d75bde2b6b8eb81e32d1afd6615bfaaf05d8285708800840d5e73936c491af(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    feature_online_store: builtins.str,
    big_query_source: typing.Optional[typing.Union[VertexAiFeatureOnlineStoreFeatureviewBigQuerySource, typing.Dict[builtins.str, typing.Any]]] = None,
    feature_registry_source: typing.Optional[typing.Union[VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySource, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    sync_config: typing.Optional[typing.Union[VertexAiFeatureOnlineStoreFeatureviewSyncConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[VertexAiFeatureOnlineStoreFeatureviewTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__4cb23c2fe2dc327bb82680e8b78cabe51545c0870bdd1b9e0c861794837d2bff(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d1334daf6bec856172af5e94d420bbd3181e6fa9ecb4ccfe7b824f9d4a3d4aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1de18896d6bf7bd23904803afadc7128f8d89070bed6e263d5ce3682a5b615bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb47a7aa7aae1fa448604493c863512f44ea2972d167aa05330f5abaa8390d4e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd160f5a5829e936b40901ce89fdf4b96766234006c2558129d6d27e1896a9ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c35fd63bea9927ee33361613017915decc88b637dd39f3be0b8b7a9fdda23930(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48118afa4abb59c3ff268bfc661033a97838ce35180bc75001fc63d49350c2b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c2708e0d2a0b0033eddfca405772819fdb20c094ae06c611bc045ad79f7db3f(
    *,
    entity_id_columns: typing.Sequence[builtins.str],
    uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e2ebeba2dba28cebe605faece429394891b72016664145e6d5aa94203f34122(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71f5b1cfdb8dea9f1d98e4d377102dbff8a812f4c9f3a194834cbc96a922c77e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43fa74627bc03969b5fef6aef3082e467811a66364849d2b3023089cd3a6908b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__351db6976037b8d901b50b9b2fa328379dfeb95193366abdf8672da04bc05bb3(
    value: typing.Optional[VertexAiFeatureOnlineStoreFeatureviewBigQuerySource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6f53f720df0cd74d8f73770872bc7757f9246ff2a6b56449ec8b1d987cf21da(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    feature_online_store: builtins.str,
    big_query_source: typing.Optional[typing.Union[VertexAiFeatureOnlineStoreFeatureviewBigQuerySource, typing.Dict[builtins.str, typing.Any]]] = None,
    feature_registry_source: typing.Optional[typing.Union[VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySource, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    sync_config: typing.Optional[typing.Union[VertexAiFeatureOnlineStoreFeatureviewSyncConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[VertexAiFeatureOnlineStoreFeatureviewTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__494c0f1bd08d79366002235b1f30172737330ada6749b066e4f8541582269ca3(
    *,
    feature_groups: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups, typing.Dict[builtins.str, typing.Any]]]],
    project_number: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17d01ca7a836fbe7dc3952040e0ecb9ba731718cf8e91d02a3f114d9804c0df5(
    *,
    feature_group_id: builtins.str,
    feature_ids: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7f15dc0d8245d86e38122f782e4da390063d99faca631ba505946a5acdae9ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5320c3d783c37171c4f43eee9b6a32a49b282ec462bd79419999104ed1da7e99(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__690123fe4f9083233a08a1570dd6ae3fdc0c575399b82a958d2f5c880f33f6bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fae8dee314ccc7b2a1523d8e0206a6890fb65defbe9d07cea5048221a08721a5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d27e720c60d6ad6ffba207bbc74a38a3d26de61183048bbdf3a8c16c5aa87651(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a4f0cca1dd5c600036b86622d36225ed70252a0ce86ce5c4f0a96a57eda6b24(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53587917d95525da7fe05d26a5b63fca4e6265540a75e429e07451dcad818597(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d01d04bb6b473772a2a85c748e465131b026b0f61cee6bfb19223e04e1dfe04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2735e35400d749fa43a6e7831905513760e4883be57c8114187e5e40470016cf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a018cd6099e8f6ccb3ed83fa555f77b62dccfe8b6ef66309e79b4e3a17ab6b8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b23e5e198b4dd3466f378e875f775ef40808fae2c54ac49b13abd9c5a60fb786(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b09946f9c06ec6b8da41c9b275d3924b549905aaba3d6e4e2fd44378a5f50d6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySourceFeatureGroups, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12eff6388fd5ac9a8fb99681bd377df81df363d057b91cdbdbf264d3529e9efa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5402e27e42a11a6836b7f79c800ef6cdadd17dbbebfb9d196605426b6fdf93d7(
    value: typing.Optional[VertexAiFeatureOnlineStoreFeatureviewFeatureRegistrySource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25676f7a243a7ee3816357586bbeffb86aa0e07b55ef70ed3c1a9e2ef0795d52(
    *,
    cron: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f056d23e802062d0a07f1f331e6f49d05b577ecf7a72043116ba9992fc0a323(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4aba912f9afb2980fea551fda499fda2b51ffd3a9a831b15554145e8d2867b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__494c59770722afdb6b65c114e557920d54c27bbe1a58e3365e32aa4231eba379(
    value: typing.Optional[VertexAiFeatureOnlineStoreFeatureviewSyncConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b71c204bea8254fdd64a1ebebd8941d472e08ba22066b1082dd265c2d4bd473(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b11ddb17c0c645bb304b5d4a0d78bb594d273297348120b0b4b2234471a09f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47e738a7517918e32a20b04e236357f76697a1bd33d231e6e2bc7a7a3b035091(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b422ec1bc622797503f4617aab67ea3e719e1138435cca3a99065435a443b943(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41dd84e7a9bbf9187b4f95772012c008fba5e99bd41bc8c256f2efc54c97e5be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__452058adf4b11db0d3ce7f4eeb8a4e9448fb372bd010a2fb5a27741df73e7f91(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiFeatureOnlineStoreFeatureviewTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
