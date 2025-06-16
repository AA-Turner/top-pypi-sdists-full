r'''
# `google_discovery_engine_chat_engine`

Refer to the Terraform Registry for docs: [`google_discovery_engine_chat_engine`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine).
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


class GoogleDiscoveryEngineChatEngine(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineChatEngine.GoogleDiscoveryEngineChatEngine",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine google_discovery_engine_chat_engine}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        chat_engine_config: typing.Union["GoogleDiscoveryEngineChatEngineChatEngineConfig", typing.Dict[builtins.str, typing.Any]],
        collection_id: builtins.str,
        data_store_ids: typing.Sequence[builtins.str],
        display_name: builtins.str,
        engine_id: builtins.str,
        location: builtins.str,
        common_config: typing.Optional[typing.Union["GoogleDiscoveryEngineChatEngineCommonConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        industry_vertical: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDiscoveryEngineChatEngineTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine google_discovery_engine_chat_engine} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param chat_engine_config: chat_engine_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#chat_engine_config GoogleDiscoveryEngineChatEngine#chat_engine_config}
        :param collection_id: The collection ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#collection_id GoogleDiscoveryEngineChatEngine#collection_id}
        :param data_store_ids: The data stores associated with this engine. Multiple DataStores in the same Collection can be associated here. All listed DataStores must be 'SOLUTION_TYPE_CHAT'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#data_store_ids GoogleDiscoveryEngineChatEngine#data_store_ids}
        :param display_name: The display name of the engine. Should be human readable. UTF-8 encoded string with limit of 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#display_name GoogleDiscoveryEngineChatEngine#display_name}
        :param engine_id: The ID to use for chat engine. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#engine_id GoogleDiscoveryEngineChatEngine#engine_id}
        :param location: Location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#location GoogleDiscoveryEngineChatEngine#location}
        :param common_config: common_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#common_config GoogleDiscoveryEngineChatEngine#common_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#id GoogleDiscoveryEngineChatEngine#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param industry_vertical: The industry vertical that the chat engine registers. Vertical on Engine has to match vertical of the DataStore linked to the engine. Default value: "GENERIC" Possible values: ["GENERIC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#industry_vertical GoogleDiscoveryEngineChatEngine#industry_vertical}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#project GoogleDiscoveryEngineChatEngine#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#timeouts GoogleDiscoveryEngineChatEngine#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d67f73bb2ab24d9b469b0ea73f74daea43ed7a9fa0d2f5913c03801fa433a8de)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDiscoveryEngineChatEngineConfig(
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
        '''Generates CDKTF code for importing a GoogleDiscoveryEngineChatEngine resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDiscoveryEngineChatEngine to import.
        :param import_from_id: The id of the existing GoogleDiscoveryEngineChatEngine that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDiscoveryEngineChatEngine to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d469dd8c3f719571b5ce7066975a32b8035480de4c79dde45069034fc7dd299)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putChatEngineConfig")
    def put_chat_engine_config(
        self,
        *,
        agent_creation_config: typing.Optional[typing.Union["GoogleDiscoveryEngineChatEngineChatEngineConfigAgentCreationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        allow_cross_region: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dialogflow_agent_to_link: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param agent_creation_config: agent_creation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#agent_creation_config GoogleDiscoveryEngineChatEngine#agent_creation_config}
        :param allow_cross_region: If the flag set to true, we allow the agent and engine are in different locations, otherwise the agent and engine are required to be in the same location. The flag is set to false by default. Note that the 'allow_cross_region' are one-time consumed by and passed to EngineService.CreateEngine. It means they cannot be retrieved using EngineService.GetEngine or EngineService.ListEngines API after engine creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#allow_cross_region GoogleDiscoveryEngineChatEngine#allow_cross_region}
        :param dialogflow_agent_to_link: The resource name of an existing Dialogflow agent to link to this Chat Engine. Format: 'projects/<Project_ID>/locations/<Location_ID>/agents/<Agent_ID>'. Exactly one of 'agent_creation_config' or 'dialogflow_agent_to_link' must be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#dialogflow_agent_to_link GoogleDiscoveryEngineChatEngine#dialogflow_agent_to_link}
        '''
        value = GoogleDiscoveryEngineChatEngineChatEngineConfig(
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
        :param company_name: The name of the company, business or entity that is associated with the engine. Setting this may help improve LLM related features. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#company_name GoogleDiscoveryEngineChatEngine#company_name}
        '''
        value = GoogleDiscoveryEngineChatEngineCommonConfig(company_name=company_name)

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#create GoogleDiscoveryEngineChatEngine#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#delete GoogleDiscoveryEngineChatEngine#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#update GoogleDiscoveryEngineChatEngine#update}.
        '''
        value = GoogleDiscoveryEngineChatEngineTimeouts(
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
    ) -> "GoogleDiscoveryEngineChatEngineChatEngineConfigOutputReference":
        return typing.cast("GoogleDiscoveryEngineChatEngineChatEngineConfigOutputReference", jsii.get(self, "chatEngineConfig"))

    @builtins.property
    @jsii.member(jsii_name="chatEngineMetadata")
    def chat_engine_metadata(
        self,
    ) -> "GoogleDiscoveryEngineChatEngineChatEngineMetadataList":
        return typing.cast("GoogleDiscoveryEngineChatEngineChatEngineMetadataList", jsii.get(self, "chatEngineMetadata"))

    @builtins.property
    @jsii.member(jsii_name="commonConfig")
    def common_config(
        self,
    ) -> "GoogleDiscoveryEngineChatEngineCommonConfigOutputReference":
        return typing.cast("GoogleDiscoveryEngineChatEngineCommonConfigOutputReference", jsii.get(self, "commonConfig"))

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
    def timeouts(self) -> "GoogleDiscoveryEngineChatEngineTimeoutsOutputReference":
        return typing.cast("GoogleDiscoveryEngineChatEngineTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="chatEngineConfigInput")
    def chat_engine_config_input(
        self,
    ) -> typing.Optional["GoogleDiscoveryEngineChatEngineChatEngineConfig"]:
        return typing.cast(typing.Optional["GoogleDiscoveryEngineChatEngineChatEngineConfig"], jsii.get(self, "chatEngineConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="collectionIdInput")
    def collection_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "collectionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="commonConfigInput")
    def common_config_input(
        self,
    ) -> typing.Optional["GoogleDiscoveryEngineChatEngineCommonConfig"]:
        return typing.cast(typing.Optional["GoogleDiscoveryEngineChatEngineCommonConfig"], jsii.get(self, "commonConfigInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDiscoveryEngineChatEngineTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDiscoveryEngineChatEngineTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="collectionId")
    def collection_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "collectionId"))

    @collection_id.setter
    def collection_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17aae83cd4a2f530e993d2575719e795eb066fba80c6f44489cfeff578b002c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collectionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataStoreIds")
    def data_store_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dataStoreIds"))

    @data_store_ids.setter
    def data_store_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5db3ea55de591df897cc61bc4173719c1d1e945f9216be3007cecb8cc447622a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataStoreIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15559a8e47bf7afe7004295ce0846bffb0218cbe06c2aaa4be17896f9b7dca51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="engineId")
    def engine_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "engineId"))

    @engine_id.setter
    def engine_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__221bafea61b695a569558fa7b1f9a68bbe456ac17ff7dabbcd87c153174fe60b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ee6a7cd7e543acbcc96959e98f002995b574ad0333a2400e83a5893625cf4dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="industryVertical")
    def industry_vertical(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "industryVertical"))

    @industry_vertical.setter
    def industry_vertical(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__712650c321e783e68fd12ca641bed4bc8879de787992fb2dcd781ba28d66d960)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "industryVertical", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51252afa389fb74acef5adfeb7486afd4bef6a623d973bfb3a502277f5909204)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cddf4e6c5fba2e85722773f64fc2e9e6619a5ccd63da17c9a758304f3240945d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineChatEngine.GoogleDiscoveryEngineChatEngineChatEngineConfig",
    jsii_struct_bases=[],
    name_mapping={
        "agent_creation_config": "agentCreationConfig",
        "allow_cross_region": "allowCrossRegion",
        "dialogflow_agent_to_link": "dialogflowAgentToLink",
    },
)
class GoogleDiscoveryEngineChatEngineChatEngineConfig:
    def __init__(
        self,
        *,
        agent_creation_config: typing.Optional[typing.Union["GoogleDiscoveryEngineChatEngineChatEngineConfigAgentCreationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        allow_cross_region: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dialogflow_agent_to_link: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param agent_creation_config: agent_creation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#agent_creation_config GoogleDiscoveryEngineChatEngine#agent_creation_config}
        :param allow_cross_region: If the flag set to true, we allow the agent and engine are in different locations, otherwise the agent and engine are required to be in the same location. The flag is set to false by default. Note that the 'allow_cross_region' are one-time consumed by and passed to EngineService.CreateEngine. It means they cannot be retrieved using EngineService.GetEngine or EngineService.ListEngines API after engine creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#allow_cross_region GoogleDiscoveryEngineChatEngine#allow_cross_region}
        :param dialogflow_agent_to_link: The resource name of an existing Dialogflow agent to link to this Chat Engine. Format: 'projects/<Project_ID>/locations/<Location_ID>/agents/<Agent_ID>'. Exactly one of 'agent_creation_config' or 'dialogflow_agent_to_link' must be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#dialogflow_agent_to_link GoogleDiscoveryEngineChatEngine#dialogflow_agent_to_link}
        '''
        if isinstance(agent_creation_config, dict):
            agent_creation_config = GoogleDiscoveryEngineChatEngineChatEngineConfigAgentCreationConfig(**agent_creation_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e95562fc5baae5ffa4b12850b477c77a0f252efca8710d97f770a93f227d735f)
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
    ) -> typing.Optional["GoogleDiscoveryEngineChatEngineChatEngineConfigAgentCreationConfig"]:
        '''agent_creation_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#agent_creation_config GoogleDiscoveryEngineChatEngine#agent_creation_config}
        '''
        result = self._values.get("agent_creation_config")
        return typing.cast(typing.Optional["GoogleDiscoveryEngineChatEngineChatEngineConfigAgentCreationConfig"], result)

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#allow_cross_region GoogleDiscoveryEngineChatEngine#allow_cross_region}
        '''
        result = self._values.get("allow_cross_region")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def dialogflow_agent_to_link(self) -> typing.Optional[builtins.str]:
        '''The resource name of an existing Dialogflow agent to link to this Chat Engine.

        Format: 'projects/<Project_ID>/locations/<Location_ID>/agents/<Agent_ID>'.
        Exactly one of 'agent_creation_config' or 'dialogflow_agent_to_link' must be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#dialogflow_agent_to_link GoogleDiscoveryEngineChatEngine#dialogflow_agent_to_link}
        '''
        result = self._values.get("dialogflow_agent_to_link")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDiscoveryEngineChatEngineChatEngineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineChatEngine.GoogleDiscoveryEngineChatEngineChatEngineConfigAgentCreationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "default_language_code": "defaultLanguageCode",
        "time_zone": "timeZone",
        "business": "business",
        "location": "location",
    },
)
class GoogleDiscoveryEngineChatEngineChatEngineConfigAgentCreationConfig:
    def __init__(
        self,
        *,
        default_language_code: builtins.str,
        time_zone: builtins.str,
        business: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_language_code: The default language of the agent as a language tag. See `Language Support <https://cloud.google.com/dialogflow/docs/reference/language>`_ for a list of the currently supported language codes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#default_language_code GoogleDiscoveryEngineChatEngine#default_language_code}
        :param time_zone: The time zone of the agent from the `time zone database <https://www.iana.org/time-zones>`_, e.g., America/New_York, Europe/Paris. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#time_zone GoogleDiscoveryEngineChatEngine#time_zone}
        :param business: Name of the company, organization or other entity that the agent represents. Used for knowledge connector LLM prompt and for knowledge search. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#business GoogleDiscoveryEngineChatEngine#business}
        :param location: Agent location for Agent creation, currently supported values: global/us/eu, it needs to be the same region as the Chat Engine. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#location GoogleDiscoveryEngineChatEngine#location}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d13468486687d0225578506143ace046f62a1ab03689376be0286b6c70fe2d8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#default_language_code GoogleDiscoveryEngineChatEngine#default_language_code}
        '''
        result = self._values.get("default_language_code")
        assert result is not None, "Required property 'default_language_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def time_zone(self) -> builtins.str:
        '''The time zone of the agent from the `time zone database <https://www.iana.org/time-zones>`_, e.g., America/New_York, Europe/Paris.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#time_zone GoogleDiscoveryEngineChatEngine#time_zone}
        '''
        result = self._values.get("time_zone")
        assert result is not None, "Required property 'time_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def business(self) -> typing.Optional[builtins.str]:
        '''Name of the company, organization or other entity that the agent represents.

        Used for knowledge connector LLM prompt and for knowledge search.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#business GoogleDiscoveryEngineChatEngine#business}
        '''
        result = self._values.get("business")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''Agent location for Agent creation, currently supported values: global/us/eu, it needs to be the same region as the Chat Engine.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#location GoogleDiscoveryEngineChatEngine#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDiscoveryEngineChatEngineChatEngineConfigAgentCreationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDiscoveryEngineChatEngineChatEngineConfigAgentCreationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineChatEngine.GoogleDiscoveryEngineChatEngineChatEngineConfigAgentCreationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__850339c9eca31576d67551f1ee64589569bde95be225f8bca5e88f0112a442be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__234454a0a77061fe9546d6bc9d361567546dc90c8eb6021a061b1cb235425b52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "business", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultLanguageCode")
    def default_language_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultLanguageCode"))

    @default_language_code.setter
    def default_language_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72fb347e4f66c928aec29e857a713de2bacc3aa781047d00612c331001319a7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultLanguageCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3310964595bb2634a0c123b90c95778a09b3d97c660cf785fc482f1f873fbf8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6e35fe7e2adbba68b0d2128437e8d49cc38c1eb7c8a496171303dbbd88082eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineChatEngineChatEngineConfigAgentCreationConfig]:
        return typing.cast(typing.Optional[GoogleDiscoveryEngineChatEngineChatEngineConfigAgentCreationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDiscoveryEngineChatEngineChatEngineConfigAgentCreationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bd2b27ea37aea3ebae0bd58f4be9ab5152d18d92388a337db417e71adb6dc5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDiscoveryEngineChatEngineChatEngineConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineChatEngine.GoogleDiscoveryEngineChatEngineChatEngineConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3275e4d4352e905606f7afe05a04898ececabb7516278ed66cbc4c37f3d143a6)
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
        :param default_language_code: The default language of the agent as a language tag. See `Language Support <https://cloud.google.com/dialogflow/docs/reference/language>`_ for a list of the currently supported language codes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#default_language_code GoogleDiscoveryEngineChatEngine#default_language_code}
        :param time_zone: The time zone of the agent from the `time zone database <https://www.iana.org/time-zones>`_, e.g., America/New_York, Europe/Paris. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#time_zone GoogleDiscoveryEngineChatEngine#time_zone}
        :param business: Name of the company, organization or other entity that the agent represents. Used for knowledge connector LLM prompt and for knowledge search. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#business GoogleDiscoveryEngineChatEngine#business}
        :param location: Agent location for Agent creation, currently supported values: global/us/eu, it needs to be the same region as the Chat Engine. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#location GoogleDiscoveryEngineChatEngine#location}
        '''
        value = GoogleDiscoveryEngineChatEngineChatEngineConfigAgentCreationConfig(
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
    ) -> GoogleDiscoveryEngineChatEngineChatEngineConfigAgentCreationConfigOutputReference:
        return typing.cast(GoogleDiscoveryEngineChatEngineChatEngineConfigAgentCreationConfigOutputReference, jsii.get(self, "agentCreationConfig"))

    @builtins.property
    @jsii.member(jsii_name="agentCreationConfigInput")
    def agent_creation_config_input(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineChatEngineChatEngineConfigAgentCreationConfig]:
        return typing.cast(typing.Optional[GoogleDiscoveryEngineChatEngineChatEngineConfigAgentCreationConfig], jsii.get(self, "agentCreationConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__1cfdcef29aed5b2132c0533f1ea712ee88b26f81e78b689296346e4167ae27ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowCrossRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dialogflowAgentToLink")
    def dialogflow_agent_to_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dialogflowAgentToLink"))

    @dialogflow_agent_to_link.setter
    def dialogflow_agent_to_link(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a697c5c1b6c449f8118820580fdacad348ee674723eb89bb733d22635bf43d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dialogflowAgentToLink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineChatEngineChatEngineConfig]:
        return typing.cast(typing.Optional[GoogleDiscoveryEngineChatEngineChatEngineConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDiscoveryEngineChatEngineChatEngineConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f21eb8bc2d646f311969757a11824f32d08dd335643943688db2e63c7b0c4b92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineChatEngine.GoogleDiscoveryEngineChatEngineChatEngineMetadata",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDiscoveryEngineChatEngineChatEngineMetadata:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDiscoveryEngineChatEngineChatEngineMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDiscoveryEngineChatEngineChatEngineMetadataList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineChatEngine.GoogleDiscoveryEngineChatEngineChatEngineMetadataList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d860f3a749f534fd3e5c9b571a4e890382d9a72129a9c74f0f75a6c29acb30fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDiscoveryEngineChatEngineChatEngineMetadataOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93c16a2ea7af51e4ee5bbf5037f598f84a2d74117ae2e91a8242193669ad57b9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDiscoveryEngineChatEngineChatEngineMetadataOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41ba3352617c90ccc594f22402fea35cd37c11c64371803b84f84c40016c38d8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__125a585f77efc5ef424caf928ac8b99a2ed77308282c245f103888a5cd2cf098)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6d69981633371f932c49253012188ba2d224349075520dee28ff52c8a9917ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDiscoveryEngineChatEngineChatEngineMetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineChatEngine.GoogleDiscoveryEngineChatEngineChatEngineMetadataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__064619f035e5bb0330fa48f733ba2c9bcba63f86903df4e19d337edfdd9f4967)
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
    ) -> typing.Optional[GoogleDiscoveryEngineChatEngineChatEngineMetadata]:
        return typing.cast(typing.Optional[GoogleDiscoveryEngineChatEngineChatEngineMetadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDiscoveryEngineChatEngineChatEngineMetadata],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a0e3d5ad597b7a6687e1f7af7dcef1a87f03bdc5c13ce89ffe862d971bfc4b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineChatEngine.GoogleDiscoveryEngineChatEngineCommonConfig",
    jsii_struct_bases=[],
    name_mapping={"company_name": "companyName"},
)
class GoogleDiscoveryEngineChatEngineCommonConfig:
    def __init__(self, *, company_name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param company_name: The name of the company, business or entity that is associated with the engine. Setting this may help improve LLM related features. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#company_name GoogleDiscoveryEngineChatEngine#company_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__718f4bf6aa8b68b03bc69cb90bf6a6721f13ac354f508b4873f04b9d6e0fa6f6)
            check_type(argname="argument company_name", value=company_name, expected_type=type_hints["company_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if company_name is not None:
            self._values["company_name"] = company_name

    @builtins.property
    def company_name(self) -> typing.Optional[builtins.str]:
        '''The name of the company, business or entity that is associated with the engine.

        Setting this may help improve LLM related features.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#company_name GoogleDiscoveryEngineChatEngine#company_name}
        '''
        result = self._values.get("company_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDiscoveryEngineChatEngineCommonConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDiscoveryEngineChatEngineCommonConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineChatEngine.GoogleDiscoveryEngineChatEngineCommonConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b585f784cda916bea81a62cac22090f45b3525b199c0fd31064bba9a2a91f75)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c0ce18ab64baee0234bd43e418f3186e72128b34af799907ee76952824d07e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "companyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineChatEngineCommonConfig]:
        return typing.cast(typing.Optional[GoogleDiscoveryEngineChatEngineCommonConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDiscoveryEngineChatEngineCommonConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ede44e6dbef0d67f2503dfc731d8afc3f469ee268a89ee7b00628d4ef39ba08b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineChatEngine.GoogleDiscoveryEngineChatEngineConfig",
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
class GoogleDiscoveryEngineChatEngineConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        chat_engine_config: typing.Union[GoogleDiscoveryEngineChatEngineChatEngineConfig, typing.Dict[builtins.str, typing.Any]],
        collection_id: builtins.str,
        data_store_ids: typing.Sequence[builtins.str],
        display_name: builtins.str,
        engine_id: builtins.str,
        location: builtins.str,
        common_config: typing.Optional[typing.Union[GoogleDiscoveryEngineChatEngineCommonConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        industry_vertical: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDiscoveryEngineChatEngineTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param chat_engine_config: chat_engine_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#chat_engine_config GoogleDiscoveryEngineChatEngine#chat_engine_config}
        :param collection_id: The collection ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#collection_id GoogleDiscoveryEngineChatEngine#collection_id}
        :param data_store_ids: The data stores associated with this engine. Multiple DataStores in the same Collection can be associated here. All listed DataStores must be 'SOLUTION_TYPE_CHAT'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#data_store_ids GoogleDiscoveryEngineChatEngine#data_store_ids}
        :param display_name: The display name of the engine. Should be human readable. UTF-8 encoded string with limit of 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#display_name GoogleDiscoveryEngineChatEngine#display_name}
        :param engine_id: The ID to use for chat engine. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#engine_id GoogleDiscoveryEngineChatEngine#engine_id}
        :param location: Location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#location GoogleDiscoveryEngineChatEngine#location}
        :param common_config: common_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#common_config GoogleDiscoveryEngineChatEngine#common_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#id GoogleDiscoveryEngineChatEngine#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param industry_vertical: The industry vertical that the chat engine registers. Vertical on Engine has to match vertical of the DataStore linked to the engine. Default value: "GENERIC" Possible values: ["GENERIC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#industry_vertical GoogleDiscoveryEngineChatEngine#industry_vertical}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#project GoogleDiscoveryEngineChatEngine#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#timeouts GoogleDiscoveryEngineChatEngine#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(chat_engine_config, dict):
            chat_engine_config = GoogleDiscoveryEngineChatEngineChatEngineConfig(**chat_engine_config)
        if isinstance(common_config, dict):
            common_config = GoogleDiscoveryEngineChatEngineCommonConfig(**common_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleDiscoveryEngineChatEngineTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27910f52f59b4c9489be4dcebfdff12747f37f6ac3d090a915b107f2cda90431)
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
    def chat_engine_config(self) -> GoogleDiscoveryEngineChatEngineChatEngineConfig:
        '''chat_engine_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#chat_engine_config GoogleDiscoveryEngineChatEngine#chat_engine_config}
        '''
        result = self._values.get("chat_engine_config")
        assert result is not None, "Required property 'chat_engine_config' is missing"
        return typing.cast(GoogleDiscoveryEngineChatEngineChatEngineConfig, result)

    @builtins.property
    def collection_id(self) -> builtins.str:
        '''The collection ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#collection_id GoogleDiscoveryEngineChatEngine#collection_id}
        '''
        result = self._values.get("collection_id")
        assert result is not None, "Required property 'collection_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_store_ids(self) -> typing.List[builtins.str]:
        '''The data stores associated with this engine.

        Multiple DataStores in the same Collection can be associated here. All listed DataStores must be 'SOLUTION_TYPE_CHAT'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#data_store_ids GoogleDiscoveryEngineChatEngine#data_store_ids}
        '''
        result = self._values.get("data_store_ids")
        assert result is not None, "Required property 'data_store_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''The display name of the engine. Should be human readable. UTF-8 encoded string with limit of 1024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#display_name GoogleDiscoveryEngineChatEngine#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def engine_id(self) -> builtins.str:
        '''The ID to use for chat engine.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#engine_id GoogleDiscoveryEngineChatEngine#engine_id}
        '''
        result = self._values.get("engine_id")
        assert result is not None, "Required property 'engine_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Location.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#location GoogleDiscoveryEngineChatEngine#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def common_config(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineChatEngineCommonConfig]:
        '''common_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#common_config GoogleDiscoveryEngineChatEngine#common_config}
        '''
        result = self._values.get("common_config")
        return typing.cast(typing.Optional[GoogleDiscoveryEngineChatEngineCommonConfig], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#id GoogleDiscoveryEngineChatEngine#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def industry_vertical(self) -> typing.Optional[builtins.str]:
        '''The industry vertical that the chat engine registers.

        Vertical on Engine has to match vertical of the DataStore linked to the engine. Default value: "GENERIC" Possible values: ["GENERIC"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#industry_vertical GoogleDiscoveryEngineChatEngine#industry_vertical}
        '''
        result = self._values.get("industry_vertical")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#project GoogleDiscoveryEngineChatEngine#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleDiscoveryEngineChatEngineTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#timeouts GoogleDiscoveryEngineChatEngine#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleDiscoveryEngineChatEngineTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDiscoveryEngineChatEngineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineChatEngine.GoogleDiscoveryEngineChatEngineTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleDiscoveryEngineChatEngineTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#create GoogleDiscoveryEngineChatEngine#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#delete GoogleDiscoveryEngineChatEngine#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#update GoogleDiscoveryEngineChatEngine#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea68aaace86ab030f89a9356a3aeb6e6957309fd1a6d31f697b86f4b50d309d3)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#create GoogleDiscoveryEngineChatEngine#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#delete GoogleDiscoveryEngineChatEngine#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_chat_engine#update GoogleDiscoveryEngineChatEngine#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDiscoveryEngineChatEngineTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDiscoveryEngineChatEngineTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineChatEngine.GoogleDiscoveryEngineChatEngineTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c91b17ae81a4f5e51d152cfc6e98e34dda17f66fd53a42f5d8b045ff249c21ee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c938b355dc9d2cd985a051a1dbec8537d9c1febbb279c1492c14c46af37a44f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1ca0eba689941c06500fc7c68893a8335cacac64c425c2c47e8c81591926707)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41363739103740ad67dc02bf45a8cc0ab294bd39a7627faae81124235cd21887)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDiscoveryEngineChatEngineTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDiscoveryEngineChatEngineTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDiscoveryEngineChatEngineTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5caac036c8b0c69d51549aed95120ca74498e9dfdb3001f51dbb6533ad32683b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleDiscoveryEngineChatEngine",
    "GoogleDiscoveryEngineChatEngineChatEngineConfig",
    "GoogleDiscoveryEngineChatEngineChatEngineConfigAgentCreationConfig",
    "GoogleDiscoveryEngineChatEngineChatEngineConfigAgentCreationConfigOutputReference",
    "GoogleDiscoveryEngineChatEngineChatEngineConfigOutputReference",
    "GoogleDiscoveryEngineChatEngineChatEngineMetadata",
    "GoogleDiscoveryEngineChatEngineChatEngineMetadataList",
    "GoogleDiscoveryEngineChatEngineChatEngineMetadataOutputReference",
    "GoogleDiscoveryEngineChatEngineCommonConfig",
    "GoogleDiscoveryEngineChatEngineCommonConfigOutputReference",
    "GoogleDiscoveryEngineChatEngineConfig",
    "GoogleDiscoveryEngineChatEngineTimeouts",
    "GoogleDiscoveryEngineChatEngineTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__d67f73bb2ab24d9b469b0ea73f74daea43ed7a9fa0d2f5913c03801fa433a8de(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    chat_engine_config: typing.Union[GoogleDiscoveryEngineChatEngineChatEngineConfig, typing.Dict[builtins.str, typing.Any]],
    collection_id: builtins.str,
    data_store_ids: typing.Sequence[builtins.str],
    display_name: builtins.str,
    engine_id: builtins.str,
    location: builtins.str,
    common_config: typing.Optional[typing.Union[GoogleDiscoveryEngineChatEngineCommonConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    industry_vertical: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDiscoveryEngineChatEngineTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__7d469dd8c3f719571b5ce7066975a32b8035480de4c79dde45069034fc7dd299(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17aae83cd4a2f530e993d2575719e795eb066fba80c6f44489cfeff578b002c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5db3ea55de591df897cc61bc4173719c1d1e945f9216be3007cecb8cc447622a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15559a8e47bf7afe7004295ce0846bffb0218cbe06c2aaa4be17896f9b7dca51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__221bafea61b695a569558fa7b1f9a68bbe456ac17ff7dabbcd87c153174fe60b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ee6a7cd7e543acbcc96959e98f002995b574ad0333a2400e83a5893625cf4dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__712650c321e783e68fd12ca641bed4bc8879de787992fb2dcd781ba28d66d960(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51252afa389fb74acef5adfeb7486afd4bef6a623d973bfb3a502277f5909204(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cddf4e6c5fba2e85722773f64fc2e9e6619a5ccd63da17c9a758304f3240945d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e95562fc5baae5ffa4b12850b477c77a0f252efca8710d97f770a93f227d735f(
    *,
    agent_creation_config: typing.Optional[typing.Union[GoogleDiscoveryEngineChatEngineChatEngineConfigAgentCreationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    allow_cross_region: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dialogflow_agent_to_link: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d13468486687d0225578506143ace046f62a1ab03689376be0286b6c70fe2d8(
    *,
    default_language_code: builtins.str,
    time_zone: builtins.str,
    business: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__850339c9eca31576d67551f1ee64589569bde95be225f8bca5e88f0112a442be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__234454a0a77061fe9546d6bc9d361567546dc90c8eb6021a061b1cb235425b52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72fb347e4f66c928aec29e857a713de2bacc3aa781047d00612c331001319a7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3310964595bb2634a0c123b90c95778a09b3d97c660cf785fc482f1f873fbf8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6e35fe7e2adbba68b0d2128437e8d49cc38c1eb7c8a496171303dbbd88082eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bd2b27ea37aea3ebae0bd58f4be9ab5152d18d92388a337db417e71adb6dc5e(
    value: typing.Optional[GoogleDiscoveryEngineChatEngineChatEngineConfigAgentCreationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3275e4d4352e905606f7afe05a04898ececabb7516278ed66cbc4c37f3d143a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cfdcef29aed5b2132c0533f1ea712ee88b26f81e78b689296346e4167ae27ab(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a697c5c1b6c449f8118820580fdacad348ee674723eb89bb733d22635bf43d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f21eb8bc2d646f311969757a11824f32d08dd335643943688db2e63c7b0c4b92(
    value: typing.Optional[GoogleDiscoveryEngineChatEngineChatEngineConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d860f3a749f534fd3e5c9b571a4e890382d9a72129a9c74f0f75a6c29acb30fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93c16a2ea7af51e4ee5bbf5037f598f84a2d74117ae2e91a8242193669ad57b9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41ba3352617c90ccc594f22402fea35cd37c11c64371803b84f84c40016c38d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__125a585f77efc5ef424caf928ac8b99a2ed77308282c245f103888a5cd2cf098(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6d69981633371f932c49253012188ba2d224349075520dee28ff52c8a9917ea(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__064619f035e5bb0330fa48f733ba2c9bcba63f86903df4e19d337edfdd9f4967(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a0e3d5ad597b7a6687e1f7af7dcef1a87f03bdc5c13ce89ffe862d971bfc4b3(
    value: typing.Optional[GoogleDiscoveryEngineChatEngineChatEngineMetadata],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__718f4bf6aa8b68b03bc69cb90bf6a6721f13ac354f508b4873f04b9d6e0fa6f6(
    *,
    company_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b585f784cda916bea81a62cac22090f45b3525b199c0fd31064bba9a2a91f75(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c0ce18ab64baee0234bd43e418f3186e72128b34af799907ee76952824d07e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ede44e6dbef0d67f2503dfc731d8afc3f469ee268a89ee7b00628d4ef39ba08b(
    value: typing.Optional[GoogleDiscoveryEngineChatEngineCommonConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27910f52f59b4c9489be4dcebfdff12747f37f6ac3d090a915b107f2cda90431(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    chat_engine_config: typing.Union[GoogleDiscoveryEngineChatEngineChatEngineConfig, typing.Dict[builtins.str, typing.Any]],
    collection_id: builtins.str,
    data_store_ids: typing.Sequence[builtins.str],
    display_name: builtins.str,
    engine_id: builtins.str,
    location: builtins.str,
    common_config: typing.Optional[typing.Union[GoogleDiscoveryEngineChatEngineCommonConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    industry_vertical: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDiscoveryEngineChatEngineTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea68aaace86ab030f89a9356a3aeb6e6957309fd1a6d31f697b86f4b50d309d3(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c91b17ae81a4f5e51d152cfc6e98e34dda17f66fd53a42f5d8b045ff249c21ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c938b355dc9d2cd985a051a1dbec8537d9c1febbb279c1492c14c46af37a44f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1ca0eba689941c06500fc7c68893a8335cacac64c425c2c47e8c81591926707(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41363739103740ad67dc02bf45a8cc0ab294bd39a7627faae81124235cd21887(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5caac036c8b0c69d51549aed95120ca74498e9dfdb3001f51dbb6533ad32683b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDiscoveryEngineChatEngineTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
