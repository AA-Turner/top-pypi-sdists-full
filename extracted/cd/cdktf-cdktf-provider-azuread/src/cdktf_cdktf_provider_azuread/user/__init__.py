r'''
# `azuread_user`

Refer to the Terraform Registry for docs: [`azuread_user`](https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user).
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


class User(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.user.User",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user azuread_user}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        user_principal_name: builtins.str,
        account_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        age_group: typing.Optional[builtins.str] = None,
        business_phones: typing.Optional[typing.Sequence[builtins.str]] = None,
        city: typing.Optional[builtins.str] = None,
        company_name: typing.Optional[builtins.str] = None,
        consent_provided_for_minor: typing.Optional[builtins.str] = None,
        cost_center: typing.Optional[builtins.str] = None,
        country: typing.Optional[builtins.str] = None,
        department: typing.Optional[builtins.str] = None,
        disable_password_expiration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_strong_password: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        division: typing.Optional[builtins.str] = None,
        employee_hire_date: typing.Optional[builtins.str] = None,
        employee_id: typing.Optional[builtins.str] = None,
        employee_type: typing.Optional[builtins.str] = None,
        fax_number: typing.Optional[builtins.str] = None,
        force_password_change: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        given_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        job_title: typing.Optional[builtins.str] = None,
        mail: typing.Optional[builtins.str] = None,
        mail_nickname: typing.Optional[builtins.str] = None,
        manager_id: typing.Optional[builtins.str] = None,
        mobile_phone: typing.Optional[builtins.str] = None,
        office_location: typing.Optional[builtins.str] = None,
        onpremises_immutable_id: typing.Optional[builtins.str] = None,
        other_mails: typing.Optional[typing.Sequence[builtins.str]] = None,
        password: typing.Optional[builtins.str] = None,
        postal_code: typing.Optional[builtins.str] = None,
        preferred_language: typing.Optional[builtins.str] = None,
        show_in_address_list: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        state: typing.Optional[builtins.str] = None,
        street_address: typing.Optional[builtins.str] = None,
        surname: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["UserTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        usage_location: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user azuread_user} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: The name to display in the address book for the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#display_name User#display_name}
        :param user_principal_name: The user principal name (UPN) of the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#user_principal_name User#user_principal_name}
        :param account_enabled: Whether or not the account should be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#account_enabled User#account_enabled}
        :param age_group: The age group of the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#age_group User#age_group}
        :param business_phones: The telephone numbers for the user. Only one number can be set for this property. Read-only for users synced with Azure AD Connect Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#business_phones User#business_phones}
        :param city: The city in which the user is located. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#city User#city}
        :param company_name: The company name which the user is associated. This property can be useful for describing the company that an external user comes from Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#company_name User#company_name}
        :param consent_provided_for_minor: Whether consent has been obtained for minors. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#consent_provided_for_minor User#consent_provided_for_minor}
        :param cost_center: The cost center associated with the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#cost_center User#cost_center}
        :param country: The country/region in which the user is located, e.g. ``US`` or ``UK``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#country User#country}
        :param department: The name for the department in which the user works. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#department User#department}
        :param disable_password_expiration: Whether the users password is exempt from expiring. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#disable_password_expiration User#disable_password_expiration}
        :param disable_strong_password: Whether the user is allowed weaker passwords than the default policy to be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#disable_strong_password User#disable_strong_password}
        :param division: The name of the division in which the user works. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#division User#division}
        :param employee_hire_date: The hire date of the user, formatted as an RFC3339 date string (e.g. ``2018-01-01T01:02:03Z``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#employee_hire_date User#employee_hire_date}
        :param employee_id: The employee identifier assigned to the user by the organisation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#employee_id User#employee_id}
        :param employee_type: Captures enterprise worker type. For example, Employee, Contractor, Consultant, or Vendor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#employee_type User#employee_type}
        :param fax_number: The fax number of the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#fax_number User#fax_number}
        :param force_password_change: Whether the user is forced to change the password during the next sign-in. Only takes effect when also changing the password Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#force_password_change User#force_password_change}
        :param given_name: The given name (first name) of the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#given_name User#given_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#id User#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param job_title: The user’s job title. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#job_title User#job_title}
        :param mail: The SMTP address for the user. Cannot be unset. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#mail User#mail}
        :param mail_nickname: The mail alias for the user. Defaults to the user name part of the user principal name (UPN). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#mail_nickname User#mail_nickname}
        :param manager_id: The object ID of the user's manager. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#manager_id User#manager_id}
        :param mobile_phone: The primary cellular telephone number for the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#mobile_phone User#mobile_phone}
        :param office_location: The office location in the user's place of business. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#office_location User#office_location}
        :param onpremises_immutable_id: The value used to associate an on-premise Active Directory user account with their Azure AD user object. This must be specified if you are using a federated domain for the user's ``user_principal_name`` property when creating a new user account Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#onpremises_immutable_id User#onpremises_immutable_id}
        :param other_mails: Additional email addresses for the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#other_mails User#other_mails}
        :param password: The password for the user. The password must satisfy minimum requirements as specified by the password policy. The maximum length is 256 characters. This property is required when creating a new user Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#password User#password}
        :param postal_code: The postal code for the user's postal address. The postal code is specific to the user's country/region. In the United States of America, this attribute contains the ZIP code Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#postal_code User#postal_code}
        :param preferred_language: The user's preferred language, in ISO 639-1 notation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#preferred_language User#preferred_language}
        :param show_in_address_list: Whether or not the Outlook global address list should include this user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#show_in_address_list User#show_in_address_list}
        :param state: The state or province in the user's address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#state User#state}
        :param street_address: The street address of the user's place of business. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#street_address User#street_address}
        :param surname: The user's surname (family name or last name). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#surname User#surname}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#timeouts User#timeouts}
        :param usage_location: The usage location of the user. Required for users that will be assigned licenses due to legal requirement to check for availability of services in countries. The usage location is a two letter country code (ISO standard 3166). Examples include: ``NO``, ``JP``, and ``GB``. Cannot be reset to null once set Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#usage_location User#usage_location}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2caa3287346913b942de56568fb64d1ad049468e78a6135a6c7b0312e9a8ff0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = UserConfig(
            display_name=display_name,
            user_principal_name=user_principal_name,
            account_enabled=account_enabled,
            age_group=age_group,
            business_phones=business_phones,
            city=city,
            company_name=company_name,
            consent_provided_for_minor=consent_provided_for_minor,
            cost_center=cost_center,
            country=country,
            department=department,
            disable_password_expiration=disable_password_expiration,
            disable_strong_password=disable_strong_password,
            division=division,
            employee_hire_date=employee_hire_date,
            employee_id=employee_id,
            employee_type=employee_type,
            fax_number=fax_number,
            force_password_change=force_password_change,
            given_name=given_name,
            id=id,
            job_title=job_title,
            mail=mail,
            mail_nickname=mail_nickname,
            manager_id=manager_id,
            mobile_phone=mobile_phone,
            office_location=office_location,
            onpremises_immutable_id=onpremises_immutable_id,
            other_mails=other_mails,
            password=password,
            postal_code=postal_code,
            preferred_language=preferred_language,
            show_in_address_list=show_in_address_list,
            state=state,
            street_address=street_address,
            surname=surname,
            timeouts=timeouts,
            usage_location=usage_location,
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
        '''Generates CDKTF code for importing a User resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the User to import.
        :param import_from_id: The id of the existing User that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the User to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc7bf5bdbee23ba23aa89522a3b532b5d5c210e77ba63f1b6dbb460a119cb0a0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#create User#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#delete User#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#read User#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#update User#update}.
        '''
        value = UserTimeouts(create=create, delete=delete, read=read, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAccountEnabled")
    def reset_account_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountEnabled", []))

    @jsii.member(jsii_name="resetAgeGroup")
    def reset_age_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAgeGroup", []))

    @jsii.member(jsii_name="resetBusinessPhones")
    def reset_business_phones(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBusinessPhones", []))

    @jsii.member(jsii_name="resetCity")
    def reset_city(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCity", []))

    @jsii.member(jsii_name="resetCompanyName")
    def reset_company_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompanyName", []))

    @jsii.member(jsii_name="resetConsentProvidedForMinor")
    def reset_consent_provided_for_minor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsentProvidedForMinor", []))

    @jsii.member(jsii_name="resetCostCenter")
    def reset_cost_center(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCostCenter", []))

    @jsii.member(jsii_name="resetCountry")
    def reset_country(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCountry", []))

    @jsii.member(jsii_name="resetDepartment")
    def reset_department(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDepartment", []))

    @jsii.member(jsii_name="resetDisablePasswordExpiration")
    def reset_disable_password_expiration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisablePasswordExpiration", []))

    @jsii.member(jsii_name="resetDisableStrongPassword")
    def reset_disable_strong_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableStrongPassword", []))

    @jsii.member(jsii_name="resetDivision")
    def reset_division(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDivision", []))

    @jsii.member(jsii_name="resetEmployeeHireDate")
    def reset_employee_hire_date(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmployeeHireDate", []))

    @jsii.member(jsii_name="resetEmployeeId")
    def reset_employee_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmployeeId", []))

    @jsii.member(jsii_name="resetEmployeeType")
    def reset_employee_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmployeeType", []))

    @jsii.member(jsii_name="resetFaxNumber")
    def reset_fax_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFaxNumber", []))

    @jsii.member(jsii_name="resetForcePasswordChange")
    def reset_force_password_change(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForcePasswordChange", []))

    @jsii.member(jsii_name="resetGivenName")
    def reset_given_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGivenName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetJobTitle")
    def reset_job_title(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJobTitle", []))

    @jsii.member(jsii_name="resetMail")
    def reset_mail(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMail", []))

    @jsii.member(jsii_name="resetMailNickname")
    def reset_mail_nickname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMailNickname", []))

    @jsii.member(jsii_name="resetManagerId")
    def reset_manager_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagerId", []))

    @jsii.member(jsii_name="resetMobilePhone")
    def reset_mobile_phone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMobilePhone", []))

    @jsii.member(jsii_name="resetOfficeLocation")
    def reset_office_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOfficeLocation", []))

    @jsii.member(jsii_name="resetOnpremisesImmutableId")
    def reset_onpremises_immutable_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnpremisesImmutableId", []))

    @jsii.member(jsii_name="resetOtherMails")
    def reset_other_mails(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOtherMails", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPostalCode")
    def reset_postal_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostalCode", []))

    @jsii.member(jsii_name="resetPreferredLanguage")
    def reset_preferred_language(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreferredLanguage", []))

    @jsii.member(jsii_name="resetShowInAddressList")
    def reset_show_in_address_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShowInAddressList", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

    @jsii.member(jsii_name="resetStreetAddress")
    def reset_street_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStreetAddress", []))

    @jsii.member(jsii_name="resetSurname")
    def reset_surname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSurname", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUsageLocation")
    def reset_usage_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsageLocation", []))

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
    @jsii.member(jsii_name="aboutMe")
    def about_me(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aboutMe"))

    @builtins.property
    @jsii.member(jsii_name="creationType")
    def creation_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationType"))

    @builtins.property
    @jsii.member(jsii_name="externalUserState")
    def external_user_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalUserState"))

    @builtins.property
    @jsii.member(jsii_name="imAddresses")
    def im_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "imAddresses"))

    @builtins.property
    @jsii.member(jsii_name="objectId")
    def object_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectId"))

    @builtins.property
    @jsii.member(jsii_name="onpremisesDistinguishedName")
    def onpremises_distinguished_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onpremisesDistinguishedName"))

    @builtins.property
    @jsii.member(jsii_name="onpremisesDomainName")
    def onpremises_domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onpremisesDomainName"))

    @builtins.property
    @jsii.member(jsii_name="onpremisesSamAccountName")
    def onpremises_sam_account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onpremisesSamAccountName"))

    @builtins.property
    @jsii.member(jsii_name="onpremisesSecurityIdentifier")
    def onpremises_security_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onpremisesSecurityIdentifier"))

    @builtins.property
    @jsii.member(jsii_name="onpremisesSyncEnabled")
    def onpremises_sync_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "onpremisesSyncEnabled"))

    @builtins.property
    @jsii.member(jsii_name="onpremisesUserPrincipalName")
    def onpremises_user_principal_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onpremisesUserPrincipalName"))

    @builtins.property
    @jsii.member(jsii_name="proxyAddresses")
    def proxy_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "proxyAddresses"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "UserTimeoutsOutputReference":
        return typing.cast("UserTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="userType")
    def user_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userType"))

    @builtins.property
    @jsii.member(jsii_name="accountEnabledInput")
    def account_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "accountEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="ageGroupInput")
    def age_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ageGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="businessPhonesInput")
    def business_phones_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "businessPhonesInput"))

    @builtins.property
    @jsii.member(jsii_name="cityInput")
    def city_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cityInput"))

    @builtins.property
    @jsii.member(jsii_name="companyNameInput")
    def company_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "companyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="consentProvidedForMinorInput")
    def consent_provided_for_minor_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consentProvidedForMinorInput"))

    @builtins.property
    @jsii.member(jsii_name="costCenterInput")
    def cost_center_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "costCenterInput"))

    @builtins.property
    @jsii.member(jsii_name="countryInput")
    def country_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countryInput"))

    @builtins.property
    @jsii.member(jsii_name="departmentInput")
    def department_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "departmentInput"))

    @builtins.property
    @jsii.member(jsii_name="disablePasswordExpirationInput")
    def disable_password_expiration_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disablePasswordExpirationInput"))

    @builtins.property
    @jsii.member(jsii_name="disableStrongPasswordInput")
    def disable_strong_password_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableStrongPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="divisionInput")
    def division_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "divisionInput"))

    @builtins.property
    @jsii.member(jsii_name="employeeHireDateInput")
    def employee_hire_date_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "employeeHireDateInput"))

    @builtins.property
    @jsii.member(jsii_name="employeeIdInput")
    def employee_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "employeeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="employeeTypeInput")
    def employee_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "employeeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="faxNumberInput")
    def fax_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "faxNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="forcePasswordChangeInput")
    def force_password_change_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forcePasswordChangeInput"))

    @builtins.property
    @jsii.member(jsii_name="givenNameInput")
    def given_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "givenNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="jobTitleInput")
    def job_title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobTitleInput"))

    @builtins.property
    @jsii.member(jsii_name="mailInput")
    def mail_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mailInput"))

    @builtins.property
    @jsii.member(jsii_name="mailNicknameInput")
    def mail_nickname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mailNicknameInput"))

    @builtins.property
    @jsii.member(jsii_name="managerIdInput")
    def manager_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="mobilePhoneInput")
    def mobile_phone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mobilePhoneInput"))

    @builtins.property
    @jsii.member(jsii_name="officeLocationInput")
    def office_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "officeLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="onpremisesImmutableIdInput")
    def onpremises_immutable_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "onpremisesImmutableIdInput"))

    @builtins.property
    @jsii.member(jsii_name="otherMailsInput")
    def other_mails_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "otherMailsInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="postalCodeInput")
    def postal_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "postalCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="preferredLanguageInput")
    def preferred_language_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preferredLanguageInput"))

    @builtins.property
    @jsii.member(jsii_name="showInAddressListInput")
    def show_in_address_list_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "showInAddressListInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="streetAddressInput")
    def street_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "streetAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="surnameInput")
    def surname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "surnameInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "UserTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "UserTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="usageLocationInput")
    def usage_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usageLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="userPrincipalNameInput")
    def user_principal_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userPrincipalNameInput"))

    @builtins.property
    @jsii.member(jsii_name="accountEnabled")
    def account_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "accountEnabled"))

    @account_enabled.setter
    def account_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b49e86e4caf2ec5ea0a4a585b4346ffceafdc78c4de32db3adae6388b4073f28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ageGroup")
    def age_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ageGroup"))

    @age_group.setter
    def age_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c50c73ac161624abd503e2af84e5d9f951499bff22f0a3ab7ae7031863847ca2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ageGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="businessPhones")
    def business_phones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "businessPhones"))

    @business_phones.setter
    def business_phones(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41e8c82203fb3ccaae84acc04990c6c52bc2ccc2d17f95bc0c50d4e28f45e06c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "businessPhones", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="city")
    def city(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "city"))

    @city.setter
    def city(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22dd7f79acbf389cbc782373caaa493147dfc49fd228df950855a7933370f81f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "city", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="companyName")
    def company_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "companyName"))

    @company_name.setter
    def company_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90665ce81aee406e5b18fbe48936e72395f98abebcda1dc17bce4e78b58fbeb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "companyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="consentProvidedForMinor")
    def consent_provided_for_minor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consentProvidedForMinor"))

    @consent_provided_for_minor.setter
    def consent_provided_for_minor(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbcb71906a2abb24abf360de4cced2938bdfca580a57fba067f161659ffb0d5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consentProvidedForMinor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="costCenter")
    def cost_center(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "costCenter"))

    @cost_center.setter
    def cost_center(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76957dd5481dae13f99ed8594c38cecd50242920dc57a1a889db28758deac0a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "costCenter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="country")
    def country(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "country"))

    @country.setter
    def country(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7262ff363c18cb7072df2afe026808fa52c48fbdafbdd99c3f9827d57eed5f40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "country", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="department")
    def department(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "department"))

    @department.setter
    def department(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9d5eaee78621c40dd139f8d58628a8414eb3bfc7c1eea0faafe27d7be1d95d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "department", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disablePasswordExpiration")
    def disable_password_expiration(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disablePasswordExpiration"))

    @disable_password_expiration.setter
    def disable_password_expiration(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd9b53785e140f1f0dc1a575a408cda9e99851014e05f7e16275f9e3832a1e15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disablePasswordExpiration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableStrongPassword")
    def disable_strong_password(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableStrongPassword"))

    @disable_strong_password.setter
    def disable_strong_password(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8a2962900c4f32be78790b1f4c9af16159ee08995519d9f8b7ee06fb32ff3ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableStrongPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__009c747c52e67e99d6695e08bfee11145cea436df79ed5b92161b6500e4992e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="division")
    def division(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "division"))

    @division.setter
    def division(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9371cbaa50228dacb06827ce9071869ae22a49041574a09b477b7b7c6070879)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "division", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="employeeHireDate")
    def employee_hire_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "employeeHireDate"))

    @employee_hire_date.setter
    def employee_hire_date(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d43b97e320d192e5a11f061577cd961f948f7a6c9e0edad43796c8a142233cba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "employeeHireDate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="employeeId")
    def employee_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "employeeId"))

    @employee_id.setter
    def employee_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5229132f37db8423cc83f87d692d37534cb0f3390f204f09e8f5d32750ccbb0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "employeeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="employeeType")
    def employee_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "employeeType"))

    @employee_type.setter
    def employee_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b68741e39121c6d7f08558b9d8ba49b71deabf38d8f395be7290ae549a7e272)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "employeeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="faxNumber")
    def fax_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "faxNumber"))

    @fax_number.setter
    def fax_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4fa43520b4b48a066a40a9988ef3453c3457964691f78db5483c3dcb2f3fb54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "faxNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forcePasswordChange")
    def force_password_change(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forcePasswordChange"))

    @force_password_change.setter
    def force_password_change(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93d11bc6e8e8243163d9f9a8c3530cc7148c5a5026a9162e58cc0327ab40080a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forcePasswordChange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="givenName")
    def given_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "givenName"))

    @given_name.setter
    def given_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9c104bf4795798543ec4474c9a6b002410dcee0ca185a1044c806c05cf6f396)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "givenName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31689e394bff1a86f7c40428b7ecd764427d4adb777df9ee1057418f3906d2ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jobTitle")
    def job_title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobTitle"))

    @job_title.setter
    def job_title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf4d24f8a8fef346ad3f8b1829ab7d3624fe90ded3c416c6db99916f25cd3177)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobTitle", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mail")
    def mail(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mail"))

    @mail.setter
    def mail(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba5f5f0134efed55fc910211ebbf0859e06ba80168099cb22092c3812e86ce21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mailNickname")
    def mail_nickname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mailNickname"))

    @mail_nickname.setter
    def mail_nickname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__406b1b896061fec42ecc1858600163c92863e8498fca73b6cce038cf9d09f92d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mailNickname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="managerId")
    def manager_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managerId"))

    @manager_id.setter
    def manager_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d015e83e6638818c2191a8691fd97eb71d9f7fb3dfbe46bb207eb5d98a861cbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mobilePhone")
    def mobile_phone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mobilePhone"))

    @mobile_phone.setter
    def mobile_phone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ab5ea7d135688aec8be58d8478f881bd383725413bfc247023fb2f6de79203b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mobilePhone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="officeLocation")
    def office_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "officeLocation"))

    @office_location.setter
    def office_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__172a8714b336f95faae2993bb71f7b397cbb3b3b475e4ad6347db457f4df786e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "officeLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onpremisesImmutableId")
    def onpremises_immutable_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onpremisesImmutableId"))

    @onpremises_immutable_id.setter
    def onpremises_immutable_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f42023e96f5d7da06b5714aa9046f478af58f233d8701468c4dc812b99fc47e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onpremisesImmutableId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="otherMails")
    def other_mails(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "otherMails"))

    @other_mails.setter
    def other_mails(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55d1a86d9d6841d8591d73dde19d9466e037bfd925c88bf7ed5996a9c237cbd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "otherMails", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b4511de15e21e0c907b1c24677a379d1149b5deb7ad6b3a87ff877a5548d2a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postalCode")
    def postal_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postalCode"))

    @postal_code.setter
    def postal_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4d707cde43232ba9c945ea0032818328f521f7ae4f1e0b34096ecaa098edd89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postalCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preferredLanguage")
    def preferred_language(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preferredLanguage"))

    @preferred_language.setter
    def preferred_language(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c887d7de3986a1fc5b17c10e2efb5576bb7caad15a9e131ebcbf31241a70b017)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredLanguage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="showInAddressList")
    def show_in_address_list(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "showInAddressList"))

    @show_in_address_list.setter
    def show_in_address_list(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3bf84b8717cccbf13c8662afd24f1b7d8bb07753a2bd2df0dd06286943fa42b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "showInAddressList", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__701ae591d68934b192ce532b50e0d6d8128ec41bfe0f2bfd5466049e4177fb0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="streetAddress")
    def street_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "streetAddress"))

    @street_address.setter
    def street_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef84c53165148a84cb95330e1ae27af4fa77480fb8819131104617ca7bccc3f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streetAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="surname")
    def surname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "surname"))

    @surname.setter
    def surname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6f3d8e6cc6eac725bbc94af6e972e5ca0cffa0b9d854d7657099e5a8195658f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "surname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="usageLocation")
    def usage_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "usageLocation"))

    @usage_location.setter
    def usage_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__397519792c24bf90db9b2c933fe54b848403b1657821e75e3ef22092a585e5ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usageLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userPrincipalName")
    def user_principal_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userPrincipalName"))

    @user_principal_name.setter
    def user_principal_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61c08befc89ec67d14751825629bcb2b08195210409bd1f959439cacc53c3b75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userPrincipalName", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.user.UserConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "display_name": "displayName",
        "user_principal_name": "userPrincipalName",
        "account_enabled": "accountEnabled",
        "age_group": "ageGroup",
        "business_phones": "businessPhones",
        "city": "city",
        "company_name": "companyName",
        "consent_provided_for_minor": "consentProvidedForMinor",
        "cost_center": "costCenter",
        "country": "country",
        "department": "department",
        "disable_password_expiration": "disablePasswordExpiration",
        "disable_strong_password": "disableStrongPassword",
        "division": "division",
        "employee_hire_date": "employeeHireDate",
        "employee_id": "employeeId",
        "employee_type": "employeeType",
        "fax_number": "faxNumber",
        "force_password_change": "forcePasswordChange",
        "given_name": "givenName",
        "id": "id",
        "job_title": "jobTitle",
        "mail": "mail",
        "mail_nickname": "mailNickname",
        "manager_id": "managerId",
        "mobile_phone": "mobilePhone",
        "office_location": "officeLocation",
        "onpremises_immutable_id": "onpremisesImmutableId",
        "other_mails": "otherMails",
        "password": "password",
        "postal_code": "postalCode",
        "preferred_language": "preferredLanguage",
        "show_in_address_list": "showInAddressList",
        "state": "state",
        "street_address": "streetAddress",
        "surname": "surname",
        "timeouts": "timeouts",
        "usage_location": "usageLocation",
    },
)
class UserConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        display_name: builtins.str,
        user_principal_name: builtins.str,
        account_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        age_group: typing.Optional[builtins.str] = None,
        business_phones: typing.Optional[typing.Sequence[builtins.str]] = None,
        city: typing.Optional[builtins.str] = None,
        company_name: typing.Optional[builtins.str] = None,
        consent_provided_for_minor: typing.Optional[builtins.str] = None,
        cost_center: typing.Optional[builtins.str] = None,
        country: typing.Optional[builtins.str] = None,
        department: typing.Optional[builtins.str] = None,
        disable_password_expiration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_strong_password: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        division: typing.Optional[builtins.str] = None,
        employee_hire_date: typing.Optional[builtins.str] = None,
        employee_id: typing.Optional[builtins.str] = None,
        employee_type: typing.Optional[builtins.str] = None,
        fax_number: typing.Optional[builtins.str] = None,
        force_password_change: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        given_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        job_title: typing.Optional[builtins.str] = None,
        mail: typing.Optional[builtins.str] = None,
        mail_nickname: typing.Optional[builtins.str] = None,
        manager_id: typing.Optional[builtins.str] = None,
        mobile_phone: typing.Optional[builtins.str] = None,
        office_location: typing.Optional[builtins.str] = None,
        onpremises_immutable_id: typing.Optional[builtins.str] = None,
        other_mails: typing.Optional[typing.Sequence[builtins.str]] = None,
        password: typing.Optional[builtins.str] = None,
        postal_code: typing.Optional[builtins.str] = None,
        preferred_language: typing.Optional[builtins.str] = None,
        show_in_address_list: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        state: typing.Optional[builtins.str] = None,
        street_address: typing.Optional[builtins.str] = None,
        surname: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["UserTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        usage_location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: The name to display in the address book for the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#display_name User#display_name}
        :param user_principal_name: The user principal name (UPN) of the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#user_principal_name User#user_principal_name}
        :param account_enabled: Whether or not the account should be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#account_enabled User#account_enabled}
        :param age_group: The age group of the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#age_group User#age_group}
        :param business_phones: The telephone numbers for the user. Only one number can be set for this property. Read-only for users synced with Azure AD Connect Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#business_phones User#business_phones}
        :param city: The city in which the user is located. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#city User#city}
        :param company_name: The company name which the user is associated. This property can be useful for describing the company that an external user comes from Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#company_name User#company_name}
        :param consent_provided_for_minor: Whether consent has been obtained for minors. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#consent_provided_for_minor User#consent_provided_for_minor}
        :param cost_center: The cost center associated with the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#cost_center User#cost_center}
        :param country: The country/region in which the user is located, e.g. ``US`` or ``UK``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#country User#country}
        :param department: The name for the department in which the user works. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#department User#department}
        :param disable_password_expiration: Whether the users password is exempt from expiring. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#disable_password_expiration User#disable_password_expiration}
        :param disable_strong_password: Whether the user is allowed weaker passwords than the default policy to be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#disable_strong_password User#disable_strong_password}
        :param division: The name of the division in which the user works. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#division User#division}
        :param employee_hire_date: The hire date of the user, formatted as an RFC3339 date string (e.g. ``2018-01-01T01:02:03Z``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#employee_hire_date User#employee_hire_date}
        :param employee_id: The employee identifier assigned to the user by the organisation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#employee_id User#employee_id}
        :param employee_type: Captures enterprise worker type. For example, Employee, Contractor, Consultant, or Vendor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#employee_type User#employee_type}
        :param fax_number: The fax number of the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#fax_number User#fax_number}
        :param force_password_change: Whether the user is forced to change the password during the next sign-in. Only takes effect when also changing the password Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#force_password_change User#force_password_change}
        :param given_name: The given name (first name) of the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#given_name User#given_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#id User#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param job_title: The user’s job title. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#job_title User#job_title}
        :param mail: The SMTP address for the user. Cannot be unset. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#mail User#mail}
        :param mail_nickname: The mail alias for the user. Defaults to the user name part of the user principal name (UPN). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#mail_nickname User#mail_nickname}
        :param manager_id: The object ID of the user's manager. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#manager_id User#manager_id}
        :param mobile_phone: The primary cellular telephone number for the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#mobile_phone User#mobile_phone}
        :param office_location: The office location in the user's place of business. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#office_location User#office_location}
        :param onpremises_immutable_id: The value used to associate an on-premise Active Directory user account with their Azure AD user object. This must be specified if you are using a federated domain for the user's ``user_principal_name`` property when creating a new user account Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#onpremises_immutable_id User#onpremises_immutable_id}
        :param other_mails: Additional email addresses for the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#other_mails User#other_mails}
        :param password: The password for the user. The password must satisfy minimum requirements as specified by the password policy. The maximum length is 256 characters. This property is required when creating a new user Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#password User#password}
        :param postal_code: The postal code for the user's postal address. The postal code is specific to the user's country/region. In the United States of America, this attribute contains the ZIP code Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#postal_code User#postal_code}
        :param preferred_language: The user's preferred language, in ISO 639-1 notation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#preferred_language User#preferred_language}
        :param show_in_address_list: Whether or not the Outlook global address list should include this user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#show_in_address_list User#show_in_address_list}
        :param state: The state or province in the user's address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#state User#state}
        :param street_address: The street address of the user's place of business. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#street_address User#street_address}
        :param surname: The user's surname (family name or last name). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#surname User#surname}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#timeouts User#timeouts}
        :param usage_location: The usage location of the user. Required for users that will be assigned licenses due to legal requirement to check for availability of services in countries. The usage location is a two letter country code (ISO standard 3166). Examples include: ``NO``, ``JP``, and ``GB``. Cannot be reset to null once set Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#usage_location User#usage_location}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = UserTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9153058857c3bf2b274914b6e038133983dc23801d9cc65d324ef3797c4c2e1)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument user_principal_name", value=user_principal_name, expected_type=type_hints["user_principal_name"])
            check_type(argname="argument account_enabled", value=account_enabled, expected_type=type_hints["account_enabled"])
            check_type(argname="argument age_group", value=age_group, expected_type=type_hints["age_group"])
            check_type(argname="argument business_phones", value=business_phones, expected_type=type_hints["business_phones"])
            check_type(argname="argument city", value=city, expected_type=type_hints["city"])
            check_type(argname="argument company_name", value=company_name, expected_type=type_hints["company_name"])
            check_type(argname="argument consent_provided_for_minor", value=consent_provided_for_minor, expected_type=type_hints["consent_provided_for_minor"])
            check_type(argname="argument cost_center", value=cost_center, expected_type=type_hints["cost_center"])
            check_type(argname="argument country", value=country, expected_type=type_hints["country"])
            check_type(argname="argument department", value=department, expected_type=type_hints["department"])
            check_type(argname="argument disable_password_expiration", value=disable_password_expiration, expected_type=type_hints["disable_password_expiration"])
            check_type(argname="argument disable_strong_password", value=disable_strong_password, expected_type=type_hints["disable_strong_password"])
            check_type(argname="argument division", value=division, expected_type=type_hints["division"])
            check_type(argname="argument employee_hire_date", value=employee_hire_date, expected_type=type_hints["employee_hire_date"])
            check_type(argname="argument employee_id", value=employee_id, expected_type=type_hints["employee_id"])
            check_type(argname="argument employee_type", value=employee_type, expected_type=type_hints["employee_type"])
            check_type(argname="argument fax_number", value=fax_number, expected_type=type_hints["fax_number"])
            check_type(argname="argument force_password_change", value=force_password_change, expected_type=type_hints["force_password_change"])
            check_type(argname="argument given_name", value=given_name, expected_type=type_hints["given_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument job_title", value=job_title, expected_type=type_hints["job_title"])
            check_type(argname="argument mail", value=mail, expected_type=type_hints["mail"])
            check_type(argname="argument mail_nickname", value=mail_nickname, expected_type=type_hints["mail_nickname"])
            check_type(argname="argument manager_id", value=manager_id, expected_type=type_hints["manager_id"])
            check_type(argname="argument mobile_phone", value=mobile_phone, expected_type=type_hints["mobile_phone"])
            check_type(argname="argument office_location", value=office_location, expected_type=type_hints["office_location"])
            check_type(argname="argument onpremises_immutable_id", value=onpremises_immutable_id, expected_type=type_hints["onpremises_immutable_id"])
            check_type(argname="argument other_mails", value=other_mails, expected_type=type_hints["other_mails"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument postal_code", value=postal_code, expected_type=type_hints["postal_code"])
            check_type(argname="argument preferred_language", value=preferred_language, expected_type=type_hints["preferred_language"])
            check_type(argname="argument show_in_address_list", value=show_in_address_list, expected_type=type_hints["show_in_address_list"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument street_address", value=street_address, expected_type=type_hints["street_address"])
            check_type(argname="argument surname", value=surname, expected_type=type_hints["surname"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument usage_location", value=usage_location, expected_type=type_hints["usage_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
            "user_principal_name": user_principal_name,
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
        if account_enabled is not None:
            self._values["account_enabled"] = account_enabled
        if age_group is not None:
            self._values["age_group"] = age_group
        if business_phones is not None:
            self._values["business_phones"] = business_phones
        if city is not None:
            self._values["city"] = city
        if company_name is not None:
            self._values["company_name"] = company_name
        if consent_provided_for_minor is not None:
            self._values["consent_provided_for_minor"] = consent_provided_for_minor
        if cost_center is not None:
            self._values["cost_center"] = cost_center
        if country is not None:
            self._values["country"] = country
        if department is not None:
            self._values["department"] = department
        if disable_password_expiration is not None:
            self._values["disable_password_expiration"] = disable_password_expiration
        if disable_strong_password is not None:
            self._values["disable_strong_password"] = disable_strong_password
        if division is not None:
            self._values["division"] = division
        if employee_hire_date is not None:
            self._values["employee_hire_date"] = employee_hire_date
        if employee_id is not None:
            self._values["employee_id"] = employee_id
        if employee_type is not None:
            self._values["employee_type"] = employee_type
        if fax_number is not None:
            self._values["fax_number"] = fax_number
        if force_password_change is not None:
            self._values["force_password_change"] = force_password_change
        if given_name is not None:
            self._values["given_name"] = given_name
        if id is not None:
            self._values["id"] = id
        if job_title is not None:
            self._values["job_title"] = job_title
        if mail is not None:
            self._values["mail"] = mail
        if mail_nickname is not None:
            self._values["mail_nickname"] = mail_nickname
        if manager_id is not None:
            self._values["manager_id"] = manager_id
        if mobile_phone is not None:
            self._values["mobile_phone"] = mobile_phone
        if office_location is not None:
            self._values["office_location"] = office_location
        if onpremises_immutable_id is not None:
            self._values["onpremises_immutable_id"] = onpremises_immutable_id
        if other_mails is not None:
            self._values["other_mails"] = other_mails
        if password is not None:
            self._values["password"] = password
        if postal_code is not None:
            self._values["postal_code"] = postal_code
        if preferred_language is not None:
            self._values["preferred_language"] = preferred_language
        if show_in_address_list is not None:
            self._values["show_in_address_list"] = show_in_address_list
        if state is not None:
            self._values["state"] = state
        if street_address is not None:
            self._values["street_address"] = street_address
        if surname is not None:
            self._values["surname"] = surname
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if usage_location is not None:
            self._values["usage_location"] = usage_location

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
    def display_name(self) -> builtins.str:
        '''The name to display in the address book for the user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#display_name User#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_principal_name(self) -> builtins.str:
        '''The user principal name (UPN) of the user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#user_principal_name User#user_principal_name}
        '''
        result = self._values.get("user_principal_name")
        assert result is not None, "Required property 'user_principal_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not the account should be enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#account_enabled User#account_enabled}
        '''
        result = self._values.get("account_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def age_group(self) -> typing.Optional[builtins.str]:
        '''The age group of the user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#age_group User#age_group}
        '''
        result = self._values.get("age_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def business_phones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The telephone numbers for the user.

        Only one number can be set for this property. Read-only for users synced with Azure AD Connect

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#business_phones User#business_phones}
        '''
        result = self._values.get("business_phones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def city(self) -> typing.Optional[builtins.str]:
        '''The city in which the user is located.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#city User#city}
        '''
        result = self._values.get("city")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def company_name(self) -> typing.Optional[builtins.str]:
        '''The company name which the user is associated.

        This property can be useful for describing the company that an external user comes from

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#company_name User#company_name}
        '''
        result = self._values.get("company_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def consent_provided_for_minor(self) -> typing.Optional[builtins.str]:
        '''Whether consent has been obtained for minors.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#consent_provided_for_minor User#consent_provided_for_minor}
        '''
        result = self._values.get("consent_provided_for_minor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cost_center(self) -> typing.Optional[builtins.str]:
        '''The cost center associated with the user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#cost_center User#cost_center}
        '''
        result = self._values.get("cost_center")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def country(self) -> typing.Optional[builtins.str]:
        '''The country/region in which the user is located, e.g. ``US`` or ``UK``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#country User#country}
        '''
        result = self._values.get("country")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def department(self) -> typing.Optional[builtins.str]:
        '''The name for the department in which the user works.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#department User#department}
        '''
        result = self._values.get("department")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_password_expiration(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the users password is exempt from expiring.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#disable_password_expiration User#disable_password_expiration}
        '''
        result = self._values.get("disable_password_expiration")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disable_strong_password(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the user is allowed weaker passwords than the default policy to be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#disable_strong_password User#disable_strong_password}
        '''
        result = self._values.get("disable_strong_password")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def division(self) -> typing.Optional[builtins.str]:
        '''The name of the division in which the user works.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#division User#division}
        '''
        result = self._values.get("division")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def employee_hire_date(self) -> typing.Optional[builtins.str]:
        '''The hire date of the user, formatted as an RFC3339 date string (e.g. ``2018-01-01T01:02:03Z``).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#employee_hire_date User#employee_hire_date}
        '''
        result = self._values.get("employee_hire_date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def employee_id(self) -> typing.Optional[builtins.str]:
        '''The employee identifier assigned to the user by the organisation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#employee_id User#employee_id}
        '''
        result = self._values.get("employee_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def employee_type(self) -> typing.Optional[builtins.str]:
        '''Captures enterprise worker type. For example, Employee, Contractor, Consultant, or Vendor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#employee_type User#employee_type}
        '''
        result = self._values.get("employee_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fax_number(self) -> typing.Optional[builtins.str]:
        '''The fax number of the user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#fax_number User#fax_number}
        '''
        result = self._values.get("fax_number")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def force_password_change(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the user is forced to change the password during the next sign-in.

        Only takes effect when also changing the password

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#force_password_change User#force_password_change}
        '''
        result = self._values.get("force_password_change")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def given_name(self) -> typing.Optional[builtins.str]:
        '''The given name (first name) of the user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#given_name User#given_name}
        '''
        result = self._values.get("given_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#id User#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_title(self) -> typing.Optional[builtins.str]:
        '''The user’s job title.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#job_title User#job_title}
        '''
        result = self._values.get("job_title")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mail(self) -> typing.Optional[builtins.str]:
        '''The SMTP address for the user. Cannot be unset.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#mail User#mail}
        '''
        result = self._values.get("mail")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mail_nickname(self) -> typing.Optional[builtins.str]:
        '''The mail alias for the user. Defaults to the user name part of the user principal name (UPN).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#mail_nickname User#mail_nickname}
        '''
        result = self._values.get("mail_nickname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def manager_id(self) -> typing.Optional[builtins.str]:
        '''The object ID of the user's manager.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#manager_id User#manager_id}
        '''
        result = self._values.get("manager_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mobile_phone(self) -> typing.Optional[builtins.str]:
        '''The primary cellular telephone number for the user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#mobile_phone User#mobile_phone}
        '''
        result = self._values.get("mobile_phone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def office_location(self) -> typing.Optional[builtins.str]:
        '''The office location in the user's place of business.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#office_location User#office_location}
        '''
        result = self._values.get("office_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def onpremises_immutable_id(self) -> typing.Optional[builtins.str]:
        '''The value used to associate an on-premise Active Directory user account with their Azure AD user object.

        This must be specified if you are using a federated domain for the user's ``user_principal_name`` property when creating a new user account

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#onpremises_immutable_id User#onpremises_immutable_id}
        '''
        result = self._values.get("onpremises_immutable_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def other_mails(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Additional email addresses for the user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#other_mails User#other_mails}
        '''
        result = self._values.get("other_mails")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''The password for the user.

        The password must satisfy minimum requirements as specified by the password policy. The maximum length is 256 characters. This property is required when creating a new user

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#password User#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def postal_code(self) -> typing.Optional[builtins.str]:
        '''The postal code for the user's postal address.

        The postal code is specific to the user's country/region. In the United States of America, this attribute contains the ZIP code

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#postal_code User#postal_code}
        '''
        result = self._values.get("postal_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preferred_language(self) -> typing.Optional[builtins.str]:
        '''The user's preferred language, in ISO 639-1 notation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#preferred_language User#preferred_language}
        '''
        result = self._values.get("preferred_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def show_in_address_list(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not the Outlook global address list should include this user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#show_in_address_list User#show_in_address_list}
        '''
        result = self._values.get("show_in_address_list")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''The state or province in the user's address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#state User#state}
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def street_address(self) -> typing.Optional[builtins.str]:
        '''The street address of the user's place of business.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#street_address User#street_address}
        '''
        result = self._values.get("street_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def surname(self) -> typing.Optional[builtins.str]:
        '''The user's surname (family name or last name).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#surname User#surname}
        '''
        result = self._values.get("surname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["UserTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#timeouts User#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["UserTimeouts"], result)

    @builtins.property
    def usage_location(self) -> typing.Optional[builtins.str]:
        '''The usage location of the user.

        Required for users that will be assigned licenses due to legal requirement to check for availability of services in countries. The usage location is a two letter country code (ISO standard 3166). Examples include: ``NO``, ``JP``, and ``GB``. Cannot be reset to null once set

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#usage_location User#usage_location}
        '''
        result = self._values.get("usage_location")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.user.UserTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class UserTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#create User#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#delete User#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#read User#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#update User#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edb3e871e66b06960cf328cde7ac13dcd8879a4dc3dab43bc4163c67d31283cb)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#create User#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#delete User#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#read User#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/user#update User#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.user.UserTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74b49a9a0065df396d0fe868ca98a17a11024269822b3a371a617cbdbf231988)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f646af121667a7b64a307304c2eb95d7bac3e74fbe1ea48fd004c4fce42d6bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc3d2e514bad0366619321d23a611511663a93563310a40b4510e2cacdb2f330)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__474a86d42abed2c03a5e2808f7c38047139822b8196edbcef802d419eac5b68c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d67bb0dc8e63e4f514b17570a462221267d843445d899d50d3e11dc46c92260f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, UserTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, UserTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, UserTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cab1a121948619e1231bb0c411634565afdf5b0175eabe9b685663af5410c5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "User",
    "UserConfig",
    "UserTimeouts",
    "UserTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__a2caa3287346913b942de56568fb64d1ad049468e78a6135a6c7b0312e9a8ff0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    user_principal_name: builtins.str,
    account_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    age_group: typing.Optional[builtins.str] = None,
    business_phones: typing.Optional[typing.Sequence[builtins.str]] = None,
    city: typing.Optional[builtins.str] = None,
    company_name: typing.Optional[builtins.str] = None,
    consent_provided_for_minor: typing.Optional[builtins.str] = None,
    cost_center: typing.Optional[builtins.str] = None,
    country: typing.Optional[builtins.str] = None,
    department: typing.Optional[builtins.str] = None,
    disable_password_expiration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_strong_password: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    division: typing.Optional[builtins.str] = None,
    employee_hire_date: typing.Optional[builtins.str] = None,
    employee_id: typing.Optional[builtins.str] = None,
    employee_type: typing.Optional[builtins.str] = None,
    fax_number: typing.Optional[builtins.str] = None,
    force_password_change: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    given_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    job_title: typing.Optional[builtins.str] = None,
    mail: typing.Optional[builtins.str] = None,
    mail_nickname: typing.Optional[builtins.str] = None,
    manager_id: typing.Optional[builtins.str] = None,
    mobile_phone: typing.Optional[builtins.str] = None,
    office_location: typing.Optional[builtins.str] = None,
    onpremises_immutable_id: typing.Optional[builtins.str] = None,
    other_mails: typing.Optional[typing.Sequence[builtins.str]] = None,
    password: typing.Optional[builtins.str] = None,
    postal_code: typing.Optional[builtins.str] = None,
    preferred_language: typing.Optional[builtins.str] = None,
    show_in_address_list: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    state: typing.Optional[builtins.str] = None,
    street_address: typing.Optional[builtins.str] = None,
    surname: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[UserTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    usage_location: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__fc7bf5bdbee23ba23aa89522a3b532b5d5c210e77ba63f1b6dbb460a119cb0a0(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b49e86e4caf2ec5ea0a4a585b4346ffceafdc78c4de32db3adae6388b4073f28(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c50c73ac161624abd503e2af84e5d9f951499bff22f0a3ab7ae7031863847ca2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41e8c82203fb3ccaae84acc04990c6c52bc2ccc2d17f95bc0c50d4e28f45e06c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22dd7f79acbf389cbc782373caaa493147dfc49fd228df950855a7933370f81f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90665ce81aee406e5b18fbe48936e72395f98abebcda1dc17bce4e78b58fbeb2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbcb71906a2abb24abf360de4cced2938bdfca580a57fba067f161659ffb0d5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76957dd5481dae13f99ed8594c38cecd50242920dc57a1a889db28758deac0a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7262ff363c18cb7072df2afe026808fa52c48fbdafbdd99c3f9827d57eed5f40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9d5eaee78621c40dd139f8d58628a8414eb3bfc7c1eea0faafe27d7be1d95d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd9b53785e140f1f0dc1a575a408cda9e99851014e05f7e16275f9e3832a1e15(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8a2962900c4f32be78790b1f4c9af16159ee08995519d9f8b7ee06fb32ff3ad(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__009c747c52e67e99d6695e08bfee11145cea436df79ed5b92161b6500e4992e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9371cbaa50228dacb06827ce9071869ae22a49041574a09b477b7b7c6070879(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d43b97e320d192e5a11f061577cd961f948f7a6c9e0edad43796c8a142233cba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5229132f37db8423cc83f87d692d37534cb0f3390f204f09e8f5d32750ccbb0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b68741e39121c6d7f08558b9d8ba49b71deabf38d8f395be7290ae549a7e272(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4fa43520b4b48a066a40a9988ef3453c3457964691f78db5483c3dcb2f3fb54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93d11bc6e8e8243163d9f9a8c3530cc7148c5a5026a9162e58cc0327ab40080a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9c104bf4795798543ec4474c9a6b002410dcee0ca185a1044c806c05cf6f396(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31689e394bff1a86f7c40428b7ecd764427d4adb777df9ee1057418f3906d2ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf4d24f8a8fef346ad3f8b1829ab7d3624fe90ded3c416c6db99916f25cd3177(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba5f5f0134efed55fc910211ebbf0859e06ba80168099cb22092c3812e86ce21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__406b1b896061fec42ecc1858600163c92863e8498fca73b6cce038cf9d09f92d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d015e83e6638818c2191a8691fd97eb71d9f7fb3dfbe46bb207eb5d98a861cbc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ab5ea7d135688aec8be58d8478f881bd383725413bfc247023fb2f6de79203b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__172a8714b336f95faae2993bb71f7b397cbb3b3b475e4ad6347db457f4df786e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f42023e96f5d7da06b5714aa9046f478af58f233d8701468c4dc812b99fc47e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55d1a86d9d6841d8591d73dde19d9466e037bfd925c88bf7ed5996a9c237cbd8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b4511de15e21e0c907b1c24677a379d1149b5deb7ad6b3a87ff877a5548d2a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4d707cde43232ba9c945ea0032818328f521f7ae4f1e0b34096ecaa098edd89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c887d7de3986a1fc5b17c10e2efb5576bb7caad15a9e131ebcbf31241a70b017(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3bf84b8717cccbf13c8662afd24f1b7d8bb07753a2bd2df0dd06286943fa42b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__701ae591d68934b192ce532b50e0d6d8128ec41bfe0f2bfd5466049e4177fb0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef84c53165148a84cb95330e1ae27af4fa77480fb8819131104617ca7bccc3f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6f3d8e6cc6eac725bbc94af6e972e5ca0cffa0b9d854d7657099e5a8195658f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__397519792c24bf90db9b2c933fe54b848403b1657821e75e3ef22092a585e5ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61c08befc89ec67d14751825629bcb2b08195210409bd1f959439cacc53c3b75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9153058857c3bf2b274914b6e038133983dc23801d9cc65d324ef3797c4c2e1(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: builtins.str,
    user_principal_name: builtins.str,
    account_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    age_group: typing.Optional[builtins.str] = None,
    business_phones: typing.Optional[typing.Sequence[builtins.str]] = None,
    city: typing.Optional[builtins.str] = None,
    company_name: typing.Optional[builtins.str] = None,
    consent_provided_for_minor: typing.Optional[builtins.str] = None,
    cost_center: typing.Optional[builtins.str] = None,
    country: typing.Optional[builtins.str] = None,
    department: typing.Optional[builtins.str] = None,
    disable_password_expiration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_strong_password: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    division: typing.Optional[builtins.str] = None,
    employee_hire_date: typing.Optional[builtins.str] = None,
    employee_id: typing.Optional[builtins.str] = None,
    employee_type: typing.Optional[builtins.str] = None,
    fax_number: typing.Optional[builtins.str] = None,
    force_password_change: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    given_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    job_title: typing.Optional[builtins.str] = None,
    mail: typing.Optional[builtins.str] = None,
    mail_nickname: typing.Optional[builtins.str] = None,
    manager_id: typing.Optional[builtins.str] = None,
    mobile_phone: typing.Optional[builtins.str] = None,
    office_location: typing.Optional[builtins.str] = None,
    onpremises_immutable_id: typing.Optional[builtins.str] = None,
    other_mails: typing.Optional[typing.Sequence[builtins.str]] = None,
    password: typing.Optional[builtins.str] = None,
    postal_code: typing.Optional[builtins.str] = None,
    preferred_language: typing.Optional[builtins.str] = None,
    show_in_address_list: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    state: typing.Optional[builtins.str] = None,
    street_address: typing.Optional[builtins.str] = None,
    surname: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[UserTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    usage_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edb3e871e66b06960cf328cde7ac13dcd8879a4dc3dab43bc4163c67d31283cb(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74b49a9a0065df396d0fe868ca98a17a11024269822b3a371a617cbdbf231988(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f646af121667a7b64a307304c2eb95d7bac3e74fbe1ea48fd004c4fce42d6bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc3d2e514bad0366619321d23a611511663a93563310a40b4510e2cacdb2f330(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__474a86d42abed2c03a5e2808f7c38047139822b8196edbcef802d419eac5b68c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d67bb0dc8e63e4f514b17570a462221267d843445d899d50d3e11dc46c92260f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cab1a121948619e1231bb0c411634565afdf5b0175eabe9b685663af5410c5a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, UserTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
