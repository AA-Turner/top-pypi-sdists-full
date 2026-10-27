r'''
# AWS::Polly Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_polly as polly
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for Polly construct libraries](https://constructs.dev/search?q=polly)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::Polly resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Polly.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Polly](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Polly.html).

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
    import aws_cdk.interfaces.aws_polly as _aws_polly_a9a0b132
    import constructs as _constructs_77d1e7e8
else:

    _aws_cdk_0cae9daa = _LazyImport("aws_cdk")
    _aws_polly_a9a0b132 = _LazyImport("aws_cdk.interfaces.aws_polly")
    _constructs_77d1e7e8 = _LazyImport("constructs")


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_polly_a9a0b132.ILexiconRef)
class CfnLexicon(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_polly.CfnLexicon",
):
    '''Resource Type definition for AWS::Polly::Lexicon.

    A pronunciation lexicon that stores custom pronunciations for speech synthesis.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-polly-lexicon.html
    :cloudformationResource: AWS::Polly::Lexicon
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_polly as polly
        
        cfn_lexicon = polly.CfnLexicon(self, "MyCfnLexicon",
            content="content",
            name="name"
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        content: builtins.str,
        name: builtins.str,
    ) -> None:
        '''Create a new ``AWS::Polly::Lexicon``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param content: The content of the PLS lexicon in string format.
        :param name: The name of the lexicon. Must be an alphanumeric string up to 20 characters long.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__4ef6edf96fa2f203907e6d95e21ea5010697b37a177a62719a3a841b24272ac2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLexiconProps(content=content, name=name)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForLexicon")
    @builtins.classmethod
    def arn_for_lexicon(
        cls,
        resource: "_aws_polly_a9a0b132.ILexiconRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__abaa70fbeca03e08f3066c7cae97bef8772749c359438b7c121a971cc610c532)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForLexicon", [resource]))

    @jsii.member(jsii_name="isCfnLexicon")
    @builtins.classmethod
    def is_cfn_lexicon(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnLexicon.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__10c9377ced75b54dfdcc3cee9bf439d5e9b3c4262a1b677af4e4a0a2c7fabba9)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnLexicon", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ef8a3d84f8c76ac426c6f2fb3d8fa741ee3fbde4fecc871ace1fe1f397c73e50)
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
            type_hints = cached_type_hints(_typecheckingstub__707a525822f80b639161bcb06f68951181184f9bd841706f269d90767ff1f3d9)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    @builtins.classmethod
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAlphabet")
    def attr_alphabet(self) -> builtins.str:
        '''The phonetic alphabet used in the lexicon.

        Valid values are ipa and x-sampa.

        :cloudformationAttribute: Alphabet
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAlphabet"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the lexicon.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrLanguageCode")
    def attr_language_code(self) -> builtins.str:
        '''The language code that the lexicon applies to.

        :cloudformationAttribute: LanguageCode
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLanguageCode"))

    @builtins.property
    @jsii.member(jsii_name="attrLastModified")
    def attr_last_modified(self) -> builtins.str:
        '''The date the lexicon was last modified (ISO 8601 timestamp).

        :cloudformationAttribute: LastModified
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastModified"))

    @builtins.property
    @jsii.member(jsii_name="attrLexemesCount")
    def attr_lexemes_count(self) -> jsii.Number:
        '''The number of lexemes in the lexicon.

        :cloudformationAttribute: LexemesCount
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrLexemesCount"))

    @builtins.property
    @jsii.member(jsii_name="attrSize")
    def attr_size(self) -> jsii.Number:
        '''The total size of the lexicon, in characters.

        :cloudformationAttribute: Size
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrSize"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="lexiconRef")
    def lexicon_ref(self) -> "_aws_polly_a9a0b132.LexiconReference":
        '''A reference to a Lexicon resource.'''
        return typing.cast("_aws_polly_a9a0b132.LexiconReference", jsii.get(self, "lexiconRef"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        '''The content of the PLS lexicon in string format.'''
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__dce9aed7c504a9d16480f41ad0fa13a68dbfca1ba476d6644591ea44c0ce2309)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the lexicon.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__0112de1f8bf6fd799799fc330f38741285e58d2fd084c7b7f87b67d3a5962606)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_polly.CfnLexiconProps",
    jsii_struct_bases=[],
    name_mapping={"content": "content", "name": "name"},
)
class CfnLexiconProps:
    def __init__(self, *, content: builtins.str, name: builtins.str) -> None:
        '''Properties for defining a ``CfnLexicon``.

        :param content: The content of the PLS lexicon in string format.
        :param name: The name of the lexicon. Must be an alphanumeric string up to 20 characters long.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-polly-lexicon.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_polly as polly
            
            cfn_lexicon_props = polly.CfnLexiconProps(
                content="content",
                name="name"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__47cfc34e8bded01f2f5913759ba8076fa52b653a2c8d78cd8b9e94fb9701f5e3)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
            "name": name,
        }

    @builtins.property
    def content(self) -> builtins.str:
        '''The content of the PLS lexicon in string format.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-polly-lexicon.html#cfn-polly-lexicon-content
        '''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the lexicon.

        Must be an alphanumeric string up to 20 characters long.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-polly-lexicon.html#cfn-polly-lexicon-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLexiconProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnLexicon",
    "CfnLexiconProps",
]

publication.publish()

def _typecheckingstub__4ef6edf96fa2f203907e6d95e21ea5010697b37a177a62719a3a841b24272ac2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    content: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abaa70fbeca03e08f3066c7cae97bef8772749c359438b7c121a971cc610c532(
    resource: _aws_polly_a9a0b132.ILexiconRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10c9377ced75b54dfdcc3cee9bf439d5e9b3c4262a1b677af4e4a0a2c7fabba9(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef8a3d84f8c76ac426c6f2fb3d8fa741ee3fbde4fecc871ace1fe1f397c73e50(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__707a525822f80b639161bcb06f68951181184f9bd841706f269d90767ff1f3d9(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dce9aed7c504a9d16480f41ad0fa13a68dbfca1ba476d6644591ea44c0ce2309(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0112de1f8bf6fd799799fc330f38741285e58d2fd084c7b7f87b67d3a5962606(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47cfc34e8bded01f2f5913759ba8076fa52b653a2c8d78cd8b9e94fb9701f5e3(
    *,
    content: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
