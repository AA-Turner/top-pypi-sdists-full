r'''
# `data_azuread_user`

Refer to the Terraform Registry for docs: [`data_azuread_user`](https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/data-sources/user).
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


class DataAzureadUser(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.dataAzureadUser.DataAzureadUser",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/data-sources/user azuread_user}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        employee_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        mail: typing.Optional[builtins.str] = None,
        mail_nickname: typing.Optional[builtins.str] = None,
        object_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataAzureadUserTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_principal_name: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/data-sources/user azuread_user} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param employee_id: The employee identifier assigned to the user by the organisation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/data-sources/user#employee_id DataAzureadUser#employee_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/data-sources/user#id DataAzureadUser#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param mail: The SMTP address for the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/data-sources/user#mail DataAzureadUser#mail}
        :param mail_nickname: The email alias of the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/data-sources/user#mail_nickname DataAzureadUser#mail_nickname}
        :param object_id: The object ID of the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/data-sources/user#object_id DataAzureadUser#object_id}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/data-sources/user#timeouts DataAzureadUser#timeouts}
        :param user_principal_name: The user principal name (UPN) of the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/data-sources/user#user_principal_name DataAzureadUser#user_principal_name}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f2eb5c3b56abd12687b991210cbfcf7505584474a3051b3cb7d27514fbb092d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataAzureadUserConfig(
            employee_id=employee_id,
            id=id,
            mail=mail,
            mail_nickname=mail_nickname,
            object_id=object_id,
            timeouts=timeouts,
            user_principal_name=user_principal_name,
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
        '''Generates CDKTF code for importing a DataAzureadUser resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataAzureadUser to import.
        :param import_from_id: The id of the existing DataAzureadUser that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/data-sources/user#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataAzureadUser to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeeb6e626801550007f29b36a2b25d805f2c63b4406d10b69fabcfa285e0ba9a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(self, *, read: typing.Optional[builtins.str] = None) -> None:
        '''
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/data-sources/user#read DataAzureadUser#read}.
        '''
        value = DataAzureadUserTimeouts(read=read)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetEmployeeId")
    def reset_employee_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmployeeId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMail")
    def reset_mail(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMail", []))

    @jsii.member(jsii_name="resetMailNickname")
    def reset_mail_nickname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMailNickname", []))

    @jsii.member(jsii_name="resetObjectId")
    def reset_object_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObjectId", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUserPrincipalName")
    def reset_user_principal_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserPrincipalName", []))

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
    @jsii.member(jsii_name="accountEnabled")
    def account_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "accountEnabled"))

    @builtins.property
    @jsii.member(jsii_name="ageGroup")
    def age_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ageGroup"))

    @builtins.property
    @jsii.member(jsii_name="businessPhones")
    def business_phones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "businessPhones"))

    @builtins.property
    @jsii.member(jsii_name="city")
    def city(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "city"))

    @builtins.property
    @jsii.member(jsii_name="companyName")
    def company_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "companyName"))

    @builtins.property
    @jsii.member(jsii_name="consentProvidedForMinor")
    def consent_provided_for_minor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consentProvidedForMinor"))

    @builtins.property
    @jsii.member(jsii_name="costCenter")
    def cost_center(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "costCenter"))

    @builtins.property
    @jsii.member(jsii_name="country")
    def country(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "country"))

    @builtins.property
    @jsii.member(jsii_name="creationType")
    def creation_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationType"))

    @builtins.property
    @jsii.member(jsii_name="department")
    def department(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "department"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @builtins.property
    @jsii.member(jsii_name="division")
    def division(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "division"))

    @builtins.property
    @jsii.member(jsii_name="employeeHireDate")
    def employee_hire_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "employeeHireDate"))

    @builtins.property
    @jsii.member(jsii_name="employeeType")
    def employee_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "employeeType"))

    @builtins.property
    @jsii.member(jsii_name="externalUserState")
    def external_user_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalUserState"))

    @builtins.property
    @jsii.member(jsii_name="faxNumber")
    def fax_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "faxNumber"))

    @builtins.property
    @jsii.member(jsii_name="givenName")
    def given_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "givenName"))

    @builtins.property
    @jsii.member(jsii_name="imAddresses")
    def im_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "imAddresses"))

    @builtins.property
    @jsii.member(jsii_name="jobTitle")
    def job_title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobTitle"))

    @builtins.property
    @jsii.member(jsii_name="managerId")
    def manager_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managerId"))

    @builtins.property
    @jsii.member(jsii_name="mobilePhone")
    def mobile_phone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mobilePhone"))

    @builtins.property
    @jsii.member(jsii_name="officeLocation")
    def office_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "officeLocation"))

    @builtins.property
    @jsii.member(jsii_name="onpremisesDistinguishedName")
    def onpremises_distinguished_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onpremisesDistinguishedName"))

    @builtins.property
    @jsii.member(jsii_name="onpremisesDomainName")
    def onpremises_domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onpremisesDomainName"))

    @builtins.property
    @jsii.member(jsii_name="onpremisesImmutableId")
    def onpremises_immutable_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onpremisesImmutableId"))

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
    @jsii.member(jsii_name="otherMails")
    def other_mails(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "otherMails"))

    @builtins.property
    @jsii.member(jsii_name="postalCode")
    def postal_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postalCode"))

    @builtins.property
    @jsii.member(jsii_name="preferredLanguage")
    def preferred_language(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preferredLanguage"))

    @builtins.property
    @jsii.member(jsii_name="proxyAddresses")
    def proxy_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "proxyAddresses"))

    @builtins.property
    @jsii.member(jsii_name="showInAddressList")
    def show_in_address_list(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "showInAddressList"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="streetAddress")
    def street_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "streetAddress"))

    @builtins.property
    @jsii.member(jsii_name="surname")
    def surname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "surname"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DataAzureadUserTimeoutsOutputReference":
        return typing.cast("DataAzureadUserTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="usageLocation")
    def usage_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "usageLocation"))

    @builtins.property
    @jsii.member(jsii_name="userType")
    def user_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userType"))

    @builtins.property
    @jsii.member(jsii_name="employeeIdInput")
    def employee_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "employeeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="mailInput")
    def mail_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mailInput"))

    @builtins.property
    @jsii.member(jsii_name="mailNicknameInput")
    def mail_nickname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mailNicknameInput"))

    @builtins.property
    @jsii.member(jsii_name="objectIdInput")
    def object_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataAzureadUserTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataAzureadUserTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="userPrincipalNameInput")
    def user_principal_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userPrincipalNameInput"))

    @builtins.property
    @jsii.member(jsii_name="employeeId")
    def employee_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "employeeId"))

    @employee_id.setter
    def employee_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dec7b85b5549bf1752402f50cbf43472683db569de63e537714aef99d4f8e2e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "employeeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5aaef3b37e4f31ffdfbc9484b64c4668ecbe029a742e64cd7a7bbc272c7abe69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mail")
    def mail(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mail"))

    @mail.setter
    def mail(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fcd40ea8b7605446b4fdb3d5f7c2a2bfc98b70c1eb43295dd2ae1e06d9422b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mailNickname")
    def mail_nickname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mailNickname"))

    @mail_nickname.setter
    def mail_nickname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__374d1d710cc3ecb4ac7b58de7a56693b01a4b022c4b442333d1f5d402588368d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mailNickname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="objectId")
    def object_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectId"))

    @object_id.setter
    def object_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__020468c8e6d4f7ccc94fa115bdf52ee6a4c0308ec14e26fb5c1d778cc3c5197e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userPrincipalName")
    def user_principal_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userPrincipalName"))

    @user_principal_name.setter
    def user_principal_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3266b2ebceb6a57d6da7301671c4f8c27049eabb3a2d0d8116d41764cf9059b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userPrincipalName", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.dataAzureadUser.DataAzureadUserConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "employee_id": "employeeId",
        "id": "id",
        "mail": "mail",
        "mail_nickname": "mailNickname",
        "object_id": "objectId",
        "timeouts": "timeouts",
        "user_principal_name": "userPrincipalName",
    },
)
class DataAzureadUserConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        employee_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        mail: typing.Optional[builtins.str] = None,
        mail_nickname: typing.Optional[builtins.str] = None,
        object_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataAzureadUserTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_principal_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param employee_id: The employee identifier assigned to the user by the organisation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/data-sources/user#employee_id DataAzureadUser#employee_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/data-sources/user#id DataAzureadUser#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param mail: The SMTP address for the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/data-sources/user#mail DataAzureadUser#mail}
        :param mail_nickname: The email alias of the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/data-sources/user#mail_nickname DataAzureadUser#mail_nickname}
        :param object_id: The object ID of the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/data-sources/user#object_id DataAzureadUser#object_id}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/data-sources/user#timeouts DataAzureadUser#timeouts}
        :param user_principal_name: The user principal name (UPN) of the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/data-sources/user#user_principal_name DataAzureadUser#user_principal_name}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = DataAzureadUserTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b15bfeabbd529af98e72fb4a753bac549f5e9aed10d0d977edaf856b6396f79b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument employee_id", value=employee_id, expected_type=type_hints["employee_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument mail", value=mail, expected_type=type_hints["mail"])
            check_type(argname="argument mail_nickname", value=mail_nickname, expected_type=type_hints["mail_nickname"])
            check_type(argname="argument object_id", value=object_id, expected_type=type_hints["object_id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument user_principal_name", value=user_principal_name, expected_type=type_hints["user_principal_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if employee_id is not None:
            self._values["employee_id"] = employee_id
        if id is not None:
            self._values["id"] = id
        if mail is not None:
            self._values["mail"] = mail
        if mail_nickname is not None:
            self._values["mail_nickname"] = mail_nickname
        if object_id is not None:
            self._values["object_id"] = object_id
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if user_principal_name is not None:
            self._values["user_principal_name"] = user_principal_name

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
    def employee_id(self) -> typing.Optional[builtins.str]:
        '''The employee identifier assigned to the user by the organisation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/data-sources/user#employee_id DataAzureadUser#employee_id}
        '''
        result = self._values.get("employee_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/data-sources/user#id DataAzureadUser#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mail(self) -> typing.Optional[builtins.str]:
        '''The SMTP address for the user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/data-sources/user#mail DataAzureadUser#mail}
        '''
        result = self._values.get("mail")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mail_nickname(self) -> typing.Optional[builtins.str]:
        '''The email alias of the user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/data-sources/user#mail_nickname DataAzureadUser#mail_nickname}
        '''
        result = self._values.get("mail_nickname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def object_id(self) -> typing.Optional[builtins.str]:
        '''The object ID of the user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/data-sources/user#object_id DataAzureadUser#object_id}
        '''
        result = self._values.get("object_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DataAzureadUserTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/data-sources/user#timeouts DataAzureadUser#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataAzureadUserTimeouts"], result)

    @builtins.property
    def user_principal_name(self) -> typing.Optional[builtins.str]:
        '''The user principal name (UPN) of the user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/data-sources/user#user_principal_name DataAzureadUser#user_principal_name}
        '''
        result = self._values.get("user_principal_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAzureadUserConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.dataAzureadUser.DataAzureadUserTimeouts",
    jsii_struct_bases=[],
    name_mapping={"read": "read"},
)
class DataAzureadUserTimeouts:
    def __init__(self, *, read: typing.Optional[builtins.str] = None) -> None:
        '''
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/data-sources/user#read DataAzureadUser#read}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c350b958dce25cf78a155c3377bd4ca8b1eb813ab664adde64f8e3e4049f2d8f)
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if read is not None:
            self._values["read"] = read

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/data-sources/user#read DataAzureadUser#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAzureadUserTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAzureadUserTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.dataAzureadUser.DataAzureadUserTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f4c76cb0e847909ca3c5b4ecbdb74f0f54977eba4c20a9afe3f339c3947463a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

    @builtins.property
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f736fd14c9ad45a89bc377977b0cb9c62458ee8916eca1c33e654c1760027d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataAzureadUserTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataAzureadUserTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataAzureadUserTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a76e0bbc9df0e539b07fae91670af21cf055c3f6902bceda454eacc1ea42b77b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataAzureadUser",
    "DataAzureadUserConfig",
    "DataAzureadUserTimeouts",
    "DataAzureadUserTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__0f2eb5c3b56abd12687b991210cbfcf7505584474a3051b3cb7d27514fbb092d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    employee_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    mail: typing.Optional[builtins.str] = None,
    mail_nickname: typing.Optional[builtins.str] = None,
    object_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataAzureadUserTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_principal_name: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__aeeb6e626801550007f29b36a2b25d805f2c63b4406d10b69fabcfa285e0ba9a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dec7b85b5549bf1752402f50cbf43472683db569de63e537714aef99d4f8e2e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aaef3b37e4f31ffdfbc9484b64c4668ecbe029a742e64cd7a7bbc272c7abe69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fcd40ea8b7605446b4fdb3d5f7c2a2bfc98b70c1eb43295dd2ae1e06d9422b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__374d1d710cc3ecb4ac7b58de7a56693b01a4b022c4b442333d1f5d402588368d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__020468c8e6d4f7ccc94fa115bdf52ee6a4c0308ec14e26fb5c1d778cc3c5197e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3266b2ebceb6a57d6da7301671c4f8c27049eabb3a2d0d8116d41764cf9059b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b15bfeabbd529af98e72fb4a753bac549f5e9aed10d0d977edaf856b6396f79b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    employee_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    mail: typing.Optional[builtins.str] = None,
    mail_nickname: typing.Optional[builtins.str] = None,
    object_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataAzureadUserTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_principal_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c350b958dce25cf78a155c3377bd4ca8b1eb813ab664adde64f8e3e4049f2d8f(
    *,
    read: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f4c76cb0e847909ca3c5b4ecbdb74f0f54977eba4c20a9afe3f339c3947463a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f736fd14c9ad45a89bc377977b0cb9c62458ee8916eca1c33e654c1760027d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a76e0bbc9df0e539b07fae91670af21cf055c3f6902bceda454eacc1ea42b77b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataAzureadUserTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
