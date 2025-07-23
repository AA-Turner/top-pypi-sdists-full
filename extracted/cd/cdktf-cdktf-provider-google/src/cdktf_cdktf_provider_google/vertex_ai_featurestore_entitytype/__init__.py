r'''
# `google_vertex_ai_featurestore_entitytype`

Refer to the Terraform Registry for docs: [`google_vertex_ai_featurestore_entitytype`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype).
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


class VertexAiFeaturestoreEntitytype(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiFeaturestoreEntitytype.VertexAiFeaturestoreEntitytype",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype google_vertex_ai_featurestore_entitytype}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        featurestore: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        monitoring_config: typing.Optional[typing.Union["VertexAiFeaturestoreEntitytypeMonitoringConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["VertexAiFeaturestoreEntitytypeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype google_vertex_ai_featurestore_entitytype} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param featurestore: The name of the Featurestore to use, in the format projects/{project}/locations/{location}/featurestores/{featurestore}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#featurestore VertexAiFeaturestoreEntitytype#featurestore}
        :param description: Optional. Description of the EntityType. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#description VertexAiFeaturestoreEntitytype#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#id VertexAiFeaturestoreEntitytype#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: A set of key/value label pairs to assign to this EntityType. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#labels VertexAiFeaturestoreEntitytype#labels}
        :param monitoring_config: monitoring_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#monitoring_config VertexAiFeaturestoreEntitytype#monitoring_config}
        :param name: The name of the EntityType. This value may be up to 60 characters, and valid characters are [a-z0-9_]. The first character cannot be a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#name VertexAiFeaturestoreEntitytype#name}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#timeouts VertexAiFeaturestoreEntitytype#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a16b5e0cfedc415a166ce59a970643df23ac5bb4fac781e7b3db52e60adf60e2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VertexAiFeaturestoreEntitytypeConfig(
            featurestore=featurestore,
            description=description,
            id=id,
            labels=labels,
            monitoring_config=monitoring_config,
            name=name,
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
        '''Generates CDKTF code for importing a VertexAiFeaturestoreEntitytype resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VertexAiFeaturestoreEntitytype to import.
        :param import_from_id: The id of the existing VertexAiFeaturestoreEntitytype that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VertexAiFeaturestoreEntitytype to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e6c5fbf3a1fcbf121d34a356c25d2ea40efaa4467e8ae1cac6f6861bb04ae23)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putMonitoringConfig")
    def put_monitoring_config(
        self,
        *,
        categorical_threshold_config: typing.Optional[typing.Union["VertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        import_features_analysis: typing.Optional[typing.Union["VertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis", typing.Dict[builtins.str, typing.Any]]] = None,
        numerical_threshold_config: typing.Optional[typing.Union["VertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        snapshot_analysis: typing.Optional[typing.Union["VertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param categorical_threshold_config: categorical_threshold_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#categorical_threshold_config VertexAiFeaturestoreEntitytype#categorical_threshold_config}
        :param import_features_analysis: import_features_analysis block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#import_features_analysis VertexAiFeaturestoreEntitytype#import_features_analysis}
        :param numerical_threshold_config: numerical_threshold_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#numerical_threshold_config VertexAiFeaturestoreEntitytype#numerical_threshold_config}
        :param snapshot_analysis: snapshot_analysis block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#snapshot_analysis VertexAiFeaturestoreEntitytype#snapshot_analysis}
        '''
        value = VertexAiFeaturestoreEntitytypeMonitoringConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#create VertexAiFeaturestoreEntitytype#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#delete VertexAiFeaturestoreEntitytype#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#update VertexAiFeaturestoreEntitytype#update}.
        '''
        value = VertexAiFeaturestoreEntitytypeTimeouts(
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
    ) -> "VertexAiFeaturestoreEntitytypeMonitoringConfigOutputReference":
        return typing.cast("VertexAiFeaturestoreEntitytypeMonitoringConfigOutputReference", jsii.get(self, "monitoringConfig"))

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
    def timeouts(self) -> "VertexAiFeaturestoreEntitytypeTimeoutsOutputReference":
        return typing.cast("VertexAiFeaturestoreEntitytypeTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["VertexAiFeaturestoreEntitytypeMonitoringConfig"]:
        return typing.cast(typing.Optional["VertexAiFeaturestoreEntitytypeMonitoringConfig"], jsii.get(self, "monitoringConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VertexAiFeaturestoreEntitytypeTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VertexAiFeaturestoreEntitytypeTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4c792e9fd2fff9d421bb01ed636e8ef4a9e808737e092bc81cd7b905dcc6b1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="featurestore")
    def featurestore(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "featurestore"))

    @featurestore.setter
    def featurestore(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a855b71a674b837bc9d514b6d5b52e3f3de3af1072ed27896934a64fde945fff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "featurestore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ad2a5e68dc73385f316590f159ab14db872bfe2888f92eeed47449b30a0b738)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cb3e9a8feda059575a78c03b3666baf2c3e358163fa18d91ca2c37a3246296f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9af6dffb47d9c7e406b2d266f144c1e9e668b02192e2a95613a1b48622d3551d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiFeaturestoreEntitytype.VertexAiFeaturestoreEntitytypeConfig",
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
        "timeouts": "timeouts",
    },
)
class VertexAiFeaturestoreEntitytypeConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        monitoring_config: typing.Optional[typing.Union["VertexAiFeaturestoreEntitytypeMonitoringConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["VertexAiFeaturestoreEntitytypeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param featurestore: The name of the Featurestore to use, in the format projects/{project}/locations/{location}/featurestores/{featurestore}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#featurestore VertexAiFeaturestoreEntitytype#featurestore}
        :param description: Optional. Description of the EntityType. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#description VertexAiFeaturestoreEntitytype#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#id VertexAiFeaturestoreEntitytype#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: A set of key/value label pairs to assign to this EntityType. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#labels VertexAiFeaturestoreEntitytype#labels}
        :param monitoring_config: monitoring_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#monitoring_config VertexAiFeaturestoreEntitytype#monitoring_config}
        :param name: The name of the EntityType. This value may be up to 60 characters, and valid characters are [a-z0-9_]. The first character cannot be a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#name VertexAiFeaturestoreEntitytype#name}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#timeouts VertexAiFeaturestoreEntitytype#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(monitoring_config, dict):
            monitoring_config = VertexAiFeaturestoreEntitytypeMonitoringConfig(**monitoring_config)
        if isinstance(timeouts, dict):
            timeouts = VertexAiFeaturestoreEntitytypeTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98a682deb7bee5662775d595e1d3ff3e0904a2af1adc78deb1672d4dd964c97f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#featurestore VertexAiFeaturestoreEntitytype#featurestore}
        '''
        result = self._values.get("featurestore")
        assert result is not None, "Required property 'featurestore' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional. Description of the EntityType.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#description VertexAiFeaturestoreEntitytype#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#id VertexAiFeaturestoreEntitytype#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#labels VertexAiFeaturestoreEntitytype#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def monitoring_config(
        self,
    ) -> typing.Optional["VertexAiFeaturestoreEntitytypeMonitoringConfig"]:
        '''monitoring_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#monitoring_config VertexAiFeaturestoreEntitytype#monitoring_config}
        '''
        result = self._values.get("monitoring_config")
        return typing.cast(typing.Optional["VertexAiFeaturestoreEntitytypeMonitoringConfig"], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the EntityType.

        This value may be up to 60 characters, and valid characters are [a-z0-9_]. The first character cannot be a number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#name VertexAiFeaturestoreEntitytype#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["VertexAiFeaturestoreEntitytypeTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#timeouts VertexAiFeaturestoreEntitytype#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["VertexAiFeaturestoreEntitytypeTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiFeaturestoreEntitytypeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiFeaturestoreEntitytype.VertexAiFeaturestoreEntitytypeMonitoringConfig",
    jsii_struct_bases=[],
    name_mapping={
        "categorical_threshold_config": "categoricalThresholdConfig",
        "import_features_analysis": "importFeaturesAnalysis",
        "numerical_threshold_config": "numericalThresholdConfig",
        "snapshot_analysis": "snapshotAnalysis",
    },
)
class VertexAiFeaturestoreEntitytypeMonitoringConfig:
    def __init__(
        self,
        *,
        categorical_threshold_config: typing.Optional[typing.Union["VertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        import_features_analysis: typing.Optional[typing.Union["VertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis", typing.Dict[builtins.str, typing.Any]]] = None,
        numerical_threshold_config: typing.Optional[typing.Union["VertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        snapshot_analysis: typing.Optional[typing.Union["VertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param categorical_threshold_config: categorical_threshold_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#categorical_threshold_config VertexAiFeaturestoreEntitytype#categorical_threshold_config}
        :param import_features_analysis: import_features_analysis block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#import_features_analysis VertexAiFeaturestoreEntitytype#import_features_analysis}
        :param numerical_threshold_config: numerical_threshold_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#numerical_threshold_config VertexAiFeaturestoreEntitytype#numerical_threshold_config}
        :param snapshot_analysis: snapshot_analysis block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#snapshot_analysis VertexAiFeaturestoreEntitytype#snapshot_analysis}
        '''
        if isinstance(categorical_threshold_config, dict):
            categorical_threshold_config = VertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig(**categorical_threshold_config)
        if isinstance(import_features_analysis, dict):
            import_features_analysis = VertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis(**import_features_analysis)
        if isinstance(numerical_threshold_config, dict):
            numerical_threshold_config = VertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig(**numerical_threshold_config)
        if isinstance(snapshot_analysis, dict):
            snapshot_analysis = VertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis(**snapshot_analysis)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e4e75e3387afd3222f9f07c2becbb1f02177ff4a98b1e3f927eae00a2942b0b)
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
    ) -> typing.Optional["VertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig"]:
        '''categorical_threshold_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#categorical_threshold_config VertexAiFeaturestoreEntitytype#categorical_threshold_config}
        '''
        result = self._values.get("categorical_threshold_config")
        return typing.cast(typing.Optional["VertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig"], result)

    @builtins.property
    def import_features_analysis(
        self,
    ) -> typing.Optional["VertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis"]:
        '''import_features_analysis block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#import_features_analysis VertexAiFeaturestoreEntitytype#import_features_analysis}
        '''
        result = self._values.get("import_features_analysis")
        return typing.cast(typing.Optional["VertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis"], result)

    @builtins.property
    def numerical_threshold_config(
        self,
    ) -> typing.Optional["VertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig"]:
        '''numerical_threshold_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#numerical_threshold_config VertexAiFeaturestoreEntitytype#numerical_threshold_config}
        '''
        result = self._values.get("numerical_threshold_config")
        return typing.cast(typing.Optional["VertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig"], result)

    @builtins.property
    def snapshot_analysis(
        self,
    ) -> typing.Optional["VertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis"]:
        '''snapshot_analysis block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#snapshot_analysis VertexAiFeaturestoreEntitytype#snapshot_analysis}
        '''
        result = self._values.get("snapshot_analysis")
        return typing.cast(typing.Optional["VertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiFeaturestoreEntitytypeMonitoringConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiFeaturestoreEntitytype.VertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig",
    jsii_struct_bases=[],
    name_mapping={"value": "value"},
)
class VertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig:
    def __init__(self, *, value: jsii.Number) -> None:
        '''
        :param value: Specify a threshold value that can trigger the alert. For categorical feature, the distribution distance is calculated by L-inifinity norm. Each feature must have a non-zero threshold if they need to be monitored. Otherwise no alert will be triggered for that feature. The default value is 0.3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#value VertexAiFeaturestoreEntitytype#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53060bd0875c678fd90e6f2f37e3a8239b5e1c425cb96f7458c12fd8ee95ca93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "value": value,
        }

    @builtins.property
    def value(self) -> jsii.Number:
        '''Specify a threshold value that can trigger the alert.

        For categorical feature, the distribution distance is calculated by L-inifinity norm. Each feature must have a non-zero threshold if they need to be monitored. Otherwise no alert will be triggered for that feature. The default value is 0.3.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#value VertexAiFeaturestoreEntitytype#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiFeaturestoreEntitytype.VertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2dfbf681b430dab7ebff0b6b1b297fbe1bc1ff6b6d43418e6c5cd903523ed630)
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
            type_hints = typing.get_type_hints(_typecheckingstub__43e023bb4288153e129a96d23ff49b148470090da5f2cef48939dabc52e8fc20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig]:
        return typing.cast(typing.Optional[VertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b922aaf6fa063bb60197225f79970057be21252def3b7bb7c62086e6002c8f7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiFeaturestoreEntitytype.VertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis",
    jsii_struct_bases=[],
    name_mapping={
        "anomaly_detection_baseline": "anomalyDetectionBaseline",
        "state": "state",
    },
)
class VertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis:
    def __init__(
        self,
        *,
        anomaly_detection_baseline: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param anomaly_detection_baseline: Defines the baseline to do anomaly detection for feature values imported by each [entityTypes.importFeatureValues][] operation. The value must be one of the values below: * LATEST_STATS: Choose the later one statistics generated by either most recent snapshot analysis or previous import features analysis. If non of them exists, skip anomaly detection and only generate a statistics. * MOST_RECENT_SNAPSHOT_STATS: Use the statistics generated by the most recent snapshot analysis if exists. * PREVIOUS_IMPORT_FEATURES_STATS: Use the statistics generated by the previous import features analysis if exists. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#anomaly_detection_baseline VertexAiFeaturestoreEntitytype#anomaly_detection_baseline}
        :param state: Whether to enable / disable / inherite default hebavior for import features analysis. The value must be one of the values below: - DEFAULT: The default behavior of whether to enable the monitoring. EntityType-level config: disabled. - ENABLED: Explicitly enables import features analysis. EntityType-level config: by default enables import features analysis for all Features under it. - DISABLED: Explicitly disables import features analysis. EntityType-level config: by default disables import features analysis for all Features under it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#state VertexAiFeaturestoreEntitytype#state}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__364cdb2f316fafedb2e48d63a633c6709ac8f5207237f1689118afe37cd930f8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#anomaly_detection_baseline VertexAiFeaturestoreEntitytype#anomaly_detection_baseline}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#state VertexAiFeaturestoreEntitytype#state}
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysisOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiFeaturestoreEntitytype.VertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysisOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__88668194566a7d42fc79c9a90b16fe61eec83fc6c1be6a6c4879796cd24a4878)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d61382f5fb2133283d6606ad83c23a2f62255eb7991479230689ec3689d776a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "anomalyDetectionBaseline", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcc161affc37a5ee6212fb6d617f3952cfa55264e2cb2c5cf47bbf3c764a766b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis]:
        return typing.cast(typing.Optional[VertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eddbe8fa6f8318ed1f9f0ecd54f4172f6a23af0c2e732fe5be1998789f5d223f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiFeaturestoreEntitytype.VertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig",
    jsii_struct_bases=[],
    name_mapping={"value": "value"},
)
class VertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig:
    def __init__(self, *, value: jsii.Number) -> None:
        '''
        :param value: Specify a threshold value that can trigger the alert. For numerical feature, the distribution distance is calculated by Jensen–Shannon divergence. Each feature must have a non-zero threshold if they need to be monitored. Otherwise no alert will be triggered for that feature. The default value is 0.3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#value VertexAiFeaturestoreEntitytype#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b39c6c25a4636ffaca8e69aa0ebe44a44b423e28b182f57e7e9826769576762b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "value": value,
        }

    @builtins.property
    def value(self) -> jsii.Number:
        '''Specify a threshold value that can trigger the alert.

        For numerical feature, the distribution distance is calculated by Jensen–Shannon divergence. Each feature must have a non-zero threshold if they need to be monitored. Otherwise no alert will be triggered for that feature. The default value is 0.3.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#value VertexAiFeaturestoreEntitytype#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiFeaturestoreEntitytype.VertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f4e08155c72ae7860b8d63b91485bfa905a9cabc002a27d1684f023041b6050)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f05f837a11e6e73bce092becf6aaf080c26df53bb911e9145fa2b0ef458b6acd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig]:
        return typing.cast(typing.Optional[VertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dfc0759c5cdb7abb11eb70bc3e105400f3758edc8c0c6ca2771c249d8a7435f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VertexAiFeaturestoreEntitytypeMonitoringConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiFeaturestoreEntitytype.VertexAiFeaturestoreEntitytypeMonitoringConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc589d01e142fcb34f6997d7867d246189dbc9e3748e43b21f6afd93d7007102)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCategoricalThresholdConfig")
    def put_categorical_threshold_config(self, *, value: jsii.Number) -> None:
        '''
        :param value: Specify a threshold value that can trigger the alert. For categorical feature, the distribution distance is calculated by L-inifinity norm. Each feature must have a non-zero threshold if they need to be monitored. Otherwise no alert will be triggered for that feature. The default value is 0.3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#value VertexAiFeaturestoreEntitytype#value}
        '''
        value_ = VertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig(
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
        :param anomaly_detection_baseline: Defines the baseline to do anomaly detection for feature values imported by each [entityTypes.importFeatureValues][] operation. The value must be one of the values below: * LATEST_STATS: Choose the later one statistics generated by either most recent snapshot analysis or previous import features analysis. If non of them exists, skip anomaly detection and only generate a statistics. * MOST_RECENT_SNAPSHOT_STATS: Use the statistics generated by the most recent snapshot analysis if exists. * PREVIOUS_IMPORT_FEATURES_STATS: Use the statistics generated by the previous import features analysis if exists. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#anomaly_detection_baseline VertexAiFeaturestoreEntitytype#anomaly_detection_baseline}
        :param state: Whether to enable / disable / inherite default hebavior for import features analysis. The value must be one of the values below: - DEFAULT: The default behavior of whether to enable the monitoring. EntityType-level config: disabled. - ENABLED: Explicitly enables import features analysis. EntityType-level config: by default enables import features analysis for all Features under it. - DISABLED: Explicitly disables import features analysis. EntityType-level config: by default disables import features analysis for all Features under it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#state VertexAiFeaturestoreEntitytype#state}
        '''
        value = VertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis(
            anomaly_detection_baseline=anomaly_detection_baseline, state=state
        )

        return typing.cast(None, jsii.invoke(self, "putImportFeaturesAnalysis", [value]))

    @jsii.member(jsii_name="putNumericalThresholdConfig")
    def put_numerical_threshold_config(self, *, value: jsii.Number) -> None:
        '''
        :param value: Specify a threshold value that can trigger the alert. For numerical feature, the distribution distance is calculated by Jensen–Shannon divergence. Each feature must have a non-zero threshold if they need to be monitored. Otherwise no alert will be triggered for that feature. The default value is 0.3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#value VertexAiFeaturestoreEntitytype#value}
        '''
        value_ = VertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig(
            value=value
        )

        return typing.cast(None, jsii.invoke(self, "putNumericalThresholdConfig", [value_]))

    @jsii.member(jsii_name="putSnapshotAnalysis")
    def put_snapshot_analysis(
        self,
        *,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        monitoring_interval_days: typing.Optional[jsii.Number] = None,
        staleness_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param disabled: The monitoring schedule for snapshot analysis. For EntityType-level config: unset / disabled = true indicates disabled by default for Features under it; otherwise by default enable snapshot analysis monitoring with monitoringInterval for Features under it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#disabled VertexAiFeaturestoreEntitytype#disabled}
        :param monitoring_interval_days: Configuration of the snapshot analysis based monitoring pipeline running interval. The value indicates number of days. The default value is 1. If both FeaturestoreMonitoringConfig.SnapshotAnalysis.monitoring_interval_days and [FeaturestoreMonitoringConfig.SnapshotAnalysis.monitoring_interval][] are set when creating/updating EntityTypes/Features, FeaturestoreMonitoringConfig.SnapshotAnalysis.monitoring_interval_days will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#monitoring_interval_days VertexAiFeaturestoreEntitytype#monitoring_interval_days}
        :param staleness_days: Customized export features time window for snapshot analysis. Unit is one day. The default value is 21 days. Minimum value is 1 day. Maximum value is 4000 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#staleness_days VertexAiFeaturestoreEntitytype#staleness_days}
        '''
        value = VertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis(
            disabled=disabled,
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
    ) -> VertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfigOutputReference:
        return typing.cast(VertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfigOutputReference, jsii.get(self, "categoricalThresholdConfig"))

    @builtins.property
    @jsii.member(jsii_name="importFeaturesAnalysis")
    def import_features_analysis(
        self,
    ) -> VertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysisOutputReference:
        return typing.cast(VertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysisOutputReference, jsii.get(self, "importFeaturesAnalysis"))

    @builtins.property
    @jsii.member(jsii_name="numericalThresholdConfig")
    def numerical_threshold_config(
        self,
    ) -> VertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfigOutputReference:
        return typing.cast(VertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfigOutputReference, jsii.get(self, "numericalThresholdConfig"))

    @builtins.property
    @jsii.member(jsii_name="snapshotAnalysis")
    def snapshot_analysis(
        self,
    ) -> "VertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysisOutputReference":
        return typing.cast("VertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysisOutputReference", jsii.get(self, "snapshotAnalysis"))

    @builtins.property
    @jsii.member(jsii_name="categoricalThresholdConfigInput")
    def categorical_threshold_config_input(
        self,
    ) -> typing.Optional[VertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig]:
        return typing.cast(typing.Optional[VertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig], jsii.get(self, "categoricalThresholdConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="importFeaturesAnalysisInput")
    def import_features_analysis_input(
        self,
    ) -> typing.Optional[VertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis]:
        return typing.cast(typing.Optional[VertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis], jsii.get(self, "importFeaturesAnalysisInput"))

    @builtins.property
    @jsii.member(jsii_name="numericalThresholdConfigInput")
    def numerical_threshold_config_input(
        self,
    ) -> typing.Optional[VertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig]:
        return typing.cast(typing.Optional[VertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig], jsii.get(self, "numericalThresholdConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotAnalysisInput")
    def snapshot_analysis_input(
        self,
    ) -> typing.Optional["VertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis"]:
        return typing.cast(typing.Optional["VertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis"], jsii.get(self, "snapshotAnalysisInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiFeaturestoreEntitytypeMonitoringConfig]:
        return typing.cast(typing.Optional[VertexAiFeaturestoreEntitytypeMonitoringConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiFeaturestoreEntitytypeMonitoringConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7815bf865002b7cec82982504e8acb067149683b1e51e0394684fbd2bc7ec086)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiFeaturestoreEntitytype.VertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis",
    jsii_struct_bases=[],
    name_mapping={
        "disabled": "disabled",
        "monitoring_interval_days": "monitoringIntervalDays",
        "staleness_days": "stalenessDays",
    },
)
class VertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis:
    def __init__(
        self,
        *,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        monitoring_interval_days: typing.Optional[jsii.Number] = None,
        staleness_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param disabled: The monitoring schedule for snapshot analysis. For EntityType-level config: unset / disabled = true indicates disabled by default for Features under it; otherwise by default enable snapshot analysis monitoring with monitoringInterval for Features under it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#disabled VertexAiFeaturestoreEntitytype#disabled}
        :param monitoring_interval_days: Configuration of the snapshot analysis based monitoring pipeline running interval. The value indicates number of days. The default value is 1. If both FeaturestoreMonitoringConfig.SnapshotAnalysis.monitoring_interval_days and [FeaturestoreMonitoringConfig.SnapshotAnalysis.monitoring_interval][] are set when creating/updating EntityTypes/Features, FeaturestoreMonitoringConfig.SnapshotAnalysis.monitoring_interval_days will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#monitoring_interval_days VertexAiFeaturestoreEntitytype#monitoring_interval_days}
        :param staleness_days: Customized export features time window for snapshot analysis. Unit is one day. The default value is 21 days. Minimum value is 1 day. Maximum value is 4000 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#staleness_days VertexAiFeaturestoreEntitytype#staleness_days}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faa52f50b60ff9cb9f2262b7bc259b9c7d281e1b1d7ae1b44e86758c30f3efa1)
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument monitoring_interval_days", value=monitoring_interval_days, expected_type=type_hints["monitoring_interval_days"])
            check_type(argname="argument staleness_days", value=staleness_days, expected_type=type_hints["staleness_days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disabled is not None:
            self._values["disabled"] = disabled
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#disabled VertexAiFeaturestoreEntitytype#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def monitoring_interval_days(self) -> typing.Optional[jsii.Number]:
        '''Configuration of the snapshot analysis based monitoring pipeline running interval.

        The value indicates number of days. The default value is 1.
        If both FeaturestoreMonitoringConfig.SnapshotAnalysis.monitoring_interval_days and [FeaturestoreMonitoringConfig.SnapshotAnalysis.monitoring_interval][] are set when creating/updating EntityTypes/Features, FeaturestoreMonitoringConfig.SnapshotAnalysis.monitoring_interval_days will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#monitoring_interval_days VertexAiFeaturestoreEntitytype#monitoring_interval_days}
        '''
        result = self._values.get("monitoring_interval_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def staleness_days(self) -> typing.Optional[jsii.Number]:
        '''Customized export features time window for snapshot analysis.

        Unit is one day. The default value is 21 days. Minimum value is 1 day. Maximum value is 4000 days.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#staleness_days VertexAiFeaturestoreEntitytype#staleness_days}
        '''
        result = self._values.get("staleness_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysisOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiFeaturestoreEntitytype.VertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysisOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__13cd128e4a71e55d5c41c7452f7900766f8e99d04ea958ae41e7942c3c631560)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDisabled")
    def reset_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabled", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__95ea08a4013eea003207570d6a9a3c94fd408a31549b79cc9cfcab24b116193f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="monitoringIntervalDays")
    def monitoring_interval_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "monitoringIntervalDays"))

    @monitoring_interval_days.setter
    def monitoring_interval_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4da71057abc47707e7a6d81e40192fdde692eb1922ef3671c224cea70de5ad51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitoringIntervalDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stalenessDays")
    def staleness_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "stalenessDays"))

    @staleness_days.setter
    def staleness_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c013624fb7ae162989303c1ca05821a45240eaf894c7aca1103df17db1a9848)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stalenessDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis]:
        return typing.cast(typing.Optional[VertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b47df42877ef7ac8ce81663cd5ef9797b11fb52220b2b19ecb5584a161023c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiFeaturestoreEntitytype.VertexAiFeaturestoreEntitytypeTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class VertexAiFeaturestoreEntitytypeTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#create VertexAiFeaturestoreEntitytype#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#delete VertexAiFeaturestoreEntitytype#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#update VertexAiFeaturestoreEntitytype#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83ca790c6cffe6f896efc5eefefdd1061d40d8b6b616f9b998c0c514951854e5)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#create VertexAiFeaturestoreEntitytype#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#delete VertexAiFeaturestoreEntitytype#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_featurestore_entitytype#update VertexAiFeaturestoreEntitytype#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiFeaturestoreEntitytypeTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiFeaturestoreEntitytypeTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiFeaturestoreEntitytype.VertexAiFeaturestoreEntitytypeTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cadf7384f8112d9114ae4828c6a056001bc2f5cdeba79fb2e49c441b487ecc9c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7452d6fd1c14ae5d3d02f23037fbaca310ca7817ebd2f4b93c22be5fad23cec0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cc3e791c6c5091d22c484ed2604f08315ff24869e5d8df54ab272719778e9a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a00f0295ea4e02869468936aa21e6fb5eb7e5566fe62e5a4b92d3707072d98b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiFeaturestoreEntitytypeTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiFeaturestoreEntitytypeTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiFeaturestoreEntitytypeTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0285bc86c2fb358cedb5ddc3e1506c742fb6d73c523a0e2f1f47fe775cd8752b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "VertexAiFeaturestoreEntitytype",
    "VertexAiFeaturestoreEntitytypeConfig",
    "VertexAiFeaturestoreEntitytypeMonitoringConfig",
    "VertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig",
    "VertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfigOutputReference",
    "VertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis",
    "VertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysisOutputReference",
    "VertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig",
    "VertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfigOutputReference",
    "VertexAiFeaturestoreEntitytypeMonitoringConfigOutputReference",
    "VertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis",
    "VertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysisOutputReference",
    "VertexAiFeaturestoreEntitytypeTimeouts",
    "VertexAiFeaturestoreEntitytypeTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__a16b5e0cfedc415a166ce59a970643df23ac5bb4fac781e7b3db52e60adf60e2(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    featurestore: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    monitoring_config: typing.Optional[typing.Union[VertexAiFeaturestoreEntitytypeMonitoringConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[VertexAiFeaturestoreEntitytypeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__2e6c5fbf3a1fcbf121d34a356c25d2ea40efaa4467e8ae1cac6f6861bb04ae23(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4c792e9fd2fff9d421bb01ed636e8ef4a9e808737e092bc81cd7b905dcc6b1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a855b71a674b837bc9d514b6d5b52e3f3de3af1072ed27896934a64fde945fff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ad2a5e68dc73385f316590f159ab14db872bfe2888f92eeed47449b30a0b738(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cb3e9a8feda059575a78c03b3666baf2c3e358163fa18d91ca2c37a3246296f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9af6dffb47d9c7e406b2d266f144c1e9e668b02192e2a95613a1b48622d3551d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98a682deb7bee5662775d595e1d3ff3e0904a2af1adc78deb1672d4dd964c97f(
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
    monitoring_config: typing.Optional[typing.Union[VertexAiFeaturestoreEntitytypeMonitoringConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[VertexAiFeaturestoreEntitytypeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e4e75e3387afd3222f9f07c2becbb1f02177ff4a98b1e3f927eae00a2942b0b(
    *,
    categorical_threshold_config: typing.Optional[typing.Union[VertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    import_features_analysis: typing.Optional[typing.Union[VertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis, typing.Dict[builtins.str, typing.Any]]] = None,
    numerical_threshold_config: typing.Optional[typing.Union[VertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    snapshot_analysis: typing.Optional[typing.Union[VertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53060bd0875c678fd90e6f2f37e3a8239b5e1c425cb96f7458c12fd8ee95ca93(
    *,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dfbf681b430dab7ebff0b6b1b297fbe1bc1ff6b6d43418e6c5cd903523ed630(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43e023bb4288153e129a96d23ff49b148470090da5f2cef48939dabc52e8fc20(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b922aaf6fa063bb60197225f79970057be21252def3b7bb7c62086e6002c8f7f(
    value: typing.Optional[VertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__364cdb2f316fafedb2e48d63a633c6709ac8f5207237f1689118afe37cd930f8(
    *,
    anomaly_detection_baseline: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88668194566a7d42fc79c9a90b16fe61eec83fc6c1be6a6c4879796cd24a4878(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d61382f5fb2133283d6606ad83c23a2f62255eb7991479230689ec3689d776a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcc161affc37a5ee6212fb6d617f3952cfa55264e2cb2c5cf47bbf3c764a766b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eddbe8fa6f8318ed1f9f0ecd54f4172f6a23af0c2e732fe5be1998789f5d223f(
    value: typing.Optional[VertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b39c6c25a4636ffaca8e69aa0ebe44a44b423e28b182f57e7e9826769576762b(
    *,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f4e08155c72ae7860b8d63b91485bfa905a9cabc002a27d1684f023041b6050(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f05f837a11e6e73bce092becf6aaf080c26df53bb911e9145fa2b0ef458b6acd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dfc0759c5cdb7abb11eb70bc3e105400f3758edc8c0c6ca2771c249d8a7435f(
    value: typing.Optional[VertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc589d01e142fcb34f6997d7867d246189dbc9e3748e43b21f6afd93d7007102(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7815bf865002b7cec82982504e8acb067149683b1e51e0394684fbd2bc7ec086(
    value: typing.Optional[VertexAiFeaturestoreEntitytypeMonitoringConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faa52f50b60ff9cb9f2262b7bc259b9c7d281e1b1d7ae1b44e86758c30f3efa1(
    *,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    monitoring_interval_days: typing.Optional[jsii.Number] = None,
    staleness_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13cd128e4a71e55d5c41c7452f7900766f8e99d04ea958ae41e7942c3c631560(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95ea08a4013eea003207570d6a9a3c94fd408a31549b79cc9cfcab24b116193f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4da71057abc47707e7a6d81e40192fdde692eb1922ef3671c224cea70de5ad51(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c013624fb7ae162989303c1ca05821a45240eaf894c7aca1103df17db1a9848(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b47df42877ef7ac8ce81663cd5ef9797b11fb52220b2b19ecb5584a161023c3(
    value: typing.Optional[VertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83ca790c6cffe6f896efc5eefefdd1061d40d8b6b616f9b998c0c514951854e5(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cadf7384f8112d9114ae4828c6a056001bc2f5cdeba79fb2e49c441b487ecc9c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7452d6fd1c14ae5d3d02f23037fbaca310ca7817ebd2f4b93c22be5fad23cec0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cc3e791c6c5091d22c484ed2604f08315ff24869e5d8df54ab272719778e9a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a00f0295ea4e02869468936aa21e6fb5eb7e5566fe62e5a4b92d3707072d98b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0285bc86c2fb358cedb5ddc3e1506c742fb6d73c523a0e2f1f47fe775cd8752b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiFeaturestoreEntitytypeTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
