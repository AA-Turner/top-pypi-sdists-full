r'''
# `google_discovery_engine_recommendation_engine`

Refer to the Terraform Registry for docs: [`google_discovery_engine_recommendation_engine`](https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine).
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


class GoogleDiscoveryEngineRecommendationEngine(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineRecommendationEngine.GoogleDiscoveryEngineRecommendationEngine",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine google_discovery_engine_recommendation_engine}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        data_store_ids: typing.Sequence[builtins.str],
        display_name: builtins.str,
        engine_id: builtins.str,
        location: builtins.str,
        common_config: typing.Optional[typing.Union["GoogleDiscoveryEngineRecommendationEngineCommonConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        industry_vertical: typing.Optional[builtins.str] = None,
        media_recommendation_engine_config: typing.Optional[typing.Union["GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDiscoveryEngineRecommendationEngineTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine google_discovery_engine_recommendation_engine} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param data_store_ids: The data stores associated with this engine. For SOLUTION_TYPE_RECOMMENDATION type of engines, they can only associate with at most one data store. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#data_store_ids GoogleDiscoveryEngineRecommendationEngine#data_store_ids}
        :param display_name: Required. The display name of the engine. Should be human readable. UTF-8 encoded string with limit of 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#display_name GoogleDiscoveryEngineRecommendationEngine#display_name}
        :param engine_id: Unique ID to use for Recommendation Engine. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#engine_id GoogleDiscoveryEngineRecommendationEngine#engine_id}
        :param location: The geographic location where the data store should reside. The value can only be one of "global", "us" and "eu". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#location GoogleDiscoveryEngineRecommendationEngine#location}
        :param common_config: common_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#common_config GoogleDiscoveryEngineRecommendationEngine#common_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#id GoogleDiscoveryEngineRecommendationEngine#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param industry_vertical: The industry vertical that the engine registers. The restriction of the Engine industry vertical is based on DataStore: If unspecified, default to GENERIC. Vertical on Engine has to match vertical of the DataStore liniked to the engine. Default value: "GENERIC" Possible values: ["GENERIC", "MEDIA"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#industry_vertical GoogleDiscoveryEngineRecommendationEngine#industry_vertical}
        :param media_recommendation_engine_config: media_recommendation_engine_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#media_recommendation_engine_config GoogleDiscoveryEngineRecommendationEngine#media_recommendation_engine_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#project GoogleDiscoveryEngineRecommendationEngine#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#timeouts GoogleDiscoveryEngineRecommendationEngine#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c96af48b343468f53b30b941f62bc7fe249a9ff462d8d743d7b7f24f27b248b0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDiscoveryEngineRecommendationEngineConfig(
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
        '''Generates CDKTF code for importing a GoogleDiscoveryEngineRecommendationEngine resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDiscoveryEngineRecommendationEngine to import.
        :param import_from_id: The id of the existing GoogleDiscoveryEngineRecommendationEngine that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDiscoveryEngineRecommendationEngine to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01094206c7ece8d2d2efb36cc0e497f6a807a93ebd0fd1e367c1a423bc96b592)
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
        :param company_name: The name of the company, business or entity that is associated with the engine. Setting this may help improve LLM related features.cd Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#company_name GoogleDiscoveryEngineRecommendationEngine#company_name}
        '''
        value = GoogleDiscoveryEngineRecommendationEngineCommonConfig(
            company_name=company_name
        )

        return typing.cast(None, jsii.invoke(self, "putCommonConfig", [value]))

    @jsii.member(jsii_name="putMediaRecommendationEngineConfig")
    def put_media_recommendation_engine_config(
        self,
        *,
        engine_features_config: typing.Optional[typing.Union["GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        optimization_objective: typing.Optional[builtins.str] = None,
        optimization_objective_config: typing.Optional[typing.Union["GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        training_state: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param engine_features_config: engine_features_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#engine_features_config GoogleDiscoveryEngineRecommendationEngine#engine_features_config}
        :param optimization_objective: The optimization objective. e.g., 'cvr'. This field together with MediaRecommendationEngineConfig.type describes engine metadata to use to control engine training and serving. Currently supported values: 'ctr', 'cvr'. If not specified, we choose default based on engine type. Default depends on type of recommendation: 'recommended-for-you' => 'ctr' 'others-you-may-like' => 'ctr' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#optimization_objective GoogleDiscoveryEngineRecommendationEngine#optimization_objective}
        :param optimization_objective_config: optimization_objective_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#optimization_objective_config GoogleDiscoveryEngineRecommendationEngine#optimization_objective_config}
        :param training_state: The training state that the engine is in (e.g. 'TRAINING' or 'PAUSED'). Since part of the cost of running the service is frequency of training - this can be used to determine when to train engine in order to control cost. If not specified: the default value for 'CreateEngine' method is 'TRAINING'. The default value for 'UpdateEngine' method is to keep the state the same as before. Possible values: ["PAUSED", "TRAINING"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#training_state GoogleDiscoveryEngineRecommendationEngine#training_state}
        :param type: The type of engine. e.g., 'recommended-for-you'. This field together with MediaRecommendationEngineConfig.optimizationObjective describes engine metadata to use to control engine training and serving. Currently supported values: 'recommended-for-you', 'others-you-may-like', 'more-like-this', 'most-popular-items'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#type GoogleDiscoveryEngineRecommendationEngine#type}
        '''
        value = GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#create GoogleDiscoveryEngineRecommendationEngine#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#delete GoogleDiscoveryEngineRecommendationEngine#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#update GoogleDiscoveryEngineRecommendationEngine#update}.
        '''
        value = GoogleDiscoveryEngineRecommendationEngineTimeouts(
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
    ) -> "GoogleDiscoveryEngineRecommendationEngineCommonConfigOutputReference":
        return typing.cast("GoogleDiscoveryEngineRecommendationEngineCommonConfigOutputReference", jsii.get(self, "commonConfig"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="mediaRecommendationEngineConfig")
    def media_recommendation_engine_config(
        self,
    ) -> "GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOutputReference":
        return typing.cast("GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOutputReference", jsii.get(self, "mediaRecommendationEngineConfig"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "GoogleDiscoveryEngineRecommendationEngineTimeoutsOutputReference":
        return typing.cast("GoogleDiscoveryEngineRecommendationEngineTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="commonConfigInput")
    def common_config_input(
        self,
    ) -> typing.Optional["GoogleDiscoveryEngineRecommendationEngineCommonConfig"]:
        return typing.cast(typing.Optional["GoogleDiscoveryEngineRecommendationEngineCommonConfig"], jsii.get(self, "commonConfigInput"))

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
    ) -> typing.Optional["GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfig"]:
        return typing.cast(typing.Optional["GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfig"], jsii.get(self, "mediaRecommendationEngineConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDiscoveryEngineRecommendationEngineTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDiscoveryEngineRecommendationEngineTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataStoreIds")
    def data_store_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dataStoreIds"))

    @data_store_ids.setter
    def data_store_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22a911bf59e67c22ef43b3cb57d7a674b4f78e672276e675210888c3eae1e23a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataStoreIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c4f9953b23df54fb0193d80cd570d2068da9cc1fe96b429039409ea7a222871)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="engineId")
    def engine_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "engineId"))

    @engine_id.setter
    def engine_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffd6e7f1ee654d8c10e3a22270417f4e8a24ecd03d5475f14e9c9194e4eeb028)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66771fc926bbf364415a2b370cb0593813d71f7441fbcbf576c690bcf36026ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="industryVertical")
    def industry_vertical(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "industryVertical"))

    @industry_vertical.setter
    def industry_vertical(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e447ec3508fabf778e64e17af3252b110928d3a2c8fa7f76dda5fcffb5e2eb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "industryVertical", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3203fa9518c8e3cb63cd1130cb9294e0561fcf553451855b3c3c910ff7db21d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9140d2ad32029e031bc82e075666a2c880376a0f0c898a073bb8a9598bd16db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineRecommendationEngine.GoogleDiscoveryEngineRecommendationEngineCommonConfig",
    jsii_struct_bases=[],
    name_mapping={"company_name": "companyName"},
)
class GoogleDiscoveryEngineRecommendationEngineCommonConfig:
    def __init__(self, *, company_name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param company_name: The name of the company, business or entity that is associated with the engine. Setting this may help improve LLM related features.cd Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#company_name GoogleDiscoveryEngineRecommendationEngine#company_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c04e843e39738a4763893bc04808347ced8bbcb180c4afdda299db2c1df984c7)
            check_type(argname="argument company_name", value=company_name, expected_type=type_hints["company_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if company_name is not None:
            self._values["company_name"] = company_name

    @builtins.property
    def company_name(self) -> typing.Optional[builtins.str]:
        '''The name of the company, business or entity that is associated with the engine.

        Setting this may help improve LLM related features.cd

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#company_name GoogleDiscoveryEngineRecommendationEngine#company_name}
        '''
        result = self._values.get("company_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDiscoveryEngineRecommendationEngineCommonConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDiscoveryEngineRecommendationEngineCommonConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineRecommendationEngine.GoogleDiscoveryEngineRecommendationEngineCommonConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ba2e8bd1a072da6aa179fd5ca97634b40aaf8c22dee15c5a8a41031461862e1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d5d17f2f39bc26cdb2538f33f95f03b52761986f85d52084e801cf859b8a141)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "companyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineRecommendationEngineCommonConfig]:
        return typing.cast(typing.Optional[GoogleDiscoveryEngineRecommendationEngineCommonConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDiscoveryEngineRecommendationEngineCommonConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__750bf8d18b8a980e6a638496a1f9856f03b104da8a424591f03f097b41681fdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineRecommendationEngine.GoogleDiscoveryEngineRecommendationEngineConfig",
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
class GoogleDiscoveryEngineRecommendationEngineConfig(
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
        data_store_ids: typing.Sequence[builtins.str],
        display_name: builtins.str,
        engine_id: builtins.str,
        location: builtins.str,
        common_config: typing.Optional[typing.Union[GoogleDiscoveryEngineRecommendationEngineCommonConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        industry_vertical: typing.Optional[builtins.str] = None,
        media_recommendation_engine_config: typing.Optional[typing.Union["GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDiscoveryEngineRecommendationEngineTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param data_store_ids: The data stores associated with this engine. For SOLUTION_TYPE_RECOMMENDATION type of engines, they can only associate with at most one data store. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#data_store_ids GoogleDiscoveryEngineRecommendationEngine#data_store_ids}
        :param display_name: Required. The display name of the engine. Should be human readable. UTF-8 encoded string with limit of 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#display_name GoogleDiscoveryEngineRecommendationEngine#display_name}
        :param engine_id: Unique ID to use for Recommendation Engine. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#engine_id GoogleDiscoveryEngineRecommendationEngine#engine_id}
        :param location: The geographic location where the data store should reside. The value can only be one of "global", "us" and "eu". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#location GoogleDiscoveryEngineRecommendationEngine#location}
        :param common_config: common_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#common_config GoogleDiscoveryEngineRecommendationEngine#common_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#id GoogleDiscoveryEngineRecommendationEngine#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param industry_vertical: The industry vertical that the engine registers. The restriction of the Engine industry vertical is based on DataStore: If unspecified, default to GENERIC. Vertical on Engine has to match vertical of the DataStore liniked to the engine. Default value: "GENERIC" Possible values: ["GENERIC", "MEDIA"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#industry_vertical GoogleDiscoveryEngineRecommendationEngine#industry_vertical}
        :param media_recommendation_engine_config: media_recommendation_engine_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#media_recommendation_engine_config GoogleDiscoveryEngineRecommendationEngine#media_recommendation_engine_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#project GoogleDiscoveryEngineRecommendationEngine#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#timeouts GoogleDiscoveryEngineRecommendationEngine#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(common_config, dict):
            common_config = GoogleDiscoveryEngineRecommendationEngineCommonConfig(**common_config)
        if isinstance(media_recommendation_engine_config, dict):
            media_recommendation_engine_config = GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfig(**media_recommendation_engine_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleDiscoveryEngineRecommendationEngineTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01402ecaf966b3451c87022f910f15d05470c9542318285729bd766f3ce50755)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#data_store_ids GoogleDiscoveryEngineRecommendationEngine#data_store_ids}
        '''
        result = self._values.get("data_store_ids")
        assert result is not None, "Required property 'data_store_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''Required. The display name of the engine. Should be human readable. UTF-8 encoded string with limit of 1024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#display_name GoogleDiscoveryEngineRecommendationEngine#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def engine_id(self) -> builtins.str:
        '''Unique ID to use for Recommendation Engine.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#engine_id GoogleDiscoveryEngineRecommendationEngine#engine_id}
        '''
        result = self._values.get("engine_id")
        assert result is not None, "Required property 'engine_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The geographic location where the data store should reside. The value can only be one of "global", "us" and "eu".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#location GoogleDiscoveryEngineRecommendationEngine#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def common_config(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineRecommendationEngineCommonConfig]:
        '''common_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#common_config GoogleDiscoveryEngineRecommendationEngine#common_config}
        '''
        result = self._values.get("common_config")
        return typing.cast(typing.Optional[GoogleDiscoveryEngineRecommendationEngineCommonConfig], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#id GoogleDiscoveryEngineRecommendationEngine#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def industry_vertical(self) -> typing.Optional[builtins.str]:
        '''The industry vertical that the engine registers.

        The restriction of the Engine industry vertical is based on DataStore: If unspecified, default to GENERIC. Vertical on Engine has to match vertical of the DataStore liniked to the engine. Default value: "GENERIC" Possible values: ["GENERIC", "MEDIA"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#industry_vertical GoogleDiscoveryEngineRecommendationEngine#industry_vertical}
        '''
        result = self._values.get("industry_vertical")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def media_recommendation_engine_config(
        self,
    ) -> typing.Optional["GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfig"]:
        '''media_recommendation_engine_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#media_recommendation_engine_config GoogleDiscoveryEngineRecommendationEngine#media_recommendation_engine_config}
        '''
        result = self._values.get("media_recommendation_engine_config")
        return typing.cast(typing.Optional["GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#project GoogleDiscoveryEngineRecommendationEngine#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleDiscoveryEngineRecommendationEngineTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#timeouts GoogleDiscoveryEngineRecommendationEngine#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleDiscoveryEngineRecommendationEngineTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDiscoveryEngineRecommendationEngineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineRecommendationEngine.GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfig",
    jsii_struct_bases=[],
    name_mapping={
        "engine_features_config": "engineFeaturesConfig",
        "optimization_objective": "optimizationObjective",
        "optimization_objective_config": "optimizationObjectiveConfig",
        "training_state": "trainingState",
        "type": "type",
    },
)
class GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfig:
    def __init__(
        self,
        *,
        engine_features_config: typing.Optional[typing.Union["GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        optimization_objective: typing.Optional[builtins.str] = None,
        optimization_objective_config: typing.Optional[typing.Union["GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        training_state: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param engine_features_config: engine_features_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#engine_features_config GoogleDiscoveryEngineRecommendationEngine#engine_features_config}
        :param optimization_objective: The optimization objective. e.g., 'cvr'. This field together with MediaRecommendationEngineConfig.type describes engine metadata to use to control engine training and serving. Currently supported values: 'ctr', 'cvr'. If not specified, we choose default based on engine type. Default depends on type of recommendation: 'recommended-for-you' => 'ctr' 'others-you-may-like' => 'ctr' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#optimization_objective GoogleDiscoveryEngineRecommendationEngine#optimization_objective}
        :param optimization_objective_config: optimization_objective_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#optimization_objective_config GoogleDiscoveryEngineRecommendationEngine#optimization_objective_config}
        :param training_state: The training state that the engine is in (e.g. 'TRAINING' or 'PAUSED'). Since part of the cost of running the service is frequency of training - this can be used to determine when to train engine in order to control cost. If not specified: the default value for 'CreateEngine' method is 'TRAINING'. The default value for 'UpdateEngine' method is to keep the state the same as before. Possible values: ["PAUSED", "TRAINING"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#training_state GoogleDiscoveryEngineRecommendationEngine#training_state}
        :param type: The type of engine. e.g., 'recommended-for-you'. This field together with MediaRecommendationEngineConfig.optimizationObjective describes engine metadata to use to control engine training and serving. Currently supported values: 'recommended-for-you', 'others-you-may-like', 'more-like-this', 'most-popular-items'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#type GoogleDiscoveryEngineRecommendationEngine#type}
        '''
        if isinstance(engine_features_config, dict):
            engine_features_config = GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfig(**engine_features_config)
        if isinstance(optimization_objective_config, dict):
            optimization_objective_config = GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfig(**optimization_objective_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70f7f33da8aadb053f7f5f6bfcc6c0c110464be87d5f9724cda614d5d992cd13)
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
    ) -> typing.Optional["GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfig"]:
        '''engine_features_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#engine_features_config GoogleDiscoveryEngineRecommendationEngine#engine_features_config}
        '''
        result = self._values.get("engine_features_config")
        return typing.cast(typing.Optional["GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfig"], result)

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#optimization_objective GoogleDiscoveryEngineRecommendationEngine#optimization_objective}
        '''
        result = self._values.get("optimization_objective")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def optimization_objective_config(
        self,
    ) -> typing.Optional["GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfig"]:
        '''optimization_objective_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#optimization_objective_config GoogleDiscoveryEngineRecommendationEngine#optimization_objective_config}
        '''
        result = self._values.get("optimization_objective_config")
        return typing.cast(typing.Optional["GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfig"], result)

    @builtins.property
    def training_state(self) -> typing.Optional[builtins.str]:
        '''The training state that the engine is in (e.g. 'TRAINING' or 'PAUSED'). Since part of the cost of running the service is frequency of training - this can be used to determine when to train engine in order to control cost. If not specified: the default value for 'CreateEngine' method is 'TRAINING'. The default value for 'UpdateEngine' method is to keep the state the same as before. Possible values: ["PAUSED", "TRAINING"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#training_state GoogleDiscoveryEngineRecommendationEngine#training_state}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#type GoogleDiscoveryEngineRecommendationEngine#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineRecommendationEngine.GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfig",
    jsii_struct_bases=[],
    name_mapping={
        "most_popular_config": "mostPopularConfig",
        "recommended_for_you_config": "recommendedForYouConfig",
    },
)
class GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfig:
    def __init__(
        self,
        *,
        most_popular_config: typing.Optional[typing.Union["GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        recommended_for_you_config: typing.Optional[typing.Union["GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param most_popular_config: most_popular_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#most_popular_config GoogleDiscoveryEngineRecommendationEngine#most_popular_config}
        :param recommended_for_you_config: recommended_for_you_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#recommended_for_you_config GoogleDiscoveryEngineRecommendationEngine#recommended_for_you_config}
        '''
        if isinstance(most_popular_config, dict):
            most_popular_config = GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfig(**most_popular_config)
        if isinstance(recommended_for_you_config, dict):
            recommended_for_you_config = GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfig(**recommended_for_you_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2a6d35ee98bb22adc69a449f9deaecc8d4d417ab6ce8f28b4d1334719390bd2)
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
    ) -> typing.Optional["GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfig"]:
        '''most_popular_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#most_popular_config GoogleDiscoveryEngineRecommendationEngine#most_popular_config}
        '''
        result = self._values.get("most_popular_config")
        return typing.cast(typing.Optional["GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfig"], result)

    @builtins.property
    def recommended_for_you_config(
        self,
    ) -> typing.Optional["GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfig"]:
        '''recommended_for_you_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#recommended_for_you_config GoogleDiscoveryEngineRecommendationEngine#recommended_for_you_config}
        '''
        result = self._values.get("recommended_for_you_config")
        return typing.cast(typing.Optional["GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineRecommendationEngine.GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfig",
    jsii_struct_bases=[],
    name_mapping={"time_window_days": "timeWindowDays"},
)
class GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfig:
    def __init__(
        self,
        *,
        time_window_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param time_window_days: The time window of which the engine is queried at training and prediction time. Positive integers only. The value translates to the last X days of events. Currently required for the 'most-popular-items' engine. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#time_window_days GoogleDiscoveryEngineRecommendationEngine#time_window_days}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3adac342ff0b7540a23adf9fc005f9c7645f431ae5b80833fe8e7590f6502419)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#time_window_days GoogleDiscoveryEngineRecommendationEngine#time_window_days}
        '''
        result = self._values.get("time_window_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineRecommendationEngine.GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__156e04fdfe29f6751227d771c7df6d6713072ba237674cc321f34124b1c893de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9faa14bf09a099aa10d6292817183b334209cb0572db0b2aa960bf719b641ebc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeWindowDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfig]:
        return typing.cast(typing.Optional[GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdfcea9f4d5d8ea7c651ec2ad8883922b9507ecc63868099abed0efa075a17ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineRecommendationEngine.GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1a3a96a03e5d60d424f4822cd35b3183533b6d02989a0b9063f568dcbd4aec4)
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
        :param time_window_days: The time window of which the engine is queried at training and prediction time. Positive integers only. The value translates to the last X days of events. Currently required for the 'most-popular-items' engine. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#time_window_days GoogleDiscoveryEngineRecommendationEngine#time_window_days}
        '''
        value = GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfig(
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
        :param context_event_type: The type of event with which the engine is queried at prediction time. If set to 'generic', only 'view-item', 'media-play',and 'media-complete' will be used as 'context-event' in engine training. If set to 'view-home-page', 'view-home-page' will also be used as 'context-events' in addition to 'view-item', 'media-play', and 'media-complete'. Currently supported for the 'recommended-for-you' engine. Currently supported values: 'view-home-page', 'generic'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#context_event_type GoogleDiscoveryEngineRecommendationEngine#context_event_type}
        '''
        value = GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfig(
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
    ) -> GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfigOutputReference:
        return typing.cast(GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfigOutputReference, jsii.get(self, "mostPopularConfig"))

    @builtins.property
    @jsii.member(jsii_name="recommendedForYouConfig")
    def recommended_for_you_config(
        self,
    ) -> "GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfigOutputReference":
        return typing.cast("GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfigOutputReference", jsii.get(self, "recommendedForYouConfig"))

    @builtins.property
    @jsii.member(jsii_name="mostPopularConfigInput")
    def most_popular_config_input(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfig]:
        return typing.cast(typing.Optional[GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfig], jsii.get(self, "mostPopularConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="recommendedForYouConfigInput")
    def recommended_for_you_config_input(
        self,
    ) -> typing.Optional["GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfig"]:
        return typing.cast(typing.Optional["GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfig"], jsii.get(self, "recommendedForYouConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfig]:
        return typing.cast(typing.Optional[GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43b73a1d11ee362a66b1b784231cac97c620baf8c670153b7aac0b0eded00c47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineRecommendationEngine.GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfig",
    jsii_struct_bases=[],
    name_mapping={"context_event_type": "contextEventType"},
)
class GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfig:
    def __init__(
        self,
        *,
        context_event_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param context_event_type: The type of event with which the engine is queried at prediction time. If set to 'generic', only 'view-item', 'media-play',and 'media-complete' will be used as 'context-event' in engine training. If set to 'view-home-page', 'view-home-page' will also be used as 'context-events' in addition to 'view-item', 'media-play', and 'media-complete'. Currently supported for the 'recommended-for-you' engine. Currently supported values: 'view-home-page', 'generic'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#context_event_type GoogleDiscoveryEngineRecommendationEngine#context_event_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ca1fa7594577b9e247aa2d7bad99fa889ebb8b4b83943fb080cc0139c369647)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#context_event_type GoogleDiscoveryEngineRecommendationEngine#context_event_type}
        '''
        result = self._values.get("context_event_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineRecommendationEngine.GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7245c3e83f71c354f0923624fd8fe55aa2018d7056ea40c9b5e9dc20c6977d08)
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
            type_hints = typing.get_type_hints(_typecheckingstub__763821ceab2bb45f8d1566d16d485624f5c6fe659fa2c56d4b9f3bf34accb601)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contextEventType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfig]:
        return typing.cast(typing.Optional[GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a5a8e3473a3cacb517f5e2c578a35c3d8ab8835d6cb3b70c06d6f1a05249369)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineRecommendationEngine.GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfig",
    jsii_struct_bases=[],
    name_mapping={
        "target_field": "targetField",
        "target_field_value_float": "targetFieldValueFloat",
    },
)
class GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfig:
    def __init__(
        self,
        *,
        target_field: typing.Optional[builtins.str] = None,
        target_field_value_float: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param target_field: The name of the field to target. Currently supported values: 'watch-percentage', 'watch-time'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#target_field GoogleDiscoveryEngineRecommendationEngine#target_field}
        :param target_field_value_float: The threshold to be applied to the target (e.g., 0.5). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#target_field_value_float GoogleDiscoveryEngineRecommendationEngine#target_field_value_float}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64556cb8fd5cd21e0162def4f34a977e89fc368320aace84a86df490fa29e62e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#target_field GoogleDiscoveryEngineRecommendationEngine#target_field}
        '''
        result = self._values.get("target_field")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_field_value_float(self) -> typing.Optional[jsii.Number]:
        '''The threshold to be applied to the target (e.g., 0.5).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#target_field_value_float GoogleDiscoveryEngineRecommendationEngine#target_field_value_float}
        '''
        result = self._values.get("target_field_value_float")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineRecommendationEngine.GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a27b51ad9e4dffcaaac8c6068929dde47d414eb97a15b6d228a7492f0186ce9f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__576a12dc84811997c960e1b6dbbbd4e04b5440b42e9ab0f3553b62942aed599c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetField", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetFieldValueFloat")
    def target_field_value_float(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetFieldValueFloat"))

    @target_field_value_float.setter
    def target_field_value_float(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4290dac6abb8cde37b6615b74d75a2466c7f4f7e2c817bf2f839e88ea313ccf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetFieldValueFloat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfig]:
        return typing.cast(typing.Optional[GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9738a4f964ae2d124f0a0fa923799605e671537eff6858a9a2aa906eabf0456c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineRecommendationEngine.GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8183fcfd18e762629dae420dda51038688cfcad18c501cd2cf6e20dbda7de4a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEngineFeaturesConfig")
    def put_engine_features_config(
        self,
        *,
        most_popular_config: typing.Optional[typing.Union[GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        recommended_for_you_config: typing.Optional[typing.Union[GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param most_popular_config: most_popular_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#most_popular_config GoogleDiscoveryEngineRecommendationEngine#most_popular_config}
        :param recommended_for_you_config: recommended_for_you_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#recommended_for_you_config GoogleDiscoveryEngineRecommendationEngine#recommended_for_you_config}
        '''
        value = GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfig(
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
        :param target_field: The name of the field to target. Currently supported values: 'watch-percentage', 'watch-time'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#target_field GoogleDiscoveryEngineRecommendationEngine#target_field}
        :param target_field_value_float: The threshold to be applied to the target (e.g., 0.5). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#target_field_value_float GoogleDiscoveryEngineRecommendationEngine#target_field_value_float}
        '''
        value = GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfig(
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
    ) -> GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigOutputReference:
        return typing.cast(GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigOutputReference, jsii.get(self, "engineFeaturesConfig"))

    @builtins.property
    @jsii.member(jsii_name="optimizationObjectiveConfig")
    def optimization_objective_config(
        self,
    ) -> GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfigOutputReference:
        return typing.cast(GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfigOutputReference, jsii.get(self, "optimizationObjectiveConfig"))

    @builtins.property
    @jsii.member(jsii_name="engineFeaturesConfigInput")
    def engine_features_config_input(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfig]:
        return typing.cast(typing.Optional[GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfig], jsii.get(self, "engineFeaturesConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="optimizationObjectiveConfigInput")
    def optimization_objective_config_input(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfig]:
        return typing.cast(typing.Optional[GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfig], jsii.get(self, "optimizationObjectiveConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ae75337aff464c9d70f0b86a53bea3ffd3a534ddaa1c367966f1a3e1b1e7ae6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optimizationObjective", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trainingState")
    def training_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trainingState"))

    @training_state.setter
    def training_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b34b193de291204356e21db424972ffd3fa3644999360b8c541d75fe4cfd640)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trainingState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9fdf2de0ee4d3dad133b1bb60eea0efee6d00da1a3d657fb408ae37bfdda3e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfig]:
        return typing.cast(typing.Optional[GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5be1da7703444fca24009fd546ebc3d5aaeab63b9e106978a50e75fa976f5851)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineRecommendationEngine.GoogleDiscoveryEngineRecommendationEngineTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleDiscoveryEngineRecommendationEngineTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#create GoogleDiscoveryEngineRecommendationEngine#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#delete GoogleDiscoveryEngineRecommendationEngine#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#update GoogleDiscoveryEngineRecommendationEngine#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acfc0f234ef8a5195a9bcfb08ca6fae165c24302282032cc95d87815b6abc8a7)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#create GoogleDiscoveryEngineRecommendationEngine#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#delete GoogleDiscoveryEngineRecommendationEngine#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_discovery_engine_recommendation_engine#update GoogleDiscoveryEngineRecommendationEngine#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDiscoveryEngineRecommendationEngineTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDiscoveryEngineRecommendationEngineTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineRecommendationEngine.GoogleDiscoveryEngineRecommendationEngineTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a01f103d2da34539f6c43d842dc0e5f88e84b6b160ce29b6e58d86180e304c6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__555c6f102da45d5af9a194c700c935be2a7c386c753a4a6038e63c0136c9bd06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03a99ae425a25b039f6f87b0960e45832297ffb348bfe161fc8801289b1bd63f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a4f6ef94ed90dc86aa4a506a63638a3a419b1d98f4b641853a33717feae0d68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDiscoveryEngineRecommendationEngineTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDiscoveryEngineRecommendationEngineTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDiscoveryEngineRecommendationEngineTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__251910e39bfa347b09ddbe1dfa996258f9dfb9fa89c6961331f6cab07ab3ac6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleDiscoveryEngineRecommendationEngine",
    "GoogleDiscoveryEngineRecommendationEngineCommonConfig",
    "GoogleDiscoveryEngineRecommendationEngineCommonConfigOutputReference",
    "GoogleDiscoveryEngineRecommendationEngineConfig",
    "GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfig",
    "GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfig",
    "GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfig",
    "GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfigOutputReference",
    "GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigOutputReference",
    "GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfig",
    "GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfigOutputReference",
    "GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfig",
    "GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfigOutputReference",
    "GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOutputReference",
    "GoogleDiscoveryEngineRecommendationEngineTimeouts",
    "GoogleDiscoveryEngineRecommendationEngineTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c96af48b343468f53b30b941f62bc7fe249a9ff462d8d743d7b7f24f27b248b0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    data_store_ids: typing.Sequence[builtins.str],
    display_name: builtins.str,
    engine_id: builtins.str,
    location: builtins.str,
    common_config: typing.Optional[typing.Union[GoogleDiscoveryEngineRecommendationEngineCommonConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    industry_vertical: typing.Optional[builtins.str] = None,
    media_recommendation_engine_config: typing.Optional[typing.Union[GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDiscoveryEngineRecommendationEngineTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__01094206c7ece8d2d2efb36cc0e497f6a807a93ebd0fd1e367c1a423bc96b592(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22a911bf59e67c22ef43b3cb57d7a674b4f78e672276e675210888c3eae1e23a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c4f9953b23df54fb0193d80cd570d2068da9cc1fe96b429039409ea7a222871(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffd6e7f1ee654d8c10e3a22270417f4e8a24ecd03d5475f14e9c9194e4eeb028(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66771fc926bbf364415a2b370cb0593813d71f7441fbcbf576c690bcf36026ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e447ec3508fabf778e64e17af3252b110928d3a2c8fa7f76dda5fcffb5e2eb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3203fa9518c8e3cb63cd1130cb9294e0561fcf553451855b3c3c910ff7db21d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9140d2ad32029e031bc82e075666a2c880376a0f0c898a073bb8a9598bd16db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c04e843e39738a4763893bc04808347ced8bbcb180c4afdda299db2c1df984c7(
    *,
    company_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ba2e8bd1a072da6aa179fd5ca97634b40aaf8c22dee15c5a8a41031461862e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d5d17f2f39bc26cdb2538f33f95f03b52761986f85d52084e801cf859b8a141(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__750bf8d18b8a980e6a638496a1f9856f03b104da8a424591f03f097b41681fdc(
    value: typing.Optional[GoogleDiscoveryEngineRecommendationEngineCommonConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01402ecaf966b3451c87022f910f15d05470c9542318285729bd766f3ce50755(
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
    common_config: typing.Optional[typing.Union[GoogleDiscoveryEngineRecommendationEngineCommonConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    industry_vertical: typing.Optional[builtins.str] = None,
    media_recommendation_engine_config: typing.Optional[typing.Union[GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDiscoveryEngineRecommendationEngineTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70f7f33da8aadb053f7f5f6bfcc6c0c110464be87d5f9724cda614d5d992cd13(
    *,
    engine_features_config: typing.Optional[typing.Union[GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    optimization_objective: typing.Optional[builtins.str] = None,
    optimization_objective_config: typing.Optional[typing.Union[GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    training_state: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2a6d35ee98bb22adc69a449f9deaecc8d4d417ab6ce8f28b4d1334719390bd2(
    *,
    most_popular_config: typing.Optional[typing.Union[GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    recommended_for_you_config: typing.Optional[typing.Union[GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3adac342ff0b7540a23adf9fc005f9c7645f431ae5b80833fe8e7590f6502419(
    *,
    time_window_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__156e04fdfe29f6751227d771c7df6d6713072ba237674cc321f34124b1c893de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9faa14bf09a099aa10d6292817183b334209cb0572db0b2aa960bf719b641ebc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdfcea9f4d5d8ea7c651ec2ad8883922b9507ecc63868099abed0efa075a17ad(
    value: typing.Optional[GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigMostPopularConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1a3a96a03e5d60d424f4822cd35b3183533b6d02989a0b9063f568dcbd4aec4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43b73a1d11ee362a66b1b784231cac97c620baf8c670153b7aac0b0eded00c47(
    value: typing.Optional[GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ca1fa7594577b9e247aa2d7bad99fa889ebb8b4b83943fb080cc0139c369647(
    *,
    context_event_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7245c3e83f71c354f0923624fd8fe55aa2018d7056ea40c9b5e9dc20c6977d08(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__763821ceab2bb45f8d1566d16d485624f5c6fe659fa2c56d4b9f3bf34accb601(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a5a8e3473a3cacb517f5e2c578a35c3d8ab8835d6cb3b70c06d6f1a05249369(
    value: typing.Optional[GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigEngineFeaturesConfigRecommendedForYouConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64556cb8fd5cd21e0162def4f34a977e89fc368320aace84a86df490fa29e62e(
    *,
    target_field: typing.Optional[builtins.str] = None,
    target_field_value_float: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a27b51ad9e4dffcaaac8c6068929dde47d414eb97a15b6d228a7492f0186ce9f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__576a12dc84811997c960e1b6dbbbd4e04b5440b42e9ab0f3553b62942aed599c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4290dac6abb8cde37b6615b74d75a2466c7f4f7e2c817bf2f839e88ea313ccf2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9738a4f964ae2d124f0a0fa923799605e671537eff6858a9a2aa906eabf0456c(
    value: typing.Optional[GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfigOptimizationObjectiveConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8183fcfd18e762629dae420dda51038688cfcad18c501cd2cf6e20dbda7de4a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae75337aff464c9d70f0b86a53bea3ffd3a534ddaa1c367966f1a3e1b1e7ae6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b34b193de291204356e21db424972ffd3fa3644999360b8c541d75fe4cfd640(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9fdf2de0ee4d3dad133b1bb60eea0efee6d00da1a3d657fb408ae37bfdda3e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5be1da7703444fca24009fd546ebc3d5aaeab63b9e106978a50e75fa976f5851(
    value: typing.Optional[GoogleDiscoveryEngineRecommendationEngineMediaRecommendationEngineConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acfc0f234ef8a5195a9bcfb08ca6fae165c24302282032cc95d87815b6abc8a7(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a01f103d2da34539f6c43d842dc0e5f88e84b6b160ce29b6e58d86180e304c6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__555c6f102da45d5af9a194c700c935be2a7c386c753a4a6038e63c0136c9bd06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03a99ae425a25b039f6f87b0960e45832297ffb348bfe161fc8801289b1bd63f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a4f6ef94ed90dc86aa4a506a63638a3a419b1d98f4b641853a33717feae0d68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__251910e39bfa347b09ddbe1dfa996258f9dfb9fa89c6961331f6cab07ab3ac6a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDiscoveryEngineRecommendationEngineTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
