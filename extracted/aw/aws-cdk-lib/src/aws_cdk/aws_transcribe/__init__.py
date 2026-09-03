r'''
# AWS::Transcribe Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_transcribe as transcribe
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for Transcribe construct libraries](https://constructs.dev/search?q=transcribe)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::Transcribe resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Transcribe.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Transcribe](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Transcribe.html).

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
    import aws_cdk.interfaces.aws_transcribe as _aws_transcribe_5ed72ef1
    import constructs as _constructs_77d1e7e8
else:

    _aws_cdk_0cae9daa = _LazyImport("aws_cdk")
    _aws_transcribe_5ed72ef1 = _LazyImport("aws_cdk.interfaces.aws_transcribe")
    _constructs_77d1e7e8 = _LazyImport("constructs")


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_transcribe_5ed72ef1.IVocabularyFilterRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnVocabularyFilter(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_transcribe.CfnVocabularyFilter",
):
    '''Creates a custom vocabulary filter that you can use to mask, delete, or flag specific words from your transcript.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transcribe-vocabularyfilter.html
    :cloudformationResource: AWS::Transcribe::VocabularyFilter
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_transcribe as transcribe
        
        cfn_vocabulary_filter = transcribe.CfnVocabularyFilter(self, "MyCfnVocabularyFilter",
            language_code="languageCode",
            vocabulary_filter_name="vocabularyFilterName",
        
            # the properties below are optional
            data_access_role_arn="dataAccessRoleArn",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vocabulary_filter_file_uri="vocabularyFilterFileUri",
            words=["words"]
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        language_code: builtins.str,
        vocabulary_filter_name: builtins.str,
        data_access_role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
        vocabulary_filter_file_uri: typing.Optional[builtins.str] = None,
        words: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::Transcribe::VocabularyFilter``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param language_code: The language code that represents the language of the entries in your vocabulary filter.
        :param vocabulary_filter_name: A unique name, chosen by you, for your custom vocabulary filter.
        :param data_access_role_arn: The Amazon Resource Name (ARN) of an IAM role that has permissions to access the Amazon S3 bucket that contains your input files.
        :param tags: Tags associated with the vocabulary filter.
        :param vocabulary_filter_file_uri: The Amazon S3 location of the text file that contains your custom vocabulary filter terms.
        :param words: Use this parameter if you want to create your custom vocabulary filter by including all desired terms, as comma-separated values, within your request.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__4f379d43d1fb010196b1b7a0b7e190146a43a7817c4380b2a03c12a999b04403)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnVocabularyFilterProps(
            language_code=language_code,
            vocabulary_filter_name=vocabulary_filter_name,
            data_access_role_arn=data_access_role_arn,
            tags=tags,
            vocabulary_filter_file_uri=vocabulary_filter_file_uri,
            words=words,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForVocabularyFilter")
    @builtins.classmethod
    def arn_for_vocabulary_filter(
        cls,
        resource: "_aws_transcribe_5ed72ef1.IVocabularyFilterRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3d0d5fdd990c1e6f1f1578a57f2b1e07615e187c424de0cdb38c99ece36033ef)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForVocabularyFilter", [resource]))

    @jsii.member(jsii_name="isCfnVocabularyFilter")
    @builtins.classmethod
    def is_cfn_vocabulary_filter(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnVocabularyFilter.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b0842abbe55306ec5ea964df044d6068a3c93f961b8887d1ef9ab244365b53f9)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnVocabularyFilter", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__7e830e28f80376a22cc4875f2b2300dbc631c5e21a8ae0f3c1bd24ae3571e971)
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
            type_hints = cached_type_hints(_typecheckingstub__c5fffa3ebb60cbba9b4e3ded20ec86764ef3468786e2e8168b68abbe2f0d217a)
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
        '''The Amazon Resource Name (ARN) of the vocabulary filter.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

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
    @jsii.member(jsii_name="vocabularyFilterRef")
    def vocabulary_filter_ref(
        self,
    ) -> "_aws_transcribe_5ed72ef1.VocabularyFilterReference":
        '''A reference to a VocabularyFilter resource.'''
        return typing.cast("_aws_transcribe_5ed72ef1.VocabularyFilterReference", jsii.get(self, "vocabularyFilterRef"))

    @builtins.property
    @jsii.member(jsii_name="languageCode")
    def language_code(self) -> builtins.str:
        '''The language code that represents the language of the entries in your vocabulary filter.'''
        return typing.cast(builtins.str, jsii.get(self, "languageCode"))

    @language_code.setter
    def language_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__02de5607a020110473f71afee0afc19fa4d720c960821f6356e48a84d39652d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "languageCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vocabularyFilterName")
    def vocabulary_filter_name(self) -> builtins.str:
        '''A unique name, chosen by you, for your custom vocabulary filter.'''
        return typing.cast(builtins.str, jsii.get(self, "vocabularyFilterName"))

    @vocabulary_filter_name.setter
    def vocabulary_filter_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d4fd94c77da23e798b90215596efbf7d11955e5a50f658c75bdbda30e6f96924)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vocabularyFilterName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataAccessRoleArn")
    def data_access_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of an IAM role that has permissions to access the Amazon S3 bucket that contains your input files.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataAccessRoleArn"))

    @data_access_role_arn.setter
    def data_access_role_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__23780790450e1c427f7c6e5f873fd7e2b15f7d8b507361ef12a5cc0d96a0d21a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataAccessRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''Tags associated with the vocabulary filter.'''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__070bdd4161a53bdf7e27d3f41aa541151e5854ddbe9052abd9361fb6a8d67cb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vocabularyFilterFileUri")
    def vocabulary_filter_file_uri(self) -> typing.Optional[builtins.str]:
        '''The Amazon S3 location of the text file that contains your custom vocabulary filter terms.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vocabularyFilterFileUri"))

    @vocabulary_filter_file_uri.setter
    def vocabulary_filter_file_uri(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__bc1f52ba1318d8b74f111bca20754506fbde302f7929088130e8e1bc376e0c99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vocabularyFilterFileUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="words")
    def words(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Use this parameter if you want to create your custom vocabulary filter by including all desired terms, as comma-separated values, within your request.'''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "words"))

    @words.setter
    def words(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__4c5fccbb27376565b530d579ac68343c535ef849918794d84bfb1b41241d5003)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "words", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_transcribe.CfnVocabularyFilterProps",
    jsii_struct_bases=[],
    name_mapping={
        "language_code": "languageCode",
        "vocabulary_filter_name": "vocabularyFilterName",
        "data_access_role_arn": "dataAccessRoleArn",
        "tags": "tags",
        "vocabulary_filter_file_uri": "vocabularyFilterFileUri",
        "words": "words",
    },
)
class CfnVocabularyFilterProps:
    def __init__(
        self,
        *,
        language_code: builtins.str,
        vocabulary_filter_name: builtins.str,
        data_access_role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
        vocabulary_filter_file_uri: typing.Optional[builtins.str] = None,
        words: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnVocabularyFilter``.

        :param language_code: The language code that represents the language of the entries in your vocabulary filter.
        :param vocabulary_filter_name: A unique name, chosen by you, for your custom vocabulary filter.
        :param data_access_role_arn: The Amazon Resource Name (ARN) of an IAM role that has permissions to access the Amazon S3 bucket that contains your input files.
        :param tags: Tags associated with the vocabulary filter.
        :param vocabulary_filter_file_uri: The Amazon S3 location of the text file that contains your custom vocabulary filter terms.
        :param words: Use this parameter if you want to create your custom vocabulary filter by including all desired terms, as comma-separated values, within your request.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transcribe-vocabularyfilter.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_transcribe as transcribe
            
            cfn_vocabulary_filter_props = transcribe.CfnVocabularyFilterProps(
                language_code="languageCode",
                vocabulary_filter_name="vocabularyFilterName",
            
                # the properties below are optional
                data_access_role_arn="dataAccessRoleArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vocabulary_filter_file_uri="vocabularyFilterFileUri",
                words=["words"]
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__2cdb6bfa5f45a15ed27722517b6b7c36595415a65bd62ee987f46cf27184b4b2)
            check_type(argname="argument language_code", value=language_code, expected_type=type_hints["language_code"])
            check_type(argname="argument vocabulary_filter_name", value=vocabulary_filter_name, expected_type=type_hints["vocabulary_filter_name"])
            check_type(argname="argument data_access_role_arn", value=data_access_role_arn, expected_type=type_hints["data_access_role_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vocabulary_filter_file_uri", value=vocabulary_filter_file_uri, expected_type=type_hints["vocabulary_filter_file_uri"])
            check_type(argname="argument words", value=words, expected_type=type_hints["words"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "language_code": language_code,
            "vocabulary_filter_name": vocabulary_filter_name,
        }
        if data_access_role_arn is not None:
            self._values["data_access_role_arn"] = data_access_role_arn
        if tags is not None:
            self._values["tags"] = tags
        if vocabulary_filter_file_uri is not None:
            self._values["vocabulary_filter_file_uri"] = vocabulary_filter_file_uri
        if words is not None:
            self._values["words"] = words

    @builtins.property
    def language_code(self) -> builtins.str:
        '''The language code that represents the language of the entries in your vocabulary filter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transcribe-vocabularyfilter.html#cfn-transcribe-vocabularyfilter-languagecode
        '''
        result = self._values.get("language_code")
        assert result is not None, "Required property 'language_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vocabulary_filter_name(self) -> builtins.str:
        '''A unique name, chosen by you, for your custom vocabulary filter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transcribe-vocabularyfilter.html#cfn-transcribe-vocabularyfilter-vocabularyfiltername
        '''
        result = self._values.get("vocabulary_filter_name")
        assert result is not None, "Required property 'vocabulary_filter_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_access_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of an IAM role that has permissions to access the Amazon S3 bucket that contains your input files.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transcribe-vocabularyfilter.html#cfn-transcribe-vocabularyfilter-dataaccessrolearn
        '''
        result = self._values.get("data_access_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''Tags associated with the vocabulary filter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transcribe-vocabularyfilter.html#cfn-transcribe-vocabularyfilter-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    @builtins.property
    def vocabulary_filter_file_uri(self) -> typing.Optional[builtins.str]:
        '''The Amazon S3 location of the text file that contains your custom vocabulary filter terms.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transcribe-vocabularyfilter.html#cfn-transcribe-vocabularyfilter-vocabularyfilterfileuri
        '''
        result = self._values.get("vocabulary_filter_file_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def words(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Use this parameter if you want to create your custom vocabulary filter by including all desired terms, as comma-separated values, within your request.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transcribe-vocabularyfilter.html#cfn-transcribe-vocabularyfilter-words
        '''
        result = self._values.get("words")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVocabularyFilterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnVocabularyFilter",
    "CfnVocabularyFilterProps",
]

publication.publish()

def _typecheckingstub__4f379d43d1fb010196b1b7a0b7e190146a43a7817c4380b2a03c12a999b04403(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    language_code: builtins.str,
    vocabulary_filter_name: builtins.str,
    data_access_role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vocabulary_filter_file_uri: typing.Optional[builtins.str] = None,
    words: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d0d5fdd990c1e6f1f1578a57f2b1e07615e187c424de0cdb38c99ece36033ef(
    resource: _aws_transcribe_5ed72ef1.IVocabularyFilterRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0842abbe55306ec5ea964df044d6068a3c93f961b8887d1ef9ab244365b53f9(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e830e28f80376a22cc4875f2b2300dbc631c5e21a8ae0f3c1bd24ae3571e971(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5fffa3ebb60cbba9b4e3ded20ec86764ef3468786e2e8168b68abbe2f0d217a(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02de5607a020110473f71afee0afc19fa4d720c960821f6356e48a84d39652d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4fd94c77da23e798b90215596efbf7d11955e5a50f658c75bdbda30e6f96924(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23780790450e1c427f7c6e5f873fd7e2b15f7d8b507361ef12a5cc0d96a0d21a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__070bdd4161a53bdf7e27d3f41aa541151e5854ddbe9052abd9361fb6a8d67cb7(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc1f52ba1318d8b74f111bca20754506fbde302f7929088130e8e1bc376e0c99(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c5fccbb27376565b530d579ac68343c535ef849918794d84bfb1b41241d5003(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cdb6bfa5f45a15ed27722517b6b7c36595415a65bd62ee987f46cf27184b4b2(
    *,
    language_code: builtins.str,
    vocabulary_filter_name: builtins.str,
    data_access_role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vocabulary_filter_file_uri: typing.Optional[builtins.str] = None,
    words: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
