r'''
# AWS::Signer Construct Library

AWS Signer is a fully managed code-signing service to ensure the trust and integrity of your code. Organizations validate code against
a digital signature to confirm that the code is unaltered and from a trusted publisher. For more information, see [What Is AWS
Signer?](https://docs.aws.amazon.com/signer/latest/developerguide/Welcome.html)

## Table of Contents

* [Signing Platform](#signing-platform)
* [Signing Profile](#signing-profile)

## Signing Platform

A signing platform is a predefined set of instructions that specifies the signature format and signing algorithms that AWS Signer should use
to sign a zip file. For more information go to [Signing Platforms in AWS Signer](https://docs.aws.amazon.com/signer/latest/developerguide/gs-platform.html).

AWS Signer provides a pre-defined set of signing platforms. They are available in the CDK as -

```text
Platform.AWS_IOT_DEVICE_MANAGEMENT_SHA256_ECDSA
Platform.AWS_LAMBDA_SHA384_ECDSA
Platform.AMAZON_FREE_RTOS_TI_CC3220SF
Platform.AMAZON_FREE_RTOS_DEFAULT
```

## Signing Profile

A signing profile is a code-signing template that can be used to pre-define the signature specifications for a signing job.
A signing profile includes a signing platform to designate the file type to be signed, the signature format, and the signature algorithms.
For more information, visit [Signing Profiles in AWS Signer](https://docs.aws.amazon.com/signer/latest/developerguide/gs-profile.html).

The following code sets up a signing profile for signing lambda code bundles -

```python
signing_profile = signer.SigningProfile(self, "SigningProfile",
    platform=signer.Platform.AWS_LAMBDA_SHA384_ECDSA
)
```

A signing profile is valid by default for 135 months. This can be modified by specifying the `signatureValidityPeriod` property.
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
    import aws_cdk.interfaces.aws_signer as _aws_signer_fcf3aa48
    import constructs as _constructs_77d1e7e8
else:

    _aws_cdk_0cae9daa = _LazyImport("aws_cdk")
    _aws_signer_fcf3aa48 = _LazyImport("aws_cdk.interfaces.aws_signer")
    _constructs_77d1e7e8 = _LazyImport("constructs")


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_signer_fcf3aa48.IProfilePermissionRef)
class CfnProfilePermission(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_signer.CfnProfilePermission",
):
    '''Adds cross-account permissions to a signing profile.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-profilepermission.html
    :cloudformationResource: AWS::Signer::ProfilePermission
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_signer as signer
        
        cfn_profile_permission = signer.CfnProfilePermission(self, "MyCfnProfilePermission",
            action="action",
            principal="principal",
            profile_name="profileName",
            statement_id="statementId",
        
            # the properties below are optional
            profile_version="profileVersion"
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        action: builtins.str,
        principal: builtins.str,
        profile_name: builtins.str,
        statement_id: builtins.str,
        profile_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Signer::ProfilePermission``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param action: The AWS Signer action permitted as part of cross-account permissions.
        :param principal: The AWS principal receiving cross-account permissions. This may be an IAM role or another AWS account ID.
        :param profile_name: The human-readable name of the signing profile.
        :param statement_id: A unique identifier for the cross-account permission statement.
        :param profile_version: The version of the signing profile.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__7b7dd51e7eac664b5afe9a1b7d1972f7da8883244b3f554de5c8d1e0cc84f053)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnProfilePermissionProps(
            action=action,
            principal=principal,
            profile_name=profile_name,
            statement_id=statement_id,
            profile_version=profile_version,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="isCfnProfilePermission")
    @builtins.classmethod
    def is_cfn_profile_permission(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnProfilePermission.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__fa9b2b5c20a313a6a8736730c6a3112613d411a11743beb2f9de986fce357c4a)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnProfilePermission", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1c27c534af2f676e9fe9c9b1c8462b7339b8b65f0c4b9b08f485033feefe4741)
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
            type_hints = cached_type_hints(_typecheckingstub__662ce8c205095e7c693616c7c2d43b18432d9c948d131c1a3e91e7b5aafc2323)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="profilePermissionRef")
    def profile_permission_ref(
        self,
    ) -> "_aws_signer_fcf3aa48.ProfilePermissionReference":
        '''A reference to a ProfilePermission resource.'''
        return typing.cast("_aws_signer_fcf3aa48.ProfilePermissionReference", jsii.get(self, "profilePermissionRef"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        '''The AWS Signer action permitted as part of cross-account permissions.'''
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__9b8c32d87b73fa4fb5094ae3e46175df93629f45d64c0d2b3130d5471eca086e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="principal")
    def principal(self) -> builtins.str:
        '''The AWS principal receiving cross-account permissions.'''
        return typing.cast(builtins.str, jsii.get(self, "principal"))

    @principal.setter
    def principal(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__37b3db8c74061df8a65eeda431f6a41091db1cf687f78d71f79a9441f95b0644)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principal", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="profileName")
    def profile_name(self) -> builtins.str:
        '''The human-readable name of the signing profile.'''
        return typing.cast(builtins.str, jsii.get(self, "profileName"))

    @profile_name.setter
    def profile_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__0284177166884a4428819ca021ca73daecd877943a7bf90e79aec6e00f5ad07a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profileName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statementId")
    def statement_id(self) -> builtins.str:
        '''A unique identifier for the cross-account permission statement.'''
        return typing.cast(builtins.str, jsii.get(self, "statementId"))

    @statement_id.setter
    def statement_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__9e8ca5148f26e102d75c04bb95550132d3a29824e2932a98f9f87725df3962fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statementId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="profileVersion")
    def profile_version(self) -> typing.Optional[builtins.str]:
        '''The version of the signing profile.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "profileVersion"))

    @profile_version.setter
    def profile_version(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__80bd95afa9c654fc5d026db2cad497a96dc240f466154896c0c5c3cc15b54bdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profileVersion", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_signer.CfnProfilePermissionProps",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "principal": "principal",
        "profile_name": "profileName",
        "statement_id": "statementId",
        "profile_version": "profileVersion",
    },
)
class CfnProfilePermissionProps:
    def __init__(
        self,
        *,
        action: builtins.str,
        principal: builtins.str,
        profile_name: builtins.str,
        statement_id: builtins.str,
        profile_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnProfilePermission``.

        :param action: The AWS Signer action permitted as part of cross-account permissions.
        :param principal: The AWS principal receiving cross-account permissions. This may be an IAM role or another AWS account ID.
        :param profile_name: The human-readable name of the signing profile.
        :param statement_id: A unique identifier for the cross-account permission statement.
        :param profile_version: The version of the signing profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-profilepermission.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_signer as signer
            
            cfn_profile_permission_props = signer.CfnProfilePermissionProps(
                action="action",
                principal="principal",
                profile_name="profileName",
                statement_id="statementId",
            
                # the properties below are optional
                profile_version="profileVersion"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__cc7158edcf57ecc13c1e912574c38dd0ad2f9585f23f02536376f63ed728fe86)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
            check_type(argname="argument profile_name", value=profile_name, expected_type=type_hints["profile_name"])
            check_type(argname="argument statement_id", value=statement_id, expected_type=type_hints["statement_id"])
            check_type(argname="argument profile_version", value=profile_version, expected_type=type_hints["profile_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "principal": principal,
            "profile_name": profile_name,
            "statement_id": statement_id,
        }
        if profile_version is not None:
            self._values["profile_version"] = profile_version

    @builtins.property
    def action(self) -> builtins.str:
        '''The AWS Signer action permitted as part of cross-account permissions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-profilepermission.html#cfn-signer-profilepermission-action
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def principal(self) -> builtins.str:
        '''The AWS principal receiving cross-account permissions.

        This may be an IAM role or another AWS account ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-profilepermission.html#cfn-signer-profilepermission-principal
        '''
        result = self._values.get("principal")
        assert result is not None, "Required property 'principal' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def profile_name(self) -> builtins.str:
        '''The human-readable name of the signing profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-profilepermission.html#cfn-signer-profilepermission-profilename
        '''
        result = self._values.get("profile_name")
        assert result is not None, "Required property 'profile_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def statement_id(self) -> builtins.str:
        '''A unique identifier for the cross-account permission statement.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-profilepermission.html#cfn-signer-profilepermission-statementid
        '''
        result = self._values.get("statement_id")
        assert result is not None, "Required property 'statement_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def profile_version(self) -> typing.Optional[builtins.str]:
        '''The version of the signing profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-profilepermission.html#cfn-signer-profilepermission-profileversion
        '''
        result = self._values.get("profile_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProfilePermissionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_signer_fcf3aa48.ISigningJobRef)
class CfnSigningJob(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_signer.CfnSigningJob",
):
    '''Represents an AWS Signer signing job.

    Signing jobs are initiated via StartSigningJob and are read-only resources that provide visibility into code signing operations.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-signingjob.html
    :cloudformationResource: AWS::Signer::SigningJob
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_signer as signer
        
        cfn_signing_job = signer.CfnSigningJob(self, "MyCfnSigningJob",
            profile_name="profileName"
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        profile_name: builtins.str,
    ) -> None:
        '''Create a new ``AWS::Signer::SigningJob``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param profile_name: The name of the signing profile.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ab4bda8b7d5eaea8c6dc7889d4296f6ea822b1c2cb553c36b67a116ed558b6c5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSigningJobProps(profile_name=profile_name)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForSigningJob")
    @builtins.classmethod
    def arn_for_signing_job(
        cls,
        resource: "_aws_signer_fcf3aa48.ISigningJobRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__9dcb26787091b618a59a613bf0f199239b366e05b44cde3663af37bf978e09e0)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForSigningJob", [resource]))

    @jsii.member(jsii_name="isCfnSigningJob")
    @builtins.classmethod
    def is_cfn_signing_job(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnSigningJob.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__90f411dd9a69746e85dc03853e0db69f25857f2c81107040f333fca5e6c96d96)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnSigningJob", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__abe96d636a14bb3f70be144a1f7e704b482e30d63d75628d33a1e95c0bd048f8)
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
            type_hints = cached_type_hints(_typecheckingstub__791e96e43922635f4184768f9bba8ebfa19e53ae037914b01c76c0f7e3586602)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The ARN of the signing job.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCompletedAt")
    def attr_completed_at(self) -> builtins.str:
        '''Date and time that the signing job was completed.

        :cloudformationAttribute: CompletedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCompletedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''Date and time that the signing job was created.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrJobId")
    def attr_job_id(self) -> builtins.str:
        '''The ID of the signing job.

        :cloudformationAttribute: JobId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrJobId"))

    @builtins.property
    @jsii.member(jsii_name="attrJobInvoker")
    def attr_job_invoker(self) -> builtins.str:
        '''The IAM entity that initiated the signing job.

        :cloudformationAttribute: JobInvoker
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrJobInvoker"))

    @builtins.property
    @jsii.member(jsii_name="attrJobOwner")
    def attr_job_owner(self) -> builtins.str:
        '''The AWS account ID of the job owner.

        :cloudformationAttribute: JobOwner
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrJobOwner"))

    @builtins.property
    @jsii.member(jsii_name="attrPlatformDisplayName")
    def attr_platform_display_name(self) -> builtins.str:
        '''A human-readable name for the signing platform associated with the signing job.

        :cloudformationAttribute: PlatformDisplayName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPlatformDisplayName"))

    @builtins.property
    @jsii.member(jsii_name="attrPlatformId")
    def attr_platform_id(self) -> builtins.str:
        '''The microcontroller platform to which the signed code image will be distributed.

        :cloudformationAttribute: PlatformId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPlatformId"))

    @builtins.property
    @jsii.member(jsii_name="attrProfileVersion")
    def attr_profile_version(self) -> builtins.str:
        '''The version of the signing profile used to initiate the signing job.

        :cloudformationAttribute: ProfileVersion
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrProfileVersion"))

    @builtins.property
    @jsii.member(jsii_name="attrRequestedBy")
    def attr_requested_by(self) -> builtins.str:
        '''The IAM principal that requested the signing job.

        :cloudformationAttribute: RequestedBy
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRequestedBy"))

    @builtins.property
    @jsii.member(jsii_name="attrSignatureExpiresAt")
    def attr_signature_expires_at(self) -> builtins.str:
        '''The expiration timestamp for the signature generated by the signing job.

        :cloudformationAttribute: SignatureExpiresAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSignatureExpiresAt"))

    @builtins.property
    @jsii.member(jsii_name="attrSignedObject")
    def attr_signed_object(self) -> "_aws_cdk_0cae9daa.IResolvable":
        '''The S3 location of the signed code image.

        :cloudformationAttribute: SignedObject
        '''
        return typing.cast("_aws_cdk_0cae9daa.IResolvable", jsii.get(self, "attrSignedObject"))

    @builtins.property
    @jsii.member(jsii_name="attrSource")
    def attr_source(self) -> "_aws_cdk_0cae9daa.IResolvable":
        '''Information about the S3 bucket where unsigned code is stored.

        :cloudformationAttribute: Source
        '''
        return typing.cast("_aws_cdk_0cae9daa.IResolvable", jsii.get(self, "attrSource"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''Status of the signing job.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="signingJobRef")
    def signing_job_ref(self) -> "_aws_signer_fcf3aa48.SigningJobReference":
        '''A reference to a SigningJob resource.'''
        return typing.cast("_aws_signer_fcf3aa48.SigningJobReference", jsii.get(self, "signingJobRef"))

    @builtins.property
    @jsii.member(jsii_name="profileName")
    def profile_name(self) -> builtins.str:
        '''The name of the signing profile.'''
        return typing.cast(builtins.str, jsii.get(self, "profileName"))

    @profile_name.setter
    def profile_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__cf7baa61b0509981041de7ab4c5c9b09955802ce8be72bf4e42f3afb9e654b21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profileName", value) # pyright: ignore[reportArgumentType]

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_signer.CfnSigningJob.S3SignedObjectProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket_name": "bucketName", "key": "key"},
    )
    class S3SignedObjectProperty:
        def __init__(
            self,
            *,
            bucket_name: typing.Optional[builtins.str] = None,
            key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Amazon S3 bucket name and key where Signer saved the signed code image.

            :param bucket_name: Name of the S3 bucket.
            :param key: Key name that uniquely identifies a signed code image in the bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-signer-signingjob-s3signedobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_signer as signer
                
                s3_signed_object_property = signer.CfnSigningJob.S3SignedObjectProperty(
                    bucket_name="bucketName",
                    key="key"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__58836aeb809f68ae4865dad7598c85530241b919317954f6976c9edc5757081f)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name
            if key is not None:
                self._values["key"] = key

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            '''Name of the S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-signer-signingjob-s3signedobject.html#cfn-signer-signingjob-s3signedobject-bucketname
            '''
            result = self._values.get("bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''Key name that uniquely identifies a signed code image in the bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-signer-signingjob-s3signedobject.html#cfn-signer-signingjob-s3signedobject-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3SignedObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_signer.CfnSigningJob.S3SourceProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket_name": "bucketName", "key": "key", "version": "version"},
    )
    class S3SourceProperty:
        def __init__(
            self,
            *,
            bucket_name: builtins.str,
            key: builtins.str,
            version: builtins.str,
        ) -> None:
            '''Information about the Amazon S3 bucket where unsigned code is stored.

            :param bucket_name: Name of the S3 bucket.
            :param key: Key name of the bucket object that contains unsigned code.
            :param version: Version of the source image in the version-enabled S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-signer-signingjob-s3source.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_signer as signer
                
                s3_source_property = signer.CfnSigningJob.S3SourceProperty(
                    bucket_name="bucketName",
                    key="key",
                    version="version"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__8ade25d735cba1b883bfc479fef183a91da725ebb30105c3d60cbf32df16d16d)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket_name": bucket_name,
                "key": key,
                "version": version,
            }

        @builtins.property
        def bucket_name(self) -> builtins.str:
            '''Name of the S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-signer-signingjob-s3source.html#cfn-signer-signingjob-s3source-bucketname
            '''
            result = self._values.get("bucket_name")
            assert result is not None, "Required property 'bucket_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key(self) -> builtins.str:
            '''Key name of the bucket object that contains unsigned code.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-signer-signingjob-s3source.html#cfn-signer-signingjob-s3source-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def version(self) -> builtins.str:
            '''Version of the source image in the version-enabled S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-signer-signingjob-s3source.html#cfn-signer-signingjob-s3source-version
            '''
            result = self._values.get("version")
            assert result is not None, "Required property 'version' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3SourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_signer.CfnSigningJob.SignedObjectProperty",
        jsii_struct_bases=[],
        name_mapping={"s3": "s3"},
    )
    class SignedObjectProperty:
        def __init__(
            self,
            *,
            s3: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnSigningJob.S3SignedObjectProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The S3 location of the signed code image.

            :param s3: The Amazon S3 bucket name and key where Signer saved the signed code image.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-signer-signingjob-signedobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_signer as signer
                
                signed_object_property = signer.CfnSigningJob.SignedObjectProperty(
                    s3=signer.CfnSigningJob.S3SignedObjectProperty(
                        bucket_name="bucketName",
                        key="key"
                    )
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__acc54aa7f5738da3a6d649a358b6c64501a1de92862a645694f512b0b18f6fa5)
                check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3 is not None:
                self._values["s3"] = s3

        @builtins.property
        def s3(
            self,
        ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnSigningJob.S3SignedObjectProperty"]]:
            '''The Amazon S3 bucket name and key where Signer saved the signed code image.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-signer-signingjob-signedobject.html#cfn-signer-signingjob-signedobject-s3
            '''
            result = self._values.get("s3")
            return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnSigningJob.S3SignedObjectProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SignedObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_signer.CfnSigningJob.SourceProperty",
        jsii_struct_bases=[],
        name_mapping={"s3": "s3"},
    )
    class SourceProperty:
        def __init__(
            self,
            *,
            s3: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnSigningJob.S3SourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information about the S3 bucket where unsigned code is stored.

            :param s3: Information about the Amazon S3 bucket where unsigned code is stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-signer-signingjob-source.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_signer as signer
                
                source_property = signer.CfnSigningJob.SourceProperty(
                    s3=signer.CfnSigningJob.S3SourceProperty(
                        bucket_name="bucketName",
                        key="key",
                        version="version"
                    )
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__4861fc8f98a207465561eede33a73377b1eaca415bea7844cd8e878050cf7f9b)
                check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3 is not None:
                self._values["s3"] = s3

        @builtins.property
        def s3(
            self,
        ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnSigningJob.S3SourceProperty"]]:
            '''Information about the Amazon S3 bucket where unsigned code is stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-signer-signingjob-source.html#cfn-signer-signingjob-source-s3
            '''
            result = self._values.get("s3")
            return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnSigningJob.S3SourceProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_signer.CfnSigningJobProps",
    jsii_struct_bases=[],
    name_mapping={"profile_name": "profileName"},
)
class CfnSigningJobProps:
    def __init__(self, *, profile_name: builtins.str) -> None:
        '''Properties for defining a ``CfnSigningJob``.

        :param profile_name: The name of the signing profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-signingjob.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_signer as signer
            
            cfn_signing_job_props = signer.CfnSigningJobProps(
                profile_name="profileName"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b8c57eff50d383c03cd8511b0bd7973e5b281f4f35609df6e7dc048909c6a732)
            check_type(argname="argument profile_name", value=profile_name, expected_type=type_hints["profile_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "profile_name": profile_name,
        }

    @builtins.property
    def profile_name(self) -> builtins.str:
        '''The name of the signing profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-signingjob.html#cfn-signer-signingjob-profilename
        '''
        result = self._values.get("profile_name")
        assert result is not None, "Required property 'profile_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSigningJobProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_signer_fcf3aa48.ISigningProfileRef, _aws_cdk_0cae9daa.ITaggable)
class CfnSigningProfile(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_signer.CfnSigningProfile",
):
    '''Creates a signing profile.

    A signing profile is a code-signing template that can be used to carry out a pre-defined signing job.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-signingprofile.html
    :cloudformationResource: AWS::Signer::SigningProfile
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_signer as signer
        
        cfn_signing_profile = signer.CfnSigningProfile(self, "MyCfnSigningProfile",
            platform_id="platformId",
        
            # the properties below are optional
            profile_name="profileName",
            signature_validity_period=signer.CfnSigningProfile.SignatureValidityPeriodProperty(
                type="type",
                value=123
            ),
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
        platform_id: builtins.str,
        profile_name: typing.Optional[builtins.str] = None,
        signature_validity_period: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnSigningProfile.SignatureValidityPeriodProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Signer::SigningProfile``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param platform_id: The ID of a platform that is available for use by a signing profile.
        :param profile_name: The name of the signing profile.
        :param signature_validity_period: The validity period override for any signature generated using this signing profile. If unspecified, the default is 135 months.
        :param tags: A list of tags associated with the signing profile.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d84fe196f81722ce814c09f8bd21719acd97c32e92c1de922d0f04c31912d65b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSigningProfileProps(
            platform_id=platform_id,
            profile_name=profile_name,
            signature_validity_period=signature_validity_period,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForSigningProfile")
    @builtins.classmethod
    def arn_for_signing_profile(
        cls,
        resource: "_aws_signer_fcf3aa48.ISigningProfileRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f88b9c5ab8f3709756f086e40d555988785e2364dbe7e70f2cd9c77e7cc59634)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForSigningProfile", [resource]))

    @jsii.member(jsii_name="isCfnSigningProfile")
    @builtins.classmethod
    def is_cfn_signing_profile(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnSigningProfile.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c3e32d4beb10fbb8b17ae147070d2bc9be76eea0d4a93458b396357b7b5d3473)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnSigningProfile", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__796b31e3d9d2ce1d3b20283186f1c0c54ce0f3bb426633c056466f92264e35b9)
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
            type_hints = cached_type_hints(_typecheckingstub__59eb44451cc01c28f44f21713cf6296a564f672edd6fd097e34d4dadad14cdf5)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the signing profile created.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrProfileName")
    def attr_profile_name(self) -> builtins.str:
        '''The name of the signing profile created.

        :cloudformationAttribute: ProfileName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrProfileName"))

    @builtins.property
    @jsii.member(jsii_name="attrProfileVersion")
    def attr_profile_version(self) -> builtins.str:
        '''The version of the signing profile created.

        :cloudformationAttribute: ProfileVersion
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrProfileVersion"))

    @builtins.property
    @jsii.member(jsii_name="attrProfileVersionArn")
    def attr_profile_version_arn(self) -> builtins.str:
        '''The signing profile ARN, including the profile version.

        :cloudformationAttribute: ProfileVersionArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrProfileVersionArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="signingProfileRef")
    def signing_profile_ref(self) -> "_aws_signer_fcf3aa48.SigningProfileReference":
        '''A reference to a SigningProfile resource.'''
        return typing.cast("_aws_signer_fcf3aa48.SigningProfileReference", jsii.get(self, "signingProfileRef"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> "_aws_cdk_0cae9daa.TagManager":
        '''Tag Manager which manages the tags for this resource.'''
        return typing.cast("_aws_cdk_0cae9daa.TagManager", jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="platformId")
    def platform_id(self) -> builtins.str:
        '''The ID of a platform that is available for use by a signing profile.'''
        return typing.cast(builtins.str, jsii.get(self, "platformId"))

    @platform_id.setter
    def platform_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__fe4af9baf88789da4f861a18d37152a49a2947c30e555d2e1fff8d9d3f3d5f1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "platformId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="profileName")
    def profile_name(self) -> typing.Optional[builtins.str]:
        '''The name of the signing profile.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "profileName"))

    @profile_name.setter
    def profile_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__2972dbaf65147ccdb4e647ac0428126af6fbc8681dd95b936d84537b98769a3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profileName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="signatureValidityPeriod")
    def signature_validity_period(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnSigningProfile.SignatureValidityPeriodProperty"]]:
        '''The validity period override for any signature generated using this signing profile.'''
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnSigningProfile.SignatureValidityPeriodProperty"]], jsii.get(self, "signatureValidityPeriod"))

    @signature_validity_period.setter
    def signature_validity_period(
        self,
        value: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnSigningProfile.SignatureValidityPeriodProperty"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d3142352951a0c8c38151f31fb1da21f644b00a82a7383e211cfa3feb49aaea8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signatureValidityPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsRaw")
    def tags_raw(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''A list of tags associated with the signing profile.'''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tagsRaw"))

    @tags_raw.setter
    def tags_raw(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__580ec6652b4c39cad7404de2ec2116ee0ba26fab741371a13d0201ad7c60ad0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsRaw", value) # pyright: ignore[reportArgumentType]

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_signer.CfnSigningProfile.SignatureValidityPeriodProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "value": "value"},
    )
    class SignatureValidityPeriodProperty:
        def __init__(
            self,
            *,
            type: typing.Optional[builtins.str] = None,
            value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The validity period for the signing job.

            :param type: The time unit for signature validity: DAYS | MONTHS | YEARS.
            :param value: The numerical value of the time unit for signature validity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-signer-signingprofile-signaturevalidityperiod.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_signer as signer
                
                signature_validity_period_property = signer.CfnSigningProfile.SignatureValidityPeriodProperty(
                    type="type",
                    value=123
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__3efe44bef5492c74fa08cef22b7e2a158db85808147bf0c6792e238cfdcc5fa4)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The time unit for signature validity: DAYS | MONTHS | YEARS.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-signer-signingprofile-signaturevalidityperiod.html#cfn-signer-signingprofile-signaturevalidityperiod-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            '''The numerical value of the time unit for signature validity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-signer-signingprofile-signaturevalidityperiod.html#cfn-signer-signingprofile-signaturevalidityperiod-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SignatureValidityPeriodProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_signer.CfnSigningProfileProps",
    jsii_struct_bases=[],
    name_mapping={
        "platform_id": "platformId",
        "profile_name": "profileName",
        "signature_validity_period": "signatureValidityPeriod",
        "tags": "tags",
    },
)
class CfnSigningProfileProps:
    def __init__(
        self,
        *,
        platform_id: builtins.str,
        profile_name: typing.Optional[builtins.str] = None,
        signature_validity_period: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnSigningProfile.SignatureValidityPeriodProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnSigningProfile``.

        :param platform_id: The ID of a platform that is available for use by a signing profile.
        :param profile_name: The name of the signing profile.
        :param signature_validity_period: The validity period override for any signature generated using this signing profile. If unspecified, the default is 135 months.
        :param tags: A list of tags associated with the signing profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-signingprofile.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_signer as signer
            
            cfn_signing_profile_props = signer.CfnSigningProfileProps(
                platform_id="platformId",
            
                # the properties below are optional
                profile_name="profileName",
                signature_validity_period=signer.CfnSigningProfile.SignatureValidityPeriodProperty(
                    type="type",
                    value=123
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__9e40d7ccf57c93b4e1db5a4e6b98b562bce8ff86b219931d0d4cfb16a346cb0e)
            check_type(argname="argument platform_id", value=platform_id, expected_type=type_hints["platform_id"])
            check_type(argname="argument profile_name", value=profile_name, expected_type=type_hints["profile_name"])
            check_type(argname="argument signature_validity_period", value=signature_validity_period, expected_type=type_hints["signature_validity_period"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "platform_id": platform_id,
        }
        if profile_name is not None:
            self._values["profile_name"] = profile_name
        if signature_validity_period is not None:
            self._values["signature_validity_period"] = signature_validity_period
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def platform_id(self) -> builtins.str:
        '''The ID of a platform that is available for use by a signing profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-signingprofile.html#cfn-signer-signingprofile-platformid
        '''
        result = self._values.get("platform_id")
        assert result is not None, "Required property 'platform_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def profile_name(self) -> typing.Optional[builtins.str]:
        '''The name of the signing profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-signingprofile.html#cfn-signer-signingprofile-profilename
        '''
        result = self._values.get("profile_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def signature_validity_period(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnSigningProfile.SignatureValidityPeriodProperty"]]:
        '''The validity period override for any signature generated using this signing profile.

        If unspecified, the default is 135 months.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-signingprofile.html#cfn-signer-signingprofile-signaturevalidityperiod
        '''
        result = self._values.get("signature_validity_period")
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnSigningProfile.SignatureValidityPeriodProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''A list of tags associated with the signing profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-signingprofile.html#cfn-signer-signingprofile-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSigningProfileProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="aws-cdk-lib.aws_signer.ISigningProfile")
class ISigningProfile(
    _aws_cdk_0cae9daa.IResource,
    _aws_signer_fcf3aa48.ISigningProfileRef,
    typing_extensions.Protocol,
):
    '''A Signer Profile.'''

    @builtins.property
    @jsii.member(jsii_name="signingProfileArn")
    def signing_profile_arn(self) -> builtins.str:
        '''The ARN of the signing profile.

        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="signingProfileName")
    def signing_profile_name(self) -> builtins.str:
        '''The name of signing profile.

        :attribute: ProfileName
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="signingProfileVersion")
    def signing_profile_version(self) -> builtins.str:
        '''The version of signing profile.

        :attribute: ProfileVersion
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="signingProfileVersionArn")
    def signing_profile_version_arn(self) -> builtins.str:
        '''The ARN of signing profile version.

        :attribute: ProfileVersionArn
        '''
        ...


class _ISigningProfileProxy(
    jsii.proxy_for(_aws_cdk_0cae9daa.IResource), # type: ignore[misc]
    jsii.proxy_for(_aws_signer_fcf3aa48.ISigningProfileRef), # type: ignore[misc]
):
    '''A Signer Profile.'''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.aws_signer.ISigningProfile"

    @builtins.property
    @jsii.member(jsii_name="signingProfileArn")
    def signing_profile_arn(self) -> builtins.str:
        '''The ARN of the signing profile.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "signingProfileArn"))

    @builtins.property
    @jsii.member(jsii_name="signingProfileName")
    def signing_profile_name(self) -> builtins.str:
        '''The name of signing profile.

        :attribute: ProfileName
        '''
        return typing.cast(builtins.str, jsii.get(self, "signingProfileName"))

    @builtins.property
    @jsii.member(jsii_name="signingProfileVersion")
    def signing_profile_version(self) -> builtins.str:
        '''The version of signing profile.

        :attribute: ProfileVersion
        '''
        return typing.cast(builtins.str, jsii.get(self, "signingProfileVersion"))

    @builtins.property
    @jsii.member(jsii_name="signingProfileVersionArn")
    def signing_profile_version_arn(self) -> builtins.str:
        '''The ARN of signing profile version.

        :attribute: ProfileVersionArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "signingProfileVersionArn"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISigningProfile).__jsii_proxy_class__ = lambda : _ISigningProfileProxy


class Platform(metaclass=jsii.JSIIMeta, jsii_type="aws-cdk-lib.aws_signer.Platform"):
    '''Platforms that are allowed with signing config.

    :see: https://docs.aws.amazon.com/signer/latest/developerguide/gs-platform.html
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_signer as signer
        
        
        signing_profile = signer.SigningProfile(self, "SigningProfile",
            platform=signer.Platform.AWS_LAMBDA_SHA384_ECDSA
        )
        
        code_signing_config = lambda_.CodeSigningConfig(self, "CodeSigningConfig",
            signing_profiles=[signing_profile]
        )
        
        lambda_.Function(self, "Function",
            code_signing_config=code_signing_config,
            runtime=lambda_.Runtime.NODEJS_LATEST,
            handler="index.handler",
            code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler"))
        )
    '''

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, platform_id: builtins.str) -> "Platform":
        '''Custom signing profile platform.

        :param platform_id: - The id of signing platform.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-signer-signingprofile.html#cfn-signer-signingprofile-platformid
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d87af39f6269f8a900ddd70cc76e7c44cea15649627230d7b387b9814c9d1672)
            check_type(argname="argument platform_id", value=platform_id, expected_type=type_hints["platform_id"])
        return typing.cast("Platform", jsii.sinvoke(cls, "of", [platform_id]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_FREE_RTOS_DEFAULT")
    def AMAZON_FREE_RTOS_DEFAULT(cls) -> "Platform":
        '''(deprecated) Specification of signature format and signing algorithms with SHA256 hash and ECDSA encryption for Amazon FreeRTOS.

        :deprecated: This signature platform has been discontinued.

        :stability: deprecated
        '''
        return typing.cast("Platform", jsii.sget(cls, "AMAZON_FREE_RTOS_DEFAULT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_FREE_RTOS_TI_CC3220SF")
    def AMAZON_FREE_RTOS_TI_CC3220_SF(cls) -> "Platform":
        '''(deprecated) Specification of signature format and signing algorithms with SHA1 hash and RSA encryption for Amazon FreeRTOS.

        :deprecated: This signature platform has been discontinued.

        :stability: deprecated
        '''
        return typing.cast("Platform", jsii.sget(cls, "AMAZON_FREE_RTOS_TI_CC3220SF"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AWS_IOT_DEVICE_MANAGEMENT_SHA256_ECDSA")
    def AWS_IOT_DEVICE_MANAGEMENT_SHA256_ECDSA(cls) -> "Platform":
        '''Specification of signature format and signing algorithms for AWS IoT Device.'''
        return typing.cast("Platform", jsii.sget(cls, "AWS_IOT_DEVICE_MANAGEMENT_SHA256_ECDSA"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AWS_LAMBDA_SHA384_ECDSA")
    def AWS_LAMBDA_SHA384_ECDSA(cls) -> "Platform":
        '''Specification of signature format and signing algorithms for AWS Lambda.'''
        return typing.cast("Platform", jsii.sget(cls, "AWS_LAMBDA_SHA384_ECDSA"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="NOTATION_OCI_SHA384_ECDSA")
    def NOTATION_OCI_SHA384_ECDSA(cls) -> "Platform":
        '''Specification of signature format and signing algorithms with SHA256 hash and ECDSA encryption for container registries with notation.'''
        return typing.cast("Platform", jsii.sget(cls, "NOTATION_OCI_SHA384_ECDSA"))

    @builtins.property
    @jsii.member(jsii_name="platformId")
    def platform_id(self) -> builtins.str:
        '''- The id of signing platform.'''
        return typing.cast(builtins.str, jsii.get(self, "platformId"))


@jsii.implements(ISigningProfile)
class SigningProfile(
    _aws_cdk_0cae9daa.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_signer.SigningProfile",
):
    '''Defines a Signing Profile.

    :resource: AWS::Signer::SigningProfile
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_signer as signer
        
        
        signing_profile = signer.SigningProfile(self, "SigningProfile",
            platform=signer.Platform.AWS_LAMBDA_SHA384_ECDSA
        )
        
        code_signing_config = lambda_.CodeSigningConfig(self, "CodeSigningConfig",
            signing_profiles=[signing_profile]
        )
        
        lambda_.Function(self, "Function",
            code_signing_config=code_signing_config,
            runtime=lambda_.Runtime.NODEJS_LATEST,
            handler="index.handler",
            code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler"))
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        platform: "Platform",
        signature_validity: typing.Optional["_aws_cdk_0cae9daa.Duration"] = None,
        signing_profile_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param platform: The Signing Platform available for signing profile.
        :param signature_validity: The validity period for signatures generated using this signing profile. Default: - 135 months
        :param signing_profile_name: Physical name of this Signing Profile. Default: - Assigned by CloudFormation (recommended).
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__98d9bc1982105f0416e608780fc4048b7d0a29f62734adc8b7c72c6ddb875169)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SigningProfileProps(
            platform=platform,
            signature_validity=signature_validity,
            signing_profile_name=signing_profile_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromSigningProfileAttributes")
    @builtins.classmethod
    def from_signing_profile_attributes(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        signing_profile_name: builtins.str,
        signing_profile_version: builtins.str,
    ) -> "ISigningProfile":
        '''Creates a Signing Profile construct that represents an external Signing Profile.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param signing_profile_name: The name of signing profile.
        :param signing_profile_version: The version of signing profile.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__dc8f241831391377f031dff9aa28ccba43b2e0c1261214e4326b1d0b861b1e9e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = SigningProfileAttributes(
            signing_profile_name=signing_profile_name,
            signing_profile_version=signing_profile_version,
        )

        return typing.cast("ISigningProfile", jsii.sinvoke(cls, "fromSigningProfileAttributes", [scope, id, attrs]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''Uniquely identifies this class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="signingProfileArn")
    def signing_profile_arn(self) -> builtins.str:
        '''The ARN of the signing profile.'''
        return typing.cast(builtins.str, jsii.get(self, "signingProfileArn"))

    @builtins.property
    @jsii.member(jsii_name="signingProfileName")
    def signing_profile_name(self) -> builtins.str:
        '''The name of signing profile.'''
        return typing.cast(builtins.str, jsii.get(self, "signingProfileName"))

    @builtins.property
    @jsii.member(jsii_name="signingProfileRef")
    def signing_profile_ref(self) -> "_aws_signer_fcf3aa48.SigningProfileReference":
        '''A reference to a SigningProfile resource.'''
        return typing.cast("_aws_signer_fcf3aa48.SigningProfileReference", jsii.get(self, "signingProfileRef"))

    @builtins.property
    @jsii.member(jsii_name="signingProfileVersion")
    def signing_profile_version(self) -> builtins.str:
        '''The version of signing profile.'''
        return typing.cast(builtins.str, jsii.get(self, "signingProfileVersion"))

    @builtins.property
    @jsii.member(jsii_name="signingProfileVersionArn")
    def signing_profile_version_arn(self) -> builtins.str:
        '''The ARN of signing profile version.'''
        return typing.cast(builtins.str, jsii.get(self, "signingProfileVersionArn"))


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_signer.SigningProfileAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "signing_profile_name": "signingProfileName",
        "signing_profile_version": "signingProfileVersion",
    },
)
class SigningProfileAttributes:
    def __init__(
        self,
        *,
        signing_profile_name: builtins.str,
        signing_profile_version: builtins.str,
    ) -> None:
        '''A reference to a Signing Profile.

        :param signing_profile_name: The name of signing profile.
        :param signing_profile_version: The version of signing profile.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_signer as signer
            
            signing_profile_attributes = signer.SigningProfileAttributes(
                signing_profile_name="signingProfileName",
                signing_profile_version="signingProfileVersion"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__322df56afb65c36b455aea6e5bb84898157da190e69f2f74001dcb0db998fcca)
            check_type(argname="argument signing_profile_name", value=signing_profile_name, expected_type=type_hints["signing_profile_name"])
            check_type(argname="argument signing_profile_version", value=signing_profile_version, expected_type=type_hints["signing_profile_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "signing_profile_name": signing_profile_name,
            "signing_profile_version": signing_profile_version,
        }

    @builtins.property
    def signing_profile_name(self) -> builtins.str:
        '''The name of signing profile.'''
        result = self._values.get("signing_profile_name")
        assert result is not None, "Required property 'signing_profile_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def signing_profile_version(self) -> builtins.str:
        '''The version of signing profile.'''
        result = self._values.get("signing_profile_version")
        assert result is not None, "Required property 'signing_profile_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SigningProfileAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_signer.SigningProfileProps",
    jsii_struct_bases=[],
    name_mapping={
        "platform": "platform",
        "signature_validity": "signatureValidity",
        "signing_profile_name": "signingProfileName",
    },
)
class SigningProfileProps:
    def __init__(
        self,
        *,
        platform: "Platform",
        signature_validity: typing.Optional["_aws_cdk_0cae9daa.Duration"] = None,
        signing_profile_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Construction properties for a Signing Profile object.

        :param platform: The Signing Platform available for signing profile.
        :param signature_validity: The validity period for signatures generated using this signing profile. Default: - 135 months
        :param signing_profile_name: Physical name of this Signing Profile. Default: - Assigned by CloudFormation (recommended).

        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_signer as signer
            
            
            signing_profile = signer.SigningProfile(self, "SigningProfile",
                platform=signer.Platform.AWS_LAMBDA_SHA384_ECDSA
            )
            
            code_signing_config = lambda_.CodeSigningConfig(self, "CodeSigningConfig",
                signing_profiles=[signing_profile]
            )
            
            lambda_.Function(self, "Function",
                code_signing_config=code_signing_config,
                runtime=lambda_.Runtime.NODEJS_LATEST,
                handler="index.handler",
                code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler"))
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ec491d4441d5ea10770b4741a09e04ab0b29fa9f7cfddbbaa4ee950829f0085f)
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument signature_validity", value=signature_validity, expected_type=type_hints["signature_validity"])
            check_type(argname="argument signing_profile_name", value=signing_profile_name, expected_type=type_hints["signing_profile_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "platform": platform,
        }
        if signature_validity is not None:
            self._values["signature_validity"] = signature_validity
        if signing_profile_name is not None:
            self._values["signing_profile_name"] = signing_profile_name

    @builtins.property
    def platform(self) -> "Platform":
        '''The Signing Platform available for signing profile.

        :see: https://docs.aws.amazon.com/signer/latest/developerguide/gs-platform.html
        '''
        result = self._values.get("platform")
        assert result is not None, "Required property 'platform' is missing"
        return typing.cast("Platform", result)

    @builtins.property
    def signature_validity(self) -> typing.Optional["_aws_cdk_0cae9daa.Duration"]:
        '''The validity period for signatures generated using this signing profile.

        :default: - 135 months
        '''
        result = self._values.get("signature_validity")
        return typing.cast(typing.Optional["_aws_cdk_0cae9daa.Duration"], result)

    @builtins.property
    def signing_profile_name(self) -> typing.Optional[builtins.str]:
        '''Physical name of this Signing Profile.

        :default: - Assigned by CloudFormation (recommended).
        '''
        result = self._values.get("signing_profile_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SigningProfileProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnProfilePermission",
    "CfnProfilePermissionProps",
    "CfnSigningJob",
    "CfnSigningJobProps",
    "CfnSigningProfile",
    "CfnSigningProfileProps",
    "ISigningProfile",
    "Platform",
    "SigningProfile",
    "SigningProfileAttributes",
    "SigningProfileProps",
]

publication.publish()

def _typecheckingstub__7b7dd51e7eac664b5afe9a1b7d1972f7da8883244b3f554de5c8d1e0cc84f053(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    action: builtins.str,
    principal: builtins.str,
    profile_name: builtins.str,
    statement_id: builtins.str,
    profile_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa9b2b5c20a313a6a8736730c6a3112613d411a11743beb2f9de986fce357c4a(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c27c534af2f676e9fe9c9b1c8462b7339b8b65f0c4b9b08f485033feefe4741(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__662ce8c205095e7c693616c7c2d43b18432d9c948d131c1a3e91e7b5aafc2323(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b8c32d87b73fa4fb5094ae3e46175df93629f45d64c0d2b3130d5471eca086e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37b3db8c74061df8a65eeda431f6a41091db1cf687f78d71f79a9441f95b0644(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0284177166884a4428819ca021ca73daecd877943a7bf90e79aec6e00f5ad07a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e8ca5148f26e102d75c04bb95550132d3a29824e2932a98f9f87725df3962fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80bd95afa9c654fc5d026db2cad497a96dc240f466154896c0c5c3cc15b54bdd(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc7158edcf57ecc13c1e912574c38dd0ad2f9585f23f02536376f63ed728fe86(
    *,
    action: builtins.str,
    principal: builtins.str,
    profile_name: builtins.str,
    statement_id: builtins.str,
    profile_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab4bda8b7d5eaea8c6dc7889d4296f6ea822b1c2cb553c36b67a116ed558b6c5(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    profile_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dcb26787091b618a59a613bf0f199239b366e05b44cde3663af37bf978e09e0(
    resource: _aws_signer_fcf3aa48.ISigningJobRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90f411dd9a69746e85dc03853e0db69f25857f2c81107040f333fca5e6c96d96(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abe96d636a14bb3f70be144a1f7e704b482e30d63d75628d33a1e95c0bd048f8(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__791e96e43922635f4184768f9bba8ebfa19e53ae037914b01c76c0f7e3586602(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf7baa61b0509981041de7ab4c5c9b09955802ce8be72bf4e42f3afb9e654b21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58836aeb809f68ae4865dad7598c85530241b919317954f6976c9edc5757081f(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ade25d735cba1b883bfc479fef183a91da725ebb30105c3d60cbf32df16d16d(
    *,
    bucket_name: builtins.str,
    key: builtins.str,
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acc54aa7f5738da3a6d649a358b6c64501a1de92862a645694f512b0b18f6fa5(
    *,
    s3: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnSigningJob.S3SignedObjectProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4861fc8f98a207465561eede33a73377b1eaca415bea7844cd8e878050cf7f9b(
    *,
    s3: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnSigningJob.S3SourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8c57eff50d383c03cd8511b0bd7973e5b281f4f35609df6e7dc048909c6a732(
    *,
    profile_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d84fe196f81722ce814c09f8bd21719acd97c32e92c1de922d0f04c31912d65b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    platform_id: builtins.str,
    profile_name: typing.Optional[builtins.str] = None,
    signature_validity_period: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnSigningProfile.SignatureValidityPeriodProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f88b9c5ab8f3709756f086e40d555988785e2364dbe7e70f2cd9c77e7cc59634(
    resource: _aws_signer_fcf3aa48.ISigningProfileRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3e32d4beb10fbb8b17ae147070d2bc9be76eea0d4a93458b396357b7b5d3473(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__796b31e3d9d2ce1d3b20283186f1c0c54ce0f3bb426633c056466f92264e35b9(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59eb44451cc01c28f44f21713cf6296a564f672edd6fd097e34d4dadad14cdf5(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe4af9baf88789da4f861a18d37152a49a2947c30e555d2e1fff8d9d3f3d5f1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2972dbaf65147ccdb4e647ac0428126af6fbc8681dd95b936d84537b98769a3e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3142352951a0c8c38151f31fb1da21f644b00a82a7383e211cfa3feb49aaea8(
    value: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnSigningProfile.SignatureValidityPeriodProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__580ec6652b4c39cad7404de2ec2116ee0ba26fab741371a13d0201ad7c60ad0c(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3efe44bef5492c74fa08cef22b7e2a158db85808147bf0c6792e238cfdcc5fa4(
    *,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e40d7ccf57c93b4e1db5a4e6b98b562bce8ff86b219931d0d4cfb16a346cb0e(
    *,
    platform_id: builtins.str,
    profile_name: typing.Optional[builtins.str] = None,
    signature_validity_period: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnSigningProfile.SignatureValidityPeriodProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d87af39f6269f8a900ddd70cc76e7c44cea15649627230d7b387b9814c9d1672(
    platform_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98d9bc1982105f0416e608780fc4048b7d0a29f62734adc8b7c72c6ddb875169(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    platform: Platform,
    signature_validity: typing.Optional[_aws_cdk_0cae9daa.Duration] = None,
    signing_profile_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc8f241831391377f031dff9aa28ccba43b2e0c1261214e4326b1d0b861b1e9e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    signing_profile_name: builtins.str,
    signing_profile_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__322df56afb65c36b455aea6e5bb84898157da190e69f2f74001dcb0db998fcca(
    *,
    signing_profile_name: builtins.str,
    signing_profile_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec491d4441d5ea10770b4741a09e04ab0b29fa9f7cfddbbaa4ee950829f0085f(
    *,
    platform: Platform,
    signature_validity: typing.Optional[_aws_cdk_0cae9daa.Duration] = None,
    signing_profile_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

for cls in [ISigningProfile]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
