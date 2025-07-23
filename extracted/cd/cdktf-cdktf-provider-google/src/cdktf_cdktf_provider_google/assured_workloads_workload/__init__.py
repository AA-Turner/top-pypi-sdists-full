r'''
# `google_assured_workloads_workload`

Refer to the Terraform Registry for docs: [`google_assured_workloads_workload`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload).
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


class AssuredWorkloadsWorkload(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.assuredWorkloadsWorkload.AssuredWorkloadsWorkload",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload google_assured_workloads_workload}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        compliance_regime: builtins.str,
        display_name: builtins.str,
        location: builtins.str,
        organization: builtins.str,
        billing_account: typing.Optional[builtins.str] = None,
        enable_sovereign_controls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        kms_settings: typing.Optional[typing.Union["AssuredWorkloadsWorkloadKmsSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        partner: typing.Optional[builtins.str] = None,
        partner_permissions: typing.Optional[typing.Union["AssuredWorkloadsWorkloadPartnerPermissions", typing.Dict[builtins.str, typing.Any]]] = None,
        partner_services_billing_account: typing.Optional[builtins.str] = None,
        provisioned_resources_parent: typing.Optional[builtins.str] = None,
        resource_settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AssuredWorkloadsWorkloadResourceSettings", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["AssuredWorkloadsWorkloadTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        violation_notifications_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        workload_options: typing.Optional[typing.Union["AssuredWorkloadsWorkloadWorkloadOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload google_assured_workloads_workload} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param compliance_regime: Required. Immutable. Compliance Regime associated with this workload. Possible values: COMPLIANCE_REGIME_UNSPECIFIED, IL4, CJIS, FEDRAMP_HIGH, FEDRAMP_MODERATE, US_REGIONAL_ACCESS, HIPAA, HITRUST, EU_REGIONS_AND_SUPPORT, CA_REGIONS_AND_SUPPORT, ITAR, AU_REGIONS_AND_US_SUPPORT, ASSURED_WORKLOADS_FOR_PARTNERS, ISR_REGIONS, ISR_REGIONS_AND_SUPPORT, CA_PROTECTED_B, IL5, IL2, JP_REGIONS_AND_SUPPORT, KSA_REGIONS_AND_SUPPORT_WITH_SOVEREIGNTY_CONTROLS, REGIONAL_CONTROLS, HEALTHCARE_AND_LIFE_SCIENCES_CONTROLS, HEALTHCARE_AND_LIFE_SCIENCES_CONTROLS_US_SUPPORT, IRS_1075 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#compliance_regime AssuredWorkloadsWorkload#compliance_regime}
        :param display_name: Required. The user-assigned display name of the Workload. When present it must be between 4 to 30 characters. Allowed characters are: lowercase and uppercase letters, numbers, hyphen, and spaces. Example: My Workload Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#display_name AssuredWorkloadsWorkload#display_name}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#location AssuredWorkloadsWorkload#location}
        :param organization: The organization for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#organization AssuredWorkloadsWorkload#organization}
        :param billing_account: Optional. Input only. The billing account used for the resources which are direct children of workload. This billing account is initially associated with the resources created as part of Workload creation. After the initial creation of these resources, the customer can change the assigned billing account. The resource name has the form ``billingAccounts/{billing_account_id}``. For example, ``billingAccounts/012345-567890-ABCDEF``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#billing_account AssuredWorkloadsWorkload#billing_account}
        :param enable_sovereign_controls: Optional. Indicates the sovereignty status of the given workload. Currently meant to be used by Europe/Canada customers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#enable_sovereign_controls AssuredWorkloadsWorkload#enable_sovereign_controls}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#id AssuredWorkloadsWorkload#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_settings: kms_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#kms_settings AssuredWorkloadsWorkload#kms_settings}
        :param labels: Optional. Labels applied to the workload. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field ``effective_labels`` for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#labels AssuredWorkloadsWorkload#labels}
        :param partner: Optional. Partner regime associated with this workload. Possible values: PARTNER_UNSPECIFIED, LOCAL_CONTROLS_BY_S3NS, SOVEREIGN_CONTROLS_BY_T_SYSTEMS, SOVEREIGN_CONTROLS_BY_SIA_MINSAIT, SOVEREIGN_CONTROLS_BY_PSN, SOVEREIGN_CONTROLS_BY_CNTXT, SOVEREIGN_CONTROLS_BY_CNTXT_NO_EKM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#partner AssuredWorkloadsWorkload#partner}
        :param partner_permissions: partner_permissions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#partner_permissions AssuredWorkloadsWorkload#partner_permissions}
        :param partner_services_billing_account: Optional. Input only. Billing account necessary for purchasing services from Sovereign Partners. This field is required for creating SIA/PSN/CNTXT partner workloads. The caller should have 'billing.resourceAssociations.create' IAM permission on this billing-account. The format of this string is billingAccounts/AAAAAA-BBBBBB-CCCCCC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#partner_services_billing_account AssuredWorkloadsWorkload#partner_services_billing_account}
        :param provisioned_resources_parent: Input only. The parent resource for the resources managed by this Assured Workload. May be either empty or a folder resource which is a child of the Workload parent. If not specified all resources are created under the parent organization. Format: folders/{folder_id} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#provisioned_resources_parent AssuredWorkloadsWorkload#provisioned_resources_parent}
        :param resource_settings: resource_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#resource_settings AssuredWorkloadsWorkload#resource_settings}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#timeouts AssuredWorkloadsWorkload#timeouts}
        :param violation_notifications_enabled: Optional. Indicates whether the e-mail notification for a violation is enabled for a workload. This value will be by default True, and if not present will be considered as true. This should only be updated via updateWorkload call. Any Changes to this field during the createWorkload call will not be honored. This will always be true while creating the workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#violation_notifications_enabled AssuredWorkloadsWorkload#violation_notifications_enabled}
        :param workload_options: workload_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#workload_options AssuredWorkloadsWorkload#workload_options}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b493891b361c29b35e36907c4ff5a79748c1159dadc1a19ddac4d7067810173)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AssuredWorkloadsWorkloadConfig(
            compliance_regime=compliance_regime,
            display_name=display_name,
            location=location,
            organization=organization,
            billing_account=billing_account,
            enable_sovereign_controls=enable_sovereign_controls,
            id=id,
            kms_settings=kms_settings,
            labels=labels,
            partner=partner,
            partner_permissions=partner_permissions,
            partner_services_billing_account=partner_services_billing_account,
            provisioned_resources_parent=provisioned_resources_parent,
            resource_settings=resource_settings,
            timeouts=timeouts,
            violation_notifications_enabled=violation_notifications_enabled,
            workload_options=workload_options,
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
        '''Generates CDKTF code for importing a AssuredWorkloadsWorkload resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AssuredWorkloadsWorkload to import.
        :param import_from_id: The id of the existing AssuredWorkloadsWorkload that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AssuredWorkloadsWorkload to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ad7ba81712ef99d07ca4eb45bf5132828895e3502b3117102fbc940966f35cc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putKmsSettings")
    def put_kms_settings(
        self,
        *,
        next_rotation_time: builtins.str,
        rotation_period: builtins.str,
    ) -> None:
        '''
        :param next_rotation_time: Required. Input only. Immutable. The time at which the Key Management Service will automatically create a new version of the crypto key and mark it as the primary. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#next_rotation_time AssuredWorkloadsWorkload#next_rotation_time}
        :param rotation_period: Required. Input only. Immutable. will be advanced by this period when the Key Management Service automatically rotates a key. Must be at least 24 hours and at most 876,000 hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#rotation_period AssuredWorkloadsWorkload#rotation_period}
        '''
        value = AssuredWorkloadsWorkloadKmsSettings(
            next_rotation_time=next_rotation_time, rotation_period=rotation_period
        )

        return typing.cast(None, jsii.invoke(self, "putKmsSettings", [value]))

    @jsii.member(jsii_name="putPartnerPermissions")
    def put_partner_permissions(
        self,
        *,
        assured_workloads_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        data_logs_viewer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        service_access_approver: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param assured_workloads_monitoring: Optional. Allow partner to view violation alerts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#assured_workloads_monitoring AssuredWorkloadsWorkload#assured_workloads_monitoring}
        :param data_logs_viewer: Allow the partner to view inspectability logs and monitoring violations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#data_logs_viewer AssuredWorkloadsWorkload#data_logs_viewer}
        :param service_access_approver: Optional. Allow partner to view access approval logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#service_access_approver AssuredWorkloadsWorkload#service_access_approver}
        '''
        value = AssuredWorkloadsWorkloadPartnerPermissions(
            assured_workloads_monitoring=assured_workloads_monitoring,
            data_logs_viewer=data_logs_viewer,
            service_access_approver=service_access_approver,
        )

        return typing.cast(None, jsii.invoke(self, "putPartnerPermissions", [value]))

    @jsii.member(jsii_name="putResourceSettings")
    def put_resource_settings(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AssuredWorkloadsWorkloadResourceSettings", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83dad5a03a19d31547e17625f47644bed50d5f1be2ed4c4d7e8749574ce171d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResourceSettings", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#create AssuredWorkloadsWorkload#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#delete AssuredWorkloadsWorkload#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#update AssuredWorkloadsWorkload#update}.
        '''
        value = AssuredWorkloadsWorkloadTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putWorkloadOptions")
    def put_workload_options(
        self,
        *,
        kaj_enrollment_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kaj_enrollment_type: Indicates type of KAJ enrollment for the workload. Currently, only specifiying KEY_ACCESS_TRANSPARENCY_OFF is implemented to not enroll in KAT-level KAJ enrollment for Regional Controls workloads. Possible values: KAJ_ENROLLMENT_TYPE_UNSPECIFIED, FULL_KAJ, EKM_ONLY, KEY_ACCESS_TRANSPARENCY_OFF Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#kaj_enrollment_type AssuredWorkloadsWorkload#kaj_enrollment_type}
        '''
        value = AssuredWorkloadsWorkloadWorkloadOptions(
            kaj_enrollment_type=kaj_enrollment_type
        )

        return typing.cast(None, jsii.invoke(self, "putWorkloadOptions", [value]))

    @jsii.member(jsii_name="resetBillingAccount")
    def reset_billing_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBillingAccount", []))

    @jsii.member(jsii_name="resetEnableSovereignControls")
    def reset_enable_sovereign_controls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableSovereignControls", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKmsSettings")
    def reset_kms_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsSettings", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetPartner")
    def reset_partner(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartner", []))

    @jsii.member(jsii_name="resetPartnerPermissions")
    def reset_partner_permissions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartnerPermissions", []))

    @jsii.member(jsii_name="resetPartnerServicesBillingAccount")
    def reset_partner_services_billing_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartnerServicesBillingAccount", []))

    @jsii.member(jsii_name="resetProvisionedResourcesParent")
    def reset_provisioned_resources_parent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvisionedResourcesParent", []))

    @jsii.member(jsii_name="resetResourceSettings")
    def reset_resource_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceSettings", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetViolationNotificationsEnabled")
    def reset_violation_notifications_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetViolationNotificationsEnabled", []))

    @jsii.member(jsii_name="resetWorkloadOptions")
    def reset_workload_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkloadOptions", []))

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
    @jsii.member(jsii_name="complianceStatus")
    def compliance_status(self) -> "AssuredWorkloadsWorkloadComplianceStatusList":
        return typing.cast("AssuredWorkloadsWorkloadComplianceStatusList", jsii.get(self, "complianceStatus"))

    @builtins.property
    @jsii.member(jsii_name="compliantButDisallowedServices")
    def compliant_but_disallowed_services(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "compliantButDisallowedServices"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="ekmProvisioningResponse")
    def ekm_provisioning_response(
        self,
    ) -> "AssuredWorkloadsWorkloadEkmProvisioningResponseList":
        return typing.cast("AssuredWorkloadsWorkloadEkmProvisioningResponseList", jsii.get(self, "ekmProvisioningResponse"))

    @builtins.property
    @jsii.member(jsii_name="kajEnrollmentState")
    def kaj_enrollment_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kajEnrollmentState"))

    @builtins.property
    @jsii.member(jsii_name="kmsSettings")
    def kms_settings(self) -> "AssuredWorkloadsWorkloadKmsSettingsOutputReference":
        return typing.cast("AssuredWorkloadsWorkloadKmsSettingsOutputReference", jsii.get(self, "kmsSettings"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="partnerPermissions")
    def partner_permissions(
        self,
    ) -> "AssuredWorkloadsWorkloadPartnerPermissionsOutputReference":
        return typing.cast("AssuredWorkloadsWorkloadPartnerPermissionsOutputReference", jsii.get(self, "partnerPermissions"))

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> "AssuredWorkloadsWorkloadResourcesList":
        return typing.cast("AssuredWorkloadsWorkloadResourcesList", jsii.get(self, "resources"))

    @builtins.property
    @jsii.member(jsii_name="resourceSettings")
    def resource_settings(self) -> "AssuredWorkloadsWorkloadResourceSettingsList":
        return typing.cast("AssuredWorkloadsWorkloadResourceSettingsList", jsii.get(self, "resourceSettings"))

    @builtins.property
    @jsii.member(jsii_name="saaEnrollmentResponse")
    def saa_enrollment_response(
        self,
    ) -> "AssuredWorkloadsWorkloadSaaEnrollmentResponseList":
        return typing.cast("AssuredWorkloadsWorkloadSaaEnrollmentResponseList", jsii.get(self, "saaEnrollmentResponse"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "AssuredWorkloadsWorkloadTimeoutsOutputReference":
        return typing.cast("AssuredWorkloadsWorkloadTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="workloadOptions")
    def workload_options(
        self,
    ) -> "AssuredWorkloadsWorkloadWorkloadOptionsOutputReference":
        return typing.cast("AssuredWorkloadsWorkloadWorkloadOptionsOutputReference", jsii.get(self, "workloadOptions"))

    @builtins.property
    @jsii.member(jsii_name="billingAccountInput")
    def billing_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "billingAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="complianceRegimeInput")
    def compliance_regime_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "complianceRegimeInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="enableSovereignControlsInput")
    def enable_sovereign_controls_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableSovereignControlsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsSettingsInput")
    def kms_settings_input(
        self,
    ) -> typing.Optional["AssuredWorkloadsWorkloadKmsSettings"]:
        return typing.cast(typing.Optional["AssuredWorkloadsWorkloadKmsSettings"], jsii.get(self, "kmsSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="organizationInput")
    def organization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationInput"))

    @builtins.property
    @jsii.member(jsii_name="partnerInput")
    def partner_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "partnerInput"))

    @builtins.property
    @jsii.member(jsii_name="partnerPermissionsInput")
    def partner_permissions_input(
        self,
    ) -> typing.Optional["AssuredWorkloadsWorkloadPartnerPermissions"]:
        return typing.cast(typing.Optional["AssuredWorkloadsWorkloadPartnerPermissions"], jsii.get(self, "partnerPermissionsInput"))

    @builtins.property
    @jsii.member(jsii_name="partnerServicesBillingAccountInput")
    def partner_services_billing_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "partnerServicesBillingAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="provisionedResourcesParentInput")
    def provisioned_resources_parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "provisionedResourcesParentInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceSettingsInput")
    def resource_settings_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AssuredWorkloadsWorkloadResourceSettings"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AssuredWorkloadsWorkloadResourceSettings"]]], jsii.get(self, "resourceSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AssuredWorkloadsWorkloadTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AssuredWorkloadsWorkloadTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="violationNotificationsEnabledInput")
    def violation_notifications_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "violationNotificationsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="workloadOptionsInput")
    def workload_options_input(
        self,
    ) -> typing.Optional["AssuredWorkloadsWorkloadWorkloadOptions"]:
        return typing.cast(typing.Optional["AssuredWorkloadsWorkloadWorkloadOptions"], jsii.get(self, "workloadOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="billingAccount")
    def billing_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "billingAccount"))

    @billing_account.setter
    def billing_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91e09f58058c104f9b316a303841400d9c786fddf59cb2285d9a29c0fb629767)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "billingAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="complianceRegime")
    def compliance_regime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "complianceRegime"))

    @compliance_regime.setter
    def compliance_regime(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7cd28d14ecf44aaefe723ab7471be5b241b013de9e624f5e610e3c6e4e87acd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "complianceRegime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dce6b9e98563d828504dc306b86d2ac950e2bf3ea07be3549fa3c0495a7ace7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableSovereignControls")
    def enable_sovereign_controls(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableSovereignControls"))

    @enable_sovereign_controls.setter
    def enable_sovereign_controls(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ebd5a3aac2ff4eb9aeeb956b90f573b1eba7d0910a6f96de3decd082ce90919)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableSovereignControls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4293f426d1938306a24553625b139ce8f048e3569c552b99417d0de5ae97b4b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa815911f4f561033664c5bbfcf6bca3583b4c15ad92c494cb432681999ca004)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4568c390f6fa9a0e4fd619635facbcc37ebd3d2466646784c888fb38fdeb725c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7a690d999a1141c7629bb4073f234d89a5475f838933e87ce3232afffddbf57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partner")
    def partner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "partner"))

    @partner.setter
    def partner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a41bc1084ca38a70446697dd3e918b60de9ea2481b0a93d0f9f2912b5a0afa44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partner", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partnerServicesBillingAccount")
    def partner_services_billing_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "partnerServicesBillingAccount"))

    @partner_services_billing_account.setter
    def partner_services_billing_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1394048e9a369ec618a8325e7e201b308958f070de77abc0422cc278d9d9d52e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partnerServicesBillingAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="provisionedResourcesParent")
    def provisioned_resources_parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "provisionedResourcesParent"))

    @provisioned_resources_parent.setter
    def provisioned_resources_parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b9cb4d5e0e344b669f32bb54aec62635c3be56c6a050e0078df215ab0d78fa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisionedResourcesParent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="violationNotificationsEnabled")
    def violation_notifications_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "violationNotificationsEnabled"))

    @violation_notifications_enabled.setter
    def violation_notifications_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cea346201ab60fdcf60d453449a18f0f2f50e49c1e2f51e293777931b85514ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "violationNotificationsEnabled", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.assuredWorkloadsWorkload.AssuredWorkloadsWorkloadComplianceStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class AssuredWorkloadsWorkloadComplianceStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssuredWorkloadsWorkloadComplianceStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AssuredWorkloadsWorkloadComplianceStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.assuredWorkloadsWorkload.AssuredWorkloadsWorkloadComplianceStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a26d67ebdb37554f9ccbf1364e752585a9eec49e5d43b2629b15d1778e97ace4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AssuredWorkloadsWorkloadComplianceStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7517506b80f8e15efc9a5ea5378afb5ceed8c99337d240134ed1962f21187ae2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AssuredWorkloadsWorkloadComplianceStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d67f1909a60ab4efed87c5a2acb8d502d8e787aeb1d35b9c263a492b383d97dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9943dc537b8bc077eb0d307696c2eea2a07f94204742ccdc6b52a5a5693d6f52)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e11c11e12c1888727622b80b839bf837954ac419e95c5532ec6768162feef2bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class AssuredWorkloadsWorkloadComplianceStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.assuredWorkloadsWorkload.AssuredWorkloadsWorkloadComplianceStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__78b506ceab12e514fd1814ef941fb32e2dd1cdbadb8de3c59fa5fd67de854f87)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="acknowledgedViolationCount")
    def acknowledged_violation_count(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "acknowledgedViolationCount"))

    @builtins.property
    @jsii.member(jsii_name="activeViolationCount")
    def active_violation_count(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "activeViolationCount"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AssuredWorkloadsWorkloadComplianceStatus]:
        return typing.cast(typing.Optional[AssuredWorkloadsWorkloadComplianceStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AssuredWorkloadsWorkloadComplianceStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66be60f9cd235002cf746a4f4943da66ba9b474c9e809b39ca9f37e8a46939e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.assuredWorkloadsWorkload.AssuredWorkloadsWorkloadConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "compliance_regime": "complianceRegime",
        "display_name": "displayName",
        "location": "location",
        "organization": "organization",
        "billing_account": "billingAccount",
        "enable_sovereign_controls": "enableSovereignControls",
        "id": "id",
        "kms_settings": "kmsSettings",
        "labels": "labels",
        "partner": "partner",
        "partner_permissions": "partnerPermissions",
        "partner_services_billing_account": "partnerServicesBillingAccount",
        "provisioned_resources_parent": "provisionedResourcesParent",
        "resource_settings": "resourceSettings",
        "timeouts": "timeouts",
        "violation_notifications_enabled": "violationNotificationsEnabled",
        "workload_options": "workloadOptions",
    },
)
class AssuredWorkloadsWorkloadConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        compliance_regime: builtins.str,
        display_name: builtins.str,
        location: builtins.str,
        organization: builtins.str,
        billing_account: typing.Optional[builtins.str] = None,
        enable_sovereign_controls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        kms_settings: typing.Optional[typing.Union["AssuredWorkloadsWorkloadKmsSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        partner: typing.Optional[builtins.str] = None,
        partner_permissions: typing.Optional[typing.Union["AssuredWorkloadsWorkloadPartnerPermissions", typing.Dict[builtins.str, typing.Any]]] = None,
        partner_services_billing_account: typing.Optional[builtins.str] = None,
        provisioned_resources_parent: typing.Optional[builtins.str] = None,
        resource_settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AssuredWorkloadsWorkloadResourceSettings", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["AssuredWorkloadsWorkloadTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        violation_notifications_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        workload_options: typing.Optional[typing.Union["AssuredWorkloadsWorkloadWorkloadOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param compliance_regime: Required. Immutable. Compliance Regime associated with this workload. Possible values: COMPLIANCE_REGIME_UNSPECIFIED, IL4, CJIS, FEDRAMP_HIGH, FEDRAMP_MODERATE, US_REGIONAL_ACCESS, HIPAA, HITRUST, EU_REGIONS_AND_SUPPORT, CA_REGIONS_AND_SUPPORT, ITAR, AU_REGIONS_AND_US_SUPPORT, ASSURED_WORKLOADS_FOR_PARTNERS, ISR_REGIONS, ISR_REGIONS_AND_SUPPORT, CA_PROTECTED_B, IL5, IL2, JP_REGIONS_AND_SUPPORT, KSA_REGIONS_AND_SUPPORT_WITH_SOVEREIGNTY_CONTROLS, REGIONAL_CONTROLS, HEALTHCARE_AND_LIFE_SCIENCES_CONTROLS, HEALTHCARE_AND_LIFE_SCIENCES_CONTROLS_US_SUPPORT, IRS_1075 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#compliance_regime AssuredWorkloadsWorkload#compliance_regime}
        :param display_name: Required. The user-assigned display name of the Workload. When present it must be between 4 to 30 characters. Allowed characters are: lowercase and uppercase letters, numbers, hyphen, and spaces. Example: My Workload Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#display_name AssuredWorkloadsWorkload#display_name}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#location AssuredWorkloadsWorkload#location}
        :param organization: The organization for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#organization AssuredWorkloadsWorkload#organization}
        :param billing_account: Optional. Input only. The billing account used for the resources which are direct children of workload. This billing account is initially associated with the resources created as part of Workload creation. After the initial creation of these resources, the customer can change the assigned billing account. The resource name has the form ``billingAccounts/{billing_account_id}``. For example, ``billingAccounts/012345-567890-ABCDEF``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#billing_account AssuredWorkloadsWorkload#billing_account}
        :param enable_sovereign_controls: Optional. Indicates the sovereignty status of the given workload. Currently meant to be used by Europe/Canada customers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#enable_sovereign_controls AssuredWorkloadsWorkload#enable_sovereign_controls}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#id AssuredWorkloadsWorkload#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_settings: kms_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#kms_settings AssuredWorkloadsWorkload#kms_settings}
        :param labels: Optional. Labels applied to the workload. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field ``effective_labels`` for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#labels AssuredWorkloadsWorkload#labels}
        :param partner: Optional. Partner regime associated with this workload. Possible values: PARTNER_UNSPECIFIED, LOCAL_CONTROLS_BY_S3NS, SOVEREIGN_CONTROLS_BY_T_SYSTEMS, SOVEREIGN_CONTROLS_BY_SIA_MINSAIT, SOVEREIGN_CONTROLS_BY_PSN, SOVEREIGN_CONTROLS_BY_CNTXT, SOVEREIGN_CONTROLS_BY_CNTXT_NO_EKM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#partner AssuredWorkloadsWorkload#partner}
        :param partner_permissions: partner_permissions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#partner_permissions AssuredWorkloadsWorkload#partner_permissions}
        :param partner_services_billing_account: Optional. Input only. Billing account necessary for purchasing services from Sovereign Partners. This field is required for creating SIA/PSN/CNTXT partner workloads. The caller should have 'billing.resourceAssociations.create' IAM permission on this billing-account. The format of this string is billingAccounts/AAAAAA-BBBBBB-CCCCCC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#partner_services_billing_account AssuredWorkloadsWorkload#partner_services_billing_account}
        :param provisioned_resources_parent: Input only. The parent resource for the resources managed by this Assured Workload. May be either empty or a folder resource which is a child of the Workload parent. If not specified all resources are created under the parent organization. Format: folders/{folder_id} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#provisioned_resources_parent AssuredWorkloadsWorkload#provisioned_resources_parent}
        :param resource_settings: resource_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#resource_settings AssuredWorkloadsWorkload#resource_settings}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#timeouts AssuredWorkloadsWorkload#timeouts}
        :param violation_notifications_enabled: Optional. Indicates whether the e-mail notification for a violation is enabled for a workload. This value will be by default True, and if not present will be considered as true. This should only be updated via updateWorkload call. Any Changes to this field during the createWorkload call will not be honored. This will always be true while creating the workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#violation_notifications_enabled AssuredWorkloadsWorkload#violation_notifications_enabled}
        :param workload_options: workload_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#workload_options AssuredWorkloadsWorkload#workload_options}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(kms_settings, dict):
            kms_settings = AssuredWorkloadsWorkloadKmsSettings(**kms_settings)
        if isinstance(partner_permissions, dict):
            partner_permissions = AssuredWorkloadsWorkloadPartnerPermissions(**partner_permissions)
        if isinstance(timeouts, dict):
            timeouts = AssuredWorkloadsWorkloadTimeouts(**timeouts)
        if isinstance(workload_options, dict):
            workload_options = AssuredWorkloadsWorkloadWorkloadOptions(**workload_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fb5f2cf44656f0ba7ed7252143086a63586c170e93e60e4111947d2a7995246)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument compliance_regime", value=compliance_regime, expected_type=type_hints["compliance_regime"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
            check_type(argname="argument billing_account", value=billing_account, expected_type=type_hints["billing_account"])
            check_type(argname="argument enable_sovereign_controls", value=enable_sovereign_controls, expected_type=type_hints["enable_sovereign_controls"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kms_settings", value=kms_settings, expected_type=type_hints["kms_settings"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument partner", value=partner, expected_type=type_hints["partner"])
            check_type(argname="argument partner_permissions", value=partner_permissions, expected_type=type_hints["partner_permissions"])
            check_type(argname="argument partner_services_billing_account", value=partner_services_billing_account, expected_type=type_hints["partner_services_billing_account"])
            check_type(argname="argument provisioned_resources_parent", value=provisioned_resources_parent, expected_type=type_hints["provisioned_resources_parent"])
            check_type(argname="argument resource_settings", value=resource_settings, expected_type=type_hints["resource_settings"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument violation_notifications_enabled", value=violation_notifications_enabled, expected_type=type_hints["violation_notifications_enabled"])
            check_type(argname="argument workload_options", value=workload_options, expected_type=type_hints["workload_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "compliance_regime": compliance_regime,
            "display_name": display_name,
            "location": location,
            "organization": organization,
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
        if billing_account is not None:
            self._values["billing_account"] = billing_account
        if enable_sovereign_controls is not None:
            self._values["enable_sovereign_controls"] = enable_sovereign_controls
        if id is not None:
            self._values["id"] = id
        if kms_settings is not None:
            self._values["kms_settings"] = kms_settings
        if labels is not None:
            self._values["labels"] = labels
        if partner is not None:
            self._values["partner"] = partner
        if partner_permissions is not None:
            self._values["partner_permissions"] = partner_permissions
        if partner_services_billing_account is not None:
            self._values["partner_services_billing_account"] = partner_services_billing_account
        if provisioned_resources_parent is not None:
            self._values["provisioned_resources_parent"] = provisioned_resources_parent
        if resource_settings is not None:
            self._values["resource_settings"] = resource_settings
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if violation_notifications_enabled is not None:
            self._values["violation_notifications_enabled"] = violation_notifications_enabled
        if workload_options is not None:
            self._values["workload_options"] = workload_options

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
    def compliance_regime(self) -> builtins.str:
        '''Required.

        Immutable. Compliance Regime associated with this workload. Possible values: COMPLIANCE_REGIME_UNSPECIFIED, IL4, CJIS, FEDRAMP_HIGH, FEDRAMP_MODERATE, US_REGIONAL_ACCESS, HIPAA, HITRUST, EU_REGIONS_AND_SUPPORT, CA_REGIONS_AND_SUPPORT, ITAR, AU_REGIONS_AND_US_SUPPORT, ASSURED_WORKLOADS_FOR_PARTNERS, ISR_REGIONS, ISR_REGIONS_AND_SUPPORT, CA_PROTECTED_B, IL5, IL2, JP_REGIONS_AND_SUPPORT, KSA_REGIONS_AND_SUPPORT_WITH_SOVEREIGNTY_CONTROLS, REGIONAL_CONTROLS, HEALTHCARE_AND_LIFE_SCIENCES_CONTROLS, HEALTHCARE_AND_LIFE_SCIENCES_CONTROLS_US_SUPPORT, IRS_1075

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#compliance_regime AssuredWorkloadsWorkload#compliance_regime}
        '''
        result = self._values.get("compliance_regime")
        assert result is not None, "Required property 'compliance_regime' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''Required.

        The user-assigned display name of the Workload. When present it must be between 4 to 30 characters. Allowed characters are: lowercase and uppercase letters, numbers, hyphen, and spaces. Example: My Workload

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#display_name AssuredWorkloadsWorkload#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#location AssuredWorkloadsWorkload#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def organization(self) -> builtins.str:
        '''The organization for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#organization AssuredWorkloadsWorkload#organization}
        '''
        result = self._values.get("organization")
        assert result is not None, "Required property 'organization' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def billing_account(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Input only. The billing account used for the resources which are direct children of workload. This billing account is initially associated with the resources created as part of Workload creation. After the initial creation of these resources, the customer can change the assigned billing account. The resource name has the form ``billingAccounts/{billing_account_id}``. For example, ``billingAccounts/012345-567890-ABCDEF``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#billing_account AssuredWorkloadsWorkload#billing_account}
        '''
        result = self._values.get("billing_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_sovereign_controls(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. Indicates the sovereignty status of the given workload. Currently meant to be used by Europe/Canada customers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#enable_sovereign_controls AssuredWorkloadsWorkload#enable_sovereign_controls}
        '''
        result = self._values.get("enable_sovereign_controls")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#id AssuredWorkloadsWorkload#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_settings(self) -> typing.Optional["AssuredWorkloadsWorkloadKmsSettings"]:
        '''kms_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#kms_settings AssuredWorkloadsWorkload#kms_settings}
        '''
        result = self._values.get("kms_settings")
        return typing.cast(typing.Optional["AssuredWorkloadsWorkloadKmsSettings"], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional. Labels applied to the workload.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field ``effective_labels`` for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#labels AssuredWorkloadsWorkload#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def partner(self) -> typing.Optional[builtins.str]:
        '''Optional. Partner regime associated with this workload. Possible values: PARTNER_UNSPECIFIED, LOCAL_CONTROLS_BY_S3NS, SOVEREIGN_CONTROLS_BY_T_SYSTEMS, SOVEREIGN_CONTROLS_BY_SIA_MINSAIT, SOVEREIGN_CONTROLS_BY_PSN, SOVEREIGN_CONTROLS_BY_CNTXT, SOVEREIGN_CONTROLS_BY_CNTXT_NO_EKM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#partner AssuredWorkloadsWorkload#partner}
        '''
        result = self._values.get("partner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def partner_permissions(
        self,
    ) -> typing.Optional["AssuredWorkloadsWorkloadPartnerPermissions"]:
        '''partner_permissions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#partner_permissions AssuredWorkloadsWorkload#partner_permissions}
        '''
        result = self._values.get("partner_permissions")
        return typing.cast(typing.Optional["AssuredWorkloadsWorkloadPartnerPermissions"], result)

    @builtins.property
    def partner_services_billing_account(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Input only. Billing account necessary for purchasing services from Sovereign Partners. This field is required for creating SIA/PSN/CNTXT partner workloads. The caller should have 'billing.resourceAssociations.create' IAM permission on this billing-account. The format of this string is billingAccounts/AAAAAA-BBBBBB-CCCCCC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#partner_services_billing_account AssuredWorkloadsWorkload#partner_services_billing_account}
        '''
        result = self._values.get("partner_services_billing_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provisioned_resources_parent(self) -> typing.Optional[builtins.str]:
        '''Input only.

        The parent resource for the resources managed by this Assured Workload. May be either empty or a folder resource which is a child of the Workload parent. If not specified all resources are created under the parent organization. Format: folders/{folder_id}

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#provisioned_resources_parent AssuredWorkloadsWorkload#provisioned_resources_parent}
        '''
        result = self._values.get("provisioned_resources_parent")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_settings(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AssuredWorkloadsWorkloadResourceSettings"]]]:
        '''resource_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#resource_settings AssuredWorkloadsWorkload#resource_settings}
        '''
        result = self._values.get("resource_settings")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AssuredWorkloadsWorkloadResourceSettings"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["AssuredWorkloadsWorkloadTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#timeouts AssuredWorkloadsWorkload#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["AssuredWorkloadsWorkloadTimeouts"], result)

    @builtins.property
    def violation_notifications_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        Indicates whether the e-mail notification for a violation is enabled for a workload. This value will be by default True, and if not present will be considered as true. This should only be updated via updateWorkload call. Any Changes to this field during the createWorkload call will not be honored. This will always be true while creating the workload.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#violation_notifications_enabled AssuredWorkloadsWorkload#violation_notifications_enabled}
        '''
        result = self._values.get("violation_notifications_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def workload_options(
        self,
    ) -> typing.Optional["AssuredWorkloadsWorkloadWorkloadOptions"]:
        '''workload_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#workload_options AssuredWorkloadsWorkload#workload_options}
        '''
        result = self._values.get("workload_options")
        return typing.cast(typing.Optional["AssuredWorkloadsWorkloadWorkloadOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssuredWorkloadsWorkloadConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.assuredWorkloadsWorkload.AssuredWorkloadsWorkloadEkmProvisioningResponse",
    jsii_struct_bases=[],
    name_mapping={},
)
class AssuredWorkloadsWorkloadEkmProvisioningResponse:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssuredWorkloadsWorkloadEkmProvisioningResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AssuredWorkloadsWorkloadEkmProvisioningResponseList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.assuredWorkloadsWorkload.AssuredWorkloadsWorkloadEkmProvisioningResponseList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b898b65b23972f826abdae145e8c02c60072cf1d696d6256f671f306c62f2c01)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AssuredWorkloadsWorkloadEkmProvisioningResponseOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd2ece3d2a3069c4b1e47d2feb1eba79dfdfebcdf5c3c9b73d7ef347ba399d24)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AssuredWorkloadsWorkloadEkmProvisioningResponseOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b1cfe7a35af479f10fbae419dc224be9c54a80156388253d58e9a6be92367a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9884904f57a5c9c76e1a1f092b224b7789c5cc5c801358e9cef37b5217a36c7a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__901a8e28dda0779a6cc5dd8c3f8fcea169b7e72efa71e6305a150cc9d9b64318)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class AssuredWorkloadsWorkloadEkmProvisioningResponseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.assuredWorkloadsWorkload.AssuredWorkloadsWorkloadEkmProvisioningResponseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd7f295df0aca2fe90565cb82af2ec9e71cc1d97a7da05949dbf70fcc0c12713)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="ekmProvisioningErrorDomain")
    def ekm_provisioning_error_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ekmProvisioningErrorDomain"))

    @builtins.property
    @jsii.member(jsii_name="ekmProvisioningErrorMapping")
    def ekm_provisioning_error_mapping(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ekmProvisioningErrorMapping"))

    @builtins.property
    @jsii.member(jsii_name="ekmProvisioningState")
    def ekm_provisioning_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ekmProvisioningState"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AssuredWorkloadsWorkloadEkmProvisioningResponse]:
        return typing.cast(typing.Optional[AssuredWorkloadsWorkloadEkmProvisioningResponse], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AssuredWorkloadsWorkloadEkmProvisioningResponse],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eb0fdc0f277ad0b0155f037e0add156b407528fd53c2121bc310852c95f6458)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.assuredWorkloadsWorkload.AssuredWorkloadsWorkloadKmsSettings",
    jsii_struct_bases=[],
    name_mapping={
        "next_rotation_time": "nextRotationTime",
        "rotation_period": "rotationPeriod",
    },
)
class AssuredWorkloadsWorkloadKmsSettings:
    def __init__(
        self,
        *,
        next_rotation_time: builtins.str,
        rotation_period: builtins.str,
    ) -> None:
        '''
        :param next_rotation_time: Required. Input only. Immutable. The time at which the Key Management Service will automatically create a new version of the crypto key and mark it as the primary. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#next_rotation_time AssuredWorkloadsWorkload#next_rotation_time}
        :param rotation_period: Required. Input only. Immutable. will be advanced by this period when the Key Management Service automatically rotates a key. Must be at least 24 hours and at most 876,000 hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#rotation_period AssuredWorkloadsWorkload#rotation_period}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75ead2659dc228ffba2affa06b30430535376b5a77237f66bf1244bcebcedc3a)
            check_type(argname="argument next_rotation_time", value=next_rotation_time, expected_type=type_hints["next_rotation_time"])
            check_type(argname="argument rotation_period", value=rotation_period, expected_type=type_hints["rotation_period"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "next_rotation_time": next_rotation_time,
            "rotation_period": rotation_period,
        }

    @builtins.property
    def next_rotation_time(self) -> builtins.str:
        '''Required.

        Input only. Immutable. The time at which the Key Management Service will automatically create a new version of the crypto key and mark it as the primary.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#next_rotation_time AssuredWorkloadsWorkload#next_rotation_time}
        '''
        result = self._values.get("next_rotation_time")
        assert result is not None, "Required property 'next_rotation_time' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rotation_period(self) -> builtins.str:
        '''Required.

        Input only. Immutable. will be advanced by this period when the Key Management Service automatically rotates a key. Must be at least 24 hours and at most 876,000 hours.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#rotation_period AssuredWorkloadsWorkload#rotation_period}
        '''
        result = self._values.get("rotation_period")
        assert result is not None, "Required property 'rotation_period' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssuredWorkloadsWorkloadKmsSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AssuredWorkloadsWorkloadKmsSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.assuredWorkloadsWorkload.AssuredWorkloadsWorkloadKmsSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c211879aac5debac51c4cc9a089cc9cd2266065dc0aa38fd459657f5551297c3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="nextRotationTimeInput")
    def next_rotation_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nextRotationTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="rotationPeriodInput")
    def rotation_period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rotationPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="nextRotationTime")
    def next_rotation_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextRotationTime"))

    @next_rotation_time.setter
    def next_rotation_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7916674322b3d89aabeeea448108a6bbd41e16bcc3f77664610461001be05b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nextRotationTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rotationPeriod")
    def rotation_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rotationPeriod"))

    @rotation_period.setter
    def rotation_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2bf75bd679c6377cc414b7ec1d30fbab8aa7b2858f2f461af8301fdcf28bb8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rotationPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AssuredWorkloadsWorkloadKmsSettings]:
        return typing.cast(typing.Optional[AssuredWorkloadsWorkloadKmsSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AssuredWorkloadsWorkloadKmsSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f11fc118f46be1cc764988453d764daa6e7ba2c709cde62f83a34c17093b32e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.assuredWorkloadsWorkload.AssuredWorkloadsWorkloadPartnerPermissions",
    jsii_struct_bases=[],
    name_mapping={
        "assured_workloads_monitoring": "assuredWorkloadsMonitoring",
        "data_logs_viewer": "dataLogsViewer",
        "service_access_approver": "serviceAccessApprover",
    },
)
class AssuredWorkloadsWorkloadPartnerPermissions:
    def __init__(
        self,
        *,
        assured_workloads_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        data_logs_viewer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        service_access_approver: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param assured_workloads_monitoring: Optional. Allow partner to view violation alerts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#assured_workloads_monitoring AssuredWorkloadsWorkload#assured_workloads_monitoring}
        :param data_logs_viewer: Allow the partner to view inspectability logs and monitoring violations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#data_logs_viewer AssuredWorkloadsWorkload#data_logs_viewer}
        :param service_access_approver: Optional. Allow partner to view access approval logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#service_access_approver AssuredWorkloadsWorkload#service_access_approver}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26fecf633db461cf2f69e6873c311207de1b63621d06c044cfbf801ef94100d6)
            check_type(argname="argument assured_workloads_monitoring", value=assured_workloads_monitoring, expected_type=type_hints["assured_workloads_monitoring"])
            check_type(argname="argument data_logs_viewer", value=data_logs_viewer, expected_type=type_hints["data_logs_viewer"])
            check_type(argname="argument service_access_approver", value=service_access_approver, expected_type=type_hints["service_access_approver"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if assured_workloads_monitoring is not None:
            self._values["assured_workloads_monitoring"] = assured_workloads_monitoring
        if data_logs_viewer is not None:
            self._values["data_logs_viewer"] = data_logs_viewer
        if service_access_approver is not None:
            self._values["service_access_approver"] = service_access_approver

    @builtins.property
    def assured_workloads_monitoring(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. Allow partner to view violation alerts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#assured_workloads_monitoring AssuredWorkloadsWorkload#assured_workloads_monitoring}
        '''
        result = self._values.get("assured_workloads_monitoring")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def data_logs_viewer(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allow the partner to view inspectability logs and monitoring violations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#data_logs_viewer AssuredWorkloadsWorkload#data_logs_viewer}
        '''
        result = self._values.get("data_logs_viewer")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def service_access_approver(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. Allow partner to view access approval logs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#service_access_approver AssuredWorkloadsWorkload#service_access_approver}
        '''
        result = self._values.get("service_access_approver")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssuredWorkloadsWorkloadPartnerPermissions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AssuredWorkloadsWorkloadPartnerPermissionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.assuredWorkloadsWorkload.AssuredWorkloadsWorkloadPartnerPermissionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2d967c5aa74c1b49bc968b3f2357d32490d1126164b37f6d386e96e5025973c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAssuredWorkloadsMonitoring")
    def reset_assured_workloads_monitoring(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssuredWorkloadsMonitoring", []))

    @jsii.member(jsii_name="resetDataLogsViewer")
    def reset_data_logs_viewer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataLogsViewer", []))

    @jsii.member(jsii_name="resetServiceAccessApprover")
    def reset_service_access_approver(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccessApprover", []))

    @builtins.property
    @jsii.member(jsii_name="assuredWorkloadsMonitoringInput")
    def assured_workloads_monitoring_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "assuredWorkloadsMonitoringInput"))

    @builtins.property
    @jsii.member(jsii_name="dataLogsViewerInput")
    def data_logs_viewer_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dataLogsViewerInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccessApproverInput")
    def service_access_approver_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "serviceAccessApproverInput"))

    @builtins.property
    @jsii.member(jsii_name="assuredWorkloadsMonitoring")
    def assured_workloads_monitoring(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "assuredWorkloadsMonitoring"))

    @assured_workloads_monitoring.setter
    def assured_workloads_monitoring(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d8cfab3cd67b8adba0573197ed2efa29295d2a44dd1f1ca66795827a4eace79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assuredWorkloadsMonitoring", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataLogsViewer")
    def data_logs_viewer(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dataLogsViewer"))

    @data_logs_viewer.setter
    def data_logs_viewer(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2f632bd62672674a6f2d49d3ab41ad2b70e5581a0acb30b81f727c327f60f59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataLogsViewer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccessApprover")
    def service_access_approver(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "serviceAccessApprover"))

    @service_access_approver.setter
    def service_access_approver(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58bbe12fb4485ca6dabd7c1b469dfd1c021ade3ec3585807adc3f05a211cdb9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccessApprover", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AssuredWorkloadsWorkloadPartnerPermissions]:
        return typing.cast(typing.Optional[AssuredWorkloadsWorkloadPartnerPermissions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AssuredWorkloadsWorkloadPartnerPermissions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74e6d73aff808f1d08e382270713c10a95e7dd03a73126eec517ba061a836078)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.assuredWorkloadsWorkload.AssuredWorkloadsWorkloadResourceSettings",
    jsii_struct_bases=[],
    name_mapping={
        "display_name": "displayName",
        "resource_id": "resourceId",
        "resource_type": "resourceType",
    },
)
class AssuredWorkloadsWorkloadResourceSettings:
    def __init__(
        self,
        *,
        display_name: typing.Optional[builtins.str] = None,
        resource_id: typing.Optional[builtins.str] = None,
        resource_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param display_name: User-assigned resource display name. If not empty it will be used to create a resource with the specified name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#display_name AssuredWorkloadsWorkload#display_name}
        :param resource_id: Resource identifier. For a project this represents projectId. If the project is already taken, the workload creation will fail. For KeyRing, this represents the keyring_id. For a folder, don't set this value as folder_id is assigned by Google. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#resource_id AssuredWorkloadsWorkload#resource_id}
        :param resource_type: Indicates the type of resource. This field should be specified to correspond the id to the right project type (CONSUMER_PROJECT or ENCRYPTION_KEYS_PROJECT) Possible values: RESOURCE_TYPE_UNSPECIFIED, CONSUMER_PROJECT, ENCRYPTION_KEYS_PROJECT, KEYRING, CONSUMER_FOLDER Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#resource_type AssuredWorkloadsWorkload#resource_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29333448b387f8833a7a625af9e0ba2e99f3780ce71bd5363f3bddadb6f24f20)
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if display_name is not None:
            self._values["display_name"] = display_name
        if resource_id is not None:
            self._values["resource_id"] = resource_id
        if resource_type is not None:
            self._values["resource_type"] = resource_type

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''User-assigned resource display name. If not empty it will be used to create a resource with the specified name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#display_name AssuredWorkloadsWorkload#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_id(self) -> typing.Optional[builtins.str]:
        '''Resource identifier.

        For a project this represents projectId. If the project is already taken, the workload creation will fail. For KeyRing, this represents the keyring_id. For a folder, don't set this value as folder_id is assigned by Google.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#resource_id AssuredWorkloadsWorkload#resource_id}
        '''
        result = self._values.get("resource_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_type(self) -> typing.Optional[builtins.str]:
        '''Indicates the type of resource.

        This field should be specified to correspond the id to the right project type (CONSUMER_PROJECT or ENCRYPTION_KEYS_PROJECT) Possible values: RESOURCE_TYPE_UNSPECIFIED, CONSUMER_PROJECT, ENCRYPTION_KEYS_PROJECT, KEYRING, CONSUMER_FOLDER

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#resource_type AssuredWorkloadsWorkload#resource_type}
        '''
        result = self._values.get("resource_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssuredWorkloadsWorkloadResourceSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AssuredWorkloadsWorkloadResourceSettingsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.assuredWorkloadsWorkload.AssuredWorkloadsWorkloadResourceSettingsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2edc8d6fdd754d8bc4f4c2635a7f3f3869f1e624c211901446d63db016b83a57)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AssuredWorkloadsWorkloadResourceSettingsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fba53c2cdb04a97d675b7e880dce13ca44948e33e73ce72de3b347ad572cf79b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AssuredWorkloadsWorkloadResourceSettingsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e188fa8d29a28a543aa40bee88a49acea719e6c50b18665a02a4ac0f0a6f9b61)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c818c3b6fdf2da85e1a132ad51574849ef76e8fc8735a15e318b3e2b02bcca45)
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
            type_hints = typing.get_type_hints(_typecheckingstub__803f31ec5ff4f87a6c372627b089aeeb72068c33c586faf73890909172d28238)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AssuredWorkloadsWorkloadResourceSettings]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AssuredWorkloadsWorkloadResourceSettings]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AssuredWorkloadsWorkloadResourceSettings]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bd66bcd56042aa8a5a99cac4620c2325a6996d774f35a851333d1c502ef36ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AssuredWorkloadsWorkloadResourceSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.assuredWorkloadsWorkload.AssuredWorkloadsWorkloadResourceSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__87a2e1ebae6a9567e1fd4ad009b5286b82d7edaf2f98fd87b761dcd7e1a7f2bf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetResourceId")
    def reset_resource_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceId", []))

    @jsii.member(jsii_name="resetResourceType")
    def reset_resource_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceType", []))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceIdInput")
    def resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypeInput")
    def resource_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fd92ef61a405749cb260c839837f3c971025fd97245082864cdc11497b1cd0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceId"))

    @resource_id.setter
    def resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bae7ae0559f4a97238635f2500c8b00f5bcead1f6611ce817bf2ad93a1131378)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceType"))

    @resource_type.setter
    def resource_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be473f7c8c8cf502ab2b3ab6f8cbfbf6c05247ecad6dc51e024c443349ebe529)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AssuredWorkloadsWorkloadResourceSettings]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AssuredWorkloadsWorkloadResourceSettings]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AssuredWorkloadsWorkloadResourceSettings]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a591fbe0233be9446c69c309d6e538524947d03eccd61c3428b1926572725bdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.assuredWorkloadsWorkload.AssuredWorkloadsWorkloadResources",
    jsii_struct_bases=[],
    name_mapping={},
)
class AssuredWorkloadsWorkloadResources:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssuredWorkloadsWorkloadResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AssuredWorkloadsWorkloadResourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.assuredWorkloadsWorkload.AssuredWorkloadsWorkloadResourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__69700436ae37bbe694a65d427a67e721e89138c693dfbde9606715f67f60090e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AssuredWorkloadsWorkloadResourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f65710f1077283170d34d842d12b5e47e838dd528db015ec76501cc9be9cb62)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AssuredWorkloadsWorkloadResourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b875e254b6a5060e6cfdb7d23f2ca93d4dc47af45e618eefd5baaf869c37fca2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f921a8ea2cfef72109c34288233587199a5140ff50a27c7e3a63e6f955e46ef4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__799c3e12b4ba4057e033a1ed307dbca2373d55b52e68bbb31f6081ad69626294)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class AssuredWorkloadsWorkloadResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.assuredWorkloadsWorkload.AssuredWorkloadsWorkloadResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2a1969256111c9a97ab8800460094430d2307a0ea290fc0a8439d71d334b03e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "resourceId"))

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceType"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AssuredWorkloadsWorkloadResources]:
        return typing.cast(typing.Optional[AssuredWorkloadsWorkloadResources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AssuredWorkloadsWorkloadResources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e666d80ca96373237959583ade263e6f513672dcdb007e09044975e5c535af5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.assuredWorkloadsWorkload.AssuredWorkloadsWorkloadSaaEnrollmentResponse",
    jsii_struct_bases=[],
    name_mapping={},
)
class AssuredWorkloadsWorkloadSaaEnrollmentResponse:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssuredWorkloadsWorkloadSaaEnrollmentResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AssuredWorkloadsWorkloadSaaEnrollmentResponseList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.assuredWorkloadsWorkload.AssuredWorkloadsWorkloadSaaEnrollmentResponseList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a88020acac07faec14c878dc04315c8a6df1631ed92933dbe9a4461c0bed437e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AssuredWorkloadsWorkloadSaaEnrollmentResponseOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd858a950d26e2c3e352f731e24615cf545a216683460fe122b9a048af7f11f1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AssuredWorkloadsWorkloadSaaEnrollmentResponseOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9619f5b244c29cc3dc79e35fc124984b2f0da7539140c986d3cb199bdc0cf5f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fbb782c763af60ec1e672b9f415e113dbadec399a7977b227e2c66eab74055c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__faf3428e82b734dc4072b4c4e7a813536a31f9623b0d2667cf60c7be901ca60e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class AssuredWorkloadsWorkloadSaaEnrollmentResponseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.assuredWorkloadsWorkload.AssuredWorkloadsWorkloadSaaEnrollmentResponseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0a5c222dabddb29e8af6825351c18517cfd7f97b3b92f0e05a4cc368a36b904)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="setupErrors")
    def setup_errors(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "setupErrors"))

    @builtins.property
    @jsii.member(jsii_name="setupStatus")
    def setup_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "setupStatus"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AssuredWorkloadsWorkloadSaaEnrollmentResponse]:
        return typing.cast(typing.Optional[AssuredWorkloadsWorkloadSaaEnrollmentResponse], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AssuredWorkloadsWorkloadSaaEnrollmentResponse],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42a2f490c8e26f5e61b6227b07b69b43efad11288c516eb14be9188821035789)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.assuredWorkloadsWorkload.AssuredWorkloadsWorkloadTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class AssuredWorkloadsWorkloadTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#create AssuredWorkloadsWorkload#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#delete AssuredWorkloadsWorkload#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#update AssuredWorkloadsWorkload#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__083c7c18b70baf6a2460ae5b777763b4d9ba4c82eaf9cdf06b1d2cfe22010430)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#create AssuredWorkloadsWorkload#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#delete AssuredWorkloadsWorkload#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#update AssuredWorkloadsWorkload#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssuredWorkloadsWorkloadTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AssuredWorkloadsWorkloadTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.assuredWorkloadsWorkload.AssuredWorkloadsWorkloadTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e49b66e8e95fe2439af51ebade52eec0bfa3c4553cbbc64de9f2310e3f9e1cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e21dbe3316f98984ccc3909d4c41c83e60ee0aeb0b0ca06c48b6e2401bcf38fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a19520efc4598e5e333248b003478924ff5850cd9806f834da8539f5f8613b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00574888656c2b2d62396856465237d0f8dc55985684aaa25da36677ca9ae7e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AssuredWorkloadsWorkloadTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AssuredWorkloadsWorkloadTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AssuredWorkloadsWorkloadTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36fb9cac6faa1a4649d65813c7eaca4665445f14079811a4b30309f51a855da6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.assuredWorkloadsWorkload.AssuredWorkloadsWorkloadWorkloadOptions",
    jsii_struct_bases=[],
    name_mapping={"kaj_enrollment_type": "kajEnrollmentType"},
)
class AssuredWorkloadsWorkloadWorkloadOptions:
    def __init__(
        self,
        *,
        kaj_enrollment_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kaj_enrollment_type: Indicates type of KAJ enrollment for the workload. Currently, only specifiying KEY_ACCESS_TRANSPARENCY_OFF is implemented to not enroll in KAT-level KAJ enrollment for Regional Controls workloads. Possible values: KAJ_ENROLLMENT_TYPE_UNSPECIFIED, FULL_KAJ, EKM_ONLY, KEY_ACCESS_TRANSPARENCY_OFF Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#kaj_enrollment_type AssuredWorkloadsWorkload#kaj_enrollment_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72593d30b81559fb8e14130a83f762dd5be1c04a0cabdb5f2f8c4bb7e419e899)
            check_type(argname="argument kaj_enrollment_type", value=kaj_enrollment_type, expected_type=type_hints["kaj_enrollment_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kaj_enrollment_type is not None:
            self._values["kaj_enrollment_type"] = kaj_enrollment_type

    @builtins.property
    def kaj_enrollment_type(self) -> typing.Optional[builtins.str]:
        '''Indicates type of KAJ enrollment for the workload.

        Currently, only specifiying KEY_ACCESS_TRANSPARENCY_OFF is implemented to not enroll in KAT-level KAJ enrollment for Regional Controls workloads. Possible values: KAJ_ENROLLMENT_TYPE_UNSPECIFIED, FULL_KAJ, EKM_ONLY, KEY_ACCESS_TRANSPARENCY_OFF

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/assured_workloads_workload#kaj_enrollment_type AssuredWorkloadsWorkload#kaj_enrollment_type}
        '''
        result = self._values.get("kaj_enrollment_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssuredWorkloadsWorkloadWorkloadOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AssuredWorkloadsWorkloadWorkloadOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.assuredWorkloadsWorkload.AssuredWorkloadsWorkloadWorkloadOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb861d0855e15b0a09f5be130b748afe06438b3af49566bc6d4ee5a7778ef054)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKajEnrollmentType")
    def reset_kaj_enrollment_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKajEnrollmentType", []))

    @builtins.property
    @jsii.member(jsii_name="kajEnrollmentTypeInput")
    def kaj_enrollment_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kajEnrollmentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="kajEnrollmentType")
    def kaj_enrollment_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kajEnrollmentType"))

    @kaj_enrollment_type.setter
    def kaj_enrollment_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f493286e56aef64dac157adeddf944593c0e6e7f6055e646c16bcdc7054b2429)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kajEnrollmentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AssuredWorkloadsWorkloadWorkloadOptions]:
        return typing.cast(typing.Optional[AssuredWorkloadsWorkloadWorkloadOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AssuredWorkloadsWorkloadWorkloadOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18edeef89c52b2c72ce9a1669840fef75543a6ae917843430d1f1a5ba673fe4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AssuredWorkloadsWorkload",
    "AssuredWorkloadsWorkloadComplianceStatus",
    "AssuredWorkloadsWorkloadComplianceStatusList",
    "AssuredWorkloadsWorkloadComplianceStatusOutputReference",
    "AssuredWorkloadsWorkloadConfig",
    "AssuredWorkloadsWorkloadEkmProvisioningResponse",
    "AssuredWorkloadsWorkloadEkmProvisioningResponseList",
    "AssuredWorkloadsWorkloadEkmProvisioningResponseOutputReference",
    "AssuredWorkloadsWorkloadKmsSettings",
    "AssuredWorkloadsWorkloadKmsSettingsOutputReference",
    "AssuredWorkloadsWorkloadPartnerPermissions",
    "AssuredWorkloadsWorkloadPartnerPermissionsOutputReference",
    "AssuredWorkloadsWorkloadResourceSettings",
    "AssuredWorkloadsWorkloadResourceSettingsList",
    "AssuredWorkloadsWorkloadResourceSettingsOutputReference",
    "AssuredWorkloadsWorkloadResources",
    "AssuredWorkloadsWorkloadResourcesList",
    "AssuredWorkloadsWorkloadResourcesOutputReference",
    "AssuredWorkloadsWorkloadSaaEnrollmentResponse",
    "AssuredWorkloadsWorkloadSaaEnrollmentResponseList",
    "AssuredWorkloadsWorkloadSaaEnrollmentResponseOutputReference",
    "AssuredWorkloadsWorkloadTimeouts",
    "AssuredWorkloadsWorkloadTimeoutsOutputReference",
    "AssuredWorkloadsWorkloadWorkloadOptions",
    "AssuredWorkloadsWorkloadWorkloadOptionsOutputReference",
]

publication.publish()

def _typecheckingstub__7b493891b361c29b35e36907c4ff5a79748c1159dadc1a19ddac4d7067810173(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    compliance_regime: builtins.str,
    display_name: builtins.str,
    location: builtins.str,
    organization: builtins.str,
    billing_account: typing.Optional[builtins.str] = None,
    enable_sovereign_controls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    kms_settings: typing.Optional[typing.Union[AssuredWorkloadsWorkloadKmsSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    partner: typing.Optional[builtins.str] = None,
    partner_permissions: typing.Optional[typing.Union[AssuredWorkloadsWorkloadPartnerPermissions, typing.Dict[builtins.str, typing.Any]]] = None,
    partner_services_billing_account: typing.Optional[builtins.str] = None,
    provisioned_resources_parent: typing.Optional[builtins.str] = None,
    resource_settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AssuredWorkloadsWorkloadResourceSettings, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[AssuredWorkloadsWorkloadTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    violation_notifications_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    workload_options: typing.Optional[typing.Union[AssuredWorkloadsWorkloadWorkloadOptions, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__4ad7ba81712ef99d07ca4eb45bf5132828895e3502b3117102fbc940966f35cc(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83dad5a03a19d31547e17625f47644bed50d5f1be2ed4c4d7e8749574ce171d6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AssuredWorkloadsWorkloadResourceSettings, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91e09f58058c104f9b316a303841400d9c786fddf59cb2285d9a29c0fb629767(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7cd28d14ecf44aaefe723ab7471be5b241b013de9e624f5e610e3c6e4e87acd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dce6b9e98563d828504dc306b86d2ac950e2bf3ea07be3549fa3c0495a7ace7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ebd5a3aac2ff4eb9aeeb956b90f573b1eba7d0910a6f96de3decd082ce90919(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4293f426d1938306a24553625b139ce8f048e3569c552b99417d0de5ae97b4b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa815911f4f561033664c5bbfcf6bca3583b4c15ad92c494cb432681999ca004(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4568c390f6fa9a0e4fd619635facbcc37ebd3d2466646784c888fb38fdeb725c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7a690d999a1141c7629bb4073f234d89a5475f838933e87ce3232afffddbf57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a41bc1084ca38a70446697dd3e918b60de9ea2481b0a93d0f9f2912b5a0afa44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1394048e9a369ec618a8325e7e201b308958f070de77abc0422cc278d9d9d52e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b9cb4d5e0e344b669f32bb54aec62635c3be56c6a050e0078df215ab0d78fa7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cea346201ab60fdcf60d453449a18f0f2f50e49c1e2f51e293777931b85514ff(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a26d67ebdb37554f9ccbf1364e752585a9eec49e5d43b2629b15d1778e97ace4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7517506b80f8e15efc9a5ea5378afb5ceed8c99337d240134ed1962f21187ae2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d67f1909a60ab4efed87c5a2acb8d502d8e787aeb1d35b9c263a492b383d97dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9943dc537b8bc077eb0d307696c2eea2a07f94204742ccdc6b52a5a5693d6f52(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e11c11e12c1888727622b80b839bf837954ac419e95c5532ec6768162feef2bd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78b506ceab12e514fd1814ef941fb32e2dd1cdbadb8de3c59fa5fd67de854f87(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66be60f9cd235002cf746a4f4943da66ba9b474c9e809b39ca9f37e8a46939e8(
    value: typing.Optional[AssuredWorkloadsWorkloadComplianceStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fb5f2cf44656f0ba7ed7252143086a63586c170e93e60e4111947d2a7995246(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    compliance_regime: builtins.str,
    display_name: builtins.str,
    location: builtins.str,
    organization: builtins.str,
    billing_account: typing.Optional[builtins.str] = None,
    enable_sovereign_controls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    kms_settings: typing.Optional[typing.Union[AssuredWorkloadsWorkloadKmsSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    partner: typing.Optional[builtins.str] = None,
    partner_permissions: typing.Optional[typing.Union[AssuredWorkloadsWorkloadPartnerPermissions, typing.Dict[builtins.str, typing.Any]]] = None,
    partner_services_billing_account: typing.Optional[builtins.str] = None,
    provisioned_resources_parent: typing.Optional[builtins.str] = None,
    resource_settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AssuredWorkloadsWorkloadResourceSettings, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[AssuredWorkloadsWorkloadTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    violation_notifications_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    workload_options: typing.Optional[typing.Union[AssuredWorkloadsWorkloadWorkloadOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b898b65b23972f826abdae145e8c02c60072cf1d696d6256f671f306c62f2c01(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd2ece3d2a3069c4b1e47d2feb1eba79dfdfebcdf5c3c9b73d7ef347ba399d24(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b1cfe7a35af479f10fbae419dc224be9c54a80156388253d58e9a6be92367a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9884904f57a5c9c76e1a1f092b224b7789c5cc5c801358e9cef37b5217a36c7a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__901a8e28dda0779a6cc5dd8c3f8fcea169b7e72efa71e6305a150cc9d9b64318(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd7f295df0aca2fe90565cb82af2ec9e71cc1d97a7da05949dbf70fcc0c12713(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eb0fdc0f277ad0b0155f037e0add156b407528fd53c2121bc310852c95f6458(
    value: typing.Optional[AssuredWorkloadsWorkloadEkmProvisioningResponse],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75ead2659dc228ffba2affa06b30430535376b5a77237f66bf1244bcebcedc3a(
    *,
    next_rotation_time: builtins.str,
    rotation_period: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c211879aac5debac51c4cc9a089cc9cd2266065dc0aa38fd459657f5551297c3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7916674322b3d89aabeeea448108a6bbd41e16bcc3f77664610461001be05b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2bf75bd679c6377cc414b7ec1d30fbab8aa7b2858f2f461af8301fdcf28bb8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f11fc118f46be1cc764988453d764daa6e7ba2c709cde62f83a34c17093b32e(
    value: typing.Optional[AssuredWorkloadsWorkloadKmsSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26fecf633db461cf2f69e6873c311207de1b63621d06c044cfbf801ef94100d6(
    *,
    assured_workloads_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    data_logs_viewer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    service_access_approver: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2d967c5aa74c1b49bc968b3f2357d32490d1126164b37f6d386e96e5025973c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d8cfab3cd67b8adba0573197ed2efa29295d2a44dd1f1ca66795827a4eace79(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2f632bd62672674a6f2d49d3ab41ad2b70e5581a0acb30b81f727c327f60f59(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58bbe12fb4485ca6dabd7c1b469dfd1c021ade3ec3585807adc3f05a211cdb9e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74e6d73aff808f1d08e382270713c10a95e7dd03a73126eec517ba061a836078(
    value: typing.Optional[AssuredWorkloadsWorkloadPartnerPermissions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29333448b387f8833a7a625af9e0ba2e99f3780ce71bd5363f3bddadb6f24f20(
    *,
    display_name: typing.Optional[builtins.str] = None,
    resource_id: typing.Optional[builtins.str] = None,
    resource_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2edc8d6fdd754d8bc4f4c2635a7f3f3869f1e624c211901446d63db016b83a57(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fba53c2cdb04a97d675b7e880dce13ca44948e33e73ce72de3b347ad572cf79b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e188fa8d29a28a543aa40bee88a49acea719e6c50b18665a02a4ac0f0a6f9b61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c818c3b6fdf2da85e1a132ad51574849ef76e8fc8735a15e318b3e2b02bcca45(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__803f31ec5ff4f87a6c372627b089aeeb72068c33c586faf73890909172d28238(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bd66bcd56042aa8a5a99cac4620c2325a6996d774f35a851333d1c502ef36ef(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AssuredWorkloadsWorkloadResourceSettings]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87a2e1ebae6a9567e1fd4ad009b5286b82d7edaf2f98fd87b761dcd7e1a7f2bf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fd92ef61a405749cb260c839837f3c971025fd97245082864cdc11497b1cd0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bae7ae0559f4a97238635f2500c8b00f5bcead1f6611ce817bf2ad93a1131378(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be473f7c8c8cf502ab2b3ab6f8cbfbf6c05247ecad6dc51e024c443349ebe529(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a591fbe0233be9446c69c309d6e538524947d03eccd61c3428b1926572725bdd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AssuredWorkloadsWorkloadResourceSettings]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69700436ae37bbe694a65d427a67e721e89138c693dfbde9606715f67f60090e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f65710f1077283170d34d842d12b5e47e838dd528db015ec76501cc9be9cb62(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b875e254b6a5060e6cfdb7d23f2ca93d4dc47af45e618eefd5baaf869c37fca2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f921a8ea2cfef72109c34288233587199a5140ff50a27c7e3a63e6f955e46ef4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__799c3e12b4ba4057e033a1ed307dbca2373d55b52e68bbb31f6081ad69626294(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2a1969256111c9a97ab8800460094430d2307a0ea290fc0a8439d71d334b03e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e666d80ca96373237959583ade263e6f513672dcdb007e09044975e5c535af5(
    value: typing.Optional[AssuredWorkloadsWorkloadResources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a88020acac07faec14c878dc04315c8a6df1631ed92933dbe9a4461c0bed437e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd858a950d26e2c3e352f731e24615cf545a216683460fe122b9a048af7f11f1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9619f5b244c29cc3dc79e35fc124984b2f0da7539140c986d3cb199bdc0cf5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fbb782c763af60ec1e672b9f415e113dbadec399a7977b227e2c66eab74055c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faf3428e82b734dc4072b4c4e7a813536a31f9623b0d2667cf60c7be901ca60e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0a5c222dabddb29e8af6825351c18517cfd7f97b3b92f0e05a4cc368a36b904(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42a2f490c8e26f5e61b6227b07b69b43efad11288c516eb14be9188821035789(
    value: typing.Optional[AssuredWorkloadsWorkloadSaaEnrollmentResponse],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__083c7c18b70baf6a2460ae5b777763b4d9ba4c82eaf9cdf06b1d2cfe22010430(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e49b66e8e95fe2439af51ebade52eec0bfa3c4553cbbc64de9f2310e3f9e1cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e21dbe3316f98984ccc3909d4c41c83e60ee0aeb0b0ca06c48b6e2401bcf38fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a19520efc4598e5e333248b003478924ff5850cd9806f834da8539f5f8613b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00574888656c2b2d62396856465237d0f8dc55985684aaa25da36677ca9ae7e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36fb9cac6faa1a4649d65813c7eaca4665445f14079811a4b30309f51a855da6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AssuredWorkloadsWorkloadTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72593d30b81559fb8e14130a83f762dd5be1c04a0cabdb5f2f8c4bb7e419e899(
    *,
    kaj_enrollment_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb861d0855e15b0a09f5be130b748afe06438b3af49566bc6d4ee5a7778ef054(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f493286e56aef64dac157adeddf944593c0e6e7f6055e646c16bcdc7054b2429(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18edeef89c52b2c72ce9a1669840fef75543a6ae917843430d1f1a5ba673fe4c(
    value: typing.Optional[AssuredWorkloadsWorkloadWorkloadOptions],
) -> None:
    """Type checking stubs"""
    pass
