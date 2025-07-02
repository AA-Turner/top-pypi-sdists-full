r'''
# `google_dialogflow_cx_generative_settings`

Refer to the Terraform Registry for docs: [`google_dialogflow_cx_generative_settings`](https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings).
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


class GoogleDialogflowCxGenerativeSettings(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxGenerativeSettings.GoogleDialogflowCxGenerativeSettings",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings google_dialogflow_cx_generative_settings}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        language_code: builtins.str,
        fallback_settings: typing.Optional[typing.Union["GoogleDialogflowCxGenerativeSettingsFallbackSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        generative_safety_settings: typing.Optional[typing.Union["GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettings", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        knowledge_connector_settings: typing.Optional[typing.Union["GoogleDialogflowCxGenerativeSettingsKnowledgeConnectorSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        llm_model_settings: typing.Optional[typing.Union["GoogleDialogflowCxGenerativeSettingsLlmModelSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        parent: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDialogflowCxGenerativeSettingsTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings google_dialogflow_cx_generative_settings} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param language_code: Language for this settings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#language_code GoogleDialogflowCxGenerativeSettings#language_code}
        :param fallback_settings: fallback_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#fallback_settings GoogleDialogflowCxGenerativeSettings#fallback_settings}
        :param generative_safety_settings: generative_safety_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#generative_safety_settings GoogleDialogflowCxGenerativeSettings#generative_safety_settings}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#id GoogleDialogflowCxGenerativeSettings#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param knowledge_connector_settings: knowledge_connector_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#knowledge_connector_settings GoogleDialogflowCxGenerativeSettings#knowledge_connector_settings}
        :param llm_model_settings: llm_model_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#llm_model_settings GoogleDialogflowCxGenerativeSettings#llm_model_settings}
        :param parent: The agent to create a flow for. Format: projects//locations//agents/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#parent GoogleDialogflowCxGenerativeSettings#parent}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#timeouts GoogleDialogflowCxGenerativeSettings#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cad6c470f2e90c88e698e666607bde7960d5b0258ff977e4088895f939a31166)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDialogflowCxGenerativeSettingsConfig(
            language_code=language_code,
            fallback_settings=fallback_settings,
            generative_safety_settings=generative_safety_settings,
            id=id,
            knowledge_connector_settings=knowledge_connector_settings,
            llm_model_settings=llm_model_settings,
            parent=parent,
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
        '''Generates CDKTF code for importing a GoogleDialogflowCxGenerativeSettings resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDialogflowCxGenerativeSettings to import.
        :param import_from_id: The id of the existing GoogleDialogflowCxGenerativeSettings that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDialogflowCxGenerativeSettings to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65f305373b74d2125b8ec2d4a0b383f7f53fe3b2f22d045771cd3a948f736892)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putFallbackSettings")
    def put_fallback_settings(
        self,
        *,
        prompt_templates: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates", typing.Dict[builtins.str, typing.Any]]]]] = None,
        selected_prompt: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param prompt_templates: prompt_templates block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#prompt_templates GoogleDialogflowCxGenerativeSettings#prompt_templates}
        :param selected_prompt: Display name of the selected prompt. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#selected_prompt GoogleDialogflowCxGenerativeSettings#selected_prompt}
        '''
        value = GoogleDialogflowCxGenerativeSettingsFallbackSettings(
            prompt_templates=prompt_templates, selected_prompt=selected_prompt
        )

        return typing.cast(None, jsii.invoke(self, "putFallbackSettings", [value]))

    @jsii.member(jsii_name="putGenerativeSafetySettings")
    def put_generative_safety_settings(
        self,
        *,
        banned_phrases: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_banned_phrase_match_strategy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param banned_phrases: banned_phrases block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#banned_phrases GoogleDialogflowCxGenerativeSettings#banned_phrases}
        :param default_banned_phrase_match_strategy: Optional. Default phrase match strategy for banned phrases. See `PhraseMatchStrategy <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/GenerativeSettings#phrasematchstrategy>`_ for valid values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#default_banned_phrase_match_strategy GoogleDialogflowCxGenerativeSettings#default_banned_phrase_match_strategy}
        '''
        value = GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettings(
            banned_phrases=banned_phrases,
            default_banned_phrase_match_strategy=default_banned_phrase_match_strategy,
        )

        return typing.cast(None, jsii.invoke(self, "putGenerativeSafetySettings", [value]))

    @jsii.member(jsii_name="putKnowledgeConnectorSettings")
    def put_knowledge_connector_settings(
        self,
        *,
        agent: typing.Optional[builtins.str] = None,
        agent_identity: typing.Optional[builtins.str] = None,
        agent_scope: typing.Optional[builtins.str] = None,
        business: typing.Optional[builtins.str] = None,
        business_description: typing.Optional[builtins.str] = None,
        disable_data_store_fallback: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param agent: Name of the virtual agent. Used for LLM prompt. Can be left empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#agent GoogleDialogflowCxGenerativeSettings#agent}
        :param agent_identity: Identity of the agent, e.g. "virtual agent", "AI assistant". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#agent_identity GoogleDialogflowCxGenerativeSettings#agent_identity}
        :param agent_scope: Agent scope, e.g. "Example company website", "internal Example company website for employees", "manual of car owner". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#agent_scope GoogleDialogflowCxGenerativeSettings#agent_scope}
        :param business: Name of the company, organization or other entity that the agent represents. Used for knowledge connector LLM prompt and for knowledge search. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#business GoogleDialogflowCxGenerativeSettings#business}
        :param business_description: Company description, used for LLM prompt, e.g. "a family company selling freshly roasted coffee beans".''. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#business_description GoogleDialogflowCxGenerativeSettings#business_description}
        :param disable_data_store_fallback: Whether to disable fallback to Data Store search results (in case the LLM couldn't pick a proper answer). Per default the feature is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#disable_data_store_fallback GoogleDialogflowCxGenerativeSettings#disable_data_store_fallback}
        '''
        value = GoogleDialogflowCxGenerativeSettingsKnowledgeConnectorSettings(
            agent=agent,
            agent_identity=agent_identity,
            agent_scope=agent_scope,
            business=business,
            business_description=business_description,
            disable_data_store_fallback=disable_data_store_fallback,
        )

        return typing.cast(None, jsii.invoke(self, "putKnowledgeConnectorSettings", [value]))

    @jsii.member(jsii_name="putLlmModelSettings")
    def put_llm_model_settings(
        self,
        *,
        model: typing.Optional[builtins.str] = None,
        prompt_text: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param model: The selected LLM model. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#model GoogleDialogflowCxGenerativeSettings#model}
        :param prompt_text: The custom prompt to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#prompt_text GoogleDialogflowCxGenerativeSettings#prompt_text}
        '''
        value = GoogleDialogflowCxGenerativeSettingsLlmModelSettings(
            model=model, prompt_text=prompt_text
        )

        return typing.cast(None, jsii.invoke(self, "putLlmModelSettings", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#create GoogleDialogflowCxGenerativeSettings#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#delete GoogleDialogflowCxGenerativeSettings#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#update GoogleDialogflowCxGenerativeSettings#update}.
        '''
        value = GoogleDialogflowCxGenerativeSettingsTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetFallbackSettings")
    def reset_fallback_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFallbackSettings", []))

    @jsii.member(jsii_name="resetGenerativeSafetySettings")
    def reset_generative_safety_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGenerativeSafetySettings", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKnowledgeConnectorSettings")
    def reset_knowledge_connector_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKnowledgeConnectorSettings", []))

    @jsii.member(jsii_name="resetLlmModelSettings")
    def reset_llm_model_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLlmModelSettings", []))

    @jsii.member(jsii_name="resetParent")
    def reset_parent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParent", []))

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
    @jsii.member(jsii_name="fallbackSettings")
    def fallback_settings(
        self,
    ) -> "GoogleDialogflowCxGenerativeSettingsFallbackSettingsOutputReference":
        return typing.cast("GoogleDialogflowCxGenerativeSettingsFallbackSettingsOutputReference", jsii.get(self, "fallbackSettings"))

    @builtins.property
    @jsii.member(jsii_name="generativeSafetySettings")
    def generative_safety_settings(
        self,
    ) -> "GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettingsOutputReference":
        return typing.cast("GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettingsOutputReference", jsii.get(self, "generativeSafetySettings"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeConnectorSettings")
    def knowledge_connector_settings(
        self,
    ) -> "GoogleDialogflowCxGenerativeSettingsKnowledgeConnectorSettingsOutputReference":
        return typing.cast("GoogleDialogflowCxGenerativeSettingsKnowledgeConnectorSettingsOutputReference", jsii.get(self, "knowledgeConnectorSettings"))

    @builtins.property
    @jsii.member(jsii_name="llmModelSettings")
    def llm_model_settings(
        self,
    ) -> "GoogleDialogflowCxGenerativeSettingsLlmModelSettingsOutputReference":
        return typing.cast("GoogleDialogflowCxGenerativeSettingsLlmModelSettingsOutputReference", jsii.get(self, "llmModelSettings"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleDialogflowCxGenerativeSettingsTimeoutsOutputReference":
        return typing.cast("GoogleDialogflowCxGenerativeSettingsTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="fallbackSettingsInput")
    def fallback_settings_input(
        self,
    ) -> typing.Optional["GoogleDialogflowCxGenerativeSettingsFallbackSettings"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxGenerativeSettingsFallbackSettings"], jsii.get(self, "fallbackSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="generativeSafetySettingsInput")
    def generative_safety_settings_input(
        self,
    ) -> typing.Optional["GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettings"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettings"], jsii.get(self, "generativeSafetySettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeConnectorSettingsInput")
    def knowledge_connector_settings_input(
        self,
    ) -> typing.Optional["GoogleDialogflowCxGenerativeSettingsKnowledgeConnectorSettings"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxGenerativeSettingsKnowledgeConnectorSettings"], jsii.get(self, "knowledgeConnectorSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="languageCodeInput")
    def language_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "languageCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="llmModelSettingsInput")
    def llm_model_settings_input(
        self,
    ) -> typing.Optional["GoogleDialogflowCxGenerativeSettingsLlmModelSettings"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxGenerativeSettingsLlmModelSettings"], jsii.get(self, "llmModelSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="parentInput")
    def parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDialogflowCxGenerativeSettingsTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDialogflowCxGenerativeSettingsTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1183393965f146b9a76603e6b157c35ed251ef0fd81ad57806fc5a11c3b189c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="languageCode")
    def language_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "languageCode"))

    @language_code.setter
    def language_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85ddc4e974092c5a54583f62adf08294a6ac5c92d45914179484b7227bb05e0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "languageCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25438e77f7e4ad8c1bd4d6562785a083650f9a3a5c5d139931d36ff2acde8cdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxGenerativeSettings.GoogleDialogflowCxGenerativeSettingsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "language_code": "languageCode",
        "fallback_settings": "fallbackSettings",
        "generative_safety_settings": "generativeSafetySettings",
        "id": "id",
        "knowledge_connector_settings": "knowledgeConnectorSettings",
        "llm_model_settings": "llmModelSettings",
        "parent": "parent",
        "timeouts": "timeouts",
    },
)
class GoogleDialogflowCxGenerativeSettingsConfig(
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
        language_code: builtins.str,
        fallback_settings: typing.Optional[typing.Union["GoogleDialogflowCxGenerativeSettingsFallbackSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        generative_safety_settings: typing.Optional[typing.Union["GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettings", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        knowledge_connector_settings: typing.Optional[typing.Union["GoogleDialogflowCxGenerativeSettingsKnowledgeConnectorSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        llm_model_settings: typing.Optional[typing.Union["GoogleDialogflowCxGenerativeSettingsLlmModelSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        parent: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDialogflowCxGenerativeSettingsTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param language_code: Language for this settings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#language_code GoogleDialogflowCxGenerativeSettings#language_code}
        :param fallback_settings: fallback_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#fallback_settings GoogleDialogflowCxGenerativeSettings#fallback_settings}
        :param generative_safety_settings: generative_safety_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#generative_safety_settings GoogleDialogflowCxGenerativeSettings#generative_safety_settings}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#id GoogleDialogflowCxGenerativeSettings#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param knowledge_connector_settings: knowledge_connector_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#knowledge_connector_settings GoogleDialogflowCxGenerativeSettings#knowledge_connector_settings}
        :param llm_model_settings: llm_model_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#llm_model_settings GoogleDialogflowCxGenerativeSettings#llm_model_settings}
        :param parent: The agent to create a flow for. Format: projects//locations//agents/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#parent GoogleDialogflowCxGenerativeSettings#parent}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#timeouts GoogleDialogflowCxGenerativeSettings#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(fallback_settings, dict):
            fallback_settings = GoogleDialogflowCxGenerativeSettingsFallbackSettings(**fallback_settings)
        if isinstance(generative_safety_settings, dict):
            generative_safety_settings = GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettings(**generative_safety_settings)
        if isinstance(knowledge_connector_settings, dict):
            knowledge_connector_settings = GoogleDialogflowCxGenerativeSettingsKnowledgeConnectorSettings(**knowledge_connector_settings)
        if isinstance(llm_model_settings, dict):
            llm_model_settings = GoogleDialogflowCxGenerativeSettingsLlmModelSettings(**llm_model_settings)
        if isinstance(timeouts, dict):
            timeouts = GoogleDialogflowCxGenerativeSettingsTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b86c7283eb3849fb2ff8e261e136ef7acb188386c8db81e4c2ebca714d25fee0)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument language_code", value=language_code, expected_type=type_hints["language_code"])
            check_type(argname="argument fallback_settings", value=fallback_settings, expected_type=type_hints["fallback_settings"])
            check_type(argname="argument generative_safety_settings", value=generative_safety_settings, expected_type=type_hints["generative_safety_settings"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument knowledge_connector_settings", value=knowledge_connector_settings, expected_type=type_hints["knowledge_connector_settings"])
            check_type(argname="argument llm_model_settings", value=llm_model_settings, expected_type=type_hints["llm_model_settings"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "language_code": language_code,
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
        if fallback_settings is not None:
            self._values["fallback_settings"] = fallback_settings
        if generative_safety_settings is not None:
            self._values["generative_safety_settings"] = generative_safety_settings
        if id is not None:
            self._values["id"] = id
        if knowledge_connector_settings is not None:
            self._values["knowledge_connector_settings"] = knowledge_connector_settings
        if llm_model_settings is not None:
            self._values["llm_model_settings"] = llm_model_settings
        if parent is not None:
            self._values["parent"] = parent
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
    def language_code(self) -> builtins.str:
        '''Language for this settings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#language_code GoogleDialogflowCxGenerativeSettings#language_code}
        '''
        result = self._values.get("language_code")
        assert result is not None, "Required property 'language_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fallback_settings(
        self,
    ) -> typing.Optional["GoogleDialogflowCxGenerativeSettingsFallbackSettings"]:
        '''fallback_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#fallback_settings GoogleDialogflowCxGenerativeSettings#fallback_settings}
        '''
        result = self._values.get("fallback_settings")
        return typing.cast(typing.Optional["GoogleDialogflowCxGenerativeSettingsFallbackSettings"], result)

    @builtins.property
    def generative_safety_settings(
        self,
    ) -> typing.Optional["GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettings"]:
        '''generative_safety_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#generative_safety_settings GoogleDialogflowCxGenerativeSettings#generative_safety_settings}
        '''
        result = self._values.get("generative_safety_settings")
        return typing.cast(typing.Optional["GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettings"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#id GoogleDialogflowCxGenerativeSettings#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def knowledge_connector_settings(
        self,
    ) -> typing.Optional["GoogleDialogflowCxGenerativeSettingsKnowledgeConnectorSettings"]:
        '''knowledge_connector_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#knowledge_connector_settings GoogleDialogflowCxGenerativeSettings#knowledge_connector_settings}
        '''
        result = self._values.get("knowledge_connector_settings")
        return typing.cast(typing.Optional["GoogleDialogflowCxGenerativeSettingsKnowledgeConnectorSettings"], result)

    @builtins.property
    def llm_model_settings(
        self,
    ) -> typing.Optional["GoogleDialogflowCxGenerativeSettingsLlmModelSettings"]:
        '''llm_model_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#llm_model_settings GoogleDialogflowCxGenerativeSettings#llm_model_settings}
        '''
        result = self._values.get("llm_model_settings")
        return typing.cast(typing.Optional["GoogleDialogflowCxGenerativeSettingsLlmModelSettings"], result)

    @builtins.property
    def parent(self) -> typing.Optional[builtins.str]:
        '''The agent to create a flow for. Format: projects//locations//agents/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#parent GoogleDialogflowCxGenerativeSettings#parent}
        '''
        result = self._values.get("parent")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleDialogflowCxGenerativeSettingsTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#timeouts GoogleDialogflowCxGenerativeSettings#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleDialogflowCxGenerativeSettingsTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxGenerativeSettingsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxGenerativeSettings.GoogleDialogflowCxGenerativeSettingsFallbackSettings",
    jsii_struct_bases=[],
    name_mapping={
        "prompt_templates": "promptTemplates",
        "selected_prompt": "selectedPrompt",
    },
)
class GoogleDialogflowCxGenerativeSettingsFallbackSettings:
    def __init__(
        self,
        *,
        prompt_templates: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates", typing.Dict[builtins.str, typing.Any]]]]] = None,
        selected_prompt: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param prompt_templates: prompt_templates block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#prompt_templates GoogleDialogflowCxGenerativeSettings#prompt_templates}
        :param selected_prompt: Display name of the selected prompt. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#selected_prompt GoogleDialogflowCxGenerativeSettings#selected_prompt}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebb91d8d9a7af1fc2eb8b7cbf8392d119f3487487fff3154b6e20c5f02d15bb7)
            check_type(argname="argument prompt_templates", value=prompt_templates, expected_type=type_hints["prompt_templates"])
            check_type(argname="argument selected_prompt", value=selected_prompt, expected_type=type_hints["selected_prompt"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if prompt_templates is not None:
            self._values["prompt_templates"] = prompt_templates
        if selected_prompt is not None:
            self._values["selected_prompt"] = selected_prompt

    @builtins.property
    def prompt_templates(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates"]]]:
        '''prompt_templates block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#prompt_templates GoogleDialogflowCxGenerativeSettings#prompt_templates}
        '''
        result = self._values.get("prompt_templates")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates"]]], result)

    @builtins.property
    def selected_prompt(self) -> typing.Optional[builtins.str]:
        '''Display name of the selected prompt.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#selected_prompt GoogleDialogflowCxGenerativeSettings#selected_prompt}
        '''
        result = self._values.get("selected_prompt")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxGenerativeSettingsFallbackSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxGenerativeSettingsFallbackSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxGenerativeSettings.GoogleDialogflowCxGenerativeSettingsFallbackSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f4dc3ef95fede0a3a63bc0ccc787547a2df08151b7f146a92b6024ad9dbc2ea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPromptTemplates")
    def put_prompt_templates(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a2c27c20a0db20927e5f9c203a9512937373e2893b418405c5aa2c8392ba95d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPromptTemplates", [value]))

    @jsii.member(jsii_name="resetPromptTemplates")
    def reset_prompt_templates(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPromptTemplates", []))

    @jsii.member(jsii_name="resetSelectedPrompt")
    def reset_selected_prompt(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelectedPrompt", []))

    @builtins.property
    @jsii.member(jsii_name="promptTemplates")
    def prompt_templates(
        self,
    ) -> "GoogleDialogflowCxGenerativeSettingsFallbackSettingsPromptTemplatesList":
        return typing.cast("GoogleDialogflowCxGenerativeSettingsFallbackSettingsPromptTemplatesList", jsii.get(self, "promptTemplates"))

    @builtins.property
    @jsii.member(jsii_name="promptTemplatesInput")
    def prompt_templates_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates"]]], jsii.get(self, "promptTemplatesInput"))

    @builtins.property
    @jsii.member(jsii_name="selectedPromptInput")
    def selected_prompt_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "selectedPromptInput"))

    @builtins.property
    @jsii.member(jsii_name="selectedPrompt")
    def selected_prompt(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selectedPrompt"))

    @selected_prompt.setter
    def selected_prompt(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f36414f53df1616179ad98aae625bd4eb6b114eedcd08f11bc6bc37e98f909cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "selectedPrompt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxGenerativeSettingsFallbackSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowCxGenerativeSettingsFallbackSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxGenerativeSettingsFallbackSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7258ed9bdcf620fd524f55f81e05b8baddecb483c4f8c2c4147928978bd630cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxGenerativeSettings.GoogleDialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates",
    jsii_struct_bases=[],
    name_mapping={
        "display_name": "displayName",
        "frozen": "frozen",
        "prompt_text": "promptText",
    },
)
class GoogleDialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates:
    def __init__(
        self,
        *,
        display_name: typing.Optional[builtins.str] = None,
        frozen: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prompt_text: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param display_name: Prompt name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#display_name GoogleDialogflowCxGenerativeSettings#display_name}
        :param frozen: If the flag is true, the prompt is frozen and cannot be modified by users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#frozen GoogleDialogflowCxGenerativeSettings#frozen}
        :param prompt_text: Prompt text that is sent to a LLM on no-match default, placeholders are filled downstream. For example: "Here is a conversation $conversation, a response is: " Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#prompt_text GoogleDialogflowCxGenerativeSettings#prompt_text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff3a653f809e257093e4f6ffea3b0c0de56dec485e583bd0fe4faa0a05512b0b)
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument frozen", value=frozen, expected_type=type_hints["frozen"])
            check_type(argname="argument prompt_text", value=prompt_text, expected_type=type_hints["prompt_text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if display_name is not None:
            self._values["display_name"] = display_name
        if frozen is not None:
            self._values["frozen"] = frozen
        if prompt_text is not None:
            self._values["prompt_text"] = prompt_text

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Prompt name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#display_name GoogleDialogflowCxGenerativeSettings#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def frozen(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the flag is true, the prompt is frozen and cannot be modified by users.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#frozen GoogleDialogflowCxGenerativeSettings#frozen}
        '''
        result = self._values.get("frozen")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prompt_text(self) -> typing.Optional[builtins.str]:
        '''Prompt text that is sent to a LLM on no-match default, placeholders are filled downstream.

        For example: "Here is a conversation $conversation, a response is: "

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#prompt_text GoogleDialogflowCxGenerativeSettings#prompt_text}
        '''
        result = self._values.get("prompt_text")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxGenerativeSettingsFallbackSettingsPromptTemplatesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxGenerativeSettings.GoogleDialogflowCxGenerativeSettingsFallbackSettingsPromptTemplatesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a668a7c4ec9f16ce23b1be3bef522319d55143473590d10f493990fb6aac663f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDialogflowCxGenerativeSettingsFallbackSettingsPromptTemplatesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f137bc189ef0117a4463e924a8ef23b022121482da16f5703a3f3ce19af90ed)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDialogflowCxGenerativeSettingsFallbackSettingsPromptTemplatesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8b51d11130f1daabdc3945ce58dcfc109dcc8b7f0fa86a111d0cea04217154d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b177591b60e76b6d5ec8f3da1234346e5500986891b5b61cf3176bf962ec20e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc5b42b387012f51b35986290562d178b80ba1298ef979a39bf51e06e873bf5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56fe32fc2e92950e01a36930e32012c4c2ff56147bf2b508f53acc9f90437299)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxGenerativeSettingsFallbackSettingsPromptTemplatesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxGenerativeSettings.GoogleDialogflowCxGenerativeSettingsFallbackSettingsPromptTemplatesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0d55c575d84a33003262611d89c3c821041155a658e179cd07141054f7c56e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetFrozen")
    def reset_frozen(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFrozen", []))

    @jsii.member(jsii_name="resetPromptText")
    def reset_prompt_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPromptText", []))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="frozenInput")
    def frozen_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "frozenInput"))

    @builtins.property
    @jsii.member(jsii_name="promptTextInput")
    def prompt_text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "promptTextInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17e30a4ca1cd35c4c08189afca59a3982461e6a707b03124d706e08b9490b189)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="frozen")
    def frozen(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "frozen"))

    @frozen.setter
    def frozen(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e710b76c4f50beece475d8b0627a2e8a85b488fe9ad87a437941d311b10af95a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frozen", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="promptText")
    def prompt_text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "promptText"))

    @prompt_text.setter
    def prompt_text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4810d3408006cbaae17ee3d4abf9f0d2cbdeb8e292e2fa949febe7f887772ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "promptText", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eca0503e1bf6e9063ce4febc86fc6e45e6c953dbdb3b2d8db6c98ced5259542)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxGenerativeSettings.GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettings",
    jsii_struct_bases=[],
    name_mapping={
        "banned_phrases": "bannedPhrases",
        "default_banned_phrase_match_strategy": "defaultBannedPhraseMatchStrategy",
    },
)
class GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettings:
    def __init__(
        self,
        *,
        banned_phrases: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_banned_phrase_match_strategy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param banned_phrases: banned_phrases block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#banned_phrases GoogleDialogflowCxGenerativeSettings#banned_phrases}
        :param default_banned_phrase_match_strategy: Optional. Default phrase match strategy for banned phrases. See `PhraseMatchStrategy <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/GenerativeSettings#phrasematchstrategy>`_ for valid values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#default_banned_phrase_match_strategy GoogleDialogflowCxGenerativeSettings#default_banned_phrase_match_strategy}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ebd352961140bc4b5fa9ff9850ed50746d8a1ab8ef25c6418270ac824900ca9)
            check_type(argname="argument banned_phrases", value=banned_phrases, expected_type=type_hints["banned_phrases"])
            check_type(argname="argument default_banned_phrase_match_strategy", value=default_banned_phrase_match_strategy, expected_type=type_hints["default_banned_phrase_match_strategy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if banned_phrases is not None:
            self._values["banned_phrases"] = banned_phrases
        if default_banned_phrase_match_strategy is not None:
            self._values["default_banned_phrase_match_strategy"] = default_banned_phrase_match_strategy

    @builtins.property
    def banned_phrases(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases"]]]:
        '''banned_phrases block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#banned_phrases GoogleDialogflowCxGenerativeSettings#banned_phrases}
        '''
        result = self._values.get("banned_phrases")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases"]]], result)

    @builtins.property
    def default_banned_phrase_match_strategy(self) -> typing.Optional[builtins.str]:
        '''Optional. Default phrase match strategy for banned phrases. See `PhraseMatchStrategy <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/GenerativeSettings#phrasematchstrategy>`_ for valid values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#default_banned_phrase_match_strategy GoogleDialogflowCxGenerativeSettings#default_banned_phrase_match_strategy}
        '''
        result = self._values.get("default_banned_phrase_match_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxGenerativeSettings.GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases",
    jsii_struct_bases=[],
    name_mapping={"language_code": "languageCode", "text": "text"},
)
class GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases:
    def __init__(self, *, language_code: builtins.str, text: builtins.str) -> None:
        '''
        :param language_code: Language code of the phrase. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#language_code GoogleDialogflowCxGenerativeSettings#language_code}
        :param text: Text input which can be used for prompt or banned phrases. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#text GoogleDialogflowCxGenerativeSettings#text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__423317be8ff6df7f63f00f6afafe1bbfc99d73cd40d4a49572cb0efc69a3b93c)
            check_type(argname="argument language_code", value=language_code, expected_type=type_hints["language_code"])
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "language_code": language_code,
            "text": text,
        }

    @builtins.property
    def language_code(self) -> builtins.str:
        '''Language code of the phrase.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#language_code GoogleDialogflowCxGenerativeSettings#language_code}
        '''
        result = self._values.get("language_code")
        assert result is not None, "Required property 'language_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def text(self) -> builtins.str:
        '''Text input which can be used for prompt or banned phrases.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#text GoogleDialogflowCxGenerativeSettings#text}
        '''
        result = self._values.get("text")
        assert result is not None, "Required property 'text' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrasesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxGenerativeSettings.GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrasesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__05b226c46c300b1f3ac7884e759e025e65b3625f48ad9b80eac226ad087a9f9c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrasesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00f1eb520a0642b438a1c699344ad44af93fcfc5902b50371f40911ec1e7bd8f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrasesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__137e7b41a0d2a4df0923cb6d707e9788e387d6e53fb27172953a616bda74b23b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aee03e9ea300ab0acd6bd02a8d7fa6831b0178fd199f4b9464473d4e2255a5cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e97faeeeaa923b2297524ab8af0da68a230024bf0f52f9cd71566db9c29f8fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af3e682aec293bff1ec89f92d6a96d7c936dde082624d6c2bdefe7ff9def462e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrasesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxGenerativeSettings.GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrasesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9fadf512ea9970fab9f9c449069a55e0c9161437c3c3cb08168a90d55fb2125d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="languageCodeInput")
    def language_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "languageCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="textInput")
    def text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "textInput"))

    @builtins.property
    @jsii.member(jsii_name="languageCode")
    def language_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "languageCode"))

    @language_code.setter
    def language_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96f089788d1e7fffe0104b527704148cfa2f079b9ddfb08eef85a6866ac4c64c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "languageCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "text"))

    @text.setter
    def text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4ca9320e74e0ad69f4126bde730b18107ad0ab05214111317e53254a09c69d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "text", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4aa62a608255b3762a24459e660e55e5bbbee7b5e6e6f5175ec6bf82eedf8b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxGenerativeSettings.GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__719b5de998e81763bada70c04b8ea3b72a6bec9aa5ff4a2d8135c66e05bc23ac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBannedPhrases")
    def put_banned_phrases(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c7e0bfca3a96bcbda5e2e701351e189918f975f40887ec16eda573974948695)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBannedPhrases", [value]))

    @jsii.member(jsii_name="resetBannedPhrases")
    def reset_banned_phrases(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBannedPhrases", []))

    @jsii.member(jsii_name="resetDefaultBannedPhraseMatchStrategy")
    def reset_default_banned_phrase_match_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultBannedPhraseMatchStrategy", []))

    @builtins.property
    @jsii.member(jsii_name="bannedPhrases")
    def banned_phrases(
        self,
    ) -> GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrasesList:
        return typing.cast(GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrasesList, jsii.get(self, "bannedPhrases"))

    @builtins.property
    @jsii.member(jsii_name="bannedPhrasesInput")
    def banned_phrases_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases]]], jsii.get(self, "bannedPhrasesInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultBannedPhraseMatchStrategyInput")
    def default_banned_phrase_match_strategy_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultBannedPhraseMatchStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultBannedPhraseMatchStrategy")
    def default_banned_phrase_match_strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultBannedPhraseMatchStrategy"))

    @default_banned_phrase_match_strategy.setter
    def default_banned_phrase_match_strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b723cc490449dfff1995f05dbaab38aa53ec3751f755e2efe191bc67c6bc6da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultBannedPhraseMatchStrategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettings]:
        return typing.cast(typing.Optional[GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__041a5d46527e7b601977a360c7af805bbc514cb3891e697aa201528158c81b8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxGenerativeSettings.GoogleDialogflowCxGenerativeSettingsKnowledgeConnectorSettings",
    jsii_struct_bases=[],
    name_mapping={
        "agent": "agent",
        "agent_identity": "agentIdentity",
        "agent_scope": "agentScope",
        "business": "business",
        "business_description": "businessDescription",
        "disable_data_store_fallback": "disableDataStoreFallback",
    },
)
class GoogleDialogflowCxGenerativeSettingsKnowledgeConnectorSettings:
    def __init__(
        self,
        *,
        agent: typing.Optional[builtins.str] = None,
        agent_identity: typing.Optional[builtins.str] = None,
        agent_scope: typing.Optional[builtins.str] = None,
        business: typing.Optional[builtins.str] = None,
        business_description: typing.Optional[builtins.str] = None,
        disable_data_store_fallback: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param agent: Name of the virtual agent. Used for LLM prompt. Can be left empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#agent GoogleDialogflowCxGenerativeSettings#agent}
        :param agent_identity: Identity of the agent, e.g. "virtual agent", "AI assistant". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#agent_identity GoogleDialogflowCxGenerativeSettings#agent_identity}
        :param agent_scope: Agent scope, e.g. "Example company website", "internal Example company website for employees", "manual of car owner". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#agent_scope GoogleDialogflowCxGenerativeSettings#agent_scope}
        :param business: Name of the company, organization or other entity that the agent represents. Used for knowledge connector LLM prompt and for knowledge search. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#business GoogleDialogflowCxGenerativeSettings#business}
        :param business_description: Company description, used for LLM prompt, e.g. "a family company selling freshly roasted coffee beans".''. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#business_description GoogleDialogflowCxGenerativeSettings#business_description}
        :param disable_data_store_fallback: Whether to disable fallback to Data Store search results (in case the LLM couldn't pick a proper answer). Per default the feature is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#disable_data_store_fallback GoogleDialogflowCxGenerativeSettings#disable_data_store_fallback}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__008ae4a1cd9688a3ba47d75019f6c9ed6228a2632757b478421b76a25ea43ffb)
            check_type(argname="argument agent", value=agent, expected_type=type_hints["agent"])
            check_type(argname="argument agent_identity", value=agent_identity, expected_type=type_hints["agent_identity"])
            check_type(argname="argument agent_scope", value=agent_scope, expected_type=type_hints["agent_scope"])
            check_type(argname="argument business", value=business, expected_type=type_hints["business"])
            check_type(argname="argument business_description", value=business_description, expected_type=type_hints["business_description"])
            check_type(argname="argument disable_data_store_fallback", value=disable_data_store_fallback, expected_type=type_hints["disable_data_store_fallback"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if agent is not None:
            self._values["agent"] = agent
        if agent_identity is not None:
            self._values["agent_identity"] = agent_identity
        if agent_scope is not None:
            self._values["agent_scope"] = agent_scope
        if business is not None:
            self._values["business"] = business
        if business_description is not None:
            self._values["business_description"] = business_description
        if disable_data_store_fallback is not None:
            self._values["disable_data_store_fallback"] = disable_data_store_fallback

    @builtins.property
    def agent(self) -> typing.Optional[builtins.str]:
        '''Name of the virtual agent. Used for LLM prompt. Can be left empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#agent GoogleDialogflowCxGenerativeSettings#agent}
        '''
        result = self._values.get("agent")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def agent_identity(self) -> typing.Optional[builtins.str]:
        '''Identity of the agent, e.g. "virtual agent", "AI assistant".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#agent_identity GoogleDialogflowCxGenerativeSettings#agent_identity}
        '''
        result = self._values.get("agent_identity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def agent_scope(self) -> typing.Optional[builtins.str]:
        '''Agent scope, e.g. "Example company website", "internal Example company website for employees", "manual of car owner".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#agent_scope GoogleDialogflowCxGenerativeSettings#agent_scope}
        '''
        result = self._values.get("agent_scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def business(self) -> typing.Optional[builtins.str]:
        '''Name of the company, organization or other entity that the agent represents.

        Used for knowledge connector LLM prompt and for knowledge search.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#business GoogleDialogflowCxGenerativeSettings#business}
        '''
        result = self._values.get("business")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def business_description(self) -> typing.Optional[builtins.str]:
        '''Company description, used for LLM prompt, e.g. "a family company selling freshly roasted coffee beans".''.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#business_description GoogleDialogflowCxGenerativeSettings#business_description}
        '''
        result = self._values.get("business_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_data_store_fallback(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to disable fallback to Data Store search results (in case the LLM couldn't pick a proper answer).

        Per default the feature is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#disable_data_store_fallback GoogleDialogflowCxGenerativeSettings#disable_data_store_fallback}
        '''
        result = self._values.get("disable_data_store_fallback")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxGenerativeSettingsKnowledgeConnectorSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxGenerativeSettingsKnowledgeConnectorSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxGenerativeSettings.GoogleDialogflowCxGenerativeSettingsKnowledgeConnectorSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__39a3df07828b01fbe4f627fc61027cfe6ee456eb9d8d7e4a967c71f6e3a53dc5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAgent")
    def reset_agent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAgent", []))

    @jsii.member(jsii_name="resetAgentIdentity")
    def reset_agent_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAgentIdentity", []))

    @jsii.member(jsii_name="resetAgentScope")
    def reset_agent_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAgentScope", []))

    @jsii.member(jsii_name="resetBusiness")
    def reset_business(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBusiness", []))

    @jsii.member(jsii_name="resetBusinessDescription")
    def reset_business_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBusinessDescription", []))

    @jsii.member(jsii_name="resetDisableDataStoreFallback")
    def reset_disable_data_store_fallback(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableDataStoreFallback", []))

    @builtins.property
    @jsii.member(jsii_name="agentIdentityInput")
    def agent_identity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agentIdentityInput"))

    @builtins.property
    @jsii.member(jsii_name="agentInput")
    def agent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agentInput"))

    @builtins.property
    @jsii.member(jsii_name="agentScopeInput")
    def agent_scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agentScopeInput"))

    @builtins.property
    @jsii.member(jsii_name="businessDescriptionInput")
    def business_description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "businessDescriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="businessInput")
    def business_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "businessInput"))

    @builtins.property
    @jsii.member(jsii_name="disableDataStoreFallbackInput")
    def disable_data_store_fallback_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableDataStoreFallbackInput"))

    @builtins.property
    @jsii.member(jsii_name="agent")
    def agent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agent"))

    @agent.setter
    def agent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf53be4756e2fde6ac29e3c515680a09135bf012aa1964af261be8c6b867c193)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="agentIdentity")
    def agent_identity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agentIdentity"))

    @agent_identity.setter
    def agent_identity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c4093979ea519bc2c08944bbb94b0639fded427b4e9fbdf187eccb27b7bf99d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agentIdentity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="agentScope")
    def agent_scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agentScope"))

    @agent_scope.setter
    def agent_scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc1a47cddd27dbc40ca22b0fe804c4ca5d40450633d4d6e59040100bf9361ae0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agentScope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="business")
    def business(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "business"))

    @business.setter
    def business(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__428487c771eac59437a8ed17982919680b71ae7ce95e42cb62602397a5f8d9bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "business", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="businessDescription")
    def business_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "businessDescription"))

    @business_description.setter
    def business_description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d4052cf3d4e29845e0b2b610ca429d2d9bbb2b45a28ef210a3bf3c3888eea7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "businessDescription", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableDataStoreFallback")
    def disable_data_store_fallback(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableDataStoreFallback"))

    @disable_data_store_fallback.setter
    def disable_data_store_fallback(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60b24e941a0361674a1838e6906ec1fcf76776e1cb9d4d4a653807eaf61cd05a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableDataStoreFallback", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxGenerativeSettingsKnowledgeConnectorSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowCxGenerativeSettingsKnowledgeConnectorSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxGenerativeSettingsKnowledgeConnectorSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a01cee9a3b0e3925ae9d1307e98b0025a2410409e8f75600002039112aafd05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxGenerativeSettings.GoogleDialogflowCxGenerativeSettingsLlmModelSettings",
    jsii_struct_bases=[],
    name_mapping={"model": "model", "prompt_text": "promptText"},
)
class GoogleDialogflowCxGenerativeSettingsLlmModelSettings:
    def __init__(
        self,
        *,
        model: typing.Optional[builtins.str] = None,
        prompt_text: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param model: The selected LLM model. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#model GoogleDialogflowCxGenerativeSettings#model}
        :param prompt_text: The custom prompt to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#prompt_text GoogleDialogflowCxGenerativeSettings#prompt_text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e33ccdd77f73e09c7e5fb5f20620ccafb9ab9f04298c07330b55b07e2a84913)
            check_type(argname="argument model", value=model, expected_type=type_hints["model"])
            check_type(argname="argument prompt_text", value=prompt_text, expected_type=type_hints["prompt_text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if model is not None:
            self._values["model"] = model
        if prompt_text is not None:
            self._values["prompt_text"] = prompt_text

    @builtins.property
    def model(self) -> typing.Optional[builtins.str]:
        '''The selected LLM model.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#model GoogleDialogflowCxGenerativeSettings#model}
        '''
        result = self._values.get("model")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prompt_text(self) -> typing.Optional[builtins.str]:
        '''The custom prompt to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#prompt_text GoogleDialogflowCxGenerativeSettings#prompt_text}
        '''
        result = self._values.get("prompt_text")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxGenerativeSettingsLlmModelSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxGenerativeSettingsLlmModelSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxGenerativeSettings.GoogleDialogflowCxGenerativeSettingsLlmModelSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b76b91035b3aba4666b046d33c0e0a607231ea489e5ac7e9c923dc587ac5e621)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetModel")
    def reset_model(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModel", []))

    @jsii.member(jsii_name="resetPromptText")
    def reset_prompt_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPromptText", []))

    @builtins.property
    @jsii.member(jsii_name="modelInput")
    def model_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modelInput"))

    @builtins.property
    @jsii.member(jsii_name="promptTextInput")
    def prompt_text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "promptTextInput"))

    @builtins.property
    @jsii.member(jsii_name="model")
    def model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "model"))

    @model.setter
    def model(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e34a95bd5cc78b6a5a8028dd897d1237bb85dd3f15563fefdbc65706fcf5ce7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "model", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="promptText")
    def prompt_text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "promptText"))

    @prompt_text.setter
    def prompt_text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f6f839168fe0cda8a2f78b5c893bc0dd267997bf7c7f2f0e243fabb427c00fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "promptText", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxGenerativeSettingsLlmModelSettings]:
        return typing.cast(typing.Optional[GoogleDialogflowCxGenerativeSettingsLlmModelSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxGenerativeSettingsLlmModelSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__274544be8792946d9c30c19879123cd5813f45dafa88f7963cc8ef64c4626263)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxGenerativeSettings.GoogleDialogflowCxGenerativeSettingsTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleDialogflowCxGenerativeSettingsTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#create GoogleDialogflowCxGenerativeSettings#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#delete GoogleDialogflowCxGenerativeSettings#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#update GoogleDialogflowCxGenerativeSettings#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__123ef6f62ed3bbdcd7557c39277154972452d98e43dcd95ddd9b1824ecd968f4)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#create GoogleDialogflowCxGenerativeSettings#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#delete GoogleDialogflowCxGenerativeSettings#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_generative_settings#update GoogleDialogflowCxGenerativeSettings#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxGenerativeSettingsTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxGenerativeSettingsTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxGenerativeSettings.GoogleDialogflowCxGenerativeSettingsTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__843b55ee9670cb52fec029985624d8dc8b34e51bb45e45c93a01c3cd7546dda2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__27cef5cdc993d440a6bba4ccbec97427b8440cb99c3969375fbe1b3711d45b76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24ae2db731420127bacdfe95e86820e649c0c59200f8751e32bccf282b0f35d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__012a6bb047e4a9379b90f7475c653e0e41493101555910c7b5d27d866ffee893)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxGenerativeSettingsTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxGenerativeSettingsTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxGenerativeSettingsTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__420a3b40bce1d5c2ab8ac136dd6ee4bfec20a7ea96f294dc7be0a2dde08b38f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleDialogflowCxGenerativeSettings",
    "GoogleDialogflowCxGenerativeSettingsConfig",
    "GoogleDialogflowCxGenerativeSettingsFallbackSettings",
    "GoogleDialogflowCxGenerativeSettingsFallbackSettingsOutputReference",
    "GoogleDialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates",
    "GoogleDialogflowCxGenerativeSettingsFallbackSettingsPromptTemplatesList",
    "GoogleDialogflowCxGenerativeSettingsFallbackSettingsPromptTemplatesOutputReference",
    "GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettings",
    "GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases",
    "GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrasesList",
    "GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrasesOutputReference",
    "GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettingsOutputReference",
    "GoogleDialogflowCxGenerativeSettingsKnowledgeConnectorSettings",
    "GoogleDialogflowCxGenerativeSettingsKnowledgeConnectorSettingsOutputReference",
    "GoogleDialogflowCxGenerativeSettingsLlmModelSettings",
    "GoogleDialogflowCxGenerativeSettingsLlmModelSettingsOutputReference",
    "GoogleDialogflowCxGenerativeSettingsTimeouts",
    "GoogleDialogflowCxGenerativeSettingsTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__cad6c470f2e90c88e698e666607bde7960d5b0258ff977e4088895f939a31166(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    language_code: builtins.str,
    fallback_settings: typing.Optional[typing.Union[GoogleDialogflowCxGenerativeSettingsFallbackSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    generative_safety_settings: typing.Optional[typing.Union[GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettings, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    knowledge_connector_settings: typing.Optional[typing.Union[GoogleDialogflowCxGenerativeSettingsKnowledgeConnectorSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    llm_model_settings: typing.Optional[typing.Union[GoogleDialogflowCxGenerativeSettingsLlmModelSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    parent: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDialogflowCxGenerativeSettingsTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__65f305373b74d2125b8ec2d4a0b383f7f53fe3b2f22d045771cd3a948f736892(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1183393965f146b9a76603e6b157c35ed251ef0fd81ad57806fc5a11c3b189c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85ddc4e974092c5a54583f62adf08294a6ac5c92d45914179484b7227bb05e0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25438e77f7e4ad8c1bd4d6562785a083650f9a3a5c5d139931d36ff2acde8cdb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b86c7283eb3849fb2ff8e261e136ef7acb188386c8db81e4c2ebca714d25fee0(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    language_code: builtins.str,
    fallback_settings: typing.Optional[typing.Union[GoogleDialogflowCxGenerativeSettingsFallbackSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    generative_safety_settings: typing.Optional[typing.Union[GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettings, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    knowledge_connector_settings: typing.Optional[typing.Union[GoogleDialogflowCxGenerativeSettingsKnowledgeConnectorSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    llm_model_settings: typing.Optional[typing.Union[GoogleDialogflowCxGenerativeSettingsLlmModelSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    parent: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDialogflowCxGenerativeSettingsTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebb91d8d9a7af1fc2eb8b7cbf8392d119f3487487fff3154b6e20c5f02d15bb7(
    *,
    prompt_templates: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates, typing.Dict[builtins.str, typing.Any]]]]] = None,
    selected_prompt: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f4dc3ef95fede0a3a63bc0ccc787547a2df08151b7f146a92b6024ad9dbc2ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a2c27c20a0db20927e5f9c203a9512937373e2893b418405c5aa2c8392ba95d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f36414f53df1616179ad98aae625bd4eb6b114eedcd08f11bc6bc37e98f909cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7258ed9bdcf620fd524f55f81e05b8baddecb483c4f8c2c4147928978bd630cb(
    value: typing.Optional[GoogleDialogflowCxGenerativeSettingsFallbackSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff3a653f809e257093e4f6ffea3b0c0de56dec485e583bd0fe4faa0a05512b0b(
    *,
    display_name: typing.Optional[builtins.str] = None,
    frozen: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prompt_text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a668a7c4ec9f16ce23b1be3bef522319d55143473590d10f493990fb6aac663f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f137bc189ef0117a4463e924a8ef23b022121482da16f5703a3f3ce19af90ed(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8b51d11130f1daabdc3945ce58dcfc109dcc8b7f0fa86a111d0cea04217154d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b177591b60e76b6d5ec8f3da1234346e5500986891b5b61cf3176bf962ec20e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc5b42b387012f51b35986290562d178b80ba1298ef979a39bf51e06e873bf5c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56fe32fc2e92950e01a36930e32012c4c2ff56147bf2b508f53acc9f90437299(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0d55c575d84a33003262611d89c3c821041155a658e179cd07141054f7c56e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17e30a4ca1cd35c4c08189afca59a3982461e6a707b03124d706e08b9490b189(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e710b76c4f50beece475d8b0627a2e8a85b488fe9ad87a437941d311b10af95a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4810d3408006cbaae17ee3d4abf9f0d2cbdeb8e292e2fa949febe7f887772ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eca0503e1bf6e9063ce4febc86fc6e45e6c953dbdb3b2d8db6c98ced5259542(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ebd352961140bc4b5fa9ff9850ed50746d8a1ab8ef25c6418270ac824900ca9(
    *,
    banned_phrases: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_banned_phrase_match_strategy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__423317be8ff6df7f63f00f6afafe1bbfc99d73cd40d4a49572cb0efc69a3b93c(
    *,
    language_code: builtins.str,
    text: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05b226c46c300b1f3ac7884e759e025e65b3625f48ad9b80eac226ad087a9f9c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00f1eb520a0642b438a1c699344ad44af93fcfc5902b50371f40911ec1e7bd8f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__137e7b41a0d2a4df0923cb6d707e9788e387d6e53fb27172953a616bda74b23b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aee03e9ea300ab0acd6bd02a8d7fa6831b0178fd199f4b9464473d4e2255a5cb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e97faeeeaa923b2297524ab8af0da68a230024bf0f52f9cd71566db9c29f8fb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af3e682aec293bff1ec89f92d6a96d7c936dde082624d6c2bdefe7ff9def462e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fadf512ea9970fab9f9c449069a55e0c9161437c3c3cb08168a90d55fb2125d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96f089788d1e7fffe0104b527704148cfa2f079b9ddfb08eef85a6866ac4c64c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ca9320e74e0ad69f4126bde730b18107ad0ab05214111317e53254a09c69d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4aa62a608255b3762a24459e660e55e5bbbee7b5e6e6f5175ec6bf82eedf8b7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__719b5de998e81763bada70c04b8ea3b72a6bec9aa5ff4a2d8135c66e05bc23ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c7e0bfca3a96bcbda5e2e701351e189918f975f40887ec16eda573974948695(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b723cc490449dfff1995f05dbaab38aa53ec3751f755e2efe191bc67c6bc6da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__041a5d46527e7b601977a360c7af805bbc514cb3891e697aa201528158c81b8e(
    value: typing.Optional[GoogleDialogflowCxGenerativeSettingsGenerativeSafetySettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__008ae4a1cd9688a3ba47d75019f6c9ed6228a2632757b478421b76a25ea43ffb(
    *,
    agent: typing.Optional[builtins.str] = None,
    agent_identity: typing.Optional[builtins.str] = None,
    agent_scope: typing.Optional[builtins.str] = None,
    business: typing.Optional[builtins.str] = None,
    business_description: typing.Optional[builtins.str] = None,
    disable_data_store_fallback: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39a3df07828b01fbe4f627fc61027cfe6ee456eb9d8d7e4a967c71f6e3a53dc5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf53be4756e2fde6ac29e3c515680a09135bf012aa1964af261be8c6b867c193(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c4093979ea519bc2c08944bbb94b0639fded427b4e9fbdf187eccb27b7bf99d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc1a47cddd27dbc40ca22b0fe804c4ca5d40450633d4d6e59040100bf9361ae0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__428487c771eac59437a8ed17982919680b71ae7ce95e42cb62602397a5f8d9bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d4052cf3d4e29845e0b2b610ca429d2d9bbb2b45a28ef210a3bf3c3888eea7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60b24e941a0361674a1838e6906ec1fcf76776e1cb9d4d4a653807eaf61cd05a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a01cee9a3b0e3925ae9d1307e98b0025a2410409e8f75600002039112aafd05(
    value: typing.Optional[GoogleDialogflowCxGenerativeSettingsKnowledgeConnectorSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e33ccdd77f73e09c7e5fb5f20620ccafb9ab9f04298c07330b55b07e2a84913(
    *,
    model: typing.Optional[builtins.str] = None,
    prompt_text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b76b91035b3aba4666b046d33c0e0a607231ea489e5ac7e9c923dc587ac5e621(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e34a95bd5cc78b6a5a8028dd897d1237bb85dd3f15563fefdbc65706fcf5ce7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f6f839168fe0cda8a2f78b5c893bc0dd267997bf7c7f2f0e243fabb427c00fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__274544be8792946d9c30c19879123cd5813f45dafa88f7963cc8ef64c4626263(
    value: typing.Optional[GoogleDialogflowCxGenerativeSettingsLlmModelSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__123ef6f62ed3bbdcd7557c39277154972452d98e43dcd95ddd9b1824ecd968f4(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__843b55ee9670cb52fec029985624d8dc8b34e51bb45e45c93a01c3cd7546dda2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27cef5cdc993d440a6bba4ccbec97427b8440cb99c3969375fbe1b3711d45b76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24ae2db731420127bacdfe95e86820e649c0c59200f8751e32bccf282b0f35d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__012a6bb047e4a9379b90f7475c653e0e41493101555910c7b5d27d866ffee893(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__420a3b40bce1d5c2ab8ac136dd6ee4bfec20a7ea96f294dc7be0a2dde08b38f6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxGenerativeSettingsTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
