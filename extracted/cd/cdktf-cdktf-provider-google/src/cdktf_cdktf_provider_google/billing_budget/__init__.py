r'''
# `google_billing_budget`

Refer to the Terraform Registry for docs: [`google_billing_budget`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget).
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


class BillingBudget(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.billingBudget.BillingBudget",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget google_billing_budget}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        amount: typing.Union["BillingBudgetAmount", typing.Dict[builtins.str, typing.Any]],
        billing_account: builtins.str,
        all_updates_rule: typing.Optional[typing.Union["BillingBudgetAllUpdatesRule", typing.Dict[builtins.str, typing.Any]]] = None,
        budget_filter: typing.Optional[typing.Union["BillingBudgetBudgetFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ownership_scope: typing.Optional[builtins.str] = None,
        threshold_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BillingBudgetThresholdRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["BillingBudgetTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget google_billing_budget} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param amount: amount block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#amount BillingBudget#amount}
        :param billing_account: ID of the billing account to set a budget on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#billing_account BillingBudget#billing_account}
        :param all_updates_rule: all_updates_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#all_updates_rule BillingBudget#all_updates_rule}
        :param budget_filter: budget_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#budget_filter BillingBudget#budget_filter}
        :param display_name: User data for display name in UI. Must be <= 60 chars. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#display_name BillingBudget#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#id BillingBudget#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ownership_scope: The ownership scope of the budget. The ownership scope and users' IAM permissions determine who has full access to the budget's data. Possible values: ["OWNERSHIP_SCOPE_UNSPECIFIED", "ALL_USERS", "BILLING_ACCOUNT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#ownership_scope BillingBudget#ownership_scope}
        :param threshold_rules: threshold_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#threshold_rules BillingBudget#threshold_rules}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#timeouts BillingBudget#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5dfb892cd5bb4634dcf0b613e8d38c2bfe920362ffa161947d69a77416d58a8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BillingBudgetConfig(
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
        '''Generates CDKTF code for importing a BillingBudget resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BillingBudget to import.
        :param import_from_id: The id of the existing BillingBudget that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BillingBudget to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dddb8d47732c8e36a521dc4632aed64a05224328d99d6737e4ead68646aad44)
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
        :param disable_default_iam_recipients: Boolean. When set to true, disables default notifications sent when a threshold is exceeded. Default recipients are those with Billing Account Administrators and Billing Account Users IAM roles for the target account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#disable_default_iam_recipients BillingBudget#disable_default_iam_recipients}
        :param enable_project_level_recipients: When set to true, and when the budget has a single project configured, notifications will be sent to project level recipients of that project. This field will be ignored if the budget has multiple or no project configured. Currently, project level recipients are the users with Owner role on a cloud project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#enable_project_level_recipients BillingBudget#enable_project_level_recipients}
        :param monitoring_notification_channels: The full resource name of a monitoring notification channel in the form projects/{project_id}/notificationChannels/{channel_id}. A maximum of 5 channels are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#monitoring_notification_channels BillingBudget#monitoring_notification_channels}
        :param pubsub_topic: The name of the Cloud Pub/Sub topic where budget related messages will be published, in the form projects/{project_id}/topics/{topic_id}. Updates are sent at regular intervals to the topic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#pubsub_topic BillingBudget#pubsub_topic}
        :param schema_version: The schema version of the notification. Only "1.0" is accepted. It represents the JSON schema as defined in https://cloud.google.com/billing/docs/how-to/budgets#notification_format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#schema_version BillingBudget#schema_version}
        '''
        value = BillingBudgetAllUpdatesRule(
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
        specified_amount: typing.Optional[typing.Union["BillingBudgetAmountSpecifiedAmount", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param last_period_amount: Configures a budget amount that is automatically set to 100% of last period's spend. Boolean. Set value to true to use. Do not set to false, instead use the 'specified_amount' block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#last_period_amount BillingBudget#last_period_amount}
        :param specified_amount: specified_amount block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#specified_amount BillingBudget#specified_amount}
        '''
        value = BillingBudgetAmount(
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
        custom_period: typing.Optional[typing.Union["BillingBudgetBudgetFilterCustomPeriod", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        projects: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_ancestors: typing.Optional[typing.Sequence[builtins.str]] = None,
        services: typing.Optional[typing.Sequence[builtins.str]] = None,
        subaccounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param calendar_period: A CalendarPeriod represents the abstract concept of a recurring time period that has a canonical start. Grammatically, "the start of the current CalendarPeriod". All calendar times begin at 12 AM US and Canadian Pacific Time (UTC-8). Exactly one of 'calendar_period', 'custom_period' must be provided. Possible values: ["MONTH", "QUARTER", "YEAR", "CALENDAR_PERIOD_UNSPECIFIED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#calendar_period BillingBudget#calendar_period}
        :param credit_types: Optional. If creditTypesTreatment is INCLUDE_SPECIFIED_CREDITS, this is a list of credit types to be subtracted from gross cost to determine the spend for threshold calculations. See a list of acceptable credit type values. If creditTypesTreatment is not INCLUDE_SPECIFIED_CREDITS, this field must be empty. **Note:** If the field has a value in the config and needs to be removed, the field has to be an empty array in the config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#credit_types BillingBudget#credit_types}
        :param credit_types_treatment: Specifies how credits should be treated when determining spend for threshold calculations. Default value: "INCLUDE_ALL_CREDITS" Possible values: ["INCLUDE_ALL_CREDITS", "EXCLUDE_ALL_CREDITS", "INCLUDE_SPECIFIED_CREDITS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#credit_types_treatment BillingBudget#credit_types_treatment}
        :param custom_period: custom_period block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#custom_period BillingBudget#custom_period}
        :param labels: A single label and value pair specifying that usage from only this set of labeled resources should be included in the budget. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#labels BillingBudget#labels}
        :param projects: A set of projects of the form projects/{project_number}, specifying that usage from only this set of projects should be included in the budget. If omitted, the report will include all usage for the billing account, regardless of which project the usage occurred on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#projects BillingBudget#projects}
        :param resource_ancestors: A set of folder and organization names of the form folders/{folderId} or organizations/{organizationId}, specifying that usage from only this set of folders and organizations should be included in the budget. If omitted, the budget includes all usage that the billing account pays for. If the folder or organization contains projects that are paid for by a different Cloud Billing account, the budget doesn't apply to those projects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#resource_ancestors BillingBudget#resource_ancestors}
        :param services: A set of services of the form services/{service_id}, specifying that usage from only this set of services should be included in the budget. If omitted, the report will include usage for all the services. The service names are available through the Catalog API: https://cloud.google.com/billing/v1/how-tos/catalog-api. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#services BillingBudget#services}
        :param subaccounts: A set of subaccounts of the form billingAccounts/{account_id}, specifying that usage from only this set of subaccounts should be included in the budget. If a subaccount is set to the name of the parent account, usage from the parent account will be included. If the field is omitted, the report will include usage from the parent account and all subaccounts, if they exist. **Note:** If the field has a value in the config and needs to be removed, the field has to be an empty array in the config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#subaccounts BillingBudget#subaccounts}
        '''
        value = BillingBudgetBudgetFilter(
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BillingBudgetThresholdRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8dd6b9a4fcbd5b9128047ad62c7563de723dd282c9ad722e1c953106024a975)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#create BillingBudget#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#delete BillingBudget#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#update BillingBudget#update}.
        '''
        value = BillingBudgetTimeouts(create=create, delete=delete, update=update)

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
    def all_updates_rule(self) -> "BillingBudgetAllUpdatesRuleOutputReference":
        return typing.cast("BillingBudgetAllUpdatesRuleOutputReference", jsii.get(self, "allUpdatesRule"))

    @builtins.property
    @jsii.member(jsii_name="amount")
    def amount(self) -> "BillingBudgetAmountOutputReference":
        return typing.cast("BillingBudgetAmountOutputReference", jsii.get(self, "amount"))

    @builtins.property
    @jsii.member(jsii_name="budgetFilter")
    def budget_filter(self) -> "BillingBudgetBudgetFilterOutputReference":
        return typing.cast("BillingBudgetBudgetFilterOutputReference", jsii.get(self, "budgetFilter"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="thresholdRules")
    def threshold_rules(self) -> "BillingBudgetThresholdRulesList":
        return typing.cast("BillingBudgetThresholdRulesList", jsii.get(self, "thresholdRules"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "BillingBudgetTimeoutsOutputReference":
        return typing.cast("BillingBudgetTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="allUpdatesRuleInput")
    def all_updates_rule_input(self) -> typing.Optional["BillingBudgetAllUpdatesRule"]:
        return typing.cast(typing.Optional["BillingBudgetAllUpdatesRule"], jsii.get(self, "allUpdatesRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="amountInput")
    def amount_input(self) -> typing.Optional["BillingBudgetAmount"]:
        return typing.cast(typing.Optional["BillingBudgetAmount"], jsii.get(self, "amountInput"))

    @builtins.property
    @jsii.member(jsii_name="billingAccountInput")
    def billing_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "billingAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="budgetFilterInput")
    def budget_filter_input(self) -> typing.Optional["BillingBudgetBudgetFilter"]:
        return typing.cast(typing.Optional["BillingBudgetBudgetFilter"], jsii.get(self, "budgetFilterInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BillingBudgetThresholdRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BillingBudgetThresholdRules"]]], jsii.get(self, "thresholdRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BillingBudgetTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BillingBudgetTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="billingAccount")
    def billing_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "billingAccount"))

    @billing_account.setter
    def billing_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2772f9884abf1e50db179ce97df61a04e2e285fe61079e7d99afa2d9aed52806)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "billingAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a77d0cd0f738b8a0efa9245d8590e8eb1a2ac00e13e6142657d176186389cca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbb8d7558fedb3baf3bfee25a46aad2948363cea7c5d632d1fa6c05cceced4b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ownershipScope")
    def ownership_scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ownershipScope"))

    @ownership_scope.setter
    def ownership_scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b01cda9d0d93d11c5919fb37d269e8f05738b0bda44d5f550457c772d569f20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ownershipScope", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.billingBudget.BillingBudgetAllUpdatesRule",
    jsii_struct_bases=[],
    name_mapping={
        "disable_default_iam_recipients": "disableDefaultIamRecipients",
        "enable_project_level_recipients": "enableProjectLevelRecipients",
        "monitoring_notification_channels": "monitoringNotificationChannels",
        "pubsub_topic": "pubsubTopic",
        "schema_version": "schemaVersion",
    },
)
class BillingBudgetAllUpdatesRule:
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
        :param disable_default_iam_recipients: Boolean. When set to true, disables default notifications sent when a threshold is exceeded. Default recipients are those with Billing Account Administrators and Billing Account Users IAM roles for the target account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#disable_default_iam_recipients BillingBudget#disable_default_iam_recipients}
        :param enable_project_level_recipients: When set to true, and when the budget has a single project configured, notifications will be sent to project level recipients of that project. This field will be ignored if the budget has multiple or no project configured. Currently, project level recipients are the users with Owner role on a cloud project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#enable_project_level_recipients BillingBudget#enable_project_level_recipients}
        :param monitoring_notification_channels: The full resource name of a monitoring notification channel in the form projects/{project_id}/notificationChannels/{channel_id}. A maximum of 5 channels are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#monitoring_notification_channels BillingBudget#monitoring_notification_channels}
        :param pubsub_topic: The name of the Cloud Pub/Sub topic where budget related messages will be published, in the form projects/{project_id}/topics/{topic_id}. Updates are sent at regular intervals to the topic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#pubsub_topic BillingBudget#pubsub_topic}
        :param schema_version: The schema version of the notification. Only "1.0" is accepted. It represents the JSON schema as defined in https://cloud.google.com/billing/docs/how-to/budgets#notification_format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#schema_version BillingBudget#schema_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43d17a529aec735e4d2cac3192982fc577e659150d8305cf3b5be185a49db2aa)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#disable_default_iam_recipients BillingBudget#disable_default_iam_recipients}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#enable_project_level_recipients BillingBudget#enable_project_level_recipients}
        '''
        result = self._values.get("enable_project_level_recipients")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def monitoring_notification_channels(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''The full resource name of a monitoring notification channel in the form projects/{project_id}/notificationChannels/{channel_id}. A maximum of 5 channels are allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#monitoring_notification_channels BillingBudget#monitoring_notification_channels}
        '''
        result = self._values.get("monitoring_notification_channels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def pubsub_topic(self) -> typing.Optional[builtins.str]:
        '''The name of the Cloud Pub/Sub topic where budget related messages will be published, in the form projects/{project_id}/topics/{topic_id}.

        Updates are sent
        at regular intervals to the topic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#pubsub_topic BillingBudget#pubsub_topic}
        '''
        result = self._values.get("pubsub_topic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_version(self) -> typing.Optional[builtins.str]:
        '''The schema version of the notification. Only "1.0" is accepted. It represents the JSON schema as defined in https://cloud.google.com/billing/docs/how-to/budgets#notification_format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#schema_version BillingBudget#schema_version}
        '''
        result = self._values.get("schema_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BillingBudgetAllUpdatesRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BillingBudgetAllUpdatesRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.billingBudget.BillingBudgetAllUpdatesRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e571f97b221a8ddad9774a0045332b12ecdfbe597730cf8ca6f5f1498e5b6c8e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b84abdd0f716e396400801dbf90bdb9c481ec892cb56a268103eaaeb56d7df5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__92be9e08ce4667f19539e4fae87bab61f966d344377fda9fdf491d4fb444ceec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__55064bcd87d6c6f0e743f0e67d253c46c6730b804d51df191b89a705c3f4c0b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitoringNotificationChannels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pubsubTopic")
    def pubsub_topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pubsubTopic"))

    @pubsub_topic.setter
    def pubsub_topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ba834adaead54ad7936453ea8e496184f58eceb755ced7d8610af4c52cf9479)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pubsubTopic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schemaVersion")
    def schema_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schemaVersion"))

    @schema_version.setter
    def schema_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df9185c3d2233382f584edd2383e6cdf9c225cb8c3f5b3a0ae7fee2e0312f0de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schemaVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BillingBudgetAllUpdatesRule]:
        return typing.cast(typing.Optional[BillingBudgetAllUpdatesRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BillingBudgetAllUpdatesRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e5613f79e20dd17e9ff644cc716a7110342d52dc59872ec9e114eaaa5396180)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.billingBudget.BillingBudgetAmount",
    jsii_struct_bases=[],
    name_mapping={
        "last_period_amount": "lastPeriodAmount",
        "specified_amount": "specifiedAmount",
    },
)
class BillingBudgetAmount:
    def __init__(
        self,
        *,
        last_period_amount: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        specified_amount: typing.Optional[typing.Union["BillingBudgetAmountSpecifiedAmount", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param last_period_amount: Configures a budget amount that is automatically set to 100% of last period's spend. Boolean. Set value to true to use. Do not set to false, instead use the 'specified_amount' block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#last_period_amount BillingBudget#last_period_amount}
        :param specified_amount: specified_amount block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#specified_amount BillingBudget#specified_amount}
        '''
        if isinstance(specified_amount, dict):
            specified_amount = BillingBudgetAmountSpecifiedAmount(**specified_amount)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3920adfcbef552d0a57de87a95d431a623e446069ef730af9a5b76d50c530bd2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#last_period_amount BillingBudget#last_period_amount}
        '''
        result = self._values.get("last_period_amount")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def specified_amount(self) -> typing.Optional["BillingBudgetAmountSpecifiedAmount"]:
        '''specified_amount block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#specified_amount BillingBudget#specified_amount}
        '''
        result = self._values.get("specified_amount")
        return typing.cast(typing.Optional["BillingBudgetAmountSpecifiedAmount"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BillingBudgetAmount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BillingBudgetAmountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.billingBudget.BillingBudgetAmountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2621e88a1055ffb514b2b7bb7184b83a70b65c7015c80ee4282cf0d3477d182d)
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
        :param currency_code: The 3-letter currency code defined in ISO 4217. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#currency_code BillingBudget#currency_code}
        :param nanos: Number of nano (10^-9) units of the amount. The value must be between -999,999,999 and +999,999,999 inclusive. If units is positive, nanos must be positive or zero. If units is zero, nanos can be positive, zero, or negative. If units is negative, nanos must be negative or zero. For example $-1.75 is represented as units=-1 and nanos=-750,000,000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#nanos BillingBudget#nanos}
        :param units: The whole units of the amount. For example if currencyCode is "USD", then 1 unit is one US dollar. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#units BillingBudget#units}
        '''
        value = BillingBudgetAmountSpecifiedAmount(
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
    def specified_amount(self) -> "BillingBudgetAmountSpecifiedAmountOutputReference":
        return typing.cast("BillingBudgetAmountSpecifiedAmountOutputReference", jsii.get(self, "specifiedAmount"))

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
    ) -> typing.Optional["BillingBudgetAmountSpecifiedAmount"]:
        return typing.cast(typing.Optional["BillingBudgetAmountSpecifiedAmount"], jsii.get(self, "specifiedAmountInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__0e21fc3892542460b9d8d92729beaca6fc1cff94decdcbab8637af11b2894ef7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lastPeriodAmount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BillingBudgetAmount]:
        return typing.cast(typing.Optional[BillingBudgetAmount], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[BillingBudgetAmount]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b90797323f648db2f729ed93478a55891960fb465b7888e39444e45edfd15cd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.billingBudget.BillingBudgetAmountSpecifiedAmount",
    jsii_struct_bases=[],
    name_mapping={"currency_code": "currencyCode", "nanos": "nanos", "units": "units"},
)
class BillingBudgetAmountSpecifiedAmount:
    def __init__(
        self,
        *,
        currency_code: typing.Optional[builtins.str] = None,
        nanos: typing.Optional[jsii.Number] = None,
        units: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param currency_code: The 3-letter currency code defined in ISO 4217. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#currency_code BillingBudget#currency_code}
        :param nanos: Number of nano (10^-9) units of the amount. The value must be between -999,999,999 and +999,999,999 inclusive. If units is positive, nanos must be positive or zero. If units is zero, nanos can be positive, zero, or negative. If units is negative, nanos must be negative or zero. For example $-1.75 is represented as units=-1 and nanos=-750,000,000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#nanos BillingBudget#nanos}
        :param units: The whole units of the amount. For example if currencyCode is "USD", then 1 unit is one US dollar. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#units BillingBudget#units}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43373f9b7d88b051912bbd996010df0bf64680617f270889d02208608816b724)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#currency_code BillingBudget#currency_code}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#nanos BillingBudget#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def units(self) -> typing.Optional[builtins.str]:
        '''The whole units of the amount. For example if currencyCode is "USD", then 1 unit is one US dollar.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#units BillingBudget#units}
        '''
        result = self._values.get("units")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BillingBudgetAmountSpecifiedAmount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BillingBudgetAmountSpecifiedAmountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.billingBudget.BillingBudgetAmountSpecifiedAmountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bdeaeff999e3bdaf42c6bb79a8c8100d4472ae2fa5a26da67c7dc8271a9ef0b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2185abdf93d40e03c671bcb997eda9d6355b4767cae41b8452e2e0801eafe829)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "currencyCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9195375115d39a3b001b68abc9163ccd39eeed16873978be4c907c4eab96d8a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="units")
    def units(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "units"))

    @units.setter
    def units(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4debaf47267c81291630d3cb0bc9c78c5a005ad48b2b904cbdb8ab3c26e5a258)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "units", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BillingBudgetAmountSpecifiedAmount]:
        return typing.cast(typing.Optional[BillingBudgetAmountSpecifiedAmount], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BillingBudgetAmountSpecifiedAmount],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0c3a99fe4c3468bb01ad48a9c29e13d6b01e152673d1ee2756a8885ddf1c647)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.billingBudget.BillingBudgetBudgetFilter",
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
class BillingBudgetBudgetFilter:
    def __init__(
        self,
        *,
        calendar_period: typing.Optional[builtins.str] = None,
        credit_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        credit_types_treatment: typing.Optional[builtins.str] = None,
        custom_period: typing.Optional[typing.Union["BillingBudgetBudgetFilterCustomPeriod", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        projects: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_ancestors: typing.Optional[typing.Sequence[builtins.str]] = None,
        services: typing.Optional[typing.Sequence[builtins.str]] = None,
        subaccounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param calendar_period: A CalendarPeriod represents the abstract concept of a recurring time period that has a canonical start. Grammatically, "the start of the current CalendarPeriod". All calendar times begin at 12 AM US and Canadian Pacific Time (UTC-8). Exactly one of 'calendar_period', 'custom_period' must be provided. Possible values: ["MONTH", "QUARTER", "YEAR", "CALENDAR_PERIOD_UNSPECIFIED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#calendar_period BillingBudget#calendar_period}
        :param credit_types: Optional. If creditTypesTreatment is INCLUDE_SPECIFIED_CREDITS, this is a list of credit types to be subtracted from gross cost to determine the spend for threshold calculations. See a list of acceptable credit type values. If creditTypesTreatment is not INCLUDE_SPECIFIED_CREDITS, this field must be empty. **Note:** If the field has a value in the config and needs to be removed, the field has to be an empty array in the config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#credit_types BillingBudget#credit_types}
        :param credit_types_treatment: Specifies how credits should be treated when determining spend for threshold calculations. Default value: "INCLUDE_ALL_CREDITS" Possible values: ["INCLUDE_ALL_CREDITS", "EXCLUDE_ALL_CREDITS", "INCLUDE_SPECIFIED_CREDITS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#credit_types_treatment BillingBudget#credit_types_treatment}
        :param custom_period: custom_period block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#custom_period BillingBudget#custom_period}
        :param labels: A single label and value pair specifying that usage from only this set of labeled resources should be included in the budget. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#labels BillingBudget#labels}
        :param projects: A set of projects of the form projects/{project_number}, specifying that usage from only this set of projects should be included in the budget. If omitted, the report will include all usage for the billing account, regardless of which project the usage occurred on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#projects BillingBudget#projects}
        :param resource_ancestors: A set of folder and organization names of the form folders/{folderId} or organizations/{organizationId}, specifying that usage from only this set of folders and organizations should be included in the budget. If omitted, the budget includes all usage that the billing account pays for. If the folder or organization contains projects that are paid for by a different Cloud Billing account, the budget doesn't apply to those projects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#resource_ancestors BillingBudget#resource_ancestors}
        :param services: A set of services of the form services/{service_id}, specifying that usage from only this set of services should be included in the budget. If omitted, the report will include usage for all the services. The service names are available through the Catalog API: https://cloud.google.com/billing/v1/how-tos/catalog-api. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#services BillingBudget#services}
        :param subaccounts: A set of subaccounts of the form billingAccounts/{account_id}, specifying that usage from only this set of subaccounts should be included in the budget. If a subaccount is set to the name of the parent account, usage from the parent account will be included. If the field is omitted, the report will include usage from the parent account and all subaccounts, if they exist. **Note:** If the field has a value in the config and needs to be removed, the field has to be an empty array in the config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#subaccounts BillingBudget#subaccounts}
        '''
        if isinstance(custom_period, dict):
            custom_period = BillingBudgetBudgetFilterCustomPeriod(**custom_period)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44d748a1ef6b007fc9dc8ec991fe0f7c548bb6a2625850bd065297f594ac5cd2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#calendar_period BillingBudget#calendar_period}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#credit_types BillingBudget#credit_types}
        '''
        result = self._values.get("credit_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def credit_types_treatment(self) -> typing.Optional[builtins.str]:
        '''Specifies how credits should be treated when determining spend for threshold calculations. Default value: "INCLUDE_ALL_CREDITS" Possible values: ["INCLUDE_ALL_CREDITS", "EXCLUDE_ALL_CREDITS", "INCLUDE_SPECIFIED_CREDITS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#credit_types_treatment BillingBudget#credit_types_treatment}
        '''
        result = self._values.get("credit_types_treatment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_period(self) -> typing.Optional["BillingBudgetBudgetFilterCustomPeriod"]:
        '''custom_period block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#custom_period BillingBudget#custom_period}
        '''
        result = self._values.get("custom_period")
        return typing.cast(typing.Optional["BillingBudgetBudgetFilterCustomPeriod"], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A single label and value pair specifying that usage from only this set of labeled resources should be included in the budget.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#labels BillingBudget#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def projects(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A set of projects of the form projects/{project_number}, specifying that usage from only this set of projects should be included in the budget.

        If omitted, the report will include
        all usage for the billing account, regardless of which project
        the usage occurred on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#projects BillingBudget#projects}
        '''
        result = self._values.get("projects")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resource_ancestors(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A set of folder and organization names of the form folders/{folderId} or organizations/{organizationId}, specifying that usage from only this set of folders and organizations should be included in the budget.

        If omitted, the budget includes all usage that the billing account pays for. If the folder or organization
        contains projects that are paid for by a different Cloud Billing account, the budget doesn't apply to those projects.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#resource_ancestors BillingBudget#resource_ancestors}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#services BillingBudget#services}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#subaccounts BillingBudget#subaccounts}
        '''
        result = self._values.get("subaccounts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BillingBudgetBudgetFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.billingBudget.BillingBudgetBudgetFilterCustomPeriod",
    jsii_struct_bases=[],
    name_mapping={"start_date": "startDate", "end_date": "endDate"},
)
class BillingBudgetBudgetFilterCustomPeriod:
    def __init__(
        self,
        *,
        start_date: typing.Union["BillingBudgetBudgetFilterCustomPeriodStartDate", typing.Dict[builtins.str, typing.Any]],
        end_date: typing.Optional[typing.Union["BillingBudgetBudgetFilterCustomPeriodEndDate", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param start_date: start_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#start_date BillingBudget#start_date}
        :param end_date: end_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#end_date BillingBudget#end_date}
        '''
        if isinstance(start_date, dict):
            start_date = BillingBudgetBudgetFilterCustomPeriodStartDate(**start_date)
        if isinstance(end_date, dict):
            end_date = BillingBudgetBudgetFilterCustomPeriodEndDate(**end_date)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9d5615dbb7f32ff11bc98b9ca698934e7ab15212febc55a79ca1805fe69b3e8)
            check_type(argname="argument start_date", value=start_date, expected_type=type_hints["start_date"])
            check_type(argname="argument end_date", value=end_date, expected_type=type_hints["end_date"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "start_date": start_date,
        }
        if end_date is not None:
            self._values["end_date"] = end_date

    @builtins.property
    def start_date(self) -> "BillingBudgetBudgetFilterCustomPeriodStartDate":
        '''start_date block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#start_date BillingBudget#start_date}
        '''
        result = self._values.get("start_date")
        assert result is not None, "Required property 'start_date' is missing"
        return typing.cast("BillingBudgetBudgetFilterCustomPeriodStartDate", result)

    @builtins.property
    def end_date(
        self,
    ) -> typing.Optional["BillingBudgetBudgetFilterCustomPeriodEndDate"]:
        '''end_date block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#end_date BillingBudget#end_date}
        '''
        result = self._values.get("end_date")
        return typing.cast(typing.Optional["BillingBudgetBudgetFilterCustomPeriodEndDate"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BillingBudgetBudgetFilterCustomPeriod(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.billingBudget.BillingBudgetBudgetFilterCustomPeriodEndDate",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "month": "month", "year": "year"},
)
class BillingBudgetBudgetFilterCustomPeriodEndDate:
    def __init__(
        self,
        *,
        day: jsii.Number,
        month: jsii.Number,
        year: jsii.Number,
    ) -> None:
        '''
        :param day: Day of a month. Must be from 1 to 31 and valid for the year and month. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#day BillingBudget#day}
        :param month: Month of a year. Must be from 1 to 12. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#month BillingBudget#month}
        :param year: Year of the date. Must be from 1 to 9999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#year BillingBudget#year}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6b8ee0d72e4d45a5456aaec726e06096cdfe18ccddb41104a4a88557816b83b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#day BillingBudget#day}
        '''
        result = self._values.get("day")
        assert result is not None, "Required property 'day' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def month(self) -> jsii.Number:
        '''Month of a year. Must be from 1 to 12.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#month BillingBudget#month}
        '''
        result = self._values.get("month")
        assert result is not None, "Required property 'month' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def year(self) -> jsii.Number:
        '''Year of the date. Must be from 1 to 9999.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#year BillingBudget#year}
        '''
        result = self._values.get("year")
        assert result is not None, "Required property 'year' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BillingBudgetBudgetFilterCustomPeriodEndDate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BillingBudgetBudgetFilterCustomPeriodEndDateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.billingBudget.BillingBudgetBudgetFilterCustomPeriodEndDateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cda492222b8ebdb111173aaf95a2010eadb16e2ec6584562e34128d44e22ac09)
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
            type_hints = typing.get_type_hints(_typecheckingstub__98dcff02249fff0ff9f871081ff0945b1e1ff4b0ced27c5e81e218b1471b3617)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="month")
    def month(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "month"))

    @month.setter
    def month(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d47d078661aae0ad2ca5725bf1986b4e0589e42fe186d36e72c360d1f8c1cd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "month", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="year")
    def year(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "year"))

    @year.setter
    def year(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__042906f8600187603248471afc470dd3beb05f95adf68f9c2240bd419fa35ae5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "year", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BillingBudgetBudgetFilterCustomPeriodEndDate]:
        return typing.cast(typing.Optional[BillingBudgetBudgetFilterCustomPeriodEndDate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BillingBudgetBudgetFilterCustomPeriodEndDate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f6ffacb776284a01334e7973442eeae01eb27ef9bf24d9ca4baaaa1d2804ebe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BillingBudgetBudgetFilterCustomPeriodOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.billingBudget.BillingBudgetBudgetFilterCustomPeriodOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab0eeea3da868dbb5b70799c1620dbab53b0383746b6953e9cc2b693f4a1e33a)
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
        :param day: Day of a month. Must be from 1 to 31 and valid for the year and month. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#day BillingBudget#day}
        :param month: Month of a year. Must be from 1 to 12. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#month BillingBudget#month}
        :param year: Year of the date. Must be from 1 to 9999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#year BillingBudget#year}
        '''
        value = BillingBudgetBudgetFilterCustomPeriodEndDate(
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
        :param day: Day of a month. Must be from 1 to 31 and valid for the year and month. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#day BillingBudget#day}
        :param month: Month of a year. Must be from 1 to 12. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#month BillingBudget#month}
        :param year: Year of the date. Must be from 1 to 9999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#year BillingBudget#year}
        '''
        value = BillingBudgetBudgetFilterCustomPeriodStartDate(
            day=day, month=month, year=year
        )

        return typing.cast(None, jsii.invoke(self, "putStartDate", [value]))

    @jsii.member(jsii_name="resetEndDate")
    def reset_end_date(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndDate", []))

    @builtins.property
    @jsii.member(jsii_name="endDate")
    def end_date(self) -> BillingBudgetBudgetFilterCustomPeriodEndDateOutputReference:
        return typing.cast(BillingBudgetBudgetFilterCustomPeriodEndDateOutputReference, jsii.get(self, "endDate"))

    @builtins.property
    @jsii.member(jsii_name="startDate")
    def start_date(
        self,
    ) -> "BillingBudgetBudgetFilterCustomPeriodStartDateOutputReference":
        return typing.cast("BillingBudgetBudgetFilterCustomPeriodStartDateOutputReference", jsii.get(self, "startDate"))

    @builtins.property
    @jsii.member(jsii_name="endDateInput")
    def end_date_input(
        self,
    ) -> typing.Optional[BillingBudgetBudgetFilterCustomPeriodEndDate]:
        return typing.cast(typing.Optional[BillingBudgetBudgetFilterCustomPeriodEndDate], jsii.get(self, "endDateInput"))

    @builtins.property
    @jsii.member(jsii_name="startDateInput")
    def start_date_input(
        self,
    ) -> typing.Optional["BillingBudgetBudgetFilterCustomPeriodStartDate"]:
        return typing.cast(typing.Optional["BillingBudgetBudgetFilterCustomPeriodStartDate"], jsii.get(self, "startDateInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BillingBudgetBudgetFilterCustomPeriod]:
        return typing.cast(typing.Optional[BillingBudgetBudgetFilterCustomPeriod], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BillingBudgetBudgetFilterCustomPeriod],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad98c962063989c22c292cab2dcab0d964c2af728baf1c9993c9317e557c0ac6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.billingBudget.BillingBudgetBudgetFilterCustomPeriodStartDate",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "month": "month", "year": "year"},
)
class BillingBudgetBudgetFilterCustomPeriodStartDate:
    def __init__(
        self,
        *,
        day: jsii.Number,
        month: jsii.Number,
        year: jsii.Number,
    ) -> None:
        '''
        :param day: Day of a month. Must be from 1 to 31 and valid for the year and month. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#day BillingBudget#day}
        :param month: Month of a year. Must be from 1 to 12. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#month BillingBudget#month}
        :param year: Year of the date. Must be from 1 to 9999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#year BillingBudget#year}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24ca9c314c1272f9d71f24fe997275d069882e2e31d0274635d7b4064f96ba94)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#day BillingBudget#day}
        '''
        result = self._values.get("day")
        assert result is not None, "Required property 'day' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def month(self) -> jsii.Number:
        '''Month of a year. Must be from 1 to 12.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#month BillingBudget#month}
        '''
        result = self._values.get("month")
        assert result is not None, "Required property 'month' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def year(self) -> jsii.Number:
        '''Year of the date. Must be from 1 to 9999.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#year BillingBudget#year}
        '''
        result = self._values.get("year")
        assert result is not None, "Required property 'year' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BillingBudgetBudgetFilterCustomPeriodStartDate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BillingBudgetBudgetFilterCustomPeriodStartDateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.billingBudget.BillingBudgetBudgetFilterCustomPeriodStartDateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b210b3daab1829177eb7edad74ba99bd2caa0adda54ddf6391bc1fe9ddc4f36b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__108b5601f11ef328e5929638b2ff51e9b37ea2d1d77607a92dbea5fc42130107)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="month")
    def month(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "month"))

    @month.setter
    def month(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b33386c9780369a513d006d572924d1cb64e5b189cc4c10e27f5d680c782c26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "month", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="year")
    def year(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "year"))

    @year.setter
    def year(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f580ef77480ac1cbf79aeffca51512c5aac07dcc95a998b372be3c38a144a389)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "year", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BillingBudgetBudgetFilterCustomPeriodStartDate]:
        return typing.cast(typing.Optional[BillingBudgetBudgetFilterCustomPeriodStartDate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BillingBudgetBudgetFilterCustomPeriodStartDate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bd95bae665774801eac431b8154bcababef2fde69e9507c3004217382756fb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BillingBudgetBudgetFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.billingBudget.BillingBudgetBudgetFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d16628eb44a66ce48a3d91e5b5d6d2e54868a2c4d9aced3a7a486411619a587d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomPeriod")
    def put_custom_period(
        self,
        *,
        start_date: typing.Union[BillingBudgetBudgetFilterCustomPeriodStartDate, typing.Dict[builtins.str, typing.Any]],
        end_date: typing.Optional[typing.Union[BillingBudgetBudgetFilterCustomPeriodEndDate, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param start_date: start_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#start_date BillingBudget#start_date}
        :param end_date: end_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#end_date BillingBudget#end_date}
        '''
        value = BillingBudgetBudgetFilterCustomPeriod(
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
    def custom_period(self) -> BillingBudgetBudgetFilterCustomPeriodOutputReference:
        return typing.cast(BillingBudgetBudgetFilterCustomPeriodOutputReference, jsii.get(self, "customPeriod"))

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
    ) -> typing.Optional[BillingBudgetBudgetFilterCustomPeriod]:
        return typing.cast(typing.Optional[BillingBudgetBudgetFilterCustomPeriod], jsii.get(self, "customPeriodInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__30436dce086246c0d10fe30936543b7c185d400dc2e100c245262260c5877d6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "calendarPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="creditTypes")
    def credit_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "creditTypes"))

    @credit_types.setter
    def credit_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8aead85b2cce313aec938196738e8dc34554f9a76540fa59ad67e28021b68b85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "creditTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="creditTypesTreatment")
    def credit_types_treatment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creditTypesTreatment"))

    @credit_types_treatment.setter
    def credit_types_treatment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2066675f88b09775487829b45b641b133844a88f0bbeaa50b008564aaca453a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "creditTypesTreatment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__823a34453d4eb8ec9a7bec5ea1a982af4772ce974b68ef0246391dcd252814de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projects")
    def projects(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "projects"))

    @projects.setter
    def projects(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7346576970bddd20b34d5786ef1bc6a02ff4ba65a75cb0bd5f51b7c0478ad863)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projects", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceAncestors")
    def resource_ancestors(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceAncestors"))

    @resource_ancestors.setter
    def resource_ancestors(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87cfc59068082edf7aaa256d72b88dc033fbac9c4132eebe2067e91fc52dc412)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceAncestors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="services")
    def services(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "services"))

    @services.setter
    def services(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90712c3d84c807b07419016ba47df227214ba27e2ea62c83899b2fcb927824ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "services", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subaccounts")
    def subaccounts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subaccounts"))

    @subaccounts.setter
    def subaccounts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__289649bc42475d7f77d235bfe2fbc836518c790ec2804a833620653bf81c3d3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subaccounts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BillingBudgetBudgetFilter]:
        return typing.cast(typing.Optional[BillingBudgetBudgetFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[BillingBudgetBudgetFilter]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c400e201b27590f86c0dbdb02f9613359af8a53558d465fd17b23b4bdd4aab3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.billingBudget.BillingBudgetConfig",
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
class BillingBudgetConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        amount: typing.Union[BillingBudgetAmount, typing.Dict[builtins.str, typing.Any]],
        billing_account: builtins.str,
        all_updates_rule: typing.Optional[typing.Union[BillingBudgetAllUpdatesRule, typing.Dict[builtins.str, typing.Any]]] = None,
        budget_filter: typing.Optional[typing.Union[BillingBudgetBudgetFilter, typing.Dict[builtins.str, typing.Any]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ownership_scope: typing.Optional[builtins.str] = None,
        threshold_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BillingBudgetThresholdRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["BillingBudgetTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param amount: amount block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#amount BillingBudget#amount}
        :param billing_account: ID of the billing account to set a budget on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#billing_account BillingBudget#billing_account}
        :param all_updates_rule: all_updates_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#all_updates_rule BillingBudget#all_updates_rule}
        :param budget_filter: budget_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#budget_filter BillingBudget#budget_filter}
        :param display_name: User data for display name in UI. Must be <= 60 chars. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#display_name BillingBudget#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#id BillingBudget#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ownership_scope: The ownership scope of the budget. The ownership scope and users' IAM permissions determine who has full access to the budget's data. Possible values: ["OWNERSHIP_SCOPE_UNSPECIFIED", "ALL_USERS", "BILLING_ACCOUNT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#ownership_scope BillingBudget#ownership_scope}
        :param threshold_rules: threshold_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#threshold_rules BillingBudget#threshold_rules}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#timeouts BillingBudget#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(amount, dict):
            amount = BillingBudgetAmount(**amount)
        if isinstance(all_updates_rule, dict):
            all_updates_rule = BillingBudgetAllUpdatesRule(**all_updates_rule)
        if isinstance(budget_filter, dict):
            budget_filter = BillingBudgetBudgetFilter(**budget_filter)
        if isinstance(timeouts, dict):
            timeouts = BillingBudgetTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abd37a5794fc05df231effddbe3129331f4d41764951dbf6261f30cf38da30dc)
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
    def amount(self) -> BillingBudgetAmount:
        '''amount block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#amount BillingBudget#amount}
        '''
        result = self._values.get("amount")
        assert result is not None, "Required property 'amount' is missing"
        return typing.cast(BillingBudgetAmount, result)

    @builtins.property
    def billing_account(self) -> builtins.str:
        '''ID of the billing account to set a budget on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#billing_account BillingBudget#billing_account}
        '''
        result = self._values.get("billing_account")
        assert result is not None, "Required property 'billing_account' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def all_updates_rule(self) -> typing.Optional[BillingBudgetAllUpdatesRule]:
        '''all_updates_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#all_updates_rule BillingBudget#all_updates_rule}
        '''
        result = self._values.get("all_updates_rule")
        return typing.cast(typing.Optional[BillingBudgetAllUpdatesRule], result)

    @builtins.property
    def budget_filter(self) -> typing.Optional[BillingBudgetBudgetFilter]:
        '''budget_filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#budget_filter BillingBudget#budget_filter}
        '''
        result = self._values.get("budget_filter")
        return typing.cast(typing.Optional[BillingBudgetBudgetFilter], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''User data for display name in UI. Must be <= 60 chars.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#display_name BillingBudget#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#id BillingBudget#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#ownership_scope BillingBudget#ownership_scope}
        '''
        result = self._values.get("ownership_scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def threshold_rules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BillingBudgetThresholdRules"]]]:
        '''threshold_rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#threshold_rules BillingBudget#threshold_rules}
        '''
        result = self._values.get("threshold_rules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BillingBudgetThresholdRules"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["BillingBudgetTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#timeouts BillingBudget#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["BillingBudgetTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BillingBudgetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.billingBudget.BillingBudgetThresholdRules",
    jsii_struct_bases=[],
    name_mapping={
        "threshold_percent": "thresholdPercent",
        "spend_basis": "spendBasis",
    },
)
class BillingBudgetThresholdRules:
    def __init__(
        self,
        *,
        threshold_percent: jsii.Number,
        spend_basis: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param threshold_percent: Send an alert when this threshold is exceeded. This is a 1.0-based percentage, so 0.5 = 50%. Must be >= 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#threshold_percent BillingBudget#threshold_percent}
        :param spend_basis: The type of basis used to determine if spend has passed the threshold. Default value: "CURRENT_SPEND" Possible values: ["CURRENT_SPEND", "FORECASTED_SPEND"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#spend_basis BillingBudget#spend_basis}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61d0b8711d6f2e4d3755e71c2781c072358dc665aadb7f84d4cf9f87dcfcf35a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#threshold_percent BillingBudget#threshold_percent}
        '''
        result = self._values.get("threshold_percent")
        assert result is not None, "Required property 'threshold_percent' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def spend_basis(self) -> typing.Optional[builtins.str]:
        '''The type of basis used to determine if spend has passed the threshold. Default value: "CURRENT_SPEND" Possible values: ["CURRENT_SPEND", "FORECASTED_SPEND"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#spend_basis BillingBudget#spend_basis}
        '''
        result = self._values.get("spend_basis")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BillingBudgetThresholdRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BillingBudgetThresholdRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.billingBudget.BillingBudgetThresholdRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__772db867830978f5d4bdc24a858ea87e2a1b3faadfa83a22683122da4777b314)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "BillingBudgetThresholdRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10063bce078be922b35e656d5410c422956baf6d177beed97fb569fd84aa5bb9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BillingBudgetThresholdRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78f1320f3e66efa29665b74c2cad8a4185324dab101cfafe846f6d4dff210f65)
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
            type_hints = typing.get_type_hints(_typecheckingstub__270381dae1327d2da9e339d43aece045ec482d047fbdaeefb136fe268e8e6bd1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e86cad4be7ea67402c1bb651cc1136322f88f4d4463102fc04fb7067efe73a57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BillingBudgetThresholdRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BillingBudgetThresholdRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BillingBudgetThresholdRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__848143449c7ac070f4b083215e80a5b69a0cec981cc2a0f2e4775a93bab4f167)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BillingBudgetThresholdRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.billingBudget.BillingBudgetThresholdRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__879fd75aab47f0982f94d70dd6f5e0a0e65166c27cc8990aeb9567f7a980a64f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__059a74dfc68e189fad8418155cdd7a13eab4e181ae818e2689117a94a99fd44d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spendBasis", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="thresholdPercent")
    def threshold_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "thresholdPercent"))

    @threshold_percent.setter
    def threshold_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c13314de416c208fe87c04f03a55cd2a3ddadadcc5e931417d24d252fe2029d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thresholdPercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BillingBudgetThresholdRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BillingBudgetThresholdRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BillingBudgetThresholdRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7953db5b64e2f3573ce722460f31aa198166f9bb1ed56751fce64304e2be2026)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.billingBudget.BillingBudgetTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class BillingBudgetTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#create BillingBudget#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#delete BillingBudget#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#update BillingBudget#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d37ee4ab58600a20b2543f0437aab21d44b87aa2b2a7e2039282e64598d6507)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#create BillingBudget#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#delete BillingBudget#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/billing_budget#update BillingBudget#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BillingBudgetTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BillingBudgetTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.billingBudget.BillingBudgetTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b27780d62e3d858d5935f5f9e6631d4b21e730d0a888ebdaa5205649a72ebf64)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eadbfd56f84b5b07fb80688787395748383ff2e736226d98d8e6b06016611467)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cab818ac00bb3e347f7c414c625a65ed58e9276e57adfe2bb5d2240d97cc79e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f7a66f256804e04c43f9a234061a5cdb4ebf6e3024386c45656f4831bb15b93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BillingBudgetTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BillingBudgetTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BillingBudgetTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d9c432f70219f65dab97dbbaeb3a4a0810eab73f4918b4397d3804c7008bd84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BillingBudget",
    "BillingBudgetAllUpdatesRule",
    "BillingBudgetAllUpdatesRuleOutputReference",
    "BillingBudgetAmount",
    "BillingBudgetAmountOutputReference",
    "BillingBudgetAmountSpecifiedAmount",
    "BillingBudgetAmountSpecifiedAmountOutputReference",
    "BillingBudgetBudgetFilter",
    "BillingBudgetBudgetFilterCustomPeriod",
    "BillingBudgetBudgetFilterCustomPeriodEndDate",
    "BillingBudgetBudgetFilterCustomPeriodEndDateOutputReference",
    "BillingBudgetBudgetFilterCustomPeriodOutputReference",
    "BillingBudgetBudgetFilterCustomPeriodStartDate",
    "BillingBudgetBudgetFilterCustomPeriodStartDateOutputReference",
    "BillingBudgetBudgetFilterOutputReference",
    "BillingBudgetConfig",
    "BillingBudgetThresholdRules",
    "BillingBudgetThresholdRulesList",
    "BillingBudgetThresholdRulesOutputReference",
    "BillingBudgetTimeouts",
    "BillingBudgetTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__b5dfb892cd5bb4634dcf0b613e8d38c2bfe920362ffa161947d69a77416d58a8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    amount: typing.Union[BillingBudgetAmount, typing.Dict[builtins.str, typing.Any]],
    billing_account: builtins.str,
    all_updates_rule: typing.Optional[typing.Union[BillingBudgetAllUpdatesRule, typing.Dict[builtins.str, typing.Any]]] = None,
    budget_filter: typing.Optional[typing.Union[BillingBudgetBudgetFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ownership_scope: typing.Optional[builtins.str] = None,
    threshold_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BillingBudgetThresholdRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[BillingBudgetTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__8dddb8d47732c8e36a521dc4632aed64a05224328d99d6737e4ead68646aad44(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8dd6b9a4fcbd5b9128047ad62c7563de723dd282c9ad722e1c953106024a975(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BillingBudgetThresholdRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2772f9884abf1e50db179ce97df61a04e2e285fe61079e7d99afa2d9aed52806(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a77d0cd0f738b8a0efa9245d8590e8eb1a2ac00e13e6142657d176186389cca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbb8d7558fedb3baf3bfee25a46aad2948363cea7c5d632d1fa6c05cceced4b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b01cda9d0d93d11c5919fb37d269e8f05738b0bda44d5f550457c772d569f20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43d17a529aec735e4d2cac3192982fc577e659150d8305cf3b5be185a49db2aa(
    *,
    disable_default_iam_recipients: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_project_level_recipients: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    monitoring_notification_channels: typing.Optional[typing.Sequence[builtins.str]] = None,
    pubsub_topic: typing.Optional[builtins.str] = None,
    schema_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e571f97b221a8ddad9774a0045332b12ecdfbe597730cf8ca6f5f1498e5b6c8e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b84abdd0f716e396400801dbf90bdb9c481ec892cb56a268103eaaeb56d7df5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92be9e08ce4667f19539e4fae87bab61f966d344377fda9fdf491d4fb444ceec(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55064bcd87d6c6f0e743f0e67d253c46c6730b804d51df191b89a705c3f4c0b8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ba834adaead54ad7936453ea8e496184f58eceb755ced7d8610af4c52cf9479(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df9185c3d2233382f584edd2383e6cdf9c225cb8c3f5b3a0ae7fee2e0312f0de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e5613f79e20dd17e9ff644cc716a7110342d52dc59872ec9e114eaaa5396180(
    value: typing.Optional[BillingBudgetAllUpdatesRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3920adfcbef552d0a57de87a95d431a623e446069ef730af9a5b76d50c530bd2(
    *,
    last_period_amount: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    specified_amount: typing.Optional[typing.Union[BillingBudgetAmountSpecifiedAmount, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2621e88a1055ffb514b2b7bb7184b83a70b65c7015c80ee4282cf0d3477d182d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e21fc3892542460b9d8d92729beaca6fc1cff94decdcbab8637af11b2894ef7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b90797323f648db2f729ed93478a55891960fb465b7888e39444e45edfd15cd8(
    value: typing.Optional[BillingBudgetAmount],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43373f9b7d88b051912bbd996010df0bf64680617f270889d02208608816b724(
    *,
    currency_code: typing.Optional[builtins.str] = None,
    nanos: typing.Optional[jsii.Number] = None,
    units: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdeaeff999e3bdaf42c6bb79a8c8100d4472ae2fa5a26da67c7dc8271a9ef0b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2185abdf93d40e03c671bcb997eda9d6355b4767cae41b8452e2e0801eafe829(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9195375115d39a3b001b68abc9163ccd39eeed16873978be4c907c4eab96d8a9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4debaf47267c81291630d3cb0bc9c78c5a005ad48b2b904cbdb8ab3c26e5a258(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0c3a99fe4c3468bb01ad48a9c29e13d6b01e152673d1ee2756a8885ddf1c647(
    value: typing.Optional[BillingBudgetAmountSpecifiedAmount],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44d748a1ef6b007fc9dc8ec991fe0f7c548bb6a2625850bd065297f594ac5cd2(
    *,
    calendar_period: typing.Optional[builtins.str] = None,
    credit_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    credit_types_treatment: typing.Optional[builtins.str] = None,
    custom_period: typing.Optional[typing.Union[BillingBudgetBudgetFilterCustomPeriod, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    projects: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_ancestors: typing.Optional[typing.Sequence[builtins.str]] = None,
    services: typing.Optional[typing.Sequence[builtins.str]] = None,
    subaccounts: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9d5615dbb7f32ff11bc98b9ca698934e7ab15212febc55a79ca1805fe69b3e8(
    *,
    start_date: typing.Union[BillingBudgetBudgetFilterCustomPeriodStartDate, typing.Dict[builtins.str, typing.Any]],
    end_date: typing.Optional[typing.Union[BillingBudgetBudgetFilterCustomPeriodEndDate, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6b8ee0d72e4d45a5456aaec726e06096cdfe18ccddb41104a4a88557816b83b(
    *,
    day: jsii.Number,
    month: jsii.Number,
    year: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cda492222b8ebdb111173aaf95a2010eadb16e2ec6584562e34128d44e22ac09(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98dcff02249fff0ff9f871081ff0945b1e1ff4b0ced27c5e81e218b1471b3617(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d47d078661aae0ad2ca5725bf1986b4e0589e42fe186d36e72c360d1f8c1cd5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__042906f8600187603248471afc470dd3beb05f95adf68f9c2240bd419fa35ae5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f6ffacb776284a01334e7973442eeae01eb27ef9bf24d9ca4baaaa1d2804ebe(
    value: typing.Optional[BillingBudgetBudgetFilterCustomPeriodEndDate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab0eeea3da868dbb5b70799c1620dbab53b0383746b6953e9cc2b693f4a1e33a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad98c962063989c22c292cab2dcab0d964c2af728baf1c9993c9317e557c0ac6(
    value: typing.Optional[BillingBudgetBudgetFilterCustomPeriod],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24ca9c314c1272f9d71f24fe997275d069882e2e31d0274635d7b4064f96ba94(
    *,
    day: jsii.Number,
    month: jsii.Number,
    year: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b210b3daab1829177eb7edad74ba99bd2caa0adda54ddf6391bc1fe9ddc4f36b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__108b5601f11ef328e5929638b2ff51e9b37ea2d1d77607a92dbea5fc42130107(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b33386c9780369a513d006d572924d1cb64e5b189cc4c10e27f5d680c782c26(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f580ef77480ac1cbf79aeffca51512c5aac07dcc95a998b372be3c38a144a389(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bd95bae665774801eac431b8154bcababef2fde69e9507c3004217382756fb4(
    value: typing.Optional[BillingBudgetBudgetFilterCustomPeriodStartDate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d16628eb44a66ce48a3d91e5b5d6d2e54868a2c4d9aced3a7a486411619a587d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30436dce086246c0d10fe30936543b7c185d400dc2e100c245262260c5877d6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aead85b2cce313aec938196738e8dc34554f9a76540fa59ad67e28021b68b85(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2066675f88b09775487829b45b641b133844a88f0bbeaa50b008564aaca453a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__823a34453d4eb8ec9a7bec5ea1a982af4772ce974b68ef0246391dcd252814de(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7346576970bddd20b34d5786ef1bc6a02ff4ba65a75cb0bd5f51b7c0478ad863(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87cfc59068082edf7aaa256d72b88dc033fbac9c4132eebe2067e91fc52dc412(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90712c3d84c807b07419016ba47df227214ba27e2ea62c83899b2fcb927824ca(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__289649bc42475d7f77d235bfe2fbc836518c790ec2804a833620653bf81c3d3a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c400e201b27590f86c0dbdb02f9613359af8a53558d465fd17b23b4bdd4aab3a(
    value: typing.Optional[BillingBudgetBudgetFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abd37a5794fc05df231effddbe3129331f4d41764951dbf6261f30cf38da30dc(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    amount: typing.Union[BillingBudgetAmount, typing.Dict[builtins.str, typing.Any]],
    billing_account: builtins.str,
    all_updates_rule: typing.Optional[typing.Union[BillingBudgetAllUpdatesRule, typing.Dict[builtins.str, typing.Any]]] = None,
    budget_filter: typing.Optional[typing.Union[BillingBudgetBudgetFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ownership_scope: typing.Optional[builtins.str] = None,
    threshold_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BillingBudgetThresholdRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[BillingBudgetTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61d0b8711d6f2e4d3755e71c2781c072358dc665aadb7f84d4cf9f87dcfcf35a(
    *,
    threshold_percent: jsii.Number,
    spend_basis: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__772db867830978f5d4bdc24a858ea87e2a1b3faadfa83a22683122da4777b314(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10063bce078be922b35e656d5410c422956baf6d177beed97fb569fd84aa5bb9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78f1320f3e66efa29665b74c2cad8a4185324dab101cfafe846f6d4dff210f65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__270381dae1327d2da9e339d43aece045ec482d047fbdaeefb136fe268e8e6bd1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e86cad4be7ea67402c1bb651cc1136322f88f4d4463102fc04fb7067efe73a57(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__848143449c7ac070f4b083215e80a5b69a0cec981cc2a0f2e4775a93bab4f167(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BillingBudgetThresholdRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__879fd75aab47f0982f94d70dd6f5e0a0e65166c27cc8990aeb9567f7a980a64f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__059a74dfc68e189fad8418155cdd7a13eab4e181ae818e2689117a94a99fd44d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c13314de416c208fe87c04f03a55cd2a3ddadadcc5e931417d24d252fe2029d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7953db5b64e2f3573ce722460f31aa198166f9bb1ed56751fce64304e2be2026(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BillingBudgetThresholdRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d37ee4ab58600a20b2543f0437aab21d44b87aa2b2a7e2039282e64598d6507(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b27780d62e3d858d5935f5f9e6631d4b21e730d0a888ebdaa5205649a72ebf64(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eadbfd56f84b5b07fb80688787395748383ff2e736226d98d8e6b06016611467(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cab818ac00bb3e347f7c414c625a65ed58e9276e57adfe2bb5d2240d97cc79e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f7a66f256804e04c43f9a234061a5cdb4ebf6e3024386c45656f4831bb15b93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d9c432f70219f65dab97dbbaeb3a4a0810eab73f4918b4397d3804c7008bd84(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BillingBudgetTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
