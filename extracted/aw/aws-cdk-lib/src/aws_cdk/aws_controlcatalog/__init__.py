r'''
# AWS::ControlCatalog Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_controlcatalog as controlcatalog
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for ControlCatalog construct libraries](https://constructs.dev/search?q=controlcatalog)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::ControlCatalog resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ControlCatalog.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::ControlCatalog](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ControlCatalog.html).

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
    import aws_cdk.interfaces.aws_controlcatalog as _aws_controlcatalog_ba0aacba
    import constructs as _constructs_77d1e7e8
else:

    _aws_cdk_0cae9daa = _LazyImport("aws_cdk")
    _aws_controlcatalog_ba0aacba = _LazyImport("aws_cdk.interfaces.aws_controlcatalog")
    _constructs_77d1e7e8 = _LazyImport("constructs")


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_controlcatalog_ba0aacba.ICommonControlRef)
class CfnCommonControl(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_controlcatalog.CfnCommonControl",
):
    '''Resource Type definition for AWS::ControlCatalog::CommonControl.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-controlcatalog-commoncontrol.html
    :cloudformationResource: AWS::ControlCatalog::CommonControl
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_controlcatalog as controlcatalog
        
        cfn_common_control = controlcatalog.CfnCommonControl(self, "MyCfnCommonControl")
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
    ) -> None:
        '''Create a new ``AWS::ControlCatalog::CommonControl``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__55035577284b9e4dffdb9a96115ce1a1f93b1d54b5b253975d588f620a4f961e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnCommonControlProps()

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForCommonControl")
    @builtins.classmethod
    def arn_for_common_control(
        cls,
        resource: "_aws_controlcatalog_ba0aacba.ICommonControlRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__8f9ea506feff611542b30c972325dc22aa75544c704943561d24c62220218a75)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForCommonControl", [resource]))

    @jsii.member(jsii_name="fromCommonControlArn")
    @builtins.classmethod
    def from_common_control_arn(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        arn: builtins.str,
    ) -> "_aws_controlcatalog_ba0aacba.ICommonControlRef":
        '''Creates a new ICommonControlRef from an ARN.

        :param scope: -
        :param id: -
        :param arn: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a2916892c67baebe1de6bd3842d01a39b42766934f2ac401783e34d9e4b2abe7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
        return typing.cast("_aws_controlcatalog_ba0aacba.ICommonControlRef", jsii.sinvoke(cls, "fromCommonControlArn", [scope, id, arn]))

    @jsii.member(jsii_name="fromCommonControlId")
    @builtins.classmethod
    def from_common_control_id(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        common_control_id: builtins.str,
    ) -> "_aws_controlcatalog_ba0aacba.ICommonControlRef":
        '''Creates a new ICommonControlRef from a commonControlId.

        :param scope: -
        :param id: -
        :param common_control_id: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__14205388d8b979f13447b5893cd7ccff146857287b8f89aad1b6512c815429e2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument common_control_id", value=common_control_id, expected_type=type_hints["common_control_id"])
        return typing.cast("_aws_controlcatalog_ba0aacba.ICommonControlRef", jsii.sinvoke(cls, "fromCommonControlId", [scope, id, common_control_id]))

    @jsii.member(jsii_name="isCfnCommonControl")
    @builtins.classmethod
    def is_cfn_common_control(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnCommonControl.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__23a75b0f5359576d242c4894e7e3c5b8ba544ac00a199b6730d401d014ec36bf)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnCommonControl", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__04e86de89cef5c8348504772befa4afe29a5e30db20506f1c36986a3eb7c8d1d)
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
            type_hints = cached_type_hints(_typecheckingstub__c77c11fe749ae628b7372d66721c72eeb1815d6a2f1c7f6f0a4693770a309143)
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
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCommonControlId")
    def attr_common_control_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: CommonControlId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCommonControlId"))

    @builtins.property
    @jsii.member(jsii_name="attrCreateTime")
    def attr_create_time(self) -> builtins.str:
        '''
        :cloudformationAttribute: CreateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreateTime"))

    @builtins.property
    @jsii.member(jsii_name="attrDescription")
    def attr_description(self) -> builtins.str:
        '''
        :cloudformationAttribute: Description
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDescription"))

    @builtins.property
    @jsii.member(jsii_name="attrDomain")
    def attr_domain(self) -> "_aws_cdk_0cae9daa.IResolvable":
        '''
        :cloudformationAttribute: Domain
        '''
        return typing.cast("_aws_cdk_0cae9daa.IResolvable", jsii.get(self, "attrDomain"))

    @builtins.property
    @jsii.member(jsii_name="attrDomainArn")
    def attr_domain_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: Domain.Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDomainArn"))

    @builtins.property
    @jsii.member(jsii_name="attrDomainName")
    def attr_domain_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: Domain.Name
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDomainName"))

    @builtins.property
    @jsii.member(jsii_name="attrLastUpdateTime")
    def attr_last_update_time(self) -> builtins.str:
        '''
        :cloudformationAttribute: LastUpdateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastUpdateTime"))

    @builtins.property
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: Name
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrName"))

    @builtins.property
    @jsii.member(jsii_name="attrObjective")
    def attr_objective(self) -> "_aws_cdk_0cae9daa.IResolvable":
        '''
        :cloudformationAttribute: Objective
        '''
        return typing.cast("_aws_cdk_0cae9daa.IResolvable", jsii.get(self, "attrObjective"))

    @builtins.property
    @jsii.member(jsii_name="attrObjectiveArn")
    def attr_objective_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: Objective.Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrObjectiveArn"))

    @builtins.property
    @jsii.member(jsii_name="attrObjectiveName")
    def attr_objective_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: Objective.Name
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrObjectiveName"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="commonControlRef")
    def common_control_ref(
        self,
    ) -> "_aws_controlcatalog_ba0aacba.CommonControlReference":
        '''A reference to a CommonControl resource.'''
        return typing.cast("_aws_controlcatalog_ba0aacba.CommonControlReference", jsii.get(self, "commonControlRef"))

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_controlcatalog.CfnCommonControl.DomainProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn", "name": "name"},
    )
    class DomainProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param arn: 
            :param name: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-controlcatalog-commoncontrol-domain.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_controlcatalog as controlcatalog
                
                domain_property = controlcatalog.CfnCommonControl.DomainProperty(
                    arn="arn",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__e186dc10d6a04a873b3122669e6b57ec2d2ca2d5293a12f55d0e366cd02ce493)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-controlcatalog-commoncontrol-domain.html#cfn-controlcatalog-commoncontrol-domain-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-controlcatalog-commoncontrol-domain.html#cfn-controlcatalog-commoncontrol-domain-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DomainProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_controlcatalog.CfnCommonControl.ObjectiveProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn", "name": "name"},
    )
    class ObjectiveProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param arn: 
            :param name: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-controlcatalog-commoncontrol-objective.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_controlcatalog as controlcatalog
                
                objective_property = controlcatalog.CfnCommonControl.ObjectiveProperty(
                    arn="arn",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__033bd910c7c9cf15a6f8c974078c1e9d784af8760e8f90d6277a2866b9d7df31)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-controlcatalog-commoncontrol-objective.html#cfn-controlcatalog-commoncontrol-objective-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-controlcatalog-commoncontrol-objective.html#cfn-controlcatalog-commoncontrol-objective-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ObjectiveProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_controlcatalog.CfnCommonControlProps",
    jsii_struct_bases=[],
    name_mapping={},
)
class CfnCommonControlProps:
    def __init__(self) -> None:
        '''Properties for defining a ``CfnCommonControl``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-controlcatalog-commoncontrol.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_controlcatalog as controlcatalog
            
            cfn_common_control_props = controlcatalog.CfnCommonControlProps()
        '''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCommonControlProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_controlcatalog_ba0aacba.IControlRef)
