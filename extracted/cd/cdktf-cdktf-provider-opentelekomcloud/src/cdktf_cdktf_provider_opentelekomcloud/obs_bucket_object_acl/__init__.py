r'''
# `opentelekomcloud_obs_bucket_object_acl`

Refer to the Terraform Registry for docs: [`opentelekomcloud_obs_bucket_object_acl`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_object_acl).
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


class ObsBucketObjectAcl(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucketObjectAcl.ObsBucketObjectAcl",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_object_acl opentelekomcloud_obs_bucket_object_acl}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        bucket: builtins.str,
        key: builtins.str,
        account_permission: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObsBucketObjectAclAccountPermission", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        public_permission: typing.Optional[typing.Union["ObsBucketObjectAclPublicPermission", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_object_acl opentelekomcloud_obs_bucket_object_acl} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_object_acl#bucket ObsBucketObjectAcl#bucket}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_object_acl#key ObsBucketObjectAcl#key}.
        :param account_permission: account_permission block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_object_acl#account_permission ObsBucketObjectAcl#account_permission}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_object_acl#id ObsBucketObjectAcl#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param public_permission: public_permission block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_object_acl#public_permission ObsBucketObjectAcl#public_permission}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__838a6d613be2c3d06a4e7bfb2f87a998908309234c52df798cb16c0c82b099a8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ObsBucketObjectAclConfig(
            bucket=bucket,
            key=key,
            account_permission=account_permission,
            id=id,
            public_permission=public_permission,
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
        '''Generates CDKTF code for importing a ObsBucketObjectAcl resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ObsBucketObjectAcl to import.
        :param import_from_id: The id of the existing ObsBucketObjectAcl that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_object_acl#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ObsBucketObjectAcl to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76252fab7d542548698f89ce2199dc3ca591dc62ba17921b76ae959f4e7db9c9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAccountPermission")
    def put_account_permission(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObsBucketObjectAclAccountPermission", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2db9f13e5024a3458d2fcd7a470ff964bdb088ab7a63270fdca71f959ad21832)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAccountPermission", [value]))

    @jsii.member(jsii_name="putPublicPermission")
    def put_public_permission(
        self,
        *,
        access_to_acl: typing.Optional[typing.Sequence[builtins.str]] = None,
        access_to_object: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param access_to_acl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_object_acl#access_to_acl ObsBucketObjectAcl#access_to_acl}.
        :param access_to_object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_object_acl#access_to_object ObsBucketObjectAcl#access_to_object}.
        '''
        value = ObsBucketObjectAclPublicPermission(
            access_to_acl=access_to_acl, access_to_object=access_to_object
        )

        return typing.cast(None, jsii.invoke(self, "putPublicPermission", [value]))

    @jsii.member(jsii_name="resetAccountPermission")
    def reset_account_permission(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountPermission", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPublicPermission")
    def reset_public_permission(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicPermission", []))

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
    @jsii.member(jsii_name="accountPermission")
    def account_permission(self) -> "ObsBucketObjectAclAccountPermissionList":
        return typing.cast("ObsBucketObjectAclAccountPermissionList", jsii.get(self, "accountPermission"))

    @builtins.property
    @jsii.member(jsii_name="ownerPermission")
    def owner_permission(self) -> "ObsBucketObjectAclOwnerPermissionList":
        return typing.cast("ObsBucketObjectAclOwnerPermissionList", jsii.get(self, "ownerPermission"))

    @builtins.property
    @jsii.member(jsii_name="publicPermission")
    def public_permission(self) -> "ObsBucketObjectAclPublicPermissionOutputReference":
        return typing.cast("ObsBucketObjectAclPublicPermissionOutputReference", jsii.get(self, "publicPermission"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="accountPermissionInput")
    def account_permission_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObsBucketObjectAclAccountPermission"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObsBucketObjectAclAccountPermission"]]], jsii.get(self, "accountPermissionInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="publicPermissionInput")
    def public_permission_input(
        self,
    ) -> typing.Optional["ObsBucketObjectAclPublicPermission"]:
        return typing.cast(typing.Optional["ObsBucketObjectAclPublicPermission"], jsii.get(self, "publicPermissionInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35bed17c6691992752ea742f6704ce5ca621b3d73acf34d75450ea87c5693da7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92cbec4705a706c64ab20248a4cd89ea9c978c38714ec75ed16497356080892a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__854eea54d123d7695eac52eb9f426c90ad433a231145cdb1d14bc1e520290eb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucketObjectAcl.ObsBucketObjectAclAccountPermission",
    jsii_struct_bases=[],
    name_mapping={
        "account_id": "accountId",
        "access_to_acl": "accessToAcl",
        "access_to_object": "accessToObject",
    },
)
class ObsBucketObjectAclAccountPermission:
    def __init__(
        self,
        *,
        account_id: builtins.str,
        access_to_acl: typing.Optional[typing.Sequence[builtins.str]] = None,
        access_to_object: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_object_acl#account_id ObsBucketObjectAcl#account_id}.
        :param access_to_acl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_object_acl#access_to_acl ObsBucketObjectAcl#access_to_acl}.
        :param access_to_object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_object_acl#access_to_object ObsBucketObjectAcl#access_to_object}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3202fab42d4059292c6a4bcc808dc78c9278e914040ed8aa09858a0f19d779c7)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument access_to_acl", value=access_to_acl, expected_type=type_hints["access_to_acl"])
            check_type(argname="argument access_to_object", value=access_to_object, expected_type=type_hints["access_to_object"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
        }
        if access_to_acl is not None:
            self._values["access_to_acl"] = access_to_acl
        if access_to_object is not None:
            self._values["access_to_object"] = access_to_object

    @builtins.property
    def account_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_object_acl#account_id ObsBucketObjectAcl#account_id}.'''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_to_acl(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_object_acl#access_to_acl ObsBucketObjectAcl#access_to_acl}.'''
        result = self._values.get("access_to_acl")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def access_to_object(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_object_acl#access_to_object ObsBucketObjectAcl#access_to_object}.'''
        result = self._values.get("access_to_object")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObsBucketObjectAclAccountPermission(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ObsBucketObjectAclAccountPermissionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucketObjectAcl.ObsBucketObjectAclAccountPermissionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0f1da546b7a90a4a6966a5769da21b7ffd6f81c5f881624519bd7f6d6006533)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ObsBucketObjectAclAccountPermissionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__335075eed2275e8e94d524eeac4211708c90b62aa80ff580f4a6884731923023)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ObsBucketObjectAclAccountPermissionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad91ff029108c2ffdfa187c7829f350894c7ffe1fa638a6db79e2dd91001cf77)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9cb8da47d24767eeb44b0ef1ee2385cee57a30600d6483f15ba7ee13d7455063)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f8cf9e0ac7f0e0c10ac7de1040e411b192179bcba8efdb8edb8b500b3420ea8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketObjectAclAccountPermission]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketObjectAclAccountPermission]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketObjectAclAccountPermission]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c771dba75f4bc5ceeb57a5234276d6ac4ae47c1cd767937dd06cfaf22ff6f92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObsBucketObjectAclAccountPermissionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucketObjectAcl.ObsBucketObjectAclAccountPermissionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__821f4d26303efbc3c0a6cdb0dfb2c34504b44ef0e77043a81da24e2c52aa4453)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccessToAcl")
    def reset_access_to_acl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessToAcl", []))

    @jsii.member(jsii_name="resetAccessToObject")
    def reset_access_to_object(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessToObject", []))

    @builtins.property
    @jsii.member(jsii_name="accessToAclInput")
    def access_to_acl_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accessToAclInput"))

    @builtins.property
    @jsii.member(jsii_name="accessToObjectInput")
    def access_to_object_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accessToObjectInput"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="accessToAcl")
    def access_to_acl(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accessToAcl"))

    @access_to_acl.setter
    def access_to_acl(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__362c7b269fce000b6d8cfaada9beff7dd94b0ecf0659da429f3a71de04280024)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToAcl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="accessToObject")
    def access_to_object(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accessToObject"))

    @access_to_object.setter
    def access_to_object(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d94d8ae42b449d87d4b321a2269712ba3da7bf1eed2850a0b327ca29b1784322)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToObject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdd506ca4dfb27ecc746fd4b7f3c8aa0512562e88291ec53fb46239a97ca0624)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketObjectAclAccountPermission]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketObjectAclAccountPermission]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketObjectAclAccountPermission]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8addc3aead0ccfb3284424b2043bd070e28987a7c4a0e163c1f4cd107888097c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucketObjectAcl.ObsBucketObjectAclConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "bucket": "bucket",
        "key": "key",
        "account_permission": "accountPermission",
        "id": "id",
        "public_permission": "publicPermission",
    },
)
class ObsBucketObjectAclConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        bucket: builtins.str,
        key: builtins.str,
        account_permission: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObsBucketObjectAclAccountPermission, typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        public_permission: typing.Optional[typing.Union["ObsBucketObjectAclPublicPermission", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_object_acl#bucket ObsBucketObjectAcl#bucket}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_object_acl#key ObsBucketObjectAcl#key}.
        :param account_permission: account_permission block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_object_acl#account_permission ObsBucketObjectAcl#account_permission}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_object_acl#id ObsBucketObjectAcl#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param public_permission: public_permission block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_object_acl#public_permission ObsBucketObjectAcl#public_permission}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(public_permission, dict):
            public_permission = ObsBucketObjectAclPublicPermission(**public_permission)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffd2560ca1c33d54a27519bce30d1bc69389633b0e8a7bdf38cca989eb1a6675)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument account_permission", value=account_permission, expected_type=type_hints["account_permission"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument public_permission", value=public_permission, expected_type=type_hints["public_permission"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
            "key": key,
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
        if account_permission is not None:
            self._values["account_permission"] = account_permission
        if id is not None:
            self._values["id"] = id
        if public_permission is not None:
            self._values["public_permission"] = public_permission

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
    def bucket(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_object_acl#bucket ObsBucketObjectAcl#bucket}.'''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_object_acl#key ObsBucketObjectAcl#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_permission(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketObjectAclAccountPermission]]]:
        '''account_permission block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_object_acl#account_permission ObsBucketObjectAcl#account_permission}
        '''
        result = self._values.get("account_permission")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketObjectAclAccountPermission]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_object_acl#id ObsBucketObjectAcl#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_permission(
        self,
    ) -> typing.Optional["ObsBucketObjectAclPublicPermission"]:
        '''public_permission block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_object_acl#public_permission ObsBucketObjectAcl#public_permission}
        '''
        result = self._values.get("public_permission")
        return typing.cast(typing.Optional["ObsBucketObjectAclPublicPermission"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObsBucketObjectAclConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucketObjectAcl.ObsBucketObjectAclOwnerPermission",
    jsii_struct_bases=[],
    name_mapping={},
)
class ObsBucketObjectAclOwnerPermission:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObsBucketObjectAclOwnerPermission(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ObsBucketObjectAclOwnerPermissionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucketObjectAcl.ObsBucketObjectAclOwnerPermissionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__11d74ce1ab5ed0e7ef2e18dffa971b0716fbca2c320efa35fef69946cf7db135)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ObsBucketObjectAclOwnerPermissionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4b51c5aa0c5d2bd4ad7baf225aba45787e072d10ae58efd4b7beb11e9371730)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ObsBucketObjectAclOwnerPermissionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b45bbb66c46b1d8decd991d5a2f85a1b4a14b3215f66d8688cc34fb13bf5456b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62f95ca5a04cef72d4862c7f28765f7b68ad70a89c2047c163d25c7e8e52927d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc15b232fd28fccd9408b156670f855dba04038dff6d5125eaae633851be9fc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ObsBucketObjectAclOwnerPermissionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucketObjectAcl.ObsBucketObjectAclOwnerPermissionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f65ddc4b81f6e5a8448d8e842cdb12be67727a3fd5494cc9c6b8d6b5a0f23d7a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="accessToAcl")
    def access_to_acl(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accessToAcl"))

    @builtins.property
    @jsii.member(jsii_name="accessToObject")
    def access_to_object(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accessToObject"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ObsBucketObjectAclOwnerPermission]:
        return typing.cast(typing.Optional[ObsBucketObjectAclOwnerPermission], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ObsBucketObjectAclOwnerPermission],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b12bf07b2de1e3e6c9bc3b78ed5144625d8b1fa32cde9509f0798b6ba05b896)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucketObjectAcl.ObsBucketObjectAclPublicPermission",
    jsii_struct_bases=[],
    name_mapping={
        "access_to_acl": "accessToAcl",
        "access_to_object": "accessToObject",
    },
)
class ObsBucketObjectAclPublicPermission:
    def __init__(
        self,
        *,
        access_to_acl: typing.Optional[typing.Sequence[builtins.str]] = None,
        access_to_object: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param access_to_acl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_object_acl#access_to_acl ObsBucketObjectAcl#access_to_acl}.
        :param access_to_object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_object_acl#access_to_object ObsBucketObjectAcl#access_to_object}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36a8d5b428178f0e6c9c9cfab6382160f028e9b25d2daa1e7de7c44942d0320d)
            check_type(argname="argument access_to_acl", value=access_to_acl, expected_type=type_hints["access_to_acl"])
            check_type(argname="argument access_to_object", value=access_to_object, expected_type=type_hints["access_to_object"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_to_acl is not None:
            self._values["access_to_acl"] = access_to_acl
        if access_to_object is not None:
            self._values["access_to_object"] = access_to_object

    @builtins.property
    def access_to_acl(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_object_acl#access_to_acl ObsBucketObjectAcl#access_to_acl}.'''
        result = self._values.get("access_to_acl")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def access_to_object(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_object_acl#access_to_object ObsBucketObjectAcl#access_to_object}.'''
        result = self._values.get("access_to_object")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObsBucketObjectAclPublicPermission(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ObsBucketObjectAclPublicPermissionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucketObjectAcl.ObsBucketObjectAclPublicPermissionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5c3ddf49ef060603ddd8a266b772976d1ef2b64e11396f2414ad082cf01b5ea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAccessToAcl")
    def reset_access_to_acl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessToAcl", []))

    @jsii.member(jsii_name="resetAccessToObject")
    def reset_access_to_object(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessToObject", []))

    @builtins.property
    @jsii.member(jsii_name="accessToAclInput")
    def access_to_acl_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accessToAclInput"))

    @builtins.property
    @jsii.member(jsii_name="accessToObjectInput")
    def access_to_object_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accessToObjectInput"))

    @builtins.property
    @jsii.member(jsii_name="accessToAcl")
    def access_to_acl(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accessToAcl"))

    @access_to_acl.setter
    def access_to_acl(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c36b5c1765f06755d99f4c71a2e7aa211e8425a1e2334e48867a750241fff377)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToAcl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="accessToObject")
    def access_to_object(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accessToObject"))

    @access_to_object.setter
    def access_to_object(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__373838341987c79f67f66786d4fe6d52e5111834d7bf5f075541aba211bafed7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToObject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ObsBucketObjectAclPublicPermission]:
        return typing.cast(typing.Optional[ObsBucketObjectAclPublicPermission], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ObsBucketObjectAclPublicPermission],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b84755d11531cc97555043034db3f20b4247671ca5748add2380a3537dea2fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ObsBucketObjectAcl",
    "ObsBucketObjectAclAccountPermission",
    "ObsBucketObjectAclAccountPermissionList",
    "ObsBucketObjectAclAccountPermissionOutputReference",
    "ObsBucketObjectAclConfig",
    "ObsBucketObjectAclOwnerPermission",
    "ObsBucketObjectAclOwnerPermissionList",
    "ObsBucketObjectAclOwnerPermissionOutputReference",
    "ObsBucketObjectAclPublicPermission",
    "ObsBucketObjectAclPublicPermissionOutputReference",
]

publication.publish()

def _typecheckingstub__838a6d613be2c3d06a4e7bfb2f87a998908309234c52df798cb16c0c82b099a8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    bucket: builtins.str,
    key: builtins.str,
    account_permission: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObsBucketObjectAclAccountPermission, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    public_permission: typing.Optional[typing.Union[ObsBucketObjectAclPublicPermission, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__76252fab7d542548698f89ce2199dc3ca591dc62ba17921b76ae959f4e7db9c9(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2db9f13e5024a3458d2fcd7a470ff964bdb088ab7a63270fdca71f959ad21832(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObsBucketObjectAclAccountPermission, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35bed17c6691992752ea742f6704ce5ca621b3d73acf34d75450ea87c5693da7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92cbec4705a706c64ab20248a4cd89ea9c978c38714ec75ed16497356080892a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__854eea54d123d7695eac52eb9f426c90ad433a231145cdb1d14bc1e520290eb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3202fab42d4059292c6a4bcc808dc78c9278e914040ed8aa09858a0f19d779c7(
    *,
    account_id: builtins.str,
    access_to_acl: typing.Optional[typing.Sequence[builtins.str]] = None,
    access_to_object: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0f1da546b7a90a4a6966a5769da21b7ffd6f81c5f881624519bd7f6d6006533(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__335075eed2275e8e94d524eeac4211708c90b62aa80ff580f4a6884731923023(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad91ff029108c2ffdfa187c7829f350894c7ffe1fa638a6db79e2dd91001cf77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cb8da47d24767eeb44b0ef1ee2385cee57a30600d6483f15ba7ee13d7455063(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f8cf9e0ac7f0e0c10ac7de1040e411b192179bcba8efdb8edb8b500b3420ea8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c771dba75f4bc5ceeb57a5234276d6ac4ae47c1cd767937dd06cfaf22ff6f92(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketObjectAclAccountPermission]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__821f4d26303efbc3c0a6cdb0dfb2c34504b44ef0e77043a81da24e2c52aa4453(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__362c7b269fce000b6d8cfaada9beff7dd94b0ecf0659da429f3a71de04280024(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d94d8ae42b449d87d4b321a2269712ba3da7bf1eed2850a0b327ca29b1784322(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdd506ca4dfb27ecc746fd4b7f3c8aa0512562e88291ec53fb46239a97ca0624(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8addc3aead0ccfb3284424b2043bd070e28987a7c4a0e163c1f4cd107888097c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketObjectAclAccountPermission]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffd2560ca1c33d54a27519bce30d1bc69389633b0e8a7bdf38cca989eb1a6675(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    bucket: builtins.str,
    key: builtins.str,
    account_permission: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObsBucketObjectAclAccountPermission, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    public_permission: typing.Optional[typing.Union[ObsBucketObjectAclPublicPermission, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11d74ce1ab5ed0e7ef2e18dffa971b0716fbca2c320efa35fef69946cf7db135(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4b51c5aa0c5d2bd4ad7baf225aba45787e072d10ae58efd4b7beb11e9371730(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b45bbb66c46b1d8decd991d5a2f85a1b4a14b3215f66d8688cc34fb13bf5456b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62f95ca5a04cef72d4862c7f28765f7b68ad70a89c2047c163d25c7e8e52927d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc15b232fd28fccd9408b156670f855dba04038dff6d5125eaae633851be9fc2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f65ddc4b81f6e5a8448d8e842cdb12be67727a3fd5494cc9c6b8d6b5a0f23d7a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b12bf07b2de1e3e6c9bc3b78ed5144625d8b1fa32cde9509f0798b6ba05b896(
    value: typing.Optional[ObsBucketObjectAclOwnerPermission],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36a8d5b428178f0e6c9c9cfab6382160f028e9b25d2daa1e7de7c44942d0320d(
    *,
    access_to_acl: typing.Optional[typing.Sequence[builtins.str]] = None,
    access_to_object: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5c3ddf49ef060603ddd8a266b772976d1ef2b64e11396f2414ad082cf01b5ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c36b5c1765f06755d99f4c71a2e7aa211e8425a1e2334e48867a750241fff377(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__373838341987c79f67f66786d4fe6d52e5111834d7bf5f075541aba211bafed7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b84755d11531cc97555043034db3f20b4247671ca5748add2380a3537dea2fd(
    value: typing.Optional[ObsBucketObjectAclPublicPermission],
) -> None:
    """Type checking stubs"""
    pass
