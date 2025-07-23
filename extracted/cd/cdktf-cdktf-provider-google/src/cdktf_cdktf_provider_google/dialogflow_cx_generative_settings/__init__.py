r'''
# `google_dialogflow_cx_generative_settings`

Refer to the Terraform Registry for docs: [`google_dialogflow_cx_generative_settings`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings).
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


class DialogflowCxGenerativeSettings(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxGenerativeSettings.DialogflowCxGenerativeSettings",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings google_dialogflow_cx_generative_settings}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        language_code: builtins.str,
        fallback_settings: typing.Optional[typing.Union["DialogflowCxGenerativeSettingsFallbackSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        generative_safety_settings: typing.Optional[typing.Union["DialogflowCxGenerativeSettingsGenerativeSafetySettings", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        knowledge_connector_settings: typing.Optional[typing.Union["DialogflowCxGenerativeSettingsKnowledgeConnectorSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        llm_model_settings: typing.Optional[typing.Union["DialogflowCxGenerativeSettingsLlmModelSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        parent: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DialogflowCxGenerativeSettingsTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings google_dialogflow_cx_generative_settings} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param language_code: Language for this settings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#language_code DialogflowCxGenerativeSettings#language_code}
        :param fallback_settings: fallback_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#fallback_settings DialogflowCxGenerativeSettings#fallback_settings}
        :param generative_safety_settings: generative_safety_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#generative_safety_settings DialogflowCxGenerativeSettings#generative_safety_settings}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#id DialogflowCxGenerativeSettings#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param knowledge_connector_settings: knowledge_connector_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#knowledge_connector_settings DialogflowCxGenerativeSettings#knowledge_connector_settings}
        :param llm_model_settings: llm_model_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#llm_model_settings DialogflowCxGenerativeSettings#llm_model_settings}
        :param parent: The agent to create a flow for. Format: projects//locations//agents/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#parent DialogflowCxGenerativeSettings#parent}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#timeouts DialogflowCxGenerativeSettings#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f9e13a0eba5c6c58ab03ba3bffabaa1503eeca8a535347c65bef5b1cddb3b30)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DialogflowCxGenerativeSettingsConfig(
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
        '''Generates CDKTF code for importing a DialogflowCxGenerativeSettings resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DialogflowCxGenerativeSettings to import.
        :param import_from_id: The id of the existing DialogflowCxGenerativeSettings that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DialogflowCxGenerativeSettings to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__498fc38d8ccee4e0281493b841db1f592c35328dba78bdc04347c8bd270c3a53)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putFallbackSettings")
    def put_fallback_settings(
        self,
        *,
        prompt_templates: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates", typing.Dict[builtins.str, typing.Any]]]]] = None,
        selected_prompt: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param prompt_templates: prompt_templates block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#prompt_templates DialogflowCxGenerativeSettings#prompt_templates}
        :param selected_prompt: Display name of the selected prompt. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#selected_prompt DialogflowCxGenerativeSettings#selected_prompt}
        '''
        value = DialogflowCxGenerativeSettingsFallbackSettings(
            prompt_templates=prompt_templates, selected_prompt=selected_prompt
        )

        return typing.cast(None, jsii.invoke(self, "putFallbackSettings", [value]))

    @jsii.member(jsii_name="putGenerativeSafetySettings")
    def put_generative_safety_settings(
        self,
        *,
        banned_phrases: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_banned_phrase_match_strategy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param banned_phrases: banned_phrases block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#banned_phrases DialogflowCxGenerativeSettings#banned_phrases}
        :param default_banned_phrase_match_strategy: Optional. Default phrase match strategy for banned phrases. See `PhraseMatchStrategy <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/GenerativeSettings#phrasematchstrategy>`_ for valid values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#default_banned_phrase_match_strategy DialogflowCxGenerativeSettings#default_banned_phrase_match_strategy}
        '''
        value = DialogflowCxGenerativeSettingsGenerativeSafetySettings(
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
        :param agent: Name of the virtual agent. Used for LLM prompt. Can be left empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#agent DialogflowCxGenerativeSettings#agent}
        :param agent_identity: Identity of the agent, e.g. "virtual agent", "AI assistant". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#agent_identity DialogflowCxGenerativeSettings#agent_identity}
        :param agent_scope: Agent scope, e.g. "Example company website", "internal Example company website for employees", "manual of car owner". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#agent_scope DialogflowCxGenerativeSettings#agent_scope}
        :param business: Name of the company, organization or other entity that the agent represents. Used for knowledge connector LLM prompt and for knowledge search. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#business DialogflowCxGenerativeSettings#business}
        :param business_description: Company description, used for LLM prompt, e.g. "a family company selling freshly roasted coffee beans".''. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#business_description DialogflowCxGenerativeSettings#business_description}
        :param disable_data_store_fallback: Whether to disable fallback to Data Store search results (in case the LLM couldn't pick a proper answer). Per default the feature is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#disable_data_store_fallback DialogflowCxGenerativeSettings#disable_data_store_fallback}
        '''
        value = DialogflowCxGenerativeSettingsKnowledgeConnectorSettings(
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
        :param model: The selected LLM model. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#model DialogflowCxGenerativeSettings#model}
        :param prompt_text: The custom prompt to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#prompt_text DialogflowCxGenerativeSettings#prompt_text}
        '''
        value = DialogflowCxGenerativeSettingsLlmModelSettings(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#create DialogflowCxGenerativeSettings#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#delete DialogflowCxGenerativeSettings#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#update DialogflowCxGenerativeSettings#update}.
        '''
        value = DialogflowCxGenerativeSettingsTimeouts(
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
    ) -> "DialogflowCxGenerativeSettingsFallbackSettingsOutputReference":
        return typing.cast("DialogflowCxGenerativeSettingsFallbackSettingsOutputReference", jsii.get(self, "fallbackSettings"))

    @builtins.property
    @jsii.member(jsii_name="generativeSafetySettings")
    def generative_safety_settings(
        self,
    ) -> "DialogflowCxGenerativeSettingsGenerativeSafetySettingsOutputReference":
        return typing.cast("DialogflowCxGenerativeSettingsGenerativeSafetySettingsOutputReference", jsii.get(self, "generativeSafetySettings"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeConnectorSettings")
    def knowledge_connector_settings(
        self,
    ) -> "DialogflowCxGenerativeSettingsKnowledgeConnectorSettingsOutputReference":
        return typing.cast("DialogflowCxGenerativeSettingsKnowledgeConnectorSettingsOutputReference", jsii.get(self, "knowledgeConnectorSettings"))

    @builtins.property
    @jsii.member(jsii_name="llmModelSettings")
    def llm_model_settings(
        self,
    ) -> "DialogflowCxGenerativeSettingsLlmModelSettingsOutputReference":
        return typing.cast("DialogflowCxGenerativeSettingsLlmModelSettingsOutputReference", jsii.get(self, "llmModelSettings"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DialogflowCxGenerativeSettingsTimeoutsOutputReference":
        return typing.cast("DialogflowCxGenerativeSettingsTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="fallbackSettingsInput")
    def fallback_settings_input(
        self,
    ) -> typing.Optional["DialogflowCxGenerativeSettingsFallbackSettings"]:
        return typing.cast(typing.Optional["DialogflowCxGenerativeSettingsFallbackSettings"], jsii.get(self, "fallbackSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="generativeSafetySettingsInput")
    def generative_safety_settings_input(
        self,
    ) -> typing.Optional["DialogflowCxGenerativeSettingsGenerativeSafetySettings"]:
        return typing.cast(typing.Optional["DialogflowCxGenerativeSettingsGenerativeSafetySettings"], jsii.get(self, "generativeSafetySettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeConnectorSettingsInput")
    def knowledge_connector_settings_input(
        self,
    ) -> typing.Optional["DialogflowCxGenerativeSettingsKnowledgeConnectorSettings"]:
        return typing.cast(typing.Optional["DialogflowCxGenerativeSettingsKnowledgeConnectorSettings"], jsii.get(self, "knowledgeConnectorSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="languageCodeInput")
    def language_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "languageCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="llmModelSettingsInput")
    def llm_model_settings_input(
        self,
    ) -> typing.Optional["DialogflowCxGenerativeSettingsLlmModelSettings"]:
        return typing.cast(typing.Optional["DialogflowCxGenerativeSettingsLlmModelSettings"], jsii.get(self, "llmModelSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="parentInput")
    def parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DialogflowCxGenerativeSettingsTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DialogflowCxGenerativeSettingsTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed61e33dbe415f2ce2cdbd4b98716e4ff3ae25a7452c414d2c3b779ee29dfb26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="languageCode")
    def language_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "languageCode"))

    @language_code.setter
    def language_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e72dae76564ad2c3563cf0d757ef89d802228b826fec300849d2e15278cd332)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "languageCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__110093a41cd98fc02e9722edd8b3d3d2d4fc96569e5c201898b9315fb389c739)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxGenerativeSettings.DialogflowCxGenerativeSettingsConfig",
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
class DialogflowCxGenerativeSettingsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        fallback_settings: typing.Optional[typing.Union["DialogflowCxGenerativeSettingsFallbackSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        generative_safety_settings: typing.Optional[typing.Union["DialogflowCxGenerativeSettingsGenerativeSafetySettings", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        knowledge_connector_settings: typing.Optional[typing.Union["DialogflowCxGenerativeSettingsKnowledgeConnectorSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        llm_model_settings: typing.Optional[typing.Union["DialogflowCxGenerativeSettingsLlmModelSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        parent: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DialogflowCxGenerativeSettingsTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param language_code: Language for this settings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#language_code DialogflowCxGenerativeSettings#language_code}
        :param fallback_settings: fallback_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#fallback_settings DialogflowCxGenerativeSettings#fallback_settings}
        :param generative_safety_settings: generative_safety_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#generative_safety_settings DialogflowCxGenerativeSettings#generative_safety_settings}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#id DialogflowCxGenerativeSettings#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param knowledge_connector_settings: knowledge_connector_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#knowledge_connector_settings DialogflowCxGenerativeSettings#knowledge_connector_settings}
        :param llm_model_settings: llm_model_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#llm_model_settings DialogflowCxGenerativeSettings#llm_model_settings}
        :param parent: The agent to create a flow for. Format: projects//locations//agents/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#parent DialogflowCxGenerativeSettings#parent}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#timeouts DialogflowCxGenerativeSettings#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(fallback_settings, dict):
            fallback_settings = DialogflowCxGenerativeSettingsFallbackSettings(**fallback_settings)
        if isinstance(generative_safety_settings, dict):
            generative_safety_settings = DialogflowCxGenerativeSettingsGenerativeSafetySettings(**generative_safety_settings)
        if isinstance(knowledge_connector_settings, dict):
            knowledge_connector_settings = DialogflowCxGenerativeSettingsKnowledgeConnectorSettings(**knowledge_connector_settings)
        if isinstance(llm_model_settings, dict):
            llm_model_settings = DialogflowCxGenerativeSettingsLlmModelSettings(**llm_model_settings)
        if isinstance(timeouts, dict):
            timeouts = DialogflowCxGenerativeSettingsTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af797bd9ac005f9cb5e0c8b682d0d102e5f9d53abe369add05a1cdd1e91be8b2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#language_code DialogflowCxGenerativeSettings#language_code}
        '''
        result = self._values.get("language_code")
        assert result is not None, "Required property 'language_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fallback_settings(
        self,
    ) -> typing.Optional["DialogflowCxGenerativeSettingsFallbackSettings"]:
        '''fallback_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#fallback_settings DialogflowCxGenerativeSettings#fallback_settings}
        '''
        result = self._values.get("fallback_settings")
        return typing.cast(typing.Optional["DialogflowCxGenerativeSettingsFallbackSettings"], result)

    @builtins.property
    def generative_safety_settings(
        self,
    ) -> typing.Optional["DialogflowCxGenerativeSettingsGenerativeSafetySettings"]:
        '''generative_safety_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#generative_safety_settings DialogflowCxGenerativeSettings#generative_safety_settings}
        '''
        result = self._values.get("generative_safety_settings")
        return typing.cast(typing.Optional["DialogflowCxGenerativeSettingsGenerativeSafetySettings"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#id DialogflowCxGenerativeSettings#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def knowledge_connector_settings(
        self,
    ) -> typing.Optional["DialogflowCxGenerativeSettingsKnowledgeConnectorSettings"]:
        '''knowledge_connector_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#knowledge_connector_settings DialogflowCxGenerativeSettings#knowledge_connector_settings}
        '''
        result = self._values.get("knowledge_connector_settings")
        return typing.cast(typing.Optional["DialogflowCxGenerativeSettingsKnowledgeConnectorSettings"], result)

    @builtins.property
    def llm_model_settings(
        self,
    ) -> typing.Optional["DialogflowCxGenerativeSettingsLlmModelSettings"]:
        '''llm_model_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#llm_model_settings DialogflowCxGenerativeSettings#llm_model_settings}
        '''
        result = self._values.get("llm_model_settings")
        return typing.cast(typing.Optional["DialogflowCxGenerativeSettingsLlmModelSettings"], result)

    @builtins.property
    def parent(self) -> typing.Optional[builtins.str]:
        '''The agent to create a flow for. Format: projects//locations//agents/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#parent DialogflowCxGenerativeSettings#parent}
        '''
        result = self._values.get("parent")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DialogflowCxGenerativeSettingsTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#timeouts DialogflowCxGenerativeSettings#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DialogflowCxGenerativeSettingsTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxGenerativeSettingsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxGenerativeSettings.DialogflowCxGenerativeSettingsFallbackSettings",
    jsii_struct_bases=[],
    name_mapping={
        "prompt_templates": "promptTemplates",
        "selected_prompt": "selectedPrompt",
    },
)
class DialogflowCxGenerativeSettingsFallbackSettings:
    def __init__(
        self,
        *,
        prompt_templates: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates", typing.Dict[builtins.str, typing.Any]]]]] = None,
        selected_prompt: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param prompt_templates: prompt_templates block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#prompt_templates DialogflowCxGenerativeSettings#prompt_templates}
        :param selected_prompt: Display name of the selected prompt. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#selected_prompt DialogflowCxGenerativeSettings#selected_prompt}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2033f4d4bae1361748107906fa4c87a0a77666ff961a47e4961fc55daf443e73)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates"]]]:
        '''prompt_templates block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#prompt_templates DialogflowCxGenerativeSettings#prompt_templates}
        '''
        result = self._values.get("prompt_templates")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates"]]], result)

    @builtins.property
    def selected_prompt(self) -> typing.Optional[builtins.str]:
        '''Display name of the selected prompt.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#selected_prompt DialogflowCxGenerativeSettings#selected_prompt}
        '''
        result = self._values.get("selected_prompt")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxGenerativeSettingsFallbackSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxGenerativeSettingsFallbackSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxGenerativeSettings.DialogflowCxGenerativeSettingsFallbackSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6cefbb0ac84d00bea0f90867e816e88b60cd5e8d6495191d0388042bdb41fd8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPromptTemplates")
    def put_prompt_templates(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9f7c1a246051d5d9e3c23bdbbbffd56163fdb3a2d7e3920d34ca961bba066c9)
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
    ) -> "DialogflowCxGenerativeSettingsFallbackSettingsPromptTemplatesList":
        return typing.cast("DialogflowCxGenerativeSettingsFallbackSettingsPromptTemplatesList", jsii.get(self, "promptTemplates"))

    @builtins.property
    @jsii.member(jsii_name="promptTemplatesInput")
    def prompt_templates_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates"]]], jsii.get(self, "promptTemplatesInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__3897135f1506fc39cdfbebcfd38161ca91d5bffb3c80c9360e3823b971227732)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "selectedPrompt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxGenerativeSettingsFallbackSettings]:
        return typing.cast(typing.Optional[DialogflowCxGenerativeSettingsFallbackSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxGenerativeSettingsFallbackSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af00d30c4153292d50cc93283599e23ec3cfc1773335959cd5b6e8a9643bc1a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxGenerativeSettings.DialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates",
    jsii_struct_bases=[],
    name_mapping={
        "display_name": "displayName",
        "frozen": "frozen",
        "prompt_text": "promptText",
    },
)
class DialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates:
    def __init__(
        self,
        *,
        display_name: typing.Optional[builtins.str] = None,
        frozen: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prompt_text: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param display_name: Prompt name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#display_name DialogflowCxGenerativeSettings#display_name}
        :param frozen: If the flag is true, the prompt is frozen and cannot be modified by users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#frozen DialogflowCxGenerativeSettings#frozen}
        :param prompt_text: Prompt text that is sent to a LLM on no-match default, placeholders are filled downstream. For example: "Here is a conversation $conversation, a response is: " Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#prompt_text DialogflowCxGenerativeSettings#prompt_text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76e576b38c0dbf7cd1bde2ab603173287168b8a7cced02bb7cd7697b1a05e8ed)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#display_name DialogflowCxGenerativeSettings#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def frozen(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the flag is true, the prompt is frozen and cannot be modified by users.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#frozen DialogflowCxGenerativeSettings#frozen}
        '''
        result = self._values.get("frozen")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prompt_text(self) -> typing.Optional[builtins.str]:
        '''Prompt text that is sent to a LLM on no-match default, placeholders are filled downstream.

        For example: "Here is a conversation $conversation, a response is: "

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#prompt_text DialogflowCxGenerativeSettings#prompt_text}
        '''
        result = self._values.get("prompt_text")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxGenerativeSettingsFallbackSettingsPromptTemplatesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxGenerativeSettings.DialogflowCxGenerativeSettingsFallbackSettingsPromptTemplatesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9e2889b80ce764c508f3423e12aacb32a36e1cb6dfb84d25e7123f2ac55cca5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DialogflowCxGenerativeSettingsFallbackSettingsPromptTemplatesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a65fe4f1322b7022606d3695ad54b7245d2d9bd297c1d962515e6205440d6fe9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DialogflowCxGenerativeSettingsFallbackSettingsPromptTemplatesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e877f375242aac7d50bbb0af207e9a1f62b775b2343f2a8462fa6f0536140d3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d925e15add917b6570ea63dd83e6069423e67480ab52350fd05727b16ac8ead)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c45979ea224c082706905600811fd718984d3e138309177b63c4594c3660f097)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7afbd9efc0be046c43d73448be22ad2e2291dfee76da7a8c4dc7cafb3b9fb2e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxGenerativeSettingsFallbackSettingsPromptTemplatesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxGenerativeSettings.DialogflowCxGenerativeSettingsFallbackSettingsPromptTemplatesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2a0040d8b7c6619f4010964982299a06b30b2879e44a09bf9a6df8e27331b8b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed828726adc9119ef4ae0f77b96579e493f3b2b8b1ce29e8cb1e9b69893ffdc0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf8cb3d3cf7f943083e6d66361815365a095e3536f69932256fb0684a5f98b29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frozen", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="promptText")
    def prompt_text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "promptText"))

    @prompt_text.setter
    def prompt_text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4157c87fb1c9576e93c35a57d6da352bc85c81e4e801a6131450ed991de52663)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "promptText", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0236e2047d3b96fccfcc2f1543ff1c5c88aac06dfc54424d863817a2ad3e6833)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxGenerativeSettings.DialogflowCxGenerativeSettingsGenerativeSafetySettings",
    jsii_struct_bases=[],
    name_mapping={
        "banned_phrases": "bannedPhrases",
        "default_banned_phrase_match_strategy": "defaultBannedPhraseMatchStrategy",
    },
)
class DialogflowCxGenerativeSettingsGenerativeSafetySettings:
    def __init__(
        self,
        *,
        banned_phrases: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_banned_phrase_match_strategy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param banned_phrases: banned_phrases block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#banned_phrases DialogflowCxGenerativeSettings#banned_phrases}
        :param default_banned_phrase_match_strategy: Optional. Default phrase match strategy for banned phrases. See `PhraseMatchStrategy <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/GenerativeSettings#phrasematchstrategy>`_ for valid values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#default_banned_phrase_match_strategy DialogflowCxGenerativeSettings#default_banned_phrase_match_strategy}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aafa25e7a87cfdab684399b326d3bde07184ea94ecf2b9fe1b43c96bb85f61e)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases"]]]:
        '''banned_phrases block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#banned_phrases DialogflowCxGenerativeSettings#banned_phrases}
        '''
        result = self._values.get("banned_phrases")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases"]]], result)

    @builtins.property
    def default_banned_phrase_match_strategy(self) -> typing.Optional[builtins.str]:
        '''Optional. Default phrase match strategy for banned phrases. See `PhraseMatchStrategy <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/GenerativeSettings#phrasematchstrategy>`_ for valid values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#default_banned_phrase_match_strategy DialogflowCxGenerativeSettings#default_banned_phrase_match_strategy}
        '''
        result = self._values.get("default_banned_phrase_match_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxGenerativeSettingsGenerativeSafetySettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxGenerativeSettings.DialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases",
    jsii_struct_bases=[],
    name_mapping={"language_code": "languageCode", "text": "text"},
)
class DialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases:
    def __init__(self, *, language_code: builtins.str, text: builtins.str) -> None:
        '''
        :param language_code: Language code of the phrase. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#language_code DialogflowCxGenerativeSettings#language_code}
        :param text: Text input which can be used for prompt or banned phrases. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#text DialogflowCxGenerativeSettings#text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__799b93b78e93eccee09f188d345bc6697b5b3354d2900129fab4ad115d2bc0ae)
            check_type(argname="argument language_code", value=language_code, expected_type=type_hints["language_code"])
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "language_code": language_code,
            "text": text,
        }

    @builtins.property
    def language_code(self) -> builtins.str:
        '''Language code of the phrase.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#language_code DialogflowCxGenerativeSettings#language_code}
        '''
        result = self._values.get("language_code")
        assert result is not None, "Required property 'language_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def text(self) -> builtins.str:
        '''Text input which can be used for prompt or banned phrases.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#text DialogflowCxGenerativeSettings#text}
        '''
        result = self._values.get("text")
        assert result is not None, "Required property 'text' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrasesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxGenerativeSettings.DialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrasesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8a5e7f46202f8da0de71b532f524c9a09108de88b69b793cb1dd0ac141b018a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrasesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e47a3def89abb602d81e2465df71db5ce220f19fc9fd256164f19269b81d782)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrasesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa36f4586a222c5b7394bc4b10765d73de67c236daf068df0c08ed2d6216bcdc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__497ac92a3b4acf2d0c3574ba5c671b5195bf9c79b65fdbcc418d55e34d34ff8c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__299b53b6cb9085026e18199fb7a9c02037d01d376f881f00f83e84898d715be9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__828bc472c3ef4240066e672dc9b6249ee85bd56faa613c95a0c8a0b5e865ccde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrasesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxGenerativeSettings.DialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrasesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d44298f6d9d3709a0a9547220370f13c446438ddb97f6ff6982ec9d653dff625)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b695d3ce9b122cc7a366cfee6ef08b902e429fa5f7c867765a1ed1bae4e5fcc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "languageCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "text"))

    @text.setter
    def text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c5ba77cce9e00a9c50b682eb41f509da3d926d79ce9549681bb873a95318759)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "text", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5706daa3ec85fe3eeda768bf81ac3ae86f83dd1fbd947ea1297718e67f63de3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxGenerativeSettingsGenerativeSafetySettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxGenerativeSettings.DialogflowCxGenerativeSettingsGenerativeSafetySettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__389aa372d24429af330e9dd7c3c189e6cf4281932bb546cbacdfc2d6478dff18)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBannedPhrases")
    def put_banned_phrases(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff4acedcea066a3d0b287457365312e2c5d2c85d1f995104e0313417bcb5d0ae)
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
    ) -> DialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrasesList:
        return typing.cast(DialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrasesList, jsii.get(self, "bannedPhrases"))

    @builtins.property
    @jsii.member(jsii_name="bannedPhrasesInput")
    def banned_phrases_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases]]], jsii.get(self, "bannedPhrasesInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__a04acace05a22e2bdcdd47d1494ff865ceb111bb9e118ebc3bdb1f665dafde82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultBannedPhraseMatchStrategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxGenerativeSettingsGenerativeSafetySettings]:
        return typing.cast(typing.Optional[DialogflowCxGenerativeSettingsGenerativeSafetySettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxGenerativeSettingsGenerativeSafetySettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9fd5ef6e90f651b0a98b83539d3856683a6a66ea70a403cb2b6f5a22b181bd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxGenerativeSettings.DialogflowCxGenerativeSettingsKnowledgeConnectorSettings",
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
class DialogflowCxGenerativeSettingsKnowledgeConnectorSettings:
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
        :param agent: Name of the virtual agent. Used for LLM prompt. Can be left empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#agent DialogflowCxGenerativeSettings#agent}
        :param agent_identity: Identity of the agent, e.g. "virtual agent", "AI assistant". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#agent_identity DialogflowCxGenerativeSettings#agent_identity}
        :param agent_scope: Agent scope, e.g. "Example company website", "internal Example company website for employees", "manual of car owner". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#agent_scope DialogflowCxGenerativeSettings#agent_scope}
        :param business: Name of the company, organization or other entity that the agent represents. Used for knowledge connector LLM prompt and for knowledge search. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#business DialogflowCxGenerativeSettings#business}
        :param business_description: Company description, used for LLM prompt, e.g. "a family company selling freshly roasted coffee beans".''. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#business_description DialogflowCxGenerativeSettings#business_description}
        :param disable_data_store_fallback: Whether to disable fallback to Data Store search results (in case the LLM couldn't pick a proper answer). Per default the feature is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#disable_data_store_fallback DialogflowCxGenerativeSettings#disable_data_store_fallback}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0f22e5ab24673e30b1b1db9a6a71e3d4354b92c71627385e3562552381a1385)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#agent DialogflowCxGenerativeSettings#agent}
        '''
        result = self._values.get("agent")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def agent_identity(self) -> typing.Optional[builtins.str]:
        '''Identity of the agent, e.g. "virtual agent", "AI assistant".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#agent_identity DialogflowCxGenerativeSettings#agent_identity}
        '''
        result = self._values.get("agent_identity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def agent_scope(self) -> typing.Optional[builtins.str]:
        '''Agent scope, e.g. "Example company website", "internal Example company website for employees", "manual of car owner".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#agent_scope DialogflowCxGenerativeSettings#agent_scope}
        '''
        result = self._values.get("agent_scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def business(self) -> typing.Optional[builtins.str]:
        '''Name of the company, organization or other entity that the agent represents.

        Used for knowledge connector LLM prompt and for knowledge search.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#business DialogflowCxGenerativeSettings#business}
        '''
        result = self._values.get("business")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def business_description(self) -> typing.Optional[builtins.str]:
        '''Company description, used for LLM prompt, e.g. "a family company selling freshly roasted coffee beans".''.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#business_description DialogflowCxGenerativeSettings#business_description}
        '''
        result = self._values.get("business_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_data_store_fallback(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to disable fallback to Data Store search results (in case the LLM couldn't pick a proper answer).

        Per default the feature is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#disable_data_store_fallback DialogflowCxGenerativeSettings#disable_data_store_fallback}
        '''
        result = self._values.get("disable_data_store_fallback")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxGenerativeSettingsKnowledgeConnectorSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxGenerativeSettingsKnowledgeConnectorSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxGenerativeSettings.DialogflowCxGenerativeSettingsKnowledgeConnectorSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b29de2cb9630efedfb60d8589b4fe8b99ff3b36afad82314b219ed30268c011)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d02f556de3eb2590236932562c99f042336d247b61cda103373d8507abf6fe37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="agentIdentity")
    def agent_identity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agentIdentity"))

    @agent_identity.setter
    def agent_identity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c1560b04dc051a39614718d3182e6c8c67e7fb8850e65ee35d857b1e982cd72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agentIdentity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="agentScope")
    def agent_scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agentScope"))

    @agent_scope.setter
    def agent_scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4f579cf465d9aa95eeb7ab4db99786bc3e10802dc81815b88e2a215ee7e264f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agentScope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="business")
    def business(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "business"))

    @business.setter
    def business(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef7f6471c32d5320bd304037df99f64567a986ac01bc188cbfc2520bfde60962)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "business", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="businessDescription")
    def business_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "businessDescription"))

    @business_description.setter
    def business_description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f868853af833b0600ac386ffffd9aeb16564320adcc0365aa3960711eca77e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7303ff59ef7a9d06c5303acc5c40ba31ccd9c884ad4fefd97abe61011ddba846)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableDataStoreFallback", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxGenerativeSettingsKnowledgeConnectorSettings]:
        return typing.cast(typing.Optional[DialogflowCxGenerativeSettingsKnowledgeConnectorSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxGenerativeSettingsKnowledgeConnectorSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b91edb0e448bc75327f1b262b5a6f90c59967c4fbeba4f04bb1a8efd813aea5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxGenerativeSettings.DialogflowCxGenerativeSettingsLlmModelSettings",
    jsii_struct_bases=[],
    name_mapping={"model": "model", "prompt_text": "promptText"},
)
class DialogflowCxGenerativeSettingsLlmModelSettings:
    def __init__(
        self,
        *,
        model: typing.Optional[builtins.str] = None,
        prompt_text: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param model: The selected LLM model. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#model DialogflowCxGenerativeSettings#model}
        :param prompt_text: The custom prompt to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#prompt_text DialogflowCxGenerativeSettings#prompt_text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__607eb357a726144355be3840a6bc58530b57f053d5d2418e0a2e47d7f7c2ef2f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#model DialogflowCxGenerativeSettings#model}
        '''
        result = self._values.get("model")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prompt_text(self) -> typing.Optional[builtins.str]:
        '''The custom prompt to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#prompt_text DialogflowCxGenerativeSettings#prompt_text}
        '''
        result = self._values.get("prompt_text")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxGenerativeSettingsLlmModelSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxGenerativeSettingsLlmModelSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxGenerativeSettings.DialogflowCxGenerativeSettingsLlmModelSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8ca4ce879420b8c95180757eff4ab5022285727fe0dc6ba0e4ef77ddd1db241)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31670bf9675b6def63e94588682460b4d36596a4292ae1a5ab284118ec015ca3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "model", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="promptText")
    def prompt_text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "promptText"))

    @prompt_text.setter
    def prompt_text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b03ad26a105ca508f38eed8c1879fd69c98120e415549840f86406768eb5b6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "promptText", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxGenerativeSettingsLlmModelSettings]:
        return typing.cast(typing.Optional[DialogflowCxGenerativeSettingsLlmModelSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxGenerativeSettingsLlmModelSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77c4781bc57bd484a9a88095e03b9d4d488e4b25c84e9a93684011984c690575)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxGenerativeSettings.DialogflowCxGenerativeSettingsTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DialogflowCxGenerativeSettingsTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#create DialogflowCxGenerativeSettings#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#delete DialogflowCxGenerativeSettings#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#update DialogflowCxGenerativeSettings#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0667d05f2c297e6de0f3b7499f846536a522df1a5f4f52f299115b11a3a1c613)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#create DialogflowCxGenerativeSettings#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#delete DialogflowCxGenerativeSettings#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generative_settings#update DialogflowCxGenerativeSettings#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxGenerativeSettingsTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxGenerativeSettingsTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxGenerativeSettings.DialogflowCxGenerativeSettingsTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__82814718050a66dc7c36149c12d92e3866a2a536415180d2824d2af0cb3c7fed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7036f3d4e633964b2e00c9941faca91fae5656c03b3483bacd6ca89f58ecdd1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27c93466e19fddae29e13d0468d3efe89c9ef3196b2c535b36253d55546d6f08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__740161c604680fa699c316bd0bedc252fba0a5adf978e31dc78794b9beb23433)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxGenerativeSettingsTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxGenerativeSettingsTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxGenerativeSettingsTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee839dac3579f7e1774bf8c99fef63898d0efb9c767275f0171848a1f4520ea5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DialogflowCxGenerativeSettings",
    "DialogflowCxGenerativeSettingsConfig",
    "DialogflowCxGenerativeSettingsFallbackSettings",
    "DialogflowCxGenerativeSettingsFallbackSettingsOutputReference",
    "DialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates",
    "DialogflowCxGenerativeSettingsFallbackSettingsPromptTemplatesList",
    "DialogflowCxGenerativeSettingsFallbackSettingsPromptTemplatesOutputReference",
    "DialogflowCxGenerativeSettingsGenerativeSafetySettings",
    "DialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases",
    "DialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrasesList",
    "DialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrasesOutputReference",
    "DialogflowCxGenerativeSettingsGenerativeSafetySettingsOutputReference",
    "DialogflowCxGenerativeSettingsKnowledgeConnectorSettings",
    "DialogflowCxGenerativeSettingsKnowledgeConnectorSettingsOutputReference",
    "DialogflowCxGenerativeSettingsLlmModelSettings",
    "DialogflowCxGenerativeSettingsLlmModelSettingsOutputReference",
    "DialogflowCxGenerativeSettingsTimeouts",
    "DialogflowCxGenerativeSettingsTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__6f9e13a0eba5c6c58ab03ba3bffabaa1503eeca8a535347c65bef5b1cddb3b30(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    language_code: builtins.str,
    fallback_settings: typing.Optional[typing.Union[DialogflowCxGenerativeSettingsFallbackSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    generative_safety_settings: typing.Optional[typing.Union[DialogflowCxGenerativeSettingsGenerativeSafetySettings, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    knowledge_connector_settings: typing.Optional[typing.Union[DialogflowCxGenerativeSettingsKnowledgeConnectorSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    llm_model_settings: typing.Optional[typing.Union[DialogflowCxGenerativeSettingsLlmModelSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    parent: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DialogflowCxGenerativeSettingsTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__498fc38d8ccee4e0281493b841db1f592c35328dba78bdc04347c8bd270c3a53(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed61e33dbe415f2ce2cdbd4b98716e4ff3ae25a7452c414d2c3b779ee29dfb26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e72dae76564ad2c3563cf0d757ef89d802228b826fec300849d2e15278cd332(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__110093a41cd98fc02e9722edd8b3d3d2d4fc96569e5c201898b9315fb389c739(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af797bd9ac005f9cb5e0c8b682d0d102e5f9d53abe369add05a1cdd1e91be8b2(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    language_code: builtins.str,
    fallback_settings: typing.Optional[typing.Union[DialogflowCxGenerativeSettingsFallbackSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    generative_safety_settings: typing.Optional[typing.Union[DialogflowCxGenerativeSettingsGenerativeSafetySettings, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    knowledge_connector_settings: typing.Optional[typing.Union[DialogflowCxGenerativeSettingsKnowledgeConnectorSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    llm_model_settings: typing.Optional[typing.Union[DialogflowCxGenerativeSettingsLlmModelSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    parent: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DialogflowCxGenerativeSettingsTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2033f4d4bae1361748107906fa4c87a0a77666ff961a47e4961fc55daf443e73(
    *,
    prompt_templates: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates, typing.Dict[builtins.str, typing.Any]]]]] = None,
    selected_prompt: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6cefbb0ac84d00bea0f90867e816e88b60cd5e8d6495191d0388042bdb41fd8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9f7c1a246051d5d9e3c23bdbbbffd56163fdb3a2d7e3920d34ca961bba066c9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3897135f1506fc39cdfbebcfd38161ca91d5bffb3c80c9360e3823b971227732(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af00d30c4153292d50cc93283599e23ec3cfc1773335959cd5b6e8a9643bc1a7(
    value: typing.Optional[DialogflowCxGenerativeSettingsFallbackSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76e576b38c0dbf7cd1bde2ab603173287168b8a7cced02bb7cd7697b1a05e8ed(
    *,
    display_name: typing.Optional[builtins.str] = None,
    frozen: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prompt_text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9e2889b80ce764c508f3423e12aacb32a36e1cb6dfb84d25e7123f2ac55cca5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a65fe4f1322b7022606d3695ad54b7245d2d9bd297c1d962515e6205440d6fe9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e877f375242aac7d50bbb0af207e9a1f62b775b2343f2a8462fa6f0536140d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d925e15add917b6570ea63dd83e6069423e67480ab52350fd05727b16ac8ead(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c45979ea224c082706905600811fd718984d3e138309177b63c4594c3660f097(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7afbd9efc0be046c43d73448be22ad2e2291dfee76da7a8c4dc7cafb3b9fb2e5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2a0040d8b7c6619f4010964982299a06b30b2879e44a09bf9a6df8e27331b8b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed828726adc9119ef4ae0f77b96579e493f3b2b8b1ce29e8cb1e9b69893ffdc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf8cb3d3cf7f943083e6d66361815365a095e3536f69932256fb0684a5f98b29(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4157c87fb1c9576e93c35a57d6da352bc85c81e4e801a6131450ed991de52663(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0236e2047d3b96fccfcc2f1543ff1c5c88aac06dfc54424d863817a2ad3e6833(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxGenerativeSettingsFallbackSettingsPromptTemplates]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aafa25e7a87cfdab684399b326d3bde07184ea94ecf2b9fe1b43c96bb85f61e(
    *,
    banned_phrases: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_banned_phrase_match_strategy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__799b93b78e93eccee09f188d345bc6697b5b3354d2900129fab4ad115d2bc0ae(
    *,
    language_code: builtins.str,
    text: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8a5e7f46202f8da0de71b532f524c9a09108de88b69b793cb1dd0ac141b018a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e47a3def89abb602d81e2465df71db5ce220f19fc9fd256164f19269b81d782(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa36f4586a222c5b7394bc4b10765d73de67c236daf068df0c08ed2d6216bcdc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__497ac92a3b4acf2d0c3574ba5c671b5195bf9c79b65fdbcc418d55e34d34ff8c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__299b53b6cb9085026e18199fb7a9c02037d01d376f881f00f83e84898d715be9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__828bc472c3ef4240066e672dc9b6249ee85bd56faa613c95a0c8a0b5e865ccde(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d44298f6d9d3709a0a9547220370f13c446438ddb97f6ff6982ec9d653dff625(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b695d3ce9b122cc7a366cfee6ef08b902e429fa5f7c867765a1ed1bae4e5fcc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c5ba77cce9e00a9c50b682eb41f509da3d926d79ce9549681bb873a95318759(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5706daa3ec85fe3eeda768bf81ac3ae86f83dd1fbd947ea1297718e67f63de3f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__389aa372d24429af330e9dd7c3c189e6cf4281932bb546cbacdfc2d6478dff18(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff4acedcea066a3d0b287457365312e2c5d2c85d1f995104e0313417bcb5d0ae(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxGenerativeSettingsGenerativeSafetySettingsBannedPhrases, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a04acace05a22e2bdcdd47d1494ff865ceb111bb9e118ebc3bdb1f665dafde82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9fd5ef6e90f651b0a98b83539d3856683a6a66ea70a403cb2b6f5a22b181bd5(
    value: typing.Optional[DialogflowCxGenerativeSettingsGenerativeSafetySettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0f22e5ab24673e30b1b1db9a6a71e3d4354b92c71627385e3562552381a1385(
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

def _typecheckingstub__5b29de2cb9630efedfb60d8589b4fe8b99ff3b36afad82314b219ed30268c011(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d02f556de3eb2590236932562c99f042336d247b61cda103373d8507abf6fe37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c1560b04dc051a39614718d3182e6c8c67e7fb8850e65ee35d857b1e982cd72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4f579cf465d9aa95eeb7ab4db99786bc3e10802dc81815b88e2a215ee7e264f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef7f6471c32d5320bd304037df99f64567a986ac01bc188cbfc2520bfde60962(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f868853af833b0600ac386ffffd9aeb16564320adcc0365aa3960711eca77e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7303ff59ef7a9d06c5303acc5c40ba31ccd9c884ad4fefd97abe61011ddba846(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b91edb0e448bc75327f1b262b5a6f90c59967c4fbeba4f04bb1a8efd813aea5a(
    value: typing.Optional[DialogflowCxGenerativeSettingsKnowledgeConnectorSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__607eb357a726144355be3840a6bc58530b57f053d5d2418e0a2e47d7f7c2ef2f(
    *,
    model: typing.Optional[builtins.str] = None,
    prompt_text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8ca4ce879420b8c95180757eff4ab5022285727fe0dc6ba0e4ef77ddd1db241(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31670bf9675b6def63e94588682460b4d36596a4292ae1a5ab284118ec015ca3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b03ad26a105ca508f38eed8c1879fd69c98120e415549840f86406768eb5b6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77c4781bc57bd484a9a88095e03b9d4d488e4b25c84e9a93684011984c690575(
    value: typing.Optional[DialogflowCxGenerativeSettingsLlmModelSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0667d05f2c297e6de0f3b7499f846536a522df1a5f4f52f299115b11a3a1c613(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82814718050a66dc7c36149c12d92e3866a2a536415180d2824d2af0cb3c7fed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7036f3d4e633964b2e00c9941faca91fae5656c03b3483bacd6ca89f58ecdd1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27c93466e19fddae29e13d0468d3efe89c9ef3196b2c535b36253d55546d6f08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__740161c604680fa699c316bd0bedc252fba0a5adf978e31dc78794b9beb23433(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee839dac3579f7e1774bf8c99fef63898d0efb9c767275f0171848a1f4520ea5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxGenerativeSettingsTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
