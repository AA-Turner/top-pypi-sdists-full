r'''
# `google_discovery_engine_search_engine`

Refer to the Terraform Registry for docs: [`google_discovery_engine_search_engine`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine).
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


class GoogleDiscoveryEngineSearchEngine(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineSearchEngine.GoogleDiscoveryEngineSearchEngine",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine google_discovery_engine_search_engine}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        collection_id: builtins.str,
        data_store_ids: typing.Sequence[builtins.str],
        display_name: builtins.str,
        engine_id: builtins.str,
        location: builtins.str,
        search_engine_config: typing.Union["GoogleDiscoveryEngineSearchEngineSearchEngineConfig", typing.Dict[builtins.str, typing.Any]],
        common_config: typing.Optional[typing.Union["GoogleDiscoveryEngineSearchEngineCommonConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        industry_vertical: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDiscoveryEngineSearchEngineTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine google_discovery_engine_search_engine} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param collection_id: The collection ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#collection_id GoogleDiscoveryEngineSearchEngine#collection_id}
        :param data_store_ids: The data stores associated with this engine. For SOLUTION_TYPE_SEARCH type of engines, they can only associate with at most one data store. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#data_store_ids GoogleDiscoveryEngineSearchEngine#data_store_ids}
        :param display_name: Required. The display name of the engine. Should be human readable. UTF-8 encoded string with limit of 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#display_name GoogleDiscoveryEngineSearchEngine#display_name}
        :param engine_id: Unique ID to use for Search Engine App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#engine_id GoogleDiscoveryEngineSearchEngine#engine_id}
        :param location: Location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#location GoogleDiscoveryEngineSearchEngine#location}
        :param search_engine_config: search_engine_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#search_engine_config GoogleDiscoveryEngineSearchEngine#search_engine_config}
        :param common_config: common_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#common_config GoogleDiscoveryEngineSearchEngine#common_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#id GoogleDiscoveryEngineSearchEngine#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param industry_vertical: The industry vertical that the engine registers. The restriction of the Engine industry vertical is based on DataStore: If unspecified, default to GENERIC. Vertical on Engine has to match vertical of the DataStore liniked to the engine. Default value: "GENERIC" Possible values: ["GENERIC", "MEDIA", "HEALTHCARE_FHIR"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#industry_vertical GoogleDiscoveryEngineSearchEngine#industry_vertical}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#project GoogleDiscoveryEngineSearchEngine#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#timeouts GoogleDiscoveryEngineSearchEngine#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1aa63b9726a32746d900f87ad0839988145be8b66772cb6c9419760bb6661aa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDiscoveryEngineSearchEngineConfig(
            collection_id=collection_id,
            data_store_ids=data_store_ids,
            display_name=display_name,
            engine_id=engine_id,
            location=location,
            search_engine_config=search_engine_config,
            common_config=common_config,
            id=id,
            industry_vertical=industry_vertical,
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
        '''Generates CDKTF code for importing a GoogleDiscoveryEngineSearchEngine resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDiscoveryEngineSearchEngine to import.
        :param import_from_id: The id of the existing GoogleDiscoveryEngineSearchEngine that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDiscoveryEngineSearchEngine to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbe4f633a39350c9acf61162709705536f7674ffa1eac4a2f07d7e47ca0963e6)
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
        :param company_name: The name of the company, business or entity that is associated with the engine. Setting this may help improve LLM related features.cd Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#company_name GoogleDiscoveryEngineSearchEngine#company_name}
        '''
        value = GoogleDiscoveryEngineSearchEngineCommonConfig(
            company_name=company_name
        )

        return typing.cast(None, jsii.invoke(self, "putCommonConfig", [value]))

    @jsii.member(jsii_name="putSearchEngineConfig")
    def put_search_engine_config(
        self,
        *,
        search_add_ons: typing.Optional[typing.Sequence[builtins.str]] = None,
        search_tier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param search_add_ons: The add-on that this search engine enables. Possible values: ["SEARCH_ADD_ON_LLM"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#search_add_ons GoogleDiscoveryEngineSearchEngine#search_add_ons}
        :param search_tier: The search feature tier of this engine. Defaults to SearchTier.SEARCH_TIER_STANDARD if not specified. Default value: "SEARCH_TIER_STANDARD" Possible values: ["SEARCH_TIER_STANDARD", "SEARCH_TIER_ENTERPRISE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#search_tier GoogleDiscoveryEngineSearchEngine#search_tier}
        '''
        value = GoogleDiscoveryEngineSearchEngineSearchEngineConfig(
            search_add_ons=search_add_ons, search_tier=search_tier
        )

        return typing.cast(None, jsii.invoke(self, "putSearchEngineConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#create GoogleDiscoveryEngineSearchEngine#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#delete GoogleDiscoveryEngineSearchEngine#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#update GoogleDiscoveryEngineSearchEngine#update}.
        '''
        value = GoogleDiscoveryEngineSearchEngineTimeouts(
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
    ) -> "GoogleDiscoveryEngineSearchEngineCommonConfigOutputReference":
        return typing.cast("GoogleDiscoveryEngineSearchEngineCommonConfigOutputReference", jsii.get(self, "commonConfig"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="searchEngineConfig")
    def search_engine_config(
        self,
    ) -> "GoogleDiscoveryEngineSearchEngineSearchEngineConfigOutputReference":
        return typing.cast("GoogleDiscoveryEngineSearchEngineSearchEngineConfigOutputReference", jsii.get(self, "searchEngineConfig"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleDiscoveryEngineSearchEngineTimeoutsOutputReference":
        return typing.cast("GoogleDiscoveryEngineSearchEngineTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="collectionIdInput")
    def collection_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "collectionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="commonConfigInput")
    def common_config_input(
        self,
    ) -> typing.Optional["GoogleDiscoveryEngineSearchEngineCommonConfig"]:
        return typing.cast(typing.Optional["GoogleDiscoveryEngineSearchEngineCommonConfig"], jsii.get(self, "commonConfigInput"))

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
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="searchEngineConfigInput")
    def search_engine_config_input(
        self,
    ) -> typing.Optional["GoogleDiscoveryEngineSearchEngineSearchEngineConfig"]:
        return typing.cast(typing.Optional["GoogleDiscoveryEngineSearchEngineSearchEngineConfig"], jsii.get(self, "searchEngineConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDiscoveryEngineSearchEngineTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDiscoveryEngineSearchEngineTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="collectionId")
    def collection_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "collectionId"))

    @collection_id.setter
    def collection_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14e4dfa5433c6c65e0cafa9a5fd31c6d67381869c54574e38656ea6ebc74b8c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collectionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataStoreIds")
    def data_store_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dataStoreIds"))

    @data_store_ids.setter
    def data_store_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9410f76736c84fdfbf51c3537fc6659dbffbffb840e11e1949f48ef353356eac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataStoreIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e23a27525ddece76dfc61259157b35713d75bc37f77d7a1ac84a2d47e7f1a949)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="engineId")
    def engine_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "engineId"))

    @engine_id.setter
    def engine_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c595446272fda6f08f05c7e2bb57f497bab25816979181a324cddd84ed96b161)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b303adce72cbfa632330ba0b6d13723487689468114f2bcdc10ad56cf319698c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="industryVertical")
    def industry_vertical(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "industryVertical"))

    @industry_vertical.setter
    def industry_vertical(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d412d13482f7a6b76ee2c4df53e040d836d870631fbc7abdb60871fa1644e083)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "industryVertical", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9217654982c644950186dd1e6f7d4e360fefb5e53bdc8b0285a336e09a387da8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84936ed45c8e1e257b4f80dbb72286b2a009c645efa16a576bc1d0e6b22f26e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineSearchEngine.GoogleDiscoveryEngineSearchEngineCommonConfig",
    jsii_struct_bases=[],
    name_mapping={"company_name": "companyName"},
)
class GoogleDiscoveryEngineSearchEngineCommonConfig:
    def __init__(self, *, company_name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param company_name: The name of the company, business or entity that is associated with the engine. Setting this may help improve LLM related features.cd Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#company_name GoogleDiscoveryEngineSearchEngine#company_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c604ef50936dbd85ada722b31b6651b6ac92ec3ddd43d4cf14cea9048322e247)
            check_type(argname="argument company_name", value=company_name, expected_type=type_hints["company_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if company_name is not None:
            self._values["company_name"] = company_name

    @builtins.property
    def company_name(self) -> typing.Optional[builtins.str]:
        '''The name of the company, business or entity that is associated with the engine.

        Setting this may help improve LLM related features.cd

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#company_name GoogleDiscoveryEngineSearchEngine#company_name}
        '''
        result = self._values.get("company_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDiscoveryEngineSearchEngineCommonConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDiscoveryEngineSearchEngineCommonConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineSearchEngine.GoogleDiscoveryEngineSearchEngineCommonConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48fe499b1c4dd5effa21de6d1a9c186628227fd0b2689251c95154f58de0c81d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c99c42f3d241f25c52ed330646c344791ccd7516350e65217be15d74e699cb4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "companyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineSearchEngineCommonConfig]:
        return typing.cast(typing.Optional[GoogleDiscoveryEngineSearchEngineCommonConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDiscoveryEngineSearchEngineCommonConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb24b55da7f4297be8d4c95914f31e509792a98384d8abb945242d966a51d80a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineSearchEngine.GoogleDiscoveryEngineSearchEngineConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "collection_id": "collectionId",
        "data_store_ids": "dataStoreIds",
        "display_name": "displayName",
        "engine_id": "engineId",
        "location": "location",
        "search_engine_config": "searchEngineConfig",
        "common_config": "commonConfig",
        "id": "id",
        "industry_vertical": "industryVertical",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class GoogleDiscoveryEngineSearchEngineConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        collection_id: builtins.str,
        data_store_ids: typing.Sequence[builtins.str],
        display_name: builtins.str,
        engine_id: builtins.str,
        location: builtins.str,
        search_engine_config: typing.Union["GoogleDiscoveryEngineSearchEngineSearchEngineConfig", typing.Dict[builtins.str, typing.Any]],
        common_config: typing.Optional[typing.Union[GoogleDiscoveryEngineSearchEngineCommonConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        industry_vertical: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDiscoveryEngineSearchEngineTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param collection_id: The collection ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#collection_id GoogleDiscoveryEngineSearchEngine#collection_id}
        :param data_store_ids: The data stores associated with this engine. For SOLUTION_TYPE_SEARCH type of engines, they can only associate with at most one data store. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#data_store_ids GoogleDiscoveryEngineSearchEngine#data_store_ids}
        :param display_name: Required. The display name of the engine. Should be human readable. UTF-8 encoded string with limit of 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#display_name GoogleDiscoveryEngineSearchEngine#display_name}
        :param engine_id: Unique ID to use for Search Engine App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#engine_id GoogleDiscoveryEngineSearchEngine#engine_id}
        :param location: Location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#location GoogleDiscoveryEngineSearchEngine#location}
        :param search_engine_config: search_engine_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#search_engine_config GoogleDiscoveryEngineSearchEngine#search_engine_config}
        :param common_config: common_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#common_config GoogleDiscoveryEngineSearchEngine#common_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#id GoogleDiscoveryEngineSearchEngine#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param industry_vertical: The industry vertical that the engine registers. The restriction of the Engine industry vertical is based on DataStore: If unspecified, default to GENERIC. Vertical on Engine has to match vertical of the DataStore liniked to the engine. Default value: "GENERIC" Possible values: ["GENERIC", "MEDIA", "HEALTHCARE_FHIR"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#industry_vertical GoogleDiscoveryEngineSearchEngine#industry_vertical}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#project GoogleDiscoveryEngineSearchEngine#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#timeouts GoogleDiscoveryEngineSearchEngine#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(search_engine_config, dict):
            search_engine_config = GoogleDiscoveryEngineSearchEngineSearchEngineConfig(**search_engine_config)
        if isinstance(common_config, dict):
            common_config = GoogleDiscoveryEngineSearchEngineCommonConfig(**common_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleDiscoveryEngineSearchEngineTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b248c42fbb03043e620b3d9ca885518c69a909d2525391deff974dda6fe90059)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument collection_id", value=collection_id, expected_type=type_hints["collection_id"])
            check_type(argname="argument data_store_ids", value=data_store_ids, expected_type=type_hints["data_store_ids"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument engine_id", value=engine_id, expected_type=type_hints["engine_id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument search_engine_config", value=search_engine_config, expected_type=type_hints["search_engine_config"])
            check_type(argname="argument common_config", value=common_config, expected_type=type_hints["common_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument industry_vertical", value=industry_vertical, expected_type=type_hints["industry_vertical"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "collection_id": collection_id,
            "data_store_ids": data_store_ids,
            "display_name": display_name,
            "engine_id": engine_id,
            "location": location,
            "search_engine_config": search_engine_config,
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
    def collection_id(self) -> builtins.str:
        '''The collection ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#collection_id GoogleDiscoveryEngineSearchEngine#collection_id}
        '''
        result = self._values.get("collection_id")
        assert result is not None, "Required property 'collection_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_store_ids(self) -> typing.List[builtins.str]:
        '''The data stores associated with this engine.

        For SOLUTION_TYPE_SEARCH type of engines, they can only associate with at most one data store.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#data_store_ids GoogleDiscoveryEngineSearchEngine#data_store_ids}
        '''
        result = self._values.get("data_store_ids")
        assert result is not None, "Required property 'data_store_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''Required. The display name of the engine. Should be human readable. UTF-8 encoded string with limit of 1024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#display_name GoogleDiscoveryEngineSearchEngine#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def engine_id(self) -> builtins.str:
        '''Unique ID to use for Search Engine App.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#engine_id GoogleDiscoveryEngineSearchEngine#engine_id}
        '''
        result = self._values.get("engine_id")
        assert result is not None, "Required property 'engine_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Location.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#location GoogleDiscoveryEngineSearchEngine#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def search_engine_config(
        self,
    ) -> "GoogleDiscoveryEngineSearchEngineSearchEngineConfig":
        '''search_engine_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#search_engine_config GoogleDiscoveryEngineSearchEngine#search_engine_config}
        '''
        result = self._values.get("search_engine_config")
        assert result is not None, "Required property 'search_engine_config' is missing"
        return typing.cast("GoogleDiscoveryEngineSearchEngineSearchEngineConfig", result)

    @builtins.property
    def common_config(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineSearchEngineCommonConfig]:
        '''common_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#common_config GoogleDiscoveryEngineSearchEngine#common_config}
        '''
        result = self._values.get("common_config")
        return typing.cast(typing.Optional[GoogleDiscoveryEngineSearchEngineCommonConfig], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#id GoogleDiscoveryEngineSearchEngine#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def industry_vertical(self) -> typing.Optional[builtins.str]:
        '''The industry vertical that the engine registers.

        The restriction of the Engine industry vertical is based on DataStore: If unspecified, default to GENERIC. Vertical on Engine has to match vertical of the DataStore liniked to the engine. Default value: "GENERIC" Possible values: ["GENERIC", "MEDIA", "HEALTHCARE_FHIR"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#industry_vertical GoogleDiscoveryEngineSearchEngine#industry_vertical}
        '''
        result = self._values.get("industry_vertical")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#project GoogleDiscoveryEngineSearchEngine#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleDiscoveryEngineSearchEngineTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#timeouts GoogleDiscoveryEngineSearchEngine#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleDiscoveryEngineSearchEngineTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDiscoveryEngineSearchEngineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineSearchEngine.GoogleDiscoveryEngineSearchEngineSearchEngineConfig",
    jsii_struct_bases=[],
    name_mapping={"search_add_ons": "searchAddOns", "search_tier": "searchTier"},
)
class GoogleDiscoveryEngineSearchEngineSearchEngineConfig:
    def __init__(
        self,
        *,
        search_add_ons: typing.Optional[typing.Sequence[builtins.str]] = None,
        search_tier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param search_add_ons: The add-on that this search engine enables. Possible values: ["SEARCH_ADD_ON_LLM"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#search_add_ons GoogleDiscoveryEngineSearchEngine#search_add_ons}
        :param search_tier: The search feature tier of this engine. Defaults to SearchTier.SEARCH_TIER_STANDARD if not specified. Default value: "SEARCH_TIER_STANDARD" Possible values: ["SEARCH_TIER_STANDARD", "SEARCH_TIER_ENTERPRISE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#search_tier GoogleDiscoveryEngineSearchEngine#search_tier}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b3475b9489e924e9d737f11a220f13b0d54bfcef6ea59ce8b963d721121b17e)
            check_type(argname="argument search_add_ons", value=search_add_ons, expected_type=type_hints["search_add_ons"])
            check_type(argname="argument search_tier", value=search_tier, expected_type=type_hints["search_tier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if search_add_ons is not None:
            self._values["search_add_ons"] = search_add_ons
        if search_tier is not None:
            self._values["search_tier"] = search_tier

    @builtins.property
    def search_add_ons(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The add-on that this search engine enables. Possible values: ["SEARCH_ADD_ON_LLM"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#search_add_ons GoogleDiscoveryEngineSearchEngine#search_add_ons}
        '''
        result = self._values.get("search_add_ons")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def search_tier(self) -> typing.Optional[builtins.str]:
        '''The search feature tier of this engine.

        Defaults to SearchTier.SEARCH_TIER_STANDARD if not specified. Default value: "SEARCH_TIER_STANDARD" Possible values: ["SEARCH_TIER_STANDARD", "SEARCH_TIER_ENTERPRISE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#search_tier GoogleDiscoveryEngineSearchEngine#search_tier}
        '''
        result = self._values.get("search_tier")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDiscoveryEngineSearchEngineSearchEngineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDiscoveryEngineSearchEngineSearchEngineConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineSearchEngine.GoogleDiscoveryEngineSearchEngineSearchEngineConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5a2f19f2bc5285f24eb1ffc9ae985f3222aa31fd444c3872194c19135beb89a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSearchAddOns")
    def reset_search_add_ons(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSearchAddOns", []))

    @jsii.member(jsii_name="resetSearchTier")
    def reset_search_tier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSearchTier", []))

    @builtins.property
    @jsii.member(jsii_name="searchAddOnsInput")
    def search_add_ons_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "searchAddOnsInput"))

    @builtins.property
    @jsii.member(jsii_name="searchTierInput")
    def search_tier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "searchTierInput"))

    @builtins.property
    @jsii.member(jsii_name="searchAddOns")
    def search_add_ons(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "searchAddOns"))

    @search_add_ons.setter
    def search_add_ons(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa59b766064240dd490a1de8e9bcd8fd6154b7d69336d107a19652e5fa28d7ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "searchAddOns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="searchTier")
    def search_tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "searchTier"))

    @search_tier.setter
    def search_tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72e5e54880ffe324ee044e17a4ac204360597b4014ba7db94a863bc8e85b594b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "searchTier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineSearchEngineSearchEngineConfig]:
        return typing.cast(typing.Optional[GoogleDiscoveryEngineSearchEngineSearchEngineConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDiscoveryEngineSearchEngineSearchEngineConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0435321588e91906ba49a955cf9b5458473c1cd253289ca3086d0760a91a469)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineSearchEngine.GoogleDiscoveryEngineSearchEngineTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleDiscoveryEngineSearchEngineTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#create GoogleDiscoveryEngineSearchEngine#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#delete GoogleDiscoveryEngineSearchEngine#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#update GoogleDiscoveryEngineSearchEngine#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__228c0f113cbd69a297d5a446af104686b4aae1bdc98784399743d3fe3e823706)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#create GoogleDiscoveryEngineSearchEngine#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#delete GoogleDiscoveryEngineSearchEngine#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_search_engine#update GoogleDiscoveryEngineSearchEngine#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDiscoveryEngineSearchEngineTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDiscoveryEngineSearchEngineTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineSearchEngine.GoogleDiscoveryEngineSearchEngineTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab5e5067da212eb9d595bad04480acc4bddc7e05f3d44ea45c8c2816bc084481)
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
            type_hints = typing.get_type_hints(_typecheckingstub__428f4ee306fe427b04e0a4cf400883280b02e9cc515a32c0e769b377bc5f8733)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18818ed0446e2ae5db03941e896dc11413c91d82d85735217120d354bf174f8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d991ae3eb85a172fad7af0f9c3c6d197273f87a7a66ef45d3dbdab4ea07d241)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDiscoveryEngineSearchEngineTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDiscoveryEngineSearchEngineTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDiscoveryEngineSearchEngineTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e812aaa3dcefb1a6ed19fcdfe003de19296d0e8f9ee6f863d2708ca298835146)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleDiscoveryEngineSearchEngine",
    "GoogleDiscoveryEngineSearchEngineCommonConfig",
    "GoogleDiscoveryEngineSearchEngineCommonConfigOutputReference",
    "GoogleDiscoveryEngineSearchEngineConfig",
    "GoogleDiscoveryEngineSearchEngineSearchEngineConfig",
    "GoogleDiscoveryEngineSearchEngineSearchEngineConfigOutputReference",
    "GoogleDiscoveryEngineSearchEngineTimeouts",
    "GoogleDiscoveryEngineSearchEngineTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__d1aa63b9726a32746d900f87ad0839988145be8b66772cb6c9419760bb6661aa(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    collection_id: builtins.str,
    data_store_ids: typing.Sequence[builtins.str],
    display_name: builtins.str,
    engine_id: builtins.str,
    location: builtins.str,
    search_engine_config: typing.Union[GoogleDiscoveryEngineSearchEngineSearchEngineConfig, typing.Dict[builtins.str, typing.Any]],
    common_config: typing.Optional[typing.Union[GoogleDiscoveryEngineSearchEngineCommonConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    industry_vertical: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDiscoveryEngineSearchEngineTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__bbe4f633a39350c9acf61162709705536f7674ffa1eac4a2f07d7e47ca0963e6(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14e4dfa5433c6c65e0cafa9a5fd31c6d67381869c54574e38656ea6ebc74b8c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9410f76736c84fdfbf51c3537fc6659dbffbffb840e11e1949f48ef353356eac(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e23a27525ddece76dfc61259157b35713d75bc37f77d7a1ac84a2d47e7f1a949(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c595446272fda6f08f05c7e2bb57f497bab25816979181a324cddd84ed96b161(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b303adce72cbfa632330ba0b6d13723487689468114f2bcdc10ad56cf319698c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d412d13482f7a6b76ee2c4df53e040d836d870631fbc7abdb60871fa1644e083(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9217654982c644950186dd1e6f7d4e360fefb5e53bdc8b0285a336e09a387da8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84936ed45c8e1e257b4f80dbb72286b2a009c645efa16a576bc1d0e6b22f26e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c604ef50936dbd85ada722b31b6651b6ac92ec3ddd43d4cf14cea9048322e247(
    *,
    company_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48fe499b1c4dd5effa21de6d1a9c186628227fd0b2689251c95154f58de0c81d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c99c42f3d241f25c52ed330646c344791ccd7516350e65217be15d74e699cb4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb24b55da7f4297be8d4c95914f31e509792a98384d8abb945242d966a51d80a(
    value: typing.Optional[GoogleDiscoveryEngineSearchEngineCommonConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b248c42fbb03043e620b3d9ca885518c69a909d2525391deff974dda6fe90059(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    collection_id: builtins.str,
    data_store_ids: typing.Sequence[builtins.str],
    display_name: builtins.str,
    engine_id: builtins.str,
    location: builtins.str,
    search_engine_config: typing.Union[GoogleDiscoveryEngineSearchEngineSearchEngineConfig, typing.Dict[builtins.str, typing.Any]],
    common_config: typing.Optional[typing.Union[GoogleDiscoveryEngineSearchEngineCommonConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    industry_vertical: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDiscoveryEngineSearchEngineTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b3475b9489e924e9d737f11a220f13b0d54bfcef6ea59ce8b963d721121b17e(
    *,
    search_add_ons: typing.Optional[typing.Sequence[builtins.str]] = None,
    search_tier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5a2f19f2bc5285f24eb1ffc9ae985f3222aa31fd444c3872194c19135beb89a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa59b766064240dd490a1de8e9bcd8fd6154b7d69336d107a19652e5fa28d7ff(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72e5e54880ffe324ee044e17a4ac204360597b4014ba7db94a863bc8e85b594b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0435321588e91906ba49a955cf9b5458473c1cd253289ca3086d0760a91a469(
    value: typing.Optional[GoogleDiscoveryEngineSearchEngineSearchEngineConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__228c0f113cbd69a297d5a446af104686b4aae1bdc98784399743d3fe3e823706(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab5e5067da212eb9d595bad04480acc4bddc7e05f3d44ea45c8c2816bc084481(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__428f4ee306fe427b04e0a4cf400883280b02e9cc515a32c0e769b377bc5f8733(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18818ed0446e2ae5db03941e896dc11413c91d82d85735217120d354bf174f8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d991ae3eb85a172fad7af0f9c3c6d197273f87a7a66ef45d3dbdab4ea07d241(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e812aaa3dcefb1a6ed19fcdfe003de19296d0e8f9ee6f863d2708ca298835146(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDiscoveryEngineSearchEngineTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
