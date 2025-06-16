r'''
# `google_vertex_ai_featurestore_entitytype`

Refer to the Terraform Registry for docs: [`google_vertex_ai_featurestore_entitytype`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype).
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


class GoogleVertexAiFeaturestoreEntitytype(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeaturestoreEntitytype.GoogleVertexAiFeaturestoreEntitytype",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype google_vertex_ai_featurestore_entitytype}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        featurestore: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        monitoring_config: typing.Optional[typing.Union["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        offline_storage_ttl_days: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["GoogleVertexAiFeaturestoreEntitytypeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype google_vertex_ai_featurestore_entitytype} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param featurestore: The name of the Featurestore to use, in the format projects/{project}/locations/{location}/featurestores/{featurestore}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#featurestore GoogleVertexAiFeaturestoreEntitytype#featurestore}
        :param description: Optional. Description of the EntityType. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#description GoogleVertexAiFeaturestoreEntitytype#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#id GoogleVertexAiFeaturestoreEntitytype#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: A set of key/value label pairs to assign to this EntityType. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#labels GoogleVertexAiFeaturestoreEntitytype#labels}
        :param monitoring_config: monitoring_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#monitoring_config GoogleVertexAiFeaturestoreEntitytype#monitoring_config}
        :param name: The name of the EntityType. This value may be up to 60 characters, and valid characters are [a-z0-9_]. The first character cannot be a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#name GoogleVertexAiFeaturestoreEntitytype#name}
        :param offline_storage_ttl_days: Config for data retention policy in offline storage. TTL in days for feature values that will be stored in offline storage. The Feature Store offline storage periodically removes obsolete feature values older than offlineStorageTtlDays since the feature generation time. If unset (or explicitly set to 0), default to 4000 days TTL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#offline_storage_ttl_days GoogleVertexAiFeaturestoreEntitytype#offline_storage_ttl_days}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#timeouts GoogleVertexAiFeaturestoreEntitytype#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4b70139098610c17e11047a17c9cfaf2cd7aa5353326848c98a16fd5ebeeb3c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleVertexAiFeaturestoreEntitytypeConfig(
            featurestore=featurestore,
            description=description,
            id=id,
            labels=labels,
            monitoring_config=monitoring_config,
            name=name,
            offline_storage_ttl_days=offline_storage_ttl_days,
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
        '''Generates CDKTF code for importing a GoogleVertexAiFeaturestoreEntitytype resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleVertexAiFeaturestoreEntitytype to import.
        :param import_from_id: The id of the existing GoogleVertexAiFeaturestoreEntitytype that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleVertexAiFeaturestoreEntitytype to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1beda63207f22e8a64645399006ba3d42f2314912d8c1ab993211adeafd9973)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putMonitoringConfig")
    def put_monitoring_config(
        self,
        *,
        categorical_threshold_config: typing.Optional[typing.Union["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        import_features_analysis: typing.Optional[typing.Union["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis", typing.Dict[builtins.str, typing.Any]]] = None,
        numerical_threshold_config: typing.Optional[typing.Union["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        snapshot_analysis: typing.Optional[typing.Union["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param categorical_threshold_config: categorical_threshold_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#categorical_threshold_config GoogleVertexAiFeaturestoreEntitytype#categorical_threshold_config}
        :param import_features_analysis: import_features_analysis block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#import_features_analysis GoogleVertexAiFeaturestoreEntitytype#import_features_analysis}
        :param numerical_threshold_config: numerical_threshold_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#numerical_threshold_config GoogleVertexAiFeaturestoreEntitytype#numerical_threshold_config}
        :param snapshot_analysis: snapshot_analysis block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#snapshot_analysis GoogleVertexAiFeaturestoreEntitytype#snapshot_analysis}
        '''
        value = GoogleVertexAiFeaturestoreEntitytypeMonitoringConfig(
            categorical_threshold_config=categorical_threshold_config,
            import_features_analysis=import_features_analysis,
            numerical_threshold_config=numerical_threshold_config,
            snapshot_analysis=snapshot_analysis,
        )

        return typing.cast(None, jsii.invoke(self, "putMonitoringConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#create GoogleVertexAiFeaturestoreEntitytype#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#delete GoogleVertexAiFeaturestoreEntitytype#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#update GoogleVertexAiFeaturestoreEntitytype#update}.
        '''
        value = GoogleVertexAiFeaturestoreEntitytypeTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMonitoringConfig")
    def reset_monitoring_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitoringConfig", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetOfflineStorageTtlDays")
    def reset_offline_storage_ttl_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOfflineStorageTtlDays", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="monitoringConfig")
    def monitoring_config(
        self,
    ) -> "GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigOutputReference":
        return typing.cast("GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigOutputReference", jsii.get(self, "monitoringConfig"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleVertexAiFeaturestoreEntitytypeTimeoutsOutputReference":
        return typing.cast("GoogleVertexAiFeaturestoreEntitytypeTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="featurestoreInput")
    def featurestore_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "featurestoreInput"))

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
    @jsii.member(jsii_name="monitoringConfigInput")
    def monitoring_config_input(
        self,
    ) -> typing.Optional["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfig"]:
        return typing.cast(typing.Optional["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfig"], jsii.get(self, "monitoringConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="offlineStorageTtlDaysInput")
    def offline_storage_ttl_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "offlineStorageTtlDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleVertexAiFeaturestoreEntitytypeTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleVertexAiFeaturestoreEntitytypeTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eab28c2bc6a17e6d38ae87597dd8b7f155a86acd18e049d3721fdcee25cf6dd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="featurestore")
    def featurestore(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "featurestore"))

    @featurestore.setter
    def featurestore(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c44855fd21fbc6ca6170e1ee384fcde9809720b545af4523281ca0efdc0bcbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "featurestore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b08247b0d323078d62ef602c924890e0203eeb0df55c257a90c7dd1a94e2567)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__181743b6afadc118c2faa8bad8b3d04fd64fa0a55d12dff3b194528a9b34cdc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb775115645b95162cbe48853f55426e4c49330c2ae263763b11eaa8a03d7144)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="offlineStorageTtlDays")
    def offline_storage_ttl_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "offlineStorageTtlDays"))

    @offline_storage_ttl_days.setter
    def offline_storage_ttl_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93ba38cb47d6f90b8b2bbd4ba01f461da0f190e13f4a34939185c84b55b7ccd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "offlineStorageTtlDays", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeaturestoreEntitytype.GoogleVertexAiFeaturestoreEntitytypeConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "featurestore": "featurestore",
        "description": "description",
        "id": "id",
        "labels": "labels",
        "monitoring_config": "monitoringConfig",
        "name": "name",
        "offline_storage_ttl_days": "offlineStorageTtlDays",
        "timeouts": "timeouts",
    },
)
class GoogleVertexAiFeaturestoreEntitytypeConfig(
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
        featurestore: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        monitoring_config: typing.Optional[typing.Union["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        offline_storage_ttl_days: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["GoogleVertexAiFeaturestoreEntitytypeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param featurestore: The name of the Featurestore to use, in the format projects/{project}/locations/{location}/featurestores/{featurestore}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#featurestore GoogleVertexAiFeaturestoreEntitytype#featurestore}
        :param description: Optional. Description of the EntityType. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#description GoogleVertexAiFeaturestoreEntitytype#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#id GoogleVertexAiFeaturestoreEntitytype#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: A set of key/value label pairs to assign to this EntityType. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#labels GoogleVertexAiFeaturestoreEntitytype#labels}
        :param monitoring_config: monitoring_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#monitoring_config GoogleVertexAiFeaturestoreEntitytype#monitoring_config}
        :param name: The name of the EntityType. This value may be up to 60 characters, and valid characters are [a-z0-9_]. The first character cannot be a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#name GoogleVertexAiFeaturestoreEntitytype#name}
        :param offline_storage_ttl_days: Config for data retention policy in offline storage. TTL in days for feature values that will be stored in offline storage. The Feature Store offline storage periodically removes obsolete feature values older than offlineStorageTtlDays since the feature generation time. If unset (or explicitly set to 0), default to 4000 days TTL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#offline_storage_ttl_days GoogleVertexAiFeaturestoreEntitytype#offline_storage_ttl_days}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#timeouts GoogleVertexAiFeaturestoreEntitytype#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(monitoring_config, dict):
            monitoring_config = GoogleVertexAiFeaturestoreEntitytypeMonitoringConfig(**monitoring_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleVertexAiFeaturestoreEntitytypeTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cf7d62faed44c0975f56873e108e92bb9f3d3edabfe2e38e8f2ca0313cd61e3)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument featurestore", value=featurestore, expected_type=type_hints["featurestore"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument monitoring_config", value=monitoring_config, expected_type=type_hints["monitoring_config"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument offline_storage_ttl_days", value=offline_storage_ttl_days, expected_type=type_hints["offline_storage_ttl_days"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "featurestore": featurestore,
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
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if monitoring_config is not None:
            self._values["monitoring_config"] = monitoring_config
        if name is not None:
            self._values["name"] = name
        if offline_storage_ttl_days is not None:
            self._values["offline_storage_ttl_days"] = offline_storage_ttl_days
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
    def featurestore(self) -> builtins.str:
        '''The name of the Featurestore to use, in the format projects/{project}/locations/{location}/featurestores/{featurestore}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#featurestore GoogleVertexAiFeaturestoreEntitytype#featurestore}
        '''
        result = self._values.get("featurestore")
        assert result is not None, "Required property 'featurestore' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional. Description of the EntityType.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#description GoogleVertexAiFeaturestoreEntitytype#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#id GoogleVertexAiFeaturestoreEntitytype#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A set of key/value label pairs to assign to this EntityType.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#labels GoogleVertexAiFeaturestoreEntitytype#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def monitoring_config(
        self,
    ) -> typing.Optional["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfig"]:
        '''monitoring_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#monitoring_config GoogleVertexAiFeaturestoreEntitytype#monitoring_config}
        '''
        result = self._values.get("monitoring_config")
        return typing.cast(typing.Optional["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfig"], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the EntityType.

        This value may be up to 60 characters, and valid characters are [a-z0-9_]. The first character cannot be a number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#name GoogleVertexAiFeaturestoreEntitytype#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def offline_storage_ttl_days(self) -> typing.Optional[jsii.Number]:
        '''Config for data retention policy in offline storage.

        TTL in days for feature values that will be stored in offline storage. The Feature Store offline storage periodically removes obsolete feature values older than offlineStorageTtlDays since the feature generation time. If unset (or explicitly set to 0), default to 4000 days TTL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#offline_storage_ttl_days GoogleVertexAiFeaturestoreEntitytype#offline_storage_ttl_days}
        '''
        result = self._values.get("offline_storage_ttl_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleVertexAiFeaturestoreEntitytypeTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#timeouts GoogleVertexAiFeaturestoreEntitytype#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleVertexAiFeaturestoreEntitytypeTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiFeaturestoreEntitytypeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeaturestoreEntitytype.GoogleVertexAiFeaturestoreEntitytypeMonitoringConfig",
    jsii_struct_bases=[],
    name_mapping={
        "categorical_threshold_config": "categoricalThresholdConfig",
        "import_features_analysis": "importFeaturesAnalysis",
        "numerical_threshold_config": "numericalThresholdConfig",
        "snapshot_analysis": "snapshotAnalysis",
    },
)
class GoogleVertexAiFeaturestoreEntitytypeMonitoringConfig:
    def __init__(
        self,
        *,
        categorical_threshold_config: typing.Optional[typing.Union["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        import_features_analysis: typing.Optional[typing.Union["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis", typing.Dict[builtins.str, typing.Any]]] = None,
        numerical_threshold_config: typing.Optional[typing.Union["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        snapshot_analysis: typing.Optional[typing.Union["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param categorical_threshold_config: categorical_threshold_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#categorical_threshold_config GoogleVertexAiFeaturestoreEntitytype#categorical_threshold_config}
        :param import_features_analysis: import_features_analysis block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#import_features_analysis GoogleVertexAiFeaturestoreEntitytype#import_features_analysis}
        :param numerical_threshold_config: numerical_threshold_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#numerical_threshold_config GoogleVertexAiFeaturestoreEntitytype#numerical_threshold_config}
        :param snapshot_analysis: snapshot_analysis block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#snapshot_analysis GoogleVertexAiFeaturestoreEntitytype#snapshot_analysis}
        '''
        if isinstance(categorical_threshold_config, dict):
            categorical_threshold_config = GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig(**categorical_threshold_config)
        if isinstance(import_features_analysis, dict):
            import_features_analysis = GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis(**import_features_analysis)
        if isinstance(numerical_threshold_config, dict):
            numerical_threshold_config = GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig(**numerical_threshold_config)
        if isinstance(snapshot_analysis, dict):
            snapshot_analysis = GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis(**snapshot_analysis)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1e12911e66d8f1b2340efa1a96c21abba347fa66ae08cf6b74e446b52fe4b89)
            check_type(argname="argument categorical_threshold_config", value=categorical_threshold_config, expected_type=type_hints["categorical_threshold_config"])
            check_type(argname="argument import_features_analysis", value=import_features_analysis, expected_type=type_hints["import_features_analysis"])
            check_type(argname="argument numerical_threshold_config", value=numerical_threshold_config, expected_type=type_hints["numerical_threshold_config"])
            check_type(argname="argument snapshot_analysis", value=snapshot_analysis, expected_type=type_hints["snapshot_analysis"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if categorical_threshold_config is not None:
            self._values["categorical_threshold_config"] = categorical_threshold_config
        if import_features_analysis is not None:
            self._values["import_features_analysis"] = import_features_analysis
        if numerical_threshold_config is not None:
            self._values["numerical_threshold_config"] = numerical_threshold_config
        if snapshot_analysis is not None:
            self._values["snapshot_analysis"] = snapshot_analysis

    @builtins.property
    def categorical_threshold_config(
        self,
    ) -> typing.Optional["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig"]:
        '''categorical_threshold_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#categorical_threshold_config GoogleVertexAiFeaturestoreEntitytype#categorical_threshold_config}
        '''
        result = self._values.get("categorical_threshold_config")
        return typing.cast(typing.Optional["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig"], result)

    @builtins.property
    def import_features_analysis(
        self,
    ) -> typing.Optional["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis"]:
        '''import_features_analysis block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#import_features_analysis GoogleVertexAiFeaturestoreEntitytype#import_features_analysis}
        '''
        result = self._values.get("import_features_analysis")
        return typing.cast(typing.Optional["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis"], result)

    @builtins.property
    def numerical_threshold_config(
        self,
    ) -> typing.Optional["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig"]:
        '''numerical_threshold_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#numerical_threshold_config GoogleVertexAiFeaturestoreEntitytype#numerical_threshold_config}
        '''
        result = self._values.get("numerical_threshold_config")
        return typing.cast(typing.Optional["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig"], result)

    @builtins.property
    def snapshot_analysis(
        self,
    ) -> typing.Optional["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis"]:
        '''snapshot_analysis block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#snapshot_analysis GoogleVertexAiFeaturestoreEntitytype#snapshot_analysis}
        '''
        result = self._values.get("snapshot_analysis")
        return typing.cast(typing.Optional["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiFeaturestoreEntitytypeMonitoringConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeaturestoreEntitytype.GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig",
    jsii_struct_bases=[],
    name_mapping={"value": "value"},
)
class GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig:
    def __init__(self, *, value: jsii.Number) -> None:
        '''
        :param value: Specify a threshold value that can trigger the alert. For categorical feature, the distribution distance is calculated by L-inifinity norm. Each feature must have a non-zero threshold if they need to be monitored. Otherwise no alert will be triggered for that feature. The default value is 0.3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#value GoogleVertexAiFeaturestoreEntitytype#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f67d5c9a9008ab8474f5c31811e78a6966160d5afee27d4c35d80ec68271d9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "value": value,
        }

    @builtins.property
    def value(self) -> jsii.Number:
        '''Specify a threshold value that can trigger the alert.

        For categorical feature, the distribution distance is calculated by L-inifinity norm. Each feature must have a non-zero threshold if they need to be monitored. Otherwise no alert will be triggered for that feature. The default value is 0.3.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#value GoogleVertexAiFeaturestoreEntitytype#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeaturestoreEntitytype.GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b8714c27539373815561a45f8b95a854ff0623e629f3057b4cc8cf1a3c4906b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0567dd770099176cc5e1ad2385969da5a2c7219258c7313d1d2fe5504665cccf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig]:
        return typing.cast(typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3caab258ed14b0998acdc43dd3214873e026a3794eedcbff3289193614e7e9c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeaturestoreEntitytype.GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis",
    jsii_struct_bases=[],
    name_mapping={
        "anomaly_detection_baseline": "anomalyDetectionBaseline",
        "state": "state",
    },
)
class GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis:
    def __init__(
        self,
        *,
        anomaly_detection_baseline: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param anomaly_detection_baseline: Defines the baseline to do anomaly detection for feature values imported by each [entityTypes.importFeatureValues][] operation. The value must be one of the values below: * LATEST_STATS: Choose the later one statistics generated by either most recent snapshot analysis or previous import features analysis. If non of them exists, skip anomaly detection and only generate a statistics. * MOST_RECENT_SNAPSHOT_STATS: Use the statistics generated by the most recent snapshot analysis if exists. * PREVIOUS_IMPORT_FEATURES_STATS: Use the statistics generated by the previous import features analysis if exists. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#anomaly_detection_baseline GoogleVertexAiFeaturestoreEntitytype#anomaly_detection_baseline}
        :param state: Whether to enable / disable / inherite default hebavior for import features analysis. The value must be one of the values below: - DEFAULT: The default behavior of whether to enable the monitoring. EntityType-level config: disabled. - ENABLED: Explicitly enables import features analysis. EntityType-level config: by default enables import features analysis for all Features under it. - DISABLED: Explicitly disables import features analysis. EntityType-level config: by default disables import features analysis for all Features under it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#state GoogleVertexAiFeaturestoreEntitytype#state}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83a83c3b212b5a1903c9cbe2bfdca0f070bf2aa29fe87811e4ffde5422669a41)
            check_type(argname="argument anomaly_detection_baseline", value=anomaly_detection_baseline, expected_type=type_hints["anomaly_detection_baseline"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if anomaly_detection_baseline is not None:
            self._values["anomaly_detection_baseline"] = anomaly_detection_baseline
        if state is not None:
            self._values["state"] = state

    @builtins.property
    def anomaly_detection_baseline(self) -> typing.Optional[builtins.str]:
        '''Defines the baseline to do anomaly detection for feature values imported by each [entityTypes.importFeatureValues][] operation. The value must be one of the values below: * LATEST_STATS: Choose the later one statistics generated by either most recent snapshot analysis or previous import features analysis. If non of them exists, skip anomaly detection and only generate a statistics. * MOST_RECENT_SNAPSHOT_STATS: Use the statistics generated by the most recent snapshot analysis if exists. * PREVIOUS_IMPORT_FEATURES_STATS: Use the statistics generated by the previous import features analysis if exists.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#anomaly_detection_baseline GoogleVertexAiFeaturestoreEntitytype#anomaly_detection_baseline}
        '''
        result = self._values.get("anomaly_detection_baseline")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Whether to enable / disable / inherite default hebavior for import features analysis.

        The value must be one of the values below:

        - DEFAULT: The default behavior of whether to enable the monitoring. EntityType-level config: disabled.
        - ENABLED: Explicitly enables import features analysis. EntityType-level config: by default enables import features analysis for all Features under it.
        - DISABLED: Explicitly disables import features analysis. EntityType-level config: by default disables import features analysis for all Features under it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#state GoogleVertexAiFeaturestoreEntitytype#state}
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysisOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeaturestoreEntitytype.GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysisOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c07e689b571220145a68c660d7e584f38d75ecb95e55a45bedfca48b5b36624)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAnomalyDetectionBaseline")
    def reset_anomaly_detection_baseline(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnomalyDetectionBaseline", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

    @builtins.property
    @jsii.member(jsii_name="anomalyDetectionBaselineInput")
    def anomaly_detection_baseline_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "anomalyDetectionBaselineInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="anomalyDetectionBaseline")
    def anomaly_detection_baseline(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "anomalyDetectionBaseline"))

    @anomaly_detection_baseline.setter
    def anomaly_detection_baseline(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29baa584a57b3b15b604938ee61cb6af96803829d32980b68859b22fdc5423e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "anomalyDetectionBaseline", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__626fdff0659f9fddcdf193367070b0de7c2f6140099c1db334f829044397dc28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis]:
        return typing.cast(typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a8026d10945fd23b8375ccf6c85a06ac85150bf816e60e21aafa03b6e6e8825)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeaturestoreEntitytype.GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig",
    jsii_struct_bases=[],
    name_mapping={"value": "value"},
)
class GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig:
    def __init__(self, *, value: jsii.Number) -> None:
        '''
        :param value: Specify a threshold value that can trigger the alert. For numerical feature, the distribution distance is calculated by Jensen–Shannon divergence. Each feature must have a non-zero threshold if they need to be monitored. Otherwise no alert will be triggered for that feature. The default value is 0.3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#value GoogleVertexAiFeaturestoreEntitytype#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8c0215ee85081d7bf35cfadcdfab929c934f4087644627f03930326a1e8b9ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "value": value,
        }

    @builtins.property
    def value(self) -> jsii.Number:
        '''Specify a threshold value that can trigger the alert.

        For numerical feature, the distribution distance is calculated by Jensen–Shannon divergence. Each feature must have a non-zero threshold if they need to be monitored. Otherwise no alert will be triggered for that feature. The default value is 0.3.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#value GoogleVertexAiFeaturestoreEntitytype#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeaturestoreEntitytype.GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__190ace4892acf243ca74d1d3140b06d795dfb3e81aac9ff05fcb72068f3ab318)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20e2c123ea0a34c844d4acd965ccdfd999cd7c4a87d2c229ae7df0ce636bb7f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig]:
        return typing.cast(typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbdde61f5ba28f86371b0d5d98bdd6486416a0996e4d102795403852664d458b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeaturestoreEntitytype.GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c65a36eec861fa851a4f0e36b1b24670eb5679e2a4b64f4ab738101ac4a63ce1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCategoricalThresholdConfig")
    def put_categorical_threshold_config(self, *, value: jsii.Number) -> None:
        '''
        :param value: Specify a threshold value that can trigger the alert. For categorical feature, the distribution distance is calculated by L-inifinity norm. Each feature must have a non-zero threshold if they need to be monitored. Otherwise no alert will be triggered for that feature. The default value is 0.3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#value GoogleVertexAiFeaturestoreEntitytype#value}
        '''
        value_ = GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig(
            value=value
        )

        return typing.cast(None, jsii.invoke(self, "putCategoricalThresholdConfig", [value_]))

    @jsii.member(jsii_name="putImportFeaturesAnalysis")
    def put_import_features_analysis(
        self,
        *,
        anomaly_detection_baseline: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param anomaly_detection_baseline: Defines the baseline to do anomaly detection for feature values imported by each [entityTypes.importFeatureValues][] operation. The value must be one of the values below: * LATEST_STATS: Choose the later one statistics generated by either most recent snapshot analysis or previous import features analysis. If non of them exists, skip anomaly detection and only generate a statistics. * MOST_RECENT_SNAPSHOT_STATS: Use the statistics generated by the most recent snapshot analysis if exists. * PREVIOUS_IMPORT_FEATURES_STATS: Use the statistics generated by the previous import features analysis if exists. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#anomaly_detection_baseline GoogleVertexAiFeaturestoreEntitytype#anomaly_detection_baseline}
        :param state: Whether to enable / disable / inherite default hebavior for import features analysis. The value must be one of the values below: - DEFAULT: The default behavior of whether to enable the monitoring. EntityType-level config: disabled. - ENABLED: Explicitly enables import features analysis. EntityType-level config: by default enables import features analysis for all Features under it. - DISABLED: Explicitly disables import features analysis. EntityType-level config: by default disables import features analysis for all Features under it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#state GoogleVertexAiFeaturestoreEntitytype#state}
        '''
        value = GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis(
            anomaly_detection_baseline=anomaly_detection_baseline, state=state
        )

        return typing.cast(None, jsii.invoke(self, "putImportFeaturesAnalysis", [value]))

    @jsii.member(jsii_name="putNumericalThresholdConfig")
    def put_numerical_threshold_config(self, *, value: jsii.Number) -> None:
        '''
        :param value: Specify a threshold value that can trigger the alert. For numerical feature, the distribution distance is calculated by Jensen–Shannon divergence. Each feature must have a non-zero threshold if they need to be monitored. Otherwise no alert will be triggered for that feature. The default value is 0.3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#value GoogleVertexAiFeaturestoreEntitytype#value}
        '''
        value_ = GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig(
            value=value
        )

        return typing.cast(None, jsii.invoke(self, "putNumericalThresholdConfig", [value_]))

    @jsii.member(jsii_name="putSnapshotAnalysis")
    def put_snapshot_analysis(
        self,
        *,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        monitoring_interval: typing.Optional[builtins.str] = None,
        monitoring_interval_days: typing.Optional[jsii.Number] = None,
        staleness_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param disabled: The monitoring schedule for snapshot analysis. For EntityType-level config: unset / disabled = true indicates disabled by default for Features under it; otherwise by default enable snapshot analysis monitoring with monitoringInterval for Features under it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#disabled GoogleVertexAiFeaturestoreEntitytype#disabled}
        :param monitoring_interval: Configuration of the snapshot analysis based monitoring pipeline running interval. The value is rolled up to full day. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#monitoring_interval GoogleVertexAiFeaturestoreEntitytype#monitoring_interval}
        :param monitoring_interval_days: Configuration of the snapshot analysis based monitoring pipeline running interval. The value indicates number of days. The default value is 1. If both FeaturestoreMonitoringConfig.SnapshotAnalysis.monitoring_interval_days and [FeaturestoreMonitoringConfig.SnapshotAnalysis.monitoring_interval][] are set when creating/updating EntityTypes/Features, FeaturestoreMonitoringConfig.SnapshotAnalysis.monitoring_interval_days will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#monitoring_interval_days GoogleVertexAiFeaturestoreEntitytype#monitoring_interval_days}
        :param staleness_days: Customized export features time window for snapshot analysis. Unit is one day. The default value is 21 days. Minimum value is 1 day. Maximum value is 4000 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#staleness_days GoogleVertexAiFeaturestoreEntitytype#staleness_days}
        '''
        value = GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis(
            disabled=disabled,
            monitoring_interval=monitoring_interval,
            monitoring_interval_days=monitoring_interval_days,
            staleness_days=staleness_days,
        )

        return typing.cast(None, jsii.invoke(self, "putSnapshotAnalysis", [value]))

    @jsii.member(jsii_name="resetCategoricalThresholdConfig")
    def reset_categorical_threshold_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCategoricalThresholdConfig", []))

    @jsii.member(jsii_name="resetImportFeaturesAnalysis")
    def reset_import_features_analysis(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImportFeaturesAnalysis", []))

    @jsii.member(jsii_name="resetNumericalThresholdConfig")
    def reset_numerical_threshold_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumericalThresholdConfig", []))

    @jsii.member(jsii_name="resetSnapshotAnalysis")
    def reset_snapshot_analysis(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnapshotAnalysis", []))

    @builtins.property
    @jsii.member(jsii_name="categoricalThresholdConfig")
    def categorical_threshold_config(
        self,
    ) -> GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfigOutputReference:
        return typing.cast(GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfigOutputReference, jsii.get(self, "categoricalThresholdConfig"))

    @builtins.property
    @jsii.member(jsii_name="importFeaturesAnalysis")
    def import_features_analysis(
        self,
    ) -> GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysisOutputReference:
        return typing.cast(GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysisOutputReference, jsii.get(self, "importFeaturesAnalysis"))

    @builtins.property
    @jsii.member(jsii_name="numericalThresholdConfig")
    def numerical_threshold_config(
        self,
    ) -> GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfigOutputReference:
        return typing.cast(GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfigOutputReference, jsii.get(self, "numericalThresholdConfig"))

    @builtins.property
    @jsii.member(jsii_name="snapshotAnalysis")
    def snapshot_analysis(
        self,
    ) -> "GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysisOutputReference":
        return typing.cast("GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysisOutputReference", jsii.get(self, "snapshotAnalysis"))

    @builtins.property
    @jsii.member(jsii_name="categoricalThresholdConfigInput")
    def categorical_threshold_config_input(
        self,
    ) -> typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig]:
        return typing.cast(typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig], jsii.get(self, "categoricalThresholdConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="importFeaturesAnalysisInput")
    def import_features_analysis_input(
        self,
    ) -> typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis]:
        return typing.cast(typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis], jsii.get(self, "importFeaturesAnalysisInput"))

    @builtins.property
    @jsii.member(jsii_name="numericalThresholdConfigInput")
    def numerical_threshold_config_input(
        self,
    ) -> typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig]:
        return typing.cast(typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig], jsii.get(self, "numericalThresholdConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotAnalysisInput")
    def snapshot_analysis_input(
        self,
    ) -> typing.Optional["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis"]:
        return typing.cast(typing.Optional["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis"], jsii.get(self, "snapshotAnalysisInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfig]:
        return typing.cast(typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aef690299dd06cbb8ce933dc36ba553526e67807bcbac7d3fd222c24406b96e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeaturestoreEntitytype.GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis",
    jsii_struct_bases=[],
    name_mapping={
        "disabled": "disabled",
        "monitoring_interval": "monitoringInterval",
        "monitoring_interval_days": "monitoringIntervalDays",
        "staleness_days": "stalenessDays",
    },
)
class GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis:
    def __init__(
        self,
        *,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        monitoring_interval: typing.Optional[builtins.str] = None,
        monitoring_interval_days: typing.Optional[jsii.Number] = None,
        staleness_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param disabled: The monitoring schedule for snapshot analysis. For EntityType-level config: unset / disabled = true indicates disabled by default for Features under it; otherwise by default enable snapshot analysis monitoring with monitoringInterval for Features under it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#disabled GoogleVertexAiFeaturestoreEntitytype#disabled}
        :param monitoring_interval: Configuration of the snapshot analysis based monitoring pipeline running interval. The value is rolled up to full day. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#monitoring_interval GoogleVertexAiFeaturestoreEntitytype#monitoring_interval}
        :param monitoring_interval_days: Configuration of the snapshot analysis based monitoring pipeline running interval. The value indicates number of days. The default value is 1. If both FeaturestoreMonitoringConfig.SnapshotAnalysis.monitoring_interval_days and [FeaturestoreMonitoringConfig.SnapshotAnalysis.monitoring_interval][] are set when creating/updating EntityTypes/Features, FeaturestoreMonitoringConfig.SnapshotAnalysis.monitoring_interval_days will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#monitoring_interval_days GoogleVertexAiFeaturestoreEntitytype#monitoring_interval_days}
        :param staleness_days: Customized export features time window for snapshot analysis. Unit is one day. The default value is 21 days. Minimum value is 1 day. Maximum value is 4000 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#staleness_days GoogleVertexAiFeaturestoreEntitytype#staleness_days}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5947b7f2ef528a45643f15ec6ae8a018aa2c59adc9a5249a5ddc92698fe97035)
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument monitoring_interval", value=monitoring_interval, expected_type=type_hints["monitoring_interval"])
            check_type(argname="argument monitoring_interval_days", value=monitoring_interval_days, expected_type=type_hints["monitoring_interval_days"])
            check_type(argname="argument staleness_days", value=staleness_days, expected_type=type_hints["staleness_days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disabled is not None:
            self._values["disabled"] = disabled
        if monitoring_interval is not None:
            self._values["monitoring_interval"] = monitoring_interval
        if monitoring_interval_days is not None:
            self._values["monitoring_interval_days"] = monitoring_interval_days
        if staleness_days is not None:
            self._values["staleness_days"] = staleness_days

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The monitoring schedule for snapshot analysis.

        For EntityType-level config: unset / disabled = true indicates disabled by default for Features under it; otherwise by default enable snapshot analysis monitoring with monitoringInterval for Features under it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#disabled GoogleVertexAiFeaturestoreEntitytype#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def monitoring_interval(self) -> typing.Optional[builtins.str]:
        '''Configuration of the snapshot analysis based monitoring pipeline running interval. The value is rolled up to full day.

        A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#monitoring_interval GoogleVertexAiFeaturestoreEntitytype#monitoring_interval}
        '''
        result = self._values.get("monitoring_interval")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def monitoring_interval_days(self) -> typing.Optional[jsii.Number]:
        '''Configuration of the snapshot analysis based monitoring pipeline running interval.

        The value indicates number of days. The default value is 1.
        If both FeaturestoreMonitoringConfig.SnapshotAnalysis.monitoring_interval_days and [FeaturestoreMonitoringConfig.SnapshotAnalysis.monitoring_interval][] are set when creating/updating EntityTypes/Features, FeaturestoreMonitoringConfig.SnapshotAnalysis.monitoring_interval_days will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#monitoring_interval_days GoogleVertexAiFeaturestoreEntitytype#monitoring_interval_days}
        '''
        result = self._values.get("monitoring_interval_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def staleness_days(self) -> typing.Optional[jsii.Number]:
        '''Customized export features time window for snapshot analysis.

        Unit is one day. The default value is 21 days. Minimum value is 1 day. Maximum value is 4000 days.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#staleness_days GoogleVertexAiFeaturestoreEntitytype#staleness_days}
        '''
        result = self._values.get("staleness_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysisOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeaturestoreEntitytype.GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysisOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__55b0353b7c515c68d5a6768ca94113abfb7b138734072edd201dd2fc7f64e611)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDisabled")
    def reset_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabled", []))

    @jsii.member(jsii_name="resetMonitoringInterval")
    def reset_monitoring_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitoringInterval", []))

    @jsii.member(jsii_name="resetMonitoringIntervalDays")
    def reset_monitoring_interval_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitoringIntervalDays", []))

    @jsii.member(jsii_name="resetStalenessDays")
    def reset_staleness_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStalenessDays", []))

    @builtins.property
    @jsii.member(jsii_name="disabledInput")
    def disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disabledInput"))

    @builtins.property
    @jsii.member(jsii_name="monitoringIntervalDaysInput")
    def monitoring_interval_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "monitoringIntervalDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="monitoringIntervalInput")
    def monitoring_interval_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "monitoringIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="stalenessDaysInput")
    def staleness_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "stalenessDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="disabled")
    def disabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disabled"))

    @disabled.setter
    def disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__837c81a31a02ab7705d6e833f110d323c855bb404657faa4f7731c6c34c7443b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="monitoringInterval")
    def monitoring_interval(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "monitoringInterval"))

    @monitoring_interval.setter
    def monitoring_interval(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64bd579cc0a4a90a5bdbdfe7c7b64e01ba8160a18b864c5cd660488614ea3269)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitoringInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="monitoringIntervalDays")
    def monitoring_interval_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "monitoringIntervalDays"))

    @monitoring_interval_days.setter
    def monitoring_interval_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae1547b016d1c6bc9efa6a96661289b2f147d8280c1e82e3a92f6441a6941e49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitoringIntervalDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stalenessDays")
    def staleness_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "stalenessDays"))

    @staleness_days.setter
    def staleness_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2daf02a226fa9933cfe53c011f28ff1b550e8a258662b3f420c90020be3ba19a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stalenessDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis]:
        return typing.cast(typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23d74947c060d394c7d268badc50eefcdb493d75438a5a7b8a88eac3386245c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeaturestoreEntitytype.GoogleVertexAiFeaturestoreEntitytypeTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleVertexAiFeaturestoreEntitytypeTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#create GoogleVertexAiFeaturestoreEntitytype#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#delete GoogleVertexAiFeaturestoreEntitytype#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#update GoogleVertexAiFeaturestoreEntitytype#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fec19fefb6fcca2c169edec51c3782015aa207de7b24d618d36f5cb14a6eb098)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#create GoogleVertexAiFeaturestoreEntitytype#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#delete GoogleVertexAiFeaturestoreEntitytype#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_featurestore_entitytype#update GoogleVertexAiFeaturestoreEntitytype#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiFeaturestoreEntitytypeTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiFeaturestoreEntitytypeTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeaturestoreEntitytype.GoogleVertexAiFeaturestoreEntitytypeTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a254aee63d58963c5f9a5dd2518b94393ebd09bb28b158111e69d13df6b11ca4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad9c632f6863f3f68d17aaeb43a882b99b18f045774f4edfe98885112e402538)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcd1ad9289744c913a3a4630fecabbb53519836268f0d30fd20a4af6f833d5bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a3976f010f5e5dabfe7e55c593802f6becacc6259a67b28e7fbb00d9f1006ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiFeaturestoreEntitytypeTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiFeaturestoreEntitytypeTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiFeaturestoreEntitytypeTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f022a75e08553c4badf113d059353f7e2927051085d2e2edf3f2878bd4ac324)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleVertexAiFeaturestoreEntitytype",
    "GoogleVertexAiFeaturestoreEntitytypeConfig",
    "GoogleVertexAiFeaturestoreEntitytypeMonitoringConfig",
    "GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig",
    "GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfigOutputReference",
    "GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis",
    "GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysisOutputReference",
    "GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig",
    "GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfigOutputReference",
    "GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigOutputReference",
    "GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis",
    "GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysisOutputReference",
    "GoogleVertexAiFeaturestoreEntitytypeTimeouts",
    "GoogleVertexAiFeaturestoreEntitytypeTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__d4b70139098610c17e11047a17c9cfaf2cd7aa5353326848c98a16fd5ebeeb3c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    featurestore: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    monitoring_config: typing.Optional[typing.Union[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    offline_storage_ttl_days: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[GoogleVertexAiFeaturestoreEntitytypeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__f1beda63207f22e8a64645399006ba3d42f2314912d8c1ab993211adeafd9973(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eab28c2bc6a17e6d38ae87597dd8b7f155a86acd18e049d3721fdcee25cf6dd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c44855fd21fbc6ca6170e1ee384fcde9809720b545af4523281ca0efdc0bcbf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b08247b0d323078d62ef602c924890e0203eeb0df55c257a90c7dd1a94e2567(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__181743b6afadc118c2faa8bad8b3d04fd64fa0a55d12dff3b194528a9b34cdc2(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb775115645b95162cbe48853f55426e4c49330c2ae263763b11eaa8a03d7144(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93ba38cb47d6f90b8b2bbd4ba01f461da0f190e13f4a34939185c84b55b7ccd5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cf7d62faed44c0975f56873e108e92bb9f3d3edabfe2e38e8f2ca0313cd61e3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    featurestore: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    monitoring_config: typing.Optional[typing.Union[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    offline_storage_ttl_days: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[GoogleVertexAiFeaturestoreEntitytypeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1e12911e66d8f1b2340efa1a96c21abba347fa66ae08cf6b74e446b52fe4b89(
    *,
    categorical_threshold_config: typing.Optional[typing.Union[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    import_features_analysis: typing.Optional[typing.Union[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis, typing.Dict[builtins.str, typing.Any]]] = None,
    numerical_threshold_config: typing.Optional[typing.Union[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    snapshot_analysis: typing.Optional[typing.Union[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f67d5c9a9008ab8474f5c31811e78a6966160d5afee27d4c35d80ec68271d9f(
    *,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b8714c27539373815561a45f8b95a854ff0623e629f3057b4cc8cf1a3c4906b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0567dd770099176cc5e1ad2385969da5a2c7219258c7313d1d2fe5504665cccf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3caab258ed14b0998acdc43dd3214873e026a3794eedcbff3289193614e7e9c3(
    value: typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83a83c3b212b5a1903c9cbe2bfdca0f070bf2aa29fe87811e4ffde5422669a41(
    *,
    anomaly_detection_baseline: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c07e689b571220145a68c660d7e584f38d75ecb95e55a45bedfca48b5b36624(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29baa584a57b3b15b604938ee61cb6af96803829d32980b68859b22fdc5423e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__626fdff0659f9fddcdf193367070b0de7c2f6140099c1db334f829044397dc28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a8026d10945fd23b8375ccf6c85a06ac85150bf816e60e21aafa03b6e6e8825(
    value: typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8c0215ee85081d7bf35cfadcdfab929c934f4087644627f03930326a1e8b9ef(
    *,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__190ace4892acf243ca74d1d3140b06d795dfb3e81aac9ff05fcb72068f3ab318(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20e2c123ea0a34c844d4acd965ccdfd999cd7c4a87d2c229ae7df0ce636bb7f4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbdde61f5ba28f86371b0d5d98bdd6486416a0996e4d102795403852664d458b(
    value: typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c65a36eec861fa851a4f0e36b1b24670eb5679e2a4b64f4ab738101ac4a63ce1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aef690299dd06cbb8ce933dc36ba553526e67807bcbac7d3fd222c24406b96e(
    value: typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5947b7f2ef528a45643f15ec6ae8a018aa2c59adc9a5249a5ddc92698fe97035(
    *,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    monitoring_interval: typing.Optional[builtins.str] = None,
    monitoring_interval_days: typing.Optional[jsii.Number] = None,
    staleness_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55b0353b7c515c68d5a6768ca94113abfb7b138734072edd201dd2fc7f64e611(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__837c81a31a02ab7705d6e833f110d323c855bb404657faa4f7731c6c34c7443b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64bd579cc0a4a90a5bdbdfe7c7b64e01ba8160a18b864c5cd660488614ea3269(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae1547b016d1c6bc9efa6a96661289b2f147d8280c1e82e3a92f6441a6941e49(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2daf02a226fa9933cfe53c011f28ff1b550e8a258662b3f420c90020be3ba19a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23d74947c060d394c7d268badc50eefcdb493d75438a5a7b8a88eac3386245c3(
    value: typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fec19fefb6fcca2c169edec51c3782015aa207de7b24d618d36f5cb14a6eb098(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a254aee63d58963c5f9a5dd2518b94393ebd09bb28b158111e69d13df6b11ca4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad9c632f6863f3f68d17aaeb43a882b99b18f045774f4edfe98885112e402538(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcd1ad9289744c913a3a4630fecabbb53519836268f0d30fd20a4af6f833d5bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a3976f010f5e5dabfe7e55c593802f6becacc6259a67b28e7fbb00d9f1006ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f022a75e08553c4badf113d059353f7e2927051085d2e2edf3f2878bd4ac324(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiFeaturestoreEntitytypeTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
