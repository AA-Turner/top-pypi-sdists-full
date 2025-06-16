r'''
# `google_clouddomains_registration`

Refer to the Terraform Registry for docs: [`google_clouddomains_registration`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration).
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


class GoogleClouddomainsRegistration(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddomainsRegistration.GoogleClouddomainsRegistration",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration google_clouddomains_registration}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        contact_settings: typing.Union["GoogleClouddomainsRegistrationContactSettings", typing.Dict[builtins.str, typing.Any]],
        domain_name: builtins.str,
        location: builtins.str,
        yearly_price: typing.Union["GoogleClouddomainsRegistrationYearlyPrice", typing.Dict[builtins.str, typing.Any]],
        contact_notices: typing.Optional[typing.Sequence[builtins.str]] = None,
        dns_settings: typing.Optional[typing.Union["GoogleClouddomainsRegistrationDnsSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        domain_notices: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        management_settings: typing.Optional[typing.Union["GoogleClouddomainsRegistrationManagementSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleClouddomainsRegistrationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration google_clouddomains_registration} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param contact_settings: contact_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#contact_settings GoogleClouddomainsRegistration#contact_settings}
        :param domain_name: Required. The domain name. Unicode domain names must be expressed in Punycode format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#domain_name GoogleClouddomainsRegistration#domain_name}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#location GoogleClouddomainsRegistration#location}
        :param yearly_price: yearly_price block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#yearly_price GoogleClouddomainsRegistration#yearly_price}
        :param contact_notices: The list of contact notices that the caller acknowledges. Possible value is PUBLIC_CONTACT_DATA_ACKNOWLEDGEMENT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#contact_notices GoogleClouddomainsRegistration#contact_notices}
        :param dns_settings: dns_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#dns_settings GoogleClouddomainsRegistration#dns_settings}
        :param domain_notices: The list of domain notices that you acknowledge. Possible value is HSTS_PRELOADED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#domain_notices GoogleClouddomainsRegistration#domain_notices}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#id GoogleClouddomainsRegistration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of labels associated with the Registration. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#labels GoogleClouddomainsRegistration#labels}
        :param management_settings: management_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#management_settings GoogleClouddomainsRegistration#management_settings}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#project GoogleClouddomainsRegistration#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#timeouts GoogleClouddomainsRegistration#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a294f3c4b9b346d91a080138301e3d471ce1b7240964a4113e9008bbaebe23bf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleClouddomainsRegistrationConfig(
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
        '''Generates CDKTF code for importing a GoogleClouddomainsRegistration resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleClouddomainsRegistration to import.
        :param import_from_id: The id of the existing GoogleClouddomainsRegistration that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleClouddomainsRegistration to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2972634334d652cf2fa1f36d2007a2bbd879ed0c098db633d3662e91b2729fa3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putContactSettings")
    def put_contact_settings(
        self,
        *,
        admin_contact: typing.Union["GoogleClouddomainsRegistrationContactSettingsAdminContact", typing.Dict[builtins.str, typing.Any]],
        privacy: builtins.str,
        registrant_contact: typing.Union["GoogleClouddomainsRegistrationContactSettingsRegistrantContact", typing.Dict[builtins.str, typing.Any]],
        technical_contact: typing.Union["GoogleClouddomainsRegistrationContactSettingsTechnicalContact", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param admin_contact: admin_contact block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#admin_contact GoogleClouddomainsRegistration#admin_contact}
        :param privacy: Required. Privacy setting for the contacts associated with the Registration. Values are PUBLIC_CONTACT_DATA, PRIVATE_CONTACT_DATA, and REDACTED_CONTACT_DATA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#privacy GoogleClouddomainsRegistration#privacy}
        :param registrant_contact: registrant_contact block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#registrant_contact GoogleClouddomainsRegistration#registrant_contact}
        :param technical_contact: technical_contact block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#technical_contact GoogleClouddomainsRegistration#technical_contact}
        '''
        value = GoogleClouddomainsRegistrationContactSettings(
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
        custom_dns: typing.Optional[typing.Union["GoogleClouddomainsRegistrationDnsSettingsCustomDns", typing.Dict[builtins.str, typing.Any]]] = None,
        glue_records: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddomainsRegistrationDnsSettingsGlueRecords", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param custom_dns: custom_dns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#custom_dns GoogleClouddomainsRegistration#custom_dns}
        :param glue_records: glue_records block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#glue_records GoogleClouddomainsRegistration#glue_records}
        '''
        value = GoogleClouddomainsRegistrationDnsSettings(
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
        :param preferred_renewal_method: The desired renewal method for this Registration. The actual renewalMethod is automatically updated to reflect this choice. If unset or equal to RENEWAL_METHOD_UNSPECIFIED, the actual renewalMethod is treated as if it were set to AUTOMATIC_RENEWAL. You cannot use RENEWAL_DISABLED during resource creation, and you can update the renewal status only when the Registration resource has state ACTIVE or SUSPENDED. When preferredRenewalMethod is set to AUTOMATIC_RENEWAL, the actual renewalMethod can be set to RENEWAL_DISABLED in case of problems with the billing account or reported domain abuse. In such cases, check the issues field on the Registration. After the problem is resolved, the renewalMethod is automatically updated to preferredRenewalMethod in a few hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#preferred_renewal_method GoogleClouddomainsRegistration#preferred_renewal_method}
        :param transfer_lock_state: Controls whether the domain can be transferred to another registrar. Values are UNLOCKED or LOCKED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#transfer_lock_state GoogleClouddomainsRegistration#transfer_lock_state}
        '''
        value = GoogleClouddomainsRegistrationManagementSettings(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#create GoogleClouddomainsRegistration#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#delete GoogleClouddomainsRegistration#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#update GoogleClouddomainsRegistration#update}.
        '''
        value = GoogleClouddomainsRegistrationTimeouts(
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
        :param currency_code: The three-letter currency code defined in ISO 4217. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#currency_code GoogleClouddomainsRegistration#currency_code}
        :param units: The whole units of the amount. For example if currencyCode is "USD", then 1 unit is one US dollar. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#units GoogleClouddomainsRegistration#units}
        '''
        value = GoogleClouddomainsRegistrationYearlyPrice(
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
    ) -> "GoogleClouddomainsRegistrationContactSettingsOutputReference":
        return typing.cast("GoogleClouddomainsRegistrationContactSettingsOutputReference", jsii.get(self, "contactSettings"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="dnsSettings")
    def dns_settings(
        self,
    ) -> "GoogleClouddomainsRegistrationDnsSettingsOutputReference":
        return typing.cast("GoogleClouddomainsRegistrationDnsSettingsOutputReference", jsii.get(self, "dnsSettings"))

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
    ) -> "GoogleClouddomainsRegistrationManagementSettingsOutputReference":
        return typing.cast("GoogleClouddomainsRegistrationManagementSettingsOutputReference", jsii.get(self, "managementSettings"))

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
    def timeouts(self) -> "GoogleClouddomainsRegistrationTimeoutsOutputReference":
        return typing.cast("GoogleClouddomainsRegistrationTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="yearlyPrice")
    def yearly_price(
        self,
    ) -> "GoogleClouddomainsRegistrationYearlyPriceOutputReference":
        return typing.cast("GoogleClouddomainsRegistrationYearlyPriceOutputReference", jsii.get(self, "yearlyPrice"))

    @builtins.property
    @jsii.member(jsii_name="contactNoticesInput")
    def contact_notices_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "contactNoticesInput"))

    @builtins.property
    @jsii.member(jsii_name="contactSettingsInput")
    def contact_settings_input(
        self,
    ) -> typing.Optional["GoogleClouddomainsRegistrationContactSettings"]:
        return typing.cast(typing.Optional["GoogleClouddomainsRegistrationContactSettings"], jsii.get(self, "contactSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsSettingsInput")
    def dns_settings_input(
        self,
    ) -> typing.Optional["GoogleClouddomainsRegistrationDnsSettings"]:
        return typing.cast(typing.Optional["GoogleClouddomainsRegistrationDnsSettings"], jsii.get(self, "dnsSettingsInput"))

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
    ) -> typing.Optional["GoogleClouddomainsRegistrationManagementSettings"]:
        return typing.cast(typing.Optional["GoogleClouddomainsRegistrationManagementSettings"], jsii.get(self, "managementSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleClouddomainsRegistrationTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleClouddomainsRegistrationTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="yearlyPriceInput")
    def yearly_price_input(
        self,
    ) -> typing.Optional["GoogleClouddomainsRegistrationYearlyPrice"]:
        return typing.cast(typing.Optional["GoogleClouddomainsRegistrationYearlyPrice"], jsii.get(self, "yearlyPriceInput"))

    @builtins.property
    @jsii.member(jsii_name="contactNotices")
    def contact_notices(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "contactNotices"))

    @contact_notices.setter
    def contact_notices(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc88e690c681c95612a0396ae35d492a7285cf7971451bfcb4d6a84594d3464a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contactNotices", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ca8df0416dad7d5a1a68712a06159554b370fb994072f32818e3bf3b85f7123)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainNotices")
    def domain_notices(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "domainNotices"))

    @domain_notices.setter
    def domain_notices(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9b8e8d2342bbfc76f63808d1643ef7dac00e95ae5d6eb6e8a41318184790a18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainNotices", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b1a6bbd9495599c7c30eebc77aaab3375ba5188f9aa960e2250d075b79d3667)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3d91705056092a57e24b5436f062ef96da07b144f9c9a382c28d1137d026934)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeb5963f209b68367ae0ab0f5180dd5076300d905c69682d34f4593e57ce504d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44d8790b6237ab8fe082fed4095c4f914796f58f417b1b243ca177ee42df87dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddomainsRegistration.GoogleClouddomainsRegistrationConfig",
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
class GoogleClouddomainsRegistrationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        contact_settings: typing.Union["GoogleClouddomainsRegistrationContactSettings", typing.Dict[builtins.str, typing.Any]],
        domain_name: builtins.str,
        location: builtins.str,
        yearly_price: typing.Union["GoogleClouddomainsRegistrationYearlyPrice", typing.Dict[builtins.str, typing.Any]],
        contact_notices: typing.Optional[typing.Sequence[builtins.str]] = None,
        dns_settings: typing.Optional[typing.Union["GoogleClouddomainsRegistrationDnsSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        domain_notices: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        management_settings: typing.Optional[typing.Union["GoogleClouddomainsRegistrationManagementSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleClouddomainsRegistrationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param contact_settings: contact_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#contact_settings GoogleClouddomainsRegistration#contact_settings}
        :param domain_name: Required. The domain name. Unicode domain names must be expressed in Punycode format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#domain_name GoogleClouddomainsRegistration#domain_name}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#location GoogleClouddomainsRegistration#location}
        :param yearly_price: yearly_price block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#yearly_price GoogleClouddomainsRegistration#yearly_price}
        :param contact_notices: The list of contact notices that the caller acknowledges. Possible value is PUBLIC_CONTACT_DATA_ACKNOWLEDGEMENT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#contact_notices GoogleClouddomainsRegistration#contact_notices}
        :param dns_settings: dns_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#dns_settings GoogleClouddomainsRegistration#dns_settings}
        :param domain_notices: The list of domain notices that you acknowledge. Possible value is HSTS_PRELOADED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#domain_notices GoogleClouddomainsRegistration#domain_notices}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#id GoogleClouddomainsRegistration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of labels associated with the Registration. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#labels GoogleClouddomainsRegistration#labels}
        :param management_settings: management_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#management_settings GoogleClouddomainsRegistration#management_settings}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#project GoogleClouddomainsRegistration#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#timeouts GoogleClouddomainsRegistration#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(contact_settings, dict):
            contact_settings = GoogleClouddomainsRegistrationContactSettings(**contact_settings)
        if isinstance(yearly_price, dict):
            yearly_price = GoogleClouddomainsRegistrationYearlyPrice(**yearly_price)
        if isinstance(dns_settings, dict):
            dns_settings = GoogleClouddomainsRegistrationDnsSettings(**dns_settings)
        if isinstance(management_settings, dict):
            management_settings = GoogleClouddomainsRegistrationManagementSettings(**management_settings)
        if isinstance(timeouts, dict):
            timeouts = GoogleClouddomainsRegistrationTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a9f9b868ef38d88583bf3ba632b566f8a2cc66c975b6665b4180dc4f22c0926)
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
    def contact_settings(self) -> "GoogleClouddomainsRegistrationContactSettings":
        '''contact_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#contact_settings GoogleClouddomainsRegistration#contact_settings}
        '''
        result = self._values.get("contact_settings")
        assert result is not None, "Required property 'contact_settings' is missing"
        return typing.cast("GoogleClouddomainsRegistrationContactSettings", result)

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''Required. The domain name. Unicode domain names must be expressed in Punycode format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#domain_name GoogleClouddomainsRegistration#domain_name}
        '''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#location GoogleClouddomainsRegistration#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def yearly_price(self) -> "GoogleClouddomainsRegistrationYearlyPrice":
        '''yearly_price block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#yearly_price GoogleClouddomainsRegistration#yearly_price}
        '''
        result = self._values.get("yearly_price")
        assert result is not None, "Required property 'yearly_price' is missing"
        return typing.cast("GoogleClouddomainsRegistrationYearlyPrice", result)

    @builtins.property
    def contact_notices(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of contact notices that the caller acknowledges. Possible value is PUBLIC_CONTACT_DATA_ACKNOWLEDGEMENT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#contact_notices GoogleClouddomainsRegistration#contact_notices}
        '''
        result = self._values.get("contact_notices")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dns_settings(
        self,
    ) -> typing.Optional["GoogleClouddomainsRegistrationDnsSettings"]:
        '''dns_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#dns_settings GoogleClouddomainsRegistration#dns_settings}
        '''
        result = self._values.get("dns_settings")
        return typing.cast(typing.Optional["GoogleClouddomainsRegistrationDnsSettings"], result)

    @builtins.property
    def domain_notices(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of domain notices that you acknowledge. Possible value is HSTS_PRELOADED.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#domain_notices GoogleClouddomainsRegistration#domain_notices}
        '''
        result = self._values.get("domain_notices")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#id GoogleClouddomainsRegistration#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#labels GoogleClouddomainsRegistration#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def management_settings(
        self,
    ) -> typing.Optional["GoogleClouddomainsRegistrationManagementSettings"]:
        '''management_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#management_settings GoogleClouddomainsRegistration#management_settings}
        '''
        result = self._values.get("management_settings")
        return typing.cast(typing.Optional["GoogleClouddomainsRegistrationManagementSettings"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#project GoogleClouddomainsRegistration#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleClouddomainsRegistrationTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#timeouts GoogleClouddomainsRegistration#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleClouddomainsRegistrationTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddomainsRegistrationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddomainsRegistration.GoogleClouddomainsRegistrationContactSettings",
    jsii_struct_bases=[],
    name_mapping={
        "admin_contact": "adminContact",
        "privacy": "privacy",
        "registrant_contact": "registrantContact",
        "technical_contact": "technicalContact",
    },
)
class GoogleClouddomainsRegistrationContactSettings:
    def __init__(
        self,
        *,
        admin_contact: typing.Union["GoogleClouddomainsRegistrationContactSettingsAdminContact", typing.Dict[builtins.str, typing.Any]],
        privacy: builtins.str,
        registrant_contact: typing.Union["GoogleClouddomainsRegistrationContactSettingsRegistrantContact", typing.Dict[builtins.str, typing.Any]],
        technical_contact: typing.Union["GoogleClouddomainsRegistrationContactSettingsTechnicalContact", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param admin_contact: admin_contact block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#admin_contact GoogleClouddomainsRegistration#admin_contact}
        :param privacy: Required. Privacy setting for the contacts associated with the Registration. Values are PUBLIC_CONTACT_DATA, PRIVATE_CONTACT_DATA, and REDACTED_CONTACT_DATA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#privacy GoogleClouddomainsRegistration#privacy}
        :param registrant_contact: registrant_contact block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#registrant_contact GoogleClouddomainsRegistration#registrant_contact}
        :param technical_contact: technical_contact block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#technical_contact GoogleClouddomainsRegistration#technical_contact}
        '''
        if isinstance(admin_contact, dict):
            admin_contact = GoogleClouddomainsRegistrationContactSettingsAdminContact(**admin_contact)
        if isinstance(registrant_contact, dict):
            registrant_contact = GoogleClouddomainsRegistrationContactSettingsRegistrantContact(**registrant_contact)
        if isinstance(technical_contact, dict):
            technical_contact = GoogleClouddomainsRegistrationContactSettingsTechnicalContact(**technical_contact)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83086f2e6e263e44dde92d6dbd525498676532ad8b5a9b00747e6cc33951c8d1)
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
    def admin_contact(
        self,
    ) -> "GoogleClouddomainsRegistrationContactSettingsAdminContact":
        '''admin_contact block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#admin_contact GoogleClouddomainsRegistration#admin_contact}
        '''
        result = self._values.get("admin_contact")
        assert result is not None, "Required property 'admin_contact' is missing"
        return typing.cast("GoogleClouddomainsRegistrationContactSettingsAdminContact", result)

    @builtins.property
    def privacy(self) -> builtins.str:
        '''Required. Privacy setting for the contacts associated with the Registration. Values are PUBLIC_CONTACT_DATA, PRIVATE_CONTACT_DATA, and REDACTED_CONTACT_DATA.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#privacy GoogleClouddomainsRegistration#privacy}
        '''
        result = self._values.get("privacy")
        assert result is not None, "Required property 'privacy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def registrant_contact(
        self,
    ) -> "GoogleClouddomainsRegistrationContactSettingsRegistrantContact":
        '''registrant_contact block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#registrant_contact GoogleClouddomainsRegistration#registrant_contact}
        '''
        result = self._values.get("registrant_contact")
        assert result is not None, "Required property 'registrant_contact' is missing"
        return typing.cast("GoogleClouddomainsRegistrationContactSettingsRegistrantContact", result)

    @builtins.property
    def technical_contact(
        self,
    ) -> "GoogleClouddomainsRegistrationContactSettingsTechnicalContact":
        '''technical_contact block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#technical_contact GoogleClouddomainsRegistration#technical_contact}
        '''
        result = self._values.get("technical_contact")
        assert result is not None, "Required property 'technical_contact' is missing"
        return typing.cast("GoogleClouddomainsRegistrationContactSettingsTechnicalContact", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddomainsRegistrationContactSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddomainsRegistration.GoogleClouddomainsRegistrationContactSettingsAdminContact",
    jsii_struct_bases=[],
    name_mapping={
        "email": "email",
        "phone_number": "phoneNumber",
        "postal_address": "postalAddress",
        "fax_number": "faxNumber",
    },
)
class GoogleClouddomainsRegistrationContactSettingsAdminContact:
    def __init__(
        self,
        *,
        email: builtins.str,
        phone_number: builtins.str,
        postal_address: typing.Union["GoogleClouddomainsRegistrationContactSettingsAdminContactPostalAddress", typing.Dict[builtins.str, typing.Any]],
        fax_number: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param email: Required. Email address of the contact. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#email GoogleClouddomainsRegistration#email}
        :param phone_number: Required. Phone number of the contact in international format. For example, "+1-800-555-0123". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#phone_number GoogleClouddomainsRegistration#phone_number}
        :param postal_address: postal_address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#postal_address GoogleClouddomainsRegistration#postal_address}
        :param fax_number: Fax number of the contact in international format. For example, "+1-800-555-0123". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#fax_number GoogleClouddomainsRegistration#fax_number}
        '''
        if isinstance(postal_address, dict):
            postal_address = GoogleClouddomainsRegistrationContactSettingsAdminContactPostalAddress(**postal_address)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92186bad9645dfd84410d4b122309d82bda87d0a1f1149e83de82eb88bf4459a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#email GoogleClouddomainsRegistration#email}
        '''
        result = self._values.get("email")
        assert result is not None, "Required property 'email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def phone_number(self) -> builtins.str:
        '''Required. Phone number of the contact in international format. For example, "+1-800-555-0123".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#phone_number GoogleClouddomainsRegistration#phone_number}
        '''
        result = self._values.get("phone_number")
        assert result is not None, "Required property 'phone_number' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def postal_address(
        self,
    ) -> "GoogleClouddomainsRegistrationContactSettingsAdminContactPostalAddress":
        '''postal_address block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#postal_address GoogleClouddomainsRegistration#postal_address}
        '''
        result = self._values.get("postal_address")
        assert result is not None, "Required property 'postal_address' is missing"
        return typing.cast("GoogleClouddomainsRegistrationContactSettingsAdminContactPostalAddress", result)

    @builtins.property
    def fax_number(self) -> typing.Optional[builtins.str]:
        '''Fax number of the contact in international format. For example, "+1-800-555-0123".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#fax_number GoogleClouddomainsRegistration#fax_number}
        '''
        result = self._values.get("fax_number")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddomainsRegistrationContactSettingsAdminContact(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddomainsRegistrationContactSettingsAdminContactOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddomainsRegistration.GoogleClouddomainsRegistrationContactSettingsAdminContactOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d555f3719daafcff2277707ecf7a2626f3168e5368442020986d4fb820f53fc6)
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
        :param region_code: Required. CLDR region code of the country/region of the address. This is never inferred and it is up to the user to ensure the value is correct. See https://cldr.unicode.org/ and https://www.unicode.org/cldr/charts/30/supplemental/territory_information.html for details. Example: "CH" for Switzerland. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#region_code GoogleClouddomainsRegistration#region_code}
        :param address_lines: Unstructured address lines describing the lower levels of an address. Because values in addressLines do not have type information and may sometimes contain multiple values in a single field (e.g. "Austin, TX"), it is important that the line order is clear. The order of address lines should be "envelope order" for the country/region of the address. In places where this can vary (e.g. Japan), address_language is used to make it explicit (e.g. "ja" for large-to-small ordering and "ja-Latn" or "en" for small-to-large). This way, the most specific line of an address can be selected based on the language. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#address_lines GoogleClouddomainsRegistration#address_lines}
        :param administrative_area: Highest administrative subdivision which is used for postal addresses of a country or region. For example, this can be a state, a province, an oblast, or a prefecture. Specifically, for Spain this is the province and not the autonomous community (e.g. "Barcelona" and not "Catalonia"). Many countries don't use an administrative area in postal addresses. E.g. in Switzerland this should be left unpopulated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#administrative_area GoogleClouddomainsRegistration#administrative_area}
        :param locality: Generally refers to the city/town portion of the address. Examples: US city, IT comune, UK post town. In regions of the world where localities are not well defined or do not fit into this structure well, leave locality empty and use addressLines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#locality GoogleClouddomainsRegistration#locality}
        :param organization: The name of the organization at the address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#organization GoogleClouddomainsRegistration#organization}
        :param postal_code: Postal code of the address. Not all countries use or require postal codes to be present, but where they are used, they may trigger additional validation with other parts of the address (e.g. state/zip validation in the U.S.A.). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#postal_code GoogleClouddomainsRegistration#postal_code}
        :param recipients: The recipient at the address. This field may, under certain circumstances, contain multiline information. For example, it might contain "care of" information. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#recipients GoogleClouddomainsRegistration#recipients}
        '''
        value = GoogleClouddomainsRegistrationContactSettingsAdminContactPostalAddress(
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
    ) -> "GoogleClouddomainsRegistrationContactSettingsAdminContactPostalAddressOutputReference":
        return typing.cast("GoogleClouddomainsRegistrationContactSettingsAdminContactPostalAddressOutputReference", jsii.get(self, "postalAddress"))

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
    ) -> typing.Optional["GoogleClouddomainsRegistrationContactSettingsAdminContactPostalAddress"]:
        return typing.cast(typing.Optional["GoogleClouddomainsRegistrationContactSettingsAdminContactPostalAddress"], jsii.get(self, "postalAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__361c06e2678eef1e2e5391352fcf77eb334a57b3acf5579aad5848a8cf95675f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="faxNumber")
    def fax_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "faxNumber"))

    @fax_number.setter
    def fax_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da4ecedc5227eb94adf147fb70c171c6244fbf6eb7dd94477b1441111dc7521c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "faxNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="phoneNumber")
    def phone_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "phoneNumber"))

    @phone_number.setter
    def phone_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed802125b784c9c3f963a1e890cb07f3f109a4005b7d7fde81b5ca02a0c03b1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "phoneNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddomainsRegistrationContactSettingsAdminContact]:
        return typing.cast(typing.Optional[GoogleClouddomainsRegistrationContactSettingsAdminContact], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddomainsRegistrationContactSettingsAdminContact],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9220de7d02473fac5890d75655953ff6bffccb6065925a84d804cc6d3fa395c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddomainsRegistration.GoogleClouddomainsRegistrationContactSettingsAdminContactPostalAddress",
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
class GoogleClouddomainsRegistrationContactSettingsAdminContactPostalAddress:
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
        :param region_code: Required. CLDR region code of the country/region of the address. This is never inferred and it is up to the user to ensure the value is correct. See https://cldr.unicode.org/ and https://www.unicode.org/cldr/charts/30/supplemental/territory_information.html for details. Example: "CH" for Switzerland. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#region_code GoogleClouddomainsRegistration#region_code}
        :param address_lines: Unstructured address lines describing the lower levels of an address. Because values in addressLines do not have type information and may sometimes contain multiple values in a single field (e.g. "Austin, TX"), it is important that the line order is clear. The order of address lines should be "envelope order" for the country/region of the address. In places where this can vary (e.g. Japan), address_language is used to make it explicit (e.g. "ja" for large-to-small ordering and "ja-Latn" or "en" for small-to-large). This way, the most specific line of an address can be selected based on the language. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#address_lines GoogleClouddomainsRegistration#address_lines}
        :param administrative_area: Highest administrative subdivision which is used for postal addresses of a country or region. For example, this can be a state, a province, an oblast, or a prefecture. Specifically, for Spain this is the province and not the autonomous community (e.g. "Barcelona" and not "Catalonia"). Many countries don't use an administrative area in postal addresses. E.g. in Switzerland this should be left unpopulated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#administrative_area GoogleClouddomainsRegistration#administrative_area}
        :param locality: Generally refers to the city/town portion of the address. Examples: US city, IT comune, UK post town. In regions of the world where localities are not well defined or do not fit into this structure well, leave locality empty and use addressLines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#locality GoogleClouddomainsRegistration#locality}
        :param organization: The name of the organization at the address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#organization GoogleClouddomainsRegistration#organization}
        :param postal_code: Postal code of the address. Not all countries use or require postal codes to be present, but where they are used, they may trigger additional validation with other parts of the address (e.g. state/zip validation in the U.S.A.). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#postal_code GoogleClouddomainsRegistration#postal_code}
        :param recipients: The recipient at the address. This field may, under certain circumstances, contain multiline information. For example, it might contain "care of" information. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#recipients GoogleClouddomainsRegistration#recipients}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dc11b889b846ca5538fcb8c2f6fd9438d7b8688da95e1cc3854d096f3bd28c1)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#region_code GoogleClouddomainsRegistration#region_code}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#address_lines GoogleClouddomainsRegistration#address_lines}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#administrative_area GoogleClouddomainsRegistration#administrative_area}
        '''
        result = self._values.get("administrative_area")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def locality(self) -> typing.Optional[builtins.str]:
        '''Generally refers to the city/town portion of the address.

        Examples: US city, IT comune, UK post town. In regions of the world
        where localities are not well defined or do not fit into this structure well, leave locality empty and use addressLines.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#locality GoogleClouddomainsRegistration#locality}
        '''
        result = self._values.get("locality")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organization(self) -> typing.Optional[builtins.str]:
        '''The name of the organization at the address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#organization GoogleClouddomainsRegistration#organization}
        '''
        result = self._values.get("organization")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def postal_code(self) -> typing.Optional[builtins.str]:
        '''Postal code of the address.

        Not all countries use or require postal codes to be present, but where they are used,
        they may trigger additional validation with other parts of the address (e.g. state/zip validation in the U.S.A.).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#postal_code GoogleClouddomainsRegistration#postal_code}
        '''
        result = self._values.get("postal_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recipients(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The recipient at the address.

        This field may, under certain circumstances, contain multiline information. For example,
        it might contain "care of" information.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#recipients GoogleClouddomainsRegistration#recipients}
        '''
        result = self._values.get("recipients")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddomainsRegistrationContactSettingsAdminContactPostalAddress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddomainsRegistrationContactSettingsAdminContactPostalAddressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddomainsRegistration.GoogleClouddomainsRegistrationContactSettingsAdminContactPostalAddressOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d020173bf3768ca1c8984f172b7941b88b2b7c849af536b3e745b0ecd67a544f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2b42c918b9c76114c10c9abeafe34335ce05d73baeafd68f8c50a70fe64d6f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addressLines", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="administrativeArea")
    def administrative_area(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "administrativeArea"))

    @administrative_area.setter
    def administrative_area(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a86162607d3cb00a09faf85f07e74bb62f7d7e090b6f26dc80b0a7fc774f4609)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "administrativeArea", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="locality")
    def locality(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "locality"))

    @locality.setter
    def locality(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d8b93aeb01a0f6797fb88c7e81c5c9eddec478d1d00b221a165b8bcbbe4cac6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locality", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80a84279b1278deef6e779786cf38dde6e440267f3672ce0af6972efbcd540ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postalCode")
    def postal_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postalCode"))

    @postal_code.setter
    def postal_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94e85170edf4cab6ececa0ac9a7323505b22f61ad17976d3e908b01bafa742c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postalCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recipients")
    def recipients(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "recipients"))

    @recipients.setter
    def recipients(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__256fd957e0a8418c94dc97d35ba7b80f6115d4439b2f2336ccf0380d8435b2b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regionCode")
    def region_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regionCode"))

    @region_code.setter
    def region_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71aecb02f8b286592082b40d9d8d8d98618439dba0bce048689ddbf7b6afb2b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regionCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddomainsRegistrationContactSettingsAdminContactPostalAddress]:
        return typing.cast(typing.Optional[GoogleClouddomainsRegistrationContactSettingsAdminContactPostalAddress], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddomainsRegistrationContactSettingsAdminContactPostalAddress],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d12c9ba778ab49f5c2d46d557dab5214863b977091b3f967bba327ead1bda4bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleClouddomainsRegistrationContactSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddomainsRegistration.GoogleClouddomainsRegistrationContactSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__447100207d444ba0b8e4b59a1506f42e63ace0d0af73a33e88096a9cfd339c1d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdminContact")
    def put_admin_contact(
        self,
        *,
        email: builtins.str,
        phone_number: builtins.str,
        postal_address: typing.Union[GoogleClouddomainsRegistrationContactSettingsAdminContactPostalAddress, typing.Dict[builtins.str, typing.Any]],
        fax_number: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param email: Required. Email address of the contact. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#email GoogleClouddomainsRegistration#email}
        :param phone_number: Required. Phone number of the contact in international format. For example, "+1-800-555-0123". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#phone_number GoogleClouddomainsRegistration#phone_number}
        :param postal_address: postal_address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#postal_address GoogleClouddomainsRegistration#postal_address}
        :param fax_number: Fax number of the contact in international format. For example, "+1-800-555-0123". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#fax_number GoogleClouddomainsRegistration#fax_number}
        '''
        value = GoogleClouddomainsRegistrationContactSettingsAdminContact(
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
        postal_address: typing.Union["GoogleClouddomainsRegistrationContactSettingsRegistrantContactPostalAddress", typing.Dict[builtins.str, typing.Any]],
        fax_number: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param email: Required. Email address of the contact. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#email GoogleClouddomainsRegistration#email}
        :param phone_number: Required. Phone number of the contact in international format. For example, "+1-800-555-0123". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#phone_number GoogleClouddomainsRegistration#phone_number}
        :param postal_address: postal_address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#postal_address GoogleClouddomainsRegistration#postal_address}
        :param fax_number: Fax number of the contact in international format. For example, "+1-800-555-0123". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#fax_number GoogleClouddomainsRegistration#fax_number}
        '''
        value = GoogleClouddomainsRegistrationContactSettingsRegistrantContact(
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
        postal_address: typing.Union["GoogleClouddomainsRegistrationContactSettingsTechnicalContactPostalAddress", typing.Dict[builtins.str, typing.Any]],
        fax_number: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param email: Required. Email address of the contact. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#email GoogleClouddomainsRegistration#email}
        :param phone_number: Required. Phone number of the contact in international format. For example, "+1-800-555-0123". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#phone_number GoogleClouddomainsRegistration#phone_number}
        :param postal_address: postal_address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#postal_address GoogleClouddomainsRegistration#postal_address}
        :param fax_number: Fax number of the contact in international format. For example, "+1-800-555-0123". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#fax_number GoogleClouddomainsRegistration#fax_number}
        '''
        value = GoogleClouddomainsRegistrationContactSettingsTechnicalContact(
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
    ) -> GoogleClouddomainsRegistrationContactSettingsAdminContactOutputReference:
        return typing.cast(GoogleClouddomainsRegistrationContactSettingsAdminContactOutputReference, jsii.get(self, "adminContact"))

    @builtins.property
    @jsii.member(jsii_name="registrantContact")
    def registrant_contact(
        self,
    ) -> "GoogleClouddomainsRegistrationContactSettingsRegistrantContactOutputReference":
        return typing.cast("GoogleClouddomainsRegistrationContactSettingsRegistrantContactOutputReference", jsii.get(self, "registrantContact"))

    @builtins.property
    @jsii.member(jsii_name="technicalContact")
    def technical_contact(
        self,
    ) -> "GoogleClouddomainsRegistrationContactSettingsTechnicalContactOutputReference":
        return typing.cast("GoogleClouddomainsRegistrationContactSettingsTechnicalContactOutputReference", jsii.get(self, "technicalContact"))

    @builtins.property
    @jsii.member(jsii_name="adminContactInput")
    def admin_contact_input(
        self,
    ) -> typing.Optional[GoogleClouddomainsRegistrationContactSettingsAdminContact]:
        return typing.cast(typing.Optional[GoogleClouddomainsRegistrationContactSettingsAdminContact], jsii.get(self, "adminContactInput"))

    @builtins.property
    @jsii.member(jsii_name="privacyInput")
    def privacy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privacyInput"))

    @builtins.property
    @jsii.member(jsii_name="registrantContactInput")
    def registrant_contact_input(
        self,
    ) -> typing.Optional["GoogleClouddomainsRegistrationContactSettingsRegistrantContact"]:
        return typing.cast(typing.Optional["GoogleClouddomainsRegistrationContactSettingsRegistrantContact"], jsii.get(self, "registrantContactInput"))

    @builtins.property
    @jsii.member(jsii_name="technicalContactInput")
    def technical_contact_input(
        self,
    ) -> typing.Optional["GoogleClouddomainsRegistrationContactSettingsTechnicalContact"]:
        return typing.cast(typing.Optional["GoogleClouddomainsRegistrationContactSettingsTechnicalContact"], jsii.get(self, "technicalContactInput"))

    @builtins.property
    @jsii.member(jsii_name="privacy")
    def privacy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privacy"))

    @privacy.setter
    def privacy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0ad530233682843837bc4b18955fa5016fc98dd4679bd7ce7883f2a0081eb47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privacy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddomainsRegistrationContactSettings]:
        return typing.cast(typing.Optional[GoogleClouddomainsRegistrationContactSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddomainsRegistrationContactSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e3c9aacfa3fbbe86647a32938976e567a37b927ba2809a932e7b09ff909f686)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddomainsRegistration.GoogleClouddomainsRegistrationContactSettingsRegistrantContact",
    jsii_struct_bases=[],
    name_mapping={
        "email": "email",
        "phone_number": "phoneNumber",
        "postal_address": "postalAddress",
        "fax_number": "faxNumber",
    },
)
class GoogleClouddomainsRegistrationContactSettingsRegistrantContact:
    def __init__(
        self,
        *,
        email: builtins.str,
        phone_number: builtins.str,
        postal_address: typing.Union["GoogleClouddomainsRegistrationContactSettingsRegistrantContactPostalAddress", typing.Dict[builtins.str, typing.Any]],
        fax_number: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param email: Required. Email address of the contact. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#email GoogleClouddomainsRegistration#email}
        :param phone_number: Required. Phone number of the contact in international format. For example, "+1-800-555-0123". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#phone_number GoogleClouddomainsRegistration#phone_number}
        :param postal_address: postal_address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#postal_address GoogleClouddomainsRegistration#postal_address}
        :param fax_number: Fax number of the contact in international format. For example, "+1-800-555-0123". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#fax_number GoogleClouddomainsRegistration#fax_number}
        '''
        if isinstance(postal_address, dict):
            postal_address = GoogleClouddomainsRegistrationContactSettingsRegistrantContactPostalAddress(**postal_address)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__931eef4884efd6c9308dfaa2c708e9378980cebf05ddf21d680f0fbfbbaa41b5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#email GoogleClouddomainsRegistration#email}
        '''
        result = self._values.get("email")
        assert result is not None, "Required property 'email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def phone_number(self) -> builtins.str:
        '''Required. Phone number of the contact in international format. For example, "+1-800-555-0123".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#phone_number GoogleClouddomainsRegistration#phone_number}
        '''
        result = self._values.get("phone_number")
        assert result is not None, "Required property 'phone_number' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def postal_address(
        self,
    ) -> "GoogleClouddomainsRegistrationContactSettingsRegistrantContactPostalAddress":
        '''postal_address block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#postal_address GoogleClouddomainsRegistration#postal_address}
        '''
        result = self._values.get("postal_address")
        assert result is not None, "Required property 'postal_address' is missing"
        return typing.cast("GoogleClouddomainsRegistrationContactSettingsRegistrantContactPostalAddress", result)

    @builtins.property
    def fax_number(self) -> typing.Optional[builtins.str]:
        '''Fax number of the contact in international format. For example, "+1-800-555-0123".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#fax_number GoogleClouddomainsRegistration#fax_number}
        '''
        result = self._values.get("fax_number")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddomainsRegistrationContactSettingsRegistrantContact(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddomainsRegistrationContactSettingsRegistrantContactOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddomainsRegistration.GoogleClouddomainsRegistrationContactSettingsRegistrantContactOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c981be60741d7510b901ff75f390048b56b0e68e61eb6460e60e1d6889530b96)
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
        :param region_code: Required. CLDR region code of the country/region of the address. This is never inferred and it is up to the user to ensure the value is correct. See https://cldr.unicode.org/ and https://www.unicode.org/cldr/charts/30/supplemental/territory_information.html for details. Example: "CH" for Switzerland. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#region_code GoogleClouddomainsRegistration#region_code}
        :param address_lines: Unstructured address lines describing the lower levels of an address. Because values in addressLines do not have type information and may sometimes contain multiple values in a single field (e.g. "Austin, TX"), it is important that the line order is clear. The order of address lines should be "envelope order" for the country/region of the address. In places where this can vary (e.g. Japan), address_language is used to make it explicit (e.g. "ja" for large-to-small ordering and "ja-Latn" or "en" for small-to-large). This way, the most specific line of an address can be selected based on the language. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#address_lines GoogleClouddomainsRegistration#address_lines}
        :param administrative_area: Highest administrative subdivision which is used for postal addresses of a country or region. For example, this can be a state, a province, an oblast, or a prefecture. Specifically, for Spain this is the province and not the autonomous community (e.g. "Barcelona" and not "Catalonia"). Many countries don't use an administrative area in postal addresses. E.g. in Switzerland this should be left unpopulated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#administrative_area GoogleClouddomainsRegistration#administrative_area}
        :param locality: Generally refers to the city/town portion of the address. Examples: US city, IT comune, UK post town. In regions of the world where localities are not well defined or do not fit into this structure well, leave locality empty and use addressLines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#locality GoogleClouddomainsRegistration#locality}
        :param organization: The name of the organization at the address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#organization GoogleClouddomainsRegistration#organization}
        :param postal_code: Postal code of the address. Not all countries use or require postal codes to be present, but where they are used, they may trigger additional validation with other parts of the address (e.g. state/zip validation in the U.S.A.). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#postal_code GoogleClouddomainsRegistration#postal_code}
        :param recipients: The recipient at the address. This field may, under certain circumstances, contain multiline information. For example, it might contain "care of" information. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#recipients GoogleClouddomainsRegistration#recipients}
        '''
        value = GoogleClouddomainsRegistrationContactSettingsRegistrantContactPostalAddress(
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
    ) -> "GoogleClouddomainsRegistrationContactSettingsRegistrantContactPostalAddressOutputReference":
        return typing.cast("GoogleClouddomainsRegistrationContactSettingsRegistrantContactPostalAddressOutputReference", jsii.get(self, "postalAddress"))

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
    ) -> typing.Optional["GoogleClouddomainsRegistrationContactSettingsRegistrantContactPostalAddress"]:
        return typing.cast(typing.Optional["GoogleClouddomainsRegistrationContactSettingsRegistrantContactPostalAddress"], jsii.get(self, "postalAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9dafeded75aa067df85b3d2779212458908b35c6c508959d6d4264f45f98db3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="faxNumber")
    def fax_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "faxNumber"))

    @fax_number.setter
    def fax_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deb2af4b757ff094e1fff3d57fdb17d4e196bae32dd9576c58acbd4ea8efb131)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "faxNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="phoneNumber")
    def phone_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "phoneNumber"))

    @phone_number.setter
    def phone_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3acc18b118ccc51b9d52350582349b829bbbeb373e7f352ed196d646f18608e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "phoneNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddomainsRegistrationContactSettingsRegistrantContact]:
        return typing.cast(typing.Optional[GoogleClouddomainsRegistrationContactSettingsRegistrantContact], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddomainsRegistrationContactSettingsRegistrantContact],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56feac42d492fffa799350223489a9917cb5979571cf8b6288c4e5a398265624)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddomainsRegistration.GoogleClouddomainsRegistrationContactSettingsRegistrantContactPostalAddress",
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
class GoogleClouddomainsRegistrationContactSettingsRegistrantContactPostalAddress:
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
        :param region_code: Required. CLDR region code of the country/region of the address. This is never inferred and it is up to the user to ensure the value is correct. See https://cldr.unicode.org/ and https://www.unicode.org/cldr/charts/30/supplemental/territory_information.html for details. Example: "CH" for Switzerland. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#region_code GoogleClouddomainsRegistration#region_code}
        :param address_lines: Unstructured address lines describing the lower levels of an address. Because values in addressLines do not have type information and may sometimes contain multiple values in a single field (e.g. "Austin, TX"), it is important that the line order is clear. The order of address lines should be "envelope order" for the country/region of the address. In places where this can vary (e.g. Japan), address_language is used to make it explicit (e.g. "ja" for large-to-small ordering and "ja-Latn" or "en" for small-to-large). This way, the most specific line of an address can be selected based on the language. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#address_lines GoogleClouddomainsRegistration#address_lines}
        :param administrative_area: Highest administrative subdivision which is used for postal addresses of a country or region. For example, this can be a state, a province, an oblast, or a prefecture. Specifically, for Spain this is the province and not the autonomous community (e.g. "Barcelona" and not "Catalonia"). Many countries don't use an administrative area in postal addresses. E.g. in Switzerland this should be left unpopulated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#administrative_area GoogleClouddomainsRegistration#administrative_area}
        :param locality: Generally refers to the city/town portion of the address. Examples: US city, IT comune, UK post town. In regions of the world where localities are not well defined or do not fit into this structure well, leave locality empty and use addressLines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#locality GoogleClouddomainsRegistration#locality}
        :param organization: The name of the organization at the address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#organization GoogleClouddomainsRegistration#organization}
        :param postal_code: Postal code of the address. Not all countries use or require postal codes to be present, but where they are used, they may trigger additional validation with other parts of the address (e.g. state/zip validation in the U.S.A.). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#postal_code GoogleClouddomainsRegistration#postal_code}
        :param recipients: The recipient at the address. This field may, under certain circumstances, contain multiline information. For example, it might contain "care of" information. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#recipients GoogleClouddomainsRegistration#recipients}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff8c9132fefd2b9023ab95ab9587173b269968ff31b3f715f1628c1916328726)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#region_code GoogleClouddomainsRegistration#region_code}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#address_lines GoogleClouddomainsRegistration#address_lines}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#administrative_area GoogleClouddomainsRegistration#administrative_area}
        '''
        result = self._values.get("administrative_area")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def locality(self) -> typing.Optional[builtins.str]:
        '''Generally refers to the city/town portion of the address.

        Examples: US city, IT comune, UK post town. In regions of the world
        where localities are not well defined or do not fit into this structure well, leave locality empty and use addressLines.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#locality GoogleClouddomainsRegistration#locality}
        '''
        result = self._values.get("locality")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organization(self) -> typing.Optional[builtins.str]:
        '''The name of the organization at the address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#organization GoogleClouddomainsRegistration#organization}
        '''
        result = self._values.get("organization")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def postal_code(self) -> typing.Optional[builtins.str]:
        '''Postal code of the address.

        Not all countries use or require postal codes to be present, but where they are used,
        they may trigger additional validation with other parts of the address (e.g. state/zip validation in the U.S.A.).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#postal_code GoogleClouddomainsRegistration#postal_code}
        '''
        result = self._values.get("postal_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recipients(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The recipient at the address.

        This field may, under certain circumstances, contain multiline information. For example,
        it might contain "care of" information.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#recipients GoogleClouddomainsRegistration#recipients}
        '''
        result = self._values.get("recipients")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddomainsRegistrationContactSettingsRegistrantContactPostalAddress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddomainsRegistrationContactSettingsRegistrantContactPostalAddressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddomainsRegistration.GoogleClouddomainsRegistrationContactSettingsRegistrantContactPostalAddressOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__59f6f95ef03bba518f48e69110200621ade67cd10c57d3b31457d8dbb4bc6317)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6983064682d21352bc2d17958d3d08d28034d48f8f5a07aea505ce7b59139bbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addressLines", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="administrativeArea")
    def administrative_area(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "administrativeArea"))

    @administrative_area.setter
    def administrative_area(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79868bf3b8a615655327477a727122caf1a515bb5ca685e9fa89ba8d158467ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "administrativeArea", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="locality")
    def locality(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "locality"))

    @locality.setter
    def locality(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__598dd28d62846febba38c2801d5e3b1ceefc97aac8c04df0f841d0e523a3392c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locality", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82dac7610dda162c2ee6f33fb39572797be31775dcea1c6cdb4d9b753e41695b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postalCode")
    def postal_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postalCode"))

    @postal_code.setter
    def postal_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4caefb0462d79beaf65605f2fde0819181592d2f05e9db17369b412da26efab9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postalCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recipients")
    def recipients(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "recipients"))

    @recipients.setter
    def recipients(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd70f509be6fdb0c897ca3a1175b3f951da625298628e68e12e1c8b1fb8c56e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regionCode")
    def region_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regionCode"))

    @region_code.setter
    def region_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b005e2fe4b10cef95c50829849f378965146d92ad8e40acaff3f351460b18e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regionCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddomainsRegistrationContactSettingsRegistrantContactPostalAddress]:
        return typing.cast(typing.Optional[GoogleClouddomainsRegistrationContactSettingsRegistrantContactPostalAddress], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddomainsRegistrationContactSettingsRegistrantContactPostalAddress],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb0cf733974ea22815d23a3eb8c5b2b84542eb4e22051cdbcb805b6ae308309a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddomainsRegistration.GoogleClouddomainsRegistrationContactSettingsTechnicalContact",
    jsii_struct_bases=[],
    name_mapping={
        "email": "email",
        "phone_number": "phoneNumber",
        "postal_address": "postalAddress",
        "fax_number": "faxNumber",
    },
)
class GoogleClouddomainsRegistrationContactSettingsTechnicalContact:
    def __init__(
        self,
        *,
        email: builtins.str,
        phone_number: builtins.str,
        postal_address: typing.Union["GoogleClouddomainsRegistrationContactSettingsTechnicalContactPostalAddress", typing.Dict[builtins.str, typing.Any]],
        fax_number: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param email: Required. Email address of the contact. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#email GoogleClouddomainsRegistration#email}
        :param phone_number: Required. Phone number of the contact in international format. For example, "+1-800-555-0123". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#phone_number GoogleClouddomainsRegistration#phone_number}
        :param postal_address: postal_address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#postal_address GoogleClouddomainsRegistration#postal_address}
        :param fax_number: Fax number of the contact in international format. For example, "+1-800-555-0123". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#fax_number GoogleClouddomainsRegistration#fax_number}
        '''
        if isinstance(postal_address, dict):
            postal_address = GoogleClouddomainsRegistrationContactSettingsTechnicalContactPostalAddress(**postal_address)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c435694310c55b5d509740cfa648e6a5536cb78f0b366ec780724bb668e1fda)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#email GoogleClouddomainsRegistration#email}
        '''
        result = self._values.get("email")
        assert result is not None, "Required property 'email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def phone_number(self) -> builtins.str:
        '''Required. Phone number of the contact in international format. For example, "+1-800-555-0123".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#phone_number GoogleClouddomainsRegistration#phone_number}
        '''
        result = self._values.get("phone_number")
        assert result is not None, "Required property 'phone_number' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def postal_address(
        self,
    ) -> "GoogleClouddomainsRegistrationContactSettingsTechnicalContactPostalAddress":
        '''postal_address block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#postal_address GoogleClouddomainsRegistration#postal_address}
        '''
        result = self._values.get("postal_address")
        assert result is not None, "Required property 'postal_address' is missing"
        return typing.cast("GoogleClouddomainsRegistrationContactSettingsTechnicalContactPostalAddress", result)

    @builtins.property
    def fax_number(self) -> typing.Optional[builtins.str]:
        '''Fax number of the contact in international format. For example, "+1-800-555-0123".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#fax_number GoogleClouddomainsRegistration#fax_number}
        '''
        result = self._values.get("fax_number")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddomainsRegistrationContactSettingsTechnicalContact(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddomainsRegistrationContactSettingsTechnicalContactOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddomainsRegistration.GoogleClouddomainsRegistrationContactSettingsTechnicalContactOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff2c36e38215559ed3944bcc27694568b3ff5692e1bac7ba93d50abfcab26d22)
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
        :param region_code: Required. CLDR region code of the country/region of the address. This is never inferred and it is up to the user to ensure the value is correct. See https://cldr.unicode.org/ and https://www.unicode.org/cldr/charts/30/supplemental/territory_information.html for details. Example: "CH" for Switzerland. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#region_code GoogleClouddomainsRegistration#region_code}
        :param address_lines: Unstructured address lines describing the lower levels of an address. Because values in addressLines do not have type information and may sometimes contain multiple values in a single field (e.g. "Austin, TX"), it is important that the line order is clear. The order of address lines should be "envelope order" for the country/region of the address. In places where this can vary (e.g. Japan), address_language is used to make it explicit (e.g. "ja" for large-to-small ordering and "ja-Latn" or "en" for small-to-large). This way, the most specific line of an address can be selected based on the language. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#address_lines GoogleClouddomainsRegistration#address_lines}
        :param administrative_area: Highest administrative subdivision which is used for postal addresses of a country or region. For example, this can be a state, a province, an oblast, or a prefecture. Specifically, for Spain this is the province and not the autonomous community (e.g. "Barcelona" and not "Catalonia"). Many countries don't use an administrative area in postal addresses. E.g. in Switzerland this should be left unpopulated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#administrative_area GoogleClouddomainsRegistration#administrative_area}
        :param locality: Generally refers to the city/town portion of the address. Examples: US city, IT comune, UK post town. In regions of the world where localities are not well defined or do not fit into this structure well, leave locality empty and use addressLines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#locality GoogleClouddomainsRegistration#locality}
        :param organization: The name of the organization at the address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#organization GoogleClouddomainsRegistration#organization}
        :param postal_code: Postal code of the address. Not all countries use or require postal codes to be present, but where they are used, they may trigger additional validation with other parts of the address (e.g. state/zip validation in the U.S.A.). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#postal_code GoogleClouddomainsRegistration#postal_code}
        :param recipients: The recipient at the address. This field may, under certain circumstances, contain multiline information. For example, it might contain "care of" information. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#recipients GoogleClouddomainsRegistration#recipients}
        '''
        value = GoogleClouddomainsRegistrationContactSettingsTechnicalContactPostalAddress(
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
    ) -> "GoogleClouddomainsRegistrationContactSettingsTechnicalContactPostalAddressOutputReference":
        return typing.cast("GoogleClouddomainsRegistrationContactSettingsTechnicalContactPostalAddressOutputReference", jsii.get(self, "postalAddress"))

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
    ) -> typing.Optional["GoogleClouddomainsRegistrationContactSettingsTechnicalContactPostalAddress"]:
        return typing.cast(typing.Optional["GoogleClouddomainsRegistrationContactSettingsTechnicalContactPostalAddress"], jsii.get(self, "postalAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0ff41f07f250d0663b4db5b66f8dc5584473163678b15bd147107e76fc090c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="faxNumber")
    def fax_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "faxNumber"))

    @fax_number.setter
    def fax_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80dd2975d9143d524f0f69f83727a34657f1d62fd5f68d7a505e7a1d7c17757f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "faxNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="phoneNumber")
    def phone_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "phoneNumber"))

    @phone_number.setter
    def phone_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4af0319412e98b093bd1d941c571279f7367198ad5cdca0c573bdb02f35a31e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "phoneNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddomainsRegistrationContactSettingsTechnicalContact]:
        return typing.cast(typing.Optional[GoogleClouddomainsRegistrationContactSettingsTechnicalContact], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddomainsRegistrationContactSettingsTechnicalContact],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b53bd944c5e7a881bf63179f22fe53c03ec9e44c554a4dbc937b4d21591c90bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddomainsRegistration.GoogleClouddomainsRegistrationContactSettingsTechnicalContactPostalAddress",
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
class GoogleClouddomainsRegistrationContactSettingsTechnicalContactPostalAddress:
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
        :param region_code: Required. CLDR region code of the country/region of the address. This is never inferred and it is up to the user to ensure the value is correct. See https://cldr.unicode.org/ and https://www.unicode.org/cldr/charts/30/supplemental/territory_information.html for details. Example: "CH" for Switzerland. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#region_code GoogleClouddomainsRegistration#region_code}
        :param address_lines: Unstructured address lines describing the lower levels of an address. Because values in addressLines do not have type information and may sometimes contain multiple values in a single field (e.g. "Austin, TX"), it is important that the line order is clear. The order of address lines should be "envelope order" for the country/region of the address. In places where this can vary (e.g. Japan), address_language is used to make it explicit (e.g. "ja" for large-to-small ordering and "ja-Latn" or "en" for small-to-large). This way, the most specific line of an address can be selected based on the language. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#address_lines GoogleClouddomainsRegistration#address_lines}
        :param administrative_area: Highest administrative subdivision which is used for postal addresses of a country or region. For example, this can be a state, a province, an oblast, or a prefecture. Specifically, for Spain this is the province and not the autonomous community (e.g. "Barcelona" and not "Catalonia"). Many countries don't use an administrative area in postal addresses. E.g. in Switzerland this should be left unpopulated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#administrative_area GoogleClouddomainsRegistration#administrative_area}
        :param locality: Generally refers to the city/town portion of the address. Examples: US city, IT comune, UK post town. In regions of the world where localities are not well defined or do not fit into this structure well, leave locality empty and use addressLines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#locality GoogleClouddomainsRegistration#locality}
        :param organization: The name of the organization at the address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#organization GoogleClouddomainsRegistration#organization}
        :param postal_code: Postal code of the address. Not all countries use or require postal codes to be present, but where they are used, they may trigger additional validation with other parts of the address (e.g. state/zip validation in the U.S.A.). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#postal_code GoogleClouddomainsRegistration#postal_code}
        :param recipients: The recipient at the address. This field may, under certain circumstances, contain multiline information. For example, it might contain "care of" information. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#recipients GoogleClouddomainsRegistration#recipients}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__325023bf4589db33d94283999e628b345ef214691f5fb0fade3ad6956bb2bf4c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#region_code GoogleClouddomainsRegistration#region_code}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#address_lines GoogleClouddomainsRegistration#address_lines}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#administrative_area GoogleClouddomainsRegistration#administrative_area}
        '''
        result = self._values.get("administrative_area")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def locality(self) -> typing.Optional[builtins.str]:
        '''Generally refers to the city/town portion of the address.

        Examples: US city, IT comune, UK post town. In regions of the world
        where localities are not well defined or do not fit into this structure well, leave locality empty and use addressLines.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#locality GoogleClouddomainsRegistration#locality}
        '''
        result = self._values.get("locality")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organization(self) -> typing.Optional[builtins.str]:
        '''The name of the organization at the address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#organization GoogleClouddomainsRegistration#organization}
        '''
        result = self._values.get("organization")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def postal_code(self) -> typing.Optional[builtins.str]:
        '''Postal code of the address.

        Not all countries use or require postal codes to be present, but where they are used,
        they may trigger additional validation with other parts of the address (e.g. state/zip validation in the U.S.A.).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#postal_code GoogleClouddomainsRegistration#postal_code}
        '''
        result = self._values.get("postal_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recipients(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The recipient at the address.

        This field may, under certain circumstances, contain multiline information. For example,
        it might contain "care of" information.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#recipients GoogleClouddomainsRegistration#recipients}
        '''
        result = self._values.get("recipients")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddomainsRegistrationContactSettingsTechnicalContactPostalAddress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddomainsRegistrationContactSettingsTechnicalContactPostalAddressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddomainsRegistration.GoogleClouddomainsRegistrationContactSettingsTechnicalContactPostalAddressOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef9435b2fdb808f834a1b730d31b1a30677c97e0f530a8b6df9c2adf6dde3758)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7085057724c9107308c0a8a3947caa8715f1fc417d308c2eaa354649a2dcf3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addressLines", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="administrativeArea")
    def administrative_area(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "administrativeArea"))

    @administrative_area.setter
    def administrative_area(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b7f494b8182b764de0b7a81e2bc7938e8ac6ae1441b3d0456760447751c838d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "administrativeArea", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="locality")
    def locality(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "locality"))

    @locality.setter
    def locality(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3acd58dec4c9c58877fb293acb78e9d3455557f654a60d6c985f97cf4b8ff817)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locality", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cd3e26c54a8ca71047a63bd5723e95c66cd56d38c056487283c23dc9d9bf540)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postalCode")
    def postal_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postalCode"))

    @postal_code.setter
    def postal_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3135a6c55c000a97441f2bd567a33c9097c13e43d8afc20bf4b520f3045b41e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postalCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recipients")
    def recipients(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "recipients"))

    @recipients.setter
    def recipients(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__637905b68574c14cac81ee7183791356e22e0ea0f984286f96d15a73cb61be4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regionCode")
    def region_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regionCode"))

    @region_code.setter
    def region_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f865737d09034ca4482f5a055e279495a42b70e4a36c73ccbe381ea0869576f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regionCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddomainsRegistrationContactSettingsTechnicalContactPostalAddress]:
        return typing.cast(typing.Optional[GoogleClouddomainsRegistrationContactSettingsTechnicalContactPostalAddress], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddomainsRegistrationContactSettingsTechnicalContactPostalAddress],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a88d417fb757140987281bce4183d173a2481b8a654c75a6b64aaa400777e51c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddomainsRegistration.GoogleClouddomainsRegistrationDnsSettings",
    jsii_struct_bases=[],
    name_mapping={"custom_dns": "customDns", "glue_records": "glueRecords"},
)
class GoogleClouddomainsRegistrationDnsSettings:
    def __init__(
        self,
        *,
        custom_dns: typing.Optional[typing.Union["GoogleClouddomainsRegistrationDnsSettingsCustomDns", typing.Dict[builtins.str, typing.Any]]] = None,
        glue_records: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddomainsRegistrationDnsSettingsGlueRecords", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param custom_dns: custom_dns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#custom_dns GoogleClouddomainsRegistration#custom_dns}
        :param glue_records: glue_records block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#glue_records GoogleClouddomainsRegistration#glue_records}
        '''
        if isinstance(custom_dns, dict):
            custom_dns = GoogleClouddomainsRegistrationDnsSettingsCustomDns(**custom_dns)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b79a9bb4c7df315eef8842469489db87b14710e5225e20287863c3b65603f212)
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
    ) -> typing.Optional["GoogleClouddomainsRegistrationDnsSettingsCustomDns"]:
        '''custom_dns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#custom_dns GoogleClouddomainsRegistration#custom_dns}
        '''
        result = self._values.get("custom_dns")
        return typing.cast(typing.Optional["GoogleClouddomainsRegistrationDnsSettingsCustomDns"], result)

    @builtins.property
    def glue_records(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddomainsRegistrationDnsSettingsGlueRecords"]]]:
        '''glue_records block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#glue_records GoogleClouddomainsRegistration#glue_records}
        '''
        result = self._values.get("glue_records")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddomainsRegistrationDnsSettingsGlueRecords"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddomainsRegistrationDnsSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddomainsRegistration.GoogleClouddomainsRegistrationDnsSettingsCustomDns",
    jsii_struct_bases=[],
    name_mapping={"name_servers": "nameServers", "ds_records": "dsRecords"},
)
class GoogleClouddomainsRegistrationDnsSettingsCustomDns:
    def __init__(
        self,
        *,
        name_servers: typing.Sequence[builtins.str],
        ds_records: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddomainsRegistrationDnsSettingsCustomDnsDsRecords", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name_servers: Required. A list of name servers that store the DNS zone for this domain. Each name server is a domain name, with Unicode domain names expressed in Punycode format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#name_servers GoogleClouddomainsRegistration#name_servers}
        :param ds_records: ds_records block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#ds_records GoogleClouddomainsRegistration#ds_records}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95e52ba66d03eb1bc38f3fe0d2bbc9736b0173ee3a318cb88a317a0161f37a23)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#name_servers GoogleClouddomainsRegistration#name_servers}
        '''
        result = self._values.get("name_servers")
        assert result is not None, "Required property 'name_servers' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def ds_records(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddomainsRegistrationDnsSettingsCustomDnsDsRecords"]]]:
        '''ds_records block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#ds_records GoogleClouddomainsRegistration#ds_records}
        '''
        result = self._values.get("ds_records")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddomainsRegistrationDnsSettingsCustomDnsDsRecords"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddomainsRegistrationDnsSettingsCustomDns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddomainsRegistration.GoogleClouddomainsRegistrationDnsSettingsCustomDnsDsRecords",
    jsii_struct_bases=[],
    name_mapping={
        "algorithm": "algorithm",
        "digest": "digest",
        "digest_type": "digestType",
        "key_tag": "keyTag",
    },
)
class GoogleClouddomainsRegistrationDnsSettingsCustomDnsDsRecords:
    def __init__(
        self,
        *,
        algorithm: typing.Optional[builtins.str] = None,
        digest: typing.Optional[builtins.str] = None,
        digest_type: typing.Optional[builtins.str] = None,
        key_tag: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param algorithm: The algorithm used to generate the referenced DNSKEY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#algorithm GoogleClouddomainsRegistration#algorithm}
        :param digest: The digest generated from the referenced DNSKEY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#digest GoogleClouddomainsRegistration#digest}
        :param digest_type: The hash function used to generate the digest of the referenced DNSKEY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#digest_type GoogleClouddomainsRegistration#digest_type}
        :param key_tag: The key tag of the record. Must be set in range 0 -- 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#key_tag GoogleClouddomainsRegistration#key_tag}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e006b3a3cc1341e780b441b6dd8b43251553a485eb262da388fcc84c284b4aa9)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#algorithm GoogleClouddomainsRegistration#algorithm}
        '''
        result = self._values.get("algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def digest(self) -> typing.Optional[builtins.str]:
        '''The digest generated from the referenced DNSKEY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#digest GoogleClouddomainsRegistration#digest}
        '''
        result = self._values.get("digest")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def digest_type(self) -> typing.Optional[builtins.str]:
        '''The hash function used to generate the digest of the referenced DNSKEY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#digest_type GoogleClouddomainsRegistration#digest_type}
        '''
        result = self._values.get("digest_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_tag(self) -> typing.Optional[jsii.Number]:
        '''The key tag of the record. Must be set in range 0 -- 65535.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#key_tag GoogleClouddomainsRegistration#key_tag}
        '''
        result = self._values.get("key_tag")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddomainsRegistrationDnsSettingsCustomDnsDsRecords(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddomainsRegistrationDnsSettingsCustomDnsDsRecordsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddomainsRegistration.GoogleClouddomainsRegistrationDnsSettingsCustomDnsDsRecordsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aef12ff1200e1f5c37e282754a1df8788877384f82c66ec134610695ca6dc699)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleClouddomainsRegistrationDnsSettingsCustomDnsDsRecordsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b15367ec098546a2faf1557c5d317a765500f2b0274255057f806c396813c5d8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleClouddomainsRegistrationDnsSettingsCustomDnsDsRecordsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ff9588b1401fc2ddf11fdc77c73cf27da3d2b2934f57064142991959d7ec246)
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
            type_hints = typing.get_type_hints(_typecheckingstub__00dbd9f8b5ef0692df97bca6c70cb98485224a799ca859516b8effe3b1a13c64)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c4c7be7e82feb97c119c1121e5989993954a0a38eb135cb6dc5aa35f9c9bb71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddomainsRegistrationDnsSettingsCustomDnsDsRecords]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddomainsRegistrationDnsSettingsCustomDnsDsRecords]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddomainsRegistrationDnsSettingsCustomDnsDsRecords]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75ec0eb1a65438328448ece0ab84b0776e7968c0005341ae8bee1e9ddf9575fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleClouddomainsRegistrationDnsSettingsCustomDnsDsRecordsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddomainsRegistration.GoogleClouddomainsRegistrationDnsSettingsCustomDnsDsRecordsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d0791c6916723d4a55aab55c7b0190c11bbbc542b5a1f5d9714c42a5896211f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf4be18e3ce9c0bbb0f80b65b9a0d38f000f90e9efe8cfa1c1c5993745613ea2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "algorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="digest")
    def digest(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "digest"))

    @digest.setter
    def digest(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b9168f5405023489fdda419f5123d55304bebc0e2c134d62ba214a6ac24a690)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "digest", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="digestType")
    def digest_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "digestType"))

    @digest_type.setter
    def digest_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b38a8ac19bf008a249cf96cfeeca4203ec31a38d67783ad52d7b3e97e567e8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "digestType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyTag")
    def key_tag(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "keyTag"))

    @key_tag.setter
    def key_tag(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c243674851825f7d1b84ab4a245b183adbff0cc67fa318b5f892713f32f17fd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyTag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddomainsRegistrationDnsSettingsCustomDnsDsRecords]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddomainsRegistrationDnsSettingsCustomDnsDsRecords]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddomainsRegistrationDnsSettingsCustomDnsDsRecords]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8a4652e967a347d14b866320361b5154964f650895f2d1c15739ba09e984db6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleClouddomainsRegistrationDnsSettingsCustomDnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddomainsRegistration.GoogleClouddomainsRegistrationDnsSettingsCustomDnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a27dfc616b5d4683416da12c82fd30eefbfc81ea3f0a433f2c16557eb9a78fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDsRecords")
    def put_ds_records(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddomainsRegistrationDnsSettingsCustomDnsDsRecords, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__750c308b8799031c15fae645709b0064fdc0f484746e88dbcd71fee0474cce71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDsRecords", [value]))

    @jsii.member(jsii_name="resetDsRecords")
    def reset_ds_records(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDsRecords", []))

    @builtins.property
    @jsii.member(jsii_name="dsRecords")
    def ds_records(
        self,
    ) -> GoogleClouddomainsRegistrationDnsSettingsCustomDnsDsRecordsList:
        return typing.cast(GoogleClouddomainsRegistrationDnsSettingsCustomDnsDsRecordsList, jsii.get(self, "dsRecords"))

    @builtins.property
    @jsii.member(jsii_name="dsRecordsInput")
    def ds_records_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddomainsRegistrationDnsSettingsCustomDnsDsRecords]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddomainsRegistrationDnsSettingsCustomDnsDsRecords]]], jsii.get(self, "dsRecordsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__6314ecf59e12e7086473cf1d0cd10d1293d572a076a9dc9eb742b2be8aa80b10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nameServers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddomainsRegistrationDnsSettingsCustomDns]:
        return typing.cast(typing.Optional[GoogleClouddomainsRegistrationDnsSettingsCustomDns], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddomainsRegistrationDnsSettingsCustomDns],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98eb69cb1a666d3dfc3147824dcdb06b1bbdaed7b05e3083bc443b85f290a1e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddomainsRegistration.GoogleClouddomainsRegistrationDnsSettingsGlueRecords",
    jsii_struct_bases=[],
    name_mapping={
        "host_name": "hostName",
        "ipv4_addresses": "ipv4Addresses",
        "ipv6_addresses": "ipv6Addresses",
    },
)
class GoogleClouddomainsRegistrationDnsSettingsGlueRecords:
    def __init__(
        self,
        *,
        host_name: builtins.str,
        ipv4_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        ipv6_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param host_name: Required. Domain name of the host in Punycode format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#host_name GoogleClouddomainsRegistration#host_name}
        :param ipv4_addresses: List of IPv4 addresses corresponding to this host in the standard decimal format (e.g. 198.51.100.1). At least one of ipv4_address and ipv6_address must be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#ipv4_addresses GoogleClouddomainsRegistration#ipv4_addresses}
        :param ipv6_addresses: List of IPv4 addresses corresponding to this host in the standard decimal format (e.g. 198.51.100.1). At least one of ipv4_address and ipv6_address must be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#ipv6_addresses GoogleClouddomainsRegistration#ipv6_addresses}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f94cf27fd5e3e4d34b4afbdff3d0ae70ef712df7ccafb1d277ccf0bf16c986a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#host_name GoogleClouddomainsRegistration#host_name}
        '''
        result = self._values.get("host_name")
        assert result is not None, "Required property 'host_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ipv4_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of IPv4 addresses corresponding to this host in the standard decimal format (e.g. 198.51.100.1). At least one of ipv4_address and ipv6_address must be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#ipv4_addresses GoogleClouddomainsRegistration#ipv4_addresses}
        '''
        result = self._values.get("ipv4_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ipv6_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of IPv4 addresses corresponding to this host in the standard decimal format (e.g. 198.51.100.1). At least one of ipv4_address and ipv6_address must be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#ipv6_addresses GoogleClouddomainsRegistration#ipv6_addresses}
        '''
        result = self._values.get("ipv6_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddomainsRegistrationDnsSettingsGlueRecords(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddomainsRegistrationDnsSettingsGlueRecordsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddomainsRegistration.GoogleClouddomainsRegistrationDnsSettingsGlueRecordsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__374292ea3819e037c7df1bc58b2bd39276db8295075c7616b33d371b8a1d986a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleClouddomainsRegistrationDnsSettingsGlueRecordsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3653013a035f7ded098b95be85da968200fd575b6dfe6723526993695c4f3a30)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleClouddomainsRegistrationDnsSettingsGlueRecordsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9966294ad1704a02546c496210aa854fe3143d5ba6ef6d5a992eec92dd82bfdb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__acde21366728b7397cb6563100df32dc1f0bd2d15212cb9972df6e2700abd6c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3050e468b6e1b5e5901fa04161bddef1ead946bee95b5f9d021c58b6c7129402)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddomainsRegistrationDnsSettingsGlueRecords]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddomainsRegistrationDnsSettingsGlueRecords]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddomainsRegistrationDnsSettingsGlueRecords]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b51891375b3f37873c22e3c0442f7d05bf19f99a5c31c3226a7b0c1c81c0006b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleClouddomainsRegistrationDnsSettingsGlueRecordsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddomainsRegistration.GoogleClouddomainsRegistrationDnsSettingsGlueRecordsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7073eddc948243b384c934a9018a287305270416681811e3347bb4f3b343083f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__caac7b4605ef4a25d4b6099cd90b876c8c1b1f980783eeb78d0e87637714a323)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipv4Addresses")
    def ipv4_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipv4Addresses"))

    @ipv4_addresses.setter
    def ipv4_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f54027134259ff5c72037364f969d2b38581beab65ebed308e1d80c4ed07e7fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv4Addresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipv6Addresses")
    def ipv6_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipv6Addresses"))

    @ipv6_addresses.setter
    def ipv6_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbc8d6b13c4c25419d9a5d407121008d840161778f5c55cbf6e4aaf5cd5f622c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv6Addresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddomainsRegistrationDnsSettingsGlueRecords]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddomainsRegistrationDnsSettingsGlueRecords]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddomainsRegistrationDnsSettingsGlueRecords]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03b348714cc5dc50786707e3d9059d928010b64c1296ad771abe10bcba995ceb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleClouddomainsRegistrationDnsSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddomainsRegistration.GoogleClouddomainsRegistrationDnsSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9dc753cdac399aae2da79ca40fad3effa10fc729b004384ae205eef8a052d568)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomDns")
    def put_custom_dns(
        self,
        *,
        name_servers: typing.Sequence[builtins.str],
        ds_records: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddomainsRegistrationDnsSettingsCustomDnsDsRecords, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name_servers: Required. A list of name servers that store the DNS zone for this domain. Each name server is a domain name, with Unicode domain names expressed in Punycode format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#name_servers GoogleClouddomainsRegistration#name_servers}
        :param ds_records: ds_records block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#ds_records GoogleClouddomainsRegistration#ds_records}
        '''
        value = GoogleClouddomainsRegistrationDnsSettingsCustomDns(
            name_servers=name_servers, ds_records=ds_records
        )

        return typing.cast(None, jsii.invoke(self, "putCustomDns", [value]))

    @jsii.member(jsii_name="putGlueRecords")
    def put_glue_records(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddomainsRegistrationDnsSettingsGlueRecords, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b2419c1a57c74b1fefb63f989273ba4422617c5838d05f90b88758031d85c30)
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
    def custom_dns(
        self,
    ) -> GoogleClouddomainsRegistrationDnsSettingsCustomDnsOutputReference:
        return typing.cast(GoogleClouddomainsRegistrationDnsSettingsCustomDnsOutputReference, jsii.get(self, "customDns"))

    @builtins.property
    @jsii.member(jsii_name="glueRecords")
    def glue_records(self) -> GoogleClouddomainsRegistrationDnsSettingsGlueRecordsList:
        return typing.cast(GoogleClouddomainsRegistrationDnsSettingsGlueRecordsList, jsii.get(self, "glueRecords"))

    @builtins.property
    @jsii.member(jsii_name="customDnsInput")
    def custom_dns_input(
        self,
    ) -> typing.Optional[GoogleClouddomainsRegistrationDnsSettingsCustomDns]:
        return typing.cast(typing.Optional[GoogleClouddomainsRegistrationDnsSettingsCustomDns], jsii.get(self, "customDnsInput"))

    @builtins.property
    @jsii.member(jsii_name="glueRecordsInput")
    def glue_records_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddomainsRegistrationDnsSettingsGlueRecords]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddomainsRegistrationDnsSettingsGlueRecords]]], jsii.get(self, "glueRecordsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddomainsRegistrationDnsSettings]:
        return typing.cast(typing.Optional[GoogleClouddomainsRegistrationDnsSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddomainsRegistrationDnsSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4d7bf55ee8769b550bdf902118c2293215d4ce9b0a939e828748e15615ddc59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddomainsRegistration.GoogleClouddomainsRegistrationManagementSettings",
    jsii_struct_bases=[],
    name_mapping={
        "preferred_renewal_method": "preferredRenewalMethod",
        "transfer_lock_state": "transferLockState",
    },
)
class GoogleClouddomainsRegistrationManagementSettings:
    def __init__(
        self,
        *,
        preferred_renewal_method: typing.Optional[builtins.str] = None,
        transfer_lock_state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param preferred_renewal_method: The desired renewal method for this Registration. The actual renewalMethod is automatically updated to reflect this choice. If unset or equal to RENEWAL_METHOD_UNSPECIFIED, the actual renewalMethod is treated as if it were set to AUTOMATIC_RENEWAL. You cannot use RENEWAL_DISABLED during resource creation, and you can update the renewal status only when the Registration resource has state ACTIVE or SUSPENDED. When preferredRenewalMethod is set to AUTOMATIC_RENEWAL, the actual renewalMethod can be set to RENEWAL_DISABLED in case of problems with the billing account or reported domain abuse. In such cases, check the issues field on the Registration. After the problem is resolved, the renewalMethod is automatically updated to preferredRenewalMethod in a few hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#preferred_renewal_method GoogleClouddomainsRegistration#preferred_renewal_method}
        :param transfer_lock_state: Controls whether the domain can be transferred to another registrar. Values are UNLOCKED or LOCKED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#transfer_lock_state GoogleClouddomainsRegistration#transfer_lock_state}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3706ab355436176639c47f9be8bbcd3600789249a06129bff44c601110b1b9b3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#preferred_renewal_method GoogleClouddomainsRegistration#preferred_renewal_method}
        '''
        result = self._values.get("preferred_renewal_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transfer_lock_state(self) -> typing.Optional[builtins.str]:
        '''Controls whether the domain can be transferred to another registrar. Values are UNLOCKED or LOCKED.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#transfer_lock_state GoogleClouddomainsRegistration#transfer_lock_state}
        '''
        result = self._values.get("transfer_lock_state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddomainsRegistrationManagementSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddomainsRegistrationManagementSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddomainsRegistration.GoogleClouddomainsRegistrationManagementSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2de1924fefff37b869f8f3c496bb6e780e65fc7fb2fe089e6415c4669b952d5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__29c88ee7fe6aa9e89d9d86e9e3458993352104603a3dd51455077e50406a75a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredRenewalMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transferLockState")
    def transfer_lock_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transferLockState"))

    @transfer_lock_state.setter
    def transfer_lock_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6043f5b17a87b031a4c9600d7570fe213442ea8c6fc265236d19ff5cf2ccb25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transferLockState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddomainsRegistrationManagementSettings]:
        return typing.cast(typing.Optional[GoogleClouddomainsRegistrationManagementSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddomainsRegistrationManagementSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eaf758e0db719a11c0d70c4680314b0f7c9faf94f37b675570c1305106ee9ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddomainsRegistration.GoogleClouddomainsRegistrationTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleClouddomainsRegistrationTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#create GoogleClouddomainsRegistration#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#delete GoogleClouddomainsRegistration#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#update GoogleClouddomainsRegistration#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75f26b4a065e946e62b61ffce5a28d50c6c55ac48fcf96d2ce3c47a22f4d83ad)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#create GoogleClouddomainsRegistration#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#delete GoogleClouddomainsRegistration#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#update GoogleClouddomainsRegistration#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddomainsRegistrationTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddomainsRegistrationTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddomainsRegistration.GoogleClouddomainsRegistrationTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d24c05d5a2a67aef05cf70c98719c1c4566f6b1858171b3ed50d6d40b5fce9ce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f42200652bc4b0cf630603e82d055b6aa5da163b806a9e37ff6f994f29472d78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81c54c7d623e3f7c10b8d94dae77e6b65acae1cee29bd41bf559ae0dd55d0333)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f3a3774afcb29941685aecb8ed2534bd4eadc375027e685caec32a9c5446008)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddomainsRegistrationTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddomainsRegistrationTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddomainsRegistrationTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d908f60404786282ae677e9fa3db91aeabdc502bb3d96950b66856fda7120fcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddomainsRegistration.GoogleClouddomainsRegistrationYearlyPrice",
    jsii_struct_bases=[],
    name_mapping={"currency_code": "currencyCode", "units": "units"},
)
class GoogleClouddomainsRegistrationYearlyPrice:
    def __init__(
        self,
        *,
        currency_code: typing.Optional[builtins.str] = None,
        units: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param currency_code: The three-letter currency code defined in ISO 4217. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#currency_code GoogleClouddomainsRegistration#currency_code}
        :param units: The whole units of the amount. For example if currencyCode is "USD", then 1 unit is one US dollar. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#units GoogleClouddomainsRegistration#units}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f1eeede8a4ad51957c622dd685219ad7e8cba832043429e7a45e7112db6656a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#currency_code GoogleClouddomainsRegistration#currency_code}
        '''
        result = self._values.get("currency_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def units(self) -> typing.Optional[builtins.str]:
        '''The whole units of the amount. For example if currencyCode is "USD", then 1 unit is one US dollar.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddomains_registration#units GoogleClouddomainsRegistration#units}
        '''
        result = self._values.get("units")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddomainsRegistrationYearlyPrice(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddomainsRegistrationYearlyPriceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddomainsRegistration.GoogleClouddomainsRegistrationYearlyPriceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7eb2c334aa26264b91df4f2ecfef40b424ef19482562abe3501b44a116fa759d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__760f0411d9893078acedc7837541dafa050b941946a79ca1d6cf7671ec1e4c5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "currencyCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="units")
    def units(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "units"))

    @units.setter
    def units(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bff4de39a721a2cc960b7d9864f9cfc13eb6117b479707dc89383a93a08de8d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "units", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddomainsRegistrationYearlyPrice]:
        return typing.cast(typing.Optional[GoogleClouddomainsRegistrationYearlyPrice], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddomainsRegistrationYearlyPrice],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba56f0bc06ba0dfb3a6b64bd80a95a82ac1445b6fd89a21bf43d8e562b8ebfb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleClouddomainsRegistration",
    "GoogleClouddomainsRegistrationConfig",
    "GoogleClouddomainsRegistrationContactSettings",
    "GoogleClouddomainsRegistrationContactSettingsAdminContact",
    "GoogleClouddomainsRegistrationContactSettingsAdminContactOutputReference",
    "GoogleClouddomainsRegistrationContactSettingsAdminContactPostalAddress",
    "GoogleClouddomainsRegistrationContactSettingsAdminContactPostalAddressOutputReference",
    "GoogleClouddomainsRegistrationContactSettingsOutputReference",
    "GoogleClouddomainsRegistrationContactSettingsRegistrantContact",
    "GoogleClouddomainsRegistrationContactSettingsRegistrantContactOutputReference",
    "GoogleClouddomainsRegistrationContactSettingsRegistrantContactPostalAddress",
    "GoogleClouddomainsRegistrationContactSettingsRegistrantContactPostalAddressOutputReference",
    "GoogleClouddomainsRegistrationContactSettingsTechnicalContact",
    "GoogleClouddomainsRegistrationContactSettingsTechnicalContactOutputReference",
    "GoogleClouddomainsRegistrationContactSettingsTechnicalContactPostalAddress",
    "GoogleClouddomainsRegistrationContactSettingsTechnicalContactPostalAddressOutputReference",
    "GoogleClouddomainsRegistrationDnsSettings",
    "GoogleClouddomainsRegistrationDnsSettingsCustomDns",
    "GoogleClouddomainsRegistrationDnsSettingsCustomDnsDsRecords",
    "GoogleClouddomainsRegistrationDnsSettingsCustomDnsDsRecordsList",
    "GoogleClouddomainsRegistrationDnsSettingsCustomDnsDsRecordsOutputReference",
    "GoogleClouddomainsRegistrationDnsSettingsCustomDnsOutputReference",
    "GoogleClouddomainsRegistrationDnsSettingsGlueRecords",
    "GoogleClouddomainsRegistrationDnsSettingsGlueRecordsList",
    "GoogleClouddomainsRegistrationDnsSettingsGlueRecordsOutputReference",
    "GoogleClouddomainsRegistrationDnsSettingsOutputReference",
    "GoogleClouddomainsRegistrationManagementSettings",
    "GoogleClouddomainsRegistrationManagementSettingsOutputReference",
    "GoogleClouddomainsRegistrationTimeouts",
    "GoogleClouddomainsRegistrationTimeoutsOutputReference",
    "GoogleClouddomainsRegistrationYearlyPrice",
    "GoogleClouddomainsRegistrationYearlyPriceOutputReference",
]

publication.publish()

def _typecheckingstub__a294f3c4b9b346d91a080138301e3d471ce1b7240964a4113e9008bbaebe23bf(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    contact_settings: typing.Union[GoogleClouddomainsRegistrationContactSettings, typing.Dict[builtins.str, typing.Any]],
    domain_name: builtins.str,
    location: builtins.str,
    yearly_price: typing.Union[GoogleClouddomainsRegistrationYearlyPrice, typing.Dict[builtins.str, typing.Any]],
    contact_notices: typing.Optional[typing.Sequence[builtins.str]] = None,
    dns_settings: typing.Optional[typing.Union[GoogleClouddomainsRegistrationDnsSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    domain_notices: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    management_settings: typing.Optional[typing.Union[GoogleClouddomainsRegistrationManagementSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleClouddomainsRegistrationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__2972634334d652cf2fa1f36d2007a2bbd879ed0c098db633d3662e91b2729fa3(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc88e690c681c95612a0396ae35d492a7285cf7971451bfcb4d6a84594d3464a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ca8df0416dad7d5a1a68712a06159554b370fb994072f32818e3bf3b85f7123(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9b8e8d2342bbfc76f63808d1643ef7dac00e95ae5d6eb6e8a41318184790a18(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b1a6bbd9495599c7c30eebc77aaab3375ba5188f9aa960e2250d075b79d3667(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3d91705056092a57e24b5436f062ef96da07b144f9c9a382c28d1137d026934(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeb5963f209b68367ae0ab0f5180dd5076300d905c69682d34f4593e57ce504d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44d8790b6237ab8fe082fed4095c4f914796f58f417b1b243ca177ee42df87dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a9f9b868ef38d88583bf3ba632b566f8a2cc66c975b6665b4180dc4f22c0926(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    contact_settings: typing.Union[GoogleClouddomainsRegistrationContactSettings, typing.Dict[builtins.str, typing.Any]],
    domain_name: builtins.str,
    location: builtins.str,
    yearly_price: typing.Union[GoogleClouddomainsRegistrationYearlyPrice, typing.Dict[builtins.str, typing.Any]],
    contact_notices: typing.Optional[typing.Sequence[builtins.str]] = None,
    dns_settings: typing.Optional[typing.Union[GoogleClouddomainsRegistrationDnsSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    domain_notices: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    management_settings: typing.Optional[typing.Union[GoogleClouddomainsRegistrationManagementSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleClouddomainsRegistrationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83086f2e6e263e44dde92d6dbd525498676532ad8b5a9b00747e6cc33951c8d1(
    *,
    admin_contact: typing.Union[GoogleClouddomainsRegistrationContactSettingsAdminContact, typing.Dict[builtins.str, typing.Any]],
    privacy: builtins.str,
    registrant_contact: typing.Union[GoogleClouddomainsRegistrationContactSettingsRegistrantContact, typing.Dict[builtins.str, typing.Any]],
    technical_contact: typing.Union[GoogleClouddomainsRegistrationContactSettingsTechnicalContact, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92186bad9645dfd84410d4b122309d82bda87d0a1f1149e83de82eb88bf4459a(
    *,
    email: builtins.str,
    phone_number: builtins.str,
    postal_address: typing.Union[GoogleClouddomainsRegistrationContactSettingsAdminContactPostalAddress, typing.Dict[builtins.str, typing.Any]],
    fax_number: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d555f3719daafcff2277707ecf7a2626f3168e5368442020986d4fb820f53fc6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__361c06e2678eef1e2e5391352fcf77eb334a57b3acf5579aad5848a8cf95675f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da4ecedc5227eb94adf147fb70c171c6244fbf6eb7dd94477b1441111dc7521c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed802125b784c9c3f963a1e890cb07f3f109a4005b7d7fde81b5ca02a0c03b1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9220de7d02473fac5890d75655953ff6bffccb6065925a84d804cc6d3fa395c3(
    value: typing.Optional[GoogleClouddomainsRegistrationContactSettingsAdminContact],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dc11b889b846ca5538fcb8c2f6fd9438d7b8688da95e1cc3854d096f3bd28c1(
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

def _typecheckingstub__d020173bf3768ca1c8984f172b7941b88b2b7c849af536b3e745b0ecd67a544f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2b42c918b9c76114c10c9abeafe34335ce05d73baeafd68f8c50a70fe64d6f3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a86162607d3cb00a09faf85f07e74bb62f7d7e090b6f26dc80b0a7fc774f4609(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d8b93aeb01a0f6797fb88c7e81c5c9eddec478d1d00b221a165b8bcbbe4cac6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80a84279b1278deef6e779786cf38dde6e440267f3672ce0af6972efbcd540ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94e85170edf4cab6ececa0ac9a7323505b22f61ad17976d3e908b01bafa742c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__256fd957e0a8418c94dc97d35ba7b80f6115d4439b2f2336ccf0380d8435b2b1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71aecb02f8b286592082b40d9d8d8d98618439dba0bce048689ddbf7b6afb2b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d12c9ba778ab49f5c2d46d557dab5214863b977091b3f967bba327ead1bda4bc(
    value: typing.Optional[GoogleClouddomainsRegistrationContactSettingsAdminContactPostalAddress],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__447100207d444ba0b8e4b59a1506f42e63ace0d0af73a33e88096a9cfd339c1d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0ad530233682843837bc4b18955fa5016fc98dd4679bd7ce7883f2a0081eb47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e3c9aacfa3fbbe86647a32938976e567a37b927ba2809a932e7b09ff909f686(
    value: typing.Optional[GoogleClouddomainsRegistrationContactSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__931eef4884efd6c9308dfaa2c708e9378980cebf05ddf21d680f0fbfbbaa41b5(
    *,
    email: builtins.str,
    phone_number: builtins.str,
    postal_address: typing.Union[GoogleClouddomainsRegistrationContactSettingsRegistrantContactPostalAddress, typing.Dict[builtins.str, typing.Any]],
    fax_number: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c981be60741d7510b901ff75f390048b56b0e68e61eb6460e60e1d6889530b96(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9dafeded75aa067df85b3d2779212458908b35c6c508959d6d4264f45f98db3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deb2af4b757ff094e1fff3d57fdb17d4e196bae32dd9576c58acbd4ea8efb131(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3acc18b118ccc51b9d52350582349b829bbbeb373e7f352ed196d646f18608e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56feac42d492fffa799350223489a9917cb5979571cf8b6288c4e5a398265624(
    value: typing.Optional[GoogleClouddomainsRegistrationContactSettingsRegistrantContact],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff8c9132fefd2b9023ab95ab9587173b269968ff31b3f715f1628c1916328726(
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

def _typecheckingstub__59f6f95ef03bba518f48e69110200621ade67cd10c57d3b31457d8dbb4bc6317(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6983064682d21352bc2d17958d3d08d28034d48f8f5a07aea505ce7b59139bbf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79868bf3b8a615655327477a727122caf1a515bb5ca685e9fa89ba8d158467ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__598dd28d62846febba38c2801d5e3b1ceefc97aac8c04df0f841d0e523a3392c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82dac7610dda162c2ee6f33fb39572797be31775dcea1c6cdb4d9b753e41695b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4caefb0462d79beaf65605f2fde0819181592d2f05e9db17369b412da26efab9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd70f509be6fdb0c897ca3a1175b3f951da625298628e68e12e1c8b1fb8c56e7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b005e2fe4b10cef95c50829849f378965146d92ad8e40acaff3f351460b18e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb0cf733974ea22815d23a3eb8c5b2b84542eb4e22051cdbcb805b6ae308309a(
    value: typing.Optional[GoogleClouddomainsRegistrationContactSettingsRegistrantContactPostalAddress],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c435694310c55b5d509740cfa648e6a5536cb78f0b366ec780724bb668e1fda(
    *,
    email: builtins.str,
    phone_number: builtins.str,
    postal_address: typing.Union[GoogleClouddomainsRegistrationContactSettingsTechnicalContactPostalAddress, typing.Dict[builtins.str, typing.Any]],
    fax_number: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff2c36e38215559ed3944bcc27694568b3ff5692e1bac7ba93d50abfcab26d22(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0ff41f07f250d0663b4db5b66f8dc5584473163678b15bd147107e76fc090c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80dd2975d9143d524f0f69f83727a34657f1d62fd5f68d7a505e7a1d7c17757f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4af0319412e98b093bd1d941c571279f7367198ad5cdca0c573bdb02f35a31e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b53bd944c5e7a881bf63179f22fe53c03ec9e44c554a4dbc937b4d21591c90bd(
    value: typing.Optional[GoogleClouddomainsRegistrationContactSettingsTechnicalContact],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__325023bf4589db33d94283999e628b345ef214691f5fb0fade3ad6956bb2bf4c(
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

def _typecheckingstub__ef9435b2fdb808f834a1b730d31b1a30677c97e0f530a8b6df9c2adf6dde3758(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7085057724c9107308c0a8a3947caa8715f1fc417d308c2eaa354649a2dcf3e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b7f494b8182b764de0b7a81e2bc7938e8ac6ae1441b3d0456760447751c838d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3acd58dec4c9c58877fb293acb78e9d3455557f654a60d6c985f97cf4b8ff817(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cd3e26c54a8ca71047a63bd5723e95c66cd56d38c056487283c23dc9d9bf540(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3135a6c55c000a97441f2bd567a33c9097c13e43d8afc20bf4b520f3045b41e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__637905b68574c14cac81ee7183791356e22e0ea0f984286f96d15a73cb61be4f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f865737d09034ca4482f5a055e279495a42b70e4a36c73ccbe381ea0869576f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a88d417fb757140987281bce4183d173a2481b8a654c75a6b64aaa400777e51c(
    value: typing.Optional[GoogleClouddomainsRegistrationContactSettingsTechnicalContactPostalAddress],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b79a9bb4c7df315eef8842469489db87b14710e5225e20287863c3b65603f212(
    *,
    custom_dns: typing.Optional[typing.Union[GoogleClouddomainsRegistrationDnsSettingsCustomDns, typing.Dict[builtins.str, typing.Any]]] = None,
    glue_records: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddomainsRegistrationDnsSettingsGlueRecords, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95e52ba66d03eb1bc38f3fe0d2bbc9736b0173ee3a318cb88a317a0161f37a23(
    *,
    name_servers: typing.Sequence[builtins.str],
    ds_records: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddomainsRegistrationDnsSettingsCustomDnsDsRecords, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e006b3a3cc1341e780b441b6dd8b43251553a485eb262da388fcc84c284b4aa9(
    *,
    algorithm: typing.Optional[builtins.str] = None,
    digest: typing.Optional[builtins.str] = None,
    digest_type: typing.Optional[builtins.str] = None,
    key_tag: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aef12ff1200e1f5c37e282754a1df8788877384f82c66ec134610695ca6dc699(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b15367ec098546a2faf1557c5d317a765500f2b0274255057f806c396813c5d8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ff9588b1401fc2ddf11fdc77c73cf27da3d2b2934f57064142991959d7ec246(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00dbd9f8b5ef0692df97bca6c70cb98485224a799ca859516b8effe3b1a13c64(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c4c7be7e82feb97c119c1121e5989993954a0a38eb135cb6dc5aa35f9c9bb71(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75ec0eb1a65438328448ece0ab84b0776e7968c0005341ae8bee1e9ddf9575fe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddomainsRegistrationDnsSettingsCustomDnsDsRecords]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d0791c6916723d4a55aab55c7b0190c11bbbc542b5a1f5d9714c42a5896211f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf4be18e3ce9c0bbb0f80b65b9a0d38f000f90e9efe8cfa1c1c5993745613ea2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b9168f5405023489fdda419f5123d55304bebc0e2c134d62ba214a6ac24a690(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b38a8ac19bf008a249cf96cfeeca4203ec31a38d67783ad52d7b3e97e567e8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c243674851825f7d1b84ab4a245b183adbff0cc67fa318b5f892713f32f17fd3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8a4652e967a347d14b866320361b5154964f650895f2d1c15739ba09e984db6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddomainsRegistrationDnsSettingsCustomDnsDsRecords]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a27dfc616b5d4683416da12c82fd30eefbfc81ea3f0a433f2c16557eb9a78fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__750c308b8799031c15fae645709b0064fdc0f484746e88dbcd71fee0474cce71(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddomainsRegistrationDnsSettingsCustomDnsDsRecords, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6314ecf59e12e7086473cf1d0cd10d1293d572a076a9dc9eb742b2be8aa80b10(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98eb69cb1a666d3dfc3147824dcdb06b1bbdaed7b05e3083bc443b85f290a1e3(
    value: typing.Optional[GoogleClouddomainsRegistrationDnsSettingsCustomDns],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f94cf27fd5e3e4d34b4afbdff3d0ae70ef712df7ccafb1d277ccf0bf16c986a(
    *,
    host_name: builtins.str,
    ipv4_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    ipv6_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__374292ea3819e037c7df1bc58b2bd39276db8295075c7616b33d371b8a1d986a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3653013a035f7ded098b95be85da968200fd575b6dfe6723526993695c4f3a30(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9966294ad1704a02546c496210aa854fe3143d5ba6ef6d5a992eec92dd82bfdb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acde21366728b7397cb6563100df32dc1f0bd2d15212cb9972df6e2700abd6c7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3050e468b6e1b5e5901fa04161bddef1ead946bee95b5f9d021c58b6c7129402(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b51891375b3f37873c22e3c0442f7d05bf19f99a5c31c3226a7b0c1c81c0006b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddomainsRegistrationDnsSettingsGlueRecords]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7073eddc948243b384c934a9018a287305270416681811e3347bb4f3b343083f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caac7b4605ef4a25d4b6099cd90b876c8c1b1f980783eeb78d0e87637714a323(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f54027134259ff5c72037364f969d2b38581beab65ebed308e1d80c4ed07e7fa(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbc8d6b13c4c25419d9a5d407121008d840161778f5c55cbf6e4aaf5cd5f622c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03b348714cc5dc50786707e3d9059d928010b64c1296ad771abe10bcba995ceb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddomainsRegistrationDnsSettingsGlueRecords]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dc753cdac399aae2da79ca40fad3effa10fc729b004384ae205eef8a052d568(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b2419c1a57c74b1fefb63f989273ba4422617c5838d05f90b88758031d85c30(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddomainsRegistrationDnsSettingsGlueRecords, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4d7bf55ee8769b550bdf902118c2293215d4ce9b0a939e828748e15615ddc59(
    value: typing.Optional[GoogleClouddomainsRegistrationDnsSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3706ab355436176639c47f9be8bbcd3600789249a06129bff44c601110b1b9b3(
    *,
    preferred_renewal_method: typing.Optional[builtins.str] = None,
    transfer_lock_state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2de1924fefff37b869f8f3c496bb6e780e65fc7fb2fe089e6415c4669b952d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29c88ee7fe6aa9e89d9d86e9e3458993352104603a3dd51455077e50406a75a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6043f5b17a87b031a4c9600d7570fe213442ea8c6fc265236d19ff5cf2ccb25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eaf758e0db719a11c0d70c4680314b0f7c9faf94f37b675570c1305106ee9ff(
    value: typing.Optional[GoogleClouddomainsRegistrationManagementSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75f26b4a065e946e62b61ffce5a28d50c6c55ac48fcf96d2ce3c47a22f4d83ad(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d24c05d5a2a67aef05cf70c98719c1c4566f6b1858171b3ed50d6d40b5fce9ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f42200652bc4b0cf630603e82d055b6aa5da163b806a9e37ff6f994f29472d78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81c54c7d623e3f7c10b8d94dae77e6b65acae1cee29bd41bf559ae0dd55d0333(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f3a3774afcb29941685aecb8ed2534bd4eadc375027e685caec32a9c5446008(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d908f60404786282ae677e9fa3db91aeabdc502bb3d96950b66856fda7120fcf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddomainsRegistrationTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f1eeede8a4ad51957c622dd685219ad7e8cba832043429e7a45e7112db6656a(
    *,
    currency_code: typing.Optional[builtins.str] = None,
    units: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eb2c334aa26264b91df4f2ecfef40b424ef19482562abe3501b44a116fa759d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__760f0411d9893078acedc7837541dafa050b941946a79ca1d6cf7671ec1e4c5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bff4de39a721a2cc960b7d9864f9cfc13eb6117b479707dc89383a93a08de8d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba56f0bc06ba0dfb3a6b64bd80a95a82ac1445b6fd89a21bf43d8e562b8ebfb1(
    value: typing.Optional[GoogleClouddomainsRegistrationYearlyPrice],
) -> None:
    """Type checking stubs"""
    pass
