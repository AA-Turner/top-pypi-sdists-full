r'''
# AWS::Translate Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_translate as translate
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for Translate construct libraries](https://constructs.dev/search?q=translate)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::Translate resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Translate.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Translate](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Translate.html).

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
    import aws_cdk.interfaces.aws_translate as _aws_translate_87e061c6
    import constructs as _constructs_77d1e7e8
else:

    _aws_cdk_0cae9daa = _LazyImport("aws_cdk")
    _aws_translate_87e061c6 = _LazyImport("aws_cdk.interfaces.aws_translate")
    _constructs_77d1e7e8 = _LazyImport("constructs")


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_translate_87e061c6.IParallelDataRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnParallelData(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_translate.CfnParallelData",
):
    '''A parallel data resource in Amazon Translate used to customize machine translation output.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-translate-paralleldata.html
    :cloudformationResource: AWS::Translate::ParallelData
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_translate as translate
        
        cfn_parallel_data = translate.CfnParallelData(self, "MyCfnParallelData",
            name="name",
            parallel_data_config=translate.CfnParallelData.ParallelDataConfigProperty(
                format="format",
                s3_uri="s3Uri"
            ),
        
            # the properties below are optional
            description="description",
            encryption_key=translate.CfnParallelData.EncryptionKeyProperty(
                id="id",
                type="type"
            ),
            tags=[translate.CfnParallelData.TagsItemsProperty(
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
        name: builtins.str,
        parallel_data_config: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnParallelData.ParallelDataConfigProperty", typing.Dict[builtins.str, typing.Any]]],
        description: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnParallelData.EncryptionKeyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnParallelData.TagsItemsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Translate::ParallelData``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param name: A custom name for the parallel data resource. Must be unique in the account and region.
        :param parallel_data_config: Specifies the format and S3 location of the parallel data input file.
        :param description: A custom description for the parallel data resource.
        :param encryption_key: The encryption key used to encrypt this object.
        :param tags: Tags associated with the parallel data resource.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c8d8767a857c9919236ecf283c61654b275b703188c449130dff6302fb94abed)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnParallelDataProps(
            name=name,
            parallel_data_config=parallel_data_config,
            description=description,
            encryption_key=encryption_key,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForParallelData")
    @builtins.classmethod
    def arn_for_parallel_data(
        cls,
        resource: "_aws_translate_87e061c6.IParallelDataRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__56fafa8c8147c926b325dbf2ca6a825cda0d1c93eff567a47053b917bd135cb4)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForParallelData", [resource]))

    @jsii.member(jsii_name="isCfnParallelData")
    @builtins.classmethod
    def is_cfn_parallel_data(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnParallelData.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__4d5c1d9c94df775a40fe7d6ec87ea53cd440367233c4e37bc38d245ae32890bb)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnParallelData", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__65fa00f57273fee9f33068ef848a4264837d69866b01c3559083da7fe95344a7)
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
            type_hints = cached_type_hints(_typecheckingstub__62c6d79d24195287d3045b7ad2898d8307f8de5cb999c3f9391e31cc6b0a1334)
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
        '''The Amazon Resource Name (ARN) of the parallel data resource.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''The time at which the parallel data resource was created.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrFailedRecordCount")
    def attr_failed_record_count(self) -> jsii.Number:
        '''The number of records unsuccessfully imported.

        :cloudformationAttribute: FailedRecordCount
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrFailedRecordCount"))

    @builtins.property
    @jsii.member(jsii_name="attrImportedDataSize")
    def attr_imported_data_size(self) -> jsii.Number:
        '''The number of UTF-8 characters imported from the parallel data input file.

        :cloudformationAttribute: ImportedDataSize
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrImportedDataSize"))

    @builtins.property
    @jsii.member(jsii_name="attrImportedRecordCount")
    def attr_imported_record_count(self) -> jsii.Number:
        '''The number of records successfully imported.

        :cloudformationAttribute: ImportedRecordCount
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrImportedRecordCount"))

    @builtins.property
    @jsii.member(jsii_name="attrLastUpdatedAt")
    def attr_last_updated_at(self) -> builtins.str:
        '''The time at which the parallel data resource was last updated.

        :cloudformationAttribute: LastUpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrSkippedRecordCount")
    def attr_skipped_record_count(self) -> jsii.Number:
        '''The number of items skipped during import.

        :cloudformationAttribute: SkippedRecordCount
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrSkippedRecordCount"))

    @builtins.property
    @jsii.member(jsii_name="attrSourceLanguageCode")
    def attr_source_language_code(self) -> builtins.str:
        '''The source language of the translations in the parallel data file.

        :cloudformationAttribute: SourceLanguageCode
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSourceLanguageCode"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The status of the parallel data resource.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrTargetLanguageCodes")
    def attr_target_language_codes(self) -> typing.List[builtins.str]:
        '''The language codes for the target languages available in the parallel data file.

        :cloudformationAttribute: TargetLanguageCodes
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "attrTargetLanguageCodes"))

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
    @jsii.member(jsii_name="parallelDataRef")
    def parallel_data_ref(self) -> "_aws_translate_87e061c6.ParallelDataReference":
        '''A reference to a ParallelData resource.'''
        return typing.cast("_aws_translate_87e061c6.ParallelDataReference", jsii.get(self, "parallelDataRef"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''A custom name for the parallel data resource.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__97f718facff8f4b58a92a6fa10539fef44a949898d2a287f05ba41a545eebfd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parallelDataConfig")
    def parallel_data_config(
        self,
    ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnParallelData.ParallelDataConfigProperty"]:
        '''Specifies the format and S3 location of the parallel data input file.'''
        return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnParallelData.ParallelDataConfigProperty"], jsii.get(self, "parallelDataConfig"))

    @parallel_data_config.setter
    def parallel_data_config(
        self,
        value: typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnParallelData.ParallelDataConfigProperty"],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__2a5935aca36b0f03f4344a91d663167c7a1686c6ac3a440367f180ebf7f6c482)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parallelDataConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A custom description for the parallel data resource.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__7699a9dfa806d9960c658ac0594b99faaa6b5213a1db21a0eb6b838f64601ae2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnParallelData.EncryptionKeyProperty"]]:
        '''The encryption key used to encrypt this object.'''
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnParallelData.EncryptionKeyProperty"]], jsii.get(self, "encryptionKey"))

    @encryption_key.setter
    def encryption_key(
        self,
        value: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnParallelData.EncryptionKeyProperty"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__cbc625fe497dae754fd3717d67d19eaef35120ce0352138699c71843de004e92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["CfnParallelData.TagsItemsProperty"]]:
        '''Tags associated with the parallel data resource.'''
        return typing.cast(typing.Optional[typing.List["CfnParallelData.TagsItemsProperty"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["CfnParallelData.TagsItemsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__871ad6be66bec9d0b23c1ba4e4dbf39ad4cb2e41b05685bb5efd13ca852691e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_translate.CfnParallelData.EncryptionKeyProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id", "type": "type"},
    )
    class EncryptionKeyProperty:
        def __init__(self, *, id: builtins.str, type: builtins.str) -> None:
            '''The encryption key used to encrypt this object.

            :param id: The Amazon Resource Name (ARN) of the encryption key.
            :param type: The type of encryption key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-translate-paralleldata-encryptionkey.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_translate as translate
                
                encryption_key_property = translate.CfnParallelData.EncryptionKeyProperty(
                    id="id",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__0467ff2b2b67e5e28d7c3d6c6abdeccc4639f156c214643a255899d03ae919bc)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "id": id,
                "type": type,
            }

        @builtins.property
        def id(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the encryption key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-translate-paralleldata-encryptionkey.html#cfn-translate-paralleldata-encryptionkey-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def type(self) -> builtins.str:
            '''The type of encryption key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-translate-paralleldata-encryptionkey.html#cfn-translate-paralleldata-encryptionkey-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionKeyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_translate.CfnParallelData.ParallelDataConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"format": "format", "s3_uri": "s3Uri"},
    )
    class ParallelDataConfigProperty:
        def __init__(self, *, format: builtins.str, s3_uri: builtins.str) -> None:
            '''Specifies the format and S3 location of the parallel data input file.

            :param format: The format of the parallel data input file.
            :param s3_uri: The URI of the Amazon S3 folder that contains the parallel data input file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-translate-paralleldata-paralleldataconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_translate as translate
                
                parallel_data_config_property = translate.CfnParallelData.ParallelDataConfigProperty(
                    format="format",
                    s3_uri="s3Uri"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__c707d8dd30a3c001c141858f90b9e140355ac8446a0edb5bab17eede3888b026)
                check_type(argname="argument format", value=format, expected_type=type_hints["format"])
                check_type(argname="argument s3_uri", value=s3_uri, expected_type=type_hints["s3_uri"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "format": format,
                "s3_uri": s3_uri,
            }

        @builtins.property
        def format(self) -> builtins.str:
            '''The format of the parallel data input file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-translate-paralleldata-paralleldataconfig.html#cfn-translate-paralleldata-paralleldataconfig-format
            '''
            result = self._values.get("format")
            assert result is not None, "Required property 'format' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def s3_uri(self) -> builtins.str:
            '''The URI of the Amazon S3 folder that contains the parallel data input file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-translate-paralleldata-paralleldataconfig.html#cfn-translate-paralleldata-paralleldataconfig-s3uri
            '''
            result = self._values.get("s3_uri")
            assert result is not None, "Required property 's3_uri' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParallelDataConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_translate.CfnParallelData.TagsItemsProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagsItemsProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            '''
            :param key: 
            :param value: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-translate-paralleldata-tagsitems.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_translate as translate
                
                tags_items_property = translate.CfnParallelData.TagsItemsProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__aca58f6864e3ff057a23855d4ac1f1acedc644e85f74ce17f16a76b9861dd012)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-translate-paralleldata-tagsitems.html#cfn-translate-paralleldata-tagsitems-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-translate-paralleldata-tagsitems.html#cfn-translate-paralleldata-tagsitems-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagsItemsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_translate.CfnParallelDataProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "parallel_data_config": "parallelDataConfig",
        "description": "description",
        "encryption_key": "encryptionKey",
        "tags": "tags",
    },
)
class CfnParallelDataProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        parallel_data_config: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnParallelData.ParallelDataConfigProperty", typing.Dict[builtins.str, typing.Any]]],
        description: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnParallelData.EncryptionKeyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnParallelData.TagsItemsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnParallelData``.

        :param name: A custom name for the parallel data resource. Must be unique in the account and region.
        :param parallel_data_config: Specifies the format and S3 location of the parallel data input file.
        :param description: A custom description for the parallel data resource.
        :param encryption_key: The encryption key used to encrypt this object.
        :param tags: Tags associated with the parallel data resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-translate-paralleldata.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_translate as translate
            
            cfn_parallel_data_props = translate.CfnParallelDataProps(
                name="name",
                parallel_data_config=translate.CfnParallelData.ParallelDataConfigProperty(
                    format="format",
                    s3_uri="s3Uri"
                ),
            
                # the properties below are optional
                description="description",
                encryption_key=translate.CfnParallelData.EncryptionKeyProperty(
                    id="id",
                    type="type"
                ),
                tags=[translate.CfnParallelData.TagsItemsProperty(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ebd5be680e7116ce32cc9f4153b2191f99a52aad688c8d4792a875e86a1d6199)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parallel_data_config", value=parallel_data_config, expected_type=type_hints["parallel_data_config"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "parallel_data_config": parallel_data_config,
        }
        if description is not None:
            self._values["description"] = description
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''A custom name for the parallel data resource.

        Must be unique in the account and region.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-translate-paralleldata.html#cfn-translate-paralleldata-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parallel_data_config(
        self,
    ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnParallelData.ParallelDataConfigProperty"]:
        '''Specifies the format and S3 location of the parallel data input file.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-translate-paralleldata.html#cfn-translate-paralleldata-paralleldataconfig
        '''
        result = self._values.get("parallel_data_config")
        assert result is not None, "Required property 'parallel_data_config' is missing"
        return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnParallelData.ParallelDataConfigProperty"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A custom description for the parallel data resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-translate-paralleldata.html#cfn-translate-paralleldata-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_key(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnParallelData.EncryptionKeyProperty"]]:
        '''The encryption key used to encrypt this object.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-translate-paralleldata.html#cfn-translate-paralleldata-encryptionkey
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnParallelData.EncryptionKeyProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["CfnParallelData.TagsItemsProperty"]]:
        '''Tags associated with the parallel data resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-translate-paralleldata.html#cfn-translate-paralleldata-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["CfnParallelData.TagsItemsProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnParallelDataProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_translate_87e061c6.ITerminologyRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnTerminology(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_translate.CfnTerminology",
):
    '''A custom terminology resource for Amazon Translate that enables customized translations.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-translate-terminology.html
    :cloudformationResource: AWS::Translate::Terminology
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_translate as translate
        
        cfn_terminology = translate.CfnTerminology(self, "MyCfnTerminology",
            name="name",
        
            # the properties below are optional
            description="description",
            encryption_key=translate.CfnTerminology.EncryptionKeyProperty(
                id="id",
                type="type"
            ),
            merge_strategy="mergeStrategy",
            tags=[translate.CfnTerminology.TagsItemsProperty(
                key="key",
                value="value"
            )],
            terminology_data=translate.CfnTerminology.TerminologyDataProperty(
                file="file",
                format="format",
        
                # the properties below are optional
                directionality="directionality"
            )
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnTerminology.EncryptionKeyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        merge_strategy: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnTerminology.TagsItemsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        terminology_data: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnTerminology.TerminologyDataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Translate::Terminology``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param name: The name of the custom terminology.
        :param description: The description of the custom terminology.
        :param encryption_key: The encryption key for the custom terminology.
        :param merge_strategy: The merge strategy for the custom terminology. Currently only OVERWRITE is supported.
        :param tags: Tags associated with the terminology.
        :param terminology_data: The terminology data for the custom terminology being imported.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__9952d47aeea4c109259ee598077fb3ac75a138f17dd7ecf59c9c7109620d8d03)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnTerminologyProps(
            name=name,
            description=description,
            encryption_key=encryption_key,
            merge_strategy=merge_strategy,
            tags=tags,
            terminology_data=terminology_data,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForTerminology")
    @builtins.classmethod
    def arn_for_terminology(
        cls,
        resource: "_aws_translate_87e061c6.ITerminologyRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__574c2361a588095b546b759356a6be75061aa5cf45aa5ff681b7a0b963ecea9d)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForTerminology", [resource]))

    @jsii.member(jsii_name="isCfnTerminology")
    @builtins.classmethod
    def is_cfn_terminology(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnTerminology.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__90c1ef98938676e94bdc48b88cd3fba325a52cf79d41e3cda63e7eaaa7f37e9c)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnTerminology", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__2bfdafdcf74be4a071cb8bade6a3b55e9e4ca25f724b2ce71b0d8926f46538a3)
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
            type_hints = cached_type_hints(_typecheckingstub__3c39a591d0e801edf260110eef07883e762ff4cbceb68c637df96482f56ab192)
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
        '''The Amazon Resource Name (ARN) of the custom terminology.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''The time the terminology was created.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrDirectionality")
    def attr_directionality(self) -> builtins.str:
        '''The directionality of the terminology.

        :cloudformationAttribute: Directionality
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDirectionality"))

    @builtins.property
    @jsii.member(jsii_name="attrFormat")
    def attr_format(self) -> builtins.str:
        '''The format of the terminology data.

        :cloudformationAttribute: Format
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrFormat"))

    @builtins.property
    @jsii.member(jsii_name="attrLastUpdatedAt")
    def attr_last_updated_at(self) -> builtins.str:
        '''The time the terminology was last updated.

        :cloudformationAttribute: LastUpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrSizeBytes")
    def attr_size_bytes(self) -> jsii.Number:
        '''The size of the terminology file in bytes.

        :cloudformationAttribute: SizeBytes
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrSizeBytes"))

    @builtins.property
    @jsii.member(jsii_name="attrSourceLanguageCode")
    def attr_source_language_code(self) -> builtins.str:
        '''The source language code for the custom terminology.

        :cloudformationAttribute: SourceLanguageCode
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSourceLanguageCode"))

    @builtins.property
    @jsii.member(jsii_name="attrTargetLanguageCodes")
    def attr_target_language_codes(self) -> typing.List[builtins.str]:
        '''The target language codes for the custom terminology.

        :cloudformationAttribute: TargetLanguageCodes
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "attrTargetLanguageCodes"))

    @builtins.property
    @jsii.member(jsii_name="attrTermCount")
    def attr_term_count(self) -> jsii.Number:
        '''The number of terms in the custom terminology.

        :cloudformationAttribute: TermCount
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrTermCount"))

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
    @jsii.member(jsii_name="terminologyRef")
    def terminology_ref(self) -> "_aws_translate_87e061c6.TerminologyReference":
        '''A reference to a Terminology resource.'''
        return typing.cast("_aws_translate_87e061c6.TerminologyReference", jsii.get(self, "terminologyRef"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the custom terminology.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3cd928adc66a375994b438d17bca789f259f95225818cd01cfba93d39a454f08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the custom terminology.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__275c757c82dcbf0a9d75d3812d8eb182dba0c4951e6fd43031e2389bc4e14910)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnTerminology.EncryptionKeyProperty"]]:
        '''The encryption key for the custom terminology.'''
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnTerminology.EncryptionKeyProperty"]], jsii.get(self, "encryptionKey"))

    @encryption_key.setter
    def encryption_key(
        self,
        value: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnTerminology.EncryptionKeyProperty"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__7c3c95bb62cc8da45f796394c88dc84a0134435345034e198a819852994160fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mergeStrategy")
    def merge_strategy(self) -> typing.Optional[builtins.str]:
        '''The merge strategy for the custom terminology.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mergeStrategy"))

    @merge_strategy.setter
    def merge_strategy(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ab4d0d921aa8246154618894a5fe889463302f7ecdd55b273306740d506f10dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mergeStrategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["CfnTerminology.TagsItemsProperty"]]:
        '''Tags associated with the terminology.'''
        return typing.cast(typing.Optional[typing.List["CfnTerminology.TagsItemsProperty"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["CfnTerminology.TagsItemsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__94c2068e0799445fe6129f4d598810200f3e4da70669569961b5e1ac6c9e1427)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terminologyData")
    def terminology_data(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnTerminology.TerminologyDataProperty"]]:
        '''The terminology data for the custom terminology being imported.'''
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnTerminology.TerminologyDataProperty"]], jsii.get(self, "terminologyData"))

    @terminology_data.setter
    def terminology_data(
        self,
        value: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnTerminology.TerminologyDataProperty"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e1c366793c1312875aba463288787fee0253f436325073e7462e9c2310ba21e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terminologyData", value) # pyright: ignore[reportArgumentType]

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_translate.CfnTerminology.EncryptionKeyProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id", "type": "type"},
    )
    class EncryptionKeyProperty:
        def __init__(self, *, id: builtins.str, type: builtins.str) -> None:
            '''The encryption key for the custom terminology.

            :param id: The Amazon Resource Name (ARN) of the encryption key.
            :param type: The type of encryption key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-translate-terminology-encryptionkey.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_translate as translate
                
                encryption_key_property = translate.CfnTerminology.EncryptionKeyProperty(
                    id="id",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__55bb4fbb715dfe50fb9c5bf01af304843770a836a90d6db742ef4d7929896e36)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "id": id,
                "type": type,
            }

        @builtins.property
        def id(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the encryption key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-translate-terminology-encryptionkey.html#cfn-translate-terminology-encryptionkey-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def type(self) -> builtins.str:
            '''The type of encryption key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-translate-terminology-encryptionkey.html#cfn-translate-terminology-encryptionkey-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionKeyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_translate.CfnTerminology.TagsItemsProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagsItemsProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            '''
            :param key: The key of the tag.
            :param value: The value of the tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-translate-terminology-tagsitems.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_translate as translate
                
                tags_items_property = translate.CfnTerminology.TagsItemsProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__1598f34e2f25f9f040ec8d1958a8eef00e27009bfe2c26029a4d5c61c76ec849)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''The key of the tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-translate-terminology-tagsitems.html#cfn-translate-terminology-tagsitems-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''The value of the tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-translate-terminology-tagsitems.html#cfn-translate-terminology-tagsitems-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagsItemsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_translate.CfnTerminology.TerminologyDataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "file": "file",
            "format": "format",
            "directionality": "directionality",
        },
    )
    class TerminologyDataProperty:
        def __init__(
            self,
            *,
            file: builtins.str,
            format: builtins.str,
            directionality: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The terminology data for the custom terminology being imported.

            :param file: The file containing the custom terminology data, base64-encoded.
            :param format: The data format of the custom terminology.
            :param directionality: The directionality of the terminology resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-translate-terminology-terminologydata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_translate as translate
                
                terminology_data_property = translate.CfnTerminology.TerminologyDataProperty(
                    file="file",
                    format="format",
                
                    # the properties below are optional
                    directionality="directionality"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__80dc6bc4be6a1d3b5feec48e201b361ee5da1b0a6207f58a884a0c959edf7a23)
                check_type(argname="argument file", value=file, expected_type=type_hints["file"])
                check_type(argname="argument format", value=format, expected_type=type_hints["format"])
                check_type(argname="argument directionality", value=directionality, expected_type=type_hints["directionality"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "file": file,
                "format": format,
            }
            if directionality is not None:
                self._values["directionality"] = directionality

        @builtins.property
        def file(self) -> builtins.str:
            '''The file containing the custom terminology data, base64-encoded.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-translate-terminology-terminologydata.html#cfn-translate-terminology-terminologydata-file
            '''
            result = self._values.get("file")
            assert result is not None, "Required property 'file' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def format(self) -> builtins.str:
            '''The data format of the custom terminology.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-translate-terminology-terminologydata.html#cfn-translate-terminology-terminologydata-format
            '''
            result = self._values.get("format")
            assert result is not None, "Required property 'format' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def directionality(self) -> typing.Optional[builtins.str]:
            '''The directionality of the terminology resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-translate-terminology-terminologydata.html#cfn-translate-terminology-terminologydata-directionality
            '''
            result = self._values.get("directionality")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TerminologyDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_translate.CfnTerminologyProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "description": "description",
        "encryption_key": "encryptionKey",
        "merge_strategy": "mergeStrategy",
        "tags": "tags",
        "terminology_data": "terminologyData",
    },
)
class CfnTerminologyProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnTerminology.EncryptionKeyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        merge_strategy: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnTerminology.TagsItemsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        terminology_data: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnTerminology.TerminologyDataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnTerminology``.

        :param name: The name of the custom terminology.
        :param description: The description of the custom terminology.
        :param encryption_key: The encryption key for the custom terminology.
        :param merge_strategy: The merge strategy for the custom terminology. Currently only OVERWRITE is supported.
        :param tags: Tags associated with the terminology.
        :param terminology_data: The terminology data for the custom terminology being imported.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-translate-terminology.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_translate as translate
            
            cfn_terminology_props = translate.CfnTerminologyProps(
                name="name",
            
                # the properties below are optional
                description="description",
                encryption_key=translate.CfnTerminology.EncryptionKeyProperty(
                    id="id",
                    type="type"
                ),
                merge_strategy="mergeStrategy",
                tags=[translate.CfnTerminology.TagsItemsProperty(
                    key="key",
                    value="value"
                )],
                terminology_data=translate.CfnTerminology.TerminologyDataProperty(
                    file="file",
                    format="format",
            
                    # the properties below are optional
                    directionality="directionality"
                )
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__eb610a00c9e0e22c8a308adbe36c201dd086267d28fa8bab3bb9dc06def4e591)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument merge_strategy", value=merge_strategy, expected_type=type_hints["merge_strategy"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument terminology_data", value=terminology_data, expected_type=type_hints["terminology_data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if merge_strategy is not None:
            self._values["merge_strategy"] = merge_strategy
        if tags is not None:
            self._values["tags"] = tags
        if terminology_data is not None:
            self._values["terminology_data"] = terminology_data

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the custom terminology.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-translate-terminology.html#cfn-translate-terminology-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the custom terminology.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-translate-terminology.html#cfn-translate-terminology-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_key(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnTerminology.EncryptionKeyProperty"]]:
        '''The encryption key for the custom terminology.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-translate-terminology.html#cfn-translate-terminology-encryptionkey
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnTerminology.EncryptionKeyProperty"]], result)

    @builtins.property
    def merge_strategy(self) -> typing.Optional[builtins.str]:
        '''The merge strategy for the custom terminology.

        Currently only OVERWRITE is supported.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-translate-terminology.html#cfn-translate-terminology-mergestrategy
        '''
        result = self._values.get("merge_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["CfnTerminology.TagsItemsProperty"]]:
        '''Tags associated with the terminology.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-translate-terminology.html#cfn-translate-terminology-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["CfnTerminology.TagsItemsProperty"]], result)

    @builtins.property
    def terminology_data(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnTerminology.TerminologyDataProperty"]]:
        '''The terminology data for the custom terminology being imported.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-translate-terminology.html#cfn-translate-terminology-terminologydata
        '''
        result = self._values.get("terminology_data")
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnTerminology.TerminologyDataProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTerminologyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnParallelData",
    "CfnParallelDataProps",
    "CfnTerminology",
    "CfnTerminologyProps",
]

publication.publish()

def _typecheckingstub__c8d8767a857c9919236ecf283c61654b275b703188c449130dff6302fb94abed(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    parallel_data_config: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnParallelData.ParallelDataConfigProperty, typing.Dict[builtins.str, typing.Any]]],
    description: typing.Optional[builtins.str] = None,
    encryption_key: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnParallelData.EncryptionKeyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnParallelData.TagsItemsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56fafa8c8147c926b325dbf2ca6a825cda0d1c93eff567a47053b917bd135cb4(
    resource: _aws_translate_87e061c6.IParallelDataRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d5c1d9c94df775a40fe7d6ec87ea53cd440367233c4e37bc38d245ae32890bb(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65fa00f57273fee9f33068ef848a4264837d69866b01c3559083da7fe95344a7(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62c6d79d24195287d3045b7ad2898d8307f8de5cb999c3f9391e31cc6b0a1334(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97f718facff8f4b58a92a6fa10539fef44a949898d2a287f05ba41a545eebfd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a5935aca36b0f03f4344a91d663167c7a1686c6ac3a440367f180ebf7f6c482(
    value: typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnParallelData.ParallelDataConfigProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7699a9dfa806d9960c658ac0594b99faaa6b5213a1db21a0eb6b838f64601ae2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbc625fe497dae754fd3717d67d19eaef35120ce0352138699c71843de004e92(
    value: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnParallelData.EncryptionKeyProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__871ad6be66bec9d0b23c1ba4e4dbf39ad4cb2e41b05685bb5efd13ca852691e1(
    value: typing.Optional[typing.List[CfnParallelData.TagsItemsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0467ff2b2b67e5e28d7c3d6c6abdeccc4639f156c214643a255899d03ae919bc(
    *,
    id: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c707d8dd30a3c001c141858f90b9e140355ac8446a0edb5bab17eede3888b026(
    *,
    format: builtins.str,
    s3_uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aca58f6864e3ff057a23855d4ac1f1acedc644e85f74ce17f16a76b9861dd012(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebd5be680e7116ce32cc9f4153b2191f99a52aad688c8d4792a875e86a1d6199(
    *,
    name: builtins.str,
    parallel_data_config: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnParallelData.ParallelDataConfigProperty, typing.Dict[builtins.str, typing.Any]]],
    description: typing.Optional[builtins.str] = None,
    encryption_key: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnParallelData.EncryptionKeyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnParallelData.TagsItemsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9952d47aeea4c109259ee598077fb3ac75a138f17dd7ecf59c9c7109620d8d03(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    encryption_key: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnTerminology.EncryptionKeyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    merge_strategy: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnTerminology.TagsItemsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    terminology_data: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnTerminology.TerminologyDataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__574c2361a588095b546b759356a6be75061aa5cf45aa5ff681b7a0b963ecea9d(
    resource: _aws_translate_87e061c6.ITerminologyRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90c1ef98938676e94bdc48b88cd3fba325a52cf79d41e3cda63e7eaaa7f37e9c(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bfdafdcf74be4a071cb8bade6a3b55e9e4ca25f724b2ce71b0d8926f46538a3(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c39a591d0e801edf260110eef07883e762ff4cbceb68c637df96482f56ab192(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cd928adc66a375994b438d17bca789f259f95225818cd01cfba93d39a454f08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__275c757c82dcbf0a9d75d3812d8eb182dba0c4951e6fd43031e2389bc4e14910(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c3c95bb62cc8da45f796394c88dc84a0134435345034e198a819852994160fa(
    value: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnTerminology.EncryptionKeyProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab4d0d921aa8246154618894a5fe889463302f7ecdd55b273306740d506f10dc(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94c2068e0799445fe6129f4d598810200f3e4da70669569961b5e1ac6c9e1427(
    value: typing.Optional[typing.List[CfnTerminology.TagsItemsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1c366793c1312875aba463288787fee0253f436325073e7462e9c2310ba21e5(
    value: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnTerminology.TerminologyDataProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55bb4fbb715dfe50fb9c5bf01af304843770a836a90d6db742ef4d7929896e36(
    *,
    id: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1598f34e2f25f9f040ec8d1958a8eef00e27009bfe2c26029a4d5c61c76ec849(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80dc6bc4be6a1d3b5feec48e201b361ee5da1b0a6207f58a884a0c959edf7a23(
    *,
    file: builtins.str,
    format: builtins.str,
    directionality: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb610a00c9e0e22c8a308adbe36c201dd086267d28fa8bab3bb9dc06def4e591(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    encryption_key: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnTerminology.EncryptionKeyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    merge_strategy: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnTerminology.TagsItemsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    terminology_data: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnTerminology.TerminologyDataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
