r'''
# `google_discovery_engine_recommendation_engine`

Refer to the Terraform Registry for docs: [`google_discovery_engine_recommendation_engine`](https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine).
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


class DiscoveryEngineRecommendationEngine(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.discoveryEngineRecommendationEngine.DiscoveryEngineRecommendationEngine",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine google_discovery_engine_recommendation_engine}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        data_store_ids: typing.Sequence[builtins.str],
        display_name: builtins.str,
        engine_id: builtins.str,
        location: builtins.str,
        common_config: typing.Optional[typing.Union["DiscoveryEngineRecommendationEngineCommonConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        industry_vertical: typing.Optional[builtins.str] = None,
        media_recommendation_engine_config: typing.Optional[typing.Union["DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DiscoveryEngineRecommendationEngineTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine google_discovery_engine_recommendation_engine} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param data_store_ids: The data stores associated with this engine. For SOLUTION_TYPE_RECOMMENDATION type of engines, they can only associate with at most one data store. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#data_store_ids DiscoveryEngineRecommendationEngine#data_store_ids}
        :param display_name: Required. The display name of the engine. Should be human readable. UTF-8 encoded string with limit of 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#display_name DiscoveryEngineRecommendationEngine#display_name}
        :param engine_id: Unique ID to use for Recommendation Engine. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#engine_id DiscoveryEngineRecommendationEngine#engine_id}
        :param location: The geographic location where the data store should reside. The value can only be one of "global", "us" and "eu". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#location DiscoveryEngineRecommendationEngine#location}
        :param common_config: common_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#common_config DiscoveryEngineRecommendationEngine#common_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#id DiscoveryEngineRecommendationEngine#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param industry_vertical: The industry vertical that the engine registers. The restriction of the Engine industry vertical is based on DataStore: If unspecified, default to GENERIC. Vertical on Engine has to match vertical of the DataStore liniked to the engine. Default value: "GENERIC" Possible values: ["GENERIC", "MEDIA"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#industry_vertical DiscoveryEngineRecommendationEngine#industry_vertical}
        :param media_recommendation_engine_config: media_recommendation_engine_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#media_recommendation_engine_config DiscoveryEngineRecommendationEngine#media_recommendation_engine_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#project DiscoveryEngineRecommendationEngine#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#timeouts DiscoveryEngineRecommendationEngine#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__550e288bf88580167082973118fcf0a4813eda389728ee7ca2d38695f35f82bd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DiscoveryEngineRecommendationEngineConfig(
            data_store_ids=data_store_ids,
            display_name=display_name,
            engine_id=engine_id,
            location=location,
            common_config=common_config,
            id=id,
            industry_vertical=industry_vertical,
            media_recommendation_engine_config=media_recommendation_engine_config,
            project=project,
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
        '''Generates CDKTF code for importing a DiscoveryEngineRecommendationEngine resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DiscoveryEngineRecommendationEngine to import.
        :param import_from_id: The id of the existing DiscoveryEngineRecommendationEngine that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DiscoveryEngineRecommendationEngine to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45a3aa9c47c6142626d0dabb17e242759db5c7235f86b261adc1d51b5e870033)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCommonConfig")
    def put_common_config(
        self,
        *,
        company_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param company_name: The name of the company, business or entity that is associated with the engine. Setting this may help improve LLM related features.cd Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#company_name DiscoveryEngineRecommendationEngine#company_name}
        '''
        value = DiscoveryEngineRecommendationEngineCommonConfig(
            company_name=company_name
        )

        return typing.cast(None, jsii.invoke(self, "putCommonConfig", [value]))

    @jsii.member(jsii_name="putMediaRecommendationEngineConfig")
    def put_media_recommendation_engine_config(
        self,
        *,
        engine_features_config: typing.Optional[typing.Union["DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        optimization_objective: typing.Optional[builtins.str] = None,
        optimization_objective_config: typing.Optional[typing.Union["DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        training_state: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param engine_features_config: engine_features_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#engine_features_config DiscoveryEngineRecommendationEngine#engine_features_config}
        :param optimization_objective: The optimization objective. e.g., 'cvr'. This field together with MediaRecommendationEngineConfig.type describes engine metadata to use to control engine training and serving. Currently supported values: 'ctr', 'cvr'. If not specified, we choose default based on engine type. Default depends on type of recommendation: 'recommended-for-you' => 'ctr' 'others-you-may-like' => 'ctr' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#optimization_objective DiscoveryEngineRecommendationEngine#optimization_objective}
        :param optimization_objective_config: optimization_objective_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#optimization_objective_config DiscoveryEngineRecommendationEngine#optimization_objective_config}
        :param training_state: The training state that the engine is in (e.g. 'TRAINING' or 'PAUSED'). Since part of the cost of running the service is frequency of training - this can be used to determine when to train engine in order to control cost. If not specified: the default value for 'CreateEngine' method is 'TRAINING'. The default value for 'UpdateEngine' method is to keep the state the same as before. Possible values: ["PAUSED", "TRAINING"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#training_state DiscoveryEngineRecommendationEngine#training_state}
        :param type: The type of engine. e.g., 'recommended-for-you'. This field together with MediaRecommendationEngineConfig.optimizationObjective describes engine metadata to use to control engine training and serving. Currently supported values: 'recommended-for-you', 'others-you-may-like', 'more-like-this', 'most-popular-items'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#type DiscoveryEngineRecommendationEngine#type}
        '''
        value = DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfig(
            engine_features_config=engine_features_config,
            optimization_objective=optimization_objective,
            optimization_objective_config=optimization_objective_config,
            training_state=training_state,
            type=type,
        )

        return typing.cast(None, jsii.invoke(self, "putMediaRecommendationEngineConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#create DiscoveryEngineRecommendationEngine#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#delete DiscoveryEngineRecommendationEngine#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#update DiscoveryEngineRecommendationEngine#update}.
        '''
        value = DiscoveryEngineRecommendationEngineTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCommonConfig")
    def reset_common_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommonConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIndustryVertical")
    def reset_industry_vertical(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIndustryVertical", []))

    @jsii.member(jsii_name="resetMediaRecommendationEngineConfig")
    def reset_media_recommendation_engine_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMediaRecommendationEngineConfig", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

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
    @jsii.member(jsii_name="commonConfig")
    def common_config(
        self,
    ) -> "DiscoveryEngineRecommendationEngineCommonConfigOutputReference":
        return typing.cast("DiscoveryEngineRecommendationEngineCommonConfigOutputReference", jsii.get(self, "commonConfig"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="mediaRecommendationEngineConfig")
    def media_recommendation_engine_config(
        self,
    ) -> "DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOutputReference":
        return typing.cast("DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOutputReference", jsii.get(self, "mediaRecommendationEngineConfig"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DiscoveryEngineRecommendationEngineTimeoutsOutputReference":
        return typing.cast("DiscoveryEngineRecommendationEngineTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="commonConfigInput")
    def common_config_input(
        self,
    ) -> typing.Optional["DiscoveryEngineRecommendationEngineCommonConfig"]:
        return typing.cast(typing.Optional["DiscoveryEngineRecommendationEngineCommonConfig"], jsii.get(self, "commonConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="dataStoreIdsInput")
    def data_store_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dataStoreIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="engineIdInput")
    def engine_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "engineIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="industryVerticalInput")
    def industry_vertical_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "industryVerticalInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="mediaRecommendationEngineConfigInput")
    def media_recommendation_engine_config_input(
        self,
    ) -> typing.Optional["DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfig"]:
        return typing.cast(typing.Optional["DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfig"], jsii.get(self, "mediaRecommendationEngineConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DiscoveryEngineRecommendationEngineTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DiscoveryEngineRecommendationEngineTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataStoreIds")
    def data_store_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dataStoreIds"))

    @data_store_ids.setter
    def data_store_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aedbf7957c39f7ef5622bbd3d289c4ec27e3f44824c9696f0e42f3256ac5ee5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataStoreIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ad84b1751532cbc47239f6484baf2d56404d63afe699568b4d8641f798b13e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="engineId")
    def engine_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "engineId"))

    @engine_id.setter
    def engine_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52052772d9c2265607a4a4dd0d9246bd374f39133a40d8632c0e706905b3decb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46c20a6bdeb24ff95d39327ac480a0acff49beb92811d841c5788abb846c32ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="industryVertical")
    def industry_vertical(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "industryVertical"))

    @industry_vertical.setter
    def industry_vertical(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb4059bc0519a8697121a57b1a76c5fcfa548e9e79163973f4f7e98b5d855f73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "industryVertical", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50688225551adcc988bfdb9ef314e95dd5e1f3cca62116b59eef51e6bc640d89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77b2fa6daed8aac35f1f449a5c01d388d3d132ebd67481af4105e228e826fcbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.discoveryEngineRecommendationEngine.DiscoveryEngineRecommendationEngineCommonConfig",
    jsii_struct_bases=[],
    name_mapping={"company_name": "companyName"},
)
class DiscoveryEngineRecommendationEngineCommonConfig:
    def __init__(self, *, company_name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param company_name: The name of the company, business or entity that is associated with the engine. Setting this may help improve LLM related features.cd Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#company_name DiscoveryEngineRecommendationEngine#company_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15f26efe8ec93f487864f6c1ae549946c853e442dfae517c9a430e1dd55b4214)
            check_type(argname="argument company_name", value=company_name, expected_type=type_hints["company_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if company_name is not None:
            self._values["company_name"] = company_name

    @builtins.property
    def company_name(self) -> typing.Optional[builtins.str]:
        '''The name of the company, business or entity that is associated with the engine.

        Setting this may help improve LLM related features.cd

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#company_name DiscoveryEngineRecommendationEngine#company_name}
        '''
        result = self._values.get("company_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiscoveryEngineRecommendationEngineCommonConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DiscoveryEngineRecommendationEngineCommonConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.discoveryEngineRecommendationEngine.DiscoveryEngineRecommendationEngineCommonConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__504134f5a14976c5d71251abc1abd9d3f9e65fbe8314f99e264b0a36e0d2b8d5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCompanyName")
    def reset_company_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompanyName", []))

    @builtins.property
    @jsii.member(jsii_name="companyNameInput")
    def company_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "companyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="companyName")
    def company_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "companyName"))

    @company_name.setter
    def company_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8018f520215af9d7f14285584c6785aa61dc08a11476982553ec82d451a6033)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "companyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DiscoveryEngineRecommendationEngineCommonConfig]:
        return typing.cast(typing.Optional[DiscoveryEngineRecommendationEngineCommonConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DiscoveryEngineRecommendationEngineCommonConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19634f2ef5e22dc172b4c94ee29f37367616dc0d6692b98f10cf2ee6746a8487)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.discoveryEngineRecommendationEngine.DiscoveryEngineRecommendationEngineConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "data_store_ids": "dataStoreIds",
        "display_name": "displayName",
        "engine_id": "engineId",
        "location": "location",
        "common_config": "commonConfig",
        "id": "id",
        "industry_vertical": "industryVertical",
        "media_recommendation_engine_config": "mediaRecommendationEngineConfig",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class DiscoveryEngineRecommendationEngineConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        data_store_ids: typing.Sequence[builtins.str],
        display_name: builtins.str,
        engine_id: builtins.str,
        location: builtins.str,
        common_config: typing.Optional[typing.Union[DiscoveryEngineRecommendationEngineCommonConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        industry_vertical: typing.Optional[builtins.str] = None,
        media_recommendation_engine_config: typing.Optional[typing.Union["DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DiscoveryEngineRecommendationEngineTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param data_store_ids: The data stores associated with this engine. For SOLUTION_TYPE_RECOMMENDATION type of engines, they can only associate with at most one data store. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#data_store_ids DiscoveryEngineRecommendationEngine#data_store_ids}
        :param display_name: Required. The display name of the engine. Should be human readable. UTF-8 encoded string with limit of 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#display_name DiscoveryEngineRecommendationEngine#display_name}
        :param engine_id: Unique ID to use for Recommendation Engine. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#engine_id DiscoveryEngineRecommendationEngine#engine_id}
        :param location: The geographic location where the data store should reside. The value can only be one of "global", "us" and "eu". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#location DiscoveryEngineRecommendationEngine#location}
        :param common_config: common_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#common_config DiscoveryEngineRecommendationEngine#common_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#id DiscoveryEngineRecommendationEngine#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param industry_vertical: The industry vertical that the engine registers. The restriction of the Engine industry vertical is based on DataStore: If unspecified, default to GENERIC. Vertical on Engine has to match vertical of the DataStore liniked to the engine. Default value: "GENERIC" Possible values: ["GENERIC", "MEDIA"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#industry_vertical DiscoveryEngineRecommendationEngine#industry_vertical}
        :param media_recommendation_engine_config: media_recommendation_engine_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#media_recommendation_engine_config DiscoveryEngineRecommendationEngine#media_recommendation_engine_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#project DiscoveryEngineRecommendationEngine#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#timeouts DiscoveryEngineRecommendationEngine#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(common_config, dict):
            common_config = DiscoveryEngineRecommendationEngineCommonConfig(**common_config)
        if isinstance(media_recommendation_engine_config, dict):
            media_recommendation_engine_config = DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfig(**media_recommendation_engine_config)
        if isinstance(timeouts, dict):
            timeouts = DiscoveryEngineRecommendationEngineTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5f0bfd523154e836b75c9b80586e4ad316f44974844a121c6bc68f5f78a3164)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument data_store_ids", value=data_store_ids, expected_type=type_hints["data_store_ids"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument engine_id", value=engine_id, expected_type=type_hints["engine_id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument common_config", value=common_config, expected_type=type_hints["common_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument industry_vertical", value=industry_vertical, expected_type=type_hints["industry_vertical"])
            check_type(argname="argument media_recommendation_engine_config", value=media_recommendation_engine_config, expected_type=type_hints["media_recommendation_engine_config"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_store_ids": data_store_ids,
            "display_name": display_name,
            "engine_id": engine_id,
            "location": location,
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
        if common_config is not None:
            self._values["common_config"] = common_config
        if id is not None:
            self._values["id"] = id
        if industry_vertical is not None:
            self._values["industry_vertical"] = industry_vertical
        if media_recommendation_engine_config is not None:
            self._values["media_recommendation_engine_config"] = media_recommendation_engine_config
        if project is not None:
            self._values["project"] = project
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
    def data_store_ids(self) -> typing.List[builtins.str]:
        '''The data stores associated with this engine.

        For SOLUTION_TYPE_RECOMMENDATION type of engines, they can only associate with at most one data store.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#data_store_ids DiscoveryEngineRecommendationEngine#data_store_ids}
        '''
        result = self._values.get("data_store_ids")
        assert result is not None, "Required property 'data_store_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''Required. The display name of the engine. Should be human readable. UTF-8 encoded string with limit of 1024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#display_name DiscoveryEngineRecommendationEngine#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def engine_id(self) -> builtins.str:
        '''Unique ID to use for Recommendation Engine.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#engine_id DiscoveryEngineRecommendationEngine#engine_id}
        '''
        result = self._values.get("engine_id")
        assert result is not None, "Required property 'engine_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The geographic location where the data store should reside. The value can only be one of "global", "us" and "eu".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#location DiscoveryEngineRecommendationEngine#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def common_config(
        self,
    ) -> typing.Optional[DiscoveryEngineRecommendationEngineCommonConfig]:
        '''common_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#common_config DiscoveryEngineRecommendationEngine#common_config}
        '''
        result = self._values.get("common_config")
        return typing.cast(typing.Optional[DiscoveryEngineRecommendationEngineCommonConfig], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#id DiscoveryEngineRecommendationEngine#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def industry_vertical(self) -> typing.Optional[builtins.str]:
        '''The industry vertical that the engine registers.

        The restriction of the Engine industry vertical is based on DataStore: If unspecified, default to GENERIC. Vertical on Engine has to match vertical of the DataStore liniked to the engine. Default value: "GENERIC" Possible values: ["GENERIC", "MEDIA"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#industry_vertical DiscoveryEngineRecommendationEngine#industry_vertical}
        '''
        result = self._values.get("industry_vertical")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def media_recommendation_engine_config(
        self,
    ) -> typing.Optional["DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfig"]:
        '''media_recommendation_engine_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#media_recommendation_engine_config DiscoveryEngineRecommendationEngine#media_recommendation_engine_config}
        '''
        result = self._values.get("media_recommendation_engine_config")
        return typing.cast(typing.Optional["DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#project DiscoveryEngineRecommendationEngine#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["DiscoveryEngineRecommendationEngineTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#timeouts DiscoveryEngineRecommendationEngine#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DiscoveryEngineRecommendationEngineTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiscoveryEngineRecommendationEngineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.discoveryEngineRecommendationEngine.DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfig",
    jsii_struct_bases=[],
    name_mapping={
        "engine_features_config": "engineFeaturesConfig",
        "optimization_objective": "optimizationObjective",
        "optimization_objective_config": "optimizationObjectiveConfig",
        "training_state": "trainingState",
        "type": "type",
    },
)
class DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfig:
    def __init__(
        self,
        *,
        engine_features_config: typing.Optional[typing.Union["DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        optimization_objective: typing.Optional[builtins.str] = None,
        optimization_objective_config: typing.Optional[typing.Union["DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        training_state: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param engine_features_config: engine_features_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#engine_features_config DiscoveryEngineRecommendationEngine#engine_features_config}
        :param optimization_objective: The optimization objective. e.g., 'cvr'. This field together with MediaRecommendationEngineConfig.type describes engine metadata to use to control engine training and serving. Currently supported values: 'ctr', 'cvr'. If not specified, we choose default based on engine type. Default depends on type of recommendation: 'recommended-for-you' => 'ctr' 'others-you-may-like' => 'ctr' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#optimization_objective DiscoveryEngineRecommendationEngine#optimization_objective}
        :param optimization_objective_config: optimization_objective_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#optimization_objective_config DiscoveryEngineRecommendationEngine#optimization_objective_config}
        :param training_state: The training state that the engine is in (e.g. 'TRAINING' or 'PAUSED'). Since part of the cost of running the service is frequency of training - this can be used to determine when to train engine in order to control cost. If not specified: the default value for 'CreateEngine' method is 'TRAINING'. The default value for 'UpdateEngine' method is to keep the state the same as before. Possible values: ["PAUSED", "TRAINING"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#training_state DiscoveryEngineRecommendationEngine#training_state}
        :param type: The type of engine. e.g., 'recommended-for-you'. This field together with MediaRecommendationEngineConfig.optimizationObjective describes engine metadata to use to control engine training and serving. Currently supported values: 'recommended-for-you', 'others-you-may-like', 'more-like-this', 'most-popular-items'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#type DiscoveryEngineRecommendationEngine#type}
        '''
        if isinstance(engine_features_config, dict):
            engine_features_config = DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfig(**engine_features_config)
        if isinstance(optimization_objective_config, dict):
            optimization_objective_config = DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfig(**optimization_objective_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54b240cc8765dc4b68eaf376a44ad6d237ecff7ba0403ba9b306bc1f6f77e2cb)
            check_type(argname="argument engine_features_config", value=engine_features_config, expected_type=type_hints["engine_features_config"])
            check_type(argname="argument optimization_objective", value=optimization_objective, expected_type=type_hints["optimization_objective"])
            check_type(argname="argument optimization_objective_config", value=optimization_objective_config, expected_type=type_hints["optimization_objective_config"])
            check_type(argname="argument training_state", value=training_state, expected_type=type_hints["training_state"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if engine_features_config is not None:
            self._values["engine_features_config"] = engine_features_config
        if optimization_objective is not None:
            self._values["optimization_objective"] = optimization_objective
        if optimization_objective_config is not None:
            self._values["optimization_objective_config"] = optimization_objective_config
        if training_state is not None:
            self._values["training_state"] = training_state
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def engine_features_config(
        self,
    ) -> typing.Optional["DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfig"]:
        '''engine_features_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#engine_features_config DiscoveryEngineRecommendationEngine#engine_features_config}
        '''
        result = self._values.get("engine_features_config")
        return typing.cast(typing.Optional["DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfig"], result)

    @builtins.property
    def optimization_objective(self) -> typing.Optional[builtins.str]:
        '''The optimization objective.

        e.g., 'cvr'.
        This field together with MediaRecommendationEngineConfig.type describes
        engine metadata to use to control engine training and serving.
        Currently supported values: 'ctr', 'cvr'.
        If not specified, we choose default based on engine type. Default depends on type of recommendation:
        'recommended-for-you' => 'ctr'
        'others-you-may-like' => 'ctr'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#optimization_objective DiscoveryEngineRecommendationEngine#optimization_objective}
        '''
        result = self._values.get("optimization_objective")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def optimization_objective_config(
        self,
    ) -> typing.Optional["DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfig"]:
        '''optimization_objective_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#optimization_objective_config DiscoveryEngineRecommendationEngine#optimization_objective_config}
        '''
        result = self._values.get("optimization_objective_config")
        return typing.cast(typing.Optional["DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfig"], result)

    @builtins.property
    def training_state(self) -> typing.Optional[builtins.str]:
        '''The training state that the engine is in (e.g. 'TRAINING' or 'PAUSED'). Since part of the cost of running the service is frequency of training - this can be used to determine when to train engine in order to control cost. If not specified: the default value for 'CreateEngine' method is 'TRAINING'. The default value for 'UpdateEngine' method is to keep the state the same as before. Possible values: ["PAUSED", "TRAINING"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#training_state DiscoveryEngineRecommendationEngine#training_state}
        '''
        result = self._values.get("training_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of engine.

        e.g., 'recommended-for-you'.
        This field together with MediaRecommendationEngineConfig.optimizationObjective describes
        engine metadata to use to control engine training and serving.
        Currently supported values: 'recommended-for-you', 'others-you-may-like',
        'more-like-this', 'most-popular-items'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#type DiscoveryEngineRecommendationEngine#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.discoveryEngineRecommendationEngine.DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfig",
    jsii_struct_bases=[],
    name_mapping={
        "most_popular_config": "mostPopularConfig",
        "recommended_for_you_config": "recommendedForYouConfig",
    },
)
class DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfig:
    def __init__(
        self,
        *,
        most_popular_config: typing.Optional[typing.Union["DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        recommended_for_you_config: typing.Optional[typing.Union["DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param most_popular_config: most_popular_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#most_popular_config DiscoveryEngineRecommendationEngine#most_popular_config}
        :param recommended_for_you_config: recommended_for_you_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#recommended_for_you_config DiscoveryEngineRecommendationEngine#recommended_for_you_config}
        '''
        if isinstance(most_popular_config, dict):
            most_popular_config = DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfig(**most_popular_config)
        if isinstance(recommended_for_you_config, dict):
            recommended_for_you_config = DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfig(**recommended_for_you_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a79278b2f8a94816ebeaa3074b8b8bd9d3185f95b986fecb97198f551fbc82b5)
            check_type(argname="argument most_popular_config", value=most_popular_config, expected_type=type_hints["most_popular_config"])
            check_type(argname="argument recommended_for_you_config", value=recommended_for_you_config, expected_type=type_hints["recommended_for_you_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if most_popular_config is not None:
            self._values["most_popular_config"] = most_popular_config
        if recommended_for_you_config is not None:
            self._values["recommended_for_you_config"] = recommended_for_you_config

    @builtins.property
    def most_popular_config(
        self,
    ) -> typing.Optional["DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfig"]:
        '''most_popular_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#most_popular_config DiscoveryEngineRecommendationEngine#most_popular_config}
        '''
        result = self._values.get("most_popular_config")
        return typing.cast(typing.Optional["DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfig"], result)

    @builtins.property
    def recommended_for_you_config(
        self,
    ) -> typing.Optional["DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfig"]:
        '''recommended_for_you_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#recommended_for_you_config DiscoveryEngineRecommendationEngine#recommended_for_you_config}
        '''
        result = self._values.get("recommended_for_you_config")
        return typing.cast(typing.Optional["DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.discoveryEngineRecommendationEngine.DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfig",
    jsii_struct_bases=[],
    name_mapping={"time_window_days": "timeWindowDays"},
)
class DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfig:
    def __init__(
        self,
        *,
        time_window_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param time_window_days: The time window of which the engine is queried at training and prediction time. Positive integers only. The value translates to the last X days of events. Currently required for the 'most-popular-items' engine. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#time_window_days DiscoveryEngineRecommendationEngine#time_window_days}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1df94b569ea522f47bcf819a64573b0da739748b95dcf8e1549f19f91b4993a8)
            check_type(argname="argument time_window_days", value=time_window_days, expected_type=type_hints["time_window_days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if time_window_days is not None:
            self._values["time_window_days"] = time_window_days

    @builtins.property
    def time_window_days(self) -> typing.Optional[jsii.Number]:
        '''The time window of which the engine is queried at training and prediction time.

        Positive integers only. The value translates to the
        last X days of events. Currently required for the 'most-popular-items'
        engine.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#time_window_days DiscoveryEngineRecommendationEngine#time_window_days}
        '''
        result = self._values.get("time_window_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.discoveryEngineRecommendationEngine.DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe5982427e48ec85991e46e73b27dc013b256b986e563b46d463602329774f2a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTimeWindowDays")
    def reset_time_window_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeWindowDays", []))

    @builtins.property
    @jsii.member(jsii_name="timeWindowDaysInput")
    def time_window_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeWindowDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="timeWindowDays")
    def time_window_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeWindowDays"))

    @time_window_days.setter
    def time_window_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40854b49e83d54dc8648608ecb3a5afca4769abef2f653bc53c335d0b9dd4277)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeWindowDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfig]:
        return typing.cast(typing.Optional[DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8a5d18c1cf9cc1bb3b244e4774dd6b2b414039bf36d270dfe3479fa81a6b08f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.discoveryEngineRecommendationEngine.DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a896f01c99f8cee1faaa15dcf7f6795e9ff3a978c6f459c2075dafa3f7eb05f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMostPopularConfig")
    def put_most_popular_config(
        self,
        *,
        time_window_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param time_window_days: The time window of which the engine is queried at training and prediction time. Positive integers only. The value translates to the last X days of events. Currently required for the 'most-popular-items' engine. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#time_window_days DiscoveryEngineRecommendationEngine#time_window_days}
        '''
        value = DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfig(
            time_window_days=time_window_days
        )

        return typing.cast(None, jsii.invoke(self, "putMostPopularConfig", [value]))

    @jsii.member(jsii_name="putRecommendedForYouConfig")
    def put_recommended_for_you_config(
        self,
        *,
        context_event_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param context_event_type: The type of event with which the engine is queried at prediction time. If set to 'generic', only 'view-item', 'media-play',and 'media-complete' will be used as 'context-event' in engine training. If set to 'view-home-page', 'view-home-page' will also be used as 'context-events' in addition to 'view-item', 'media-play', and 'media-complete'. Currently supported for the 'recommended-for-you' engine. Currently supported values: 'view-home-page', 'generic'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#context_event_type DiscoveryEngineRecommendationEngine#context_event_type}
        '''
        value = DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfig(
            context_event_type=context_event_type
        )

        return typing.cast(None, jsii.invoke(self, "putRecommendedForYouConfig", [value]))

    @jsii.member(jsii_name="resetMostPopularConfig")
    def reset_most_popular_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMostPopularConfig", []))

    @jsii.member(jsii_name="resetRecommendedForYouConfig")
    def reset_recommended_for_you_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecommendedForYouConfig", []))

    @builtins.property
    @jsii.member(jsii_name="mostPopularConfig")
    def most_popular_config(
        self,
    ) -> DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfigOutputReference:
        return typing.cast(DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfigOutputReference, jsii.get(self, "mostPopularConfig"))

    @builtins.property
    @jsii.member(jsii_name="recommendedForYouConfig")
    def recommended_for_you_config(
        self,
    ) -> "DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfigOutputReference":
        return typing.cast("DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfigOutputReference", jsii.get(self, "recommendedForYouConfig"))

    @builtins.property
    @jsii.member(jsii_name="mostPopularConfigInput")
    def most_popular_config_input(
        self,
    ) -> typing.Optional[DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfig]:
        return typing.cast(typing.Optional[DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfig], jsii.get(self, "mostPopularConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="recommendedForYouConfigInput")
    def recommended_for_you_config_input(
        self,
    ) -> typing.Optional["DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfig"]:
        return typing.cast(typing.Optional["DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfig"], jsii.get(self, "recommendedForYouConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfig]:
        return typing.cast(typing.Optional[DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0169cb764e3ee603ca583d051bc35faa804d12716a4ccae0b6e10f9d3406228)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.discoveryEngineRecommendationEngine.DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfig",
    jsii_struct_bases=[],
    name_mapping={"context_event_type": "contextEventType"},
)
class DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfig:
    def __init__(
        self,
        *,
        context_event_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param context_event_type: The type of event with which the engine is queried at prediction time. If set to 'generic', only 'view-item', 'media-play',and 'media-complete' will be used as 'context-event' in engine training. If set to 'view-home-page', 'view-home-page' will also be used as 'context-events' in addition to 'view-item', 'media-play', and 'media-complete'. Currently supported for the 'recommended-for-you' engine. Currently supported values: 'view-home-page', 'generic'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#context_event_type DiscoveryEngineRecommendationEngine#context_event_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6146b55137966a60911649d4f5d8601939639acb809927b372e4a41d3bdeefd6)
            check_type(argname="argument context_event_type", value=context_event_type, expected_type=type_hints["context_event_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if context_event_type is not None:
            self._values["context_event_type"] = context_event_type

    @builtins.property
    def context_event_type(self) -> typing.Optional[builtins.str]:
        '''The type of event with which the engine is queried at prediction time.

        If set to 'generic', only 'view-item', 'media-play',and
        'media-complete' will be used as 'context-event' in engine training. If
        set to 'view-home-page', 'view-home-page' will also be used as
        'context-events' in addition to 'view-item', 'media-play', and
        'media-complete'. Currently supported for the 'recommended-for-you'
        engine. Currently supported values: 'view-home-page', 'generic'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#context_event_type DiscoveryEngineRecommendationEngine#context_event_type}
        '''
        result = self._values.get("context_event_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.discoveryEngineRecommendationEngine.DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__11f6dbdf989acd1714b54666a66b239d8657de6dad864718160c68cb11653309)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetContextEventType")
    def reset_context_event_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContextEventType", []))

    @builtins.property
    @jsii.member(jsii_name="contextEventTypeInput")
    def context_event_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contextEventTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="contextEventType")
    def context_event_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contextEventType"))

    @context_event_type.setter
    def context_event_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__968562719eda4ae0732f0552005cffdd37e5f0941c673be12b733b24a8cde805)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contextEventType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfig]:
        return typing.cast(typing.Optional[DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20de5ab5a61eda897fa47b523794c1bb30d79edce08ae622efe21b842a221349)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.discoveryEngineRecommendationEngine.DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfig",
    jsii_struct_bases=[],
    name_mapping={
        "target_field": "targetField",
        "target_field_value_float": "targetFieldValueFloat",
    },
)
class DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfig:
    def __init__(
        self,
        *,
        target_field: typing.Optional[builtins.str] = None,
        target_field_value_float: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param target_field: The name of the field to target. Currently supported values: 'watch-percentage', 'watch-time'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#target_field DiscoveryEngineRecommendationEngine#target_field}
        :param target_field_value_float: The threshold to be applied to the target (e.g., 0.5). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#target_field_value_float DiscoveryEngineRecommendationEngine#target_field_value_float}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__919200fc714f90aa9b6d7ad609697d1e8d3c23bf492ffdd634ddccc692033916)
            check_type(argname="argument target_field", value=target_field, expected_type=type_hints["target_field"])
            check_type(argname="argument target_field_value_float", value=target_field_value_float, expected_type=type_hints["target_field_value_float"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if target_field is not None:
            self._values["target_field"] = target_field
        if target_field_value_float is not None:
            self._values["target_field_value_float"] = target_field_value_float

    @builtins.property
    def target_field(self) -> typing.Optional[builtins.str]:
        '''The name of the field to target. Currently supported values: 'watch-percentage', 'watch-time'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#target_field DiscoveryEngineRecommendationEngine#target_field}
        '''
        result = self._values.get("target_field")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_field_value_float(self) -> typing.Optional[jsii.Number]:
        '''The threshold to be applied to the target (e.g., 0.5).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#target_field_value_float DiscoveryEngineRecommendationEngine#target_field_value_float}
        '''
        result = self._values.get("target_field_value_float")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.discoveryEngineRecommendationEngine.DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c10707028fea5e78774620f7a3a89dbf9419142757a9767cb092e68840e5160a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTargetField")
    def reset_target_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetField", []))

    @jsii.member(jsii_name="resetTargetFieldValueFloat")
    def reset_target_field_value_float(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetFieldValueFloat", []))

    @builtins.property
    @jsii.member(jsii_name="targetFieldInput")
    def target_field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="targetFieldValueFloatInput")
    def target_field_value_float_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetFieldValueFloatInput"))

    @builtins.property
    @jsii.member(jsii_name="targetField")
    def target_field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetField"))

    @target_field.setter
    def target_field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70b554addde6864a58cddfaff7bbc8728fc6b2985af55b73fb2ca929089359fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetField", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetFieldValueFloat")
    def target_field_value_float(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetFieldValueFloat"))

    @target_field_value_float.setter
    def target_field_value_float(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e74dcb628ea8d94e49913ed54a9221fe506a444be249e991cf8f2f6a0669e136)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetFieldValueFloat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfig]:
        return typing.cast(typing.Optional[DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa0f4debfaebf63ed4b480468c8ac1972a1bcc06627b675270f86d36a1aaa7ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.discoveryEngineRecommendationEngine.DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b558ee06345ffbee04b250709d23bae9bf57a2c572054ee8ffdb544b9d7862df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEngineFeaturesConfig")
    def put_engine_features_config(
        self,
        *,
        most_popular_config: typing.Optional[typing.Union[DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        recommended_for_you_config: typing.Optional[typing.Union[DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param most_popular_config: most_popular_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#most_popular_config DiscoveryEngineRecommendationEngine#most_popular_config}
        :param recommended_for_you_config: recommended_for_you_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#recommended_for_you_config DiscoveryEngineRecommendationEngine#recommended_for_you_config}
        '''
        value = DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfig(
            most_popular_config=most_popular_config,
            recommended_for_you_config=recommended_for_you_config,
        )

        return typing.cast(None, jsii.invoke(self, "putEngineFeaturesConfig", [value]))

    @jsii.member(jsii_name="putOptimizationObjectiveConfig")
    def put_optimization_objective_config(
        self,
        *,
        target_field: typing.Optional[builtins.str] = None,
        target_field_value_float: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param target_field: The name of the field to target. Currently supported values: 'watch-percentage', 'watch-time'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#target_field DiscoveryEngineRecommendationEngine#target_field}
        :param target_field_value_float: The threshold to be applied to the target (e.g., 0.5). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#target_field_value_float DiscoveryEngineRecommendationEngine#target_field_value_float}
        '''
        value = DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfig(
            target_field=target_field,
            target_field_value_float=target_field_value_float,
        )

        return typing.cast(None, jsii.invoke(self, "putOptimizationObjectiveConfig", [value]))

    @jsii.member(jsii_name="resetEngineFeaturesConfig")
    def reset_engine_features_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEngineFeaturesConfig", []))

    @jsii.member(jsii_name="resetOptimizationObjective")
    def reset_optimization_objective(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptimizationObjective", []))

    @jsii.member(jsii_name="resetOptimizationObjectiveConfig")
    def reset_optimization_objective_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptimizationObjectiveConfig", []))

    @jsii.member(jsii_name="resetTrainingState")
    def reset_training_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrainingState", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="engineFeaturesConfig")
    def engine_features_config(
        self,
    ) -> DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigOutputReference:
        return typing.cast(DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigOutputReference, jsii.get(self, "engineFeaturesConfig"))

    @builtins.property
    @jsii.member(jsii_name="optimizationObjectiveConfig")
    def optimization_objective_config(
        self,
    ) -> DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfigOutputReference:
        return typing.cast(DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfigOutputReference, jsii.get(self, "optimizationObjectiveConfig"))

    @builtins.property
    @jsii.member(jsii_name="engineFeaturesConfigInput")
    def engine_features_config_input(
        self,
    ) -> typing.Optional[DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfig]:
        return typing.cast(typing.Optional[DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfig], jsii.get(self, "engineFeaturesConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="optimizationObjectiveConfigInput")
    def optimization_objective_config_input(
        self,
    ) -> typing.Optional[DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfig]:
        return typing.cast(typing.Optional[DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfig], jsii.get(self, "optimizationObjectiveConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="optimizationObjectiveInput")
    def optimization_objective_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "optimizationObjectiveInput"))

    @builtins.property
    @jsii.member(jsii_name="trainingStateInput")
    def training_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "trainingStateInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="optimizationObjective")
    def optimization_objective(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "optimizationObjective"))

    @optimization_objective.setter
    def optimization_objective(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96e1dd50b8d8f2e9e16580d58ead06e0c4d0334d9121585509dad81b1ccb8746)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optimizationObjective", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trainingState")
    def training_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trainingState"))

    @training_state.setter
    def training_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9474d8070ab700cac88e1715be432a450f0540d7609f6c90e02619fb44151870)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trainingState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ab6fd0969c710176d932cc9fd98780c40473d6a6d118545a89ecd7fb4935658)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfig]:
        return typing.cast(typing.Optional[DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc98106d23ba7c1728167a72585efbef6de1a494deec7e0b7db3d137d7ce1fdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.discoveryEngineRecommendationEngine.DiscoveryEngineRecommendationEngineTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DiscoveryEngineRecommendationEngineTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#create DiscoveryEngineRecommendationEngine#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#delete DiscoveryEngineRecommendationEngine#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#update DiscoveryEngineRecommendationEngine#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__799caaab05fa58d25189d3054c39d07a833eb817bf00f970a4b383ea1641b113)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#create DiscoveryEngineRecommendationEngine#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#delete DiscoveryEngineRecommendationEngine#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.46.0/docs/resources/discovery_engine_recommendation_engine#update DiscoveryEngineRecommendationEngine#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiscoveryEngineRecommendationEngineTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DiscoveryEngineRecommendationEngineTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.discoveryEngineRecommendationEngine.DiscoveryEngineRecommendationEngineTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fd361ad4d0908e8047a0d3626a3d2fd5cca219a06a66377c4ed7fa935f31e82)
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
            type_hints = typing.get_type_hints(_typecheckingstub__52d3dc8f35c0650325a8fe9c8bba12f9806a4268c0ff9524e6e61b4605f8d231)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bd88cd06dfafd1ad5eb80c3c1b33d5f263618b6833b846d9e6d3784895db61f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c03bb37a4c0cd7e69f93f404d29ce62118ad877d941e9ebed111b5d0abaa30af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DiscoveryEngineRecommendationEngineTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DiscoveryEngineRecommendationEngineTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DiscoveryEngineRecommendationEngineTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19f19acaaa8ec9f68952d4753deb67022bfaa81d6a13afe288bf5bc5e45398bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DiscoveryEngineRecommendationEngine",
    "DiscoveryEngineRecommendationEngineCommonConfig",
    "DiscoveryEngineRecommendationEngineCommonConfigOutputReference",
    "DiscoveryEngineRecommendationEngineConfig",
    "DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfig",
    "DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfig",
    "DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfig",
    "DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfigOutputReference",
    "DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigOutputReference",
    "DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfig",
    "DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfigOutputReference",
    "DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfig",
    "DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfigOutputReference",
    "DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOutputReference",
    "DiscoveryEngineRecommendationEngineTimeouts",
    "DiscoveryEngineRecommendationEngineTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__550e288bf88580167082973118fcf0a4813eda389728ee7ca2d38695f35f82bd(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    data_store_ids: typing.Sequence[builtins.str],
    display_name: builtins.str,
    engine_id: builtins.str,
    location: builtins.str,
    common_config: typing.Optional[typing.Union[DiscoveryEngineRecommendationEngineCommonConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    industry_vertical: typing.Optional[builtins.str] = None,
    media_recommendation_engine_config: typing.Optional[typing.Union[DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DiscoveryEngineRecommendationEngineTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__45a3aa9c47c6142626d0dabb17e242759db5c7235f86b261adc1d51b5e870033(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aedbf7957c39f7ef5622bbd3d289c4ec27e3f44824c9696f0e42f3256ac5ee5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ad84b1751532cbc47239f6484baf2d56404d63afe699568b4d8641f798b13e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52052772d9c2265607a4a4dd0d9246bd374f39133a40d8632c0e706905b3decb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46c20a6bdeb24ff95d39327ac480a0acff49beb92811d841c5788abb846c32ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb4059bc0519a8697121a57b1a76c5fcfa548e9e79163973f4f7e98b5d855f73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50688225551adcc988bfdb9ef314e95dd5e1f3cca62116b59eef51e6bc640d89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77b2fa6daed8aac35f1f449a5c01d388d3d132ebd67481af4105e228e826fcbb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15f26efe8ec93f487864f6c1ae549946c853e442dfae517c9a430e1dd55b4214(
    *,
    company_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__504134f5a14976c5d71251abc1abd9d3f9e65fbe8314f99e264b0a36e0d2b8d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8018f520215af9d7f14285584c6785aa61dc08a11476982553ec82d451a6033(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19634f2ef5e22dc172b4c94ee29f37367616dc0d6692b98f10cf2ee6746a8487(
    value: typing.Optional[DiscoveryEngineRecommendationEngineCommonConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5f0bfd523154e836b75c9b80586e4ad316f44974844a121c6bc68f5f78a3164(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_store_ids: typing.Sequence[builtins.str],
    display_name: builtins.str,
    engine_id: builtins.str,
    location: builtins.str,
    common_config: typing.Optional[typing.Union[DiscoveryEngineRecommendationEngineCommonConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    industry_vertical: typing.Optional[builtins.str] = None,
    media_recommendation_engine_config: typing.Optional[typing.Union[DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DiscoveryEngineRecommendationEngineTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54b240cc8765dc4b68eaf376a44ad6d237ecff7ba0403ba9b306bc1f6f77e2cb(
    *,
    engine_features_config: typing.Optional[typing.Union[DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    optimization_objective: typing.Optional[builtins.str] = None,
    optimization_objective_config: typing.Optional[typing.Union[DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    training_state: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a79278b2f8a94816ebeaa3074b8b8bd9d3185f95b986fecb97198f551fbc82b5(
    *,
    most_popular_config: typing.Optional[typing.Union[DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    recommended_for_you_config: typing.Optional[typing.Union[DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1df94b569ea522f47bcf819a64573b0da739748b95dcf8e1549f19f91b4993a8(
    *,
    time_window_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe5982427e48ec85991e46e73b27dc013b256b986e563b46d463602329774f2a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40854b49e83d54dc8648608ecb3a5afca4769abef2f653bc53c335d0b9dd4277(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8a5d18c1cf9cc1bb3b244e4774dd6b2b414039bf36d270dfe3479fa81a6b08f(
    value: typing.Optional[DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a896f01c99f8cee1faaa15dcf7f6795e9ff3a978c6f459c2075dafa3f7eb05f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0169cb764e3ee603ca583d051bc35faa804d12716a4ccae0b6e10f9d3406228(
    value: typing.Optional[DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6146b55137966a60911649d4f5d8601939639acb809927b372e4a41d3bdeefd6(
    *,
    context_event_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11f6dbdf989acd1714b54666a66b239d8657de6dad864718160c68cb11653309(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__968562719eda4ae0732f0552005cffdd37e5f0941c673be12b733b24a8cde805(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20de5ab5a61eda897fa47b523794c1bb30d79edce08ae622efe21b842a221349(
    value: typing.Optional[DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__919200fc714f90aa9b6d7ad609697d1e8d3c23bf492ffdd634ddccc692033916(
    *,
    target_field: typing.Optional[builtins.str] = None,
    target_field_value_float: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c10707028fea5e78774620f7a3a89dbf9419142757a9767cb092e68840e5160a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70b554addde6864a58cddfaff7bbc8728fc6b2985af55b73fb2ca929089359fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e74dcb628ea8d94e49913ed54a9221fe506a444be249e991cf8f2f6a0669e136(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa0f4debfaebf63ed4b480468c8ac1972a1bcc06627b675270f86d36a1aaa7ad(
    value: typing.Optional[DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b558ee06345ffbee04b250709d23bae9bf57a2c572054ee8ffdb544b9d7862df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96e1dd50b8d8f2e9e16580d58ead06e0c4d0334d9121585509dad81b1ccb8746(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9474d8070ab700cac88e1715be432a450f0540d7609f6c90e02619fb44151870(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ab6fd0969c710176d932cc9fd98780c40473d6a6d118545a89ecd7fb4935658(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc98106d23ba7c1728167a72585efbef6de1a494deec7e0b7db3d137d7ce1fdc(
    value: typing.Optional[DiscoveryEngineRecommendationEngineMediaRecommendationEngineConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__799caaab05fa58d25189d3054c39d07a833eb817bf00f970a4b383ea1641b113(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fd361ad4d0908e8047a0d3626a3d2fd5cca219a06a66377c4ed7fa935f31e82(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52d3dc8f35c0650325a8fe9c8bba12f9806a4268c0ff9524e6e61b4605f8d231(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bd88cd06dfafd1ad5eb80c3c1b33d5f263618b6833b846d9e6d3784895db61f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c03bb37a4c0cd7e69f93f404d29ce62118ad877d941e9ebed111b5d0abaa30af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19f19acaaa8ec9f68952d4753deb67022bfaa81d6a13afe288bf5bc5e45398bb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DiscoveryEngineRecommendationEngineTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
