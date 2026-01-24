r'''
# resources module

<!--BEGIN STABILITY BANNER-->---


![Stability: Experimental](https://img.shields.io/badge/stability-Experimental-important.svg?style=for-the-badge)

> All classes are under active development and subject to non-backward compatible changes or removal in any
> future version. These are not subject to the [Semantic Versioning](https://semver.org/) model.
> This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

| **Reference Documentation**:| <span style="font-weight: normal">https://docs.aws.amazon.com/solutions/latest/constructs/</span>|
|:-------------|:-------------|

<div style="height:8px"></div>

The resources library contains reusable resources that can be leveraged from solutions constructs. These resources are deployable units with their own sets of integration tests (to contrast them with the solutions constructs `core` library).

The first resource being published is the `template-writer`, which does automatic text transformation/substiution, implemented as a custom resource, and run as part of a CloudFormation stack Create/Update/Delete lifecycle. Some use-cases for using the `template-writer` resource can be seen in the `aws-openapigateway-lambda` Solutions Construct, where it transforms an incoming OpenAPI Definition (residing locally or in S3) by auto-populating the `uri` fields of the `x-amazon-apigateway-integration` integrations with the resolved value of the backing lambda functions.
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

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_cloudfront as _aws_cdk_aws_cloudfront_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d


@jsii.data_type(
    jsii_type="@aws-solutions-constructs/resources.CreateKeyPolicyUpdaterResponse",
    jsii_struct_bases=[],
    name_mapping={
        "custom_resource": "customResource",
        "lambda_function": "lambdaFunction",
    },
)
class CreateKeyPolicyUpdaterResponse:
    def __init__(
        self,
        *,
        custom_resource: _aws_cdk_ceddda9d.CustomResource,
        lambda_function: _aws_cdk_aws_lambda_ceddda9d.Function,
    ) -> None:
        '''
        :param custom_resource: -
        :param lambda_function: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db2d9ca4922707514a16e9e7adca6e36754836876b9ff802d8a838ae0149487a)
            check_type(argname="argument custom_resource", value=custom_resource, expected_type=type_hints["custom_resource"])
            check_type(argname="argument lambda_function", value=lambda_function, expected_type=type_hints["lambda_function"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "custom_resource": custom_resource,
            "lambda_function": lambda_function,
        }

    @builtins.property
    def custom_resource(self) -> _aws_cdk_ceddda9d.CustomResource:
        result = self._values.get("custom_resource")
        assert result is not None, "Required property 'custom_resource' is missing"
        return typing.cast(_aws_cdk_ceddda9d.CustomResource, result)

    @builtins.property
    def lambda_function(self) -> _aws_cdk_aws_lambda_ceddda9d.Function:
        result = self._values.get("lambda_function")
        assert result is not None, "Required property 'lambda_function' is missing"
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.Function, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CreateKeyPolicyUpdaterResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-solutions-constructs/resources.CreateTemplateWriterResponse",
    jsii_struct_bases=[],
    name_mapping={
        "custom_resource": "customResource",
        "s3_bucket": "s3Bucket",
        "s3_key": "s3Key",
    },
)
class CreateTemplateWriterResponse:
    def __init__(
        self,
        *,
        custom_resource: _aws_cdk_ceddda9d.CustomResource,
        s3_bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        s3_key: builtins.str,
    ) -> None:
        '''
        :param custom_resource: -
        :param s3_bucket: -
        :param s3_key: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9875a381803cda5616956080ef2d7dca10defd66f5a2b13144fc9f009e550510)
            check_type(argname="argument custom_resource", value=custom_resource, expected_type=type_hints["custom_resource"])
            check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
            check_type(argname="argument s3_key", value=s3_key, expected_type=type_hints["s3_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "custom_resource": custom_resource,
            "s3_bucket": s3_bucket,
            "s3_key": s3_key,
        }

    @builtins.property
    def custom_resource(self) -> _aws_cdk_ceddda9d.CustomResource:
        result = self._values.get("custom_resource")
        assert result is not None, "Required property 'custom_resource' is missing"
        return typing.cast(_aws_cdk_ceddda9d.CustomResource, result)

    @builtins.property
    def s3_bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        result = self._values.get("s3_bucket")
        assert result is not None, "Required property 's3_bucket' is missing"
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, result)

    @builtins.property
    def s3_key(self) -> builtins.str:
        result = self._values.get("s3_key")
        assert result is not None, "Required property 's3_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CreateTemplateWriterResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-solutions-constructs/resources.KeyPolicyUpdaterProps",
    jsii_struct_bases=[],
    name_mapping={
        "distribution": "distribution",
        "encryption_key": "encryptionKey",
        "memory_size": "memorySize",
        "timeout": "timeout",
    },
)
class KeyPolicyUpdaterProps:
    def __init__(
        self,
        *,
        distribution: _aws_cdk_aws_cloudfront_ceddda9d.Distribution,
        encryption_key: _aws_cdk_aws_kms_ceddda9d.IKey,
        memory_size: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''
        :param distribution: -
        :param encryption_key: -
        :param memory_size: -
        :param timeout: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__091fa1427d76d318b5fec71b78b097c9dcc0876002c77e0526d5c4b19401a0c2)
            check_type(argname="argument distribution", value=distribution, expected_type=type_hints["distribution"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument memory_size", value=memory_size, expected_type=type_hints["memory_size"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "distribution": distribution,
            "encryption_key": encryption_key,
        }
        if memory_size is not None:
            self._values["memory_size"] = memory_size
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def distribution(self) -> _aws_cdk_aws_cloudfront_ceddda9d.Distribution:
        result = self._values.get("distribution")
        assert result is not None, "Required property 'distribution' is missing"
        return typing.cast(_aws_cdk_aws_cloudfront_ceddda9d.Distribution, result)

    @builtins.property
    def encryption_key(self) -> _aws_cdk_aws_kms_ceddda9d.IKey:
        result = self._values.get("encryption_key")
        assert result is not None, "Required property 'encryption_key' is missing"
        return typing.cast(_aws_cdk_aws_kms_ceddda9d.IKey, result)

    @builtins.property
    def memory_size(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("memory_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyPolicyUpdaterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-solutions-constructs/resources.TemplateValue",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "value": "value"},
)
class TemplateValue:
    def __init__(self, *, id: builtins.str, value: builtins.str) -> None:
        '''The TemplateValue interface defines the id-value pair that will be substituted in the template.

        For example, given the template:
        template:
        hello name_placeholder, nice to meet you

        and an instantiation of TemplateValue { id: 'name_placeholder', value: 'jeff' }

        the template will be transformed to:
        template:
        hello jeff, nice to meet you

        :param id: The placeholder string to be replaced in the template.
        :param value: The value to replace the placeholder in the template with.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07edd751bd56e6c333e2880fa79c00732a419aacb20ed9d3bf1018601fde9816)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "value": value,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''The placeholder string to be replaced in the template.'''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The value to replace the placeholder in the template with.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TemplateValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-solutions-constructs/resources.TemplateWriterProps",
    jsii_struct_bases=[],
    name_mapping={
        "template_bucket": "templateBucket",
        "template_key": "templateKey",
        "template_values": "templateValues",
        "memory_size": "memorySize",
        "timeout": "timeout",
    },
)
class TemplateWriterProps:
    def __init__(
        self,
        *,
        template_bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        template_key: builtins.str,
        template_values: typing.Sequence[typing.Union[TemplateValue, typing.Dict[builtins.str, typing.Any]]],
        memory_size: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''
        :param template_bucket: The S3 bucket that holds the template to transform. Upstream this can come either from an Asset or S3 bucket directly. Internally it will always resolve to S3 bucket in either case (the cdk asset bucket or the customer-defined bucket).
        :param template_key: The S3 object key of the template to transform.
        :param template_values: An array of TemplateValue objects, each defining a placeholder string in the template that will be replaced with its corresponding value.
        :param memory_size: Optional configuration for user-defined memorySize of the backing Lambda function, which may be necessary when transforming very large objects. Default: 128
        :param timeout: Optional configuration for user-defined duration of the backing Lambda function, which may be necessary when transforming very large objects. Default: Duration.seconds(3)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d405c0230bc215a1bf6decb772d82168f126bb36206887f35518835d644f0b4f)
            check_type(argname="argument template_bucket", value=template_bucket, expected_type=type_hints["template_bucket"])
            check_type(argname="argument template_key", value=template_key, expected_type=type_hints["template_key"])
            check_type(argname="argument template_values", value=template_values, expected_type=type_hints["template_values"])
            check_type(argname="argument memory_size", value=memory_size, expected_type=type_hints["memory_size"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "template_bucket": template_bucket,
            "template_key": template_key,
            "template_values": template_values,
        }
        if memory_size is not None:
            self._values["memory_size"] = memory_size
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def template_bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        '''The S3 bucket that holds the template to transform.

        Upstream this can come either from an Asset or S3 bucket directly.
        Internally it will always resolve to S3 bucket in either case (the cdk asset bucket or the customer-defined bucket).
        '''
        result = self._values.get("template_bucket")
        assert result is not None, "Required property 'template_bucket' is missing"
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, result)

    @builtins.property
    def template_key(self) -> builtins.str:
        '''The S3 object key of the template to transform.'''
        result = self._values.get("template_key")
        assert result is not None, "Required property 'template_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def template_values(self) -> typing.List[TemplateValue]:
        '''An array of TemplateValue objects, each defining a placeholder string in the template that will be replaced with its corresponding value.'''
        result = self._values.get("template_values")
        assert result is not None, "Required property 'template_values' is missing"
        return typing.cast(typing.List[TemplateValue], result)

    @builtins.property
    def memory_size(self) -> typing.Optional[jsii.Number]:
        '''Optional configuration for user-defined memorySize of the backing Lambda function, which may be necessary when transforming very large objects.

        :default: 128
        '''
        result = self._values.get("memory_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''Optional configuration for user-defined duration of the backing Lambda function, which may be necessary when transforming very large objects.

        :default: Duration.seconds(3)
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TemplateWriterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CreateKeyPolicyUpdaterResponse",
    "CreateTemplateWriterResponse",
    "KeyPolicyUpdaterProps",
    "TemplateValue",
    "TemplateWriterProps",
]

publication.publish()

def _typecheckingstub__db2d9ca4922707514a16e9e7adca6e36754836876b9ff802d8a838ae0149487a(
    *,
    custom_resource: _aws_cdk_ceddda9d.CustomResource,
    lambda_function: _aws_cdk_aws_lambda_ceddda9d.Function,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9875a381803cda5616956080ef2d7dca10defd66f5a2b13144fc9f009e550510(
    *,
    custom_resource: _aws_cdk_ceddda9d.CustomResource,
    s3_bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    s3_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__091fa1427d76d318b5fec71b78b097c9dcc0876002c77e0526d5c4b19401a0c2(
    *,
    distribution: _aws_cdk_aws_cloudfront_ceddda9d.Distribution,
    encryption_key: _aws_cdk_aws_kms_ceddda9d.IKey,
    memory_size: typing.Optional[jsii.Number] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07edd751bd56e6c333e2880fa79c00732a419aacb20ed9d3bf1018601fde9816(
    *,
    id: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d405c0230bc215a1bf6decb772d82168f126bb36206887f35518835d644f0b4f(
    *,
    template_bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    template_key: builtins.str,
    template_values: typing.Sequence[typing.Union[TemplateValue, typing.Dict[builtins.str, typing.Any]]],
    memory_size: typing.Optional[jsii.Number] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass
