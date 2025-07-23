r'''
# `google_dialogflow_cx_generator`

Refer to the Terraform Registry for docs: [`google_dialogflow_cx_generator`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator).
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


class DialogflowCxGenerator(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxGenerator.DialogflowCxGenerator",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator google_dialogflow_cx_generator}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        prompt_text: typing.Union["DialogflowCxGeneratorPromptText", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        language_code: typing.Optional[builtins.str] = None,
        llm_model_settings: typing.Optional[typing.Union["DialogflowCxGeneratorLlmModelSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        model_parameter: typing.Optional[typing.Union["DialogflowCxGeneratorModelParameter", typing.Dict[builtins.str, typing.Any]]] = None,
        parent: typing.Optional[builtins.str] = None,
        placeholders: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxGeneratorPlaceholders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["DialogflowCxGeneratorTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator google_dialogflow_cx_generator} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: The human-readable name of the generator, unique within the agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#display_name DialogflowCxGenerator#display_name}
        :param prompt_text: prompt_text block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#prompt_text DialogflowCxGenerator#prompt_text}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#id DialogflowCxGenerator#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param language_code: The language to create generators for the following fields: * Generator.prompt_text.text If not specified, the agent's default language is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#language_code DialogflowCxGenerator#language_code}
        :param llm_model_settings: llm_model_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#llm_model_settings DialogflowCxGenerator#llm_model_settings}
        :param model_parameter: model_parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#model_parameter DialogflowCxGenerator#model_parameter}
        :param parent: The agent to create a Generator for. Format: projects//locations//agents/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#parent DialogflowCxGenerator#parent}
        :param placeholders: placeholders block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#placeholders DialogflowCxGenerator#placeholders}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#timeouts DialogflowCxGenerator#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8459aa47de511f41c9b3055557f2df345a2c2da301c7c9a0ec462ed0ca8dafe5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DialogflowCxGeneratorConfig(
            display_name=display_name,
            prompt_text=prompt_text,
            id=id,
            language_code=language_code,
            llm_model_settings=llm_model_settings,
            model_parameter=model_parameter,
            parent=parent,
            placeholders=placeholders,
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
        '''Generates CDKTF code for importing a DialogflowCxGenerator resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DialogflowCxGenerator to import.
        :param import_from_id: The id of the existing DialogflowCxGenerator that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DialogflowCxGenerator to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6724a18668a5129af9fd6f131186f3ce059e496ef642e88bd9cbf814f3b82971)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putLlmModelSettings")
    def put_llm_model_settings(
        self,
        *,
        model: typing.Optional[builtins.str] = None,
        prompt_text: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param model: The selected LLM model. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#model DialogflowCxGenerator#model}
        :param prompt_text: The custom prompt to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#prompt_text DialogflowCxGenerator#prompt_text}
        '''
        value = DialogflowCxGeneratorLlmModelSettings(
            model=model, prompt_text=prompt_text
        )

        return typing.cast(None, jsii.invoke(self, "putLlmModelSettings", [value]))

    @jsii.member(jsii_name="putModelParameter")
    def put_model_parameter(
        self,
        *,
        max_decode_steps: typing.Optional[jsii.Number] = None,
        temperature: typing.Optional[jsii.Number] = None,
        top_k: typing.Optional[jsii.Number] = None,
        top_p: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_decode_steps: The maximum number of tokens to generate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#max_decode_steps DialogflowCxGenerator#max_decode_steps}
        :param temperature: The temperature used for sampling. Temperature sampling occurs after both topP and topK have been applied. Valid range: [0.0, 1.0] Low temperature = less random. High temperature = more random. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#temperature DialogflowCxGenerator#temperature}
        :param top_k: If set, the sampling process in each step is limited to the topK tokens with highest probabilities. Valid range: [1, 40] or 1000+. Small topK = less random. Large topK = more random. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#top_k DialogflowCxGenerator#top_k}
        :param top_p: If set, only the tokens comprising the top topP probability mass are considered. If both topP and topK are set, topP will be used for further refining candidates selected with topK. Valid range: (0.0, 1.0]. Small topP = less random. Large topP = more random. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#top_p DialogflowCxGenerator#top_p}
        '''
        value = DialogflowCxGeneratorModelParameter(
            max_decode_steps=max_decode_steps,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
        )

        return typing.cast(None, jsii.invoke(self, "putModelParameter", [value]))

    @jsii.member(jsii_name="putPlaceholders")
    def put_placeholders(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxGeneratorPlaceholders", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad43b479cc92e117ef33953c05325cc579bd835b484f95ffe5ee03d5f2e7e603)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPlaceholders", [value]))

    @jsii.member(jsii_name="putPromptText")
    def put_prompt_text(self, *, text: typing.Optional[builtins.str] = None) -> None:
        '''
        :param text: Text input which can be used for prompt or banned phrases. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#text DialogflowCxGenerator#text}
        '''
        value = DialogflowCxGeneratorPromptText(text=text)

        return typing.cast(None, jsii.invoke(self, "putPromptText", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#create DialogflowCxGenerator#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#delete DialogflowCxGenerator#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#update DialogflowCxGenerator#update}.
        '''
        value = DialogflowCxGeneratorTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLanguageCode")
    def reset_language_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLanguageCode", []))

    @jsii.member(jsii_name="resetLlmModelSettings")
    def reset_llm_model_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLlmModelSettings", []))

    @jsii.member(jsii_name="resetModelParameter")
    def reset_model_parameter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModelParameter", []))

    @jsii.member(jsii_name="resetParent")
    def reset_parent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParent", []))

    @jsii.member(jsii_name="resetPlaceholders")
    def reset_placeholders(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlaceholders", []))

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
    @jsii.member(jsii_name="llmModelSettings")
    def llm_model_settings(
        self,
    ) -> "DialogflowCxGeneratorLlmModelSettingsOutputReference":
        return typing.cast("DialogflowCxGeneratorLlmModelSettingsOutputReference", jsii.get(self, "llmModelSettings"))

    @builtins.property
    @jsii.member(jsii_name="modelParameter")
    def model_parameter(self) -> "DialogflowCxGeneratorModelParameterOutputReference":
        return typing.cast("DialogflowCxGeneratorModelParameterOutputReference", jsii.get(self, "modelParameter"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="placeholders")
    def placeholders(self) -> "DialogflowCxGeneratorPlaceholdersList":
        return typing.cast("DialogflowCxGeneratorPlaceholdersList", jsii.get(self, "placeholders"))

    @builtins.property
    @jsii.member(jsii_name="promptText")
    def prompt_text(self) -> "DialogflowCxGeneratorPromptTextOutputReference":
        return typing.cast("DialogflowCxGeneratorPromptTextOutputReference", jsii.get(self, "promptText"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DialogflowCxGeneratorTimeoutsOutputReference":
        return typing.cast("DialogflowCxGeneratorTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="languageCodeInput")
    def language_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "languageCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="llmModelSettingsInput")
    def llm_model_settings_input(
        self,
    ) -> typing.Optional["DialogflowCxGeneratorLlmModelSettings"]:
        return typing.cast(typing.Optional["DialogflowCxGeneratorLlmModelSettings"], jsii.get(self, "llmModelSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="modelParameterInput")
    def model_parameter_input(
        self,
    ) -> typing.Optional["DialogflowCxGeneratorModelParameter"]:
        return typing.cast(typing.Optional["DialogflowCxGeneratorModelParameter"], jsii.get(self, "modelParameterInput"))

    @builtins.property
    @jsii.member(jsii_name="parentInput")
    def parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentInput"))

    @builtins.property
    @jsii.member(jsii_name="placeholdersInput")
    def placeholders_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxGeneratorPlaceholders"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxGeneratorPlaceholders"]]], jsii.get(self, "placeholdersInput"))

    @builtins.property
    @jsii.member(jsii_name="promptTextInput")
    def prompt_text_input(self) -> typing.Optional["DialogflowCxGeneratorPromptText"]:
        return typing.cast(typing.Optional["DialogflowCxGeneratorPromptText"], jsii.get(self, "promptTextInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DialogflowCxGeneratorTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DialogflowCxGeneratorTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e6a87059c1c42b4072b85bdfad22af7b647e24c7877961d268b80ba54d9585d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74a9a790eedabd9d9246ae9c46908067b6c51e59790acc4346f603196d884021)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="languageCode")
    def language_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "languageCode"))

    @language_code.setter
    def language_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e319feda697b6676c68b708f1158a83c98ed6d67abd65900e19fe12476840fbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "languageCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b7764d55b9e9a3be86cabc53b2dbda2288e9608984929d603d9574ca5502a65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxGenerator.DialogflowCxGeneratorConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "display_name": "displayName",
        "prompt_text": "promptText",
        "id": "id",
        "language_code": "languageCode",
        "llm_model_settings": "llmModelSettings",
        "model_parameter": "modelParameter",
        "parent": "parent",
        "placeholders": "placeholders",
        "timeouts": "timeouts",
    },
)
class DialogflowCxGeneratorConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        display_name: builtins.str,
        prompt_text: typing.Union["DialogflowCxGeneratorPromptText", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        language_code: typing.Optional[builtins.str] = None,
        llm_model_settings: typing.Optional[typing.Union["DialogflowCxGeneratorLlmModelSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        model_parameter: typing.Optional[typing.Union["DialogflowCxGeneratorModelParameter", typing.Dict[builtins.str, typing.Any]]] = None,
        parent: typing.Optional[builtins.str] = None,
        placeholders: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxGeneratorPlaceholders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["DialogflowCxGeneratorTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: The human-readable name of the generator, unique within the agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#display_name DialogflowCxGenerator#display_name}
        :param prompt_text: prompt_text block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#prompt_text DialogflowCxGenerator#prompt_text}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#id DialogflowCxGenerator#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param language_code: The language to create generators for the following fields: * Generator.prompt_text.text If not specified, the agent's default language is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#language_code DialogflowCxGenerator#language_code}
        :param llm_model_settings: llm_model_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#llm_model_settings DialogflowCxGenerator#llm_model_settings}
        :param model_parameter: model_parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#model_parameter DialogflowCxGenerator#model_parameter}
        :param parent: The agent to create a Generator for. Format: projects//locations//agents/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#parent DialogflowCxGenerator#parent}
        :param placeholders: placeholders block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#placeholders DialogflowCxGenerator#placeholders}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#timeouts DialogflowCxGenerator#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(prompt_text, dict):
            prompt_text = DialogflowCxGeneratorPromptText(**prompt_text)
        if isinstance(llm_model_settings, dict):
            llm_model_settings = DialogflowCxGeneratorLlmModelSettings(**llm_model_settings)
        if isinstance(model_parameter, dict):
            model_parameter = DialogflowCxGeneratorModelParameter(**model_parameter)
        if isinstance(timeouts, dict):
            timeouts = DialogflowCxGeneratorTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21d92b179cbc8d5ba37c6879419415ddea7619bd5524219a52b533fa955b3181)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument prompt_text", value=prompt_text, expected_type=type_hints["prompt_text"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument language_code", value=language_code, expected_type=type_hints["language_code"])
            check_type(argname="argument llm_model_settings", value=llm_model_settings, expected_type=type_hints["llm_model_settings"])
            check_type(argname="argument model_parameter", value=model_parameter, expected_type=type_hints["model_parameter"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument placeholders", value=placeholders, expected_type=type_hints["placeholders"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
            "prompt_text": prompt_text,
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
        if id is not None:
            self._values["id"] = id
        if language_code is not None:
            self._values["language_code"] = language_code
        if llm_model_settings is not None:
            self._values["llm_model_settings"] = llm_model_settings
        if model_parameter is not None:
            self._values["model_parameter"] = model_parameter
        if parent is not None:
            self._values["parent"] = parent
        if placeholders is not None:
            self._values["placeholders"] = placeholders
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
    def display_name(self) -> builtins.str:
        '''The human-readable name of the generator, unique within the agent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#display_name DialogflowCxGenerator#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def prompt_text(self) -> "DialogflowCxGeneratorPromptText":
        '''prompt_text block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#prompt_text DialogflowCxGenerator#prompt_text}
        '''
        result = self._values.get("prompt_text")
        assert result is not None, "Required property 'prompt_text' is missing"
        return typing.cast("DialogflowCxGeneratorPromptText", result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#id DialogflowCxGenerator#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def language_code(self) -> typing.Optional[builtins.str]:
        '''The language to create generators for the following fields: * Generator.prompt_text.text If not specified, the agent's default language is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#language_code DialogflowCxGenerator#language_code}
        '''
        result = self._values.get("language_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def llm_model_settings(
        self,
    ) -> typing.Optional["DialogflowCxGeneratorLlmModelSettings"]:
        '''llm_model_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#llm_model_settings DialogflowCxGenerator#llm_model_settings}
        '''
        result = self._values.get("llm_model_settings")
        return typing.cast(typing.Optional["DialogflowCxGeneratorLlmModelSettings"], result)

    @builtins.property
    def model_parameter(self) -> typing.Optional["DialogflowCxGeneratorModelParameter"]:
        '''model_parameter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#model_parameter DialogflowCxGenerator#model_parameter}
        '''
        result = self._values.get("model_parameter")
        return typing.cast(typing.Optional["DialogflowCxGeneratorModelParameter"], result)

    @builtins.property
    def parent(self) -> typing.Optional[builtins.str]:
        '''The agent to create a Generator for. Format: projects//locations//agents/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#parent DialogflowCxGenerator#parent}
        '''
        result = self._values.get("parent")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def placeholders(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxGeneratorPlaceholders"]]]:
        '''placeholders block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#placeholders DialogflowCxGenerator#placeholders}
        '''
        result = self._values.get("placeholders")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxGeneratorPlaceholders"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DialogflowCxGeneratorTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#timeouts DialogflowCxGenerator#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DialogflowCxGeneratorTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxGeneratorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxGenerator.DialogflowCxGeneratorLlmModelSettings",
    jsii_struct_bases=[],
    name_mapping={"model": "model", "prompt_text": "promptText"},
)
class DialogflowCxGeneratorLlmModelSettings:
    def __init__(
        self,
        *,
        model: typing.Optional[builtins.str] = None,
        prompt_text: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param model: The selected LLM model. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#model DialogflowCxGenerator#model}
        :param prompt_text: The custom prompt to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#prompt_text DialogflowCxGenerator#prompt_text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c981ce346c4d35f46b9c1b3a3bc61c1ce9c69f06b250cc556d0c53427329d02)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#model DialogflowCxGenerator#model}
        '''
        result = self._values.get("model")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prompt_text(self) -> typing.Optional[builtins.str]:
        '''The custom prompt to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#prompt_text DialogflowCxGenerator#prompt_text}
        '''
        result = self._values.get("prompt_text")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxGeneratorLlmModelSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxGeneratorLlmModelSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxGenerator.DialogflowCxGeneratorLlmModelSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d543ec27753481de44c45c9194ed94ee9f24e099013cc86e6bf285cc6f411f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d03d8ef1ca9b46d4ff2eaca3c2c8cfd60d8a69d77bacb377119adcc60072f31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "model", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="promptText")
    def prompt_text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "promptText"))

    @prompt_text.setter
    def prompt_text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8238baf55101b6a2ed891bb3661cbcf4c8fc182c26587692b738ac048258f5df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "promptText", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DialogflowCxGeneratorLlmModelSettings]:
        return typing.cast(typing.Optional[DialogflowCxGeneratorLlmModelSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxGeneratorLlmModelSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3d58ad9218d163802dd70082d6a2cf9d50e33c444cd3ebf5d4291774e9c4fdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxGenerator.DialogflowCxGeneratorModelParameter",
    jsii_struct_bases=[],
    name_mapping={
        "max_decode_steps": "maxDecodeSteps",
        "temperature": "temperature",
        "top_k": "topK",
        "top_p": "topP",
    },
)
class DialogflowCxGeneratorModelParameter:
    def __init__(
        self,
        *,
        max_decode_steps: typing.Optional[jsii.Number] = None,
        temperature: typing.Optional[jsii.Number] = None,
        top_k: typing.Optional[jsii.Number] = None,
        top_p: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_decode_steps: The maximum number of tokens to generate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#max_decode_steps DialogflowCxGenerator#max_decode_steps}
        :param temperature: The temperature used for sampling. Temperature sampling occurs after both topP and topK have been applied. Valid range: [0.0, 1.0] Low temperature = less random. High temperature = more random. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#temperature DialogflowCxGenerator#temperature}
        :param top_k: If set, the sampling process in each step is limited to the topK tokens with highest probabilities. Valid range: [1, 40] or 1000+. Small topK = less random. Large topK = more random. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#top_k DialogflowCxGenerator#top_k}
        :param top_p: If set, only the tokens comprising the top topP probability mass are considered. If both topP and topK are set, topP will be used for further refining candidates selected with topK. Valid range: (0.0, 1.0]. Small topP = less random. Large topP = more random. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#top_p DialogflowCxGenerator#top_p}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69796093af44e42135297bd4b89260fa9d97195a6d60fe0c7e9a8ebb2ea560b7)
            check_type(argname="argument max_decode_steps", value=max_decode_steps, expected_type=type_hints["max_decode_steps"])
            check_type(argname="argument temperature", value=temperature, expected_type=type_hints["temperature"])
            check_type(argname="argument top_k", value=top_k, expected_type=type_hints["top_k"])
            check_type(argname="argument top_p", value=top_p, expected_type=type_hints["top_p"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_decode_steps is not None:
            self._values["max_decode_steps"] = max_decode_steps
        if temperature is not None:
            self._values["temperature"] = temperature
        if top_k is not None:
            self._values["top_k"] = top_k
        if top_p is not None:
            self._values["top_p"] = top_p

    @builtins.property
    def max_decode_steps(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of tokens to generate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#max_decode_steps DialogflowCxGenerator#max_decode_steps}
        '''
        result = self._values.get("max_decode_steps")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def temperature(self) -> typing.Optional[jsii.Number]:
        '''The temperature used for sampling.

        Temperature sampling occurs after both topP and topK have been applied.
        Valid range: [0.0, 1.0] Low temperature = less random. High temperature = more random.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#temperature DialogflowCxGenerator#temperature}
        '''
        result = self._values.get("temperature")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def top_k(self) -> typing.Optional[jsii.Number]:
        '''If set, the sampling process in each step is limited to the topK tokens with highest probabilities.

        Valid range: [1, 40] or 1000+. Small topK = less random. Large topK = more random.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#top_k DialogflowCxGenerator#top_k}
        '''
        result = self._values.get("top_k")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def top_p(self) -> typing.Optional[jsii.Number]:
        '''If set, only the tokens comprising the top topP probability mass are considered.

        If both topP and topK are set, topP will be used for further refining candidates selected with topK.
        Valid range: (0.0, 1.0]. Small topP = less random. Large topP = more random.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#top_p DialogflowCxGenerator#top_p}
        '''
        result = self._values.get("top_p")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxGeneratorModelParameter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxGeneratorModelParameterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxGenerator.DialogflowCxGeneratorModelParameterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3cbecfc30f29f5e07d41e4d97a98da23596a6744f982a32c3b5a56f5ac79b64d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxDecodeSteps")
    def reset_max_decode_steps(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxDecodeSteps", []))

    @jsii.member(jsii_name="resetTemperature")
    def reset_temperature(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTemperature", []))

    @jsii.member(jsii_name="resetTopK")
    def reset_top_k(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTopK", []))

    @jsii.member(jsii_name="resetTopP")
    def reset_top_p(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTopP", []))

    @builtins.property
    @jsii.member(jsii_name="maxDecodeStepsInput")
    def max_decode_steps_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxDecodeStepsInput"))

    @builtins.property
    @jsii.member(jsii_name="temperatureInput")
    def temperature_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "temperatureInput"))

    @builtins.property
    @jsii.member(jsii_name="topKInput")
    def top_k_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "topKInput"))

    @builtins.property
    @jsii.member(jsii_name="topPInput")
    def top_p_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "topPInput"))

    @builtins.property
    @jsii.member(jsii_name="maxDecodeSteps")
    def max_decode_steps(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxDecodeSteps"))

    @max_decode_steps.setter
    def max_decode_steps(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a163b6a1c45476b9b95a56b2cb45ef3c9d337c0aee9a99e0b0c37829c9ca93b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxDecodeSteps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="temperature")
    def temperature(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "temperature"))

    @temperature.setter
    def temperature(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c68057539340da862ad3b972fc16650c039c395139ff23ec6f53e20d453da3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "temperature", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topK")
    def top_k(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "topK"))

    @top_k.setter
    def top_k(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5ac46713fdc0ffb63fe580bf12a25350656b34ff5847ec2e94faf0235d29401)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topK", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topP")
    def top_p(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "topP"))

    @top_p.setter
    def top_p(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1e8878df0c74b8d204eea1be2758568a3c2cd0c4999730f07d599981b91c5d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topP", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DialogflowCxGeneratorModelParameter]:
        return typing.cast(typing.Optional[DialogflowCxGeneratorModelParameter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxGeneratorModelParameter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1afc0f2d9c414fd74bd10691f4afbe187a8d45c734bd0a9e8184ce90ded0b55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxGenerator.DialogflowCxGeneratorPlaceholders",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "name": "name"},
)
class DialogflowCxGeneratorPlaceholders:
    def __init__(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: Unique ID used to map custom placeholder to parameters in fulfillment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#id DialogflowCxGenerator#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Custom placeholder value in the prompt text. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#name DialogflowCxGenerator#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e3ee39984a3cbd5d3a8632c2d827ba84422e16a859ae464df1f5ffacc2efcb2)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if id is not None:
            self._values["id"] = id
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Unique ID used to map custom placeholder to parameters in fulfillment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#id DialogflowCxGenerator#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Custom placeholder value in the prompt text.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#name DialogflowCxGenerator#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxGeneratorPlaceholders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxGeneratorPlaceholdersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxGenerator.DialogflowCxGeneratorPlaceholdersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be84e7ecd96e7fc9212d4150aa4de802018dec937d0a14921e8a4ab03ea399b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DialogflowCxGeneratorPlaceholdersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2271c1b2f29dfa0c21e1a385a8358333eab392e891af88579b10e6f8cf431b35)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DialogflowCxGeneratorPlaceholdersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfb0658fc4e1c5c0151f745b78a33e72bee405b877d5f7c13660e67bdf565ce9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7b776594ff7a258a3dd743cc3aab08e1caf3b38780edfb5670bb7705db908f2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea714b444031fd2b2228ea55a46bb6742b548e8a66bf3cfdb269898fc5d4892b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxGeneratorPlaceholders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxGeneratorPlaceholders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxGeneratorPlaceholders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29157b6ffeaff434cdc3520880a27798465a97edf54ad7295f25e876849be648)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxGeneratorPlaceholdersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxGenerator.DialogflowCxGeneratorPlaceholdersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__13a4a96d44f6c0675bef56d6a2cae18736f6c76407ad7eb7a0f26eccecfa6085)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44bdb21d04bc3fcbaada29ba0239775cc437685371dc44a121d8bcc238fea80c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbec06b1f66fb26f5d4dd08031f6a9b2e19387ae909ef2c301daa87e26ebf8bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxGeneratorPlaceholders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxGeneratorPlaceholders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxGeneratorPlaceholders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e813de0ed0c6de5cceb1fe97cb023c4fdfffe1fe47f73e3e2bf0e13db7b92425)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxGenerator.DialogflowCxGeneratorPromptText",
    jsii_struct_bases=[],
    name_mapping={"text": "text"},
)
class DialogflowCxGeneratorPromptText:
    def __init__(self, *, text: typing.Optional[builtins.str] = None) -> None:
        '''
        :param text: Text input which can be used for prompt or banned phrases. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#text DialogflowCxGenerator#text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7b08ef39d9c43ac82033e12c6b51e95b56d714663df307bc53ca6cb967aba62)
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if text is not None:
            self._values["text"] = text

    @builtins.property
    def text(self) -> typing.Optional[builtins.str]:
        '''Text input which can be used for prompt or banned phrases.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#text DialogflowCxGenerator#text}
        '''
        result = self._values.get("text")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxGeneratorPromptText(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxGeneratorPromptTextOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxGenerator.DialogflowCxGeneratorPromptTextOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8a8421fc1d130296ef2d17e59a7b63715492dbc6ead990986b95e25e110a157)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetText")
    def reset_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetText", []))

    @builtins.property
    @jsii.member(jsii_name="textInput")
    def text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "textInput"))

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "text"))

    @text.setter
    def text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95a18f54013440127446452d685d2a81a7a23e2cc0585696067d6150d0acac0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "text", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DialogflowCxGeneratorPromptText]:
        return typing.cast(typing.Optional[DialogflowCxGeneratorPromptText], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxGeneratorPromptText],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2578958035a0c36f57bd712d66344afe0f5175cf11cbf7c1c05c5b925996ef70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxGenerator.DialogflowCxGeneratorTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DialogflowCxGeneratorTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#create DialogflowCxGenerator#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#delete DialogflowCxGenerator#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#update DialogflowCxGenerator#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14dbc29b7d4cb0dd422160bc74f3b725fd19cfef10566b302ae637d25042f393)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#create DialogflowCxGenerator#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#delete DialogflowCxGenerator#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_generator#update DialogflowCxGenerator#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxGeneratorTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxGeneratorTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxGenerator.DialogflowCxGeneratorTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d30705f9f337a7d20f1b7fb7ca49934a08f5665983fe51bbbc6faf56b0c2a963)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c39e34b220f2d269bbd0254240913f6a39391589712450809043d5a3f922dc28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36042fe98c62e8f28deafa43db5739dffca36459ce5048489af0d219d9595926)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff79391b3cff6e95ce38f0bcbdad89dac014225ee9736929793428460ee8ec07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxGeneratorTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxGeneratorTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxGeneratorTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bbc0a51997c547617f2c29a2c2fa8f6ecf3580719d99271f0099565155508d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DialogflowCxGenerator",
    "DialogflowCxGeneratorConfig",
    "DialogflowCxGeneratorLlmModelSettings",
    "DialogflowCxGeneratorLlmModelSettingsOutputReference",
    "DialogflowCxGeneratorModelParameter",
    "DialogflowCxGeneratorModelParameterOutputReference",
    "DialogflowCxGeneratorPlaceholders",
    "DialogflowCxGeneratorPlaceholdersList",
    "DialogflowCxGeneratorPlaceholdersOutputReference",
    "DialogflowCxGeneratorPromptText",
    "DialogflowCxGeneratorPromptTextOutputReference",
    "DialogflowCxGeneratorTimeouts",
    "DialogflowCxGeneratorTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__8459aa47de511f41c9b3055557f2df345a2c2da301c7c9a0ec462ed0ca8dafe5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    prompt_text: typing.Union[DialogflowCxGeneratorPromptText, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    language_code: typing.Optional[builtins.str] = None,
    llm_model_settings: typing.Optional[typing.Union[DialogflowCxGeneratorLlmModelSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    model_parameter: typing.Optional[typing.Union[DialogflowCxGeneratorModelParameter, typing.Dict[builtins.str, typing.Any]]] = None,
    parent: typing.Optional[builtins.str] = None,
    placeholders: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxGeneratorPlaceholders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[DialogflowCxGeneratorTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__6724a18668a5129af9fd6f131186f3ce059e496ef642e88bd9cbf814f3b82971(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad43b479cc92e117ef33953c05325cc579bd835b484f95ffe5ee03d5f2e7e603(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxGeneratorPlaceholders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e6a87059c1c42b4072b85bdfad22af7b647e24c7877961d268b80ba54d9585d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74a9a790eedabd9d9246ae9c46908067b6c51e59790acc4346f603196d884021(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e319feda697b6676c68b708f1158a83c98ed6d67abd65900e19fe12476840fbf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b7764d55b9e9a3be86cabc53b2dbda2288e9608984929d603d9574ca5502a65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21d92b179cbc8d5ba37c6879419415ddea7619bd5524219a52b533fa955b3181(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: builtins.str,
    prompt_text: typing.Union[DialogflowCxGeneratorPromptText, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    language_code: typing.Optional[builtins.str] = None,
    llm_model_settings: typing.Optional[typing.Union[DialogflowCxGeneratorLlmModelSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    model_parameter: typing.Optional[typing.Union[DialogflowCxGeneratorModelParameter, typing.Dict[builtins.str, typing.Any]]] = None,
    parent: typing.Optional[builtins.str] = None,
    placeholders: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxGeneratorPlaceholders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[DialogflowCxGeneratorTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c981ce346c4d35f46b9c1b3a3bc61c1ce9c69f06b250cc556d0c53427329d02(
    *,
    model: typing.Optional[builtins.str] = None,
    prompt_text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d543ec27753481de44c45c9194ed94ee9f24e099013cc86e6bf285cc6f411f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d03d8ef1ca9b46d4ff2eaca3c2c8cfd60d8a69d77bacb377119adcc60072f31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8238baf55101b6a2ed891bb3661cbcf4c8fc182c26587692b738ac048258f5df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3d58ad9218d163802dd70082d6a2cf9d50e33c444cd3ebf5d4291774e9c4fdf(
    value: typing.Optional[DialogflowCxGeneratorLlmModelSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69796093af44e42135297bd4b89260fa9d97195a6d60fe0c7e9a8ebb2ea560b7(
    *,
    max_decode_steps: typing.Optional[jsii.Number] = None,
    temperature: typing.Optional[jsii.Number] = None,
    top_k: typing.Optional[jsii.Number] = None,
    top_p: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cbecfc30f29f5e07d41e4d97a98da23596a6744f982a32c3b5a56f5ac79b64d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a163b6a1c45476b9b95a56b2cb45ef3c9d337c0aee9a99e0b0c37829c9ca93b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c68057539340da862ad3b972fc16650c039c395139ff23ec6f53e20d453da3c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5ac46713fdc0ffb63fe580bf12a25350656b34ff5847ec2e94faf0235d29401(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1e8878df0c74b8d204eea1be2758568a3c2cd0c4999730f07d599981b91c5d1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1afc0f2d9c414fd74bd10691f4afbe187a8d45c734bd0a9e8184ce90ded0b55(
    value: typing.Optional[DialogflowCxGeneratorModelParameter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e3ee39984a3cbd5d3a8632c2d827ba84422e16a859ae464df1f5ffacc2efcb2(
    *,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be84e7ecd96e7fc9212d4150aa4de802018dec937d0a14921e8a4ab03ea399b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2271c1b2f29dfa0c21e1a385a8358333eab392e891af88579b10e6f8cf431b35(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfb0658fc4e1c5c0151f745b78a33e72bee405b877d5f7c13660e67bdf565ce9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7b776594ff7a258a3dd743cc3aab08e1caf3b38780edfb5670bb7705db908f2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea714b444031fd2b2228ea55a46bb6742b548e8a66bf3cfdb269898fc5d4892b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29157b6ffeaff434cdc3520880a27798465a97edf54ad7295f25e876849be648(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxGeneratorPlaceholders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13a4a96d44f6c0675bef56d6a2cae18736f6c76407ad7eb7a0f26eccecfa6085(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44bdb21d04bc3fcbaada29ba0239775cc437685371dc44a121d8bcc238fea80c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbec06b1f66fb26f5d4dd08031f6a9b2e19387ae909ef2c301daa87e26ebf8bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e813de0ed0c6de5cceb1fe97cb023c4fdfffe1fe47f73e3e2bf0e13db7b92425(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxGeneratorPlaceholders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7b08ef39d9c43ac82033e12c6b51e95b56d714663df307bc53ca6cb967aba62(
    *,
    text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8a8421fc1d130296ef2d17e59a7b63715492dbc6ead990986b95e25e110a157(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95a18f54013440127446452d685d2a81a7a23e2cc0585696067d6150d0acac0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2578958035a0c36f57bd712d66344afe0f5175cf11cbf7c1c05c5b925996ef70(
    value: typing.Optional[DialogflowCxGeneratorPromptText],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14dbc29b7d4cb0dd422160bc74f3b725fd19cfef10566b302ae637d25042f393(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d30705f9f337a7d20f1b7fb7ca49934a08f5665983fe51bbbc6faf56b0c2a963(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c39e34b220f2d269bbd0254240913f6a39391589712450809043d5a3f922dc28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36042fe98c62e8f28deafa43db5739dffca36459ce5048489af0d219d9595926(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff79391b3cff6e95ce38f0bcbdad89dac014225ee9736929793428460ee8ec07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bbc0a51997c547617f2c29a2c2fa8f6ecf3580719d99271f0099565155508d3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxGeneratorTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
