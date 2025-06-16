r'''
# `google_billing_budget`

Refer to the Terraform Registry for docs: [`google_billing_budget`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget).
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


class GoogleBillingBudget(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBillingBudget.GoogleBillingBudget",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget google_billing_budget}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        amount: typing.Union["GoogleBillingBudgetAmount", typing.Dict[builtins.str, typing.Any]],
        billing_account: builtins.str,
        all_updates_rule: typing.Optional[typing.Union["GoogleBillingBudgetAllUpdatesRule", typing.Dict[builtins.str, typing.Any]]] = None,
        budget_filter: typing.Optional[typing.Union["GoogleBillingBudgetBudgetFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ownership_scope: typing.Optional[builtins.str] = None,
        threshold_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleBillingBudgetThresholdRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleBillingBudgetTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget google_billing_budget} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param amount: amount block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#amount GoogleBillingBudget#amount}
        :param billing_account: ID of the billing account to set a budget on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#billing_account GoogleBillingBudget#billing_account}
        :param all_updates_rule: all_updates_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#all_updates_rule GoogleBillingBudget#all_updates_rule}
        :param budget_filter: budget_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#budget_filter GoogleBillingBudget#budget_filter}
        :param display_name: User data for display name in UI. Must be <= 60 chars. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#display_name GoogleBillingBudget#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#id GoogleBillingBudget#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ownership_scope: The ownership scope of the budget. The ownership scope and users' IAM permissions determine who has full access to the budget's data. Possible values: ["OWNERSHIP_SCOPE_UNSPECIFIED", "ALL_USERS", "BILLING_ACCOUNT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#ownership_scope GoogleBillingBudget#ownership_scope}
        :param threshold_rules: threshold_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#threshold_rules GoogleBillingBudget#threshold_rules}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#timeouts GoogleBillingBudget#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4e7c06110316e69b0d05657484388e3ff765d48a293200b2d2347bbd240412e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleBillingBudgetConfig(
            amount=amount,
            billing_account=billing_account,
            all_updates_rule=all_updates_rule,
            budget_filter=budget_filter,
            display_name=display_name,
            id=id,
            ownership_scope=ownership_scope,
            threshold_rules=threshold_rules,
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
        '''Generates CDKTF code for importing a GoogleBillingBudget resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleBillingBudget to import.
        :param import_from_id: The id of the existing GoogleBillingBudget that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleBillingBudget to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bf3e976a39bcd3ceb697f62fe3be425921fed0363274dd5526f1e98a8c59948)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAllUpdatesRule")
    def put_all_updates_rule(
        self,
        *,
        disable_default_iam_recipients: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_project_level_recipients: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        monitoring_notification_channels: typing.Optional[typing.Sequence[builtins.str]] = None,
        pubsub_topic: typing.Optional[builtins.str] = None,
        schema_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disable_default_iam_recipients: Boolean. When set to true, disables default notifications sent when a threshold is exceeded. Default recipients are those with Billing Account Administrators and Billing Account Users IAM roles for the target account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#disable_default_iam_recipients GoogleBillingBudget#disable_default_iam_recipients}
        :param enable_project_level_recipients: When set to true, and when the budget has a single project configured, notifications will be sent to project level recipients of that project. This field will be ignored if the budget has multiple or no project configured. Currently, project level recipients are the users with Owner role on a cloud project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#enable_project_level_recipients GoogleBillingBudget#enable_project_level_recipients}
        :param monitoring_notification_channels: The full resource name of a monitoring notification channel in the form projects/{project_id}/notificationChannels/{channel_id}. A maximum of 5 channels are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#monitoring_notification_channels GoogleBillingBudget#monitoring_notification_channels}
        :param pubsub_topic: The name of the Cloud Pub/Sub topic where budget related messages will be published, in the form projects/{project_id}/topics/{topic_id}. Updates are sent at regular intervals to the topic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#pubsub_topic GoogleBillingBudget#pubsub_topic}
        :param schema_version: The schema version of the notification. Only "1.0" is accepted. It represents the JSON schema as defined in https://cloud.google.com/billing/docs/how-to/budgets#notification_format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#schema_version GoogleBillingBudget#schema_version}
        '''
        value = GoogleBillingBudgetAllUpdatesRule(
            disable_default_iam_recipients=disable_default_iam_recipients,
            enable_project_level_recipients=enable_project_level_recipients,
            monitoring_notification_channels=monitoring_notification_channels,
            pubsub_topic=pubsub_topic,
            schema_version=schema_version,
        )

        return typing.cast(None, jsii.invoke(self, "putAllUpdatesRule", [value]))

    @jsii.member(jsii_name="putAmount")
    def put_amount(
        self,
        *,
        last_period_amount: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        specified_amount: typing.Optional[typing.Union["GoogleBillingBudgetAmountSpecifiedAmount", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param last_period_amount: Configures a budget amount that is automatically set to 100% of last period's spend. Boolean. Set value to true to use. Do not set to false, instead use the 'specified_amount' block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#last_period_amount GoogleBillingBudget#last_period_amount}
        :param specified_amount: specified_amount block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#specified_amount GoogleBillingBudget#specified_amount}
        '''
        value = GoogleBillingBudgetAmount(
            last_period_amount=last_period_amount, specified_amount=specified_amount
        )

        return typing.cast(None, jsii.invoke(self, "putAmount", [value]))

    @jsii.member(jsii_name="putBudgetFilter")
    def put_budget_filter(
        self,
        *,
        calendar_period: typing.Optional[builtins.str] = None,
        credit_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        credit_types_treatment: typing.Optional[builtins.str] = None,
        custom_period: typing.Optional[typing.Union["GoogleBillingBudgetBudgetFilterCustomPeriod", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        projects: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_ancestors: typing.Optional[typing.Sequence[builtins.str]] = None,
        services: typing.Optional[typing.Sequence[builtins.str]] = None,
        subaccounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param calendar_period: A CalendarPeriod represents the abstract concept of a recurring time period that has a canonical start. Grammatically, "the start of the current CalendarPeriod". All calendar times begin at 12 AM US and Canadian Pacific Time (UTC-8). Exactly one of 'calendar_period', 'custom_period' must be provided. Possible values: ["MONTH", "QUARTER", "YEAR", "CALENDAR_PERIOD_UNSPECIFIED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#calendar_period GoogleBillingBudget#calendar_period}
        :param credit_types: Optional. If creditTypesTreatment is INCLUDE_SPECIFIED_CREDITS, this is a list of credit types to be subtracted from gross cost to determine the spend for threshold calculations. See a list of acceptable credit type values. If creditTypesTreatment is not INCLUDE_SPECIFIED_CREDITS, this field must be empty. **Note:** If the field has a value in the config and needs to be removed, the field has to be an empty array in the config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#credit_types GoogleBillingBudget#credit_types}
        :param credit_types_treatment: Specifies how credits should be treated when determining spend for threshold calculations. Default value: "INCLUDE_ALL_CREDITS" Possible values: ["INCLUDE_ALL_CREDITS", "EXCLUDE_ALL_CREDITS", "INCLUDE_SPECIFIED_CREDITS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#credit_types_treatment GoogleBillingBudget#credit_types_treatment}
        :param custom_period: custom_period block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#custom_period GoogleBillingBudget#custom_period}
        :param labels: A single label and value pair specifying that usage from only this set of labeled resources should be included in the budget. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#labels GoogleBillingBudget#labels}
        :param projects: A set of projects of the form projects/{project_number}, specifying that usage from only this set of projects should be included in the budget. If omitted, the report will include all usage for the billing account, regardless of which project the usage occurred on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#projects GoogleBillingBudget#projects}
        :param resource_ancestors: A set of folder and organization names of the form folders/{folderId} or organizations/{organizationId}, specifying that usage from only this set of folders and organizations should be included in the budget. If omitted, the budget includes all usage that the billing account pays for. If the folder or organization contains projects that are paid for by a different Cloud Billing account, the budget doesn't apply to those projects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#resource_ancestors GoogleBillingBudget#resource_ancestors}
        :param services: A set of services of the form services/{service_id}, specifying that usage from only this set of services should be included in the budget. If omitted, the report will include usage for all the services. The service names are available through the Catalog API: https://cloud.google.com/billing/v1/how-tos/catalog-api. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#services GoogleBillingBudget#services}
        :param subaccounts: A set of subaccounts of the form billingAccounts/{account_id}, specifying that usage from only this set of subaccounts should be included in the budget. If a subaccount is set to the name of the parent account, usage from the parent account will be included. If the field is omitted, the report will include usage from the parent account and all subaccounts, if they exist. **Note:** If the field has a value in the config and needs to be removed, the field has to be an empty array in the config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#subaccounts GoogleBillingBudget#subaccounts}
        '''
        value = GoogleBillingBudgetBudgetFilter(
            calendar_period=calendar_period,
            credit_types=credit_types,
            credit_types_treatment=credit_types_treatment,
            custom_period=custom_period,
            labels=labels,
            projects=projects,
            resource_ancestors=resource_ancestors,
            services=services,
            subaccounts=subaccounts,
        )

        return typing.cast(None, jsii.invoke(self, "putBudgetFilter", [value]))

    @jsii.member(jsii_name="putThresholdRules")
    def put_threshold_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleBillingBudgetThresholdRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb5bb0b39a81bac5566db0eb48986ee95ca1a862beea6ed142aea74e20682816)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putThresholdRules", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#create GoogleBillingBudget#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#delete GoogleBillingBudget#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#update GoogleBillingBudget#update}.
        '''
        value = GoogleBillingBudgetTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAllUpdatesRule")
    def reset_all_updates_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllUpdatesRule", []))

    @jsii.member(jsii_name="resetBudgetFilter")
    def reset_budget_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBudgetFilter", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOwnershipScope")
    def reset_ownership_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOwnershipScope", []))

    @jsii.member(jsii_name="resetThresholdRules")
    def reset_threshold_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThresholdRules", []))

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
    @jsii.member(jsii_name="allUpdatesRule")
    def all_updates_rule(self) -> "GoogleBillingBudgetAllUpdatesRuleOutputReference":
        return typing.cast("GoogleBillingBudgetAllUpdatesRuleOutputReference", jsii.get(self, "allUpdatesRule"))

    @builtins.property
    @jsii.member(jsii_name="amount")
    def amount(self) -> "GoogleBillingBudgetAmountOutputReference":
        return typing.cast("GoogleBillingBudgetAmountOutputReference", jsii.get(self, "amount"))

    @builtins.property
    @jsii.member(jsii_name="budgetFilter")
    def budget_filter(self) -> "GoogleBillingBudgetBudgetFilterOutputReference":
        return typing.cast("GoogleBillingBudgetBudgetFilterOutputReference", jsii.get(self, "budgetFilter"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="thresholdRules")
    def threshold_rules(self) -> "GoogleBillingBudgetThresholdRulesList":
        return typing.cast("GoogleBillingBudgetThresholdRulesList", jsii.get(self, "thresholdRules"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleBillingBudgetTimeoutsOutputReference":
        return typing.cast("GoogleBillingBudgetTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="allUpdatesRuleInput")
    def all_updates_rule_input(
        self,
    ) -> typing.Optional["GoogleBillingBudgetAllUpdatesRule"]:
        return typing.cast(typing.Optional["GoogleBillingBudgetAllUpdatesRule"], jsii.get(self, "allUpdatesRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="amountInput")
    def amount_input(self) -> typing.Optional["GoogleBillingBudgetAmount"]:
        return typing.cast(typing.Optional["GoogleBillingBudgetAmount"], jsii.get(self, "amountInput"))

    @builtins.property
    @jsii.member(jsii_name="billingAccountInput")
    def billing_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "billingAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="budgetFilterInput")
    def budget_filter_input(self) -> typing.Optional["GoogleBillingBudgetBudgetFilter"]:
        return typing.cast(typing.Optional["GoogleBillingBudgetBudgetFilter"], jsii.get(self, "budgetFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ownershipScopeInput")
    def ownership_scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ownershipScopeInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdRulesInput")
    def threshold_rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBillingBudgetThresholdRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBillingBudgetThresholdRules"]]], jsii.get(self, "thresholdRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleBillingBudgetTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleBillingBudgetTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="billingAccount")
    def billing_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "billingAccount"))

    @billing_account.setter
    def billing_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec9f6d2147393b402d6f6d22ad33f73c014d76741f56e2c57e3983756d36ee48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "billingAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c693ff57065a01d0126f88539c91bcbe5a56e7ec0a09604186050e6ee44cef1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a291a31793ef151fc7fc69a2014d0297bc192e23dcd5b9b5fe25537ee38aeea3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ownershipScope")
    def ownership_scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ownershipScope"))

    @ownership_scope.setter
    def ownership_scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2402ece2f4bde0b8048fc3c5f6bee33c86a7b42afbeea9bccb58711022cc058)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ownershipScope", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBillingBudget.GoogleBillingBudgetAllUpdatesRule",
    jsii_struct_bases=[],
    name_mapping={
        "disable_default_iam_recipients": "disableDefaultIamRecipients",
        "enable_project_level_recipients": "enableProjectLevelRecipients",
        "monitoring_notification_channels": "monitoringNotificationChannels",
        "pubsub_topic": "pubsubTopic",
        "schema_version": "schemaVersion",
    },
)
class GoogleBillingBudgetAllUpdatesRule:
    def __init__(
        self,
        *,
        disable_default_iam_recipients: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_project_level_recipients: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        monitoring_notification_channels: typing.Optional[typing.Sequence[builtins.str]] = None,
        pubsub_topic: typing.Optional[builtins.str] = None,
        schema_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disable_default_iam_recipients: Boolean. When set to true, disables default notifications sent when a threshold is exceeded. Default recipients are those with Billing Account Administrators and Billing Account Users IAM roles for the target account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#disable_default_iam_recipients GoogleBillingBudget#disable_default_iam_recipients}
        :param enable_project_level_recipients: When set to true, and when the budget has a single project configured, notifications will be sent to project level recipients of that project. This field will be ignored if the budget has multiple or no project configured. Currently, project level recipients are the users with Owner role on a cloud project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#enable_project_level_recipients GoogleBillingBudget#enable_project_level_recipients}
        :param monitoring_notification_channels: The full resource name of a monitoring notification channel in the form projects/{project_id}/notificationChannels/{channel_id}. A maximum of 5 channels are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#monitoring_notification_channels GoogleBillingBudget#monitoring_notification_channels}
        :param pubsub_topic: The name of the Cloud Pub/Sub topic where budget related messages will be published, in the form projects/{project_id}/topics/{topic_id}. Updates are sent at regular intervals to the topic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#pubsub_topic GoogleBillingBudget#pubsub_topic}
        :param schema_version: The schema version of the notification. Only "1.0" is accepted. It represents the JSON schema as defined in https://cloud.google.com/billing/docs/how-to/budgets#notification_format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#schema_version GoogleBillingBudget#schema_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c99c3f40026102571c49a0ea5647dc5fb3ef983619c29b998ed8a6eeaecf89d)
            check_type(argname="argument disable_default_iam_recipients", value=disable_default_iam_recipients, expected_type=type_hints["disable_default_iam_recipients"])
            check_type(argname="argument enable_project_level_recipients", value=enable_project_level_recipients, expected_type=type_hints["enable_project_level_recipients"])
            check_type(argname="argument monitoring_notification_channels", value=monitoring_notification_channels, expected_type=type_hints["monitoring_notification_channels"])
            check_type(argname="argument pubsub_topic", value=pubsub_topic, expected_type=type_hints["pubsub_topic"])
            check_type(argname="argument schema_version", value=schema_version, expected_type=type_hints["schema_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disable_default_iam_recipients is not None:
            self._values["disable_default_iam_recipients"] = disable_default_iam_recipients
        if enable_project_level_recipients is not None:
            self._values["enable_project_level_recipients"] = enable_project_level_recipients
        if monitoring_notification_channels is not None:
            self._values["monitoring_notification_channels"] = monitoring_notification_channels
        if pubsub_topic is not None:
            self._values["pubsub_topic"] = pubsub_topic
        if schema_version is not None:
            self._values["schema_version"] = schema_version

    @builtins.property
    def disable_default_iam_recipients(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean.

        When set to true, disables default notifications sent
        when a threshold is exceeded. Default recipients are
        those with Billing Account Administrators and Billing
        Account Users IAM roles for the target account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#disable_default_iam_recipients GoogleBillingBudget#disable_default_iam_recipients}
        '''
        result = self._values.get("disable_default_iam_recipients")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_project_level_recipients(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When set to true, and when the budget has a single project configured, notifications will be sent to project level recipients of that project.

        This field will be ignored if the budget has multiple or no project configured.

        Currently, project level recipients are the users with Owner role on a cloud project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#enable_project_level_recipients GoogleBillingBudget#enable_project_level_recipients}
        '''
        result = self._values.get("enable_project_level_recipients")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def monitoring_notification_channels(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''The full resource name of a monitoring notification channel in the form projects/{project_id}/notificationChannels/{channel_id}. A maximum of 5 channels are allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#monitoring_notification_channels GoogleBillingBudget#monitoring_notification_channels}
        '''
        result = self._values.get("monitoring_notification_channels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def pubsub_topic(self) -> typing.Optional[builtins.str]:
        '''The name of the Cloud Pub/Sub topic where budget related messages will be published, in the form projects/{project_id}/topics/{topic_id}.

        Updates are sent
        at regular intervals to the topic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#pubsub_topic GoogleBillingBudget#pubsub_topic}
        '''
        result = self._values.get("pubsub_topic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_version(self) -> typing.Optional[builtins.str]:
        '''The schema version of the notification. Only "1.0" is accepted. It represents the JSON schema as defined in https://cloud.google.com/billing/docs/how-to/budgets#notification_format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#schema_version GoogleBillingBudget#schema_version}
        '''
        result = self._values.get("schema_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBillingBudgetAllUpdatesRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBillingBudgetAllUpdatesRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBillingBudget.GoogleBillingBudgetAllUpdatesRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2401441be282fc1c871c433aefd1719e52170dcb5b5de9b8b2bc0f45468c81fd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDisableDefaultIamRecipients")
    def reset_disable_default_iam_recipients(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableDefaultIamRecipients", []))

    @jsii.member(jsii_name="resetEnableProjectLevelRecipients")
    def reset_enable_project_level_recipients(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableProjectLevelRecipients", []))

    @jsii.member(jsii_name="resetMonitoringNotificationChannels")
    def reset_monitoring_notification_channels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitoringNotificationChannels", []))

    @jsii.member(jsii_name="resetPubsubTopic")
    def reset_pubsub_topic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPubsubTopic", []))

    @jsii.member(jsii_name="resetSchemaVersion")
    def reset_schema_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaVersion", []))

    @builtins.property
    @jsii.member(jsii_name="disableDefaultIamRecipientsInput")
    def disable_default_iam_recipients_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableDefaultIamRecipientsInput"))

    @builtins.property
    @jsii.member(jsii_name="enableProjectLevelRecipientsInput")
    def enable_project_level_recipients_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableProjectLevelRecipientsInput"))

    @builtins.property
    @jsii.member(jsii_name="monitoringNotificationChannelsInput")
    def monitoring_notification_channels_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "monitoringNotificationChannelsInput"))

    @builtins.property
    @jsii.member(jsii_name="pubsubTopicInput")
    def pubsub_topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pubsubTopicInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaVersionInput")
    def schema_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="disableDefaultIamRecipients")
    def disable_default_iam_recipients(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableDefaultIamRecipients"))

    @disable_default_iam_recipients.setter
    def disable_default_iam_recipients(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b981fc669ed875c1cbd0455cbb1d268d3c710637b45b0641b8fc4e6eb0b38f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableDefaultIamRecipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableProjectLevelRecipients")
    def enable_project_level_recipients(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableProjectLevelRecipients"))

    @enable_project_level_recipients.setter
    def enable_project_level_recipients(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20651ab314c6f000b3dc1d2692b998c8084bc594dba5ef41b0bcbfddb7528052)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableProjectLevelRecipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="monitoringNotificationChannels")
    def monitoring_notification_channels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "monitoringNotificationChannels"))

    @monitoring_notification_channels.setter
    def monitoring_notification_channels(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44245d55f438522ae0d114caceca0edca18be59f835d7e76054905a91681cf66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitoringNotificationChannels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pubsubTopic")
    def pubsub_topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pubsubTopic"))

    @pubsub_topic.setter
    def pubsub_topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5289c0ba665e85ad3e030bcf3ed7e92ad956eb897991381a434f582317ca5bdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pubsubTopic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schemaVersion")
    def schema_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schemaVersion"))

    @schema_version.setter
    def schema_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3125df601f571f9d97c44702ea18233148982748b240609f18307d1b47755f8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schemaVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleBillingBudgetAllUpdatesRule]:
        return typing.cast(typing.Optional[GoogleBillingBudgetAllUpdatesRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBillingBudgetAllUpdatesRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f1735f700da8d416d9b758f8fb8cc88938b76dcd725443531c260b324458c55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBillingBudget.GoogleBillingBudgetAmount",
    jsii_struct_bases=[],
    name_mapping={
        "last_period_amount": "lastPeriodAmount",
        "specified_amount": "specifiedAmount",
    },
)
class GoogleBillingBudgetAmount:
    def __init__(
        self,
        *,
        last_period_amount: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        specified_amount: typing.Optional[typing.Union["GoogleBillingBudgetAmountSpecifiedAmount", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param last_period_amount: Configures a budget amount that is automatically set to 100% of last period's spend. Boolean. Set value to true to use. Do not set to false, instead use the 'specified_amount' block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#last_period_amount GoogleBillingBudget#last_period_amount}
        :param specified_amount: specified_amount block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#specified_amount GoogleBillingBudget#specified_amount}
        '''
        if isinstance(specified_amount, dict):
            specified_amount = GoogleBillingBudgetAmountSpecifiedAmount(**specified_amount)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7084ac84968791be0c5d43f261f538fb5c8e1139292cf87856ba99ef136f9ea2)
            check_type(argname="argument last_period_amount", value=last_period_amount, expected_type=type_hints["last_period_amount"])
            check_type(argname="argument specified_amount", value=specified_amount, expected_type=type_hints["specified_amount"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if last_period_amount is not None:
            self._values["last_period_amount"] = last_period_amount
        if specified_amount is not None:
            self._values["specified_amount"] = specified_amount

    @builtins.property
    def last_period_amount(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Configures a budget amount that is automatically set to 100% of last period's spend.

        Boolean. Set value to true to use. Do not set to false, instead
        use the 'specified_amount' block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#last_period_amount GoogleBillingBudget#last_period_amount}
        '''
        result = self._values.get("last_period_amount")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def specified_amount(
        self,
    ) -> typing.Optional["GoogleBillingBudgetAmountSpecifiedAmount"]:
        '''specified_amount block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#specified_amount GoogleBillingBudget#specified_amount}
        '''
        result = self._values.get("specified_amount")
        return typing.cast(typing.Optional["GoogleBillingBudgetAmountSpecifiedAmount"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBillingBudgetAmount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBillingBudgetAmountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBillingBudget.GoogleBillingBudgetAmountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f952fdea372cee55ee6803776a16d16250e51a669d925d583f3531018abe14ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSpecifiedAmount")
    def put_specified_amount(
        self,
        *,
        currency_code: typing.Optional[builtins.str] = None,
        nanos: typing.Optional[jsii.Number] = None,
        units: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param currency_code: The 3-letter currency code defined in ISO 4217. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#currency_code GoogleBillingBudget#currency_code}
        :param nanos: Number of nano (10^-9) units of the amount. The value must be between -999,999,999 and +999,999,999 inclusive. If units is positive, nanos must be positive or zero. If units is zero, nanos can be positive, zero, or negative. If units is negative, nanos must be negative or zero. For example $-1.75 is represented as units=-1 and nanos=-750,000,000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#nanos GoogleBillingBudget#nanos}
        :param units: The whole units of the amount. For example if currencyCode is "USD", then 1 unit is one US dollar. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#units GoogleBillingBudget#units}
        '''
        value = GoogleBillingBudgetAmountSpecifiedAmount(
            currency_code=currency_code, nanos=nanos, units=units
        )

        return typing.cast(None, jsii.invoke(self, "putSpecifiedAmount", [value]))

    @jsii.member(jsii_name="resetLastPeriodAmount")
    def reset_last_period_amount(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLastPeriodAmount", []))

    @jsii.member(jsii_name="resetSpecifiedAmount")
    def reset_specified_amount(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpecifiedAmount", []))

    @builtins.property
    @jsii.member(jsii_name="specifiedAmount")
    def specified_amount(
        self,
    ) -> "GoogleBillingBudgetAmountSpecifiedAmountOutputReference":
        return typing.cast("GoogleBillingBudgetAmountSpecifiedAmountOutputReference", jsii.get(self, "specifiedAmount"))

    @builtins.property
    @jsii.member(jsii_name="lastPeriodAmountInput")
    def last_period_amount_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "lastPeriodAmountInput"))

    @builtins.property
    @jsii.member(jsii_name="specifiedAmountInput")
    def specified_amount_input(
        self,
    ) -> typing.Optional["GoogleBillingBudgetAmountSpecifiedAmount"]:
        return typing.cast(typing.Optional["GoogleBillingBudgetAmountSpecifiedAmount"], jsii.get(self, "specifiedAmountInput"))

    @builtins.property
    @jsii.member(jsii_name="lastPeriodAmount")
    def last_period_amount(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "lastPeriodAmount"))

    @last_period_amount.setter
    def last_period_amount(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16b51c241412818fef828cf54b1908df6bf0d9eb15903159afa54df7364b07c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lastPeriodAmount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleBillingBudgetAmount]:
        return typing.cast(typing.Optional[GoogleBillingBudgetAmount], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[GoogleBillingBudgetAmount]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2d28ad9b21b83feb411d6c4e4e7f513b5df53032eb24e8d2b3b304f24faf371)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBillingBudget.GoogleBillingBudgetAmountSpecifiedAmount",
    jsii_struct_bases=[],
    name_mapping={"currency_code": "currencyCode", "nanos": "nanos", "units": "units"},
)
class GoogleBillingBudgetAmountSpecifiedAmount:
    def __init__(
        self,
        *,
        currency_code: typing.Optional[builtins.str] = None,
        nanos: typing.Optional[jsii.Number] = None,
        units: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param currency_code: The 3-letter currency code defined in ISO 4217. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#currency_code GoogleBillingBudget#currency_code}
        :param nanos: Number of nano (10^-9) units of the amount. The value must be between -999,999,999 and +999,999,999 inclusive. If units is positive, nanos must be positive or zero. If units is zero, nanos can be positive, zero, or negative. If units is negative, nanos must be negative or zero. For example $-1.75 is represented as units=-1 and nanos=-750,000,000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#nanos GoogleBillingBudget#nanos}
        :param units: The whole units of the amount. For example if currencyCode is "USD", then 1 unit is one US dollar. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#units GoogleBillingBudget#units}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b9a4d4c4ef85cbc7670cee6e9430b2d49fb78e31c9bd5c474791546be0f150a)
            check_type(argname="argument currency_code", value=currency_code, expected_type=type_hints["currency_code"])
            check_type(argname="argument nanos", value=nanos, expected_type=type_hints["nanos"])
            check_type(argname="argument units", value=units, expected_type=type_hints["units"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if currency_code is not None:
            self._values["currency_code"] = currency_code
        if nanos is not None:
            self._values["nanos"] = nanos
        if units is not None:
            self._values["units"] = units

    @builtins.property
    def currency_code(self) -> typing.Optional[builtins.str]:
        '''The 3-letter currency code defined in ISO 4217.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#currency_code GoogleBillingBudget#currency_code}
        '''
        result = self._values.get("currency_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Number of nano (10^-9) units of the amount.

        The value must be between -999,999,999 and +999,999,999
        inclusive. If units is positive, nanos must be positive or
        zero. If units is zero, nanos can be positive, zero, or
        negative. If units is negative, nanos must be negative or
        zero. For example $-1.75 is represented as units=-1 and
        nanos=-750,000,000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#nanos GoogleBillingBudget#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def units(self) -> typing.Optional[builtins.str]:
        '''The whole units of the amount. For example if currencyCode is "USD", then 1 unit is one US dollar.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#units GoogleBillingBudget#units}
        '''
        result = self._values.get("units")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBillingBudgetAmountSpecifiedAmount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBillingBudgetAmountSpecifiedAmountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBillingBudget.GoogleBillingBudgetAmountSpecifiedAmountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5bb82ed161f447e7d8d70027abafc86eb837c2affa1a71a58b4e66bbf465bc6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCurrencyCode")
    def reset_currency_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCurrencyCode", []))

    @jsii.member(jsii_name="resetNanos")
    def reset_nanos(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNanos", []))

    @jsii.member(jsii_name="resetUnits")
    def reset_units(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnits", []))

    @builtins.property
    @jsii.member(jsii_name="currencyCodeInput")
    def currency_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "currencyCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="nanosInput")
    def nanos_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nanosInput"))

    @builtins.property
    @jsii.member(jsii_name="unitsInput")
    def units_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unitsInput"))

    @builtins.property
    @jsii.member(jsii_name="currencyCode")
    def currency_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "currencyCode"))

    @currency_code.setter
    def currency_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0080610b1e1559d096c05db5f10775b509ecb69c9bc30ab043e84eea7aa08c26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "currencyCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d38c0e1628e0adafa85f19dc950e51f2e89f00673ea6147f61ddfc87064d827)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="units")
    def units(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "units"))

    @units.setter
    def units(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__523a86a05b7b0937ec828429f28618654d54528fd3c896e82508500a1d514367)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "units", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleBillingBudgetAmountSpecifiedAmount]:
        return typing.cast(typing.Optional[GoogleBillingBudgetAmountSpecifiedAmount], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBillingBudgetAmountSpecifiedAmount],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78509252991b366afc45ac67e266572f0cde192c11c800bad6cd410fa3b8c8a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBillingBudget.GoogleBillingBudgetBudgetFilter",
    jsii_struct_bases=[],
    name_mapping={
        "calendar_period": "calendarPeriod",
        "credit_types": "creditTypes",
        "credit_types_treatment": "creditTypesTreatment",
        "custom_period": "customPeriod",
        "labels": "labels",
        "projects": "projects",
        "resource_ancestors": "resourceAncestors",
        "services": "services",
        "subaccounts": "subaccounts",
    },
)
class GoogleBillingBudgetBudgetFilter:
    def __init__(
        self,
        *,
        calendar_period: typing.Optional[builtins.str] = None,
        credit_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        credit_types_treatment: typing.Optional[builtins.str] = None,
        custom_period: typing.Optional[typing.Union["GoogleBillingBudgetBudgetFilterCustomPeriod", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        projects: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_ancestors: typing.Optional[typing.Sequence[builtins.str]] = None,
        services: typing.Optional[typing.Sequence[builtins.str]] = None,
        subaccounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param calendar_period: A CalendarPeriod represents the abstract concept of a recurring time period that has a canonical start. Grammatically, "the start of the current CalendarPeriod". All calendar times begin at 12 AM US and Canadian Pacific Time (UTC-8). Exactly one of 'calendar_period', 'custom_period' must be provided. Possible values: ["MONTH", "QUARTER", "YEAR", "CALENDAR_PERIOD_UNSPECIFIED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#calendar_period GoogleBillingBudget#calendar_period}
        :param credit_types: Optional. If creditTypesTreatment is INCLUDE_SPECIFIED_CREDITS, this is a list of credit types to be subtracted from gross cost to determine the spend for threshold calculations. See a list of acceptable credit type values. If creditTypesTreatment is not INCLUDE_SPECIFIED_CREDITS, this field must be empty. **Note:** If the field has a value in the config and needs to be removed, the field has to be an empty array in the config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#credit_types GoogleBillingBudget#credit_types}
        :param credit_types_treatment: Specifies how credits should be treated when determining spend for threshold calculations. Default value: "INCLUDE_ALL_CREDITS" Possible values: ["INCLUDE_ALL_CREDITS", "EXCLUDE_ALL_CREDITS", "INCLUDE_SPECIFIED_CREDITS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#credit_types_treatment GoogleBillingBudget#credit_types_treatment}
        :param custom_period: custom_period block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#custom_period GoogleBillingBudget#custom_period}
        :param labels: A single label and value pair specifying that usage from only this set of labeled resources should be included in the budget. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#labels GoogleBillingBudget#labels}
        :param projects: A set of projects of the form projects/{project_number}, specifying that usage from only this set of projects should be included in the budget. If omitted, the report will include all usage for the billing account, regardless of which project the usage occurred on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#projects GoogleBillingBudget#projects}
        :param resource_ancestors: A set of folder and organization names of the form folders/{folderId} or organizations/{organizationId}, specifying that usage from only this set of folders and organizations should be included in the budget. If omitted, the budget includes all usage that the billing account pays for. If the folder or organization contains projects that are paid for by a different Cloud Billing account, the budget doesn't apply to those projects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#resource_ancestors GoogleBillingBudget#resource_ancestors}
        :param services: A set of services of the form services/{service_id}, specifying that usage from only this set of services should be included in the budget. If omitted, the report will include usage for all the services. The service names are available through the Catalog API: https://cloud.google.com/billing/v1/how-tos/catalog-api. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#services GoogleBillingBudget#services}
        :param subaccounts: A set of subaccounts of the form billingAccounts/{account_id}, specifying that usage from only this set of subaccounts should be included in the budget. If a subaccount is set to the name of the parent account, usage from the parent account will be included. If the field is omitted, the report will include usage from the parent account and all subaccounts, if they exist. **Note:** If the field has a value in the config and needs to be removed, the field has to be an empty array in the config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#subaccounts GoogleBillingBudget#subaccounts}
        '''
        if isinstance(custom_period, dict):
            custom_period = GoogleBillingBudgetBudgetFilterCustomPeriod(**custom_period)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42f80f23ea2a0deed8b600b2b0517e0407cffc06bac553621768321879b1b912)
            check_type(argname="argument calendar_period", value=calendar_period, expected_type=type_hints["calendar_period"])
            check_type(argname="argument credit_types", value=credit_types, expected_type=type_hints["credit_types"])
            check_type(argname="argument credit_types_treatment", value=credit_types_treatment, expected_type=type_hints["credit_types_treatment"])
            check_type(argname="argument custom_period", value=custom_period, expected_type=type_hints["custom_period"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument projects", value=projects, expected_type=type_hints["projects"])
            check_type(argname="argument resource_ancestors", value=resource_ancestors, expected_type=type_hints["resource_ancestors"])
            check_type(argname="argument services", value=services, expected_type=type_hints["services"])
            check_type(argname="argument subaccounts", value=subaccounts, expected_type=type_hints["subaccounts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if calendar_period is not None:
            self._values["calendar_period"] = calendar_period
        if credit_types is not None:
            self._values["credit_types"] = credit_types
        if credit_types_treatment is not None:
            self._values["credit_types_treatment"] = credit_types_treatment
        if custom_period is not None:
            self._values["custom_period"] = custom_period
        if labels is not None:
            self._values["labels"] = labels
        if projects is not None:
            self._values["projects"] = projects
        if resource_ancestors is not None:
            self._values["resource_ancestors"] = resource_ancestors
        if services is not None:
            self._values["services"] = services
        if subaccounts is not None:
            self._values["subaccounts"] = subaccounts

    @builtins.property
    def calendar_period(self) -> typing.Optional[builtins.str]:
        '''A CalendarPeriod represents the abstract concept of a recurring time period that has a canonical start.

        Grammatically, "the start of the current CalendarPeriod".
        All calendar times begin at 12 AM US and Canadian Pacific Time (UTC-8).

        Exactly one of 'calendar_period', 'custom_period' must be provided. Possible values: ["MONTH", "QUARTER", "YEAR", "CALENDAR_PERIOD_UNSPECIFIED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#calendar_period GoogleBillingBudget#calendar_period}
        '''
        result = self._values.get("calendar_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def credit_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        If creditTypesTreatment is INCLUDE_SPECIFIED_CREDITS,
        this is a list of credit types to be subtracted from gross cost to determine the spend for threshold calculations. See a list of acceptable credit type values.
        If creditTypesTreatment is not INCLUDE_SPECIFIED_CREDITS, this field must be empty.

        **Note:** If the field has a value in the config and needs to be removed, the field has to be an empty array in the config.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#credit_types GoogleBillingBudget#credit_types}
        '''
        result = self._values.get("credit_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def credit_types_treatment(self) -> typing.Optional[builtins.str]:
        '''Specifies how credits should be treated when determining spend for threshold calculations. Default value: "INCLUDE_ALL_CREDITS" Possible values: ["INCLUDE_ALL_CREDITS", "EXCLUDE_ALL_CREDITS", "INCLUDE_SPECIFIED_CREDITS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#credit_types_treatment GoogleBillingBudget#credit_types_treatment}
        '''
        result = self._values.get("credit_types_treatment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_period(
        self,
    ) -> typing.Optional["GoogleBillingBudgetBudgetFilterCustomPeriod"]:
        '''custom_period block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#custom_period GoogleBillingBudget#custom_period}
        '''
        result = self._values.get("custom_period")
        return typing.cast(typing.Optional["GoogleBillingBudgetBudgetFilterCustomPeriod"], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A single label and value pair specifying that usage from only this set of labeled resources should be included in the budget.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#labels GoogleBillingBudget#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def projects(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A set of projects of the form projects/{project_number}, specifying that usage from only this set of projects should be included in the budget.

        If omitted, the report will include
        all usage for the billing account, regardless of which project
        the usage occurred on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#projects GoogleBillingBudget#projects}
        '''
        result = self._values.get("projects")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resource_ancestors(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A set of folder and organization names of the form folders/{folderId} or organizations/{organizationId}, specifying that usage from only this set of folders and organizations should be included in the budget.

        If omitted, the budget includes all usage that the billing account pays for. If the folder or organization
        contains projects that are paid for by a different Cloud Billing account, the budget doesn't apply to those projects.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#resource_ancestors GoogleBillingBudget#resource_ancestors}
        '''
        result = self._values.get("resource_ancestors")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def services(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A set of services of the form services/{service_id}, specifying that usage from only this set of services should be included in the budget.

        If omitted, the report will include
        usage for all the services. The service names are available
        through the Catalog API:
        https://cloud.google.com/billing/v1/how-tos/catalog-api.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#services GoogleBillingBudget#services}
        '''
        result = self._values.get("services")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subaccounts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A set of subaccounts of the form billingAccounts/{account_id}, specifying that usage from only this set of subaccounts should be included in the budget.

        If a subaccount is set to the name of
        the parent account, usage from the parent account will be included.
        If the field is omitted, the report will include usage from the parent
        account and all subaccounts, if they exist.

        **Note:** If the field has a value in the config and needs to be removed, the field has to be an empty array in the config.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#subaccounts GoogleBillingBudget#subaccounts}
        '''
        result = self._values.get("subaccounts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBillingBudgetBudgetFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBillingBudget.GoogleBillingBudgetBudgetFilterCustomPeriod",
    jsii_struct_bases=[],
    name_mapping={"start_date": "startDate", "end_date": "endDate"},
)
class GoogleBillingBudgetBudgetFilterCustomPeriod:
    def __init__(
        self,
        *,
        start_date: typing.Union["GoogleBillingBudgetBudgetFilterCustomPeriodStartDate", typing.Dict[builtins.str, typing.Any]],
        end_date: typing.Optional[typing.Union["GoogleBillingBudgetBudgetFilterCustomPeriodEndDate", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param start_date: start_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#start_date GoogleBillingBudget#start_date}
        :param end_date: end_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#end_date GoogleBillingBudget#end_date}
        '''
        if isinstance(start_date, dict):
            start_date = GoogleBillingBudgetBudgetFilterCustomPeriodStartDate(**start_date)
        if isinstance(end_date, dict):
            end_date = GoogleBillingBudgetBudgetFilterCustomPeriodEndDate(**end_date)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f3e7c69e658254178f2a55143a5ae494c69e21473bfb4bd15a097e08856a6b2)
            check_type(argname="argument start_date", value=start_date, expected_type=type_hints["start_date"])
            check_type(argname="argument end_date", value=end_date, expected_type=type_hints["end_date"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "start_date": start_date,
        }
        if end_date is not None:
            self._values["end_date"] = end_date

    @builtins.property
    def start_date(self) -> "GoogleBillingBudgetBudgetFilterCustomPeriodStartDate":
        '''start_date block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#start_date GoogleBillingBudget#start_date}
        '''
        result = self._values.get("start_date")
        assert result is not None, "Required property 'start_date' is missing"
        return typing.cast("GoogleBillingBudgetBudgetFilterCustomPeriodStartDate", result)

    @builtins.property
    def end_date(
        self,
    ) -> typing.Optional["GoogleBillingBudgetBudgetFilterCustomPeriodEndDate"]:
        '''end_date block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#end_date GoogleBillingBudget#end_date}
        '''
        result = self._values.get("end_date")
        return typing.cast(typing.Optional["GoogleBillingBudgetBudgetFilterCustomPeriodEndDate"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBillingBudgetBudgetFilterCustomPeriod(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBillingBudget.GoogleBillingBudgetBudgetFilterCustomPeriodEndDate",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "month": "month", "year": "year"},
)
class GoogleBillingBudgetBudgetFilterCustomPeriodEndDate:
    def __init__(
        self,
        *,
        day: jsii.Number,
        month: jsii.Number,
        year: jsii.Number,
    ) -> None:
        '''
        :param day: Day of a month. Must be from 1 to 31 and valid for the year and month. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#day GoogleBillingBudget#day}
        :param month: Month of a year. Must be from 1 to 12. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#month GoogleBillingBudget#month}
        :param year: Year of the date. Must be from 1 to 9999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#year GoogleBillingBudget#year}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50b743ccc24ee85343240e3d0e35ea0c8362f19c1849726cf62b19a4c598ee50)
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
            check_type(argname="argument month", value=month, expected_type=type_hints["month"])
            check_type(argname="argument year", value=year, expected_type=type_hints["year"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "day": day,
            "month": month,
            "year": year,
        }

    @builtins.property
    def day(self) -> jsii.Number:
        '''Day of a month. Must be from 1 to 31 and valid for the year and month.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#day GoogleBillingBudget#day}
        '''
        result = self._values.get("day")
        assert result is not None, "Required property 'day' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def month(self) -> jsii.Number:
        '''Month of a year. Must be from 1 to 12.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#month GoogleBillingBudget#month}
        '''
        result = self._values.get("month")
        assert result is not None, "Required property 'month' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def year(self) -> jsii.Number:
        '''Year of the date. Must be from 1 to 9999.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#year GoogleBillingBudget#year}
        '''
        result = self._values.get("year")
        assert result is not None, "Required property 'year' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBillingBudgetBudgetFilterCustomPeriodEndDate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBillingBudgetBudgetFilterCustomPeriodEndDateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBillingBudget.GoogleBillingBudgetBudgetFilterCustomPeriodEndDateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed41a0fdbb8cc95fddcbaa182f7cc454274a35aef8bc077d05c4fb393b292bb6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="dayInput")
    def day_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dayInput"))

    @builtins.property
    @jsii.member(jsii_name="monthInput")
    def month_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "monthInput"))

    @builtins.property
    @jsii.member(jsii_name="yearInput")
    def year_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "yearInput"))

    @builtins.property
    @jsii.member(jsii_name="day")
    def day(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "day"))

    @day.setter
    def day(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c37543cd06f90baf3a1b02ab9df5098ed83f27336e9da43f1c24917ef9174fef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="month")
    def month(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "month"))

    @month.setter
    def month(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63796adc3b681c1b9b482ebf971e80a4a2cdf1c95715832fcd0f3aa96bd85fdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "month", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="year")
    def year(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "year"))

    @year.setter
    def year(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd67e8d015f645c38567fd4674d5f25c41be6e4ef0de3cc12d0f18d971e3365a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "year", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleBillingBudgetBudgetFilterCustomPeriodEndDate]:
        return typing.cast(typing.Optional[GoogleBillingBudgetBudgetFilterCustomPeriodEndDate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBillingBudgetBudgetFilterCustomPeriodEndDate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc709bd0fc8219a2b5ef49a36c2cb18a5a8d81528f3d435897a89b51501c150b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleBillingBudgetBudgetFilterCustomPeriodOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBillingBudget.GoogleBillingBudgetBudgetFilterCustomPeriodOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__031bfac227dadf1484104c327be05a9c8939fe54047c302fd47a836de0276c72)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEndDate")
    def put_end_date(
        self,
        *,
        day: jsii.Number,
        month: jsii.Number,
        year: jsii.Number,
    ) -> None:
        '''
        :param day: Day of a month. Must be from 1 to 31 and valid for the year and month. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#day GoogleBillingBudget#day}
        :param month: Month of a year. Must be from 1 to 12. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#month GoogleBillingBudget#month}
        :param year: Year of the date. Must be from 1 to 9999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#year GoogleBillingBudget#year}
        '''
        value = GoogleBillingBudgetBudgetFilterCustomPeriodEndDate(
            day=day, month=month, year=year
        )

        return typing.cast(None, jsii.invoke(self, "putEndDate", [value]))

    @jsii.member(jsii_name="putStartDate")
    def put_start_date(
        self,
        *,
        day: jsii.Number,
        month: jsii.Number,
        year: jsii.Number,
    ) -> None:
        '''
        :param day: Day of a month. Must be from 1 to 31 and valid for the year and month. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#day GoogleBillingBudget#day}
        :param month: Month of a year. Must be from 1 to 12. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#month GoogleBillingBudget#month}
        :param year: Year of the date. Must be from 1 to 9999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#year GoogleBillingBudget#year}
        '''
        value = GoogleBillingBudgetBudgetFilterCustomPeriodStartDate(
            day=day, month=month, year=year
        )

        return typing.cast(None, jsii.invoke(self, "putStartDate", [value]))

    @jsii.member(jsii_name="resetEndDate")
    def reset_end_date(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndDate", []))

    @builtins.property
    @jsii.member(jsii_name="endDate")
    def end_date(
        self,
    ) -> GoogleBillingBudgetBudgetFilterCustomPeriodEndDateOutputReference:
        return typing.cast(GoogleBillingBudgetBudgetFilterCustomPeriodEndDateOutputReference, jsii.get(self, "endDate"))

    @builtins.property
    @jsii.member(jsii_name="startDate")
    def start_date(
        self,
    ) -> "GoogleBillingBudgetBudgetFilterCustomPeriodStartDateOutputReference":
        return typing.cast("GoogleBillingBudgetBudgetFilterCustomPeriodStartDateOutputReference", jsii.get(self, "startDate"))

    @builtins.property
    @jsii.member(jsii_name="endDateInput")
    def end_date_input(
        self,
    ) -> typing.Optional[GoogleBillingBudgetBudgetFilterCustomPeriodEndDate]:
        return typing.cast(typing.Optional[GoogleBillingBudgetBudgetFilterCustomPeriodEndDate], jsii.get(self, "endDateInput"))

    @builtins.property
    @jsii.member(jsii_name="startDateInput")
    def start_date_input(
        self,
    ) -> typing.Optional["GoogleBillingBudgetBudgetFilterCustomPeriodStartDate"]:
        return typing.cast(typing.Optional["GoogleBillingBudgetBudgetFilterCustomPeriodStartDate"], jsii.get(self, "startDateInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleBillingBudgetBudgetFilterCustomPeriod]:
        return typing.cast(typing.Optional[GoogleBillingBudgetBudgetFilterCustomPeriod], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBillingBudgetBudgetFilterCustomPeriod],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f67c72d3924b4da8625322135e84ee51b58eb01cbb724e559d2f332f8b05d82d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBillingBudget.GoogleBillingBudgetBudgetFilterCustomPeriodStartDate",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "month": "month", "year": "year"},
)
class GoogleBillingBudgetBudgetFilterCustomPeriodStartDate:
    def __init__(
        self,
        *,
        day: jsii.Number,
        month: jsii.Number,
        year: jsii.Number,
    ) -> None:
        '''
        :param day: Day of a month. Must be from 1 to 31 and valid for the year and month. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#day GoogleBillingBudget#day}
        :param month: Month of a year. Must be from 1 to 12. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#month GoogleBillingBudget#month}
        :param year: Year of the date. Must be from 1 to 9999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#year GoogleBillingBudget#year}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50b4608751836a7be2fbb389d6f2160df1f272e6ef3f5bd35750157c9ddd70f0)
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
            check_type(argname="argument month", value=month, expected_type=type_hints["month"])
            check_type(argname="argument year", value=year, expected_type=type_hints["year"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "day": day,
            "month": month,
            "year": year,
        }

    @builtins.property
    def day(self) -> jsii.Number:
        '''Day of a month. Must be from 1 to 31 and valid for the year and month.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#day GoogleBillingBudget#day}
        '''
        result = self._values.get("day")
        assert result is not None, "Required property 'day' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def month(self) -> jsii.Number:
        '''Month of a year. Must be from 1 to 12.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#month GoogleBillingBudget#month}
        '''
        result = self._values.get("month")
        assert result is not None, "Required property 'month' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def year(self) -> jsii.Number:
        '''Year of the date. Must be from 1 to 9999.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#year GoogleBillingBudget#year}
        '''
        result = self._values.get("year")
        assert result is not None, "Required property 'year' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBillingBudgetBudgetFilterCustomPeriodStartDate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBillingBudgetBudgetFilterCustomPeriodStartDateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBillingBudget.GoogleBillingBudgetBudgetFilterCustomPeriodStartDateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f97e271c7ed756822a17a0f46ec0f52ee99ab5e861c44fc51c7d0c4a8b64075f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="dayInput")
    def day_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dayInput"))

    @builtins.property
    @jsii.member(jsii_name="monthInput")
    def month_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "monthInput"))

    @builtins.property
    @jsii.member(jsii_name="yearInput")
    def year_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "yearInput"))

    @builtins.property
    @jsii.member(jsii_name="day")
    def day(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "day"))

    @day.setter
    def day(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05be8837b08aecd6e195c7d3bdc4198aac220740fb7782798389d48574b784fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="month")
    def month(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "month"))

    @month.setter
    def month(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__953cb7e2fb4ce3fd598fc2c54bca60fb6dce945fca94d7a52b99e67072faf137)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "month", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="year")
    def year(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "year"))

    @year.setter
    def year(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df7189419d9e44fbe9f53548d3f3c33d6adb2a7958c4dbec1646e75f1ba4184b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "year", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleBillingBudgetBudgetFilterCustomPeriodStartDate]:
        return typing.cast(typing.Optional[GoogleBillingBudgetBudgetFilterCustomPeriodStartDate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBillingBudgetBudgetFilterCustomPeriodStartDate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36e281d942ef5a747a8515f06b069b96c21f0166813d68545fe27911523fbdb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleBillingBudgetBudgetFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBillingBudget.GoogleBillingBudgetBudgetFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b17f2fc0e156cbb18fddcd22dcc5b3d85d2397e4e73f46682a5ededd1f2a7a7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomPeriod")
    def put_custom_period(
        self,
        *,
        start_date: typing.Union[GoogleBillingBudgetBudgetFilterCustomPeriodStartDate, typing.Dict[builtins.str, typing.Any]],
        end_date: typing.Optional[typing.Union[GoogleBillingBudgetBudgetFilterCustomPeriodEndDate, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param start_date: start_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#start_date GoogleBillingBudget#start_date}
        :param end_date: end_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#end_date GoogleBillingBudget#end_date}
        '''
        value = GoogleBillingBudgetBudgetFilterCustomPeriod(
            start_date=start_date, end_date=end_date
        )

        return typing.cast(None, jsii.invoke(self, "putCustomPeriod", [value]))

    @jsii.member(jsii_name="resetCalendarPeriod")
    def reset_calendar_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCalendarPeriod", []))

    @jsii.member(jsii_name="resetCreditTypes")
    def reset_credit_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreditTypes", []))

    @jsii.member(jsii_name="resetCreditTypesTreatment")
    def reset_credit_types_treatment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreditTypesTreatment", []))

    @jsii.member(jsii_name="resetCustomPeriod")
    def reset_custom_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomPeriod", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetProjects")
    def reset_projects(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjects", []))

    @jsii.member(jsii_name="resetResourceAncestors")
    def reset_resource_ancestors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceAncestors", []))

    @jsii.member(jsii_name="resetServices")
    def reset_services(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServices", []))

    @jsii.member(jsii_name="resetSubaccounts")
    def reset_subaccounts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubaccounts", []))

    @builtins.property
    @jsii.member(jsii_name="customPeriod")
    def custom_period(
        self,
    ) -> GoogleBillingBudgetBudgetFilterCustomPeriodOutputReference:
        return typing.cast(GoogleBillingBudgetBudgetFilterCustomPeriodOutputReference, jsii.get(self, "customPeriod"))

    @builtins.property
    @jsii.member(jsii_name="calendarPeriodInput")
    def calendar_period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "calendarPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="creditTypesInput")
    def credit_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "creditTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="creditTypesTreatmentInput")
    def credit_types_treatment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "creditTypesTreatmentInput"))

    @builtins.property
    @jsii.member(jsii_name="customPeriodInput")
    def custom_period_input(
        self,
    ) -> typing.Optional[GoogleBillingBudgetBudgetFilterCustomPeriod]:
        return typing.cast(typing.Optional[GoogleBillingBudgetBudgetFilterCustomPeriod], jsii.get(self, "customPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="projectsInput")
    def projects_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "projectsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceAncestorsInput")
    def resource_ancestors_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceAncestorsInput"))

    @builtins.property
    @jsii.member(jsii_name="servicesInput")
    def services_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "servicesInput"))

    @builtins.property
    @jsii.member(jsii_name="subaccountsInput")
    def subaccounts_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subaccountsInput"))

    @builtins.property
    @jsii.member(jsii_name="calendarPeriod")
    def calendar_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "calendarPeriod"))

    @calendar_period.setter
    def calendar_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8ffad16727a3de0680ce3d1ae7240700d3bbb564e021598124c225455863762)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "calendarPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="creditTypes")
    def credit_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "creditTypes"))

    @credit_types.setter
    def credit_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ededb810187dcab5660db8a8a4fccce8393281038e7a17a690dc5dc4ee8897d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "creditTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="creditTypesTreatment")
    def credit_types_treatment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creditTypesTreatment"))

    @credit_types_treatment.setter
    def credit_types_treatment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b452cdb8ed1dd384305e9ea4922d9576d15a7478507953fd3dbf3d526ef561f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "creditTypesTreatment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69b48bb4b190d752c7bfaca37e92b185a0262c2f574e8ac940f579f0c1f7232d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projects")
    def projects(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "projects"))

    @projects.setter
    def projects(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfdbd96a353f3771ef566db2bfc7b6a01c15a3fa09a8ffe5655951a51c17a3be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projects", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceAncestors")
    def resource_ancestors(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceAncestors"))

    @resource_ancestors.setter
    def resource_ancestors(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07ff3b549123fdac54cee0c68453990e0a9cf712ca417bebdac261173537d20a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceAncestors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="services")
    def services(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "services"))

    @services.setter
    def services(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65b44add76ab0f9c2c311142e90ac03bac2caa1451aeb950e29b8509bd1f56af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "services", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subaccounts")
    def subaccounts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subaccounts"))

    @subaccounts.setter
    def subaccounts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__256cebfdb86e8ab2cecffd296d89eb0b1d8db7e58b78de9a9a59d36b8f211c1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subaccounts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleBillingBudgetBudgetFilter]:
        return typing.cast(typing.Optional[GoogleBillingBudgetBudgetFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBillingBudgetBudgetFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d709bf198b65d8256966bf7b0571868482991c5eeaa7287ff283eafc11aaa094)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBillingBudget.GoogleBillingBudgetConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "amount": "amount",
        "billing_account": "billingAccount",
        "all_updates_rule": "allUpdatesRule",
        "budget_filter": "budgetFilter",
        "display_name": "displayName",
        "id": "id",
        "ownership_scope": "ownershipScope",
        "threshold_rules": "thresholdRules",
        "timeouts": "timeouts",
    },
)
class GoogleBillingBudgetConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        amount: typing.Union[GoogleBillingBudgetAmount, typing.Dict[builtins.str, typing.Any]],
        billing_account: builtins.str,
        all_updates_rule: typing.Optional[typing.Union[GoogleBillingBudgetAllUpdatesRule, typing.Dict[builtins.str, typing.Any]]] = None,
        budget_filter: typing.Optional[typing.Union[GoogleBillingBudgetBudgetFilter, typing.Dict[builtins.str, typing.Any]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ownership_scope: typing.Optional[builtins.str] = None,
        threshold_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleBillingBudgetThresholdRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleBillingBudgetTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param amount: amount block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#amount GoogleBillingBudget#amount}
        :param billing_account: ID of the billing account to set a budget on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#billing_account GoogleBillingBudget#billing_account}
        :param all_updates_rule: all_updates_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#all_updates_rule GoogleBillingBudget#all_updates_rule}
        :param budget_filter: budget_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#budget_filter GoogleBillingBudget#budget_filter}
        :param display_name: User data for display name in UI. Must be <= 60 chars. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#display_name GoogleBillingBudget#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#id GoogleBillingBudget#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ownership_scope: The ownership scope of the budget. The ownership scope and users' IAM permissions determine who has full access to the budget's data. Possible values: ["OWNERSHIP_SCOPE_UNSPECIFIED", "ALL_USERS", "BILLING_ACCOUNT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#ownership_scope GoogleBillingBudget#ownership_scope}
        :param threshold_rules: threshold_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#threshold_rules GoogleBillingBudget#threshold_rules}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#timeouts GoogleBillingBudget#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(amount, dict):
            amount = GoogleBillingBudgetAmount(**amount)
        if isinstance(all_updates_rule, dict):
            all_updates_rule = GoogleBillingBudgetAllUpdatesRule(**all_updates_rule)
        if isinstance(budget_filter, dict):
            budget_filter = GoogleBillingBudgetBudgetFilter(**budget_filter)
        if isinstance(timeouts, dict):
            timeouts = GoogleBillingBudgetTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c52d4b123b059a691da40753c8a68f816373e2b63c1fa2df789c5dfbe74163e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument amount", value=amount, expected_type=type_hints["amount"])
            check_type(argname="argument billing_account", value=billing_account, expected_type=type_hints["billing_account"])
            check_type(argname="argument all_updates_rule", value=all_updates_rule, expected_type=type_hints["all_updates_rule"])
            check_type(argname="argument budget_filter", value=budget_filter, expected_type=type_hints["budget_filter"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ownership_scope", value=ownership_scope, expected_type=type_hints["ownership_scope"])
            check_type(argname="argument threshold_rules", value=threshold_rules, expected_type=type_hints["threshold_rules"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "amount": amount,
            "billing_account": billing_account,
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
        if all_updates_rule is not None:
            self._values["all_updates_rule"] = all_updates_rule
        if budget_filter is not None:
            self._values["budget_filter"] = budget_filter
        if display_name is not None:
            self._values["display_name"] = display_name
        if id is not None:
            self._values["id"] = id
        if ownership_scope is not None:
            self._values["ownership_scope"] = ownership_scope
        if threshold_rules is not None:
            self._values["threshold_rules"] = threshold_rules
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
    def amount(self) -> GoogleBillingBudgetAmount:
        '''amount block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#amount GoogleBillingBudget#amount}
        '''
        result = self._values.get("amount")
        assert result is not None, "Required property 'amount' is missing"
        return typing.cast(GoogleBillingBudgetAmount, result)

    @builtins.property
    def billing_account(self) -> builtins.str:
        '''ID of the billing account to set a budget on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#billing_account GoogleBillingBudget#billing_account}
        '''
        result = self._values.get("billing_account")
        assert result is not None, "Required property 'billing_account' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def all_updates_rule(self) -> typing.Optional[GoogleBillingBudgetAllUpdatesRule]:
        '''all_updates_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#all_updates_rule GoogleBillingBudget#all_updates_rule}
        '''
        result = self._values.get("all_updates_rule")
        return typing.cast(typing.Optional[GoogleBillingBudgetAllUpdatesRule], result)

    @builtins.property
    def budget_filter(self) -> typing.Optional[GoogleBillingBudgetBudgetFilter]:
        '''budget_filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#budget_filter GoogleBillingBudget#budget_filter}
        '''
        result = self._values.get("budget_filter")
        return typing.cast(typing.Optional[GoogleBillingBudgetBudgetFilter], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''User data for display name in UI. Must be <= 60 chars.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#display_name GoogleBillingBudget#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#id GoogleBillingBudget#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ownership_scope(self) -> typing.Optional[builtins.str]:
        '''The ownership scope of the budget.

        The ownership scope and users'
        IAM permissions determine who has full access to the budget's data. Possible values: ["OWNERSHIP_SCOPE_UNSPECIFIED", "ALL_USERS", "BILLING_ACCOUNT"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#ownership_scope GoogleBillingBudget#ownership_scope}
        '''
        result = self._values.get("ownership_scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def threshold_rules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBillingBudgetThresholdRules"]]]:
        '''threshold_rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#threshold_rules GoogleBillingBudget#threshold_rules}
        '''
        result = self._values.get("threshold_rules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBillingBudgetThresholdRules"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleBillingBudgetTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#timeouts GoogleBillingBudget#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleBillingBudgetTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBillingBudgetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBillingBudget.GoogleBillingBudgetThresholdRules",
    jsii_struct_bases=[],
    name_mapping={
        "threshold_percent": "thresholdPercent",
        "spend_basis": "spendBasis",
    },
)
class GoogleBillingBudgetThresholdRules:
    def __init__(
        self,
        *,
        threshold_percent: jsii.Number,
        spend_basis: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param threshold_percent: Send an alert when this threshold is exceeded. This is a 1.0-based percentage, so 0.5 = 50%. Must be >= 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#threshold_percent GoogleBillingBudget#threshold_percent}
        :param spend_basis: The type of basis used to determine if spend has passed the threshold. Default value: "CURRENT_SPEND" Possible values: ["CURRENT_SPEND", "FORECASTED_SPEND"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#spend_basis GoogleBillingBudget#spend_basis}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2884dfd304939f84a14b72bc8c7d1592d12d9c48d1b1b929df6624a9a0a8646a)
            check_type(argname="argument threshold_percent", value=threshold_percent, expected_type=type_hints["threshold_percent"])
            check_type(argname="argument spend_basis", value=spend_basis, expected_type=type_hints["spend_basis"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "threshold_percent": threshold_percent,
        }
        if spend_basis is not None:
            self._values["spend_basis"] = spend_basis

    @builtins.property
    def threshold_percent(self) -> jsii.Number:
        '''Send an alert when this threshold is exceeded.

        This is a
        1.0-based percentage, so 0.5 = 50%. Must be >= 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#threshold_percent GoogleBillingBudget#threshold_percent}
        '''
        result = self._values.get("threshold_percent")
        assert result is not None, "Required property 'threshold_percent' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def spend_basis(self) -> typing.Optional[builtins.str]:
        '''The type of basis used to determine if spend has passed the threshold. Default value: "CURRENT_SPEND" Possible values: ["CURRENT_SPEND", "FORECASTED_SPEND"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#spend_basis GoogleBillingBudget#spend_basis}
        '''
        result = self._values.get("spend_basis")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBillingBudgetThresholdRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBillingBudgetThresholdRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBillingBudget.GoogleBillingBudgetThresholdRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57c323302b1d52e3ca8d116a8f5e60e139062c91a8ca7e98865d46d1e747cbd5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleBillingBudgetThresholdRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e121f4c90781a17049c8271ffc6f212a916402a06a4a5386feb99cbf9e512dc2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleBillingBudgetThresholdRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8e258afe3720157a572bb0a319dec642282149be5427dee453851fcb473a2a3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd972042af7cae2a300600a531ceab60de69e732b37f4840901733645f2915a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1dc05c6d8acb56862d0244aaaad41f7b8a490953bc00e7c9971065e057db0af2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBillingBudgetThresholdRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBillingBudgetThresholdRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBillingBudgetThresholdRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f20987d3adc1d60c73f36b5f4c30940b90d98d35b038a126749630d0315c23c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleBillingBudgetThresholdRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBillingBudget.GoogleBillingBudgetThresholdRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__43b446ad4a7e47070b8504674b9d919fa10620bd7d131c5801f83c69b8f227ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSpendBasis")
    def reset_spend_basis(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpendBasis", []))

    @builtins.property
    @jsii.member(jsii_name="spendBasisInput")
    def spend_basis_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "spendBasisInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdPercentInput")
    def threshold_percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "thresholdPercentInput"))

    @builtins.property
    @jsii.member(jsii_name="spendBasis")
    def spend_basis(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "spendBasis"))

    @spend_basis.setter
    def spend_basis(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__177732d1f72dbc4598f63ae0b51f41236581ab9991a26254aba46011b8272128)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spendBasis", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="thresholdPercent")
    def threshold_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "thresholdPercent"))

    @threshold_percent.setter
    def threshold_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__825cca1819ece02a58d237aacfd76bae657d1e93a6b9f8a10835dc508109d0d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thresholdPercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBillingBudgetThresholdRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBillingBudgetThresholdRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBillingBudgetThresholdRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__349e489a0674c14e561d323e2f23a34e98a003c2f5ed178ec15e195d2428a3c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBillingBudget.GoogleBillingBudgetTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleBillingBudgetTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#create GoogleBillingBudget#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#delete GoogleBillingBudget#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#update GoogleBillingBudget#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe667b31e4d8f1fc562c50e0afdd9c380f4abe8098aa0e7470bdda4e915feb33)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#create GoogleBillingBudget#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#delete GoogleBillingBudget#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_billing_budget#update GoogleBillingBudget#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBillingBudgetTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBillingBudgetTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBillingBudget.GoogleBillingBudgetTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ddbc7e3ed0e2f85325dd038f1724444ef59de24cd223a5091acdeff588e923f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d8b25f6086a8537e9ca15ed6b85222139ee0d538841189812ae90fcd0c7c773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__404b0f3eda86b24a342be094db2eeaab98929eadf1982e8e7ebc7ba47d0c63d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__365404516589ebf114ee7b28ef63141e3f7d41c47a1b88877774a9003c5ea3fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBillingBudgetTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBillingBudgetTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBillingBudgetTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a2f69a9bf94386edf245fa39f0db63d061088c641a910c6d02078d56ac4f503)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleBillingBudget",
    "GoogleBillingBudgetAllUpdatesRule",
    "GoogleBillingBudgetAllUpdatesRuleOutputReference",
    "GoogleBillingBudgetAmount",
    "GoogleBillingBudgetAmountOutputReference",
    "GoogleBillingBudgetAmountSpecifiedAmount",
    "GoogleBillingBudgetAmountSpecifiedAmountOutputReference",
    "GoogleBillingBudgetBudgetFilter",
    "GoogleBillingBudgetBudgetFilterCustomPeriod",
    "GoogleBillingBudgetBudgetFilterCustomPeriodEndDate",
    "GoogleBillingBudgetBudgetFilterCustomPeriodEndDateOutputReference",
    "GoogleBillingBudgetBudgetFilterCustomPeriodOutputReference",
    "GoogleBillingBudgetBudgetFilterCustomPeriodStartDate",
    "GoogleBillingBudgetBudgetFilterCustomPeriodStartDateOutputReference",
    "GoogleBillingBudgetBudgetFilterOutputReference",
    "GoogleBillingBudgetConfig",
    "GoogleBillingBudgetThresholdRules",
    "GoogleBillingBudgetThresholdRulesList",
    "GoogleBillingBudgetThresholdRulesOutputReference",
    "GoogleBillingBudgetTimeouts",
    "GoogleBillingBudgetTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__b4e7c06110316e69b0d05657484388e3ff765d48a293200b2d2347bbd240412e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    amount: typing.Union[GoogleBillingBudgetAmount, typing.Dict[builtins.str, typing.Any]],
    billing_account: builtins.str,
    all_updates_rule: typing.Optional[typing.Union[GoogleBillingBudgetAllUpdatesRule, typing.Dict[builtins.str, typing.Any]]] = None,
    budget_filter: typing.Optional[typing.Union[GoogleBillingBudgetBudgetFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ownership_scope: typing.Optional[builtins.str] = None,
    threshold_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleBillingBudgetThresholdRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleBillingBudgetTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__9bf3e976a39bcd3ceb697f62fe3be425921fed0363274dd5526f1e98a8c59948(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb5bb0b39a81bac5566db0eb48986ee95ca1a862beea6ed142aea74e20682816(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleBillingBudgetThresholdRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec9f6d2147393b402d6f6d22ad33f73c014d76741f56e2c57e3983756d36ee48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c693ff57065a01d0126f88539c91bcbe5a56e7ec0a09604186050e6ee44cef1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a291a31793ef151fc7fc69a2014d0297bc192e23dcd5b9b5fe25537ee38aeea3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2402ece2f4bde0b8048fc3c5f6bee33c86a7b42afbeea9bccb58711022cc058(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c99c3f40026102571c49a0ea5647dc5fb3ef983619c29b998ed8a6eeaecf89d(
    *,
    disable_default_iam_recipients: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_project_level_recipients: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    monitoring_notification_channels: typing.Optional[typing.Sequence[builtins.str]] = None,
    pubsub_topic: typing.Optional[builtins.str] = None,
    schema_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2401441be282fc1c871c433aefd1719e52170dcb5b5de9b8b2bc0f45468c81fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b981fc669ed875c1cbd0455cbb1d268d3c710637b45b0641b8fc4e6eb0b38f3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20651ab314c6f000b3dc1d2692b998c8084bc594dba5ef41b0bcbfddb7528052(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44245d55f438522ae0d114caceca0edca18be59f835d7e76054905a91681cf66(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5289c0ba665e85ad3e030bcf3ed7e92ad956eb897991381a434f582317ca5bdd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3125df601f571f9d97c44702ea18233148982748b240609f18307d1b47755f8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f1735f700da8d416d9b758f8fb8cc88938b76dcd725443531c260b324458c55(
    value: typing.Optional[GoogleBillingBudgetAllUpdatesRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7084ac84968791be0c5d43f261f538fb5c8e1139292cf87856ba99ef136f9ea2(
    *,
    last_period_amount: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    specified_amount: typing.Optional[typing.Union[GoogleBillingBudgetAmountSpecifiedAmount, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f952fdea372cee55ee6803776a16d16250e51a669d925d583f3531018abe14ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16b51c241412818fef828cf54b1908df6bf0d9eb15903159afa54df7364b07c9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2d28ad9b21b83feb411d6c4e4e7f513b5df53032eb24e8d2b3b304f24faf371(
    value: typing.Optional[GoogleBillingBudgetAmount],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b9a4d4c4ef85cbc7670cee6e9430b2d49fb78e31c9bd5c474791546be0f150a(
    *,
    currency_code: typing.Optional[builtins.str] = None,
    nanos: typing.Optional[jsii.Number] = None,
    units: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5bb82ed161f447e7d8d70027abafc86eb837c2affa1a71a58b4e66bbf465bc6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0080610b1e1559d096c05db5f10775b509ecb69c9bc30ab043e84eea7aa08c26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d38c0e1628e0adafa85f19dc950e51f2e89f00673ea6147f61ddfc87064d827(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__523a86a05b7b0937ec828429f28618654d54528fd3c896e82508500a1d514367(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78509252991b366afc45ac67e266572f0cde192c11c800bad6cd410fa3b8c8a4(
    value: typing.Optional[GoogleBillingBudgetAmountSpecifiedAmount],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42f80f23ea2a0deed8b600b2b0517e0407cffc06bac553621768321879b1b912(
    *,
    calendar_period: typing.Optional[builtins.str] = None,
    credit_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    credit_types_treatment: typing.Optional[builtins.str] = None,
    custom_period: typing.Optional[typing.Union[GoogleBillingBudgetBudgetFilterCustomPeriod, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    projects: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_ancestors: typing.Optional[typing.Sequence[builtins.str]] = None,
    services: typing.Optional[typing.Sequence[builtins.str]] = None,
    subaccounts: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f3e7c69e658254178f2a55143a5ae494c69e21473bfb4bd15a097e08856a6b2(
    *,
    start_date: typing.Union[GoogleBillingBudgetBudgetFilterCustomPeriodStartDate, typing.Dict[builtins.str, typing.Any]],
    end_date: typing.Optional[typing.Union[GoogleBillingBudgetBudgetFilterCustomPeriodEndDate, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50b743ccc24ee85343240e3d0e35ea0c8362f19c1849726cf62b19a4c598ee50(
    *,
    day: jsii.Number,
    month: jsii.Number,
    year: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed41a0fdbb8cc95fddcbaa182f7cc454274a35aef8bc077d05c4fb393b292bb6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c37543cd06f90baf3a1b02ab9df5098ed83f27336e9da43f1c24917ef9174fef(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63796adc3b681c1b9b482ebf971e80a4a2cdf1c95715832fcd0f3aa96bd85fdf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd67e8d015f645c38567fd4674d5f25c41be6e4ef0de3cc12d0f18d971e3365a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc709bd0fc8219a2b5ef49a36c2cb18a5a8d81528f3d435897a89b51501c150b(
    value: typing.Optional[GoogleBillingBudgetBudgetFilterCustomPeriodEndDate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__031bfac227dadf1484104c327be05a9c8939fe54047c302fd47a836de0276c72(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f67c72d3924b4da8625322135e84ee51b58eb01cbb724e559d2f332f8b05d82d(
    value: typing.Optional[GoogleBillingBudgetBudgetFilterCustomPeriod],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50b4608751836a7be2fbb389d6f2160df1f272e6ef3f5bd35750157c9ddd70f0(
    *,
    day: jsii.Number,
    month: jsii.Number,
    year: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f97e271c7ed756822a17a0f46ec0f52ee99ab5e861c44fc51c7d0c4a8b64075f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05be8837b08aecd6e195c7d3bdc4198aac220740fb7782798389d48574b784fc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__953cb7e2fb4ce3fd598fc2c54bca60fb6dce945fca94d7a52b99e67072faf137(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df7189419d9e44fbe9f53548d3f3c33d6adb2a7958c4dbec1646e75f1ba4184b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36e281d942ef5a747a8515f06b069b96c21f0166813d68545fe27911523fbdb2(
    value: typing.Optional[GoogleBillingBudgetBudgetFilterCustomPeriodStartDate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b17f2fc0e156cbb18fddcd22dcc5b3d85d2397e4e73f46682a5ededd1f2a7a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8ffad16727a3de0680ce3d1ae7240700d3bbb564e021598124c225455863762(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ededb810187dcab5660db8a8a4fccce8393281038e7a17a690dc5dc4ee8897d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b452cdb8ed1dd384305e9ea4922d9576d15a7478507953fd3dbf3d526ef561f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69b48bb4b190d752c7bfaca37e92b185a0262c2f574e8ac940f579f0c1f7232d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfdbd96a353f3771ef566db2bfc7b6a01c15a3fa09a8ffe5655951a51c17a3be(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07ff3b549123fdac54cee0c68453990e0a9cf712ca417bebdac261173537d20a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65b44add76ab0f9c2c311142e90ac03bac2caa1451aeb950e29b8509bd1f56af(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__256cebfdb86e8ab2cecffd296d89eb0b1d8db7e58b78de9a9a59d36b8f211c1b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d709bf198b65d8256966bf7b0571868482991c5eeaa7287ff283eafc11aaa094(
    value: typing.Optional[GoogleBillingBudgetBudgetFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c52d4b123b059a691da40753c8a68f816373e2b63c1fa2df789c5dfbe74163e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    amount: typing.Union[GoogleBillingBudgetAmount, typing.Dict[builtins.str, typing.Any]],
    billing_account: builtins.str,
    all_updates_rule: typing.Optional[typing.Union[GoogleBillingBudgetAllUpdatesRule, typing.Dict[builtins.str, typing.Any]]] = None,
    budget_filter: typing.Optional[typing.Union[GoogleBillingBudgetBudgetFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ownership_scope: typing.Optional[builtins.str] = None,
    threshold_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleBillingBudgetThresholdRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleBillingBudgetTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2884dfd304939f84a14b72bc8c7d1592d12d9c48d1b1b929df6624a9a0a8646a(
    *,
    threshold_percent: jsii.Number,
    spend_basis: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57c323302b1d52e3ca8d116a8f5e60e139062c91a8ca7e98865d46d1e747cbd5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e121f4c90781a17049c8271ffc6f212a916402a06a4a5386feb99cbf9e512dc2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8e258afe3720157a572bb0a319dec642282149be5427dee453851fcb473a2a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd972042af7cae2a300600a531ceab60de69e732b37f4840901733645f2915a7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dc05c6d8acb56862d0244aaaad41f7b8a490953bc00e7c9971065e057db0af2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f20987d3adc1d60c73f36b5f4c30940b90d98d35b038a126749630d0315c23c2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBillingBudgetThresholdRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43b446ad4a7e47070b8504674b9d919fa10620bd7d131c5801f83c69b8f227ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__177732d1f72dbc4598f63ae0b51f41236581ab9991a26254aba46011b8272128(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__825cca1819ece02a58d237aacfd76bae657d1e93a6b9f8a10835dc508109d0d2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__349e489a0674c14e561d323e2f23a34e98a003c2f5ed178ec15e195d2428a3c1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBillingBudgetThresholdRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe667b31e4d8f1fc562c50e0afdd9c380f4abe8098aa0e7470bdda4e915feb33(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ddbc7e3ed0e2f85325dd038f1724444ef59de24cd223a5091acdeff588e923f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d8b25f6086a8537e9ca15ed6b85222139ee0d538841189812ae90fcd0c7c773(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__404b0f3eda86b24a342be094db2eeaab98929eadf1982e8e7ebc7ba47d0c63d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__365404516589ebf114ee7b28ef63141e3f7d41c47a1b88877774a9003c5ea3fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a2f69a9bf94386edf245fa39f0db63d061088c641a910c6d02078d56ac4f503(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBillingBudgetTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