class CfnControl(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_controlcatalog.CfnControl",
):
    '''Resource Type definition for AWS::ControlCatalog::Control.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-controlcatalog-control.html
    :cloudformationResource: AWS::ControlCatalog::Control
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_controlcatalog as controlcatalog
        
        cfn_control = controlcatalog.CfnControl(self, "MyCfnControl")
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
    ) -> None:
        '''Create a new ``AWS::ControlCatalog::Control``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__9a65383842971c24e836b96168c36a19361c8272595d54cf83aea60e07e4e715)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnControlProps()

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForControl")
    @builtins.classmethod
    def arn_for_control(
        cls,
        resource: "_aws_controlcatalog_ba0aacba.IControlRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__0e7e62dd623945c74a175fd9b4362b0d06895bf2322b25ac5f9ef629f3ee9f9c)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForControl", [resource]))

    @jsii.member(jsii_name="fromControlArn")
    @builtins.classmethod
    def from_control_arn(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        arn: builtins.str,
    ) -> "_aws_controlcatalog_ba0aacba.IControlRef":
        '''Creates a new IControlRef from an ARN.

        :param scope: -
        :param id: -
        :param arn: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__92ac2f667d215a22144426a3767587c97d78b7ad11e25fe167acd190ae2e1e8c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
        return typing.cast("_aws_controlcatalog_ba0aacba.IControlRef", jsii.sinvoke(cls, "fromControlArn", [scope, id, arn]))

    @jsii.member(jsii_name="fromControlId")
    @builtins.classmethod
    def from_control_id(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        control_id: builtins.str,
    ) -> "_aws_controlcatalog_ba0aacba.IControlRef":
        '''Creates a new IControlRef from a controlId.

        :param scope: -
        :param id: -
        :param control_id: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e427a8327f26b8083c45478f10c05bb0ee7f4dbe45de600d4dea66c548de716c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument control_id", value=control_id, expected_type=type_hints["control_id"])
        return typing.cast("_aws_controlcatalog_ba0aacba.IControlRef", jsii.sinvoke(cls, "fromControlId", [scope, id, control_id]))

    @jsii.member(jsii_name="isCfnControl")
    @builtins.classmethod
    def is_cfn_control(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnControl.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__9e1281bdc45f9b850ca2244701dcf554ed56de42e54974ce875f1c1fede91498)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnControl", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__12d54d95725d1c4c8b8cc59e724edd3f33f1fbcd3fd62267a63d95403af971b2)
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
            type_hints = cached_type_hints(_typecheckingstub__733b0fd1fd8a57192daf9cef8dd1f57451fcd86592f1dc53a5e99f1e89ad3f20)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAliases")
    def attr_aliases(self) -> typing.List[builtins.str]:
        '''
        :cloudformationAttribute: Aliases
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "attrAliases"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrBehavior")
    def attr_behavior(self) -> builtins.str:
        '''
        :cloudformationAttribute: Behavior
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrBehavior"))

    @builtins.property
    @jsii.member(jsii_name="attrControlId")
    def attr_control_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: ControlId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrControlId"))

    @builtins.property
    @jsii.member(jsii_name="attrCreateTime")
    def attr_create_time(self) -> builtins.str:
        '''
        :cloudformationAttribute: CreateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreateTime"))

    @builtins.property
    @jsii.member(jsii_name="attrDescription")
    def attr_description(self) -> builtins.str:
        '''
        :cloudformationAttribute: Description
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDescription"))

    @builtins.property
    @jsii.member(jsii_name="attrGovernedResources")
    def attr_governed_resources(self) -> typing.List[builtins.str]:
        '''
        :cloudformationAttribute: GovernedResources
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "attrGovernedResources"))

    @builtins.property
    @jsii.member(jsii_name="attrImplementation")
    def attr_implementation(self) -> "_aws_cdk_0cae9daa.IResolvable":
        '''
        :cloudformationAttribute: Implementation
        '''
        return typing.cast("_aws_cdk_0cae9daa.IResolvable", jsii.get(self, "attrImplementation"))

    @builtins.property
    @jsii.member(jsii_name="attrImplementationIdentifier")
    def attr_implementation_identifier(self) -> builtins.str:
        '''
        :cloudformationAttribute: Implementation.Identifier
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrImplementationIdentifier"))

    @builtins.property
    @jsii.member(jsii_name="attrImplementationType")
    def attr_implementation_type(self) -> builtins.str:
        '''
        :cloudformationAttribute: Implementation.Type
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrImplementationType"))

    @builtins.property
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: Name
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrName"))

    @builtins.property
    @jsii.member(jsii_name="attrRegionConfiguration")
    def attr_region_configuration(self) -> "_aws_cdk_0cae9daa.IResolvable":
        '''
        :cloudformationAttribute: RegionConfiguration
        '''
        return typing.cast("_aws_cdk_0cae9daa.IResolvable", jsii.get(self, "attrRegionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="attrRegionConfigurationDeployableRegions")
    def attr_region_configuration_deployable_regions(self) -> typing.List[builtins.str]:
        '''
        :cloudformationAttribute: RegionConfiguration.DeployableRegions
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "attrRegionConfigurationDeployableRegions"))

    @builtins.property
    @jsii.member(jsii_name="attrRegionConfigurationScope")
    def attr_region_configuration_scope(self) -> builtins.str:
        '''
        :cloudformationAttribute: RegionConfiguration.Scope
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRegionConfigurationScope"))

    @builtins.property
    @jsii.member(jsii_name="attrSeverity")
    def attr_severity(self) -> builtins.str:
        '''
        :cloudformationAttribute: Severity
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSeverity"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="controlRef")
    def control_ref(self) -> "_aws_controlcatalog_ba0aacba.ControlReference":
        '''A reference to a Control resource.'''
        return typing.cast("_aws_controlcatalog_ba0aacba.ControlReference", jsii.get(self, "controlRef"))

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_controlcatalog.CfnControl.ImplementationDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "identifier": "identifier"},
    )
    class ImplementationDetailsProperty:
        def __init__(
            self,
            *,
            type: builtins.str,
            identifier: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param type: 
            :param identifier: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-controlcatalog-control-implementationdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_controlcatalog as controlcatalog
                
                implementation_details_property = controlcatalog.CfnControl.ImplementationDetailsProperty(
                    type="type",
                
                    # the properties below are optional
                    identifier="identifier"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__742596fd14b1eb91492b51a907dd1a27fe02c8bbb018498aa18bf8fae5655429)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument identifier", value=identifier, expected_type=type_hints["identifier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "type": type,
            }
            if identifier is not None:
                self._values["identifier"] = identifier

        @builtins.property
        def type(self) -> builtins.str:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-controlcatalog-control-implementationdetails.html#cfn-controlcatalog-control-implementationdetails-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def identifier(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-controlcatalog-control-implementationdetails.html#cfn-controlcatalog-control-implementationdetails-identifier
            '''
            result = self._values.get("identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ImplementationDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_controlcatalog.CfnControl.RegionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"scope": "scope", "deployable_regions": "deployableRegions"},
    )
    class RegionConfigurationProperty:
        def __init__(
            self,
            *,
            scope: builtins.str,
            deployable_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param scope: 
            :param deployable_regions: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-controlcatalog-control-regionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_controlcatalog as controlcatalog
                
                region_configuration_property = controlcatalog.CfnControl.RegionConfigurationProperty(
                    scope="scope",
                
                    # the properties below are optional
                    deployable_regions=["deployableRegions"]
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__0d501542b5c47fdbd2fc95a87c5f5c4cc8a4f3fb75556aadb2d3b66f1a51a341)
                check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
                check_type(argname="argument deployable_regions", value=deployable_regions, expected_type=type_hints["deployable_regions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "scope": scope,
            }
            if deployable_regions is not None:
                self._values["deployable_regions"] = deployable_regions

        @builtins.property
        def scope(self) -> builtins.str:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-controlcatalog-control-regionconfiguration.html#cfn-controlcatalog-control-regionconfiguration-scope
            '''
            result = self._values.get("scope")
            assert result is not None, "Required property 'scope' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def deployable_regions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-controlcatalog-control-regionconfiguration.html#cfn-controlcatalog-control-regionconfiguration-deployableregions
            '''
            result = self._values.get("deployable_regions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RegionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_controlcatalog.CfnControlProps",
    jsii_struct_bases=[],
    name_mapping={},
)
class CfnControlProps:
    def __init__(self) -> None:
        '''Properties for defining a ``CfnControl``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-controlcatalog-control.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_controlcatalog as controlcatalog
            
            cfn_control_props = controlcatalog.CfnControlProps()
        '''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnControlProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnCommonControl",
    "CfnCommonControlProps",
    "CfnControl",
    "CfnControlProps",
]

publication.publish()

def _typecheckingstub__55035577284b9e4dffdb9a96115ce1a1f93b1d54b5b253975d588f620a4f961e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f9ea506feff611542b30c972325dc22aa75544c704943561d24c62220218a75(
    resource: _aws_controlcatalog_ba0aacba.ICommonControlRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2916892c67baebe1de6bd3842d01a39b42766934f2ac401783e34d9e4b2abe7(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14205388d8b979f13447b5893cd7ccff146857287b8f89aad1b6512c815429e2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    common_control_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23a75b0f5359576d242c4894e7e3c5b8ba544ac00a199b6730d401d014ec36bf(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04e86de89cef5c8348504772befa4afe29a5e30db20506f1c36986a3eb7c8d1d(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c77c11fe749ae628b7372d66721c72eeb1815d6a2f1c7f6f0a4693770a309143(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e186dc10d6a04a873b3122669e6b57ec2d2ca2d5293a12f55d0e366cd02ce493(
    *,
    arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__033bd910c7c9cf15a6f8c974078c1e9d784af8760e8f90d6277a2866b9d7df31(
    *,
    arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a65383842971c24e836b96168c36a19361c8272595d54cf83aea60e07e4e715(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e7e62dd623945c74a175fd9b4362b0d06895bf2322b25ac5f9ef629f3ee9f9c(
    resource: _aws_controlcatalog_ba0aacba.IControlRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92ac2f667d215a22144426a3767587c97d78b7ad11e25fe167acd190ae2e1e8c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e427a8327f26b8083c45478f10c05bb0ee7f4dbe45de600d4dea66c548de716c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    control_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e1281bdc45f9b850ca2244701dcf554ed56de42e54974ce875f1c1fede91498(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12d54d95725d1c4c8b8cc59e724edd3f33f1fbcd3fd62267a63d95403af971b2(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__733b0fd1fd8a57192daf9cef8dd1f57451fcd86592f1dc53a5e99f1e89ad3f20(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__742596fd14b1eb91492b51a907dd1a27fe02c8bbb018498aa18bf8fae5655429(
    *,
    type: builtins.str,
    identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d501542b5c47fdbd2fc95a87c5f5c4cc8a4f3fb75556aadb2d3b66f1a51a341(
    *,
    scope: builtins.str,
    deployable_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
