r'''
# `opentelekomcloud_obs_bucket_acl`

Refer to the Terraform Registry for docs: [`opentelekomcloud_obs_bucket_acl`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl).
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


class ObsBucketAcl(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucketAcl.ObsBucketAcl",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl opentelekomcloud_obs_bucket_acl}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        bucket: builtins.str,
        account_permission: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObsBucketAclAccountPermission", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        log_delivery_user_permission: typing.Optional[typing.Union["ObsBucketAclLogDeliveryUserPermission", typing.Dict[builtins.str, typing.Any]]] = None,
        owner_permission: typing.Optional[typing.Union["ObsBucketAclOwnerPermission", typing.Dict[builtins.str, typing.Any]]] = None,
        public_permission: typing.Optional[typing.Union["ObsBucketAclPublicPermission", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl opentelekomcloud_obs_bucket_acl} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#bucket ObsBucketAcl#bucket}.
        :param account_permission: account_permission block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#account_permission ObsBucketAcl#account_permission}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#id ObsBucketAcl#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_delivery_user_permission: log_delivery_user_permission block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#log_delivery_user_permission ObsBucketAcl#log_delivery_user_permission}
        :param owner_permission: owner_permission block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#owner_permission ObsBucketAcl#owner_permission}
        :param public_permission: public_permission block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#public_permission ObsBucketAcl#public_permission}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__815e77d8edd646867f148c115d3cbdef51f14b19b054291735411f942c175df8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ObsBucketAclConfig(
            bucket=bucket,
            account_permission=account_permission,
            id=id,
            log_delivery_user_permission=log_delivery_user_permission,
            owner_permission=owner_permission,
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
        '''Generates CDKTF code for importing a ObsBucketAcl resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ObsBucketAcl to import.
        :param import_from_id: The id of the existing ObsBucketAcl that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ObsBucketAcl to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6791eafb7ba42b6f5fed15d615676196a4b66568636a29b3a28cc2fe5626849)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAccountPermission")
    def put_account_permission(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObsBucketAclAccountPermission", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b94c7ec5ba4f4dd105c8b4267b564bc9b31c36fa49e324191a2b24dad5226b8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAccountPermission", [value]))

    @jsii.member(jsii_name="putLogDeliveryUserPermission")
    def put_log_delivery_user_permission(
        self,
        *,
        access_to_acl: typing.Optional[typing.Sequence[builtins.str]] = None,
        access_to_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param access_to_acl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#access_to_acl ObsBucketAcl#access_to_acl}.
        :param access_to_bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#access_to_bucket ObsBucketAcl#access_to_bucket}.
        '''
        value = ObsBucketAclLogDeliveryUserPermission(
            access_to_acl=access_to_acl, access_to_bucket=access_to_bucket
        )

        return typing.cast(None, jsii.invoke(self, "putLogDeliveryUserPermission", [value]))

    @jsii.member(jsii_name="putOwnerPermission")
    def put_owner_permission(
        self,
        *,
        access_to_acl: typing.Optional[typing.Sequence[builtins.str]] = None,
        access_to_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param access_to_acl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#access_to_acl ObsBucketAcl#access_to_acl}.
        :param access_to_bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#access_to_bucket ObsBucketAcl#access_to_bucket}.
        '''
        value = ObsBucketAclOwnerPermission(
            access_to_acl=access_to_acl, access_to_bucket=access_to_bucket
        )

        return typing.cast(None, jsii.invoke(self, "putOwnerPermission", [value]))

    @jsii.member(jsii_name="putPublicPermission")
    def put_public_permission(
        self,
        *,
        access_to_acl: typing.Optional[typing.Sequence[builtins.str]] = None,
        access_to_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param access_to_acl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#access_to_acl ObsBucketAcl#access_to_acl}.
        :param access_to_bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#access_to_bucket ObsBucketAcl#access_to_bucket}.
        '''
        value = ObsBucketAclPublicPermission(
            access_to_acl=access_to_acl, access_to_bucket=access_to_bucket
        )

        return typing.cast(None, jsii.invoke(self, "putPublicPermission", [value]))

    @jsii.member(jsii_name="resetAccountPermission")
    def reset_account_permission(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountPermission", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLogDeliveryUserPermission")
    def reset_log_delivery_user_permission(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogDeliveryUserPermission", []))

    @jsii.member(jsii_name="resetOwnerPermission")
    def reset_owner_permission(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOwnerPermission", []))

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
    def account_permission(self) -> "ObsBucketAclAccountPermissionList":
        return typing.cast("ObsBucketAclAccountPermissionList", jsii.get(self, "accountPermission"))

    @builtins.property
    @jsii.member(jsii_name="logDeliveryUserPermission")
    def log_delivery_user_permission(
        self,
    ) -> "ObsBucketAclLogDeliveryUserPermissionOutputReference":
        return typing.cast("ObsBucketAclLogDeliveryUserPermissionOutputReference", jsii.get(self, "logDeliveryUserPermission"))

    @builtins.property
    @jsii.member(jsii_name="ownerPermission")
    def owner_permission(self) -> "ObsBucketAclOwnerPermissionOutputReference":
        return typing.cast("ObsBucketAclOwnerPermissionOutputReference", jsii.get(self, "ownerPermission"))

    @builtins.property
    @jsii.member(jsii_name="publicPermission")
    def public_permission(self) -> "ObsBucketAclPublicPermissionOutputReference":
        return typing.cast("ObsBucketAclPublicPermissionOutputReference", jsii.get(self, "publicPermission"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="accountPermissionInput")
    def account_permission_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObsBucketAclAccountPermission"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObsBucketAclAccountPermission"]]], jsii.get(self, "accountPermissionInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="logDeliveryUserPermissionInput")
    def log_delivery_user_permission_input(
        self,
    ) -> typing.Optional["ObsBucketAclLogDeliveryUserPermission"]:
        return typing.cast(typing.Optional["ObsBucketAclLogDeliveryUserPermission"], jsii.get(self, "logDeliveryUserPermissionInput"))

    @builtins.property
    @jsii.member(jsii_name="ownerPermissionInput")
    def owner_permission_input(self) -> typing.Optional["ObsBucketAclOwnerPermission"]:
        return typing.cast(typing.Optional["ObsBucketAclOwnerPermission"], jsii.get(self, "ownerPermissionInput"))

    @builtins.property
    @jsii.member(jsii_name="publicPermissionInput")
    def public_permission_input(
        self,
    ) -> typing.Optional["ObsBucketAclPublicPermission"]:
        return typing.cast(typing.Optional["ObsBucketAclPublicPermission"], jsii.get(self, "publicPermissionInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__354a2e15c9d5c0b801687c5c581c1d1a946a5fc1f8f365a1a6e48748b943c58d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d946644b4fe590c1082f5d6c3057e9f779d85a5f0579cfc72687ed6874156e6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucketAcl.ObsBucketAclAccountPermission",
    jsii_struct_bases=[],
    name_mapping={
        "account_id": "accountId",
        "access_to_acl": "accessToAcl",
        "access_to_bucket": "accessToBucket",
    },
)
class ObsBucketAclAccountPermission:
    def __init__(
        self,
        *,
        account_id: builtins.str,
        access_to_acl: typing.Optional[typing.Sequence[builtins.str]] = None,
        access_to_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#account_id ObsBucketAcl#account_id}.
        :param access_to_acl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#access_to_acl ObsBucketAcl#access_to_acl}.
        :param access_to_bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#access_to_bucket ObsBucketAcl#access_to_bucket}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c661d0dbec9b3ab3de59e65b73d2d8e28239a19f651c2874ee22d2dc727d6536)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument access_to_acl", value=access_to_acl, expected_type=type_hints["access_to_acl"])
            check_type(argname="argument access_to_bucket", value=access_to_bucket, expected_type=type_hints["access_to_bucket"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
        }
        if access_to_acl is not None:
            self._values["access_to_acl"] = access_to_acl
        if access_to_bucket is not None:
            self._values["access_to_bucket"] = access_to_bucket

    @builtins.property
    def account_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#account_id ObsBucketAcl#account_id}.'''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_to_acl(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#access_to_acl ObsBucketAcl#access_to_acl}.'''
        result = self._values.get("access_to_acl")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def access_to_bucket(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#access_to_bucket ObsBucketAcl#access_to_bucket}.'''
        result = self._values.get("access_to_bucket")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObsBucketAclAccountPermission(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ObsBucketAclAccountPermissionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucketAcl.ObsBucketAclAccountPermissionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0ee1cfb52ff5e37c0e74ae0643e302cc1a7cb99177576f468621c745f6bd35d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ObsBucketAclAccountPermissionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__302825c5996d3ea0413e207958bf634a20ae05e077bbb41723ca2fe83d43a02d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ObsBucketAclAccountPermissionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32db0a9fc9a56d031ec9580c10c3373ad883f9fdb02bfdfb9b196ed5b5489b23)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae11b2c96f9e5fff171be4f5dc90542c8cca1a9f11b4d721a9e0cfd002e7b62a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f158ad60b779ced700d2b5817d5862415c175784b61a2ff3cb71c25db5f7de08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketAclAccountPermission]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketAclAccountPermission]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketAclAccountPermission]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04b78898809dfbad20ed6d9c8689bedc717d9b10a38f0f9fa9dd5faf02147361)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObsBucketAclAccountPermissionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucketAcl.ObsBucketAclAccountPermissionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__87541045efd594d8c11939e15afdd8b8e7915095a40df5735b5cd895178bf4b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccessToAcl")
    def reset_access_to_acl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessToAcl", []))

    @jsii.member(jsii_name="resetAccessToBucket")
    def reset_access_to_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessToBucket", []))

    @builtins.property
    @jsii.member(jsii_name="accessToAclInput")
    def access_to_acl_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accessToAclInput"))

    @builtins.property
    @jsii.member(jsii_name="accessToBucketInput")
    def access_to_bucket_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accessToBucketInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__41eb5ffcb5fabe28c8cbc1575def1bf7dcc2f2d990cd94fea7cc9813bd200829)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToAcl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="accessToBucket")
    def access_to_bucket(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accessToBucket"))

    @access_to_bucket.setter
    def access_to_bucket(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e8dafdc97c508d20d31d9db12921425a41b5c524638cfef248396c80bc331c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToBucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed1e0dc66e00be1da1a93636e378679232da2b634439f4fba27e3cd789893264)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketAclAccountPermission]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketAclAccountPermission]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketAclAccountPermission]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41c1cbfe1fce34bab6b0942eadad4aebb3abbb3111d98023a59e7a401b0065b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucketAcl.ObsBucketAclConfig",
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
        "account_permission": "accountPermission",
        "id": "id",
        "log_delivery_user_permission": "logDeliveryUserPermission",
        "owner_permission": "ownerPermission",
        "public_permission": "publicPermission",
    },
)
class ObsBucketAclConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        account_permission: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObsBucketAclAccountPermission, typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        log_delivery_user_permission: typing.Optional[typing.Union["ObsBucketAclLogDeliveryUserPermission", typing.Dict[builtins.str, typing.Any]]] = None,
        owner_permission: typing.Optional[typing.Union["ObsBucketAclOwnerPermission", typing.Dict[builtins.str, typing.Any]]] = None,
        public_permission: typing.Optional[typing.Union["ObsBucketAclPublicPermission", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#bucket ObsBucketAcl#bucket}.
        :param account_permission: account_permission block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#account_permission ObsBucketAcl#account_permission}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#id ObsBucketAcl#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_delivery_user_permission: log_delivery_user_permission block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#log_delivery_user_permission ObsBucketAcl#log_delivery_user_permission}
        :param owner_permission: owner_permission block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#owner_permission ObsBucketAcl#owner_permission}
        :param public_permission: public_permission block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#public_permission ObsBucketAcl#public_permission}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(log_delivery_user_permission, dict):
            log_delivery_user_permission = ObsBucketAclLogDeliveryUserPermission(**log_delivery_user_permission)
        if isinstance(owner_permission, dict):
            owner_permission = ObsBucketAclOwnerPermission(**owner_permission)
        if isinstance(public_permission, dict):
            public_permission = ObsBucketAclPublicPermission(**public_permission)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bfffa81ad10585b5057a4d305fd993efaf736b9ae283f19833f159d24bc9c39)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument account_permission", value=account_permission, expected_type=type_hints["account_permission"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument log_delivery_user_permission", value=log_delivery_user_permission, expected_type=type_hints["log_delivery_user_permission"])
            check_type(argname="argument owner_permission", value=owner_permission, expected_type=type_hints["owner_permission"])
            check_type(argname="argument public_permission", value=public_permission, expected_type=type_hints["public_permission"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
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
        if log_delivery_user_permission is not None:
            self._values["log_delivery_user_permission"] = log_delivery_user_permission
        if owner_permission is not None:
            self._values["owner_permission"] = owner_permission
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#bucket ObsBucketAcl#bucket}.'''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_permission(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketAclAccountPermission]]]:
        '''account_permission block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#account_permission ObsBucketAcl#account_permission}
        '''
        result = self._values.get("account_permission")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketAclAccountPermission]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#id ObsBucketAcl#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_delivery_user_permission(
        self,
    ) -> typing.Optional["ObsBucketAclLogDeliveryUserPermission"]:
        '''log_delivery_user_permission block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#log_delivery_user_permission ObsBucketAcl#log_delivery_user_permission}
        '''
        result = self._values.get("log_delivery_user_permission")
        return typing.cast(typing.Optional["ObsBucketAclLogDeliveryUserPermission"], result)

    @builtins.property
    def owner_permission(self) -> typing.Optional["ObsBucketAclOwnerPermission"]:
        '''owner_permission block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#owner_permission ObsBucketAcl#owner_permission}
        '''
        result = self._values.get("owner_permission")
        return typing.cast(typing.Optional["ObsBucketAclOwnerPermission"], result)

    @builtins.property
    def public_permission(self) -> typing.Optional["ObsBucketAclPublicPermission"]:
        '''public_permission block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#public_permission ObsBucketAcl#public_permission}
        '''
        result = self._values.get("public_permission")
        return typing.cast(typing.Optional["ObsBucketAclPublicPermission"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObsBucketAclConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucketAcl.ObsBucketAclLogDeliveryUserPermission",
    jsii_struct_bases=[],
    name_mapping={
        "access_to_acl": "accessToAcl",
        "access_to_bucket": "accessToBucket",
    },
)
class ObsBucketAclLogDeliveryUserPermission:
    def __init__(
        self,
        *,
        access_to_acl: typing.Optional[typing.Sequence[builtins.str]] = None,
        access_to_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param access_to_acl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#access_to_acl ObsBucketAcl#access_to_acl}.
        :param access_to_bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#access_to_bucket ObsBucketAcl#access_to_bucket}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__461dfd53c3cb8fe497be92c2605835509dcdbcf06cbc87fcc6b348e24014425f)
            check_type(argname="argument access_to_acl", value=access_to_acl, expected_type=type_hints["access_to_acl"])
            check_type(argname="argument access_to_bucket", value=access_to_bucket, expected_type=type_hints["access_to_bucket"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_to_acl is not None:
            self._values["access_to_acl"] = access_to_acl
        if access_to_bucket is not None:
            self._values["access_to_bucket"] = access_to_bucket

    @builtins.property
    def access_to_acl(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#access_to_acl ObsBucketAcl#access_to_acl}.'''
        result = self._values.get("access_to_acl")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def access_to_bucket(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#access_to_bucket ObsBucketAcl#access_to_bucket}.'''
        result = self._values.get("access_to_bucket")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObsBucketAclLogDeliveryUserPermission(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ObsBucketAclLogDeliveryUserPermissionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucketAcl.ObsBucketAclLogDeliveryUserPermissionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8f9a6ee8b7c40bf642d8122a70f5f1eb93f6cd040e6afe960d029199e9388a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAccessToAcl")
    def reset_access_to_acl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessToAcl", []))

    @jsii.member(jsii_name="resetAccessToBucket")
    def reset_access_to_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessToBucket", []))

    @builtins.property
    @jsii.member(jsii_name="accessToAclInput")
    def access_to_acl_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accessToAclInput"))

    @builtins.property
    @jsii.member(jsii_name="accessToBucketInput")
    def access_to_bucket_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accessToBucketInput"))

    @builtins.property
    @jsii.member(jsii_name="accessToAcl")
    def access_to_acl(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accessToAcl"))

    @access_to_acl.setter
    def access_to_acl(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d287dba95fe68ab01ccccd096ffe758fe16fd27d363bb026cdd5265a22b8a42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToAcl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="accessToBucket")
    def access_to_bucket(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accessToBucket"))

    @access_to_bucket.setter
    def access_to_bucket(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4df3782e2fe1e24c7657fae4c5882a623e7fdb1f60a78ad9de7bbf184bf333e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToBucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ObsBucketAclLogDeliveryUserPermission]:
        return typing.cast(typing.Optional[ObsBucketAclLogDeliveryUserPermission], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ObsBucketAclLogDeliveryUserPermission],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b262ec3735895b1cb0fe093e2e4c4374f21de305cc2e88f2e7d1827b1c7b6d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucketAcl.ObsBucketAclOwnerPermission",
    jsii_struct_bases=[],
    name_mapping={
        "access_to_acl": "accessToAcl",
        "access_to_bucket": "accessToBucket",
    },
)
class ObsBucketAclOwnerPermission:
    def __init__(
        self,
        *,
        access_to_acl: typing.Optional[typing.Sequence[builtins.str]] = None,
        access_to_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param access_to_acl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#access_to_acl ObsBucketAcl#access_to_acl}.
        :param access_to_bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#access_to_bucket ObsBucketAcl#access_to_bucket}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__482e31ce7f04bc06dfd1d1fa7406ee4b5d96c76bcd7838de22e6a2f5583bd37d)
            check_type(argname="argument access_to_acl", value=access_to_acl, expected_type=type_hints["access_to_acl"])
            check_type(argname="argument access_to_bucket", value=access_to_bucket, expected_type=type_hints["access_to_bucket"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_to_acl is not None:
            self._values["access_to_acl"] = access_to_acl
        if access_to_bucket is not None:
            self._values["access_to_bucket"] = access_to_bucket

    @builtins.property
    def access_to_acl(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#access_to_acl ObsBucketAcl#access_to_acl}.'''
        result = self._values.get("access_to_acl")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def access_to_bucket(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#access_to_bucket ObsBucketAcl#access_to_bucket}.'''
        result = self._values.get("access_to_bucket")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObsBucketAclOwnerPermission(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ObsBucketAclOwnerPermissionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucketAcl.ObsBucketAclOwnerPermissionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d977c4a543645b30fa69cf1b37bdab425e33539c0a6c0ab8da9331d1050ad7d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAccessToAcl")
    def reset_access_to_acl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessToAcl", []))

    @jsii.member(jsii_name="resetAccessToBucket")
    def reset_access_to_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessToBucket", []))

    @builtins.property
    @jsii.member(jsii_name="accessToAclInput")
    def access_to_acl_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accessToAclInput"))

    @builtins.property
    @jsii.member(jsii_name="accessToBucketInput")
    def access_to_bucket_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accessToBucketInput"))

    @builtins.property
    @jsii.member(jsii_name="accessToAcl")
    def access_to_acl(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accessToAcl"))

    @access_to_acl.setter
    def access_to_acl(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__583b25d3d7db94fb443a4b8052f81ee36422090a3d81eeaebf3783fa65718ced)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToAcl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="accessToBucket")
    def access_to_bucket(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accessToBucket"))

    @access_to_bucket.setter
    def access_to_bucket(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f328a228211647455da78348445650c84ed0ab69e0cfa28ef9e733ebad79797)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToBucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ObsBucketAclOwnerPermission]:
        return typing.cast(typing.Optional[ObsBucketAclOwnerPermission], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ObsBucketAclOwnerPermission],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dade632c3a4fa72b81422c81cd5a94811ab3ba4e7f897bb84df2cac290d25246)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucketAcl.ObsBucketAclPublicPermission",
    jsii_struct_bases=[],
    name_mapping={
        "access_to_acl": "accessToAcl",
        "access_to_bucket": "accessToBucket",
    },
)
class ObsBucketAclPublicPermission:
    def __init__(
        self,
        *,
        access_to_acl: typing.Optional[typing.Sequence[builtins.str]] = None,
        access_to_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param access_to_acl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#access_to_acl ObsBucketAcl#access_to_acl}.
        :param access_to_bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#access_to_bucket ObsBucketAcl#access_to_bucket}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__912c013ff21f6af994d5acfbeeae85e457fa72cef34f5220b29698558c0e606e)
            check_type(argname="argument access_to_acl", value=access_to_acl, expected_type=type_hints["access_to_acl"])
            check_type(argname="argument access_to_bucket", value=access_to_bucket, expected_type=type_hints["access_to_bucket"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_to_acl is not None:
            self._values["access_to_acl"] = access_to_acl
        if access_to_bucket is not None:
            self._values["access_to_bucket"] = access_to_bucket

    @builtins.property
    def access_to_acl(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#access_to_acl ObsBucketAcl#access_to_acl}.'''
        result = self._values.get("access_to_acl")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def access_to_bucket(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/obs_bucket_acl#access_to_bucket ObsBucketAcl#access_to_bucket}.'''
        result = self._values.get("access_to_bucket")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObsBucketAclPublicPermission(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ObsBucketAclPublicPermissionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.obsBucketAcl.ObsBucketAclPublicPermissionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd9a64466fe60ac3ac8ba997b284f438411702bdc865fd815bab4454599169be)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAccessToAcl")
    def reset_access_to_acl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessToAcl", []))

    @jsii.member(jsii_name="resetAccessToBucket")
    def reset_access_to_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessToBucket", []))

    @builtins.property
    @jsii.member(jsii_name="accessToAclInput")
    def access_to_acl_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accessToAclInput"))

    @builtins.property
    @jsii.member(jsii_name="accessToBucketInput")
    def access_to_bucket_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accessToBucketInput"))

    @builtins.property
    @jsii.member(jsii_name="accessToAcl")
    def access_to_acl(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accessToAcl"))

    @access_to_acl.setter
    def access_to_acl(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e50c237022c4c708e00c796886b1199314b1c483aff275061a55f54f9883331d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToAcl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="accessToBucket")
    def access_to_bucket(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accessToBucket"))

    @access_to_bucket.setter
    def access_to_bucket(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad79cfc9a2e72fc0f509c95e98960502534aa19d4a77c725a2751660359b88cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToBucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ObsBucketAclPublicPermission]:
        return typing.cast(typing.Optional[ObsBucketAclPublicPermission], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ObsBucketAclPublicPermission],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81208f156492ca7222edd1248bc9ad36eb36d41fb795290b71637d742e8e2a32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ObsBucketAcl",
    "ObsBucketAclAccountPermission",
    "ObsBucketAclAccountPermissionList",
    "ObsBucketAclAccountPermissionOutputReference",
    "ObsBucketAclConfig",
    "ObsBucketAclLogDeliveryUserPermission",
    "ObsBucketAclLogDeliveryUserPermissionOutputReference",
    "ObsBucketAclOwnerPermission",
    "ObsBucketAclOwnerPermissionOutputReference",
    "ObsBucketAclPublicPermission",
    "ObsBucketAclPublicPermissionOutputReference",
]

publication.publish()

def _typecheckingstub__815e77d8edd646867f148c115d3cbdef51f14b19b054291735411f942c175df8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    bucket: builtins.str,
    account_permission: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObsBucketAclAccountPermission, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    log_delivery_user_permission: typing.Optional[typing.Union[ObsBucketAclLogDeliveryUserPermission, typing.Dict[builtins.str, typing.Any]]] = None,
    owner_permission: typing.Optional[typing.Union[ObsBucketAclOwnerPermission, typing.Dict[builtins.str, typing.Any]]] = None,
    public_permission: typing.Optional[typing.Union[ObsBucketAclPublicPermission, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__b6791eafb7ba42b6f5fed15d615676196a4b66568636a29b3a28cc2fe5626849(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b94c7ec5ba4f4dd105c8b4267b564bc9b31c36fa49e324191a2b24dad5226b8e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObsBucketAclAccountPermission, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__354a2e15c9d5c0b801687c5c581c1d1a946a5fc1f8f365a1a6e48748b943c58d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d946644b4fe590c1082f5d6c3057e9f779d85a5f0579cfc72687ed6874156e6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c661d0dbec9b3ab3de59e65b73d2d8e28239a19f651c2874ee22d2dc727d6536(
    *,
    account_id: builtins.str,
    access_to_acl: typing.Optional[typing.Sequence[builtins.str]] = None,
    access_to_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0ee1cfb52ff5e37c0e74ae0643e302cc1a7cb99177576f468621c745f6bd35d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__302825c5996d3ea0413e207958bf634a20ae05e077bbb41723ca2fe83d43a02d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32db0a9fc9a56d031ec9580c10c3373ad883f9fdb02bfdfb9b196ed5b5489b23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae11b2c96f9e5fff171be4f5dc90542c8cca1a9f11b4d721a9e0cfd002e7b62a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f158ad60b779ced700d2b5817d5862415c175784b61a2ff3cb71c25db5f7de08(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04b78898809dfbad20ed6d9c8689bedc717d9b10a38f0f9fa9dd5faf02147361(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObsBucketAclAccountPermission]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87541045efd594d8c11939e15afdd8b8e7915095a40df5735b5cd895178bf4b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41eb5ffcb5fabe28c8cbc1575def1bf7dcc2f2d990cd94fea7cc9813bd200829(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e8dafdc97c508d20d31d9db12921425a41b5c524638cfef248396c80bc331c5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed1e0dc66e00be1da1a93636e378679232da2b634439f4fba27e3cd789893264(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41c1cbfe1fce34bab6b0942eadad4aebb3abbb3111d98023a59e7a401b0065b0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObsBucketAclAccountPermission]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bfffa81ad10585b5057a4d305fd993efaf736b9ae283f19833f159d24bc9c39(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    bucket: builtins.str,
    account_permission: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObsBucketAclAccountPermission, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    log_delivery_user_permission: typing.Optional[typing.Union[ObsBucketAclLogDeliveryUserPermission, typing.Dict[builtins.str, typing.Any]]] = None,
    owner_permission: typing.Optional[typing.Union[ObsBucketAclOwnerPermission, typing.Dict[builtins.str, typing.Any]]] = None,
    public_permission: typing.Optional[typing.Union[ObsBucketAclPublicPermission, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__461dfd53c3cb8fe497be92c2605835509dcdbcf06cbc87fcc6b348e24014425f(
    *,
    access_to_acl: typing.Optional[typing.Sequence[builtins.str]] = None,
    access_to_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8f9a6ee8b7c40bf642d8122a70f5f1eb93f6cd040e6afe960d029199e9388a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d287dba95fe68ab01ccccd096ffe758fe16fd27d363bb026cdd5265a22b8a42(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4df3782e2fe1e24c7657fae4c5882a623e7fdb1f60a78ad9de7bbf184bf333e5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b262ec3735895b1cb0fe093e2e4c4374f21de305cc2e88f2e7d1827b1c7b6d0(
    value: typing.Optional[ObsBucketAclLogDeliveryUserPermission],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__482e31ce7f04bc06dfd1d1fa7406ee4b5d96c76bcd7838de22e6a2f5583bd37d(
    *,
    access_to_acl: typing.Optional[typing.Sequence[builtins.str]] = None,
    access_to_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d977c4a543645b30fa69cf1b37bdab425e33539c0a6c0ab8da9331d1050ad7d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__583b25d3d7db94fb443a4b8052f81ee36422090a3d81eeaebf3783fa65718ced(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f328a228211647455da78348445650c84ed0ab69e0cfa28ef9e733ebad79797(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dade632c3a4fa72b81422c81cd5a94811ab3ba4e7f897bb84df2cac290d25246(
    value: typing.Optional[ObsBucketAclOwnerPermission],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__912c013ff21f6af994d5acfbeeae85e457fa72cef34f5220b29698558c0e606e(
    *,
    access_to_acl: typing.Optional[typing.Sequence[builtins.str]] = None,
    access_to_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd9a64466fe60ac3ac8ba997b284f438411702bdc865fd815bab4454599169be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e50c237022c4c708e00c796886b1199314b1c483aff275061a55f54f9883331d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad79cfc9a2e72fc0f509c95e98960502534aa19d4a77c725a2751660359b88cb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81208f156492ca7222edd1248bc9ad36eb36d41fb795290b71637d742e8e2a32(
    value: typing.Optional[ObsBucketAclPublicPermission],
) -> None:
    """Type checking stubs"""
    pass
