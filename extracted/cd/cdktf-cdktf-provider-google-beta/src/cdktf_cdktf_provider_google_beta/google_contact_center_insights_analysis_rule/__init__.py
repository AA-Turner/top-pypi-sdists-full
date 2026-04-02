r'''
# `google_contact_center_insights_analysis_rule`

Refer to the Terraform Registry for docs: [`google_contact_center_insights_analysis_rule`](https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule).
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


class GoogleContactCenterInsightsAnalysisRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContactCenterInsightsAnalysisRule.GoogleContactCenterInsightsAnalysisRule",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule google_contact_center_insights_analysis_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        analysis_percentage: typing.Optional[jsii.Number] = None,
        annotator_selector: typing.Optional[typing.Union["GoogleContactCenterInsightsAnalysisRuleAnnotatorSelector", typing.Dict[builtins.str, typing.Any]]] = None,
        conversation_filter: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleContactCenterInsightsAnalysisRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule google_contact_center_insights_analysis_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Location of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#location GoogleContactCenterInsightsAnalysisRule#location}
        :param active: If true, apply this rule to conversations. Otherwise, this rule is inactive and saved as a draft. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#active GoogleContactCenterInsightsAnalysisRule#active}
        :param analysis_percentage: Percentage of conversations that we should apply this analysis setting automatically, between [0, 1]. For example, 0.1 means 10%. Conversations are sampled in a determenestic way. The original runtime_percentage & upload percentage will be replaced by defining filters on the conversation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#analysis_percentage GoogleContactCenterInsightsAnalysisRule#analysis_percentage}
        :param annotator_selector: annotator_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#annotator_selector GoogleContactCenterInsightsAnalysisRule#annotator_selector}
        :param conversation_filter: Filter for the conversations that should apply this analysis rule. An empty filter means this analysis rule applies to all conversations. Refer to https://cloud.google.com/contact-center/insights/docs/filtering for details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#conversation_filter GoogleContactCenterInsightsAnalysisRule#conversation_filter}
        :param display_name: Display Name of the analysis rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#display_name GoogleContactCenterInsightsAnalysisRule#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#id GoogleContactCenterInsightsAnalysisRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#project GoogleContactCenterInsightsAnalysisRule#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#timeouts GoogleContactCenterInsightsAnalysisRule#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13f55f48dee705516744b584c01db4fee3030660353a244d85a0a2fd3f8235cc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleContactCenterInsightsAnalysisRuleConfig(
            location=location,
            active=active,
            analysis_percentage=analysis_percentage,
            annotator_selector=annotator_selector,
            conversation_filter=conversation_filter,
            display_name=display_name,
            id=id,
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
        '''Generates CDKTF code for importing a GoogleContactCenterInsightsAnalysisRule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleContactCenterInsightsAnalysisRule to import.
        :param import_from_id: The id of the existing GoogleContactCenterInsightsAnalysisRule that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleContactCenterInsightsAnalysisRule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6867becc3d38b5ecc77799f9447c766eeee3e7fb622fdf99a1c005bfd5725202)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAnnotatorSelector")
    def put_annotator_selector(
        self,
        *,
        issue_models: typing.Optional[typing.Sequence[builtins.str]] = None,
        phrase_matchers: typing.Optional[typing.Sequence[builtins.str]] = None,
        qa_config: typing.Optional[typing.Union["GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        run_entity_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run_intent_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run_interruption_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run_issue_model_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run_phrase_matcher_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run_qa_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run_sentiment_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run_silence_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run_summarization_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        summarization_config: typing.Optional[typing.Union["GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param issue_models: The issue model to run. If not provided, the most recently deployed topic model will be used. The provided issue model will only be used for inference if the issue model is deployed and if run_issue_model_annotator is set to true. If more than one issue model is provided, only the first provided issue model will be used for inference. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#issue_models GoogleContactCenterInsightsAnalysisRule#issue_models}
        :param phrase_matchers: The list of phrase matchers to run. If not provided, all active phrase matchers will be used. If inactive phrase matchers are provided, they will not be used. Phrase matchers will be run only if run_phrase_matcher_annotator is set to true. Format: projects/{project}/locations/{location}/phraseMatchers/{phrase_matcher} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#phrase_matchers GoogleContactCenterInsightsAnalysisRule#phrase_matchers}
        :param qa_config: qa_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#qa_config GoogleContactCenterInsightsAnalysisRule#qa_config}
        :param run_entity_annotator: Whether to run the entity annotator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#run_entity_annotator GoogleContactCenterInsightsAnalysisRule#run_entity_annotator}
        :param run_intent_annotator: Whether to run the intent annotator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#run_intent_annotator GoogleContactCenterInsightsAnalysisRule#run_intent_annotator}
        :param run_interruption_annotator: Whether to run the interruption annotator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#run_interruption_annotator GoogleContactCenterInsightsAnalysisRule#run_interruption_annotator}
        :param run_issue_model_annotator: Whether to run the issue model annotator. A model should have already been deployed for this to take effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#run_issue_model_annotator GoogleContactCenterInsightsAnalysisRule#run_issue_model_annotator}
        :param run_phrase_matcher_annotator: Whether to run the active phrase matcher annotator(s). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#run_phrase_matcher_annotator GoogleContactCenterInsightsAnalysisRule#run_phrase_matcher_annotator}
        :param run_qa_annotator: Whether to run the QA annotator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#run_qa_annotator GoogleContactCenterInsightsAnalysisRule#run_qa_annotator}
        :param run_sentiment_annotator: Whether to run the sentiment annotator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#run_sentiment_annotator GoogleContactCenterInsightsAnalysisRule#run_sentiment_annotator}
        :param run_silence_annotator: Whether to run the silence annotator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#run_silence_annotator GoogleContactCenterInsightsAnalysisRule#run_silence_annotator}
        :param run_summarization_annotator: Whether to run the summarization annotator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#run_summarization_annotator GoogleContactCenterInsightsAnalysisRule#run_summarization_annotator}
        :param summarization_config: summarization_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#summarization_config GoogleContactCenterInsightsAnalysisRule#summarization_config}
        '''
        value = GoogleContactCenterInsightsAnalysisRuleAnnotatorSelector(
            issue_models=issue_models,
            phrase_matchers=phrase_matchers,
            qa_config=qa_config,
            run_entity_annotator=run_entity_annotator,
            run_intent_annotator=run_intent_annotator,
            run_interruption_annotator=run_interruption_annotator,
            run_issue_model_annotator=run_issue_model_annotator,
            run_phrase_matcher_annotator=run_phrase_matcher_annotator,
            run_qa_annotator=run_qa_annotator,
            run_sentiment_annotator=run_sentiment_annotator,
            run_silence_annotator=run_silence_annotator,
            run_summarization_annotator=run_summarization_annotator,
            summarization_config=summarization_config,
        )

        return typing.cast(None, jsii.invoke(self, "putAnnotatorSelector", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#create GoogleContactCenterInsightsAnalysisRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#delete GoogleContactCenterInsightsAnalysisRule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#update GoogleContactCenterInsightsAnalysisRule#update}.
        '''
        value = GoogleContactCenterInsightsAnalysisRuleTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetActive")
    def reset_active(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActive", []))

    @jsii.member(jsii_name="resetAnalysisPercentage")
    def reset_analysis_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnalysisPercentage", []))

    @jsii.member(jsii_name="resetAnnotatorSelector")
    def reset_annotator_selector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotatorSelector", []))

    @jsii.member(jsii_name="resetConversationFilter")
    def reset_conversation_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConversationFilter", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="annotatorSelector")
    def annotator_selector(
        self,
    ) -> "GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorOutputReference":
        return typing.cast("GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorOutputReference", jsii.get(self, "annotatorSelector"))

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
    def timeouts(
        self,
    ) -> "GoogleContactCenterInsightsAnalysisRuleTimeoutsOutputReference":
        return typing.cast("GoogleContactCenterInsightsAnalysisRuleTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="activeInput")
    def active_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "activeInput"))

    @builtins.property
    @jsii.member(jsii_name="analysisPercentageInput")
    def analysis_percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "analysisPercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="annotatorSelectorInput")
    def annotator_selector_input(
        self,
    ) -> typing.Optional["GoogleContactCenterInsightsAnalysisRuleAnnotatorSelector"]:
        return typing.cast(typing.Optional["GoogleContactCenterInsightsAnalysisRuleAnnotatorSelector"], jsii.get(self, "annotatorSelectorInput"))

    @builtins.property
    @jsii.member(jsii_name="conversationFilterInput")
    def conversation_filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conversationFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleContactCenterInsightsAnalysisRuleTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleContactCenterInsightsAnalysisRuleTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="active")
    def active(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "active"))

    @active.setter
    def active(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dbc69829331f60c639e0ddd71de76dc1566eb71d5a1e4a659f35115bc0f503a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "active", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="analysisPercentage")
    def analysis_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "analysisPercentage"))

    @analysis_percentage.setter
    def analysis_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bbb7c00ef571b363bd804d8e15401f12f11516e21b24ca1776bdf88d11e31c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "analysisPercentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="conversationFilter")
    def conversation_filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "conversationFilter"))

    @conversation_filter.setter
    def conversation_filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7629d5313fb845c6edc348a7beaa02331c34741cc5f3e98b5eefa0cc000807c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "conversationFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21f3aabede791aa3f9f3ba8297cc255e0661ff66ef3ab5c170e9e53c44ac4323)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4345285f8b724b7e1f1401ee3afa0a2edbf8b7f2820b4f4246e7086e718bd51f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a52ebb7667eb8b3385b2e108fb79f730a138a25d35f01637d4bc559bc631c93d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdf4d21cf25de11c53c952383f52b6a2109497745e0f09787297f04375814b1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContactCenterInsightsAnalysisRule.GoogleContactCenterInsightsAnalysisRuleAnnotatorSelector",
    jsii_struct_bases=[],
    name_mapping={
        "issue_models": "issueModels",
        "phrase_matchers": "phraseMatchers",
        "qa_config": "qaConfig",
        "run_entity_annotator": "runEntityAnnotator",
        "run_intent_annotator": "runIntentAnnotator",
        "run_interruption_annotator": "runInterruptionAnnotator",
        "run_issue_model_annotator": "runIssueModelAnnotator",
        "run_phrase_matcher_annotator": "runPhraseMatcherAnnotator",
        "run_qa_annotator": "runQaAnnotator",
        "run_sentiment_annotator": "runSentimentAnnotator",
        "run_silence_annotator": "runSilenceAnnotator",
        "run_summarization_annotator": "runSummarizationAnnotator",
        "summarization_config": "summarizationConfig",
    },
)
class GoogleContactCenterInsightsAnalysisRuleAnnotatorSelector:
    def __init__(
        self,
        *,
        issue_models: typing.Optional[typing.Sequence[builtins.str]] = None,
        phrase_matchers: typing.Optional[typing.Sequence[builtins.str]] = None,
        qa_config: typing.Optional[typing.Union["GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        run_entity_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run_intent_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run_interruption_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run_issue_model_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run_phrase_matcher_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run_qa_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run_sentiment_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run_silence_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run_summarization_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        summarization_config: typing.Optional[typing.Union["GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param issue_models: The issue model to run. If not provided, the most recently deployed topic model will be used. The provided issue model will only be used for inference if the issue model is deployed and if run_issue_model_annotator is set to true. If more than one issue model is provided, only the first provided issue model will be used for inference. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#issue_models GoogleContactCenterInsightsAnalysisRule#issue_models}
        :param phrase_matchers: The list of phrase matchers to run. If not provided, all active phrase matchers will be used. If inactive phrase matchers are provided, they will not be used. Phrase matchers will be run only if run_phrase_matcher_annotator is set to true. Format: projects/{project}/locations/{location}/phraseMatchers/{phrase_matcher} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#phrase_matchers GoogleContactCenterInsightsAnalysisRule#phrase_matchers}
        :param qa_config: qa_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#qa_config GoogleContactCenterInsightsAnalysisRule#qa_config}
        :param run_entity_annotator: Whether to run the entity annotator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#run_entity_annotator GoogleContactCenterInsightsAnalysisRule#run_entity_annotator}
        :param run_intent_annotator: Whether to run the intent annotator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#run_intent_annotator GoogleContactCenterInsightsAnalysisRule#run_intent_annotator}
        :param run_interruption_annotator: Whether to run the interruption annotator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#run_interruption_annotator GoogleContactCenterInsightsAnalysisRule#run_interruption_annotator}
        :param run_issue_model_annotator: Whether to run the issue model annotator. A model should have already been deployed for this to take effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#run_issue_model_annotator GoogleContactCenterInsightsAnalysisRule#run_issue_model_annotator}
        :param run_phrase_matcher_annotator: Whether to run the active phrase matcher annotator(s). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#run_phrase_matcher_annotator GoogleContactCenterInsightsAnalysisRule#run_phrase_matcher_annotator}
        :param run_qa_annotator: Whether to run the QA annotator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#run_qa_annotator GoogleContactCenterInsightsAnalysisRule#run_qa_annotator}
        :param run_sentiment_annotator: Whether to run the sentiment annotator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#run_sentiment_annotator GoogleContactCenterInsightsAnalysisRule#run_sentiment_annotator}
        :param run_silence_annotator: Whether to run the silence annotator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#run_silence_annotator GoogleContactCenterInsightsAnalysisRule#run_silence_annotator}
        :param run_summarization_annotator: Whether to run the summarization annotator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#run_summarization_annotator GoogleContactCenterInsightsAnalysisRule#run_summarization_annotator}
        :param summarization_config: summarization_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#summarization_config GoogleContactCenterInsightsAnalysisRule#summarization_config}
        '''
        if isinstance(qa_config, dict):
            qa_config = GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfig(**qa_config)
        if isinstance(summarization_config, dict):
            summarization_config = GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfig(**summarization_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ec4ed87c9e262d3eee1c10ccf50a5ac2e79a6a00de18e5d87053400ea2db845)
            check_type(argname="argument issue_models", value=issue_models, expected_type=type_hints["issue_models"])
            check_type(argname="argument phrase_matchers", value=phrase_matchers, expected_type=type_hints["phrase_matchers"])
            check_type(argname="argument qa_config", value=qa_config, expected_type=type_hints["qa_config"])
            check_type(argname="argument run_entity_annotator", value=run_entity_annotator, expected_type=type_hints["run_entity_annotator"])
            check_type(argname="argument run_intent_annotator", value=run_intent_annotator, expected_type=type_hints["run_intent_annotator"])
            check_type(argname="argument run_interruption_annotator", value=run_interruption_annotator, expected_type=type_hints["run_interruption_annotator"])
            check_type(argname="argument run_issue_model_annotator", value=run_issue_model_annotator, expected_type=type_hints["run_issue_model_annotator"])
            check_type(argname="argument run_phrase_matcher_annotator", value=run_phrase_matcher_annotator, expected_type=type_hints["run_phrase_matcher_annotator"])
            check_type(argname="argument run_qa_annotator", value=run_qa_annotator, expected_type=type_hints["run_qa_annotator"])
            check_type(argname="argument run_sentiment_annotator", value=run_sentiment_annotator, expected_type=type_hints["run_sentiment_annotator"])
            check_type(argname="argument run_silence_annotator", value=run_silence_annotator, expected_type=type_hints["run_silence_annotator"])
            check_type(argname="argument run_summarization_annotator", value=run_summarization_annotator, expected_type=type_hints["run_summarization_annotator"])
            check_type(argname="argument summarization_config", value=summarization_config, expected_type=type_hints["summarization_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if issue_models is not None:
            self._values["issue_models"] = issue_models
        if phrase_matchers is not None:
            self._values["phrase_matchers"] = phrase_matchers
        if qa_config is not None:
            self._values["qa_config"] = qa_config
        if run_entity_annotator is not None:
            self._values["run_entity_annotator"] = run_entity_annotator
        if run_intent_annotator is not None:
            self._values["run_intent_annotator"] = run_intent_annotator
        if run_interruption_annotator is not None:
            self._values["run_interruption_annotator"] = run_interruption_annotator
        if run_issue_model_annotator is not None:
            self._values["run_issue_model_annotator"] = run_issue_model_annotator
        if run_phrase_matcher_annotator is not None:
            self._values["run_phrase_matcher_annotator"] = run_phrase_matcher_annotator
        if run_qa_annotator is not None:
            self._values["run_qa_annotator"] = run_qa_annotator
        if run_sentiment_annotator is not None:
            self._values["run_sentiment_annotator"] = run_sentiment_annotator
        if run_silence_annotator is not None:
            self._values["run_silence_annotator"] = run_silence_annotator
        if run_summarization_annotator is not None:
            self._values["run_summarization_annotator"] = run_summarization_annotator
        if summarization_config is not None:
            self._values["summarization_config"] = summarization_config

    @builtins.property
    def issue_models(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The issue model to run.

        If not provided, the most recently deployed topic
        model will be used. The provided issue model will only be used for
        inference if the issue model is deployed and if run_issue_model_annotator
        is set to true. If more than one issue model is provided, only the first
        provided issue model will be used for inference.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#issue_models GoogleContactCenterInsightsAnalysisRule#issue_models}
        '''
        result = self._values.get("issue_models")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def phrase_matchers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of phrase matchers to run.

        If not provided, all active phrase
        matchers will be used. If inactive phrase matchers are provided, they will
        not be used. Phrase matchers will be run only if
        run_phrase_matcher_annotator is set to true. Format:
        projects/{project}/locations/{location}/phraseMatchers/{phrase_matcher}

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#phrase_matchers GoogleContactCenterInsightsAnalysisRule#phrase_matchers}
        '''
        result = self._values.get("phrase_matchers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def qa_config(
        self,
    ) -> typing.Optional["GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfig"]:
        '''qa_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#qa_config GoogleContactCenterInsightsAnalysisRule#qa_config}
        '''
        result = self._values.get("qa_config")
        return typing.cast(typing.Optional["GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfig"], result)

    @builtins.property
    def run_entity_annotator(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to run the entity annotator.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#run_entity_annotator GoogleContactCenterInsightsAnalysisRule#run_entity_annotator}
        '''
        result = self._values.get("run_entity_annotator")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def run_intent_annotator(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to run the intent annotator.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#run_intent_annotator GoogleContactCenterInsightsAnalysisRule#run_intent_annotator}
        '''
        result = self._values.get("run_intent_annotator")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def run_interruption_annotator(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to run the interruption annotator.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#run_interruption_annotator GoogleContactCenterInsightsAnalysisRule#run_interruption_annotator}
        '''
        result = self._values.get("run_interruption_annotator")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def run_issue_model_annotator(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to run the issue model annotator. A model should have already been deployed for this to take effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#run_issue_model_annotator GoogleContactCenterInsightsAnalysisRule#run_issue_model_annotator}
        '''
        result = self._values.get("run_issue_model_annotator")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def run_phrase_matcher_annotator(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to run the active phrase matcher annotator(s).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#run_phrase_matcher_annotator GoogleContactCenterInsightsAnalysisRule#run_phrase_matcher_annotator}
        '''
        result = self._values.get("run_phrase_matcher_annotator")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def run_qa_annotator(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to run the QA annotator.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#run_qa_annotator GoogleContactCenterInsightsAnalysisRule#run_qa_annotator}
        '''
        result = self._values.get("run_qa_annotator")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def run_sentiment_annotator(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to run the sentiment annotator.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#run_sentiment_annotator GoogleContactCenterInsightsAnalysisRule#run_sentiment_annotator}
        '''
        result = self._values.get("run_sentiment_annotator")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def run_silence_annotator(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to run the silence annotator.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#run_silence_annotator GoogleContactCenterInsightsAnalysisRule#run_silence_annotator}
        '''
        result = self._values.get("run_silence_annotator")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def run_summarization_annotator(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to run the summarization annotator.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#run_summarization_annotator GoogleContactCenterInsightsAnalysisRule#run_summarization_annotator}
        '''
        result = self._values.get("run_summarization_annotator")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def summarization_config(
        self,
    ) -> typing.Optional["GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfig"]:
        '''summarization_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#summarization_config GoogleContactCenterInsightsAnalysisRule#summarization_config}
        '''
        result = self._values.get("summarization_config")
        return typing.cast(typing.Optional["GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContactCenterInsightsAnalysisRuleAnnotatorSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContactCenterInsightsAnalysisRule.GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4359c97a947cdd3ec37a674c2e04d512d59cfc6865a6e59ec5d3bf18ee36ff46)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putQaConfig")
    def put_qa_config(
        self,
        *,
        scorecard_list: typing.Optional[typing.Union["GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStruct", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scorecard_list: scorecard_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#scorecard_list GoogleContactCenterInsightsAnalysisRule#scorecard_list}
        '''
        value = GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfig(
            scorecard_list=scorecard_list
        )

        return typing.cast(None, jsii.invoke(self, "putQaConfig", [value]))

    @jsii.member(jsii_name="putSummarizationConfig")
    def put_summarization_config(
        self,
        *,
        conversation_profile: typing.Optional[builtins.str] = None,
        summarization_model: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param conversation_profile: Resource name of the Dialogflow conversation profile. Format: projects/{project}/locations/{location}/conversationProfiles/{conversation_profile}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#conversation_profile GoogleContactCenterInsightsAnalysisRule#conversation_profile}
        :param summarization_model: Default summarization model to be used. Possible values: SUMMARIZATION_MODEL_UNSPECIFIED BASELINE_MODEL BASELINE_MODEL_V2_0 Possible values: ["BASELINE_MODEL", "BASELINE_MODEL_V2_0"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#summarization_model GoogleContactCenterInsightsAnalysisRule#summarization_model}
        '''
        value = GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfig(
            conversation_profile=conversation_profile,
            summarization_model=summarization_model,
        )

        return typing.cast(None, jsii.invoke(self, "putSummarizationConfig", [value]))

    @jsii.member(jsii_name="resetIssueModels")
    def reset_issue_models(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIssueModels", []))

    @jsii.member(jsii_name="resetPhraseMatchers")
    def reset_phrase_matchers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPhraseMatchers", []))

    @jsii.member(jsii_name="resetQaConfig")
    def reset_qa_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQaConfig", []))

    @jsii.member(jsii_name="resetRunEntityAnnotator")
    def reset_run_entity_annotator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRunEntityAnnotator", []))

    @jsii.member(jsii_name="resetRunIntentAnnotator")
    def reset_run_intent_annotator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRunIntentAnnotator", []))

    @jsii.member(jsii_name="resetRunInterruptionAnnotator")
    def reset_run_interruption_annotator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRunInterruptionAnnotator", []))

    @jsii.member(jsii_name="resetRunIssueModelAnnotator")
    def reset_run_issue_model_annotator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRunIssueModelAnnotator", []))

    @jsii.member(jsii_name="resetRunPhraseMatcherAnnotator")
    def reset_run_phrase_matcher_annotator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRunPhraseMatcherAnnotator", []))

    @jsii.member(jsii_name="resetRunQaAnnotator")
    def reset_run_qa_annotator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRunQaAnnotator", []))

    @jsii.member(jsii_name="resetRunSentimentAnnotator")
    def reset_run_sentiment_annotator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRunSentimentAnnotator", []))

    @jsii.member(jsii_name="resetRunSilenceAnnotator")
    def reset_run_silence_annotator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRunSilenceAnnotator", []))

    @jsii.member(jsii_name="resetRunSummarizationAnnotator")
    def reset_run_summarization_annotator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRunSummarizationAnnotator", []))

    @jsii.member(jsii_name="resetSummarizationConfig")
    def reset_summarization_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSummarizationConfig", []))

    @builtins.property
    @jsii.member(jsii_name="qaConfig")
    def qa_config(
        self,
    ) -> "GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigOutputReference":
        return typing.cast("GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigOutputReference", jsii.get(self, "qaConfig"))

    @builtins.property
    @jsii.member(jsii_name="summarizationConfig")
    def summarization_config(
        self,
    ) -> "GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfigOutputReference":
        return typing.cast("GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfigOutputReference", jsii.get(self, "summarizationConfig"))

    @builtins.property
    @jsii.member(jsii_name="issueModelsInput")
    def issue_models_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "issueModelsInput"))

    @builtins.property
    @jsii.member(jsii_name="phraseMatchersInput")
    def phrase_matchers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "phraseMatchersInput"))

    @builtins.property
    @jsii.member(jsii_name="qaConfigInput")
    def qa_config_input(
        self,
    ) -> typing.Optional["GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfig"]:
        return typing.cast(typing.Optional["GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfig"], jsii.get(self, "qaConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="runEntityAnnotatorInput")
    def run_entity_annotator_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "runEntityAnnotatorInput"))

    @builtins.property
    @jsii.member(jsii_name="runIntentAnnotatorInput")
    def run_intent_annotator_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "runIntentAnnotatorInput"))

    @builtins.property
    @jsii.member(jsii_name="runInterruptionAnnotatorInput")
    def run_interruption_annotator_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "runInterruptionAnnotatorInput"))

    @builtins.property
    @jsii.member(jsii_name="runIssueModelAnnotatorInput")
    def run_issue_model_annotator_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "runIssueModelAnnotatorInput"))

    @builtins.property
    @jsii.member(jsii_name="runPhraseMatcherAnnotatorInput")
    def run_phrase_matcher_annotator_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "runPhraseMatcherAnnotatorInput"))

    @builtins.property
    @jsii.member(jsii_name="runQaAnnotatorInput")
    def run_qa_annotator_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "runQaAnnotatorInput"))

    @builtins.property
    @jsii.member(jsii_name="runSentimentAnnotatorInput")
    def run_sentiment_annotator_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "runSentimentAnnotatorInput"))

    @builtins.property
    @jsii.member(jsii_name="runSilenceAnnotatorInput")
    def run_silence_annotator_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "runSilenceAnnotatorInput"))

    @builtins.property
    @jsii.member(jsii_name="runSummarizationAnnotatorInput")
    def run_summarization_annotator_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "runSummarizationAnnotatorInput"))

    @builtins.property
    @jsii.member(jsii_name="summarizationConfigInput")
    def summarization_config_input(
        self,
    ) -> typing.Optional["GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfig"]:
        return typing.cast(typing.Optional["GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfig"], jsii.get(self, "summarizationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="issueModels")
    def issue_models(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "issueModels"))

    @issue_models.setter
    def issue_models(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23405bedeb7088c4edb4b49d34a49abfdf3e0684890caab29415c242c6d92805)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issueModels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="phraseMatchers")
    def phrase_matchers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "phraseMatchers"))

    @phrase_matchers.setter
    def phrase_matchers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e740f61013d4b8514f78b6aed045affe99c4a17ffb83ee537741a76781603282)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "phraseMatchers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runEntityAnnotator")
    def run_entity_annotator(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "runEntityAnnotator"))

    @run_entity_annotator.setter
    def run_entity_annotator(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8c64d49d854b46190fcd866edc91dbe9492af49a0a818103d1f2f58edbf6301)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runEntityAnnotator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runIntentAnnotator")
    def run_intent_annotator(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "runIntentAnnotator"))

    @run_intent_annotator.setter
    def run_intent_annotator(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c52e135e51b23cef97418092b6924e61e48c705a5e58fba3275ccc4f1618ed2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runIntentAnnotator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runInterruptionAnnotator")
    def run_interruption_annotator(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "runInterruptionAnnotator"))

    @run_interruption_annotator.setter
    def run_interruption_annotator(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac44ac4aead16c7b96c3a28f7b26b2c3a44a00b8864c869f9101a3f67cc14923)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runInterruptionAnnotator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runIssueModelAnnotator")
    def run_issue_model_annotator(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "runIssueModelAnnotator"))

    @run_issue_model_annotator.setter
    def run_issue_model_annotator(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94a94de08f3410271472435d3150da12f40354c98a246764dbf2f06b4de01e7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runIssueModelAnnotator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runPhraseMatcherAnnotator")
    def run_phrase_matcher_annotator(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "runPhraseMatcherAnnotator"))

    @run_phrase_matcher_annotator.setter
    def run_phrase_matcher_annotator(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec9ae53d41c4b6339f26ea84180bddf93de716ea79ce08de2fad166546c37ccd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runPhraseMatcherAnnotator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runQaAnnotator")
    def run_qa_annotator(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "runQaAnnotator"))

    @run_qa_annotator.setter
    def run_qa_annotator(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66bd57f7002f4ef3741a017c2e56558ea22dea79db92f3e99d3245f57a02ff53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runQaAnnotator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runSentimentAnnotator")
    def run_sentiment_annotator(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "runSentimentAnnotator"))

    @run_sentiment_annotator.setter
    def run_sentiment_annotator(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc9473b0bcd7b0e77c987c2c91e143f5a9aea2f6362bd443f281831ef00c90bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runSentimentAnnotator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runSilenceAnnotator")
    def run_silence_annotator(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "runSilenceAnnotator"))

    @run_silence_annotator.setter
    def run_silence_annotator(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df2fbb048698454712eae6a77020d124e256666bd54d0eee0175de08078c2e5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runSilenceAnnotator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runSummarizationAnnotator")
    def run_summarization_annotator(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "runSummarizationAnnotator"))

    @run_summarization_annotator.setter
    def run_summarization_annotator(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec861ef4749590e14abf7dc3470871db44b41a852c675a2d260384f2a4b4d64d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runSummarizationAnnotator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContactCenterInsightsAnalysisRuleAnnotatorSelector]:
        return typing.cast(typing.Optional[GoogleContactCenterInsightsAnalysisRuleAnnotatorSelector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContactCenterInsightsAnalysisRuleAnnotatorSelector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dedf6378972d2b006a0e93ca0df8dee3148da09475c628db5f59f8c50b258f70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContactCenterInsightsAnalysisRule.GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfig",
    jsii_struct_bases=[],
    name_mapping={"scorecard_list": "scorecardList"},
)
class GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfig:
    def __init__(
        self,
        *,
        scorecard_list: typing.Optional[typing.Union["GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStruct", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scorecard_list: scorecard_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#scorecard_list GoogleContactCenterInsightsAnalysisRule#scorecard_list}
        '''
        if isinstance(scorecard_list, dict):
            scorecard_list = GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStruct(**scorecard_list)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__568d3b75d7485d3dfa30cb126007158b0039b8104c00345331c89852eea55099)
            check_type(argname="argument scorecard_list", value=scorecard_list, expected_type=type_hints["scorecard_list"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if scorecard_list is not None:
            self._values["scorecard_list"] = scorecard_list

    @builtins.property
    def scorecard_list(
        self,
    ) -> typing.Optional["GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStruct"]:
        '''scorecard_list block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#scorecard_list GoogleContactCenterInsightsAnalysisRule#scorecard_list}
        '''
        result = self._values.get("scorecard_list")
        return typing.cast(typing.Optional["GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStruct"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContactCenterInsightsAnalysisRule.GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33d4d98ce6fd8b17ecef67c0c1d98ea6733769f471d2ad95b2bbe68c31a05ff9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putScorecardList")
    def put_scorecard_list(
        self,
        *,
        qa_scorecard_revisions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param qa_scorecard_revisions: List of QaScorecardRevisions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#qa_scorecard_revisions GoogleContactCenterInsightsAnalysisRule#qa_scorecard_revisions}
        '''
        value = GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStruct(
            qa_scorecard_revisions=qa_scorecard_revisions
        )

        return typing.cast(None, jsii.invoke(self, "putScorecardList", [value]))

    @jsii.member(jsii_name="resetScorecardList")
    def reset_scorecard_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScorecardList", []))

    @builtins.property
    @jsii.member(jsii_name="scorecardList")
    def scorecard_list(
        self,
    ) -> "GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStructOutputReference":
        return typing.cast("GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStructOutputReference", jsii.get(self, "scorecardList"))

    @builtins.property
    @jsii.member(jsii_name="scorecardListInput")
    def scorecard_list_input(
        self,
    ) -> typing.Optional["GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStruct"]:
        return typing.cast(typing.Optional["GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStruct"], jsii.get(self, "scorecardListInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfig]:
        return typing.cast(typing.Optional[GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b12f7a880becac808afbd87096e9f823ef72fb3a5497d6f77d1b110fd7615627)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContactCenterInsightsAnalysisRule.GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStruct",
    jsii_struct_bases=[],
    name_mapping={"qa_scorecard_revisions": "qaScorecardRevisions"},
)
class GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStruct:
    def __init__(
        self,
        *,
        qa_scorecard_revisions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param qa_scorecard_revisions: List of QaScorecardRevisions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#qa_scorecard_revisions GoogleContactCenterInsightsAnalysisRule#qa_scorecard_revisions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee3231ef5485296673f969494086a3568aa9e7a86b82bbec648bd65deb16f312)
            check_type(argname="argument qa_scorecard_revisions", value=qa_scorecard_revisions, expected_type=type_hints["qa_scorecard_revisions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if qa_scorecard_revisions is not None:
            self._values["qa_scorecard_revisions"] = qa_scorecard_revisions

    @builtins.property
    def qa_scorecard_revisions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of QaScorecardRevisions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#qa_scorecard_revisions GoogleContactCenterInsightsAnalysisRule#qa_scorecard_revisions}
        '''
        result = self._values.get("qa_scorecard_revisions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContactCenterInsightsAnalysisRule.GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9d6c058c45a23d11f7967074791a4597dc5a74e30f2727f9c02386241d7e48f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetQaScorecardRevisions")
    def reset_qa_scorecard_revisions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQaScorecardRevisions", []))

    @builtins.property
    @jsii.member(jsii_name="qaScorecardRevisionsInput")
    def qa_scorecard_revisions_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "qaScorecardRevisionsInput"))

    @builtins.property
    @jsii.member(jsii_name="qaScorecardRevisions")
    def qa_scorecard_revisions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "qaScorecardRevisions"))

    @qa_scorecard_revisions.setter
    def qa_scorecard_revisions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afbbbf75706bb810130db1e1d9996dc2c5c7672ffdbd1f157e747740ad00fe50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "qaScorecardRevisions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStruct]:
        return typing.cast(typing.Optional[GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b80c5d6922bbaf0b169ff3f3698ed95828dfe70e8e8b89348e0614b993e30ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContactCenterInsightsAnalysisRule.GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "conversation_profile": "conversationProfile",
        "summarization_model": "summarizationModel",
    },
)
class GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfig:
    def __init__(
        self,
        *,
        conversation_profile: typing.Optional[builtins.str] = None,
        summarization_model: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param conversation_profile: Resource name of the Dialogflow conversation profile. Format: projects/{project}/locations/{location}/conversationProfiles/{conversation_profile}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#conversation_profile GoogleContactCenterInsightsAnalysisRule#conversation_profile}
        :param summarization_model: Default summarization model to be used. Possible values: SUMMARIZATION_MODEL_UNSPECIFIED BASELINE_MODEL BASELINE_MODEL_V2_0 Possible values: ["BASELINE_MODEL", "BASELINE_MODEL_V2_0"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#summarization_model GoogleContactCenterInsightsAnalysisRule#summarization_model}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b72b4cffa18cd7503df32c0215486ee8f5f839d3d109ae174727f2087b3459a)
            check_type(argname="argument conversation_profile", value=conversation_profile, expected_type=type_hints["conversation_profile"])
            check_type(argname="argument summarization_model", value=summarization_model, expected_type=type_hints["summarization_model"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if conversation_profile is not None:
            self._values["conversation_profile"] = conversation_profile
        if summarization_model is not None:
            self._values["summarization_model"] = summarization_model

    @builtins.property
    def conversation_profile(self) -> typing.Optional[builtins.str]:
        '''Resource name of the Dialogflow conversation profile. Format: projects/{project}/locations/{location}/conversationProfiles/{conversation_profile}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#conversation_profile GoogleContactCenterInsightsAnalysisRule#conversation_profile}
        '''
        result = self._values.get("conversation_profile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def summarization_model(self) -> typing.Optional[builtins.str]:
        '''Default summarization model to be used. Possible values: SUMMARIZATION_MODEL_UNSPECIFIED BASELINE_MODEL BASELINE_MODEL_V2_0 Possible values: ["BASELINE_MODEL", "BASELINE_MODEL_V2_0"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#summarization_model GoogleContactCenterInsightsAnalysisRule#summarization_model}
        '''
        result = self._values.get("summarization_model")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContactCenterInsightsAnalysisRule.GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9fa42b643bffeb19472832a7c165af9cb3c0d8e4a71d7ca7f8ba82b2edc0e4b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetConversationProfile")
    def reset_conversation_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConversationProfile", []))

    @jsii.member(jsii_name="resetSummarizationModel")
    def reset_summarization_model(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSummarizationModel", []))

    @builtins.property
    @jsii.member(jsii_name="conversationProfileInput")
    def conversation_profile_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conversationProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="summarizationModelInput")
    def summarization_model_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "summarizationModelInput"))

    @builtins.property
    @jsii.member(jsii_name="conversationProfile")
    def conversation_profile(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "conversationProfile"))

    @conversation_profile.setter
    def conversation_profile(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b813f0b763d6e3682789e3d2e88b8c91a61c93c19fac4b00931736a79f1e751)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "conversationProfile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="summarizationModel")
    def summarization_model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "summarizationModel"))

    @summarization_model.setter
    def summarization_model(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af52cb9b0f99ac3a5abbb1628a953690db43a2834966fc35520fc37e66c5a24c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "summarizationModel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfig]:
        return typing.cast(typing.Optional[GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01db6204e677546e56e1f81af77327c8f343f0dc9571c2399509256c5ee49302)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContactCenterInsightsAnalysisRule.GoogleContactCenterInsightsAnalysisRuleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "active": "active",
        "analysis_percentage": "analysisPercentage",
        "annotator_selector": "annotatorSelector",
        "conversation_filter": "conversationFilter",
        "display_name": "displayName",
        "id": "id",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class GoogleContactCenterInsightsAnalysisRuleConfig(
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
        location: builtins.str,
        active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        analysis_percentage: typing.Optional[jsii.Number] = None,
        annotator_selector: typing.Optional[typing.Union[GoogleContactCenterInsightsAnalysisRuleAnnotatorSelector, typing.Dict[builtins.str, typing.Any]]] = None,
        conversation_filter: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleContactCenterInsightsAnalysisRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Location of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#location GoogleContactCenterInsightsAnalysisRule#location}
        :param active: If true, apply this rule to conversations. Otherwise, this rule is inactive and saved as a draft. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#active GoogleContactCenterInsightsAnalysisRule#active}
        :param analysis_percentage: Percentage of conversations that we should apply this analysis setting automatically, between [0, 1]. For example, 0.1 means 10%. Conversations are sampled in a determenestic way. The original runtime_percentage & upload percentage will be replaced by defining filters on the conversation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#analysis_percentage GoogleContactCenterInsightsAnalysisRule#analysis_percentage}
        :param annotator_selector: annotator_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#annotator_selector GoogleContactCenterInsightsAnalysisRule#annotator_selector}
        :param conversation_filter: Filter for the conversations that should apply this analysis rule. An empty filter means this analysis rule applies to all conversations. Refer to https://cloud.google.com/contact-center/insights/docs/filtering for details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#conversation_filter GoogleContactCenterInsightsAnalysisRule#conversation_filter}
        :param display_name: Display Name of the analysis rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#display_name GoogleContactCenterInsightsAnalysisRule#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#id GoogleContactCenterInsightsAnalysisRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#project GoogleContactCenterInsightsAnalysisRule#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#timeouts GoogleContactCenterInsightsAnalysisRule#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(annotator_selector, dict):
            annotator_selector = GoogleContactCenterInsightsAnalysisRuleAnnotatorSelector(**annotator_selector)
        if isinstance(timeouts, dict):
            timeouts = GoogleContactCenterInsightsAnalysisRuleTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__654cc55b72c7637c49a90b869cdd7dbd2939e56c09e0f4417d72998e059f3cc9)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument active", value=active, expected_type=type_hints["active"])
            check_type(argname="argument analysis_percentage", value=analysis_percentage, expected_type=type_hints["analysis_percentage"])
            check_type(argname="argument annotator_selector", value=annotator_selector, expected_type=type_hints["annotator_selector"])
            check_type(argname="argument conversation_filter", value=conversation_filter, expected_type=type_hints["conversation_filter"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if active is not None:
            self._values["active"] = active
        if analysis_percentage is not None:
            self._values["analysis_percentage"] = analysis_percentage
        if annotator_selector is not None:
            self._values["annotator_selector"] = annotator_selector
        if conversation_filter is not None:
            self._values["conversation_filter"] = conversation_filter
        if display_name is not None:
            self._values["display_name"] = display_name
        if id is not None:
            self._values["id"] = id
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
    def location(self) -> builtins.str:
        '''Location of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#location GoogleContactCenterInsightsAnalysisRule#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def active(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, apply this rule to conversations. Otherwise, this rule is inactive and saved as a draft.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#active GoogleContactCenterInsightsAnalysisRule#active}
        '''
        result = self._values.get("active")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def analysis_percentage(self) -> typing.Optional[jsii.Number]:
        '''Percentage of conversations that we should apply this analysis setting automatically, between [0, 1].

        For example, 0.1 means 10%. Conversations
        are sampled in a determenestic way. The original runtime_percentage &
        upload percentage will be replaced by defining filters on the conversation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#analysis_percentage GoogleContactCenterInsightsAnalysisRule#analysis_percentage}
        '''
        result = self._values.get("analysis_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def annotator_selector(
        self,
    ) -> typing.Optional[GoogleContactCenterInsightsAnalysisRuleAnnotatorSelector]:
        '''annotator_selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#annotator_selector GoogleContactCenterInsightsAnalysisRule#annotator_selector}
        '''
        result = self._values.get("annotator_selector")
        return typing.cast(typing.Optional[GoogleContactCenterInsightsAnalysisRuleAnnotatorSelector], result)

    @builtins.property
    def conversation_filter(self) -> typing.Optional[builtins.str]:
        '''Filter for the conversations that should apply this analysis rule.

        An empty filter means this analysis rule applies to all
        conversations.
        Refer to https://cloud.google.com/contact-center/insights/docs/filtering
        for details.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#conversation_filter GoogleContactCenterInsightsAnalysisRule#conversation_filter}
        '''
        result = self._values.get("conversation_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Display Name of the analysis rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#display_name GoogleContactCenterInsightsAnalysisRule#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#id GoogleContactCenterInsightsAnalysisRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#project GoogleContactCenterInsightsAnalysisRule#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleContactCenterInsightsAnalysisRuleTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#timeouts GoogleContactCenterInsightsAnalysisRule#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleContactCenterInsightsAnalysisRuleTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContactCenterInsightsAnalysisRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContactCenterInsightsAnalysisRule.GoogleContactCenterInsightsAnalysisRuleTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleContactCenterInsightsAnalysisRuleTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#create GoogleContactCenterInsightsAnalysisRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#delete GoogleContactCenterInsightsAnalysisRule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#update GoogleContactCenterInsightsAnalysisRule#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1196f242afe5c3c397baba28b7fc50a6f9f6b534a3da30e1c756a7e127e64c8)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#create GoogleContactCenterInsightsAnalysisRule#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#delete GoogleContactCenterInsightsAnalysisRule#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_contact_center_insights_analysis_rule#update GoogleContactCenterInsightsAnalysisRule#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContactCenterInsightsAnalysisRuleTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContactCenterInsightsAnalysisRuleTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContactCenterInsightsAnalysisRule.GoogleContactCenterInsightsAnalysisRuleTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d805c42071b39e7a46a1f6b75a38c6de786492a33bef90f9a71a5c0a470d696b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6af3c212ff2af5a493e55022afa39a189b347b50993878f4bc4ba1d0d33a2361)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f31bf511373799768bde1dba9121e1f831fd54f37a05820bdb9d40b21ba44ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fba071807457e096b61244b3c74f5e4786147623613e5182aca1c75525f3062b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContactCenterInsightsAnalysisRuleTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContactCenterInsightsAnalysisRuleTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContactCenterInsightsAnalysisRuleTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bdfeae4b6a10a41d80b954ad712ebcfa781ef4016f33ed402ebe8e60bf6bd05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleContactCenterInsightsAnalysisRule",
    "GoogleContactCenterInsightsAnalysisRuleAnnotatorSelector",
    "GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorOutputReference",
    "GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfig",
    "GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigOutputReference",
    "GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStruct",
    "GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStructOutputReference",
    "GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfig",
    "GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfigOutputReference",
    "GoogleContactCenterInsightsAnalysisRuleConfig",
    "GoogleContactCenterInsightsAnalysisRuleTimeouts",
    "GoogleContactCenterInsightsAnalysisRuleTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__13f55f48dee705516744b584c01db4fee3030660353a244d85a0a2fd3f8235cc(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    analysis_percentage: typing.Optional[jsii.Number] = None,
    annotator_selector: typing.Optional[typing.Union[GoogleContactCenterInsightsAnalysisRuleAnnotatorSelector, typing.Dict[builtins.str, typing.Any]]] = None,
    conversation_filter: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleContactCenterInsightsAnalysisRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__6867becc3d38b5ecc77799f9447c766eeee3e7fb622fdf99a1c005bfd5725202(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dbc69829331f60c639e0ddd71de76dc1566eb71d5a1e4a659f35115bc0f503a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bbb7c00ef571b363bd804d8e15401f12f11516e21b24ca1776bdf88d11e31c7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7629d5313fb845c6edc348a7beaa02331c34741cc5f3e98b5eefa0cc000807c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21f3aabede791aa3f9f3ba8297cc255e0661ff66ef3ab5c170e9e53c44ac4323(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4345285f8b724b7e1f1401ee3afa0a2edbf8b7f2820b4f4246e7086e718bd51f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a52ebb7667eb8b3385b2e108fb79f730a138a25d35f01637d4bc559bc631c93d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdf4d21cf25de11c53c952383f52b6a2109497745e0f09787297f04375814b1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ec4ed87c9e262d3eee1c10ccf50a5ac2e79a6a00de18e5d87053400ea2db845(
    *,
    issue_models: typing.Optional[typing.Sequence[builtins.str]] = None,
    phrase_matchers: typing.Optional[typing.Sequence[builtins.str]] = None,
    qa_config: typing.Optional[typing.Union[GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    run_entity_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    run_intent_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    run_interruption_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    run_issue_model_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    run_phrase_matcher_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    run_qa_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    run_sentiment_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    run_silence_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    run_summarization_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    summarization_config: typing.Optional[typing.Union[GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4359c97a947cdd3ec37a674c2e04d512d59cfc6865a6e59ec5d3bf18ee36ff46(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23405bedeb7088c4edb4b49d34a49abfdf3e0684890caab29415c242c6d92805(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e740f61013d4b8514f78b6aed045affe99c4a17ffb83ee537741a76781603282(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8c64d49d854b46190fcd866edc91dbe9492af49a0a818103d1f2f58edbf6301(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c52e135e51b23cef97418092b6924e61e48c705a5e58fba3275ccc4f1618ed2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac44ac4aead16c7b96c3a28f7b26b2c3a44a00b8864c869f9101a3f67cc14923(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94a94de08f3410271472435d3150da12f40354c98a246764dbf2f06b4de01e7e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec9ae53d41c4b6339f26ea84180bddf93de716ea79ce08de2fad166546c37ccd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66bd57f7002f4ef3741a017c2e56558ea22dea79db92f3e99d3245f57a02ff53(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc9473b0bcd7b0e77c987c2c91e143f5a9aea2f6362bd443f281831ef00c90bd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df2fbb048698454712eae6a77020d124e256666bd54d0eee0175de08078c2e5e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec861ef4749590e14abf7dc3470871db44b41a852c675a2d260384f2a4b4d64d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dedf6378972d2b006a0e93ca0df8dee3148da09475c628db5f59f8c50b258f70(
    value: typing.Optional[GoogleContactCenterInsightsAnalysisRuleAnnotatorSelector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__568d3b75d7485d3dfa30cb126007158b0039b8104c00345331c89852eea55099(
    *,
    scorecard_list: typing.Optional[typing.Union[GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33d4d98ce6fd8b17ecef67c0c1d98ea6733769f471d2ad95b2bbe68c31a05ff9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b12f7a880becac808afbd87096e9f823ef72fb3a5497d6f77d1b110fd7615627(
    value: typing.Optional[GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee3231ef5485296673f969494086a3568aa9e7a86b82bbec648bd65deb16f312(
    *,
    qa_scorecard_revisions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9d6c058c45a23d11f7967074791a4597dc5a74e30f2727f9c02386241d7e48f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afbbbf75706bb810130db1e1d9996dc2c5c7672ffdbd1f157e747740ad00fe50(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b80c5d6922bbaf0b169ff3f3698ed95828dfe70e8e8b89348e0614b993e30ba(
    value: typing.Optional[GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b72b4cffa18cd7503df32c0215486ee8f5f839d3d109ae174727f2087b3459a(
    *,
    conversation_profile: typing.Optional[builtins.str] = None,
    summarization_model: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9fa42b643bffeb19472832a7c165af9cb3c0d8e4a71d7ca7f8ba82b2edc0e4b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b813f0b763d6e3682789e3d2e88b8c91a61c93c19fac4b00931736a79f1e751(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af52cb9b0f99ac3a5abbb1628a953690db43a2834966fc35520fc37e66c5a24c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01db6204e677546e56e1f81af77327c8f343f0dc9571c2399509256c5ee49302(
    value: typing.Optional[GoogleContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__654cc55b72c7637c49a90b869cdd7dbd2939e56c09e0f4417d72998e059f3cc9(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    analysis_percentage: typing.Optional[jsii.Number] = None,
    annotator_selector: typing.Optional[typing.Union[GoogleContactCenterInsightsAnalysisRuleAnnotatorSelector, typing.Dict[builtins.str, typing.Any]]] = None,
    conversation_filter: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleContactCenterInsightsAnalysisRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1196f242afe5c3c397baba28b7fc50a6f9f6b534a3da30e1c756a7e127e64c8(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d805c42071b39e7a46a1f6b75a38c6de786492a33bef90f9a71a5c0a470d696b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6af3c212ff2af5a493e55022afa39a189b347b50993878f4bc4ba1d0d33a2361(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f31bf511373799768bde1dba9121e1f831fd54f37a05820bdb9d40b21ba44ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fba071807457e096b61244b3c74f5e4786147623613e5182aca1c75525f3062b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bdfeae4b6a10a41d80b954ad712ebcfa781ef4016f33ed402ebe8e60bf6bd05(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContactCenterInsightsAnalysisRuleTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
