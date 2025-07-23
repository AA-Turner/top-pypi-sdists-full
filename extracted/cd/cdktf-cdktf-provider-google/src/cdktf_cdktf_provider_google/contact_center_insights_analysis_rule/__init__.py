r'''
# `google_contact_center_insights_analysis_rule`

Refer to the Terraform Registry for docs: [`google_contact_center_insights_analysis_rule`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule).
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


class ContactCenterInsightsAnalysisRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.contactCenterInsightsAnalysisRule.ContactCenterInsightsAnalysisRule",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule google_contact_center_insights_analysis_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        analysis_percentage: typing.Optional[jsii.Number] = None,
        annotator_selector: typing.Optional[typing.Union["ContactCenterInsightsAnalysisRuleAnnotatorSelector", typing.Dict[builtins.str, typing.Any]]] = None,
        conversation_filter: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ContactCenterInsightsAnalysisRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule google_contact_center_insights_analysis_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Location of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#location ContactCenterInsightsAnalysisRule#location}
        :param active: If true, apply this rule to conversations. Otherwise, this rule is inactive and saved as a draft. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#active ContactCenterInsightsAnalysisRule#active}
        :param analysis_percentage: Percentage of conversations that we should apply this analysis setting automatically, between [0, 1]. For example, 0.1 means 10%. Conversations are sampled in a determenestic way. The original runtime_percentage & upload percentage will be replaced by defining filters on the conversation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#analysis_percentage ContactCenterInsightsAnalysisRule#analysis_percentage}
        :param annotator_selector: annotator_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#annotator_selector ContactCenterInsightsAnalysisRule#annotator_selector}
        :param conversation_filter: Filter for the conversations that should apply this analysis rule. An empty filter means this analysis rule applies to all conversations. Refer to https://cloud.google.com/contact-center/insights/docs/filtering for details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#conversation_filter ContactCenterInsightsAnalysisRule#conversation_filter}
        :param display_name: Display Name of the analysis rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#display_name ContactCenterInsightsAnalysisRule#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#id ContactCenterInsightsAnalysisRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#project ContactCenterInsightsAnalysisRule#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#timeouts ContactCenterInsightsAnalysisRule#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3772ea7feb7a7cf7cd93a29f0077f86ca88ff9d62602469ea047a45baab6ce9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ContactCenterInsightsAnalysisRuleConfig(
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
        '''Generates CDKTF code for importing a ContactCenterInsightsAnalysisRule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ContactCenterInsightsAnalysisRule to import.
        :param import_from_id: The id of the existing ContactCenterInsightsAnalysisRule that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ContactCenterInsightsAnalysisRule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__434804b17ef9cb7be369c42caeccc8e3672a8873b4ed1fbd53f73a38e873fbe3)
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
        qa_config: typing.Optional[typing.Union["ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        run_entity_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run_intent_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run_interruption_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run_issue_model_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run_phrase_matcher_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run_qa_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run_sentiment_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run_silence_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run_summarization_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        summarization_config: typing.Optional[typing.Union["ContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param issue_models: The issue model to run. If not provided, the most recently deployed topic model will be used. The provided issue model will only be used for inference if the issue model is deployed and if run_issue_model_annotator is set to true. If more than one issue model is provided, only the first provided issue model will be used for inference. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#issue_models ContactCenterInsightsAnalysisRule#issue_models}
        :param phrase_matchers: The list of phrase matchers to run. If not provided, all active phrase matchers will be used. If inactive phrase matchers are provided, they will not be used. Phrase matchers will be run only if run_phrase_matcher_annotator is set to true. Format: projects/{project}/locations/{location}/phraseMatchers/{phrase_matcher} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#phrase_matchers ContactCenterInsightsAnalysisRule#phrase_matchers}
        :param qa_config: qa_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#qa_config ContactCenterInsightsAnalysisRule#qa_config}
        :param run_entity_annotator: Whether to run the entity annotator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#run_entity_annotator ContactCenterInsightsAnalysisRule#run_entity_annotator}
        :param run_intent_annotator: Whether to run the intent annotator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#run_intent_annotator ContactCenterInsightsAnalysisRule#run_intent_annotator}
        :param run_interruption_annotator: Whether to run the interruption annotator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#run_interruption_annotator ContactCenterInsightsAnalysisRule#run_interruption_annotator}
        :param run_issue_model_annotator: Whether to run the issue model annotator. A model should have already been deployed for this to take effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#run_issue_model_annotator ContactCenterInsightsAnalysisRule#run_issue_model_annotator}
        :param run_phrase_matcher_annotator: Whether to run the active phrase matcher annotator(s). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#run_phrase_matcher_annotator ContactCenterInsightsAnalysisRule#run_phrase_matcher_annotator}
        :param run_qa_annotator: Whether to run the QA annotator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#run_qa_annotator ContactCenterInsightsAnalysisRule#run_qa_annotator}
        :param run_sentiment_annotator: Whether to run the sentiment annotator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#run_sentiment_annotator ContactCenterInsightsAnalysisRule#run_sentiment_annotator}
        :param run_silence_annotator: Whether to run the silence annotator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#run_silence_annotator ContactCenterInsightsAnalysisRule#run_silence_annotator}
        :param run_summarization_annotator: Whether to run the summarization annotator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#run_summarization_annotator ContactCenterInsightsAnalysisRule#run_summarization_annotator}
        :param summarization_config: summarization_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#summarization_config ContactCenterInsightsAnalysisRule#summarization_config}
        '''
        value = ContactCenterInsightsAnalysisRuleAnnotatorSelector(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#create ContactCenterInsightsAnalysisRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#delete ContactCenterInsightsAnalysisRule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#update ContactCenterInsightsAnalysisRule#update}.
        '''
        value = ContactCenterInsightsAnalysisRuleTimeouts(
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
    ) -> "ContactCenterInsightsAnalysisRuleAnnotatorSelectorOutputReference":
        return typing.cast("ContactCenterInsightsAnalysisRuleAnnotatorSelectorOutputReference", jsii.get(self, "annotatorSelector"))

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
    def timeouts(self) -> "ContactCenterInsightsAnalysisRuleTimeoutsOutputReference":
        return typing.cast("ContactCenterInsightsAnalysisRuleTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["ContactCenterInsightsAnalysisRuleAnnotatorSelector"]:
        return typing.cast(typing.Optional["ContactCenterInsightsAnalysisRuleAnnotatorSelector"], jsii.get(self, "annotatorSelectorInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ContactCenterInsightsAnalysisRuleTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ContactCenterInsightsAnalysisRuleTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__727df8da52bdde23396026b50c773f1d3fe48bf80bcec8fbecffaf930fa795cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "active", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="analysisPercentage")
    def analysis_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "analysisPercentage"))

    @analysis_percentage.setter
    def analysis_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4063239b52036c1dfbda346b7455ec6e8b3d04b6185ec7e765cbe23d4a34066a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "analysisPercentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="conversationFilter")
    def conversation_filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "conversationFilter"))

    @conversation_filter.setter
    def conversation_filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2153c2b0a1ddf57bc567f1253fd5c3bb9ac52fc4ce52007f8aa80bc4b71b0c36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "conversationFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7d93dfad1f83e00859c57827bf1e64b8ffeac83c17858dcba9b82bb665cc762)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70c7be4e2e17ef505c31f709970988e279f10cd0db908188271e6c7a1a42f020)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f4fe53695e05e717f84595a2c908a9e0fc9485abf311ac353da833cc5052326)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adb8902f7bdf1ffd50ed20073434e43df458e6bf9c80b6e71e1e8ce22c4dc387)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.contactCenterInsightsAnalysisRule.ContactCenterInsightsAnalysisRuleAnnotatorSelector",
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
class ContactCenterInsightsAnalysisRuleAnnotatorSelector:
    def __init__(
        self,
        *,
        issue_models: typing.Optional[typing.Sequence[builtins.str]] = None,
        phrase_matchers: typing.Optional[typing.Sequence[builtins.str]] = None,
        qa_config: typing.Optional[typing.Union["ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        run_entity_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run_intent_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run_interruption_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run_issue_model_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run_phrase_matcher_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run_qa_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run_sentiment_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run_silence_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run_summarization_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        summarization_config: typing.Optional[typing.Union["ContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param issue_models: The issue model to run. If not provided, the most recently deployed topic model will be used. The provided issue model will only be used for inference if the issue model is deployed and if run_issue_model_annotator is set to true. If more than one issue model is provided, only the first provided issue model will be used for inference. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#issue_models ContactCenterInsightsAnalysisRule#issue_models}
        :param phrase_matchers: The list of phrase matchers to run. If not provided, all active phrase matchers will be used. If inactive phrase matchers are provided, they will not be used. Phrase matchers will be run only if run_phrase_matcher_annotator is set to true. Format: projects/{project}/locations/{location}/phraseMatchers/{phrase_matcher} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#phrase_matchers ContactCenterInsightsAnalysisRule#phrase_matchers}
        :param qa_config: qa_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#qa_config ContactCenterInsightsAnalysisRule#qa_config}
        :param run_entity_annotator: Whether to run the entity annotator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#run_entity_annotator ContactCenterInsightsAnalysisRule#run_entity_annotator}
        :param run_intent_annotator: Whether to run the intent annotator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#run_intent_annotator ContactCenterInsightsAnalysisRule#run_intent_annotator}
        :param run_interruption_annotator: Whether to run the interruption annotator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#run_interruption_annotator ContactCenterInsightsAnalysisRule#run_interruption_annotator}
        :param run_issue_model_annotator: Whether to run the issue model annotator. A model should have already been deployed for this to take effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#run_issue_model_annotator ContactCenterInsightsAnalysisRule#run_issue_model_annotator}
        :param run_phrase_matcher_annotator: Whether to run the active phrase matcher annotator(s). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#run_phrase_matcher_annotator ContactCenterInsightsAnalysisRule#run_phrase_matcher_annotator}
        :param run_qa_annotator: Whether to run the QA annotator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#run_qa_annotator ContactCenterInsightsAnalysisRule#run_qa_annotator}
        :param run_sentiment_annotator: Whether to run the sentiment annotator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#run_sentiment_annotator ContactCenterInsightsAnalysisRule#run_sentiment_annotator}
        :param run_silence_annotator: Whether to run the silence annotator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#run_silence_annotator ContactCenterInsightsAnalysisRule#run_silence_annotator}
        :param run_summarization_annotator: Whether to run the summarization annotator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#run_summarization_annotator ContactCenterInsightsAnalysisRule#run_summarization_annotator}
        :param summarization_config: summarization_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#summarization_config ContactCenterInsightsAnalysisRule#summarization_config}
        '''
        if isinstance(qa_config, dict):
            qa_config = ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfig(**qa_config)
        if isinstance(summarization_config, dict):
            summarization_config = ContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfig(**summarization_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ca037ba4746011245f5fb544ccebcf130222db10cbb01704f732e6bb370f9de)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#issue_models ContactCenterInsightsAnalysisRule#issue_models}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#phrase_matchers ContactCenterInsightsAnalysisRule#phrase_matchers}
        '''
        result = self._values.get("phrase_matchers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def qa_config(
        self,
    ) -> typing.Optional["ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfig"]:
        '''qa_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#qa_config ContactCenterInsightsAnalysisRule#qa_config}
        '''
        result = self._values.get("qa_config")
        return typing.cast(typing.Optional["ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfig"], result)

    @builtins.property
    def run_entity_annotator(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to run the entity annotator.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#run_entity_annotator ContactCenterInsightsAnalysisRule#run_entity_annotator}
        '''
        result = self._values.get("run_entity_annotator")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def run_intent_annotator(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to run the intent annotator.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#run_intent_annotator ContactCenterInsightsAnalysisRule#run_intent_annotator}
        '''
        result = self._values.get("run_intent_annotator")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def run_interruption_annotator(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to run the interruption annotator.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#run_interruption_annotator ContactCenterInsightsAnalysisRule#run_interruption_annotator}
        '''
        result = self._values.get("run_interruption_annotator")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def run_issue_model_annotator(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to run the issue model annotator. A model should have already been deployed for this to take effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#run_issue_model_annotator ContactCenterInsightsAnalysisRule#run_issue_model_annotator}
        '''
        result = self._values.get("run_issue_model_annotator")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def run_phrase_matcher_annotator(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to run the active phrase matcher annotator(s).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#run_phrase_matcher_annotator ContactCenterInsightsAnalysisRule#run_phrase_matcher_annotator}
        '''
        result = self._values.get("run_phrase_matcher_annotator")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def run_qa_annotator(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to run the QA annotator.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#run_qa_annotator ContactCenterInsightsAnalysisRule#run_qa_annotator}
        '''
        result = self._values.get("run_qa_annotator")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def run_sentiment_annotator(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to run the sentiment annotator.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#run_sentiment_annotator ContactCenterInsightsAnalysisRule#run_sentiment_annotator}
        '''
        result = self._values.get("run_sentiment_annotator")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def run_silence_annotator(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to run the silence annotator.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#run_silence_annotator ContactCenterInsightsAnalysisRule#run_silence_annotator}
        '''
        result = self._values.get("run_silence_annotator")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def run_summarization_annotator(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to run the summarization annotator.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#run_summarization_annotator ContactCenterInsightsAnalysisRule#run_summarization_annotator}
        '''
        result = self._values.get("run_summarization_annotator")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def summarization_config(
        self,
    ) -> typing.Optional["ContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfig"]:
        '''summarization_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#summarization_config ContactCenterInsightsAnalysisRule#summarization_config}
        '''
        result = self._values.get("summarization_config")
        return typing.cast(typing.Optional["ContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContactCenterInsightsAnalysisRuleAnnotatorSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContactCenterInsightsAnalysisRuleAnnotatorSelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.contactCenterInsightsAnalysisRule.ContactCenterInsightsAnalysisRuleAnnotatorSelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6806b4e7ee9890479b1a45a376c17443b592f62acc3ca3d19af7e9bac26a667)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putQaConfig")
    def put_qa_config(
        self,
        *,
        scorecard_list: typing.Optional[typing.Union["ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStruct", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scorecard_list: scorecard_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#scorecard_list ContactCenterInsightsAnalysisRule#scorecard_list}
        '''
        value = ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfig(
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
        :param conversation_profile: Resource name of the Dialogflow conversation profile. Format: projects/{project}/locations/{location}/conversationProfiles/{conversation_profile}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#conversation_profile ContactCenterInsightsAnalysisRule#conversation_profile}
        :param summarization_model: Default summarization model to be used. Possible values: SUMMARIZATION_MODEL_UNSPECIFIED BASELINE_MODEL BASELINE_MODEL_V2_0 Possible values: ["BASELINE_MODEL", "BASELINE_MODEL_V2_0"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#summarization_model ContactCenterInsightsAnalysisRule#summarization_model}
        '''
        value = ContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfig(
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
    ) -> "ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigOutputReference":
        return typing.cast("ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigOutputReference", jsii.get(self, "qaConfig"))

    @builtins.property
    @jsii.member(jsii_name="summarizationConfig")
    def summarization_config(
        self,
    ) -> "ContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfigOutputReference":
        return typing.cast("ContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfigOutputReference", jsii.get(self, "summarizationConfig"))

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
    ) -> typing.Optional["ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfig"]:
        return typing.cast(typing.Optional["ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfig"], jsii.get(self, "qaConfigInput"))

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
    ) -> typing.Optional["ContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfig"]:
        return typing.cast(typing.Optional["ContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfig"], jsii.get(self, "summarizationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="issueModels")
    def issue_models(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "issueModels"))

    @issue_models.setter
    def issue_models(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e6a581df4975803de6a7afb4b75d95770e05accac71c985a15964a0ef365e9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issueModels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="phraseMatchers")
    def phrase_matchers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "phraseMatchers"))

    @phrase_matchers.setter
    def phrase_matchers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33f3d25c471653a5898213b69bd9d32b2ad13483090024ed293e7fe210c59273)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09766b7becd5827196d839cf76a207e4d250b0fba6f275e1e34bf0de3dc43841)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd66b496a22f336ae9513b9d3283d44940d3b0e4d1dc795a7068a1f783f57000)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f477fff4249f79144583df13a2400059e34b2fcc833685a6a50d7beb5a2a2f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4091935704949df4a3180aa11535269eee6a5c4ac444a10a038fd91191f558ce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3459cd53791f84201d3411d6cbfa67200422df98b1c10b45028626e4dd0adb0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__04df5246c741055fb020fbe6151d9ed7a9244d8db511f2e9ef692f4573472324)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f673aff8b61104009b72b7195acbd689def05d9ae34217bd3bab967bd350faef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__50f05a88d719611133695c3e6cd443ba80d1f59b5e9d87b667e44bb7527fb185)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ac43125b4ef60839620e92661817ef9cc7aba2bd57fc7bfa2509fa94d55deff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runSummarizationAnnotator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContactCenterInsightsAnalysisRuleAnnotatorSelector]:
        return typing.cast(typing.Optional[ContactCenterInsightsAnalysisRuleAnnotatorSelector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContactCenterInsightsAnalysisRuleAnnotatorSelector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__536e503133b6e684839400a373d52dbd076949501b0c87cdae3ff0a50b003ad9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.contactCenterInsightsAnalysisRule.ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfig",
    jsii_struct_bases=[],
    name_mapping={"scorecard_list": "scorecardList"},
)
class ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfig:
    def __init__(
        self,
        *,
        scorecard_list: typing.Optional[typing.Union["ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStruct", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scorecard_list: scorecard_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#scorecard_list ContactCenterInsightsAnalysisRule#scorecard_list}
        '''
        if isinstance(scorecard_list, dict):
            scorecard_list = ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStruct(**scorecard_list)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a5d19417532ce1edc35bc55c479cfb92902d0e73b5fe6037536f6bcf05a04e0)
            check_type(argname="argument scorecard_list", value=scorecard_list, expected_type=type_hints["scorecard_list"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if scorecard_list is not None:
            self._values["scorecard_list"] = scorecard_list

    @builtins.property
    def scorecard_list(
        self,
    ) -> typing.Optional["ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStruct"]:
        '''scorecard_list block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#scorecard_list ContactCenterInsightsAnalysisRule#scorecard_list}
        '''
        result = self._values.get("scorecard_list")
        return typing.cast(typing.Optional["ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStruct"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.contactCenterInsightsAnalysisRule.ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1991e526effee286bcbf485e497f347423318c7899bdf309a1679d84e22973c)
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
        :param qa_scorecard_revisions: List of QaScorecardRevisions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#qa_scorecard_revisions ContactCenterInsightsAnalysisRule#qa_scorecard_revisions}
        '''
        value = ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStruct(
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
    ) -> "ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStructOutputReference":
        return typing.cast("ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStructOutputReference", jsii.get(self, "scorecardList"))

    @builtins.property
    @jsii.member(jsii_name="scorecardListInput")
    def scorecard_list_input(
        self,
    ) -> typing.Optional["ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStruct"]:
        return typing.cast(typing.Optional["ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStruct"], jsii.get(self, "scorecardListInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfig]:
        return typing.cast(typing.Optional[ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5094197abbeb03168634a264103335aa3d2b99c9a6e034833ca5ba673b544b70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.contactCenterInsightsAnalysisRule.ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStruct",
    jsii_struct_bases=[],
    name_mapping={"qa_scorecard_revisions": "qaScorecardRevisions"},
)
class ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStruct:
    def __init__(
        self,
        *,
        qa_scorecard_revisions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param qa_scorecard_revisions: List of QaScorecardRevisions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#qa_scorecard_revisions ContactCenterInsightsAnalysisRule#qa_scorecard_revisions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90d0190053d2a5a7615f770fce0d2635ae197e42bef1658a28427ba98491b23f)
            check_type(argname="argument qa_scorecard_revisions", value=qa_scorecard_revisions, expected_type=type_hints["qa_scorecard_revisions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if qa_scorecard_revisions is not None:
            self._values["qa_scorecard_revisions"] = qa_scorecard_revisions

    @builtins.property
    def qa_scorecard_revisions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of QaScorecardRevisions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#qa_scorecard_revisions ContactCenterInsightsAnalysisRule#qa_scorecard_revisions}
        '''
        result = self._values.get("qa_scorecard_revisions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.contactCenterInsightsAnalysisRule.ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fe4b2b87a556b0843800f939aa69647e144967ba55bcbc5113a531179c589a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eacfe0a4c2ba4c6eee56985d25b497a4306b946a2de76c8b9c4e2b803814c244)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "qaScorecardRevisions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStruct]:
        return typing.cast(typing.Optional[ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82b9733a26ecc73360c378ff0546b4369dc276ff7148171c310e869f9d444da2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.contactCenterInsightsAnalysisRule.ContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "conversation_profile": "conversationProfile",
        "summarization_model": "summarizationModel",
    },
)
class ContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfig:
    def __init__(
        self,
        *,
        conversation_profile: typing.Optional[builtins.str] = None,
        summarization_model: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param conversation_profile: Resource name of the Dialogflow conversation profile. Format: projects/{project}/locations/{location}/conversationProfiles/{conversation_profile}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#conversation_profile ContactCenterInsightsAnalysisRule#conversation_profile}
        :param summarization_model: Default summarization model to be used. Possible values: SUMMARIZATION_MODEL_UNSPECIFIED BASELINE_MODEL BASELINE_MODEL_V2_0 Possible values: ["BASELINE_MODEL", "BASELINE_MODEL_V2_0"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#summarization_model ContactCenterInsightsAnalysisRule#summarization_model}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e88ff8e43be6d1a0116c4ad68d5857095ff495940846dd5c765fd746df36421f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#conversation_profile ContactCenterInsightsAnalysisRule#conversation_profile}
        '''
        result = self._values.get("conversation_profile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def summarization_model(self) -> typing.Optional[builtins.str]:
        '''Default summarization model to be used. Possible values: SUMMARIZATION_MODEL_UNSPECIFIED BASELINE_MODEL BASELINE_MODEL_V2_0 Possible values: ["BASELINE_MODEL", "BASELINE_MODEL_V2_0"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#summarization_model ContactCenterInsightsAnalysisRule#summarization_model}
        '''
        result = self._values.get("summarization_model")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.contactCenterInsightsAnalysisRule.ContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a9bd21a91f68206da7fe8f777d24298288e6b278033e67325792d7427c0542b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9f116e9c3bcacd08d6552fcc0a1c90acb27dc2f6b10e6af569f214995e823f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "conversationProfile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="summarizationModel")
    def summarization_model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "summarizationModel"))

    @summarization_model.setter
    def summarization_model(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1972612defdd4ec6fee273c31f0bb411f70617c1fc411ab2d027145474531c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "summarizationModel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfig]:
        return typing.cast(typing.Optional[ContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e796c26ea5d873f69c2e403356dc37b879d8e35703431737d6c1a2d0ac319c15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.contactCenterInsightsAnalysisRule.ContactCenterInsightsAnalysisRuleConfig",
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
class ContactCenterInsightsAnalysisRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        annotator_selector: typing.Optional[typing.Union[ContactCenterInsightsAnalysisRuleAnnotatorSelector, typing.Dict[builtins.str, typing.Any]]] = None,
        conversation_filter: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ContactCenterInsightsAnalysisRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Location of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#location ContactCenterInsightsAnalysisRule#location}
        :param active: If true, apply this rule to conversations. Otherwise, this rule is inactive and saved as a draft. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#active ContactCenterInsightsAnalysisRule#active}
        :param analysis_percentage: Percentage of conversations that we should apply this analysis setting automatically, between [0, 1]. For example, 0.1 means 10%. Conversations are sampled in a determenestic way. The original runtime_percentage & upload percentage will be replaced by defining filters on the conversation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#analysis_percentage ContactCenterInsightsAnalysisRule#analysis_percentage}
        :param annotator_selector: annotator_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#annotator_selector ContactCenterInsightsAnalysisRule#annotator_selector}
        :param conversation_filter: Filter for the conversations that should apply this analysis rule. An empty filter means this analysis rule applies to all conversations. Refer to https://cloud.google.com/contact-center/insights/docs/filtering for details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#conversation_filter ContactCenterInsightsAnalysisRule#conversation_filter}
        :param display_name: Display Name of the analysis rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#display_name ContactCenterInsightsAnalysisRule#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#id ContactCenterInsightsAnalysisRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#project ContactCenterInsightsAnalysisRule#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#timeouts ContactCenterInsightsAnalysisRule#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(annotator_selector, dict):
            annotator_selector = ContactCenterInsightsAnalysisRuleAnnotatorSelector(**annotator_selector)
        if isinstance(timeouts, dict):
            timeouts = ContactCenterInsightsAnalysisRuleTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8adf78674049c3a2b63a4d9c96fa7dbe93c0b1ee4e0af6670907e40cb0763770)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#location ContactCenterInsightsAnalysisRule#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def active(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, apply this rule to conversations. Otherwise, this rule is inactive and saved as a draft.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#active ContactCenterInsightsAnalysisRule#active}
        '''
        result = self._values.get("active")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def analysis_percentage(self) -> typing.Optional[jsii.Number]:
        '''Percentage of conversations that we should apply this analysis setting automatically, between [0, 1].

        For example, 0.1 means 10%. Conversations
        are sampled in a determenestic way. The original runtime_percentage &
        upload percentage will be replaced by defining filters on the conversation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#analysis_percentage ContactCenterInsightsAnalysisRule#analysis_percentage}
        '''
        result = self._values.get("analysis_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def annotator_selector(
        self,
    ) -> typing.Optional[ContactCenterInsightsAnalysisRuleAnnotatorSelector]:
        '''annotator_selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#annotator_selector ContactCenterInsightsAnalysisRule#annotator_selector}
        '''
        result = self._values.get("annotator_selector")
        return typing.cast(typing.Optional[ContactCenterInsightsAnalysisRuleAnnotatorSelector], result)

    @builtins.property
    def conversation_filter(self) -> typing.Optional[builtins.str]:
        '''Filter for the conversations that should apply this analysis rule.

        An empty filter means this analysis rule applies to all
        conversations.
        Refer to https://cloud.google.com/contact-center/insights/docs/filtering
        for details.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#conversation_filter ContactCenterInsightsAnalysisRule#conversation_filter}
        '''
        result = self._values.get("conversation_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Display Name of the analysis rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#display_name ContactCenterInsightsAnalysisRule#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#id ContactCenterInsightsAnalysisRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#project ContactCenterInsightsAnalysisRule#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ContactCenterInsightsAnalysisRuleTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#timeouts ContactCenterInsightsAnalysisRule#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ContactCenterInsightsAnalysisRuleTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContactCenterInsightsAnalysisRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.contactCenterInsightsAnalysisRule.ContactCenterInsightsAnalysisRuleTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ContactCenterInsightsAnalysisRuleTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#create ContactCenterInsightsAnalysisRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#delete ContactCenterInsightsAnalysisRule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#update ContactCenterInsightsAnalysisRule#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cbe5a6603c07a5083c434e58f02a5db68a94c96edb078e7e3e48fe74b497221)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#create ContactCenterInsightsAnalysisRule#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#delete ContactCenterInsightsAnalysisRule#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/contact_center_insights_analysis_rule#update ContactCenterInsightsAnalysisRule#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContactCenterInsightsAnalysisRuleTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContactCenterInsightsAnalysisRuleTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.contactCenterInsightsAnalysisRule.ContactCenterInsightsAnalysisRuleTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2f1a4e2f5948f149700761dfa7a80b79e74c871e21363abc4b28be38dc63767)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d714fb6f3736dc0c8dffbf2e2616a7976bc3dd79c38410ec429e61cfb6cebf80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee9fc9f7483c23cb725973991dce895c3108b50da3370859785814c47ad804fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6444658f5d04979d69f3ce8495b2038b419c30b72d9afb67cf6ff198dd463f60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContactCenterInsightsAnalysisRuleTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContactCenterInsightsAnalysisRuleTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContactCenterInsightsAnalysisRuleTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09adf09e9261df3ec9b9b0655aabc671e82c6923d1256e53a9eae6de568fef9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ContactCenterInsightsAnalysisRule",
    "ContactCenterInsightsAnalysisRuleAnnotatorSelector",
    "ContactCenterInsightsAnalysisRuleAnnotatorSelectorOutputReference",
    "ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfig",
    "ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigOutputReference",
    "ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStruct",
    "ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStructOutputReference",
    "ContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfig",
    "ContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfigOutputReference",
    "ContactCenterInsightsAnalysisRuleConfig",
    "ContactCenterInsightsAnalysisRuleTimeouts",
    "ContactCenterInsightsAnalysisRuleTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__a3772ea7feb7a7cf7cd93a29f0077f86ca88ff9d62602469ea047a45baab6ce9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    analysis_percentage: typing.Optional[jsii.Number] = None,
    annotator_selector: typing.Optional[typing.Union[ContactCenterInsightsAnalysisRuleAnnotatorSelector, typing.Dict[builtins.str, typing.Any]]] = None,
    conversation_filter: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ContactCenterInsightsAnalysisRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__434804b17ef9cb7be369c42caeccc8e3672a8873b4ed1fbd53f73a38e873fbe3(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__727df8da52bdde23396026b50c773f1d3fe48bf80bcec8fbecffaf930fa795cd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4063239b52036c1dfbda346b7455ec6e8b3d04b6185ec7e765cbe23d4a34066a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2153c2b0a1ddf57bc567f1253fd5c3bb9ac52fc4ce52007f8aa80bc4b71b0c36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7d93dfad1f83e00859c57827bf1e64b8ffeac83c17858dcba9b82bb665cc762(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70c7be4e2e17ef505c31f709970988e279f10cd0db908188271e6c7a1a42f020(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f4fe53695e05e717f84595a2c908a9e0fc9485abf311ac353da833cc5052326(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adb8902f7bdf1ffd50ed20073434e43df458e6bf9c80b6e71e1e8ce22c4dc387(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ca037ba4746011245f5fb544ccebcf130222db10cbb01704f732e6bb370f9de(
    *,
    issue_models: typing.Optional[typing.Sequence[builtins.str]] = None,
    phrase_matchers: typing.Optional[typing.Sequence[builtins.str]] = None,
    qa_config: typing.Optional[typing.Union[ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    run_entity_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    run_intent_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    run_interruption_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    run_issue_model_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    run_phrase_matcher_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    run_qa_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    run_sentiment_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    run_silence_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    run_summarization_annotator: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    summarization_config: typing.Optional[typing.Union[ContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6806b4e7ee9890479b1a45a376c17443b592f62acc3ca3d19af7e9bac26a667(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e6a581df4975803de6a7afb4b75d95770e05accac71c985a15964a0ef365e9c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33f3d25c471653a5898213b69bd9d32b2ad13483090024ed293e7fe210c59273(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09766b7becd5827196d839cf76a207e4d250b0fba6f275e1e34bf0de3dc43841(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd66b496a22f336ae9513b9d3283d44940d3b0e4d1dc795a7068a1f783f57000(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f477fff4249f79144583df13a2400059e34b2fcc833685a6a50d7beb5a2a2f5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4091935704949df4a3180aa11535269eee6a5c4ac444a10a038fd91191f558ce(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3459cd53791f84201d3411d6cbfa67200422df98b1c10b45028626e4dd0adb0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04df5246c741055fb020fbe6151d9ed7a9244d8db511f2e9ef692f4573472324(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f673aff8b61104009b72b7195acbd689def05d9ae34217bd3bab967bd350faef(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50f05a88d719611133695c3e6cd443ba80d1f59b5e9d87b667e44bb7527fb185(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ac43125b4ef60839620e92661817ef9cc7aba2bd57fc7bfa2509fa94d55deff(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__536e503133b6e684839400a373d52dbd076949501b0c87cdae3ff0a50b003ad9(
    value: typing.Optional[ContactCenterInsightsAnalysisRuleAnnotatorSelector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a5d19417532ce1edc35bc55c479cfb92902d0e73b5fe6037536f6bcf05a04e0(
    *,
    scorecard_list: typing.Optional[typing.Union[ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1991e526effee286bcbf485e497f347423318c7899bdf309a1679d84e22973c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5094197abbeb03168634a264103335aa3d2b99c9a6e034833ca5ba673b544b70(
    value: typing.Optional[ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90d0190053d2a5a7615f770fce0d2635ae197e42bef1658a28427ba98491b23f(
    *,
    qa_scorecard_revisions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fe4b2b87a556b0843800f939aa69647e144967ba55bcbc5113a531179c589a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eacfe0a4c2ba4c6eee56985d25b497a4306b946a2de76c8b9c4e2b803814c244(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82b9733a26ecc73360c378ff0546b4369dc276ff7148171c310e869f9d444da2(
    value: typing.Optional[ContactCenterInsightsAnalysisRuleAnnotatorSelectorQaConfigScorecardListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e88ff8e43be6d1a0116c4ad68d5857095ff495940846dd5c765fd746df36421f(
    *,
    conversation_profile: typing.Optional[builtins.str] = None,
    summarization_model: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a9bd21a91f68206da7fe8f777d24298288e6b278033e67325792d7427c0542b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9f116e9c3bcacd08d6552fcc0a1c90acb27dc2f6b10e6af569f214995e823f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1972612defdd4ec6fee273c31f0bb411f70617c1fc411ab2d027145474531c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e796c26ea5d873f69c2e403356dc37b879d8e35703431737d6c1a2d0ac319c15(
    value: typing.Optional[ContactCenterInsightsAnalysisRuleAnnotatorSelectorSummarizationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8adf78674049c3a2b63a4d9c96fa7dbe93c0b1ee4e0af6670907e40cb0763770(
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
    annotator_selector: typing.Optional[typing.Union[ContactCenterInsightsAnalysisRuleAnnotatorSelector, typing.Dict[builtins.str, typing.Any]]] = None,
    conversation_filter: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ContactCenterInsightsAnalysisRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cbe5a6603c07a5083c434e58f02a5db68a94c96edb078e7e3e48fe74b497221(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2f1a4e2f5948f149700761dfa7a80b79e74c871e21363abc4b28be38dc63767(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d714fb6f3736dc0c8dffbf2e2616a7976bc3dd79c38410ec429e61cfb6cebf80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee9fc9f7483c23cb725973991dce895c3108b50da3370859785814c47ad804fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6444658f5d04979d69f3ce8495b2038b419c30b72d9afb67cf6ff198dd463f60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09adf09e9261df3ec9b9b0655aabc671e82c6923d1256e53a9eae6de568fef9a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContactCenterInsightsAnalysisRuleTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
