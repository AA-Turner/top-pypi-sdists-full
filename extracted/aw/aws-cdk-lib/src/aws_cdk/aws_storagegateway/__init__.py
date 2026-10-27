r'''
# AWS::StorageGateway Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_storagegateway as storagegateway
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for StorageGateway construct libraries](https://constructs.dev/search?q=storagegateway)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::StorageGateway resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_StorageGateway.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::StorageGateway](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_StorageGateway.html).

(Read the [CDK Contributing Guide](https://github.com/aws/aws-cdk/blob/main/CONTRIBUTING.md) and submit an RFC if you are interested in contributing to this construct library.)

<!--END CFNONLY DISCLAIMER-->
'''
from __future__ import annotations

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

from jsii._type_checking import cached_type_hints, check_type


from .._jsii import *

class _LazyImport:
    def __init__(self, module_name: str) -> None:
        self._module_name = module_name
        self._module: typing.Any = None
    def __getattr__(self, name: str) -> typing.Any:
        if self._module is None:
            import importlib
            self._module = importlib.import_module(self._module_name)
        return getattr(self._module, name)

if typing.TYPE_CHECKING:

    import aws_cdk as _aws_cdk_0cae9daa
    import aws_cdk.interfaces.aws_storagegateway as _aws_storagegateway_f426d4c4
    import constructs as _constructs_77d1e7e8
