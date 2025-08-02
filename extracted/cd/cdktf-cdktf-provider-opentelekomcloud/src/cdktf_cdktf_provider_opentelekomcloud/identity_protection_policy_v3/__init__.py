r'''
# `opentelekomcloud_identity_protection_policy_v3`

Refer to the Terraform Registry for docs: [`opentelekomcloud_identity_protection_policy_v3`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protection_policy_v3).
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


class IdentityProtectionPolicyV3(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.identityProtectionPolicyV3.IdentityProtectionPolicyV3",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protection_policy_v3 opentelekomcloud_identity_protection_policy_v3}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        enable_operation_protection_policy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        self_management: typing.Optional[typing.Union["IdentityProtectionPolicyV3SelfManagement", typing.Dict[builtins.str, typing.Any]]] = None,
        verification_email: typing.Optional[builtins.str] = None,
        verification_mobile: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protection_policy_v3 opentelekomcloud_identity_protection_policy_v3} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param enable_operation_protection_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protection_policy_v3#enable_operation_protection_policy IdentityProtectionPolicyV3#enable_operation_protection_policy}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protection_policy_v3#id IdentityProtectionPolicyV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param self_management: self_management block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protection_policy_v3#self_management IdentityProtectionPolicyV3#self_management}
        :param verification_email: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protection_policy_v3#verification_email IdentityProtectionPolicyV3#verification_email}.
        :param verification_mobile: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protection_policy_v3#verification_mobile IdentityProtectionPolicyV3#verification_mobile}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04d141aceba24eaf1cda5fbb991b9b09cb59ad912b0cb8f862cdbabb6501d0ca)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = IdentityProtectionPolicyV3Config(
            enable_operation_protection_policy=enable_operation_protection_policy,
            id=id,
            self_management=self_management,
            verification_email=verification_email,
            verification_mobile=verification_mobile,
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
        '''Generates CDKTF code for importing a IdentityProtectionPolicyV3 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the IdentityProtectionPolicyV3 to import.
        :param import_from_id: The id of the existing IdentityProtectionPolicyV3 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protection_policy_v3#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the IdentityProtectionPolicyV3 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c46f22c7ad0d61a2ccd2ef96a993608710661df437b4e988082641a008ed38c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putSelfManagement")
    def put_self_management(
        self,
        *,
        access_key: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        email: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        mobile: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param access_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protection_policy_v3#access_key IdentityProtectionPolicyV3#access_key}.
        :param email: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protection_policy_v3#email IdentityProtectionPolicyV3#email}.
        :param mobile: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protection_policy_v3#mobile IdentityProtectionPolicyV3#mobile}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protection_policy_v3#password IdentityProtectionPolicyV3#password}.
        '''
        value = IdentityProtectionPolicyV3SelfManagement(
            access_key=access_key, email=email, mobile=mobile, password=password
        )

        return typing.cast(None, jsii.invoke(self, "putSelfManagement", [value]))

    @jsii.member(jsii_name="resetEnableOperationProtectionPolicy")
    def reset_enable_operation_protection_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableOperationProtectionPolicy", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetSelfManagement")
    def reset_self_management(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelfManagement", []))

    @jsii.member(jsii_name="resetVerificationEmail")
    def reset_verification_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerificationEmail", []))

    @jsii.member(jsii_name="resetVerificationMobile")
    def reset_verification_mobile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerificationMobile", []))

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
    @jsii.member(jsii_name="selfManagement")
    def self_management(
        self,
    ) -> "IdentityProtectionPolicyV3SelfManagementOutputReference":
        return typing.cast("IdentityProtectionPolicyV3SelfManagementOutputReference", jsii.get(self, "selfManagement"))

    @builtins.property
    @jsii.member(jsii_name="selfVerification")
    def self_verification(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "selfVerification"))

    @builtins.property
    @jsii.member(jsii_name="enableOperationProtectionPolicyInput")
    def enable_operation_protection_policy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableOperationProtectionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="selfManagementInput")
    def self_management_input(
        self,
    ) -> typing.Optional["IdentityProtectionPolicyV3SelfManagement"]:
        return typing.cast(typing.Optional["IdentityProtectionPolicyV3SelfManagement"], jsii.get(self, "selfManagementInput"))

    @builtins.property
    @jsii.member(jsii_name="verificationEmailInput")
    def verification_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "verificationEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="verificationMobileInput")
    def verification_mobile_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "verificationMobileInput"))

    @builtins.property
    @jsii.member(jsii_name="enableOperationProtectionPolicy")
    def enable_operation_protection_policy(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableOperationProtectionPolicy"))

    @enable_operation_protection_policy.setter
    def enable_operation_protection_policy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__303104ab8ca5734fa862e25defd3213bdfea5deabbcf105d429236fe67bce0e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableOperationProtectionPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44445fb1a180f53fbcf0b6e48d866ca220755a6afc5abe1d3e985e8bcf474bfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="verificationEmail")
    def verification_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "verificationEmail"))

    @verification_email.setter
    def verification_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20c944f84f3ffb25929c4835820ed50cbaefea48e4d942f64efbabf4437c5a26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verificationEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="verificationMobile")
    def verification_mobile(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "verificationMobile"))

    @verification_mobile.setter
    def verification_mobile(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__330a2e347e26d3f301f230cadfd9685fdaf15e5285051d42cb395aabad5deac8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verificationMobile", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.identityProtectionPolicyV3.IdentityProtectionPolicyV3Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "enable_operation_protection_policy": "enableOperationProtectionPolicy",
        "id": "id",
        "self_management": "selfManagement",
        "verification_email": "verificationEmail",
        "verification_mobile": "verificationMobile",
    },
)
class IdentityProtectionPolicyV3Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        enable_operation_protection_policy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        self_management: typing.Optional[typing.Union["IdentityProtectionPolicyV3SelfManagement", typing.Dict[builtins.str, typing.Any]]] = None,
        verification_email: typing.Optional[builtins.str] = None,
        verification_mobile: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param enable_operation_protection_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protection_policy_v3#enable_operation_protection_policy IdentityProtectionPolicyV3#enable_operation_protection_policy}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protection_policy_v3#id IdentityProtectionPolicyV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param self_management: self_management block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protection_policy_v3#self_management IdentityProtectionPolicyV3#self_management}
        :param verification_email: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protection_policy_v3#verification_email IdentityProtectionPolicyV3#verification_email}.
        :param verification_mobile: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protection_policy_v3#verification_mobile IdentityProtectionPolicyV3#verification_mobile}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(self_management, dict):
            self_management = IdentityProtectionPolicyV3SelfManagement(**self_management)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5703b9865136581b90ac0d1f5db1a99329fc57d4018653d0a7f8b9f2d121a8e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument enable_operation_protection_policy", value=enable_operation_protection_policy, expected_type=type_hints["enable_operation_protection_policy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument self_management", value=self_management, expected_type=type_hints["self_management"])
            check_type(argname="argument verification_email", value=verification_email, expected_type=type_hints["verification_email"])
            check_type(argname="argument verification_mobile", value=verification_mobile, expected_type=type_hints["verification_mobile"])
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
        if enable_operation_protection_policy is not None:
            self._values["enable_operation_protection_policy"] = enable_operation_protection_policy
        if id is not None:
            self._values["id"] = id
        if self_management is not None:
            self._values["self_management"] = self_management
        if verification_email is not None:
            self._values["verification_email"] = verification_email
        if verification_mobile is not None:
            self._values["verification_mobile"] = verification_mobile

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
    def enable_operation_protection_policy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protection_policy_v3#enable_operation_protection_policy IdentityProtectionPolicyV3#enable_operation_protection_policy}.'''
        result = self._values.get("enable_operation_protection_policy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protection_policy_v3#id IdentityProtectionPolicyV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def self_management(
        self,
    ) -> typing.Optional["IdentityProtectionPolicyV3SelfManagement"]:
        '''self_management block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protection_policy_v3#self_management IdentityProtectionPolicyV3#self_management}
        '''
        result = self._values.get("self_management")
        return typing.cast(typing.Optional["IdentityProtectionPolicyV3SelfManagement"], result)

    @builtins.property
    def verification_email(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protection_policy_v3#verification_email IdentityProtectionPolicyV3#verification_email}.'''
        result = self._values.get("verification_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def verification_mobile(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protection_policy_v3#verification_mobile IdentityProtectionPolicyV3#verification_mobile}.'''
        result = self._values.get("verification_mobile")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityProtectionPolicyV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.identityProtectionPolicyV3.IdentityProtectionPolicyV3SelfManagement",
    jsii_struct_bases=[],
    name_mapping={
        "access_key": "accessKey",
        "email": "email",
        "mobile": "mobile",
        "password": "password",
    },
)
class IdentityProtectionPolicyV3SelfManagement:
    def __init__(
        self,
        *,
        access_key: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        email: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        mobile: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param access_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protection_policy_v3#access_key IdentityProtectionPolicyV3#access_key}.
        :param email: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protection_policy_v3#email IdentityProtectionPolicyV3#email}.
        :param mobile: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protection_policy_v3#mobile IdentityProtectionPolicyV3#mobile}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protection_policy_v3#password IdentityProtectionPolicyV3#password}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ebafddee8db7da6dd4134f6563329b5f417b23fe2df9c1b7f5264863c4cb273)
            check_type(argname="argument access_key", value=access_key, expected_type=type_hints["access_key"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument mobile", value=mobile, expected_type=type_hints["mobile"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_key is not None:
            self._values["access_key"] = access_key
        if email is not None:
            self._values["email"] = email
        if mobile is not None:
            self._values["mobile"] = mobile
        if password is not None:
            self._values["password"] = password

    @builtins.property
    def access_key(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protection_policy_v3#access_key IdentityProtectionPolicyV3#access_key}.'''
        result = self._values.get("access_key")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def email(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protection_policy_v3#email IdentityProtectionPolicyV3#email}.'''
        result = self._values.get("email")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def mobile(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protection_policy_v3#mobile IdentityProtectionPolicyV3#mobile}.'''
        result = self._values.get("mobile")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def password(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_protection_policy_v3#password IdentityProtectionPolicyV3#password}.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityProtectionPolicyV3SelfManagement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IdentityProtectionPolicyV3SelfManagementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.identityProtectionPolicyV3.IdentityProtectionPolicyV3SelfManagementOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e25797a2757abcd23679acf88dee31d0228e02fa9bb857bedb78b264dfbdb527)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAccessKey")
    def reset_access_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessKey", []))

    @jsii.member(jsii_name="resetEmail")
    def reset_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmail", []))

    @jsii.member(jsii_name="resetMobile")
    def reset_mobile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMobile", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @builtins.property
    @jsii.member(jsii_name="accessKeyInput")
    def access_key_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "accessKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="mobileInput")
    def mobile_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mobileInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="accessKey")
    def access_key(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "accessKey"))

    @access_key.setter
    def access_key(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a8815ab3b80c0fe05a2c50317e770e11ac54124c6de1d7b14651d49a411b4bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "email"))

    @email.setter
    def email(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95a952218f4f1118c4857db2d0de87ae7592a65215204712be06279fd5d21999)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mobile")
    def mobile(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mobile"))

    @mobile.setter
    def mobile(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68763ed0c20d6ee6369c85ae65e34d413ad5c9855be3c4fc6d0397bd2e950692)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mobile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "password"))

    @password.setter
    def password(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01fdc01539fd641ea3cd230373109e89e803a5664175ea566cb9ba6494a856d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IdentityProtectionPolicyV3SelfManagement]:
        return typing.cast(typing.Optional[IdentityProtectionPolicyV3SelfManagement], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IdentityProtectionPolicyV3SelfManagement],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d457a5ccb83464364c52d4bd692c45381e95a2d6e7b3b8805cafab84a89c92d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "IdentityProtectionPolicyV3",
    "IdentityProtectionPolicyV3Config",
    "IdentityProtectionPolicyV3SelfManagement",
    "IdentityProtectionPolicyV3SelfManagementOutputReference",
]

publication.publish()

def _typecheckingstub__04d141aceba24eaf1cda5fbb991b9b09cb59ad912b0cb8f862cdbabb6501d0ca(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    enable_operation_protection_policy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    self_management: typing.Optional[typing.Union[IdentityProtectionPolicyV3SelfManagement, typing.Dict[builtins.str, typing.Any]]] = None,
    verification_email: typing.Optional[builtins.str] = None,
    verification_mobile: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__3c46f22c7ad0d61a2ccd2ef96a993608710661df437b4e988082641a008ed38c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__303104ab8ca5734fa862e25defd3213bdfea5deabbcf105d429236fe67bce0e5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44445fb1a180f53fbcf0b6e48d866ca220755a6afc5abe1d3e985e8bcf474bfb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20c944f84f3ffb25929c4835820ed50cbaefea48e4d942f64efbabf4437c5a26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__330a2e347e26d3f301f230cadfd9685fdaf15e5285051d42cb395aabad5deac8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5703b9865136581b90ac0d1f5db1a99329fc57d4018653d0a7f8b9f2d121a8e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enable_operation_protection_policy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    self_management: typing.Optional[typing.Union[IdentityProtectionPolicyV3SelfManagement, typing.Dict[builtins.str, typing.Any]]] = None,
    verification_email: typing.Optional[builtins.str] = None,
    verification_mobile: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ebafddee8db7da6dd4134f6563329b5f417b23fe2df9c1b7f5264863c4cb273(
    *,
    access_key: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    email: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    mobile: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e25797a2757abcd23679acf88dee31d0228e02fa9bb857bedb78b264dfbdb527(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a8815ab3b80c0fe05a2c50317e770e11ac54124c6de1d7b14651d49a411b4bb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95a952218f4f1118c4857db2d0de87ae7592a65215204712be06279fd5d21999(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68763ed0c20d6ee6369c85ae65e34d413ad5c9855be3c4fc6d0397bd2e950692(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01fdc01539fd641ea3cd230373109e89e803a5664175ea566cb9ba6494a856d1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d457a5ccb83464364c52d4bd692c45381e95a2d6e7b3b8805cafab84a89c92d1(
    value: typing.Optional[IdentityProtectionPolicyV3SelfManagement],
) -> None:
    """Type checking stubs"""
    pass
