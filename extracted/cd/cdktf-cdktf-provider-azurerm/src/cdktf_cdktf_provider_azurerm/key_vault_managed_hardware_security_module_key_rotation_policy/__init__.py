r'''
# `azurerm_key_vault_managed_hardware_security_module_key_rotation_policy`

Refer to the Terraform Registry for docs: [`azurerm_key_vault_managed_hardware_security_module_key_rotation_policy`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_managed_hardware_security_module_key_rotation_policy).
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


class KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.keyVaultManagedHardwareSecurityModuleKeyRotationPolicy.KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_managed_hardware_security_module_key_rotation_policy azurerm_key_vault_managed_hardware_security_module_key_rotation_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        expire_after: builtins.str,
        managed_hsm_key_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        time_after_creation: typing.Optional[builtins.str] = None,
        time_before_expiry: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["KeyVaultManagedHardwareSecurityModuleKeyRotationPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_managed_hardware_security_module_key_rotation_policy azurerm_key_vault_managed_hardware_security_module_key_rotation_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param expire_after: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_managed_hardware_security_module_key_rotation_policy#expire_after KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy#expire_after}.
        :param managed_hsm_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_managed_hardware_security_module_key_rotation_policy#managed_hsm_key_id KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy#managed_hsm_key_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_managed_hardware_security_module_key_rotation_policy#id KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param time_after_creation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_managed_hardware_security_module_key_rotation_policy#time_after_creation KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy#time_after_creation}.
        :param time_before_expiry: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_managed_hardware_security_module_key_rotation_policy#time_before_expiry KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy#time_before_expiry}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_managed_hardware_security_module_key_rotation_policy#timeouts KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__600acf206520603e61611b57c57b069b8762d3f48f9277103d66b95a948af6be)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = KeyVaultManagedHardwareSecurityModuleKeyRotationPolicyConfig(
            expire_after=expire_after,
            managed_hsm_key_id=managed_hsm_key_id,
            id=id,
            time_after_creation=time_after_creation,
            time_before_expiry=time_before_expiry,
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
        '''Generates CDKTF code for importing a KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy to import.
        :param import_from_id: The id of the existing KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_managed_hardware_security_module_key_rotation_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68a48c3844c8fb048386b2664e1fd1b580560f09b60434c0ac2b3b986b2863d4)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_managed_hardware_security_module_key_rotation_policy#create KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_managed_hardware_security_module_key_rotation_policy#delete KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_managed_hardware_security_module_key_rotation_policy#read KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_managed_hardware_security_module_key_rotation_policy#update KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy#update}.
        '''
        value = KeyVaultManagedHardwareSecurityModuleKeyRotationPolicyTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetTimeAfterCreation")
    def reset_time_after_creation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeAfterCreation", []))

    @jsii.member(jsii_name="resetTimeBeforeExpiry")
    def reset_time_before_expiry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeBeforeExpiry", []))

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
    def timeouts(
        self,
    ) -> "KeyVaultManagedHardwareSecurityModuleKeyRotationPolicyTimeoutsOutputReference":
        return typing.cast("KeyVaultManagedHardwareSecurityModuleKeyRotationPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="expireAfterInput")
    def expire_after_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expireAfterInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="managedHsmKeyIdInput")
    def managed_hsm_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managedHsmKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeAfterCreationInput")
    def time_after_creation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeAfterCreationInput"))

    @builtins.property
    @jsii.member(jsii_name="timeBeforeExpiryInput")
    def time_before_expiry_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeBeforeExpiryInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "KeyVaultManagedHardwareSecurityModuleKeyRotationPolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "KeyVaultManagedHardwareSecurityModuleKeyRotationPolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="expireAfter")
    def expire_after(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expireAfter"))

    @expire_after.setter
    def expire_after(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbba426c3afed74f83d788643c7047b90acaed12a072ed1120981588036681d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expireAfter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b46135770a21c0c40523aeefb3f9ba962314b8acf704b2fcd4c389fd835001b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="managedHsmKeyId")
    def managed_hsm_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managedHsmKeyId"))

    @managed_hsm_key_id.setter
    def managed_hsm_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c309f8742fbf5af4c6f1b82f8444a094fda3490e10b0fbc1ab697fd333fc9cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedHsmKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeAfterCreation")
    def time_after_creation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeAfterCreation"))

    @time_after_creation.setter
    def time_after_creation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e613ff33d9d7b8900fcb892bfefe28d41bd829f35d0a4e77e0f0c31481a5969)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeAfterCreation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeBeforeExpiry")
    def time_before_expiry(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeBeforeExpiry"))

    @time_before_expiry.setter
    def time_before_expiry(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3125733a672c07452486cab4ccf882f5915b2e3001a719003f2307d15d7b550)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeBeforeExpiry", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.keyVaultManagedHardwareSecurityModuleKeyRotationPolicy.KeyVaultManagedHardwareSecurityModuleKeyRotationPolicyConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "expire_after": "expireAfter",
        "managed_hsm_key_id": "managedHsmKeyId",
        "id": "id",
        "time_after_creation": "timeAfterCreation",
        "time_before_expiry": "timeBeforeExpiry",
        "timeouts": "timeouts",
    },
)
class KeyVaultManagedHardwareSecurityModuleKeyRotationPolicyConfig(
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
        expire_after: builtins.str,
        managed_hsm_key_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        time_after_creation: typing.Optional[builtins.str] = None,
        time_before_expiry: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["KeyVaultManagedHardwareSecurityModuleKeyRotationPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param expire_after: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_managed_hardware_security_module_key_rotation_policy#expire_after KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy#expire_after}.
        :param managed_hsm_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_managed_hardware_security_module_key_rotation_policy#managed_hsm_key_id KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy#managed_hsm_key_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_managed_hardware_security_module_key_rotation_policy#id KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param time_after_creation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_managed_hardware_security_module_key_rotation_policy#time_after_creation KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy#time_after_creation}.
        :param time_before_expiry: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_managed_hardware_security_module_key_rotation_policy#time_before_expiry KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy#time_before_expiry}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_managed_hardware_security_module_key_rotation_policy#timeouts KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = KeyVaultManagedHardwareSecurityModuleKeyRotationPolicyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d455918ea463241fbe9ca8c254947794448e973a9f073d6d154eb977369e0eb5)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument expire_after", value=expire_after, expected_type=type_hints["expire_after"])
            check_type(argname="argument managed_hsm_key_id", value=managed_hsm_key_id, expected_type=type_hints["managed_hsm_key_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument time_after_creation", value=time_after_creation, expected_type=type_hints["time_after_creation"])
            check_type(argname="argument time_before_expiry", value=time_before_expiry, expected_type=type_hints["time_before_expiry"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "expire_after": expire_after,
            "managed_hsm_key_id": managed_hsm_key_id,
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
        if id is not None:
            self._values["id"] = id
        if time_after_creation is not None:
            self._values["time_after_creation"] = time_after_creation
        if time_before_expiry is not None:
            self._values["time_before_expiry"] = time_before_expiry
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
    def expire_after(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_managed_hardware_security_module_key_rotation_policy#expire_after KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy#expire_after}.'''
        result = self._values.get("expire_after")
        assert result is not None, "Required property 'expire_after' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def managed_hsm_key_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_managed_hardware_security_module_key_rotation_policy#managed_hsm_key_id KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy#managed_hsm_key_id}.'''
        result = self._values.get("managed_hsm_key_id")
        assert result is not None, "Required property 'managed_hsm_key_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_managed_hardware_security_module_key_rotation_policy#id KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_after_creation(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_managed_hardware_security_module_key_rotation_policy#time_after_creation KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy#time_after_creation}.'''
        result = self._values.get("time_after_creation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_before_expiry(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_managed_hardware_security_module_key_rotation_policy#time_before_expiry KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy#time_before_expiry}.'''
        result = self._values.get("time_before_expiry")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["KeyVaultManagedHardwareSecurityModuleKeyRotationPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_managed_hardware_security_module_key_rotation_policy#timeouts KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["KeyVaultManagedHardwareSecurityModuleKeyRotationPolicyTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyVaultManagedHardwareSecurityModuleKeyRotationPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.keyVaultManagedHardwareSecurityModuleKeyRotationPolicy.KeyVaultManagedHardwareSecurityModuleKeyRotationPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class KeyVaultManagedHardwareSecurityModuleKeyRotationPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_managed_hardware_security_module_key_rotation_policy#create KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_managed_hardware_security_module_key_rotation_policy#delete KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_managed_hardware_security_module_key_rotation_policy#read KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_managed_hardware_security_module_key_rotation_policy#update KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__247d44448256bf0e3b487898aefd76c15ce203226bf6010bfe537a556705b27b)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_managed_hardware_security_module_key_rotation_policy#create KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_managed_hardware_security_module_key_rotation_policy#delete KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_managed_hardware_security_module_key_rotation_policy#read KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/key_vault_managed_hardware_security_module_key_rotation_policy#update KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyVaultManagedHardwareSecurityModuleKeyRotationPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KeyVaultManagedHardwareSecurityModuleKeyRotationPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.keyVaultManagedHardwareSecurityModuleKeyRotationPolicy.KeyVaultManagedHardwareSecurityModuleKeyRotationPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff51b0c038f5b2bb2fe79523e81b16ddc7dfe6570424d0ab6cf9c8add1cfe657)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a12dc09766f1a54d08a084e4bc5b1d97c73935c3286f1915cac7b31bd22ea374)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8db2e90767ef6e3617e0bb95f43d23fe4d6aec50754d2d38a1e63d601ec22d5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26dc60a2556303502fb6a7df45d86ed48665c26216ec03cbbeed7275fce30f90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6793a4c1cd73b1e843e10c1692990c1f265f072b936419342899d4583c0922cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KeyVaultManagedHardwareSecurityModuleKeyRotationPolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KeyVaultManagedHardwareSecurityModuleKeyRotationPolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KeyVaultManagedHardwareSecurityModuleKeyRotationPolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5943037373f177a27b826d71bc29a5a7e067fb98166a92a26287fe78745feebc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "KeyVaultManagedHardwareSecurityModuleKeyRotationPolicy",
    "KeyVaultManagedHardwareSecurityModuleKeyRotationPolicyConfig",
    "KeyVaultManagedHardwareSecurityModuleKeyRotationPolicyTimeouts",
    "KeyVaultManagedHardwareSecurityModuleKeyRotationPolicyTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__600acf206520603e61611b57c57b069b8762d3f48f9277103d66b95a948af6be(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    expire_after: builtins.str,
    managed_hsm_key_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    time_after_creation: typing.Optional[builtins.str] = None,
    time_before_expiry: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[KeyVaultManagedHardwareSecurityModuleKeyRotationPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__68a48c3844c8fb048386b2664e1fd1b580560f09b60434c0ac2b3b986b2863d4(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbba426c3afed74f83d788643c7047b90acaed12a072ed1120981588036681d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b46135770a21c0c40523aeefb3f9ba962314b8acf704b2fcd4c389fd835001b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c309f8742fbf5af4c6f1b82f8444a094fda3490e10b0fbc1ab697fd333fc9cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e613ff33d9d7b8900fcb892bfefe28d41bd829f35d0a4e77e0f0c31481a5969(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3125733a672c07452486cab4ccf882f5915b2e3001a719003f2307d15d7b550(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d455918ea463241fbe9ca8c254947794448e973a9f073d6d154eb977369e0eb5(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    expire_after: builtins.str,
    managed_hsm_key_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    time_after_creation: typing.Optional[builtins.str] = None,
    time_before_expiry: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[KeyVaultManagedHardwareSecurityModuleKeyRotationPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__247d44448256bf0e3b487898aefd76c15ce203226bf6010bfe537a556705b27b(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff51b0c038f5b2bb2fe79523e81b16ddc7dfe6570424d0ab6cf9c8add1cfe657(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a12dc09766f1a54d08a084e4bc5b1d97c73935c3286f1915cac7b31bd22ea374(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8db2e90767ef6e3617e0bb95f43d23fe4d6aec50754d2d38a1e63d601ec22d5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26dc60a2556303502fb6a7df45d86ed48665c26216ec03cbbeed7275fce30f90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6793a4c1cd73b1e843e10c1692990c1f265f072b936419342899d4583c0922cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5943037373f177a27b826d71bc29a5a7e067fb98166a92a26287fe78745feebc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KeyVaultManagedHardwareSecurityModuleKeyRotationPolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