else:

    _aws_cdk_0cae9daa = _LazyImport("aws_cdk")
    _aws_storagegateway_f426d4c4 = _LazyImport("aws_cdk.interfaces.aws_storagegateway")
    _constructs_77d1e7e8 = _LazyImport("constructs")


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_storagegateway_f426d4c4.INFSFileShareRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnNFSFileShare(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_storagegateway.CfnNFSFileShare",
):
    '''Resource Type definition for AWS::StorageGateway::NFSFileShare.

    An NFS file share exposes an Amazon S3 bucket through a Storage Gateway file gateway, so clients read and write objects as files over NFS. The share's variant is fixed by its resource type rather than by a property: the service constructs the two variants with different APIs, and a property carrying the choice would belong to neither API's input.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-nfsfileshare.html
    :cloudformationResource: AWS::StorageGateway::NFSFileShare
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_storagegateway as storagegateway
        
        cfn_nfs_file_share = storagegateway.CfnNFSFileShare(self, "MyCfnNFSFileShare",
            gateway_arn="gatewayArn",
            location_arn="locationArn",
            role="role",
        
            # the properties below are optional
            audit_destination_arn="auditDestinationArn",
            bucket_region="bucketRegion",
            cache_attributes=storagegateway.CfnNFSFileShare.CacheAttributesProperty(
                cache_stale_timeout_in_seconds=123
            ),
            client_list=["clientList"],
            default_storage_class="defaultStorageClass",
            encryption_type="encryptionType",
            file_share_name="fileShareName",
            guess_mime_type_enabled=False,
            kms_encrypted=False,
            kms_key="kmsKey",
            nfs_file_share_defaults=storagegateway.CfnNFSFileShare.NFSFileShareDefaultsProperty(
                directory_mode="directoryMode",
                file_mode="fileMode",
                group_id=123,
                owner_id=123
            ),
            notification_policy="notificationPolicy",
            object_acl="objectAcl",
            read_only=False,
            requester_pays=False,
            squash="squash",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpc_endpoint_dns_name="vpcEndpointDnsName"
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        gateway_arn: builtins.str,
        location_arn: builtins.str,
        role: builtins.str,
        audit_destination_arn: typing.Optional[builtins.str] = None,
        bucket_region: typing.Optional[builtins.str] = None,
        cache_attributes: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnNFSFileShare.CacheAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        client_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_storage_class: typing.Optional[builtins.str] = None,
        encryption_type: typing.Optional[builtins.str] = None,
        file_share_name: typing.Optional[builtins.str] = None,
        guess_mime_type_enabled: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        kms_encrypted: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        kms_key: typing.Optional[builtins.str] = None,
        nfs_file_share_defaults: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnNFSFileShare.NFSFileShareDefaultsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        notification_policy: typing.Optional[builtins.str] = None,
        object_acl: typing.Optional[builtins.str] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        requester_pays: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        squash: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_endpoint_dns_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::StorageGateway::NFSFileShare``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param gateway_arn: The ARN of the S3 File Gateway that hosts the share.
        :param location_arn: The ARN of the S3 bucket, or bucket prefix, the share exposes.
        :param role: The ARN of the IAM role the gateway assumes when it accesses the S3 location.
        :param audit_destination_arn: The ARN of the CloudWatch log group that receives the share's audit logs. Removing this property from a template detaches audit logging: the update sends the empty string, which the service treats as the reset.
        :param bucket_region: The Region of the S3 bucket, required when the bucket is reached through a VPC endpoint.
        :param cache_attributes: Refresh cache information for the file share. Removing this property from a template leaves the share's current value: the service documents no value that resets it.
        :param client_list: The IPv4 or IPv6 addresses and CIDR blocks permitted to mount the NFS share. Removing this property from a template leaves the share's current value: the service documents no value that resets it.
        :param default_storage_class: The S3 storage class for new objects. The service accepts S3_STANDARD, S3_INTELLIGENT_TIERING, S3_STANDARD_IA and S3_ONEZONE_IA; it is a length-bounded string in the API model rather than an enumeration.
        :param encryption_type: The server-side encryption the gateway applies to objects it writes.
        :param file_share_name: The name of the file share, which defaults to the bucket name when omitted. Removing this property from a template leaves the share's current value: the service documents no value that resets it.
        :param guess_mime_type_enabled: Whether the gateway infers the MIME type of uploaded objects from their extension.
        :param kms_encrypted: Deprecated by the service in favour of EncryptionType; true selects KMS encryption. Retained because it remains readable and settable.
        :param kms_key: The KMS key used for encryption, when EncryptionType selects KMS. Removing this property from a template leaves the share's current value: the service documents no value that resets it.
        :param nfs_file_share_defaults: Default values for the file and directory permissions of an NFS share. Removing this property from a template leaves the live values unchanged rather than clearing them, because the service has no reset for it: a create that omits the object leaves it absent, but the update path merges member by member keyed on the same internal sentinel that reports absence, so no request can restore that state. Set the members you want rather than relying on removal.
        :param notification_policy: The upload-notification settling period, as a JSON document.
        :param object_acl: The canned S3 ACL applied to objects the gateway writes.
        :param read_only: Whether clients may write to the share.
        :param requester_pays: Whether the bucket is a Requester Pays bucket.
        :param squash: How the NFS share maps client user IDs. The service accepts RootSquash, NoSquash and AllSquash; it is a length-bounded string in the API model rather than an enumeration.
        :param tags: Tags assigned to the file share.
        :param vpc_endpoint_dns_name: The DNS name of the S3 VPC endpoint the gateway uses to reach the bucket.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__7ef63c1a3284eb06e5bf240b6a307d7aa0f5ba59dc929caaff3babba37d53ef4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnNFSFileShareProps(
            gateway_arn=gateway_arn,
            location_arn=location_arn,
            role=role,
            audit_destination_arn=audit_destination_arn,
            bucket_region=bucket_region,
            cache_attributes=cache_attributes,
            client_list=client_list,
            default_storage_class=default_storage_class,
            encryption_type=encryption_type,
            file_share_name=file_share_name,
            guess_mime_type_enabled=guess_mime_type_enabled,
            kms_encrypted=kms_encrypted,
            kms_key=kms_key,
            nfs_file_share_defaults=nfs_file_share_defaults,
            notification_policy=notification_policy,
            object_acl=object_acl,
            read_only=read_only,
            requester_pays=requester_pays,
            squash=squash,
            tags=tags,
            vpc_endpoint_dns_name=vpc_endpoint_dns_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="isCfnNFSFileShare")
    @builtins.classmethod
    def is_cfn_nfs_file_share(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnNFSFileShare.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__0c1185683125ee8884d3836ce90d58776a2a5f56c4f69741839718006dc1dacc)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnNFSFileShare", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__96f0a0025a4b96ce1509ba648f96a294efc2d1f3ce65765ecb5dc9be93bd2273)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e37baa8f7d67c8d0b82cc3568a4b79928930ee9210e970bf56e24ea342b5de30)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    @builtins.classmethod
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrFileShareArn")
    def attr_file_share_arn(self) -> builtins.str:
        '''The ARN of the file share.

        :cloudformationAttribute: FileShareARN
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrFileShareArn"))

    @builtins.property
    @jsii.member(jsii_name="attrFileShareId")
    def attr_file_share_id(self) -> builtins.str:
        '''The ID of the file share.

        :cloudformationAttribute: FileShareId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrFileShareId"))

    @builtins.property
    @jsii.member(jsii_name="attrFileShareStatus")
    def attr_file_share_status(self) -> builtins.str:
        '''The status of the file share.

        The service reports CREATING, UPDATING, AVAILABLE, DELETING and FORCE_DELETING; it is a length-bounded string in the API model rather than an enumeration.

        :cloudformationAttribute: FileShareStatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrFileShareStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrPath")
    def attr_path(self) -> builtins.str:
        '''The export path the share is mounted or mapped at.

        :cloudformationAttribute: Path
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPath"))

    @builtins.property
    @jsii.member(jsii_name="cdkTagManager")
    def cdk_tag_manager(self) -> "_aws_cdk_0cae9daa.TagManager":
        '''Tag Manager which manages the tags for this resource.'''
        return typing.cast("_aws_cdk_0cae9daa.TagManager", jsii.get(self, "cdkTagManager"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="nfsFileShareRef")
    def nfs_file_share_ref(
        self,
    ) -> "_aws_storagegateway_f426d4c4.NFSFileShareReference":
        '''A reference to a NFSFileShare resource.'''
        return typing.cast("_aws_storagegateway_f426d4c4.NFSFileShareReference", jsii.get(self, "nfsFileShareRef"))

    @builtins.property
    @jsii.member(jsii_name="gatewayArn")
    def gateway_arn(self) -> builtins.str:
        '''The ARN of the S3 File Gateway that hosts the share.'''
        return typing.cast(builtins.str, jsii.get(self, "gatewayArn"))

    @gateway_arn.setter
    def gateway_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__53155bb263973ce3a9e5f2c0b76de8be7dce51f7d1799bfc33e51a1ab5dad3d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gatewayArn", value)

    @builtins.property
    @jsii.member(jsii_name="locationArn")
    def location_arn(self) -> builtins.str:
        '''The ARN of the S3 bucket, or bucket prefix, the share exposes.'''
        return typing.cast(builtins.str, jsii.get(self, "locationArn"))

    @location_arn.setter
    def location_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6f3e8e1e4709da66e338af5e419c5ee1990fe879cdfba8fe941e7b4213607a10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locationArn", value)

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        '''The ARN of the IAM role the gateway assumes when it accesses the S3 location.'''
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @role.setter
    def role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__85f3483626b68046b4759b86e6e1b0209668f20cc6b813e5398694ec752039a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "role", value)

    @builtins.property
    @jsii.member(jsii_name="auditDestinationArn")
    def audit_destination_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the CloudWatch log group that receives the share's audit logs.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "auditDestinationArn"))

    @audit_destination_arn.setter
    def audit_destination_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__851116e770cd210889ab05753d306a346224b088658634e3311b9cf905f06d95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "auditDestinationArn", value)

    @builtins.property
    @jsii.member(jsii_name="bucketRegion")
    def bucket_region(self) -> typing.Optional[builtins.str]:
        '''The Region of the S3 bucket, required when the bucket is reached through a VPC endpoint.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketRegion"))

    @bucket_region.setter
    def bucket_region(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ecfee355fac83f818940cdfa55b40a73ea9d5799d942ffc28b5c8178e159ea41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketRegion", value)

    @builtins.property
    @jsii.member(jsii_name="cacheAttributes")
    def cache_attributes(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnNFSFileShare.CacheAttributesProperty"]]:
        '''Refresh cache information for the file share.'''
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnNFSFileShare.CacheAttributesProperty"]], jsii.get(self, "cacheAttributes"))

    @cache_attributes.setter
    def cache_attributes(
        self,
        value: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnNFSFileShare.CacheAttributesProperty"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c967508d24c8c842c0f01aa7d8de77afbd08cf93d33b0621f30f7ed532cd3b51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheAttributes", value)

    @builtins.property
    @jsii.member(jsii_name="clientList")
    def client_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The IPv4 or IPv6 addresses and CIDR blocks permitted to mount the NFS share.'''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "clientList"))

    @client_list.setter
    def client_list(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__58fe1c1d70835fdba1afe70cc5e209fd51464559d9d354cbe878eb2a112c766d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientList", value)

    @builtins.property
    @jsii.member(jsii_name="defaultStorageClass")
    def default_storage_class(self) -> typing.Optional[builtins.str]:
        '''The S3 storage class for new objects.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultStorageClass"))

    @default_storage_class.setter
    def default_storage_class(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__846b61c9d9a9c51b702c72514dcce6073620fb97bbfcaf8f22bfd34892c92d34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultStorageClass", value)

    @builtins.property
    @jsii.member(jsii_name="encryptionType")
    def encryption_type(self) -> typing.Optional[builtins.str]:
        '''The server-side encryption the gateway applies to objects it writes.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionType"))

    @encryption_type.setter
    def encryption_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__43fc7b2154332f9a73494569e0d04083adbc5a77191e92ca445667e462749925)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionType", value)

    @builtins.property
    @jsii.member(jsii_name="fileShareName")
    def file_share_name(self) -> typing.Optional[builtins.str]:
        '''The name of the file share, which defaults to the bucket name when omitted.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileShareName"))

    @file_share_name.setter
    def file_share_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__148f53ee8b5859e717eb3f96d4407f9c1b6934a9d070ca024249e56bf1ec0feb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileShareName", value)

    @builtins.property
    @jsii.member(jsii_name="guessMimeTypeEnabled")
    def guess_mime_type_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Whether the gateway infers the MIME type of uploaded objects from their extension.'''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], jsii.get(self, "guessMimeTypeEnabled"))

    @guess_mime_type_enabled.setter
    def guess_mime_type_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__85bb9e909f255c5f3c749bab54fbd615c4b1d0cc114b3e9630a52b5e9063709a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "guessMimeTypeEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="kmsEncrypted")
    def kms_encrypted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Deprecated by the service in favour of EncryptionType;'''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], jsii.get(self, "kmsEncrypted"))

    @kms_encrypted.setter
    def kms_encrypted(
        self,
        value: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b47104c11c902f5223e9165a4b2544a4f7c32de36910080219aa3785e2fc15d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsEncrypted", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''The KMS key used for encryption, when EncryptionType selects KMS.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKey"))

    @kms_key.setter
    def kms_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__27a7e056ec32f4c1ed0cb2907fa43558008624cba8cc4d3fa2d66c09b9fc8b72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value)

    @builtins.property
    @jsii.member(jsii_name="nfsFileShareDefaults")
    def nfs_file_share_defaults(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnNFSFileShare.NFSFileShareDefaultsProperty"]]:
        '''Default values for the file and directory permissions of an NFS share.'''
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnNFSFileShare.NFSFileShareDefaultsProperty"]], jsii.get(self, "nfsFileShareDefaults"))

    @nfs_file_share_defaults.setter
    def nfs_file_share_defaults(
        self,
        value: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnNFSFileShare.NFSFileShareDefaultsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__aa4d188d7f07fd20222c301d8ededf842b3adbaab853908f285a2e5f34aac21c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nfsFileShareDefaults", value)

    @builtins.property
    @jsii.member(jsii_name="notificationPolicy")
    def notification_policy(self) -> typing.Optional[builtins.str]:
        '''The upload-notification settling period, as a JSON document.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notificationPolicy"))

    @notification_policy.setter
    def notification_policy(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b22cfea05dcaced75a3624aab81c94d685c87b0740a7969588051c112e1dd26a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="objectAcl")
    def object_acl(self) -> typing.Optional[builtins.str]:
        '''The canned S3 ACL applied to objects the gateway writes.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectAcl"))

    @object_acl.setter
    def object_acl(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__2d871fcb7ed387d48c95cf93b0fb16dc5613ffb9b7dfc632ec22197f5bf86eed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectAcl", value)

    @builtins.property
    @jsii.member(jsii_name="readOnly")
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Whether clients may write to the share.'''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], jsii.get(self, "readOnly"))

    @read_only.setter
    def read_only(
        self,
        value: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__13fd549d9d9a11181a11137d1fe05f4dfc1a1d4b391761e3c06f54ebc77194ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value)

    @builtins.property
    @jsii.member(jsii_name="requesterPays")
    def requester_pays(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Whether the bucket is a Requester Pays bucket.'''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], jsii.get(self, "requesterPays"))

    @requester_pays.setter
    def requester_pays(
        self,
        value: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__88460ec56bd29074ee994fb48a4e3ce9529f03c2d1b63d84cb5f8cf2510d82d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requesterPays", value)

    @builtins.property
    @jsii.member(jsii_name="squash")
    def squash(self) -> typing.Optional[builtins.str]:
        '''How the NFS share maps client user IDs.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "squash"))

    @squash.setter
    def squash(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__af099dacadf510ce80db3e5b75a49b97cea24d4bf88a2ce989dad363e7ec7803)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "squash", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''Tags assigned to the file share.'''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__8a08a8b45a5ed44fef3f50b814ec5cdc51e3a65d2b92fbeb45dd630ec33f0a6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="vpcEndpointDnsName")
    def vpc_endpoint_dns_name(self) -> typing.Optional[builtins.str]:
        '''The DNS name of the S3 VPC endpoint the gateway uses to reach the bucket.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcEndpointDnsName"))

    @vpc_endpoint_dns_name.setter
    def vpc_endpoint_dns_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__507903680420bfd15ce65af69b7b8443d63e48fa07017f926ab76186c97103c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcEndpointDnsName", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_storagegateway.CfnNFSFileShare.CacheAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={"cache_stale_timeout_in_seconds": "cacheStaleTimeoutInSeconds"},
    )
    class CacheAttributesProperty:
        def __init__(
            self,
            *,
            cache_stale_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Refresh cache information for the file share.

            Removing this property from a template leaves the share's current value: the service documents no value that resets it.

            :param cache_stale_timeout_in_seconds: How long the directory contents cached by the gateway are considered valid.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-storagegateway-nfsfileshare-cacheattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_storagegateway as storagegateway
                
                cache_attributes_property = storagegateway.CfnNFSFileShare.CacheAttributesProperty(
                    cache_stale_timeout_in_seconds=123
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__536adc436761db31735a84265405310a1264490dc2b23bd4adc8fc9d0b092eec)
                check_type(argname="argument cache_stale_timeout_in_seconds", value=cache_stale_timeout_in_seconds, expected_type=type_hints["cache_stale_timeout_in_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cache_stale_timeout_in_seconds is not None:
                self._values["cache_stale_timeout_in_seconds"] = cache_stale_timeout_in_seconds

        @builtins.property
        def cache_stale_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''How long the directory contents cached by the gateway are considered valid.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-storagegateway-nfsfileshare-cacheattributes.html#cfn-storagegateway-nfsfileshare-cacheattributes-cachestaletimeoutinseconds
            '''
            result = self._values.get("cache_stale_timeout_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CacheAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_storagegateway.CfnNFSFileShare.NFSFileShareDefaultsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "directory_mode": "directoryMode",
            "file_mode": "fileMode",
            "group_id": "groupId",
            "owner_id": "ownerId",
        },
    )
    class NFSFileShareDefaultsProperty:
        def __init__(
            self,
            *,
            directory_mode: typing.Optional[builtins.str] = None,
            file_mode: typing.Optional[builtins.str] = None,
            group_id: typing.Optional[jsii.Number] = None,
            owner_id: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Default values for the file and directory permissions of an NFS share.

            Removing this property from a template leaves the live values unchanged rather than clearing them, because the service has no reset for it: a create that omits the object leaves it absent, but the update path merges member by member keyed on the same internal sentinel that reports absence, so no request can restore that state. Set the members you want rather than relying on removal.

            :param directory_mode: The Unix directory mode in the form nnnn.
            :param file_mode: The Unix file mode in the form nnnn.
            :param group_id: The default group ID for files in the file share.
            :param owner_id: The default owner ID for files in the file share.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-storagegateway-nfsfileshare-nfsfilesharedefaults.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_storagegateway as storagegateway
                
                n_fs_file_share_defaults_property = storagegateway.CfnNFSFileShare.NFSFileShareDefaultsProperty(
                    directory_mode="directoryMode",
                    file_mode="fileMode",
                    group_id=123,
                    owner_id=123
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__e87af42d4132b4fbf18b2ddcf34339bbb3699f8be82e4bfe1d2b722804b92522)
                check_type(argname="argument directory_mode", value=directory_mode, expected_type=type_hints["directory_mode"])
                check_type(argname="argument file_mode", value=file_mode, expected_type=type_hints["file_mode"])
                check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
                check_type(argname="argument owner_id", value=owner_id, expected_type=type_hints["owner_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if directory_mode is not None:
                self._values["directory_mode"] = directory_mode
            if file_mode is not None:
                self._values["file_mode"] = file_mode
            if group_id is not None:
                self._values["group_id"] = group_id
            if owner_id is not None:
                self._values["owner_id"] = owner_id

        @builtins.property
        def directory_mode(self) -> typing.Optional[builtins.str]:
            '''The Unix directory mode in the form nnnn.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-storagegateway-nfsfileshare-nfsfilesharedefaults.html#cfn-storagegateway-nfsfileshare-nfsfilesharedefaults-directorymode
            '''
            result = self._values.get("directory_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def file_mode(self) -> typing.Optional[builtins.str]:
            '''The Unix file mode in the form nnnn.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-storagegateway-nfsfileshare-nfsfilesharedefaults.html#cfn-storagegateway-nfsfileshare-nfsfilesharedefaults-filemode
            '''
            result = self._values.get("file_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def group_id(self) -> typing.Optional[jsii.Number]:
            '''The default group ID for files in the file share.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-storagegateway-nfsfileshare-nfsfilesharedefaults.html#cfn-storagegateway-nfsfileshare-nfsfilesharedefaults-groupid
            '''
            result = self._values.get("group_id")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def owner_id(self) -> typing.Optional[jsii.Number]:
            '''The default owner ID for files in the file share.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-storagegateway-nfsfileshare-nfsfilesharedefaults.html#cfn-storagegateway-nfsfileshare-nfsfilesharedefaults-ownerid
            '''
            result = self._values.get("owner_id")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NFSFileShareDefaultsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_storagegateway.CfnNFSFileShareProps",
    jsii_struct_bases=[],
    name_mapping={
        "gateway_arn": "gatewayArn",
        "location_arn": "locationArn",
        "role": "role",
        "audit_destination_arn": "auditDestinationArn",
        "bucket_region": "bucketRegion",
        "cache_attributes": "cacheAttributes",
        "client_list": "clientList",
        "default_storage_class": "defaultStorageClass",
        "encryption_type": "encryptionType",
        "file_share_name": "fileShareName",
        "guess_mime_type_enabled": "guessMimeTypeEnabled",
        "kms_encrypted": "kmsEncrypted",
        "kms_key": "kmsKey",
        "nfs_file_share_defaults": "nfsFileShareDefaults",
        "notification_policy": "notificationPolicy",
        "object_acl": "objectAcl",
        "read_only": "readOnly",
        "requester_pays": "requesterPays",
        "squash": "squash",
        "tags": "tags",
        "vpc_endpoint_dns_name": "vpcEndpointDnsName",
    },
)
class CfnNFSFileShareProps:
    def __init__(
        self,
        *,
        gateway_arn: builtins.str,
        location_arn: builtins.str,
        role: builtins.str,
        audit_destination_arn: typing.Optional[builtins.str] = None,
        bucket_region: typing.Optional[builtins.str] = None,
        cache_attributes: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnNFSFileShare.CacheAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        client_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_storage_class: typing.Optional[builtins.str] = None,
        encryption_type: typing.Optional[builtins.str] = None,
        file_share_name: typing.Optional[builtins.str] = None,
        guess_mime_type_enabled: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        kms_encrypted: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        kms_key: typing.Optional[builtins.str] = None,
        nfs_file_share_defaults: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnNFSFileShare.NFSFileShareDefaultsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        notification_policy: typing.Optional[builtins.str] = None,
        object_acl: typing.Optional[builtins.str] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        requester_pays: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        squash: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_endpoint_dns_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnNFSFileShare``.

        :param gateway_arn: The ARN of the S3 File Gateway that hosts the share.
        :param location_arn: The ARN of the S3 bucket, or bucket prefix, the share exposes.
        :param role: The ARN of the IAM role the gateway assumes when it accesses the S3 location.
        :param audit_destination_arn: The ARN of the CloudWatch log group that receives the share's audit logs. Removing this property from a template detaches audit logging: the update sends the empty string, which the service treats as the reset.
        :param bucket_region: The Region of the S3 bucket, required when the bucket is reached through a VPC endpoint.
        :param cache_attributes: Refresh cache information for the file share. Removing this property from a template leaves the share's current value: the service documents no value that resets it.
        :param client_list: The IPv4 or IPv6 addresses and CIDR blocks permitted to mount the NFS share. Removing this property from a template leaves the share's current value: the service documents no value that resets it.
        :param default_storage_class: The S3 storage class for new objects. The service accepts S3_STANDARD, S3_INTELLIGENT_TIERING, S3_STANDARD_IA and S3_ONEZONE_IA; it is a length-bounded string in the API model rather than an enumeration.
        :param encryption_type: The server-side encryption the gateway applies to objects it writes.
        :param file_share_name: The name of the file share, which defaults to the bucket name when omitted. Removing this property from a template leaves the share's current value: the service documents no value that resets it.
        :param guess_mime_type_enabled: Whether the gateway infers the MIME type of uploaded objects from their extension.
        :param kms_encrypted: Deprecated by the service in favour of EncryptionType; true selects KMS encryption. Retained because it remains readable and settable.
        :param kms_key: The KMS key used for encryption, when EncryptionType selects KMS. Removing this property from a template leaves the share's current value: the service documents no value that resets it.
        :param nfs_file_share_defaults: Default values for the file and directory permissions of an NFS share. Removing this property from a template leaves the live values unchanged rather than clearing them, because the service has no reset for it: a create that omits the object leaves it absent, but the update path merges member by member keyed on the same internal sentinel that reports absence, so no request can restore that state. Set the members you want rather than relying on removal.
        :param notification_policy: The upload-notification settling period, as a JSON document.
        :param object_acl: The canned S3 ACL applied to objects the gateway writes.
        :param read_only: Whether clients may write to the share.
        :param requester_pays: Whether the bucket is a Requester Pays bucket.
        :param squash: How the NFS share maps client user IDs. The service accepts RootSquash, NoSquash and AllSquash; it is a length-bounded string in the API model rather than an enumeration.
        :param tags: Tags assigned to the file share.
        :param vpc_endpoint_dns_name: The DNS name of the S3 VPC endpoint the gateway uses to reach the bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-nfsfileshare.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_storagegateway as storagegateway
            
            cfn_nfs_file_share_props = storagegateway.CfnNFSFileShareProps(
                gateway_arn="gatewayArn",
                location_arn="locationArn",
                role="role",
            
                # the properties below are optional
                audit_destination_arn="auditDestinationArn",
                bucket_region="bucketRegion",
                cache_attributes=storagegateway.CfnNFSFileShare.CacheAttributesProperty(
                    cache_stale_timeout_in_seconds=123
                ),
                client_list=["clientList"],
                default_storage_class="defaultStorageClass",
                encryption_type="encryptionType",
                file_share_name="fileShareName",
                guess_mime_type_enabled=False,
                kms_encrypted=False,
                kms_key="kmsKey",
                nfs_file_share_defaults=storagegateway.CfnNFSFileShare.NFSFileShareDefaultsProperty(
                    directory_mode="directoryMode",
                    file_mode="fileMode",
                    group_id=123,
                    owner_id=123
                ),
                notification_policy="notificationPolicy",
                object_acl="objectAcl",
                read_only=False,
                requester_pays=False,
                squash="squash",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_endpoint_dns_name="vpcEndpointDnsName"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__741a7608895c12875c075fcd58a1ae221040db3c96eb08b0255df43b2ec93a5c)
            check_type(argname="argument gateway_arn", value=gateway_arn, expected_type=type_hints["gateway_arn"])
            check_type(argname="argument location_arn", value=location_arn, expected_type=type_hints["location_arn"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument audit_destination_arn", value=audit_destination_arn, expected_type=type_hints["audit_destination_arn"])
            check_type(argname="argument bucket_region", value=bucket_region, expected_type=type_hints["bucket_region"])
            check_type(argname="argument cache_attributes", value=cache_attributes, expected_type=type_hints["cache_attributes"])
            check_type(argname="argument client_list", value=client_list, expected_type=type_hints["client_list"])
            check_type(argname="argument default_storage_class", value=default_storage_class, expected_type=type_hints["default_storage_class"])
            check_type(argname="argument encryption_type", value=encryption_type, expected_type=type_hints["encryption_type"])
            check_type(argname="argument file_share_name", value=file_share_name, expected_type=type_hints["file_share_name"])
            check_type(argname="argument guess_mime_type_enabled", value=guess_mime_type_enabled, expected_type=type_hints["guess_mime_type_enabled"])
            check_type(argname="argument kms_encrypted", value=kms_encrypted, expected_type=type_hints["kms_encrypted"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument nfs_file_share_defaults", value=nfs_file_share_defaults, expected_type=type_hints["nfs_file_share_defaults"])
            check_type(argname="argument notification_policy", value=notification_policy, expected_type=type_hints["notification_policy"])
            check_type(argname="argument object_acl", value=object_acl, expected_type=type_hints["object_acl"])
            check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
            check_type(argname="argument requester_pays", value=requester_pays, expected_type=type_hints["requester_pays"])
            check_type(argname="argument squash", value=squash, expected_type=type_hints["squash"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_endpoint_dns_name", value=vpc_endpoint_dns_name, expected_type=type_hints["vpc_endpoint_dns_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "gateway_arn": gateway_arn,
            "location_arn": location_arn,
            "role": role,
        }
        if audit_destination_arn is not None:
            self._values["audit_destination_arn"] = audit_destination_arn
        if bucket_region is not None:
            self._values["bucket_region"] = bucket_region
        if cache_attributes is not None:
            self._values["cache_attributes"] = cache_attributes
        if client_list is not None:
            self._values["client_list"] = client_list
        if default_storage_class is not None:
            self._values["default_storage_class"] = default_storage_class
        if encryption_type is not None:
            self._values["encryption_type"] = encryption_type
        if file_share_name is not None:
            self._values["file_share_name"] = file_share_name
        if guess_mime_type_enabled is not None:
            self._values["guess_mime_type_enabled"] = guess_mime_type_enabled
        if kms_encrypted is not None:
            self._values["kms_encrypted"] = kms_encrypted
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if nfs_file_share_defaults is not None:
            self._values["nfs_file_share_defaults"] = nfs_file_share_defaults
        if notification_policy is not None:
            self._values["notification_policy"] = notification_policy
        if object_acl is not None:
            self._values["object_acl"] = object_acl
        if read_only is not None:
            self._values["read_only"] = read_only
        if requester_pays is not None:
            self._values["requester_pays"] = requester_pays
        if squash is not None:
            self._values["squash"] = squash
        if tags is not None:
            self._values["tags"] = tags
        if vpc_endpoint_dns_name is not None:
            self._values["vpc_endpoint_dns_name"] = vpc_endpoint_dns_name

    @builtins.property
    def gateway_arn(self) -> builtins.str:
        '''The ARN of the S3 File Gateway that hosts the share.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-nfsfileshare.html#cfn-storagegateway-nfsfileshare-gatewayarn
        '''
        result = self._values.get("gateway_arn")
        assert result is not None, "Required property 'gateway_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location_arn(self) -> builtins.str:
        '''The ARN of the S3 bucket, or bucket prefix, the share exposes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-nfsfileshare.html#cfn-storagegateway-nfsfileshare-locationarn
        '''
        result = self._values.get("location_arn")
        assert result is not None, "Required property 'location_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role(self) -> builtins.str:
        '''The ARN of the IAM role the gateway assumes when it accesses the S3 location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-nfsfileshare.html#cfn-storagegateway-nfsfileshare-role
        '''
        result = self._values.get("role")
        assert result is not None, "Required property 'role' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def audit_destination_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the CloudWatch log group that receives the share's audit logs.

        Removing this property from a template detaches audit logging: the update sends the empty string, which the service treats as the reset.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-nfsfileshare.html#cfn-storagegateway-nfsfileshare-auditdestinationarn
        '''
        result = self._values.get("audit_destination_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_region(self) -> typing.Optional[builtins.str]:
        '''The Region of the S3 bucket, required when the bucket is reached through a VPC endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-nfsfileshare.html#cfn-storagegateway-nfsfileshare-bucketregion
        '''
        result = self._values.get("bucket_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cache_attributes(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnNFSFileShare.CacheAttributesProperty"]]:
        '''Refresh cache information for the file share.

        Removing this property from a template leaves the share's current value: the service documents no value that resets it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-nfsfileshare.html#cfn-storagegateway-nfsfileshare-cacheattributes
        '''
        result = self._values.get("cache_attributes")
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnNFSFileShare.CacheAttributesProperty"]], result)

    @builtins.property
    def client_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The IPv4 or IPv6 addresses and CIDR blocks permitted to mount the NFS share.

        Removing this property from a template leaves the share's current value: the service documents no value that resets it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-nfsfileshare.html#cfn-storagegateway-nfsfileshare-clientlist
        '''
        result = self._values.get("client_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def default_storage_class(self) -> typing.Optional[builtins.str]:
        '''The S3 storage class for new objects.

        The service accepts S3_STANDARD, S3_INTELLIGENT_TIERING, S3_STANDARD_IA and S3_ONEZONE_IA; it is a length-bounded string in the API model rather than an enumeration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-nfsfileshare.html#cfn-storagegateway-nfsfileshare-defaultstorageclass
        '''
        result = self._values.get("default_storage_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_type(self) -> typing.Optional[builtins.str]:
        '''The server-side encryption the gateway applies to objects it writes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-nfsfileshare.html#cfn-storagegateway-nfsfileshare-encryptiontype
        '''
        result = self._values.get("encryption_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_share_name(self) -> typing.Optional[builtins.str]:
        '''The name of the file share, which defaults to the bucket name when omitted.

        Removing this property from a template leaves the share's current value: the service documents no value that resets it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-nfsfileshare.html#cfn-storagegateway-nfsfileshare-filesharename
        '''
        result = self._values.get("file_share_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def guess_mime_type_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Whether the gateway infers the MIME type of uploaded objects from their extension.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-nfsfileshare.html#cfn-storagegateway-nfsfileshare-guessmimetypeenabled
        '''
        result = self._values.get("guess_mime_type_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], result)

    @builtins.property
    def kms_encrypted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Deprecated by the service in favour of EncryptionType;

        true selects KMS encryption. Retained because it remains readable and settable.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-nfsfileshare.html#cfn-storagegateway-nfsfileshare-kmsencrypted
        '''
        result = self._values.get("kms_encrypted")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''The KMS key used for encryption, when EncryptionType selects KMS.

        Removing this property from a template leaves the share's current value: the service documents no value that resets it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-nfsfileshare.html#cfn-storagegateway-nfsfileshare-kmskey
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nfs_file_share_defaults(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnNFSFileShare.NFSFileShareDefaultsProperty"]]:
        '''Default values for the file and directory permissions of an NFS share.

        Removing this property from a template leaves the live values unchanged rather than clearing them, because the service has no reset for it: a create that omits the object leaves it absent, but the update path merges member by member keyed on the same internal sentinel that reports absence, so no request can restore that state. Set the members you want rather than relying on removal.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-nfsfileshare.html#cfn-storagegateway-nfsfileshare-nfsfilesharedefaults
        '''
        result = self._values.get("nfs_file_share_defaults")
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnNFSFileShare.NFSFileShareDefaultsProperty"]], result)

    @builtins.property
    def notification_policy(self) -> typing.Optional[builtins.str]:
        '''The upload-notification settling period, as a JSON document.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-nfsfileshare.html#cfn-storagegateway-nfsfileshare-notificationpolicy
        '''
        result = self._values.get("notification_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def object_acl(self) -> typing.Optional[builtins.str]:
        '''The canned S3 ACL applied to objects the gateway writes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-nfsfileshare.html#cfn-storagegateway-nfsfileshare-objectacl
        '''
        result = self._values.get("object_acl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Whether clients may write to the share.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-nfsfileshare.html#cfn-storagegateway-nfsfileshare-readonly
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], result)

    @builtins.property
    def requester_pays(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Whether the bucket is a Requester Pays bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-nfsfileshare.html#cfn-storagegateway-nfsfileshare-requesterpays
        '''
        result = self._values.get("requester_pays")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], result)

    @builtins.property
    def squash(self) -> typing.Optional[builtins.str]:
        '''How the NFS share maps client user IDs.

        The service accepts RootSquash, NoSquash and AllSquash; it is a length-bounded string in the API model rather than an enumeration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-nfsfileshare.html#cfn-storagegateway-nfsfileshare-squash
        '''
        result = self._values.get("squash")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''Tags assigned to the file share.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-nfsfileshare.html#cfn-storagegateway-nfsfileshare-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    @builtins.property
    def vpc_endpoint_dns_name(self) -> typing.Optional[builtins.str]:
        '''The DNS name of the S3 VPC endpoint the gateway uses to reach the bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-nfsfileshare.html#cfn-storagegateway-nfsfileshare-vpcendpointdnsname
        '''
        result = self._values.get("vpc_endpoint_dns_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnNFSFileShareProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_storagegateway_f426d4c4.ISMBFileShareRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnSMBFileShare(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_storagegateway.CfnSMBFileShare",
):
    '''Resource Type definition for AWS::StorageGateway::SMBFileShare.

    An SMB file share exposes an Amazon S3 bucket through a Storage Gateway file gateway, so clients read and write objects as files over SMB. The share's variant is fixed by its resource type rather than by a property: the service constructs the two variants with different APIs, and a property carrying the choice would belong to neither API's input.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-smbfileshare.html
    :cloudformationResource: AWS::StorageGateway::SMBFileShare
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_storagegateway as storagegateway
        
        cfn_smb_file_share = storagegateway.CfnSMBFileShare(self, "MyCfnSMBFileShare",
            gateway_arn="gatewayArn",
            location_arn="locationArn",
            role="role",
        
            # the properties below are optional
            access_based_enumeration=False,
            admin_user_list=["adminUserList"],
            audit_destination_arn="auditDestinationArn",
            authentication="authentication",
            bucket_region="bucketRegion",
            cache_attributes=storagegateway.CfnSMBFileShare.CacheAttributesProperty(
                cache_stale_timeout_in_seconds=123
            ),
            case_sensitivity="caseSensitivity",
            default_storage_class="defaultStorageClass",
            encryption_type="encryptionType",
            file_share_name="fileShareName",
            guess_mime_type_enabled=False,
            invalid_user_list=["invalidUserList"],
            kms_encrypted=False,
            kms_key="kmsKey",
            notification_policy="notificationPolicy",
            object_acl="objectAcl",
            oplocks_enabled=False,
            read_only=False,
            requester_pays=False,
            smbacl_enabled=False,
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            valid_user_list=["validUserList"],
            vpc_endpoint_dns_name="vpcEndpointDnsName"
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        gateway_arn: builtins.str,
        location_arn: builtins.str,
        role: builtins.str,
        access_based_enumeration: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        admin_user_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        audit_destination_arn: typing.Optional[builtins.str] = None,
        authentication: typing.Optional[builtins.str] = None,
        bucket_region: typing.Optional[builtins.str] = None,
        cache_attributes: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnSMBFileShare.CacheAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        case_sensitivity: typing.Optional[builtins.str] = None,
        default_storage_class: typing.Optional[builtins.str] = None,
        encryption_type: typing.Optional[builtins.str] = None,
        file_share_name: typing.Optional[builtins.str] = None,
        guess_mime_type_enabled: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        invalid_user_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        kms_encrypted: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        kms_key: typing.Optional[builtins.str] = None,
        notification_policy: typing.Optional[builtins.str] = None,
        object_acl: typing.Optional[builtins.str] = None,
        oplocks_enabled: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        requester_pays: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        smbacl_enabled: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
        valid_user_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc_endpoint_dns_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::StorageGateway::SMBFileShare``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param gateway_arn: The ARN of the S3 File Gateway that hosts the share.
        :param location_arn: The ARN of the S3 bucket, or bucket prefix, the share exposes.
        :param role: The ARN of the IAM role the gateway assumes when it accesses the S3 location.
        :param access_based_enumeration: Whether clients see only the files and folders they may access.
        :param admin_user_list: Users and groups granted administrative privileges on the SMB share.
        :param audit_destination_arn: The ARN of the CloudWatch log group that receives the share's audit logs. Removing this property from a template detaches audit logging: the update sends the empty string, which the service treats as the reset.
        :param authentication: The authentication the SMB share uses. The service accepts ActiveDirectory and GuestAccess; it is a length-bounded string in the API model rather than an enumeration.
        :param bucket_region: The Region of the S3 bucket, required when the bucket is reached through a VPC endpoint.
        :param cache_attributes: Refresh cache information for the file share. Removing this property from a template leaves the share's current value: the service documents no value that resets it.
        :param case_sensitivity: Whether the SMB share is case sensitive or defers to the client.
        :param default_storage_class: The S3 storage class for new objects. The service accepts S3_STANDARD, S3_INTELLIGENT_TIERING, S3_STANDARD_IA and S3_ONEZONE_IA; it is a length-bounded string in the API model rather than an enumeration.
        :param encryption_type: The server-side encryption the gateway applies to objects it writes.
        :param file_share_name: The name of the file share, which defaults to the bucket name when omitted. Removing this property from a template leaves the share's current value: the service documents no value that resets it.
        :param guess_mime_type_enabled: Whether the gateway infers the MIME type of uploaded objects from their extension.
        :param invalid_user_list: Users and groups denied access to the SMB share.
        :param kms_encrypted: Deprecated by the service in favour of EncryptionType; true selects KMS encryption. Retained because it remains readable and settable.
        :param kms_key: The KMS key used for encryption, when EncryptionType selects KMS. Removing this property from a template leaves the share's current value: the service documents no value that resets it.
        :param notification_policy: The upload-notification settling period, as a JSON document.
        :param object_acl: The canned S3 ACL applied to objects the gateway writes.
        :param oplocks_enabled: Whether the SMB share grants opportunistic locks. Removing this property from a template leaves the live value unchanged rather than restoring the created default, because that default depends on the gateway's software version -- opportunistic locking is enabled by default only on appliances at 1.19.0.0 or above -- and the version is not part of this resource. Set the value explicitly rather than relying on removal.
        :param read_only: Whether clients may write to the share.
        :param requester_pays: Whether the bucket is a Requester Pays bucket.
        :param smbacl_enabled: Whether the SMB share uses Windows ACLs rather than POSIX permissions.
        :param tags: Tags assigned to the file share.
        :param valid_user_list: Users and groups permitted to access the SMB share.
        :param vpc_endpoint_dns_name: The DNS name of the S3 VPC endpoint the gateway uses to reach the bucket.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__0d6bb5e76e3bfd08c7e205da1ce11d1dbbad406ac72865b79b0124c6ecc2a865)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSMBFileShareProps(
            gateway_arn=gateway_arn,
            location_arn=location_arn,
            role=role,
            access_based_enumeration=access_based_enumeration,
            admin_user_list=admin_user_list,
            audit_destination_arn=audit_destination_arn,
            authentication=authentication,
            bucket_region=bucket_region,
            cache_attributes=cache_attributes,
            case_sensitivity=case_sensitivity,
            default_storage_class=default_storage_class,
            encryption_type=encryption_type,
            file_share_name=file_share_name,
            guess_mime_type_enabled=guess_mime_type_enabled,
            invalid_user_list=invalid_user_list,
            kms_encrypted=kms_encrypted,
            kms_key=kms_key,
            notification_policy=notification_policy,
            object_acl=object_acl,
            oplocks_enabled=oplocks_enabled,
            read_only=read_only,
            requester_pays=requester_pays,
            smbacl_enabled=smbacl_enabled,
            tags=tags,
            valid_user_list=valid_user_list,
            vpc_endpoint_dns_name=vpc_endpoint_dns_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="isCfnSMBFileShare")
    @builtins.classmethod
    def is_cfn_smb_file_share(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnSMBFileShare.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__aa2f2fb851dc7b3a0160b4bc79e157532796e26aa58dd9e47cca559f61b70a99)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnSMBFileShare", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__2952cd8e0e1de99556d1f14043692590b78f7e059aba21e8beefdb3b49f6cfa9)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e5c11900f02ffaecdc0c153147d58275cea721b94221790e744948f887782997)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    @builtins.classmethod
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrFileShareArn")
    def attr_file_share_arn(self) -> builtins.str:
        '''The ARN of the file share.

        :cloudformationAttribute: FileShareARN
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrFileShareArn"))

    @builtins.property
    @jsii.member(jsii_name="attrFileShareId")
    def attr_file_share_id(self) -> builtins.str:
        '''The ID of the file share.

        :cloudformationAttribute: FileShareId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrFileShareId"))

    @builtins.property
    @jsii.member(jsii_name="attrFileShareStatus")
    def attr_file_share_status(self) -> builtins.str:
        '''The status of the file share.

        The service reports CREATING, UPDATING, AVAILABLE, DELETING and FORCE_DELETING; it is a length-bounded string in the API model rather than an enumeration.

        :cloudformationAttribute: FileShareStatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrFileShareStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrPath")
    def attr_path(self) -> builtins.str:
        '''The export path the share is mounted or mapped at.

        :cloudformationAttribute: Path
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPath"))

    @builtins.property
    @jsii.member(jsii_name="cdkTagManager")
    def cdk_tag_manager(self) -> "_aws_cdk_0cae9daa.TagManager":
        '''Tag Manager which manages the tags for this resource.'''
        return typing.cast("_aws_cdk_0cae9daa.TagManager", jsii.get(self, "cdkTagManager"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="smbFileShareRef")
    def smb_file_share_ref(
        self,
    ) -> "_aws_storagegateway_f426d4c4.SMBFileShareReference":
        '''A reference to a SMBFileShare resource.'''
        return typing.cast("_aws_storagegateway_f426d4c4.SMBFileShareReference", jsii.get(self, "smbFileShareRef"))

    @builtins.property
    @jsii.member(jsii_name="gatewayArn")
    def gateway_arn(self) -> builtins.str:
        '''The ARN of the S3 File Gateway that hosts the share.'''
        return typing.cast(builtins.str, jsii.get(self, "gatewayArn"))

    @gateway_arn.setter
    def gateway_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__94a3e907858c6cbfca5d6e824321158c80d5141a8029e4b9571467c38a54b774)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gatewayArn", value)

    @builtins.property
    @jsii.member(jsii_name="locationArn")
    def location_arn(self) -> builtins.str:
        '''The ARN of the S3 bucket, or bucket prefix, the share exposes.'''
        return typing.cast(builtins.str, jsii.get(self, "locationArn"))

    @location_arn.setter
    def location_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__0bdc9e88265f90023f2c4a1eff8a693428bf1f616d7a5ed00b0c1a318a42075a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locationArn", value)

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        '''The ARN of the IAM role the gateway assumes when it accesses the S3 location.'''
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @role.setter
    def role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__af5b503d360be9b2de28b2bfd7519d8de746ea86e14c290e773852e082bcb1e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "role", value)

    @builtins.property
    @jsii.member(jsii_name="accessBasedEnumeration")
    def access_based_enumeration(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Whether clients see only the files and folders they may access.'''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], jsii.get(self, "accessBasedEnumeration"))

    @access_based_enumeration.setter
    def access_based_enumeration(
        self,
        value: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__85df24584502d0bf371ebb7e7bbe6c20793e3135b0ff7225de37dfc007f1da0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessBasedEnumeration", value)

    @builtins.property
    @jsii.member(jsii_name="adminUserList")
    def admin_user_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Users and groups granted administrative privileges on the SMB share.'''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "adminUserList"))

    @admin_user_list.setter
    def admin_user_list(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__dec1c106ec5fff369b90e170f1d456a214c69657d0ffc831e7916468b7b08c3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminUserList", value)

    @builtins.property
    @jsii.member(jsii_name="auditDestinationArn")
    def audit_destination_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the CloudWatch log group that receives the share's audit logs.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "auditDestinationArn"))

    @audit_destination_arn.setter
    def audit_destination_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d8ca1a82707bc3db43d1a40c58f4ddf69a9ea4a9ffb23934d8b521fc3c3e24c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "auditDestinationArn", value)

    @builtins.property
    @jsii.member(jsii_name="authentication")
    def authentication(self) -> typing.Optional[builtins.str]:
        '''The authentication the SMB share uses.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authentication"))

    @authentication.setter
    def authentication(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__fa50f11d8c76a0e4c87b50619757f632477611e3f887b9892edfc0776516a41d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authentication", value)

    @builtins.property
    @jsii.member(jsii_name="bucketRegion")
    def bucket_region(self) -> typing.Optional[builtins.str]:
        '''The Region of the S3 bucket, required when the bucket is reached through a VPC endpoint.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketRegion"))

    @bucket_region.setter
    def bucket_region(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6f9680c7a89d371b5827c7cf3b1a7ccf962841f4af5c23a0a095a87805890e57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketRegion", value)

    @builtins.property
    @jsii.member(jsii_name="cacheAttributes")
    def cache_attributes(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnSMBFileShare.CacheAttributesProperty"]]:
        '''Refresh cache information for the file share.'''
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnSMBFileShare.CacheAttributesProperty"]], jsii.get(self, "cacheAttributes"))

    @cache_attributes.setter
    def cache_attributes(
        self,
        value: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnSMBFileShare.CacheAttributesProperty"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d17d6f8978747ebb37e5e06e137530bcf93d05e77a0872f24636de884e36279c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheAttributes", value)

    @builtins.property
    @jsii.member(jsii_name="caseSensitivity")
    def case_sensitivity(self) -> typing.Optional[builtins.str]:
        '''Whether the SMB share is case sensitive or defers to the client.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "caseSensitivity"))

    @case_sensitivity.setter
    def case_sensitivity(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6a872099b2cd659541d1c208e9584391b4e23a57adcfc5bb578de0668e0c3858)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caseSensitivity", value)

    @builtins.property
    @jsii.member(jsii_name="defaultStorageClass")
    def default_storage_class(self) -> typing.Optional[builtins.str]:
        '''The S3 storage class for new objects.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultStorageClass"))

    @default_storage_class.setter
    def default_storage_class(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ef6376f6854dab2c7a8a3a750830665070d99fc74579e94238ee3136177704b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultStorageClass", value)

    @builtins.property
    @jsii.member(jsii_name="encryptionType")
    def encryption_type(self) -> typing.Optional[builtins.str]:
        '''The server-side encryption the gateway applies to objects it writes.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionType"))

    @encryption_type.setter
    def encryption_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6b51829ae2c28f2d69b672f4389c6c01681e11d4342c505746dbc21037f0aee3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionType", value)

    @builtins.property
    @jsii.member(jsii_name="fileShareName")
    def file_share_name(self) -> typing.Optional[builtins.str]:
        '''The name of the file share, which defaults to the bucket name when omitted.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileShareName"))

    @file_share_name.setter
    def file_share_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a73a22858d1a68e5652ba15c03c4d11e94c3e6bcdb3d52d68082690ff08b4a69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileShareName", value)

    @builtins.property
    @jsii.member(jsii_name="guessMimeTypeEnabled")
    def guess_mime_type_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Whether the gateway infers the MIME type of uploaded objects from their extension.'''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], jsii.get(self, "guessMimeTypeEnabled"))

    @guess_mime_type_enabled.setter
    def guess_mime_type_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__db41ec01c93215225838b459984262d37db3ac2a4ca00bb553e323052f216def)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "guessMimeTypeEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="invalidUserList")
    def invalid_user_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Users and groups denied access to the SMB share.'''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "invalidUserList"))

    @invalid_user_list.setter
    def invalid_user_list(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__945ec0159776e271724e8c48a573501880be85e73c6b0c95d2077f84fb14796c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invalidUserList", value)

    @builtins.property
    @jsii.member(jsii_name="kmsEncrypted")
    def kms_encrypted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Deprecated by the service in favour of EncryptionType;'''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], jsii.get(self, "kmsEncrypted"))

    @kms_encrypted.setter
    def kms_encrypted(
        self,
        value: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__715f75c3a39191a34932f3b493b4d4a29bc7afa37c16944229e32f1afae61899)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsEncrypted", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''The KMS key used for encryption, when EncryptionType selects KMS.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKey"))

    @kms_key.setter
    def kms_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__8ca48bb7e8df73fd2251ce341a7b69379c8e6f23196dc12f09dbc689aa7bf80f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value)

    @builtins.property
    @jsii.member(jsii_name="notificationPolicy")
    def notification_policy(self) -> typing.Optional[builtins.str]:
        '''The upload-notification settling period, as a JSON document.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notificationPolicy"))

    @notification_policy.setter
    def notification_policy(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e8ae7905fa41b2bc4e90ee792c16279cb22f4b0e627bc6bfd006929df28460fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="objectAcl")
    def object_acl(self) -> typing.Optional[builtins.str]:
        '''The canned S3 ACL applied to objects the gateway writes.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectAcl"))

    @object_acl.setter
    def object_acl(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3e0708a578d7594fcedd855b2819ebaa94a421402afc7d53298ef7f07139efa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectAcl", value)

    @builtins.property
    @jsii.member(jsii_name="oplocksEnabled")
    def oplocks_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Whether the SMB share grants opportunistic locks.'''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], jsii.get(self, "oplocksEnabled"))

    @oplocks_enabled.setter
    def oplocks_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__722ac7cf59e36cc000d6d09702358efdea6a4d992d1e403c240509df0d67e83e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oplocksEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="readOnly")
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Whether clients may write to the share.'''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], jsii.get(self, "readOnly"))

    @read_only.setter
    def read_only(
        self,
        value: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1e4538b395b0c7805353f2d34b6aa14f10659d91b91aad0ae91e7e82f1d7075a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value)

    @builtins.property
    @jsii.member(jsii_name="requesterPays")
    def requester_pays(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Whether the bucket is a Requester Pays bucket.'''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], jsii.get(self, "requesterPays"))

    @requester_pays.setter
    def requester_pays(
        self,
        value: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d52a2b5e396e18a8840cb0a693d3efdcb90ec550427e73242e023b92066cbfa1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requesterPays", value)

    @builtins.property
    @jsii.member(jsii_name="smbaclEnabled")
    def smbacl_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Whether the SMB share uses Windows ACLs rather than POSIX permissions.'''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], jsii.get(self, "smbaclEnabled"))

    @smbacl_enabled.setter
    def smbacl_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__406978e9ef07a5ae055fd473d8e06592063b4954ea39e495931132a5b2590c59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "smbaclEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''Tags assigned to the file share.'''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e3a32bcc5e5e849d91c51015e4ce02da661ec4f18ded7113a1b022e70807404a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="validUserList")
    def valid_user_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Users and groups permitted to access the SMB share.'''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "validUserList"))

    @valid_user_list.setter
    def valid_user_list(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__60234f0dc8233bfe2510847a086df7412f8f60f50f91bac0cdea39bfa0652d49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validUserList", value)

    @builtins.property
    @jsii.member(jsii_name="vpcEndpointDnsName")
    def vpc_endpoint_dns_name(self) -> typing.Optional[builtins.str]:
        '''The DNS name of the S3 VPC endpoint the gateway uses to reach the bucket.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcEndpointDnsName"))

    @vpc_endpoint_dns_name.setter
    def vpc_endpoint_dns_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ab2eb11dae31778936a83e019d01b5742cd8cf1fe5c83008fe70c81dd2b3cc7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcEndpointDnsName", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_storagegateway.CfnSMBFileShare.CacheAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={"cache_stale_timeout_in_seconds": "cacheStaleTimeoutInSeconds"},
    )
    class CacheAttributesProperty:
        def __init__(
            self,
            *,
            cache_stale_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Refresh cache information for the file share.

            Removing this property from a template leaves the share's current value: the service documents no value that resets it.

            :param cache_stale_timeout_in_seconds: How long the directory contents cached by the gateway are considered valid.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-storagegateway-smbfileshare-cacheattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_storagegateway as storagegateway
                
                cache_attributes_property = storagegateway.CfnSMBFileShare.CacheAttributesProperty(
                    cache_stale_timeout_in_seconds=123
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__3ab3dd1647fc75ea364afc0c3c9d5f6069e78fdf71d8d5ea4ccc1a3ff51e266d)
                check_type(argname="argument cache_stale_timeout_in_seconds", value=cache_stale_timeout_in_seconds, expected_type=type_hints["cache_stale_timeout_in_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cache_stale_timeout_in_seconds is not None:
                self._values["cache_stale_timeout_in_seconds"] = cache_stale_timeout_in_seconds

        @builtins.property
        def cache_stale_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''How long the directory contents cached by the gateway are considered valid.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-storagegateway-smbfileshare-cacheattributes.html#cfn-storagegateway-smbfileshare-cacheattributes-cachestaletimeoutinseconds
            '''
            result = self._values.get("cache_stale_timeout_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CacheAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_storagegateway.CfnSMBFileShareProps",
    jsii_struct_bases=[],
    name_mapping={
        "gateway_arn": "gatewayArn",
        "location_arn": "locationArn",
        "role": "role",
        "access_based_enumeration": "accessBasedEnumeration",
        "admin_user_list": "adminUserList",
        "audit_destination_arn": "auditDestinationArn",
        "authentication": "authentication",
        "bucket_region": "bucketRegion",
        "cache_attributes": "cacheAttributes",
        "case_sensitivity": "caseSensitivity",
        "default_storage_class": "defaultStorageClass",
        "encryption_type": "encryptionType",
        "file_share_name": "fileShareName",
        "guess_mime_type_enabled": "guessMimeTypeEnabled",
        "invalid_user_list": "invalidUserList",
        "kms_encrypted": "kmsEncrypted",
        "kms_key": "kmsKey",
        "notification_policy": "notificationPolicy",
        "object_acl": "objectAcl",
        "oplocks_enabled": "oplocksEnabled",
        "read_only": "readOnly",
        "requester_pays": "requesterPays",
        "smbacl_enabled": "smbaclEnabled",
        "tags": "tags",
        "valid_user_list": "validUserList",
        "vpc_endpoint_dns_name": "vpcEndpointDnsName",
    },
)
class CfnSMBFileShareProps:
    def __init__(
        self,
        *,
        gateway_arn: builtins.str,
        location_arn: builtins.str,
        role: builtins.str,
        access_based_enumeration: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        admin_user_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        audit_destination_arn: typing.Optional[builtins.str] = None,
        authentication: typing.Optional[builtins.str] = None,
        bucket_region: typing.Optional[builtins.str] = None,
        cache_attributes: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnSMBFileShare.CacheAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        case_sensitivity: typing.Optional[builtins.str] = None,
        default_storage_class: typing.Optional[builtins.str] = None,
        encryption_type: typing.Optional[builtins.str] = None,
        file_share_name: typing.Optional[builtins.str] = None,
        guess_mime_type_enabled: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        invalid_user_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        kms_encrypted: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        kms_key: typing.Optional[builtins.str] = None,
        notification_policy: typing.Optional[builtins.str] = None,
        object_acl: typing.Optional[builtins.str] = None,
        oplocks_enabled: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        requester_pays: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        smbacl_enabled: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
        valid_user_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc_endpoint_dns_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnSMBFileShare``.

        :param gateway_arn: The ARN of the S3 File Gateway that hosts the share.
        :param location_arn: The ARN of the S3 bucket, or bucket prefix, the share exposes.
        :param role: The ARN of the IAM role the gateway assumes when it accesses the S3 location.
        :param access_based_enumeration: Whether clients see only the files and folders they may access.
        :param admin_user_list: Users and groups granted administrative privileges on the SMB share.
        :param audit_destination_arn: The ARN of the CloudWatch log group that receives the share's audit logs. Removing this property from a template detaches audit logging: the update sends the empty string, which the service treats as the reset.
        :param authentication: The authentication the SMB share uses. The service accepts ActiveDirectory and GuestAccess; it is a length-bounded string in the API model rather than an enumeration.
        :param bucket_region: The Region of the S3 bucket, required when the bucket is reached through a VPC endpoint.
        :param cache_attributes: Refresh cache information for the file share. Removing this property from a template leaves the share's current value: the service documents no value that resets it.
        :param case_sensitivity: Whether the SMB share is case sensitive or defers to the client.
        :param default_storage_class: The S3 storage class for new objects. The service accepts S3_STANDARD, S3_INTELLIGENT_TIERING, S3_STANDARD_IA and S3_ONEZONE_IA; it is a length-bounded string in the API model rather than an enumeration.
        :param encryption_type: The server-side encryption the gateway applies to objects it writes.
        :param file_share_name: The name of the file share, which defaults to the bucket name when omitted. Removing this property from a template leaves the share's current value: the service documents no value that resets it.
        :param guess_mime_type_enabled: Whether the gateway infers the MIME type of uploaded objects from their extension.
        :param invalid_user_list: Users and groups denied access to the SMB share.
        :param kms_encrypted: Deprecated by the service in favour of EncryptionType; true selects KMS encryption. Retained because it remains readable and settable.
        :param kms_key: The KMS key used for encryption, when EncryptionType selects KMS. Removing this property from a template leaves the share's current value: the service documents no value that resets it.
        :param notification_policy: The upload-notification settling period, as a JSON document.
        :param object_acl: The canned S3 ACL applied to objects the gateway writes.
        :param oplocks_enabled: Whether the SMB share grants opportunistic locks. Removing this property from a template leaves the live value unchanged rather than restoring the created default, because that default depends on the gateway's software version -- opportunistic locking is enabled by default only on appliances at 1.19.0.0 or above -- and the version is not part of this resource. Set the value explicitly rather than relying on removal.
        :param read_only: Whether clients may write to the share.
        :param requester_pays: Whether the bucket is a Requester Pays bucket.
        :param smbacl_enabled: Whether the SMB share uses Windows ACLs rather than POSIX permissions.
        :param tags: Tags assigned to the file share.
        :param valid_user_list: Users and groups permitted to access the SMB share.
        :param vpc_endpoint_dns_name: The DNS name of the S3 VPC endpoint the gateway uses to reach the bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-smbfileshare.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_storagegateway as storagegateway
            
            cfn_smb_file_share_props = storagegateway.CfnSMBFileShareProps(
                gateway_arn="gatewayArn",
                location_arn="locationArn",
                role="role",
            
                # the properties below are optional
                access_based_enumeration=False,
                admin_user_list=["adminUserList"],
                audit_destination_arn="auditDestinationArn",
                authentication="authentication",
                bucket_region="bucketRegion",
                cache_attributes=storagegateway.CfnSMBFileShare.CacheAttributesProperty(
                    cache_stale_timeout_in_seconds=123
                ),
                case_sensitivity="caseSensitivity",
                default_storage_class="defaultStorageClass",
                encryption_type="encryptionType",
                file_share_name="fileShareName",
                guess_mime_type_enabled=False,
                invalid_user_list=["invalidUserList"],
                kms_encrypted=False,
                kms_key="kmsKey",
                notification_policy="notificationPolicy",
                object_acl="objectAcl",
                oplocks_enabled=False,
                read_only=False,
                requester_pays=False,
                smbacl_enabled=False,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                valid_user_list=["validUserList"],
                vpc_endpoint_dns_name="vpcEndpointDnsName"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__8282ebf6180403a4ae32ac9a75091ca13ed4abcc284bef166c4b01e91ddebd97)
            check_type(argname="argument gateway_arn", value=gateway_arn, expected_type=type_hints["gateway_arn"])
            check_type(argname="argument location_arn", value=location_arn, expected_type=type_hints["location_arn"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument access_based_enumeration", value=access_based_enumeration, expected_type=type_hints["access_based_enumeration"])
            check_type(argname="argument admin_user_list", value=admin_user_list, expected_type=type_hints["admin_user_list"])
            check_type(argname="argument audit_destination_arn", value=audit_destination_arn, expected_type=type_hints["audit_destination_arn"])
            check_type(argname="argument authentication", value=authentication, expected_type=type_hints["authentication"])
            check_type(argname="argument bucket_region", value=bucket_region, expected_type=type_hints["bucket_region"])
            check_type(argname="argument cache_attributes", value=cache_attributes, expected_type=type_hints["cache_attributes"])
            check_type(argname="argument case_sensitivity", value=case_sensitivity, expected_type=type_hints["case_sensitivity"])
            check_type(argname="argument default_storage_class", value=default_storage_class, expected_type=type_hints["default_storage_class"])
            check_type(argname="argument encryption_type", value=encryption_type, expected_type=type_hints["encryption_type"])
            check_type(argname="argument file_share_name", value=file_share_name, expected_type=type_hints["file_share_name"])
            check_type(argname="argument guess_mime_type_enabled", value=guess_mime_type_enabled, expected_type=type_hints["guess_mime_type_enabled"])
            check_type(argname="argument invalid_user_list", value=invalid_user_list, expected_type=type_hints["invalid_user_list"])
            check_type(argname="argument kms_encrypted", value=kms_encrypted, expected_type=type_hints["kms_encrypted"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument notification_policy", value=notification_policy, expected_type=type_hints["notification_policy"])
            check_type(argname="argument object_acl", value=object_acl, expected_type=type_hints["object_acl"])
            check_type(argname="argument oplocks_enabled", value=oplocks_enabled, expected_type=type_hints["oplocks_enabled"])
            check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
            check_type(argname="argument requester_pays", value=requester_pays, expected_type=type_hints["requester_pays"])
            check_type(argname="argument smbacl_enabled", value=smbacl_enabled, expected_type=type_hints["smbacl_enabled"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument valid_user_list", value=valid_user_list, expected_type=type_hints["valid_user_list"])
            check_type(argname="argument vpc_endpoint_dns_name", value=vpc_endpoint_dns_name, expected_type=type_hints["vpc_endpoint_dns_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "gateway_arn": gateway_arn,
            "location_arn": location_arn,
            "role": role,
        }
        if access_based_enumeration is not None:
            self._values["access_based_enumeration"] = access_based_enumeration
        if admin_user_list is not None:
            self._values["admin_user_list"] = admin_user_list
        if audit_destination_arn is not None:
            self._values["audit_destination_arn"] = audit_destination_arn
        if authentication is not None:
            self._values["authentication"] = authentication
        if bucket_region is not None:
            self._values["bucket_region"] = bucket_region
        if cache_attributes is not None:
            self._values["cache_attributes"] = cache_attributes
        if case_sensitivity is not None:
            self._values["case_sensitivity"] = case_sensitivity
        if default_storage_class is not None:
            self._values["default_storage_class"] = default_storage_class
        if encryption_type is not None:
            self._values["encryption_type"] = encryption_type
        if file_share_name is not None:
            self._values["file_share_name"] = file_share_name
        if guess_mime_type_enabled is not None:
            self._values["guess_mime_type_enabled"] = guess_mime_type_enabled
        if invalid_user_list is not None:
            self._values["invalid_user_list"] = invalid_user_list
        if kms_encrypted is not None:
            self._values["kms_encrypted"] = kms_encrypted
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if notification_policy is not None:
            self._values["notification_policy"] = notification_policy
        if object_acl is not None:
            self._values["object_acl"] = object_acl
        if oplocks_enabled is not None:
            self._values["oplocks_enabled"] = oplocks_enabled
        if read_only is not None:
            self._values["read_only"] = read_only
        if requester_pays is not None:
            self._values["requester_pays"] = requester_pays
        if smbacl_enabled is not None:
            self._values["smbacl_enabled"] = smbacl_enabled
        if tags is not None:
            self._values["tags"] = tags
        if valid_user_list is not None:
            self._values["valid_user_list"] = valid_user_list
        if vpc_endpoint_dns_name is not None:
            self._values["vpc_endpoint_dns_name"] = vpc_endpoint_dns_name

    @builtins.property
    def gateway_arn(self) -> builtins.str:
        '''The ARN of the S3 File Gateway that hosts the share.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-smbfileshare.html#cfn-storagegateway-smbfileshare-gatewayarn
        '''
        result = self._values.get("gateway_arn")
        assert result is not None, "Required property 'gateway_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location_arn(self) -> builtins.str:
        '''The ARN of the S3 bucket, or bucket prefix, the share exposes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-smbfileshare.html#cfn-storagegateway-smbfileshare-locationarn
        '''
        result = self._values.get("location_arn")
        assert result is not None, "Required property 'location_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role(self) -> builtins.str:
        '''The ARN of the IAM role the gateway assumes when it accesses the S3 location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-smbfileshare.html#cfn-storagegateway-smbfileshare-role
        '''
        result = self._values.get("role")
        assert result is not None, "Required property 'role' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_based_enumeration(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Whether clients see only the files and folders they may access.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-smbfileshare.html#cfn-storagegateway-smbfileshare-accessbasedenumeration
        '''
        result = self._values.get("access_based_enumeration")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], result)

    @builtins.property
    def admin_user_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Users and groups granted administrative privileges on the SMB share.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-smbfileshare.html#cfn-storagegateway-smbfileshare-adminuserlist
        '''
        result = self._values.get("admin_user_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def audit_destination_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the CloudWatch log group that receives the share's audit logs.

        Removing this property from a template detaches audit logging: the update sends the empty string, which the service treats as the reset.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-smbfileshare.html#cfn-storagegateway-smbfileshare-auditdestinationarn
        '''
        result = self._values.get("audit_destination_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authentication(self) -> typing.Optional[builtins.str]:
        '''The authentication the SMB share uses.

        The service accepts ActiveDirectory and GuestAccess; it is a length-bounded string in the API model rather than an enumeration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-smbfileshare.html#cfn-storagegateway-smbfileshare-authentication
        '''
        result = self._values.get("authentication")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_region(self) -> typing.Optional[builtins.str]:
        '''The Region of the S3 bucket, required when the bucket is reached through a VPC endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-smbfileshare.html#cfn-storagegateway-smbfileshare-bucketregion
        '''
        result = self._values.get("bucket_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cache_attributes(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnSMBFileShare.CacheAttributesProperty"]]:
        '''Refresh cache information for the file share.

        Removing this property from a template leaves the share's current value: the service documents no value that resets it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-smbfileshare.html#cfn-storagegateway-smbfileshare-cacheattributes
        '''
        result = self._values.get("cache_attributes")
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnSMBFileShare.CacheAttributesProperty"]], result)

    @builtins.property
    def case_sensitivity(self) -> typing.Optional[builtins.str]:
        '''Whether the SMB share is case sensitive or defers to the client.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-smbfileshare.html#cfn-storagegateway-smbfileshare-casesensitivity
        '''
        result = self._values.get("case_sensitivity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_storage_class(self) -> typing.Optional[builtins.str]:
        '''The S3 storage class for new objects.

        The service accepts S3_STANDARD, S3_INTELLIGENT_TIERING, S3_STANDARD_IA and S3_ONEZONE_IA; it is a length-bounded string in the API model rather than an enumeration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-smbfileshare.html#cfn-storagegateway-smbfileshare-defaultstorageclass
        '''
        result = self._values.get("default_storage_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_type(self) -> typing.Optional[builtins.str]:
        '''The server-side encryption the gateway applies to objects it writes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-smbfileshare.html#cfn-storagegateway-smbfileshare-encryptiontype
        '''
        result = self._values.get("encryption_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_share_name(self) -> typing.Optional[builtins.str]:
        '''The name of the file share, which defaults to the bucket name when omitted.

        Removing this property from a template leaves the share's current value: the service documents no value that resets it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-smbfileshare.html#cfn-storagegateway-smbfileshare-filesharename
        '''
        result = self._values.get("file_share_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def guess_mime_type_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Whether the gateway infers the MIME type of uploaded objects from their extension.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-smbfileshare.html#cfn-storagegateway-smbfileshare-guessmimetypeenabled
        '''
        result = self._values.get("guess_mime_type_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], result)

    @builtins.property
    def invalid_user_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Users and groups denied access to the SMB share.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-smbfileshare.html#cfn-storagegateway-smbfileshare-invaliduserlist
        '''
        result = self._values.get("invalid_user_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def kms_encrypted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Deprecated by the service in favour of EncryptionType;

        true selects KMS encryption. Retained because it remains readable and settable.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-smbfileshare.html#cfn-storagegateway-smbfileshare-kmsencrypted
        '''
        result = self._values.get("kms_encrypted")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''The KMS key used for encryption, when EncryptionType selects KMS.

        Removing this property from a template leaves the share's current value: the service documents no value that resets it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-smbfileshare.html#cfn-storagegateway-smbfileshare-kmskey
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_policy(self) -> typing.Optional[builtins.str]:
        '''The upload-notification settling period, as a JSON document.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-smbfileshare.html#cfn-storagegateway-smbfileshare-notificationpolicy
        '''
        result = self._values.get("notification_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def object_acl(self) -> typing.Optional[builtins.str]:
        '''The canned S3 ACL applied to objects the gateway writes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-smbfileshare.html#cfn-storagegateway-smbfileshare-objectacl
        '''
        result = self._values.get("object_acl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oplocks_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Whether the SMB share grants opportunistic locks.

        Removing this property from a template leaves the live value unchanged rather than restoring the created default, because that default depends on the gateway's software version -- opportunistic locking is enabled by default only on appliances at 1.19.0.0 or above -- and the version is not part of this resource. Set the value explicitly rather than relying on removal.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-smbfileshare.html#cfn-storagegateway-smbfileshare-oplocksenabled
        '''
        result = self._values.get("oplocks_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Whether clients may write to the share.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-smbfileshare.html#cfn-storagegateway-smbfileshare-readonly
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], result)

    @builtins.property
    def requester_pays(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Whether the bucket is a Requester Pays bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-smbfileshare.html#cfn-storagegateway-smbfileshare-requesterpays
        '''
        result = self._values.get("requester_pays")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], result)

    @builtins.property
    def smbacl_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Whether the SMB share uses Windows ACLs rather than POSIX permissions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-smbfileshare.html#cfn-storagegateway-smbfileshare-smbaclenabled
        '''
        result = self._values.get("smbacl_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''Tags assigned to the file share.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-smbfileshare.html#cfn-storagegateway-smbfileshare-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    @builtins.property
    def valid_user_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Users and groups permitted to access the SMB share.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-smbfileshare.html#cfn-storagegateway-smbfileshare-validuserlist
        '''
        result = self._values.get("valid_user_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def vpc_endpoint_dns_name(self) -> typing.Optional[builtins.str]:
        '''The DNS name of the S3 VPC endpoint the gateway uses to reach the bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-smbfileshare.html#cfn-storagegateway-smbfileshare-vpcendpointdnsname
        '''
        result = self._values.get("vpc_endpoint_dns_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSMBFileShareProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_storagegateway_f426d4c4.ITapeRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnTape(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_storagegateway.CfnTape",
):
    '''Creates a virtual tape with a user-defined barcode on a Tape Gateway (VTL).

    A virtual tape is stored in Amazon S3 and can be archived to S3 Glacier or S3 Glacier Deep Archive.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-tape.html
    :cloudformationResource: AWS::StorageGateway::Tape
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_storagegateway as storagegateway
        
        cfn_tape = storagegateway.CfnTape(self, "MyCfnTape",
            gateway_arn="gatewayArn",
            tape_size_in_bytes=123,
        
            # the properties below are optional
            kms_encrypted=False,
            kms_key="kmsKey",
            pool_id="poolId",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            tape_barcode="tapeBarcode",
            worm=False
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        gateway_arn: builtins.str,
        tape_size_in_bytes: jsii.Number,
        kms_encrypted: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        kms_key: typing.Optional[builtins.str] = None,
        pool_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
        tape_barcode: typing.Optional[builtins.str] = None,
        worm: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
    ) -> None:
        '''Create a new ``AWS::StorageGateway::Tape``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param gateway_arn: The Amazon Resource Name (ARN) of the Tape Gateway that hosts the virtual tape.
        :param tape_size_in_bytes: The size, in bytes, of the virtual tape that you want to create.
        :param kms_encrypted: Set to true to use Amazon S3 server-side encryption with your own KMS key, or false to use a key managed by Amazon S3. Optional.
        :param kms_key: The Amazon Resource Name (ARN) of a symmetric customer master key (CMK) used for Amazon S3 server-side encryption. This value must be set if KMSEncrypted is true.
        :param pool_id: The ID of the pool that you want to add your tape to for archiving. Tapes in this pool are archived in the S3 storage class that is associated with the pool.
        :param tags: A list of up to 50 tags to assign to the virtual tape.
        :param tape_barcode: The barcode that you want to assign to the virtual tape. Barcodes cannot be reused, even after a tape is deleted.
        :param worm: Set to true to create a write-once-read-many (WORM) virtual tape.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__363b2f7813c184123160ffaf59a488211565913fb5126a1fa69bcb36310d32dc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnTapeProps(
            gateway_arn=gateway_arn,
            tape_size_in_bytes=tape_size_in_bytes,
            kms_encrypted=kms_encrypted,
            kms_key=kms_key,
            pool_id=pool_id,
            tags=tags,
            tape_barcode=tape_barcode,
            worm=worm,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForTape")
    @builtins.classmethod
    def arn_for_tape(
        cls,
        resource: "_aws_storagegateway_f426d4c4.ITapeRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ae610be3890fbb42584972211b0c5af3006370462c1bf3c6c3b219eb44a03b39)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForTape", [resource]))

    @jsii.member(jsii_name="isCfnTape")
    @builtins.classmethod
    def is_cfn_tape(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnTape.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ebb8f5d769e86e9451e9c5e5b3470e03b5d0dfb0c67afc78fc0e8c2598c707dd)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnTape", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__bd33548844c3c66482e5960a6a6f61789c9af04eb374db35a888509e0a56ab58)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__7ae0da0b888c3ffbaa5eb6cd82d55bf20a66d98c9c309e38a2589910332683ed)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    @builtins.classmethod
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrTapeArn")
    def attr_tape_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the virtual tape.

        :cloudformationAttribute: TapeARN
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrTapeArn"))

    @builtins.property
    @jsii.member(jsii_name="attrTapeCreatedDate")
    def attr_tape_created_date(self) -> builtins.str:
        '''The date and time that the virtual tape was created.

        :cloudformationAttribute: TapeCreatedDate
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrTapeCreatedDate"))

    @builtins.property
    @jsii.member(jsii_name="attrTapeStatus")
    def attr_tape_status(self) -> builtins.str:
        '''The current status of the virtual tape.

        :cloudformationAttribute: TapeStatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrTapeStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrTapeUsedInBytes")
    def attr_tape_used_in_bytes(self) -> "_aws_cdk_0cae9daa.IResolvable":
        '''The size, in bytes, of data stored on the virtual tape.

        :cloudformationAttribute: TapeUsedInBytes
        '''
        return typing.cast("_aws_cdk_0cae9daa.IResolvable", jsii.get(self, "attrTapeUsedInBytes"))

    @builtins.property
    @jsii.member(jsii_name="cdkTagManager")
    def cdk_tag_manager(self) -> "_aws_cdk_0cae9daa.TagManager":
        '''Tag Manager which manages the tags for this resource.'''
        return typing.cast("_aws_cdk_0cae9daa.TagManager", jsii.get(self, "cdkTagManager"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="tapeRef")
    def tape_ref(self) -> "_aws_storagegateway_f426d4c4.TapeReference":
        '''A reference to a Tape resource.'''
        return typing.cast("_aws_storagegateway_f426d4c4.TapeReference", jsii.get(self, "tapeRef"))

    @builtins.property
    @jsii.member(jsii_name="gatewayArn")
    def gateway_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the Tape Gateway that hosts the virtual tape.'''
        return typing.cast(builtins.str, jsii.get(self, "gatewayArn"))

    @gateway_arn.setter
    def gateway_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__662f1b01cec9fb4c578c1bbb30288dbf38679b5353e5dda5dbd320ef43291325)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gatewayArn", value)

    @builtins.property
    @jsii.member(jsii_name="tapeSizeInBytes")
    def tape_size_in_bytes(self) -> jsii.Number:
        '''The size, in bytes, of the virtual tape that you want to create.'''
        return typing.cast(jsii.Number, jsii.get(self, "tapeSizeInBytes"))

    @tape_size_in_bytes.setter
    def tape_size_in_bytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__020d09dce3e65ad2aaf95651a3b71d13e7e4491b13562a0833109864a3cdaa0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tapeSizeInBytes", value)

    @builtins.property
    @jsii.member(jsii_name="kmsEncrypted")
    def kms_encrypted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Set to true to use Amazon S3 server-side encryption with your own KMS key, or false to use a key managed by Amazon S3.'''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], jsii.get(self, "kmsEncrypted"))

    @kms_encrypted.setter
    def kms_encrypted(
        self,
        value: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ee66a67c862d78755548260dd465bb54d1d4135b9bbb9ac1bae6ba2ea3475fe8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsEncrypted", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of a symmetric customer master key (CMK) used for Amazon S3 server-side encryption.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKey"))

    @kms_key.setter
    def kms_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e1696f2d90ac34d1befe0d8f8fdff10c6a152824cfb1cea61f78cb3c939d074b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value)

    @builtins.property
    @jsii.member(jsii_name="poolId")
    def pool_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the pool that you want to add your tape to for archiving.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "poolId"))

    @pool_id.setter
    def pool_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__771aea9bb34cd7a52d93c075fca8422288c8149c586c2433579b77e674bbc411)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "poolId", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''A list of up to 50 tags to assign to the virtual tape.'''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b43111da63c8804b5553828beed62e0fc46e21d09e17e06cfa23a83a7d5f7756)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="tapeBarcode")
    def tape_barcode(self) -> typing.Optional[builtins.str]:
        '''The barcode that you want to assign to the virtual tape.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tapeBarcode"))

    @tape_barcode.setter
    def tape_barcode(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__5023431719ea44a143693a72e05f0b2a264ee01337c78f4ade43d1fe0d4746bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tapeBarcode", value)

    @builtins.property
    @jsii.member(jsii_name="worm")
    def worm(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Set to true to create a write-once-read-many (WORM) virtual tape.'''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], jsii.get(self, "worm"))

    @worm.setter
    def worm(
        self,
        value: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__cdca3fd4b57f957db6910289a79178f6960086b883d0e146cdbbf55066ade533)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "worm", value)


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_storagegateway_f426d4c4.ITapePoolRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnTapePool(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_storagegateway.CfnTapePool",
):
    '''Creates a custom tape pool for archiving virtual tapes with optional retention lock.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-tapepool.html
    :cloudformationResource: AWS::StorageGateway::TapePool
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_storagegateway as storagegateway
        
        cfn_tape_pool = storagegateway.CfnTapePool(self, "MyCfnTapePool",
            pool_name="poolName",
            storage_class="storageClass",
        
            # the properties below are optional
            retention_lock_time_in_days=123,
            retention_lock_type="retentionLockType",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        pool_name: builtins.str,
        storage_class: builtins.str,
        retention_lock_time_in_days: typing.Optional[jsii.Number] = None,
        retention_lock_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::StorageGateway::TapePool``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param pool_name: The name of the custom tape pool.
        :param storage_class: The storage class associated with the custom pool (S3 Glacier or S3 Glacier Deep Archive).
        :param retention_lock_time_in_days: Tape retention lock time in days (up to 36,500 days / 100 years).
        :param retention_lock_type: Tape retention lock type. Governance mode allows authorized removal; compliance mode prevents all removal.
        :param tags: A list of up to 50 tags for the tape pool.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ac2c1692ba4edccb604aef75af4b88463d090c7db3c8f08741d200a884adedac)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnTapePoolProps(
            pool_name=pool_name,
            storage_class=storage_class,
            retention_lock_time_in_days=retention_lock_time_in_days,
            retention_lock_type=retention_lock_type,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForTapePool")
    @builtins.classmethod
    def arn_for_tape_pool(
        cls,
        resource: "_aws_storagegateway_f426d4c4.ITapePoolRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3bdaa23426ff87911afa19f9997f4ea57420c29c61fc1892987875628fdf638b)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForTapePool", [resource]))

    @jsii.member(jsii_name="fromPoolId")
    @builtins.classmethod
    def from_pool_id(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        pool_id: builtins.str,
    ) -> "_aws_storagegateway_f426d4c4.ITapePoolRef":
        '''Creates a new ITapePoolRef from a poolId.

        :param scope: -
        :param id: -
        :param pool_id: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a8b4c436c83b9aad89b0f338e63d3ef15cdc1d6880fa6e5c24369f59ab7d5e34)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument pool_id", value=pool_id, expected_type=type_hints["pool_id"])
        return typing.cast("_aws_storagegateway_f426d4c4.ITapePoolRef", jsii.sinvoke(cls, "fromPoolId", [scope, id, pool_id]))

    @jsii.member(jsii_name="isCfnTapePool")
    @builtins.classmethod
    def is_cfn_tape_pool(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnTapePool.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__4f4ac6b6ba23515dcc27d4c5a84961fe7a159a83305f9188d9b81d341eac359a)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnTapePool", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__bb3a41212781376c4f3874b92a3aeae3808be50104fb587f50096ee25d9cbdfe)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__9a89e9380fc69f21f542d0c5d15978f09dbb5fc7563f2badbf156059dafb2775)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    @builtins.classmethod
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrPoolArn")
    def attr_pool_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the custom tape pool.

        :cloudformationAttribute: PoolARN
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPoolArn"))

    @builtins.property
    @jsii.member(jsii_name="attrPoolId")
    def attr_pool_id(self) -> builtins.str:
        '''The unique identifier of the custom tape pool, extracted from the ARN.

        :cloudformationAttribute: PoolId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPoolId"))

    @builtins.property
    @jsii.member(jsii_name="cdkTagManager")
    def cdk_tag_manager(self) -> "_aws_cdk_0cae9daa.TagManager":
        '''Tag Manager which manages the tags for this resource.'''
        return typing.cast("_aws_cdk_0cae9daa.TagManager", jsii.get(self, "cdkTagManager"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="tapePoolRef")
    def tape_pool_ref(self) -> "_aws_storagegateway_f426d4c4.TapePoolReference":
        '''A reference to a TapePool resource.'''
        return typing.cast("_aws_storagegateway_f426d4c4.TapePoolReference", jsii.get(self, "tapePoolRef"))

    @builtins.property
    @jsii.member(jsii_name="poolName")
    def pool_name(self) -> builtins.str:
        '''The name of the custom tape pool.'''
        return typing.cast(builtins.str, jsii.get(self, "poolName"))

    @pool_name.setter
    def pool_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e2aa2850a80df094617446432f9ff1341cc436487f9fdcde124fff6e23224b3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "poolName", value)

    @builtins.property
    @jsii.member(jsii_name="storageClass")
    def storage_class(self) -> builtins.str:
        '''The storage class associated with the custom pool (S3 Glacier or S3 Glacier Deep Archive).'''
        return typing.cast(builtins.str, jsii.get(self, "storageClass"))

    @storage_class.setter
    def storage_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__59e6b638819f00096b40770703546150877b22e670bd72107418a00ab661a3c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageClass", value)

    @builtins.property
    @jsii.member(jsii_name="retentionLockTimeInDays")
    def retention_lock_time_in_days(self) -> typing.Optional[jsii.Number]:
        '''Tape retention lock time in days (up to 36,500 days / 100 years).'''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionLockTimeInDays"))

    @retention_lock_time_in_days.setter
    def retention_lock_time_in_days(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f9a75e037e394e1a483c9c37c628c1a3fd5236ed311d296563d7c92ed300cf84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionLockTimeInDays", value)

    @builtins.property
    @jsii.member(jsii_name="retentionLockType")
    def retention_lock_type(self) -> typing.Optional[builtins.str]:
        '''Tape retention lock type.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "retentionLockType"))

    @retention_lock_type.setter
    def retention_lock_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__4607d71dfda14f2f335c62ade52d5f18924d070d446cf3004dcb39ec784be160)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionLockType", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''A list of up to 50 tags for the tape pool.'''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3795fcc974a44ec324d8e597cdf4de7162f69066e260ed1f4273fc3bc7275cc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_storagegateway.CfnTapePoolProps",
    jsii_struct_bases=[],
    name_mapping={
        "pool_name": "poolName",
        "storage_class": "storageClass",
        "retention_lock_time_in_days": "retentionLockTimeInDays",
        "retention_lock_type": "retentionLockType",
        "tags": "tags",
    },
)
class CfnTapePoolProps:
    def __init__(
        self,
        *,
        pool_name: builtins.str,
        storage_class: builtins.str,
        retention_lock_time_in_days: typing.Optional[jsii.Number] = None,
        retention_lock_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnTapePool``.

        :param pool_name: The name of the custom tape pool.
        :param storage_class: The storage class associated with the custom pool (S3 Glacier or S3 Glacier Deep Archive).
        :param retention_lock_time_in_days: Tape retention lock time in days (up to 36,500 days / 100 years).
        :param retention_lock_type: Tape retention lock type. Governance mode allows authorized removal; compliance mode prevents all removal.
        :param tags: A list of up to 50 tags for the tape pool.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-tapepool.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_storagegateway as storagegateway
            
            cfn_tape_pool_props = storagegateway.CfnTapePoolProps(
                pool_name="poolName",
                storage_class="storageClass",
            
                # the properties below are optional
                retention_lock_time_in_days=123,
                retention_lock_type="retentionLockType",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__313c929df3254bd85bbd9d06cbd71bce8cccb516d3867f49894385585d8f30e9)
            check_type(argname="argument pool_name", value=pool_name, expected_type=type_hints["pool_name"])
            check_type(argname="argument storage_class", value=storage_class, expected_type=type_hints["storage_class"])
            check_type(argname="argument retention_lock_time_in_days", value=retention_lock_time_in_days, expected_type=type_hints["retention_lock_time_in_days"])
            check_type(argname="argument retention_lock_type", value=retention_lock_type, expected_type=type_hints["retention_lock_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pool_name": pool_name,
            "storage_class": storage_class,
        }
        if retention_lock_time_in_days is not None:
            self._values["retention_lock_time_in_days"] = retention_lock_time_in_days
        if retention_lock_type is not None:
            self._values["retention_lock_type"] = retention_lock_type
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def pool_name(self) -> builtins.str:
        '''The name of the custom tape pool.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-tapepool.html#cfn-storagegateway-tapepool-poolname
        '''
        result = self._values.get("pool_name")
        assert result is not None, "Required property 'pool_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_class(self) -> builtins.str:
        '''The storage class associated with the custom pool (S3 Glacier or S3 Glacier Deep Archive).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-tapepool.html#cfn-storagegateway-tapepool-storageclass
        '''
        result = self._values.get("storage_class")
        assert result is not None, "Required property 'storage_class' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def retention_lock_time_in_days(self) -> typing.Optional[jsii.Number]:
        '''Tape retention lock time in days (up to 36,500 days / 100 years).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-tapepool.html#cfn-storagegateway-tapepool-retentionlocktimeindays
        '''
        result = self._values.get("retention_lock_time_in_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retention_lock_type(self) -> typing.Optional[builtins.str]:
        '''Tape retention lock type.

        Governance mode allows authorized removal; compliance mode prevents all removal.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-tapepool.html#cfn-storagegateway-tapepool-retentionlocktype
        '''
        result = self._values.get("retention_lock_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''A list of up to 50 tags for the tape pool.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-tapepool.html#cfn-storagegateway-tapepool-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTapePoolProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_storagegateway.CfnTapeProps",
    jsii_struct_bases=[],
    name_mapping={
        "gateway_arn": "gatewayArn",
        "tape_size_in_bytes": "tapeSizeInBytes",
        "kms_encrypted": "kmsEncrypted",
        "kms_key": "kmsKey",
        "pool_id": "poolId",
        "tags": "tags",
        "tape_barcode": "tapeBarcode",
        "worm": "worm",
    },
)
class CfnTapeProps:
    def __init__(
        self,
        *,
        gateway_arn: builtins.str,
        tape_size_in_bytes: jsii.Number,
        kms_encrypted: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        kms_key: typing.Optional[builtins.str] = None,
        pool_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
        tape_barcode: typing.Optional[builtins.str] = None,
        worm: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
    ) -> None:
        '''Properties for defining a ``CfnTape``.

        :param gateway_arn: The Amazon Resource Name (ARN) of the Tape Gateway that hosts the virtual tape.
        :param tape_size_in_bytes: The size, in bytes, of the virtual tape that you want to create.
        :param kms_encrypted: Set to true to use Amazon S3 server-side encryption with your own KMS key, or false to use a key managed by Amazon S3. Optional.
        :param kms_key: The Amazon Resource Name (ARN) of a symmetric customer master key (CMK) used for Amazon S3 server-side encryption. This value must be set if KMSEncrypted is true.
        :param pool_id: The ID of the pool that you want to add your tape to for archiving. Tapes in this pool are archived in the S3 storage class that is associated with the pool.
        :param tags: A list of up to 50 tags to assign to the virtual tape.
        :param tape_barcode: The barcode that you want to assign to the virtual tape. Barcodes cannot be reused, even after a tape is deleted.
        :param worm: Set to true to create a write-once-read-many (WORM) virtual tape.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-tape.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_storagegateway as storagegateway
            
            cfn_tape_props = storagegateway.CfnTapeProps(
                gateway_arn="gatewayArn",
                tape_size_in_bytes=123,
            
                # the properties below are optional
                kms_encrypted=False,
                kms_key="kmsKey",
                pool_id="poolId",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                tape_barcode="tapeBarcode",
                worm=False
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__aa2d145c5722622b5c7cd133c48409678c375141152fd14546bec9a5731ba577)
            check_type(argname="argument gateway_arn", value=gateway_arn, expected_type=type_hints["gateway_arn"])
            check_type(argname="argument tape_size_in_bytes", value=tape_size_in_bytes, expected_type=type_hints["tape_size_in_bytes"])
            check_type(argname="argument kms_encrypted", value=kms_encrypted, expected_type=type_hints["kms_encrypted"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument pool_id", value=pool_id, expected_type=type_hints["pool_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tape_barcode", value=tape_barcode, expected_type=type_hints["tape_barcode"])
            check_type(argname="argument worm", value=worm, expected_type=type_hints["worm"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "gateway_arn": gateway_arn,
            "tape_size_in_bytes": tape_size_in_bytes,
        }
        if kms_encrypted is not None:
            self._values["kms_encrypted"] = kms_encrypted
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if pool_id is not None:
            self._values["pool_id"] = pool_id
        if tags is not None:
            self._values["tags"] = tags
        if tape_barcode is not None:
            self._values["tape_barcode"] = tape_barcode
        if worm is not None:
            self._values["worm"] = worm

    @builtins.property
    def gateway_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the Tape Gateway that hosts the virtual tape.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-tape.html#cfn-storagegateway-tape-gatewayarn
        '''
        result = self._values.get("gateway_arn")
        assert result is not None, "Required property 'gateway_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tape_size_in_bytes(self) -> jsii.Number:
        '''The size, in bytes, of the virtual tape that you want to create.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-tape.html#cfn-storagegateway-tape-tapesizeinbytes
        '''
        result = self._values.get("tape_size_in_bytes")
        assert result is not None, "Required property 'tape_size_in_bytes' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def kms_encrypted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Set to true to use Amazon S3 server-side encryption with your own KMS key, or false to use a key managed by Amazon S3.

        Optional.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-tape.html#cfn-storagegateway-tape-kmsencrypted
        '''
        result = self._values.get("kms_encrypted")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of a symmetric customer master key (CMK) used for Amazon S3 server-side encryption.

        This value must be set if KMSEncrypted is true.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-tape.html#cfn-storagegateway-tape-kmskey
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pool_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the pool that you want to add your tape to for archiving.

        Tapes in this pool are archived in the S3 storage class that is associated with the pool.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-tape.html#cfn-storagegateway-tape-poolid
        '''
        result = self._values.get("pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''A list of up to 50 tags to assign to the virtual tape.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-tape.html#cfn-storagegateway-tape-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    @builtins.property
    def tape_barcode(self) -> typing.Optional[builtins.str]:
        '''The barcode that you want to assign to the virtual tape.

        Barcodes cannot be reused, even after a tape is deleted.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-tape.html#cfn-storagegateway-tape-tapebarcode
        '''
        result = self._values.get("tape_barcode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def worm(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Set to true to create a write-once-read-many (WORM) virtual tape.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-tape.html#cfn-storagegateway-tape-worm
        '''
        result = self._values.get("worm")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTapeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_storagegateway_f426d4c4.IVolumeRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnVolume(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_storagegateway.CfnVolume",
):
    '''Creates a cached iSCSI volume on a Storage Gateway.

    A cached volume stores data in Amazon S3 and retains a copy of frequently accessed data subsets locally.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-volume.html
    :cloudformationResource: AWS::StorageGateway::Volume
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_storagegateway as storagegateway
        
        cfn_volume = storagegateway.CfnVolume(self, "MyCfnVolume",
            gateway_arn="gatewayArn",
            network_interface_id="networkInterfaceId",
            target_name="targetName",
            volume_size_in_bytes=123,
        
            # the properties below are optional
            kms_encrypted=False,
            kms_key="kmsKey",
            snapshot_id="snapshotId",
            source_volume_arn="sourceVolumeArn",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        gateway_arn: builtins.str,
        network_interface_id: builtins.str,
        target_name: builtins.str,
        volume_size_in_bytes: jsii.Number,
        kms_encrypted: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        kms_key: typing.Optional[builtins.str] = None,
        snapshot_id: typing.Optional[builtins.str] = None,
        source_volume_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::StorageGateway::Volume``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param gateway_arn: The Amazon Resource Name (ARN) of the gateway on which to create the volume.
        :param network_interface_id: The network interface of the gateway on which to expose the iSCSI target. Only IPv4 addresses are accepted.
        :param target_name: The name of the iSCSI target used by an initiator to connect to a volume and used as a suffix for the target ARN.
        :param volume_size_in_bytes: The size of the volume in bytes.
        :param kms_encrypted: Set to true to use Amazon S3 server-side encryption with your own KMS key, or false to use a key managed by Amazon S3.
        :param kms_key: The Amazon Resource Name (ARN) of a symmetric customer master key (CMK) used for Amazon S3 server-side encryption.
        :param snapshot_id: The snapshot ID of the snapshot to restore as the new cached volume (e.g., snap-1122aabb).
        :param source_volume_arn: The ARN of an existing volume from which to create the new volume.
        :param tags: A list of up to 50 tags to assign to the volume.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__271ddda20ad6264f77cc2f79555b3fa6ea997c8e5dccba6d566d2dcf154f898f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnVolumeProps(
            gateway_arn=gateway_arn,
            network_interface_id=network_interface_id,
            target_name=target_name,
            volume_size_in_bytes=volume_size_in_bytes,
            kms_encrypted=kms_encrypted,
            kms_key=kms_key,
            snapshot_id=snapshot_id,
            source_volume_arn=source_volume_arn,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForVolume")
    @builtins.classmethod
    def arn_for_volume(
        cls,
        resource: "_aws_storagegateway_f426d4c4.IVolumeRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__bf4b04a4849965fc4cd022c8e0fd09da482cd62aef80e780fb96a074696e4817)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForVolume", [resource]))

    @jsii.member(jsii_name="isCfnVolume")
    @builtins.classmethod
    def is_cfn_volume(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnVolume.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__8697be7703a6f5458994a17690dde8dd46e21cc40628f1a0720415688dddf65b)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnVolume", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__10e0a5d67c599ccc35a189f881ed3e303c2f2e0453a222f914017c743a9e364d)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__21658029a19b77c6623b63fe0a949fb1e70c240363e99c57a2637e632dc6f9b3)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    @builtins.classmethod
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedDate")
    def attr_created_date(self) -> builtins.str:
        '''The date the volume was created.

        :cloudformationAttribute: CreatedDate
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedDate"))

    @builtins.property
    @jsii.member(jsii_name="attrTargetArn")
    def attr_target_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the volume target, which includes the iSCSI target name.

        :cloudformationAttribute: TargetARN
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrTargetArn"))

    @builtins.property
    @jsii.member(jsii_name="attrVolumeArn")
    def attr_volume_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the storage volume.

        :cloudformationAttribute: VolumeARN
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVolumeArn"))

    @builtins.property
    @jsii.member(jsii_name="attrVolumeAttachmentStatus")
    def attr_volume_attachment_status(self) -> builtins.str:
        '''Indicates whether the storage volume is attached to or detached from the gateway.

        :cloudformationAttribute: VolumeAttachmentStatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVolumeAttachmentStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrVolumeId")
    def attr_volume_id(self) -> builtins.str:
        '''The unique identifier of the volume, extracted from the ARN.

        :cloudformationAttribute: VolumeId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVolumeId"))

    @builtins.property
    @jsii.member(jsii_name="attrVolumeStatus")
    def attr_volume_status(self) -> builtins.str:
        '''The status of the storage volume.

        :cloudformationAttribute: VolumeStatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVolumeStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrVolumeType")
    def attr_volume_type(self) -> builtins.str:
        '''The type of the volume (CACHED iSCSI).

        :cloudformationAttribute: VolumeType
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVolumeType"))

    @builtins.property
    @jsii.member(jsii_name="attrVolumeUsedInBytes")
    def attr_volume_used_in_bytes(self) -> "_aws_cdk_0cae9daa.IResolvable":
        '''The size of the data stored on the volume in bytes.

        :cloudformationAttribute: VolumeUsedInBytes
        '''
        return typing.cast("_aws_cdk_0cae9daa.IResolvable", jsii.get(self, "attrVolumeUsedInBytes"))

    @builtins.property
    @jsii.member(jsii_name="cdkTagManager")
    def cdk_tag_manager(self) -> "_aws_cdk_0cae9daa.TagManager":
        '''Tag Manager which manages the tags for this resource.'''
        return typing.cast("_aws_cdk_0cae9daa.TagManager", jsii.get(self, "cdkTagManager"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="volumeRef")
    def volume_ref(self) -> "_aws_storagegateway_f426d4c4.VolumeReference":
        '''A reference to a Volume resource.'''
        return typing.cast("_aws_storagegateway_f426d4c4.VolumeReference", jsii.get(self, "volumeRef"))

    @builtins.property
    @jsii.member(jsii_name="gatewayArn")
    def gateway_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the gateway on which to create the volume.'''
        return typing.cast(builtins.str, jsii.get(self, "gatewayArn"))

    @gateway_arn.setter
    def gateway_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1ba45071b81b984f48cd44af0429167dc533fc2274a5191804ba42e94d90d6dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gatewayArn", value)

    @builtins.property
    @jsii.member(jsii_name="networkInterfaceId")
    def network_interface_id(self) -> builtins.str:
        '''The network interface of the gateway on which to expose the iSCSI target.'''
        return typing.cast(builtins.str, jsii.get(self, "networkInterfaceId"))

    @network_interface_id.setter
    def network_interface_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b987f8d436ae585f6d3372ba67b76fb477d21bb29ad5e0b2846a3acc95a00b4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkInterfaceId", value)

    @builtins.property
    @jsii.member(jsii_name="targetName")
    def target_name(self) -> builtins.str:
        '''The name of the iSCSI target used by an initiator to connect to a volume and used as a suffix for the target ARN.'''
        return typing.cast(builtins.str, jsii.get(self, "targetName"))

    @target_name.setter
    def target_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f9c563b890b87a18c8920e9fabc30de93962af66c51e6b9482efbbe74a9c65a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetName", value)

    @builtins.property
    @jsii.member(jsii_name="volumeSizeInBytes")
    def volume_size_in_bytes(self) -> jsii.Number:
        '''The size of the volume in bytes.'''
        return typing.cast(jsii.Number, jsii.get(self, "volumeSizeInBytes"))

    @volume_size_in_bytes.setter
    def volume_size_in_bytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__da7ac1e7e402554d7ddb599eda8bfd6a13d073cbfd9f82c7199f8413538d8524)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeSizeInBytes", value)

    @builtins.property
    @jsii.member(jsii_name="kmsEncrypted")
    def kms_encrypted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Set to true to use Amazon S3 server-side encryption with your own KMS key, or false to use a key managed by Amazon S3.'''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], jsii.get(self, "kmsEncrypted"))

    @kms_encrypted.setter
    def kms_encrypted(
        self,
        value: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a7e2fbfba7700d7ecaed89d90b0c98d7dde5dc9c07231f2de5eef729fce3e004)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsEncrypted", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of a symmetric customer master key (CMK) used for Amazon S3 server-side encryption.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKey"))

    @kms_key.setter
    def kms_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__50c125bdcfd2df308abe2d69461be24ac0d3452057ad900b769e284c51bc97b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value)

    @builtins.property
    @jsii.member(jsii_name="snapshotId")
    def snapshot_id(self) -> typing.Optional[builtins.str]:
        '''The snapshot ID of the snapshot to restore as the new cached volume (e.g., snap-1122aabb).'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snapshotId"))

    @snapshot_id.setter
    def snapshot_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__143b58e3ee8398af2ded9c9c4ddbd83a8a7e8e239bff88ebeac284c9e4ea9542)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotId", value)

    @builtins.property
    @jsii.member(jsii_name="sourceVolumeArn")
    def source_volume_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of an existing volume from which to create the new volume.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceVolumeArn"))

    @source_volume_arn.setter
    def source_volume_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__9ae42c42008f06ea12289b5afddd7ba4a9127c40a6e07538bbc94150850d4fa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceVolumeArn", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''A list of up to 50 tags to assign to the volume.'''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b684f61a2857a73881de4565194ef2d7854f72db3bf20d5d1f7ec27f1dcad007)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_storagegateway.CfnVolumeProps",
    jsii_struct_bases=[],
    name_mapping={
        "gateway_arn": "gatewayArn",
        "network_interface_id": "networkInterfaceId",
        "target_name": "targetName",
        "volume_size_in_bytes": "volumeSizeInBytes",
        "kms_encrypted": "kmsEncrypted",
        "kms_key": "kmsKey",
        "snapshot_id": "snapshotId",
        "source_volume_arn": "sourceVolumeArn",
        "tags": "tags",
    },
)
class CfnVolumeProps:
    def __init__(
        self,
        *,
        gateway_arn: builtins.str,
        network_interface_id: builtins.str,
        target_name: builtins.str,
        volume_size_in_bytes: jsii.Number,
        kms_encrypted: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        kms_key: typing.Optional[builtins.str] = None,
        snapshot_id: typing.Optional[builtins.str] = None,
        source_volume_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnVolume``.

        :param gateway_arn: The Amazon Resource Name (ARN) of the gateway on which to create the volume.
        :param network_interface_id: The network interface of the gateway on which to expose the iSCSI target. Only IPv4 addresses are accepted.
        :param target_name: The name of the iSCSI target used by an initiator to connect to a volume and used as a suffix for the target ARN.
        :param volume_size_in_bytes: The size of the volume in bytes.
        :param kms_encrypted: Set to true to use Amazon S3 server-side encryption with your own KMS key, or false to use a key managed by Amazon S3.
        :param kms_key: The Amazon Resource Name (ARN) of a symmetric customer master key (CMK) used for Amazon S3 server-side encryption.
        :param snapshot_id: The snapshot ID of the snapshot to restore as the new cached volume (e.g., snap-1122aabb).
        :param source_volume_arn: The ARN of an existing volume from which to create the new volume.
        :param tags: A list of up to 50 tags to assign to the volume.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-volume.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_storagegateway as storagegateway
            
            cfn_volume_props = storagegateway.CfnVolumeProps(
                gateway_arn="gatewayArn",
                network_interface_id="networkInterfaceId",
                target_name="targetName",
                volume_size_in_bytes=123,
            
                # the properties below are optional
                kms_encrypted=False,
                kms_key="kmsKey",
                snapshot_id="snapshotId",
                source_volume_arn="sourceVolumeArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__94b026bb8c34e7ff0faded979ad91712d2af5384fb09b5c6708123e14328a801)
            check_type(argname="argument gateway_arn", value=gateway_arn, expected_type=type_hints["gateway_arn"])
            check_type(argname="argument network_interface_id", value=network_interface_id, expected_type=type_hints["network_interface_id"])
            check_type(argname="argument target_name", value=target_name, expected_type=type_hints["target_name"])
            check_type(argname="argument volume_size_in_bytes", value=volume_size_in_bytes, expected_type=type_hints["volume_size_in_bytes"])
            check_type(argname="argument kms_encrypted", value=kms_encrypted, expected_type=type_hints["kms_encrypted"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument snapshot_id", value=snapshot_id, expected_type=type_hints["snapshot_id"])
            check_type(argname="argument source_volume_arn", value=source_volume_arn, expected_type=type_hints["source_volume_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "gateway_arn": gateway_arn,
            "network_interface_id": network_interface_id,
            "target_name": target_name,
            "volume_size_in_bytes": volume_size_in_bytes,
        }
        if kms_encrypted is not None:
            self._values["kms_encrypted"] = kms_encrypted
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if snapshot_id is not None:
            self._values["snapshot_id"] = snapshot_id
        if source_volume_arn is not None:
            self._values["source_volume_arn"] = source_volume_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def gateway_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the gateway on which to create the volume.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-volume.html#cfn-storagegateway-volume-gatewayarn
        '''
        result = self._values.get("gateway_arn")
        assert result is not None, "Required property 'gateway_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_interface_id(self) -> builtins.str:
        '''The network interface of the gateway on which to expose the iSCSI target.

        Only IPv4 addresses are accepted.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-volume.html#cfn-storagegateway-volume-networkinterfaceid
        '''
        result = self._values.get("network_interface_id")
        assert result is not None, "Required property 'network_interface_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_name(self) -> builtins.str:
        '''The name of the iSCSI target used by an initiator to connect to a volume and used as a suffix for the target ARN.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-volume.html#cfn-storagegateway-volume-targetname
        '''
        result = self._values.get("target_name")
        assert result is not None, "Required property 'target_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def volume_size_in_bytes(self) -> jsii.Number:
        '''The size of the volume in bytes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-volume.html#cfn-storagegateway-volume-volumesizeinbytes
        '''
        result = self._values.get("volume_size_in_bytes")
        assert result is not None, "Required property 'volume_size_in_bytes' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def kms_encrypted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Set to true to use Amazon S3 server-side encryption with your own KMS key, or false to use a key managed by Amazon S3.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-volume.html#cfn-storagegateway-volume-kmsencrypted
        '''
        result = self._values.get("kms_encrypted")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of a symmetric customer master key (CMK) used for Amazon S3 server-side encryption.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-volume.html#cfn-storagegateway-volume-kmskey
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snapshot_id(self) -> typing.Optional[builtins.str]:
        '''The snapshot ID of the snapshot to restore as the new cached volume (e.g., snap-1122aabb).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-volume.html#cfn-storagegateway-volume-snapshotid
        '''
        result = self._values.get("snapshot_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_volume_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of an existing volume from which to create the new volume.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-volume.html#cfn-storagegateway-volume-sourcevolumearn
        '''
        result = self._values.get("source_volume_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''A list of up to 50 tags to assign to the volume.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-volume.html#cfn-storagegateway-volume-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVolumeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnNFSFileShare",
    "CfnNFSFileShareProps",
    "CfnSMBFileShare",
    "CfnSMBFileShareProps",
    "CfnTape",
    "CfnTapePool",
    "CfnTapePoolProps",
    "CfnTapeProps",
    "CfnVolume",
    "CfnVolumeProps",
]

publication.publish()

def _typecheckingstub__7ef63c1a3284eb06e5bf240b6a307d7aa0f5ba59dc929caaff3babba37d53ef4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    gateway_arn: builtins.str,
    location_arn: builtins.str,
    role: builtins.str,
    audit_destination_arn: typing.Optional[builtins.str] = None,
    bucket_region: typing.Optional[builtins.str] = None,
    cache_attributes: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnNFSFileShare.CacheAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    client_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    default_storage_class: typing.Optional[builtins.str] = None,
    encryption_type: typing.Optional[builtins.str] = None,
    file_share_name: typing.Optional[builtins.str] = None,
    guess_mime_type_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    kms_encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    kms_key: typing.Optional[builtins.str] = None,
    nfs_file_share_defaults: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnNFSFileShare.NFSFileShareDefaultsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    notification_policy: typing.Optional[builtins.str] = None,
    object_acl: typing.Optional[builtins.str] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    requester_pays: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    squash: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_endpoint_dns_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c1185683125ee8884d3836ce90d58776a2a5f56c4f69741839718006dc1dacc(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96f0a0025a4b96ce1509ba648f96a294efc2d1f3ce65765ecb5dc9be93bd2273(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e37baa8f7d67c8d0b82cc3568a4b79928930ee9210e970bf56e24ea342b5de30(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53155bb263973ce3a9e5f2c0b76de8be7dce51f7d1799bfc33e51a1ab5dad3d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f3e8e1e4709da66e338af5e419c5ee1990fe879cdfba8fe941e7b4213607a10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85f3483626b68046b4759b86e6e1b0209668f20cc6b813e5398694ec752039a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__851116e770cd210889ab05753d306a346224b088658634e3311b9cf905f06d95(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecfee355fac83f818940cdfa55b40a73ea9d5799d942ffc28b5c8178e159ea41(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c967508d24c8c842c0f01aa7d8de77afbd08cf93d33b0621f30f7ed532cd3b51(
    value: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnNFSFileShare.CacheAttributesProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58fe1c1d70835fdba1afe70cc5e209fd51464559d9d354cbe878eb2a112c766d(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__846b61c9d9a9c51b702c72514dcce6073620fb97bbfcaf8f22bfd34892c92d34(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43fc7b2154332f9a73494569e0d04083adbc5a77191e92ca445667e462749925(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__148f53ee8b5859e717eb3f96d4407f9c1b6934a9d070ca024249e56bf1ec0feb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85bb9e909f255c5f3c749bab54fbd615c4b1d0cc114b3e9630a52b5e9063709a(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b47104c11c902f5223e9165a4b2544a4f7c32de36910080219aa3785e2fc15d6(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27a7e056ec32f4c1ed0cb2907fa43558008624cba8cc4d3fa2d66c09b9fc8b72(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa4d188d7f07fd20222c301d8ededf842b3adbaab853908f285a2e5f34aac21c(
    value: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnNFSFileShare.NFSFileShareDefaultsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b22cfea05dcaced75a3624aab81c94d685c87b0740a7969588051c112e1dd26a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d871fcb7ed387d48c95cf93b0fb16dc5613ffb9b7dfc632ec22197f5bf86eed(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13fd549d9d9a11181a11137d1fe05f4dfc1a1d4b391761e3c06f54ebc77194ab(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88460ec56bd29074ee994fb48a4e3ce9529f03c2d1b63d84cb5f8cf2510d82d0(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af099dacadf510ce80db3e5b75a49b97cea24d4bf88a2ce989dad363e7ec7803(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a08a8b45a5ed44fef3f50b814ec5cdc51e3a65d2b92fbeb45dd630ec33f0a6b(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__507903680420bfd15ce65af69b7b8443d63e48fa07017f926ab76186c97103c6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__536adc436761db31735a84265405310a1264490dc2b23bd4adc8fc9d0b092eec(
    *,
    cache_stale_timeout_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e87af42d4132b4fbf18b2ddcf34339bbb3699f8be82e4bfe1d2b722804b92522(
    *,
    directory_mode: typing.Optional[builtins.str] = None,
    file_mode: typing.Optional[builtins.str] = None,
    group_id: typing.Optional[jsii.Number] = None,
    owner_id: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__741a7608895c12875c075fcd58a1ae221040db3c96eb08b0255df43b2ec93a5c(
    *,
    gateway_arn: builtins.str,
    location_arn: builtins.str,
    role: builtins.str,
    audit_destination_arn: typing.Optional[builtins.str] = None,
    bucket_region: typing.Optional[builtins.str] = None,
    cache_attributes: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnNFSFileShare.CacheAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    client_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    default_storage_class: typing.Optional[builtins.str] = None,
    encryption_type: typing.Optional[builtins.str] = None,
    file_share_name: typing.Optional[builtins.str] = None,
    guess_mime_type_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    kms_encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    kms_key: typing.Optional[builtins.str] = None,
    nfs_file_share_defaults: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnNFSFileShare.NFSFileShareDefaultsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    notification_policy: typing.Optional[builtins.str] = None,
    object_acl: typing.Optional[builtins.str] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    requester_pays: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    squash: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_endpoint_dns_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d6bb5e76e3bfd08c7e205da1ce11d1dbbad406ac72865b79b0124c6ecc2a865(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    gateway_arn: builtins.str,
    location_arn: builtins.str,
    role: builtins.str,
    access_based_enumeration: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    admin_user_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    audit_destination_arn: typing.Optional[builtins.str] = None,
    authentication: typing.Optional[builtins.str] = None,
    bucket_region: typing.Optional[builtins.str] = None,
    cache_attributes: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnSMBFileShare.CacheAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    case_sensitivity: typing.Optional[builtins.str] = None,
    default_storage_class: typing.Optional[builtins.str] = None,
    encryption_type: typing.Optional[builtins.str] = None,
    file_share_name: typing.Optional[builtins.str] = None,
    guess_mime_type_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    invalid_user_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    kms_encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    kms_key: typing.Optional[builtins.str] = None,
    notification_policy: typing.Optional[builtins.str] = None,
    object_acl: typing.Optional[builtins.str] = None,
    oplocks_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    requester_pays: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    smbacl_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    valid_user_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_endpoint_dns_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa2f2fb851dc7b3a0160b4bc79e157532796e26aa58dd9e47cca559f61b70a99(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2952cd8e0e1de99556d1f14043692590b78f7e059aba21e8beefdb3b49f6cfa9(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5c11900f02ffaecdc0c153147d58275cea721b94221790e744948f887782997(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94a3e907858c6cbfca5d6e824321158c80d5141a8029e4b9571467c38a54b774(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bdc9e88265f90023f2c4a1eff8a693428bf1f616d7a5ed00b0c1a318a42075a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af5b503d360be9b2de28b2bfd7519d8de746ea86e14c290e773852e082bcb1e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85df24584502d0bf371ebb7e7bbe6c20793e3135b0ff7225de37dfc007f1da0f(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dec1c106ec5fff369b90e170f1d456a214c69657d0ffc831e7916468b7b08c3f(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8ca1a82707bc3db43d1a40c58f4ddf69a9ea4a9ffb23934d8b521fc3c3e24c3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa50f11d8c76a0e4c87b50619757f632477611e3f887b9892edfc0776516a41d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f9680c7a89d371b5827c7cf3b1a7ccf962841f4af5c23a0a095a87805890e57(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d17d6f8978747ebb37e5e06e137530bcf93d05e77a0872f24636de884e36279c(
    value: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnSMBFileShare.CacheAttributesProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a872099b2cd659541d1c208e9584391b4e23a57adcfc5bb578de0668e0c3858(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef6376f6854dab2c7a8a3a750830665070d99fc74579e94238ee3136177704b9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b51829ae2c28f2d69b672f4389c6c01681e11d4342c505746dbc21037f0aee3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a73a22858d1a68e5652ba15c03c4d11e94c3e6bcdb3d52d68082690ff08b4a69(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db41ec01c93215225838b459984262d37db3ac2a4ca00bb553e323052f216def(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__945ec0159776e271724e8c48a573501880be85e73c6b0c95d2077f84fb14796c(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__715f75c3a39191a34932f3b493b4d4a29bc7afa37c16944229e32f1afae61899(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ca48bb7e8df73fd2251ce341a7b69379c8e6f23196dc12f09dbc689aa7bf80f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8ae7905fa41b2bc4e90ee792c16279cb22f4b0e627bc6bfd006929df28460fe(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e0708a578d7594fcedd855b2819ebaa94a421402afc7d53298ef7f07139efa8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__722ac7cf59e36cc000d6d09702358efdea6a4d992d1e403c240509df0d67e83e(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e4538b395b0c7805353f2d34b6aa14f10659d91b91aad0ae91e7e82f1d7075a(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d52a2b5e396e18a8840cb0a693d3efdcb90ec550427e73242e023b92066cbfa1(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__406978e9ef07a5ae055fd473d8e06592063b4954ea39e495931132a5b2590c59(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3a32bcc5e5e849d91c51015e4ce02da661ec4f18ded7113a1b022e70807404a(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60234f0dc8233bfe2510847a086df7412f8f60f50f91bac0cdea39bfa0652d49(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab2eb11dae31778936a83e019d01b5742cd8cf1fe5c83008fe70c81dd2b3cc7c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ab3dd1647fc75ea364afc0c3c9d5f6069e78fdf71d8d5ea4ccc1a3ff51e266d(
    *,
    cache_stale_timeout_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8282ebf6180403a4ae32ac9a75091ca13ed4abcc284bef166c4b01e91ddebd97(
    *,
    gateway_arn: builtins.str,
    location_arn: builtins.str,
    role: builtins.str,
    access_based_enumeration: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    admin_user_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    audit_destination_arn: typing.Optional[builtins.str] = None,
    authentication: typing.Optional[builtins.str] = None,
    bucket_region: typing.Optional[builtins.str] = None,
    cache_attributes: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnSMBFileShare.CacheAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    case_sensitivity: typing.Optional[builtins.str] = None,
    default_storage_class: typing.Optional[builtins.str] = None,
    encryption_type: typing.Optional[builtins.str] = None,
    file_share_name: typing.Optional[builtins.str] = None,
    guess_mime_type_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    invalid_user_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    kms_encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    kms_key: typing.Optional[builtins.str] = None,
    notification_policy: typing.Optional[builtins.str] = None,
    object_acl: typing.Optional[builtins.str] = None,
    oplocks_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    requester_pays: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    smbacl_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    valid_user_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_endpoint_dns_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__363b2f7813c184123160ffaf59a488211565913fb5126a1fa69bcb36310d32dc(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    gateway_arn: builtins.str,
    tape_size_in_bytes: jsii.Number,
    kms_encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    kms_key: typing.Optional[builtins.str] = None,
    pool_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    tape_barcode: typing.Optional[builtins.str] = None,
    worm: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae610be3890fbb42584972211b0c5af3006370462c1bf3c6c3b219eb44a03b39(
    resource: _aws_storagegateway_f426d4c4.ITapeRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebb8f5d769e86e9451e9c5e5b3470e03b5d0dfb0c67afc78fc0e8c2598c707dd(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd33548844c3c66482e5960a6a6f61789c9af04eb374db35a888509e0a56ab58(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ae0da0b888c3ffbaa5eb6cd82d55bf20a66d98c9c309e38a2589910332683ed(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__662f1b01cec9fb4c578c1bbb30288dbf38679b5353e5dda5dbd320ef43291325(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__020d09dce3e65ad2aaf95651a3b71d13e7e4491b13562a0833109864a3cdaa0b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee66a67c862d78755548260dd465bb54d1d4135b9bbb9ac1bae6ba2ea3475fe8(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1696f2d90ac34d1befe0d8f8fdff10c6a152824cfb1cea61f78cb3c939d074b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__771aea9bb34cd7a52d93c075fca8422288c8149c586c2433579b77e674bbc411(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b43111da63c8804b5553828beed62e0fc46e21d09e17e06cfa23a83a7d5f7756(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5023431719ea44a143693a72e05f0b2a264ee01337c78f4ade43d1fe0d4746bb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdca3fd4b57f957db6910289a79178f6960086b883d0e146cdbbf55066ade533(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac2c1692ba4edccb604aef75af4b88463d090c7db3c8f08741d200a884adedac(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    pool_name: builtins.str,
    storage_class: builtins.str,
    retention_lock_time_in_days: typing.Optional[jsii.Number] = None,
    retention_lock_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bdaa23426ff87911afa19f9997f4ea57420c29c61fc1892987875628fdf638b(
    resource: _aws_storagegateway_f426d4c4.ITapePoolRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8b4c436c83b9aad89b0f338e63d3ef15cdc1d6880fa6e5c24369f59ab7d5e34(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    pool_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f4ac6b6ba23515dcc27d4c5a84961fe7a159a83305f9188d9b81d341eac359a(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb3a41212781376c4f3874b92a3aeae3808be50104fb587f50096ee25d9cbdfe(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a89e9380fc69f21f542d0c5d15978f09dbb5fc7563f2badbf156059dafb2775(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2aa2850a80df094617446432f9ff1341cc436487f9fdcde124fff6e23224b3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59e6b638819f00096b40770703546150877b22e670bd72107418a00ab661a3c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9a75e037e394e1a483c9c37c628c1a3fd5236ed311d296563d7c92ed300cf84(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4607d71dfda14f2f335c62ade52d5f18924d070d446cf3004dcb39ec784be160(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3795fcc974a44ec324d8e597cdf4de7162f69066e260ed1f4273fc3bc7275cc1(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__313c929df3254bd85bbd9d06cbd71bce8cccb516d3867f49894385585d8f30e9(
    *,
    pool_name: builtins.str,
    storage_class: builtins.str,
    retention_lock_time_in_days: typing.Optional[jsii.Number] = None,
    retention_lock_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa2d145c5722622b5c7cd133c48409678c375141152fd14546bec9a5731ba577(
    *,
    gateway_arn: builtins.str,
    tape_size_in_bytes: jsii.Number,
    kms_encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    kms_key: typing.Optional[builtins.str] = None,
    pool_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    tape_barcode: typing.Optional[builtins.str] = None,
    worm: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__271ddda20ad6264f77cc2f79555b3fa6ea997c8e5dccba6d566d2dcf154f898f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    gateway_arn: builtins.str,
    network_interface_id: builtins.str,
    target_name: builtins.str,
    volume_size_in_bytes: jsii.Number,
    kms_encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    kms_key: typing.Optional[builtins.str] = None,
    snapshot_id: typing.Optional[builtins.str] = None,
    source_volume_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf4b04a4849965fc4cd022c8e0fd09da482cd62aef80e780fb96a074696e4817(
    resource: _aws_storagegateway_f426d4c4.IVolumeRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8697be7703a6f5458994a17690dde8dd46e21cc40628f1a0720415688dddf65b(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10e0a5d67c599ccc35a189f881ed3e303c2f2e0453a222f914017c743a9e364d(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21658029a19b77c6623b63fe0a949fb1e70c240363e99c57a2637e632dc6f9b3(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ba45071b81b984f48cd44af0429167dc533fc2274a5191804ba42e94d90d6dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b987f8d436ae585f6d3372ba67b76fb477d21bb29ad5e0b2846a3acc95a00b4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9c563b890b87a18c8920e9fabc30de93962af66c51e6b9482efbbe74a9c65a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da7ac1e7e402554d7ddb599eda8bfd6a13d073cbfd9f82c7199f8413538d8524(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7e2fbfba7700d7ecaed89d90b0c98d7dde5dc9c07231f2de5eef729fce3e004(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50c125bdcfd2df308abe2d69461be24ac0d3452057ad900b769e284c51bc97b1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__143b58e3ee8398af2ded9c9c4ddbd83a8a7e8e239bff88ebeac284c9e4ea9542(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ae42c42008f06ea12289b5afddd7ba4a9127c40a6e07538bbc94150850d4fa8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b684f61a2857a73881de4565194ef2d7854f72db3bf20d5d1f7ec27f1dcad007(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94b026bb8c34e7ff0faded979ad91712d2af5384fb09b5c6708123e14328a801(
    *,
    gateway_arn: builtins.str,
    network_interface_id: builtins.str,
    target_name: builtins.str,
    volume_size_in_bytes: jsii.Number,
    kms_encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    kms_key: typing.Optional[builtins.str] = None,
    snapshot_id: typing.Optional[builtins.str] = None,
    source_volume_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
