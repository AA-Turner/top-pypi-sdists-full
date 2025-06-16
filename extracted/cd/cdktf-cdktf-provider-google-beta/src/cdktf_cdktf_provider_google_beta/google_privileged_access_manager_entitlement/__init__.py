r'''
# `google_privileged_access_manager_entitlement`

Refer to the Terraform Registry for docs: [`google_privileged_access_manager_entitlement`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement).
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


class GooglePrivilegedAccessManagerEntitlement(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivilegedAccessManagerEntitlement.GooglePrivilegedAccessManagerEntitlement",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement google_privileged_access_manager_entitlement}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        eligible_users: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GooglePrivilegedAccessManagerEntitlementEligibleUsers", typing.Dict[builtins.str, typing.Any]]]],
        entitlement_id: builtins.str,
        location: builtins.str,
        max_request_duration: builtins.str,
        parent: builtins.str,
        privileged_access: typing.Union["GooglePrivilegedAccessManagerEntitlementPrivilegedAccess", typing.Dict[builtins.str, typing.Any]],
        requester_justification_config: typing.Union["GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfig", typing.Dict[builtins.str, typing.Any]],
        additional_notification_targets: typing.Optional[typing.Union["GooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargets", typing.Dict[builtins.str, typing.Any]]] = None,
        approval_workflow: typing.Optional[typing.Union["GooglePrivilegedAccessManagerEntitlementApprovalWorkflow", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GooglePrivilegedAccessManagerEntitlementTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement google_privileged_access_manager_entitlement} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param eligible_users: eligible_users block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#eligible_users GooglePrivilegedAccessManagerEntitlement#eligible_users}
        :param entitlement_id: The ID to use for this Entitlement. This will become the last part of the resource name. This value should be 4-63 characters, and valid characters are "[a-z]", "[0-9]", and "-". The first character should be from [a-z]. This value should be unique among all other Entitlements under the specified 'parent'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#entitlement_id GooglePrivilegedAccessManagerEntitlement#entitlement_id}
        :param location: The region of the Entitlement resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#location GooglePrivilegedAccessManagerEntitlement#location}
        :param max_request_duration: The maximum amount of time for which access would be granted for a request. A requester can choose to ask for access for less than this duration but never more. Format: calculate the time in seconds and concatenate it with 's' i.e. 2 hours = "7200s", 45 minutes = "2700s" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#max_request_duration GooglePrivilegedAccessManagerEntitlement#max_request_duration}
        :param parent: Format: projects/{project-id|project-number} or organizations/{organization-number} or folders/{folder-number}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#parent GooglePrivilegedAccessManagerEntitlement#parent}
        :param privileged_access: privileged_access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#privileged_access GooglePrivilegedAccessManagerEntitlement#privileged_access}
        :param requester_justification_config: requester_justification_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#requester_justification_config GooglePrivilegedAccessManagerEntitlement#requester_justification_config}
        :param additional_notification_targets: additional_notification_targets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#additional_notification_targets GooglePrivilegedAccessManagerEntitlement#additional_notification_targets}
        :param approval_workflow: approval_workflow block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#approval_workflow GooglePrivilegedAccessManagerEntitlement#approval_workflow}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#id GooglePrivilegedAccessManagerEntitlement#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#timeouts GooglePrivilegedAccessManagerEntitlement#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e318f0152ba381b30b9900a7d0afde9c459dbb22740ba9246081a051480f8d3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GooglePrivilegedAccessManagerEntitlementConfig(
            eligible_users=eligible_users,
            entitlement_id=entitlement_id,
            location=location,
            max_request_duration=max_request_duration,
            parent=parent,
            privileged_access=privileged_access,
            requester_justification_config=requester_justification_config,
            additional_notification_targets=additional_notification_targets,
            approval_workflow=approval_workflow,
            id=id,
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
        '''Generates CDKTF code for importing a GooglePrivilegedAccessManagerEntitlement resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GooglePrivilegedAccessManagerEntitlement to import.
        :param import_from_id: The id of the existing GooglePrivilegedAccessManagerEntitlement that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GooglePrivilegedAccessManagerEntitlement to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98ae0d583fa5e45ae3f2fecc0c79e1d90ca6ed1d13151b092d6e55ac87660ae2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAdditionalNotificationTargets")
    def put_additional_notification_targets(
        self,
        *,
        admin_email_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
        requester_email_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param admin_email_recipients: Optional. Additional email addresses to be notified when a principal(requester) is granted access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#admin_email_recipients GooglePrivilegedAccessManagerEntitlement#admin_email_recipients}
        :param requester_email_recipients: Optional. Additional email address to be notified about an eligible entitlement. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#requester_email_recipients GooglePrivilegedAccessManagerEntitlement#requester_email_recipients}
        '''
        value = GooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargets(
            admin_email_recipients=admin_email_recipients,
            requester_email_recipients=requester_email_recipients,
        )

        return typing.cast(None, jsii.invoke(self, "putAdditionalNotificationTargets", [value]))

    @jsii.member(jsii_name="putApprovalWorkflow")
    def put_approval_workflow(
        self,
        *,
        manual_approvals: typing.Union["GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param manual_approvals: manual_approvals block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#manual_approvals GooglePrivilegedAccessManagerEntitlement#manual_approvals}
        '''
        value = GooglePrivilegedAccessManagerEntitlementApprovalWorkflow(
            manual_approvals=manual_approvals
        )

        return typing.cast(None, jsii.invoke(self, "putApprovalWorkflow", [value]))

    @jsii.member(jsii_name="putEligibleUsers")
    def put_eligible_users(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GooglePrivilegedAccessManagerEntitlementEligibleUsers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__776571c0d4f9ef341ce9497601511b08e8b90a98fc4d4f396283f84c64ebe8cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEligibleUsers", [value]))

    @jsii.member(jsii_name="putPrivilegedAccess")
    def put_privileged_access(
        self,
        *,
        gcp_iam_access: typing.Union["GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param gcp_iam_access: gcp_iam_access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#gcp_iam_access GooglePrivilegedAccessManagerEntitlement#gcp_iam_access}
        '''
        value = GooglePrivilegedAccessManagerEntitlementPrivilegedAccess(
            gcp_iam_access=gcp_iam_access
        )

        return typing.cast(None, jsii.invoke(self, "putPrivilegedAccess", [value]))

    @jsii.member(jsii_name="putRequesterJustificationConfig")
    def put_requester_justification_config(
        self,
        *,
        not_mandatory: typing.Optional[typing.Union["GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory", typing.Dict[builtins.str, typing.Any]]] = None,
        unstructured: typing.Optional[typing.Union["GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param not_mandatory: not_mandatory block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#not_mandatory GooglePrivilegedAccessManagerEntitlement#not_mandatory}
        :param unstructured: unstructured block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#unstructured GooglePrivilegedAccessManagerEntitlement#unstructured}
        '''
        value = GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfig(
            not_mandatory=not_mandatory, unstructured=unstructured
        )

        return typing.cast(None, jsii.invoke(self, "putRequesterJustificationConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#create GooglePrivilegedAccessManagerEntitlement#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#delete GooglePrivilegedAccessManagerEntitlement#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#update GooglePrivilegedAccessManagerEntitlement#update}.
        '''
        value = GooglePrivilegedAccessManagerEntitlementTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAdditionalNotificationTargets")
    def reset_additional_notification_targets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalNotificationTargets", []))

    @jsii.member(jsii_name="resetApprovalWorkflow")
    def reset_approval_workflow(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApprovalWorkflow", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="additionalNotificationTargets")
    def additional_notification_targets(
        self,
    ) -> "GooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargetsOutputReference":
        return typing.cast("GooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargetsOutputReference", jsii.get(self, "additionalNotificationTargets"))

    @builtins.property
    @jsii.member(jsii_name="approvalWorkflow")
    def approval_workflow(
        self,
    ) -> "GooglePrivilegedAccessManagerEntitlementApprovalWorkflowOutputReference":
        return typing.cast("GooglePrivilegedAccessManagerEntitlementApprovalWorkflowOutputReference", jsii.get(self, "approvalWorkflow"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="eligibleUsers")
    def eligible_users(
        self,
    ) -> "GooglePrivilegedAccessManagerEntitlementEligibleUsersList":
        return typing.cast("GooglePrivilegedAccessManagerEntitlementEligibleUsersList", jsii.get(self, "eligibleUsers"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="privilegedAccess")
    def privileged_access(
        self,
    ) -> "GooglePrivilegedAccessManagerEntitlementPrivilegedAccessOutputReference":
        return typing.cast("GooglePrivilegedAccessManagerEntitlementPrivilegedAccessOutputReference", jsii.get(self, "privilegedAccess"))

    @builtins.property
    @jsii.member(jsii_name="requesterJustificationConfig")
    def requester_justification_config(
        self,
    ) -> "GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigOutputReference":
        return typing.cast("GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigOutputReference", jsii.get(self, "requesterJustificationConfig"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "GooglePrivilegedAccessManagerEntitlementTimeoutsOutputReference":
        return typing.cast("GooglePrivilegedAccessManagerEntitlementTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="additionalNotificationTargetsInput")
    def additional_notification_targets_input(
        self,
    ) -> typing.Optional["GooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargets"]:
        return typing.cast(typing.Optional["GooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargets"], jsii.get(self, "additionalNotificationTargetsInput"))

    @builtins.property
    @jsii.member(jsii_name="approvalWorkflowInput")
    def approval_workflow_input(
        self,
    ) -> typing.Optional["GooglePrivilegedAccessManagerEntitlementApprovalWorkflow"]:
        return typing.cast(typing.Optional["GooglePrivilegedAccessManagerEntitlementApprovalWorkflow"], jsii.get(self, "approvalWorkflowInput"))

    @builtins.property
    @jsii.member(jsii_name="eligibleUsersInput")
    def eligible_users_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GooglePrivilegedAccessManagerEntitlementEligibleUsers"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GooglePrivilegedAccessManagerEntitlementEligibleUsers"]]], jsii.get(self, "eligibleUsersInput"))

    @builtins.property
    @jsii.member(jsii_name="entitlementIdInput")
    def entitlement_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "entitlementIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRequestDurationInput")
    def max_request_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxRequestDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="parentInput")
    def parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentInput"))

    @builtins.property
    @jsii.member(jsii_name="privilegedAccessInput")
    def privileged_access_input(
        self,
    ) -> typing.Optional["GooglePrivilegedAccessManagerEntitlementPrivilegedAccess"]:
        return typing.cast(typing.Optional["GooglePrivilegedAccessManagerEntitlementPrivilegedAccess"], jsii.get(self, "privilegedAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="requesterJustificationConfigInput")
    def requester_justification_config_input(
        self,
    ) -> typing.Optional["GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfig"]:
        return typing.cast(typing.Optional["GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfig"], jsii.get(self, "requesterJustificationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GooglePrivilegedAccessManagerEntitlementTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GooglePrivilegedAccessManagerEntitlementTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="entitlementId")
    def entitlement_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entitlementId"))

    @entitlement_id.setter
    def entitlement_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69d299f26c0ea7401c016bec8fc3333bd4a0baf7593c8035fd2b848ed2627aa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entitlementId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e0a1effc5ab70e928de713894ed9b663e3a3434712432e9352b0bc2fbe5c5a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15d8b441878297141c9a08f54190ff9d61e6ab6a4a0655e7b128e28c58f76c04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRequestDuration")
    def max_request_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxRequestDuration"))

    @max_request_duration.setter
    def max_request_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d43eecd83ebd58b2525e2c67e8f102de68114748e15661981f1fd16f953f5ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRequestDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e86aacf4347b30610d6a8204e5e4ba3481bf96ea32415d43323b5d3bc5c86344)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePrivilegedAccessManagerEntitlement.GooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargets",
    jsii_struct_bases=[],
    name_mapping={
        "admin_email_recipients": "adminEmailRecipients",
        "requester_email_recipients": "requesterEmailRecipients",
    },
)
class GooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargets:
    def __init__(
        self,
        *,
        admin_email_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
        requester_email_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param admin_email_recipients: Optional. Additional email addresses to be notified when a principal(requester) is granted access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#admin_email_recipients GooglePrivilegedAccessManagerEntitlement#admin_email_recipients}
        :param requester_email_recipients: Optional. Additional email address to be notified about an eligible entitlement. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#requester_email_recipients GooglePrivilegedAccessManagerEntitlement#requester_email_recipients}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf57fa7e4d441163b94daea7783866d9eef4704626816c2f641bc88c4f7c4b38)
            check_type(argname="argument admin_email_recipients", value=admin_email_recipients, expected_type=type_hints["admin_email_recipients"])
            check_type(argname="argument requester_email_recipients", value=requester_email_recipients, expected_type=type_hints["requester_email_recipients"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if admin_email_recipients is not None:
            self._values["admin_email_recipients"] = admin_email_recipients
        if requester_email_recipients is not None:
            self._values["requester_email_recipients"] = requester_email_recipients

    @builtins.property
    def admin_email_recipients(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. Additional email addresses to be notified when a principal(requester) is granted access.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#admin_email_recipients GooglePrivilegedAccessManagerEntitlement#admin_email_recipients}
        '''
        result = self._values.get("admin_email_recipients")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def requester_email_recipients(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. Additional email address to be notified about an eligible entitlement.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#requester_email_recipients GooglePrivilegedAccessManagerEntitlement#requester_email_recipients}
        '''
        result = self._values.get("requester_email_recipients")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargetsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivilegedAccessManagerEntitlement.GooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargetsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4452b6e0547c4fc83c9caaf5696cfe318b9b5960001a0cf16cdfc5e8a7e5e7b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAdminEmailRecipients")
    def reset_admin_email_recipients(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminEmailRecipients", []))

    @jsii.member(jsii_name="resetRequesterEmailRecipients")
    def reset_requester_email_recipients(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequesterEmailRecipients", []))

    @builtins.property
    @jsii.member(jsii_name="adminEmailRecipientsInput")
    def admin_email_recipients_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "adminEmailRecipientsInput"))

    @builtins.property
    @jsii.member(jsii_name="requesterEmailRecipientsInput")
    def requester_email_recipients_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "requesterEmailRecipientsInput"))

    @builtins.property
    @jsii.member(jsii_name="adminEmailRecipients")
    def admin_email_recipients(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "adminEmailRecipients"))

    @admin_email_recipients.setter
    def admin_email_recipients(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4260b7a3f278f12158285f4855b87f8d1765e7dbf0b99f706ca9e457ce2645b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminEmailRecipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requesterEmailRecipients")
    def requester_email_recipients(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "requesterEmailRecipients"))

    @requester_email_recipients.setter
    def requester_email_recipients(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14e44c9054f8778f4d6e7e1c26214bf3f721b4c043f630473e9c31a44f09cc95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requesterEmailRecipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargets]:
        return typing.cast(typing.Optional[GooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ba0edb4da219fa732ab46c424828dc3b2512f6be557017c42ffdfe93325d4fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePrivilegedAccessManagerEntitlement.GooglePrivilegedAccessManagerEntitlementApprovalWorkflow",
    jsii_struct_bases=[],
    name_mapping={"manual_approvals": "manualApprovals"},
)
class GooglePrivilegedAccessManagerEntitlementApprovalWorkflow:
    def __init__(
        self,
        *,
        manual_approvals: typing.Union["GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param manual_approvals: manual_approvals block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#manual_approvals GooglePrivilegedAccessManagerEntitlement#manual_approvals}
        '''
        if isinstance(manual_approvals, dict):
            manual_approvals = GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals(**manual_approvals)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4db3a123da1b4a3010fe5b85ab0b07576f839cf3ff6fbb6d7d5902293491a0e1)
            check_type(argname="argument manual_approvals", value=manual_approvals, expected_type=type_hints["manual_approvals"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "manual_approvals": manual_approvals,
        }

    @builtins.property
    def manual_approvals(
        self,
    ) -> "GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals":
        '''manual_approvals block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#manual_approvals GooglePrivilegedAccessManagerEntitlement#manual_approvals}
        '''
        result = self._values.get("manual_approvals")
        assert result is not None, "Required property 'manual_approvals' is missing"
        return typing.cast("GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePrivilegedAccessManagerEntitlementApprovalWorkflow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePrivilegedAccessManagerEntitlement.GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals",
    jsii_struct_bases=[],
    name_mapping={
        "steps": "steps",
        "require_approver_justification": "requireApproverJustification",
    },
)
class GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals:
    def __init__(
        self,
        *,
        steps: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps", typing.Dict[builtins.str, typing.Any]]]],
        require_approver_justification: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param steps: steps block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#steps GooglePrivilegedAccessManagerEntitlement#steps}
        :param require_approver_justification: Optional. Do the approvers need to provide a justification for their actions? Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#require_approver_justification GooglePrivilegedAccessManagerEntitlement#require_approver_justification}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b370c1e2cf0a596bc369775013c7898710e9d1625f2382c4891495f12629f4ef)
            check_type(argname="argument steps", value=steps, expected_type=type_hints["steps"])
            check_type(argname="argument require_approver_justification", value=require_approver_justification, expected_type=type_hints["require_approver_justification"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "steps": steps,
        }
        if require_approver_justification is not None:
            self._values["require_approver_justification"] = require_approver_justification

    @builtins.property
    def steps(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps"]]:
        '''steps block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#steps GooglePrivilegedAccessManagerEntitlement#steps}
        '''
        result = self._values.get("steps")
        assert result is not None, "Required property 'steps' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps"]], result)

    @builtins.property
    def require_approver_justification(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. Do the approvers need to provide a justification for their actions?

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#require_approver_justification GooglePrivilegedAccessManagerEntitlement#require_approver_justification}
        '''
        result = self._values.get("require_approver_justification")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivilegedAccessManagerEntitlement.GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f450b3a8f64143b18e4feec62ed0145f836cf81d8c424974befcc3e730583ee7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSteps")
    def put_steps(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46747e89344484df98f598a3c8bb13d224a30931643bd8efe31c0d57ee684f51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSteps", [value]))

    @jsii.member(jsii_name="resetRequireApproverJustification")
    def reset_require_approver_justification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireApproverJustification", []))

    @builtins.property
    @jsii.member(jsii_name="steps")
    def steps(
        self,
    ) -> "GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsList":
        return typing.cast("GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsList", jsii.get(self, "steps"))

    @builtins.property
    @jsii.member(jsii_name="requireApproverJustificationInput")
    def require_approver_justification_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireApproverJustificationInput"))

    @builtins.property
    @jsii.member(jsii_name="stepsInput")
    def steps_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps"]]], jsii.get(self, "stepsInput"))

    @builtins.property
    @jsii.member(jsii_name="requireApproverJustification")
    def require_approver_justification(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireApproverJustification"))

    @require_approver_justification.setter
    def require_approver_justification(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__374e7adf3fdd77798561c665a3af9f0903226ad7e9453354ab357cdcc39b646c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireApproverJustification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals]:
        return typing.cast(typing.Optional[GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2d2a79f0e54ab7f3d104c09f1cde825d870d306af16e38447032e550fa12629)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePrivilegedAccessManagerEntitlement.GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps",
    jsii_struct_bases=[],
    name_mapping={
        "approvers": "approvers",
        "approvals_needed": "approvalsNeeded",
        "approver_email_recipients": "approverEmailRecipients",
    },
)
class GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps:
    def __init__(
        self,
        *,
        approvers: typing.Union["GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers", typing.Dict[builtins.str, typing.Any]],
        approvals_needed: typing.Optional[jsii.Number] = None,
        approver_email_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param approvers: approvers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#approvers GooglePrivilegedAccessManagerEntitlement#approvers}
        :param approvals_needed: How many users from the above list need to approve. If there are not enough distinct users in the list above then the workflow will indefinitely block. Should always be greater than 0. Currently 1 is the only supported value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#approvals_needed GooglePrivilegedAccessManagerEntitlement#approvals_needed}
        :param approver_email_recipients: Optional. Additional email addresses to be notified when a grant is pending approval. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#approver_email_recipients GooglePrivilegedAccessManagerEntitlement#approver_email_recipients}
        '''
        if isinstance(approvers, dict):
            approvers = GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers(**approvers)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__918d7816b6442751079850a49e06d9cce26de24d85c34c66b017e2ee9d2cd5c7)
            check_type(argname="argument approvers", value=approvers, expected_type=type_hints["approvers"])
            check_type(argname="argument approvals_needed", value=approvals_needed, expected_type=type_hints["approvals_needed"])
            check_type(argname="argument approver_email_recipients", value=approver_email_recipients, expected_type=type_hints["approver_email_recipients"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "approvers": approvers,
        }
        if approvals_needed is not None:
            self._values["approvals_needed"] = approvals_needed
        if approver_email_recipients is not None:
            self._values["approver_email_recipients"] = approver_email_recipients

    @builtins.property
    def approvers(
        self,
    ) -> "GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers":
        '''approvers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#approvers GooglePrivilegedAccessManagerEntitlement#approvers}
        '''
        result = self._values.get("approvers")
        assert result is not None, "Required property 'approvers' is missing"
        return typing.cast("GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers", result)

    @builtins.property
    def approvals_needed(self) -> typing.Optional[jsii.Number]:
        '''How many users from the above list need to approve.

        If there are not enough distinct users in the list above then the workflow
        will indefinitely block. Should always be greater than 0. Currently 1 is the only
        supported value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#approvals_needed GooglePrivilegedAccessManagerEntitlement#approvals_needed}
        '''
        result = self._values.get("approvals_needed")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def approver_email_recipients(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. Additional email addresses to be notified when a grant is pending approval.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#approver_email_recipients GooglePrivilegedAccessManagerEntitlement#approver_email_recipients}
        '''
        result = self._values.get("approver_email_recipients")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePrivilegedAccessManagerEntitlement.GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers",
    jsii_struct_bases=[],
    name_mapping={"principals": "principals"},
)
class GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers:
    def __init__(self, *, principals: typing.Sequence[builtins.str]) -> None:
        '''
        :param principals: Users who are being allowed for the operation. Each entry should be a valid v1 IAM Principal Identifier. Format for these is documented at: https://cloud.google.com/iam/docs/principal-identifiers#v1 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#principals GooglePrivilegedAccessManagerEntitlement#principals}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c35f2c624e3449720df9c2e8c48b881195d8b1db81cdd003320a151012abad77)
            check_type(argname="argument principals", value=principals, expected_type=type_hints["principals"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "principals": principals,
        }

    @builtins.property
    def principals(self) -> typing.List[builtins.str]:
        '''Users who are being allowed for the operation.

        Each entry should be a valid v1 IAM Principal Identifier. Format for these is documented at: https://cloud.google.com/iam/docs/principal-identifiers#v1

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#principals GooglePrivilegedAccessManagerEntitlement#principals}
        '''
        result = self._values.get("principals")
        assert result is not None, "Required property 'principals' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApproversOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivilegedAccessManagerEntitlement.GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApproversOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__800a4cf257d15365e780cb2b02db833aaee9abcf65202d16ed44c2cde3bcb370)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="principalsInput")
    def principals_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "principalsInput"))

    @builtins.property
    @jsii.member(jsii_name="principals")
    def principals(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "principals"))

    @principals.setter
    def principals(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64b63de32ab2804e442309f975fe8ffa9e5109a5896f14a52c50ef8d4b45cb79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principals", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers]:
        return typing.cast(typing.Optional[GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60b76a427606e2c0e3385efd79f0eed5690e5e18c6484dce23ea5bcdeed3a2d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivilegedAccessManagerEntitlement.GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f037dfdbe1038b5942605b9d3d77fdee5a7f0da6ba22dcabf82245a6e12037de)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e532787322aacd854c416b6b6d81088a8780a6713bbb4af48c67fec190049046)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59965b7979fb1be436b220d27c1041cd4dcd60834ce2970bf8c3abd246fdf8b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__15cdf384229c9a1ea269461efddae96448ad406a141c91de4531b2f4e6635c1a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ed5a209385f66f11ba4766f5e2139ac1d188163917fe1a8b19bf21e304335d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a4c439aef439a8c22b99a21f4178e9ee04156b2222a4ecf00fb69e5cf75ea3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivilegedAccessManagerEntitlement.GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aec0506173f83841c02b225c09181c77134f84df68c0cbc8c27fd4dca995f9c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putApprovers")
    def put_approvers(self, *, principals: typing.Sequence[builtins.str]) -> None:
        '''
        :param principals: Users who are being allowed for the operation. Each entry should be a valid v1 IAM Principal Identifier. Format for these is documented at: https://cloud.google.com/iam/docs/principal-identifiers#v1 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#principals GooglePrivilegedAccessManagerEntitlement#principals}
        '''
        value = GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers(
            principals=principals
        )

        return typing.cast(None, jsii.invoke(self, "putApprovers", [value]))

    @jsii.member(jsii_name="resetApprovalsNeeded")
    def reset_approvals_needed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApprovalsNeeded", []))

    @jsii.member(jsii_name="resetApproverEmailRecipients")
    def reset_approver_email_recipients(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApproverEmailRecipients", []))

    @builtins.property
    @jsii.member(jsii_name="approvers")
    def approvers(
        self,
    ) -> GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApproversOutputReference:
        return typing.cast(GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApproversOutputReference, jsii.get(self, "approvers"))

    @builtins.property
    @jsii.member(jsii_name="approvalsNeededInput")
    def approvals_needed_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "approvalsNeededInput"))

    @builtins.property
    @jsii.member(jsii_name="approverEmailRecipientsInput")
    def approver_email_recipients_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "approverEmailRecipientsInput"))

    @builtins.property
    @jsii.member(jsii_name="approversInput")
    def approvers_input(
        self,
    ) -> typing.Optional[GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers]:
        return typing.cast(typing.Optional[GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers], jsii.get(self, "approversInput"))

    @builtins.property
    @jsii.member(jsii_name="approvalsNeeded")
    def approvals_needed(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "approvalsNeeded"))

    @approvals_needed.setter
    def approvals_needed(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2714440277f164d2c90c8e8f32be58b0efe7103242afb1851bdfd1a176e5d02d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "approvalsNeeded", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="approverEmailRecipients")
    def approver_email_recipients(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "approverEmailRecipients"))

    @approver_email_recipients.setter
    def approver_email_recipients(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fc0d30fc88967a8d8f969a35df29c56926e4f3548c2d85b048e617089753e39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "approverEmailRecipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e1aee8c4e0c43bc09cab2ed37c0a3a0a54f96fb350a12f3cfb9fae33688cc6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GooglePrivilegedAccessManagerEntitlementApprovalWorkflowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivilegedAccessManagerEntitlement.GooglePrivilegedAccessManagerEntitlementApprovalWorkflowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ff6e9a59ea6233ac96f11a6f49bc6e674688b2c466d3c732128592359bb470d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putManualApprovals")
    def put_manual_approvals(
        self,
        *,
        steps: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps, typing.Dict[builtins.str, typing.Any]]]],
        require_approver_justification: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param steps: steps block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#steps GooglePrivilegedAccessManagerEntitlement#steps}
        :param require_approver_justification: Optional. Do the approvers need to provide a justification for their actions? Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#require_approver_justification GooglePrivilegedAccessManagerEntitlement#require_approver_justification}
        '''
        value = GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals(
            steps=steps, require_approver_justification=require_approver_justification
        )

        return typing.cast(None, jsii.invoke(self, "putManualApprovals", [value]))

    @builtins.property
    @jsii.member(jsii_name="manualApprovals")
    def manual_approvals(
        self,
    ) -> GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsOutputReference:
        return typing.cast(GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsOutputReference, jsii.get(self, "manualApprovals"))

    @builtins.property
    @jsii.member(jsii_name="manualApprovalsInput")
    def manual_approvals_input(
        self,
    ) -> typing.Optional[GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals]:
        return typing.cast(typing.Optional[GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals], jsii.get(self, "manualApprovalsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePrivilegedAccessManagerEntitlementApprovalWorkflow]:
        return typing.cast(typing.Optional[GooglePrivilegedAccessManagerEntitlementApprovalWorkflow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePrivilegedAccessManagerEntitlementApprovalWorkflow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70317e42df66d1510faf4db86f7024de2a503182c662a1f2d0b546589c073c85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePrivilegedAccessManagerEntitlement.GooglePrivilegedAccessManagerEntitlementConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "eligible_users": "eligibleUsers",
        "entitlement_id": "entitlementId",
        "location": "location",
        "max_request_duration": "maxRequestDuration",
        "parent": "parent",
        "privileged_access": "privilegedAccess",
        "requester_justification_config": "requesterJustificationConfig",
        "additional_notification_targets": "additionalNotificationTargets",
        "approval_workflow": "approvalWorkflow",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class GooglePrivilegedAccessManagerEntitlementConfig(
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
        eligible_users: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GooglePrivilegedAccessManagerEntitlementEligibleUsers", typing.Dict[builtins.str, typing.Any]]]],
        entitlement_id: builtins.str,
        location: builtins.str,
        max_request_duration: builtins.str,
        parent: builtins.str,
        privileged_access: typing.Union["GooglePrivilegedAccessManagerEntitlementPrivilegedAccess", typing.Dict[builtins.str, typing.Any]],
        requester_justification_config: typing.Union["GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfig", typing.Dict[builtins.str, typing.Any]],
        additional_notification_targets: typing.Optional[typing.Union[GooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargets, typing.Dict[builtins.str, typing.Any]]] = None,
        approval_workflow: typing.Optional[typing.Union[GooglePrivilegedAccessManagerEntitlementApprovalWorkflow, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GooglePrivilegedAccessManagerEntitlementTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param eligible_users: eligible_users block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#eligible_users GooglePrivilegedAccessManagerEntitlement#eligible_users}
        :param entitlement_id: The ID to use for this Entitlement. This will become the last part of the resource name. This value should be 4-63 characters, and valid characters are "[a-z]", "[0-9]", and "-". The first character should be from [a-z]. This value should be unique among all other Entitlements under the specified 'parent'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#entitlement_id GooglePrivilegedAccessManagerEntitlement#entitlement_id}
        :param location: The region of the Entitlement resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#location GooglePrivilegedAccessManagerEntitlement#location}
        :param max_request_duration: The maximum amount of time for which access would be granted for a request. A requester can choose to ask for access for less than this duration but never more. Format: calculate the time in seconds and concatenate it with 's' i.e. 2 hours = "7200s", 45 minutes = "2700s" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#max_request_duration GooglePrivilegedAccessManagerEntitlement#max_request_duration}
        :param parent: Format: projects/{project-id|project-number} or organizations/{organization-number} or folders/{folder-number}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#parent GooglePrivilegedAccessManagerEntitlement#parent}
        :param privileged_access: privileged_access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#privileged_access GooglePrivilegedAccessManagerEntitlement#privileged_access}
        :param requester_justification_config: requester_justification_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#requester_justification_config GooglePrivilegedAccessManagerEntitlement#requester_justification_config}
        :param additional_notification_targets: additional_notification_targets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#additional_notification_targets GooglePrivilegedAccessManagerEntitlement#additional_notification_targets}
        :param approval_workflow: approval_workflow block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#approval_workflow GooglePrivilegedAccessManagerEntitlement#approval_workflow}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#id GooglePrivilegedAccessManagerEntitlement#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#timeouts GooglePrivilegedAccessManagerEntitlement#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(privileged_access, dict):
            privileged_access = GooglePrivilegedAccessManagerEntitlementPrivilegedAccess(**privileged_access)
        if isinstance(requester_justification_config, dict):
            requester_justification_config = GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfig(**requester_justification_config)
        if isinstance(additional_notification_targets, dict):
            additional_notification_targets = GooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargets(**additional_notification_targets)
        if isinstance(approval_workflow, dict):
            approval_workflow = GooglePrivilegedAccessManagerEntitlementApprovalWorkflow(**approval_workflow)
        if isinstance(timeouts, dict):
            timeouts = GooglePrivilegedAccessManagerEntitlementTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e005de10d262f820ac88fada0701c238c209d4ae33b7d313bd8df397805ad46f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument eligible_users", value=eligible_users, expected_type=type_hints["eligible_users"])
            check_type(argname="argument entitlement_id", value=entitlement_id, expected_type=type_hints["entitlement_id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument max_request_duration", value=max_request_duration, expected_type=type_hints["max_request_duration"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument privileged_access", value=privileged_access, expected_type=type_hints["privileged_access"])
            check_type(argname="argument requester_justification_config", value=requester_justification_config, expected_type=type_hints["requester_justification_config"])
            check_type(argname="argument additional_notification_targets", value=additional_notification_targets, expected_type=type_hints["additional_notification_targets"])
            check_type(argname="argument approval_workflow", value=approval_workflow, expected_type=type_hints["approval_workflow"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "eligible_users": eligible_users,
            "entitlement_id": entitlement_id,
            "location": location,
            "max_request_duration": max_request_duration,
            "parent": parent,
            "privileged_access": privileged_access,
            "requester_justification_config": requester_justification_config,
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
        if additional_notification_targets is not None:
            self._values["additional_notification_targets"] = additional_notification_targets
        if approval_workflow is not None:
            self._values["approval_workflow"] = approval_workflow
        if id is not None:
            self._values["id"] = id
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
    def eligible_users(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GooglePrivilegedAccessManagerEntitlementEligibleUsers"]]:
        '''eligible_users block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#eligible_users GooglePrivilegedAccessManagerEntitlement#eligible_users}
        '''
        result = self._values.get("eligible_users")
        assert result is not None, "Required property 'eligible_users' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GooglePrivilegedAccessManagerEntitlementEligibleUsers"]], result)

    @builtins.property
    def entitlement_id(self) -> builtins.str:
        '''The ID to use for this Entitlement.

        This will become the last part of the resource name.
        This value should be 4-63 characters, and valid characters are "[a-z]", "[0-9]", and "-". The first character should be from [a-z].
        This value should be unique among all other Entitlements under the specified 'parent'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#entitlement_id GooglePrivilegedAccessManagerEntitlement#entitlement_id}
        '''
        result = self._values.get("entitlement_id")
        assert result is not None, "Required property 'entitlement_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The region of the Entitlement resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#location GooglePrivilegedAccessManagerEntitlement#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def max_request_duration(self) -> builtins.str:
        '''The maximum amount of time for which access would be granted for a request.

        A requester can choose to ask for access for less than this duration but never more.
        Format: calculate the time in seconds and concatenate it with 's' i.e. 2 hours = "7200s", 45 minutes = "2700s"

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#max_request_duration GooglePrivilegedAccessManagerEntitlement#max_request_duration}
        '''
        result = self._values.get("max_request_duration")
        assert result is not None, "Required property 'max_request_duration' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parent(self) -> builtins.str:
        '''Format: projects/{project-id|project-number} or organizations/{organization-number} or folders/{folder-number}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#parent GooglePrivilegedAccessManagerEntitlement#parent}
        '''
        result = self._values.get("parent")
        assert result is not None, "Required property 'parent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def privileged_access(
        self,
    ) -> "GooglePrivilegedAccessManagerEntitlementPrivilegedAccess":
        '''privileged_access block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#privileged_access GooglePrivilegedAccessManagerEntitlement#privileged_access}
        '''
        result = self._values.get("privileged_access")
        assert result is not None, "Required property 'privileged_access' is missing"
        return typing.cast("GooglePrivilegedAccessManagerEntitlementPrivilegedAccess", result)

    @builtins.property
    def requester_justification_config(
        self,
    ) -> "GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfig":
        '''requester_justification_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#requester_justification_config GooglePrivilegedAccessManagerEntitlement#requester_justification_config}
        '''
        result = self._values.get("requester_justification_config")
        assert result is not None, "Required property 'requester_justification_config' is missing"
        return typing.cast("GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfig", result)

    @builtins.property
    def additional_notification_targets(
        self,
    ) -> typing.Optional[GooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargets]:
        '''additional_notification_targets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#additional_notification_targets GooglePrivilegedAccessManagerEntitlement#additional_notification_targets}
        '''
        result = self._values.get("additional_notification_targets")
        return typing.cast(typing.Optional[GooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargets], result)

    @builtins.property
    def approval_workflow(
        self,
    ) -> typing.Optional[GooglePrivilegedAccessManagerEntitlementApprovalWorkflow]:
        '''approval_workflow block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#approval_workflow GooglePrivilegedAccessManagerEntitlement#approval_workflow}
        '''
        result = self._values.get("approval_workflow")
        return typing.cast(typing.Optional[GooglePrivilegedAccessManagerEntitlementApprovalWorkflow], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#id GooglePrivilegedAccessManagerEntitlement#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GooglePrivilegedAccessManagerEntitlementTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#timeouts GooglePrivilegedAccessManagerEntitlement#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GooglePrivilegedAccessManagerEntitlementTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePrivilegedAccessManagerEntitlementConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePrivilegedAccessManagerEntitlement.GooglePrivilegedAccessManagerEntitlementEligibleUsers",
    jsii_struct_bases=[],
    name_mapping={"principals": "principals"},
)
class GooglePrivilegedAccessManagerEntitlementEligibleUsers:
    def __init__(self, *, principals: typing.Sequence[builtins.str]) -> None:
        '''
        :param principals: Users who are being allowed for the operation. Each entry should be a valid v1 IAM Principal Identifier. Format for these is documented at "https://cloud.google.com/iam/docs/principal-identifiers#v1" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#principals GooglePrivilegedAccessManagerEntitlement#principals}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ab8ccdc13dec662f6c41d4d15d1b2733a42d567ef0598a36d0142ad511ac488)
            check_type(argname="argument principals", value=principals, expected_type=type_hints["principals"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "principals": principals,
        }

    @builtins.property
    def principals(self) -> typing.List[builtins.str]:
        '''Users who are being allowed for the operation.

        Each entry should be a valid v1 IAM Principal Identifier. Format for these is documented at "https://cloud.google.com/iam/docs/principal-identifiers#v1"

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#principals GooglePrivilegedAccessManagerEntitlement#principals}
        '''
        result = self._values.get("principals")
        assert result is not None, "Required property 'principals' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePrivilegedAccessManagerEntitlementEligibleUsers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePrivilegedAccessManagerEntitlementEligibleUsersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivilegedAccessManagerEntitlement.GooglePrivilegedAccessManagerEntitlementEligibleUsersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c82fe7de1d23fc95de5813e57710df771ef8b268034a15b2211e5a740c22f3f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GooglePrivilegedAccessManagerEntitlementEligibleUsersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9101eb575fdf8a1ff744e20a76e4b6f05f914e7f44336a33bad6ff5926c481f7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GooglePrivilegedAccessManagerEntitlementEligibleUsersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1161e6d83e029ed82a6a64d13490c231a537890455bbcaa3959a1edc2dd172a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f00786403a0ce2f62e60435c4f46c6f6b3fb7fc3c8316748556dbc0d636cca80)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a090bb6daf386f26d17af04c6a4817ec9cf63c00fae7342507b846dcd989798)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePrivilegedAccessManagerEntitlementEligibleUsers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePrivilegedAccessManagerEntitlementEligibleUsers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePrivilegedAccessManagerEntitlementEligibleUsers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdb9ddb7e23033263dad6a6240db999e6e4213f04cfa3a581b1dc5ec40a657cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GooglePrivilegedAccessManagerEntitlementEligibleUsersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivilegedAccessManagerEntitlement.GooglePrivilegedAccessManagerEntitlementEligibleUsersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0c1ec226e7203f7cad590011c379ed0b42115fb5aa2e68d98c0245f3df086de)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="principalsInput")
    def principals_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "principalsInput"))

    @builtins.property
    @jsii.member(jsii_name="principals")
    def principals(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "principals"))

    @principals.setter
    def principals(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__548ada98835b71a1304f1309add23a31ca758479c6483ff98909b1b6b97a8c8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principals", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePrivilegedAccessManagerEntitlementEligibleUsers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePrivilegedAccessManagerEntitlementEligibleUsers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePrivilegedAccessManagerEntitlementEligibleUsers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf8ec34516041e36dfe48f9426338136196bfdad1de0aa2201c11b45f6121909)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePrivilegedAccessManagerEntitlement.GooglePrivilegedAccessManagerEntitlementPrivilegedAccess",
    jsii_struct_bases=[],
    name_mapping={"gcp_iam_access": "gcpIamAccess"},
)
class GooglePrivilegedAccessManagerEntitlementPrivilegedAccess:
    def __init__(
        self,
        *,
        gcp_iam_access: typing.Union["GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param gcp_iam_access: gcp_iam_access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#gcp_iam_access GooglePrivilegedAccessManagerEntitlement#gcp_iam_access}
        '''
        if isinstance(gcp_iam_access, dict):
            gcp_iam_access = GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess(**gcp_iam_access)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6d57d5acb5ea2c4991e28456bf9a5160bb1576674047439451ca45d12e9d6bd)
            check_type(argname="argument gcp_iam_access", value=gcp_iam_access, expected_type=type_hints["gcp_iam_access"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "gcp_iam_access": gcp_iam_access,
        }

    @builtins.property
    def gcp_iam_access(
        self,
    ) -> "GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess":
        '''gcp_iam_access block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#gcp_iam_access GooglePrivilegedAccessManagerEntitlement#gcp_iam_access}
        '''
        result = self._values.get("gcp_iam_access")
        assert result is not None, "Required property 'gcp_iam_access' is missing"
        return typing.cast("GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePrivilegedAccessManagerEntitlementPrivilegedAccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePrivilegedAccessManagerEntitlement.GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess",
    jsii_struct_bases=[],
    name_mapping={
        "resource": "resource",
        "resource_type": "resourceType",
        "role_bindings": "roleBindings",
    },
)
class GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess:
    def __init__(
        self,
        *,
        resource: builtins.str,
        resource_type: builtins.str,
        role_bindings: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param resource: Name of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#resource GooglePrivilegedAccessManagerEntitlement#resource}
        :param resource_type: The type of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#resource_type GooglePrivilegedAccessManagerEntitlement#resource_type}
        :param role_bindings: role_bindings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#role_bindings GooglePrivilegedAccessManagerEntitlement#role_bindings}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__806242a8f89d5b5c1ed4c5ba5ab3c520c558903c92ee4df2abe0a178d0e2a053)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument role_bindings", value=role_bindings, expected_type=type_hints["role_bindings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource": resource,
            "resource_type": resource_type,
            "role_bindings": role_bindings,
        }

    @builtins.property
    def resource(self) -> builtins.str:
        '''Name of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#resource GooglePrivilegedAccessManagerEntitlement#resource}
        '''
        result = self._values.get("resource")
        assert result is not None, "Required property 'resource' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_type(self) -> builtins.str:
        '''The type of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#resource_type GooglePrivilegedAccessManagerEntitlement#resource_type}
        '''
        result = self._values.get("resource_type")
        assert result is not None, "Required property 'resource_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_bindings(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings"]]:
        '''role_bindings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#role_bindings GooglePrivilegedAccessManagerEntitlement#role_bindings}
        '''
        result = self._values.get("role_bindings")
        assert result is not None, "Required property 'role_bindings' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivilegedAccessManagerEntitlement.GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7104d4ee459d08f9ea710612d2848384dbf0ec4ad2b8abb763aab30228cfe401)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRoleBindings")
    def put_role_bindings(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9569edbe7b44b9758331911d5453fa0380358c53e3c4f9a734a16fd030a5b4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRoleBindings", [value]))

    @builtins.property
    @jsii.member(jsii_name="roleBindings")
    def role_bindings(
        self,
    ) -> "GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindingsList":
        return typing.cast("GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindingsList", jsii.get(self, "roleBindings"))

    @builtins.property
    @jsii.member(jsii_name="resourceInput")
    def resource_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypeInput")
    def resource_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="roleBindingsInput")
    def role_bindings_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings"]]], jsii.get(self, "roleBindingsInput"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resource"))

    @resource.setter
    def resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fcd719d547b88f175aec286d6fcfa2dca8d1db3c7e481338415223dcfcc3a12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceType"))

    @resource_type.setter
    def resource_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e64ba59b6b9901d35fe9b56d8747822cd6f14df44ef72329aa0e6c475d522133)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess]:
        return typing.cast(typing.Optional[GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d53f74fec9aa19673aefeae2cab568d332cbbdce03023b9d1046aca45a58418f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePrivilegedAccessManagerEntitlement.GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings",
    jsii_struct_bases=[],
    name_mapping={"role": "role", "condition_expression": "conditionExpression"},
)
class GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings:
    def __init__(
        self,
        *,
        role: builtins.str,
        condition_expression: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param role: IAM role to be granted. https://cloud.google.com/iam/docs/roles-overview. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#role GooglePrivilegedAccessManagerEntitlement#role}
        :param condition_expression: The expression field of the IAM condition to be associated with the role. If specified, a user with an active grant for this entitlement would be able to access the resource only if this condition evaluates to true for their request. https://cloud.google.com/iam/docs/conditions-overview#attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#condition_expression GooglePrivilegedAccessManagerEntitlement#condition_expression}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9909036c3e62cacbe0d5e2b78c7dc9bf0fed6f2f697814baf56a8a876024201f)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument condition_expression", value=condition_expression, expected_type=type_hints["condition_expression"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role": role,
        }
        if condition_expression is not None:
            self._values["condition_expression"] = condition_expression

    @builtins.property
    def role(self) -> builtins.str:
        '''IAM role to be granted. https://cloud.google.com/iam/docs/roles-overview.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#role GooglePrivilegedAccessManagerEntitlement#role}
        '''
        result = self._values.get("role")
        assert result is not None, "Required property 'role' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def condition_expression(self) -> typing.Optional[builtins.str]:
        '''The expression field of the IAM condition to be associated with the role.

        If specified, a user with an active grant for this entitlement would be able to access the resource only if this condition evaluates to true for their request.
        https://cloud.google.com/iam/docs/conditions-overview#attributes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#condition_expression GooglePrivilegedAccessManagerEntitlement#condition_expression}
        '''
        result = self._values.get("condition_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindingsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivilegedAccessManagerEntitlement.GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindingsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c28f739223ac9822ce0faa38595ae6a6ca814c27cd213b868f75b53e2e134bcc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindingsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f9b26fcabaa28782eb3a4f4d6fe4d95e31f1c8f363ec4853c7f0919c225e9ad)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindingsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e710024e166708d6cb3ed93d7210cabde343cadef4e80c7f5225d89048d9abde)
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
            type_hints = typing.get_type_hints(_typecheckingstub__94abc68ce514871cc37725258f41d13b6fec8b271bff31fb38b03acb8c234dd2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bb07cd440a4e61f1e364a2502d2f24ecc8752625015d91141912ff967efc7ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a92606930dd8bcade2f8486a05b557e18af3593013158c1c322acb29d4022a02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivilegedAccessManagerEntitlement.GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__791c7b5489eabd3e2fdb879456f36b195be217bf17b5880d5f950fd3ae4b4005)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetConditionExpression")
    def reset_condition_expression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConditionExpression", []))

    @builtins.property
    @jsii.member(jsii_name="conditionExpressionInput")
    def condition_expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conditionExpressionInput"))

    @builtins.property
    @jsii.member(jsii_name="roleInput")
    def role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionExpression")
    def condition_expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "conditionExpression"))

    @condition_expression.setter
    def condition_expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7abb3e252bb1ddb4583f7617730e4e500077c0ac887da1fc5038ea0a3768e767)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "conditionExpression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @role.setter
    def role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9a54eb287f5622651439db042269598cf808d9d728f4cb401f1170c8d9cdda8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "role", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__675c6dffd1c256e7bfcd51d513c88f870e515673ade2f24b745a035b2e2ddd72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GooglePrivilegedAccessManagerEntitlementPrivilegedAccessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivilegedAccessManagerEntitlement.GooglePrivilegedAccessManagerEntitlementPrivilegedAccessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38fcb280ba87a001096bbac80cea94132120038ae130b750661c8de7c00f98f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGcpIamAccess")
    def put_gcp_iam_access(
        self,
        *,
        resource: builtins.str,
        resource_type: builtins.str,
        role_bindings: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param resource: Name of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#resource GooglePrivilegedAccessManagerEntitlement#resource}
        :param resource_type: The type of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#resource_type GooglePrivilegedAccessManagerEntitlement#resource_type}
        :param role_bindings: role_bindings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#role_bindings GooglePrivilegedAccessManagerEntitlement#role_bindings}
        '''
        value = GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess(
            resource=resource, resource_type=resource_type, role_bindings=role_bindings
        )

        return typing.cast(None, jsii.invoke(self, "putGcpIamAccess", [value]))

    @builtins.property
    @jsii.member(jsii_name="gcpIamAccess")
    def gcp_iam_access(
        self,
    ) -> GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessOutputReference:
        return typing.cast(GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessOutputReference, jsii.get(self, "gcpIamAccess"))

    @builtins.property
    @jsii.member(jsii_name="gcpIamAccessInput")
    def gcp_iam_access_input(
        self,
    ) -> typing.Optional[GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess]:
        return typing.cast(typing.Optional[GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess], jsii.get(self, "gcpIamAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePrivilegedAccessManagerEntitlementPrivilegedAccess]:
        return typing.cast(typing.Optional[GooglePrivilegedAccessManagerEntitlementPrivilegedAccess], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePrivilegedAccessManagerEntitlementPrivilegedAccess],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8151abe5c046d26c0a4b110a161706641461e009671955071900704a0d66fc3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePrivilegedAccessManagerEntitlement.GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfig",
    jsii_struct_bases=[],
    name_mapping={"not_mandatory": "notMandatory", "unstructured": "unstructured"},
)
class GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfig:
    def __init__(
        self,
        *,
        not_mandatory: typing.Optional[typing.Union["GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory", typing.Dict[builtins.str, typing.Any]]] = None,
        unstructured: typing.Optional[typing.Union["GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param not_mandatory: not_mandatory block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#not_mandatory GooglePrivilegedAccessManagerEntitlement#not_mandatory}
        :param unstructured: unstructured block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#unstructured GooglePrivilegedAccessManagerEntitlement#unstructured}
        '''
        if isinstance(not_mandatory, dict):
            not_mandatory = GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory(**not_mandatory)
        if isinstance(unstructured, dict):
            unstructured = GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured(**unstructured)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aa660ca7ec779a77bd5699cd6e5944898fb743fc76dfa61798d4851aea29c3c)
            check_type(argname="argument not_mandatory", value=not_mandatory, expected_type=type_hints["not_mandatory"])
            check_type(argname="argument unstructured", value=unstructured, expected_type=type_hints["unstructured"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if not_mandatory is not None:
            self._values["not_mandatory"] = not_mandatory
        if unstructured is not None:
            self._values["unstructured"] = unstructured

    @builtins.property
    def not_mandatory(
        self,
    ) -> typing.Optional["GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory"]:
        '''not_mandatory block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#not_mandatory GooglePrivilegedAccessManagerEntitlement#not_mandatory}
        '''
        result = self._values.get("not_mandatory")
        return typing.cast(typing.Optional["GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory"], result)

    @builtins.property
    def unstructured(
        self,
    ) -> typing.Optional["GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured"]:
        '''unstructured block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#unstructured GooglePrivilegedAccessManagerEntitlement#unstructured}
        '''
        result = self._values.get("unstructured")
        return typing.cast(typing.Optional["GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePrivilegedAccessManagerEntitlement.GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory",
    jsii_struct_bases=[],
    name_mapping={},
)
class GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivilegedAccessManagerEntitlement.GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f855ba681e8ab80558a6fd6c5f8c9967d628fe4d15e130e2928886ea8170a49c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory]:
        return typing.cast(typing.Optional[GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02575fc366c006f73e2e7338923ea7be089813a6f65512e491f6723d5e8bf9b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivilegedAccessManagerEntitlement.GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__383c3b707ad3ada7e620523148cf1e265c3747138c1b100987aa9947c3bdaa17)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNotMandatory")
    def put_not_mandatory(self) -> None:
        value = GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory()

        return typing.cast(None, jsii.invoke(self, "putNotMandatory", [value]))

    @jsii.member(jsii_name="putUnstructured")
    def put_unstructured(self) -> None:
        value = GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured()

        return typing.cast(None, jsii.invoke(self, "putUnstructured", [value]))

    @jsii.member(jsii_name="resetNotMandatory")
    def reset_not_mandatory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotMandatory", []))

    @jsii.member(jsii_name="resetUnstructured")
    def reset_unstructured(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnstructured", []))

    @builtins.property
    @jsii.member(jsii_name="notMandatory")
    def not_mandatory(
        self,
    ) -> GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatoryOutputReference:
        return typing.cast(GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatoryOutputReference, jsii.get(self, "notMandatory"))

    @builtins.property
    @jsii.member(jsii_name="unstructured")
    def unstructured(
        self,
    ) -> "GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructuredOutputReference":
        return typing.cast("GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructuredOutputReference", jsii.get(self, "unstructured"))

    @builtins.property
    @jsii.member(jsii_name="notMandatoryInput")
    def not_mandatory_input(
        self,
    ) -> typing.Optional[GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory]:
        return typing.cast(typing.Optional[GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory], jsii.get(self, "notMandatoryInput"))

    @builtins.property
    @jsii.member(jsii_name="unstructuredInput")
    def unstructured_input(
        self,
    ) -> typing.Optional["GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured"]:
        return typing.cast(typing.Optional["GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured"], jsii.get(self, "unstructuredInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfig]:
        return typing.cast(typing.Optional[GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9de6b2fa009120947fb9e5df06bdf716131f635db982a32c9bd6f128218fc82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePrivilegedAccessManagerEntitlement.GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured",
    jsii_struct_bases=[],
    name_mapping={},
)
class GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructuredOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivilegedAccessManagerEntitlement.GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructuredOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c5dbbe165440fb2f5e04566f16e3db7ca7d4be6feb11753f3e86bc6f968afbf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured]:
        return typing.cast(typing.Optional[GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1068c301d775a21adb732d3083f4ad94f9ba800049bdf9e78441766b0037f9b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePrivilegedAccessManagerEntitlement.GooglePrivilegedAccessManagerEntitlementTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GooglePrivilegedAccessManagerEntitlementTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#create GooglePrivilegedAccessManagerEntitlement#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#delete GooglePrivilegedAccessManagerEntitlement#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#update GooglePrivilegedAccessManagerEntitlement#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d99fa31bcf83bfb3167811efa3c9ac3f049ac2e062cfe6fbf08686f68e0ec9a2)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#create GooglePrivilegedAccessManagerEntitlement#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#delete GooglePrivilegedAccessManagerEntitlement#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privileged_access_manager_entitlement#update GooglePrivilegedAccessManagerEntitlement#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePrivilegedAccessManagerEntitlementTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePrivilegedAccessManagerEntitlementTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivilegedAccessManagerEntitlement.GooglePrivilegedAccessManagerEntitlementTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5adae64215eabeb4cc4ec23ed0eb221780a4512042497487e2a23b9a89de8bcf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fab5d2f14f3cef4791b9ed673a17e6d7778daa6f1dd51eb17a75289a68389f04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e45ecaa2e2f36cb684a83cb1a48b468eefcab5b24ed7195a83ef30a02301c12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__770a301206cd8e00ac16d482f4e66061e071de7254c0c694e26c59feff961586)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePrivilegedAccessManagerEntitlementTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePrivilegedAccessManagerEntitlementTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePrivilegedAccessManagerEntitlementTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e8be4239b49fb833cf259eb9e3f804caefdc1e29cca65080f966b22a84ffcfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GooglePrivilegedAccessManagerEntitlement",
    "GooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargets",
    "GooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargetsOutputReference",
    "GooglePrivilegedAccessManagerEntitlementApprovalWorkflow",
    "GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals",
    "GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsOutputReference",
    "GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps",
    "GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers",
    "GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApproversOutputReference",
    "GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsList",
    "GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsOutputReference",
    "GooglePrivilegedAccessManagerEntitlementApprovalWorkflowOutputReference",
    "GooglePrivilegedAccessManagerEntitlementConfig",
    "GooglePrivilegedAccessManagerEntitlementEligibleUsers",
    "GooglePrivilegedAccessManagerEntitlementEligibleUsersList",
    "GooglePrivilegedAccessManagerEntitlementEligibleUsersOutputReference",
    "GooglePrivilegedAccessManagerEntitlementPrivilegedAccess",
    "GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess",
    "GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessOutputReference",
    "GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings",
    "GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindingsList",
    "GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindingsOutputReference",
    "GooglePrivilegedAccessManagerEntitlementPrivilegedAccessOutputReference",
    "GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfig",
    "GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory",
    "GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatoryOutputReference",
    "GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigOutputReference",
    "GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured",
    "GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructuredOutputReference",
    "GooglePrivilegedAccessManagerEntitlementTimeouts",
    "GooglePrivilegedAccessManagerEntitlementTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__3e318f0152ba381b30b9900a7d0afde9c459dbb22740ba9246081a051480f8d3(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    eligible_users: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GooglePrivilegedAccessManagerEntitlementEligibleUsers, typing.Dict[builtins.str, typing.Any]]]],
    entitlement_id: builtins.str,
    location: builtins.str,
    max_request_duration: builtins.str,
    parent: builtins.str,
    privileged_access: typing.Union[GooglePrivilegedAccessManagerEntitlementPrivilegedAccess, typing.Dict[builtins.str, typing.Any]],
    requester_justification_config: typing.Union[GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfig, typing.Dict[builtins.str, typing.Any]],
    additional_notification_targets: typing.Optional[typing.Union[GooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargets, typing.Dict[builtins.str, typing.Any]]] = None,
    approval_workflow: typing.Optional[typing.Union[GooglePrivilegedAccessManagerEntitlementApprovalWorkflow, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GooglePrivilegedAccessManagerEntitlementTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__98ae0d583fa5e45ae3f2fecc0c79e1d90ca6ed1d13151b092d6e55ac87660ae2(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__776571c0d4f9ef341ce9497601511b08e8b90a98fc4d4f396283f84c64ebe8cb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GooglePrivilegedAccessManagerEntitlementEligibleUsers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69d299f26c0ea7401c016bec8fc3333bd4a0baf7593c8035fd2b848ed2627aa8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e0a1effc5ab70e928de713894ed9b663e3a3434712432e9352b0bc2fbe5c5a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15d8b441878297141c9a08f54190ff9d61e6ab6a4a0655e7b128e28c58f76c04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d43eecd83ebd58b2525e2c67e8f102de68114748e15661981f1fd16f953f5ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e86aacf4347b30610d6a8204e5e4ba3481bf96ea32415d43323b5d3bc5c86344(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf57fa7e4d441163b94daea7783866d9eef4704626816c2f641bc88c4f7c4b38(
    *,
    admin_email_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    requester_email_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4452b6e0547c4fc83c9caaf5696cfe318b9b5960001a0cf16cdfc5e8a7e5e7b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4260b7a3f278f12158285f4855b87f8d1765e7dbf0b99f706ca9e457ce2645b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14e44c9054f8778f4d6e7e1c26214bf3f721b4c043f630473e9c31a44f09cc95(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ba0edb4da219fa732ab46c424828dc3b2512f6be557017c42ffdfe93325d4fe(
    value: typing.Optional[GooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4db3a123da1b4a3010fe5b85ab0b07576f839cf3ff6fbb6d7d5902293491a0e1(
    *,
    manual_approvals: typing.Union[GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b370c1e2cf0a596bc369775013c7898710e9d1625f2382c4891495f12629f4ef(
    *,
    steps: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps, typing.Dict[builtins.str, typing.Any]]]],
    require_approver_justification: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f450b3a8f64143b18e4feec62ed0145f836cf81d8c424974befcc3e730583ee7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46747e89344484df98f598a3c8bb13d224a30931643bd8efe31c0d57ee684f51(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__374e7adf3fdd77798561c665a3af9f0903226ad7e9453354ab357cdcc39b646c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2d2a79f0e54ab7f3d104c09f1cde825d870d306af16e38447032e550fa12629(
    value: typing.Optional[GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__918d7816b6442751079850a49e06d9cce26de24d85c34c66b017e2ee9d2cd5c7(
    *,
    approvers: typing.Union[GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers, typing.Dict[builtins.str, typing.Any]],
    approvals_needed: typing.Optional[jsii.Number] = None,
    approver_email_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c35f2c624e3449720df9c2e8c48b881195d8b1db81cdd003320a151012abad77(
    *,
    principals: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__800a4cf257d15365e780cb2b02db833aaee9abcf65202d16ed44c2cde3bcb370(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64b63de32ab2804e442309f975fe8ffa9e5109a5896f14a52c50ef8d4b45cb79(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60b76a427606e2c0e3385efd79f0eed5690e5e18c6484dce23ea5bcdeed3a2d5(
    value: typing.Optional[GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f037dfdbe1038b5942605b9d3d77fdee5a7f0da6ba22dcabf82245a6e12037de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e532787322aacd854c416b6b6d81088a8780a6713bbb4af48c67fec190049046(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59965b7979fb1be436b220d27c1041cd4dcd60834ce2970bf8c3abd246fdf8b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15cdf384229c9a1ea269461efddae96448ad406a141c91de4531b2f4e6635c1a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ed5a209385f66f11ba4766f5e2139ac1d188163917fe1a8b19bf21e304335d0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a4c439aef439a8c22b99a21f4178e9ee04156b2222a4ecf00fb69e5cf75ea3f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aec0506173f83841c02b225c09181c77134f84df68c0cbc8c27fd4dca995f9c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2714440277f164d2c90c8e8f32be58b0efe7103242afb1851bdfd1a176e5d02d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fc0d30fc88967a8d8f969a35df29c56926e4f3548c2d85b048e617089753e39(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e1aee8c4e0c43bc09cab2ed37c0a3a0a54f96fb350a12f3cfb9fae33688cc6a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ff6e9a59ea6233ac96f11a6f49bc6e674688b2c466d3c732128592359bb470d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70317e42df66d1510faf4db86f7024de2a503182c662a1f2d0b546589c073c85(
    value: typing.Optional[GooglePrivilegedAccessManagerEntitlementApprovalWorkflow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e005de10d262f820ac88fada0701c238c209d4ae33b7d313bd8df397805ad46f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    eligible_users: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GooglePrivilegedAccessManagerEntitlementEligibleUsers, typing.Dict[builtins.str, typing.Any]]]],
    entitlement_id: builtins.str,
    location: builtins.str,
    max_request_duration: builtins.str,
    parent: builtins.str,
    privileged_access: typing.Union[GooglePrivilegedAccessManagerEntitlementPrivilegedAccess, typing.Dict[builtins.str, typing.Any]],
    requester_justification_config: typing.Union[GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfig, typing.Dict[builtins.str, typing.Any]],
    additional_notification_targets: typing.Optional[typing.Union[GooglePrivilegedAccessManagerEntitlementAdditionalNotificationTargets, typing.Dict[builtins.str, typing.Any]]] = None,
    approval_workflow: typing.Optional[typing.Union[GooglePrivilegedAccessManagerEntitlementApprovalWorkflow, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GooglePrivilegedAccessManagerEntitlementTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ab8ccdc13dec662f6c41d4d15d1b2733a42d567ef0598a36d0142ad511ac488(
    *,
    principals: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c82fe7de1d23fc95de5813e57710df771ef8b268034a15b2211e5a740c22f3f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9101eb575fdf8a1ff744e20a76e4b6f05f914e7f44336a33bad6ff5926c481f7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1161e6d83e029ed82a6a64d13490c231a537890455bbcaa3959a1edc2dd172a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f00786403a0ce2f62e60435c4f46c6f6b3fb7fc3c8316748556dbc0d636cca80(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a090bb6daf386f26d17af04c6a4817ec9cf63c00fae7342507b846dcd989798(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdb9ddb7e23033263dad6a6240db999e6e4213f04cfa3a581b1dc5ec40a657cf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePrivilegedAccessManagerEntitlementEligibleUsers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c1ec226e7203f7cad590011c379ed0b42115fb5aa2e68d98c0245f3df086de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__548ada98835b71a1304f1309add23a31ca758479c6483ff98909b1b6b97a8c8e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf8ec34516041e36dfe48f9426338136196bfdad1de0aa2201c11b45f6121909(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePrivilegedAccessManagerEntitlementEligibleUsers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6d57d5acb5ea2c4991e28456bf9a5160bb1576674047439451ca45d12e9d6bd(
    *,
    gcp_iam_access: typing.Union[GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__806242a8f89d5b5c1ed4c5ba5ab3c520c558903c92ee4df2abe0a178d0e2a053(
    *,
    resource: builtins.str,
    resource_type: builtins.str,
    role_bindings: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7104d4ee459d08f9ea710612d2848384dbf0ec4ad2b8abb763aab30228cfe401(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9569edbe7b44b9758331911d5453fa0380358c53e3c4f9a734a16fd030a5b4f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fcd719d547b88f175aec286d6fcfa2dca8d1db3c7e481338415223dcfcc3a12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e64ba59b6b9901d35fe9b56d8747822cd6f14df44ef72329aa0e6c475d522133(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d53f74fec9aa19673aefeae2cab568d332cbbdce03023b9d1046aca45a58418f(
    value: typing.Optional[GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9909036c3e62cacbe0d5e2b78c7dc9bf0fed6f2f697814baf56a8a876024201f(
    *,
    role: builtins.str,
    condition_expression: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c28f739223ac9822ce0faa38595ae6a6ca814c27cd213b868f75b53e2e134bcc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f9b26fcabaa28782eb3a4f4d6fe4d95e31f1c8f363ec4853c7f0919c225e9ad(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e710024e166708d6cb3ed93d7210cabde343cadef4e80c7f5225d89048d9abde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94abc68ce514871cc37725258f41d13b6fec8b271bff31fb38b03acb8c234dd2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bb07cd440a4e61f1e364a2502d2f24ecc8752625015d91141912ff967efc7ec(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a92606930dd8bcade2f8486a05b557e18af3593013158c1c322acb29d4022a02(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__791c7b5489eabd3e2fdb879456f36b195be217bf17b5880d5f950fd3ae4b4005(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7abb3e252bb1ddb4583f7617730e4e500077c0ac887da1fc5038ea0a3768e767(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9a54eb287f5622651439db042269598cf808d9d728f4cb401f1170c8d9cdda8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__675c6dffd1c256e7bfcd51d513c88f870e515673ade2f24b745a035b2e2ddd72(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38fcb280ba87a001096bbac80cea94132120038ae130b750661c8de7c00f98f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8151abe5c046d26c0a4b110a161706641461e009671955071900704a0d66fc3c(
    value: typing.Optional[GooglePrivilegedAccessManagerEntitlementPrivilegedAccess],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aa660ca7ec779a77bd5699cd6e5944898fb743fc76dfa61798d4851aea29c3c(
    *,
    not_mandatory: typing.Optional[typing.Union[GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory, typing.Dict[builtins.str, typing.Any]]] = None,
    unstructured: typing.Optional[typing.Union[GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f855ba681e8ab80558a6fd6c5f8c9967d628fe4d15e130e2928886ea8170a49c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02575fc366c006f73e2e7338923ea7be089813a6f65512e491f6723d5e8bf9b7(
    value: typing.Optional[GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__383c3b707ad3ada7e620523148cf1e265c3747138c1b100987aa9947c3bdaa17(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9de6b2fa009120947fb9e5df06bdf716131f635db982a32c9bd6f128218fc82(
    value: typing.Optional[GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c5dbbe165440fb2f5e04566f16e3db7ca7d4be6feb11753f3e86bc6f968afbf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1068c301d775a21adb732d3083f4ad94f9ba800049bdf9e78441766b0037f9b2(
    value: typing.Optional[GooglePrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d99fa31bcf83bfb3167811efa3c9ac3f049ac2e062cfe6fbf08686f68e0ec9a2(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5adae64215eabeb4cc4ec23ed0eb221780a4512042497487e2a23b9a89de8bcf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fab5d2f14f3cef4791b9ed673a17e6d7778daa6f1dd51eb17a75289a68389f04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e45ecaa2e2f36cb684a83cb1a48b468eefcab5b24ed7195a83ef30a02301c12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__770a301206cd8e00ac16d482f4e66061e071de7254c0c694e26c59feff961586(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e8be4239b49fb833cf259eb9e3f804caefdc1e29cca65080f966b22a84ffcfe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePrivilegedAccessManagerEntitlementTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
