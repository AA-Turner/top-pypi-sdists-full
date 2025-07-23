r'''
# `google_discovery_engine_chat_engine`

Refer to the Terraform Registry for docs: [`google_discovery_engine_chat_engine`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine).
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


class DiscoveryEngineChatEngine(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.discoveryEngineChatEngine.DiscoveryEngineChatEngine",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine google_discovery_engine_chat_engine}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        chat_engine_config: typing.Union["DiscoveryEngineChatEngineChatEngineConfig", typing.Dict[builtins.str, typing.Any]],
        collection_id: builtins.str,
        data_store_ids: typing.Sequence[builtins.str],
        display_name: builtins.str,
        engine_id: builtins.str,
        location: builtins.str,
        common_config: typing.Optional[typing.Union["DiscoveryEngineChatEngineCommonConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        industry_vertical: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DiscoveryEngineChatEngineTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine google_discovery_engine_chat_engine} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param chat_engine_config: chat_engine_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#chat_engine_config DiscoveryEngineChatEngine#chat_engine_config}
        :param collection_id: The collection ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#collection_id DiscoveryEngineChatEngine#collection_id}
        :param data_store_ids: The data stores associated with this engine. Multiple DataStores in the same Collection can be associated here. All listed DataStores must be 'SOLUTION_TYPE_CHAT'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#data_store_ids DiscoveryEngineChatEngine#data_store_ids}
        :param display_name: The display name of the engine. Should be human readable. UTF-8 encoded string with limit of 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#display_name DiscoveryEngineChatEngine#display_name}
        :param engine_id: The ID to use for chat engine. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#engine_id DiscoveryEngineChatEngine#engine_id}
        :param location: Location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#location DiscoveryEngineChatEngine#location}
        :param common_config: common_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#common_config DiscoveryEngineChatEngine#common_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#id DiscoveryEngineChatEngine#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param industry_vertical: The industry vertical that the chat engine registers. Vertical on Engine has to match vertical of the DataStore linked to the engine. Default value: "GENERIC" Possible values: ["GENERIC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#industry_vertical DiscoveryEngineChatEngine#industry_vertical}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#project DiscoveryEngineChatEngine#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#timeouts DiscoveryEngineChatEngine#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10a9e0fd86619ce62679fe925a8a6519ca84eaae5c4e7ddb106baa2426738d89)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DiscoveryEngineChatEngineConfig(
            chat_engine_config=chat_engine_config,
            collection_id=collection_id,
            data_store_ids=data_store_ids,
            display_name=display_name,
            engine_id=engine_id,
            location=location,
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
        '''Generates CDKTF code for importing a DiscoveryEngineChatEngine resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DiscoveryEngineChatEngine to import.
        :param import_from_id: The id of the existing DiscoveryEngineChatEngine that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DiscoveryEngineChatEngine to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a560f66277f2916b2aacbb046f3422843228ca1c3868967c9b7857e658787ce0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putChatEngineConfig")
    def put_chat_engine_config(
        self,
        *,
        agent_creation_config: typing.Optional[typing.Union["DiscoveryEngineChatEngineChatEngineConfigAgentCreationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        allow_cross_region: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dialogflow_agent_to_link: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param agent_creation_config: agent_creation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#agent_creation_config DiscoveryEngineChatEngine#agent_creation_config}
        :param allow_cross_region: If the flag set to true, we allow the agent and engine are in different locations, otherwise the agent and engine are required to be in the same location. The flag is set to false by default. Note that the 'allow_cross_region' are one-time consumed by and passed to EngineService.CreateEngine. It means they cannot be retrieved using EngineService.GetEngine or EngineService.ListEngines API after engine creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#allow_cross_region DiscoveryEngineChatEngine#allow_cross_region}
        :param dialogflow_agent_to_link: The resource name of an existing Dialogflow agent to link to this Chat Engine. Format: 'projects/<Project_ID>/locations/<Location_ID>/agents/<Agent_ID>'. Exactly one of 'agent_creation_config' or 'dialogflow_agent_to_link' must be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#dialogflow_agent_to_link DiscoveryEngineChatEngine#dialogflow_agent_to_link}
        '''
        value = DiscoveryEngineChatEngineChatEngineConfig(
            agent_creation_config=agent_creation_config,
            allow_cross_region=allow_cross_region,
            dialogflow_agent_to_link=dialogflow_agent_to_link,
        )

        return typing.cast(None, jsii.invoke(self, "putChatEngineConfig", [value]))

    @jsii.member(jsii_name="putCommonConfig")
    def put_common_config(
        self,
        *,
        company_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param company_name: The name of the company, business or entity that is associated with the engine. Setting this may help improve LLM related features. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#company_name DiscoveryEngineChatEngine#company_name}
        '''
        value = DiscoveryEngineChatEngineCommonConfig(company_name=company_name)

        return typing.cast(None, jsii.invoke(self, "putCommonConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#create DiscoveryEngineChatEngine#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#delete DiscoveryEngineChatEngine#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#update DiscoveryEngineChatEngine#update}.
        '''
        value = DiscoveryEngineChatEngineTimeouts(
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
    @jsii.member(jsii_name="chatEngineConfig")
    def chat_engine_config(
        self,
    ) -> "DiscoveryEngineChatEngineChatEngineConfigOutputReference":
        return typing.cast("DiscoveryEngineChatEngineChatEngineConfigOutputReference", jsii.get(self, "chatEngineConfig"))

    @builtins.property
    @jsii.member(jsii_name="chatEngineMetadata")
    def chat_engine_metadata(self) -> "DiscoveryEngineChatEngineChatEngineMetadataList":
        return typing.cast("DiscoveryEngineChatEngineChatEngineMetadataList", jsii.get(self, "chatEngineMetadata"))

    @builtins.property
    @jsii.member(jsii_name="commonConfig")
    def common_config(self) -> "DiscoveryEngineChatEngineCommonConfigOutputReference":
        return typing.cast("DiscoveryEngineChatEngineCommonConfigOutputReference", jsii.get(self, "commonConfig"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DiscoveryEngineChatEngineTimeoutsOutputReference":
        return typing.cast("DiscoveryEngineChatEngineTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="chatEngineConfigInput")
    def chat_engine_config_input(
        self,
    ) -> typing.Optional["DiscoveryEngineChatEngineChatEngineConfig"]:
        return typing.cast(typing.Optional["DiscoveryEngineChatEngineChatEngineConfig"], jsii.get(self, "chatEngineConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="collectionIdInput")
    def collection_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "collectionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="commonConfigInput")
    def common_config_input(
        self,
    ) -> typing.Optional["DiscoveryEngineChatEngineCommonConfig"]:
        return typing.cast(typing.Optional["DiscoveryEngineChatEngineCommonConfig"], jsii.get(self, "commonConfigInput"))

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
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DiscoveryEngineChatEngineTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DiscoveryEngineChatEngineTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="collectionId")
    def collection_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "collectionId"))

    @collection_id.setter
    def collection_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f96bd90865b4f6aa9adbb052dac68c8b1fb012c99390165dd1f3e012a9d72d25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collectionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataStoreIds")
    def data_store_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dataStoreIds"))

    @data_store_ids.setter
    def data_store_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32b70bd2dcb64c1a89c9ff2cbcaba723186a063023dd7e677e33d2edbbe67e0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataStoreIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be1527022b469ffb531042f48cf6b5c5bf7f2d90f6c92a0ace7116fdb941395e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="engineId")
    def engine_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "engineId"))

    @engine_id.setter
    def engine_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ffad670982520e03e77a5a4cf032931c8b455b2d69ccb8d12512c2873771d96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c6e0849e108f9064b23d6d39412fa4cb9dd0be58af47c1c331683a6b51dcd13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="industryVertical")
    def industry_vertical(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "industryVertical"))

    @industry_vertical.setter
    def industry_vertical(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56c94b81c5e5cf9e8910a5502137e8661733de36d0535b08a4fbb974907ec812)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "industryVertical", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b4aa7fc90923b8ee794c940f4b47f7405ef0962b6b2093965da447b7ad8898b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e99bb8f6d44d4b4d96b7d7194992675a469ff385f97fbff6dbea6cbdd91aa784)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.discoveryEngineChatEngine.DiscoveryEngineChatEngineChatEngineConfig",
    jsii_struct_bases=[],
    name_mapping={
        "agent_creation_config": "agentCreationConfig",
        "allow_cross_region": "allowCrossRegion",
        "dialogflow_agent_to_link": "dialogflowAgentToLink",
    },
)
class DiscoveryEngineChatEngineChatEngineConfig:
    def __init__(
        self,
        *,
        agent_creation_config: typing.Optional[typing.Union["DiscoveryEngineChatEngineChatEngineConfigAgentCreationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        allow_cross_region: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dialogflow_agent_to_link: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param agent_creation_config: agent_creation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#agent_creation_config DiscoveryEngineChatEngine#agent_creation_config}
        :param allow_cross_region: If the flag set to true, we allow the agent and engine are in different locations, otherwise the agent and engine are required to be in the same location. The flag is set to false by default. Note that the 'allow_cross_region' are one-time consumed by and passed to EngineService.CreateEngine. It means they cannot be retrieved using EngineService.GetEngine or EngineService.ListEngines API after engine creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#allow_cross_region DiscoveryEngineChatEngine#allow_cross_region}
        :param dialogflow_agent_to_link: The resource name of an existing Dialogflow agent to link to this Chat Engine. Format: 'projects/<Project_ID>/locations/<Location_ID>/agents/<Agent_ID>'. Exactly one of 'agent_creation_config' or 'dialogflow_agent_to_link' must be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#dialogflow_agent_to_link DiscoveryEngineChatEngine#dialogflow_agent_to_link}
        '''
        if isinstance(agent_creation_config, dict):
            agent_creation_config = DiscoveryEngineChatEngineChatEngineConfigAgentCreationConfig(**agent_creation_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27373e813ce106552ed3ca5c7ed457e5782f80b724a15e44b4386efd92a4f6d8)
            check_type(argname="argument agent_creation_config", value=agent_creation_config, expected_type=type_hints["agent_creation_config"])
            check_type(argname="argument allow_cross_region", value=allow_cross_region, expected_type=type_hints["allow_cross_region"])
            check_type(argname="argument dialogflow_agent_to_link", value=dialogflow_agent_to_link, expected_type=type_hints["dialogflow_agent_to_link"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if agent_creation_config is not None:
            self._values["agent_creation_config"] = agent_creation_config
        if allow_cross_region is not None:
            self._values["allow_cross_region"] = allow_cross_region
        if dialogflow_agent_to_link is not None:
            self._values["dialogflow_agent_to_link"] = dialogflow_agent_to_link

    @builtins.property
    def agent_creation_config(
        self,
    ) -> typing.Optional["DiscoveryEngineChatEngineChatEngineConfigAgentCreationConfig"]:
        '''agent_creation_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#agent_creation_config DiscoveryEngineChatEngine#agent_creation_config}
        '''
        result = self._values.get("agent_creation_config")
        return typing.cast(typing.Optional["DiscoveryEngineChatEngineChatEngineConfigAgentCreationConfig"], result)

    @builtins.property
    def allow_cross_region(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the flag set to true, we allow the agent and engine are in different locations, otherwise the agent and engine are required to be in the same location.

        The flag is set to false by default.
        Note that the 'allow_cross_region' are one-time consumed by and passed
        to EngineService.CreateEngine. It means they cannot be retrieved using
        EngineService.GetEngine or EngineService.ListEngines API after engine
        creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#allow_cross_region DiscoveryEngineChatEngine#allow_cross_region}
        '''
        result = self._values.get("allow_cross_region")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def dialogflow_agent_to_link(self) -> typing.Optional[builtins.str]:
        '''The resource name of an existing Dialogflow agent to link to this Chat Engine.

        Format: 'projects/<Project_ID>/locations/<Location_ID>/agents/<Agent_ID>'.
        Exactly one of 'agent_creation_config' or 'dialogflow_agent_to_link' must be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#dialogflow_agent_to_link DiscoveryEngineChatEngine#dialogflow_agent_to_link}
        '''
        result = self._values.get("dialogflow_agent_to_link")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiscoveryEngineChatEngineChatEngineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.discoveryEngineChatEngine.DiscoveryEngineChatEngineChatEngineConfigAgentCreationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "default_language_code": "defaultLanguageCode",
        "time_zone": "timeZone",
        "business": "business",
        "location": "location",
    },
)
class DiscoveryEngineChatEngineChatEngineConfigAgentCreationConfig:
    def __init__(
        self,
        *,
        default_language_code: builtins.str,
        time_zone: builtins.str,
        business: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_language_code: The default language of the agent as a language tag. See `Language Support <https://cloud.google.com/dialogflow/docs/reference/language>`_ for a list of the currently supported language codes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#default_language_code DiscoveryEngineChatEngine#default_language_code}
        :param time_zone: The time zone of the agent from the `time zone database <https://www.iana.org/time-zones>`_, e.g., America/New_York, Europe/Paris. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#time_zone DiscoveryEngineChatEngine#time_zone}
        :param business: Name of the company, organization or other entity that the agent represents. Used for knowledge connector LLM prompt and for knowledge search. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#business DiscoveryEngineChatEngine#business}
        :param location: Agent location for Agent creation, currently supported values: global/us/eu, it needs to be the same region as the Chat Engine. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#location DiscoveryEngineChatEngine#location}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32d2809559cb9f21688baa73895a35f60f3cea93d5afbdee569404323330566c)
            check_type(argname="argument default_language_code", value=default_language_code, expected_type=type_hints["default_language_code"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
            check_type(argname="argument business", value=business, expected_type=type_hints["business"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_language_code": default_language_code,
            "time_zone": time_zone,
        }
        if business is not None:
            self._values["business"] = business
        if location is not None:
            self._values["location"] = location

    @builtins.property
    def default_language_code(self) -> builtins.str:
        '''The default language of the agent as a language tag.

        See `Language Support <https://cloud.google.com/dialogflow/docs/reference/language>`_ for a list of the currently supported language codes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#default_language_code DiscoveryEngineChatEngine#default_language_code}
        '''
        result = self._values.get("default_language_code")
        assert result is not None, "Required property 'default_language_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def time_zone(self) -> builtins.str:
        '''The time zone of the agent from the `time zone database <https://www.iana.org/time-zones>`_, e.g., America/New_York, Europe/Paris.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#time_zone DiscoveryEngineChatEngine#time_zone}
        '''
        result = self._values.get("time_zone")
        assert result is not None, "Required property 'time_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def business(self) -> typing.Optional[builtins.str]:
        '''Name of the company, organization or other entity that the agent represents.

        Used for knowledge connector LLM prompt and for knowledge search.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#business DiscoveryEngineChatEngine#business}
        '''
        result = self._values.get("business")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''Agent location for Agent creation, currently supported values: global/us/eu, it needs to be the same region as the Chat Engine.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#location DiscoveryEngineChatEngine#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiscoveryEngineChatEngineChatEngineConfigAgentCreationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DiscoveryEngineChatEngineChatEngineConfigAgentCreationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.discoveryEngineChatEngine.DiscoveryEngineChatEngineChatEngineConfigAgentCreationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb15f9d1e0b0ad18d366f48f439a547c5784e9e416b40e8ef302bd4b62e73e4b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBusiness")
    def reset_business(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBusiness", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @builtins.property
    @jsii.member(jsii_name="businessInput")
    def business_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "businessInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultLanguageCodeInput")
    def default_language_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultLanguageCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="business")
    def business(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "business"))

    @business.setter
    def business(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f43cedadb3dd2026258da902afe4c5c6e4fda4231f1a5a00aedf154fc6bf01ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "business", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultLanguageCode")
    def default_language_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultLanguageCode"))

    @default_language_code.setter
    def default_language_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b06f3e96426cffb148200dce80099d6471e533397dd41eff925e0a8960f153a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultLanguageCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d9d150bb0f5ee4fa1118351cf123152d3959cddbf5dc04448fc8cc56e4aeb72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c112b13fe2aa88c5c2d5a76f63a6028332c89f5dd07c55085362e917696d6c15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DiscoveryEngineChatEngineChatEngineConfigAgentCreationConfig]:
        return typing.cast(typing.Optional[DiscoveryEngineChatEngineChatEngineConfigAgentCreationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DiscoveryEngineChatEngineChatEngineConfigAgentCreationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4040e2d532bd1e7d02cf0c722e1b55102d4e2ee176277e7097074a2e354b507)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DiscoveryEngineChatEngineChatEngineConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.discoveryEngineChatEngine.DiscoveryEngineChatEngineChatEngineConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd78aba728c0675ebfd73c11cf2efbdcad3603c24f2c10d14446685e57846613)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAgentCreationConfig")
    def put_agent_creation_config(
        self,
        *,
        default_language_code: builtins.str,
        time_zone: builtins.str,
        business: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_language_code: The default language of the agent as a language tag. See `Language Support <https://cloud.google.com/dialogflow/docs/reference/language>`_ for a list of the currently supported language codes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#default_language_code DiscoveryEngineChatEngine#default_language_code}
        :param time_zone: The time zone of the agent from the `time zone database <https://www.iana.org/time-zones>`_, e.g., America/New_York, Europe/Paris. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#time_zone DiscoveryEngineChatEngine#time_zone}
        :param business: Name of the company, organization or other entity that the agent represents. Used for knowledge connector LLM prompt and for knowledge search. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#business DiscoveryEngineChatEngine#business}
        :param location: Agent location for Agent creation, currently supported values: global/us/eu, it needs to be the same region as the Chat Engine. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#location DiscoveryEngineChatEngine#location}
        '''
        value = DiscoveryEngineChatEngineChatEngineConfigAgentCreationConfig(
            default_language_code=default_language_code,
            time_zone=time_zone,
            business=business,
            location=location,
        )

        return typing.cast(None, jsii.invoke(self, "putAgentCreationConfig", [value]))

    @jsii.member(jsii_name="resetAgentCreationConfig")
    def reset_agent_creation_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAgentCreationConfig", []))

    @jsii.member(jsii_name="resetAllowCrossRegion")
    def reset_allow_cross_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowCrossRegion", []))

    @jsii.member(jsii_name="resetDialogflowAgentToLink")
    def reset_dialogflow_agent_to_link(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDialogflowAgentToLink", []))

    @builtins.property
    @jsii.member(jsii_name="agentCreationConfig")
    def agent_creation_config(
        self,
    ) -> DiscoveryEngineChatEngineChatEngineConfigAgentCreationConfigOutputReference:
        return typing.cast(DiscoveryEngineChatEngineChatEngineConfigAgentCreationConfigOutputReference, jsii.get(self, "agentCreationConfig"))

    @builtins.property
    @jsii.member(jsii_name="agentCreationConfigInput")
    def agent_creation_config_input(
        self,
    ) -> typing.Optional[DiscoveryEngineChatEngineChatEngineConfigAgentCreationConfig]:
        return typing.cast(typing.Optional[DiscoveryEngineChatEngineChatEngineConfigAgentCreationConfig], jsii.get(self, "agentCreationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="allowCrossRegionInput")
    def allow_cross_region_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowCrossRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="dialogflowAgentToLinkInput")
    def dialogflow_agent_to_link_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dialogflowAgentToLinkInput"))

    @builtins.property
    @jsii.member(jsii_name="allowCrossRegion")
    def allow_cross_region(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowCrossRegion"))

    @allow_cross_region.setter
    def allow_cross_region(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8909ed626bfd67d4335801a6568a3f3e6a8f7ac8e3061a7276aa9052c11a5740)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowCrossRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dialogflowAgentToLink")
    def dialogflow_agent_to_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dialogflowAgentToLink"))

    @dialogflow_agent_to_link.setter
    def dialogflow_agent_to_link(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__572095eb8ac2e6d19d9c34f586e87e97943b5732082c1627d20fefa710fdedbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dialogflowAgentToLink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DiscoveryEngineChatEngineChatEngineConfig]:
        return typing.cast(typing.Optional[DiscoveryEngineChatEngineChatEngineConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DiscoveryEngineChatEngineChatEngineConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5aebb3c6f6ad86434fdebe08d1f8bf11895fb007e6e5bc6ad0f2192911c06df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.discoveryEngineChatEngine.DiscoveryEngineChatEngineChatEngineMetadata",
    jsii_struct_bases=[],
    name_mapping={},
)
class DiscoveryEngineChatEngineChatEngineMetadata:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiscoveryEngineChatEngineChatEngineMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DiscoveryEngineChatEngineChatEngineMetadataList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.discoveryEngineChatEngine.DiscoveryEngineChatEngineChatEngineMetadataList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38005b571b955c267c0d3418b712524f23bcc3e3651e3647f60a93c4c5f87c4e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DiscoveryEngineChatEngineChatEngineMetadataOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d9231f66d88a458c9127ab246ab311305eac8dc98480a9167a4772ee9dda689)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DiscoveryEngineChatEngineChatEngineMetadataOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__941b3c9f44624364a1d729a627fd62ab2d3a5cc8a4b7a641207f0dc263b6633f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__77e513f203b655fd329c2ecb59af0a03e1f935ad5128fc8843d771940c616aee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__839ed8765b1fe0561c947ea0cf796878abc09daa67e2c1f2bd1bdfbe765d8d77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DiscoveryEngineChatEngineChatEngineMetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.discoveryEngineChatEngine.DiscoveryEngineChatEngineChatEngineMetadataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9cb6c4bdb1f1417009c7390d467d107ffcac911e98c8a5bdd8e88069823eff34)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="dialogflowAgent")
    def dialogflow_agent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dialogflowAgent"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DiscoveryEngineChatEngineChatEngineMetadata]:
        return typing.cast(typing.Optional[DiscoveryEngineChatEngineChatEngineMetadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DiscoveryEngineChatEngineChatEngineMetadata],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1244b25db20f666dc35c6a625c0fd911d5e1c6e864e0c1badb2297017383e04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.discoveryEngineChatEngine.DiscoveryEngineChatEngineCommonConfig",
    jsii_struct_bases=[],
    name_mapping={"company_name": "companyName"},
)
class DiscoveryEngineChatEngineCommonConfig:
    def __init__(self, *, company_name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param company_name: The name of the company, business or entity that is associated with the engine. Setting this may help improve LLM related features. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#company_name DiscoveryEngineChatEngine#company_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d784caf23f919aa31432d2657cc6b81e2b1eabae7e286f3d33869c71bd3fb7e)
            check_type(argname="argument company_name", value=company_name, expected_type=type_hints["company_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if company_name is not None:
            self._values["company_name"] = company_name

    @builtins.property
    def company_name(self) -> typing.Optional[builtins.str]:
        '''The name of the company, business or entity that is associated with the engine.

        Setting this may help improve LLM related features.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#company_name DiscoveryEngineChatEngine#company_name}
        '''
        result = self._values.get("company_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiscoveryEngineChatEngineCommonConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DiscoveryEngineChatEngineCommonConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.discoveryEngineChatEngine.DiscoveryEngineChatEngineCommonConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__803d41fc7dc1fb1167f64fd0c42c70a324b246bb9005c8732638dda12876892b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__27967d962195620ea59875ef4e5b0394f25d156e17cd6f44c5c5874a84f42145)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "companyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DiscoveryEngineChatEngineCommonConfig]:
        return typing.cast(typing.Optional[DiscoveryEngineChatEngineCommonConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DiscoveryEngineChatEngineCommonConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5ae13ecd99f101960522ce36a98ab5bb5565970ea421d1e676b514df7aa9906)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.discoveryEngineChatEngine.DiscoveryEngineChatEngineConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "chat_engine_config": "chatEngineConfig",
        "collection_id": "collectionId",
        "data_store_ids": "dataStoreIds",
        "display_name": "displayName",
        "engine_id": "engineId",
        "location": "location",
        "common_config": "commonConfig",
        "id": "id",
        "industry_vertical": "industryVertical",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class DiscoveryEngineChatEngineConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        chat_engine_config: typing.Union[DiscoveryEngineChatEngineChatEngineConfig, typing.Dict[builtins.str, typing.Any]],
        collection_id: builtins.str,
        data_store_ids: typing.Sequence[builtins.str],
        display_name: builtins.str,
        engine_id: builtins.str,
        location: builtins.str,
        common_config: typing.Optional[typing.Union[DiscoveryEngineChatEngineCommonConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        industry_vertical: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DiscoveryEngineChatEngineTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param chat_engine_config: chat_engine_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#chat_engine_config DiscoveryEngineChatEngine#chat_engine_config}
        :param collection_id: The collection ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#collection_id DiscoveryEngineChatEngine#collection_id}
        :param data_store_ids: The data stores associated with this engine. Multiple DataStores in the same Collection can be associated here. All listed DataStores must be 'SOLUTION_TYPE_CHAT'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#data_store_ids DiscoveryEngineChatEngine#data_store_ids}
        :param display_name: The display name of the engine. Should be human readable. UTF-8 encoded string with limit of 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#display_name DiscoveryEngineChatEngine#display_name}
        :param engine_id: The ID to use for chat engine. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#engine_id DiscoveryEngineChatEngine#engine_id}
        :param location: Location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#location DiscoveryEngineChatEngine#location}
        :param common_config: common_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#common_config DiscoveryEngineChatEngine#common_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#id DiscoveryEngineChatEngine#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param industry_vertical: The industry vertical that the chat engine registers. Vertical on Engine has to match vertical of the DataStore linked to the engine. Default value: "GENERIC" Possible values: ["GENERIC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#industry_vertical DiscoveryEngineChatEngine#industry_vertical}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#project DiscoveryEngineChatEngine#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#timeouts DiscoveryEngineChatEngine#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(chat_engine_config, dict):
            chat_engine_config = DiscoveryEngineChatEngineChatEngineConfig(**chat_engine_config)
        if isinstance(common_config, dict):
            common_config = DiscoveryEngineChatEngineCommonConfig(**common_config)
        if isinstance(timeouts, dict):
            timeouts = DiscoveryEngineChatEngineTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df90d57e238ce27aaf6338c9fce3bd6be43b4961b65b2b0fb057a4e52d23d6d3)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument chat_engine_config", value=chat_engine_config, expected_type=type_hints["chat_engine_config"])
            check_type(argname="argument collection_id", value=collection_id, expected_type=type_hints["collection_id"])
            check_type(argname="argument data_store_ids", value=data_store_ids, expected_type=type_hints["data_store_ids"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument engine_id", value=engine_id, expected_type=type_hints["engine_id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument common_config", value=common_config, expected_type=type_hints["common_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument industry_vertical", value=industry_vertical, expected_type=type_hints["industry_vertical"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "chat_engine_config": chat_engine_config,
            "collection_id": collection_id,
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
    def chat_engine_config(self) -> DiscoveryEngineChatEngineChatEngineConfig:
        '''chat_engine_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#chat_engine_config DiscoveryEngineChatEngine#chat_engine_config}
        '''
        result = self._values.get("chat_engine_config")
        assert result is not None, "Required property 'chat_engine_config' is missing"
        return typing.cast(DiscoveryEngineChatEngineChatEngineConfig, result)

    @builtins.property
    def collection_id(self) -> builtins.str:
        '''The collection ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#collection_id DiscoveryEngineChatEngine#collection_id}
        '''
        result = self._values.get("collection_id")
        assert result is not None, "Required property 'collection_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_store_ids(self) -> typing.List[builtins.str]:
        '''The data stores associated with this engine.

        Multiple DataStores in the same Collection can be associated here. All listed DataStores must be 'SOLUTION_TYPE_CHAT'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#data_store_ids DiscoveryEngineChatEngine#data_store_ids}
        '''
        result = self._values.get("data_store_ids")
        assert result is not None, "Required property 'data_store_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''The display name of the engine. Should be human readable. UTF-8 encoded string with limit of 1024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#display_name DiscoveryEngineChatEngine#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def engine_id(self) -> builtins.str:
        '''The ID to use for chat engine.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#engine_id DiscoveryEngineChatEngine#engine_id}
        '''
        result = self._values.get("engine_id")
        assert result is not None, "Required property 'engine_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Location.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#location DiscoveryEngineChatEngine#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def common_config(self) -> typing.Optional[DiscoveryEngineChatEngineCommonConfig]:
        '''common_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#common_config DiscoveryEngineChatEngine#common_config}
        '''
        result = self._values.get("common_config")
        return typing.cast(typing.Optional[DiscoveryEngineChatEngineCommonConfig], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#id DiscoveryEngineChatEngine#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def industry_vertical(self) -> typing.Optional[builtins.str]:
        '''The industry vertical that the chat engine registers.

        Vertical on Engine has to match vertical of the DataStore linked to the engine. Default value: "GENERIC" Possible values: ["GENERIC"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#industry_vertical DiscoveryEngineChatEngine#industry_vertical}
        '''
        result = self._values.get("industry_vertical")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#project DiscoveryEngineChatEngine#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DiscoveryEngineChatEngineTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#timeouts DiscoveryEngineChatEngine#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DiscoveryEngineChatEngineTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiscoveryEngineChatEngineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.discoveryEngineChatEngine.DiscoveryEngineChatEngineTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DiscoveryEngineChatEngineTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#create DiscoveryEngineChatEngine#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#delete DiscoveryEngineChatEngine#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#update DiscoveryEngineChatEngine#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dcdd1a24da41d34d8d36fa4d96125e8e6aac38affd6ade41a6d754bc93c7a06)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#create DiscoveryEngineChatEngine#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#delete DiscoveryEngineChatEngine#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_chat_engine#update DiscoveryEngineChatEngine#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiscoveryEngineChatEngineTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DiscoveryEngineChatEngineTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.discoveryEngineChatEngine.DiscoveryEngineChatEngineTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__564a1bed6a95efbd4bb89ab36cc57e8affae8fc2e6e0bbf7d12d0203398cb2cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__01f55aba2738a173aaa4d9ca52a55a2f933fd20d75995756be973c2633496a7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b11c915ff72f60770b3c5d202506d5ca31803d0d20d43bc3e65157ebe8865292)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9249d3082c66513d417749059f3a0786c129ef0c9030dcd17ec25baa600e9a1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DiscoveryEngineChatEngineTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DiscoveryEngineChatEngineTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DiscoveryEngineChatEngineTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af223f0d41cbdc8df4f82915be977fb70fd4d5ac28f1840b7ede2fc87920de24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DiscoveryEngineChatEngine",
    "DiscoveryEngineChatEngineChatEngineConfig",
    "DiscoveryEngineChatEngineChatEngineConfigAgentCreationConfig",
    "DiscoveryEngineChatEngineChatEngineConfigAgentCreationConfigOutputReference",
    "DiscoveryEngineChatEngineChatEngineConfigOutputReference",
    "DiscoveryEngineChatEngineChatEngineMetadata",
    "DiscoveryEngineChatEngineChatEngineMetadataList",
    "DiscoveryEngineChatEngineChatEngineMetadataOutputReference",
    "DiscoveryEngineChatEngineCommonConfig",
    "DiscoveryEngineChatEngineCommonConfigOutputReference",
    "DiscoveryEngineChatEngineConfig",
    "DiscoveryEngineChatEngineTimeouts",
    "DiscoveryEngineChatEngineTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__10a9e0fd86619ce62679fe925a8a6519ca84eaae5c4e7ddb106baa2426738d89(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    chat_engine_config: typing.Union[DiscoveryEngineChatEngineChatEngineConfig, typing.Dict[builtins.str, typing.Any]],
    collection_id: builtins.str,
    data_store_ids: typing.Sequence[builtins.str],
    display_name: builtins.str,
    engine_id: builtins.str,
    location: builtins.str,
    common_config: typing.Optional[typing.Union[DiscoveryEngineChatEngineCommonConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    industry_vertical: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DiscoveryEngineChatEngineTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__a560f66277f2916b2aacbb046f3422843228ca1c3868967c9b7857e658787ce0(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f96bd90865b4f6aa9adbb052dac68c8b1fb012c99390165dd1f3e012a9d72d25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32b70bd2dcb64c1a89c9ff2cbcaba723186a063023dd7e677e33d2edbbe67e0b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be1527022b469ffb531042f48cf6b5c5bf7f2d90f6c92a0ace7116fdb941395e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ffad670982520e03e77a5a4cf032931c8b455b2d69ccb8d12512c2873771d96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c6e0849e108f9064b23d6d39412fa4cb9dd0be58af47c1c331683a6b51dcd13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56c94b81c5e5cf9e8910a5502137e8661733de36d0535b08a4fbb974907ec812(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b4aa7fc90923b8ee794c940f4b47f7405ef0962b6b2093965da447b7ad8898b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e99bb8f6d44d4b4d96b7d7194992675a469ff385f97fbff6dbea6cbdd91aa784(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27373e813ce106552ed3ca5c7ed457e5782f80b724a15e44b4386efd92a4f6d8(
    *,
    agent_creation_config: typing.Optional[typing.Union[DiscoveryEngineChatEngineChatEngineConfigAgentCreationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    allow_cross_region: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dialogflow_agent_to_link: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32d2809559cb9f21688baa73895a35f60f3cea93d5afbdee569404323330566c(
    *,
    default_language_code: builtins.str,
    time_zone: builtins.str,
    business: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb15f9d1e0b0ad18d366f48f439a547c5784e9e416b40e8ef302bd4b62e73e4b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f43cedadb3dd2026258da902afe4c5c6e4fda4231f1a5a00aedf154fc6bf01ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b06f3e96426cffb148200dce80099d6471e533397dd41eff925e0a8960f153a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d9d150bb0f5ee4fa1118351cf123152d3959cddbf5dc04448fc8cc56e4aeb72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c112b13fe2aa88c5c2d5a76f63a6028332c89f5dd07c55085362e917696d6c15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4040e2d532bd1e7d02cf0c722e1b55102d4e2ee176277e7097074a2e354b507(
    value: typing.Optional[DiscoveryEngineChatEngineChatEngineConfigAgentCreationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd78aba728c0675ebfd73c11cf2efbdcad3603c24f2c10d14446685e57846613(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8909ed626bfd67d4335801a6568a3f3e6a8f7ac8e3061a7276aa9052c11a5740(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__572095eb8ac2e6d19d9c34f586e87e97943b5732082c1627d20fefa710fdedbc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5aebb3c6f6ad86434fdebe08d1f8bf11895fb007e6e5bc6ad0f2192911c06df(
    value: typing.Optional[DiscoveryEngineChatEngineChatEngineConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38005b571b955c267c0d3418b712524f23bcc3e3651e3647f60a93c4c5f87c4e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d9231f66d88a458c9127ab246ab311305eac8dc98480a9167a4772ee9dda689(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__941b3c9f44624364a1d729a627fd62ab2d3a5cc8a4b7a641207f0dc263b6633f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77e513f203b655fd329c2ecb59af0a03e1f935ad5128fc8843d771940c616aee(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__839ed8765b1fe0561c947ea0cf796878abc09daa67e2c1f2bd1bdfbe765d8d77(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cb6c4bdb1f1417009c7390d467d107ffcac911e98c8a5bdd8e88069823eff34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1244b25db20f666dc35c6a625c0fd911d5e1c6e864e0c1badb2297017383e04(
    value: typing.Optional[DiscoveryEngineChatEngineChatEngineMetadata],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d784caf23f919aa31432d2657cc6b81e2b1eabae7e286f3d33869c71bd3fb7e(
    *,
    company_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__803d41fc7dc1fb1167f64fd0c42c70a324b246bb9005c8732638dda12876892b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27967d962195620ea59875ef4e5b0394f25d156e17cd6f44c5c5874a84f42145(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5ae13ecd99f101960522ce36a98ab5bb5565970ea421d1e676b514df7aa9906(
    value: typing.Optional[DiscoveryEngineChatEngineCommonConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df90d57e238ce27aaf6338c9fce3bd6be43b4961b65b2b0fb057a4e52d23d6d3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    chat_engine_config: typing.Union[DiscoveryEngineChatEngineChatEngineConfig, typing.Dict[builtins.str, typing.Any]],
    collection_id: builtins.str,
    data_store_ids: typing.Sequence[builtins.str],
    display_name: builtins.str,
    engine_id: builtins.str,
    location: builtins.str,
    common_config: typing.Optional[typing.Union[DiscoveryEngineChatEngineCommonConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    industry_vertical: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DiscoveryEngineChatEngineTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dcdd1a24da41d34d8d36fa4d96125e8e6aac38affd6ade41a6d754bc93c7a06(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__564a1bed6a95efbd4bb89ab36cc57e8affae8fc2e6e0bbf7d12d0203398cb2cf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01f55aba2738a173aaa4d9ca52a55a2f933fd20d75995756be973c2633496a7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b11c915ff72f60770b3c5d202506d5ca31803d0d20d43bc3e65157ebe8865292(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9249d3082c66513d417749059f3a0786c129ef0c9030dcd17ec25baa600e9a1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af223f0d41cbdc8df4f82915be977fb70fd4d5ac28f1840b7ede2fc87920de24(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DiscoveryEngineChatEngineTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
