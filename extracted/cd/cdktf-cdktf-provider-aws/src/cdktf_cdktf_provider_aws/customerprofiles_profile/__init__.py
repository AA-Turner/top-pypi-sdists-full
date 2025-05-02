r'''
# `aws_customerprofiles_profile`

Refer to the Terraform Registry for docs: [`aws_customerprofiles_profile`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile).
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


class CustomerprofilesProfile(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.customerprofilesProfile.CustomerprofilesProfile",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile aws_customerprofiles_profile}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        domain_name: builtins.str,
        account_number: typing.Optional[builtins.str] = None,
        additional_information: typing.Optional[builtins.str] = None,
        address: typing.Optional[typing.Union["CustomerprofilesProfileAddress", typing.Dict[builtins.str, typing.Any]]] = None,
        attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        billing_address: typing.Optional[typing.Union["CustomerprofilesProfileBillingAddress", typing.Dict[builtins.str, typing.Any]]] = None,
        birth_date: typing.Optional[builtins.str] = None,
        business_email_address: typing.Optional[builtins.str] = None,
        business_name: typing.Optional[builtins.str] = None,
        business_phone_number: typing.Optional[builtins.str] = None,
        email_address: typing.Optional[builtins.str] = None,
        first_name: typing.Optional[builtins.str] = None,
        gender_string: typing.Optional[builtins.str] = None,
        home_phone_number: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        last_name: typing.Optional[builtins.str] = None,
        mailing_address: typing.Optional[typing.Union["CustomerprofilesProfileMailingAddress", typing.Dict[builtins.str, typing.Any]]] = None,
        middle_name: typing.Optional[builtins.str] = None,
        mobile_phone_number: typing.Optional[builtins.str] = None,
        party_type_string: typing.Optional[builtins.str] = None,
        personal_email_address: typing.Optional[builtins.str] = None,
        phone_number: typing.Optional[builtins.str] = None,
        shipping_address: typing.Optional[typing.Union["CustomerprofilesProfileShippingAddress", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile aws_customerprofiles_profile} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#domain_name CustomerprofilesProfile#domain_name}.
        :param account_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#account_number CustomerprofilesProfile#account_number}.
        :param additional_information: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#additional_information CustomerprofilesProfile#additional_information}.
        :param address: address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address CustomerprofilesProfile#address}
        :param attributes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#attributes CustomerprofilesProfile#attributes}.
        :param billing_address: billing_address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#billing_address CustomerprofilesProfile#billing_address}
        :param birth_date: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#birth_date CustomerprofilesProfile#birth_date}.
        :param business_email_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#business_email_address CustomerprofilesProfile#business_email_address}.
        :param business_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#business_name CustomerprofilesProfile#business_name}.
        :param business_phone_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#business_phone_number CustomerprofilesProfile#business_phone_number}.
        :param email_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#email_address CustomerprofilesProfile#email_address}.
        :param first_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#first_name CustomerprofilesProfile#first_name}.
        :param gender_string: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#gender_string CustomerprofilesProfile#gender_string}.
        :param home_phone_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#home_phone_number CustomerprofilesProfile#home_phone_number}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#id CustomerprofilesProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param last_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#last_name CustomerprofilesProfile#last_name}.
        :param mailing_address: mailing_address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#mailing_address CustomerprofilesProfile#mailing_address}
        :param middle_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#middle_name CustomerprofilesProfile#middle_name}.
        :param mobile_phone_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#mobile_phone_number CustomerprofilesProfile#mobile_phone_number}.
        :param party_type_string: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#party_type_string CustomerprofilesProfile#party_type_string}.
        :param personal_email_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#personal_email_address CustomerprofilesProfile#personal_email_address}.
        :param phone_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#phone_number CustomerprofilesProfile#phone_number}.
        :param shipping_address: shipping_address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#shipping_address CustomerprofilesProfile#shipping_address}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6879827f93e5cd75b89e51b9ed38a5af83a6f045567a7ea70035aba62fc4b9cb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CustomerprofilesProfileConfig(
            domain_name=domain_name,
            account_number=account_number,
            additional_information=additional_information,
            address=address,
            attributes=attributes,
            billing_address=billing_address,
            birth_date=birth_date,
            business_email_address=business_email_address,
            business_name=business_name,
            business_phone_number=business_phone_number,
            email_address=email_address,
            first_name=first_name,
            gender_string=gender_string,
            home_phone_number=home_phone_number,
            id=id,
            last_name=last_name,
            mailing_address=mailing_address,
            middle_name=middle_name,
            mobile_phone_number=mobile_phone_number,
            party_type_string=party_type_string,
            personal_email_address=personal_email_address,
            phone_number=phone_number,
            shipping_address=shipping_address,
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
        '''Generates CDKTF code for importing a CustomerprofilesProfile resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CustomerprofilesProfile to import.
        :param import_from_id: The id of the existing CustomerprofilesProfile that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CustomerprofilesProfile to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dac0979b61c5339f320d8fe9cd1e5bc53abc726e616d600981bd7638a66e642)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAddress")
    def put_address(
        self,
        *,
        address1: typing.Optional[builtins.str] = None,
        address2: typing.Optional[builtins.str] = None,
        address3: typing.Optional[builtins.str] = None,
        address4: typing.Optional[builtins.str] = None,
        city: typing.Optional[builtins.str] = None,
        country: typing.Optional[builtins.str] = None,
        county: typing.Optional[builtins.str] = None,
        postal_code: typing.Optional[builtins.str] = None,
        province: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address1: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_1 CustomerprofilesProfile#address_1}.
        :param address2: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_2 CustomerprofilesProfile#address_2}.
        :param address3: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_3 CustomerprofilesProfile#address_3}.
        :param address4: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_4 CustomerprofilesProfile#address_4}.
        :param city: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#city CustomerprofilesProfile#city}.
        :param country: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#country CustomerprofilesProfile#country}.
        :param county: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#county CustomerprofilesProfile#county}.
        :param postal_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#postal_code CustomerprofilesProfile#postal_code}.
        :param province: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#province CustomerprofilesProfile#province}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#state CustomerprofilesProfile#state}.
        '''
        value = CustomerprofilesProfileAddress(
            address1=address1,
            address2=address2,
            address3=address3,
            address4=address4,
            city=city,
            country=country,
            county=county,
            postal_code=postal_code,
            province=province,
            state=state,
        )

        return typing.cast(None, jsii.invoke(self, "putAddress", [value]))

    @jsii.member(jsii_name="putBillingAddress")
    def put_billing_address(
        self,
        *,
        address1: typing.Optional[builtins.str] = None,
        address2: typing.Optional[builtins.str] = None,
        address3: typing.Optional[builtins.str] = None,
        address4: typing.Optional[builtins.str] = None,
        city: typing.Optional[builtins.str] = None,
        country: typing.Optional[builtins.str] = None,
        county: typing.Optional[builtins.str] = None,
        postal_code: typing.Optional[builtins.str] = None,
        province: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address1: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_1 CustomerprofilesProfile#address_1}.
        :param address2: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_2 CustomerprofilesProfile#address_2}.
        :param address3: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_3 CustomerprofilesProfile#address_3}.
        :param address4: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_4 CustomerprofilesProfile#address_4}.
        :param city: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#city CustomerprofilesProfile#city}.
        :param country: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#country CustomerprofilesProfile#country}.
        :param county: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#county CustomerprofilesProfile#county}.
        :param postal_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#postal_code CustomerprofilesProfile#postal_code}.
        :param province: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#province CustomerprofilesProfile#province}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#state CustomerprofilesProfile#state}.
        '''
        value = CustomerprofilesProfileBillingAddress(
            address1=address1,
            address2=address2,
            address3=address3,
            address4=address4,
            city=city,
            country=country,
            county=county,
            postal_code=postal_code,
            province=province,
            state=state,
        )

        return typing.cast(None, jsii.invoke(self, "putBillingAddress", [value]))

    @jsii.member(jsii_name="putMailingAddress")
    def put_mailing_address(
        self,
        *,
        address1: typing.Optional[builtins.str] = None,
        address2: typing.Optional[builtins.str] = None,
        address3: typing.Optional[builtins.str] = None,
        address4: typing.Optional[builtins.str] = None,
        city: typing.Optional[builtins.str] = None,
        country: typing.Optional[builtins.str] = None,
        county: typing.Optional[builtins.str] = None,
        postal_code: typing.Optional[builtins.str] = None,
        province: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address1: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_1 CustomerprofilesProfile#address_1}.
        :param address2: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_2 CustomerprofilesProfile#address_2}.
        :param address3: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_3 CustomerprofilesProfile#address_3}.
        :param address4: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_4 CustomerprofilesProfile#address_4}.
        :param city: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#city CustomerprofilesProfile#city}.
        :param country: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#country CustomerprofilesProfile#country}.
        :param county: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#county CustomerprofilesProfile#county}.
        :param postal_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#postal_code CustomerprofilesProfile#postal_code}.
        :param province: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#province CustomerprofilesProfile#province}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#state CustomerprofilesProfile#state}.
        '''
        value = CustomerprofilesProfileMailingAddress(
            address1=address1,
            address2=address2,
            address3=address3,
            address4=address4,
            city=city,
            country=country,
            county=county,
            postal_code=postal_code,
            province=province,
            state=state,
        )

        return typing.cast(None, jsii.invoke(self, "putMailingAddress", [value]))

    @jsii.member(jsii_name="putShippingAddress")
    def put_shipping_address(
        self,
        *,
        address1: typing.Optional[builtins.str] = None,
        address2: typing.Optional[builtins.str] = None,
        address3: typing.Optional[builtins.str] = None,
        address4: typing.Optional[builtins.str] = None,
        city: typing.Optional[builtins.str] = None,
        country: typing.Optional[builtins.str] = None,
        county: typing.Optional[builtins.str] = None,
        postal_code: typing.Optional[builtins.str] = None,
        province: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address1: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_1 CustomerprofilesProfile#address_1}.
        :param address2: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_2 CustomerprofilesProfile#address_2}.
        :param address3: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_3 CustomerprofilesProfile#address_3}.
        :param address4: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_4 CustomerprofilesProfile#address_4}.
        :param city: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#city CustomerprofilesProfile#city}.
        :param country: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#country CustomerprofilesProfile#country}.
        :param county: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#county CustomerprofilesProfile#county}.
        :param postal_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#postal_code CustomerprofilesProfile#postal_code}.
        :param province: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#province CustomerprofilesProfile#province}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#state CustomerprofilesProfile#state}.
        '''
        value = CustomerprofilesProfileShippingAddress(
            address1=address1,
            address2=address2,
            address3=address3,
            address4=address4,
            city=city,
            country=country,
            county=county,
            postal_code=postal_code,
            province=province,
            state=state,
        )

        return typing.cast(None, jsii.invoke(self, "putShippingAddress", [value]))

    @jsii.member(jsii_name="resetAccountNumber")
    def reset_account_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountNumber", []))

    @jsii.member(jsii_name="resetAdditionalInformation")
    def reset_additional_information(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalInformation", []))

    @jsii.member(jsii_name="resetAddress")
    def reset_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress", []))

    @jsii.member(jsii_name="resetAttributes")
    def reset_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttributes", []))

    @jsii.member(jsii_name="resetBillingAddress")
    def reset_billing_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBillingAddress", []))

    @jsii.member(jsii_name="resetBirthDate")
    def reset_birth_date(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBirthDate", []))

    @jsii.member(jsii_name="resetBusinessEmailAddress")
    def reset_business_email_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBusinessEmailAddress", []))

    @jsii.member(jsii_name="resetBusinessName")
    def reset_business_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBusinessName", []))

    @jsii.member(jsii_name="resetBusinessPhoneNumber")
    def reset_business_phone_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBusinessPhoneNumber", []))

    @jsii.member(jsii_name="resetEmailAddress")
    def reset_email_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailAddress", []))

    @jsii.member(jsii_name="resetFirstName")
    def reset_first_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirstName", []))

    @jsii.member(jsii_name="resetGenderString")
    def reset_gender_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGenderString", []))

    @jsii.member(jsii_name="resetHomePhoneNumber")
    def reset_home_phone_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHomePhoneNumber", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLastName")
    def reset_last_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLastName", []))

    @jsii.member(jsii_name="resetMailingAddress")
    def reset_mailing_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMailingAddress", []))

    @jsii.member(jsii_name="resetMiddleName")
    def reset_middle_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMiddleName", []))

    @jsii.member(jsii_name="resetMobilePhoneNumber")
    def reset_mobile_phone_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMobilePhoneNumber", []))

    @jsii.member(jsii_name="resetPartyTypeString")
    def reset_party_type_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartyTypeString", []))

    @jsii.member(jsii_name="resetPersonalEmailAddress")
    def reset_personal_email_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPersonalEmailAddress", []))

    @jsii.member(jsii_name="resetPhoneNumber")
    def reset_phone_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPhoneNumber", []))

    @jsii.member(jsii_name="resetShippingAddress")
    def reset_shipping_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShippingAddress", []))

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
    @jsii.member(jsii_name="address")
    def address(self) -> "CustomerprofilesProfileAddressOutputReference":
        return typing.cast("CustomerprofilesProfileAddressOutputReference", jsii.get(self, "address"))

    @builtins.property
    @jsii.member(jsii_name="billingAddress")
    def billing_address(self) -> "CustomerprofilesProfileBillingAddressOutputReference":
        return typing.cast("CustomerprofilesProfileBillingAddressOutputReference", jsii.get(self, "billingAddress"))

    @builtins.property
    @jsii.member(jsii_name="mailingAddress")
    def mailing_address(self) -> "CustomerprofilesProfileMailingAddressOutputReference":
        return typing.cast("CustomerprofilesProfileMailingAddressOutputReference", jsii.get(self, "mailingAddress"))

    @builtins.property
    @jsii.member(jsii_name="shippingAddress")
    def shipping_address(
        self,
    ) -> "CustomerprofilesProfileShippingAddressOutputReference":
        return typing.cast("CustomerprofilesProfileShippingAddressOutputReference", jsii.get(self, "shippingAddress"))

    @builtins.property
    @jsii.member(jsii_name="accountNumberInput")
    def account_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalInformationInput")
    def additional_information_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "additionalInformationInput"))

    @builtins.property
    @jsii.member(jsii_name="addressInput")
    def address_input(self) -> typing.Optional["CustomerprofilesProfileAddress"]:
        return typing.cast(typing.Optional["CustomerprofilesProfileAddress"], jsii.get(self, "addressInput"))

    @builtins.property
    @jsii.member(jsii_name="attributesInput")
    def attributes_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "attributesInput"))

    @builtins.property
    @jsii.member(jsii_name="billingAddressInput")
    def billing_address_input(
        self,
    ) -> typing.Optional["CustomerprofilesProfileBillingAddress"]:
        return typing.cast(typing.Optional["CustomerprofilesProfileBillingAddress"], jsii.get(self, "billingAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="birthDateInput")
    def birth_date_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "birthDateInput"))

    @builtins.property
    @jsii.member(jsii_name="businessEmailAddressInput")
    def business_email_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "businessEmailAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="businessNameInput")
    def business_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "businessNameInput"))

    @builtins.property
    @jsii.member(jsii_name="businessPhoneNumberInput")
    def business_phone_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "businessPhoneNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="domainNameInput")
    def domain_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="emailAddressInput")
    def email_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="firstNameInput")
    def first_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firstNameInput"))

    @builtins.property
    @jsii.member(jsii_name="genderStringInput")
    def gender_string_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "genderStringInput"))

    @builtins.property
    @jsii.member(jsii_name="homePhoneNumberInput")
    def home_phone_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "homePhoneNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="lastNameInput")
    def last_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lastNameInput"))

    @builtins.property
    @jsii.member(jsii_name="mailingAddressInput")
    def mailing_address_input(
        self,
    ) -> typing.Optional["CustomerprofilesProfileMailingAddress"]:
        return typing.cast(typing.Optional["CustomerprofilesProfileMailingAddress"], jsii.get(self, "mailingAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="middleNameInput")
    def middle_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "middleNameInput"))

    @builtins.property
    @jsii.member(jsii_name="mobilePhoneNumberInput")
    def mobile_phone_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mobilePhoneNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="partyTypeStringInput")
    def party_type_string_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "partyTypeStringInput"))

    @builtins.property
    @jsii.member(jsii_name="personalEmailAddressInput")
    def personal_email_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "personalEmailAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="phoneNumberInput")
    def phone_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "phoneNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="shippingAddressInput")
    def shipping_address_input(
        self,
    ) -> typing.Optional["CustomerprofilesProfileShippingAddress"]:
        return typing.cast(typing.Optional["CustomerprofilesProfileShippingAddress"], jsii.get(self, "shippingAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="accountNumber")
    def account_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountNumber"))

    @account_number.setter
    def account_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3749331597c56963abf765de906d5874ff7ac0e77ba36b5a1e7930f580e1d0bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="additionalInformation")
    def additional_information(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "additionalInformation"))

    @additional_information.setter
    def additional_information(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cec85674dd8f810abf05768fbd7d014176cc6c1569b980ad0963c2981a9a61f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalInformation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="attributes")
    def attributes(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "attributes"))

    @attributes.setter
    def attributes(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c02768c713454b6bcc30d2848ca1f38151ef339b7ad63057b19d22f8c732014d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="birthDate")
    def birth_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "birthDate"))

    @birth_date.setter
    def birth_date(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__468f6c949c5365bf6eea04935df60e50684581b48529faa498626f1f9bddf2d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "birthDate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="businessEmailAddress")
    def business_email_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "businessEmailAddress"))

    @business_email_address.setter
    def business_email_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__527561215e735f1adefb4cdfa874319865eac961783a9b24d24f800da2d2d3bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "businessEmailAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="businessName")
    def business_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "businessName"))

    @business_name.setter
    def business_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38f923f88edaf8f72da9eca8be29fffab7fa53de7335a7b6014ac115b58bd8e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "businessName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="businessPhoneNumber")
    def business_phone_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "businessPhoneNumber"))

    @business_phone_number.setter
    def business_phone_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40bb21ea778523de878afc959269f2724548f791ef3dc87b0355a26edb1c8042)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "businessPhoneNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a53b25984fe155c2969b9c993b2bf9a7525a8c13d3a494c4cf28892e30594b44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="emailAddress")
    def email_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "emailAddress"))

    @email_address.setter
    def email_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ce144df49066095ef933a4de10681d402137b9a7b23481bbb3e4b3e5142304d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="firstName")
    def first_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firstName"))

    @first_name.setter
    def first_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a54b1a1338e7d1ae5610863aa9f4f0742b01b3d3645ae34c08c081a21c1350eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firstName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="genderString")
    def gender_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "genderString"))

    @gender_string.setter
    def gender_string(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24430200a06815fd98f4ed4b50a29710cbe005e8a29acc604b3a44493a7a8034)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "genderString", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="homePhoneNumber")
    def home_phone_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "homePhoneNumber"))

    @home_phone_number.setter
    def home_phone_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61387068817a1a5dafad7ca78dae245801cb9e649975931d5daeadd3c70b10ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "homePhoneNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68ae759c999f6c47e855867eeeb0e87036e754be380f43fe9ff6f7d5365634ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lastName")
    def last_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastName"))

    @last_name.setter
    def last_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52fa4db1901264602f79c410aec635bd1808733ec3c454fc29964d8f9cdafe07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lastName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="middleName")
    def middle_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "middleName"))

    @middle_name.setter
    def middle_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea801fa235cd5395b48f1c3bfcfd9d064467be003bfd8daafab4a02f02fec8f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "middleName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mobilePhoneNumber")
    def mobile_phone_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mobilePhoneNumber"))

    @mobile_phone_number.setter
    def mobile_phone_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__688dbfe75162a09f2e1e040921742ba1c2d673170398a81c8f34b998fb9ee3dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mobilePhoneNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partyTypeString")
    def party_type_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "partyTypeString"))

    @party_type_string.setter
    def party_type_string(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b650edb09329b98c03e127aa62354a0cbbc3587eefb1f15a5dce73bee3df741)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partyTypeString", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="personalEmailAddress")
    def personal_email_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "personalEmailAddress"))

    @personal_email_address.setter
    def personal_email_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5a491a27655a05c73c9ae0ad14623f74e2a43e8959c7c43f9e26f8861257860)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "personalEmailAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="phoneNumber")
    def phone_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "phoneNumber"))

    @phone_number.setter
    def phone_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43e9ad5dd5547f43270153c61f8c63b4d835518ce8ceecac3cf0096a4e11ddb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "phoneNumber", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.customerprofilesProfile.CustomerprofilesProfileAddress",
    jsii_struct_bases=[],
    name_mapping={
        "address1": "address1",
        "address2": "address2",
        "address3": "address3",
        "address4": "address4",
        "city": "city",
        "country": "country",
        "county": "county",
        "postal_code": "postalCode",
        "province": "province",
        "state": "state",
    },
)
class CustomerprofilesProfileAddress:
    def __init__(
        self,
        *,
        address1: typing.Optional[builtins.str] = None,
        address2: typing.Optional[builtins.str] = None,
        address3: typing.Optional[builtins.str] = None,
        address4: typing.Optional[builtins.str] = None,
        city: typing.Optional[builtins.str] = None,
        country: typing.Optional[builtins.str] = None,
        county: typing.Optional[builtins.str] = None,
        postal_code: typing.Optional[builtins.str] = None,
        province: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address1: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_1 CustomerprofilesProfile#address_1}.
        :param address2: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_2 CustomerprofilesProfile#address_2}.
        :param address3: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_3 CustomerprofilesProfile#address_3}.
        :param address4: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_4 CustomerprofilesProfile#address_4}.
        :param city: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#city CustomerprofilesProfile#city}.
        :param country: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#country CustomerprofilesProfile#country}.
        :param county: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#county CustomerprofilesProfile#county}.
        :param postal_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#postal_code CustomerprofilesProfile#postal_code}.
        :param province: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#province CustomerprofilesProfile#province}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#state CustomerprofilesProfile#state}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dec09c6e00db9f9a36e25888d30ac526300ecd7cbacb5639b23092da048b1b4e)
            check_type(argname="argument address1", value=address1, expected_type=type_hints["address1"])
            check_type(argname="argument address2", value=address2, expected_type=type_hints["address2"])
            check_type(argname="argument address3", value=address3, expected_type=type_hints["address3"])
            check_type(argname="argument address4", value=address4, expected_type=type_hints["address4"])
            check_type(argname="argument city", value=city, expected_type=type_hints["city"])
            check_type(argname="argument country", value=country, expected_type=type_hints["country"])
            check_type(argname="argument county", value=county, expected_type=type_hints["county"])
            check_type(argname="argument postal_code", value=postal_code, expected_type=type_hints["postal_code"])
            check_type(argname="argument province", value=province, expected_type=type_hints["province"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if address1 is not None:
            self._values["address1"] = address1
        if address2 is not None:
            self._values["address2"] = address2
        if address3 is not None:
            self._values["address3"] = address3
        if address4 is not None:
            self._values["address4"] = address4
        if city is not None:
            self._values["city"] = city
        if country is not None:
            self._values["country"] = country
        if county is not None:
            self._values["county"] = county
        if postal_code is not None:
            self._values["postal_code"] = postal_code
        if province is not None:
            self._values["province"] = province
        if state is not None:
            self._values["state"] = state

    @builtins.property
    def address1(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_1 CustomerprofilesProfile#address_1}.'''
        result = self._values.get("address1")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address2(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_2 CustomerprofilesProfile#address_2}.'''
        result = self._values.get("address2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address3(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_3 CustomerprofilesProfile#address_3}.'''
        result = self._values.get("address3")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address4(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_4 CustomerprofilesProfile#address_4}.'''
        result = self._values.get("address4")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def city(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#city CustomerprofilesProfile#city}.'''
        result = self._values.get("city")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def country(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#country CustomerprofilesProfile#country}.'''
        result = self._values.get("country")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def county(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#county CustomerprofilesProfile#county}.'''
        result = self._values.get("county")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def postal_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#postal_code CustomerprofilesProfile#postal_code}.'''
        result = self._values.get("postal_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def province(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#province CustomerprofilesProfile#province}.'''
        result = self._values.get("province")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#state CustomerprofilesProfile#state}.'''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomerprofilesProfileAddress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CustomerprofilesProfileAddressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.customerprofilesProfile.CustomerprofilesProfileAddressOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9333340d92cfcc6409a8bae1b0f1e7d36c31c304550fe6f90e2b86d4ac5e789e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAddress1")
    def reset_address1(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress1", []))

    @jsii.member(jsii_name="resetAddress2")
    def reset_address2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress2", []))

    @jsii.member(jsii_name="resetAddress3")
    def reset_address3(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress3", []))

    @jsii.member(jsii_name="resetAddress4")
    def reset_address4(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress4", []))

    @jsii.member(jsii_name="resetCity")
    def reset_city(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCity", []))

    @jsii.member(jsii_name="resetCountry")
    def reset_country(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCountry", []))

    @jsii.member(jsii_name="resetCounty")
    def reset_county(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCounty", []))

    @jsii.member(jsii_name="resetPostalCode")
    def reset_postal_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostalCode", []))

    @jsii.member(jsii_name="resetProvince")
    def reset_province(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvince", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

    @builtins.property
    @jsii.member(jsii_name="address1Input")
    def address1_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "address1Input"))

    @builtins.property
    @jsii.member(jsii_name="address2Input")
    def address2_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "address2Input"))

    @builtins.property
    @jsii.member(jsii_name="address3Input")
    def address3_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "address3Input"))

    @builtins.property
    @jsii.member(jsii_name="address4Input")
    def address4_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "address4Input"))

    @builtins.property
    @jsii.member(jsii_name="cityInput")
    def city_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cityInput"))

    @builtins.property
    @jsii.member(jsii_name="countryInput")
    def country_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countryInput"))

    @builtins.property
    @jsii.member(jsii_name="countyInput")
    def county_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countyInput"))

    @builtins.property
    @jsii.member(jsii_name="postalCodeInput")
    def postal_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "postalCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="provinceInput")
    def province_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "provinceInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="address1")
    def address1(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address1"))

    @address1.setter
    def address1(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62720a0d5368628fd9c4627cf9ce916646788a5554802788b755a5c89d4f082c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address1", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="address2")
    def address2(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address2"))

    @address2.setter
    def address2(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59e3024fa77954326a9c13cc99fb8680ff058607bfab2b8a019df738210b6f37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address2", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="address3")
    def address3(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address3"))

    @address3.setter
    def address3(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a71548319e618eedd22c4d9e567f97c3c047f526b3e79fd87da171a1ed9e325)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address3", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="address4")
    def address4(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address4"))

    @address4.setter
    def address4(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a5105d0fa9d11bde3a6cbd918588016f8ca3ebecd0d9ceef2979c96e6e61bb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address4", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="city")
    def city(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "city"))

    @city.setter
    def city(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f18b377b1580f6b13ad6906734a7907ac854021f5bd15e598cabec1f2bb37eb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "city", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="country")
    def country(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "country"))

    @country.setter
    def country(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57c433332826bc14242ceb8894790b8d706a467c506dfba60af0e662bc45c945)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "country", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="county")
    def county(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "county"))

    @county.setter
    def county(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33e50dd37069cb65f33aeecc029f0086ab392acb3c1824fd5a254ca7c0283929)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "county", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postalCode")
    def postal_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postalCode"))

    @postal_code.setter
    def postal_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1b39110dfe1e62590337be2c3fa4138becc51169fa456fe2045137b0330bced)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postalCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="province")
    def province(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "province"))

    @province.setter
    def province(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__584478a79ff643efb8767a6ca7dc36381d133a9e45a2151f4178dcead535a3ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "province", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__993241e38a2a7ee202ba20ba8947f15f1eed913c5d4b6b7062574d99bbf57e38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CustomerprofilesProfileAddress]:
        return typing.cast(typing.Optional[CustomerprofilesProfileAddress], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CustomerprofilesProfileAddress],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4f127b8dfa87c08276588d0bd4792d2b65d897c98df64dd0d440b5d57827858)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.customerprofilesProfile.CustomerprofilesProfileBillingAddress",
    jsii_struct_bases=[],
    name_mapping={
        "address1": "address1",
        "address2": "address2",
        "address3": "address3",
        "address4": "address4",
        "city": "city",
        "country": "country",
        "county": "county",
        "postal_code": "postalCode",
        "province": "province",
        "state": "state",
    },
)
class CustomerprofilesProfileBillingAddress:
    def __init__(
        self,
        *,
        address1: typing.Optional[builtins.str] = None,
        address2: typing.Optional[builtins.str] = None,
        address3: typing.Optional[builtins.str] = None,
        address4: typing.Optional[builtins.str] = None,
        city: typing.Optional[builtins.str] = None,
        country: typing.Optional[builtins.str] = None,
        county: typing.Optional[builtins.str] = None,
        postal_code: typing.Optional[builtins.str] = None,
        province: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address1: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_1 CustomerprofilesProfile#address_1}.
        :param address2: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_2 CustomerprofilesProfile#address_2}.
        :param address3: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_3 CustomerprofilesProfile#address_3}.
        :param address4: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_4 CustomerprofilesProfile#address_4}.
        :param city: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#city CustomerprofilesProfile#city}.
        :param country: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#country CustomerprofilesProfile#country}.
        :param county: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#county CustomerprofilesProfile#county}.
        :param postal_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#postal_code CustomerprofilesProfile#postal_code}.
        :param province: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#province CustomerprofilesProfile#province}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#state CustomerprofilesProfile#state}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1de07e7c7d26e1e5debbc550532645495c12f16a894814d3443d42d371f71037)
            check_type(argname="argument address1", value=address1, expected_type=type_hints["address1"])
            check_type(argname="argument address2", value=address2, expected_type=type_hints["address2"])
            check_type(argname="argument address3", value=address3, expected_type=type_hints["address3"])
            check_type(argname="argument address4", value=address4, expected_type=type_hints["address4"])
            check_type(argname="argument city", value=city, expected_type=type_hints["city"])
            check_type(argname="argument country", value=country, expected_type=type_hints["country"])
            check_type(argname="argument county", value=county, expected_type=type_hints["county"])
            check_type(argname="argument postal_code", value=postal_code, expected_type=type_hints["postal_code"])
            check_type(argname="argument province", value=province, expected_type=type_hints["province"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if address1 is not None:
            self._values["address1"] = address1
        if address2 is not None:
            self._values["address2"] = address2
        if address3 is not None:
            self._values["address3"] = address3
        if address4 is not None:
            self._values["address4"] = address4
        if city is not None:
            self._values["city"] = city
        if country is not None:
            self._values["country"] = country
        if county is not None:
            self._values["county"] = county
        if postal_code is not None:
            self._values["postal_code"] = postal_code
        if province is not None:
            self._values["province"] = province
        if state is not None:
            self._values["state"] = state

    @builtins.property
    def address1(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_1 CustomerprofilesProfile#address_1}.'''
        result = self._values.get("address1")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address2(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_2 CustomerprofilesProfile#address_2}.'''
        result = self._values.get("address2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address3(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_3 CustomerprofilesProfile#address_3}.'''
        result = self._values.get("address3")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address4(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_4 CustomerprofilesProfile#address_4}.'''
        result = self._values.get("address4")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def city(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#city CustomerprofilesProfile#city}.'''
        result = self._values.get("city")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def country(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#country CustomerprofilesProfile#country}.'''
        result = self._values.get("country")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def county(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#county CustomerprofilesProfile#county}.'''
        result = self._values.get("county")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def postal_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#postal_code CustomerprofilesProfile#postal_code}.'''
        result = self._values.get("postal_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def province(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#province CustomerprofilesProfile#province}.'''
        result = self._values.get("province")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#state CustomerprofilesProfile#state}.'''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomerprofilesProfileBillingAddress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CustomerprofilesProfileBillingAddressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.customerprofilesProfile.CustomerprofilesProfileBillingAddressOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2503e3177f5e0a4edf2e6d4a1594813c3dc09b0ddc2dbe0f920c84fa62457ef7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAddress1")
    def reset_address1(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress1", []))

    @jsii.member(jsii_name="resetAddress2")
    def reset_address2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress2", []))

    @jsii.member(jsii_name="resetAddress3")
    def reset_address3(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress3", []))

    @jsii.member(jsii_name="resetAddress4")
    def reset_address4(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress4", []))

    @jsii.member(jsii_name="resetCity")
    def reset_city(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCity", []))

    @jsii.member(jsii_name="resetCountry")
    def reset_country(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCountry", []))

    @jsii.member(jsii_name="resetCounty")
    def reset_county(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCounty", []))

    @jsii.member(jsii_name="resetPostalCode")
    def reset_postal_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostalCode", []))

    @jsii.member(jsii_name="resetProvince")
    def reset_province(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvince", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

    @builtins.property
    @jsii.member(jsii_name="address1Input")
    def address1_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "address1Input"))

    @builtins.property
    @jsii.member(jsii_name="address2Input")
    def address2_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "address2Input"))

    @builtins.property
    @jsii.member(jsii_name="address3Input")
    def address3_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "address3Input"))

    @builtins.property
    @jsii.member(jsii_name="address4Input")
    def address4_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "address4Input"))

    @builtins.property
    @jsii.member(jsii_name="cityInput")
    def city_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cityInput"))

    @builtins.property
    @jsii.member(jsii_name="countryInput")
    def country_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countryInput"))

    @builtins.property
    @jsii.member(jsii_name="countyInput")
    def county_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countyInput"))

    @builtins.property
    @jsii.member(jsii_name="postalCodeInput")
    def postal_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "postalCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="provinceInput")
    def province_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "provinceInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="address1")
    def address1(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address1"))

    @address1.setter
    def address1(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82064c0e9d3ea5f32bdbb02aa6c3c3c28403a76ce8933aa1f6df92bc8d43c904)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address1", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="address2")
    def address2(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address2"))

    @address2.setter
    def address2(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83eaafccdb162eeb7e135f0dfc891502bcf486ee6da03a3b3f8ab6bc86223f37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address2", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="address3")
    def address3(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address3"))

    @address3.setter
    def address3(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d79b58280087d41fd057afc8dc87c2c3c931fb5f9f2b9354ca5350b1fe420fcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address3", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="address4")
    def address4(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address4"))

    @address4.setter
    def address4(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fcf8149ecb68c463b318fcc8d74beaa049816d3405172653b930fccb4171049)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address4", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="city")
    def city(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "city"))

    @city.setter
    def city(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8da00c8dad4048c96e189ae162288a6ae6582b8335c386ffea952a48125356ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "city", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="country")
    def country(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "country"))

    @country.setter
    def country(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55c17b57740f693dbd601a2c70e47fd78528d5c03560694cdceb73b4e98e2a11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "country", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="county")
    def county(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "county"))

    @county.setter
    def county(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ccc92a80f0a39b441238956b9eeccda7d4a70b8c339ff438932df0710e9eddb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "county", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postalCode")
    def postal_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postalCode"))

    @postal_code.setter
    def postal_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__735e35587d33b14bec33f308fbb078c6b34e73f7e1d9affe0e1dfe6bdf430624)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postalCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="province")
    def province(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "province"))

    @province.setter
    def province(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8415bf8c335fd927ffe29709e9a2a267be35f545bbeb265ba931f128961f05ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "province", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e9c421f825e2fd000b56071463deff87e1f2b9c9135bef7d38cb0e29a1f7c30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CustomerprofilesProfileBillingAddress]:
        return typing.cast(typing.Optional[CustomerprofilesProfileBillingAddress], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CustomerprofilesProfileBillingAddress],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__398fdc8a69f489aa67a7fb38ef8580c2b2277ea84f7464e56742a6c72716c185)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.customerprofilesProfile.CustomerprofilesProfileConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "domain_name": "domainName",
        "account_number": "accountNumber",
        "additional_information": "additionalInformation",
        "address": "address",
        "attributes": "attributes",
        "billing_address": "billingAddress",
        "birth_date": "birthDate",
        "business_email_address": "businessEmailAddress",
        "business_name": "businessName",
        "business_phone_number": "businessPhoneNumber",
        "email_address": "emailAddress",
        "first_name": "firstName",
        "gender_string": "genderString",
        "home_phone_number": "homePhoneNumber",
        "id": "id",
        "last_name": "lastName",
        "mailing_address": "mailingAddress",
        "middle_name": "middleName",
        "mobile_phone_number": "mobilePhoneNumber",
        "party_type_string": "partyTypeString",
        "personal_email_address": "personalEmailAddress",
        "phone_number": "phoneNumber",
        "shipping_address": "shippingAddress",
    },
)
class CustomerprofilesProfileConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        domain_name: builtins.str,
        account_number: typing.Optional[builtins.str] = None,
        additional_information: typing.Optional[builtins.str] = None,
        address: typing.Optional[typing.Union[CustomerprofilesProfileAddress, typing.Dict[builtins.str, typing.Any]]] = None,
        attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        billing_address: typing.Optional[typing.Union[CustomerprofilesProfileBillingAddress, typing.Dict[builtins.str, typing.Any]]] = None,
        birth_date: typing.Optional[builtins.str] = None,
        business_email_address: typing.Optional[builtins.str] = None,
        business_name: typing.Optional[builtins.str] = None,
        business_phone_number: typing.Optional[builtins.str] = None,
        email_address: typing.Optional[builtins.str] = None,
        first_name: typing.Optional[builtins.str] = None,
        gender_string: typing.Optional[builtins.str] = None,
        home_phone_number: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        last_name: typing.Optional[builtins.str] = None,
        mailing_address: typing.Optional[typing.Union["CustomerprofilesProfileMailingAddress", typing.Dict[builtins.str, typing.Any]]] = None,
        middle_name: typing.Optional[builtins.str] = None,
        mobile_phone_number: typing.Optional[builtins.str] = None,
        party_type_string: typing.Optional[builtins.str] = None,
        personal_email_address: typing.Optional[builtins.str] = None,
        phone_number: typing.Optional[builtins.str] = None,
        shipping_address: typing.Optional[typing.Union["CustomerprofilesProfileShippingAddress", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#domain_name CustomerprofilesProfile#domain_name}.
        :param account_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#account_number CustomerprofilesProfile#account_number}.
        :param additional_information: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#additional_information CustomerprofilesProfile#additional_information}.
        :param address: address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address CustomerprofilesProfile#address}
        :param attributes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#attributes CustomerprofilesProfile#attributes}.
        :param billing_address: billing_address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#billing_address CustomerprofilesProfile#billing_address}
        :param birth_date: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#birth_date CustomerprofilesProfile#birth_date}.
        :param business_email_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#business_email_address CustomerprofilesProfile#business_email_address}.
        :param business_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#business_name CustomerprofilesProfile#business_name}.
        :param business_phone_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#business_phone_number CustomerprofilesProfile#business_phone_number}.
        :param email_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#email_address CustomerprofilesProfile#email_address}.
        :param first_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#first_name CustomerprofilesProfile#first_name}.
        :param gender_string: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#gender_string CustomerprofilesProfile#gender_string}.
        :param home_phone_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#home_phone_number CustomerprofilesProfile#home_phone_number}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#id CustomerprofilesProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param last_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#last_name CustomerprofilesProfile#last_name}.
        :param mailing_address: mailing_address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#mailing_address CustomerprofilesProfile#mailing_address}
        :param middle_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#middle_name CustomerprofilesProfile#middle_name}.
        :param mobile_phone_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#mobile_phone_number CustomerprofilesProfile#mobile_phone_number}.
        :param party_type_string: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#party_type_string CustomerprofilesProfile#party_type_string}.
        :param personal_email_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#personal_email_address CustomerprofilesProfile#personal_email_address}.
        :param phone_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#phone_number CustomerprofilesProfile#phone_number}.
        :param shipping_address: shipping_address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#shipping_address CustomerprofilesProfile#shipping_address}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(address, dict):
            address = CustomerprofilesProfileAddress(**address)
        if isinstance(billing_address, dict):
            billing_address = CustomerprofilesProfileBillingAddress(**billing_address)
        if isinstance(mailing_address, dict):
            mailing_address = CustomerprofilesProfileMailingAddress(**mailing_address)
        if isinstance(shipping_address, dict):
            shipping_address = CustomerprofilesProfileShippingAddress(**shipping_address)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dd541898d4275d36a1abd5c1a29e425a0cb79b367c5941cbc8e5190327faef8)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument account_number", value=account_number, expected_type=type_hints["account_number"])
            check_type(argname="argument additional_information", value=additional_information, expected_type=type_hints["additional_information"])
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument billing_address", value=billing_address, expected_type=type_hints["billing_address"])
            check_type(argname="argument birth_date", value=birth_date, expected_type=type_hints["birth_date"])
            check_type(argname="argument business_email_address", value=business_email_address, expected_type=type_hints["business_email_address"])
            check_type(argname="argument business_name", value=business_name, expected_type=type_hints["business_name"])
            check_type(argname="argument business_phone_number", value=business_phone_number, expected_type=type_hints["business_phone_number"])
            check_type(argname="argument email_address", value=email_address, expected_type=type_hints["email_address"])
            check_type(argname="argument first_name", value=first_name, expected_type=type_hints["first_name"])
            check_type(argname="argument gender_string", value=gender_string, expected_type=type_hints["gender_string"])
            check_type(argname="argument home_phone_number", value=home_phone_number, expected_type=type_hints["home_phone_number"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument last_name", value=last_name, expected_type=type_hints["last_name"])
            check_type(argname="argument mailing_address", value=mailing_address, expected_type=type_hints["mailing_address"])
            check_type(argname="argument middle_name", value=middle_name, expected_type=type_hints["middle_name"])
            check_type(argname="argument mobile_phone_number", value=mobile_phone_number, expected_type=type_hints["mobile_phone_number"])
            check_type(argname="argument party_type_string", value=party_type_string, expected_type=type_hints["party_type_string"])
            check_type(argname="argument personal_email_address", value=personal_email_address, expected_type=type_hints["personal_email_address"])
            check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
            check_type(argname="argument shipping_address", value=shipping_address, expected_type=type_hints["shipping_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain_name": domain_name,
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
        if account_number is not None:
            self._values["account_number"] = account_number
        if additional_information is not None:
            self._values["additional_information"] = additional_information
        if address is not None:
            self._values["address"] = address
        if attributes is not None:
            self._values["attributes"] = attributes
        if billing_address is not None:
            self._values["billing_address"] = billing_address
        if birth_date is not None:
            self._values["birth_date"] = birth_date
        if business_email_address is not None:
            self._values["business_email_address"] = business_email_address
        if business_name is not None:
            self._values["business_name"] = business_name
        if business_phone_number is not None:
            self._values["business_phone_number"] = business_phone_number
        if email_address is not None:
            self._values["email_address"] = email_address
        if first_name is not None:
            self._values["first_name"] = first_name
        if gender_string is not None:
            self._values["gender_string"] = gender_string
        if home_phone_number is not None:
            self._values["home_phone_number"] = home_phone_number
        if id is not None:
            self._values["id"] = id
        if last_name is not None:
            self._values["last_name"] = last_name
        if mailing_address is not None:
            self._values["mailing_address"] = mailing_address
        if middle_name is not None:
            self._values["middle_name"] = middle_name
        if mobile_phone_number is not None:
            self._values["mobile_phone_number"] = mobile_phone_number
        if party_type_string is not None:
            self._values["party_type_string"] = party_type_string
        if personal_email_address is not None:
            self._values["personal_email_address"] = personal_email_address
        if phone_number is not None:
            self._values["phone_number"] = phone_number
        if shipping_address is not None:
            self._values["shipping_address"] = shipping_address

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
    def domain_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#domain_name CustomerprofilesProfile#domain_name}.'''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_number(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#account_number CustomerprofilesProfile#account_number}.'''
        result = self._values.get("account_number")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def additional_information(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#additional_information CustomerprofilesProfile#additional_information}.'''
        result = self._values.get("additional_information")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address(self) -> typing.Optional[CustomerprofilesProfileAddress]:
        '''address block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address CustomerprofilesProfile#address}
        '''
        result = self._values.get("address")
        return typing.cast(typing.Optional[CustomerprofilesProfileAddress], result)

    @builtins.property
    def attributes(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#attributes CustomerprofilesProfile#attributes}.'''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def billing_address(self) -> typing.Optional[CustomerprofilesProfileBillingAddress]:
        '''billing_address block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#billing_address CustomerprofilesProfile#billing_address}
        '''
        result = self._values.get("billing_address")
        return typing.cast(typing.Optional[CustomerprofilesProfileBillingAddress], result)

    @builtins.property
    def birth_date(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#birth_date CustomerprofilesProfile#birth_date}.'''
        result = self._values.get("birth_date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def business_email_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#business_email_address CustomerprofilesProfile#business_email_address}.'''
        result = self._values.get("business_email_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def business_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#business_name CustomerprofilesProfile#business_name}.'''
        result = self._values.get("business_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def business_phone_number(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#business_phone_number CustomerprofilesProfile#business_phone_number}.'''
        result = self._values.get("business_phone_number")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#email_address CustomerprofilesProfile#email_address}.'''
        result = self._values.get("email_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def first_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#first_name CustomerprofilesProfile#first_name}.'''
        result = self._values.get("first_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gender_string(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#gender_string CustomerprofilesProfile#gender_string}.'''
        result = self._values.get("gender_string")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def home_phone_number(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#home_phone_number CustomerprofilesProfile#home_phone_number}.'''
        result = self._values.get("home_phone_number")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#id CustomerprofilesProfile#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def last_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#last_name CustomerprofilesProfile#last_name}.'''
        result = self._values.get("last_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mailing_address(
        self,
    ) -> typing.Optional["CustomerprofilesProfileMailingAddress"]:
        '''mailing_address block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#mailing_address CustomerprofilesProfile#mailing_address}
        '''
        result = self._values.get("mailing_address")
        return typing.cast(typing.Optional["CustomerprofilesProfileMailingAddress"], result)

    @builtins.property
    def middle_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#middle_name CustomerprofilesProfile#middle_name}.'''
        result = self._values.get("middle_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mobile_phone_number(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#mobile_phone_number CustomerprofilesProfile#mobile_phone_number}.'''
        result = self._values.get("mobile_phone_number")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def party_type_string(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#party_type_string CustomerprofilesProfile#party_type_string}.'''
        result = self._values.get("party_type_string")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def personal_email_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#personal_email_address CustomerprofilesProfile#personal_email_address}.'''
        result = self._values.get("personal_email_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def phone_number(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#phone_number CustomerprofilesProfile#phone_number}.'''
        result = self._values.get("phone_number")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shipping_address(
        self,
    ) -> typing.Optional["CustomerprofilesProfileShippingAddress"]:
        '''shipping_address block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#shipping_address CustomerprofilesProfile#shipping_address}
        '''
        result = self._values.get("shipping_address")
        return typing.cast(typing.Optional["CustomerprofilesProfileShippingAddress"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomerprofilesProfileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.customerprofilesProfile.CustomerprofilesProfileMailingAddress",
    jsii_struct_bases=[],
    name_mapping={
        "address1": "address1",
        "address2": "address2",
        "address3": "address3",
        "address4": "address4",
        "city": "city",
        "country": "country",
        "county": "county",
        "postal_code": "postalCode",
        "province": "province",
        "state": "state",
    },
)
class CustomerprofilesProfileMailingAddress:
    def __init__(
        self,
        *,
        address1: typing.Optional[builtins.str] = None,
        address2: typing.Optional[builtins.str] = None,
        address3: typing.Optional[builtins.str] = None,
        address4: typing.Optional[builtins.str] = None,
        city: typing.Optional[builtins.str] = None,
        country: typing.Optional[builtins.str] = None,
        county: typing.Optional[builtins.str] = None,
        postal_code: typing.Optional[builtins.str] = None,
        province: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address1: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_1 CustomerprofilesProfile#address_1}.
        :param address2: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_2 CustomerprofilesProfile#address_2}.
        :param address3: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_3 CustomerprofilesProfile#address_3}.
        :param address4: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_4 CustomerprofilesProfile#address_4}.
        :param city: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#city CustomerprofilesProfile#city}.
        :param country: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#country CustomerprofilesProfile#country}.
        :param county: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#county CustomerprofilesProfile#county}.
        :param postal_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#postal_code CustomerprofilesProfile#postal_code}.
        :param province: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#province CustomerprofilesProfile#province}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#state CustomerprofilesProfile#state}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c50202614f7edad856166a29463c1bf74e3fffa78265644d4e4617ca54ac5930)
            check_type(argname="argument address1", value=address1, expected_type=type_hints["address1"])
            check_type(argname="argument address2", value=address2, expected_type=type_hints["address2"])
            check_type(argname="argument address3", value=address3, expected_type=type_hints["address3"])
            check_type(argname="argument address4", value=address4, expected_type=type_hints["address4"])
            check_type(argname="argument city", value=city, expected_type=type_hints["city"])
            check_type(argname="argument country", value=country, expected_type=type_hints["country"])
            check_type(argname="argument county", value=county, expected_type=type_hints["county"])
            check_type(argname="argument postal_code", value=postal_code, expected_type=type_hints["postal_code"])
            check_type(argname="argument province", value=province, expected_type=type_hints["province"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if address1 is not None:
            self._values["address1"] = address1
        if address2 is not None:
            self._values["address2"] = address2
        if address3 is not None:
            self._values["address3"] = address3
        if address4 is not None:
            self._values["address4"] = address4
        if city is not None:
            self._values["city"] = city
        if country is not None:
            self._values["country"] = country
        if county is not None:
            self._values["county"] = county
        if postal_code is not None:
            self._values["postal_code"] = postal_code
        if province is not None:
            self._values["province"] = province
        if state is not None:
            self._values["state"] = state

    @builtins.property
    def address1(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_1 CustomerprofilesProfile#address_1}.'''
        result = self._values.get("address1")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address2(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_2 CustomerprofilesProfile#address_2}.'''
        result = self._values.get("address2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address3(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_3 CustomerprofilesProfile#address_3}.'''
        result = self._values.get("address3")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address4(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_4 CustomerprofilesProfile#address_4}.'''
        result = self._values.get("address4")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def city(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#city CustomerprofilesProfile#city}.'''
        result = self._values.get("city")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def country(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#country CustomerprofilesProfile#country}.'''
        result = self._values.get("country")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def county(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#county CustomerprofilesProfile#county}.'''
        result = self._values.get("county")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def postal_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#postal_code CustomerprofilesProfile#postal_code}.'''
        result = self._values.get("postal_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def province(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#province CustomerprofilesProfile#province}.'''
        result = self._values.get("province")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#state CustomerprofilesProfile#state}.'''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomerprofilesProfileMailingAddress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CustomerprofilesProfileMailingAddressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.customerprofilesProfile.CustomerprofilesProfileMailingAddressOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__15d6a6bd6b6ec1e88ad75202626a836f4b5b2fdc0dda9989219bfde5d593bc35)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAddress1")
    def reset_address1(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress1", []))

    @jsii.member(jsii_name="resetAddress2")
    def reset_address2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress2", []))

    @jsii.member(jsii_name="resetAddress3")
    def reset_address3(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress3", []))

    @jsii.member(jsii_name="resetAddress4")
    def reset_address4(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress4", []))

    @jsii.member(jsii_name="resetCity")
    def reset_city(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCity", []))

    @jsii.member(jsii_name="resetCountry")
    def reset_country(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCountry", []))

    @jsii.member(jsii_name="resetCounty")
    def reset_county(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCounty", []))

    @jsii.member(jsii_name="resetPostalCode")
    def reset_postal_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostalCode", []))

    @jsii.member(jsii_name="resetProvince")
    def reset_province(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvince", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

    @builtins.property
    @jsii.member(jsii_name="address1Input")
    def address1_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "address1Input"))

    @builtins.property
    @jsii.member(jsii_name="address2Input")
    def address2_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "address2Input"))

    @builtins.property
    @jsii.member(jsii_name="address3Input")
    def address3_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "address3Input"))

    @builtins.property
    @jsii.member(jsii_name="address4Input")
    def address4_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "address4Input"))

    @builtins.property
    @jsii.member(jsii_name="cityInput")
    def city_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cityInput"))

    @builtins.property
    @jsii.member(jsii_name="countryInput")
    def country_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countryInput"))

    @builtins.property
    @jsii.member(jsii_name="countyInput")
    def county_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countyInput"))

    @builtins.property
    @jsii.member(jsii_name="postalCodeInput")
    def postal_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "postalCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="provinceInput")
    def province_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "provinceInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="address1")
    def address1(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address1"))

    @address1.setter
    def address1(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4c5fac0bb0e0cb20a61a315de0430ec323cf36bfab5ee24a9b4784a39c1994b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address1", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="address2")
    def address2(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address2"))

    @address2.setter
    def address2(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3e25100eabb3047dac50825763891040559f4f188015005d92967899cbdb5e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address2", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="address3")
    def address3(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address3"))

    @address3.setter
    def address3(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b161075a5aa13c4d6afbacf5ae721d2733a7e6560b5cc4eb8d2dab5ed98fde2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address3", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="address4")
    def address4(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address4"))

    @address4.setter
    def address4(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9a627e7fe7ef12fb81be63f8430458d5e507de7791ab88168c275197f7b5d4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address4", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="city")
    def city(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "city"))

    @city.setter
    def city(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__523c5792e6e485b7f9bd5ecd1e0ca246bdbd415346cebb7953bbe4dd825df5a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "city", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="country")
    def country(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "country"))

    @country.setter
    def country(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0984294e53756773e5bf133ccd8b68500f275767a7c4323eaa0f298e59330d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "country", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="county")
    def county(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "county"))

    @county.setter
    def county(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__396a54947504c98f93a58c71744ed0e45716e20ba32e2c506135898347e0b7ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "county", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postalCode")
    def postal_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postalCode"))

    @postal_code.setter
    def postal_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dfe18eea63f9c9ba4c0c5162fdb8883a220f1cb69f7682fec9da8816e2166e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postalCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="province")
    def province(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "province"))

    @province.setter
    def province(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f68d225669d80a3e0308de93f44022406861091a2ea1e62883add0f08aaf18e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "province", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dce99405bb1f3f0e4e8897318189d08bcc4d38bc290b8a45870a3a232255b85e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CustomerprofilesProfileMailingAddress]:
        return typing.cast(typing.Optional[CustomerprofilesProfileMailingAddress], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CustomerprofilesProfileMailingAddress],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__171421fe73362e07f3aaabc3390d1344c32c04cfc1eaa9ac74d17d7024e28148)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.customerprofilesProfile.CustomerprofilesProfileShippingAddress",
    jsii_struct_bases=[],
    name_mapping={
        "address1": "address1",
        "address2": "address2",
        "address3": "address3",
        "address4": "address4",
        "city": "city",
        "country": "country",
        "county": "county",
        "postal_code": "postalCode",
        "province": "province",
        "state": "state",
    },
)
class CustomerprofilesProfileShippingAddress:
    def __init__(
        self,
        *,
        address1: typing.Optional[builtins.str] = None,
        address2: typing.Optional[builtins.str] = None,
        address3: typing.Optional[builtins.str] = None,
        address4: typing.Optional[builtins.str] = None,
        city: typing.Optional[builtins.str] = None,
        country: typing.Optional[builtins.str] = None,
        county: typing.Optional[builtins.str] = None,
        postal_code: typing.Optional[builtins.str] = None,
        province: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address1: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_1 CustomerprofilesProfile#address_1}.
        :param address2: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_2 CustomerprofilesProfile#address_2}.
        :param address3: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_3 CustomerprofilesProfile#address_3}.
        :param address4: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_4 CustomerprofilesProfile#address_4}.
        :param city: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#city CustomerprofilesProfile#city}.
        :param country: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#country CustomerprofilesProfile#country}.
        :param county: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#county CustomerprofilesProfile#county}.
        :param postal_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#postal_code CustomerprofilesProfile#postal_code}.
        :param province: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#province CustomerprofilesProfile#province}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#state CustomerprofilesProfile#state}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc3049e11bba7ee51bc36771d3d792425b698727ead300ddb65c625fc4086a8c)
            check_type(argname="argument address1", value=address1, expected_type=type_hints["address1"])
            check_type(argname="argument address2", value=address2, expected_type=type_hints["address2"])
            check_type(argname="argument address3", value=address3, expected_type=type_hints["address3"])
            check_type(argname="argument address4", value=address4, expected_type=type_hints["address4"])
            check_type(argname="argument city", value=city, expected_type=type_hints["city"])
            check_type(argname="argument country", value=country, expected_type=type_hints["country"])
            check_type(argname="argument county", value=county, expected_type=type_hints["county"])
            check_type(argname="argument postal_code", value=postal_code, expected_type=type_hints["postal_code"])
            check_type(argname="argument province", value=province, expected_type=type_hints["province"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if address1 is not None:
            self._values["address1"] = address1
        if address2 is not None:
            self._values["address2"] = address2
        if address3 is not None:
            self._values["address3"] = address3
        if address4 is not None:
            self._values["address4"] = address4
        if city is not None:
            self._values["city"] = city
        if country is not None:
            self._values["country"] = country
        if county is not None:
            self._values["county"] = county
        if postal_code is not None:
            self._values["postal_code"] = postal_code
        if province is not None:
            self._values["province"] = province
        if state is not None:
            self._values["state"] = state

    @builtins.property
    def address1(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_1 CustomerprofilesProfile#address_1}.'''
        result = self._values.get("address1")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address2(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_2 CustomerprofilesProfile#address_2}.'''
        result = self._values.get("address2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address3(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_3 CustomerprofilesProfile#address_3}.'''
        result = self._values.get("address3")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address4(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#address_4 CustomerprofilesProfile#address_4}.'''
        result = self._values.get("address4")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def city(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#city CustomerprofilesProfile#city}.'''
        result = self._values.get("city")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def country(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#country CustomerprofilesProfile#country}.'''
        result = self._values.get("country")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def county(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#county CustomerprofilesProfile#county}.'''
        result = self._values.get("county")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def postal_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#postal_code CustomerprofilesProfile#postal_code}.'''
        result = self._values.get("postal_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def province(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#province CustomerprofilesProfile#province}.'''
        result = self._values.get("province")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_profile#state CustomerprofilesProfile#state}.'''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomerprofilesProfileShippingAddress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CustomerprofilesProfileShippingAddressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.customerprofilesProfile.CustomerprofilesProfileShippingAddressOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2da727b5ab119aa44342ad36a0cefda3f1f4e4186cf5fcfad67cf67b112952ff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAddress1")
    def reset_address1(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress1", []))

    @jsii.member(jsii_name="resetAddress2")
    def reset_address2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress2", []))

    @jsii.member(jsii_name="resetAddress3")
    def reset_address3(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress3", []))

    @jsii.member(jsii_name="resetAddress4")
    def reset_address4(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress4", []))

    @jsii.member(jsii_name="resetCity")
    def reset_city(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCity", []))

    @jsii.member(jsii_name="resetCountry")
    def reset_country(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCountry", []))

    @jsii.member(jsii_name="resetCounty")
    def reset_county(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCounty", []))

    @jsii.member(jsii_name="resetPostalCode")
    def reset_postal_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostalCode", []))

    @jsii.member(jsii_name="resetProvince")
    def reset_province(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvince", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

    @builtins.property
    @jsii.member(jsii_name="address1Input")
    def address1_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "address1Input"))

    @builtins.property
    @jsii.member(jsii_name="address2Input")
    def address2_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "address2Input"))

    @builtins.property
    @jsii.member(jsii_name="address3Input")
    def address3_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "address3Input"))

    @builtins.property
    @jsii.member(jsii_name="address4Input")
    def address4_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "address4Input"))

    @builtins.property
    @jsii.member(jsii_name="cityInput")
    def city_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cityInput"))

    @builtins.property
    @jsii.member(jsii_name="countryInput")
    def country_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countryInput"))

    @builtins.property
    @jsii.member(jsii_name="countyInput")
    def county_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countyInput"))

    @builtins.property
    @jsii.member(jsii_name="postalCodeInput")
    def postal_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "postalCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="provinceInput")
    def province_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "provinceInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="address1")
    def address1(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address1"))

    @address1.setter
    def address1(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e00436809b76f64eb57428198904a33541ce9572cf4c1fa891675c50f4566086)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address1", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="address2")
    def address2(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address2"))

    @address2.setter
    def address2(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4b0718285ec55f1f3ee2ca0828a486a6ebb782b09f6e765832cc84033339279)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address2", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="address3")
    def address3(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address3"))

    @address3.setter
    def address3(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ea7103a6c33e0fa25c36ad3e7aff1b5625a4cd6c063bcc1481cc91774267ccd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address3", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="address4")
    def address4(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address4"))

    @address4.setter
    def address4(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62315d3fcea7e688f5a374a934fe1eda246fd04bd5d013466e795fa61efda7c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address4", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="city")
    def city(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "city"))

    @city.setter
    def city(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc8fe99158bfc222189d06fa92693628c28991c291d745d47e3ab688125b13f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "city", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="country")
    def country(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "country"))

    @country.setter
    def country(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db6d0dc0fa17e45e68d0fbba3688aa22f017d0168f250105fcce2e89ff5b8b75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "country", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="county")
    def county(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "county"))

    @county.setter
    def county(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d14f59ecb6d793b8bb6775cb1c23d08142782fb150a35e8f72d0163766571c6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "county", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postalCode")
    def postal_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postalCode"))

    @postal_code.setter
    def postal_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4cf2a0f95ebb9fd9f35c4c7f6dc43179ed6cc8cf7c568d0309bd0517da9b646)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postalCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="province")
    def province(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "province"))

    @province.setter
    def province(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42e6066469a57c8bf1c27e4703826cf352f6672249da3eb0d300e24d68bdd903)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "province", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92bb71b2b498ff48a4689e25b4ad0d7a8df8718157bf71c85e635491911175e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CustomerprofilesProfileShippingAddress]:
        return typing.cast(typing.Optional[CustomerprofilesProfileShippingAddress], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CustomerprofilesProfileShippingAddress],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__579c5d656ca7e8edbfba11cad74481c8150030cf5c0baecb8f5fbae8bf19e7f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CustomerprofilesProfile",
    "CustomerprofilesProfileAddress",
    "CustomerprofilesProfileAddressOutputReference",
    "CustomerprofilesProfileBillingAddress",
    "CustomerprofilesProfileBillingAddressOutputReference",
    "CustomerprofilesProfileConfig",
    "CustomerprofilesProfileMailingAddress",
    "CustomerprofilesProfileMailingAddressOutputReference",
    "CustomerprofilesProfileShippingAddress",
    "CustomerprofilesProfileShippingAddressOutputReference",
]

publication.publish()

def _typecheckingstub__6879827f93e5cd75b89e51b9ed38a5af83a6f045567a7ea70035aba62fc4b9cb(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    domain_name: builtins.str,
    account_number: typing.Optional[builtins.str] = None,
    additional_information: typing.Optional[builtins.str] = None,
    address: typing.Optional[typing.Union[CustomerprofilesProfileAddress, typing.Dict[builtins.str, typing.Any]]] = None,
    attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    billing_address: typing.Optional[typing.Union[CustomerprofilesProfileBillingAddress, typing.Dict[builtins.str, typing.Any]]] = None,
    birth_date: typing.Optional[builtins.str] = None,
    business_email_address: typing.Optional[builtins.str] = None,
    business_name: typing.Optional[builtins.str] = None,
    business_phone_number: typing.Optional[builtins.str] = None,
    email_address: typing.Optional[builtins.str] = None,
    first_name: typing.Optional[builtins.str] = None,
    gender_string: typing.Optional[builtins.str] = None,
    home_phone_number: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    last_name: typing.Optional[builtins.str] = None,
    mailing_address: typing.Optional[typing.Union[CustomerprofilesProfileMailingAddress, typing.Dict[builtins.str, typing.Any]]] = None,
    middle_name: typing.Optional[builtins.str] = None,
    mobile_phone_number: typing.Optional[builtins.str] = None,
    party_type_string: typing.Optional[builtins.str] = None,
    personal_email_address: typing.Optional[builtins.str] = None,
    phone_number: typing.Optional[builtins.str] = None,
    shipping_address: typing.Optional[typing.Union[CustomerprofilesProfileShippingAddress, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__5dac0979b61c5339f320d8fe9cd1e5bc53abc726e616d600981bd7638a66e642(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3749331597c56963abf765de906d5874ff7ac0e77ba36b5a1e7930f580e1d0bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cec85674dd8f810abf05768fbd7d014176cc6c1569b980ad0963c2981a9a61f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c02768c713454b6bcc30d2848ca1f38151ef339b7ad63057b19d22f8c732014d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__468f6c949c5365bf6eea04935df60e50684581b48529faa498626f1f9bddf2d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__527561215e735f1adefb4cdfa874319865eac961783a9b24d24f800da2d2d3bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38f923f88edaf8f72da9eca8be29fffab7fa53de7335a7b6014ac115b58bd8e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40bb21ea778523de878afc959269f2724548f791ef3dc87b0355a26edb1c8042(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a53b25984fe155c2969b9c993b2bf9a7525a8c13d3a494c4cf28892e30594b44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ce144df49066095ef933a4de10681d402137b9a7b23481bbb3e4b3e5142304d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a54b1a1338e7d1ae5610863aa9f4f0742b01b3d3645ae34c08c081a21c1350eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24430200a06815fd98f4ed4b50a29710cbe005e8a29acc604b3a44493a7a8034(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61387068817a1a5dafad7ca78dae245801cb9e649975931d5daeadd3c70b10ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68ae759c999f6c47e855867eeeb0e87036e754be380f43fe9ff6f7d5365634ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52fa4db1901264602f79c410aec635bd1808733ec3c454fc29964d8f9cdafe07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea801fa235cd5395b48f1c3bfcfd9d064467be003bfd8daafab4a02f02fec8f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__688dbfe75162a09f2e1e040921742ba1c2d673170398a81c8f34b998fb9ee3dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b650edb09329b98c03e127aa62354a0cbbc3587eefb1f15a5dce73bee3df741(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5a491a27655a05c73c9ae0ad14623f74e2a43e8959c7c43f9e26f8861257860(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43e9ad5dd5547f43270153c61f8c63b4d835518ce8ceecac3cf0096a4e11ddb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dec09c6e00db9f9a36e25888d30ac526300ecd7cbacb5639b23092da048b1b4e(
    *,
    address1: typing.Optional[builtins.str] = None,
    address2: typing.Optional[builtins.str] = None,
    address3: typing.Optional[builtins.str] = None,
    address4: typing.Optional[builtins.str] = None,
    city: typing.Optional[builtins.str] = None,
    country: typing.Optional[builtins.str] = None,
    county: typing.Optional[builtins.str] = None,
    postal_code: typing.Optional[builtins.str] = None,
    province: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9333340d92cfcc6409a8bae1b0f1e7d36c31c304550fe6f90e2b86d4ac5e789e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62720a0d5368628fd9c4627cf9ce916646788a5554802788b755a5c89d4f082c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59e3024fa77954326a9c13cc99fb8680ff058607bfab2b8a019df738210b6f37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a71548319e618eedd22c4d9e567f97c3c047f526b3e79fd87da171a1ed9e325(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a5105d0fa9d11bde3a6cbd918588016f8ca3ebecd0d9ceef2979c96e6e61bb1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f18b377b1580f6b13ad6906734a7907ac854021f5bd15e598cabec1f2bb37eb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57c433332826bc14242ceb8894790b8d706a467c506dfba60af0e662bc45c945(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33e50dd37069cb65f33aeecc029f0086ab392acb3c1824fd5a254ca7c0283929(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1b39110dfe1e62590337be2c3fa4138becc51169fa456fe2045137b0330bced(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__584478a79ff643efb8767a6ca7dc36381d133a9e45a2151f4178dcead535a3ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__993241e38a2a7ee202ba20ba8947f15f1eed913c5d4b6b7062574d99bbf57e38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4f127b8dfa87c08276588d0bd4792d2b65d897c98df64dd0d440b5d57827858(
    value: typing.Optional[CustomerprofilesProfileAddress],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1de07e7c7d26e1e5debbc550532645495c12f16a894814d3443d42d371f71037(
    *,
    address1: typing.Optional[builtins.str] = None,
    address2: typing.Optional[builtins.str] = None,
    address3: typing.Optional[builtins.str] = None,
    address4: typing.Optional[builtins.str] = None,
    city: typing.Optional[builtins.str] = None,
    country: typing.Optional[builtins.str] = None,
    county: typing.Optional[builtins.str] = None,
    postal_code: typing.Optional[builtins.str] = None,
    province: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2503e3177f5e0a4edf2e6d4a1594813c3dc09b0ddc2dbe0f920c84fa62457ef7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82064c0e9d3ea5f32bdbb02aa6c3c3c28403a76ce8933aa1f6df92bc8d43c904(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83eaafccdb162eeb7e135f0dfc891502bcf486ee6da03a3b3f8ab6bc86223f37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d79b58280087d41fd057afc8dc87c2c3c931fb5f9f2b9354ca5350b1fe420fcd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fcf8149ecb68c463b318fcc8d74beaa049816d3405172653b930fccb4171049(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8da00c8dad4048c96e189ae162288a6ae6582b8335c386ffea952a48125356ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55c17b57740f693dbd601a2c70e47fd78528d5c03560694cdceb73b4e98e2a11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ccc92a80f0a39b441238956b9eeccda7d4a70b8c339ff438932df0710e9eddb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__735e35587d33b14bec33f308fbb078c6b34e73f7e1d9affe0e1dfe6bdf430624(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8415bf8c335fd927ffe29709e9a2a267be35f545bbeb265ba931f128961f05ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e9c421f825e2fd000b56071463deff87e1f2b9c9135bef7d38cb0e29a1f7c30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__398fdc8a69f489aa67a7fb38ef8580c2b2277ea84f7464e56742a6c72716c185(
    value: typing.Optional[CustomerprofilesProfileBillingAddress],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dd541898d4275d36a1abd5c1a29e425a0cb79b367c5941cbc8e5190327faef8(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    domain_name: builtins.str,
    account_number: typing.Optional[builtins.str] = None,
    additional_information: typing.Optional[builtins.str] = None,
    address: typing.Optional[typing.Union[CustomerprofilesProfileAddress, typing.Dict[builtins.str, typing.Any]]] = None,
    attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    billing_address: typing.Optional[typing.Union[CustomerprofilesProfileBillingAddress, typing.Dict[builtins.str, typing.Any]]] = None,
    birth_date: typing.Optional[builtins.str] = None,
    business_email_address: typing.Optional[builtins.str] = None,
    business_name: typing.Optional[builtins.str] = None,
    business_phone_number: typing.Optional[builtins.str] = None,
    email_address: typing.Optional[builtins.str] = None,
    first_name: typing.Optional[builtins.str] = None,
    gender_string: typing.Optional[builtins.str] = None,
    home_phone_number: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    last_name: typing.Optional[builtins.str] = None,
    mailing_address: typing.Optional[typing.Union[CustomerprofilesProfileMailingAddress, typing.Dict[builtins.str, typing.Any]]] = None,
    middle_name: typing.Optional[builtins.str] = None,
    mobile_phone_number: typing.Optional[builtins.str] = None,
    party_type_string: typing.Optional[builtins.str] = None,
    personal_email_address: typing.Optional[builtins.str] = None,
    phone_number: typing.Optional[builtins.str] = None,
    shipping_address: typing.Optional[typing.Union[CustomerprofilesProfileShippingAddress, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c50202614f7edad856166a29463c1bf74e3fffa78265644d4e4617ca54ac5930(
    *,
    address1: typing.Optional[builtins.str] = None,
    address2: typing.Optional[builtins.str] = None,
    address3: typing.Optional[builtins.str] = None,
    address4: typing.Optional[builtins.str] = None,
    city: typing.Optional[builtins.str] = None,
    country: typing.Optional[builtins.str] = None,
    county: typing.Optional[builtins.str] = None,
    postal_code: typing.Optional[builtins.str] = None,
    province: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15d6a6bd6b6ec1e88ad75202626a836f4b5b2fdc0dda9989219bfde5d593bc35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4c5fac0bb0e0cb20a61a315de0430ec323cf36bfab5ee24a9b4784a39c1994b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3e25100eabb3047dac50825763891040559f4f188015005d92967899cbdb5e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b161075a5aa13c4d6afbacf5ae721d2733a7e6560b5cc4eb8d2dab5ed98fde2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9a627e7fe7ef12fb81be63f8430458d5e507de7791ab88168c275197f7b5d4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__523c5792e6e485b7f9bd5ecd1e0ca246bdbd415346cebb7953bbe4dd825df5a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0984294e53756773e5bf133ccd8b68500f275767a7c4323eaa0f298e59330d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__396a54947504c98f93a58c71744ed0e45716e20ba32e2c506135898347e0b7ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dfe18eea63f9c9ba4c0c5162fdb8883a220f1cb69f7682fec9da8816e2166e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f68d225669d80a3e0308de93f44022406861091a2ea1e62883add0f08aaf18e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dce99405bb1f3f0e4e8897318189d08bcc4d38bc290b8a45870a3a232255b85e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__171421fe73362e07f3aaabc3390d1344c32c04cfc1eaa9ac74d17d7024e28148(
    value: typing.Optional[CustomerprofilesProfileMailingAddress],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc3049e11bba7ee51bc36771d3d792425b698727ead300ddb65c625fc4086a8c(
    *,
    address1: typing.Optional[builtins.str] = None,
    address2: typing.Optional[builtins.str] = None,
    address3: typing.Optional[builtins.str] = None,
    address4: typing.Optional[builtins.str] = None,
    city: typing.Optional[builtins.str] = None,
    country: typing.Optional[builtins.str] = None,
    county: typing.Optional[builtins.str] = None,
    postal_code: typing.Optional[builtins.str] = None,
    province: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2da727b5ab119aa44342ad36a0cefda3f1f4e4186cf5fcfad67cf67b112952ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e00436809b76f64eb57428198904a33541ce9572cf4c1fa891675c50f4566086(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4b0718285ec55f1f3ee2ca0828a486a6ebb782b09f6e765832cc84033339279(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ea7103a6c33e0fa25c36ad3e7aff1b5625a4cd6c063bcc1481cc91774267ccd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62315d3fcea7e688f5a374a934fe1eda246fd04bd5d013466e795fa61efda7c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc8fe99158bfc222189d06fa92693628c28991c291d745d47e3ab688125b13f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db6d0dc0fa17e45e68d0fbba3688aa22f017d0168f250105fcce2e89ff5b8b75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d14f59ecb6d793b8bb6775cb1c23d08142782fb150a35e8f72d0163766571c6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4cf2a0f95ebb9fd9f35c4c7f6dc43179ed6cc8cf7c568d0309bd0517da9b646(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42e6066469a57c8bf1c27e4703826cf352f6672249da3eb0d300e24d68bdd903(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92bb71b2b498ff48a4689e25b4ad0d7a8df8718157bf71c85e635491911175e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__579c5d656ca7e8edbfba11cad74481c8150030cf5c0baecb8f5fbae8bf19e7f5(
    value: typing.Optional[CustomerprofilesProfileShippingAddress],
) -> None:
    """Type checking stubs"""
    pass
