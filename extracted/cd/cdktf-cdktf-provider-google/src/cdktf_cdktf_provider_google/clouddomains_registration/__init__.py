r'''
# `google_clouddomains_registration`

Refer to the Terraform Registry for docs: [`google_clouddomains_registration`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration).
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


class ClouddomainsRegistration(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddomainsRegistration.ClouddomainsRegistration",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration google_clouddomains_registration}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        contact_settings: typing.Union["ClouddomainsRegistrationContactSettings", typing.Dict[builtins.str, typing.Any]],
        domain_name: builtins.str,
        location: builtins.str,
        yearly_price: typing.Union["ClouddomainsRegistrationYearlyPrice", typing.Dict[builtins.str, typing.Any]],
        contact_notices: typing.Optional[typing.Sequence[builtins.str]] = None,
        dns_settings: typing.Optional[typing.Union["ClouddomainsRegistrationDnsSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        domain_notices: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        management_settings: typing.Optional[typing.Union["ClouddomainsRegistrationManagementSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ClouddomainsRegistrationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration google_clouddomains_registration} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param contact_settings: contact_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#contact_settings ClouddomainsRegistration#contact_settings}
        :param domain_name: Required. The domain name. Unicode domain names must be expressed in Punycode format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#domain_name ClouddomainsRegistration#domain_name}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#location ClouddomainsRegistration#location}
        :param yearly_price: yearly_price block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#yearly_price ClouddomainsRegistration#yearly_price}
        :param contact_notices: The list of contact notices that the caller acknowledges. Possible value is PUBLIC_CONTACT_DATA_ACKNOWLEDGEMENT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#contact_notices ClouddomainsRegistration#contact_notices}
        :param dns_settings: dns_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#dns_settings ClouddomainsRegistration#dns_settings}
        :param domain_notices: The list of domain notices that you acknowledge. Possible value is HSTS_PRELOADED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#domain_notices ClouddomainsRegistration#domain_notices}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#id ClouddomainsRegistration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of labels associated with the Registration. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#labels ClouddomainsRegistration#labels}
        :param management_settings: management_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#management_settings ClouddomainsRegistration#management_settings}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#project ClouddomainsRegistration#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#timeouts ClouddomainsRegistration#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__797180f5e86841aa5231a2ad92501266a7b765412dd26f59e71420c6ee7eb103)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ClouddomainsRegistrationConfig(
            contact_settings=contact_settings,
            domain_name=domain_name,
            location=location,
            yearly_price=yearly_price,
            contact_notices=contact_notices,
            dns_settings=dns_settings,
            domain_notices=domain_notices,
            id=id,
            labels=labels,
            management_settings=management_settings,
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
        '''Generates CDKTF code for importing a ClouddomainsRegistration resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ClouddomainsRegistration to import.
        :param import_from_id: The id of the existing ClouddomainsRegistration that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ClouddomainsRegistration to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c3b295001a5b2903131a1a92b4d4051c0339cc237e38e5f70f9343fce5625f6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putContactSettings")
    def put_contact_settings(
        self,
        *,
        admin_contact: typing.Union["ClouddomainsRegistrationContactSettingsAdminContact", typing.Dict[builtins.str, typing.Any]],
        privacy: builtins.str,
        registrant_contact: typing.Union["ClouddomainsRegistrationContactSettingsRegistrantContact", typing.Dict[builtins.str, typing.Any]],
        technical_contact: typing.Union["ClouddomainsRegistrationContactSettingsTechnicalContact", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param admin_contact: admin_contact block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#admin_contact ClouddomainsRegistration#admin_contact}
        :param privacy: Required. Privacy setting for the contacts associated with the Registration. Values are PUBLIC_CONTACT_DATA, PRIVATE_CONTACT_DATA, and REDACTED_CONTACT_DATA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#privacy ClouddomainsRegistration#privacy}
        :param registrant_contact: registrant_contact block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#registrant_contact ClouddomainsRegistration#registrant_contact}
        :param technical_contact: technical_contact block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#technical_contact ClouddomainsRegistration#technical_contact}
        '''
        value = ClouddomainsRegistrationContactSettings(
            admin_contact=admin_contact,
            privacy=privacy,
            registrant_contact=registrant_contact,
            technical_contact=technical_contact,
        )

        return typing.cast(None, jsii.invoke(self, "putContactSettings", [value]))

    @jsii.member(jsii_name="putDnsSettings")
    def put_dns_settings(
        self,
        *,
        custom_dns: typing.Optional[typing.Union["ClouddomainsRegistrationDnsSettingsCustomDns", typing.Dict[builtins.str, typing.Any]]] = None,
        glue_records: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddomainsRegistrationDnsSettingsGlueRecords", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param custom_dns: custom_dns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#custom_dns ClouddomainsRegistration#custom_dns}
        :param glue_records: glue_records block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#glue_records ClouddomainsRegistration#glue_records}
        '''
        value = ClouddomainsRegistrationDnsSettings(
            custom_dns=custom_dns, glue_records=glue_records
        )

        return typing.cast(None, jsii.invoke(self, "putDnsSettings", [value]))

    @jsii.member(jsii_name="putManagementSettings")
    def put_management_settings(
        self,
        *,
        preferred_renewal_method: typing.Optional[builtins.str] = None,
        transfer_lock_state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param preferred_renewal_method: The desired renewal method for this Registration. The actual renewalMethod is automatically updated to reflect this choice. If unset or equal to RENEWAL_METHOD_UNSPECIFIED, the actual renewalMethod is treated as if it were set to AUTOMATIC_RENEWAL. You cannot use RENEWAL_DISABLED during resource creation, and you can update the renewal status only when the Registration resource has state ACTIVE or SUSPENDED. When preferredRenewalMethod is set to AUTOMATIC_RENEWAL, the actual renewalMethod can be set to RENEWAL_DISABLED in case of problems with the billing account or reported domain abuse. In such cases, check the issues field on the Registration. After the problem is resolved, the renewalMethod is automatically updated to preferredRenewalMethod in a few hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#preferred_renewal_method ClouddomainsRegistration#preferred_renewal_method}
        :param transfer_lock_state: Controls whether the domain can be transferred to another registrar. Values are UNLOCKED or LOCKED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#transfer_lock_state ClouddomainsRegistration#transfer_lock_state}
        '''
        value = ClouddomainsRegistrationManagementSettings(
            preferred_renewal_method=preferred_renewal_method,
            transfer_lock_state=transfer_lock_state,
        )

        return typing.cast(None, jsii.invoke(self, "putManagementSettings", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#create ClouddomainsRegistration#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#delete ClouddomainsRegistration#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#update ClouddomainsRegistration#update}.
        '''
        value = ClouddomainsRegistrationTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putYearlyPrice")
    def put_yearly_price(
        self,
        *,
        currency_code: typing.Optional[builtins.str] = None,
        units: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param currency_code: The three-letter currency code defined in ISO 4217. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#currency_code ClouddomainsRegistration#currency_code}
        :param units: The whole units of the amount. For example if currencyCode is "USD", then 1 unit is one US dollar. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#units ClouddomainsRegistration#units}
        '''
        value = ClouddomainsRegistrationYearlyPrice(
            currency_code=currency_code, units=units
        )

        return typing.cast(None, jsii.invoke(self, "putYearlyPrice", [value]))

    @jsii.member(jsii_name="resetContactNotices")
    def reset_contact_notices(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContactNotices", []))

    @jsii.member(jsii_name="resetDnsSettings")
    def reset_dns_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsSettings", []))

    @jsii.member(jsii_name="resetDomainNotices")
    def reset_domain_notices(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomainNotices", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetManagementSettings")
    def reset_management_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagementSettings", []))

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
    @jsii.member(jsii_name="contactSettings")
    def contact_settings(
        self,
    ) -> "ClouddomainsRegistrationContactSettingsOutputReference":
        return typing.cast("ClouddomainsRegistrationContactSettingsOutputReference", jsii.get(self, "contactSettings"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="dnsSettings")
    def dns_settings(self) -> "ClouddomainsRegistrationDnsSettingsOutputReference":
        return typing.cast("ClouddomainsRegistrationDnsSettingsOutputReference", jsii.get(self, "dnsSettings"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="expireTime")
    def expire_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expireTime"))

    @builtins.property
    @jsii.member(jsii_name="issues")
    def issues(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "issues"))

    @builtins.property
    @jsii.member(jsii_name="managementSettings")
    def management_settings(
        self,
    ) -> "ClouddomainsRegistrationManagementSettingsOutputReference":
        return typing.cast("ClouddomainsRegistrationManagementSettingsOutputReference", jsii.get(self, "managementSettings"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="registerFailureReason")
    def register_failure_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "registerFailureReason"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="supportedPrivacy")
    def supported_privacy(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "supportedPrivacy"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ClouddomainsRegistrationTimeoutsOutputReference":
        return typing.cast("ClouddomainsRegistrationTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="yearlyPrice")
    def yearly_price(self) -> "ClouddomainsRegistrationYearlyPriceOutputReference":
        return typing.cast("ClouddomainsRegistrationYearlyPriceOutputReference", jsii.get(self, "yearlyPrice"))

    @builtins.property
    @jsii.member(jsii_name="contactNoticesInput")
    def contact_notices_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "contactNoticesInput"))

    @builtins.property
    @jsii.member(jsii_name="contactSettingsInput")
    def contact_settings_input(
        self,
    ) -> typing.Optional["ClouddomainsRegistrationContactSettings"]:
        return typing.cast(typing.Optional["ClouddomainsRegistrationContactSettings"], jsii.get(self, "contactSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsSettingsInput")
    def dns_settings_input(
        self,
    ) -> typing.Optional["ClouddomainsRegistrationDnsSettings"]:
        return typing.cast(typing.Optional["ClouddomainsRegistrationDnsSettings"], jsii.get(self, "dnsSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="domainNameInput")
    def domain_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="domainNoticesInput")
    def domain_notices_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "domainNoticesInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

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
    @jsii.member(jsii_name="managementSettingsInput")
    def management_settings_input(
        self,
    ) -> typing.Optional["ClouddomainsRegistrationManagementSettings"]:
        return typing.cast(typing.Optional["ClouddomainsRegistrationManagementSettings"], jsii.get(self, "managementSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ClouddomainsRegistrationTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ClouddomainsRegistrationTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="yearlyPriceInput")
    def yearly_price_input(
        self,
    ) -> typing.Optional["ClouddomainsRegistrationYearlyPrice"]:
        return typing.cast(typing.Optional["ClouddomainsRegistrationYearlyPrice"], jsii.get(self, "yearlyPriceInput"))

    @builtins.property
    @jsii.member(jsii_name="contactNotices")
    def contact_notices(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "contactNotices"))

    @contact_notices.setter
    def contact_notices(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe67f6d36b5126343db6838f57958dc5b1d7534cd96271ebe132c0be20cb978f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contactNotices", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03556343706ea17df9b31535f564ab6825d9c8e84143d388fc0963bf6bfa85a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainNotices")
    def domain_notices(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "domainNotices"))

    @domain_notices.setter
    def domain_notices(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ced846c6a676ae88369813ab14ae872ce99b45f75f25f65db1739a585e146270)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainNotices", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a07777231090026382ac4379fd4f588e75b0d76a73faa8b8a9227571172048a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__857002739a0725cbe458979e24abcaae93c31ad81ac638e048ce6aaef697301a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c95942581a94bed2f504fdda49faad8b46ee9bc669385edf23190f294fec2491)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbc338db614a1afe8339d01999fa774c6932ee80c43d2f14c9a4a8dbbc42f00f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddomainsRegistration.ClouddomainsRegistrationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "contact_settings": "contactSettings",
        "domain_name": "domainName",
        "location": "location",
        "yearly_price": "yearlyPrice",
        "contact_notices": "contactNotices",
        "dns_settings": "dnsSettings",
        "domain_notices": "domainNotices",
        "id": "id",
        "labels": "labels",
        "management_settings": "managementSettings",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class ClouddomainsRegistrationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        contact_settings: typing.Union["ClouddomainsRegistrationContactSettings", typing.Dict[builtins.str, typing.Any]],
        domain_name: builtins.str,
        location: builtins.str,
        yearly_price: typing.Union["ClouddomainsRegistrationYearlyPrice", typing.Dict[builtins.str, typing.Any]],
        contact_notices: typing.Optional[typing.Sequence[builtins.str]] = None,
        dns_settings: typing.Optional[typing.Union["ClouddomainsRegistrationDnsSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        domain_notices: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        management_settings: typing.Optional[typing.Union["ClouddomainsRegistrationManagementSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ClouddomainsRegistrationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param contact_settings: contact_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#contact_settings ClouddomainsRegistration#contact_settings}
        :param domain_name: Required. The domain name. Unicode domain names must be expressed in Punycode format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#domain_name ClouddomainsRegistration#domain_name}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#location ClouddomainsRegistration#location}
        :param yearly_price: yearly_price block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#yearly_price ClouddomainsRegistration#yearly_price}
        :param contact_notices: The list of contact notices that the caller acknowledges. Possible value is PUBLIC_CONTACT_DATA_ACKNOWLEDGEMENT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#contact_notices ClouddomainsRegistration#contact_notices}
        :param dns_settings: dns_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#dns_settings ClouddomainsRegistration#dns_settings}
        :param domain_notices: The list of domain notices that you acknowledge. Possible value is HSTS_PRELOADED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#domain_notices ClouddomainsRegistration#domain_notices}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#id ClouddomainsRegistration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of labels associated with the Registration. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#labels ClouddomainsRegistration#labels}
        :param management_settings: management_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#management_settings ClouddomainsRegistration#management_settings}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#project ClouddomainsRegistration#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#timeouts ClouddomainsRegistration#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(contact_settings, dict):
            contact_settings = ClouddomainsRegistrationContactSettings(**contact_settings)
        if isinstance(yearly_price, dict):
            yearly_price = ClouddomainsRegistrationYearlyPrice(**yearly_price)
        if isinstance(dns_settings, dict):
            dns_settings = ClouddomainsRegistrationDnsSettings(**dns_settings)
        if isinstance(management_settings, dict):
            management_settings = ClouddomainsRegistrationManagementSettings(**management_settings)
        if isinstance(timeouts, dict):
            timeouts = ClouddomainsRegistrationTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ecb79ef81f8b0639a535a81df958d20ebc053c2f0e500f559096b9ee2902eb4)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument contact_settings", value=contact_settings, expected_type=type_hints["contact_settings"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument yearly_price", value=yearly_price, expected_type=type_hints["yearly_price"])
            check_type(argname="argument contact_notices", value=contact_notices, expected_type=type_hints["contact_notices"])
            check_type(argname="argument dns_settings", value=dns_settings, expected_type=type_hints["dns_settings"])
            check_type(argname="argument domain_notices", value=domain_notices, expected_type=type_hints["domain_notices"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument management_settings", value=management_settings, expected_type=type_hints["management_settings"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "contact_settings": contact_settings,
            "domain_name": domain_name,
            "location": location,
            "yearly_price": yearly_price,
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
        if contact_notices is not None:
            self._values["contact_notices"] = contact_notices
        if dns_settings is not None:
            self._values["dns_settings"] = dns_settings
        if domain_notices is not None:
            self._values["domain_notices"] = domain_notices
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if management_settings is not None:
            self._values["management_settings"] = management_settings
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
    def contact_settings(self) -> "ClouddomainsRegistrationContactSettings":
        '''contact_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#contact_settings ClouddomainsRegistration#contact_settings}
        '''
        result = self._values.get("contact_settings")
        assert result is not None, "Required property 'contact_settings' is missing"
        return typing.cast("ClouddomainsRegistrationContactSettings", result)

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''Required. The domain name. Unicode domain names must be expressed in Punycode format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#domain_name ClouddomainsRegistration#domain_name}
        '''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#location ClouddomainsRegistration#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def yearly_price(self) -> "ClouddomainsRegistrationYearlyPrice":
        '''yearly_price block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#yearly_price ClouddomainsRegistration#yearly_price}
        '''
        result = self._values.get("yearly_price")
        assert result is not None, "Required property 'yearly_price' is missing"
        return typing.cast("ClouddomainsRegistrationYearlyPrice", result)

    @builtins.property
    def contact_notices(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of contact notices that the caller acknowledges. Possible value is PUBLIC_CONTACT_DATA_ACKNOWLEDGEMENT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#contact_notices ClouddomainsRegistration#contact_notices}
        '''
        result = self._values.get("contact_notices")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dns_settings(self) -> typing.Optional["ClouddomainsRegistrationDnsSettings"]:
        '''dns_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#dns_settings ClouddomainsRegistration#dns_settings}
        '''
        result = self._values.get("dns_settings")
        return typing.cast(typing.Optional["ClouddomainsRegistrationDnsSettings"], result)

    @builtins.property
    def domain_notices(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of domain notices that you acknowledge. Possible value is HSTS_PRELOADED.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#domain_notices ClouddomainsRegistration#domain_notices}
        '''
        result = self._values.get("domain_notices")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#id ClouddomainsRegistration#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Set of labels associated with the Registration.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#labels ClouddomainsRegistration#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def management_settings(
        self,
    ) -> typing.Optional["ClouddomainsRegistrationManagementSettings"]:
        '''management_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#management_settings ClouddomainsRegistration#management_settings}
        '''
        result = self._values.get("management_settings")
        return typing.cast(typing.Optional["ClouddomainsRegistrationManagementSettings"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#project ClouddomainsRegistration#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ClouddomainsRegistrationTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#timeouts ClouddomainsRegistration#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ClouddomainsRegistrationTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddomainsRegistrationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddomainsRegistration.ClouddomainsRegistrationContactSettings",
    jsii_struct_bases=[],
    name_mapping={
        "admin_contact": "adminContact",
        "privacy": "privacy",
        "registrant_contact": "registrantContact",
        "technical_contact": "technicalContact",
    },
)
class ClouddomainsRegistrationContactSettings:
    def __init__(
        self,
        *,
        admin_contact: typing.Union["ClouddomainsRegistrationContactSettingsAdminContact", typing.Dict[builtins.str, typing.Any]],
        privacy: builtins.str,
        registrant_contact: typing.Union["ClouddomainsRegistrationContactSettingsRegistrantContact", typing.Dict[builtins.str, typing.Any]],
        technical_contact: typing.Union["ClouddomainsRegistrationContactSettingsTechnicalContact", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param admin_contact: admin_contact block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#admin_contact ClouddomainsRegistration#admin_contact}
        :param privacy: Required. Privacy setting for the contacts associated with the Registration. Values are PUBLIC_CONTACT_DATA, PRIVATE_CONTACT_DATA, and REDACTED_CONTACT_DATA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#privacy ClouddomainsRegistration#privacy}
        :param registrant_contact: registrant_contact block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#registrant_contact ClouddomainsRegistration#registrant_contact}
        :param technical_contact: technical_contact block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#technical_contact ClouddomainsRegistration#technical_contact}
        '''
        if isinstance(admin_contact, dict):
            admin_contact = ClouddomainsRegistrationContactSettingsAdminContact(**admin_contact)
        if isinstance(registrant_contact, dict):
            registrant_contact = ClouddomainsRegistrationContactSettingsRegistrantContact(**registrant_contact)
        if isinstance(technical_contact, dict):
            technical_contact = ClouddomainsRegistrationContactSettingsTechnicalContact(**technical_contact)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feb620fa3ac96d8237513d8f48436a0e2670d5849870990c51cd600488bfd787)
            check_type(argname="argument admin_contact", value=admin_contact, expected_type=type_hints["admin_contact"])
            check_type(argname="argument privacy", value=privacy, expected_type=type_hints["privacy"])
            check_type(argname="argument registrant_contact", value=registrant_contact, expected_type=type_hints["registrant_contact"])
            check_type(argname="argument technical_contact", value=technical_contact, expected_type=type_hints["technical_contact"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "admin_contact": admin_contact,
            "privacy": privacy,
            "registrant_contact": registrant_contact,
            "technical_contact": technical_contact,
        }

    @builtins.property
    def admin_contact(self) -> "ClouddomainsRegistrationContactSettingsAdminContact":
        '''admin_contact block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#admin_contact ClouddomainsRegistration#admin_contact}
        '''
        result = self._values.get("admin_contact")
        assert result is not None, "Required property 'admin_contact' is missing"
        return typing.cast("ClouddomainsRegistrationContactSettingsAdminContact", result)

    @builtins.property
    def privacy(self) -> builtins.str:
        '''Required. Privacy setting for the contacts associated with the Registration. Values are PUBLIC_CONTACT_DATA, PRIVATE_CONTACT_DATA, and REDACTED_CONTACT_DATA.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#privacy ClouddomainsRegistration#privacy}
        '''
        result = self._values.get("privacy")
        assert result is not None, "Required property 'privacy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def registrant_contact(
        self,
    ) -> "ClouddomainsRegistrationContactSettingsRegistrantContact":
        '''registrant_contact block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#registrant_contact ClouddomainsRegistration#registrant_contact}
        '''
        result = self._values.get("registrant_contact")
        assert result is not None, "Required property 'registrant_contact' is missing"
        return typing.cast("ClouddomainsRegistrationContactSettingsRegistrantContact", result)

    @builtins.property
    def technical_contact(
        self,
    ) -> "ClouddomainsRegistrationContactSettingsTechnicalContact":
        '''technical_contact block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#technical_contact ClouddomainsRegistration#technical_contact}
        '''
        result = self._values.get("technical_contact")
        assert result is not None, "Required property 'technical_contact' is missing"
        return typing.cast("ClouddomainsRegistrationContactSettingsTechnicalContact", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddomainsRegistrationContactSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddomainsRegistration.ClouddomainsRegistrationContactSettingsAdminContact",
    jsii_struct_bases=[],
    name_mapping={
        "email": "email",
        "phone_number": "phoneNumber",
        "postal_address": "postalAddress",
        "fax_number": "faxNumber",
    },
)
class ClouddomainsRegistrationContactSettingsAdminContact:
    def __init__(
        self,
        *,
        email: builtins.str,
        phone_number: builtins.str,
        postal_address: typing.Union["ClouddomainsRegistrationContactSettingsAdminContactPostalAddress", typing.Dict[builtins.str, typing.Any]],
        fax_number: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param email: Required. Email address of the contact. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#email ClouddomainsRegistration#email}
        :param phone_number: Required. Phone number of the contact in international format. For example, "+1-800-555-0123". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#phone_number ClouddomainsRegistration#phone_number}
        :param postal_address: postal_address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#postal_address ClouddomainsRegistration#postal_address}
        :param fax_number: Fax number of the contact in international format. For example, "+1-800-555-0123". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#fax_number ClouddomainsRegistration#fax_number}
        '''
        if isinstance(postal_address, dict):
            postal_address = ClouddomainsRegistrationContactSettingsAdminContactPostalAddress(**postal_address)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7b305b99420c3033da38f4d9b0e24b7f3356ed46b47db72d1b0adf836a4cdd5)
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
            check_type(argname="argument postal_address", value=postal_address, expected_type=type_hints["postal_address"])
            check_type(argname="argument fax_number", value=fax_number, expected_type=type_hints["fax_number"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "email": email,
            "phone_number": phone_number,
            "postal_address": postal_address,
        }
        if fax_number is not None:
            self._values["fax_number"] = fax_number

    @builtins.property
    def email(self) -> builtins.str:
        '''Required. Email address of the contact.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#email ClouddomainsRegistration#email}
        '''
        result = self._values.get("email")
        assert result is not None, "Required property 'email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def phone_number(self) -> builtins.str:
        '''Required. Phone number of the contact in international format. For example, "+1-800-555-0123".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#phone_number ClouddomainsRegistration#phone_number}
        '''
        result = self._values.get("phone_number")
        assert result is not None, "Required property 'phone_number' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def postal_address(
        self,
    ) -> "ClouddomainsRegistrationContactSettingsAdminContactPostalAddress":
        '''postal_address block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#postal_address ClouddomainsRegistration#postal_address}
        '''
        result = self._values.get("postal_address")
        assert result is not None, "Required property 'postal_address' is missing"
        return typing.cast("ClouddomainsRegistrationContactSettingsAdminContactPostalAddress", result)

    @builtins.property
    def fax_number(self) -> typing.Optional[builtins.str]:
        '''Fax number of the contact in international format. For example, "+1-800-555-0123".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#fax_number ClouddomainsRegistration#fax_number}
        '''
        result = self._values.get("fax_number")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddomainsRegistrationContactSettingsAdminContact(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddomainsRegistrationContactSettingsAdminContactOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddomainsRegistration.ClouddomainsRegistrationContactSettingsAdminContactOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8e2eef09a8b0324f32b939001c16faf58042ff817e77e62e58f326aa2cfcdf9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPostalAddress")
    def put_postal_address(
        self,
        *,
        region_code: builtins.str,
        address_lines: typing.Optional[typing.Sequence[builtins.str]] = None,
        administrative_area: typing.Optional[builtins.str] = None,
        locality: typing.Optional[builtins.str] = None,
        organization: typing.Optional[builtins.str] = None,
        postal_code: typing.Optional[builtins.str] = None,
        recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param region_code: Required. CLDR region code of the country/region of the address. This is never inferred and it is up to the user to ensure the value is correct. See https://cldr.unicode.org/ and https://www.unicode.org/cldr/charts/30/supplemental/territory_information.html for details. Example: "CH" for Switzerland. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#region_code ClouddomainsRegistration#region_code}
        :param address_lines: Unstructured address lines describing the lower levels of an address. Because values in addressLines do not have type information and may sometimes contain multiple values in a single field (e.g. "Austin, TX"), it is important that the line order is clear. The order of address lines should be "envelope order" for the country/region of the address. In places where this can vary (e.g. Japan), address_language is used to make it explicit (e.g. "ja" for large-to-small ordering and "ja-Latn" or "en" for small-to-large). This way, the most specific line of an address can be selected based on the language. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#address_lines ClouddomainsRegistration#address_lines}
        :param administrative_area: Highest administrative subdivision which is used for postal addresses of a country or region. For example, this can be a state, a province, an oblast, or a prefecture. Specifically, for Spain this is the province and not the autonomous community (e.g. "Barcelona" and not "Catalonia"). Many countries don't use an administrative area in postal addresses. E.g. in Switzerland this should be left unpopulated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#administrative_area ClouddomainsRegistration#administrative_area}
        :param locality: Generally refers to the city/town portion of the address. Examples: US city, IT comune, UK post town. In regions of the world where localities are not well defined or do not fit into this structure well, leave locality empty and use addressLines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#locality ClouddomainsRegistration#locality}
        :param organization: The name of the organization at the address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#organization ClouddomainsRegistration#organization}
        :param postal_code: Postal code of the address. Not all countries use or require postal codes to be present, but where they are used, they may trigger additional validation with other parts of the address (e.g. state/zip validation in the U.S.A.). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#postal_code ClouddomainsRegistration#postal_code}
        :param recipients: The recipient at the address. This field may, under certain circumstances, contain multiline information. For example, it might contain "care of" information. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#recipients ClouddomainsRegistration#recipients}
        '''
        value = ClouddomainsRegistrationContactSettingsAdminContactPostalAddress(
            region_code=region_code,
            address_lines=address_lines,
            administrative_area=administrative_area,
            locality=locality,
            organization=organization,
            postal_code=postal_code,
            recipients=recipients,
        )

        return typing.cast(None, jsii.invoke(self, "putPostalAddress", [value]))

    @jsii.member(jsii_name="resetFaxNumber")
    def reset_fax_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFaxNumber", []))

    @builtins.property
    @jsii.member(jsii_name="postalAddress")
    def postal_address(
        self,
    ) -> "ClouddomainsRegistrationContactSettingsAdminContactPostalAddressOutputReference":
        return typing.cast("ClouddomainsRegistrationContactSettingsAdminContactPostalAddressOutputReference", jsii.get(self, "postalAddress"))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="faxNumberInput")
    def fax_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "faxNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="phoneNumberInput")
    def phone_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "phoneNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="postalAddressInput")
    def postal_address_input(
        self,
    ) -> typing.Optional["ClouddomainsRegistrationContactSettingsAdminContactPostalAddress"]:
        return typing.cast(typing.Optional["ClouddomainsRegistrationContactSettingsAdminContactPostalAddress"], jsii.get(self, "postalAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ba42de934b4b35e32a20b7c377a6a371415c35738eb610afeb942f9fe5a5c10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="faxNumber")
    def fax_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "faxNumber"))

    @fax_number.setter
    def fax_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__079b2ae850fcb4e2bf9cbe17a508a57ce170c09a97eecd057e88086642eef47b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "faxNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="phoneNumber")
    def phone_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "phoneNumber"))

    @phone_number.setter
    def phone_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be829bf5cb23499b928cce1960a958713b7b376c2af7f4a44615874de8f4a104)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "phoneNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddomainsRegistrationContactSettingsAdminContact]:
        return typing.cast(typing.Optional[ClouddomainsRegistrationContactSettingsAdminContact], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddomainsRegistrationContactSettingsAdminContact],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac1f26d1b1ddca47921a0db985576e6fb5f533fa2a222accb6ab41844f6de3ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddomainsRegistration.ClouddomainsRegistrationContactSettingsAdminContactPostalAddress",
    jsii_struct_bases=[],
    name_mapping={
        "region_code": "regionCode",
        "address_lines": "addressLines",
        "administrative_area": "administrativeArea",
        "locality": "locality",
        "organization": "organization",
        "postal_code": "postalCode",
        "recipients": "recipients",
    },
)
class ClouddomainsRegistrationContactSettingsAdminContactPostalAddress:
    def __init__(
        self,
        *,
        region_code: builtins.str,
        address_lines: typing.Optional[typing.Sequence[builtins.str]] = None,
        administrative_area: typing.Optional[builtins.str] = None,
        locality: typing.Optional[builtins.str] = None,
        organization: typing.Optional[builtins.str] = None,
        postal_code: typing.Optional[builtins.str] = None,
        recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param region_code: Required. CLDR region code of the country/region of the address. This is never inferred and it is up to the user to ensure the value is correct. See https://cldr.unicode.org/ and https://www.unicode.org/cldr/charts/30/supplemental/territory_information.html for details. Example: "CH" for Switzerland. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#region_code ClouddomainsRegistration#region_code}
        :param address_lines: Unstructured address lines describing the lower levels of an address. Because values in addressLines do not have type information and may sometimes contain multiple values in a single field (e.g. "Austin, TX"), it is important that the line order is clear. The order of address lines should be "envelope order" for the country/region of the address. In places where this can vary (e.g. Japan), address_language is used to make it explicit (e.g. "ja" for large-to-small ordering and "ja-Latn" or "en" for small-to-large). This way, the most specific line of an address can be selected based on the language. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#address_lines ClouddomainsRegistration#address_lines}
        :param administrative_area: Highest administrative subdivision which is used for postal addresses of a country or region. For example, this can be a state, a province, an oblast, or a prefecture. Specifically, for Spain this is the province and not the autonomous community (e.g. "Barcelona" and not "Catalonia"). Many countries don't use an administrative area in postal addresses. E.g. in Switzerland this should be left unpopulated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#administrative_area ClouddomainsRegistration#administrative_area}
        :param locality: Generally refers to the city/town portion of the address. Examples: US city, IT comune, UK post town. In regions of the world where localities are not well defined or do not fit into this structure well, leave locality empty and use addressLines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#locality ClouddomainsRegistration#locality}
        :param organization: The name of the organization at the address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#organization ClouddomainsRegistration#organization}
        :param postal_code: Postal code of the address. Not all countries use or require postal codes to be present, but where they are used, they may trigger additional validation with other parts of the address (e.g. state/zip validation in the U.S.A.). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#postal_code ClouddomainsRegistration#postal_code}
        :param recipients: The recipient at the address. This field may, under certain circumstances, contain multiline information. For example, it might contain "care of" information. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#recipients ClouddomainsRegistration#recipients}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30e724a55eacd414e0f0c016009a2381f14d4a1c6a4f1a8b678cbc84c7a8a093)
            check_type(argname="argument region_code", value=region_code, expected_type=type_hints["region_code"])
            check_type(argname="argument address_lines", value=address_lines, expected_type=type_hints["address_lines"])
            check_type(argname="argument administrative_area", value=administrative_area, expected_type=type_hints["administrative_area"])
            check_type(argname="argument locality", value=locality, expected_type=type_hints["locality"])
            check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
            check_type(argname="argument postal_code", value=postal_code, expected_type=type_hints["postal_code"])
            check_type(argname="argument recipients", value=recipients, expected_type=type_hints["recipients"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "region_code": region_code,
        }
        if address_lines is not None:
            self._values["address_lines"] = address_lines
        if administrative_area is not None:
            self._values["administrative_area"] = administrative_area
        if locality is not None:
            self._values["locality"] = locality
        if organization is not None:
            self._values["organization"] = organization
        if postal_code is not None:
            self._values["postal_code"] = postal_code
        if recipients is not None:
            self._values["recipients"] = recipients

    @builtins.property
    def region_code(self) -> builtins.str:
        '''Required.

        CLDR region code of the country/region of the address. This is never inferred and it is up to the user to
        ensure the value is correct. See https://cldr.unicode.org/ and
        https://www.unicode.org/cldr/charts/30/supplemental/territory_information.html for details. Example: "CH" for Switzerland.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#region_code ClouddomainsRegistration#region_code}
        '''
        result = self._values.get("region_code")
        assert result is not None, "Required property 'region_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def address_lines(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Unstructured address lines describing the lower levels of an address.

        Because values in addressLines do not have type information and may sometimes contain multiple values in a single
        field (e.g. "Austin, TX"), it is important that the line order is clear. The order of address lines should be
        "envelope order" for the country/region of the address. In places where this can vary (e.g. Japan), address_language
        is used to make it explicit (e.g. "ja" for large-to-small ordering and "ja-Latn" or "en" for small-to-large). This way,
        the most specific line of an address can be selected based on the language.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#address_lines ClouddomainsRegistration#address_lines}
        '''
        result = self._values.get("address_lines")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def administrative_area(self) -> typing.Optional[builtins.str]:
        '''Highest administrative subdivision which is used for postal addresses of a country or region.

        For example, this can be a state,
        a province, an oblast, or a prefecture. Specifically, for Spain this is the province and not the autonomous community
        (e.g. "Barcelona" and not "Catalonia"). Many countries don't use an administrative area in postal addresses. E.g. in Switzerland
        this should be left unpopulated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#administrative_area ClouddomainsRegistration#administrative_area}
        '''
        result = self._values.get("administrative_area")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def locality(self) -> typing.Optional[builtins.str]:
        '''Generally refers to the city/town portion of the address.

        Examples: US city, IT comune, UK post town. In regions of the world
        where localities are not well defined or do not fit into this structure well, leave locality empty and use addressLines.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#locality ClouddomainsRegistration#locality}
        '''
        result = self._values.get("locality")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organization(self) -> typing.Optional[builtins.str]:
        '''The name of the organization at the address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#organization ClouddomainsRegistration#organization}
        '''
        result = self._values.get("organization")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def postal_code(self) -> typing.Optional[builtins.str]:
        '''Postal code of the address.

        Not all countries use or require postal codes to be present, but where they are used,
        they may trigger additional validation with other parts of the address (e.g. state/zip validation in the U.S.A.).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#postal_code ClouddomainsRegistration#postal_code}
        '''
        result = self._values.get("postal_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recipients(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The recipient at the address.

        This field may, under certain circumstances, contain multiline information. For example,
        it might contain "care of" information.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#recipients ClouddomainsRegistration#recipients}
        '''
        result = self._values.get("recipients")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddomainsRegistrationContactSettingsAdminContactPostalAddress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddomainsRegistrationContactSettingsAdminContactPostalAddressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddomainsRegistration.ClouddomainsRegistrationContactSettingsAdminContactPostalAddressOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcbc64dae595f1de265c5de4d534fa2fef3bdbeb4c57f38fa0e3c938b0ecd1cd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAddressLines")
    def reset_address_lines(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddressLines", []))

    @jsii.member(jsii_name="resetAdministrativeArea")
    def reset_administrative_area(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdministrativeArea", []))

    @jsii.member(jsii_name="resetLocality")
    def reset_locality(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocality", []))

    @jsii.member(jsii_name="resetOrganization")
    def reset_organization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrganization", []))

    @jsii.member(jsii_name="resetPostalCode")
    def reset_postal_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostalCode", []))

    @jsii.member(jsii_name="resetRecipients")
    def reset_recipients(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecipients", []))

    @builtins.property
    @jsii.member(jsii_name="addressLinesInput")
    def address_lines_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "addressLinesInput"))

    @builtins.property
    @jsii.member(jsii_name="administrativeAreaInput")
    def administrative_area_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "administrativeAreaInput"))

    @builtins.property
    @jsii.member(jsii_name="localityInput")
    def locality_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localityInput"))

    @builtins.property
    @jsii.member(jsii_name="organizationInput")
    def organization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationInput"))

    @builtins.property
    @jsii.member(jsii_name="postalCodeInput")
    def postal_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "postalCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="recipientsInput")
    def recipients_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "recipientsInput"))

    @builtins.property
    @jsii.member(jsii_name="regionCodeInput")
    def region_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="addressLines")
    def address_lines(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "addressLines"))

    @address_lines.setter
    def address_lines(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c248f9534d8b2679fe5e4674ba11b4e26ef5533cec4cd418fdc14008543834e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addressLines", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="administrativeArea")
    def administrative_area(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "administrativeArea"))

    @administrative_area.setter
    def administrative_area(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9c7b10b7b3a0ae478f95cee1fe483c2405c2b8d15e14b511ae93da8ec56ca8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "administrativeArea", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="locality")
    def locality(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "locality"))

    @locality.setter
    def locality(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71ccff810325a8f32345f9c0c59bf6d9c26209083fa2503b1e35a53eef6db961)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locality", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__783469c2c84e7ab06ae6d63689e1fe950cc5c08aef8ccded920aa5ce8b38692e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postalCode")
    def postal_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postalCode"))

    @postal_code.setter
    def postal_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2b3a8c0da47372f24cbf45108878e4d556f9068690584ccbaccd7cfbb1ddccb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postalCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recipients")
    def recipients(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "recipients"))

    @recipients.setter
    def recipients(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53adcc48f1b1eea0764050df56106186f565d6c867d9bfb62f6e5557eb9b6d07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regionCode")
    def region_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regionCode"))

    @region_code.setter
    def region_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d2fdd624e5787ccd67a73a5cc70e7dd14f2314b0f9fab8339a4c507ab93d5e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regionCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddomainsRegistrationContactSettingsAdminContactPostalAddress]:
        return typing.cast(typing.Optional[ClouddomainsRegistrationContactSettingsAdminContactPostalAddress], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddomainsRegistrationContactSettingsAdminContactPostalAddress],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__def86f6284230dcbafbbb3ac34e5d6abf8163d5d59eeecfcfed435cd4140f754)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ClouddomainsRegistrationContactSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddomainsRegistration.ClouddomainsRegistrationContactSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__142295ca10bac2b284b62d55e613ef1cd0c315e8b20b175e95b480e81153aad3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdminContact")
    def put_admin_contact(
        self,
        *,
        email: builtins.str,
        phone_number: builtins.str,
        postal_address: typing.Union[ClouddomainsRegistrationContactSettingsAdminContactPostalAddress, typing.Dict[builtins.str, typing.Any]],
        fax_number: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param email: Required. Email address of the contact. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#email ClouddomainsRegistration#email}
        :param phone_number: Required. Phone number of the contact in international format. For example, "+1-800-555-0123". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#phone_number ClouddomainsRegistration#phone_number}
        :param postal_address: postal_address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#postal_address ClouddomainsRegistration#postal_address}
        :param fax_number: Fax number of the contact in international format. For example, "+1-800-555-0123". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#fax_number ClouddomainsRegistration#fax_number}
        '''
        value = ClouddomainsRegistrationContactSettingsAdminContact(
            email=email,
            phone_number=phone_number,
            postal_address=postal_address,
            fax_number=fax_number,
        )

        return typing.cast(None, jsii.invoke(self, "putAdminContact", [value]))

    @jsii.member(jsii_name="putRegistrantContact")
    def put_registrant_contact(
        self,
        *,
        email: builtins.str,
        phone_number: builtins.str,
        postal_address: typing.Union["ClouddomainsRegistrationContactSettingsRegistrantContactPostalAddress", typing.Dict[builtins.str, typing.Any]],
        fax_number: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param email: Required. Email address of the contact. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#email ClouddomainsRegistration#email}
        :param phone_number: Required. Phone number of the contact in international format. For example, "+1-800-555-0123". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#phone_number ClouddomainsRegistration#phone_number}
        :param postal_address: postal_address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#postal_address ClouddomainsRegistration#postal_address}
        :param fax_number: Fax number of the contact in international format. For example, "+1-800-555-0123". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#fax_number ClouddomainsRegistration#fax_number}
        '''
        value = ClouddomainsRegistrationContactSettingsRegistrantContact(
            email=email,
            phone_number=phone_number,
            postal_address=postal_address,
            fax_number=fax_number,
        )

        return typing.cast(None, jsii.invoke(self, "putRegistrantContact", [value]))

    @jsii.member(jsii_name="putTechnicalContact")
    def put_technical_contact(
        self,
        *,
        email: builtins.str,
        phone_number: builtins.str,
        postal_address: typing.Union["ClouddomainsRegistrationContactSettingsTechnicalContactPostalAddress", typing.Dict[builtins.str, typing.Any]],
        fax_number: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param email: Required. Email address of the contact. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#email ClouddomainsRegistration#email}
        :param phone_number: Required. Phone number of the contact in international format. For example, "+1-800-555-0123". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#phone_number ClouddomainsRegistration#phone_number}
        :param postal_address: postal_address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#postal_address ClouddomainsRegistration#postal_address}
        :param fax_number: Fax number of the contact in international format. For example, "+1-800-555-0123". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#fax_number ClouddomainsRegistration#fax_number}
        '''
        value = ClouddomainsRegistrationContactSettingsTechnicalContact(
            email=email,
            phone_number=phone_number,
            postal_address=postal_address,
            fax_number=fax_number,
        )

        return typing.cast(None, jsii.invoke(self, "putTechnicalContact", [value]))

    @builtins.property
    @jsii.member(jsii_name="adminContact")
    def admin_contact(
        self,
    ) -> ClouddomainsRegistrationContactSettingsAdminContactOutputReference:
        return typing.cast(ClouddomainsRegistrationContactSettingsAdminContactOutputReference, jsii.get(self, "adminContact"))

    @builtins.property
    @jsii.member(jsii_name="registrantContact")
    def registrant_contact(
        self,
    ) -> "ClouddomainsRegistrationContactSettingsRegistrantContactOutputReference":
        return typing.cast("ClouddomainsRegistrationContactSettingsRegistrantContactOutputReference", jsii.get(self, "registrantContact"))

    @builtins.property
    @jsii.member(jsii_name="technicalContact")
    def technical_contact(
        self,
    ) -> "ClouddomainsRegistrationContactSettingsTechnicalContactOutputReference":
        return typing.cast("ClouddomainsRegistrationContactSettingsTechnicalContactOutputReference", jsii.get(self, "technicalContact"))

    @builtins.property
    @jsii.member(jsii_name="adminContactInput")
    def admin_contact_input(
        self,
    ) -> typing.Optional[ClouddomainsRegistrationContactSettingsAdminContact]:
        return typing.cast(typing.Optional[ClouddomainsRegistrationContactSettingsAdminContact], jsii.get(self, "adminContactInput"))

    @builtins.property
    @jsii.member(jsii_name="privacyInput")
    def privacy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privacyInput"))

    @builtins.property
    @jsii.member(jsii_name="registrantContactInput")
    def registrant_contact_input(
        self,
    ) -> typing.Optional["ClouddomainsRegistrationContactSettingsRegistrantContact"]:
        return typing.cast(typing.Optional["ClouddomainsRegistrationContactSettingsRegistrantContact"], jsii.get(self, "registrantContactInput"))

    @builtins.property
    @jsii.member(jsii_name="technicalContactInput")
    def technical_contact_input(
        self,
    ) -> typing.Optional["ClouddomainsRegistrationContactSettingsTechnicalContact"]:
        return typing.cast(typing.Optional["ClouddomainsRegistrationContactSettingsTechnicalContact"], jsii.get(self, "technicalContactInput"))

    @builtins.property
    @jsii.member(jsii_name="privacy")
    def privacy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privacy"))

    @privacy.setter
    def privacy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feb24bb9425033921ac978ca36ab121d2344a605085decc4fbcfd63a19135af9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privacy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddomainsRegistrationContactSettings]:
        return typing.cast(typing.Optional[ClouddomainsRegistrationContactSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddomainsRegistrationContactSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13df58f12b50b8ac5c6ac02047b4e9626cc6c8a281df421d1f355edcbec90011)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddomainsRegistration.ClouddomainsRegistrationContactSettingsRegistrantContact",
    jsii_struct_bases=[],
    name_mapping={
        "email": "email",
        "phone_number": "phoneNumber",
        "postal_address": "postalAddress",
        "fax_number": "faxNumber",
    },
)
class ClouddomainsRegistrationContactSettingsRegistrantContact:
    def __init__(
        self,
        *,
        email: builtins.str,
        phone_number: builtins.str,
        postal_address: typing.Union["ClouddomainsRegistrationContactSettingsRegistrantContactPostalAddress", typing.Dict[builtins.str, typing.Any]],
        fax_number: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param email: Required. Email address of the contact. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#email ClouddomainsRegistration#email}
        :param phone_number: Required. Phone number of the contact in international format. For example, "+1-800-555-0123". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#phone_number ClouddomainsRegistration#phone_number}
        :param postal_address: postal_address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#postal_address ClouddomainsRegistration#postal_address}
        :param fax_number: Fax number of the contact in international format. For example, "+1-800-555-0123". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#fax_number ClouddomainsRegistration#fax_number}
        '''
        if isinstance(postal_address, dict):
            postal_address = ClouddomainsRegistrationContactSettingsRegistrantContactPostalAddress(**postal_address)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d5ed81707788bf3b701d0302032a1ccd44cf57d443142222f6ba55bb93e07e4)
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
            check_type(argname="argument postal_address", value=postal_address, expected_type=type_hints["postal_address"])
            check_type(argname="argument fax_number", value=fax_number, expected_type=type_hints["fax_number"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "email": email,
            "phone_number": phone_number,
            "postal_address": postal_address,
        }
        if fax_number is not None:
            self._values["fax_number"] = fax_number

    @builtins.property
    def email(self) -> builtins.str:
        '''Required. Email address of the contact.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#email ClouddomainsRegistration#email}
        '''
        result = self._values.get("email")
        assert result is not None, "Required property 'email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def phone_number(self) -> builtins.str:
        '''Required. Phone number of the contact in international format. For example, "+1-800-555-0123".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#phone_number ClouddomainsRegistration#phone_number}
        '''
        result = self._values.get("phone_number")
        assert result is not None, "Required property 'phone_number' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def postal_address(
        self,
    ) -> "ClouddomainsRegistrationContactSettingsRegistrantContactPostalAddress":
        '''postal_address block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#postal_address ClouddomainsRegistration#postal_address}
        '''
        result = self._values.get("postal_address")
        assert result is not None, "Required property 'postal_address' is missing"
        return typing.cast("ClouddomainsRegistrationContactSettingsRegistrantContactPostalAddress", result)

    @builtins.property
    def fax_number(self) -> typing.Optional[builtins.str]:
        '''Fax number of the contact in international format. For example, "+1-800-555-0123".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#fax_number ClouddomainsRegistration#fax_number}
        '''
        result = self._values.get("fax_number")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddomainsRegistrationContactSettingsRegistrantContact(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddomainsRegistrationContactSettingsRegistrantContactOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddomainsRegistration.ClouddomainsRegistrationContactSettingsRegistrantContactOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c0582a03214869bcee6e88a74d9d3156f5d1bf0b2bde0dafcda02ff789419d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPostalAddress")
    def put_postal_address(
        self,
        *,
        region_code: builtins.str,
        address_lines: typing.Optional[typing.Sequence[builtins.str]] = None,
        administrative_area: typing.Optional[builtins.str] = None,
        locality: typing.Optional[builtins.str] = None,
        organization: typing.Optional[builtins.str] = None,
        postal_code: typing.Optional[builtins.str] = None,
        recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param region_code: Required. CLDR region code of the country/region of the address. This is never inferred and it is up to the user to ensure the value is correct. See https://cldr.unicode.org/ and https://www.unicode.org/cldr/charts/30/supplemental/territory_information.html for details. Example: "CH" for Switzerland. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#region_code ClouddomainsRegistration#region_code}
        :param address_lines: Unstructured address lines describing the lower levels of an address. Because values in addressLines do not have type information and may sometimes contain multiple values in a single field (e.g. "Austin, TX"), it is important that the line order is clear. The order of address lines should be "envelope order" for the country/region of the address. In places where this can vary (e.g. Japan), address_language is used to make it explicit (e.g. "ja" for large-to-small ordering and "ja-Latn" or "en" for small-to-large). This way, the most specific line of an address can be selected based on the language. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#address_lines ClouddomainsRegistration#address_lines}
        :param administrative_area: Highest administrative subdivision which is used for postal addresses of a country or region. For example, this can be a state, a province, an oblast, or a prefecture. Specifically, for Spain this is the province and not the autonomous community (e.g. "Barcelona" and not "Catalonia"). Many countries don't use an administrative area in postal addresses. E.g. in Switzerland this should be left unpopulated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#administrative_area ClouddomainsRegistration#administrative_area}
        :param locality: Generally refers to the city/town portion of the address. Examples: US city, IT comune, UK post town. In regions of the world where localities are not well defined or do not fit into this structure well, leave locality empty and use addressLines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#locality ClouddomainsRegistration#locality}
        :param organization: The name of the organization at the address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#organization ClouddomainsRegistration#organization}
        :param postal_code: Postal code of the address. Not all countries use or require postal codes to be present, but where they are used, they may trigger additional validation with other parts of the address (e.g. state/zip validation in the U.S.A.). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#postal_code ClouddomainsRegistration#postal_code}
        :param recipients: The recipient at the address. This field may, under certain circumstances, contain multiline information. For example, it might contain "care of" information. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#recipients ClouddomainsRegistration#recipients}
        '''
        value = ClouddomainsRegistrationContactSettingsRegistrantContactPostalAddress(
            region_code=region_code,
            address_lines=address_lines,
            administrative_area=administrative_area,
            locality=locality,
            organization=organization,
            postal_code=postal_code,
            recipients=recipients,
        )

        return typing.cast(None, jsii.invoke(self, "putPostalAddress", [value]))

    @jsii.member(jsii_name="resetFaxNumber")
    def reset_fax_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFaxNumber", []))

    @builtins.property
    @jsii.member(jsii_name="postalAddress")
    def postal_address(
        self,
    ) -> "ClouddomainsRegistrationContactSettingsRegistrantContactPostalAddressOutputReference":
        return typing.cast("ClouddomainsRegistrationContactSettingsRegistrantContactPostalAddressOutputReference", jsii.get(self, "postalAddress"))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="faxNumberInput")
    def fax_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "faxNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="phoneNumberInput")
    def phone_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "phoneNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="postalAddressInput")
    def postal_address_input(
        self,
    ) -> typing.Optional["ClouddomainsRegistrationContactSettingsRegistrantContactPostalAddress"]:
        return typing.cast(typing.Optional["ClouddomainsRegistrationContactSettingsRegistrantContactPostalAddress"], jsii.get(self, "postalAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66d1c9cf65e17014fa967fa9cfc0197a1f3d54213ac90c98c86b3181939f595f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="faxNumber")
    def fax_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "faxNumber"))

    @fax_number.setter
    def fax_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8192181af9d7c0f25c5c55be6f59f54fda78e63b8040952f570a54a1a6fd2020)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "faxNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="phoneNumber")
    def phone_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "phoneNumber"))

    @phone_number.setter
    def phone_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb067a2f2c6e256a921ee10db25019de053dad7562a092253e678b5cf1160f16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "phoneNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddomainsRegistrationContactSettingsRegistrantContact]:
        return typing.cast(typing.Optional[ClouddomainsRegistrationContactSettingsRegistrantContact], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddomainsRegistrationContactSettingsRegistrantContact],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f6806c081c51b4dc8145edc53ee776e6858c789d8b8e444ab591c74cdab69db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddomainsRegistration.ClouddomainsRegistrationContactSettingsRegistrantContactPostalAddress",
    jsii_struct_bases=[],
    name_mapping={
        "region_code": "regionCode",
        "address_lines": "addressLines",
        "administrative_area": "administrativeArea",
        "locality": "locality",
        "organization": "organization",
        "postal_code": "postalCode",
        "recipients": "recipients",
    },
)
class ClouddomainsRegistrationContactSettingsRegistrantContactPostalAddress:
    def __init__(
        self,
        *,
        region_code: builtins.str,
        address_lines: typing.Optional[typing.Sequence[builtins.str]] = None,
        administrative_area: typing.Optional[builtins.str] = None,
        locality: typing.Optional[builtins.str] = None,
        organization: typing.Optional[builtins.str] = None,
        postal_code: typing.Optional[builtins.str] = None,
        recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param region_code: Required. CLDR region code of the country/region of the address. This is never inferred and it is up to the user to ensure the value is correct. See https://cldr.unicode.org/ and https://www.unicode.org/cldr/charts/30/supplemental/territory_information.html for details. Example: "CH" for Switzerland. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#region_code ClouddomainsRegistration#region_code}
        :param address_lines: Unstructured address lines describing the lower levels of an address. Because values in addressLines do not have type information and may sometimes contain multiple values in a single field (e.g. "Austin, TX"), it is important that the line order is clear. The order of address lines should be "envelope order" for the country/region of the address. In places where this can vary (e.g. Japan), address_language is used to make it explicit (e.g. "ja" for large-to-small ordering and "ja-Latn" or "en" for small-to-large). This way, the most specific line of an address can be selected based on the language. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#address_lines ClouddomainsRegistration#address_lines}
        :param administrative_area: Highest administrative subdivision which is used for postal addresses of a country or region. For example, this can be a state, a province, an oblast, or a prefecture. Specifically, for Spain this is the province and not the autonomous community (e.g. "Barcelona" and not "Catalonia"). Many countries don't use an administrative area in postal addresses. E.g. in Switzerland this should be left unpopulated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#administrative_area ClouddomainsRegistration#administrative_area}
        :param locality: Generally refers to the city/town portion of the address. Examples: US city, IT comune, UK post town. In regions of the world where localities are not well defined or do not fit into this structure well, leave locality empty and use addressLines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#locality ClouddomainsRegistration#locality}
        :param organization: The name of the organization at the address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#organization ClouddomainsRegistration#organization}
        :param postal_code: Postal code of the address. Not all countries use or require postal codes to be present, but where they are used, they may trigger additional validation with other parts of the address (e.g. state/zip validation in the U.S.A.). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#postal_code ClouddomainsRegistration#postal_code}
        :param recipients: The recipient at the address. This field may, under certain circumstances, contain multiline information. For example, it might contain "care of" information. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#recipients ClouddomainsRegistration#recipients}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1c185c1a7c0329f322ef817c16991b86d0c30d45d63d50f0b78e234514fcd07)
            check_type(argname="argument region_code", value=region_code, expected_type=type_hints["region_code"])
            check_type(argname="argument address_lines", value=address_lines, expected_type=type_hints["address_lines"])
            check_type(argname="argument administrative_area", value=administrative_area, expected_type=type_hints["administrative_area"])
            check_type(argname="argument locality", value=locality, expected_type=type_hints["locality"])
            check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
            check_type(argname="argument postal_code", value=postal_code, expected_type=type_hints["postal_code"])
            check_type(argname="argument recipients", value=recipients, expected_type=type_hints["recipients"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "region_code": region_code,
        }
        if address_lines is not None:
            self._values["address_lines"] = address_lines
        if administrative_area is not None:
            self._values["administrative_area"] = administrative_area
        if locality is not None:
            self._values["locality"] = locality
        if organization is not None:
            self._values["organization"] = organization
        if postal_code is not None:
            self._values["postal_code"] = postal_code
        if recipients is not None:
            self._values["recipients"] = recipients

    @builtins.property
    def region_code(self) -> builtins.str:
        '''Required.

        CLDR region code of the country/region of the address. This is never inferred and it is up to the user to
        ensure the value is correct. See https://cldr.unicode.org/ and
        https://www.unicode.org/cldr/charts/30/supplemental/territory_information.html for details. Example: "CH" for Switzerland.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#region_code ClouddomainsRegistration#region_code}
        '''
        result = self._values.get("region_code")
        assert result is not None, "Required property 'region_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def address_lines(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Unstructured address lines describing the lower levels of an address.

        Because values in addressLines do not have type information and may sometimes contain multiple values in a single
        field (e.g. "Austin, TX"), it is important that the line order is clear. The order of address lines should be
        "envelope order" for the country/region of the address. In places where this can vary (e.g. Japan), address_language
        is used to make it explicit (e.g. "ja" for large-to-small ordering and "ja-Latn" or "en" for small-to-large). This way,
        the most specific line of an address can be selected based on the language.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#address_lines ClouddomainsRegistration#address_lines}
        '''
        result = self._values.get("address_lines")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def administrative_area(self) -> typing.Optional[builtins.str]:
        '''Highest administrative subdivision which is used for postal addresses of a country or region.

        For example, this can be a state,
        a province, an oblast, or a prefecture. Specifically, for Spain this is the province and not the autonomous community
        (e.g. "Barcelona" and not "Catalonia"). Many countries don't use an administrative area in postal addresses. E.g. in Switzerland
        this should be left unpopulated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#administrative_area ClouddomainsRegistration#administrative_area}
        '''
        result = self._values.get("administrative_area")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def locality(self) -> typing.Optional[builtins.str]:
        '''Generally refers to the city/town portion of the address.

        Examples: US city, IT comune, UK post town. In regions of the world
        where localities are not well defined or do not fit into this structure well, leave locality empty and use addressLines.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#locality ClouddomainsRegistration#locality}
        '''
        result = self._values.get("locality")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organization(self) -> typing.Optional[builtins.str]:
        '''The name of the organization at the address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#organization ClouddomainsRegistration#organization}
        '''
        result = self._values.get("organization")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def postal_code(self) -> typing.Optional[builtins.str]:
        '''Postal code of the address.

        Not all countries use or require postal codes to be present, but where they are used,
        they may trigger additional validation with other parts of the address (e.g. state/zip validation in the U.S.A.).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#postal_code ClouddomainsRegistration#postal_code}
        '''
        result = self._values.get("postal_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recipients(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The recipient at the address.

        This field may, under certain circumstances, contain multiline information. For example,
        it might contain "care of" information.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#recipients ClouddomainsRegistration#recipients}
        '''
        result = self._values.get("recipients")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddomainsRegistrationContactSettingsRegistrantContactPostalAddress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddomainsRegistrationContactSettingsRegistrantContactPostalAddressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddomainsRegistration.ClouddomainsRegistrationContactSettingsRegistrantContactPostalAddressOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9c17e5ee2dd38c0cc96b7cf47813a0b828013e3279f1bd59893f9ae619d5343)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAddressLines")
    def reset_address_lines(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddressLines", []))

    @jsii.member(jsii_name="resetAdministrativeArea")
    def reset_administrative_area(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdministrativeArea", []))

    @jsii.member(jsii_name="resetLocality")
    def reset_locality(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocality", []))

    @jsii.member(jsii_name="resetOrganization")
    def reset_organization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrganization", []))

    @jsii.member(jsii_name="resetPostalCode")
    def reset_postal_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostalCode", []))

    @jsii.member(jsii_name="resetRecipients")
    def reset_recipients(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecipients", []))

    @builtins.property
    @jsii.member(jsii_name="addressLinesInput")
    def address_lines_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "addressLinesInput"))

    @builtins.property
    @jsii.member(jsii_name="administrativeAreaInput")
    def administrative_area_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "administrativeAreaInput"))

    @builtins.property
    @jsii.member(jsii_name="localityInput")
    def locality_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localityInput"))

    @builtins.property
    @jsii.member(jsii_name="organizationInput")
    def organization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationInput"))

    @builtins.property
    @jsii.member(jsii_name="postalCodeInput")
    def postal_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "postalCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="recipientsInput")
    def recipients_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "recipientsInput"))

    @builtins.property
    @jsii.member(jsii_name="regionCodeInput")
    def region_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="addressLines")
    def address_lines(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "addressLines"))

    @address_lines.setter
    def address_lines(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bae11e41fadf17ce42681d45fb83ce4326f279fb44bfb34dfda27a3270a3a942)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addressLines", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="administrativeArea")
    def administrative_area(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "administrativeArea"))

    @administrative_area.setter
    def administrative_area(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05ea1b1a553be1d97169839ef34b654edf1cc1d56f45d2ab70c0f1621ffd055b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "administrativeArea", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="locality")
    def locality(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "locality"))

    @locality.setter
    def locality(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e797bc0aa4c7673ee766ae7dafd27122590bf8b10b6b014b2cc8f772d1ed67ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locality", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf4dcc0cbea9c4fcb2c4f1d6a0b418f6f83a5b0349539834f8f233fc4f7fd984)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postalCode")
    def postal_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postalCode"))

    @postal_code.setter
    def postal_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1e957a4fcfb3a85afd33d4b597309ef4945c6018f1dc7247adc345eb0061947)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postalCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recipients")
    def recipients(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "recipients"))

    @recipients.setter
    def recipients(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a037e9780387ebd792358f6f866b860898982adf1b3ddbf80b5bdfe1ad6f6e8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regionCode")
    def region_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regionCode"))

    @region_code.setter
    def region_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a4dc843d82c730bb457fbb6f09f4d2abfd5ad8bef504e0dd5bda36961452ed9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regionCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddomainsRegistrationContactSettingsRegistrantContactPostalAddress]:
        return typing.cast(typing.Optional[ClouddomainsRegistrationContactSettingsRegistrantContactPostalAddress], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddomainsRegistrationContactSettingsRegistrantContactPostalAddress],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40daab1266114cf6a2204e501054f8427a3756b95a9cabde9d812637a8752bf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddomainsRegistration.ClouddomainsRegistrationContactSettingsTechnicalContact",
    jsii_struct_bases=[],
    name_mapping={
        "email": "email",
        "phone_number": "phoneNumber",
        "postal_address": "postalAddress",
        "fax_number": "faxNumber",
    },
)
class ClouddomainsRegistrationContactSettingsTechnicalContact:
    def __init__(
        self,
        *,
        email: builtins.str,
        phone_number: builtins.str,
        postal_address: typing.Union["ClouddomainsRegistrationContactSettingsTechnicalContactPostalAddress", typing.Dict[builtins.str, typing.Any]],
        fax_number: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param email: Required. Email address of the contact. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#email ClouddomainsRegistration#email}
        :param phone_number: Required. Phone number of the contact in international format. For example, "+1-800-555-0123". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#phone_number ClouddomainsRegistration#phone_number}
        :param postal_address: postal_address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#postal_address ClouddomainsRegistration#postal_address}
        :param fax_number: Fax number of the contact in international format. For example, "+1-800-555-0123". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#fax_number ClouddomainsRegistration#fax_number}
        '''
        if isinstance(postal_address, dict):
            postal_address = ClouddomainsRegistrationContactSettingsTechnicalContactPostalAddress(**postal_address)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5b7e784d50c14ffd9022c35883869bd33230a11a584f3783422c9a3ac03a696)
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
            check_type(argname="argument postal_address", value=postal_address, expected_type=type_hints["postal_address"])
            check_type(argname="argument fax_number", value=fax_number, expected_type=type_hints["fax_number"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "email": email,
            "phone_number": phone_number,
            "postal_address": postal_address,
        }
        if fax_number is not None:
            self._values["fax_number"] = fax_number

    @builtins.property
    def email(self) -> builtins.str:
        '''Required. Email address of the contact.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#email ClouddomainsRegistration#email}
        '''
        result = self._values.get("email")
        assert result is not None, "Required property 'email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def phone_number(self) -> builtins.str:
        '''Required. Phone number of the contact in international format. For example, "+1-800-555-0123".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#phone_number ClouddomainsRegistration#phone_number}
        '''
        result = self._values.get("phone_number")
        assert result is not None, "Required property 'phone_number' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def postal_address(
        self,
    ) -> "ClouddomainsRegistrationContactSettingsTechnicalContactPostalAddress":
        '''postal_address block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#postal_address ClouddomainsRegistration#postal_address}
        '''
        result = self._values.get("postal_address")
        assert result is not None, "Required property 'postal_address' is missing"
        return typing.cast("ClouddomainsRegistrationContactSettingsTechnicalContactPostalAddress", result)

    @builtins.property
    def fax_number(self) -> typing.Optional[builtins.str]:
        '''Fax number of the contact in international format. For example, "+1-800-555-0123".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#fax_number ClouddomainsRegistration#fax_number}
        '''
        result = self._values.get("fax_number")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddomainsRegistrationContactSettingsTechnicalContact(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddomainsRegistrationContactSettingsTechnicalContactOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddomainsRegistration.ClouddomainsRegistrationContactSettingsTechnicalContactOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4137a07c62cdaf0c2260e07338ac333f5fcc62e4324ecc1fadeb787ebbdfc57)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPostalAddress")
    def put_postal_address(
        self,
        *,
        region_code: builtins.str,
        address_lines: typing.Optional[typing.Sequence[builtins.str]] = None,
        administrative_area: typing.Optional[builtins.str] = None,
        locality: typing.Optional[builtins.str] = None,
        organization: typing.Optional[builtins.str] = None,
        postal_code: typing.Optional[builtins.str] = None,
        recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param region_code: Required. CLDR region code of the country/region of the address. This is never inferred and it is up to the user to ensure the value is correct. See https://cldr.unicode.org/ and https://www.unicode.org/cldr/charts/30/supplemental/territory_information.html for details. Example: "CH" for Switzerland. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#region_code ClouddomainsRegistration#region_code}
        :param address_lines: Unstructured address lines describing the lower levels of an address. Because values in addressLines do not have type information and may sometimes contain multiple values in a single field (e.g. "Austin, TX"), it is important that the line order is clear. The order of address lines should be "envelope order" for the country/region of the address. In places where this can vary (e.g. Japan), address_language is used to make it explicit (e.g. "ja" for large-to-small ordering and "ja-Latn" or "en" for small-to-large). This way, the most specific line of an address can be selected based on the language. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#address_lines ClouddomainsRegistration#address_lines}
        :param administrative_area: Highest administrative subdivision which is used for postal addresses of a country or region. For example, this can be a state, a province, an oblast, or a prefecture. Specifically, for Spain this is the province and not the autonomous community (e.g. "Barcelona" and not "Catalonia"). Many countries don't use an administrative area in postal addresses. E.g. in Switzerland this should be left unpopulated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#administrative_area ClouddomainsRegistration#administrative_area}
        :param locality: Generally refers to the city/town portion of the address. Examples: US city, IT comune, UK post town. In regions of the world where localities are not well defined or do not fit into this structure well, leave locality empty and use addressLines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#locality ClouddomainsRegistration#locality}
        :param organization: The name of the organization at the address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#organization ClouddomainsRegistration#organization}
        :param postal_code: Postal code of the address. Not all countries use or require postal codes to be present, but where they are used, they may trigger additional validation with other parts of the address (e.g. state/zip validation in the U.S.A.). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#postal_code ClouddomainsRegistration#postal_code}
        :param recipients: The recipient at the address. This field may, under certain circumstances, contain multiline information. For example, it might contain "care of" information. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#recipients ClouddomainsRegistration#recipients}
        '''
        value = ClouddomainsRegistrationContactSettingsTechnicalContactPostalAddress(
            region_code=region_code,
            address_lines=address_lines,
            administrative_area=administrative_area,
            locality=locality,
            organization=organization,
            postal_code=postal_code,
            recipients=recipients,
        )

        return typing.cast(None, jsii.invoke(self, "putPostalAddress", [value]))

    @jsii.member(jsii_name="resetFaxNumber")
    def reset_fax_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFaxNumber", []))

    @builtins.property
    @jsii.member(jsii_name="postalAddress")
    def postal_address(
        self,
    ) -> "ClouddomainsRegistrationContactSettingsTechnicalContactPostalAddressOutputReference":
        return typing.cast("ClouddomainsRegistrationContactSettingsTechnicalContactPostalAddressOutputReference", jsii.get(self, "postalAddress"))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="faxNumberInput")
    def fax_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "faxNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="phoneNumberInput")
    def phone_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "phoneNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="postalAddressInput")
    def postal_address_input(
        self,
    ) -> typing.Optional["ClouddomainsRegistrationContactSettingsTechnicalContactPostalAddress"]:
        return typing.cast(typing.Optional["ClouddomainsRegistrationContactSettingsTechnicalContactPostalAddress"], jsii.get(self, "postalAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90b363d61285afa4ba82e53dc8de1a06c23ed749cbbae2d9b50cb4b5ab9aca79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="faxNumber")
    def fax_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "faxNumber"))

    @fax_number.setter
    def fax_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca57f7eabae9ab63c9dc0f653dc3ba13b1371d797b66c7eab802320276a094ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "faxNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="phoneNumber")
    def phone_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "phoneNumber"))

    @phone_number.setter
    def phone_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5042a13d800bd36118de6b31efc9c495bd9de3952650581264f5faebc4278401)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "phoneNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddomainsRegistrationContactSettingsTechnicalContact]:
        return typing.cast(typing.Optional[ClouddomainsRegistrationContactSettingsTechnicalContact], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddomainsRegistrationContactSettingsTechnicalContact],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b56d019bd682ef82fde7788c8882e78fba18d906330cf844d73cb954722b588)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddomainsRegistration.ClouddomainsRegistrationContactSettingsTechnicalContactPostalAddress",
    jsii_struct_bases=[],
    name_mapping={
        "region_code": "regionCode",
        "address_lines": "addressLines",
        "administrative_area": "administrativeArea",
        "locality": "locality",
        "organization": "organization",
        "postal_code": "postalCode",
        "recipients": "recipients",
    },
)
class ClouddomainsRegistrationContactSettingsTechnicalContactPostalAddress:
    def __init__(
        self,
        *,
        region_code: builtins.str,
        address_lines: typing.Optional[typing.Sequence[builtins.str]] = None,
        administrative_area: typing.Optional[builtins.str] = None,
        locality: typing.Optional[builtins.str] = None,
        organization: typing.Optional[builtins.str] = None,
        postal_code: typing.Optional[builtins.str] = None,
        recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param region_code: Required. CLDR region code of the country/region of the address. This is never inferred and it is up to the user to ensure the value is correct. See https://cldr.unicode.org/ and https://www.unicode.org/cldr/charts/30/supplemental/territory_information.html for details. Example: "CH" for Switzerland. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#region_code ClouddomainsRegistration#region_code}
        :param address_lines: Unstructured address lines describing the lower levels of an address. Because values in addressLines do not have type information and may sometimes contain multiple values in a single field (e.g. "Austin, TX"), it is important that the line order is clear. The order of address lines should be "envelope order" for the country/region of the address. In places where this can vary (e.g. Japan), address_language is used to make it explicit (e.g. "ja" for large-to-small ordering and "ja-Latn" or "en" for small-to-large). This way, the most specific line of an address can be selected based on the language. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#address_lines ClouddomainsRegistration#address_lines}
        :param administrative_area: Highest administrative subdivision which is used for postal addresses of a country or region. For example, this can be a state, a province, an oblast, or a prefecture. Specifically, for Spain this is the province and not the autonomous community (e.g. "Barcelona" and not "Catalonia"). Many countries don't use an administrative area in postal addresses. E.g. in Switzerland this should be left unpopulated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#administrative_area ClouddomainsRegistration#administrative_area}
        :param locality: Generally refers to the city/town portion of the address. Examples: US city, IT comune, UK post town. In regions of the world where localities are not well defined or do not fit into this structure well, leave locality empty and use addressLines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#locality ClouddomainsRegistration#locality}
        :param organization: The name of the organization at the address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#organization ClouddomainsRegistration#organization}
        :param postal_code: Postal code of the address. Not all countries use or require postal codes to be present, but where they are used, they may trigger additional validation with other parts of the address (e.g. state/zip validation in the U.S.A.). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#postal_code ClouddomainsRegistration#postal_code}
        :param recipients: The recipient at the address. This field may, under certain circumstances, contain multiline information. For example, it might contain "care of" information. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#recipients ClouddomainsRegistration#recipients}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__380a1a4105d1c8b27ef85487c2ff40c0505d722f20f5938721ddfd66bd251b66)
            check_type(argname="argument region_code", value=region_code, expected_type=type_hints["region_code"])
            check_type(argname="argument address_lines", value=address_lines, expected_type=type_hints["address_lines"])
            check_type(argname="argument administrative_area", value=administrative_area, expected_type=type_hints["administrative_area"])
            check_type(argname="argument locality", value=locality, expected_type=type_hints["locality"])
            check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
            check_type(argname="argument postal_code", value=postal_code, expected_type=type_hints["postal_code"])
            check_type(argname="argument recipients", value=recipients, expected_type=type_hints["recipients"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "region_code": region_code,
        }
        if address_lines is not None:
            self._values["address_lines"] = address_lines
        if administrative_area is not None:
            self._values["administrative_area"] = administrative_area
        if locality is not None:
            self._values["locality"] = locality
        if organization is not None:
            self._values["organization"] = organization
        if postal_code is not None:
            self._values["postal_code"] = postal_code
        if recipients is not None:
            self._values["recipients"] = recipients

    @builtins.property
    def region_code(self) -> builtins.str:
        '''Required.

        CLDR region code of the country/region of the address. This is never inferred and it is up to the user to
        ensure the value is correct. See https://cldr.unicode.org/ and
        https://www.unicode.org/cldr/charts/30/supplemental/territory_information.html for details. Example: "CH" for Switzerland.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#region_code ClouddomainsRegistration#region_code}
        '''
        result = self._values.get("region_code")
        assert result is not None, "Required property 'region_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def address_lines(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Unstructured address lines describing the lower levels of an address.

        Because values in addressLines do not have type information and may sometimes contain multiple values in a single
        field (e.g. "Austin, TX"), it is important that the line order is clear. The order of address lines should be
        "envelope order" for the country/region of the address. In places where this can vary (e.g. Japan), address_language
        is used to make it explicit (e.g. "ja" for large-to-small ordering and "ja-Latn" or "en" for small-to-large). This way,
        the most specific line of an address can be selected based on the language.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#address_lines ClouddomainsRegistration#address_lines}
        '''
        result = self._values.get("address_lines")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def administrative_area(self) -> typing.Optional[builtins.str]:
        '''Highest administrative subdivision which is used for postal addresses of a country or region.

        For example, this can be a state,
        a province, an oblast, or a prefecture. Specifically, for Spain this is the province and not the autonomous community
        (e.g. "Barcelona" and not "Catalonia"). Many countries don't use an administrative area in postal addresses. E.g. in Switzerland
        this should be left unpopulated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#administrative_area ClouddomainsRegistration#administrative_area}
        '''
        result = self._values.get("administrative_area")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def locality(self) -> typing.Optional[builtins.str]:
        '''Generally refers to the city/town portion of the address.

        Examples: US city, IT comune, UK post town. In regions of the world
        where localities are not well defined or do not fit into this structure well, leave locality empty and use addressLines.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#locality ClouddomainsRegistration#locality}
        '''
        result = self._values.get("locality")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organization(self) -> typing.Optional[builtins.str]:
        '''The name of the organization at the address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#organization ClouddomainsRegistration#organization}
        '''
        result = self._values.get("organization")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def postal_code(self) -> typing.Optional[builtins.str]:
        '''Postal code of the address.

        Not all countries use or require postal codes to be present, but where they are used,
        they may trigger additional validation with other parts of the address (e.g. state/zip validation in the U.S.A.).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#postal_code ClouddomainsRegistration#postal_code}
        '''
        result = self._values.get("postal_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recipients(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The recipient at the address.

        This field may, under certain circumstances, contain multiline information. For example,
        it might contain "care of" information.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#recipients ClouddomainsRegistration#recipients}
        '''
        result = self._values.get("recipients")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddomainsRegistrationContactSettingsTechnicalContactPostalAddress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddomainsRegistrationContactSettingsTechnicalContactPostalAddressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddomainsRegistration.ClouddomainsRegistrationContactSettingsTechnicalContactPostalAddressOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c373793d165e991b71ee26ab4a016da9c618e67bc15da46732dce7292b25d047)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAddressLines")
    def reset_address_lines(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddressLines", []))

    @jsii.member(jsii_name="resetAdministrativeArea")
    def reset_administrative_area(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdministrativeArea", []))

    @jsii.member(jsii_name="resetLocality")
    def reset_locality(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocality", []))

    @jsii.member(jsii_name="resetOrganization")
    def reset_organization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrganization", []))

    @jsii.member(jsii_name="resetPostalCode")
    def reset_postal_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostalCode", []))

    @jsii.member(jsii_name="resetRecipients")
    def reset_recipients(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecipients", []))

    @builtins.property
    @jsii.member(jsii_name="addressLinesInput")
    def address_lines_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "addressLinesInput"))

    @builtins.property
    @jsii.member(jsii_name="administrativeAreaInput")
    def administrative_area_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "administrativeAreaInput"))

    @builtins.property
    @jsii.member(jsii_name="localityInput")
    def locality_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localityInput"))

    @builtins.property
    @jsii.member(jsii_name="organizationInput")
    def organization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationInput"))

    @builtins.property
    @jsii.member(jsii_name="postalCodeInput")
    def postal_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "postalCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="recipientsInput")
    def recipients_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "recipientsInput"))

    @builtins.property
    @jsii.member(jsii_name="regionCodeInput")
    def region_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="addressLines")
    def address_lines(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "addressLines"))

    @address_lines.setter
    def address_lines(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17337aee4651a3de54e36603148c75c91390e281410f9b60808afb654f4f80c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addressLines", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="administrativeArea")
    def administrative_area(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "administrativeArea"))

    @administrative_area.setter
    def administrative_area(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52d026b12de163c1fd050a163978ae40351a1d4d9578d99d57d19f7f0381e12d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "administrativeArea", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="locality")
    def locality(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "locality"))

    @locality.setter
    def locality(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3c97a4e91f440b4a618b06319b1b218738141375509d66d9353e9079a829075)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locality", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4220f19636d8889d04f7929db0e45ac15145e9b4de5a4c42ddc007ec778c1486)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postalCode")
    def postal_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postalCode"))

    @postal_code.setter
    def postal_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63c2870bbcb94b5345587848224605b48d8868f83db8728b64477e9cc093a605)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postalCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recipients")
    def recipients(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "recipients"))

    @recipients.setter
    def recipients(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c371b721f3789e588e6473766bde470c0b2a06bb40e25ab8ad97a4bea85df96b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regionCode")
    def region_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regionCode"))

    @region_code.setter
    def region_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddb79f2817f6202d63978a47d0a73c54cdfc89b1e35b4dfc88411a5a7283d7c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regionCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddomainsRegistrationContactSettingsTechnicalContactPostalAddress]:
        return typing.cast(typing.Optional[ClouddomainsRegistrationContactSettingsTechnicalContactPostalAddress], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddomainsRegistrationContactSettingsTechnicalContactPostalAddress],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70c051a2626eb4ca7a59fe83a29ef918c4b903ecd49d80f1f2477ba1f6a176b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddomainsRegistration.ClouddomainsRegistrationDnsSettings",
    jsii_struct_bases=[],
    name_mapping={"custom_dns": "customDns", "glue_records": "glueRecords"},
)
class ClouddomainsRegistrationDnsSettings:
    def __init__(
        self,
        *,
        custom_dns: typing.Optional[typing.Union["ClouddomainsRegistrationDnsSettingsCustomDns", typing.Dict[builtins.str, typing.Any]]] = None,
        glue_records: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddomainsRegistrationDnsSettingsGlueRecords", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param custom_dns: custom_dns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#custom_dns ClouddomainsRegistration#custom_dns}
        :param glue_records: glue_records block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#glue_records ClouddomainsRegistration#glue_records}
        '''
        if isinstance(custom_dns, dict):
            custom_dns = ClouddomainsRegistrationDnsSettingsCustomDns(**custom_dns)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc294b2cc57d9980e69ff5fff7027a57e7f69578696d233d7e8f11b267626889)
            check_type(argname="argument custom_dns", value=custom_dns, expected_type=type_hints["custom_dns"])
            check_type(argname="argument glue_records", value=glue_records, expected_type=type_hints["glue_records"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_dns is not None:
            self._values["custom_dns"] = custom_dns
        if glue_records is not None:
            self._values["glue_records"] = glue_records

    @builtins.property
    def custom_dns(
        self,
    ) -> typing.Optional["ClouddomainsRegistrationDnsSettingsCustomDns"]:
        '''custom_dns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#custom_dns ClouddomainsRegistration#custom_dns}
        '''
        result = self._values.get("custom_dns")
        return typing.cast(typing.Optional["ClouddomainsRegistrationDnsSettingsCustomDns"], result)

    @builtins.property
    def glue_records(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddomainsRegistrationDnsSettingsGlueRecords"]]]:
        '''glue_records block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#glue_records ClouddomainsRegistration#glue_records}
        '''
        result = self._values.get("glue_records")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddomainsRegistrationDnsSettingsGlueRecords"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddomainsRegistrationDnsSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddomainsRegistration.ClouddomainsRegistrationDnsSettingsCustomDns",
    jsii_struct_bases=[],
    name_mapping={"name_servers": "nameServers", "ds_records": "dsRecords"},
)
class ClouddomainsRegistrationDnsSettingsCustomDns:
    def __init__(
        self,
        *,
        name_servers: typing.Sequence[builtins.str],
        ds_records: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddomainsRegistrationDnsSettingsCustomDnsDsRecords", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name_servers: Required. A list of name servers that store the DNS zone for this domain. Each name server is a domain name, with Unicode domain names expressed in Punycode format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#name_servers ClouddomainsRegistration#name_servers}
        :param ds_records: ds_records block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#ds_records ClouddomainsRegistration#ds_records}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e8929209a505a213c7f37b768f4ef652a2b7537bba4204db494ade026f12a41)
            check_type(argname="argument name_servers", value=name_servers, expected_type=type_hints["name_servers"])
            check_type(argname="argument ds_records", value=ds_records, expected_type=type_hints["ds_records"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name_servers": name_servers,
        }
        if ds_records is not None:
            self._values["ds_records"] = ds_records

    @builtins.property
    def name_servers(self) -> typing.List[builtins.str]:
        '''Required.

        A list of name servers that store the DNS zone for this domain. Each name server is a domain
        name, with Unicode domain names expressed in Punycode format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#name_servers ClouddomainsRegistration#name_servers}
        '''
        result = self._values.get("name_servers")
        assert result is not None, "Required property 'name_servers' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def ds_records(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddomainsRegistrationDnsSettingsCustomDnsDsRecords"]]]:
        '''ds_records block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#ds_records ClouddomainsRegistration#ds_records}
        '''
        result = self._values.get("ds_records")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddomainsRegistrationDnsSettingsCustomDnsDsRecords"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddomainsRegistrationDnsSettingsCustomDns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddomainsRegistration.ClouddomainsRegistrationDnsSettingsCustomDnsDsRecords",
    jsii_struct_bases=[],
    name_mapping={
        "algorithm": "algorithm",
        "digest": "digest",
        "digest_type": "digestType",
        "key_tag": "keyTag",
    },
)
class ClouddomainsRegistrationDnsSettingsCustomDnsDsRecords:
    def __init__(
        self,
        *,
        algorithm: typing.Optional[builtins.str] = None,
        digest: typing.Optional[builtins.str] = None,
        digest_type: typing.Optional[builtins.str] = None,
        key_tag: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param algorithm: The algorithm used to generate the referenced DNSKEY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#algorithm ClouddomainsRegistration#algorithm}
        :param digest: The digest generated from the referenced DNSKEY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#digest ClouddomainsRegistration#digest}
        :param digest_type: The hash function used to generate the digest of the referenced DNSKEY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#digest_type ClouddomainsRegistration#digest_type}
        :param key_tag: The key tag of the record. Must be set in range 0 -- 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#key_tag ClouddomainsRegistration#key_tag}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34b3ce1306e664a75a36ecc27ef390bc07ce39cb1a76acaba36bc2a1fc87351d)
            check_type(argname="argument algorithm", value=algorithm, expected_type=type_hints["algorithm"])
            check_type(argname="argument digest", value=digest, expected_type=type_hints["digest"])
            check_type(argname="argument digest_type", value=digest_type, expected_type=type_hints["digest_type"])
            check_type(argname="argument key_tag", value=key_tag, expected_type=type_hints["key_tag"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if algorithm is not None:
            self._values["algorithm"] = algorithm
        if digest is not None:
            self._values["digest"] = digest
        if digest_type is not None:
            self._values["digest_type"] = digest_type
        if key_tag is not None:
            self._values["key_tag"] = key_tag

    @builtins.property
    def algorithm(self) -> typing.Optional[builtins.str]:
        '''The algorithm used to generate the referenced DNSKEY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#algorithm ClouddomainsRegistration#algorithm}
        '''
        result = self._values.get("algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def digest(self) -> typing.Optional[builtins.str]:
        '''The digest generated from the referenced DNSKEY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#digest ClouddomainsRegistration#digest}
        '''
        result = self._values.get("digest")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def digest_type(self) -> typing.Optional[builtins.str]:
        '''The hash function used to generate the digest of the referenced DNSKEY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#digest_type ClouddomainsRegistration#digest_type}
        '''
        result = self._values.get("digest_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_tag(self) -> typing.Optional[jsii.Number]:
        '''The key tag of the record. Must be set in range 0 -- 65535.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#key_tag ClouddomainsRegistration#key_tag}
        '''
        result = self._values.get("key_tag")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddomainsRegistrationDnsSettingsCustomDnsDsRecords(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddomainsRegistrationDnsSettingsCustomDnsDsRecordsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddomainsRegistration.ClouddomainsRegistrationDnsSettingsCustomDnsDsRecordsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c940d0b14bad3a88d05c0343acbd08754ac3f77c221836798e9dd47581d3e91)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ClouddomainsRegistrationDnsSettingsCustomDnsDsRecordsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd847afc6a9d848e702e0ab6eaa298ffff104a18abb01b286cce99152c88a906)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ClouddomainsRegistrationDnsSettingsCustomDnsDsRecordsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__149f1fef57262f3ac3c652b43104bffed4455295f8f3fd84bd9798fd969d7929)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f327347f497b636d8dac9c970f51184ace40d94905cdf7ed85f362ec7d3aee8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b9679183a105a5efdbb1c0c334d4e93eed51ba153ff03ab2bbb93d37e9e21d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddomainsRegistrationDnsSettingsCustomDnsDsRecords]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddomainsRegistrationDnsSettingsCustomDnsDsRecords]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddomainsRegistrationDnsSettingsCustomDnsDsRecords]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16508832150870b39a86e9a0cb0bc375c25e2bad0c02a4ea2f9a38362b7733a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ClouddomainsRegistrationDnsSettingsCustomDnsDsRecordsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddomainsRegistration.ClouddomainsRegistrationDnsSettingsCustomDnsDsRecordsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__05b5899315c0af470ec6c150a3dff7daf1ea36f8720f2045d17981bf7ad0a97a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAlgorithm")
    def reset_algorithm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlgorithm", []))

    @jsii.member(jsii_name="resetDigest")
    def reset_digest(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDigest", []))

    @jsii.member(jsii_name="resetDigestType")
    def reset_digest_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDigestType", []))

    @jsii.member(jsii_name="resetKeyTag")
    def reset_key_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyTag", []))

    @builtins.property
    @jsii.member(jsii_name="algorithmInput")
    def algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "algorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="digestInput")
    def digest_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "digestInput"))

    @builtins.property
    @jsii.member(jsii_name="digestTypeInput")
    def digest_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "digestTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="keyTagInput")
    def key_tag_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "keyTagInput"))

    @builtins.property
    @jsii.member(jsii_name="algorithm")
    def algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "algorithm"))

    @algorithm.setter
    def algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4fc550b17079f5fe9d6add5acb7acf92caacabfa1883cd7e90d0b07834970c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "algorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="digest")
    def digest(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "digest"))

    @digest.setter
    def digest(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7555c0d597fa79ebb1fb37a9cf3bc62e459cf0cb2c8905b4aea3c73da9776807)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "digest", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="digestType")
    def digest_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "digestType"))

    @digest_type.setter
    def digest_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abc29fc9a5ef2ad1b65d5016d86098160112a934a8263753c65e3c9bfa54dc40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "digestType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyTag")
    def key_tag(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "keyTag"))

    @key_tag.setter
    def key_tag(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47255938cb08a5d2a52e74535b040075c51b8e75065ea6410fdbec927ad626bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyTag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddomainsRegistrationDnsSettingsCustomDnsDsRecords]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddomainsRegistrationDnsSettingsCustomDnsDsRecords]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddomainsRegistrationDnsSettingsCustomDnsDsRecords]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c31b905c511221b77f8096871310e18d70aa3c481966575f909ccb7832dff84b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ClouddomainsRegistrationDnsSettingsCustomDnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddomainsRegistration.ClouddomainsRegistrationDnsSettingsCustomDnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__53476dc67e5dd1972bfa6b26f4ed47c24bb7fa34cd8e5c486600ba641074705a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDsRecords")
    def put_ds_records(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddomainsRegistrationDnsSettingsCustomDnsDsRecords, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad2c9d50b6c0d9cb3730b67fe7bea44d92130b6ac686789b3564039a621aa89c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDsRecords", [value]))

    @jsii.member(jsii_name="resetDsRecords")
    def reset_ds_records(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDsRecords", []))

    @builtins.property
    @jsii.member(jsii_name="dsRecords")
    def ds_records(self) -> ClouddomainsRegistrationDnsSettingsCustomDnsDsRecordsList:
        return typing.cast(ClouddomainsRegistrationDnsSettingsCustomDnsDsRecordsList, jsii.get(self, "dsRecords"))

    @builtins.property
    @jsii.member(jsii_name="dsRecordsInput")
    def ds_records_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddomainsRegistrationDnsSettingsCustomDnsDsRecords]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddomainsRegistrationDnsSettingsCustomDnsDsRecords]]], jsii.get(self, "dsRecordsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameServersInput")
    def name_servers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "nameServersInput"))

    @builtins.property
    @jsii.member(jsii_name="nameServers")
    def name_servers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "nameServers"))

    @name_servers.setter
    def name_servers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dedb1f89df8431e201dd79a36d6d92b9a3241e6ceedea6498a5c02a4bc6f17d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nameServers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddomainsRegistrationDnsSettingsCustomDns]:
        return typing.cast(typing.Optional[ClouddomainsRegistrationDnsSettingsCustomDns], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddomainsRegistrationDnsSettingsCustomDns],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9c785b6efb5de5d428686a8f3794176de9ad1124b41ac667a08d34c54434776)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddomainsRegistration.ClouddomainsRegistrationDnsSettingsGlueRecords",
    jsii_struct_bases=[],
    name_mapping={
        "host_name": "hostName",
        "ipv4_addresses": "ipv4Addresses",
        "ipv6_addresses": "ipv6Addresses",
    },
)
class ClouddomainsRegistrationDnsSettingsGlueRecords:
    def __init__(
        self,
        *,
        host_name: builtins.str,
        ipv4_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        ipv6_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param host_name: Required. Domain name of the host in Punycode format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#host_name ClouddomainsRegistration#host_name}
        :param ipv4_addresses: List of IPv4 addresses corresponding to this host in the standard decimal format (e.g. 198.51.100.1). At least one of ipv4_address and ipv6_address must be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#ipv4_addresses ClouddomainsRegistration#ipv4_addresses}
        :param ipv6_addresses: List of IPv4 addresses corresponding to this host in the standard decimal format (e.g. 198.51.100.1). At least one of ipv4_address and ipv6_address must be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#ipv6_addresses ClouddomainsRegistration#ipv6_addresses}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5f0b46c990d740fb1169e522767b250608aa388a50d98c367dba462fb16f098)
            check_type(argname="argument host_name", value=host_name, expected_type=type_hints["host_name"])
            check_type(argname="argument ipv4_addresses", value=ipv4_addresses, expected_type=type_hints["ipv4_addresses"])
            check_type(argname="argument ipv6_addresses", value=ipv6_addresses, expected_type=type_hints["ipv6_addresses"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host_name": host_name,
        }
        if ipv4_addresses is not None:
            self._values["ipv4_addresses"] = ipv4_addresses
        if ipv6_addresses is not None:
            self._values["ipv6_addresses"] = ipv6_addresses

    @builtins.property
    def host_name(self) -> builtins.str:
        '''Required. Domain name of the host in Punycode format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#host_name ClouddomainsRegistration#host_name}
        '''
        result = self._values.get("host_name")
        assert result is not None, "Required property 'host_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ipv4_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of IPv4 addresses corresponding to this host in the standard decimal format (e.g. 198.51.100.1). At least one of ipv4_address and ipv6_address must be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#ipv4_addresses ClouddomainsRegistration#ipv4_addresses}
        '''
        result = self._values.get("ipv4_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ipv6_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of IPv4 addresses corresponding to this host in the standard decimal format (e.g. 198.51.100.1). At least one of ipv4_address and ipv6_address must be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#ipv6_addresses ClouddomainsRegistration#ipv6_addresses}
        '''
        result = self._values.get("ipv6_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddomainsRegistrationDnsSettingsGlueRecords(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddomainsRegistrationDnsSettingsGlueRecordsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddomainsRegistration.ClouddomainsRegistrationDnsSettingsGlueRecordsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f96b11891a17427868c7693a53775282ac81f106ccb5024d2cbef03328b01d0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ClouddomainsRegistrationDnsSettingsGlueRecordsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3863c5b67a3b219ffb79156fc9fe7bd82a398366ec65b5d3404e8fbaa88bb708)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ClouddomainsRegistrationDnsSettingsGlueRecordsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83bdd1443630fa000be3a1858e07bd2a3a11419c3a0d6442afaab0d8ca81e600)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62b3635bd302d82963b8009bd6086154a620e0f3c4232e712d76d0899fb0c695)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2afa24387c701f306fb33ca512dd53999b8bf83104b46d2fd3a1261d08cf2ee0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddomainsRegistrationDnsSettingsGlueRecords]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddomainsRegistrationDnsSettingsGlueRecords]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddomainsRegistrationDnsSettingsGlueRecords]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4143c0874e25971e536792679e892a870e142c63c68772b1093d599dac82768a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ClouddomainsRegistrationDnsSettingsGlueRecordsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddomainsRegistration.ClouddomainsRegistrationDnsSettingsGlueRecordsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7127ec183a025126413a64feb10d1a1cfa11bb7a91ef7aae69b22062f8df4446)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIpv4Addresses")
    def reset_ipv4_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv4Addresses", []))

    @jsii.member(jsii_name="resetIpv6Addresses")
    def reset_ipv6_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv6Addresses", []))

    @builtins.property
    @jsii.member(jsii_name="hostNameInput")
    def host_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostNameInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv4AddressesInput")
    def ipv4_addresses_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipv4AddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv6AddressesInput")
    def ipv6_addresses_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipv6AddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="hostName")
    def host_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostName"))

    @host_name.setter
    def host_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2f0e7e6fa16dda6df4a0f724d5e041ba6894ff3d8dfd74a05546bfe6d84cdbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipv4Addresses")
    def ipv4_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipv4Addresses"))

    @ipv4_addresses.setter
    def ipv4_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fba2c74ac43c1c0f5c717f0a872f372aa467ac59a5a772a464e954087ab6685)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv4Addresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipv6Addresses")
    def ipv6_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipv6Addresses"))

    @ipv6_addresses.setter
    def ipv6_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c37cabefaee5adc8a68bdcae23dc9a554668dd1441bb38982945333684a3f71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv6Addresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddomainsRegistrationDnsSettingsGlueRecords]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddomainsRegistrationDnsSettingsGlueRecords]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddomainsRegistrationDnsSettingsGlueRecords]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4eb34a41bd0783c3355ba6e13df7e22a84566a45bf768a95a12e0cd110b2f22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ClouddomainsRegistrationDnsSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddomainsRegistration.ClouddomainsRegistrationDnsSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__24b13cd203dc8297f607caadcafdbb7f4245127f0d334796e068918f707ab95a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomDns")
    def put_custom_dns(
        self,
        *,
        name_servers: typing.Sequence[builtins.str],
        ds_records: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddomainsRegistrationDnsSettingsCustomDnsDsRecords, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name_servers: Required. A list of name servers that store the DNS zone for this domain. Each name server is a domain name, with Unicode domain names expressed in Punycode format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#name_servers ClouddomainsRegistration#name_servers}
        :param ds_records: ds_records block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#ds_records ClouddomainsRegistration#ds_records}
        '''
        value = ClouddomainsRegistrationDnsSettingsCustomDns(
            name_servers=name_servers, ds_records=ds_records
        )

        return typing.cast(None, jsii.invoke(self, "putCustomDns", [value]))

    @jsii.member(jsii_name="putGlueRecords")
    def put_glue_records(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddomainsRegistrationDnsSettingsGlueRecords, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17743f0aba8e675a7d73255da01d76c0d82fb00e51ff2a8ff1d052d873dcbacd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGlueRecords", [value]))

    @jsii.member(jsii_name="resetCustomDns")
    def reset_custom_dns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomDns", []))

    @jsii.member(jsii_name="resetGlueRecords")
    def reset_glue_records(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGlueRecords", []))

    @builtins.property
    @jsii.member(jsii_name="customDns")
    def custom_dns(self) -> ClouddomainsRegistrationDnsSettingsCustomDnsOutputReference:
        return typing.cast(ClouddomainsRegistrationDnsSettingsCustomDnsOutputReference, jsii.get(self, "customDns"))

    @builtins.property
    @jsii.member(jsii_name="glueRecords")
    def glue_records(self) -> ClouddomainsRegistrationDnsSettingsGlueRecordsList:
        return typing.cast(ClouddomainsRegistrationDnsSettingsGlueRecordsList, jsii.get(self, "glueRecords"))

    @builtins.property
    @jsii.member(jsii_name="customDnsInput")
    def custom_dns_input(
        self,
    ) -> typing.Optional[ClouddomainsRegistrationDnsSettingsCustomDns]:
        return typing.cast(typing.Optional[ClouddomainsRegistrationDnsSettingsCustomDns], jsii.get(self, "customDnsInput"))

    @builtins.property
    @jsii.member(jsii_name="glueRecordsInput")
    def glue_records_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddomainsRegistrationDnsSettingsGlueRecords]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddomainsRegistrationDnsSettingsGlueRecords]]], jsii.get(self, "glueRecordsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ClouddomainsRegistrationDnsSettings]:
        return typing.cast(typing.Optional[ClouddomainsRegistrationDnsSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddomainsRegistrationDnsSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc8d06531505e46477abea7f1f1e72f36e070b5cab8b82f8501f773212ca509e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddomainsRegistration.ClouddomainsRegistrationManagementSettings",
    jsii_struct_bases=[],
    name_mapping={
        "preferred_renewal_method": "preferredRenewalMethod",
        "transfer_lock_state": "transferLockState",
    },
)
class ClouddomainsRegistrationManagementSettings:
    def __init__(
        self,
        *,
        preferred_renewal_method: typing.Optional[builtins.str] = None,
        transfer_lock_state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param preferred_renewal_method: The desired renewal method for this Registration. The actual renewalMethod is automatically updated to reflect this choice. If unset or equal to RENEWAL_METHOD_UNSPECIFIED, the actual renewalMethod is treated as if it were set to AUTOMATIC_RENEWAL. You cannot use RENEWAL_DISABLED during resource creation, and you can update the renewal status only when the Registration resource has state ACTIVE or SUSPENDED. When preferredRenewalMethod is set to AUTOMATIC_RENEWAL, the actual renewalMethod can be set to RENEWAL_DISABLED in case of problems with the billing account or reported domain abuse. In such cases, check the issues field on the Registration. After the problem is resolved, the renewalMethod is automatically updated to preferredRenewalMethod in a few hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#preferred_renewal_method ClouddomainsRegistration#preferred_renewal_method}
        :param transfer_lock_state: Controls whether the domain can be transferred to another registrar. Values are UNLOCKED or LOCKED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#transfer_lock_state ClouddomainsRegistration#transfer_lock_state}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b196aa18227e1b5830a5ebd6f16720070df67968acf92630202c3c76de23b762)
            check_type(argname="argument preferred_renewal_method", value=preferred_renewal_method, expected_type=type_hints["preferred_renewal_method"])
            check_type(argname="argument transfer_lock_state", value=transfer_lock_state, expected_type=type_hints["transfer_lock_state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if preferred_renewal_method is not None:
            self._values["preferred_renewal_method"] = preferred_renewal_method
        if transfer_lock_state is not None:
            self._values["transfer_lock_state"] = transfer_lock_state

    @builtins.property
    def preferred_renewal_method(self) -> typing.Optional[builtins.str]:
        '''The desired renewal method for this Registration.

        The actual renewalMethod is automatically updated to reflect this choice.
        If unset or equal to RENEWAL_METHOD_UNSPECIFIED, the actual renewalMethod is treated as if it were set to AUTOMATIC_RENEWAL.
        You cannot use RENEWAL_DISABLED during resource creation, and you can update the renewal status only when the Registration
        resource has state ACTIVE or SUSPENDED.

        When preferredRenewalMethod is set to AUTOMATIC_RENEWAL, the actual renewalMethod can be set to RENEWAL_DISABLED in case of
        problems with the billing account or reported domain abuse. In such cases, check the issues field on the Registration. After
        the problem is resolved, the renewalMethod is automatically updated to preferredRenewalMethod in a few hours.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#preferred_renewal_method ClouddomainsRegistration#preferred_renewal_method}
        '''
        result = self._values.get("preferred_renewal_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transfer_lock_state(self) -> typing.Optional[builtins.str]:
        '''Controls whether the domain can be transferred to another registrar. Values are UNLOCKED or LOCKED.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#transfer_lock_state ClouddomainsRegistration#transfer_lock_state}
        '''
        result = self._values.get("transfer_lock_state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddomainsRegistrationManagementSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddomainsRegistrationManagementSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddomainsRegistration.ClouddomainsRegistrationManagementSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fd1f0516797d3d2f062683dd31bcf27d97d571f1e97c023d73af82a1f05224d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPreferredRenewalMethod")
    def reset_preferred_renewal_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreferredRenewalMethod", []))

    @jsii.member(jsii_name="resetTransferLockState")
    def reset_transfer_lock_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransferLockState", []))

    @builtins.property
    @jsii.member(jsii_name="renewalMethod")
    def renewal_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "renewalMethod"))

    @builtins.property
    @jsii.member(jsii_name="preferredRenewalMethodInput")
    def preferred_renewal_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preferredRenewalMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="transferLockStateInput")
    def transfer_lock_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transferLockStateInput"))

    @builtins.property
    @jsii.member(jsii_name="preferredRenewalMethod")
    def preferred_renewal_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preferredRenewalMethod"))

    @preferred_renewal_method.setter
    def preferred_renewal_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fa2b51a6f439f4dbc8e305ac65958578ae7c73f9f6eb91f0b40b5dd9e613642)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredRenewalMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transferLockState")
    def transfer_lock_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transferLockState"))

    @transfer_lock_state.setter
    def transfer_lock_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2af9607592d62660cc76ec94cae056dec6c357418cf8213001547599685133a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transferLockState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddomainsRegistrationManagementSettings]:
        return typing.cast(typing.Optional[ClouddomainsRegistrationManagementSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddomainsRegistrationManagementSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f54f3706da008727560f5986fca22412042c7e3f16fd1b84b0e294b7f726f66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddomainsRegistration.ClouddomainsRegistrationTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ClouddomainsRegistrationTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#create ClouddomainsRegistration#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#delete ClouddomainsRegistration#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#update ClouddomainsRegistration#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f02c268faad452d046f804ffe50005c480d350faeac235af3b1d38862cd02901)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#create ClouddomainsRegistration#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#delete ClouddomainsRegistration#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#update ClouddomainsRegistration#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddomainsRegistrationTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddomainsRegistrationTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddomainsRegistration.ClouddomainsRegistrationTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a16e4b1484f2d1f87b3ac9478df37999f39909eb82b519507e2203e4cc2589fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c188961031916280920b2f7cd8c0fb02397c686b839fdf714e3b896dbd26689e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c1f0441f0a4913c9ce3975c0e70c13d1da46920373f226c30ce6a1d28428b46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b32659d2993aec428bac187700c00740753590ecb8bef8a5f53f52e2b93606e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddomainsRegistrationTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddomainsRegistrationTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddomainsRegistrationTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f09a39cacffb04fde9e13084229b85045dc373b544a8f5094e5f136e7964040c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddomainsRegistration.ClouddomainsRegistrationYearlyPrice",
    jsii_struct_bases=[],
    name_mapping={"currency_code": "currencyCode", "units": "units"},
)
class ClouddomainsRegistrationYearlyPrice:
    def __init__(
        self,
        *,
        currency_code: typing.Optional[builtins.str] = None,
        units: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param currency_code: The three-letter currency code defined in ISO 4217. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#currency_code ClouddomainsRegistration#currency_code}
        :param units: The whole units of the amount. For example if currencyCode is "USD", then 1 unit is one US dollar. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#units ClouddomainsRegistration#units}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fb9e8a83bee1ee0b568f8e1208833448a395658546f0adc8310ec4db142aca3)
            check_type(argname="argument currency_code", value=currency_code, expected_type=type_hints["currency_code"])
            check_type(argname="argument units", value=units, expected_type=type_hints["units"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if currency_code is not None:
            self._values["currency_code"] = currency_code
        if units is not None:
            self._values["units"] = units

    @builtins.property
    def currency_code(self) -> typing.Optional[builtins.str]:
        '''The three-letter currency code defined in ISO 4217.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#currency_code ClouddomainsRegistration#currency_code}
        '''
        result = self._values.get("currency_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def units(self) -> typing.Optional[builtins.str]:
        '''The whole units of the amount. For example if currencyCode is "USD", then 1 unit is one US dollar.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddomains_registration#units ClouddomainsRegistration#units}
        '''
        result = self._values.get("units")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddomainsRegistrationYearlyPrice(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddomainsRegistrationYearlyPriceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddomainsRegistration.ClouddomainsRegistrationYearlyPriceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__abba2d8218817920879bef8c3f0ce8caffb85774d86dbad8a15fa61c38380847)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCurrencyCode")
    def reset_currency_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCurrencyCode", []))

    @jsii.member(jsii_name="resetUnits")
    def reset_units(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnits", []))

    @builtins.property
    @jsii.member(jsii_name="currencyCodeInput")
    def currency_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "currencyCodeInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b3af387139919ac23e913d697c4291cc37ba3a731a5faffb0a9a63541e4c0820)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "currencyCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="units")
    def units(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "units"))

    @units.setter
    def units(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4cc316b4ab6bbdbc34d2a83570c871feb68e520cd4868b275f6fa2be8a78b85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "units", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ClouddomainsRegistrationYearlyPrice]:
        return typing.cast(typing.Optional[ClouddomainsRegistrationYearlyPrice], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddomainsRegistrationYearlyPrice],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8bd378a7e91118db4b40ad16930031cfddc7203e843307c694c311f30b4519e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ClouddomainsRegistration",
    "ClouddomainsRegistrationConfig",
    "ClouddomainsRegistrationContactSettings",
    "ClouddomainsRegistrationContactSettingsAdminContact",
    "ClouddomainsRegistrationContactSettingsAdminContactOutputReference",
    "ClouddomainsRegistrationContactSettingsAdminContactPostalAddress",
    "ClouddomainsRegistrationContactSettingsAdminContactPostalAddressOutputReference",
    "ClouddomainsRegistrationContactSettingsOutputReference",
    "ClouddomainsRegistrationContactSettingsRegistrantContact",
    "ClouddomainsRegistrationContactSettingsRegistrantContactOutputReference",
    "ClouddomainsRegistrationContactSettingsRegistrantContactPostalAddress",
    "ClouddomainsRegistrationContactSettingsRegistrantContactPostalAddressOutputReference",
    "ClouddomainsRegistrationContactSettingsTechnicalContact",
    "ClouddomainsRegistrationContactSettingsTechnicalContactOutputReference",
    "ClouddomainsRegistrationContactSettingsTechnicalContactPostalAddress",
    "ClouddomainsRegistrationContactSettingsTechnicalContactPostalAddressOutputReference",
    "ClouddomainsRegistrationDnsSettings",
    "ClouddomainsRegistrationDnsSettingsCustomDns",
    "ClouddomainsRegistrationDnsSettingsCustomDnsDsRecords",
    "ClouddomainsRegistrationDnsSettingsCustomDnsDsRecordsList",
    "ClouddomainsRegistrationDnsSettingsCustomDnsDsRecordsOutputReference",
    "ClouddomainsRegistrationDnsSettingsCustomDnsOutputReference",
    "ClouddomainsRegistrationDnsSettingsGlueRecords",
    "ClouddomainsRegistrationDnsSettingsGlueRecordsList",
    "ClouddomainsRegistrationDnsSettingsGlueRecordsOutputReference",
    "ClouddomainsRegistrationDnsSettingsOutputReference",
    "ClouddomainsRegistrationManagementSettings",
    "ClouddomainsRegistrationManagementSettingsOutputReference",
    "ClouddomainsRegistrationTimeouts",
    "ClouddomainsRegistrationTimeoutsOutputReference",
    "ClouddomainsRegistrationYearlyPrice",
    "ClouddomainsRegistrationYearlyPriceOutputReference",
]

publication.publish()

def _typecheckingstub__797180f5e86841aa5231a2ad92501266a7b765412dd26f59e71420c6ee7eb103(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    contact_settings: typing.Union[ClouddomainsRegistrationContactSettings, typing.Dict[builtins.str, typing.Any]],
    domain_name: builtins.str,
    location: builtins.str,
    yearly_price: typing.Union[ClouddomainsRegistrationYearlyPrice, typing.Dict[builtins.str, typing.Any]],
    contact_notices: typing.Optional[typing.Sequence[builtins.str]] = None,
    dns_settings: typing.Optional[typing.Union[ClouddomainsRegistrationDnsSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    domain_notices: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    management_settings: typing.Optional[typing.Union[ClouddomainsRegistrationManagementSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ClouddomainsRegistrationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__4c3b295001a5b2903131a1a92b4d4051c0339cc237e38e5f70f9343fce5625f6(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe67f6d36b5126343db6838f57958dc5b1d7534cd96271ebe132c0be20cb978f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03556343706ea17df9b31535f564ab6825d9c8e84143d388fc0963bf6bfa85a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ced846c6a676ae88369813ab14ae872ce99b45f75f25f65db1739a585e146270(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a07777231090026382ac4379fd4f588e75b0d76a73faa8b8a9227571172048a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__857002739a0725cbe458979e24abcaae93c31ad81ac638e048ce6aaef697301a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c95942581a94bed2f504fdda49faad8b46ee9bc669385edf23190f294fec2491(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbc338db614a1afe8339d01999fa774c6932ee80c43d2f14c9a4a8dbbc42f00f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ecb79ef81f8b0639a535a81df958d20ebc053c2f0e500f559096b9ee2902eb4(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    contact_settings: typing.Union[ClouddomainsRegistrationContactSettings, typing.Dict[builtins.str, typing.Any]],
    domain_name: builtins.str,
    location: builtins.str,
    yearly_price: typing.Union[ClouddomainsRegistrationYearlyPrice, typing.Dict[builtins.str, typing.Any]],
    contact_notices: typing.Optional[typing.Sequence[builtins.str]] = None,
    dns_settings: typing.Optional[typing.Union[ClouddomainsRegistrationDnsSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    domain_notices: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    management_settings: typing.Optional[typing.Union[ClouddomainsRegistrationManagementSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ClouddomainsRegistrationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feb620fa3ac96d8237513d8f48436a0e2670d5849870990c51cd600488bfd787(
    *,
    admin_contact: typing.Union[ClouddomainsRegistrationContactSettingsAdminContact, typing.Dict[builtins.str, typing.Any]],
    privacy: builtins.str,
    registrant_contact: typing.Union[ClouddomainsRegistrationContactSettingsRegistrantContact, typing.Dict[builtins.str, typing.Any]],
    technical_contact: typing.Union[ClouddomainsRegistrationContactSettingsTechnicalContact, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7b305b99420c3033da38f4d9b0e24b7f3356ed46b47db72d1b0adf836a4cdd5(
    *,
    email: builtins.str,
    phone_number: builtins.str,
    postal_address: typing.Union[ClouddomainsRegistrationContactSettingsAdminContactPostalAddress, typing.Dict[builtins.str, typing.Any]],
    fax_number: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8e2eef09a8b0324f32b939001c16faf58042ff817e77e62e58f326aa2cfcdf9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ba42de934b4b35e32a20b7c377a6a371415c35738eb610afeb942f9fe5a5c10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__079b2ae850fcb4e2bf9cbe17a508a57ce170c09a97eecd057e88086642eef47b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be829bf5cb23499b928cce1960a958713b7b376c2af7f4a44615874de8f4a104(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac1f26d1b1ddca47921a0db985576e6fb5f533fa2a222accb6ab41844f6de3ea(
    value: typing.Optional[ClouddomainsRegistrationContactSettingsAdminContact],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30e724a55eacd414e0f0c016009a2381f14d4a1c6a4f1a8b678cbc84c7a8a093(
    *,
    region_code: builtins.str,
    address_lines: typing.Optional[typing.Sequence[builtins.str]] = None,
    administrative_area: typing.Optional[builtins.str] = None,
    locality: typing.Optional[builtins.str] = None,
    organization: typing.Optional[builtins.str] = None,
    postal_code: typing.Optional[builtins.str] = None,
    recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcbc64dae595f1de265c5de4d534fa2fef3bdbeb4c57f38fa0e3c938b0ecd1cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c248f9534d8b2679fe5e4674ba11b4e26ef5533cec4cd418fdc14008543834e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9c7b10b7b3a0ae478f95cee1fe483c2405c2b8d15e14b511ae93da8ec56ca8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71ccff810325a8f32345f9c0c59bf6d9c26209083fa2503b1e35a53eef6db961(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__783469c2c84e7ab06ae6d63689e1fe950cc5c08aef8ccded920aa5ce8b38692e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2b3a8c0da47372f24cbf45108878e4d556f9068690584ccbaccd7cfbb1ddccb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53adcc48f1b1eea0764050df56106186f565d6c867d9bfb62f6e5557eb9b6d07(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d2fdd624e5787ccd67a73a5cc70e7dd14f2314b0f9fab8339a4c507ab93d5e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__def86f6284230dcbafbbb3ac34e5d6abf8163d5d59eeecfcfed435cd4140f754(
    value: typing.Optional[ClouddomainsRegistrationContactSettingsAdminContactPostalAddress],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__142295ca10bac2b284b62d55e613ef1cd0c315e8b20b175e95b480e81153aad3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feb24bb9425033921ac978ca36ab121d2344a605085decc4fbcfd63a19135af9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13df58f12b50b8ac5c6ac02047b4e9626cc6c8a281df421d1f355edcbec90011(
    value: typing.Optional[ClouddomainsRegistrationContactSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d5ed81707788bf3b701d0302032a1ccd44cf57d443142222f6ba55bb93e07e4(
    *,
    email: builtins.str,
    phone_number: builtins.str,
    postal_address: typing.Union[ClouddomainsRegistrationContactSettingsRegistrantContactPostalAddress, typing.Dict[builtins.str, typing.Any]],
    fax_number: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c0582a03214869bcee6e88a74d9d3156f5d1bf0b2bde0dafcda02ff789419d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66d1c9cf65e17014fa967fa9cfc0197a1f3d54213ac90c98c86b3181939f595f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8192181af9d7c0f25c5c55be6f59f54fda78e63b8040952f570a54a1a6fd2020(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb067a2f2c6e256a921ee10db25019de053dad7562a092253e678b5cf1160f16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f6806c081c51b4dc8145edc53ee776e6858c789d8b8e444ab591c74cdab69db(
    value: typing.Optional[ClouddomainsRegistrationContactSettingsRegistrantContact],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1c185c1a7c0329f322ef817c16991b86d0c30d45d63d50f0b78e234514fcd07(
    *,
    region_code: builtins.str,
    address_lines: typing.Optional[typing.Sequence[builtins.str]] = None,
    administrative_area: typing.Optional[builtins.str] = None,
    locality: typing.Optional[builtins.str] = None,
    organization: typing.Optional[builtins.str] = None,
    postal_code: typing.Optional[builtins.str] = None,
    recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9c17e5ee2dd38c0cc96b7cf47813a0b828013e3279f1bd59893f9ae619d5343(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bae11e41fadf17ce42681d45fb83ce4326f279fb44bfb34dfda27a3270a3a942(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05ea1b1a553be1d97169839ef34b654edf1cc1d56f45d2ab70c0f1621ffd055b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e797bc0aa4c7673ee766ae7dafd27122590bf8b10b6b014b2cc8f772d1ed67ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf4dcc0cbea9c4fcb2c4f1d6a0b418f6f83a5b0349539834f8f233fc4f7fd984(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1e957a4fcfb3a85afd33d4b597309ef4945c6018f1dc7247adc345eb0061947(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a037e9780387ebd792358f6f866b860898982adf1b3ddbf80b5bdfe1ad6f6e8f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a4dc843d82c730bb457fbb6f09f4d2abfd5ad8bef504e0dd5bda36961452ed9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40daab1266114cf6a2204e501054f8427a3756b95a9cabde9d812637a8752bf4(
    value: typing.Optional[ClouddomainsRegistrationContactSettingsRegistrantContactPostalAddress],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5b7e784d50c14ffd9022c35883869bd33230a11a584f3783422c9a3ac03a696(
    *,
    email: builtins.str,
    phone_number: builtins.str,
    postal_address: typing.Union[ClouddomainsRegistrationContactSettingsTechnicalContactPostalAddress, typing.Dict[builtins.str, typing.Any]],
    fax_number: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4137a07c62cdaf0c2260e07338ac333f5fcc62e4324ecc1fadeb787ebbdfc57(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90b363d61285afa4ba82e53dc8de1a06c23ed749cbbae2d9b50cb4b5ab9aca79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca57f7eabae9ab63c9dc0f653dc3ba13b1371d797b66c7eab802320276a094ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5042a13d800bd36118de6b31efc9c495bd9de3952650581264f5faebc4278401(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b56d019bd682ef82fde7788c8882e78fba18d906330cf844d73cb954722b588(
    value: typing.Optional[ClouddomainsRegistrationContactSettingsTechnicalContact],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__380a1a4105d1c8b27ef85487c2ff40c0505d722f20f5938721ddfd66bd251b66(
    *,
    region_code: builtins.str,
    address_lines: typing.Optional[typing.Sequence[builtins.str]] = None,
    administrative_area: typing.Optional[builtins.str] = None,
    locality: typing.Optional[builtins.str] = None,
    organization: typing.Optional[builtins.str] = None,
    postal_code: typing.Optional[builtins.str] = None,
    recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c373793d165e991b71ee26ab4a016da9c618e67bc15da46732dce7292b25d047(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17337aee4651a3de54e36603148c75c91390e281410f9b60808afb654f4f80c7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52d026b12de163c1fd050a163978ae40351a1d4d9578d99d57d19f7f0381e12d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3c97a4e91f440b4a618b06319b1b218738141375509d66d9353e9079a829075(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4220f19636d8889d04f7929db0e45ac15145e9b4de5a4c42ddc007ec778c1486(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63c2870bbcb94b5345587848224605b48d8868f83db8728b64477e9cc093a605(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c371b721f3789e588e6473766bde470c0b2a06bb40e25ab8ad97a4bea85df96b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddb79f2817f6202d63978a47d0a73c54cdfc89b1e35b4dfc88411a5a7283d7c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70c051a2626eb4ca7a59fe83a29ef918c4b903ecd49d80f1f2477ba1f6a176b7(
    value: typing.Optional[ClouddomainsRegistrationContactSettingsTechnicalContactPostalAddress],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc294b2cc57d9980e69ff5fff7027a57e7f69578696d233d7e8f11b267626889(
    *,
    custom_dns: typing.Optional[typing.Union[ClouddomainsRegistrationDnsSettingsCustomDns, typing.Dict[builtins.str, typing.Any]]] = None,
    glue_records: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddomainsRegistrationDnsSettingsGlueRecords, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e8929209a505a213c7f37b768f4ef652a2b7537bba4204db494ade026f12a41(
    *,
    name_servers: typing.Sequence[builtins.str],
    ds_records: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddomainsRegistrationDnsSettingsCustomDnsDsRecords, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34b3ce1306e664a75a36ecc27ef390bc07ce39cb1a76acaba36bc2a1fc87351d(
    *,
    algorithm: typing.Optional[builtins.str] = None,
    digest: typing.Optional[builtins.str] = None,
    digest_type: typing.Optional[builtins.str] = None,
    key_tag: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c940d0b14bad3a88d05c0343acbd08754ac3f77c221836798e9dd47581d3e91(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd847afc6a9d848e702e0ab6eaa298ffff104a18abb01b286cce99152c88a906(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__149f1fef57262f3ac3c652b43104bffed4455295f8f3fd84bd9798fd969d7929(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f327347f497b636d8dac9c970f51184ace40d94905cdf7ed85f362ec7d3aee8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b9679183a105a5efdbb1c0c334d4e93eed51ba153ff03ab2bbb93d37e9e21d7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16508832150870b39a86e9a0cb0bc375c25e2bad0c02a4ea2f9a38362b7733a2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddomainsRegistrationDnsSettingsCustomDnsDsRecords]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05b5899315c0af470ec6c150a3dff7daf1ea36f8720f2045d17981bf7ad0a97a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4fc550b17079f5fe9d6add5acb7acf92caacabfa1883cd7e90d0b07834970c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7555c0d597fa79ebb1fb37a9cf3bc62e459cf0cb2c8905b4aea3c73da9776807(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abc29fc9a5ef2ad1b65d5016d86098160112a934a8263753c65e3c9bfa54dc40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47255938cb08a5d2a52e74535b040075c51b8e75065ea6410fdbec927ad626bd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c31b905c511221b77f8096871310e18d70aa3c481966575f909ccb7832dff84b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddomainsRegistrationDnsSettingsCustomDnsDsRecords]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53476dc67e5dd1972bfa6b26f4ed47c24bb7fa34cd8e5c486600ba641074705a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad2c9d50b6c0d9cb3730b67fe7bea44d92130b6ac686789b3564039a621aa89c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddomainsRegistrationDnsSettingsCustomDnsDsRecords, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dedb1f89df8431e201dd79a36d6d92b9a3241e6ceedea6498a5c02a4bc6f17d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9c785b6efb5de5d428686a8f3794176de9ad1124b41ac667a08d34c54434776(
    value: typing.Optional[ClouddomainsRegistrationDnsSettingsCustomDns],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5f0b46c990d740fb1169e522767b250608aa388a50d98c367dba462fb16f098(
    *,
    host_name: builtins.str,
    ipv4_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    ipv6_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f96b11891a17427868c7693a53775282ac81f106ccb5024d2cbef03328b01d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3863c5b67a3b219ffb79156fc9fe7bd82a398366ec65b5d3404e8fbaa88bb708(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83bdd1443630fa000be3a1858e07bd2a3a11419c3a0d6442afaab0d8ca81e600(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62b3635bd302d82963b8009bd6086154a620e0f3c4232e712d76d0899fb0c695(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2afa24387c701f306fb33ca512dd53999b8bf83104b46d2fd3a1261d08cf2ee0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4143c0874e25971e536792679e892a870e142c63c68772b1093d599dac82768a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddomainsRegistrationDnsSettingsGlueRecords]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7127ec183a025126413a64feb10d1a1cfa11bb7a91ef7aae69b22062f8df4446(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2f0e7e6fa16dda6df4a0f724d5e041ba6894ff3d8dfd74a05546bfe6d84cdbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fba2c74ac43c1c0f5c717f0a872f372aa467ac59a5a772a464e954087ab6685(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c37cabefaee5adc8a68bdcae23dc9a554668dd1441bb38982945333684a3f71(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4eb34a41bd0783c3355ba6e13df7e22a84566a45bf768a95a12e0cd110b2f22(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddomainsRegistrationDnsSettingsGlueRecords]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24b13cd203dc8297f607caadcafdbb7f4245127f0d334796e068918f707ab95a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17743f0aba8e675a7d73255da01d76c0d82fb00e51ff2a8ff1d052d873dcbacd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddomainsRegistrationDnsSettingsGlueRecords, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc8d06531505e46477abea7f1f1e72f36e070b5cab8b82f8501f773212ca509e(
    value: typing.Optional[ClouddomainsRegistrationDnsSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b196aa18227e1b5830a5ebd6f16720070df67968acf92630202c3c76de23b762(
    *,
    preferred_renewal_method: typing.Optional[builtins.str] = None,
    transfer_lock_state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fd1f0516797d3d2f062683dd31bcf27d97d571f1e97c023d73af82a1f05224d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fa2b51a6f439f4dbc8e305ac65958578ae7c73f9f6eb91f0b40b5dd9e613642(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2af9607592d62660cc76ec94cae056dec6c357418cf8213001547599685133a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f54f3706da008727560f5986fca22412042c7e3f16fd1b84b0e294b7f726f66(
    value: typing.Optional[ClouddomainsRegistrationManagementSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f02c268faad452d046f804ffe50005c480d350faeac235af3b1d38862cd02901(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a16e4b1484f2d1f87b3ac9478df37999f39909eb82b519507e2203e4cc2589fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c188961031916280920b2f7cd8c0fb02397c686b839fdf714e3b896dbd26689e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c1f0441f0a4913c9ce3975c0e70c13d1da46920373f226c30ce6a1d28428b46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b32659d2993aec428bac187700c00740753590ecb8bef8a5f53f52e2b93606e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f09a39cacffb04fde9e13084229b85045dc373b544a8f5094e5f136e7964040c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddomainsRegistrationTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fb9e8a83bee1ee0b568f8e1208833448a395658546f0adc8310ec4db142aca3(
    *,
    currency_code: typing.Optional[builtins.str] = None,
    units: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abba2d8218817920879bef8c3f0ce8caffb85774d86dbad8a15fa61c38380847(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3af387139919ac23e913d697c4291cc37ba3a731a5faffb0a9a63541e4c0820(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4cc316b4ab6bbdbc34d2a83570c871feb68e520cd4868b275f6fa2be8a78b85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8bd378a7e91118db4b40ad16930031cfddc7203e843307c694c311f30b4519e(
    value: typing.Optional[ClouddomainsRegistrationYearlyPrice],
) -> None:
    """Type checking stubs"""
    pass
