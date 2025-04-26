r'''
# `azuread_access_package_assignment_policy`

Refer to the Terraform Registry for docs: [`azuread_access_package_assignment_policy`](https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy).
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


class AccessPackageAssignmentPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy azuread_access_package_assignment_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        access_package_id: builtins.str,
        description: builtins.str,
        display_name: builtins.str,
        approval_settings: typing.Optional[typing.Union["AccessPackageAssignmentPolicyApprovalSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        assignment_review_settings: typing.Optional[typing.Union["AccessPackageAssignmentPolicyAssignmentReviewSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        duration_in_days: typing.Optional[jsii.Number] = None,
        expiration_date: typing.Optional[builtins.str] = None,
        extension_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        question: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPackageAssignmentPolicyQuestion", typing.Dict[builtins.str, typing.Any]]]]] = None,
        requestor_settings: typing.Optional[typing.Union["AccessPackageAssignmentPolicyRequestorSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["AccessPackageAssignmentPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy azuread_access_package_assignment_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param access_package_id: The ID of the access package that will contain the policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#access_package_id AccessPackageAssignmentPolicy#access_package_id}
        :param description: The description of the policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#description AccessPackageAssignmentPolicy#description}
        :param display_name: The display name of the policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#display_name AccessPackageAssignmentPolicy#display_name}
        :param approval_settings: approval_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#approval_settings AccessPackageAssignmentPolicy#approval_settings}
        :param assignment_review_settings: assignment_review_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#assignment_review_settings AccessPackageAssignmentPolicy#assignment_review_settings}
        :param duration_in_days: How many days this assignment is valid for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#duration_in_days AccessPackageAssignmentPolicy#duration_in_days}
        :param expiration_date: The date that this assignment expires, formatted as an RFC3339 date string in UTC (e.g. 2018-01-01T01:02:03Z). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#expiration_date AccessPackageAssignmentPolicy#expiration_date}
        :param extension_enabled: When enabled, users will be able to request extension of their access to this package before their access expires. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#extension_enabled AccessPackageAssignmentPolicy#extension_enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#id AccessPackageAssignmentPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param question: question block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#question AccessPackageAssignmentPolicy#question}
        :param requestor_settings: requestor_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#requestor_settings AccessPackageAssignmentPolicy#requestor_settings}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#timeouts AccessPackageAssignmentPolicy#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bb64ceb4f26685268acd0adb86b1903bfd9452b77156971ef068739d355d7d8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AccessPackageAssignmentPolicyConfig(
            access_package_id=access_package_id,
            description=description,
            display_name=display_name,
            approval_settings=approval_settings,
            assignment_review_settings=assignment_review_settings,
            duration_in_days=duration_in_days,
            expiration_date=expiration_date,
            extension_enabled=extension_enabled,
            id=id,
            question=question,
            requestor_settings=requestor_settings,
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
        '''Generates CDKTF code for importing a AccessPackageAssignmentPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AccessPackageAssignmentPolicy to import.
        :param import_from_id: The id of the existing AccessPackageAssignmentPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AccessPackageAssignmentPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__293ad9929c259319c055175aa4133209eee3a1d921a093091593c98c4e2c8c6c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putApprovalSettings")
    def put_approval_settings(
        self,
        *,
        approval_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        approval_required_for_extension: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        approval_stage: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPackageAssignmentPolicyApprovalSettingsApprovalStage", typing.Dict[builtins.str, typing.Any]]]]] = None,
        requestor_justification_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param approval_required: Whether an approval is required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#approval_required AccessPackageAssignmentPolicy#approval_required}
        :param approval_required_for_extension: Whether an approval is required to grant extension. Same approval settings used to approve initial access will apply. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#approval_required_for_extension AccessPackageAssignmentPolicy#approval_required_for_extension}
        :param approval_stage: approval_stage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#approval_stage AccessPackageAssignmentPolicy#approval_stage}
        :param requestor_justification_required: Whether requestor are required to provide a justification to request an access package. Justification is visible to other approvers and the requestor Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#requestor_justification_required AccessPackageAssignmentPolicy#requestor_justification_required}
        '''
        value = AccessPackageAssignmentPolicyApprovalSettings(
            approval_required=approval_required,
            approval_required_for_extension=approval_required_for_extension,
            approval_stage=approval_stage,
            requestor_justification_required=requestor_justification_required,
        )

        return typing.cast(None, jsii.invoke(self, "putApprovalSettings", [value]))

    @jsii.member(jsii_name="putAssignmentReviewSettings")
    def put_assignment_review_settings(
        self,
        *,
        access_recommendation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        access_review_timeout_behavior: typing.Optional[builtins.str] = None,
        approver_justification_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        duration_in_days: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        reviewer: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPackageAssignmentPolicyAssignmentReviewSettingsReviewer", typing.Dict[builtins.str, typing.Any]]]]] = None,
        review_frequency: typing.Optional[builtins.str] = None,
        review_type: typing.Optional[builtins.str] = None,
        starting_on: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_recommendation_enabled: Whether to show Show reviewer decision helpers. If enabled, system recommendations based on users' access information will be shown to the reviewers. The reviewer will be recommended to approve the review if the user has signed-in at least once during the last 30 days. The reviewer will be recommended to deny the review if the user has not signed-in during the last 30 days Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#access_recommendation_enabled AccessPackageAssignmentPolicy#access_recommendation_enabled}
        :param access_review_timeout_behavior: What actions the system takes if reviewers don't respond in time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#access_review_timeout_behavior AccessPackageAssignmentPolicy#access_review_timeout_behavior}
        :param approver_justification_required: Whether a reviewer need provide a justification for their decision. Justification is visible to other reviewers and the requestor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#approver_justification_required AccessPackageAssignmentPolicy#approver_justification_required}
        :param duration_in_days: How many days each occurrence of the access review series will run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#duration_in_days AccessPackageAssignmentPolicy#duration_in_days}
        :param enabled: Whether to enable assignment review. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#enabled AccessPackageAssignmentPolicy#enabled}
        :param reviewer: reviewer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#reviewer AccessPackageAssignmentPolicy#reviewer}
        :param review_frequency: This will determine how often the access review campaign runs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#review_frequency AccessPackageAssignmentPolicy#review_frequency}
        :param review_type: Self review or specific reviewers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#review_type AccessPackageAssignmentPolicy#review_type}
        :param starting_on: This is the date the access review campaign will start on, formatted as an RFC3339 date string in UTC(e.g. 2018-01-01T01:02:03Z), default is now. Once an access review has been created, you cannot update its start date. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#starting_on AccessPackageAssignmentPolicy#starting_on}
        '''
        value = AccessPackageAssignmentPolicyAssignmentReviewSettings(
            access_recommendation_enabled=access_recommendation_enabled,
            access_review_timeout_behavior=access_review_timeout_behavior,
            approver_justification_required=approver_justification_required,
            duration_in_days=duration_in_days,
            enabled=enabled,
            reviewer=reviewer,
            review_frequency=review_frequency,
            review_type=review_type,
            starting_on=starting_on,
        )

        return typing.cast(None, jsii.invoke(self, "putAssignmentReviewSettings", [value]))

    @jsii.member(jsii_name="putQuestion")
    def put_question(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPackageAssignmentPolicyQuestion", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e46446b912a7973e0f3cfa29ab03a3f4d39db6f1ead21c6bd686cfb53d2e362)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putQuestion", [value]))

    @jsii.member(jsii_name="putRequestorSettings")
    def put_requestor_settings(
        self,
        *,
        requestor: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPackageAssignmentPolicyRequestorSettingsRequestor", typing.Dict[builtins.str, typing.Any]]]]] = None,
        requests_accepted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        scope_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param requestor: requestor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#requestor AccessPackageAssignmentPolicy#requestor}
        :param requests_accepted: Whether to accept requests now, when disabled, no new requests can be made using this policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#requests_accepted AccessPackageAssignmentPolicy#requests_accepted}
        :param scope_type: Specify the scopes of the requestors. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#scope_type AccessPackageAssignmentPolicy#scope_type}
        '''
        value = AccessPackageAssignmentPolicyRequestorSettings(
            requestor=requestor,
            requests_accepted=requests_accepted,
            scope_type=scope_type,
        )

        return typing.cast(None, jsii.invoke(self, "putRequestorSettings", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#create AccessPackageAssignmentPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#delete AccessPackageAssignmentPolicy#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#read AccessPackageAssignmentPolicy#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#update AccessPackageAssignmentPolicy#update}.
        '''
        value = AccessPackageAssignmentPolicyTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetApprovalSettings")
    def reset_approval_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApprovalSettings", []))

    @jsii.member(jsii_name="resetAssignmentReviewSettings")
    def reset_assignment_review_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssignmentReviewSettings", []))

    @jsii.member(jsii_name="resetDurationInDays")
    def reset_duration_in_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDurationInDays", []))

    @jsii.member(jsii_name="resetExpirationDate")
    def reset_expiration_date(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpirationDate", []))

    @jsii.member(jsii_name="resetExtensionEnabled")
    def reset_extension_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtensionEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetQuestion")
    def reset_question(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuestion", []))

    @jsii.member(jsii_name="resetRequestorSettings")
    def reset_requestor_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestorSettings", []))

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
    @jsii.member(jsii_name="approvalSettings")
    def approval_settings(
        self,
    ) -> "AccessPackageAssignmentPolicyApprovalSettingsOutputReference":
        return typing.cast("AccessPackageAssignmentPolicyApprovalSettingsOutputReference", jsii.get(self, "approvalSettings"))

    @builtins.property
    @jsii.member(jsii_name="assignmentReviewSettings")
    def assignment_review_settings(
        self,
    ) -> "AccessPackageAssignmentPolicyAssignmentReviewSettingsOutputReference":
        return typing.cast("AccessPackageAssignmentPolicyAssignmentReviewSettingsOutputReference", jsii.get(self, "assignmentReviewSettings"))

    @builtins.property
    @jsii.member(jsii_name="question")
    def question(self) -> "AccessPackageAssignmentPolicyQuestionList":
        return typing.cast("AccessPackageAssignmentPolicyQuestionList", jsii.get(self, "question"))

    @builtins.property
    @jsii.member(jsii_name="requestorSettings")
    def requestor_settings(
        self,
    ) -> "AccessPackageAssignmentPolicyRequestorSettingsOutputReference":
        return typing.cast("AccessPackageAssignmentPolicyRequestorSettingsOutputReference", jsii.get(self, "requestorSettings"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "AccessPackageAssignmentPolicyTimeoutsOutputReference":
        return typing.cast("AccessPackageAssignmentPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="accessPackageIdInput")
    def access_package_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessPackageIdInput"))

    @builtins.property
    @jsii.member(jsii_name="approvalSettingsInput")
    def approval_settings_input(
        self,
    ) -> typing.Optional["AccessPackageAssignmentPolicyApprovalSettings"]:
        return typing.cast(typing.Optional["AccessPackageAssignmentPolicyApprovalSettings"], jsii.get(self, "approvalSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="assignmentReviewSettingsInput")
    def assignment_review_settings_input(
        self,
    ) -> typing.Optional["AccessPackageAssignmentPolicyAssignmentReviewSettings"]:
        return typing.cast(typing.Optional["AccessPackageAssignmentPolicyAssignmentReviewSettings"], jsii.get(self, "assignmentReviewSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="durationInDaysInput")
    def duration_in_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "durationInDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="expirationDateInput")
    def expiration_date_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expirationDateInput"))

    @builtins.property
    @jsii.member(jsii_name="extensionEnabledInput")
    def extension_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "extensionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="questionInput")
    def question_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPackageAssignmentPolicyQuestion"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPackageAssignmentPolicyQuestion"]]], jsii.get(self, "questionInput"))

    @builtins.property
    @jsii.member(jsii_name="requestorSettingsInput")
    def requestor_settings_input(
        self,
    ) -> typing.Optional["AccessPackageAssignmentPolicyRequestorSettings"]:
        return typing.cast(typing.Optional["AccessPackageAssignmentPolicyRequestorSettings"], jsii.get(self, "requestorSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AccessPackageAssignmentPolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AccessPackageAssignmentPolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="accessPackageId")
    def access_package_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessPackageId"))

    @access_package_id.setter
    def access_package_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b7623bc184f28d9005843c0f81a72a95497020066720b8a59b179e7ff32d4ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessPackageId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af459ca9ed2195c3d5aa5553b2a9846becc4d2cad745051175615290c33ad027)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20253bab3baf9960a274b9d7125eed3f89748f93bf7e06127897ddca9110fab7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="durationInDays")
    def duration_in_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "durationInDays"))

    @duration_in_days.setter
    def duration_in_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__844aa40fe77cb1a980ee138bf9e9b581920c987e19432993e53df709dec34724)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "durationInDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expirationDate")
    def expiration_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expirationDate"))

    @expiration_date.setter
    def expiration_date(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c78da48df502bf640facaac8812a1d7f30590c28ef616af6cc33808f8ff6189)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expirationDate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="extensionEnabled")
    def extension_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "extensionEnabled"))

    @extension_enabled.setter
    def extension_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__216f2faf8a442791cd9ecc8ae7e6b604c32ab54df3d0bdd911172d3bfba98bc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extensionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96c81d0390af024264703a1baf42a80be0b4fb89163eb04ad1f10fed68234b73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyApprovalSettings",
    jsii_struct_bases=[],
    name_mapping={
        "approval_required": "approvalRequired",
        "approval_required_for_extension": "approvalRequiredForExtension",
        "approval_stage": "approvalStage",
        "requestor_justification_required": "requestorJustificationRequired",
    },
)
class AccessPackageAssignmentPolicyApprovalSettings:
    def __init__(
        self,
        *,
        approval_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        approval_required_for_extension: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        approval_stage: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPackageAssignmentPolicyApprovalSettingsApprovalStage", typing.Dict[builtins.str, typing.Any]]]]] = None,
        requestor_justification_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param approval_required: Whether an approval is required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#approval_required AccessPackageAssignmentPolicy#approval_required}
        :param approval_required_for_extension: Whether an approval is required to grant extension. Same approval settings used to approve initial access will apply. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#approval_required_for_extension AccessPackageAssignmentPolicy#approval_required_for_extension}
        :param approval_stage: approval_stage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#approval_stage AccessPackageAssignmentPolicy#approval_stage}
        :param requestor_justification_required: Whether requestor are required to provide a justification to request an access package. Justification is visible to other approvers and the requestor Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#requestor_justification_required AccessPackageAssignmentPolicy#requestor_justification_required}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__220adbb2f4246db885dbe12f5b5f1278aa851fbce3f93987532d091f252fec55)
            check_type(argname="argument approval_required", value=approval_required, expected_type=type_hints["approval_required"])
            check_type(argname="argument approval_required_for_extension", value=approval_required_for_extension, expected_type=type_hints["approval_required_for_extension"])
            check_type(argname="argument approval_stage", value=approval_stage, expected_type=type_hints["approval_stage"])
            check_type(argname="argument requestor_justification_required", value=requestor_justification_required, expected_type=type_hints["requestor_justification_required"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if approval_required is not None:
            self._values["approval_required"] = approval_required
        if approval_required_for_extension is not None:
            self._values["approval_required_for_extension"] = approval_required_for_extension
        if approval_stage is not None:
            self._values["approval_stage"] = approval_stage
        if requestor_justification_required is not None:
            self._values["requestor_justification_required"] = requestor_justification_required

    @builtins.property
    def approval_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether an approval is required.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#approval_required AccessPackageAssignmentPolicy#approval_required}
        '''
        result = self._values.get("approval_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def approval_required_for_extension(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether an approval is required to grant extension. Same approval settings used to approve initial access will apply.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#approval_required_for_extension AccessPackageAssignmentPolicy#approval_required_for_extension}
        '''
        result = self._values.get("approval_required_for_extension")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def approval_stage(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPackageAssignmentPolicyApprovalSettingsApprovalStage"]]]:
        '''approval_stage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#approval_stage AccessPackageAssignmentPolicy#approval_stage}
        '''
        result = self._values.get("approval_stage")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPackageAssignmentPolicyApprovalSettingsApprovalStage"]]], result)

    @builtins.property
    def requestor_justification_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether requestor are required to provide a justification to request an access package.

        Justification is visible to other approvers and the requestor

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#requestor_justification_required AccessPackageAssignmentPolicy#requestor_justification_required}
        '''
        result = self._values.get("requestor_justification_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPackageAssignmentPolicyApprovalSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyApprovalSettingsApprovalStage",
    jsii_struct_bases=[],
    name_mapping={
        "approval_timeout_in_days": "approvalTimeoutInDays",
        "alternative_approval_enabled": "alternativeApprovalEnabled",
        "alternative_approver": "alternativeApprover",
        "approver_justification_required": "approverJustificationRequired",
        "enable_alternative_approval_in_days": "enableAlternativeApprovalInDays",
        "primary_approver": "primaryApprover",
    },
)
class AccessPackageAssignmentPolicyApprovalSettingsApprovalStage:
    def __init__(
        self,
        *,
        approval_timeout_in_days: jsii.Number,
        alternative_approval_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        alternative_approver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPackageAssignmentPolicyApprovalSettingsApprovalStageAlternativeApprover", typing.Dict[builtins.str, typing.Any]]]]] = None,
        approver_justification_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_alternative_approval_in_days: typing.Optional[jsii.Number] = None,
        primary_approver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPackageAssignmentPolicyApprovalSettingsApprovalStagePrimaryApprover", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param approval_timeout_in_days: Decision must be made in how many days? If a request is not approved within this time period after it is made, it will be automatically rejected Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#approval_timeout_in_days AccessPackageAssignmentPolicy#approval_timeout_in_days}
        :param alternative_approval_enabled: If no action taken, forward to alternate approvers? Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#alternative_approval_enabled AccessPackageAssignmentPolicy#alternative_approval_enabled}
        :param alternative_approver: alternative_approver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#alternative_approver AccessPackageAssignmentPolicy#alternative_approver}
        :param approver_justification_required: Whether an approver must provide a justification for their decision. Justification is visible to other approvers and the requestor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#approver_justification_required AccessPackageAssignmentPolicy#approver_justification_required}
        :param enable_alternative_approval_in_days: Forward to alternate approver(s) after how many days? Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#enable_alternative_approval_in_days AccessPackageAssignmentPolicy#enable_alternative_approval_in_days}
        :param primary_approver: primary_approver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#primary_approver AccessPackageAssignmentPolicy#primary_approver}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e02d56f2cee2ca4bfb69ea922464f90f3a3890da81c44e827afa8ad41ca29a34)
            check_type(argname="argument approval_timeout_in_days", value=approval_timeout_in_days, expected_type=type_hints["approval_timeout_in_days"])
            check_type(argname="argument alternative_approval_enabled", value=alternative_approval_enabled, expected_type=type_hints["alternative_approval_enabled"])
            check_type(argname="argument alternative_approver", value=alternative_approver, expected_type=type_hints["alternative_approver"])
            check_type(argname="argument approver_justification_required", value=approver_justification_required, expected_type=type_hints["approver_justification_required"])
            check_type(argname="argument enable_alternative_approval_in_days", value=enable_alternative_approval_in_days, expected_type=type_hints["enable_alternative_approval_in_days"])
            check_type(argname="argument primary_approver", value=primary_approver, expected_type=type_hints["primary_approver"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "approval_timeout_in_days": approval_timeout_in_days,
        }
        if alternative_approval_enabled is not None:
            self._values["alternative_approval_enabled"] = alternative_approval_enabled
        if alternative_approver is not None:
            self._values["alternative_approver"] = alternative_approver
        if approver_justification_required is not None:
            self._values["approver_justification_required"] = approver_justification_required
        if enable_alternative_approval_in_days is not None:
            self._values["enable_alternative_approval_in_days"] = enable_alternative_approval_in_days
        if primary_approver is not None:
            self._values["primary_approver"] = primary_approver

    @builtins.property
    def approval_timeout_in_days(self) -> jsii.Number:
        '''Decision must be made in how many days?

        If a request is not approved within this time period after it is made, it will be automatically rejected

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#approval_timeout_in_days AccessPackageAssignmentPolicy#approval_timeout_in_days}
        '''
        result = self._values.get("approval_timeout_in_days")
        assert result is not None, "Required property 'approval_timeout_in_days' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def alternative_approval_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If no action taken, forward to alternate approvers?

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#alternative_approval_enabled AccessPackageAssignmentPolicy#alternative_approval_enabled}
        '''
        result = self._values.get("alternative_approval_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def alternative_approver(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPackageAssignmentPolicyApprovalSettingsApprovalStageAlternativeApprover"]]]:
        '''alternative_approver block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#alternative_approver AccessPackageAssignmentPolicy#alternative_approver}
        '''
        result = self._values.get("alternative_approver")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPackageAssignmentPolicyApprovalSettingsApprovalStageAlternativeApprover"]]], result)

    @builtins.property
    def approver_justification_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether an approver must provide a justification for their decision. Justification is visible to other approvers and the requestor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#approver_justification_required AccessPackageAssignmentPolicy#approver_justification_required}
        '''
        result = self._values.get("approver_justification_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_alternative_approval_in_days(self) -> typing.Optional[jsii.Number]:
        '''Forward to alternate approver(s) after how many days?

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#enable_alternative_approval_in_days AccessPackageAssignmentPolicy#enable_alternative_approval_in_days}
        '''
        result = self._values.get("enable_alternative_approval_in_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def primary_approver(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPackageAssignmentPolicyApprovalSettingsApprovalStagePrimaryApprover"]]]:
        '''primary_approver block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#primary_approver AccessPackageAssignmentPolicy#primary_approver}
        '''
        result = self._values.get("primary_approver")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPackageAssignmentPolicyApprovalSettingsApprovalStagePrimaryApprover"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPackageAssignmentPolicyApprovalSettingsApprovalStage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyApprovalSettingsApprovalStageAlternativeApprover",
    jsii_struct_bases=[],
    name_mapping={
        "subject_type": "subjectType",
        "backup": "backup",
        "object_id": "objectId",
    },
)
class AccessPackageAssignmentPolicyApprovalSettingsApprovalStageAlternativeApprover:
    def __init__(
        self,
        *,
        subject_type: builtins.str,
        backup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        object_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param subject_type: Type of users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#subject_type AccessPackageAssignmentPolicy#subject_type}
        :param backup: For a user in an approval stage, this property indicates whether the user is a backup fallback approver. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#backup AccessPackageAssignmentPolicy#backup}
        :param object_id: The object ID of the subject. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#object_id AccessPackageAssignmentPolicy#object_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__711c0d5783023f2f13a5e8a741df6637e31bd0f527069b7f2ce5803cbd6b4d5d)
            check_type(argname="argument subject_type", value=subject_type, expected_type=type_hints["subject_type"])
            check_type(argname="argument backup", value=backup, expected_type=type_hints["backup"])
            check_type(argname="argument object_id", value=object_id, expected_type=type_hints["object_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subject_type": subject_type,
        }
        if backup is not None:
            self._values["backup"] = backup
        if object_id is not None:
            self._values["object_id"] = object_id

    @builtins.property
    def subject_type(self) -> builtins.str:
        '''Type of users.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#subject_type AccessPackageAssignmentPolicy#subject_type}
        '''
        result = self._values.get("subject_type")
        assert result is not None, "Required property 'subject_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backup(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''For a user in an approval stage, this property indicates whether the user is a backup fallback approver.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#backup AccessPackageAssignmentPolicy#backup}
        '''
        result = self._values.get("backup")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def object_id(self) -> typing.Optional[builtins.str]:
        '''The object ID of the subject.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#object_id AccessPackageAssignmentPolicy#object_id}
        '''
        result = self._values.get("object_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPackageAssignmentPolicyApprovalSettingsApprovalStageAlternativeApprover(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessPackageAssignmentPolicyApprovalSettingsApprovalStageAlternativeApproverList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyApprovalSettingsApprovalStageAlternativeApproverList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c83599ab756315cc6cbe63bc4c6e68dc9c0e9a31c25178fb52140aa331407d88)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessPackageAssignmentPolicyApprovalSettingsApprovalStageAlternativeApproverOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3668ac5df01c0618e483a21d5ba01c2c2cea8aa8d7563b1d7ddfcfb460153eca)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessPackageAssignmentPolicyApprovalSettingsApprovalStageAlternativeApproverOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fbf8a0751787d0a3f7ef00553186c989c513970144729e7a3f69ac09eaea2aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__428ee7b5492d595d32106f6e14cf2ee8e6a8ee93362f42fc66c154fde074e843)
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
            type_hints = typing.get_type_hints(_typecheckingstub__14192932f4678f2c1d22c7422439b3c1d00806abace329f08fbfac8be312260d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyApprovalSettingsApprovalStageAlternativeApprover]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyApprovalSettingsApprovalStageAlternativeApprover]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyApprovalSettingsApprovalStageAlternativeApprover]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__905c1704664df067010ea08509e3a22ef12e0e4a1b8893f16742a3c80bc0787d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessPackageAssignmentPolicyApprovalSettingsApprovalStageAlternativeApproverOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyApprovalSettingsApprovalStageAlternativeApproverOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f041bbfac7106726cd8fa6b0bdc613ff00293d1ce1f788e20c6d6b6a0ce1ab7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBackup")
    def reset_backup(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackup", []))

    @jsii.member(jsii_name="resetObjectId")
    def reset_object_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObjectId", []))

    @builtins.property
    @jsii.member(jsii_name="backupInput")
    def backup_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "backupInput"))

    @builtins.property
    @jsii.member(jsii_name="objectIdInput")
    def object_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectTypeInput")
    def subject_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subjectTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="backup")
    def backup(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "backup"))

    @backup.setter
    def backup(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb241c51ba1e534b32bd0ba3d9630497a33cb8b6bd34ab043c55d76b399203f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="objectId")
    def object_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectId"))

    @object_id.setter
    def object_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1540744684cbb39d35b2e3083e9d90d0174a695142f187887c471514a08e0c68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subjectType")
    def subject_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subjectType"))

    @subject_type.setter
    def subject_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0280d8c8e863ac71841f2602156df1edec706ed1de26bc65b7ef9e124d4a92a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subjectType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyApprovalSettingsApprovalStageAlternativeApprover]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyApprovalSettingsApprovalStageAlternativeApprover]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyApprovalSettingsApprovalStageAlternativeApprover]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb84cdc15e7030cc62f7c4f45f6d4081ba9c20d9f41d84a001970238cfc6f596)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessPackageAssignmentPolicyApprovalSettingsApprovalStageList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyApprovalSettingsApprovalStageList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77e3c523f1061ddec511dabaf453ec1f01ae863d4288b139fb975caa70feb779)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessPackageAssignmentPolicyApprovalSettingsApprovalStageOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5570fc0ff3913a13f2587a524a00f655c88355b0541a6f4baad4c0bb86251787)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessPackageAssignmentPolicyApprovalSettingsApprovalStageOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f43d559914eba9e9933e228bd3ff90f96c5d36441b8767932c41f9e025a27f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7df0fd67616cc409011f02d877d7499f27e83cef8088190d78cb301ebf6d9b2b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c04c4b2cb202462c15f55a91d2c4b9c6fcb380a56102fa92bf5584725dbc1db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyApprovalSettingsApprovalStage]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyApprovalSettingsApprovalStage]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyApprovalSettingsApprovalStage]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc80abc7de8cbd74ae5bd84c5a87567988b98c695491bd90dab2f8aec752ded3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessPackageAssignmentPolicyApprovalSettingsApprovalStageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyApprovalSettingsApprovalStageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7dcba8e33d6524aa0032aa6e3cade576d729f46e34c18c74065af9e85608f9a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAlternativeApprover")
    def put_alternative_approver(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPackageAssignmentPolicyApprovalSettingsApprovalStageAlternativeApprover, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4e7fe2f898965fc100c172a22a6d817e05d55fc99a09bcf05d2de46827ce3ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAlternativeApprover", [value]))

    @jsii.member(jsii_name="putPrimaryApprover")
    def put_primary_approver(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPackageAssignmentPolicyApprovalSettingsApprovalStagePrimaryApprover", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd382da4658be3b98acb425c2ab250eb5e508e6b8ba15876c5bcb0a285317ddf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPrimaryApprover", [value]))

    @jsii.member(jsii_name="resetAlternativeApprovalEnabled")
    def reset_alternative_approval_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlternativeApprovalEnabled", []))

    @jsii.member(jsii_name="resetAlternativeApprover")
    def reset_alternative_approver(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlternativeApprover", []))

    @jsii.member(jsii_name="resetApproverJustificationRequired")
    def reset_approver_justification_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApproverJustificationRequired", []))

    @jsii.member(jsii_name="resetEnableAlternativeApprovalInDays")
    def reset_enable_alternative_approval_in_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableAlternativeApprovalInDays", []))

    @jsii.member(jsii_name="resetPrimaryApprover")
    def reset_primary_approver(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryApprover", []))

    @builtins.property
    @jsii.member(jsii_name="alternativeApprover")
    def alternative_approver(
        self,
    ) -> AccessPackageAssignmentPolicyApprovalSettingsApprovalStageAlternativeApproverList:
        return typing.cast(AccessPackageAssignmentPolicyApprovalSettingsApprovalStageAlternativeApproverList, jsii.get(self, "alternativeApprover"))

    @builtins.property
    @jsii.member(jsii_name="primaryApprover")
    def primary_approver(
        self,
    ) -> "AccessPackageAssignmentPolicyApprovalSettingsApprovalStagePrimaryApproverList":
        return typing.cast("AccessPackageAssignmentPolicyApprovalSettingsApprovalStagePrimaryApproverList", jsii.get(self, "primaryApprover"))

    @builtins.property
    @jsii.member(jsii_name="alternativeApprovalEnabledInput")
    def alternative_approval_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "alternativeApprovalEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="alternativeApproverInput")
    def alternative_approver_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyApprovalSettingsApprovalStageAlternativeApprover]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyApprovalSettingsApprovalStageAlternativeApprover]]], jsii.get(self, "alternativeApproverInput"))

    @builtins.property
    @jsii.member(jsii_name="approvalTimeoutInDaysInput")
    def approval_timeout_in_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "approvalTimeoutInDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="approverJustificationRequiredInput")
    def approver_justification_required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "approverJustificationRequiredInput"))

    @builtins.property
    @jsii.member(jsii_name="enableAlternativeApprovalInDaysInput")
    def enable_alternative_approval_in_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "enableAlternativeApprovalInDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryApproverInput")
    def primary_approver_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPackageAssignmentPolicyApprovalSettingsApprovalStagePrimaryApprover"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPackageAssignmentPolicyApprovalSettingsApprovalStagePrimaryApprover"]]], jsii.get(self, "primaryApproverInput"))

    @builtins.property
    @jsii.member(jsii_name="alternativeApprovalEnabled")
    def alternative_approval_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "alternativeApprovalEnabled"))

    @alternative_approval_enabled.setter
    def alternative_approval_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bf16d2fa7568074524e596e1914f5d33dcc75be918e7562b3cc138535d106ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alternativeApprovalEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="approvalTimeoutInDays")
    def approval_timeout_in_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "approvalTimeoutInDays"))

    @approval_timeout_in_days.setter
    def approval_timeout_in_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4685b496a3e285e95a603bb840624be71c0ce30888a66c99d46a1a635d0fc1c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "approvalTimeoutInDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="approverJustificationRequired")
    def approver_justification_required(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "approverJustificationRequired"))

    @approver_justification_required.setter
    def approver_justification_required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a425c98b2304daa2ba7164293ca72bc8e637ed961767e624898cfc80b72b7225)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "approverJustificationRequired", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableAlternativeApprovalInDays")
    def enable_alternative_approval_in_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "enableAlternativeApprovalInDays"))

    @enable_alternative_approval_in_days.setter
    def enable_alternative_approval_in_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__413493b89dc25f7dc1664070a21f9a9a03d8ce4442dc7abc448c7f4645ce0f62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableAlternativeApprovalInDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyApprovalSettingsApprovalStage]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyApprovalSettingsApprovalStage]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyApprovalSettingsApprovalStage]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__024672f5722d26cb27da48035d0f69737a8789558071f93b160ec47d4eef60cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyApprovalSettingsApprovalStagePrimaryApprover",
    jsii_struct_bases=[],
    name_mapping={
        "subject_type": "subjectType",
        "backup": "backup",
        "object_id": "objectId",
    },
)
class AccessPackageAssignmentPolicyApprovalSettingsApprovalStagePrimaryApprover:
    def __init__(
        self,
        *,
        subject_type: builtins.str,
        backup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        object_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param subject_type: Type of users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#subject_type AccessPackageAssignmentPolicy#subject_type}
        :param backup: For a user in an approval stage, this property indicates whether the user is a backup fallback approver. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#backup AccessPackageAssignmentPolicy#backup}
        :param object_id: The object ID of the subject. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#object_id AccessPackageAssignmentPolicy#object_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1ee9e1d062c27c53daf4914f90907ad2c83721afb080ac3654b01a8c4709894)
            check_type(argname="argument subject_type", value=subject_type, expected_type=type_hints["subject_type"])
            check_type(argname="argument backup", value=backup, expected_type=type_hints["backup"])
            check_type(argname="argument object_id", value=object_id, expected_type=type_hints["object_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subject_type": subject_type,
        }
        if backup is not None:
            self._values["backup"] = backup
        if object_id is not None:
            self._values["object_id"] = object_id

    @builtins.property
    def subject_type(self) -> builtins.str:
        '''Type of users.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#subject_type AccessPackageAssignmentPolicy#subject_type}
        '''
        result = self._values.get("subject_type")
        assert result is not None, "Required property 'subject_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backup(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''For a user in an approval stage, this property indicates whether the user is a backup fallback approver.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#backup AccessPackageAssignmentPolicy#backup}
        '''
        result = self._values.get("backup")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def object_id(self) -> typing.Optional[builtins.str]:
        '''The object ID of the subject.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#object_id AccessPackageAssignmentPolicy#object_id}
        '''
        result = self._values.get("object_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPackageAssignmentPolicyApprovalSettingsApprovalStagePrimaryApprover(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessPackageAssignmentPolicyApprovalSettingsApprovalStagePrimaryApproverList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyApprovalSettingsApprovalStagePrimaryApproverList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__06b66d07f229c9b4d2d80ff01eb297e1392de3293951d67d36d5e2c6a53dc7b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessPackageAssignmentPolicyApprovalSettingsApprovalStagePrimaryApproverOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a12ad069ffa2a36922ddb2b04b600683276f4ff5c444f264b8091faea2c7bd5a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessPackageAssignmentPolicyApprovalSettingsApprovalStagePrimaryApproverOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53439b9a629099c7f66db288e67945577341bdf51ca6275ab345aadec15d087d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40c35fb6bcaddf93601c08de4377b6858ad6101d1fbc6fdd463e0547f5cb95a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f98cab3199fcb11f1e68471fc2e42d840d948bde238f12350ca1e5881432c0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyApprovalSettingsApprovalStagePrimaryApprover]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyApprovalSettingsApprovalStagePrimaryApprover]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyApprovalSettingsApprovalStagePrimaryApprover]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9df43e6d9554d2a616969ec07f7279d577e973f0f3b711da71d0e1d594ee65d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessPackageAssignmentPolicyApprovalSettingsApprovalStagePrimaryApproverOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyApprovalSettingsApprovalStagePrimaryApproverOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__080a16df5264187b209b7fb39bb2308e84d27d700abfc36db9aac64d28107f08)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBackup")
    def reset_backup(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackup", []))

    @jsii.member(jsii_name="resetObjectId")
    def reset_object_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObjectId", []))

    @builtins.property
    @jsii.member(jsii_name="backupInput")
    def backup_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "backupInput"))

    @builtins.property
    @jsii.member(jsii_name="objectIdInput")
    def object_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectTypeInput")
    def subject_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subjectTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="backup")
    def backup(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "backup"))

    @backup.setter
    def backup(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce1708f4e770c7175cdc6e75172682d29477ad9145908a0b3aa517f8a3ab533e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="objectId")
    def object_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectId"))

    @object_id.setter
    def object_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeef8dc63c0edc5ac68df2cfbe98fbd2e5dd66a8dfb2545e0e881a5f45271e36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subjectType")
    def subject_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subjectType"))

    @subject_type.setter
    def subject_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d68ac00c5ecd27af089c7e90b63f862ec1082094955d777018b79b60d53dfdcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subjectType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyApprovalSettingsApprovalStagePrimaryApprover]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyApprovalSettingsApprovalStagePrimaryApprover]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyApprovalSettingsApprovalStagePrimaryApprover]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0381b541b93bfdfb6b588c758a73b78daedbe1515515b14f4ed3bcb550abe571)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessPackageAssignmentPolicyApprovalSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyApprovalSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1613bfef6b0e6c4616303a526fc7e6123d42fe59232c43e0e0500f371aff6681)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putApprovalStage")
    def put_approval_stage(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPackageAssignmentPolicyApprovalSettingsApprovalStage, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c60d4c9ed83c12a657e8b98edb75cca236273c18c04e0cf752c948a4b50efce3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putApprovalStage", [value]))

    @jsii.member(jsii_name="resetApprovalRequired")
    def reset_approval_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApprovalRequired", []))

    @jsii.member(jsii_name="resetApprovalRequiredForExtension")
    def reset_approval_required_for_extension(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApprovalRequiredForExtension", []))

    @jsii.member(jsii_name="resetApprovalStage")
    def reset_approval_stage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApprovalStage", []))

    @jsii.member(jsii_name="resetRequestorJustificationRequired")
    def reset_requestor_justification_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestorJustificationRequired", []))

    @builtins.property
    @jsii.member(jsii_name="approvalStage")
    def approval_stage(
        self,
    ) -> AccessPackageAssignmentPolicyApprovalSettingsApprovalStageList:
        return typing.cast(AccessPackageAssignmentPolicyApprovalSettingsApprovalStageList, jsii.get(self, "approvalStage"))

    @builtins.property
    @jsii.member(jsii_name="approvalRequiredForExtensionInput")
    def approval_required_for_extension_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "approvalRequiredForExtensionInput"))

    @builtins.property
    @jsii.member(jsii_name="approvalRequiredInput")
    def approval_required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "approvalRequiredInput"))

    @builtins.property
    @jsii.member(jsii_name="approvalStageInput")
    def approval_stage_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyApprovalSettingsApprovalStage]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyApprovalSettingsApprovalStage]]], jsii.get(self, "approvalStageInput"))

    @builtins.property
    @jsii.member(jsii_name="requestorJustificationRequiredInput")
    def requestor_justification_required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requestorJustificationRequiredInput"))

    @builtins.property
    @jsii.member(jsii_name="approvalRequired")
    def approval_required(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "approvalRequired"))

    @approval_required.setter
    def approval_required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a93f89ba27784f4d4adb0dd36dc3eadae5a7095766a859c0e109f1b2e332cb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "approvalRequired", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="approvalRequiredForExtension")
    def approval_required_for_extension(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "approvalRequiredForExtension"))

    @approval_required_for_extension.setter
    def approval_required_for_extension(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1081dbe9ab37ab6e71ff5229470d73a6ebdc9cae0c23c9b4668bc88a22940eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "approvalRequiredForExtension", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestorJustificationRequired")
    def requestor_justification_required(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requestorJustificationRequired"))

    @requestor_justification_required.setter
    def requestor_justification_required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b09590bfcc89f802c7a7554e0ebe77995a820627bc1d1cbc981991462688d3a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestorJustificationRequired", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessPackageAssignmentPolicyApprovalSettings]:
        return typing.cast(typing.Optional[AccessPackageAssignmentPolicyApprovalSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessPackageAssignmentPolicyApprovalSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ec3f5c659f73022d608bb8ca1272897efaf7911605d18892891aaa495c23bb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyAssignmentReviewSettings",
    jsii_struct_bases=[],
    name_mapping={
        "access_recommendation_enabled": "accessRecommendationEnabled",
        "access_review_timeout_behavior": "accessReviewTimeoutBehavior",
        "approver_justification_required": "approverJustificationRequired",
        "duration_in_days": "durationInDays",
        "enabled": "enabled",
        "reviewer": "reviewer",
        "review_frequency": "reviewFrequency",
        "review_type": "reviewType",
        "starting_on": "startingOn",
    },
)
class AccessPackageAssignmentPolicyAssignmentReviewSettings:
    def __init__(
        self,
        *,
        access_recommendation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        access_review_timeout_behavior: typing.Optional[builtins.str] = None,
        approver_justification_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        duration_in_days: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        reviewer: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPackageAssignmentPolicyAssignmentReviewSettingsReviewer", typing.Dict[builtins.str, typing.Any]]]]] = None,
        review_frequency: typing.Optional[builtins.str] = None,
        review_type: typing.Optional[builtins.str] = None,
        starting_on: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_recommendation_enabled: Whether to show Show reviewer decision helpers. If enabled, system recommendations based on users' access information will be shown to the reviewers. The reviewer will be recommended to approve the review if the user has signed-in at least once during the last 30 days. The reviewer will be recommended to deny the review if the user has not signed-in during the last 30 days Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#access_recommendation_enabled AccessPackageAssignmentPolicy#access_recommendation_enabled}
        :param access_review_timeout_behavior: What actions the system takes if reviewers don't respond in time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#access_review_timeout_behavior AccessPackageAssignmentPolicy#access_review_timeout_behavior}
        :param approver_justification_required: Whether a reviewer need provide a justification for their decision. Justification is visible to other reviewers and the requestor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#approver_justification_required AccessPackageAssignmentPolicy#approver_justification_required}
        :param duration_in_days: How many days each occurrence of the access review series will run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#duration_in_days AccessPackageAssignmentPolicy#duration_in_days}
        :param enabled: Whether to enable assignment review. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#enabled AccessPackageAssignmentPolicy#enabled}
        :param reviewer: reviewer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#reviewer AccessPackageAssignmentPolicy#reviewer}
        :param review_frequency: This will determine how often the access review campaign runs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#review_frequency AccessPackageAssignmentPolicy#review_frequency}
        :param review_type: Self review or specific reviewers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#review_type AccessPackageAssignmentPolicy#review_type}
        :param starting_on: This is the date the access review campaign will start on, formatted as an RFC3339 date string in UTC(e.g. 2018-01-01T01:02:03Z), default is now. Once an access review has been created, you cannot update its start date. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#starting_on AccessPackageAssignmentPolicy#starting_on}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5700b4e716eee83bf2dafbc3ef89fa7c6961e31f742ed618211f0aabfbc32e64)
            check_type(argname="argument access_recommendation_enabled", value=access_recommendation_enabled, expected_type=type_hints["access_recommendation_enabled"])
            check_type(argname="argument access_review_timeout_behavior", value=access_review_timeout_behavior, expected_type=type_hints["access_review_timeout_behavior"])
            check_type(argname="argument approver_justification_required", value=approver_justification_required, expected_type=type_hints["approver_justification_required"])
            check_type(argname="argument duration_in_days", value=duration_in_days, expected_type=type_hints["duration_in_days"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument reviewer", value=reviewer, expected_type=type_hints["reviewer"])
            check_type(argname="argument review_frequency", value=review_frequency, expected_type=type_hints["review_frequency"])
            check_type(argname="argument review_type", value=review_type, expected_type=type_hints["review_type"])
            check_type(argname="argument starting_on", value=starting_on, expected_type=type_hints["starting_on"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_recommendation_enabled is not None:
            self._values["access_recommendation_enabled"] = access_recommendation_enabled
        if access_review_timeout_behavior is not None:
            self._values["access_review_timeout_behavior"] = access_review_timeout_behavior
        if approver_justification_required is not None:
            self._values["approver_justification_required"] = approver_justification_required
        if duration_in_days is not None:
            self._values["duration_in_days"] = duration_in_days
        if enabled is not None:
            self._values["enabled"] = enabled
        if reviewer is not None:
            self._values["reviewer"] = reviewer
        if review_frequency is not None:
            self._values["review_frequency"] = review_frequency
        if review_type is not None:
            self._values["review_type"] = review_type
        if starting_on is not None:
            self._values["starting_on"] = starting_on

    @builtins.property
    def access_recommendation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to show Show reviewer decision helpers.

        If enabled, system recommendations based on users' access information will be shown to the reviewers. The reviewer will be recommended to approve the review if the user has signed-in at least once during the last 30 days. The reviewer will be recommended to deny the review if the user has not signed-in during the last 30 days

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#access_recommendation_enabled AccessPackageAssignmentPolicy#access_recommendation_enabled}
        '''
        result = self._values.get("access_recommendation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def access_review_timeout_behavior(self) -> typing.Optional[builtins.str]:
        '''What actions the system takes if reviewers don't respond in time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#access_review_timeout_behavior AccessPackageAssignmentPolicy#access_review_timeout_behavior}
        '''
        result = self._values.get("access_review_timeout_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def approver_justification_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether a reviewer need provide a justification for their decision. Justification is visible to other reviewers and the requestor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#approver_justification_required AccessPackageAssignmentPolicy#approver_justification_required}
        '''
        result = self._values.get("approver_justification_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def duration_in_days(self) -> typing.Optional[jsii.Number]:
        '''How many days each occurrence of the access review series will run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#duration_in_days AccessPackageAssignmentPolicy#duration_in_days}
        '''
        result = self._values.get("duration_in_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to enable assignment review.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#enabled AccessPackageAssignmentPolicy#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def reviewer(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPackageAssignmentPolicyAssignmentReviewSettingsReviewer"]]]:
        '''reviewer block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#reviewer AccessPackageAssignmentPolicy#reviewer}
        '''
        result = self._values.get("reviewer")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPackageAssignmentPolicyAssignmentReviewSettingsReviewer"]]], result)

    @builtins.property
    def review_frequency(self) -> typing.Optional[builtins.str]:
        '''This will determine how often the access review campaign runs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#review_frequency AccessPackageAssignmentPolicy#review_frequency}
        '''
        result = self._values.get("review_frequency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def review_type(self) -> typing.Optional[builtins.str]:
        '''Self review or specific reviewers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#review_type AccessPackageAssignmentPolicy#review_type}
        '''
        result = self._values.get("review_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def starting_on(self) -> typing.Optional[builtins.str]:
        '''This is the date the access review campaign will start on, formatted as an RFC3339 date string in UTC(e.g. 2018-01-01T01:02:03Z), default is now. Once an access review has been created, you cannot update its start date.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#starting_on AccessPackageAssignmentPolicy#starting_on}
        '''
        result = self._values.get("starting_on")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPackageAssignmentPolicyAssignmentReviewSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessPackageAssignmentPolicyAssignmentReviewSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyAssignmentReviewSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ade70a87336a056a58ca1488333f9f48fb7db4f3d6105606fdec97be581916b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putReviewer")
    def put_reviewer(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPackageAssignmentPolicyAssignmentReviewSettingsReviewer", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ad86c5681836b2a3d38fb214470cf775ad334b239beeff802eeb30181d9b8a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putReviewer", [value]))

    @jsii.member(jsii_name="resetAccessRecommendationEnabled")
    def reset_access_recommendation_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessRecommendationEnabled", []))

    @jsii.member(jsii_name="resetAccessReviewTimeoutBehavior")
    def reset_access_review_timeout_behavior(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessReviewTimeoutBehavior", []))

    @jsii.member(jsii_name="resetApproverJustificationRequired")
    def reset_approver_justification_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApproverJustificationRequired", []))

    @jsii.member(jsii_name="resetDurationInDays")
    def reset_duration_in_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDurationInDays", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetReviewer")
    def reset_reviewer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReviewer", []))

    @jsii.member(jsii_name="resetReviewFrequency")
    def reset_review_frequency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReviewFrequency", []))

    @jsii.member(jsii_name="resetReviewType")
    def reset_review_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReviewType", []))

    @jsii.member(jsii_name="resetStartingOn")
    def reset_starting_on(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartingOn", []))

    @builtins.property
    @jsii.member(jsii_name="reviewer")
    def reviewer(
        self,
    ) -> "AccessPackageAssignmentPolicyAssignmentReviewSettingsReviewerList":
        return typing.cast("AccessPackageAssignmentPolicyAssignmentReviewSettingsReviewerList", jsii.get(self, "reviewer"))

    @builtins.property
    @jsii.member(jsii_name="accessRecommendationEnabledInput")
    def access_recommendation_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "accessRecommendationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="accessReviewTimeoutBehaviorInput")
    def access_review_timeout_behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessReviewTimeoutBehaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="approverJustificationRequiredInput")
    def approver_justification_required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "approverJustificationRequiredInput"))

    @builtins.property
    @jsii.member(jsii_name="durationInDaysInput")
    def duration_in_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "durationInDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="reviewerInput")
    def reviewer_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPackageAssignmentPolicyAssignmentReviewSettingsReviewer"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPackageAssignmentPolicyAssignmentReviewSettingsReviewer"]]], jsii.get(self, "reviewerInput"))

    @builtins.property
    @jsii.member(jsii_name="reviewFrequencyInput")
    def review_frequency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "reviewFrequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="reviewTypeInput")
    def review_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "reviewTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="startingOnInput")
    def starting_on_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startingOnInput"))

    @builtins.property
    @jsii.member(jsii_name="accessRecommendationEnabled")
    def access_recommendation_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "accessRecommendationEnabled"))

    @access_recommendation_enabled.setter
    def access_recommendation_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c9f9c7360c235b3e75d9f994feb84f33f5e3056491e306591d01001b4fc3026)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessRecommendationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="accessReviewTimeoutBehavior")
    def access_review_timeout_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessReviewTimeoutBehavior"))

    @access_review_timeout_behavior.setter
    def access_review_timeout_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__676d737fdbc8010841df031e0ec80e656fff5af55b90f87c50f8b451e1464eb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessReviewTimeoutBehavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="approverJustificationRequired")
    def approver_justification_required(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "approverJustificationRequired"))

    @approver_justification_required.setter
    def approver_justification_required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cb33a6b05d77478f13439f235a9e48e992fd5e480e1e77fc457db843a426007)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "approverJustificationRequired", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="durationInDays")
    def duration_in_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "durationInDays"))

    @duration_in_days.setter
    def duration_in_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4db832b8ce1c08187a5e7d690cb470f7bb06d015a0d662a2c01d1527ffe7c4dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "durationInDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5afd34f5990768cf338680c84e29f88f08adcf49e89f271b7e8ec20292da4f4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reviewFrequency")
    def review_frequency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reviewFrequency"))

    @review_frequency.setter
    def review_frequency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15343308b3c75dcbc900921d7486a3b0748ce4d6614ed2b61ac13e667d520fda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reviewFrequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reviewType")
    def review_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reviewType"))

    @review_type.setter
    def review_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f828b33e1c9da35b2ba470cffab82dce98fa970f1fb22e4b053b642f02084a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reviewType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startingOn")
    def starting_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startingOn"))

    @starting_on.setter
    def starting_on(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac6ae5a17bdfbc0da944d1eb1e633e77b5aa49219dfb422026c07884ac8d5935)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startingOn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessPackageAssignmentPolicyAssignmentReviewSettings]:
        return typing.cast(typing.Optional[AccessPackageAssignmentPolicyAssignmentReviewSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessPackageAssignmentPolicyAssignmentReviewSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92b3c6bf0bc16beac897bf363e0f9979afef2932e35298604e4dee6a237bda78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyAssignmentReviewSettingsReviewer",
    jsii_struct_bases=[],
    name_mapping={
        "subject_type": "subjectType",
        "backup": "backup",
        "object_id": "objectId",
    },
)
class AccessPackageAssignmentPolicyAssignmentReviewSettingsReviewer:
    def __init__(
        self,
        *,
        subject_type: builtins.str,
        backup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        object_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param subject_type: Type of users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#subject_type AccessPackageAssignmentPolicy#subject_type}
        :param backup: For a user in an approval stage, this property indicates whether the user is a backup fallback approver. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#backup AccessPackageAssignmentPolicy#backup}
        :param object_id: The object ID of the subject. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#object_id AccessPackageAssignmentPolicy#object_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1ecc9ff4330371026df85e601f481205c8950038015928a9f3ca8735b9c4295)
            check_type(argname="argument subject_type", value=subject_type, expected_type=type_hints["subject_type"])
            check_type(argname="argument backup", value=backup, expected_type=type_hints["backup"])
            check_type(argname="argument object_id", value=object_id, expected_type=type_hints["object_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subject_type": subject_type,
        }
        if backup is not None:
            self._values["backup"] = backup
        if object_id is not None:
            self._values["object_id"] = object_id

    @builtins.property
    def subject_type(self) -> builtins.str:
        '''Type of users.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#subject_type AccessPackageAssignmentPolicy#subject_type}
        '''
        result = self._values.get("subject_type")
        assert result is not None, "Required property 'subject_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backup(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''For a user in an approval stage, this property indicates whether the user is a backup fallback approver.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#backup AccessPackageAssignmentPolicy#backup}
        '''
        result = self._values.get("backup")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def object_id(self) -> typing.Optional[builtins.str]:
        '''The object ID of the subject.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#object_id AccessPackageAssignmentPolicy#object_id}
        '''
        result = self._values.get("object_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPackageAssignmentPolicyAssignmentReviewSettingsReviewer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessPackageAssignmentPolicyAssignmentReviewSettingsReviewerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyAssignmentReviewSettingsReviewerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__280efc4bd66ab5660559d026c486c549f6d79a51bcf5326e7846ecd181830394)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessPackageAssignmentPolicyAssignmentReviewSettingsReviewerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54e46f4671c176f4fc5738602af2bf025cf746fa0ff16c1273f65b22b0e459c4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessPackageAssignmentPolicyAssignmentReviewSettingsReviewerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24e63b08fdb7df461a03ccf2ae236667ecadf5a45448222cb7c8df0466833d5e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f13b429a5825cb42b23e8f91559a9dd9fa18f550ba835e5da609e13d931f7dd5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d74e643675312ae099882ed70ca1ae464a979668c99ec890c7c762c13a5e3b3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyAssignmentReviewSettingsReviewer]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyAssignmentReviewSettingsReviewer]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyAssignmentReviewSettingsReviewer]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c17d1ed7bc967aeb542131f34dcfadd995cffd31f6dec8838efe56b387f889b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessPackageAssignmentPolicyAssignmentReviewSettingsReviewerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyAssignmentReviewSettingsReviewerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f4f94e308afb10a3113b44abf8e482b875fc283019cde9a8815fb9bfb122498)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBackup")
    def reset_backup(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackup", []))

    @jsii.member(jsii_name="resetObjectId")
    def reset_object_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObjectId", []))

    @builtins.property
    @jsii.member(jsii_name="backupInput")
    def backup_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "backupInput"))

    @builtins.property
    @jsii.member(jsii_name="objectIdInput")
    def object_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectTypeInput")
    def subject_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subjectTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="backup")
    def backup(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "backup"))

    @backup.setter
    def backup(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__219492f69799086dcb5d3ad78aa9274e3bb109537b019c542657fcf23947167c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="objectId")
    def object_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectId"))

    @object_id.setter
    def object_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8bcf081269daf98f0ca4f794d7b5f4270b138fc6672700f37a1c85aaa52bb59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subjectType")
    def subject_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subjectType"))

    @subject_type.setter
    def subject_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0e01626e075dea054eb3fde9edc999324aa793df06c643a265f0170340b14e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subjectType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyAssignmentReviewSettingsReviewer]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyAssignmentReviewSettingsReviewer]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyAssignmentReviewSettingsReviewer]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c55e76956ef7c3b112a719b6c3fa68ad63ba89a18284a3716fbc504c00c137f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "access_package_id": "accessPackageId",
        "description": "description",
        "display_name": "displayName",
        "approval_settings": "approvalSettings",
        "assignment_review_settings": "assignmentReviewSettings",
        "duration_in_days": "durationInDays",
        "expiration_date": "expirationDate",
        "extension_enabled": "extensionEnabled",
        "id": "id",
        "question": "question",
        "requestor_settings": "requestorSettings",
        "timeouts": "timeouts",
    },
)
class AccessPackageAssignmentPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        access_package_id: builtins.str,
        description: builtins.str,
        display_name: builtins.str,
        approval_settings: typing.Optional[typing.Union[AccessPackageAssignmentPolicyApprovalSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        assignment_review_settings: typing.Optional[typing.Union[AccessPackageAssignmentPolicyAssignmentReviewSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        duration_in_days: typing.Optional[jsii.Number] = None,
        expiration_date: typing.Optional[builtins.str] = None,
        extension_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        question: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPackageAssignmentPolicyQuestion", typing.Dict[builtins.str, typing.Any]]]]] = None,
        requestor_settings: typing.Optional[typing.Union["AccessPackageAssignmentPolicyRequestorSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["AccessPackageAssignmentPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param access_package_id: The ID of the access package that will contain the policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#access_package_id AccessPackageAssignmentPolicy#access_package_id}
        :param description: The description of the policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#description AccessPackageAssignmentPolicy#description}
        :param display_name: The display name of the policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#display_name AccessPackageAssignmentPolicy#display_name}
        :param approval_settings: approval_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#approval_settings AccessPackageAssignmentPolicy#approval_settings}
        :param assignment_review_settings: assignment_review_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#assignment_review_settings AccessPackageAssignmentPolicy#assignment_review_settings}
        :param duration_in_days: How many days this assignment is valid for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#duration_in_days AccessPackageAssignmentPolicy#duration_in_days}
        :param expiration_date: The date that this assignment expires, formatted as an RFC3339 date string in UTC (e.g. 2018-01-01T01:02:03Z). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#expiration_date AccessPackageAssignmentPolicy#expiration_date}
        :param extension_enabled: When enabled, users will be able to request extension of their access to this package before their access expires. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#extension_enabled AccessPackageAssignmentPolicy#extension_enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#id AccessPackageAssignmentPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param question: question block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#question AccessPackageAssignmentPolicy#question}
        :param requestor_settings: requestor_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#requestor_settings AccessPackageAssignmentPolicy#requestor_settings}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#timeouts AccessPackageAssignmentPolicy#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(approval_settings, dict):
            approval_settings = AccessPackageAssignmentPolicyApprovalSettings(**approval_settings)
        if isinstance(assignment_review_settings, dict):
            assignment_review_settings = AccessPackageAssignmentPolicyAssignmentReviewSettings(**assignment_review_settings)
        if isinstance(requestor_settings, dict):
            requestor_settings = AccessPackageAssignmentPolicyRequestorSettings(**requestor_settings)
        if isinstance(timeouts, dict):
            timeouts = AccessPackageAssignmentPolicyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27ad95f559e35368bcfb19342ce323224837e3c8779bbac58813a967cc446449)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument access_package_id", value=access_package_id, expected_type=type_hints["access_package_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument approval_settings", value=approval_settings, expected_type=type_hints["approval_settings"])
            check_type(argname="argument assignment_review_settings", value=assignment_review_settings, expected_type=type_hints["assignment_review_settings"])
            check_type(argname="argument duration_in_days", value=duration_in_days, expected_type=type_hints["duration_in_days"])
            check_type(argname="argument expiration_date", value=expiration_date, expected_type=type_hints["expiration_date"])
            check_type(argname="argument extension_enabled", value=extension_enabled, expected_type=type_hints["extension_enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument question", value=question, expected_type=type_hints["question"])
            check_type(argname="argument requestor_settings", value=requestor_settings, expected_type=type_hints["requestor_settings"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_package_id": access_package_id,
            "description": description,
            "display_name": display_name,
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
        if approval_settings is not None:
            self._values["approval_settings"] = approval_settings
        if assignment_review_settings is not None:
            self._values["assignment_review_settings"] = assignment_review_settings
        if duration_in_days is not None:
            self._values["duration_in_days"] = duration_in_days
        if expiration_date is not None:
            self._values["expiration_date"] = expiration_date
        if extension_enabled is not None:
            self._values["extension_enabled"] = extension_enabled
        if id is not None:
            self._values["id"] = id
        if question is not None:
            self._values["question"] = question
        if requestor_settings is not None:
            self._values["requestor_settings"] = requestor_settings
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
    def access_package_id(self) -> builtins.str:
        '''The ID of the access package that will contain the policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#access_package_id AccessPackageAssignmentPolicy#access_package_id}
        '''
        result = self._values.get("access_package_id")
        assert result is not None, "Required property 'access_package_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> builtins.str:
        '''The description of the policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#description AccessPackageAssignmentPolicy#description}
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''The display name of the policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#display_name AccessPackageAssignmentPolicy#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def approval_settings(
        self,
    ) -> typing.Optional[AccessPackageAssignmentPolicyApprovalSettings]:
        '''approval_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#approval_settings AccessPackageAssignmentPolicy#approval_settings}
        '''
        result = self._values.get("approval_settings")
        return typing.cast(typing.Optional[AccessPackageAssignmentPolicyApprovalSettings], result)

    @builtins.property
    def assignment_review_settings(
        self,
    ) -> typing.Optional[AccessPackageAssignmentPolicyAssignmentReviewSettings]:
        '''assignment_review_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#assignment_review_settings AccessPackageAssignmentPolicy#assignment_review_settings}
        '''
        result = self._values.get("assignment_review_settings")
        return typing.cast(typing.Optional[AccessPackageAssignmentPolicyAssignmentReviewSettings], result)

    @builtins.property
    def duration_in_days(self) -> typing.Optional[jsii.Number]:
        '''How many days this assignment is valid for.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#duration_in_days AccessPackageAssignmentPolicy#duration_in_days}
        '''
        result = self._values.get("duration_in_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def expiration_date(self) -> typing.Optional[builtins.str]:
        '''The date that this assignment expires, formatted as an RFC3339 date string in UTC (e.g. 2018-01-01T01:02:03Z).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#expiration_date AccessPackageAssignmentPolicy#expiration_date}
        '''
        result = self._values.get("expiration_date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extension_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When enabled, users will be able to request extension of their access to this package before their access expires.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#extension_enabled AccessPackageAssignmentPolicy#extension_enabled}
        '''
        result = self._values.get("extension_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#id AccessPackageAssignmentPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def question(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPackageAssignmentPolicyQuestion"]]]:
        '''question block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#question AccessPackageAssignmentPolicy#question}
        '''
        result = self._values.get("question")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPackageAssignmentPolicyQuestion"]]], result)

    @builtins.property
    def requestor_settings(
        self,
    ) -> typing.Optional["AccessPackageAssignmentPolicyRequestorSettings"]:
        '''requestor_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#requestor_settings AccessPackageAssignmentPolicy#requestor_settings}
        '''
        result = self._values.get("requestor_settings")
        return typing.cast(typing.Optional["AccessPackageAssignmentPolicyRequestorSettings"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["AccessPackageAssignmentPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#timeouts AccessPackageAssignmentPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["AccessPackageAssignmentPolicyTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPackageAssignmentPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyQuestion",
    jsii_struct_bases=[],
    name_mapping={
        "text": "text",
        "choice": "choice",
        "required": "required",
        "sequence": "sequence",
    },
)
class AccessPackageAssignmentPolicyQuestion:
    def __init__(
        self,
        *,
        text: typing.Union["AccessPackageAssignmentPolicyQuestionText", typing.Dict[builtins.str, typing.Any]],
        choice: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPackageAssignmentPolicyQuestionChoice", typing.Dict[builtins.str, typing.Any]]]]] = None,
        required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sequence: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param text: text block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#text AccessPackageAssignmentPolicy#text}
        :param choice: choice block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#choice AccessPackageAssignmentPolicy#choice}
        :param required: Whether this question is required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#required AccessPackageAssignmentPolicy#required}
        :param sequence: The sequence number of this question. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#sequence AccessPackageAssignmentPolicy#sequence}
        '''
        if isinstance(text, dict):
            text = AccessPackageAssignmentPolicyQuestionText(**text)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36826ed3e82fb25da2ff22d0d77c6021f46b2b0b857ef518481a3f6a7dbbc65f)
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
            check_type(argname="argument choice", value=choice, expected_type=type_hints["choice"])
            check_type(argname="argument required", value=required, expected_type=type_hints["required"])
            check_type(argname="argument sequence", value=sequence, expected_type=type_hints["sequence"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "text": text,
        }
        if choice is not None:
            self._values["choice"] = choice
        if required is not None:
            self._values["required"] = required
        if sequence is not None:
            self._values["sequence"] = sequence

    @builtins.property
    def text(self) -> "AccessPackageAssignmentPolicyQuestionText":
        '''text block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#text AccessPackageAssignmentPolicy#text}
        '''
        result = self._values.get("text")
        assert result is not None, "Required property 'text' is missing"
        return typing.cast("AccessPackageAssignmentPolicyQuestionText", result)

    @builtins.property
    def choice(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPackageAssignmentPolicyQuestionChoice"]]]:
        '''choice block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#choice AccessPackageAssignmentPolicy#choice}
        '''
        result = self._values.get("choice")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPackageAssignmentPolicyQuestionChoice"]]], result)

    @builtins.property
    def required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether this question is required.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#required AccessPackageAssignmentPolicy#required}
        '''
        result = self._values.get("required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def sequence(self) -> typing.Optional[jsii.Number]:
        '''The sequence number of this question.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#sequence AccessPackageAssignmentPolicy#sequence}
        '''
        result = self._values.get("sequence")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPackageAssignmentPolicyQuestion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyQuestionChoice",
    jsii_struct_bases=[],
    name_mapping={"actual_value": "actualValue", "display_value": "displayValue"},
)
class AccessPackageAssignmentPolicyQuestionChoice:
    def __init__(
        self,
        *,
        actual_value: builtins.str,
        display_value: typing.Union["AccessPackageAssignmentPolicyQuestionChoiceDisplayValue", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param actual_value: The actual value of this choice. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#actual_value AccessPackageAssignmentPolicy#actual_value}
        :param display_value: display_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#display_value AccessPackageAssignmentPolicy#display_value}
        '''
        if isinstance(display_value, dict):
            display_value = AccessPackageAssignmentPolicyQuestionChoiceDisplayValue(**display_value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41a5af90b8593cadc5e1a45e9810368c5cca7dd8338101a108b77dfa85c35c90)
            check_type(argname="argument actual_value", value=actual_value, expected_type=type_hints["actual_value"])
            check_type(argname="argument display_value", value=display_value, expected_type=type_hints["display_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actual_value": actual_value,
            "display_value": display_value,
        }

    @builtins.property
    def actual_value(self) -> builtins.str:
        '''The actual value of this choice.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#actual_value AccessPackageAssignmentPolicy#actual_value}
        '''
        result = self._values.get("actual_value")
        assert result is not None, "Required property 'actual_value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_value(
        self,
    ) -> "AccessPackageAssignmentPolicyQuestionChoiceDisplayValue":
        '''display_value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#display_value AccessPackageAssignmentPolicy#display_value}
        '''
        result = self._values.get("display_value")
        assert result is not None, "Required property 'display_value' is missing"
        return typing.cast("AccessPackageAssignmentPolicyQuestionChoiceDisplayValue", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPackageAssignmentPolicyQuestionChoice(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyQuestionChoiceDisplayValue",
    jsii_struct_bases=[],
    name_mapping={"default_text": "defaultText", "localized_text": "localizedText"},
)
class AccessPackageAssignmentPolicyQuestionChoiceDisplayValue:
    def __init__(
        self,
        *,
        default_text: builtins.str,
        localized_text: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPackageAssignmentPolicyQuestionChoiceDisplayValueLocalizedText", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param default_text: The default text of this question. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#default_text AccessPackageAssignmentPolicy#default_text}
        :param localized_text: localized_text block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#localized_text AccessPackageAssignmentPolicy#localized_text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b435c29bc0ae4d1327fdfe8d78ec97d4bf03b197baa8f443c01b4655950d631c)
            check_type(argname="argument default_text", value=default_text, expected_type=type_hints["default_text"])
            check_type(argname="argument localized_text", value=localized_text, expected_type=type_hints["localized_text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_text": default_text,
        }
        if localized_text is not None:
            self._values["localized_text"] = localized_text

    @builtins.property
    def default_text(self) -> builtins.str:
        '''The default text of this question.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#default_text AccessPackageAssignmentPolicy#default_text}
        '''
        result = self._values.get("default_text")
        assert result is not None, "Required property 'default_text' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def localized_text(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPackageAssignmentPolicyQuestionChoiceDisplayValueLocalizedText"]]]:
        '''localized_text block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#localized_text AccessPackageAssignmentPolicy#localized_text}
        '''
        result = self._values.get("localized_text")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPackageAssignmentPolicyQuestionChoiceDisplayValueLocalizedText"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPackageAssignmentPolicyQuestionChoiceDisplayValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyQuestionChoiceDisplayValueLocalizedText",
    jsii_struct_bases=[],
    name_mapping={"content": "content", "language_code": "languageCode"},
)
class AccessPackageAssignmentPolicyQuestionChoiceDisplayValueLocalizedText:
    def __init__(self, *, content: builtins.str, language_code: builtins.str) -> None:
        '''
        :param content: The localized content of this question. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#content AccessPackageAssignmentPolicy#content}
        :param language_code: The language code of this question content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#language_code AccessPackageAssignmentPolicy#language_code}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83ce4417a5cb3b39978ab6ebf28de2a3cfbb9d0debafd3095e8b6c74f67f2b04)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument language_code", value=language_code, expected_type=type_hints["language_code"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
            "language_code": language_code,
        }

    @builtins.property
    def content(self) -> builtins.str:
        '''The localized content of this question.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#content AccessPackageAssignmentPolicy#content}
        '''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def language_code(self) -> builtins.str:
        '''The language code of this question content.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#language_code AccessPackageAssignmentPolicy#language_code}
        '''
        result = self._values.get("language_code")
        assert result is not None, "Required property 'language_code' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPackageAssignmentPolicyQuestionChoiceDisplayValueLocalizedText(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessPackageAssignmentPolicyQuestionChoiceDisplayValueLocalizedTextList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyQuestionChoiceDisplayValueLocalizedTextList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0dd0ad789094036f5d5b14515dc8837c89c552e544b2650957e667f052f57152)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessPackageAssignmentPolicyQuestionChoiceDisplayValueLocalizedTextOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7031e102ee6e4962f6dead6bdb59e88734fd9ee89bd3c9a12ab7b1752b674d8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessPackageAssignmentPolicyQuestionChoiceDisplayValueLocalizedTextOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__733300ced6c4a6bf616ae8e817cf308328e024f4fd66505d6be14df5d0fbbb45)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7520e96b8020062f191d4011da4cb56aa069aeb986d1ba858ce2769b853b99c8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__496491983cab644ac43dd2e8c41b8cef5b9955dbff6712c64d880f64595595b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyQuestionChoiceDisplayValueLocalizedText]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyQuestionChoiceDisplayValueLocalizedText]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyQuestionChoiceDisplayValueLocalizedText]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fd48329261bf8a01cf29ebdd887f31dcdb5500276f78ac530a93a9b9f0efb51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessPackageAssignmentPolicyQuestionChoiceDisplayValueLocalizedTextOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyQuestionChoiceDisplayValueLocalizedTextOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27685953bd736a5d6dbd5b71f8f38a27f01b425ddb3b07c716afa9699cd92442)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="languageCodeInput")
    def language_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "languageCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61390e5e6ff682e76cb37d604104aedb9a8158f4ca53f2bed11530f6cf3fa73a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="languageCode")
    def language_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "languageCode"))

    @language_code.setter
    def language_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7ca565e996aefcb90f8f77d56d7a8cff58827a0f0cfd88cf1b375d70f303f97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "languageCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyQuestionChoiceDisplayValueLocalizedText]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyQuestionChoiceDisplayValueLocalizedText]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyQuestionChoiceDisplayValueLocalizedText]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0210c39a144eb59750c9c93c46abc6af606fcca8882b3135a0d8c91ceab45284)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessPackageAssignmentPolicyQuestionChoiceDisplayValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyQuestionChoiceDisplayValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__814b42db092c521540def828db10020e181fd0e8068594f14554bbbaf6bbdaf5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLocalizedText")
    def put_localized_text(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPackageAssignmentPolicyQuestionChoiceDisplayValueLocalizedText, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de216ffb9caccc0d91c5bc26487d76534657f79640918c2460b60878fafd7456)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLocalizedText", [value]))

    @jsii.member(jsii_name="resetLocalizedText")
    def reset_localized_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalizedText", []))

    @builtins.property
    @jsii.member(jsii_name="localizedText")
    def localized_text(
        self,
    ) -> AccessPackageAssignmentPolicyQuestionChoiceDisplayValueLocalizedTextList:
        return typing.cast(AccessPackageAssignmentPolicyQuestionChoiceDisplayValueLocalizedTextList, jsii.get(self, "localizedText"))

    @builtins.property
    @jsii.member(jsii_name="defaultTextInput")
    def default_text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultTextInput"))

    @builtins.property
    @jsii.member(jsii_name="localizedTextInput")
    def localized_text_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyQuestionChoiceDisplayValueLocalizedText]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyQuestionChoiceDisplayValueLocalizedText]]], jsii.get(self, "localizedTextInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultText")
    def default_text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultText"))

    @default_text.setter
    def default_text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9ab0c5e8e754178ae655f7c8dee5cb89a2ab46cec5ba5933a15bf74e52e75a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultText", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessPackageAssignmentPolicyQuestionChoiceDisplayValue]:
        return typing.cast(typing.Optional[AccessPackageAssignmentPolicyQuestionChoiceDisplayValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessPackageAssignmentPolicyQuestionChoiceDisplayValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a931615cfa30d5f3d94e452b041af671417430dd19f5fbd04fbe3a16793bb780)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessPackageAssignmentPolicyQuestionChoiceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyQuestionChoiceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a15f8ae16416e993addcab6e9e4df6a3899466200a655a07a9c73ba81597c5bd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessPackageAssignmentPolicyQuestionChoiceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09cfa90658b0159cbba546f15c240e84ff6444f128e8ada00af9a9c991991a2c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessPackageAssignmentPolicyQuestionChoiceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b701956f54e3477b19d3fe106aaef118ce5e00d63d6cb5ac7bbed8e2cced23c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__83d3397c46a844439f223de0cd5a432b190e9fb63c42cf63879c8971a635ecb1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2591cc998c738c956f3f21a5b6ad6ee7d4f21c8d864a74300b2ed781de801f4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyQuestionChoice]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyQuestionChoice]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyQuestionChoice]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14d5cae9580df400c9bfda118e37649c600a4bce27179d76fab0d3af8f234f94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessPackageAssignmentPolicyQuestionChoiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyQuestionChoiceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3feb5bd463e8e1c989a8a49f0d69478db34b48626297f2f4114d5438244da0a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDisplayValue")
    def put_display_value(
        self,
        *,
        default_text: builtins.str,
        localized_text: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPackageAssignmentPolicyQuestionChoiceDisplayValueLocalizedText, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param default_text: The default text of this question. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#default_text AccessPackageAssignmentPolicy#default_text}
        :param localized_text: localized_text block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#localized_text AccessPackageAssignmentPolicy#localized_text}
        '''
        value = AccessPackageAssignmentPolicyQuestionChoiceDisplayValue(
            default_text=default_text, localized_text=localized_text
        )

        return typing.cast(None, jsii.invoke(self, "putDisplayValue", [value]))

    @builtins.property
    @jsii.member(jsii_name="displayValue")
    def display_value(
        self,
    ) -> AccessPackageAssignmentPolicyQuestionChoiceDisplayValueOutputReference:
        return typing.cast(AccessPackageAssignmentPolicyQuestionChoiceDisplayValueOutputReference, jsii.get(self, "displayValue"))

    @builtins.property
    @jsii.member(jsii_name="actualValueInput")
    def actual_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actualValueInput"))

    @builtins.property
    @jsii.member(jsii_name="displayValueInput")
    def display_value_input(
        self,
    ) -> typing.Optional[AccessPackageAssignmentPolicyQuestionChoiceDisplayValue]:
        return typing.cast(typing.Optional[AccessPackageAssignmentPolicyQuestionChoiceDisplayValue], jsii.get(self, "displayValueInput"))

    @builtins.property
    @jsii.member(jsii_name="actualValue")
    def actual_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "actualValue"))

    @actual_value.setter
    def actual_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c316b4e1d7059f6d70e24300161f153cb026c9d62d7e0d9fa0f66d566efe16f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actualValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyQuestionChoice]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyQuestionChoice]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyQuestionChoice]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b62fe0cf7336838ad9ec25db3fa8ee84095ad3fb6266c30136ed58bf7a922aab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessPackageAssignmentPolicyQuestionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyQuestionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eaa8bc450fb5bf0268bf1bf3c1b61f9a56709ac26a9556fa0ef9aee88a76bf86)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessPackageAssignmentPolicyQuestionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69304bdbec34a52dddaff883680e0ed0ad8475928a81d766181fde38f126ae1a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessPackageAssignmentPolicyQuestionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12db65b5d8c3ca3bc43b3370b019ac7a40b4641b6830d2f565f13ea92f0b0497)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ba22f08e843582aa998a29d2d8ce2fc6ac14c0682bd164575d3d63eeae89e8c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5c91731677ce7a94dd2f5dbab8fe85a2472e0e949c1f70cdfebde1782737b13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyQuestion]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyQuestion]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyQuestion]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a4aa5d8bfbd432111dae151d4450a2a33de62d007750ffdf03894dbfbbe7209)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessPackageAssignmentPolicyQuestionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyQuestionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7503a84ca8f60423d48518a76d383701458bf3e37d9ec2cc2c38eeeaab1f5fb2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putChoice")
    def put_choice(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPackageAssignmentPolicyQuestionChoice, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__452626d51762aa52baaf3aac9125b6ad4f1ac176a96886cb1a937aab3fee7692)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putChoice", [value]))

    @jsii.member(jsii_name="putText")
    def put_text(
        self,
        *,
        default_text: builtins.str,
        localized_text: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPackageAssignmentPolicyQuestionTextLocalizedText", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param default_text: The default text of this question. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#default_text AccessPackageAssignmentPolicy#default_text}
        :param localized_text: localized_text block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#localized_text AccessPackageAssignmentPolicy#localized_text}
        '''
        value = AccessPackageAssignmentPolicyQuestionText(
            default_text=default_text, localized_text=localized_text
        )

        return typing.cast(None, jsii.invoke(self, "putText", [value]))

    @jsii.member(jsii_name="resetChoice")
    def reset_choice(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChoice", []))

    @jsii.member(jsii_name="resetRequired")
    def reset_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequired", []))

    @jsii.member(jsii_name="resetSequence")
    def reset_sequence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSequence", []))

    @builtins.property
    @jsii.member(jsii_name="choice")
    def choice(self) -> AccessPackageAssignmentPolicyQuestionChoiceList:
        return typing.cast(AccessPackageAssignmentPolicyQuestionChoiceList, jsii.get(self, "choice"))

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> "AccessPackageAssignmentPolicyQuestionTextOutputReference":
        return typing.cast("AccessPackageAssignmentPolicyQuestionTextOutputReference", jsii.get(self, "text"))

    @builtins.property
    @jsii.member(jsii_name="choiceInput")
    def choice_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyQuestionChoice]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyQuestionChoice]]], jsii.get(self, "choiceInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredInput")
    def required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requiredInput"))

    @builtins.property
    @jsii.member(jsii_name="sequenceInput")
    def sequence_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sequenceInput"))

    @builtins.property
    @jsii.member(jsii_name="textInput")
    def text_input(
        self,
    ) -> typing.Optional["AccessPackageAssignmentPolicyQuestionText"]:
        return typing.cast(typing.Optional["AccessPackageAssignmentPolicyQuestionText"], jsii.get(self, "textInput"))

    @builtins.property
    @jsii.member(jsii_name="required")
    def required(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "required"))

    @required.setter
    def required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__258b5095c68f8544109c7cfd11cd2f8fa7f5a970a51c2564aaf6e2798a0ca86f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "required", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sequence")
    def sequence(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sequence"))

    @sequence.setter
    def sequence(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8b4bc16979d7f173fbe695b090b918fb8197f4a4f0aa5582159e23a28dad4de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sequence", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyQuestion]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyQuestion]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyQuestion]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11b1163ac84352f539ef9c0613c50449655393fd72873f430d0f60149f4061fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyQuestionText",
    jsii_struct_bases=[],
    name_mapping={"default_text": "defaultText", "localized_text": "localizedText"},
)
class AccessPackageAssignmentPolicyQuestionText:
    def __init__(
        self,
        *,
        default_text: builtins.str,
        localized_text: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPackageAssignmentPolicyQuestionTextLocalizedText", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param default_text: The default text of this question. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#default_text AccessPackageAssignmentPolicy#default_text}
        :param localized_text: localized_text block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#localized_text AccessPackageAssignmentPolicy#localized_text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__158edee4f5582913fce27a4819a8579866de70c7d0c063c474af26ca8a0f7b56)
            check_type(argname="argument default_text", value=default_text, expected_type=type_hints["default_text"])
            check_type(argname="argument localized_text", value=localized_text, expected_type=type_hints["localized_text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_text": default_text,
        }
        if localized_text is not None:
            self._values["localized_text"] = localized_text

    @builtins.property
    def default_text(self) -> builtins.str:
        '''The default text of this question.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#default_text AccessPackageAssignmentPolicy#default_text}
        '''
        result = self._values.get("default_text")
        assert result is not None, "Required property 'default_text' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def localized_text(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPackageAssignmentPolicyQuestionTextLocalizedText"]]]:
        '''localized_text block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#localized_text AccessPackageAssignmentPolicy#localized_text}
        '''
        result = self._values.get("localized_text")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPackageAssignmentPolicyQuestionTextLocalizedText"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPackageAssignmentPolicyQuestionText(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyQuestionTextLocalizedText",
    jsii_struct_bases=[],
    name_mapping={"content": "content", "language_code": "languageCode"},
)
class AccessPackageAssignmentPolicyQuestionTextLocalizedText:
    def __init__(self, *, content: builtins.str, language_code: builtins.str) -> None:
        '''
        :param content: The localized content of this question. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#content AccessPackageAssignmentPolicy#content}
        :param language_code: The language code of this question content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#language_code AccessPackageAssignmentPolicy#language_code}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2598a96a53f08ef5974e115b122dd5e3b738ff4b5e30bdfab18dc456e7de6a6f)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument language_code", value=language_code, expected_type=type_hints["language_code"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
            "language_code": language_code,
        }

    @builtins.property
    def content(self) -> builtins.str:
        '''The localized content of this question.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#content AccessPackageAssignmentPolicy#content}
        '''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def language_code(self) -> builtins.str:
        '''The language code of this question content.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#language_code AccessPackageAssignmentPolicy#language_code}
        '''
        result = self._values.get("language_code")
        assert result is not None, "Required property 'language_code' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPackageAssignmentPolicyQuestionTextLocalizedText(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessPackageAssignmentPolicyQuestionTextLocalizedTextList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyQuestionTextLocalizedTextList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04c886de462e7991bd44a2f6bac2bc0343ffc0b045c7e3e65f71eb965d1feb3c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessPackageAssignmentPolicyQuestionTextLocalizedTextOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c081b97343a17bd7ec468d834c785f1b65cc54a8e3ad3863d255d6808aab4854)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessPackageAssignmentPolicyQuestionTextLocalizedTextOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__145ffe664f6d6908b8fce9b49db86b3ad01cc11d23829b906a332804c7265aae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__970484e4415df719206493be72f30a08110deb57e4704c8e91cf99f851cd5cda)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcf279b666bfcd954bb152b35e25b3bc5027872aa5618db2154e4b5d73d7d5c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyQuestionTextLocalizedText]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyQuestionTextLocalizedText]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyQuestionTextLocalizedText]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c08c950ce80c11f7e6205ef8445ae6578606eaf8a8a312dee49e9c54b0799f49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessPackageAssignmentPolicyQuestionTextLocalizedTextOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyQuestionTextLocalizedTextOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26e87c4ce13602dee64092fdaf087112cb176a82efb8f56e78acf4bb16d641d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="languageCodeInput")
    def language_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "languageCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6ae517f2cff99ebebc7f11b75ef5335fa574e6e8746dd2135d53d6991c15ce9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="languageCode")
    def language_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "languageCode"))

    @language_code.setter
    def language_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__550996b91fe7ad56d6badc4599ec26026e2f8fae48f1804cc620b03eb4858ae1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "languageCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyQuestionTextLocalizedText]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyQuestionTextLocalizedText]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyQuestionTextLocalizedText]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b03d3cfdc44dedc3a1be5072027f95b9bfeb0d5f9a20d66e84ac47f916f85924)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessPackageAssignmentPolicyQuestionTextOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyQuestionTextOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d9de971cc5a593b6130e32b02b3b964f0c9a0d1fb7b9c226a032e05a662686a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLocalizedText")
    def put_localized_text(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPackageAssignmentPolicyQuestionTextLocalizedText, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8da0d32d8e35b6980f53c32558f089ae9fdfc4252352447fedc654283cf8f779)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLocalizedText", [value]))

    @jsii.member(jsii_name="resetLocalizedText")
    def reset_localized_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalizedText", []))

    @builtins.property
    @jsii.member(jsii_name="localizedText")
    def localized_text(
        self,
    ) -> AccessPackageAssignmentPolicyQuestionTextLocalizedTextList:
        return typing.cast(AccessPackageAssignmentPolicyQuestionTextLocalizedTextList, jsii.get(self, "localizedText"))

    @builtins.property
    @jsii.member(jsii_name="defaultTextInput")
    def default_text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultTextInput"))

    @builtins.property
    @jsii.member(jsii_name="localizedTextInput")
    def localized_text_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyQuestionTextLocalizedText]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyQuestionTextLocalizedText]]], jsii.get(self, "localizedTextInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultText")
    def default_text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultText"))

    @default_text.setter
    def default_text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2085238d43ac343439fe68af96b6e7d247366517cebcc5dd704e20a0dab01f6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultText", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessPackageAssignmentPolicyQuestionText]:
        return typing.cast(typing.Optional[AccessPackageAssignmentPolicyQuestionText], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessPackageAssignmentPolicyQuestionText],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51c59250e2096ca21cb053cbac311b17af61da19c985237514955ac99066d646)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyRequestorSettings",
    jsii_struct_bases=[],
    name_mapping={
        "requestor": "requestor",
        "requests_accepted": "requestsAccepted",
        "scope_type": "scopeType",
    },
)
class AccessPackageAssignmentPolicyRequestorSettings:
    def __init__(
        self,
        *,
        requestor: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPackageAssignmentPolicyRequestorSettingsRequestor", typing.Dict[builtins.str, typing.Any]]]]] = None,
        requests_accepted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        scope_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param requestor: requestor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#requestor AccessPackageAssignmentPolicy#requestor}
        :param requests_accepted: Whether to accept requests now, when disabled, no new requests can be made using this policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#requests_accepted AccessPackageAssignmentPolicy#requests_accepted}
        :param scope_type: Specify the scopes of the requestors. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#scope_type AccessPackageAssignmentPolicy#scope_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6c6e5fb4eada64a3721207ae7419218acbdaec1252b57fbe713824dfbf7227c)
            check_type(argname="argument requestor", value=requestor, expected_type=type_hints["requestor"])
            check_type(argname="argument requests_accepted", value=requests_accepted, expected_type=type_hints["requests_accepted"])
            check_type(argname="argument scope_type", value=scope_type, expected_type=type_hints["scope_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if requestor is not None:
            self._values["requestor"] = requestor
        if requests_accepted is not None:
            self._values["requests_accepted"] = requests_accepted
        if scope_type is not None:
            self._values["scope_type"] = scope_type

    @builtins.property
    def requestor(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPackageAssignmentPolicyRequestorSettingsRequestor"]]]:
        '''requestor block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#requestor AccessPackageAssignmentPolicy#requestor}
        '''
        result = self._values.get("requestor")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPackageAssignmentPolicyRequestorSettingsRequestor"]]], result)

    @builtins.property
    def requests_accepted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to accept requests now, when disabled, no new requests can be made using this policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#requests_accepted AccessPackageAssignmentPolicy#requests_accepted}
        '''
        result = self._values.get("requests_accepted")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def scope_type(self) -> typing.Optional[builtins.str]:
        '''Specify the scopes of the requestors.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#scope_type AccessPackageAssignmentPolicy#scope_type}
        '''
        result = self._values.get("scope_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPackageAssignmentPolicyRequestorSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessPackageAssignmentPolicyRequestorSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyRequestorSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fe3d7308327b8a24be1b654da55472294b8d3decbb606ad63950ff9b71730d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRequestor")
    def put_requestor(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPackageAssignmentPolicyRequestorSettingsRequestor", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed43a6397de9afc9e1368ba4d031027f5224af88bf3bd2e4c64e0ecdf21ed114)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestor", [value]))

    @jsii.member(jsii_name="resetRequestor")
    def reset_requestor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestor", []))

    @jsii.member(jsii_name="resetRequestsAccepted")
    def reset_requests_accepted(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestsAccepted", []))

    @jsii.member(jsii_name="resetScopeType")
    def reset_scope_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScopeType", []))

    @builtins.property
    @jsii.member(jsii_name="requestor")
    def requestor(
        self,
    ) -> "AccessPackageAssignmentPolicyRequestorSettingsRequestorList":
        return typing.cast("AccessPackageAssignmentPolicyRequestorSettingsRequestorList", jsii.get(self, "requestor"))

    @builtins.property
    @jsii.member(jsii_name="requestorInput")
    def requestor_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPackageAssignmentPolicyRequestorSettingsRequestor"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPackageAssignmentPolicyRequestorSettingsRequestor"]]], jsii.get(self, "requestorInput"))

    @builtins.property
    @jsii.member(jsii_name="requestsAcceptedInput")
    def requests_accepted_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requestsAcceptedInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeTypeInput")
    def scope_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="requestsAccepted")
    def requests_accepted(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requestsAccepted"))

    @requests_accepted.setter
    def requests_accepted(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2853c646cde9784000bdd97eb1df0af8cfd800b97d8a7ad9517c3a9c7aac7202)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestsAccepted", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopeType")
    def scope_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scopeType"))

    @scope_type.setter
    def scope_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46dc8cb43523c82ab5169454850a6f02200d7670ed0eaf5394252edf3888b10e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessPackageAssignmentPolicyRequestorSettings]:
        return typing.cast(typing.Optional[AccessPackageAssignmentPolicyRequestorSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessPackageAssignmentPolicyRequestorSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca17c6f7bd81cac6d724c8a085696ef96cf4fa4858ae4b6709777220e3cfe477)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyRequestorSettingsRequestor",
    jsii_struct_bases=[],
    name_mapping={
        "subject_type": "subjectType",
        "backup": "backup",
        "object_id": "objectId",
    },
)
class AccessPackageAssignmentPolicyRequestorSettingsRequestor:
    def __init__(
        self,
        *,
        subject_type: builtins.str,
        backup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        object_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param subject_type: Type of users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#subject_type AccessPackageAssignmentPolicy#subject_type}
        :param backup: For a user in an approval stage, this property indicates whether the user is a backup fallback approver. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#backup AccessPackageAssignmentPolicy#backup}
        :param object_id: The object ID of the subject. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#object_id AccessPackageAssignmentPolicy#object_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8e2d8c012de1984141d53a94c9b5441fdeb9c3f312558825d1ae139a36c3545)
            check_type(argname="argument subject_type", value=subject_type, expected_type=type_hints["subject_type"])
            check_type(argname="argument backup", value=backup, expected_type=type_hints["backup"])
            check_type(argname="argument object_id", value=object_id, expected_type=type_hints["object_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subject_type": subject_type,
        }
        if backup is not None:
            self._values["backup"] = backup
        if object_id is not None:
            self._values["object_id"] = object_id

    @builtins.property
    def subject_type(self) -> builtins.str:
        '''Type of users.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#subject_type AccessPackageAssignmentPolicy#subject_type}
        '''
        result = self._values.get("subject_type")
        assert result is not None, "Required property 'subject_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backup(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''For a user in an approval stage, this property indicates whether the user is a backup fallback approver.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#backup AccessPackageAssignmentPolicy#backup}
        '''
        result = self._values.get("backup")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def object_id(self) -> typing.Optional[builtins.str]:
        '''The object ID of the subject.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#object_id AccessPackageAssignmentPolicy#object_id}
        '''
        result = self._values.get("object_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPackageAssignmentPolicyRequestorSettingsRequestor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessPackageAssignmentPolicyRequestorSettingsRequestorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyRequestorSettingsRequestorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b188a2969196fb8bd9e64737f9389e3d0877fc6a2239c479f2f01c5691df791c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessPackageAssignmentPolicyRequestorSettingsRequestorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f9a1211b1d2f5fe8b467e23bc35853cbbadfd21322a76eb8a7aabb07661aded)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessPackageAssignmentPolicyRequestorSettingsRequestorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9dc79aef28ce85b5d6ed270505322868161e4fc74b7868602f2d661dee59868)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fd3b44c9b1811cf16bd6c699ce61b12ea7d4481f991f30733fb68a1fee7c0b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7f2b078c0a25a1858c2fe9fbd8dafd52b6eb8b35de5a8367df84ca0c0effa97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyRequestorSettingsRequestor]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyRequestorSettingsRequestor]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyRequestorSettingsRequestor]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d6c2383bb0f124fc3563d96d6718d9fbf8f4794eca35a75709477ee340cc70d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessPackageAssignmentPolicyRequestorSettingsRequestorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyRequestorSettingsRequestorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed375576fd725bf5b1d04f980e8d3aa484d212311711e98a34f805d1fffe699b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBackup")
    def reset_backup(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackup", []))

    @jsii.member(jsii_name="resetObjectId")
    def reset_object_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObjectId", []))

    @builtins.property
    @jsii.member(jsii_name="backupInput")
    def backup_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "backupInput"))

    @builtins.property
    @jsii.member(jsii_name="objectIdInput")
    def object_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectTypeInput")
    def subject_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subjectTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="backup")
    def backup(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "backup"))

    @backup.setter
    def backup(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a970d9c865a20e3a200d47299cf5415a0fe08b82b9caae522fb587671f192a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="objectId")
    def object_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectId"))

    @object_id.setter
    def object_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc73a8d5cdffe59e8f4cd4b12737ebde62703b937898095d79f9428221c96c50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subjectType")
    def subject_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subjectType"))

    @subject_type.setter
    def subject_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccc1c5bf70cb13e2e2f32514fb9748a3bae5ce29b083377a3408b9c034d1cdc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subjectType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyRequestorSettingsRequestor]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyRequestorSettingsRequestor]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyRequestorSettingsRequestor]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__628d6a67893cdc61a3b6bceb3723774846b1f0c6fc5da97562d14b41b508b93e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class AccessPackageAssignmentPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#create AccessPackageAssignmentPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#delete AccessPackageAssignmentPolicy#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#read AccessPackageAssignmentPolicy#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#update AccessPackageAssignmentPolicy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebb410d90da0384219f7d2106ef09a3beec215d44ddb25621af93ef31fb50111)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#create AccessPackageAssignmentPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#delete AccessPackageAssignmentPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#read AccessPackageAssignmentPolicy#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/access_package_assignment_policy#update AccessPackageAssignmentPolicy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPackageAssignmentPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessPackageAssignmentPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.accessPackageAssignmentPolicy.AccessPackageAssignmentPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__194b7058bd15dcd93e0a938c56d1a8a42f851da9d712f7261e1d0973f1198f17)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

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
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__65af659438c07d8a4204c5c694aa5a9a97173185563020f821b11a57ec98f6ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6acb77f70726dd0e1773999b367399419ad17abe7d31402a5859281e93a791c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03c21ee6f8b2715c93e68ea7405d04fb7582dfa27c98e6d213290d9519483c54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b7717428a750035624084b38fcb953fc096844f9b5d186454c630fe53f760ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e398a156575361dbb708f66d616d3193b2ba6b88d9df009175802e735a3668b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AccessPackageAssignmentPolicy",
    "AccessPackageAssignmentPolicyApprovalSettings",
    "AccessPackageAssignmentPolicyApprovalSettingsApprovalStage",
    "AccessPackageAssignmentPolicyApprovalSettingsApprovalStageAlternativeApprover",
    "AccessPackageAssignmentPolicyApprovalSettingsApprovalStageAlternativeApproverList",
    "AccessPackageAssignmentPolicyApprovalSettingsApprovalStageAlternativeApproverOutputReference",
    "AccessPackageAssignmentPolicyApprovalSettingsApprovalStageList",
    "AccessPackageAssignmentPolicyApprovalSettingsApprovalStageOutputReference",
    "AccessPackageAssignmentPolicyApprovalSettingsApprovalStagePrimaryApprover",
    "AccessPackageAssignmentPolicyApprovalSettingsApprovalStagePrimaryApproverList",
    "AccessPackageAssignmentPolicyApprovalSettingsApprovalStagePrimaryApproverOutputReference",
    "AccessPackageAssignmentPolicyApprovalSettingsOutputReference",
    "AccessPackageAssignmentPolicyAssignmentReviewSettings",
    "AccessPackageAssignmentPolicyAssignmentReviewSettingsOutputReference",
    "AccessPackageAssignmentPolicyAssignmentReviewSettingsReviewer",
    "AccessPackageAssignmentPolicyAssignmentReviewSettingsReviewerList",
    "AccessPackageAssignmentPolicyAssignmentReviewSettingsReviewerOutputReference",
    "AccessPackageAssignmentPolicyConfig",
    "AccessPackageAssignmentPolicyQuestion",
    "AccessPackageAssignmentPolicyQuestionChoice",
    "AccessPackageAssignmentPolicyQuestionChoiceDisplayValue",
    "AccessPackageAssignmentPolicyQuestionChoiceDisplayValueLocalizedText",
    "AccessPackageAssignmentPolicyQuestionChoiceDisplayValueLocalizedTextList",
    "AccessPackageAssignmentPolicyQuestionChoiceDisplayValueLocalizedTextOutputReference",
    "AccessPackageAssignmentPolicyQuestionChoiceDisplayValueOutputReference",
    "AccessPackageAssignmentPolicyQuestionChoiceList",
    "AccessPackageAssignmentPolicyQuestionChoiceOutputReference",
    "AccessPackageAssignmentPolicyQuestionList",
    "AccessPackageAssignmentPolicyQuestionOutputReference",
    "AccessPackageAssignmentPolicyQuestionText",
    "AccessPackageAssignmentPolicyQuestionTextLocalizedText",
    "AccessPackageAssignmentPolicyQuestionTextLocalizedTextList",
    "AccessPackageAssignmentPolicyQuestionTextLocalizedTextOutputReference",
    "AccessPackageAssignmentPolicyQuestionTextOutputReference",
    "AccessPackageAssignmentPolicyRequestorSettings",
    "AccessPackageAssignmentPolicyRequestorSettingsOutputReference",
    "AccessPackageAssignmentPolicyRequestorSettingsRequestor",
    "AccessPackageAssignmentPolicyRequestorSettingsRequestorList",
    "AccessPackageAssignmentPolicyRequestorSettingsRequestorOutputReference",
    "AccessPackageAssignmentPolicyTimeouts",
    "AccessPackageAssignmentPolicyTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__7bb64ceb4f26685268acd0adb86b1903bfd9452b77156971ef068739d355d7d8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    access_package_id: builtins.str,
    description: builtins.str,
    display_name: builtins.str,
    approval_settings: typing.Optional[typing.Union[AccessPackageAssignmentPolicyApprovalSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    assignment_review_settings: typing.Optional[typing.Union[AccessPackageAssignmentPolicyAssignmentReviewSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    duration_in_days: typing.Optional[jsii.Number] = None,
    expiration_date: typing.Optional[builtins.str] = None,
    extension_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    question: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPackageAssignmentPolicyQuestion, typing.Dict[builtins.str, typing.Any]]]]] = None,
    requestor_settings: typing.Optional[typing.Union[AccessPackageAssignmentPolicyRequestorSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[AccessPackageAssignmentPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__293ad9929c259319c055175aa4133209eee3a1d921a093091593c98c4e2c8c6c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e46446b912a7973e0f3cfa29ab03a3f4d39db6f1ead21c6bd686cfb53d2e362(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPackageAssignmentPolicyQuestion, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b7623bc184f28d9005843c0f81a72a95497020066720b8a59b179e7ff32d4ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af459ca9ed2195c3d5aa5553b2a9846becc4d2cad745051175615290c33ad027(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20253bab3baf9960a274b9d7125eed3f89748f93bf7e06127897ddca9110fab7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__844aa40fe77cb1a980ee138bf9e9b581920c987e19432993e53df709dec34724(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c78da48df502bf640facaac8812a1d7f30590c28ef616af6cc33808f8ff6189(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__216f2faf8a442791cd9ecc8ae7e6b604c32ab54df3d0bdd911172d3bfba98bc3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96c81d0390af024264703a1baf42a80be0b4fb89163eb04ad1f10fed68234b73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__220adbb2f4246db885dbe12f5b5f1278aa851fbce3f93987532d091f252fec55(
    *,
    approval_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    approval_required_for_extension: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    approval_stage: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPackageAssignmentPolicyApprovalSettingsApprovalStage, typing.Dict[builtins.str, typing.Any]]]]] = None,
    requestor_justification_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e02d56f2cee2ca4bfb69ea922464f90f3a3890da81c44e827afa8ad41ca29a34(
    *,
    approval_timeout_in_days: jsii.Number,
    alternative_approval_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    alternative_approver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPackageAssignmentPolicyApprovalSettingsApprovalStageAlternativeApprover, typing.Dict[builtins.str, typing.Any]]]]] = None,
    approver_justification_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_alternative_approval_in_days: typing.Optional[jsii.Number] = None,
    primary_approver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPackageAssignmentPolicyApprovalSettingsApprovalStagePrimaryApprover, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__711c0d5783023f2f13a5e8a741df6637e31bd0f527069b7f2ce5803cbd6b4d5d(
    *,
    subject_type: builtins.str,
    backup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    object_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c83599ab756315cc6cbe63bc4c6e68dc9c0e9a31c25178fb52140aa331407d88(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3668ac5df01c0618e483a21d5ba01c2c2cea8aa8d7563b1d7ddfcfb460153eca(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fbf8a0751787d0a3f7ef00553186c989c513970144729e7a3f69ac09eaea2aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__428ee7b5492d595d32106f6e14cf2ee8e6a8ee93362f42fc66c154fde074e843(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14192932f4678f2c1d22c7422439b3c1d00806abace329f08fbfac8be312260d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__905c1704664df067010ea08509e3a22ef12e0e4a1b8893f16742a3c80bc0787d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyApprovalSettingsApprovalStageAlternativeApprover]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f041bbfac7106726cd8fa6b0bdc613ff00293d1ce1f788e20c6d6b6a0ce1ab7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb241c51ba1e534b32bd0ba3d9630497a33cb8b6bd34ab043c55d76b399203f2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1540744684cbb39d35b2e3083e9d90d0174a695142f187887c471514a08e0c68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0280d8c8e863ac71841f2602156df1edec706ed1de26bc65b7ef9e124d4a92a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb84cdc15e7030cc62f7c4f45f6d4081ba9c20d9f41d84a001970238cfc6f596(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyApprovalSettingsApprovalStageAlternativeApprover]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77e3c523f1061ddec511dabaf453ec1f01ae863d4288b139fb975caa70feb779(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5570fc0ff3913a13f2587a524a00f655c88355b0541a6f4baad4c0bb86251787(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f43d559914eba9e9933e228bd3ff90f96c5d36441b8767932c41f9e025a27f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7df0fd67616cc409011f02d877d7499f27e83cef8088190d78cb301ebf6d9b2b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c04c4b2cb202462c15f55a91d2c4b9c6fcb380a56102fa92bf5584725dbc1db(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc80abc7de8cbd74ae5bd84c5a87567988b98c695491bd90dab2f8aec752ded3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyApprovalSettingsApprovalStage]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7dcba8e33d6524aa0032aa6e3cade576d729f46e34c18c74065af9e85608f9a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4e7fe2f898965fc100c172a22a6d817e05d55fc99a09bcf05d2de46827ce3ba(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPackageAssignmentPolicyApprovalSettingsApprovalStageAlternativeApprover, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd382da4658be3b98acb425c2ab250eb5e508e6b8ba15876c5bcb0a285317ddf(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPackageAssignmentPolicyApprovalSettingsApprovalStagePrimaryApprover, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bf16d2fa7568074524e596e1914f5d33dcc75be918e7562b3cc138535d106ec(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4685b496a3e285e95a603bb840624be71c0ce30888a66c99d46a1a635d0fc1c8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a425c98b2304daa2ba7164293ca72bc8e637ed961767e624898cfc80b72b7225(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__413493b89dc25f7dc1664070a21f9a9a03d8ce4442dc7abc448c7f4645ce0f62(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__024672f5722d26cb27da48035d0f69737a8789558071f93b160ec47d4eef60cf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyApprovalSettingsApprovalStage]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1ee9e1d062c27c53daf4914f90907ad2c83721afb080ac3654b01a8c4709894(
    *,
    subject_type: builtins.str,
    backup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    object_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06b66d07f229c9b4d2d80ff01eb297e1392de3293951d67d36d5e2c6a53dc7b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a12ad069ffa2a36922ddb2b04b600683276f4ff5c444f264b8091faea2c7bd5a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53439b9a629099c7f66db288e67945577341bdf51ca6275ab345aadec15d087d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40c35fb6bcaddf93601c08de4377b6858ad6101d1fbc6fdd463e0547f5cb95a0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f98cab3199fcb11f1e68471fc2e42d840d948bde238f12350ca1e5881432c0a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9df43e6d9554d2a616969ec07f7279d577e973f0f3b711da71d0e1d594ee65d7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyApprovalSettingsApprovalStagePrimaryApprover]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__080a16df5264187b209b7fb39bb2308e84d27d700abfc36db9aac64d28107f08(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce1708f4e770c7175cdc6e75172682d29477ad9145908a0b3aa517f8a3ab533e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeef8dc63c0edc5ac68df2cfbe98fbd2e5dd66a8dfb2545e0e881a5f45271e36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d68ac00c5ecd27af089c7e90b63f862ec1082094955d777018b79b60d53dfdcf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0381b541b93bfdfb6b588c758a73b78daedbe1515515b14f4ed3bcb550abe571(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyApprovalSettingsApprovalStagePrimaryApprover]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1613bfef6b0e6c4616303a526fc7e6123d42fe59232c43e0e0500f371aff6681(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c60d4c9ed83c12a657e8b98edb75cca236273c18c04e0cf752c948a4b50efce3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPackageAssignmentPolicyApprovalSettingsApprovalStage, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a93f89ba27784f4d4adb0dd36dc3eadae5a7095766a859c0e109f1b2e332cb7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1081dbe9ab37ab6e71ff5229470d73a6ebdc9cae0c23c9b4668bc88a22940eb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b09590bfcc89f802c7a7554e0ebe77995a820627bc1d1cbc981991462688d3a0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ec3f5c659f73022d608bb8ca1272897efaf7911605d18892891aaa495c23bb6(
    value: typing.Optional[AccessPackageAssignmentPolicyApprovalSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5700b4e716eee83bf2dafbc3ef89fa7c6961e31f742ed618211f0aabfbc32e64(
    *,
    access_recommendation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    access_review_timeout_behavior: typing.Optional[builtins.str] = None,
    approver_justification_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    duration_in_days: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    reviewer: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPackageAssignmentPolicyAssignmentReviewSettingsReviewer, typing.Dict[builtins.str, typing.Any]]]]] = None,
    review_frequency: typing.Optional[builtins.str] = None,
    review_type: typing.Optional[builtins.str] = None,
    starting_on: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ade70a87336a056a58ca1488333f9f48fb7db4f3d6105606fdec97be581916b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ad86c5681836b2a3d38fb214470cf775ad334b239beeff802eeb30181d9b8a9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPackageAssignmentPolicyAssignmentReviewSettingsReviewer, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c9f9c7360c235b3e75d9f994feb84f33f5e3056491e306591d01001b4fc3026(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__676d737fdbc8010841df031e0ec80e656fff5af55b90f87c50f8b451e1464eb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cb33a6b05d77478f13439f235a9e48e992fd5e480e1e77fc457db843a426007(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4db832b8ce1c08187a5e7d690cb470f7bb06d015a0d662a2c01d1527ffe7c4dc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5afd34f5990768cf338680c84e29f88f08adcf49e89f271b7e8ec20292da4f4e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15343308b3c75dcbc900921d7486a3b0748ce4d6614ed2b61ac13e667d520fda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f828b33e1c9da35b2ba470cffab82dce98fa970f1fb22e4b053b642f02084a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac6ae5a17bdfbc0da944d1eb1e633e77b5aa49219dfb422026c07884ac8d5935(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92b3c6bf0bc16beac897bf363e0f9979afef2932e35298604e4dee6a237bda78(
    value: typing.Optional[AccessPackageAssignmentPolicyAssignmentReviewSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1ecc9ff4330371026df85e601f481205c8950038015928a9f3ca8735b9c4295(
    *,
    subject_type: builtins.str,
    backup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    object_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__280efc4bd66ab5660559d026c486c549f6d79a51bcf5326e7846ecd181830394(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54e46f4671c176f4fc5738602af2bf025cf746fa0ff16c1273f65b22b0e459c4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24e63b08fdb7df461a03ccf2ae236667ecadf5a45448222cb7c8df0466833d5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f13b429a5825cb42b23e8f91559a9dd9fa18f550ba835e5da609e13d931f7dd5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d74e643675312ae099882ed70ca1ae464a979668c99ec890c7c762c13a5e3b3f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c17d1ed7bc967aeb542131f34dcfadd995cffd31f6dec8838efe56b387f889b3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyAssignmentReviewSettingsReviewer]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f4f94e308afb10a3113b44abf8e482b875fc283019cde9a8815fb9bfb122498(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__219492f69799086dcb5d3ad78aa9274e3bb109537b019c542657fcf23947167c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8bcf081269daf98f0ca4f794d7b5f4270b138fc6672700f37a1c85aaa52bb59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0e01626e075dea054eb3fde9edc999324aa793df06c643a265f0170340b14e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c55e76956ef7c3b112a719b6c3fa68ad63ba89a18284a3716fbc504c00c137f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyAssignmentReviewSettingsReviewer]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27ad95f559e35368bcfb19342ce323224837e3c8779bbac58813a967cc446449(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    access_package_id: builtins.str,
    description: builtins.str,
    display_name: builtins.str,
    approval_settings: typing.Optional[typing.Union[AccessPackageAssignmentPolicyApprovalSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    assignment_review_settings: typing.Optional[typing.Union[AccessPackageAssignmentPolicyAssignmentReviewSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    duration_in_days: typing.Optional[jsii.Number] = None,
    expiration_date: typing.Optional[builtins.str] = None,
    extension_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    question: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPackageAssignmentPolicyQuestion, typing.Dict[builtins.str, typing.Any]]]]] = None,
    requestor_settings: typing.Optional[typing.Union[AccessPackageAssignmentPolicyRequestorSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[AccessPackageAssignmentPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36826ed3e82fb25da2ff22d0d77c6021f46b2b0b857ef518481a3f6a7dbbc65f(
    *,
    text: typing.Union[AccessPackageAssignmentPolicyQuestionText, typing.Dict[builtins.str, typing.Any]],
    choice: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPackageAssignmentPolicyQuestionChoice, typing.Dict[builtins.str, typing.Any]]]]] = None,
    required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sequence: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41a5af90b8593cadc5e1a45e9810368c5cca7dd8338101a108b77dfa85c35c90(
    *,
    actual_value: builtins.str,
    display_value: typing.Union[AccessPackageAssignmentPolicyQuestionChoiceDisplayValue, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b435c29bc0ae4d1327fdfe8d78ec97d4bf03b197baa8f443c01b4655950d631c(
    *,
    default_text: builtins.str,
    localized_text: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPackageAssignmentPolicyQuestionChoiceDisplayValueLocalizedText, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83ce4417a5cb3b39978ab6ebf28de2a3cfbb9d0debafd3095e8b6c74f67f2b04(
    *,
    content: builtins.str,
    language_code: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dd0ad789094036f5d5b14515dc8837c89c552e544b2650957e667f052f57152(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7031e102ee6e4962f6dead6bdb59e88734fd9ee89bd3c9a12ab7b1752b674d8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__733300ced6c4a6bf616ae8e817cf308328e024f4fd66505d6be14df5d0fbbb45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7520e96b8020062f191d4011da4cb56aa069aeb986d1ba858ce2769b853b99c8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__496491983cab644ac43dd2e8c41b8cef5b9955dbff6712c64d880f64595595b0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fd48329261bf8a01cf29ebdd887f31dcdb5500276f78ac530a93a9b9f0efb51(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyQuestionChoiceDisplayValueLocalizedText]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27685953bd736a5d6dbd5b71f8f38a27f01b425ddb3b07c716afa9699cd92442(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61390e5e6ff682e76cb37d604104aedb9a8158f4ca53f2bed11530f6cf3fa73a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7ca565e996aefcb90f8f77d56d7a8cff58827a0f0cfd88cf1b375d70f303f97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0210c39a144eb59750c9c93c46abc6af606fcca8882b3135a0d8c91ceab45284(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyQuestionChoiceDisplayValueLocalizedText]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__814b42db092c521540def828db10020e181fd0e8068594f14554bbbaf6bbdaf5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de216ffb9caccc0d91c5bc26487d76534657f79640918c2460b60878fafd7456(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPackageAssignmentPolicyQuestionChoiceDisplayValueLocalizedText, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9ab0c5e8e754178ae655f7c8dee5cb89a2ab46cec5ba5933a15bf74e52e75a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a931615cfa30d5f3d94e452b041af671417430dd19f5fbd04fbe3a16793bb780(
    value: typing.Optional[AccessPackageAssignmentPolicyQuestionChoiceDisplayValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a15f8ae16416e993addcab6e9e4df6a3899466200a655a07a9c73ba81597c5bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09cfa90658b0159cbba546f15c240e84ff6444f128e8ada00af9a9c991991a2c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b701956f54e3477b19d3fe106aaef118ce5e00d63d6cb5ac7bbed8e2cced23c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83d3397c46a844439f223de0cd5a432b190e9fb63c42cf63879c8971a635ecb1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2591cc998c738c956f3f21a5b6ad6ee7d4f21c8d864a74300b2ed781de801f4b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14d5cae9580df400c9bfda118e37649c600a4bce27179d76fab0d3af8f234f94(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyQuestionChoice]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3feb5bd463e8e1c989a8a49f0d69478db34b48626297f2f4114d5438244da0a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c316b4e1d7059f6d70e24300161f153cb026c9d62d7e0d9fa0f66d566efe16f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b62fe0cf7336838ad9ec25db3fa8ee84095ad3fb6266c30136ed58bf7a922aab(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyQuestionChoice]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaa8bc450fb5bf0268bf1bf3c1b61f9a56709ac26a9556fa0ef9aee88a76bf86(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69304bdbec34a52dddaff883680e0ed0ad8475928a81d766181fde38f126ae1a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12db65b5d8c3ca3bc43b3370b019ac7a40b4641b6830d2f565f13ea92f0b0497(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ba22f08e843582aa998a29d2d8ce2fc6ac14c0682bd164575d3d63eeae89e8c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5c91731677ce7a94dd2f5dbab8fe85a2472e0e949c1f70cdfebde1782737b13(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a4aa5d8bfbd432111dae151d4450a2a33de62d007750ffdf03894dbfbbe7209(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyQuestion]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7503a84ca8f60423d48518a76d383701458bf3e37d9ec2cc2c38eeeaab1f5fb2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__452626d51762aa52baaf3aac9125b6ad4f1ac176a96886cb1a937aab3fee7692(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPackageAssignmentPolicyQuestionChoice, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__258b5095c68f8544109c7cfd11cd2f8fa7f5a970a51c2564aaf6e2798a0ca86f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8b4bc16979d7f173fbe695b090b918fb8197f4a4f0aa5582159e23a28dad4de(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11b1163ac84352f539ef9c0613c50449655393fd72873f430d0f60149f4061fa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyQuestion]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__158edee4f5582913fce27a4819a8579866de70c7d0c063c474af26ca8a0f7b56(
    *,
    default_text: builtins.str,
    localized_text: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPackageAssignmentPolicyQuestionTextLocalizedText, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2598a96a53f08ef5974e115b122dd5e3b738ff4b5e30bdfab18dc456e7de6a6f(
    *,
    content: builtins.str,
    language_code: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c886de462e7991bd44a2f6bac2bc0343ffc0b045c7e3e65f71eb965d1feb3c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c081b97343a17bd7ec468d834c785f1b65cc54a8e3ad3863d255d6808aab4854(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__145ffe664f6d6908b8fce9b49db86b3ad01cc11d23829b906a332804c7265aae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__970484e4415df719206493be72f30a08110deb57e4704c8e91cf99f851cd5cda(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf279b666bfcd954bb152b35e25b3bc5027872aa5618db2154e4b5d73d7d5c0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c08c950ce80c11f7e6205ef8445ae6578606eaf8a8a312dee49e9c54b0799f49(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyQuestionTextLocalizedText]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26e87c4ce13602dee64092fdaf087112cb176a82efb8f56e78acf4bb16d641d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6ae517f2cff99ebebc7f11b75ef5335fa574e6e8746dd2135d53d6991c15ce9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__550996b91fe7ad56d6badc4599ec26026e2f8fae48f1804cc620b03eb4858ae1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b03d3cfdc44dedc3a1be5072027f95b9bfeb0d5f9a20d66e84ac47f916f85924(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyQuestionTextLocalizedText]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d9de971cc5a593b6130e32b02b3b964f0c9a0d1fb7b9c226a032e05a662686a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8da0d32d8e35b6980f53c32558f089ae9fdfc4252352447fedc654283cf8f779(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPackageAssignmentPolicyQuestionTextLocalizedText, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2085238d43ac343439fe68af96b6e7d247366517cebcc5dd704e20a0dab01f6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51c59250e2096ca21cb053cbac311b17af61da19c985237514955ac99066d646(
    value: typing.Optional[AccessPackageAssignmentPolicyQuestionText],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6c6e5fb4eada64a3721207ae7419218acbdaec1252b57fbe713824dfbf7227c(
    *,
    requestor: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPackageAssignmentPolicyRequestorSettingsRequestor, typing.Dict[builtins.str, typing.Any]]]]] = None,
    requests_accepted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    scope_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fe3d7308327b8a24be1b654da55472294b8d3decbb606ad63950ff9b71730d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed43a6397de9afc9e1368ba4d031027f5224af88bf3bd2e4c64e0ecdf21ed114(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPackageAssignmentPolicyRequestorSettingsRequestor, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2853c646cde9784000bdd97eb1df0af8cfd800b97d8a7ad9517c3a9c7aac7202(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46dc8cb43523c82ab5169454850a6f02200d7670ed0eaf5394252edf3888b10e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca17c6f7bd81cac6d724c8a085696ef96cf4fa4858ae4b6709777220e3cfe477(
    value: typing.Optional[AccessPackageAssignmentPolicyRequestorSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8e2d8c012de1984141d53a94c9b5441fdeb9c3f312558825d1ae139a36c3545(
    *,
    subject_type: builtins.str,
    backup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    object_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b188a2969196fb8bd9e64737f9389e3d0877fc6a2239c479f2f01c5691df791c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f9a1211b1d2f5fe8b467e23bc35853cbbadfd21322a76eb8a7aabb07661aded(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9dc79aef28ce85b5d6ed270505322868161e4fc74b7868602f2d661dee59868(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fd3b44c9b1811cf16bd6c699ce61b12ea7d4481f991f30733fb68a1fee7c0b9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7f2b078c0a25a1858c2fe9fbd8dafd52b6eb8b35de5a8367df84ca0c0effa97(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d6c2383bb0f124fc3563d96d6718d9fbf8f4794eca35a75709477ee340cc70d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPackageAssignmentPolicyRequestorSettingsRequestor]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed375576fd725bf5b1d04f980e8d3aa484d212311711e98a34f805d1fffe699b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a970d9c865a20e3a200d47299cf5415a0fe08b82b9caae522fb587671f192a1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc73a8d5cdffe59e8f4cd4b12737ebde62703b937898095d79f9428221c96c50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccc1c5bf70cb13e2e2f32514fb9748a3bae5ce29b083377a3408b9c034d1cdc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__628d6a67893cdc61a3b6bceb3723774846b1f0c6fc5da97562d14b41b508b93e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyRequestorSettingsRequestor]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebb410d90da0384219f7d2106ef09a3beec215d44ddb25621af93ef31fb50111(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__194b7058bd15dcd93e0a938c56d1a8a42f851da9d712f7261e1d0973f1198f17(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65af659438c07d8a4204c5c694aa5a9a97173185563020f821b11a57ec98f6ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6acb77f70726dd0e1773999b367399419ad17abe7d31402a5859281e93a791c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03c21ee6f8b2715c93e68ea7405d04fb7582dfa27c98e6d213290d9519483c54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b7717428a750035624084b38fcb953fc096844f9b5d186454c630fe53f760ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e398a156575361dbb708f66d616d3193b2ba6b88d9df009175802e735a3668b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessPackageAssignmentPolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
