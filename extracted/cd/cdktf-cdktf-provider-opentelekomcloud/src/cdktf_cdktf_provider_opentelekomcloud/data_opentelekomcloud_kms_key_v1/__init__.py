r'''
# `data_opentelekomcloud_kms_key_v1`

Refer to the Terraform Registry for docs: [`data_opentelekomcloud_kms_key_v1`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/kms_key_v1).
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


class DataOpentelekomcloudKmsKeyV1(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudKmsKeyV1.DataOpentelekomcloudKmsKeyV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/kms_key_v1 opentelekomcloud_kms_key_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        default_key_flag: typing.Optional[builtins.str] = None,
        domain_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        key_alias: typing.Optional[builtins.str] = None,
        key_description: typing.Optional[builtins.str] = None,
        key_id: typing.Optional[builtins.str] = None,
        key_state: typing.Optional[builtins.str] = None,
        origin: typing.Optional[builtins.str] = None,
        realm: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/kms_key_v1 opentelekomcloud_kms_key_v1} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param default_key_flag: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/kms_key_v1#default_key_flag DataOpentelekomcloudKmsKeyV1#default_key_flag}.
        :param domain_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/kms_key_v1#domain_id DataOpentelekomcloudKmsKeyV1#domain_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/kms_key_v1#id DataOpentelekomcloudKmsKeyV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param key_alias: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/kms_key_v1#key_alias DataOpentelekomcloudKmsKeyV1#key_alias}.
        :param key_description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/kms_key_v1#key_description DataOpentelekomcloudKmsKeyV1#key_description}.
        :param key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/kms_key_v1#key_id DataOpentelekomcloudKmsKeyV1#key_id}.
        :param key_state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/kms_key_v1#key_state DataOpentelekomcloudKmsKeyV1#key_state}.
        :param origin: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/kms_key_v1#origin DataOpentelekomcloudKmsKeyV1#origin}.
        :param realm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/kms_key_v1#realm DataOpentelekomcloudKmsKeyV1#realm}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c06cfb363e2892a83a6bc372442fbcf209c0dc48af29cce0f9b3e01ac28af28)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataOpentelekomcloudKmsKeyV1Config(
            default_key_flag=default_key_flag,
            domain_id=domain_id,
            id=id,
            key_alias=key_alias,
            key_description=key_description,
            key_id=key_id,
            key_state=key_state,
            origin=origin,
            realm=realm,
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
        '''Generates CDKTF code for importing a DataOpentelekomcloudKmsKeyV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataOpentelekomcloudKmsKeyV1 to import.
        :param import_from_id: The id of the existing DataOpentelekomcloudKmsKeyV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/kms_key_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataOpentelekomcloudKmsKeyV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__812f106ecb4f19ce587a7e76537fefba0adec299155e228bb0d513b87664123d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetDefaultKeyFlag")
    def reset_default_key_flag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultKeyFlag", []))

    @jsii.member(jsii_name="resetDomainId")
    def reset_domain_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomainId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKeyAlias")
    def reset_key_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyAlias", []))

    @jsii.member(jsii_name="resetKeyDescription")
    def reset_key_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyDescription", []))

    @jsii.member(jsii_name="resetKeyId")
    def reset_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyId", []))

    @jsii.member(jsii_name="resetKeyState")
    def reset_key_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyState", []))

    @jsii.member(jsii_name="resetOrigin")
    def reset_origin(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrigin", []))

    @jsii.member(jsii_name="resetRealm")
    def reset_realm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRealm", []))

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
    @jsii.member(jsii_name="expirationTime")
    def expiration_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expirationTime"))

    @builtins.property
    @jsii.member(jsii_name="scheduledDeletionDate")
    def scheduled_deletion_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scheduledDeletionDate"))

    @builtins.property
    @jsii.member(jsii_name="defaultKeyFlagInput")
    def default_key_flag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultKeyFlagInput"))

    @builtins.property
    @jsii.member(jsii_name="domainIdInput")
    def domain_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="keyAliasInput")
    def key_alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyAliasInput"))

    @builtins.property
    @jsii.member(jsii_name="keyDescriptionInput")
    def key_description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyDescriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="keyIdInput")
    def key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="keyStateInput")
    def key_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyStateInput"))

    @builtins.property
    @jsii.member(jsii_name="originInput")
    def origin_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "originInput"))

    @builtins.property
    @jsii.member(jsii_name="realmInput")
    def realm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "realmInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultKeyFlag")
    def default_key_flag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultKeyFlag"))

    @default_key_flag.setter
    def default_key_flag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__358c018fcead1408268bebd83992c8849df197811a9e132e50f8c661d2414520)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultKeyFlag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainId")
    def domain_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainId"))

    @domain_id.setter
    def domain_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7319b6ffc8346cad990b3dc107082b90dbab9fa4afccc8d71601aab5cf0d04a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d60bfa5550ff9bb2a24dca0b224ce57c7d598a62ef08c8690cd8a364d6dce78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyAlias")
    def key_alias(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyAlias"))

    @key_alias.setter
    def key_alias(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6ee3bbcdc86bdc01ff2ea0a4efc8e585f439845b552efc488c61cd8fd48bb67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyAlias", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyDescription")
    def key_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyDescription"))

    @key_description.setter
    def key_description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cba95ecf109c4a569569908187458e638ce6cfbf59bcca7dc4a2d2637221a386)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyDescription", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyId")
    def key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyId"))

    @key_id.setter
    def key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb7ae8d54ab75b337eccaa7a447150557996a943b70e354b49ce1476d10cc4d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyState")
    def key_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyState"))

    @key_state.setter
    def key_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e11dcc8f115ed206baf2a53babbe8580e8f3e27da0d9fe46ea5d68ee40caeaf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="origin")
    def origin(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "origin"))

    @origin.setter
    def origin(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__304d572619a54e6f231da6385845188a43eca6bb19bcdb4e4ff212e375e722c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "origin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="realm")
    def realm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "realm"))

    @realm.setter
    def realm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84dda9a3613ffd33443f94e633be7d985aeb9fe701c4091af2167603499d8a87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "realm", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudKmsKeyV1.DataOpentelekomcloudKmsKeyV1Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "default_key_flag": "defaultKeyFlag",
        "domain_id": "domainId",
        "id": "id",
        "key_alias": "keyAlias",
        "key_description": "keyDescription",
        "key_id": "keyId",
        "key_state": "keyState",
        "origin": "origin",
        "realm": "realm",
    },
)
class DataOpentelekomcloudKmsKeyV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        default_key_flag: typing.Optional[builtins.str] = None,
        domain_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        key_alias: typing.Optional[builtins.str] = None,
        key_description: typing.Optional[builtins.str] = None,
        key_id: typing.Optional[builtins.str] = None,
        key_state: typing.Optional[builtins.str] = None,
        origin: typing.Optional[builtins.str] = None,
        realm: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param default_key_flag: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/kms_key_v1#default_key_flag DataOpentelekomcloudKmsKeyV1#default_key_flag}.
        :param domain_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/kms_key_v1#domain_id DataOpentelekomcloudKmsKeyV1#domain_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/kms_key_v1#id DataOpentelekomcloudKmsKeyV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param key_alias: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/kms_key_v1#key_alias DataOpentelekomcloudKmsKeyV1#key_alias}.
        :param key_description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/kms_key_v1#key_description DataOpentelekomcloudKmsKeyV1#key_description}.
        :param key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/kms_key_v1#key_id DataOpentelekomcloudKmsKeyV1#key_id}.
        :param key_state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/kms_key_v1#key_state DataOpentelekomcloudKmsKeyV1#key_state}.
        :param origin: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/kms_key_v1#origin DataOpentelekomcloudKmsKeyV1#origin}.
        :param realm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/kms_key_v1#realm DataOpentelekomcloudKmsKeyV1#realm}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f21c09c89a2aa42c59dd44201b8b265f8557665bdebdef3d76880c340e3dcc12)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument default_key_flag", value=default_key_flag, expected_type=type_hints["default_key_flag"])
            check_type(argname="argument domain_id", value=domain_id, expected_type=type_hints["domain_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument key_alias", value=key_alias, expected_type=type_hints["key_alias"])
            check_type(argname="argument key_description", value=key_description, expected_type=type_hints["key_description"])
            check_type(argname="argument key_id", value=key_id, expected_type=type_hints["key_id"])
            check_type(argname="argument key_state", value=key_state, expected_type=type_hints["key_state"])
            check_type(argname="argument origin", value=origin, expected_type=type_hints["origin"])
            check_type(argname="argument realm", value=realm, expected_type=type_hints["realm"])
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
        if default_key_flag is not None:
            self._values["default_key_flag"] = default_key_flag
        if domain_id is not None:
            self._values["domain_id"] = domain_id
        if id is not None:
            self._values["id"] = id
        if key_alias is not None:
            self._values["key_alias"] = key_alias
        if key_description is not None:
            self._values["key_description"] = key_description
        if key_id is not None:
            self._values["key_id"] = key_id
        if key_state is not None:
            self._values["key_state"] = key_state
        if origin is not None:
            self._values["origin"] = origin
        if realm is not None:
            self._values["realm"] = realm

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
    def default_key_flag(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/kms_key_v1#default_key_flag DataOpentelekomcloudKmsKeyV1#default_key_flag}.'''
        result = self._values.get("default_key_flag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/kms_key_v1#domain_id DataOpentelekomcloudKmsKeyV1#domain_id}.'''
        result = self._values.get("domain_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/kms_key_v1#id DataOpentelekomcloudKmsKeyV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_alias(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/kms_key_v1#key_alias DataOpentelekomcloudKmsKeyV1#key_alias}.'''
        result = self._values.get("key_alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/kms_key_v1#key_description DataOpentelekomcloudKmsKeyV1#key_description}.'''
        result = self._values.get("key_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/kms_key_v1#key_id DataOpentelekomcloudKmsKeyV1#key_id}.'''
        result = self._values.get("key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/kms_key_v1#key_state DataOpentelekomcloudKmsKeyV1#key_state}.'''
        result = self._values.get("key_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def origin(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/kms_key_v1#origin DataOpentelekomcloudKmsKeyV1#origin}.'''
        result = self._values.get("origin")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def realm(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/kms_key_v1#realm DataOpentelekomcloudKmsKeyV1#realm}.'''
        result = self._values.get("realm")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudKmsKeyV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DataOpentelekomcloudKmsKeyV1",
    "DataOpentelekomcloudKmsKeyV1Config",
]

publication.publish()

def _typecheckingstub__2c06cfb363e2892a83a6bc372442fbcf209c0dc48af29cce0f9b3e01ac28af28(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    default_key_flag: typing.Optional[builtins.str] = None,
    domain_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    key_alias: typing.Optional[builtins.str] = None,
    key_description: typing.Optional[builtins.str] = None,
    key_id: typing.Optional[builtins.str] = None,
    key_state: typing.Optional[builtins.str] = None,
    origin: typing.Optional[builtins.str] = None,
    realm: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__812f106ecb4f19ce587a7e76537fefba0adec299155e228bb0d513b87664123d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__358c018fcead1408268bebd83992c8849df197811a9e132e50f8c661d2414520(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7319b6ffc8346cad990b3dc107082b90dbab9fa4afccc8d71601aab5cf0d04a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d60bfa5550ff9bb2a24dca0b224ce57c7d598a62ef08c8690cd8a364d6dce78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6ee3bbcdc86bdc01ff2ea0a4efc8e585f439845b552efc488c61cd8fd48bb67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cba95ecf109c4a569569908187458e638ce6cfbf59bcca7dc4a2d2637221a386(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb7ae8d54ab75b337eccaa7a447150557996a943b70e354b49ce1476d10cc4d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e11dcc8f115ed206baf2a53babbe8580e8f3e27da0d9fe46ea5d68ee40caeaf8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__304d572619a54e6f231da6385845188a43eca6bb19bcdb4e4ff212e375e722c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84dda9a3613ffd33443f94e633be7d985aeb9fe701c4091af2167603499d8a87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f21c09c89a2aa42c59dd44201b8b265f8557665bdebdef3d76880c340e3dcc12(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_key_flag: typing.Optional[builtins.str] = None,
    domain_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    key_alias: typing.Optional[builtins.str] = None,
    key_description: typing.Optional[builtins.str] = None,
    key_id: typing.Optional[builtins.str] = None,
    key_state: typing.Optional[builtins.str] = None,
    origin: typing.Optional[builtins.str] = None,
    realm: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
