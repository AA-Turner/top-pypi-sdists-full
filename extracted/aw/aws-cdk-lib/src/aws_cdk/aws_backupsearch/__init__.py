r'''
# AWS::BackupSearch Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_backupsearch as backupsearch
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for BackupSearch construct libraries](https://constructs.dev/search?q=backupsearch)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::BackupSearch resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_BackupSearch.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::BackupSearch](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_BackupSearch.html).

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
    import aws_cdk.interfaces.aws_backupsearch as _aws_backupsearch_69ddc0c1
    import constructs as _constructs_77d1e7e8
else:

    _aws_backupsearch_69ddc0c1 = _LazyImport("aws_cdk.interfaces.aws_backupsearch")
    _aws_cdk_0cae9daa = _LazyImport("aws_cdk")
    _constructs_77d1e7e8 = _LazyImport("constructs")


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_backupsearch_69ddc0c1.ISearchJobRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnSearchJob(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_backupsearch.CfnSearchJob",
):
    '''Definition of AWS::BackupSearch::SearchJob Resource Type.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backupsearch-searchjob.html
    :cloudformationResource: AWS::BackupSearch::SearchJob
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_backupsearch as backupsearch
        
        cfn_search_job = backupsearch.CfnSearchJob(self, "MyCfnSearchJob",
            search_scope=backupsearch.CfnSearchJob.SearchScopeProperty(
                backup_resource_types=["backupResourceTypes"]
            ),
        
            # the properties below are optional
            name="name",
            tags=[backupsearch.CfnSearchJob.TagsItemsProperty(
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
        search_scope: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnSearchJob.SearchScopeProperty", typing.Dict[builtins.str, typing.Any]]],
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnSearchJob.TagsItemsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::BackupSearch::SearchJob``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param search_scope: The search scope for the search job.
        :param name: The name of the search job.
        :param tags: Tags associated with the search job.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6ec1691ebb850ffa07dc7f2ccfad97d19b7683761824e26fa704faadea34b5f0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSearchJobProps(search_scope=search_scope, name=name, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForSearchJob")
    @builtins.classmethod
    def arn_for_search_job(
        cls,
        resource: "_aws_backupsearch_69ddc0c1.ISearchJobRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__dd064f7fd3c6377e6503c3f86458665e69678f8e6896010f85aeff1590046fa1)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForSearchJob", [resource]))

    @jsii.member(jsii_name="isCfnSearchJob")
    @builtins.classmethod
    def is_cfn_search_job(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnSearchJob.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__54c6851c37f1c1ea7a6adedceb8d287d66dde2925387b4103efb28ab41c6b290)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnSearchJob", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1c689aaf9d138f919f639f4c174aa2e96417d36bc1d55df488632a89878bc786)
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
            type_hints = cached_type_hints(_typecheckingstub__afd6931bcd77ce18387348c6398919f463f5fd4cf36e210a73e78eede425a6ba)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationTime")
    def attr_creation_time(self) -> builtins.str:
        '''The date and time the search job was created.

        :cloudformationAttribute: CreationTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationTime"))

    @builtins.property
    @jsii.member(jsii_name="attrSearchJobArn")
    def attr_search_job_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the search job.

        :cloudformationAttribute: SearchJobArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSearchJobArn"))

    @builtins.property
    @jsii.member(jsii_name="attrSearchJobIdentifier")
    def attr_search_job_identifier(self) -> builtins.str:
        '''The unique identifier of the search job.

        :cloudformationAttribute: SearchJobIdentifier
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSearchJobIdentifier"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The current status of the search job.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

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
    @jsii.member(jsii_name="searchJobRef")
    def search_job_ref(self) -> "_aws_backupsearch_69ddc0c1.SearchJobReference":
        '''A reference to a SearchJob resource.'''
        return typing.cast("_aws_backupsearch_69ddc0c1.SearchJobReference", jsii.get(self, "searchJobRef"))

    @builtins.property
    @jsii.member(jsii_name="searchScope")
    def search_scope(
        self,
    ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnSearchJob.SearchScopeProperty"]:
        '''The search scope for the search job.'''
        return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnSearchJob.SearchScopeProperty"], jsii.get(self, "searchScope"))

    @search_scope.setter
    def search_scope(
        self,
        value: typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnSearchJob.SearchScopeProperty"],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__022dc53d06abc45e550a7bf7e04184f3c9df310ea3bb6d2b7b37ea5187e9c28b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "searchScope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the search job.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__926e5442fa23f1f0451109546dc7f8038b3461d734b9df4e5d28316d131b3af6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["CfnSearchJob.TagsItemsProperty"]]:
        '''Tags associated with the search job.'''
        return typing.cast(typing.Optional[typing.List["CfnSearchJob.TagsItemsProperty"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["CfnSearchJob.TagsItemsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__7c00895104d6892c3a69f8c328488715227389cd093ad21a6749d8c037e2502f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_backupsearch.CfnSearchJob.SearchScopeProperty",
        jsii_struct_bases=[],
        name_mapping={"backup_resource_types": "backupResourceTypes"},
    )
    class SearchScopeProperty:
        def __init__(
            self,
            *,
            backup_resource_types: typing.Sequence[builtins.str],
        ) -> None:
            '''The search scope for the search job.

            :param backup_resource_types: The resource types included in a search.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backupsearch-searchjob-searchscope.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_backupsearch as backupsearch
                
                search_scope_property = backupsearch.CfnSearchJob.SearchScopeProperty(
                    backup_resource_types=["backupResourceTypes"]
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__334deb6708f27561c0823b304ac4a055a515cd99b0915ed7726a37071d66e685)
                check_type(argname="argument backup_resource_types", value=backup_resource_types, expected_type=type_hints["backup_resource_types"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "backup_resource_types": backup_resource_types,
            }

        @builtins.property
        def backup_resource_types(self) -> typing.List[builtins.str]:
            '''The resource types included in a search.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backupsearch-searchjob-searchscope.html#cfn-backupsearch-searchjob-searchscope-backupresourcetypes
            '''
            result = self._values.get("backup_resource_types")
            assert result is not None, "Required property 'backup_resource_types' is missing"
            return typing.cast(typing.List[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SearchScopeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_backupsearch.CfnSearchJob.TagsItemsProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagsItemsProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            '''
            :param key: 
            :param value: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backupsearch-searchjob-tagsitems.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_backupsearch as backupsearch
                
                tags_items_property = backupsearch.CfnSearchJob.TagsItemsProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__6e53c38c7d5d452a563471ef4291e7423b3b464daf3189c8619957f21a7bd1f5)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backupsearch-searchjob-tagsitems.html#cfn-backupsearch-searchjob-tagsitems-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backupsearch-searchjob-tagsitems.html#cfn-backupsearch-searchjob-tagsitems-value
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
    jsii_type="aws-cdk-lib.aws_backupsearch.CfnSearchJobProps",
    jsii_struct_bases=[],
    name_mapping={"search_scope": "searchScope", "name": "name", "tags": "tags"},
)
class CfnSearchJobProps:
    def __init__(
        self,
        *,
        search_scope: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnSearchJob.SearchScopeProperty", typing.Dict[builtins.str, typing.Any]]],
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnSearchJob.TagsItemsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnSearchJob``.

        :param search_scope: The search scope for the search job.
        :param name: The name of the search job.
        :param tags: Tags associated with the search job.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backupsearch-searchjob.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_backupsearch as backupsearch
            
            cfn_search_job_props = backupsearch.CfnSearchJobProps(
                search_scope=backupsearch.CfnSearchJob.SearchScopeProperty(
                    backup_resource_types=["backupResourceTypes"]
                ),
            
                # the properties below are optional
                name="name",
                tags=[backupsearch.CfnSearchJob.TagsItemsProperty(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__cc6588c165321b42f4569ab3a568005a8d56e0ddef401268bbebfe8e1f512617)
            check_type(argname="argument search_scope", value=search_scope, expected_type=type_hints["search_scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "search_scope": search_scope,
        }
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def search_scope(
        self,
    ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnSearchJob.SearchScopeProperty"]:
        '''The search scope for the search job.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backupsearch-searchjob.html#cfn-backupsearch-searchjob-searchscope
        '''
        result = self._values.get("search_scope")
        assert result is not None, "Required property 'search_scope' is missing"
        return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnSearchJob.SearchScopeProperty"], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the search job.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backupsearch-searchjob.html#cfn-backupsearch-searchjob-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["CfnSearchJob.TagsItemsProperty"]]:
        '''Tags associated with the search job.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backupsearch-searchjob.html#cfn-backupsearch-searchjob-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["CfnSearchJob.TagsItemsProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSearchJobProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnSearchJob",
    "CfnSearchJobProps",
]

publication.publish()

def _typecheckingstub__6ec1691ebb850ffa07dc7f2ccfad97d19b7683761824e26fa704faadea34b5f0(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    search_scope: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnSearchJob.SearchScopeProperty, typing.Dict[builtins.str, typing.Any]]],
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnSearchJob.TagsItemsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd064f7fd3c6377e6503c3f86458665e69678f8e6896010f85aeff1590046fa1(
    resource: _aws_backupsearch_69ddc0c1.ISearchJobRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54c6851c37f1c1ea7a6adedceb8d287d66dde2925387b4103efb28ab41c6b290(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c689aaf9d138f919f639f4c174aa2e96417d36bc1d55df488632a89878bc786(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afd6931bcd77ce18387348c6398919f463f5fd4cf36e210a73e78eede425a6ba(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__022dc53d06abc45e550a7bf7e04184f3c9df310ea3bb6d2b7b37ea5187e9c28b(
    value: typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnSearchJob.SearchScopeProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__926e5442fa23f1f0451109546dc7f8038b3461d734b9df4e5d28316d131b3af6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c00895104d6892c3a69f8c328488715227389cd093ad21a6749d8c037e2502f(
    value: typing.Optional[typing.List[CfnSearchJob.TagsItemsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__334deb6708f27561c0823b304ac4a055a515cd99b0915ed7726a37071d66e685(
    *,
    backup_resource_types: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e53c38c7d5d452a563471ef4291e7423b3b464daf3189c8619957f21a7bd1f5(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc6588c165321b42f4569ab3a568005a8d56e0ddef401268bbebfe8e1f512617(
    *,
    search_scope: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnSearchJob.SearchScopeProperty, typing.Dict[builtins.str, typing.Any]]],
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnSearchJob.TagsItemsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
