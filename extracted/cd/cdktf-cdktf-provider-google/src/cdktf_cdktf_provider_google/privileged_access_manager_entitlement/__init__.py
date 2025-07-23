r'''
# `google_privileged_access_manager_entitlement`

Refer to the Terraform Registry for docs: [`google_privileged_access_manager_entitlement`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement).
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


class PrivilegedAccessManagerEntitlement(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privilegedAccessManagerEntitlement.PrivilegedAccessManagerEntitlement",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement google_privileged_access_manager_entitlement}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        eligible_users: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivilegedAccessManagerEntitlementEligibleUsers", typing.Dict[builtins.str, typing.Any]]]],
        entitlement_id: builtins.str,
        location: builtins.str,
        max_request_duration: builtins.str,
        parent: builtins.str,
        privileged_access: typing.Union["PrivilegedAccessManagerEntitlementPrivilegedAccess", typing.Dict[builtins.str, typing.Any]],
        requester_justification_config: typing.Union["PrivilegedAccessManagerEntitlementRequesterJustificationConfig", typing.Dict[builtins.str, typing.Any]],
        additional_notification_targets: typing.Optional[typing.Union["PrivilegedAccessManagerEntitlementAdditionalNotificationTargets", typing.Dict[builtins.str, typing.Any]]] = None,
        approval_workflow: typing.Optional[typing.Union["PrivilegedAccessManagerEntitlementApprovalWorkflow", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["PrivilegedAccessManagerEntitlementTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement google_privileged_access_manager_entitlement} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param eligible_users: eligible_users block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#eligible_users PrivilegedAccessManagerEntitlement#eligible_users}
        :param entitlement_id: The ID to use for this Entitlement. This will become the last part of the resource name. This value should be 4-63 characters, and valid characters are "[a-z]", "[0-9]", and "-". The first character should be from [a-z]. This value should be unique among all other Entitlements under the specified 'parent'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#entitlement_id PrivilegedAccessManagerEntitlement#entitlement_id}
        :param location: The region of the Entitlement resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#location PrivilegedAccessManagerEntitlement#location}
        :param max_request_duration: The maximum amount of time for which access would be granted for a request. A requester can choose to ask for access for less than this duration but never more. Format: calculate the time in seconds and concatenate it with 's' i.e. 2 hours = "7200s", 45 minutes = "2700s" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#max_request_duration PrivilegedAccessManagerEntitlement#max_request_duration}
        :param parent: Format: projects/{project-id|project-number} or organizations/{organization-number} or folders/{folder-number}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#parent PrivilegedAccessManagerEntitlement#parent}
        :param privileged_access: privileged_access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#privileged_access PrivilegedAccessManagerEntitlement#privileged_access}
        :param requester_justification_config: requester_justification_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#requester_justification_config PrivilegedAccessManagerEntitlement#requester_justification_config}
        :param additional_notification_targets: additional_notification_targets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#additional_notification_targets PrivilegedAccessManagerEntitlement#additional_notification_targets}
        :param approval_workflow: approval_workflow block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#approval_workflow PrivilegedAccessManagerEntitlement#approval_workflow}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#id PrivilegedAccessManagerEntitlement#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#timeouts PrivilegedAccessManagerEntitlement#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6241e5bd7533db9d1ceea698bd90ba52bacef0d4da57a9b4084f683a6ef0c621)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = PrivilegedAccessManagerEntitlementConfig(
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
        '''Generates CDKTF code for importing a PrivilegedAccessManagerEntitlement resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the PrivilegedAccessManagerEntitlement to import.
        :param import_from_id: The id of the existing PrivilegedAccessManagerEntitlement that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the PrivilegedAccessManagerEntitlement to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__594c016c75b39a41453af7d75aca55a0871040ea377b9674526cf8ddcabfbee5)
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
        :param admin_email_recipients: Optional. Additional email addresses to be notified when a principal(requester) is granted access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#admin_email_recipients PrivilegedAccessManagerEntitlement#admin_email_recipients}
        :param requester_email_recipients: Optional. Additional email address to be notified about an eligible entitlement. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#requester_email_recipients PrivilegedAccessManagerEntitlement#requester_email_recipients}
        '''
        value = PrivilegedAccessManagerEntitlementAdditionalNotificationTargets(
            admin_email_recipients=admin_email_recipients,
            requester_email_recipients=requester_email_recipients,
        )

        return typing.cast(None, jsii.invoke(self, "putAdditionalNotificationTargets", [value]))

    @jsii.member(jsii_name="putApprovalWorkflow")
    def put_approval_workflow(
        self,
        *,
        manual_approvals: typing.Union["PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param manual_approvals: manual_approvals block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#manual_approvals PrivilegedAccessManagerEntitlement#manual_approvals}
        '''
        value = PrivilegedAccessManagerEntitlementApprovalWorkflow(
            manual_approvals=manual_approvals
        )

        return typing.cast(None, jsii.invoke(self, "putApprovalWorkflow", [value]))

    @jsii.member(jsii_name="putEligibleUsers")
    def put_eligible_users(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivilegedAccessManagerEntitlementEligibleUsers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__649b9b6393ae2e4385a84ed5abd91b5a6a6a141903515cce2f6421dc21672afc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEligibleUsers", [value]))

    @jsii.member(jsii_name="putPrivilegedAccess")
    def put_privileged_access(
        self,
        *,
        gcp_iam_access: typing.Union["PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param gcp_iam_access: gcp_iam_access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#gcp_iam_access PrivilegedAccessManagerEntitlement#gcp_iam_access}
        '''
        value = PrivilegedAccessManagerEntitlementPrivilegedAccess(
            gcp_iam_access=gcp_iam_access
        )

        return typing.cast(None, jsii.invoke(self, "putPrivilegedAccess", [value]))

    @jsii.member(jsii_name="putRequesterJustificationConfig")
    def put_requester_justification_config(
        self,
        *,
        not_mandatory: typing.Optional[typing.Union["PrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory", typing.Dict[builtins.str, typing.Any]]] = None,
        unstructured: typing.Optional[typing.Union["PrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param not_mandatory: not_mandatory block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#not_mandatory PrivilegedAccessManagerEntitlement#not_mandatory}
        :param unstructured: unstructured block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#unstructured PrivilegedAccessManagerEntitlement#unstructured}
        '''
        value = PrivilegedAccessManagerEntitlementRequesterJustificationConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#create PrivilegedAccessManagerEntitlement#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#delete PrivilegedAccessManagerEntitlement#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#update PrivilegedAccessManagerEntitlement#update}.
        '''
        value = PrivilegedAccessManagerEntitlementTimeouts(
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
    ) -> "PrivilegedAccessManagerEntitlementAdditionalNotificationTargetsOutputReference":
        return typing.cast("PrivilegedAccessManagerEntitlementAdditionalNotificationTargetsOutputReference", jsii.get(self, "additionalNotificationTargets"))

    @builtins.property
    @jsii.member(jsii_name="approvalWorkflow")
    def approval_workflow(
        self,
    ) -> "PrivilegedAccessManagerEntitlementApprovalWorkflowOutputReference":
        return typing.cast("PrivilegedAccessManagerEntitlementApprovalWorkflowOutputReference", jsii.get(self, "approvalWorkflow"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="eligibleUsers")
    def eligible_users(self) -> "PrivilegedAccessManagerEntitlementEligibleUsersList":
        return typing.cast("PrivilegedAccessManagerEntitlementEligibleUsersList", jsii.get(self, "eligibleUsers"))

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
    ) -> "PrivilegedAccessManagerEntitlementPrivilegedAccessOutputReference":
        return typing.cast("PrivilegedAccessManagerEntitlementPrivilegedAccessOutputReference", jsii.get(self, "privilegedAccess"))

    @builtins.property
    @jsii.member(jsii_name="requesterJustificationConfig")
    def requester_justification_config(
        self,
    ) -> "PrivilegedAccessManagerEntitlementRequesterJustificationConfigOutputReference":
        return typing.cast("PrivilegedAccessManagerEntitlementRequesterJustificationConfigOutputReference", jsii.get(self, "requesterJustificationConfig"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "PrivilegedAccessManagerEntitlementTimeoutsOutputReference":
        return typing.cast("PrivilegedAccessManagerEntitlementTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="additionalNotificationTargetsInput")
    def additional_notification_targets_input(
        self,
    ) -> typing.Optional["PrivilegedAccessManagerEntitlementAdditionalNotificationTargets"]:
        return typing.cast(typing.Optional["PrivilegedAccessManagerEntitlementAdditionalNotificationTargets"], jsii.get(self, "additionalNotificationTargetsInput"))

    @builtins.property
    @jsii.member(jsii_name="approvalWorkflowInput")
    def approval_workflow_input(
        self,
    ) -> typing.Optional["PrivilegedAccessManagerEntitlementApprovalWorkflow"]:
        return typing.cast(typing.Optional["PrivilegedAccessManagerEntitlementApprovalWorkflow"], jsii.get(self, "approvalWorkflowInput"))

    @builtins.property
    @jsii.member(jsii_name="eligibleUsersInput")
    def eligible_users_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivilegedAccessManagerEntitlementEligibleUsers"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivilegedAccessManagerEntitlementEligibleUsers"]]], jsii.get(self, "eligibleUsersInput"))

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
    ) -> typing.Optional["PrivilegedAccessManagerEntitlementPrivilegedAccess"]:
        return typing.cast(typing.Optional["PrivilegedAccessManagerEntitlementPrivilegedAccess"], jsii.get(self, "privilegedAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="requesterJustificationConfigInput")
    def requester_justification_config_input(
        self,
    ) -> typing.Optional["PrivilegedAccessManagerEntitlementRequesterJustificationConfig"]:
        return typing.cast(typing.Optional["PrivilegedAccessManagerEntitlementRequesterJustificationConfig"], jsii.get(self, "requesterJustificationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PrivilegedAccessManagerEntitlementTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PrivilegedAccessManagerEntitlementTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="entitlementId")
    def entitlement_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entitlementId"))

    @entitlement_id.setter
    def entitlement_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__018b6bcf75b78ead94537d76b088ad63d4489ad1f1e233dec2ba72aad61967a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entitlementId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a243a8ebe3c2044ed3f44233efce9d2cf89c5e3969a5f2fc43aadbe263d4865)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b135b30ff543a82fa053bffc9ea773e7e14bd0719330b56c0c0ecbfd5254f260)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRequestDuration")
    def max_request_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxRequestDuration"))

    @max_request_duration.setter
    def max_request_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8171cd1baf3f2c696218117438b60025ac679244ced9c25a8fe3573a55fc5cb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRequestDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff3c6c492f364cc91ed8f1d40cbb39b91dc92dff4118a1b9b9bb065a868e8bd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privilegedAccessManagerEntitlement.PrivilegedAccessManagerEntitlementAdditionalNotificationTargets",
    jsii_struct_bases=[],
    name_mapping={
        "admin_email_recipients": "adminEmailRecipients",
        "requester_email_recipients": "requesterEmailRecipients",
    },
)
class PrivilegedAccessManagerEntitlementAdditionalNotificationTargets:
    def __init__(
        self,
        *,
        admin_email_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
        requester_email_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param admin_email_recipients: Optional. Additional email addresses to be notified when a principal(requester) is granted access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#admin_email_recipients PrivilegedAccessManagerEntitlement#admin_email_recipients}
        :param requester_email_recipients: Optional. Additional email address to be notified about an eligible entitlement. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#requester_email_recipients PrivilegedAccessManagerEntitlement#requester_email_recipients}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17540d90177c5de99cbd0a8672ce255c9986b90c90979e1611426e26a128200a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#admin_email_recipients PrivilegedAccessManagerEntitlement#admin_email_recipients}
        '''
        result = self._values.get("admin_email_recipients")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def requester_email_recipients(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. Additional email address to be notified about an eligible entitlement.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#requester_email_recipients PrivilegedAccessManagerEntitlement#requester_email_recipients}
        '''
        result = self._values.get("requester_email_recipients")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivilegedAccessManagerEntitlementAdditionalNotificationTargets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivilegedAccessManagerEntitlementAdditionalNotificationTargetsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privilegedAccessManagerEntitlement.PrivilegedAccessManagerEntitlementAdditionalNotificationTargetsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccebc1aa4d72987d8c330e5692b752d7c9e33078103b4025f88fca2cea84b7d9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__889545faebb2c338e94394e3929141ce605f285d1560812e5f1acde129ba7931)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminEmailRecipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requesterEmailRecipients")
    def requester_email_recipients(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "requesterEmailRecipients"))

    @requester_email_recipients.setter
    def requester_email_recipients(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3702ae145c2e2876095bdce0020d0e4c1f4df3e155112dabcbe4c461fb9185d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requesterEmailRecipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivilegedAccessManagerEntitlementAdditionalNotificationTargets]:
        return typing.cast(typing.Optional[PrivilegedAccessManagerEntitlementAdditionalNotificationTargets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivilegedAccessManagerEntitlementAdditionalNotificationTargets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ddd3156ec437d2e1f8ebd18cf5c8b1637a4298de58d333b51ae73b312cf4a28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privilegedAccessManagerEntitlement.PrivilegedAccessManagerEntitlementApprovalWorkflow",
    jsii_struct_bases=[],
    name_mapping={"manual_approvals": "manualApprovals"},
)
class PrivilegedAccessManagerEntitlementApprovalWorkflow:
    def __init__(
        self,
        *,
        manual_approvals: typing.Union["PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param manual_approvals: manual_approvals block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#manual_approvals PrivilegedAccessManagerEntitlement#manual_approvals}
        '''
        if isinstance(manual_approvals, dict):
            manual_approvals = PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals(**manual_approvals)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae977dbc1c02e5f7adbeedec229f83bb3ccf4c5b7b4ddf62016c79fba21ff604)
            check_type(argname="argument manual_approvals", value=manual_approvals, expected_type=type_hints["manual_approvals"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "manual_approvals": manual_approvals,
        }

    @builtins.property
    def manual_approvals(
        self,
    ) -> "PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals":
        '''manual_approvals block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#manual_approvals PrivilegedAccessManagerEntitlement#manual_approvals}
        '''
        result = self._values.get("manual_approvals")
        assert result is not None, "Required property 'manual_approvals' is missing"
        return typing.cast("PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivilegedAccessManagerEntitlementApprovalWorkflow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privilegedAccessManagerEntitlement.PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals",
    jsii_struct_bases=[],
    name_mapping={
        "steps": "steps",
        "require_approver_justification": "requireApproverJustification",
    },
)
class PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals:
    def __init__(
        self,
        *,
        steps: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps", typing.Dict[builtins.str, typing.Any]]]],
        require_approver_justification: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param steps: steps block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#steps PrivilegedAccessManagerEntitlement#steps}
        :param require_approver_justification: Optional. Do the approvers need to provide a justification for their actions? Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#require_approver_justification PrivilegedAccessManagerEntitlement#require_approver_justification}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b06642ab46ec0286b2611176bd42053df4a7ba3ab45a6dfea65ce627b5ceff1)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps"]]:
        '''steps block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#steps PrivilegedAccessManagerEntitlement#steps}
        '''
        result = self._values.get("steps")
        assert result is not None, "Required property 'steps' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps"]], result)

    @builtins.property
    def require_approver_justification(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. Do the approvers need to provide a justification for their actions?

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#require_approver_justification PrivilegedAccessManagerEntitlement#require_approver_justification}
        '''
        result = self._values.get("require_approver_justification")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privilegedAccessManagerEntitlement.PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d376dcf83214452ddbec39d7a4591dc1285f7a7184213755d035a4234a25311a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSteps")
    def put_steps(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef043b309548a37a7f32428e4a341c0c35d177183a2a340bbb2be2f186c9ba56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSteps", [value]))

    @jsii.member(jsii_name="resetRequireApproverJustification")
    def reset_require_approver_justification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireApproverJustification", []))

    @builtins.property
    @jsii.member(jsii_name="steps")
    def steps(
        self,
    ) -> "PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsList":
        return typing.cast("PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsList", jsii.get(self, "steps"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps"]]], jsii.get(self, "stepsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b8511c73189183c1d7a5ea6dc0a99d4fbb74c0e71bb9a5b7fad5cf0468a672b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireApproverJustification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals]:
        return typing.cast(typing.Optional[PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8eeeb32c04f9f1bdc0880ef428d325309a381a0eeccac40cd1ff2f3752fd2ca7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privilegedAccessManagerEntitlement.PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps",
    jsii_struct_bases=[],
    name_mapping={
        "approvers": "approvers",
        "approvals_needed": "approvalsNeeded",
        "approver_email_recipients": "approverEmailRecipients",
    },
)
class PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps:
    def __init__(
        self,
        *,
        approvers: typing.Union["PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers", typing.Dict[builtins.str, typing.Any]],
        approvals_needed: typing.Optional[jsii.Number] = None,
        approver_email_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param approvers: approvers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#approvers PrivilegedAccessManagerEntitlement#approvers}
        :param approvals_needed: How many users from the above list need to approve. If there are not enough distinct users in the list above then the workflow will indefinitely block. Should always be greater than 0. Currently 1 is the only supported value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#approvals_needed PrivilegedAccessManagerEntitlement#approvals_needed}
        :param approver_email_recipients: Optional. Additional email addresses to be notified when a grant is pending approval. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#approver_email_recipients PrivilegedAccessManagerEntitlement#approver_email_recipients}
        '''
        if isinstance(approvers, dict):
            approvers = PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers(**approvers)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0ea57e97fab7b027abad9614847a526654af728c5165f85aebb556cec11246c)
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
    ) -> "PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers":
        '''approvers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#approvers PrivilegedAccessManagerEntitlement#approvers}
        '''
        result = self._values.get("approvers")
        assert result is not None, "Required property 'approvers' is missing"
        return typing.cast("PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers", result)

    @builtins.property
    def approvals_needed(self) -> typing.Optional[jsii.Number]:
        '''How many users from the above list need to approve.

        If there are not enough distinct users in the list above then the workflow
        will indefinitely block. Should always be greater than 0. Currently 1 is the only
        supported value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#approvals_needed PrivilegedAccessManagerEntitlement#approvals_needed}
        '''
        result = self._values.get("approvals_needed")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def approver_email_recipients(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. Additional email addresses to be notified when a grant is pending approval.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#approver_email_recipients PrivilegedAccessManagerEntitlement#approver_email_recipients}
        '''
        result = self._values.get("approver_email_recipients")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privilegedAccessManagerEntitlement.PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers",
    jsii_struct_bases=[],
    name_mapping={"principals": "principals"},
)
class PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers:
    def __init__(self, *, principals: typing.Sequence[builtins.str]) -> None:
        '''
        :param principals: Users who are being allowed for the operation. Each entry should be a valid v1 IAM Principal Identifier. Format for these is documented at: https://cloud.google.com/iam/docs/principal-identifiers#v1 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#principals PrivilegedAccessManagerEntitlement#principals}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92322a70fd4ac270b2e1c4a75b4102eb618d4d2063217262c8a3becbce3faf6e)
            check_type(argname="argument principals", value=principals, expected_type=type_hints["principals"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "principals": principals,
        }

    @builtins.property
    def principals(self) -> typing.List[builtins.str]:
        '''Users who are being allowed for the operation.

        Each entry should be a valid v1 IAM Principal Identifier. Format for these is documented at: https://cloud.google.com/iam/docs/principal-identifiers#v1

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#principals PrivilegedAccessManagerEntitlement#principals}
        '''
        result = self._values.get("principals")
        assert result is not None, "Required property 'principals' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApproversOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privilegedAccessManagerEntitlement.PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApproversOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b55331fc940ad62dac600f632526bfb61d7ec68f5a6239ceee0a1cbadb86c50)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a9c5f882cc9f855f98844191266120f757793458b39aa13d2744757ce7a9822)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principals", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers]:
        return typing.cast(typing.Optional[PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__535d400ebdf178185adf95b4bdc67242427cadd89a0c1106892152316ad275f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privilegedAccessManagerEntitlement.PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d67fcf37c2c5ad543ff1362b7b10604a8b6b796f04fde5df228347da9c12d22c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dede436a1283009d2687eeff9a1e5bf7cfd67454484fd74a5095147b738dcf9b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f847dc8b1775c6d01dfddde29933ce1fc448eeda299875fe5de5b44b2b073f6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd6db0afa0011a8f20ebd5a10d971148b4738af7e04f3ee87e173a79e92d2ead)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6625c541644ce5cd7137ddd70438fb133aa00b11616cbbd3c7c3cedd89f64569)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6033ba6ad0c5cdf80fd811aa5f47a2eefc126f4b2be6d7b7fca25b1dea470fe6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privilegedAccessManagerEntitlement.PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a9670426d3dcc9cacd54fccecc0d9070ef2b97a990f3241f865902fcf2c61e2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putApprovers")
    def put_approvers(self, *, principals: typing.Sequence[builtins.str]) -> None:
        '''
        :param principals: Users who are being allowed for the operation. Each entry should be a valid v1 IAM Principal Identifier. Format for these is documented at: https://cloud.google.com/iam/docs/principal-identifiers#v1 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#principals PrivilegedAccessManagerEntitlement#principals}
        '''
        value = PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers(
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
    ) -> PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApproversOutputReference:
        return typing.cast(PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApproversOutputReference, jsii.get(self, "approvers"))

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
    ) -> typing.Optional[PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers]:
        return typing.cast(typing.Optional[PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers], jsii.get(self, "approversInput"))

    @builtins.property
    @jsii.member(jsii_name="approvalsNeeded")
    def approvals_needed(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "approvalsNeeded"))

    @approvals_needed.setter
    def approvals_needed(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edb2e5f72b3d946c10f1a1edea2bab18a236b5ecf8bd57f6f08ec3d8a8056a1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "approvalsNeeded", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="approverEmailRecipients")
    def approver_email_recipients(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "approverEmailRecipients"))

    @approver_email_recipients.setter
    def approver_email_recipients(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfe02827bffcb40d175b3f68db11987c42a1f0781cd5bb3f5cb1247e00048539)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "approverEmailRecipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8535e57e0868af521924faa98f80941dcd687ccd84a22e7f5509120a99d6c6c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivilegedAccessManagerEntitlementApprovalWorkflowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privilegedAccessManagerEntitlement.PrivilegedAccessManagerEntitlementApprovalWorkflowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de43f43a39b121b7f969a64c145ad4f9455bdeddd4626650fabbaac8bc49eb22)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putManualApprovals")
    def put_manual_approvals(
        self,
        *,
        steps: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps, typing.Dict[builtins.str, typing.Any]]]],
        require_approver_justification: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param steps: steps block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#steps PrivilegedAccessManagerEntitlement#steps}
        :param require_approver_justification: Optional. Do the approvers need to provide a justification for their actions? Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#require_approver_justification PrivilegedAccessManagerEntitlement#require_approver_justification}
        '''
        value = PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals(
            steps=steps, require_approver_justification=require_approver_justification
        )

        return typing.cast(None, jsii.invoke(self, "putManualApprovals", [value]))

    @builtins.property
    @jsii.member(jsii_name="manualApprovals")
    def manual_approvals(
        self,
    ) -> PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsOutputReference:
        return typing.cast(PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsOutputReference, jsii.get(self, "manualApprovals"))

    @builtins.property
    @jsii.member(jsii_name="manualApprovalsInput")
    def manual_approvals_input(
        self,
    ) -> typing.Optional[PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals]:
        return typing.cast(typing.Optional[PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals], jsii.get(self, "manualApprovalsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivilegedAccessManagerEntitlementApprovalWorkflow]:
        return typing.cast(typing.Optional[PrivilegedAccessManagerEntitlementApprovalWorkflow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivilegedAccessManagerEntitlementApprovalWorkflow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__550110f7913e101315f076ca1b3a1f0f542381c272518eddbc4c4b47ea117356)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privilegedAccessManagerEntitlement.PrivilegedAccessManagerEntitlementConfig",
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
class PrivilegedAccessManagerEntitlementConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        eligible_users: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivilegedAccessManagerEntitlementEligibleUsers", typing.Dict[builtins.str, typing.Any]]]],
        entitlement_id: builtins.str,
        location: builtins.str,
        max_request_duration: builtins.str,
        parent: builtins.str,
        privileged_access: typing.Union["PrivilegedAccessManagerEntitlementPrivilegedAccess", typing.Dict[builtins.str, typing.Any]],
        requester_justification_config: typing.Union["PrivilegedAccessManagerEntitlementRequesterJustificationConfig", typing.Dict[builtins.str, typing.Any]],
        additional_notification_targets: typing.Optional[typing.Union[PrivilegedAccessManagerEntitlementAdditionalNotificationTargets, typing.Dict[builtins.str, typing.Any]]] = None,
        approval_workflow: typing.Optional[typing.Union[PrivilegedAccessManagerEntitlementApprovalWorkflow, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["PrivilegedAccessManagerEntitlementTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param eligible_users: eligible_users block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#eligible_users PrivilegedAccessManagerEntitlement#eligible_users}
        :param entitlement_id: The ID to use for this Entitlement. This will become the last part of the resource name. This value should be 4-63 characters, and valid characters are "[a-z]", "[0-9]", and "-". The first character should be from [a-z]. This value should be unique among all other Entitlements under the specified 'parent'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#entitlement_id PrivilegedAccessManagerEntitlement#entitlement_id}
        :param location: The region of the Entitlement resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#location PrivilegedAccessManagerEntitlement#location}
        :param max_request_duration: The maximum amount of time for which access would be granted for a request. A requester can choose to ask for access for less than this duration but never more. Format: calculate the time in seconds and concatenate it with 's' i.e. 2 hours = "7200s", 45 minutes = "2700s" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#max_request_duration PrivilegedAccessManagerEntitlement#max_request_duration}
        :param parent: Format: projects/{project-id|project-number} or organizations/{organization-number} or folders/{folder-number}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#parent PrivilegedAccessManagerEntitlement#parent}
        :param privileged_access: privileged_access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#privileged_access PrivilegedAccessManagerEntitlement#privileged_access}
        :param requester_justification_config: requester_justification_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#requester_justification_config PrivilegedAccessManagerEntitlement#requester_justification_config}
        :param additional_notification_targets: additional_notification_targets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#additional_notification_targets PrivilegedAccessManagerEntitlement#additional_notification_targets}
        :param approval_workflow: approval_workflow block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#approval_workflow PrivilegedAccessManagerEntitlement#approval_workflow}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#id PrivilegedAccessManagerEntitlement#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#timeouts PrivilegedAccessManagerEntitlement#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(privileged_access, dict):
            privileged_access = PrivilegedAccessManagerEntitlementPrivilegedAccess(**privileged_access)
        if isinstance(requester_justification_config, dict):
            requester_justification_config = PrivilegedAccessManagerEntitlementRequesterJustificationConfig(**requester_justification_config)
        if isinstance(additional_notification_targets, dict):
            additional_notification_targets = PrivilegedAccessManagerEntitlementAdditionalNotificationTargets(**additional_notification_targets)
        if isinstance(approval_workflow, dict):
            approval_workflow = PrivilegedAccessManagerEntitlementApprovalWorkflow(**approval_workflow)
        if isinstance(timeouts, dict):
            timeouts = PrivilegedAccessManagerEntitlementTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f632305ceabf174e85d18e2b0c73b6bfff1ad54b24b8e9ac5825e45a2acf1cc4)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivilegedAccessManagerEntitlementEligibleUsers"]]:
        '''eligible_users block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#eligible_users PrivilegedAccessManagerEntitlement#eligible_users}
        '''
        result = self._values.get("eligible_users")
        assert result is not None, "Required property 'eligible_users' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivilegedAccessManagerEntitlementEligibleUsers"]], result)

    @builtins.property
    def entitlement_id(self) -> builtins.str:
        '''The ID to use for this Entitlement.

        This will become the last part of the resource name.
        This value should be 4-63 characters, and valid characters are "[a-z]", "[0-9]", and "-". The first character should be from [a-z].
        This value should be unique among all other Entitlements under the specified 'parent'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#entitlement_id PrivilegedAccessManagerEntitlement#entitlement_id}
        '''
        result = self._values.get("entitlement_id")
        assert result is not None, "Required property 'entitlement_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The region of the Entitlement resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#location PrivilegedAccessManagerEntitlement#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def max_request_duration(self) -> builtins.str:
        '''The maximum amount of time for which access would be granted for a request.

        A requester can choose to ask for access for less than this duration but never more.
        Format: calculate the time in seconds and concatenate it with 's' i.e. 2 hours = "7200s", 45 minutes = "2700s"

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#max_request_duration PrivilegedAccessManagerEntitlement#max_request_duration}
        '''
        result = self._values.get("max_request_duration")
        assert result is not None, "Required property 'max_request_duration' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parent(self) -> builtins.str:
        '''Format: projects/{project-id|project-number} or organizations/{organization-number} or folders/{folder-number}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#parent PrivilegedAccessManagerEntitlement#parent}
        '''
        result = self._values.get("parent")
        assert result is not None, "Required property 'parent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def privileged_access(self) -> "PrivilegedAccessManagerEntitlementPrivilegedAccess":
        '''privileged_access block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#privileged_access PrivilegedAccessManagerEntitlement#privileged_access}
        '''
        result = self._values.get("privileged_access")
        assert result is not None, "Required property 'privileged_access' is missing"
        return typing.cast("PrivilegedAccessManagerEntitlementPrivilegedAccess", result)

    @builtins.property
    def requester_justification_config(
        self,
    ) -> "PrivilegedAccessManagerEntitlementRequesterJustificationConfig":
        '''requester_justification_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#requester_justification_config PrivilegedAccessManagerEntitlement#requester_justification_config}
        '''
        result = self._values.get("requester_justification_config")
        assert result is not None, "Required property 'requester_justification_config' is missing"
        return typing.cast("PrivilegedAccessManagerEntitlementRequesterJustificationConfig", result)

    @builtins.property
    def additional_notification_targets(
        self,
    ) -> typing.Optional[PrivilegedAccessManagerEntitlementAdditionalNotificationTargets]:
        '''additional_notification_targets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#additional_notification_targets PrivilegedAccessManagerEntitlement#additional_notification_targets}
        '''
        result = self._values.get("additional_notification_targets")
        return typing.cast(typing.Optional[PrivilegedAccessManagerEntitlementAdditionalNotificationTargets], result)

    @builtins.property
    def approval_workflow(
        self,
    ) -> typing.Optional[PrivilegedAccessManagerEntitlementApprovalWorkflow]:
        '''approval_workflow block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#approval_workflow PrivilegedAccessManagerEntitlement#approval_workflow}
        '''
        result = self._values.get("approval_workflow")
        return typing.cast(typing.Optional[PrivilegedAccessManagerEntitlementApprovalWorkflow], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#id PrivilegedAccessManagerEntitlement#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["PrivilegedAccessManagerEntitlementTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#timeouts PrivilegedAccessManagerEntitlement#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["PrivilegedAccessManagerEntitlementTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivilegedAccessManagerEntitlementConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privilegedAccessManagerEntitlement.PrivilegedAccessManagerEntitlementEligibleUsers",
    jsii_struct_bases=[],
    name_mapping={"principals": "principals"},
)
class PrivilegedAccessManagerEntitlementEligibleUsers:
    def __init__(self, *, principals: typing.Sequence[builtins.str]) -> None:
        '''
        :param principals: Users who are being allowed for the operation. Each entry should be a valid v1 IAM Principal Identifier. Format for these is documented at "https://cloud.google.com/iam/docs/principal-identifiers#v1" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#principals PrivilegedAccessManagerEntitlement#principals}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecd229aca6e88b027d88d28f4f6bb10e5fd425a0b93a5f47698cc42b31f0d410)
            check_type(argname="argument principals", value=principals, expected_type=type_hints["principals"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "principals": principals,
        }

    @builtins.property
    def principals(self) -> typing.List[builtins.str]:
        '''Users who are being allowed for the operation.

        Each entry should be a valid v1 IAM Principal Identifier. Format for these is documented at "https://cloud.google.com/iam/docs/principal-identifiers#v1"

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#principals PrivilegedAccessManagerEntitlement#principals}
        '''
        result = self._values.get("principals")
        assert result is not None, "Required property 'principals' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivilegedAccessManagerEntitlementEligibleUsers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivilegedAccessManagerEntitlementEligibleUsersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privilegedAccessManagerEntitlement.PrivilegedAccessManagerEntitlementEligibleUsersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__65961d2894ed651e49460ce2160e6b078400080e50dee1d18de450f3a0862e00)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivilegedAccessManagerEntitlementEligibleUsersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3645d2d0d2a1419f24d930830d676a055d286862983c8fc450b545aee7bb5d9d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivilegedAccessManagerEntitlementEligibleUsersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aba3e0903e670a71f84b521136e7621d7443846a15d816e64c6cbbb1d7992fb2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__37789999095be30c6c51133490cd981fe10c3f0bc2a32eb837a02530e509aa3f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__efacb7083c207526990c8bda26e81190c954320a1bba1d82047819f795114014)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivilegedAccessManagerEntitlementEligibleUsers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivilegedAccessManagerEntitlementEligibleUsers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivilegedAccessManagerEntitlementEligibleUsers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85498080a0fc5efe2d3808a355dc388628900a884f3bdd7f97a9b63340e82163)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivilegedAccessManagerEntitlementEligibleUsersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privilegedAccessManagerEntitlement.PrivilegedAccessManagerEntitlementEligibleUsersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__292edfca66e7bef2f3144ccbe88eb980b1ff981a9a1103f5132ffda478e2b3ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4823416b13f42ac8a4298503559d17f42305fd9351941e3b2bed9655f5b87874)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principals", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivilegedAccessManagerEntitlementEligibleUsers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivilegedAccessManagerEntitlementEligibleUsers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivilegedAccessManagerEntitlementEligibleUsers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d9e7ca251ee14caed8986c5dc4f351d3fef5a9abf67fb48b10e2fd3d0db828f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privilegedAccessManagerEntitlement.PrivilegedAccessManagerEntitlementPrivilegedAccess",
    jsii_struct_bases=[],
    name_mapping={"gcp_iam_access": "gcpIamAccess"},
)
class PrivilegedAccessManagerEntitlementPrivilegedAccess:
    def __init__(
        self,
        *,
        gcp_iam_access: typing.Union["PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param gcp_iam_access: gcp_iam_access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#gcp_iam_access PrivilegedAccessManagerEntitlement#gcp_iam_access}
        '''
        if isinstance(gcp_iam_access, dict):
            gcp_iam_access = PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess(**gcp_iam_access)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36318f37225131252fca306d34a87478d2ca935847353b2f5a98c0c5d1d5cf6c)
            check_type(argname="argument gcp_iam_access", value=gcp_iam_access, expected_type=type_hints["gcp_iam_access"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "gcp_iam_access": gcp_iam_access,
        }

    @builtins.property
    def gcp_iam_access(
        self,
    ) -> "PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess":
        '''gcp_iam_access block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#gcp_iam_access PrivilegedAccessManagerEntitlement#gcp_iam_access}
        '''
        result = self._values.get("gcp_iam_access")
        assert result is not None, "Required property 'gcp_iam_access' is missing"
        return typing.cast("PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivilegedAccessManagerEntitlementPrivilegedAccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privilegedAccessManagerEntitlement.PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess",
    jsii_struct_bases=[],
    name_mapping={
        "resource": "resource",
        "resource_type": "resourceType",
        "role_bindings": "roleBindings",
    },
)
class PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess:
    def __init__(
        self,
        *,
        resource: builtins.str,
        resource_type: builtins.str,
        role_bindings: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param resource: Name of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#resource PrivilegedAccessManagerEntitlement#resource}
        :param resource_type: The type of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#resource_type PrivilegedAccessManagerEntitlement#resource_type}
        :param role_bindings: role_bindings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#role_bindings PrivilegedAccessManagerEntitlement#role_bindings}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e7a53949e67fa5c73c27097ff8230af8292df9170bbc1fe3f0e5f1dff0ac370)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#resource PrivilegedAccessManagerEntitlement#resource}
        '''
        result = self._values.get("resource")
        assert result is not None, "Required property 'resource' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_type(self) -> builtins.str:
        '''The type of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#resource_type PrivilegedAccessManagerEntitlement#resource_type}
        '''
        result = self._values.get("resource_type")
        assert result is not None, "Required property 'resource_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_bindings(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings"]]:
        '''role_bindings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#role_bindings PrivilegedAccessManagerEntitlement#role_bindings}
        '''
        result = self._values.get("role_bindings")
        assert result is not None, "Required property 'role_bindings' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privilegedAccessManagerEntitlement.PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e2dc34bfee26553a1deb632ca6f5be37b6aba1c641b7212b03ad9ca7faccdf0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRoleBindings")
    def put_role_bindings(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__167738d128a873981d30435348139ba5758e820ebbbbe6c3a4e976115be33fbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRoleBindings", [value]))

    @builtins.property
    @jsii.member(jsii_name="roleBindings")
    def role_bindings(
        self,
    ) -> "PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindingsList":
        return typing.cast("PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindingsList", jsii.get(self, "roleBindings"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings"]]], jsii.get(self, "roleBindingsInput"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resource"))

    @resource.setter
    def resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c76e6c5f82286547e654d86ca0b6a3ca32615ce1e6401d3cfa5e58867e73eeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceType"))

    @resource_type.setter
    def resource_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb0328ca1e10ea1ceda11a5f83b01378df488c83bbca9d464819634008cf894a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess]:
        return typing.cast(typing.Optional[PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c8882311119a53112230505608dbb2b407e51fe43cde008b1734a81d75fe60c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privilegedAccessManagerEntitlement.PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings",
    jsii_struct_bases=[],
    name_mapping={"role": "role", "condition_expression": "conditionExpression"},
)
class PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings:
    def __init__(
        self,
        *,
        role: builtins.str,
        condition_expression: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param role: IAM role to be granted. https://cloud.google.com/iam/docs/roles-overview. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#role PrivilegedAccessManagerEntitlement#role}
        :param condition_expression: The expression field of the IAM condition to be associated with the role. If specified, a user with an active grant for this entitlement would be able to access the resource only if this condition evaluates to true for their request. https://cloud.google.com/iam/docs/conditions-overview#attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#condition_expression PrivilegedAccessManagerEntitlement#condition_expression}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34ec2165f126deb08e42528c5d5bc16862028dc9ff13ff4395bb8f89179126cb)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#role PrivilegedAccessManagerEntitlement#role}
        '''
        result = self._values.get("role")
        assert result is not None, "Required property 'role' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def condition_expression(self) -> typing.Optional[builtins.str]:
        '''The expression field of the IAM condition to be associated with the role.

        If specified, a user with an active grant for this entitlement would be able to access the resource only if this condition evaluates to true for their request.
        https://cloud.google.com/iam/docs/conditions-overview#attributes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#condition_expression PrivilegedAccessManagerEntitlement#condition_expression}
        '''
        result = self._values.get("condition_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindingsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privilegedAccessManagerEntitlement.PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindingsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__833e9518fdd64539af12bfa9235014faa7dee08ba76de8f7c3fbb55e2b3d1ff5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindingsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__940da6a27c425a2608eb8bdb229b2a6723b027d8953ee0b5718dc9777a8eaf2f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindingsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__250929dad61fd5b0d9e188c1bedde3825ae310d58712f029d0442ba7c08e1552)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b0b76bf6f59df0388b950f439e6df8af671876462318fb49f95d61e4f015077)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca98afa333be03a1799ef70594dbf7ac323bd000694c1c933487858b78ef74de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b56750e53b412ae40206d84d01c3584f87d2b9284bfd2f04125113e730e48948)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privilegedAccessManagerEntitlement.PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f96c0cb3c6b2302bc10b7c94f612834ba6b3a2a6bf3764de7854cbaa8c4a0ee0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b50d46207cdaec416549cd9c429881a7998f9d2f5df93defe400b594a9db90f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "conditionExpression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @role.setter
    def role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72869d99de520b8b312efc4fb11661e8fe56e534f07b1fb73c0fe3d9faa3be9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "role", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a9907e0421782595661f368c6ca250cc0c9f18a6a06e4eba428743ee820a076)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivilegedAccessManagerEntitlementPrivilegedAccessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privilegedAccessManagerEntitlement.PrivilegedAccessManagerEntitlementPrivilegedAccessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5c8404380b1f17cdda5527e2083d9c5f545429f7015678e999ef10618086b58)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGcpIamAccess")
    def put_gcp_iam_access(
        self,
        *,
        resource: builtins.str,
        resource_type: builtins.str,
        role_bindings: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param resource: Name of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#resource PrivilegedAccessManagerEntitlement#resource}
        :param resource_type: The type of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#resource_type PrivilegedAccessManagerEntitlement#resource_type}
        :param role_bindings: role_bindings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#role_bindings PrivilegedAccessManagerEntitlement#role_bindings}
        '''
        value = PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess(
            resource=resource, resource_type=resource_type, role_bindings=role_bindings
        )

        return typing.cast(None, jsii.invoke(self, "putGcpIamAccess", [value]))

    @builtins.property
    @jsii.member(jsii_name="gcpIamAccess")
    def gcp_iam_access(
        self,
    ) -> PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessOutputReference:
        return typing.cast(PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessOutputReference, jsii.get(self, "gcpIamAccess"))

    @builtins.property
    @jsii.member(jsii_name="gcpIamAccessInput")
    def gcp_iam_access_input(
        self,
    ) -> typing.Optional[PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess]:
        return typing.cast(typing.Optional[PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess], jsii.get(self, "gcpIamAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivilegedAccessManagerEntitlementPrivilegedAccess]:
        return typing.cast(typing.Optional[PrivilegedAccessManagerEntitlementPrivilegedAccess], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivilegedAccessManagerEntitlementPrivilegedAccess],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a3109c932b9c44f4a7290411b69b9a6fa3dfd197f15f00557f2a4e21fefa9ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privilegedAccessManagerEntitlement.PrivilegedAccessManagerEntitlementRequesterJustificationConfig",
    jsii_struct_bases=[],
    name_mapping={"not_mandatory": "notMandatory", "unstructured": "unstructured"},
)
class PrivilegedAccessManagerEntitlementRequesterJustificationConfig:
    def __init__(
        self,
        *,
        not_mandatory: typing.Optional[typing.Union["PrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory", typing.Dict[builtins.str, typing.Any]]] = None,
        unstructured: typing.Optional[typing.Union["PrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param not_mandatory: not_mandatory block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#not_mandatory PrivilegedAccessManagerEntitlement#not_mandatory}
        :param unstructured: unstructured block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#unstructured PrivilegedAccessManagerEntitlement#unstructured}
        '''
        if isinstance(not_mandatory, dict):
            not_mandatory = PrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory(**not_mandatory)
        if isinstance(unstructured, dict):
            unstructured = PrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured(**unstructured)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbf66f24e532ceea4395d640da827b8b9b9307dc9b187995472d596217f81af2)
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
    ) -> typing.Optional["PrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory"]:
        '''not_mandatory block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#not_mandatory PrivilegedAccessManagerEntitlement#not_mandatory}
        '''
        result = self._values.get("not_mandatory")
        return typing.cast(typing.Optional["PrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory"], result)

    @builtins.property
    def unstructured(
        self,
    ) -> typing.Optional["PrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured"]:
        '''unstructured block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#unstructured PrivilegedAccessManagerEntitlement#unstructured}
        '''
        result = self._values.get("unstructured")
        return typing.cast(typing.Optional["PrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivilegedAccessManagerEntitlementRequesterJustificationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privilegedAccessManagerEntitlement.PrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory",
    jsii_struct_bases=[],
    name_mapping={},
)
class PrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privilegedAccessManagerEntitlement.PrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a62e6d670993c9b37582bd0a7d875e00cd349829eb583de49d488342e42f67d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory]:
        return typing.cast(typing.Optional[PrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cba0094c065cfc1dec9ba55f6149041b6ba0ac79635c07dbe9b3fc1965a0932)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivilegedAccessManagerEntitlementRequesterJustificationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privilegedAccessManagerEntitlement.PrivilegedAccessManagerEntitlementRequesterJustificationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f259b57fbc4fcc232108779b1df5e11742d5d3573d6ab6c7372ce675682e09a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNotMandatory")
    def put_not_mandatory(self) -> None:
        value = PrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory()

        return typing.cast(None, jsii.invoke(self, "putNotMandatory", [value]))

    @jsii.member(jsii_name="putUnstructured")
    def put_unstructured(self) -> None:
        value = PrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured()

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
    ) -> PrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatoryOutputReference:
        return typing.cast(PrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatoryOutputReference, jsii.get(self, "notMandatory"))

    @builtins.property
    @jsii.member(jsii_name="unstructured")
    def unstructured(
        self,
    ) -> "PrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructuredOutputReference":
        return typing.cast("PrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructuredOutputReference", jsii.get(self, "unstructured"))

    @builtins.property
    @jsii.member(jsii_name="notMandatoryInput")
    def not_mandatory_input(
        self,
    ) -> typing.Optional[PrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory]:
        return typing.cast(typing.Optional[PrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory], jsii.get(self, "notMandatoryInput"))

    @builtins.property
    @jsii.member(jsii_name="unstructuredInput")
    def unstructured_input(
        self,
    ) -> typing.Optional["PrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured"]:
        return typing.cast(typing.Optional["PrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured"], jsii.get(self, "unstructuredInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivilegedAccessManagerEntitlementRequesterJustificationConfig]:
        return typing.cast(typing.Optional[PrivilegedAccessManagerEntitlementRequesterJustificationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivilegedAccessManagerEntitlementRequesterJustificationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41b9138187cb0f0bdbf12675d7318ddf513fa018ddfe545c79517153dd06c147)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privilegedAccessManagerEntitlement.PrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured",
    jsii_struct_bases=[],
    name_mapping={},
)
class PrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructuredOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privilegedAccessManagerEntitlement.PrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructuredOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__886fecf70c02d64d7a762bb7b041346aac9cf4ac6f66e80eab47b24ca66a2da9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured]:
        return typing.cast(typing.Optional[PrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf140ea24e6bfc2d4b1b782945a2663c753f1d6df25c75ec3575f008c6d3badb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privilegedAccessManagerEntitlement.PrivilegedAccessManagerEntitlementTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class PrivilegedAccessManagerEntitlementTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#create PrivilegedAccessManagerEntitlement#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#delete PrivilegedAccessManagerEntitlement#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#update PrivilegedAccessManagerEntitlement#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b7ffe7056ee73adf18ab4cac181981128c072b9eea2218130cd15cce49a3681)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#create PrivilegedAccessManagerEntitlement#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#delete PrivilegedAccessManagerEntitlement#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privileged_access_manager_entitlement#update PrivilegedAccessManagerEntitlement#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivilegedAccessManagerEntitlementTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivilegedAccessManagerEntitlementTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privilegedAccessManagerEntitlement.PrivilegedAccessManagerEntitlementTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc63e77b542e28cf0633d8b996160cd6ab2e50308a795adf345ce6f2106601b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__03bbc439291eb8e36f9ff425aceadd9244692b3b53290b23c55361d1049ef090)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc81c0e55d4c2fabdbd551af625006af64b1f4f238d71f23090a47a8d28ce5ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2e6ec0548bfb53021dc20cb6c622bd6444557f6cab8f45ba9fd836f4fa045e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivilegedAccessManagerEntitlementTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivilegedAccessManagerEntitlementTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivilegedAccessManagerEntitlementTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f73f09fda3e3e232227615eebaa6ee3279e1a9432c80cae6ad2d063b67a08cac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "PrivilegedAccessManagerEntitlement",
    "PrivilegedAccessManagerEntitlementAdditionalNotificationTargets",
    "PrivilegedAccessManagerEntitlementAdditionalNotificationTargetsOutputReference",
    "PrivilegedAccessManagerEntitlementApprovalWorkflow",
    "PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals",
    "PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsOutputReference",
    "PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps",
    "PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers",
    "PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApproversOutputReference",
    "PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsList",
    "PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsOutputReference",
    "PrivilegedAccessManagerEntitlementApprovalWorkflowOutputReference",
    "PrivilegedAccessManagerEntitlementConfig",
    "PrivilegedAccessManagerEntitlementEligibleUsers",
    "PrivilegedAccessManagerEntitlementEligibleUsersList",
    "PrivilegedAccessManagerEntitlementEligibleUsersOutputReference",
    "PrivilegedAccessManagerEntitlementPrivilegedAccess",
    "PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess",
    "PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessOutputReference",
    "PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings",
    "PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindingsList",
    "PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindingsOutputReference",
    "PrivilegedAccessManagerEntitlementPrivilegedAccessOutputReference",
    "PrivilegedAccessManagerEntitlementRequesterJustificationConfig",
    "PrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory",
    "PrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatoryOutputReference",
    "PrivilegedAccessManagerEntitlementRequesterJustificationConfigOutputReference",
    "PrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured",
    "PrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructuredOutputReference",
    "PrivilegedAccessManagerEntitlementTimeouts",
    "PrivilegedAccessManagerEntitlementTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__6241e5bd7533db9d1ceea698bd90ba52bacef0d4da57a9b4084f683a6ef0c621(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    eligible_users: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivilegedAccessManagerEntitlementEligibleUsers, typing.Dict[builtins.str, typing.Any]]]],
    entitlement_id: builtins.str,
    location: builtins.str,
    max_request_duration: builtins.str,
    parent: builtins.str,
    privileged_access: typing.Union[PrivilegedAccessManagerEntitlementPrivilegedAccess, typing.Dict[builtins.str, typing.Any]],
    requester_justification_config: typing.Union[PrivilegedAccessManagerEntitlementRequesterJustificationConfig, typing.Dict[builtins.str, typing.Any]],
    additional_notification_targets: typing.Optional[typing.Union[PrivilegedAccessManagerEntitlementAdditionalNotificationTargets, typing.Dict[builtins.str, typing.Any]]] = None,
    approval_workflow: typing.Optional[typing.Union[PrivilegedAccessManagerEntitlementApprovalWorkflow, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[PrivilegedAccessManagerEntitlementTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__594c016c75b39a41453af7d75aca55a0871040ea377b9674526cf8ddcabfbee5(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__649b9b6393ae2e4385a84ed5abd91b5a6a6a141903515cce2f6421dc21672afc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivilegedAccessManagerEntitlementEligibleUsers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__018b6bcf75b78ead94537d76b088ad63d4489ad1f1e233dec2ba72aad61967a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a243a8ebe3c2044ed3f44233efce9d2cf89c5e3969a5f2fc43aadbe263d4865(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b135b30ff543a82fa053bffc9ea773e7e14bd0719330b56c0c0ecbfd5254f260(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8171cd1baf3f2c696218117438b60025ac679244ced9c25a8fe3573a55fc5cb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff3c6c492f364cc91ed8f1d40cbb39b91dc92dff4118a1b9b9bb065a868e8bd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17540d90177c5de99cbd0a8672ce255c9986b90c90979e1611426e26a128200a(
    *,
    admin_email_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    requester_email_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccebc1aa4d72987d8c330e5692b752d7c9e33078103b4025f88fca2cea84b7d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__889545faebb2c338e94394e3929141ce605f285d1560812e5f1acde129ba7931(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3702ae145c2e2876095bdce0020d0e4c1f4df3e155112dabcbe4c461fb9185d2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ddd3156ec437d2e1f8ebd18cf5c8b1637a4298de58d333b51ae73b312cf4a28(
    value: typing.Optional[PrivilegedAccessManagerEntitlementAdditionalNotificationTargets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae977dbc1c02e5f7adbeedec229f83bb3ccf4c5b7b4ddf62016c79fba21ff604(
    *,
    manual_approvals: typing.Union[PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b06642ab46ec0286b2611176bd42053df4a7ba3ab45a6dfea65ce627b5ceff1(
    *,
    steps: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps, typing.Dict[builtins.str, typing.Any]]]],
    require_approver_justification: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d376dcf83214452ddbec39d7a4591dc1285f7a7184213755d035a4234a25311a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef043b309548a37a7f32428e4a341c0c35d177183a2a340bbb2be2f186c9ba56(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8511c73189183c1d7a5ea6dc0a99d4fbb74c0e71bb9a5b7fad5cf0468a672b2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eeeb32c04f9f1bdc0880ef428d325309a381a0eeccac40cd1ff2f3752fd2ca7(
    value: typing.Optional[PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovals],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0ea57e97fab7b027abad9614847a526654af728c5165f85aebb556cec11246c(
    *,
    approvers: typing.Union[PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers, typing.Dict[builtins.str, typing.Any]],
    approvals_needed: typing.Optional[jsii.Number] = None,
    approver_email_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92322a70fd4ac270b2e1c4a75b4102eb618d4d2063217262c8a3becbce3faf6e(
    *,
    principals: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b55331fc940ad62dac600f632526bfb61d7ec68f5a6239ceee0a1cbadb86c50(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a9c5f882cc9f855f98844191266120f757793458b39aa13d2744757ce7a9822(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__535d400ebdf178185adf95b4bdc67242427cadd89a0c1106892152316ad275f8(
    value: typing.Optional[PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsStepsApprovers],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d67fcf37c2c5ad543ff1362b7b10604a8b6b796f04fde5df228347da9c12d22c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dede436a1283009d2687eeff9a1e5bf7cfd67454484fd74a5095147b738dcf9b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f847dc8b1775c6d01dfddde29933ce1fc448eeda299875fe5de5b44b2b073f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd6db0afa0011a8f20ebd5a10d971148b4738af7e04f3ee87e173a79e92d2ead(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6625c541644ce5cd7137ddd70438fb133aa00b11616cbbd3c7c3cedd89f64569(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6033ba6ad0c5cdf80fd811aa5f47a2eefc126f4b2be6d7b7fca25b1dea470fe6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a9670426d3dcc9cacd54fccecc0d9070ef2b97a990f3241f865902fcf2c61e2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edb2e5f72b3d946c10f1a1edea2bab18a236b5ecf8bd57f6f08ec3d8a8056a1a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfe02827bffcb40d175b3f68db11987c42a1f0781cd5bb3f5cb1247e00048539(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8535e57e0868af521924faa98f80941dcd687ccd84a22e7f5509120a99d6c6c4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivilegedAccessManagerEntitlementApprovalWorkflowManualApprovalsSteps]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de43f43a39b121b7f969a64c145ad4f9455bdeddd4626650fabbaac8bc49eb22(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__550110f7913e101315f076ca1b3a1f0f542381c272518eddbc4c4b47ea117356(
    value: typing.Optional[PrivilegedAccessManagerEntitlementApprovalWorkflow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f632305ceabf174e85d18e2b0c73b6bfff1ad54b24b8e9ac5825e45a2acf1cc4(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    eligible_users: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivilegedAccessManagerEntitlementEligibleUsers, typing.Dict[builtins.str, typing.Any]]]],
    entitlement_id: builtins.str,
    location: builtins.str,
    max_request_duration: builtins.str,
    parent: builtins.str,
    privileged_access: typing.Union[PrivilegedAccessManagerEntitlementPrivilegedAccess, typing.Dict[builtins.str, typing.Any]],
    requester_justification_config: typing.Union[PrivilegedAccessManagerEntitlementRequesterJustificationConfig, typing.Dict[builtins.str, typing.Any]],
    additional_notification_targets: typing.Optional[typing.Union[PrivilegedAccessManagerEntitlementAdditionalNotificationTargets, typing.Dict[builtins.str, typing.Any]]] = None,
    approval_workflow: typing.Optional[typing.Union[PrivilegedAccessManagerEntitlementApprovalWorkflow, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[PrivilegedAccessManagerEntitlementTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecd229aca6e88b027d88d28f4f6bb10e5fd425a0b93a5f47698cc42b31f0d410(
    *,
    principals: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65961d2894ed651e49460ce2160e6b078400080e50dee1d18de450f3a0862e00(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3645d2d0d2a1419f24d930830d676a055d286862983c8fc450b545aee7bb5d9d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aba3e0903e670a71f84b521136e7621d7443846a15d816e64c6cbbb1d7992fb2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37789999095be30c6c51133490cd981fe10c3f0bc2a32eb837a02530e509aa3f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efacb7083c207526990c8bda26e81190c954320a1bba1d82047819f795114014(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85498080a0fc5efe2d3808a355dc388628900a884f3bdd7f97a9b63340e82163(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivilegedAccessManagerEntitlementEligibleUsers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__292edfca66e7bef2f3144ccbe88eb980b1ff981a9a1103f5132ffda478e2b3ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4823416b13f42ac8a4298503559d17f42305fd9351941e3b2bed9655f5b87874(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d9e7ca251ee14caed8986c5dc4f351d3fef5a9abf67fb48b10e2fd3d0db828f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivilegedAccessManagerEntitlementEligibleUsers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36318f37225131252fca306d34a87478d2ca935847353b2f5a98c0c5d1d5cf6c(
    *,
    gcp_iam_access: typing.Union[PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e7a53949e67fa5c73c27097ff8230af8292df9170bbc1fe3f0e5f1dff0ac370(
    *,
    resource: builtins.str,
    resource_type: builtins.str,
    role_bindings: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e2dc34bfee26553a1deb632ca6f5be37b6aba1c641b7212b03ad9ca7faccdf0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__167738d128a873981d30435348139ba5758e820ebbbbe6c3a4e976115be33fbf(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c76e6c5f82286547e654d86ca0b6a3ca32615ce1e6401d3cfa5e58867e73eeb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb0328ca1e10ea1ceda11a5f83b01378df488c83bbca9d464819634008cf894a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c8882311119a53112230505608dbb2b407e51fe43cde008b1734a81d75fe60c(
    value: typing.Optional[PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccess],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34ec2165f126deb08e42528c5d5bc16862028dc9ff13ff4395bb8f89179126cb(
    *,
    role: builtins.str,
    condition_expression: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__833e9518fdd64539af12bfa9235014faa7dee08ba76de8f7c3fbb55e2b3d1ff5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__940da6a27c425a2608eb8bdb229b2a6723b027d8953ee0b5718dc9777a8eaf2f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__250929dad61fd5b0d9e188c1bedde3825ae310d58712f029d0442ba7c08e1552(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b0b76bf6f59df0388b950f439e6df8af671876462318fb49f95d61e4f015077(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca98afa333be03a1799ef70594dbf7ac323bd000694c1c933487858b78ef74de(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b56750e53b412ae40206d84d01c3584f87d2b9284bfd2f04125113e730e48948(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f96c0cb3c6b2302bc10b7c94f612834ba6b3a2a6bf3764de7854cbaa8c4a0ee0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b50d46207cdaec416549cd9c429881a7998f9d2f5df93defe400b594a9db90f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72869d99de520b8b312efc4fb11661e8fe56e534f07b1fb73c0fe3d9faa3be9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a9907e0421782595661f368c6ca250cc0c9f18a6a06e4eba428743ee820a076(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivilegedAccessManagerEntitlementPrivilegedAccessGcpIamAccessRoleBindings]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5c8404380b1f17cdda5527e2083d9c5f545429f7015678e999ef10618086b58(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a3109c932b9c44f4a7290411b69b9a6fa3dfd197f15f00557f2a4e21fefa9ed(
    value: typing.Optional[PrivilegedAccessManagerEntitlementPrivilegedAccess],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbf66f24e532ceea4395d640da827b8b9b9307dc9b187995472d596217f81af2(
    *,
    not_mandatory: typing.Optional[typing.Union[PrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory, typing.Dict[builtins.str, typing.Any]]] = None,
    unstructured: typing.Optional[typing.Union[PrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a62e6d670993c9b37582bd0a7d875e00cd349829eb583de49d488342e42f67d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cba0094c065cfc1dec9ba55f6149041b6ba0ac79635c07dbe9b3fc1965a0932(
    value: typing.Optional[PrivilegedAccessManagerEntitlementRequesterJustificationConfigNotMandatory],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f259b57fbc4fcc232108779b1df5e11742d5d3573d6ab6c7372ce675682e09a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41b9138187cb0f0bdbf12675d7318ddf513fa018ddfe545c79517153dd06c147(
    value: typing.Optional[PrivilegedAccessManagerEntitlementRequesterJustificationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__886fecf70c02d64d7a762bb7b041346aac9cf4ac6f66e80eab47b24ca66a2da9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf140ea24e6bfc2d4b1b782945a2663c753f1d6df25c75ec3575f008c6d3badb(
    value: typing.Optional[PrivilegedAccessManagerEntitlementRequesterJustificationConfigUnstructured],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b7ffe7056ee73adf18ab4cac181981128c072b9eea2218130cd15cce49a3681(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc63e77b542e28cf0633d8b996160cd6ab2e50308a795adf345ce6f2106601b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03bbc439291eb8e36f9ff425aceadd9244692b3b53290b23c55361d1049ef090(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc81c0e55d4c2fabdbd551af625006af64b1f4f238d71f23090a47a8d28ce5ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2e6ec0548bfb53021dc20cb6c622bd6444557f6cab8f45ba9fd836f4fa045e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f73f09fda3e3e232227615eebaa6ee3279e1a9432c80cae6ad2d063b67a08cac(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivilegedAccessManagerEntitlementTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
