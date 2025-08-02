r'''
# `opentelekomcloud_kms_key_v1`

Refer to the Terraform Registry for docs: [`opentelekomcloud_kms_key_v1`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1).
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


class KmsKeyV1(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.kmsKeyV1.KmsKeyV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1 opentelekomcloud_kms_key_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        key_alias: builtins.str,
        allow_cancel_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key_description: typing.Optional[builtins.str] = None,
        origin: typing.Optional[builtins.str] = None,
        pending_days: typing.Optional[builtins.str] = None,
        realm: typing.Optional[builtins.str] = None,
        rotation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rotation_interval: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1 opentelekomcloud_kms_key_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param key_alias: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1#key_alias KmsKeyV1#key_alias}.
        :param allow_cancel_deletion: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1#allow_cancel_deletion KmsKeyV1#allow_cancel_deletion}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1#id KmsKeyV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1#is_enabled KmsKeyV1#is_enabled}.
        :param key_description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1#key_description KmsKeyV1#key_description}.
        :param origin: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1#origin KmsKeyV1#origin}.
        :param pending_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1#pending_days KmsKeyV1#pending_days}.
        :param realm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1#realm KmsKeyV1#realm}.
        :param rotation_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1#rotation_enabled KmsKeyV1#rotation_enabled}.
        :param rotation_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1#rotation_interval KmsKeyV1#rotation_interval}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1#tags KmsKeyV1#tags}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__403daa5ce7d718bd85a0bf9da715e7c73ad4808d206782197e315b35d84d6a03)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = KmsKeyV1Config(
            key_alias=key_alias,
            allow_cancel_deletion=allow_cancel_deletion,
            id=id,
            is_enabled=is_enabled,
            key_description=key_description,
            origin=origin,
            pending_days=pending_days,
            realm=realm,
            rotation_enabled=rotation_enabled,
            rotation_interval=rotation_interval,
            tags=tags,
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
        '''Generates CDKTF code for importing a KmsKeyV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the KmsKeyV1 to import.
        :param import_from_id: The id of the existing KmsKeyV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the KmsKeyV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__760643760ebc882bdd2e01ba763519ac1dbae8a0916b31a26d559320404d119e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAllowCancelDeletion")
    def reset_allow_cancel_deletion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowCancelDeletion", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetKeyDescription")
    def reset_key_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyDescription", []))

    @jsii.member(jsii_name="resetOrigin")
    def reset_origin(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrigin", []))

    @jsii.member(jsii_name="resetPendingDays")
    def reset_pending_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPendingDays", []))

    @jsii.member(jsii_name="resetRealm")
    def reset_realm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRealm", []))

    @jsii.member(jsii_name="resetRotationEnabled")
    def reset_rotation_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRotationEnabled", []))

    @jsii.member(jsii_name="resetRotationInterval")
    def reset_rotation_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRotationInterval", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    @jsii.member(jsii_name="creationDate")
    def creation_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationDate"))

    @builtins.property
    @jsii.member(jsii_name="defaultKeyFlag")
    def default_key_flag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultKeyFlag"))

    @builtins.property
    @jsii.member(jsii_name="domainId")
    def domain_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainId"))

    @builtins.property
    @jsii.member(jsii_name="expirationTime")
    def expiration_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expirationTime"))

    @builtins.property
    @jsii.member(jsii_name="keyState")
    def key_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyState"))

    @builtins.property
    @jsii.member(jsii_name="rotationNumber")
    def rotation_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rotationNumber"))

    @builtins.property
    @jsii.member(jsii_name="scheduledDeletionDate")
    def scheduled_deletion_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scheduledDeletionDate"))

    @builtins.property
    @jsii.member(jsii_name="allowCancelDeletionInput")
    def allow_cancel_deletion_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowCancelDeletionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="keyAliasInput")
    def key_alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyAliasInput"))

    @builtins.property
    @jsii.member(jsii_name="keyDescriptionInput")
    def key_description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyDescriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="originInput")
    def origin_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "originInput"))

    @builtins.property
    @jsii.member(jsii_name="pendingDaysInput")
    def pending_days_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pendingDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="realmInput")
    def realm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "realmInput"))

    @builtins.property
    @jsii.member(jsii_name="rotationEnabledInput")
    def rotation_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "rotationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="rotationIntervalInput")
    def rotation_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rotationIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowCancelDeletion")
    def allow_cancel_deletion(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowCancelDeletion"))

    @allow_cancel_deletion.setter
    def allow_cancel_deletion(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8af080c2383212f54ecb20f32c95ef3b1c0d03d00dbe2a7fe81620d64c75d607)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowCancelDeletion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71928ed3fcc42947412b303c34482e9f82c46397abc6e50935e284309b78bf5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3a7827eed1f7eba54113d8e5b13870c8a9ddebf10a7a9568f3ccb9a305c2090)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyAlias")
    def key_alias(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyAlias"))

    @key_alias.setter
    def key_alias(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95f3457fdd1e88026e6c3def2d438348ecd0d84ae3ea2a18d50b5bbe028a5de8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyAlias", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyDescription")
    def key_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyDescription"))

    @key_description.setter
    def key_description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c32a590cf895e79b22adc66a236086918dba52cac2889afe4e5929729e16f24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyDescription", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="origin")
    def origin(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "origin"))

    @origin.setter
    def origin(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c9a3cfda268126a053527f16409817ee0efcee286fdbbdb1870d33ebcc2486a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "origin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pendingDays")
    def pending_days(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pendingDays"))

    @pending_days.setter
    def pending_days(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__086f8d0497b8d0cdb0f8273984165f4d2de2f23f16c92846347b54d3eba706d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pendingDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="realm")
    def realm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "realm"))

    @realm.setter
    def realm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a43270c39534c6929f4f291d8479b77848cf34e550e965fdd3885387bf728c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "realm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rotationEnabled")
    def rotation_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "rotationEnabled"))

    @rotation_enabled.setter
    def rotation_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57697377afedadafc1cedfa46404947e6800e7376ca1c45ce422d1ce294bfd21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rotationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rotationInterval")
    def rotation_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rotationInterval"))

    @rotation_interval.setter
    def rotation_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__900bdae070c117c4c358af328c5ca07a0393a00adc1d78151ec4653f1cdb084d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rotationInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31717a0e28beaec96870772b52e55bf5fae61f6b0bda66d87436457aab558421)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.kmsKeyV1.KmsKeyV1Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "key_alias": "keyAlias",
        "allow_cancel_deletion": "allowCancelDeletion",
        "id": "id",
        "is_enabled": "isEnabled",
        "key_description": "keyDescription",
        "origin": "origin",
        "pending_days": "pendingDays",
        "realm": "realm",
        "rotation_enabled": "rotationEnabled",
        "rotation_interval": "rotationInterval",
        "tags": "tags",
    },
)
class KmsKeyV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        key_alias: builtins.str,
        allow_cancel_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key_description: typing.Optional[builtins.str] = None,
        origin: typing.Optional[builtins.str] = None,
        pending_days: typing.Optional[builtins.str] = None,
        realm: typing.Optional[builtins.str] = None,
        rotation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rotation_interval: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param key_alias: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1#key_alias KmsKeyV1#key_alias}.
        :param allow_cancel_deletion: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1#allow_cancel_deletion KmsKeyV1#allow_cancel_deletion}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1#id KmsKeyV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1#is_enabled KmsKeyV1#is_enabled}.
        :param key_description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1#key_description KmsKeyV1#key_description}.
        :param origin: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1#origin KmsKeyV1#origin}.
        :param pending_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1#pending_days KmsKeyV1#pending_days}.
        :param realm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1#realm KmsKeyV1#realm}.
        :param rotation_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1#rotation_enabled KmsKeyV1#rotation_enabled}.
        :param rotation_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1#rotation_interval KmsKeyV1#rotation_interval}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1#tags KmsKeyV1#tags}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aeae3f512eab3a9acce6696fe011703ebb8747a711a4ca5d6df1d2ebb4d20bd)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument key_alias", value=key_alias, expected_type=type_hints["key_alias"])
            check_type(argname="argument allow_cancel_deletion", value=allow_cancel_deletion, expected_type=type_hints["allow_cancel_deletion"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument key_description", value=key_description, expected_type=type_hints["key_description"])
            check_type(argname="argument origin", value=origin, expected_type=type_hints["origin"])
            check_type(argname="argument pending_days", value=pending_days, expected_type=type_hints["pending_days"])
            check_type(argname="argument realm", value=realm, expected_type=type_hints["realm"])
            check_type(argname="argument rotation_enabled", value=rotation_enabled, expected_type=type_hints["rotation_enabled"])
            check_type(argname="argument rotation_interval", value=rotation_interval, expected_type=type_hints["rotation_interval"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key_alias": key_alias,
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
        if allow_cancel_deletion is not None:
            self._values["allow_cancel_deletion"] = allow_cancel_deletion
        if id is not None:
            self._values["id"] = id
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if key_description is not None:
            self._values["key_description"] = key_description
        if origin is not None:
            self._values["origin"] = origin
        if pending_days is not None:
            self._values["pending_days"] = pending_days
        if realm is not None:
            self._values["realm"] = realm
        if rotation_enabled is not None:
            self._values["rotation_enabled"] = rotation_enabled
        if rotation_interval is not None:
            self._values["rotation_interval"] = rotation_interval
        if tags is not None:
            self._values["tags"] = tags

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
    def key_alias(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1#key_alias KmsKeyV1#key_alias}.'''
        result = self._values.get("key_alias")
        assert result is not None, "Required property 'key_alias' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_cancel_deletion(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1#allow_cancel_deletion KmsKeyV1#allow_cancel_deletion}.'''
        result = self._values.get("allow_cancel_deletion")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1#id KmsKeyV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1#is_enabled KmsKeyV1#is_enabled}.'''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key_description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1#key_description KmsKeyV1#key_description}.'''
        result = self._values.get("key_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def origin(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1#origin KmsKeyV1#origin}.'''
        result = self._values.get("origin")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pending_days(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1#pending_days KmsKeyV1#pending_days}.'''
        result = self._values.get("pending_days")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def realm(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1#realm KmsKeyV1#realm}.'''
        result = self._values.get("realm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rotation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1#rotation_enabled KmsKeyV1#rotation_enabled}.'''
        result = self._values.get("rotation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def rotation_interval(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1#rotation_interval KmsKeyV1#rotation_interval}.'''
        result = self._values.get("rotation_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/kms_key_v1#tags KmsKeyV1#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KmsKeyV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "KmsKeyV1",
    "KmsKeyV1Config",
]

publication.publish()

def _typecheckingstub__403daa5ce7d718bd85a0bf9da715e7c73ad4808d206782197e315b35d84d6a03(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    key_alias: builtins.str,
    allow_cancel_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key_description: typing.Optional[builtins.str] = None,
    origin: typing.Optional[builtins.str] = None,
    pending_days: typing.Optional[builtins.str] = None,
    realm: typing.Optional[builtins.str] = None,
    rotation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    rotation_interval: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__760643760ebc882bdd2e01ba763519ac1dbae8a0916b31a26d559320404d119e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8af080c2383212f54ecb20f32c95ef3b1c0d03d00dbe2a7fe81620d64c75d607(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71928ed3fcc42947412b303c34482e9f82c46397abc6e50935e284309b78bf5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3a7827eed1f7eba54113d8e5b13870c8a9ddebf10a7a9568f3ccb9a305c2090(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95f3457fdd1e88026e6c3def2d438348ecd0d84ae3ea2a18d50b5bbe028a5de8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c32a590cf895e79b22adc66a236086918dba52cac2889afe4e5929729e16f24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c9a3cfda268126a053527f16409817ee0efcee286fdbbdb1870d33ebcc2486a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__086f8d0497b8d0cdb0f8273984165f4d2de2f23f16c92846347b54d3eba706d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a43270c39534c6929f4f291d8479b77848cf34e550e965fdd3885387bf728c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57697377afedadafc1cedfa46404947e6800e7376ca1c45ce422d1ce294bfd21(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__900bdae070c117c4c358af328c5ca07a0393a00adc1d78151ec4653f1cdb084d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31717a0e28beaec96870772b52e55bf5fae61f6b0bda66d87436457aab558421(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aeae3f512eab3a9acce6696fe011703ebb8747a711a4ca5d6df1d2ebb4d20bd(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    key_alias: builtins.str,
    allow_cancel_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key_description: typing.Optional[builtins.str] = None,
    origin: typing.Optional[builtins.str] = None,
    pending_days: typing.Optional[builtins.str] = None,
    realm: typing.Optional[builtins.str] = None,
    rotation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    rotation_interval: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
