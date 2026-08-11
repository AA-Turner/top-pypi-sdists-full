r'''
# AWS::Artifact Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_artifact as artifact
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for Artifact construct libraries](https://constructs.dev/search?q=artifact)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::Artifact resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Artifact.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Artifact](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Artifact.html).

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
    import aws_cdk.interfaces.aws_artifact as _aws_artifact_7564cbd6
    import constructs as _constructs_77d1e7e8
else:

    _aws_artifact_7564cbd6 = _LazyImport("aws_cdk.interfaces.aws_artifact")
    _aws_cdk_0cae9daa = _LazyImport("aws_cdk")
    _constructs_77d1e7e8 = _LazyImport("constructs")


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_artifact_7564cbd6.IReportRef)
class CfnReport(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_artifact.CfnReport",
):
    '''Resource schema for AWS Artifact Report.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-artifact-report.html
    :cloudformationResource: AWS::Artifact::Report
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_artifact as artifact
        
        cfn_report = artifact.CfnReport(self, "MyCfnReport")
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
    ) -> None:
        '''Create a new ``AWS::Artifact::Report``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__85b19b37a1f488261a4d7b865b2fed3007e9157244c1e9a3c3734f7787da9c83)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnReportProps()

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForReport")
    @builtins.classmethod
    def arn_for_report(
        cls,
        resource: "_aws_artifact_7564cbd6.IReportRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__fa6e3e04d063d46e9afe2fa0d585e786379976001daaba11a65897025a7d8657)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForReport", [resource]))

    @jsii.member(jsii_name="isCfnReport")
    @builtins.classmethod
    def is_cfn_report(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnReport.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__30bff0008233cad4f2fc5813e738908d9f45431f63a0bdfdd7a758c2c5e1272b)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnReport", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6e6437e28870f9ecdd5d3719c83181a4d10aa6f5f79ba268bec7e2bf95b22a09)
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
            type_hints = cached_type_hints(_typecheckingstub__866ff06996b1071b48e661057bfcc12c3671a91b95074da3ddf7d1ec106aa348)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAcceptanceType")
    def attr_acceptance_type(self) -> builtins.str:
        '''Acceptance type for report.

        :cloudformationAttribute: AcceptanceType
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAcceptanceType"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the report.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCategory")
    def attr_category(self) -> builtins.str:
        '''Category for the report resource.

        :cloudformationAttribute: Category
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCategory"))

    @builtins.property
    @jsii.member(jsii_name="attrCompanyName")
    def attr_company_name(self) -> builtins.str:
        '''Associated company name for the report resource.

        :cloudformationAttribute: CompanyName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCompanyName"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''Timestamp indicating when the report resource was created.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrDescription")
    def attr_description(self) -> builtins.str:
        '''Description for the report resource.

        :cloudformationAttribute: Description
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDescription"))

    @builtins.property
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        '''Name for the report resource.

        :cloudformationAttribute: Name
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrName"))

    @builtins.property
    @jsii.member(jsii_name="attrPeriodEnd")
    def attr_period_end(self) -> builtins.str:
        '''Timestamp indicating the report resource effective end.

        :cloudformationAttribute: PeriodEnd
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPeriodEnd"))

    @builtins.property
    @jsii.member(jsii_name="attrPeriodStart")
    def attr_period_start(self) -> builtins.str:
        '''Timestamp indicating the report resource effective start.

        :cloudformationAttribute: PeriodStart
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPeriodStart"))

    @builtins.property
    @jsii.member(jsii_name="attrProductName")
    def attr_product_name(self) -> builtins.str:
        '''Associated product name for the report resource.

        :cloudformationAttribute: ProductName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrProductName"))

    @builtins.property
    @jsii.member(jsii_name="attrReportId")
    def attr_report_id(self) -> builtins.str:
        '''Unique resource ID for the report resource.

        :cloudformationAttribute: ReportId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrReportId"))

    @builtins.property
    @jsii.member(jsii_name="attrSequenceNumber")
    def attr_sequence_number(self) -> jsii.Number:
        '''Sequence number to enforce optimistic locking.

        :cloudformationAttribute: SequenceNumber
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrSequenceNumber"))

    @builtins.property
    @jsii.member(jsii_name="attrSeries")
    def attr_series(self) -> builtins.str:
        '''Series for the report resource.

        :cloudformationAttribute: Series
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSeries"))

    @builtins.property
    @jsii.member(jsii_name="attrState")
    def attr_state(self) -> builtins.str:
        '''Current state of the report resource.

        :cloudformationAttribute: State
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrState"))

    @builtins.property
    @jsii.member(jsii_name="attrTermArn")
    def attr_term_arn(self) -> builtins.str:
        '''Unique resource ARN for term resource.

        :cloudformationAttribute: TermArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrTermArn"))

    @builtins.property
    @jsii.member(jsii_name="attrVersion")
    def attr_version(self) -> builtins.str:
        '''Version for the report resource.

        :cloudformationAttribute: Version
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVersion"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="reportRef")
    def report_ref(self) -> "_aws_artifact_7564cbd6.ReportReference":
        '''A reference to a Report resource.'''
        return typing.cast("_aws_artifact_7564cbd6.ReportReference", jsii.get(self, "reportRef"))


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_artifact.CfnReportProps",
    jsii_struct_bases=[],
    name_mapping={},
)
class CfnReportProps:
    def __init__(self) -> None:
        '''Properties for defining a ``CfnReport``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-artifact-report.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_artifact as artifact
            
            cfn_report_props = artifact.CfnReportProps()
        '''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReportProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnReport",
    "CfnReportProps",
]

publication.publish()

def _typecheckingstub__85b19b37a1f488261a4d7b865b2fed3007e9157244c1e9a3c3734f7787da9c83(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa6e3e04d063d46e9afe2fa0d585e786379976001daaba11a65897025a7d8657(
    resource: _aws_artifact_7564cbd6.IReportRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30bff0008233cad4f2fc5813e738908d9f45431f63a0bdfdd7a758c2c5e1272b(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e6437e28870f9ecdd5d3719c83181a4d10aa6f5f79ba268bec7e2bf95b22a09(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__866ff06996b1071b48e661057bfcc12c3671a91b95074da3ddf7d1ec106aa348(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass
