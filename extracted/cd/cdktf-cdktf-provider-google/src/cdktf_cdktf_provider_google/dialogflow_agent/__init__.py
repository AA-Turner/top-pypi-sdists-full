r'''
# `google_dialogflow_agent`

Refer to the Terraform Registry for docs: [`google_dialogflow_agent`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent).
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


class DialogflowAgent(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowAgent.DialogflowAgent",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent google_dialogflow_agent}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        default_language_code: builtins.str,
        display_name: builtins.str,
        time_zone: builtins.str,
        api_version: typing.Optional[builtins.str] = None,
        avatar_uri: typing.Optional[builtins.str] = None,
        classification_threshold: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        enable_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        match_mode: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        supported_language_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        tier: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DialogflowAgentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent google_dialogflow_agent} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param default_language_code: The default language of the agent as a language tag. `See Language Support <https://cloud.google.com/dialogflow/docs/reference/language>`_ for a list of the currently supported language codes. This field cannot be updated after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#default_language_code DialogflowAgent#default_language_code}
        :param display_name: The name of this agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#display_name DialogflowAgent#display_name}
        :param time_zone: The time zone of this agent from the `time zone database <https://www.iana.org/time-zones>`_, e.g., America/New_York, Europe/Paris. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#time_zone DialogflowAgent#time_zone}
        :param api_version: API version displayed in Dialogflow console. If not specified, V2 API is assumed. Clients are free to query different service endpoints for different API versions. However, bots connectors and webhook calls will follow the specified API version. - API_VERSION_V1: Legacy V1 API. - API_VERSION_V2: V2 API. - API_VERSION_V2_BETA_1: V2beta1 API. Possible values: ["API_VERSION_V1", "API_VERSION_V2", "API_VERSION_V2_BETA_1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#api_version DialogflowAgent#api_version}
        :param avatar_uri: The URI of the agent's avatar, which are used throughout the Dialogflow console. When an image URL is entered into this field, the Dialogflow will save the image in the backend. The address of the backend image returned from the API will be shown in the [avatarUriBackend] field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#avatar_uri DialogflowAgent#avatar_uri}
        :param classification_threshold: To filter out false positive results and still get variety in matched natural language inputs for your agent, you can tune the machine learning classification threshold. If the returned score value is less than the threshold value, then a fallback intent will be triggered or, if there are no fallback intents defined, no intent will be triggered. The score values range from 0.0 (completely uncertain) to 1.0 (completely certain). If set to 0.0, the default of 0.3 is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#classification_threshold DialogflowAgent#classification_threshold}
        :param description: The description of this agent. The maximum length is 500 characters. If exceeded, the request is rejected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#description DialogflowAgent#description}
        :param enable_logging: Determines whether this agent should log conversation queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#enable_logging DialogflowAgent#enable_logging}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#id DialogflowAgent#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param match_mode: Determines how intents are detected from user queries. - MATCH_MODE_HYBRID: Best for agents with a small number of examples in intents and/or wide use of templates syntax and composite entities. - MATCH_MODE_ML_ONLY: Can be used for agents with a large number of examples in intents, especially the ones using
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#project DialogflowAgent#project}.
        :param supported_language_codes: The list of all languages supported by this agent (except for the defaultLanguageCode). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#supported_language_codes DialogflowAgent#supported_language_codes}
        :param tier: The agent tier. If not specified, TIER_STANDARD is assumed. - TIER_STANDARD: Standard tier. - TIER_ENTERPRISE: Enterprise tier (Essentials). - TIER_ENTERPRISE_PLUS: Enterprise tier (Plus). NOTE: Due to consistency issues, the provider will not read this field from the API. Drift is possible between the Terraform state and Dialogflow if the agent tier is changed outside of Terraform. Possible values: ["TIER_STANDARD", "TIER_ENTERPRISE", "TIER_ENTERPRISE_PLUS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#tier DialogflowAgent#tier}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#timeouts DialogflowAgent#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df61727053125206b282c6e324ddf0e79ac277335091e1eb39b985f46c19ff1d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DialogflowAgentConfig(
            default_language_code=default_language_code,
            display_name=display_name,
            time_zone=time_zone,
            api_version=api_version,
            avatar_uri=avatar_uri,
            classification_threshold=classification_threshold,
            description=description,
            enable_logging=enable_logging,
            id=id,
            match_mode=match_mode,
            project=project,
            supported_language_codes=supported_language_codes,
            tier=tier,
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
        '''Generates CDKTF code for importing a DialogflowAgent resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DialogflowAgent to import.
        :param import_from_id: The id of the existing DialogflowAgent that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DialogflowAgent to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59fdddcdada7a7beaf6c0dc2ec34243b50c12b55a67cd040844e1bc61e4e62d3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#create DialogflowAgent#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#delete DialogflowAgent#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#update DialogflowAgent#update}.
        '''
        value = DialogflowAgentTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetApiVersion")
    def reset_api_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiVersion", []))

    @jsii.member(jsii_name="resetAvatarUri")
    def reset_avatar_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvatarUri", []))

    @jsii.member(jsii_name="resetClassificationThreshold")
    def reset_classification_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClassificationThreshold", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEnableLogging")
    def reset_enable_logging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableLogging", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMatchMode")
    def reset_match_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchMode", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetSupportedLanguageCodes")
    def reset_supported_language_codes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSupportedLanguageCodes", []))

    @jsii.member(jsii_name="resetTier")
    def reset_tier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTier", []))

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
    @jsii.member(jsii_name="avatarUriBackend")
    def avatar_uri_backend(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "avatarUriBackend"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DialogflowAgentTimeoutsOutputReference":
        return typing.cast("DialogflowAgentTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="apiVersionInput")
    def api_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="avatarUriInput")
    def avatar_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "avatarUriInput"))

    @builtins.property
    @jsii.member(jsii_name="classificationThresholdInput")
    def classification_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "classificationThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultLanguageCodeInput")
    def default_language_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultLanguageCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="enableLoggingInput")
    def enable_logging_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableLoggingInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="matchModeInput")
    def match_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "matchModeInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="supportedLanguageCodesInput")
    def supported_language_codes_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "supportedLanguageCodesInput"))

    @builtins.property
    @jsii.member(jsii_name="tierInput")
    def tier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tierInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DialogflowAgentTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DialogflowAgentTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="apiVersion")
    def api_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiVersion"))

    @api_version.setter
    def api_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e18ab9d8127e18ac953bfaa9ffc642f4766ea18188155c5d6a65463205635eba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="avatarUri")
    def avatar_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "avatarUri"))

    @avatar_uri.setter
    def avatar_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d3cbfdead0f3947ecbe8cd4b04295633b3bf1faca2fa119e7e40e12fb0df155)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "avatarUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="classificationThreshold")
    def classification_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "classificationThreshold"))

    @classification_threshold.setter
    def classification_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4d6ee27552051719f25f82f3dec9f4288299d1a8b632c33d80a81ed4044ea19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "classificationThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultLanguageCode")
    def default_language_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultLanguageCode"))

    @default_language_code.setter
    def default_language_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e4c38536776509efb66dc2c96b42f47a5d0c035af1a406c26e25c0b8797c024)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultLanguageCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73f6c1223aba38306ca16beefd84db665cf9209d68e681989ba1576a6ca2f16f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01c5976c2b798816756f2c2d88869035c50956c1dced088ef5c6bf8176bdef38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableLogging")
    def enable_logging(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableLogging"))

    @enable_logging.setter
    def enable_logging(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90cf25a2a79c2100ed82c663071380be44c298a2ff22c42c44d58ed9ef2deca6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableLogging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54e9ddb5d1fdebf32e192ac7e0cf95802a8b55992627be428c68b04ddf73fd09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="matchMode")
    def match_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "matchMode"))

    @match_mode.setter
    def match_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82344d3dc05a78d5be231c53c82a9819775fcfee2b392176cae306768cc59b70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ceb4d2ae38d9d5eaed5821318653148ce7545ad4325d090435d50428bae36c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="supportedLanguageCodes")
    def supported_language_codes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "supportedLanguageCodes"))

    @supported_language_codes.setter
    def supported_language_codes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60bd5bf6707c9f5d04f8c93bee488502de9b49a763c4bc1b7cf8774230e65d08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportedLanguageCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tier")
    def tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tier"))

    @tier.setter
    def tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__248edcf4c10fd6aa7d5abe5b4d1df9a2bd282c6c9c9a24a58774a88163ae1d66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db85b8fbf7190c701aefaac7b415f171808460970283c9224fb526c48e2e9896)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowAgent.DialogflowAgentConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "default_language_code": "defaultLanguageCode",
        "display_name": "displayName",
        "time_zone": "timeZone",
        "api_version": "apiVersion",
        "avatar_uri": "avatarUri",
        "classification_threshold": "classificationThreshold",
        "description": "description",
        "enable_logging": "enableLogging",
        "id": "id",
        "match_mode": "matchMode",
        "project": "project",
        "supported_language_codes": "supportedLanguageCodes",
        "tier": "tier",
        "timeouts": "timeouts",
    },
)
class DialogflowAgentConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        default_language_code: builtins.str,
        display_name: builtins.str,
        time_zone: builtins.str,
        api_version: typing.Optional[builtins.str] = None,
        avatar_uri: typing.Optional[builtins.str] = None,
        classification_threshold: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        enable_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        match_mode: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        supported_language_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        tier: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DialogflowAgentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param default_language_code: The default language of the agent as a language tag. `See Language Support <https://cloud.google.com/dialogflow/docs/reference/language>`_ for a list of the currently supported language codes. This field cannot be updated after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#default_language_code DialogflowAgent#default_language_code}
        :param display_name: The name of this agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#display_name DialogflowAgent#display_name}
        :param time_zone: The time zone of this agent from the `time zone database <https://www.iana.org/time-zones>`_, e.g., America/New_York, Europe/Paris. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#time_zone DialogflowAgent#time_zone}
        :param api_version: API version displayed in Dialogflow console. If not specified, V2 API is assumed. Clients are free to query different service endpoints for different API versions. However, bots connectors and webhook calls will follow the specified API version. - API_VERSION_V1: Legacy V1 API. - API_VERSION_V2: V2 API. - API_VERSION_V2_BETA_1: V2beta1 API. Possible values: ["API_VERSION_V1", "API_VERSION_V2", "API_VERSION_V2_BETA_1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#api_version DialogflowAgent#api_version}
        :param avatar_uri: The URI of the agent's avatar, which are used throughout the Dialogflow console. When an image URL is entered into this field, the Dialogflow will save the image in the backend. The address of the backend image returned from the API will be shown in the [avatarUriBackend] field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#avatar_uri DialogflowAgent#avatar_uri}
        :param classification_threshold: To filter out false positive results and still get variety in matched natural language inputs for your agent, you can tune the machine learning classification threshold. If the returned score value is less than the threshold value, then a fallback intent will be triggered or, if there are no fallback intents defined, no intent will be triggered. The score values range from 0.0 (completely uncertain) to 1.0 (completely certain). If set to 0.0, the default of 0.3 is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#classification_threshold DialogflowAgent#classification_threshold}
        :param description: The description of this agent. The maximum length is 500 characters. If exceeded, the request is rejected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#description DialogflowAgent#description}
        :param enable_logging: Determines whether this agent should log conversation queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#enable_logging DialogflowAgent#enable_logging}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#id DialogflowAgent#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param match_mode: Determines how intents are detected from user queries. - MATCH_MODE_HYBRID: Best for agents with a small number of examples in intents and/or wide use of templates syntax and composite entities. - MATCH_MODE_ML_ONLY: Can be used for agents with a large number of examples in intents, especially the ones using
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#project DialogflowAgent#project}.
        :param supported_language_codes: The list of all languages supported by this agent (except for the defaultLanguageCode). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#supported_language_codes DialogflowAgent#supported_language_codes}
        :param tier: The agent tier. If not specified, TIER_STANDARD is assumed. - TIER_STANDARD: Standard tier. - TIER_ENTERPRISE: Enterprise tier (Essentials). - TIER_ENTERPRISE_PLUS: Enterprise tier (Plus). NOTE: Due to consistency issues, the provider will not read this field from the API. Drift is possible between the Terraform state and Dialogflow if the agent tier is changed outside of Terraform. Possible values: ["TIER_STANDARD", "TIER_ENTERPRISE", "TIER_ENTERPRISE_PLUS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#tier DialogflowAgent#tier}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#timeouts DialogflowAgent#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = DialogflowAgentTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10454a9091860713e56186c185762d760d91b21e30cb1cd3e6b736b7a1a91266)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument default_language_code", value=default_language_code, expected_type=type_hints["default_language_code"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
            check_type(argname="argument api_version", value=api_version, expected_type=type_hints["api_version"])
            check_type(argname="argument avatar_uri", value=avatar_uri, expected_type=type_hints["avatar_uri"])
            check_type(argname="argument classification_threshold", value=classification_threshold, expected_type=type_hints["classification_threshold"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enable_logging", value=enable_logging, expected_type=type_hints["enable_logging"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument match_mode", value=match_mode, expected_type=type_hints["match_mode"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument supported_language_codes", value=supported_language_codes, expected_type=type_hints["supported_language_codes"])
            check_type(argname="argument tier", value=tier, expected_type=type_hints["tier"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_language_code": default_language_code,
            "display_name": display_name,
            "time_zone": time_zone,
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
        if api_version is not None:
            self._values["api_version"] = api_version
        if avatar_uri is not None:
            self._values["avatar_uri"] = avatar_uri
        if classification_threshold is not None:
            self._values["classification_threshold"] = classification_threshold
        if description is not None:
            self._values["description"] = description
        if enable_logging is not None:
            self._values["enable_logging"] = enable_logging
        if id is not None:
            self._values["id"] = id
        if match_mode is not None:
            self._values["match_mode"] = match_mode
        if project is not None:
            self._values["project"] = project
        if supported_language_codes is not None:
            self._values["supported_language_codes"] = supported_language_codes
        if tier is not None:
            self._values["tier"] = tier
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
    def default_language_code(self) -> builtins.str:
        '''The default language of the agent as a language tag.

        `See Language Support <https://cloud.google.com/dialogflow/docs/reference/language>`_
        for a list of the currently supported language codes. This field cannot be updated after creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#default_language_code DialogflowAgent#default_language_code}
        '''
        result = self._values.get("default_language_code")
        assert result is not None, "Required property 'default_language_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''The name of this agent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#display_name DialogflowAgent#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def time_zone(self) -> builtins.str:
        '''The time zone of this agent from the `time zone database <https://www.iana.org/time-zones>`_, e.g., America/New_York, Europe/Paris.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#time_zone DialogflowAgent#time_zone}
        '''
        result = self._values.get("time_zone")
        assert result is not None, "Required property 'time_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_version(self) -> typing.Optional[builtins.str]:
        '''API version displayed in Dialogflow console.

        If not specified, V2 API is assumed. Clients are free to query
        different service endpoints for different API versions. However, bots connectors and webhook calls will follow
        the specified API version.

        - API_VERSION_V1: Legacy V1 API.
        - API_VERSION_V2: V2 API.
        - API_VERSION_V2_BETA_1: V2beta1 API. Possible values: ["API_VERSION_V1", "API_VERSION_V2", "API_VERSION_V2_BETA_1"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#api_version DialogflowAgent#api_version}
        '''
        result = self._values.get("api_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def avatar_uri(self) -> typing.Optional[builtins.str]:
        '''The URI of the agent's avatar, which are used throughout the Dialogflow console.

        When an image URL is entered
        into this field, the Dialogflow will save the image in the backend. The address of the backend image returned
        from the API will be shown in the [avatarUriBackend] field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#avatar_uri DialogflowAgent#avatar_uri}
        '''
        result = self._values.get("avatar_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def classification_threshold(self) -> typing.Optional[jsii.Number]:
        '''To filter out false positive results and still get variety in matched natural language inputs for your agent, you can tune the machine learning classification threshold.

        If the returned score value is less than the threshold
        value, then a fallback intent will be triggered or, if there are no fallback intents defined, no intent will be
        triggered. The score values range from 0.0 (completely uncertain) to 1.0 (completely certain). If set to 0.0, the
        default of 0.3 is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#classification_threshold DialogflowAgent#classification_threshold}
        '''
        result = self._values.get("classification_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of this agent. The maximum length is 500 characters. If exceeded, the request is rejected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#description DialogflowAgent#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines whether this agent should log conversation queries.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#enable_logging DialogflowAgent#enable_logging}
        '''
        result = self._values.get("enable_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#id DialogflowAgent#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def match_mode(self) -> typing.Optional[builtins.str]:
        '''Determines how intents are detected from user queries.

        - MATCH_MODE_HYBRID: Best for agents with a small number of examples in intents and/or wide use of templates
          syntax and composite entities.
        - MATCH_MODE_ML_ONLY: Can be used for agents with a large number of examples in intents, especially the ones
          using

        :sys:

        .any or very large developer entities. Possible values: ["MATCH_MODE_HYBRID", "MATCH_MODE_ML_ONLY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#match_mode DialogflowAgent#match_mode}
        '''
        result = self._values.get("match_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#project DialogflowAgent#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def supported_language_codes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of all languages supported by this agent (except for the defaultLanguageCode).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#supported_language_codes DialogflowAgent#supported_language_codes}
        '''
        result = self._values.get("supported_language_codes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tier(self) -> typing.Optional[builtins.str]:
        '''The agent tier.

        If not specified, TIER_STANDARD is assumed.

        - TIER_STANDARD: Standard tier.
        - TIER_ENTERPRISE: Enterprise tier (Essentials).
        - TIER_ENTERPRISE_PLUS: Enterprise tier (Plus).
          NOTE: Due to consistency issues, the provider will not read this field from the API. Drift is possible between
          the Terraform state and Dialogflow if the agent tier is changed outside of Terraform. Possible values: ["TIER_STANDARD", "TIER_ENTERPRISE", "TIER_ENTERPRISE_PLUS"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#tier DialogflowAgent#tier}
        '''
        result = self._values.get("tier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DialogflowAgentTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#timeouts DialogflowAgent#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DialogflowAgentTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowAgentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowAgent.DialogflowAgentTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DialogflowAgentTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#create DialogflowAgent#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#delete DialogflowAgent#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#update DialogflowAgent#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f2af4e2ca177feec8cf91bd70e2c654c3dcfa2047534a59e12ac4fd57335d4f)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#create DialogflowAgent#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#delete DialogflowAgent#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_agent#update DialogflowAgent#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowAgentTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowAgentTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowAgent.DialogflowAgentTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a74cf6ede0f85e9b7fa9d9e2be3c4c939ab49ec3a1c9c0939b41c8da610678b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aae380e6218fdd490b1327bca9a713efe8f026bcbe198b5cbeab208edab84523)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be9fa486b7857ee06689b8ce64a31981d02fbf97a4525b62a5e7258c5756200b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6fcb329c4c92f9f26fddbad6bb2e19d1dac02666e264dbbc0514998f548da94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowAgentTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowAgentTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowAgentTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec03b4988e808bddf9efa1fc084d9ab8728cd61825666d51a039e91e1387ac84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DialogflowAgent",
    "DialogflowAgentConfig",
    "DialogflowAgentTimeouts",
    "DialogflowAgentTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__df61727053125206b282c6e324ddf0e79ac277335091e1eb39b985f46c19ff1d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    default_language_code: builtins.str,
    display_name: builtins.str,
    time_zone: builtins.str,
    api_version: typing.Optional[builtins.str] = None,
    avatar_uri: typing.Optional[builtins.str] = None,
    classification_threshold: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    enable_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    match_mode: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    supported_language_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
    tier: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DialogflowAgentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__59fdddcdada7a7beaf6c0dc2ec34243b50c12b55a67cd040844e1bc61e4e62d3(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e18ab9d8127e18ac953bfaa9ffc642f4766ea18188155c5d6a65463205635eba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d3cbfdead0f3947ecbe8cd4b04295633b3bf1faca2fa119e7e40e12fb0df155(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4d6ee27552051719f25f82f3dec9f4288299d1a8b632c33d80a81ed4044ea19(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e4c38536776509efb66dc2c96b42f47a5d0c035af1a406c26e25c0b8797c024(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73f6c1223aba38306ca16beefd84db665cf9209d68e681989ba1576a6ca2f16f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01c5976c2b798816756f2c2d88869035c50956c1dced088ef5c6bf8176bdef38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90cf25a2a79c2100ed82c663071380be44c298a2ff22c42c44d58ed9ef2deca6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54e9ddb5d1fdebf32e192ac7e0cf95802a8b55992627be428c68b04ddf73fd09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82344d3dc05a78d5be231c53c82a9819775fcfee2b392176cae306768cc59b70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ceb4d2ae38d9d5eaed5821318653148ce7545ad4325d090435d50428bae36c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60bd5bf6707c9f5d04f8c93bee488502de9b49a763c4bc1b7cf8774230e65d08(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__248edcf4c10fd6aa7d5abe5b4d1df9a2bd282c6c9c9a24a58774a88163ae1d66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db85b8fbf7190c701aefaac7b415f171808460970283c9224fb526c48e2e9896(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10454a9091860713e56186c185762d760d91b21e30cb1cd3e6b736b7a1a91266(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_language_code: builtins.str,
    display_name: builtins.str,
    time_zone: builtins.str,
    api_version: typing.Optional[builtins.str] = None,
    avatar_uri: typing.Optional[builtins.str] = None,
    classification_threshold: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    enable_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    match_mode: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    supported_language_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
    tier: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DialogflowAgentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f2af4e2ca177feec8cf91bd70e2c654c3dcfa2047534a59e12ac4fd57335d4f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a74cf6ede0f85e9b7fa9d9e2be3c4c939ab49ec3a1c9c0939b41c8da610678b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aae380e6218fdd490b1327bca9a713efe8f026bcbe198b5cbeab208edab84523(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be9fa486b7857ee06689b8ce64a31981d02fbf97a4525b62a5e7258c5756200b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6fcb329c4c92f9f26fddbad6bb2e19d1dac02666e264dbbc0514998f548da94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec03b4988e808bddf9efa1fc084d9ab8728cd61825666d51a039e91e1387ac84(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowAgentTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
