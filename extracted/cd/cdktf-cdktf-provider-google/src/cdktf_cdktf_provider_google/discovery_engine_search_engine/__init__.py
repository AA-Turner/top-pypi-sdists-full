r'''
# `google_discovery_engine_search_engine`

Refer to the Terraform Registry for docs: [`google_discovery_engine_search_engine`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine).
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


class DiscoveryEngineSearchEngine(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.discoveryEngineSearchEngine.DiscoveryEngineSearchEngine",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine google_discovery_engine_search_engine}.'''

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
        search_engine_config: typing.Union["DiscoveryEngineSearchEngineSearchEngineConfig", typing.Dict[builtins.str, typing.Any]],
        common_config: typing.Optional[typing.Union["DiscoveryEngineSearchEngineCommonConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        industry_vertical: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DiscoveryEngineSearchEngineTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine google_discovery_engine_search_engine} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param collection_id: The collection ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#collection_id DiscoveryEngineSearchEngine#collection_id}
        :param data_store_ids: The data stores associated with this engine. For SOLUTION_TYPE_SEARCH type of engines, they can only associate with at most one data store. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#data_store_ids DiscoveryEngineSearchEngine#data_store_ids}
        :param display_name: Required. The display name of the engine. Should be human readable. UTF-8 encoded string with limit of 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#display_name DiscoveryEngineSearchEngine#display_name}
        :param engine_id: Unique ID to use for Search Engine App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#engine_id DiscoveryEngineSearchEngine#engine_id}
        :param location: Location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#location DiscoveryEngineSearchEngine#location}
        :param search_engine_config: search_engine_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#search_engine_config DiscoveryEngineSearchEngine#search_engine_config}
        :param common_config: common_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#common_config DiscoveryEngineSearchEngine#common_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#id DiscoveryEngineSearchEngine#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param industry_vertical: The industry vertical that the engine registers. The restriction of the Engine industry vertical is based on DataStore: If unspecified, default to GENERIC. Vertical on Engine has to match vertical of the DataStore liniked to the engine. Default value: "GENERIC" Possible values: ["GENERIC", "MEDIA", "HEALTHCARE_FHIR"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#industry_vertical DiscoveryEngineSearchEngine#industry_vertical}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#project DiscoveryEngineSearchEngine#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#timeouts DiscoveryEngineSearchEngine#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b9bd503df182d57738bd3ecaf006546f1b3173b2cf069fee867b39bd920f016)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DiscoveryEngineSearchEngineConfig(
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
        '''Generates CDKTF code for importing a DiscoveryEngineSearchEngine resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DiscoveryEngineSearchEngine to import.
        :param import_from_id: The id of the existing DiscoveryEngineSearchEngine that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DiscoveryEngineSearchEngine to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2729f29d92df380cd315c29b5fe981206d3ddba31bd6312308b5a9a0f310130a)
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
        :param company_name: The name of the company, business or entity that is associated with the engine. Setting this may help improve LLM related features.cd Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#company_name DiscoveryEngineSearchEngine#company_name}
        '''
        value = DiscoveryEngineSearchEngineCommonConfig(company_name=company_name)

        return typing.cast(None, jsii.invoke(self, "putCommonConfig", [value]))

    @jsii.member(jsii_name="putSearchEngineConfig")
    def put_search_engine_config(
        self,
        *,
        search_add_ons: typing.Optional[typing.Sequence[builtins.str]] = None,
        search_tier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param search_add_ons: The add-on that this search engine enables. Possible values: ["SEARCH_ADD_ON_LLM"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#search_add_ons DiscoveryEngineSearchEngine#search_add_ons}
        :param search_tier: The search feature tier of this engine. Defaults to SearchTier.SEARCH_TIER_STANDARD if not specified. Default value: "SEARCH_TIER_STANDARD" Possible values: ["SEARCH_TIER_STANDARD", "SEARCH_TIER_ENTERPRISE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#search_tier DiscoveryEngineSearchEngine#search_tier}
        '''
        value = DiscoveryEngineSearchEngineSearchEngineConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#create DiscoveryEngineSearchEngine#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#delete DiscoveryEngineSearchEngine#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#update DiscoveryEngineSearchEngine#update}.
        '''
        value = DiscoveryEngineSearchEngineTimeouts(
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
    def common_config(self) -> "DiscoveryEngineSearchEngineCommonConfigOutputReference":
        return typing.cast("DiscoveryEngineSearchEngineCommonConfigOutputReference", jsii.get(self, "commonConfig"))

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
    ) -> "DiscoveryEngineSearchEngineSearchEngineConfigOutputReference":
        return typing.cast("DiscoveryEngineSearchEngineSearchEngineConfigOutputReference", jsii.get(self, "searchEngineConfig"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DiscoveryEngineSearchEngineTimeoutsOutputReference":
        return typing.cast("DiscoveryEngineSearchEngineTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["DiscoveryEngineSearchEngineCommonConfig"]:
        return typing.cast(typing.Optional["DiscoveryEngineSearchEngineCommonConfig"], jsii.get(self, "commonConfigInput"))

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
    ) -> typing.Optional["DiscoveryEngineSearchEngineSearchEngineConfig"]:
        return typing.cast(typing.Optional["DiscoveryEngineSearchEngineSearchEngineConfig"], jsii.get(self, "searchEngineConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DiscoveryEngineSearchEngineTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DiscoveryEngineSearchEngineTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="collectionId")
    def collection_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "collectionId"))

    @collection_id.setter
    def collection_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e7bdfac82b781dffb11355060b0b3a8665c463e3e33a77b6a3eebe4e747d19b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collectionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataStoreIds")
    def data_store_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dataStoreIds"))

    @data_store_ids.setter
    def data_store_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dd3ae46ace6d02f21ffc8b30e3808017100badd45cf2068b163b8047a976bd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataStoreIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df1e93ea770ba9d9d88ab52414810108a23d75c922d7826b62e9a648939d4de0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="engineId")
    def engine_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "engineId"))

    @engine_id.setter
    def engine_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf41167e0c812ff420976b9b553d290c1e58e781aeee195232c28c1783e6011a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa2a93da3a0c471143f94b9f28b441913e550a4387a600b243ebfe9f8bcd0dec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="industryVertical")
    def industry_vertical(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "industryVertical"))

    @industry_vertical.setter
    def industry_vertical(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c6b1f3b65eb20dd54b71649675aeff0935eb2253d3d9f278fbfd0c80766cf36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "industryVertical", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcb4d7fc1b0b43af4fcebbf7283b594b0683e436632c29d298d00b54cba571b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9753fd00a58f3f9e82e8215efa6ae1ab2a6e90a6e51361e82d90883ffa7b8e5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.discoveryEngineSearchEngine.DiscoveryEngineSearchEngineCommonConfig",
    jsii_struct_bases=[],
    name_mapping={"company_name": "companyName"},
)
class DiscoveryEngineSearchEngineCommonConfig:
    def __init__(self, *, company_name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param company_name: The name of the company, business or entity that is associated with the engine. Setting this may help improve LLM related features.cd Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#company_name DiscoveryEngineSearchEngine#company_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97ac6b8da9e6d91cbc55e0af655e6b4b3539254e25d85f8ae283ef3ec8a4a12f)
            check_type(argname="argument company_name", value=company_name, expected_type=type_hints["company_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if company_name is not None:
            self._values["company_name"] = company_name

    @builtins.property
    def company_name(self) -> typing.Optional[builtins.str]:
        '''The name of the company, business or entity that is associated with the engine.

        Setting this may help improve LLM related features.cd

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#company_name DiscoveryEngineSearchEngine#company_name}
        '''
        result = self._values.get("company_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiscoveryEngineSearchEngineCommonConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DiscoveryEngineSearchEngineCommonConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.discoveryEngineSearchEngine.DiscoveryEngineSearchEngineCommonConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb3b1c67f288d05b0fda854b8ba83ab80659e82f7075e8c7449a31c6aff8980b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6fbbd817da7d6080f9e5c0784f5957f29f073098803b213ad013c33d9a3a1db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "companyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DiscoveryEngineSearchEngineCommonConfig]:
        return typing.cast(typing.Optional[DiscoveryEngineSearchEngineCommonConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DiscoveryEngineSearchEngineCommonConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__affb5b9d96da2cc76453c00d18f8ad5c9a01607936cff514c984f4b22c27e033)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.discoveryEngineSearchEngine.DiscoveryEngineSearchEngineConfig",
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
class DiscoveryEngineSearchEngineConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        search_engine_config: typing.Union["DiscoveryEngineSearchEngineSearchEngineConfig", typing.Dict[builtins.str, typing.Any]],
        common_config: typing.Optional[typing.Union[DiscoveryEngineSearchEngineCommonConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        industry_vertical: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DiscoveryEngineSearchEngineTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param collection_id: The collection ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#collection_id DiscoveryEngineSearchEngine#collection_id}
        :param data_store_ids: The data stores associated with this engine. For SOLUTION_TYPE_SEARCH type of engines, they can only associate with at most one data store. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#data_store_ids DiscoveryEngineSearchEngine#data_store_ids}
        :param display_name: Required. The display name of the engine. Should be human readable. UTF-8 encoded string with limit of 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#display_name DiscoveryEngineSearchEngine#display_name}
        :param engine_id: Unique ID to use for Search Engine App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#engine_id DiscoveryEngineSearchEngine#engine_id}
        :param location: Location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#location DiscoveryEngineSearchEngine#location}
        :param search_engine_config: search_engine_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#search_engine_config DiscoveryEngineSearchEngine#search_engine_config}
        :param common_config: common_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#common_config DiscoveryEngineSearchEngine#common_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#id DiscoveryEngineSearchEngine#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param industry_vertical: The industry vertical that the engine registers. The restriction of the Engine industry vertical is based on DataStore: If unspecified, default to GENERIC. Vertical on Engine has to match vertical of the DataStore liniked to the engine. Default value: "GENERIC" Possible values: ["GENERIC", "MEDIA", "HEALTHCARE_FHIR"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#industry_vertical DiscoveryEngineSearchEngine#industry_vertical}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#project DiscoveryEngineSearchEngine#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#timeouts DiscoveryEngineSearchEngine#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(search_engine_config, dict):
            search_engine_config = DiscoveryEngineSearchEngineSearchEngineConfig(**search_engine_config)
        if isinstance(common_config, dict):
            common_config = DiscoveryEngineSearchEngineCommonConfig(**common_config)
        if isinstance(timeouts, dict):
            timeouts = DiscoveryEngineSearchEngineTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f22a0da8be6b181f9d3de06569b5388204aa68a0dabd92a59f925fc34660eb87)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#collection_id DiscoveryEngineSearchEngine#collection_id}
        '''
        result = self._values.get("collection_id")
        assert result is not None, "Required property 'collection_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_store_ids(self) -> typing.List[builtins.str]:
        '''The data stores associated with this engine.

        For SOLUTION_TYPE_SEARCH type of engines, they can only associate with at most one data store.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#data_store_ids DiscoveryEngineSearchEngine#data_store_ids}
        '''
        result = self._values.get("data_store_ids")
        assert result is not None, "Required property 'data_store_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''Required. The display name of the engine. Should be human readable. UTF-8 encoded string with limit of 1024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#display_name DiscoveryEngineSearchEngine#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def engine_id(self) -> builtins.str:
        '''Unique ID to use for Search Engine App.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#engine_id DiscoveryEngineSearchEngine#engine_id}
        '''
        result = self._values.get("engine_id")
        assert result is not None, "Required property 'engine_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Location.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#location DiscoveryEngineSearchEngine#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def search_engine_config(self) -> "DiscoveryEngineSearchEngineSearchEngineConfig":
        '''search_engine_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#search_engine_config DiscoveryEngineSearchEngine#search_engine_config}
        '''
        result = self._values.get("search_engine_config")
        assert result is not None, "Required property 'search_engine_config' is missing"
        return typing.cast("DiscoveryEngineSearchEngineSearchEngineConfig", result)

    @builtins.property
    def common_config(self) -> typing.Optional[DiscoveryEngineSearchEngineCommonConfig]:
        '''common_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#common_config DiscoveryEngineSearchEngine#common_config}
        '''
        result = self._values.get("common_config")
        return typing.cast(typing.Optional[DiscoveryEngineSearchEngineCommonConfig], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#id DiscoveryEngineSearchEngine#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def industry_vertical(self) -> typing.Optional[builtins.str]:
        '''The industry vertical that the engine registers.

        The restriction of the Engine industry vertical is based on DataStore: If unspecified, default to GENERIC. Vertical on Engine has to match vertical of the DataStore liniked to the engine. Default value: "GENERIC" Possible values: ["GENERIC", "MEDIA", "HEALTHCARE_FHIR"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#industry_vertical DiscoveryEngineSearchEngine#industry_vertical}
        '''
        result = self._values.get("industry_vertical")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#project DiscoveryEngineSearchEngine#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DiscoveryEngineSearchEngineTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#timeouts DiscoveryEngineSearchEngine#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DiscoveryEngineSearchEngineTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiscoveryEngineSearchEngineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.discoveryEngineSearchEngine.DiscoveryEngineSearchEngineSearchEngineConfig",
    jsii_struct_bases=[],
    name_mapping={"search_add_ons": "searchAddOns", "search_tier": "searchTier"},
)
class DiscoveryEngineSearchEngineSearchEngineConfig:
    def __init__(
        self,
        *,
        search_add_ons: typing.Optional[typing.Sequence[builtins.str]] = None,
        search_tier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param search_add_ons: The add-on that this search engine enables. Possible values: ["SEARCH_ADD_ON_LLM"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#search_add_ons DiscoveryEngineSearchEngine#search_add_ons}
        :param search_tier: The search feature tier of this engine. Defaults to SearchTier.SEARCH_TIER_STANDARD if not specified. Default value: "SEARCH_TIER_STANDARD" Possible values: ["SEARCH_TIER_STANDARD", "SEARCH_TIER_ENTERPRISE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#search_tier DiscoveryEngineSearchEngine#search_tier}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8642692fb6bdf62cd287c1f1ff5f362d6efe8f09fa2875216bdb99c13e4131f4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#search_add_ons DiscoveryEngineSearchEngine#search_add_ons}
        '''
        result = self._values.get("search_add_ons")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def search_tier(self) -> typing.Optional[builtins.str]:
        '''The search feature tier of this engine.

        Defaults to SearchTier.SEARCH_TIER_STANDARD if not specified. Default value: "SEARCH_TIER_STANDARD" Possible values: ["SEARCH_TIER_STANDARD", "SEARCH_TIER_ENTERPRISE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#search_tier DiscoveryEngineSearchEngine#search_tier}
        '''
        result = self._values.get("search_tier")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiscoveryEngineSearchEngineSearchEngineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DiscoveryEngineSearchEngineSearchEngineConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.discoveryEngineSearchEngine.DiscoveryEngineSearchEngineSearchEngineConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1dd4563e2a97903c2225ae2f4735e206dddef74c7a46e73c3dba88bff5f50487)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee2552bc395b97df314b07581e0c489bec32d3f2d8322e336fc722fe11390a14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "searchAddOns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="searchTier")
    def search_tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "searchTier"))

    @search_tier.setter
    def search_tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4765460d7c5eb78e0833bc06735b2b41f3787f1da217b3713d12bf78d52f7d29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "searchTier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DiscoveryEngineSearchEngineSearchEngineConfig]:
        return typing.cast(typing.Optional[DiscoveryEngineSearchEngineSearchEngineConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DiscoveryEngineSearchEngineSearchEngineConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c54c5d6013724495094c82b99528cc43cddf31550d9620f96a2c85adc27b5d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.discoveryEngineSearchEngine.DiscoveryEngineSearchEngineTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DiscoveryEngineSearchEngineTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#create DiscoveryEngineSearchEngine#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#delete DiscoveryEngineSearchEngine#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#update DiscoveryEngineSearchEngine#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b88a904e1c7b92ee6a16b58b3fcb25dbbd51fd3512483cbfe3025956217c416)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#create DiscoveryEngineSearchEngine#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#delete DiscoveryEngineSearchEngine#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_search_engine#update DiscoveryEngineSearchEngine#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiscoveryEngineSearchEngineTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DiscoveryEngineSearchEngineTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.discoveryEngineSearchEngine.DiscoveryEngineSearchEngineTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97dec53863d6deb98cc0e8cbc77c4acdd058bf396caf54127553815fb07a7aae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6769b1cde93af57b6a2bcf8b3b3fe2f09f217f0b160e2ef9555aced59fd7729)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55f4870167c7f1533449310ea0481bc830f0691fe5d582885e262a818c6340a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f173a1867bdcdf0808f8a99916a399b909ed5bf9e3cdad4f13f8c9f05839eec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DiscoveryEngineSearchEngineTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DiscoveryEngineSearchEngineTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DiscoveryEngineSearchEngineTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7b0fc850aca6be858f66f7113bcb689d44fe1ac2db3dffc05255a513caae6d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DiscoveryEngineSearchEngine",
    "DiscoveryEngineSearchEngineCommonConfig",
    "DiscoveryEngineSearchEngineCommonConfigOutputReference",
    "DiscoveryEngineSearchEngineConfig",
    "DiscoveryEngineSearchEngineSearchEngineConfig",
    "DiscoveryEngineSearchEngineSearchEngineConfigOutputReference",
    "DiscoveryEngineSearchEngineTimeouts",
    "DiscoveryEngineSearchEngineTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__3b9bd503df182d57738bd3ecaf006546f1b3173b2cf069fee867b39bd920f016(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    collection_id: builtins.str,
    data_store_ids: typing.Sequence[builtins.str],
    display_name: builtins.str,
    engine_id: builtins.str,
    location: builtins.str,
    search_engine_config: typing.Union[DiscoveryEngineSearchEngineSearchEngineConfig, typing.Dict[builtins.str, typing.Any]],
    common_config: typing.Optional[typing.Union[DiscoveryEngineSearchEngineCommonConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    industry_vertical: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DiscoveryEngineSearchEngineTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__2729f29d92df380cd315c29b5fe981206d3ddba31bd6312308b5a9a0f310130a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e7bdfac82b781dffb11355060b0b3a8665c463e3e33a77b6a3eebe4e747d19b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dd3ae46ace6d02f21ffc8b30e3808017100badd45cf2068b163b8047a976bd7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df1e93ea770ba9d9d88ab52414810108a23d75c922d7826b62e9a648939d4de0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf41167e0c812ff420976b9b553d290c1e58e781aeee195232c28c1783e6011a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa2a93da3a0c471143f94b9f28b441913e550a4387a600b243ebfe9f8bcd0dec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c6b1f3b65eb20dd54b71649675aeff0935eb2253d3d9f278fbfd0c80766cf36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcb4d7fc1b0b43af4fcebbf7283b594b0683e436632c29d298d00b54cba571b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9753fd00a58f3f9e82e8215efa6ae1ab2a6e90a6e51361e82d90883ffa7b8e5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97ac6b8da9e6d91cbc55e0af655e6b4b3539254e25d85f8ae283ef3ec8a4a12f(
    *,
    company_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb3b1c67f288d05b0fda854b8ba83ab80659e82f7075e8c7449a31c6aff8980b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6fbbd817da7d6080f9e5c0784f5957f29f073098803b213ad013c33d9a3a1db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__affb5b9d96da2cc76453c00d18f8ad5c9a01607936cff514c984f4b22c27e033(
    value: typing.Optional[DiscoveryEngineSearchEngineCommonConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f22a0da8be6b181f9d3de06569b5388204aa68a0dabd92a59f925fc34660eb87(
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
    search_engine_config: typing.Union[DiscoveryEngineSearchEngineSearchEngineConfig, typing.Dict[builtins.str, typing.Any]],
    common_config: typing.Optional[typing.Union[DiscoveryEngineSearchEngineCommonConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    industry_vertical: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DiscoveryEngineSearchEngineTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8642692fb6bdf62cd287c1f1ff5f362d6efe8f09fa2875216bdb99c13e4131f4(
    *,
    search_add_ons: typing.Optional[typing.Sequence[builtins.str]] = None,
    search_tier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dd4563e2a97903c2225ae2f4735e206dddef74c7a46e73c3dba88bff5f50487(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee2552bc395b97df314b07581e0c489bec32d3f2d8322e336fc722fe11390a14(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4765460d7c5eb78e0833bc06735b2b41f3787f1da217b3713d12bf78d52f7d29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c54c5d6013724495094c82b99528cc43cddf31550d9620f96a2c85adc27b5d2(
    value: typing.Optional[DiscoveryEngineSearchEngineSearchEngineConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b88a904e1c7b92ee6a16b58b3fcb25dbbd51fd3512483cbfe3025956217c416(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97dec53863d6deb98cc0e8cbc77c4acdd058bf396caf54127553815fb07a7aae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6769b1cde93af57b6a2bcf8b3b3fe2f09f217f0b160e2ef9555aced59fd7729(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55f4870167c7f1533449310ea0481bc830f0691fe5d582885e262a818c6340a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f173a1867bdcdf0808f8a99916a399b909ed5bf9e3cdad4f13f8c9f05839eec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7b0fc850aca6be858f66f7113bcb689d44fe1ac2db3dffc05255a513caae6d1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DiscoveryEngineSearchEngineTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
