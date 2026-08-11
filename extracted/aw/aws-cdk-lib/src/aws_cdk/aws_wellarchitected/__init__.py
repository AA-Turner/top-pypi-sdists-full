r'''
# AWS::WellArchitected Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_wellarchitected as wellarchitected
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for WellArchitected construct libraries](https://constructs.dev/search?q=wellarchitected)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::WellArchitected resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_WellArchitected.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::WellArchitected](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_WellArchitected.html).

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
    import aws_cdk.interfaces.aws_wellarchitected as _aws_wellarchitected_baeb38e4
    import constructs as _constructs_77d1e7e8
else:

    _aws_cdk_0cae9daa = _LazyImport("aws_cdk")
    _aws_wellarchitected_baeb38e4 = _LazyImport("aws_cdk.interfaces.aws_wellarchitected")
    _constructs_77d1e7e8 = _LazyImport("constructs")


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_wellarchitected_baeb38e4.ILensRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnLens(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_wellarchitected.CfnLens",
):
    '''Definition of AWS::WellArchitected::Lens Resource Type.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wellarchitected-lens.html
    :cloudformationResource: AWS::WellArchitected::Lens
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_wellarchitected as wellarchitected
        
        cfn_lens = wellarchitected.CfnLens(self, "MyCfnLens",
            json_string="jsonString",
            lens_version="lensVersion",
            tags=[wellarchitected.CfnLens.TagsItemsProperty(
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
        json_string: typing.Optional[builtins.str] = None,
        lens_version: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnLens.TagsItemsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::WellArchitected::Lens``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param json_string: The JSON representation of a lens.
        :param lens_version: The version of the lens.
        :param tags: The tags assigned to the lens.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3d5f05029933d22227863cbb8f7c95ab990d5661e937e3dc1e679d930c79e4e3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLensProps(
            json_string=json_string, lens_version=lens_version, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForLens")
    @builtins.classmethod
    def arn_for_lens(
        cls,
        resource: "_aws_wellarchitected_baeb38e4.ILensRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__7dcbe972bc79cf031bc9e2f981f162af789923bde849412c07ed13d29b21581d)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForLens", [resource]))

    @jsii.member(jsii_name="isCfnLens")
    @builtins.classmethod
    def is_cfn_lens(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnLens.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b0c23b12878c01c56c9ea585f96b674055360c9c1f2ca8ba550ac2faa86f50f6)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnLens", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__bfc2edea20e8b925ddf0c8bd553443d8dc573ab9b4bcfd5929935cbdcc8b7064)
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
            type_hints = cached_type_hints(_typecheckingstub__d198c93003702d18b92918407f3947a26254e0b921662b747fbf2e5943ddd196)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrDescription")
    def attr_description(self) -> builtins.str:
        '''The description of the lens.

        :cloudformationAttribute: Description
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDescription"))

    @builtins.property
    @jsii.member(jsii_name="attrLensArn")
    def attr_lens_arn(self) -> builtins.str:
        '''The ARN of the lens.

        :cloudformationAttribute: LensArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLensArn"))

    @builtins.property
    @jsii.member(jsii_name="attrLensId")
    def attr_lens_id(self) -> builtins.str:
        '''The unique identifier of the lens.

        :cloudformationAttribute: LensId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLensId"))

    @builtins.property
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        '''The full name of the lens.

        :cloudformationAttribute: Name
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrName"))

    @builtins.property
    @jsii.member(jsii_name="attrOwner")
    def attr_owner(self) -> builtins.str:
        '''The Amazon Web Services account ID that owns the lens.

        :cloudformationAttribute: Owner
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrOwner"))

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
    @jsii.member(jsii_name="lensRef")
    def lens_ref(self) -> "_aws_wellarchitected_baeb38e4.LensReference":
        '''A reference to a Lens resource.'''
        return typing.cast("_aws_wellarchitected_baeb38e4.LensReference", jsii.get(self, "lensRef"))

    @builtins.property
    @jsii.member(jsii_name="jsonString")
    def json_string(self) -> typing.Optional[builtins.str]:
        '''The JSON representation of a lens.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jsonString"))

    @json_string.setter
    def json_string(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1ba58ed3750f2fbb91d5ff6fee8eccf0cccbc03bfeb023736f17ad82ff3ad4d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jsonString", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lensVersion")
    def lens_version(self) -> typing.Optional[builtins.str]:
        '''The version of the lens.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lensVersion"))

    @lens_version.setter
    def lens_version(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__49297c3d37d9f5625c16f260e65759bb690b77764d725f61883fefb77290c939)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lensVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["CfnLens.TagsItemsProperty"]]:
        '''The tags assigned to the lens.'''
        return typing.cast(typing.Optional[typing.List["CfnLens.TagsItemsProperty"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["CfnLens.TagsItemsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__327d0922cfb2eff6ff962a367be224e19364af2935056dfbd4bf587d94527e8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_wellarchitected.CfnLens.TagsItemsProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagsItemsProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            '''
            :param key: 
            :param value: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wellarchitected-lens-tagsitems.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_wellarchitected as wellarchitected
                
                tags_items_property = wellarchitected.CfnLens.TagsItemsProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__c9cea320060f46a0c70342cd9bdad5021be997791bd808986f82e44287dc11fb)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wellarchitected-lens-tagsitems.html#cfn-wellarchitected-lens-tagsitems-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wellarchitected-lens-tagsitems.html#cfn-wellarchitected-lens-tagsitems-value
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
    jsii_type="aws-cdk-lib.aws_wellarchitected.CfnLensProps",
    jsii_struct_bases=[],
    name_mapping={
        "json_string": "jsonString",
        "lens_version": "lensVersion",
        "tags": "tags",
    },
)
class CfnLensProps:
    def __init__(
        self,
        *,
        json_string: typing.Optional[builtins.str] = None,
        lens_version: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnLens.TagsItemsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnLens``.

        :param json_string: The JSON representation of a lens.
        :param lens_version: The version of the lens.
        :param tags: The tags assigned to the lens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wellarchitected-lens.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_wellarchitected as wellarchitected
            
            cfn_lens_props = wellarchitected.CfnLensProps(
                json_string="jsonString",
                lens_version="lensVersion",
                tags=[wellarchitected.CfnLens.TagsItemsProperty(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e443ed708aafd16050058a3c4b8ee8ffc074282acba6b187cdb9d19d8f6f4a49)
            check_type(argname="argument json_string", value=json_string, expected_type=type_hints["json_string"])
            check_type(argname="argument lens_version", value=lens_version, expected_type=type_hints["lens_version"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if json_string is not None:
            self._values["json_string"] = json_string
        if lens_version is not None:
            self._values["lens_version"] = lens_version
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def json_string(self) -> typing.Optional[builtins.str]:
        '''The JSON representation of a lens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wellarchitected-lens.html#cfn-wellarchitected-lens-jsonstring
        '''
        result = self._values.get("json_string")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lens_version(self) -> typing.Optional[builtins.str]:
        '''The version of the lens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wellarchitected-lens.html#cfn-wellarchitected-lens-lensversion
        '''
        result = self._values.get("lens_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["CfnLens.TagsItemsProperty"]]:
        '''The tags assigned to the lens.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wellarchitected-lens.html#cfn-wellarchitected-lens-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["CfnLens.TagsItemsProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLensProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_wellarchitected_baeb38e4.IProfileRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnProfile(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_wellarchitected.CfnProfile",
):
    '''Definition of AWS::WellArchitected::Profile Resource Type.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wellarchitected-profile.html
    :cloudformationResource: AWS::WellArchitected::Profile
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_wellarchitected as wellarchitected
        
        cfn_profile = wellarchitected.CfnProfile(self, "MyCfnProfile",
            profile_description="profileDescription",
            profile_name="profileName",
            profile_questions=[wellarchitected.CfnProfile.ProfileQuestionUpdateProperty(
                question_id="questionId",
                selected_choice_ids=["selectedChoiceIds"]
            )],
        
            # the properties below are optional
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
        profile_description: builtins.str,
        profile_name: builtins.str,
        profile_questions: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Sequence[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnProfile.ProfileQuestionUpdateProperty", typing.Dict[builtins.str, typing.Any]]]]],
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::WellArchitected::Profile``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param profile_description: The profile description.
        :param profile_name: The name of the profile.
        :param profile_questions: The profile questions.
        :param tags: The tags assigned to the profile.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__16dbf25f3b945a7f0f5acd3f145e8c6dcb9d74886ff4be7d9d47746013010dc3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnProfileProps(
            profile_description=profile_description,
            profile_name=profile_name,
            profile_questions=profile_questions,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForProfile")
    @builtins.classmethod
    def arn_for_profile(
        cls,
        resource: "_aws_wellarchitected_baeb38e4.IProfileRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a0d97a77758d15481e2147863182fc3e2ab2b84d9aadbe59ff85c229b8808866)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForProfile", [resource]))

    @jsii.member(jsii_name="isCfnProfile")
    @builtins.classmethod
    def is_cfn_profile(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnProfile.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b09e0f521b34098e7c7380eb9fe411169420bc05cfbc2ff446e7d56374b20518)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnProfile", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__7ffb7c62ff3ea85306b944288da4ededab1f195b9056faf4f12983dabc974afc)
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
            type_hints = cached_type_hints(_typecheckingstub__a581f0345b3135f03e950404b20948286d62f52515abea4aa5dfd4df433c9aa2)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''The date and time the profile was created.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrOwner")
    def attr_owner(self) -> builtins.str:
        '''The owner of the profile.

        :cloudformationAttribute: Owner
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrOwner"))

    @builtins.property
    @jsii.member(jsii_name="attrProfileArn")
    def attr_profile_arn(self) -> builtins.str:
        '''The profile ARN.

        :cloudformationAttribute: ProfileArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrProfileArn"))

    @builtins.property
    @jsii.member(jsii_name="attrProfileVersion")
    def attr_profile_version(self) -> builtins.str:
        '''The profile version.

        :cloudformationAttribute: ProfileVersion
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrProfileVersion"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdatedAt")
    def attr_updated_at(self) -> builtins.str:
        '''The date and time the profile was last updated.

        :cloudformationAttribute: UpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdatedAt"))

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
    @jsii.member(jsii_name="profileRef")
    def profile_ref(self) -> "_aws_wellarchitected_baeb38e4.ProfileReference":
        '''A reference to a Profile resource.'''
        return typing.cast("_aws_wellarchitected_baeb38e4.ProfileReference", jsii.get(self, "profileRef"))

    @builtins.property
    @jsii.member(jsii_name="profileDescription")
    def profile_description(self) -> builtins.str:
        '''The profile description.'''
        return typing.cast(builtins.str, jsii.get(self, "profileDescription"))

    @profile_description.setter
    def profile_description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__84cadf08eb456c175c5504a45b1ec1a0d3ff3307b3b1e629e187c3ff37464a55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profileDescription", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="profileName")
    def profile_name(self) -> builtins.str:
        '''The name of the profile.'''
        return typing.cast(builtins.str, jsii.get(self, "profileName"))

    @profile_name.setter
    def profile_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__5d1a6c9c7f56e7718080d0b78b451ba67cddb323290bbc264a80f7a166397fe8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profileName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="profileQuestions")
    def profile_questions(
        self,
    ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnProfile.ProfileQuestionUpdateProperty"]]]:
        '''The profile questions.'''
        return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnProfile.ProfileQuestionUpdateProperty"]]], jsii.get(self, "profileQuestions"))

    @profile_questions.setter
    def profile_questions(
        self,
        value: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnProfile.ProfileQuestionUpdateProperty"]]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c2faedcf6f083c3a17dab52bd3a34c1454e00e4ddbd30b7d2a1f53f0e989e36d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profileQuestions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''The tags assigned to the profile.'''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__da314b539b412acb741b4c11b743e6e16c3694ff86138cd77631a7e198f09a2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_wellarchitected.CfnProfile.ProfileQuestionUpdateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "question_id": "questionId",
            "selected_choice_ids": "selectedChoiceIds",
        },
    )
    class ProfileQuestionUpdateProperty:
        def __init__(
            self,
            *,
            question_id: typing.Optional[builtins.str] = None,
            selected_choice_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''An update to a profile question.

            :param question_id: The ID of the question.
            :param selected_choice_ids: The selected choices.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wellarchitected-profile-profilequestionupdate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_wellarchitected as wellarchitected
                
                profile_question_update_property = wellarchitected.CfnProfile.ProfileQuestionUpdateProperty(
                    question_id="questionId",
                    selected_choice_ids=["selectedChoiceIds"]
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__c9998f176a1ff9f66db3e66115e83e4e2685fcdfdb900b3633d7371523cb5ff3)
                check_type(argname="argument question_id", value=question_id, expected_type=type_hints["question_id"])
                check_type(argname="argument selected_choice_ids", value=selected_choice_ids, expected_type=type_hints["selected_choice_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if question_id is not None:
                self._values["question_id"] = question_id
            if selected_choice_ids is not None:
                self._values["selected_choice_ids"] = selected_choice_ids

        @builtins.property
        def question_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the question.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wellarchitected-profile-profilequestionupdate.html#cfn-wellarchitected-profile-profilequestionupdate-questionid
            '''
            result = self._values.get("question_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def selected_choice_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The selected choices.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wellarchitected-profile-profilequestionupdate.html#cfn-wellarchitected-profile-profilequestionupdate-selectedchoiceids
            '''
            result = self._values.get("selected_choice_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProfileQuestionUpdateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_wellarchitected.CfnProfileProps",
    jsii_struct_bases=[],
    name_mapping={
        "profile_description": "profileDescription",
        "profile_name": "profileName",
        "profile_questions": "profileQuestions",
        "tags": "tags",
    },
)
class CfnProfileProps:
    def __init__(
        self,
        *,
        profile_description: builtins.str,
        profile_name: builtins.str,
        profile_questions: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Sequence[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnProfile.ProfileQuestionUpdateProperty", typing.Dict[builtins.str, typing.Any]]]]],
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnProfile``.

        :param profile_description: The profile description.
        :param profile_name: The name of the profile.
        :param profile_questions: The profile questions.
        :param tags: The tags assigned to the profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wellarchitected-profile.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_wellarchitected as wellarchitected
            
            cfn_profile_props = wellarchitected.CfnProfileProps(
                profile_description="profileDescription",
                profile_name="profileName",
                profile_questions=[wellarchitected.CfnProfile.ProfileQuestionUpdateProperty(
                    question_id="questionId",
                    selected_choice_ids=["selectedChoiceIds"]
                )],
            
                # the properties below are optional
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a2c06fa25e6e5e8ce7ee3cdf293db7e7d2f30d006afa1da06f91db02cda98d56)
            check_type(argname="argument profile_description", value=profile_description, expected_type=type_hints["profile_description"])
            check_type(argname="argument profile_name", value=profile_name, expected_type=type_hints["profile_name"])
            check_type(argname="argument profile_questions", value=profile_questions, expected_type=type_hints["profile_questions"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "profile_description": profile_description,
            "profile_name": profile_name,
            "profile_questions": profile_questions,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def profile_description(self) -> builtins.str:
        '''The profile description.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wellarchitected-profile.html#cfn-wellarchitected-profile-profiledescription
        '''
        result = self._values.get("profile_description")
        assert result is not None, "Required property 'profile_description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def profile_name(self) -> builtins.str:
        '''The name of the profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wellarchitected-profile.html#cfn-wellarchitected-profile-profilename
        '''
        result = self._values.get("profile_name")
        assert result is not None, "Required property 'profile_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def profile_questions(
        self,
    ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnProfile.ProfileQuestionUpdateProperty"]]]:
        '''The profile questions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wellarchitected-profile.html#cfn-wellarchitected-profile-profilequestions
        '''
        result = self._values.get("profile_questions")
        assert result is not None, "Required property 'profile_questions' is missing"
        return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnProfile.ProfileQuestionUpdateProperty"]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''The tags assigned to the profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wellarchitected-profile.html#cfn-wellarchitected-profile-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProfileProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_wellarchitected_baeb38e4.IReviewTemplateRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnReviewTemplate(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_wellarchitected.CfnReviewTemplate",
):
    '''Creates a review template for the Well-Architected Tool.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wellarchitected-reviewtemplate.html
    :cloudformationResource: AWS::WellArchitected::ReviewTemplate
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_wellarchitected as wellarchitected
        
        cfn_review_template = wellarchitected.CfnReviewTemplate(self, "MyCfnReviewTemplate",
            description="description",
            lenses=["lenses"],
            template_name="templateName",
        
            # the properties below are optional
            notes="notes",
            tags=[wellarchitected.CfnReviewTemplate.TagsItemsProperty(
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
        description: builtins.str,
        lenses: typing.Sequence[builtins.str],
        template_name: builtins.str,
        notes: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnReviewTemplate.TagsItemsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::WellArchitected::ReviewTemplate``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param description: The review template description.
        :param lenses: The lenses applied to the review template.
        :param template_name: The name of the review template.
        :param notes: The notes associated with the review template.
        :param tags: The tags assigned to the review template.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ed9bfb05238fe20d9001d71a736fb555a27225c18694eecfeb22613d1d086ff5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnReviewTemplateProps(
            description=description,
            lenses=lenses,
            template_name=template_name,
            notes=notes,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="isCfnReviewTemplate")
    @builtins.classmethod
    def is_cfn_review_template(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnReviewTemplate.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__57c6b7bd56a22cf3fa2a4cbac52a7eeceaf81d358faf8e8ef92d4cd8d2b8ff47)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnReviewTemplate", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__93d3e6f2e769fc5735494ed2d1f2735861488a04eede9b653980d528cd88e537)
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
            type_hints = cached_type_hints(_typecheckingstub__05d601743cd8f8f972e70133769d55d367d5c94ce2c9c81ae482178682fd5fb9)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrOwner")
    def attr_owner(self) -> builtins.str:
        '''The owner of the review template.

        :cloudformationAttribute: Owner
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrOwner"))

    @builtins.property
    @jsii.member(jsii_name="attrTemplateArn")
    def attr_template_arn(self) -> builtins.str:
        '''The review template ARN.

        :cloudformationAttribute: TemplateArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrTemplateArn"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdatedAt")
    def attr_updated_at(self) -> builtins.str:
        '''The date and time the review template was last updated.

        :cloudformationAttribute: UpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdateStatus")
    def attr_update_status(self) -> builtins.str:
        '''The latest status of the review template.

        :cloudformationAttribute: UpdateStatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdateStatus"))

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
    @jsii.member(jsii_name="reviewTemplateRef")
    def review_template_ref(
        self,
    ) -> "_aws_wellarchitected_baeb38e4.ReviewTemplateReference":
        '''A reference to a ReviewTemplate resource.'''
        return typing.cast("_aws_wellarchitected_baeb38e4.ReviewTemplateReference", jsii.get(self, "reviewTemplateRef"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        '''The review template description.'''
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1403813d81c139b4a0632e973c62f08a004ede86b9deef460daee650904034f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lenses")
    def lenses(self) -> typing.List[builtins.str]:
        '''The lenses applied to the review template.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "lenses"))

    @lenses.setter
    def lenses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__5a7af0f3ef194941dc8fb90e32d4c619ca9e28e16b739db06cbfe82fb60d3022)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lenses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="templateName")
    def template_name(self) -> builtins.str:
        '''The name of the review template.'''
        return typing.cast(builtins.str, jsii.get(self, "templateName"))

    @template_name.setter
    def template_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f597ea62eb141a0e637cd48349cd9d1615f928e180522dd5aea608efcca6c21f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notes")
    def notes(self) -> typing.Optional[builtins.str]:
        '''The notes associated with the review template.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notes"))

    @notes.setter
    def notes(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ae073e52fa4b6d35952b13fd86cb2f262f3df42060ba4cb318d4299b2493c379)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(
        self,
    ) -> typing.Optional[typing.List["CfnReviewTemplate.TagsItemsProperty"]]:
        '''The tags assigned to the review template.'''
        return typing.cast(typing.Optional[typing.List["CfnReviewTemplate.TagsItemsProperty"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["CfnReviewTemplate.TagsItemsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6ff8fbd0f70bc38c89a2d11baaa844b230802c50211badc8156ae885a85b3627)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_wellarchitected.CfnReviewTemplate.TagsItemsProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagsItemsProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            '''
            :param key: 
            :param value: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wellarchitected-reviewtemplate-tagsitems.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_wellarchitected as wellarchitected
                
                tags_items_property = wellarchitected.CfnReviewTemplate.TagsItemsProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__c6b4c4c6bf31b0e2c5342222397e967c2df0b7c4a9530a93891be49fe9f1dda9)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wellarchitected-reviewtemplate-tagsitems.html#cfn-wellarchitected-reviewtemplate-tagsitems-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wellarchitected-reviewtemplate-tagsitems.html#cfn-wellarchitected-reviewtemplate-tagsitems-value
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
    jsii_type="aws-cdk-lib.aws_wellarchitected.CfnReviewTemplateProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "lenses": "lenses",
        "template_name": "templateName",
        "notes": "notes",
        "tags": "tags",
    },
)
class CfnReviewTemplateProps:
    def __init__(
        self,
        *,
        description: builtins.str,
        lenses: typing.Sequence[builtins.str],
        template_name: builtins.str,
        notes: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnReviewTemplate.TagsItemsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnReviewTemplate``.

        :param description: The review template description.
        :param lenses: The lenses applied to the review template.
        :param template_name: The name of the review template.
        :param notes: The notes associated with the review template.
        :param tags: The tags assigned to the review template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wellarchitected-reviewtemplate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_wellarchitected as wellarchitected
            
            cfn_review_template_props = wellarchitected.CfnReviewTemplateProps(
                description="description",
                lenses=["lenses"],
                template_name="templateName",
            
                # the properties below are optional
                notes="notes",
                tags=[wellarchitected.CfnReviewTemplate.TagsItemsProperty(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__8cc0ce4fd995ce88c347c3898dd891af9cda3438ebe6053b81695e1e7909c30f)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument lenses", value=lenses, expected_type=type_hints["lenses"])
            check_type(argname="argument template_name", value=template_name, expected_type=type_hints["template_name"])
            check_type(argname="argument notes", value=notes, expected_type=type_hints["notes"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "lenses": lenses,
            "template_name": template_name,
        }
        if notes is not None:
            self._values["notes"] = notes
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> builtins.str:
        '''The review template description.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wellarchitected-reviewtemplate.html#cfn-wellarchitected-reviewtemplate-description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lenses(self) -> typing.List[builtins.str]:
        '''The lenses applied to the review template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wellarchitected-reviewtemplate.html#cfn-wellarchitected-reviewtemplate-lenses
        '''
        result = self._values.get("lenses")
        assert result is not None, "Required property 'lenses' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def template_name(self) -> builtins.str:
        '''The name of the review template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wellarchitected-reviewtemplate.html#cfn-wellarchitected-reviewtemplate-templatename
        '''
        result = self._values.get("template_name")
        assert result is not None, "Required property 'template_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def notes(self) -> typing.Optional[builtins.str]:
        '''The notes associated with the review template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wellarchitected-reviewtemplate.html#cfn-wellarchitected-reviewtemplate-notes
        '''
        result = self._values.get("notes")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.List["CfnReviewTemplate.TagsItemsProperty"]]:
        '''The tags assigned to the review template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wellarchitected-reviewtemplate.html#cfn-wellarchitected-reviewtemplate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["CfnReviewTemplate.TagsItemsProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReviewTemplateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnLens",
    "CfnLensProps",
    "CfnProfile",
    "CfnProfileProps",
    "CfnReviewTemplate",
    "CfnReviewTemplateProps",
]

publication.publish()

def _typecheckingstub__3d5f05029933d22227863cbb8f7c95ab990d5661e937e3dc1e679d930c79e4e3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    json_string: typing.Optional[builtins.str] = None,
    lens_version: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnLens.TagsItemsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dcbe972bc79cf031bc9e2f981f162af789923bde849412c07ed13d29b21581d(
    resource: _aws_wellarchitected_baeb38e4.ILensRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0c23b12878c01c56c9ea585f96b674055360c9c1f2ca8ba550ac2faa86f50f6(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfc2edea20e8b925ddf0c8bd553443d8dc573ab9b4bcfd5929935cbdcc8b7064(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d198c93003702d18b92918407f3947a26254e0b921662b747fbf2e5943ddd196(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ba58ed3750f2fbb91d5ff6fee8eccf0cccbc03bfeb023736f17ad82ff3ad4d2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49297c3d37d9f5625c16f260e65759bb690b77764d725f61883fefb77290c939(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__327d0922cfb2eff6ff962a367be224e19364af2935056dfbd4bf587d94527e8f(
    value: typing.Optional[typing.List[CfnLens.TagsItemsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9cea320060f46a0c70342cd9bdad5021be997791bd808986f82e44287dc11fb(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e443ed708aafd16050058a3c4b8ee8ffc074282acba6b187cdb9d19d8f6f4a49(
    *,
    json_string: typing.Optional[builtins.str] = None,
    lens_version: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnLens.TagsItemsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16dbf25f3b945a7f0f5acd3f145e8c6dcb9d74886ff4be7d9d47746013010dc3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    profile_description: builtins.str,
    profile_name: builtins.str,
    profile_questions: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Sequence[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnProfile.ProfileQuestionUpdateProperty, typing.Dict[builtins.str, typing.Any]]]]],
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0d97a77758d15481e2147863182fc3e2ab2b84d9aadbe59ff85c229b8808866(
    resource: _aws_wellarchitected_baeb38e4.IProfileRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b09e0f521b34098e7c7380eb9fe411169420bc05cfbc2ff446e7d56374b20518(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ffb7c62ff3ea85306b944288da4ededab1f195b9056faf4f12983dabc974afc(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a581f0345b3135f03e950404b20948286d62f52515abea4aa5dfd4df433c9aa2(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84cadf08eb456c175c5504a45b1ec1a0d3ff3307b3b1e629e187c3ff37464a55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d1a6c9c7f56e7718080d0b78b451ba67cddb323290bbc264a80f7a166397fe8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2faedcf6f083c3a17dab52bd3a34c1454e00e4ddbd30b7d2a1f53f0e989e36d(
    value: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.List[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnProfile.ProfileQuestionUpdateProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da314b539b412acb741b4c11b743e6e16c3694ff86138cd77631a7e198f09a2b(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9998f176a1ff9f66db3e66115e83e4e2685fcdfdb900b3633d7371523cb5ff3(
    *,
    question_id: typing.Optional[builtins.str] = None,
    selected_choice_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2c06fa25e6e5e8ce7ee3cdf293db7e7d2f30d006afa1da06f91db02cda98d56(
    *,
    profile_description: builtins.str,
    profile_name: builtins.str,
    profile_questions: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Sequence[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnProfile.ProfileQuestionUpdateProperty, typing.Dict[builtins.str, typing.Any]]]]],
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed9bfb05238fe20d9001d71a736fb555a27225c18694eecfeb22613d1d086ff5(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    description: builtins.str,
    lenses: typing.Sequence[builtins.str],
    template_name: builtins.str,
    notes: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnReviewTemplate.TagsItemsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57c6b7bd56a22cf3fa2a4cbac52a7eeceaf81d358faf8e8ef92d4cd8d2b8ff47(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93d3e6f2e769fc5735494ed2d1f2735861488a04eede9b653980d528cd88e537(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05d601743cd8f8f972e70133769d55d367d5c94ce2c9c81ae482178682fd5fb9(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1403813d81c139b4a0632e973c62f08a004ede86b9deef460daee650904034f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a7af0f3ef194941dc8fb90e32d4c619ca9e28e16b739db06cbfe82fb60d3022(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f597ea62eb141a0e637cd48349cd9d1615f928e180522dd5aea608efcca6c21f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae073e52fa4b6d35952b13fd86cb2f262f3df42060ba4cb318d4299b2493c379(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ff8fbd0f70bc38c89a2d11baaa844b230802c50211badc8156ae885a85b3627(
    value: typing.Optional[typing.List[CfnReviewTemplate.TagsItemsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6b4c4c6bf31b0e2c5342222397e967c2df0b7c4a9530a93891be49fe9f1dda9(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cc0ce4fd995ce88c347c3898dd891af9cda3438ebe6053b81695e1e7909c30f(
    *,
    description: builtins.str,
    lenses: typing.Sequence[builtins.str],
    template_name: builtins.str,
    notes: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnReviewTemplate.TagsItemsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
