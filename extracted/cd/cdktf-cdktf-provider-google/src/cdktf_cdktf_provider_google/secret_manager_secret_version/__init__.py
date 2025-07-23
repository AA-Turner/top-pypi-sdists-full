r'''
# `google_secret_manager_secret_version`

Refer to the Terraform Registry for docs: [`google_secret_manager_secret_version`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version).
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


class SecretManagerSecretVersion(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.secretManagerSecretVersion.SecretManagerSecretVersion",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version google_secret_manager_secret_version}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        secret: builtins.str,
        deletion_policy: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        is_secret_data_base64: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secret_data: typing.Optional[builtins.str] = None,
        secret_data_wo: typing.Optional[builtins.str] = None,
        secret_data_wo_version: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["SecretManagerSecretVersionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version google_secret_manager_secret_version} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param secret: Secret Manager secret resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#secret SecretManagerSecretVersion#secret}
        :param deletion_policy: The deletion policy for the secret version. Setting 'ABANDON' allows the resource to be abandoned rather than deleted. Setting 'DISABLE' allows the resource to be disabled rather than deleted. Default is 'DELETE'. Possible values are: - DELETE - DISABLE - ABANDON Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#deletion_policy SecretManagerSecretVersion#deletion_policy}
        :param enabled: The current state of the SecretVersion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#enabled SecretManagerSecretVersion#enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#id SecretManagerSecretVersion#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_secret_data_base64: If set to 'true', the secret data is expected to be base64-encoded string and would be sent as is. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#is_secret_data_base64 SecretManagerSecretVersion#is_secret_data_base64}
        :param secret_data: The secret data. Must be no larger than 64KiB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#secret_data SecretManagerSecretVersion#secret_data}
        :param secret_data_wo: The secret data. Must be no larger than 64KiB. For more info see `updating write-only attributes </docs/providers/google/guides/using_write_only_attributes.html#updating-write-only-attributes>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#secret_data_wo SecretManagerSecretVersion#secret_data_wo}
        :param secret_data_wo_version: Triggers update of secret data write-only. For more info see `updating write-only attributes </docs/providers/google/guides/using_write_only_attributes.html#updating-write-only-attributes>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#secret_data_wo_version SecretManagerSecretVersion#secret_data_wo_version}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#timeouts SecretManagerSecretVersion#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b36ba14bcb3b47a0bbcb107e10f724c54cdb2a06e83173e28784bd4747d0310)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SecretManagerSecretVersionConfig(
            secret=secret,
            deletion_policy=deletion_policy,
            enabled=enabled,
            id=id,
            is_secret_data_base64=is_secret_data_base64,
            secret_data=secret_data,
            secret_data_wo=secret_data_wo,
            secret_data_wo_version=secret_data_wo_version,
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
        '''Generates CDKTF code for importing a SecretManagerSecretVersion resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SecretManagerSecretVersion to import.
        :param import_from_id: The id of the existing SecretManagerSecretVersion that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SecretManagerSecretVersion to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b0183f825caae42a0733c0bf276f45ec733cda3884b1f8e31dbb4e756e35a62)
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
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#create SecretManagerSecretVersion#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#delete SecretManagerSecretVersion#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#update SecretManagerSecretVersion#update}.
        '''
        value = SecretManagerSecretVersionTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDeletionPolicy")
    def reset_deletion_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionPolicy", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIsSecretDataBase64")
    def reset_is_secret_data_base64(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsSecretDataBase64", []))

    @jsii.member(jsii_name="resetSecretData")
    def reset_secret_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretData", []))

    @jsii.member(jsii_name="resetSecretDataWo")
    def reset_secret_data_wo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretDataWo", []))

    @jsii.member(jsii_name="resetSecretDataWoVersion")
    def reset_secret_data_wo_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretDataWoVersion", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="destroyTime")
    def destroy_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destroyTime"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "SecretManagerSecretVersionTimeoutsOutputReference":
        return typing.cast("SecretManagerSecretVersionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="deletionPolicyInput")
    def deletion_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deletionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="isSecretDataBase64Input")
    def is_secret_data_base64_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isSecretDataBase64Input"))

    @builtins.property
    @jsii.member(jsii_name="secretDataInput")
    def secret_data_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretDataInput"))

    @builtins.property
    @jsii.member(jsii_name="secretDataWoInput")
    def secret_data_wo_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretDataWoInput"))

    @builtins.property
    @jsii.member(jsii_name="secretDataWoVersionInput")
    def secret_data_wo_version_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "secretDataWoVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="secretInput")
    def secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SecretManagerSecretVersionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SecretManagerSecretVersionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionPolicy")
    def deletion_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deletionPolicy"))

    @deletion_policy.setter
    def deletion_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec7a191e98f78c5e3468b8d093d816eba1c2af01848a298929714ef38355adaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__398b140943e2be240ea3acd40fe85303cf6399c445450ae021b7b0be21de876c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55095c7a6f8011213df61c76ffcf126a8d9db9c1b66cc561f416d63c5f3ab005)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isSecretDataBase64")
    def is_secret_data_base64(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isSecretDataBase64"))

    @is_secret_data_base64.setter
    def is_secret_data_base64(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a1edf8c31c46ed1be8fb70f1ab6431c4c1cf5a8ef119cc7c09d1b110bcd54d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSecretDataBase64", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secret"))

    @secret.setter
    def secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2006ca17382f084feb846d4e5b384bb1b2085ea2def518c6ab997771849a5501)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretData")
    def secret_data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretData"))

    @secret_data.setter
    def secret_data(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__644d26b758187e30456f6e4ddc15e521c68fdcf540b5d19785be520af9414753)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretData", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretDataWo")
    def secret_data_wo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretDataWo"))

    @secret_data_wo.setter
    def secret_data_wo(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1a1b2b7dd266cd2c5fead203340823a11197e7bfc558763143eab6bf8747e39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretDataWo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretDataWoVersion")
    def secret_data_wo_version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "secretDataWoVersion"))

    @secret_data_wo_version.setter
    def secret_data_wo_version(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5a004119bf20b89a3373f2fb98f065b8243f57cad574007b1e36c3305b16383)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretDataWoVersion", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.secretManagerSecretVersion.SecretManagerSecretVersionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "secret": "secret",
        "deletion_policy": "deletionPolicy",
        "enabled": "enabled",
        "id": "id",
        "is_secret_data_base64": "isSecretDataBase64",
        "secret_data": "secretData",
        "secret_data_wo": "secretDataWo",
        "secret_data_wo_version": "secretDataWoVersion",
        "timeouts": "timeouts",
    },
)
class SecretManagerSecretVersionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        secret: builtins.str,
        deletion_policy: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        is_secret_data_base64: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secret_data: typing.Optional[builtins.str] = None,
        secret_data_wo: typing.Optional[builtins.str] = None,
        secret_data_wo_version: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["SecretManagerSecretVersionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param secret: Secret Manager secret resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#secret SecretManagerSecretVersion#secret}
        :param deletion_policy: The deletion policy for the secret version. Setting 'ABANDON' allows the resource to be abandoned rather than deleted. Setting 'DISABLE' allows the resource to be disabled rather than deleted. Default is 'DELETE'. Possible values are: - DELETE - DISABLE - ABANDON Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#deletion_policy SecretManagerSecretVersion#deletion_policy}
        :param enabled: The current state of the SecretVersion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#enabled SecretManagerSecretVersion#enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#id SecretManagerSecretVersion#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_secret_data_base64: If set to 'true', the secret data is expected to be base64-encoded string and would be sent as is. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#is_secret_data_base64 SecretManagerSecretVersion#is_secret_data_base64}
        :param secret_data: The secret data. Must be no larger than 64KiB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#secret_data SecretManagerSecretVersion#secret_data}
        :param secret_data_wo: The secret data. Must be no larger than 64KiB. For more info see `updating write-only attributes </docs/providers/google/guides/using_write_only_attributes.html#updating-write-only-attributes>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#secret_data_wo SecretManagerSecretVersion#secret_data_wo}
        :param secret_data_wo_version: Triggers update of secret data write-only. For more info see `updating write-only attributes </docs/providers/google/guides/using_write_only_attributes.html#updating-write-only-attributes>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#secret_data_wo_version SecretManagerSecretVersion#secret_data_wo_version}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#timeouts SecretManagerSecretVersion#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = SecretManagerSecretVersionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18cf6db57bf8267a9f49618b0e8871f94dca98374b5df500b21da49cdda78db1)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
            check_type(argname="argument deletion_policy", value=deletion_policy, expected_type=type_hints["deletion_policy"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument is_secret_data_base64", value=is_secret_data_base64, expected_type=type_hints["is_secret_data_base64"])
            check_type(argname="argument secret_data", value=secret_data, expected_type=type_hints["secret_data"])
            check_type(argname="argument secret_data_wo", value=secret_data_wo, expected_type=type_hints["secret_data_wo"])
            check_type(argname="argument secret_data_wo_version", value=secret_data_wo_version, expected_type=type_hints["secret_data_wo_version"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret": secret,
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
        if deletion_policy is not None:
            self._values["deletion_policy"] = deletion_policy
        if enabled is not None:
            self._values["enabled"] = enabled
        if id is not None:
            self._values["id"] = id
        if is_secret_data_base64 is not None:
            self._values["is_secret_data_base64"] = is_secret_data_base64
        if secret_data is not None:
            self._values["secret_data"] = secret_data
        if secret_data_wo is not None:
            self._values["secret_data_wo"] = secret_data_wo
        if secret_data_wo_version is not None:
            self._values["secret_data_wo_version"] = secret_data_wo_version
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
    def secret(self) -> builtins.str:
        '''Secret Manager secret resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#secret SecretManagerSecretVersion#secret}
        '''
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deletion_policy(self) -> typing.Optional[builtins.str]:
        '''The deletion policy for the secret version.

        Setting 'ABANDON' allows the resource
        to be abandoned rather than deleted. Setting 'DISABLE' allows the resource to be
        disabled rather than deleted. Default is 'DELETE'. Possible values are:

        - DELETE
        - DISABLE
        - ABANDON

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#deletion_policy SecretManagerSecretVersion#deletion_policy}
        '''
        result = self._values.get("deletion_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The current state of the SecretVersion.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#enabled SecretManagerSecretVersion#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#id SecretManagerSecretVersion#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_secret_data_base64(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to 'true', the secret data is expected to be base64-encoded string and would be sent as is.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#is_secret_data_base64 SecretManagerSecretVersion#is_secret_data_base64}
        '''
        result = self._values.get("is_secret_data_base64")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def secret_data(self) -> typing.Optional[builtins.str]:
        '''The secret data. Must be no larger than 64KiB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#secret_data SecretManagerSecretVersion#secret_data}
        '''
        result = self._values.get("secret_data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_data_wo(self) -> typing.Optional[builtins.str]:
        '''The secret data. Must be no larger than 64KiB. For more info see `updating write-only attributes </docs/providers/google/guides/using_write_only_attributes.html#updating-write-only-attributes>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#secret_data_wo SecretManagerSecretVersion#secret_data_wo}
        '''
        result = self._values.get("secret_data_wo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_data_wo_version(self) -> typing.Optional[jsii.Number]:
        '''Triggers update of secret data write-only. For more info see `updating write-only attributes </docs/providers/google/guides/using_write_only_attributes.html#updating-write-only-attributes>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#secret_data_wo_version SecretManagerSecretVersion#secret_data_wo_version}
        '''
        result = self._values.get("secret_data_wo_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["SecretManagerSecretVersionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#timeouts SecretManagerSecretVersion#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["SecretManagerSecretVersionTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretManagerSecretVersionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.secretManagerSecretVersion.SecretManagerSecretVersionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class SecretManagerSecretVersionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#create SecretManagerSecretVersion#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#delete SecretManagerSecretVersion#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#update SecretManagerSecretVersion#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8d4208af16049c0abc7856b6dda5beacdbd04406b5103127f6421ddf5aafdea)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#create SecretManagerSecretVersion#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#delete SecretManagerSecretVersion#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secret_manager_secret_version#update SecretManagerSecretVersion#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretManagerSecretVersionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecretManagerSecretVersionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.secretManagerSecretVersion.SecretManagerSecretVersionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__249d74f77e7aadf0bbe1ff18c821a8b2424ded2b97723328267b6de57d0f5962)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cce56a38b72fe7dd4de4fa38944b03069765083539d08832ffc9e208adca5714)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__798b7d04b40ded8ba1ec5c45be7480e2bfd198d240924f316e27c7a921d4dfe2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e8bc57410fb4247e6e7e114688c3e81339630da21eef48976f9695bcd8b7b63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecretManagerSecretVersionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecretManagerSecretVersionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecretManagerSecretVersionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd443860827b2c787d6dfe9dc63b71c63fa06d3bc34c8487285a06fa9a098e02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SecretManagerSecretVersion",
    "SecretManagerSecretVersionConfig",
    "SecretManagerSecretVersionTimeouts",
    "SecretManagerSecretVersionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__9b36ba14bcb3b47a0bbcb107e10f724c54cdb2a06e83173e28784bd4747d0310(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    secret: builtins.str,
    deletion_policy: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    is_secret_data_base64: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    secret_data: typing.Optional[builtins.str] = None,
    secret_data_wo: typing.Optional[builtins.str] = None,
    secret_data_wo_version: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[SecretManagerSecretVersionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__3b0183f825caae42a0733c0bf276f45ec733cda3884b1f8e31dbb4e756e35a62(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec7a191e98f78c5e3468b8d093d816eba1c2af01848a298929714ef38355adaf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__398b140943e2be240ea3acd40fe85303cf6399c445450ae021b7b0be21de876c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55095c7a6f8011213df61c76ffcf126a8d9db9c1b66cc561f416d63c5f3ab005(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a1edf8c31c46ed1be8fb70f1ab6431c4c1cf5a8ef119cc7c09d1b110bcd54d8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2006ca17382f084feb846d4e5b384bb1b2085ea2def518c6ab997771849a5501(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__644d26b758187e30456f6e4ddc15e521c68fdcf540b5d19785be520af9414753(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1a1b2b7dd266cd2c5fead203340823a11197e7bfc558763143eab6bf8747e39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5a004119bf20b89a3373f2fb98f065b8243f57cad574007b1e36c3305b16383(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18cf6db57bf8267a9f49618b0e8871f94dca98374b5df500b21da49cdda78db1(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    secret: builtins.str,
    deletion_policy: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    is_secret_data_base64: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    secret_data: typing.Optional[builtins.str] = None,
    secret_data_wo: typing.Optional[builtins.str] = None,
    secret_data_wo_version: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[SecretManagerSecretVersionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8d4208af16049c0abc7856b6dda5beacdbd04406b5103127f6421ddf5aafdea(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__249d74f77e7aadf0bbe1ff18c821a8b2424ded2b97723328267b6de57d0f5962(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cce56a38b72fe7dd4de4fa38944b03069765083539d08832ffc9e208adca5714(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__798b7d04b40ded8ba1ec5c45be7480e2bfd198d240924f316e27c7a921d4dfe2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e8bc57410fb4247e6e7e114688c3e81339630da21eef48976f9695bcd8b7b63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd443860827b2c787d6dfe9dc63b71c63fa06d3bc34c8487285a06fa9a098e02(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecretManagerSecretVersionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
