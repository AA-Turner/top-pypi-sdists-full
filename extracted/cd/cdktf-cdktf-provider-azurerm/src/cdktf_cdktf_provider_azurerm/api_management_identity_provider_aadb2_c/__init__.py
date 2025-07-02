r'''
# `azurerm_api_management_identity_provider_aadb2c`

Refer to the Terraform Registry for docs: [`azurerm_api_management_identity_provider_aadb2c`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c).
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


class ApiManagementIdentityProviderAadb2C(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementIdentityProviderAadb2C.ApiManagementIdentityProviderAadb2C",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c azurerm_api_management_identity_provider_aadb2c}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        allowed_tenant: builtins.str,
        api_management_name: builtins.str,
        authority: builtins.str,
        client_id: builtins.str,
        client_secret: builtins.str,
        resource_group_name: builtins.str,
        signin_policy: builtins.str,
        signin_tenant: builtins.str,
        signup_policy: builtins.str,
        client_library: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        password_reset_policy: typing.Optional[builtins.str] = None,
        profile_editing_policy: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ApiManagementIdentityProviderAadb2CTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c azurerm_api_management_identity_provider_aadb2c} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param allowed_tenant: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#allowed_tenant ApiManagementIdentityProviderAadb2C#allowed_tenant}.
        :param api_management_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#api_management_name ApiManagementIdentityProviderAadb2C#api_management_name}.
        :param authority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#authority ApiManagementIdentityProviderAadb2C#authority}.
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#client_id ApiManagementIdentityProviderAadb2C#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#client_secret ApiManagementIdentityProviderAadb2C#client_secret}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#resource_group_name ApiManagementIdentityProviderAadb2C#resource_group_name}.
        :param signin_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#signin_policy ApiManagementIdentityProviderAadb2C#signin_policy}.
        :param signin_tenant: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#signin_tenant ApiManagementIdentityProviderAadb2C#signin_tenant}.
        :param signup_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#signup_policy ApiManagementIdentityProviderAadb2C#signup_policy}.
        :param client_library: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#client_library ApiManagementIdentityProviderAadb2C#client_library}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#id ApiManagementIdentityProviderAadb2C#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param password_reset_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#password_reset_policy ApiManagementIdentityProviderAadb2C#password_reset_policy}.
        :param profile_editing_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#profile_editing_policy ApiManagementIdentityProviderAadb2C#profile_editing_policy}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#timeouts ApiManagementIdentityProviderAadb2C#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91e08975758c10709e48effa5aa76e9ea18a2147fba4bfdfca18bb90af770abd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApiManagementIdentityProviderAadb2CConfig(
            allowed_tenant=allowed_tenant,
            api_management_name=api_management_name,
            authority=authority,
            client_id=client_id,
            client_secret=client_secret,
            resource_group_name=resource_group_name,
            signin_policy=signin_policy,
            signin_tenant=signin_tenant,
            signup_policy=signup_policy,
            client_library=client_library,
            id=id,
            password_reset_policy=password_reset_policy,
            profile_editing_policy=profile_editing_policy,
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
        '''Generates CDKTF code for importing a ApiManagementIdentityProviderAadb2C resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ApiManagementIdentityProviderAadb2C to import.
        :param import_from_id: The id of the existing ApiManagementIdentityProviderAadb2C that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ApiManagementIdentityProviderAadb2C to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c96f6fe4e8d51a6492b285ea4ca7accf48f9ef8b2d2ed9aec396f4b9ca168c6)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#create ApiManagementIdentityProviderAadb2C#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#delete ApiManagementIdentityProviderAadb2C#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#read ApiManagementIdentityProviderAadb2C#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#update ApiManagementIdentityProviderAadb2C#update}.
        '''
        value = ApiManagementIdentityProviderAadb2CTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetClientLibrary")
    def reset_client_library(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientLibrary", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPasswordResetPolicy")
    def reset_password_reset_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordResetPolicy", []))

    @jsii.member(jsii_name="resetProfileEditingPolicy")
    def reset_profile_editing_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProfileEditingPolicy", []))

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
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ApiManagementIdentityProviderAadb2CTimeoutsOutputReference":
        return typing.cast("ApiManagementIdentityProviderAadb2CTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="allowedTenantInput")
    def allowed_tenant_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "allowedTenantInput"))

    @builtins.property
    @jsii.member(jsii_name="apiManagementNameInput")
    def api_management_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiManagementNameInput"))

    @builtins.property
    @jsii.member(jsii_name="authorityInput")
    def authority_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorityInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientLibraryInput")
    def client_library_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientLibraryInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordResetPolicyInput")
    def password_reset_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordResetPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="profileEditingPolicyInput")
    def profile_editing_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "profileEditingPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="signinPolicyInput")
    def signin_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "signinPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="signinTenantInput")
    def signin_tenant_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "signinTenantInput"))

    @builtins.property
    @jsii.member(jsii_name="signupPolicyInput")
    def signup_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "signupPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApiManagementIdentityProviderAadb2CTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApiManagementIdentityProviderAadb2CTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedTenant")
    def allowed_tenant(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "allowedTenant"))

    @allowed_tenant.setter
    def allowed_tenant(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__495610938de513653425291f5bfc68fc99a94a90e9c6dfd98c68b42f1e165955)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedTenant", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiManagementName")
    def api_management_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiManagementName"))

    @api_management_name.setter
    def api_management_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abd03d222fa3e23c3d7e26a52b003e242e8f0c85ccd78c770145c71de630231c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiManagementName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authority")
    def authority(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authority"))

    @authority.setter
    def authority(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cb509b6a38927afb8a98dfdd605e5015c6756857cd3e2d457029ba0b4dd77a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbb0e76414b93612ef34a96681123303f543f22e49c6f41fa1334655642b0f4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientLibrary")
    def client_library(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientLibrary"))

    @client_library.setter
    def client_library(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d44e1c03078cf81089239bcf1ea48239bdf59f3ab8b5a3057e9daf13f423aa1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientLibrary", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4de9b5d247254d5c6dbbd53632ead1a37f19320171cf12df4505fe623016f4ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ead68c63225727d642f14298639344926f56717478cefd0f521cb8440c665eb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="passwordResetPolicy")
    def password_reset_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "passwordResetPolicy"))

    @password_reset_policy.setter
    def password_reset_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9685c1c06f8157a65b85d92448a4c8f0f9363dca81011d18d8879e7ed8d03c26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordResetPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="profileEditingPolicy")
    def profile_editing_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "profileEditingPolicy"))

    @profile_editing_policy.setter
    def profile_editing_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a8330a51c6ef9b1761f206dbfca11822df558f18b3515e295fc857a623ee189)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profileEditingPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9381286e2f49f8770ed371339ce160d94c09be67530f6122243339f1df525ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="signinPolicy")
    def signin_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signinPolicy"))

    @signin_policy.setter
    def signin_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b06f1eed2d9d3f7dff22565072f59cd9503155453bf1f35558d786bfb875466d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signinPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="signinTenant")
    def signin_tenant(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signinTenant"))

    @signin_tenant.setter
    def signin_tenant(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37e8e5f87275d37c5ce13c23d1a063ce5da336b881176aa212d547cdfeab211f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signinTenant", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="signupPolicy")
    def signup_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signupPolicy"))

    @signup_policy.setter
    def signup_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a337200a8090457669a653a7f5f7220d936f1faa409066da35a874aab978028)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signupPolicy", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementIdentityProviderAadb2C.ApiManagementIdentityProviderAadb2CConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "allowed_tenant": "allowedTenant",
        "api_management_name": "apiManagementName",
        "authority": "authority",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "resource_group_name": "resourceGroupName",
        "signin_policy": "signinPolicy",
        "signin_tenant": "signinTenant",
        "signup_policy": "signupPolicy",
        "client_library": "clientLibrary",
        "id": "id",
        "password_reset_policy": "passwordResetPolicy",
        "profile_editing_policy": "profileEditingPolicy",
        "timeouts": "timeouts",
    },
)
class ApiManagementIdentityProviderAadb2CConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        allowed_tenant: builtins.str,
        api_management_name: builtins.str,
        authority: builtins.str,
        client_id: builtins.str,
        client_secret: builtins.str,
        resource_group_name: builtins.str,
        signin_policy: builtins.str,
        signin_tenant: builtins.str,
        signup_policy: builtins.str,
        client_library: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        password_reset_policy: typing.Optional[builtins.str] = None,
        profile_editing_policy: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ApiManagementIdentityProviderAadb2CTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param allowed_tenant: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#allowed_tenant ApiManagementIdentityProviderAadb2C#allowed_tenant}.
        :param api_management_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#api_management_name ApiManagementIdentityProviderAadb2C#api_management_name}.
        :param authority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#authority ApiManagementIdentityProviderAadb2C#authority}.
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#client_id ApiManagementIdentityProviderAadb2C#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#client_secret ApiManagementIdentityProviderAadb2C#client_secret}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#resource_group_name ApiManagementIdentityProviderAadb2C#resource_group_name}.
        :param signin_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#signin_policy ApiManagementIdentityProviderAadb2C#signin_policy}.
        :param signin_tenant: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#signin_tenant ApiManagementIdentityProviderAadb2C#signin_tenant}.
        :param signup_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#signup_policy ApiManagementIdentityProviderAadb2C#signup_policy}.
        :param client_library: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#client_library ApiManagementIdentityProviderAadb2C#client_library}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#id ApiManagementIdentityProviderAadb2C#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param password_reset_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#password_reset_policy ApiManagementIdentityProviderAadb2C#password_reset_policy}.
        :param profile_editing_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#profile_editing_policy ApiManagementIdentityProviderAadb2C#profile_editing_policy}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#timeouts ApiManagementIdentityProviderAadb2C#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = ApiManagementIdentityProviderAadb2CTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13ae92988959d79ee3b2fa27d762ce3ce656be847d2d3aa6ae42467c6cf17f54)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument allowed_tenant", value=allowed_tenant, expected_type=type_hints["allowed_tenant"])
            check_type(argname="argument api_management_name", value=api_management_name, expected_type=type_hints["api_management_name"])
            check_type(argname="argument authority", value=authority, expected_type=type_hints["authority"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument signin_policy", value=signin_policy, expected_type=type_hints["signin_policy"])
            check_type(argname="argument signin_tenant", value=signin_tenant, expected_type=type_hints["signin_tenant"])
            check_type(argname="argument signup_policy", value=signup_policy, expected_type=type_hints["signup_policy"])
            check_type(argname="argument client_library", value=client_library, expected_type=type_hints["client_library"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument password_reset_policy", value=password_reset_policy, expected_type=type_hints["password_reset_policy"])
            check_type(argname="argument profile_editing_policy", value=profile_editing_policy, expected_type=type_hints["profile_editing_policy"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allowed_tenant": allowed_tenant,
            "api_management_name": api_management_name,
            "authority": authority,
            "client_id": client_id,
            "client_secret": client_secret,
            "resource_group_name": resource_group_name,
            "signin_policy": signin_policy,
            "signin_tenant": signin_tenant,
            "signup_policy": signup_policy,
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
        if client_library is not None:
            self._values["client_library"] = client_library
        if id is not None:
            self._values["id"] = id
        if password_reset_policy is not None:
            self._values["password_reset_policy"] = password_reset_policy
        if profile_editing_policy is not None:
            self._values["profile_editing_policy"] = profile_editing_policy
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
    def allowed_tenant(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#allowed_tenant ApiManagementIdentityProviderAadb2C#allowed_tenant}.'''
        result = self._values.get("allowed_tenant")
        assert result is not None, "Required property 'allowed_tenant' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_management_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#api_management_name ApiManagementIdentityProviderAadb2C#api_management_name}.'''
        result = self._values.get("api_management_name")
        assert result is not None, "Required property 'api_management_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authority(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#authority ApiManagementIdentityProviderAadb2C#authority}.'''
        result = self._values.get("authority")
        assert result is not None, "Required property 'authority' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#client_id ApiManagementIdentityProviderAadb2C#client_id}.'''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#client_secret ApiManagementIdentityProviderAadb2C#client_secret}.'''
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#resource_group_name ApiManagementIdentityProviderAadb2C#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def signin_policy(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#signin_policy ApiManagementIdentityProviderAadb2C#signin_policy}.'''
        result = self._values.get("signin_policy")
        assert result is not None, "Required property 'signin_policy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def signin_tenant(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#signin_tenant ApiManagementIdentityProviderAadb2C#signin_tenant}.'''
        result = self._values.get("signin_tenant")
        assert result is not None, "Required property 'signin_tenant' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def signup_policy(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#signup_policy ApiManagementIdentityProviderAadb2C#signup_policy}.'''
        result = self._values.get("signup_policy")
        assert result is not None, "Required property 'signup_policy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_library(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#client_library ApiManagementIdentityProviderAadb2C#client_library}.'''
        result = self._values.get("client_library")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#id ApiManagementIdentityProviderAadb2C#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password_reset_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#password_reset_policy ApiManagementIdentityProviderAadb2C#password_reset_policy}.'''
        result = self._values.get("password_reset_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def profile_editing_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#profile_editing_policy ApiManagementIdentityProviderAadb2C#profile_editing_policy}.'''
        result = self._values.get("profile_editing_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["ApiManagementIdentityProviderAadb2CTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#timeouts ApiManagementIdentityProviderAadb2C#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ApiManagementIdentityProviderAadb2CTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementIdentityProviderAadb2CConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementIdentityProviderAadb2C.ApiManagementIdentityProviderAadb2CTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class ApiManagementIdentityProviderAadb2CTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#create ApiManagementIdentityProviderAadb2C#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#delete ApiManagementIdentityProviderAadb2C#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#read ApiManagementIdentityProviderAadb2C#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#update ApiManagementIdentityProviderAadb2C#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5210df3c5104de374cfe3e0ed91ad7c67842119e877c19bed03bed1c2bcff12)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#create ApiManagementIdentityProviderAadb2C#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#delete ApiManagementIdentityProviderAadb2C#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#read ApiManagementIdentityProviderAadb2C#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_identity_provider_aadb2c#update ApiManagementIdentityProviderAadb2C#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementIdentityProviderAadb2CTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementIdentityProviderAadb2CTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementIdentityProviderAadb2C.ApiManagementIdentityProviderAadb2CTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f54636aad44ab47d2edc181ef6fba930587792f7b5c9719ee7980d5b0742ebe0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__433a5f428abe6bb1875e771224d012cad5efa361ac684963e98e551a976dc8f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3000da15560c76cca575721e84b65204dbb188813d14fce7d1e71c694daf0de3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea2a0d15965a2c1c6edb0361582c56e7f91d67a161c6b5a5c01b888ec87591d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e807fd6e1491084e5b8e14833787d2676b3ed6d549539933df0ba3d60611555)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementIdentityProviderAadb2CTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementIdentityProviderAadb2CTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementIdentityProviderAadb2CTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__615eb07d7e41f7558f8b77fd2575d7949fad575677de1b50cc6c7d33f19fca50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ApiManagementIdentityProviderAadb2C",
    "ApiManagementIdentityProviderAadb2CConfig",
    "ApiManagementIdentityProviderAadb2CTimeouts",
    "ApiManagementIdentityProviderAadb2CTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__91e08975758c10709e48effa5aa76e9ea18a2147fba4bfdfca18bb90af770abd(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    allowed_tenant: builtins.str,
    api_management_name: builtins.str,
    authority: builtins.str,
    client_id: builtins.str,
    client_secret: builtins.str,
    resource_group_name: builtins.str,
    signin_policy: builtins.str,
    signin_tenant: builtins.str,
    signup_policy: builtins.str,
    client_library: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    password_reset_policy: typing.Optional[builtins.str] = None,
    profile_editing_policy: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ApiManagementIdentityProviderAadb2CTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__0c96f6fe4e8d51a6492b285ea4ca7accf48f9ef8b2d2ed9aec396f4b9ca168c6(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__495610938de513653425291f5bfc68fc99a94a90e9c6dfd98c68b42f1e165955(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abd03d222fa3e23c3d7e26a52b003e242e8f0c85ccd78c770145c71de630231c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cb509b6a38927afb8a98dfdd605e5015c6756857cd3e2d457029ba0b4dd77a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbb0e76414b93612ef34a96681123303f543f22e49c6f41fa1334655642b0f4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d44e1c03078cf81089239bcf1ea48239bdf59f3ab8b5a3057e9daf13f423aa1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4de9b5d247254d5c6dbbd53632ead1a37f19320171cf12df4505fe623016f4ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ead68c63225727d642f14298639344926f56717478cefd0f521cb8440c665eb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9685c1c06f8157a65b85d92448a4c8f0f9363dca81011d18d8879e7ed8d03c26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a8330a51c6ef9b1761f206dbfca11822df558f18b3515e295fc857a623ee189(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9381286e2f49f8770ed371339ce160d94c09be67530f6122243339f1df525ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b06f1eed2d9d3f7dff22565072f59cd9503155453bf1f35558d786bfb875466d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37e8e5f87275d37c5ce13c23d1a063ce5da336b881176aa212d547cdfeab211f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a337200a8090457669a653a7f5f7220d936f1faa409066da35a874aab978028(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13ae92988959d79ee3b2fa27d762ce3ce656be847d2d3aa6ae42467c6cf17f54(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    allowed_tenant: builtins.str,
    api_management_name: builtins.str,
    authority: builtins.str,
    client_id: builtins.str,
    client_secret: builtins.str,
    resource_group_name: builtins.str,
    signin_policy: builtins.str,
    signin_tenant: builtins.str,
    signup_policy: builtins.str,
    client_library: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    password_reset_policy: typing.Optional[builtins.str] = None,
    profile_editing_policy: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ApiManagementIdentityProviderAadb2CTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5210df3c5104de374cfe3e0ed91ad7c67842119e877c19bed03bed1c2bcff12(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f54636aad44ab47d2edc181ef6fba930587792f7b5c9719ee7980d5b0742ebe0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__433a5f428abe6bb1875e771224d012cad5efa361ac684963e98e551a976dc8f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3000da15560c76cca575721e84b65204dbb188813d14fce7d1e71c694daf0de3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea2a0d15965a2c1c6edb0361582c56e7f91d67a161c6b5a5c01b888ec87591d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e807fd6e1491084e5b8e14833787d2676b3ed6d549539933df0ba3d60611555(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__615eb07d7e41f7558f8b77fd2575d7949fad575677de1b50cc6c7d33f19fca50(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementIdentityProviderAadb2CTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
