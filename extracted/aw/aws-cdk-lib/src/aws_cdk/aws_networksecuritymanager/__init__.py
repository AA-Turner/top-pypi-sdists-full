r'''
# AWS::NetworkSecurityManager Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_networksecuritymanager as networksecuritymanager
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for NetworkSecurityManager construct libraries](https://constructs.dev/search?q=networksecuritymanager)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::NetworkSecurityManager resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_NetworkSecurityManager.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::NetworkSecurityManager](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_NetworkSecurityManager.html).

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
    import aws_cdk.interfaces.aws_networksecuritymanager as _aws_networksecuritymanager_a06671e9
    import constructs as _constructs_77d1e7e8
else:

    _aws_cdk_0cae9daa = _LazyImport("aws_cdk")
    _aws_networksecuritymanager_a06671e9 = _LazyImport("aws_cdk.interfaces.aws_networksecuritymanager")
    _constructs_77d1e7e8 = _LazyImport("constructs")


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_networksecuritymanager_a06671e9.IDeploymentRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnDeployment(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_networksecuritymanager.CfnDeployment",
):
    '''Resource Type definition for AWS::NetworkSecurityManager::Deployment.

    Creates and manages a Network Security Manager deployment.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-deployment.html
    :cloudformationResource: AWS::NetworkSecurityManager::Deployment
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_networksecuritymanager as networksecuritymanager
        
        cfn_deployment = networksecuritymanager.CfnDeployment(self, "MyCfnDeployment",
            deployment_name="deploymentName",
        
            # the properties below are optional
            associated_policy_list=[networksecuritymanager.CfnDeployment.AssociatedPolicyProperty(
                policy_arn="policyArn"
            )],
            associated_scope_list=[networksecuritymanager.CfnDeployment.AssociatedScopeProperty(
                scope_arn="scopeArn"
            )],
            deployment_configuration=networksecuritymanager.CfnDeployment.DeploymentConfigurationProperty(
                enable_cross_account_visibility=False
            ),
            deployment_description="deploymentDescription",
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
        deployment_name: builtins.str,
        associated_policy_list: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Sequence[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnDeployment.AssociatedPolicyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        associated_scope_list: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Sequence[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnDeployment.AssociatedScopeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        deployment_configuration: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnDeployment.DeploymentConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        deployment_description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::NetworkSecurityManager::Deployment``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param deployment_name: The name of the deployment.
        :param associated_policy_list: List of policies associated with this deployment.
        :param associated_scope_list: List of scopes associated with this deployment.
        :param deployment_configuration: Configuration settings for the deployment.
        :param deployment_description: A description of the deployment.
        :param tags: The tags associated with the deployment.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3f39c840c5df17b618e9ab668273d1bd2d8972453214cbe27e1af6e7fbb8f9bb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDeploymentProps(
            deployment_name=deployment_name,
            associated_policy_list=associated_policy_list,
            associated_scope_list=associated_scope_list,
            deployment_configuration=deployment_configuration,
            deployment_description=deployment_description,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForDeployment")
    @builtins.classmethod
    def arn_for_deployment(
        cls,
        resource: "_aws_networksecuritymanager_a06671e9.IDeploymentRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__cb9100d3f5ecd518543c9d7b93315dde93e21ae8404648129d590e480c750995)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForDeployment", [resource]))

    @jsii.member(jsii_name="isCfnDeployment")
    @builtins.classmethod
    def is_cfn_deployment(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnDeployment.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d691846db836794178f9fdaf83029f3da5a6788b39e33ca4a528a7c7fbc94ed3)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnDeployment", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1a18c344f16e32e6fc04a52409866551333f2aae35e5fdb02fe8698711a0a930)
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
            type_hints = cached_type_hints(_typecheckingstub__49514bf67a86289b947047b4446045f46656df1034b4d9170cd84bec275fc852)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    @builtins.classmethod
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrDeploymentArn")
    def attr_deployment_arn(self) -> builtins.str:
        '''The ARN of the deployment.

        :cloudformationAttribute: DeploymentArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDeploymentArn"))

    @builtins.property
    @jsii.member(jsii_name="attrDeploymentId")
    def attr_deployment_id(self) -> builtins.str:
        '''The unique identifier of the deployment.

        :cloudformationAttribute: DeploymentId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDeploymentId"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The status of the deployment.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdatedAt")
    def attr_updated_at(self) -> builtins.str:
        '''An ISO 8601 timestamp indicating when the deployment was last modified.

        :cloudformationAttribute: UpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrVersion")
    def attr_version(self) -> builtins.str:
        '''The version number.

        :cloudformationAttribute: Version
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVersion"))

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
    @jsii.member(jsii_name="deploymentRef")
    def deployment_ref(
        self,
    ) -> "_aws_networksecuritymanager_a06671e9.DeploymentReference":
        '''A reference to a Deployment resource.'''
        return typing.cast("_aws_networksecuritymanager_a06671e9.DeploymentReference", jsii.get(self, "deploymentRef"))

    @builtins.property
    @jsii.member(jsii_name="deploymentName")
    def deployment_name(self) -> builtins.str:
        '''The name of the deployment.'''
        return typing.cast(builtins.str, jsii.get(self, "deploymentName"))

    @deployment_name.setter
    def deployment_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a5c0ceaaf5ade36cecdae6b388f0f5c91426589cd41c0c3f20404bc2afc55022)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentName", value)

    @builtins.property
    @jsii.member(jsii_name="associatedPolicyList")
    def associated_policy_list(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDeployment.AssociatedPolicyProperty"]]]]:
        '''List of policies associated with this deployment.'''
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDeployment.AssociatedPolicyProperty"]]]], jsii.get(self, "associatedPolicyList"))

    @associated_policy_list.setter
    def associated_policy_list(
        self,
        value: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDeployment.AssociatedPolicyProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__4df5ae837ad9251c88e4e7f89160d3a9790f05e0ac86ae1f6748b4456affd9b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "associatedPolicyList", value)

    @builtins.property
    @jsii.member(jsii_name="associatedScopeList")
    def associated_scope_list(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDeployment.AssociatedScopeProperty"]]]]:
        '''List of scopes associated with this deployment.'''
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDeployment.AssociatedScopeProperty"]]]], jsii.get(self, "associatedScopeList"))

    @associated_scope_list.setter
    def associated_scope_list(
        self,
        value: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDeployment.AssociatedScopeProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__502611450f2185f1516eac85bb373d188a6d7503e22974b812058d51af2a61fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "associatedScopeList", value)

    @builtins.property
    @jsii.member(jsii_name="deploymentConfiguration")
    def deployment_configuration(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDeployment.DeploymentConfigurationProperty"]]:
        '''Configuration settings for the deployment.'''
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDeployment.DeploymentConfigurationProperty"]], jsii.get(self, "deploymentConfiguration"))

    @deployment_configuration.setter
    def deployment_configuration(
        self,
        value: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDeployment.DeploymentConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a8583c77943e2827a47d4b8fbf4a9a60dfe18af98963360ea172a35248acaa61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="deploymentDescription")
    def deployment_description(self) -> typing.Optional[builtins.str]:
        '''A description of the deployment.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentDescription"))

    @deployment_description.setter
    def deployment_description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1d46f859371b9b0fc92538e0eb745d6bee7f3d1a0a3da83c19f68f3e0628e594)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentDescription", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''The tags associated with the deployment.'''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e95b757f6b39d96c49bd92fc69c053bf092805e3bb9adc257a23ad77288655f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_networksecuritymanager.CfnDeployment.AssociatedPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"policy_arn": "policyArn"},
    )
    class AssociatedPolicyProperty:
        def __init__(self, *, policy_arn: builtins.str) -> None:
            '''
            :param policy_arn: ARN of the associated policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networksecuritymanager-deployment-associatedpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_networksecuritymanager as networksecuritymanager
                
                associated_policy_property = networksecuritymanager.CfnDeployment.AssociatedPolicyProperty(
                    policy_arn="policyArn"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__306f7d4eae62b640a3ba14c5adc2e413887bb96f70feb8796939ef73d8dfd75f)
                check_type(argname="argument policy_arn", value=policy_arn, expected_type=type_hints["policy_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "policy_arn": policy_arn,
            }

        @builtins.property
        def policy_arn(self) -> builtins.str:
            '''ARN of the associated policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networksecuritymanager-deployment-associatedpolicy.html#cfn-networksecuritymanager-deployment-associatedpolicy-policyarn
            '''
            result = self._values.get("policy_arn")
            assert result is not None, "Required property 'policy_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssociatedPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_networksecuritymanager.CfnDeployment.AssociatedScopeProperty",
        jsii_struct_bases=[],
        name_mapping={"scope_arn": "scopeArn"},
    )
    class AssociatedScopeProperty:
        def __init__(self, *, scope_arn: builtins.str) -> None:
            '''
            :param scope_arn: ARN of the associated scope.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networksecuritymanager-deployment-associatedscope.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_networksecuritymanager as networksecuritymanager
                
                associated_scope_property = networksecuritymanager.CfnDeployment.AssociatedScopeProperty(
                    scope_arn="scopeArn"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__a584b4b537b5cb33cf1acf514ac44cd26e97863965f05c7005638fd73417392d)
                check_type(argname="argument scope_arn", value=scope_arn, expected_type=type_hints["scope_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "scope_arn": scope_arn,
            }

        @builtins.property
        def scope_arn(self) -> builtins.str:
            '''ARN of the associated scope.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networksecuritymanager-deployment-associatedscope.html#cfn-networksecuritymanager-deployment-associatedscope-scopearn
            '''
            result = self._values.get("scope_arn")
            assert result is not None, "Required property 'scope_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssociatedScopeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_networksecuritymanager.CfnDeployment.DeploymentConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enable_cross_account_visibility": "enableCrossAccountVisibility",
        },
    )
    class DeploymentConfigurationProperty:
        def __init__(
            self,
            *,
            enable_cross_account_visibility: typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"],
        ) -> None:
            '''Configuration settings for the deployment.

            :param enable_cross_account_visibility: Whether cross-account visibility is enabled for the deployment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networksecuritymanager-deployment-deploymentconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_networksecuritymanager as networksecuritymanager
                
                deployment_configuration_property = networksecuritymanager.CfnDeployment.DeploymentConfigurationProperty(
                    enable_cross_account_visibility=False
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__154eba5468d601ce94ae486b9a13246a28745f5bb16fe814194910e16ef2eca0)
                check_type(argname="argument enable_cross_account_visibility", value=enable_cross_account_visibility, expected_type=type_hints["enable_cross_account_visibility"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "enable_cross_account_visibility": enable_cross_account_visibility,
            }

        @builtins.property
        def enable_cross_account_visibility(
            self,
        ) -> typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]:
            '''Whether cross-account visibility is enabled for the deployment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networksecuritymanager-deployment-deploymentconfiguration.html#cfn-networksecuritymanager-deployment-deploymentconfiguration-enablecrossaccountvisibility
            '''
            result = self._values.get("enable_cross_account_visibility")
            assert result is not None, "Required property 'enable_cross_account_visibility' is missing"
            return typing.cast(typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeploymentConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_networksecuritymanager.CfnDeploymentProps",
    jsii_struct_bases=[],
    name_mapping={
        "deployment_name": "deploymentName",
        "associated_policy_list": "associatedPolicyList",
        "associated_scope_list": "associatedScopeList",
        "deployment_configuration": "deploymentConfiguration",
        "deployment_description": "deploymentDescription",
        "tags": "tags",
    },
)
class CfnDeploymentProps:
    def __init__(
        self,
        *,
        deployment_name: builtins.str,
        associated_policy_list: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Sequence[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnDeployment.AssociatedPolicyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        associated_scope_list: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Sequence[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnDeployment.AssociatedScopeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        deployment_configuration: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnDeployment.DeploymentConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        deployment_description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnDeployment``.

        :param deployment_name: The name of the deployment.
        :param associated_policy_list: List of policies associated with this deployment.
        :param associated_scope_list: List of scopes associated with this deployment.
        :param deployment_configuration: Configuration settings for the deployment.
        :param deployment_description: A description of the deployment.
        :param tags: The tags associated with the deployment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-deployment.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_networksecuritymanager as networksecuritymanager
            
            cfn_deployment_props = networksecuritymanager.CfnDeploymentProps(
                deployment_name="deploymentName",
            
                # the properties below are optional
                associated_policy_list=[networksecuritymanager.CfnDeployment.AssociatedPolicyProperty(
                    policy_arn="policyArn"
                )],
                associated_scope_list=[networksecuritymanager.CfnDeployment.AssociatedScopeProperty(
                    scope_arn="scopeArn"
                )],
                deployment_configuration=networksecuritymanager.CfnDeployment.DeploymentConfigurationProperty(
                    enable_cross_account_visibility=False
                ),
                deployment_description="deploymentDescription",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__4da69db68df96fa3214f35b58941f59f95df427e723ef1e2e8933c6e744114cd)
            check_type(argname="argument deployment_name", value=deployment_name, expected_type=type_hints["deployment_name"])
            check_type(argname="argument associated_policy_list", value=associated_policy_list, expected_type=type_hints["associated_policy_list"])
            check_type(argname="argument associated_scope_list", value=associated_scope_list, expected_type=type_hints["associated_scope_list"])
            check_type(argname="argument deployment_configuration", value=deployment_configuration, expected_type=type_hints["deployment_configuration"])
            check_type(argname="argument deployment_description", value=deployment_description, expected_type=type_hints["deployment_description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "deployment_name": deployment_name,
        }
        if associated_policy_list is not None:
            self._values["associated_policy_list"] = associated_policy_list
        if associated_scope_list is not None:
            self._values["associated_scope_list"] = associated_scope_list
        if deployment_configuration is not None:
            self._values["deployment_configuration"] = deployment_configuration
        if deployment_description is not None:
            self._values["deployment_description"] = deployment_description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def deployment_name(self) -> builtins.str:
        '''The name of the deployment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-deployment.html#cfn-networksecuritymanager-deployment-deploymentname
        '''
        result = self._values.get("deployment_name")
        assert result is not None, "Required property 'deployment_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def associated_policy_list(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDeployment.AssociatedPolicyProperty"]]]]:
        '''List of policies associated with this deployment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-deployment.html#cfn-networksecuritymanager-deployment-associatedpolicylist
        '''
        result = self._values.get("associated_policy_list")
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDeployment.AssociatedPolicyProperty"]]]], result)

    @builtins.property
    def associated_scope_list(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDeployment.AssociatedScopeProperty"]]]]:
        '''List of scopes associated with this deployment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-deployment.html#cfn-networksecuritymanager-deployment-associatedscopelist
        '''
        result = self._values.get("associated_scope_list")
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDeployment.AssociatedScopeProperty"]]]], result)

    @builtins.property
    def deployment_configuration(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDeployment.DeploymentConfigurationProperty"]]:
        '''Configuration settings for the deployment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-deployment.html#cfn-networksecuritymanager-deployment-deploymentconfiguration
        '''
        result = self._values.get("deployment_configuration")
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDeployment.DeploymentConfigurationProperty"]], result)

    @builtins.property
    def deployment_description(self) -> typing.Optional[builtins.str]:
        '''A description of the deployment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-deployment.html#cfn-networksecuritymanager-deployment-deploymentdescription
        '''
        result = self._values.get("deployment_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''The tags associated with the deployment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-deployment.html#cfn-networksecuritymanager-deployment-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_networksecuritymanager_a06671e9.IPolicyRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnPolicy(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_networksecuritymanager.CfnPolicy",
):
    '''Resource Type definition for AWS::NetworkSecurityManager::Policy.

    Creates and manages a Network Security Manager policy.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-policy.html
    :cloudformationResource: AWS::NetworkSecurityManager::Policy
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_networksecuritymanager as networksecuritymanager
        
        cfn_policy = networksecuritymanager.CfnPolicy(self, "MyCfnPolicy",
            firewall_type="firewallType",
            policy_configuration=networksecuritymanager.CfnPolicy.PolicyConfigurationProperty(
                remediation_enabled=False,
                resources_clean_up=False,
                waf_config=networksecuritymanager.CfnPolicy.WafConfigProperty(
                    conflict_resolution="conflictResolution",
                    existing_customer_web_acl_resolution="existingCustomerWebAclResolution"
                )
            ),
            policy_name="policyName",
            priority=123,
        
            # the properties below are optional
            associated_template_and_rule_list=[networksecuritymanager.CfnPolicy.AssociatedTemplateAndRuleProperty(
                rule_arn="ruleArn",
                template_arn="templateArn"
            )],
            policy_description="policyDescription",
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
        firewall_type: builtins.str,
        policy_configuration: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnPolicy.PolicyConfigurationProperty", typing.Dict[builtins.str, typing.Any]]],
        policy_name: builtins.str,
        priority: jsii.Number,
        associated_template_and_rule_list: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Sequence[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnPolicy.AssociatedTemplateAndRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        policy_description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::NetworkSecurityManager::Policy``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param firewall_type: The type of firewall.
        :param policy_configuration: Configuration settings for policy behavior.
        :param policy_name: The name of the policy.
        :param priority: The priority of the policy.
        :param associated_template_and_rule_list: List of templates and rules associated with this policy.
        :param policy_description: A description of the policy.
        :param tags: The tags associated with the policy.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e455d8af87a638174f344d9a93d7603b20ba5eb09596bb904ec2fd74cc5ce3d3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPolicyProps(
            firewall_type=firewall_type,
            policy_configuration=policy_configuration,
            policy_name=policy_name,
            priority=priority,
            associated_template_and_rule_list=associated_template_and_rule_list,
            policy_description=policy_description,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForPolicy")
    @builtins.classmethod
    def arn_for_policy(
        cls,
        resource: "_aws_networksecuritymanager_a06671e9.IPolicyRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b095f3e022eeefa5110592d7571739da7549a8be5f0b8f265c1d56889317f795)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForPolicy", [resource]))

    @jsii.member(jsii_name="isCfnPolicy")
    @builtins.classmethod
    def is_cfn_policy(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnPolicy.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__81843608d40596bdfec2ed93e7c070999c60ed3e2284da5ff4b6c29cc53a6c21)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnPolicy", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6081c17a0ed16f1abac4add790966f09c5b4b231547e20dd99297f1697845f8c)
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
            type_hints = cached_type_hints(_typecheckingstub__556b5797c35eb8b15df7dc91407356bbde61e40e66a67ad5e88c22a5f93e6962)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    @builtins.classmethod
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrPolicyArn")
    def attr_policy_arn(self) -> builtins.str:
        '''The ARN of the policy.

        :cloudformationAttribute: PolicyArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPolicyArn"))

    @builtins.property
    @jsii.member(jsii_name="attrPolicyId")
    def attr_policy_id(self) -> builtins.str:
        '''The unique identifier of the policy.

        :cloudformationAttribute: PolicyId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPolicyId"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The status of the policy.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdatedAt")
    def attr_updated_at(self) -> builtins.str:
        '''An ISO 8601 timestamp indicating when the policy was last modified.

        :cloudformationAttribute: UpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrVersion")
    def attr_version(self) -> builtins.str:
        '''The version number.

        :cloudformationAttribute: Version
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVersion"))

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
    @jsii.member(jsii_name="policyRef")
    def policy_ref(self) -> "_aws_networksecuritymanager_a06671e9.PolicyReference":
        '''A reference to a Policy resource.'''
        return typing.cast("_aws_networksecuritymanager_a06671e9.PolicyReference", jsii.get(self, "policyRef"))

    @builtins.property
    @jsii.member(jsii_name="firewallType")
    def firewall_type(self) -> builtins.str:
        '''The type of firewall.'''
        return typing.cast(builtins.str, jsii.get(self, "firewallType"))

    @firewall_type.setter
    def firewall_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3689b76c694f1cbcb15847ed12fcc71fc4de945907b84ec480460ddd342006b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firewallType", value)

    @builtins.property
    @jsii.member(jsii_name="policyConfiguration")
    def policy_configuration(
        self,
    ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnPolicy.PolicyConfigurationProperty"]:
        '''Configuration settings for policy behavior.'''
        return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnPolicy.PolicyConfigurationProperty"], jsii.get(self, "policyConfiguration"))

    @policy_configuration.setter
    def policy_configuration(
        self,
        value: typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnPolicy.PolicyConfigurationProperty"],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__85fe1123c733f774b5881dc32e28c60085600f5f2e10cb5b3f86b0fff3a71536)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> builtins.str:
        '''The name of the policy.'''
        return typing.cast(builtins.str, jsii.get(self, "policyName"))

    @policy_name.setter
    def policy_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d056ce533e7118a721b0fd7f581ee6faad5d0ab568d8a8407a8a3ab7c926ad8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyName", value)

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        '''The priority of the policy.'''
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__5af51aaf48b615b9d972230f14ae3e9998750105fde8b6cf6a663950a85eea6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value)

    @builtins.property
    @jsii.member(jsii_name="associatedTemplateAndRuleList")
    def associated_template_and_rule_list(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnPolicy.AssociatedTemplateAndRuleProperty"]]]]:
        '''List of templates and rules associated with this policy.'''
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnPolicy.AssociatedTemplateAndRuleProperty"]]]], jsii.get(self, "associatedTemplateAndRuleList"))

    @associated_template_and_rule_list.setter
    def associated_template_and_rule_list(
        self,
        value: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnPolicy.AssociatedTemplateAndRuleProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__5d6d0649064408e9f07375e685a9c0f377b816a338cedfde7d5ad3ba47b631dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "associatedTemplateAndRuleList", value)

    @builtins.property
    @jsii.member(jsii_name="policyDescription")
    def policy_description(self) -> typing.Optional[builtins.str]:
        '''A description of the policy.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyDescription"))

    @policy_description.setter
    def policy_description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__146edd331f95c9894b839e912f3c5e3c9e5db99b266e9f6c120c8877f57a54d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyDescription", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''The tags associated with the policy.'''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__317966e71a07d6489f5a99a868ec2bf13dae386c29fc0f76d96a686f90b0de86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_networksecuritymanager.CfnPolicy.AssociatedTemplateAndRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"rule_arn": "ruleArn", "template_arn": "templateArn"},
    )
    class AssociatedTemplateAndRuleProperty:
        def __init__(
            self,
            *,
            rule_arn: typing.Optional[builtins.str] = None,
            template_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Associates either a template or a rule with a policy.

            :param rule_arn: ARN of the associated rule.
            :param template_arn: ARN of the associated template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networksecuritymanager-policy-associatedtemplateandrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_networksecuritymanager as networksecuritymanager
                
                associated_template_and_rule_property = networksecuritymanager.CfnPolicy.AssociatedTemplateAndRuleProperty(
                    rule_arn="ruleArn",
                    template_arn="templateArn"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__22f88dff79c8071f59256fe33147daa14194ec6b52ee1ee0552d8d7b1587e6f0)
                check_type(argname="argument rule_arn", value=rule_arn, expected_type=type_hints["rule_arn"])
                check_type(argname="argument template_arn", value=template_arn, expected_type=type_hints["template_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if rule_arn is not None:
                self._values["rule_arn"] = rule_arn
            if template_arn is not None:
                self._values["template_arn"] = template_arn

        @builtins.property
        def rule_arn(self) -> typing.Optional[builtins.str]:
            '''ARN of the associated rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networksecuritymanager-policy-associatedtemplateandrule.html#cfn-networksecuritymanager-policy-associatedtemplateandrule-rulearn
            '''
            result = self._values.get("rule_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def template_arn(self) -> typing.Optional[builtins.str]:
            '''ARN of the associated template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networksecuritymanager-policy-associatedtemplateandrule.html#cfn-networksecuritymanager-policy-associatedtemplateandrule-templatearn
            '''
            result = self._values.get("template_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssociatedTemplateAndRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_networksecuritymanager.CfnPolicy.PolicyConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "remediation_enabled": "remediationEnabled",
            "resources_clean_up": "resourcesCleanUp",
            "waf_config": "wafConfig",
        },
    )
    class PolicyConfigurationProperty:
        def __init__(
            self,
            *,
            remediation_enabled: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
            resources_clean_up: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
            waf_config: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnPolicy.WafConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Configuration settings for policy behavior.

            :param remediation_enabled: Controls automatic remediation of non-compliant resources.
            :param resources_clean_up: Controls automatic cleanup of unused resources.
            :param waf_config: WAF-specific policy settings. Populated only for WAF firewall type policies.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networksecuritymanager-policy-policyconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_networksecuritymanager as networksecuritymanager
                
                policy_configuration_property = networksecuritymanager.CfnPolicy.PolicyConfigurationProperty(
                    remediation_enabled=False,
                    resources_clean_up=False,
                    waf_config=networksecuritymanager.CfnPolicy.WafConfigProperty(
                        conflict_resolution="conflictResolution",
                        existing_customer_web_acl_resolution="existingCustomerWebAclResolution"
                    )
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__759ff63568a360d5f4dd2fd4ebfa70ddb6c3ad174bf1a984add0075380b24d7a)
                check_type(argname="argument remediation_enabled", value=remediation_enabled, expected_type=type_hints["remediation_enabled"])
                check_type(argname="argument resources_clean_up", value=resources_clean_up, expected_type=type_hints["resources_clean_up"])
                check_type(argname="argument waf_config", value=waf_config, expected_type=type_hints["waf_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if remediation_enabled is not None:
                self._values["remediation_enabled"] = remediation_enabled
            if resources_clean_up is not None:
                self._values["resources_clean_up"] = resources_clean_up
            if waf_config is not None:
                self._values["waf_config"] = waf_config

        @builtins.property
        def remediation_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
            '''Controls automatic remediation of non-compliant resources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networksecuritymanager-policy-policyconfiguration.html#cfn-networksecuritymanager-policy-policyconfiguration-remediationenabled
            '''
            result = self._values.get("remediation_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], result)

        @builtins.property
        def resources_clean_up(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
            '''Controls automatic cleanup of unused resources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networksecuritymanager-policy-policyconfiguration.html#cfn-networksecuritymanager-policy-policyconfiguration-resourcescleanup
            '''
            result = self._values.get("resources_clean_up")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], result)

        @builtins.property
        def waf_config(
            self,
        ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnPolicy.WafConfigProperty"]]:
            '''WAF-specific policy settings.

            Populated only for WAF firewall type policies.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networksecuritymanager-policy-policyconfiguration.html#cfn-networksecuritymanager-policy-policyconfiguration-wafconfig
            '''
            result = self._values.get("waf_config")
            return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnPolicy.WafConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PolicyConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_networksecuritymanager.CfnPolicy.WafConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "conflict_resolution": "conflictResolution",
            "existing_customer_web_acl_resolution": "existingCustomerWebAclResolution",
        },
    )
    class WafConfigProperty:
        def __init__(
            self,
            *,
            conflict_resolution: builtins.str,
            existing_customer_web_acl_resolution: builtins.str,
        ) -> None:
            '''WAF-specific policy settings.

            Populated only for WAF firewall type policies.

            :param conflict_resolution: Conflict-resolution strategy applied to AWS WAF policies.
            :param existing_customer_web_acl_resolution: Controls how Network Security Manager handles remediation when a resource already has a customer-created WebACL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networksecuritymanager-policy-wafconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_networksecuritymanager as networksecuritymanager
                
                waf_config_property = networksecuritymanager.CfnPolicy.WafConfigProperty(
                    conflict_resolution="conflictResolution",
                    existing_customer_web_acl_resolution="existingCustomerWebAclResolution"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__e9462811bb77e5368b20d6847fd3b99806812e7301d7f6f435c3011ad7ce461c)
                check_type(argname="argument conflict_resolution", value=conflict_resolution, expected_type=type_hints["conflict_resolution"])
                check_type(argname="argument existing_customer_web_acl_resolution", value=existing_customer_web_acl_resolution, expected_type=type_hints["existing_customer_web_acl_resolution"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "conflict_resolution": conflict_resolution,
                "existing_customer_web_acl_resolution": existing_customer_web_acl_resolution,
            }

        @builtins.property
        def conflict_resolution(self) -> builtins.str:
            '''Conflict-resolution strategy applied to AWS WAF policies.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networksecuritymanager-policy-wafconfig.html#cfn-networksecuritymanager-policy-wafconfig-conflictresolution
            '''
            result = self._values.get("conflict_resolution")
            assert result is not None, "Required property 'conflict_resolution' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def existing_customer_web_acl_resolution(self) -> builtins.str:
            '''Controls how Network Security Manager handles remediation when a resource already has a customer-created WebACL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networksecuritymanager-policy-wafconfig.html#cfn-networksecuritymanager-policy-wafconfig-existingcustomerwebaclresolution
            '''
            result = self._values.get("existing_customer_web_acl_resolution")
            assert result is not None, "Required property 'existing_customer_web_acl_resolution' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WafConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_networksecuritymanager.CfnPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "firewall_type": "firewallType",
        "policy_configuration": "policyConfiguration",
        "policy_name": "policyName",
        "priority": "priority",
        "associated_template_and_rule_list": "associatedTemplateAndRuleList",
        "policy_description": "policyDescription",
        "tags": "tags",
    },
)
class CfnPolicyProps:
    def __init__(
        self,
        *,
        firewall_type: builtins.str,
        policy_configuration: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnPolicy.PolicyConfigurationProperty", typing.Dict[builtins.str, typing.Any]]],
        policy_name: builtins.str,
        priority: jsii.Number,
        associated_template_and_rule_list: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Sequence[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnPolicy.AssociatedTemplateAndRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        policy_description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnPolicy``.

        :param firewall_type: The type of firewall.
        :param policy_configuration: Configuration settings for policy behavior.
        :param policy_name: The name of the policy.
        :param priority: The priority of the policy.
        :param associated_template_and_rule_list: List of templates and rules associated with this policy.
        :param policy_description: A description of the policy.
        :param tags: The tags associated with the policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-policy.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_networksecuritymanager as networksecuritymanager
            
            cfn_policy_props = networksecuritymanager.CfnPolicyProps(
                firewall_type="firewallType",
                policy_configuration=networksecuritymanager.CfnPolicy.PolicyConfigurationProperty(
                    remediation_enabled=False,
                    resources_clean_up=False,
                    waf_config=networksecuritymanager.CfnPolicy.WafConfigProperty(
                        conflict_resolution="conflictResolution",
                        existing_customer_web_acl_resolution="existingCustomerWebAclResolution"
                    )
                ),
                policy_name="policyName",
                priority=123,
            
                # the properties below are optional
                associated_template_and_rule_list=[networksecuritymanager.CfnPolicy.AssociatedTemplateAndRuleProperty(
                    rule_arn="ruleArn",
                    template_arn="templateArn"
                )],
                policy_description="policyDescription",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__95fd24ed0adaea48b3049483dea0605c0cf80984e5a6644c8acad0107be40dab)
            check_type(argname="argument firewall_type", value=firewall_type, expected_type=type_hints["firewall_type"])
            check_type(argname="argument policy_configuration", value=policy_configuration, expected_type=type_hints["policy_configuration"])
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument associated_template_and_rule_list", value=associated_template_and_rule_list, expected_type=type_hints["associated_template_and_rule_list"])
            check_type(argname="argument policy_description", value=policy_description, expected_type=type_hints["policy_description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "firewall_type": firewall_type,
            "policy_configuration": policy_configuration,
            "policy_name": policy_name,
            "priority": priority,
        }
        if associated_template_and_rule_list is not None:
            self._values["associated_template_and_rule_list"] = associated_template_and_rule_list
        if policy_description is not None:
            self._values["policy_description"] = policy_description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def firewall_type(self) -> builtins.str:
        '''The type of firewall.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-policy.html#cfn-networksecuritymanager-policy-firewalltype
        '''
        result = self._values.get("firewall_type")
        assert result is not None, "Required property 'firewall_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy_configuration(
        self,
    ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnPolicy.PolicyConfigurationProperty"]:
        '''Configuration settings for policy behavior.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-policy.html#cfn-networksecuritymanager-policy-policyconfiguration
        '''
        result = self._values.get("policy_configuration")
        assert result is not None, "Required property 'policy_configuration' is missing"
        return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnPolicy.PolicyConfigurationProperty"], result)

    @builtins.property
    def policy_name(self) -> builtins.str:
        '''The name of the policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-policy.html#cfn-networksecuritymanager-policy-policyname
        '''
        result = self._values.get("policy_name")
        assert result is not None, "Required property 'policy_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def priority(self) -> jsii.Number:
        '''The priority of the policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-policy.html#cfn-networksecuritymanager-policy-priority
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def associated_template_and_rule_list(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnPolicy.AssociatedTemplateAndRuleProperty"]]]]:
        '''List of templates and rules associated with this policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-policy.html#cfn-networksecuritymanager-policy-associatedtemplateandrulelist
        '''
        result = self._values.get("associated_template_and_rule_list")
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnPolicy.AssociatedTemplateAndRuleProperty"]]]], result)

    @builtins.property
    def policy_description(self) -> typing.Optional[builtins.str]:
        '''A description of the policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-policy.html#cfn-networksecuritymanager-policy-policydescription
        '''
        result = self._values.get("policy_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''The tags associated with the policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-policy.html#cfn-networksecuritymanager-policy-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_networksecuritymanager_a06671e9.IRuleRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnRule(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_networksecuritymanager.CfnRule",
):
    '''Resource Type definition for AWS::NetworkSecurityManager::Rule.

    Creates and manages a Network Security Manager rule.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-rule.html
    :cloudformationResource: AWS::NetworkSecurityManager::Rule
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_networksecuritymanager as networksecuritymanager
        
        cfn_rule = networksecuritymanager.CfnRule(self, "MyCfnRule",
            rule_name="ruleName",
        
            # the properties below are optional
            configuration="configuration",
            firewall_type="firewallType",
            rule_description="ruleDescription",
            rule_type="ruleType",
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
        rule_name: builtins.str,
        configuration: typing.Optional[builtins.str] = None,
        firewall_type: typing.Optional[builtins.str] = None,
        rule_description: typing.Optional[builtins.str] = None,
        rule_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::NetworkSecurityManager::Rule``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param rule_name: The name of the rule.
        :param configuration: The rule configuration as a JSON string.
        :param firewall_type: The type of firewall for this rule.
        :param rule_description: A description of the rule.
        :param rule_type: The type of rule.
        :param tags: The tags associated with the rule.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__2716c7d1e1667ee98281c864647c62bedb2a3856518c5b49b4b64d2b03117bb3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRuleProps(
            rule_name=rule_name,
            configuration=configuration,
            firewall_type=firewall_type,
            rule_description=rule_description,
            rule_type=rule_type,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForRule")
    @builtins.classmethod
    def arn_for_rule(
        cls,
        resource: "_aws_networksecuritymanager_a06671e9.IRuleRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__968497cacd3bfcce9914185b71a22f6aeac91cba762f60aef64a3e8678bad0b0)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForRule", [resource]))

    @jsii.member(jsii_name="isCfnRule")
    @builtins.classmethod
    def is_cfn_rule(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnRule.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__05d810eba079d645808d4f22c1c81561467660a11101cf122e8c15605c787b93)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnRule", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__73bf706e6d76e5428c3c75a15b1eda84c5967f81ab730e4b2f06aa60dad424cf)
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
            type_hints = cached_type_hints(_typecheckingstub__50747cd301706f253311f65d580d9414c3b4a6eb12812cac86f2387e527335c6)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    @builtins.classmethod
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrRuleArn")
    def attr_rule_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the rule.

        :cloudformationAttribute: RuleArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRuleArn"))

    @builtins.property
    @jsii.member(jsii_name="attrRuleId")
    def attr_rule_id(self) -> builtins.str:
        '''The unique identifier of the rule.

        :cloudformationAttribute: RuleId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRuleId"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The status of the rule.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdatedAt")
    def attr_updated_at(self) -> builtins.str:
        '''An ISO 8601 timestamp indicating when the rule was last modified.

        :cloudformationAttribute: UpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrVersion")
    def attr_version(self) -> builtins.str:
        '''The version number of the rule.

        :cloudformationAttribute: Version
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVersion"))

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
    @jsii.member(jsii_name="ruleRef")
    def rule_ref(self) -> "_aws_networksecuritymanager_a06671e9.RuleReference":
        '''A reference to a Rule resource.'''
        return typing.cast("_aws_networksecuritymanager_a06671e9.RuleReference", jsii.get(self, "ruleRef"))

    @builtins.property
    @jsii.member(jsii_name="ruleName")
    def rule_name(self) -> builtins.str:
        '''The name of the rule.'''
        return typing.cast(builtins.str, jsii.get(self, "ruleName"))

    @rule_name.setter
    def rule_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c5bc020521222a5c1bfda6525d9478e8e64e9707acfbd4444ad3a651f6c79eed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleName", value)

    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(self) -> typing.Optional[builtins.str]:
        '''The rule configuration as a JSON string.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "configuration"))

    @configuration.setter
    def configuration(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d323b436fd9bf671018c23056e19303c59a72ba02490533874d6d16ce476a081)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configuration", value)

    @builtins.property
    @jsii.member(jsii_name="firewallType")
    def firewall_type(self) -> typing.Optional[builtins.str]:
        '''The type of firewall for this rule.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firewallType"))

    @firewall_type.setter
    def firewall_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__2dee95fc3c8f91d6e887a537403721e63e95c0cf5b83abb23aa94ede31adf854)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firewallType", value)

    @builtins.property
    @jsii.member(jsii_name="ruleDescription")
    def rule_description(self) -> typing.Optional[builtins.str]:
        '''A description of the rule.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleDescription"))

    @rule_description.setter
    def rule_description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c920a9da597c2ecf6b87408f27d7bc8c5191b52e03956f1e30e7f58fb605f2f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleDescription", value)

    @builtins.property
    @jsii.member(jsii_name="ruleType")
    def rule_type(self) -> typing.Optional[builtins.str]:
        '''The type of rule.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleType"))

    @rule_type.setter
    def rule_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__948f67cd8b5aff3074e2a11607ff71cfcc7e3d6e797089711b815b7c7bfd7d56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleType", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''The tags associated with the rule.'''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c73d645bfdfd294e1df04bcfabe18c5a155ffcf6c301bb3f15a63422896edbcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_networksecuritymanager.CfnRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "rule_name": "ruleName",
        "configuration": "configuration",
        "firewall_type": "firewallType",
        "rule_description": "ruleDescription",
        "rule_type": "ruleType",
        "tags": "tags",
    },
)
class CfnRuleProps:
    def __init__(
        self,
        *,
        rule_name: builtins.str,
        configuration: typing.Optional[builtins.str] = None,
        firewall_type: typing.Optional[builtins.str] = None,
        rule_description: typing.Optional[builtins.str] = None,
        rule_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnRule``.

        :param rule_name: The name of the rule.
        :param configuration: The rule configuration as a JSON string.
        :param firewall_type: The type of firewall for this rule.
        :param rule_description: A description of the rule.
        :param rule_type: The type of rule.
        :param tags: The tags associated with the rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-rule.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_networksecuritymanager as networksecuritymanager
            
            cfn_rule_props = networksecuritymanager.CfnRuleProps(
                rule_name="ruleName",
            
                # the properties below are optional
                configuration="configuration",
                firewall_type="firewallType",
                rule_description="ruleDescription",
                rule_type="ruleType",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__38ab3ccfcbc66c618c0bd8b626a1750feb6c7069578175566e38016e733d9789)
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument firewall_type", value=firewall_type, expected_type=type_hints["firewall_type"])
            check_type(argname="argument rule_description", value=rule_description, expected_type=type_hints["rule_description"])
            check_type(argname="argument rule_type", value=rule_type, expected_type=type_hints["rule_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rule_name": rule_name,
        }
        if configuration is not None:
            self._values["configuration"] = configuration
        if firewall_type is not None:
            self._values["firewall_type"] = firewall_type
        if rule_description is not None:
            self._values["rule_description"] = rule_description
        if rule_type is not None:
            self._values["rule_type"] = rule_type
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def rule_name(self) -> builtins.str:
        '''The name of the rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-rule.html#cfn-networksecuritymanager-rule-rulename
        '''
        result = self._values.get("rule_name")
        assert result is not None, "Required property 'rule_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def configuration(self) -> typing.Optional[builtins.str]:
        '''The rule configuration as a JSON string.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-rule.html#cfn-networksecuritymanager-rule-configuration
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firewall_type(self) -> typing.Optional[builtins.str]:
        '''The type of firewall for this rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-rule.html#cfn-networksecuritymanager-rule-firewalltype
        '''
        result = self._values.get("firewall_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_description(self) -> typing.Optional[builtins.str]:
        '''A description of the rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-rule.html#cfn-networksecuritymanager-rule-ruledescription
        '''
        result = self._values.get("rule_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_type(self) -> typing.Optional[builtins.str]:
        '''The type of rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-rule.html#cfn-networksecuritymanager-rule-ruletype
        '''
        result = self._values.get("rule_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''The tags associated with the rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-rule.html#cfn-networksecuritymanager-rule-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_networksecuritymanager_a06671e9.IScopeRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnScope(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_networksecuritymanager.CfnScope",
):
    '''Resource Type definition for AWS::NetworkSecurityManager::Scope.

    Creates and manages a Network Security Manager scope.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-scope.html
    :cloudformationResource: AWS::NetworkSecurityManager::Scope
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_networksecuritymanager as networksecuritymanager
        
        cfn_scope = networksecuritymanager.CfnScope(self, "MyCfnScope",
            scope_name="scopeName",
        
            # the properties below are optional
            scope_configuration="scopeConfiguration",
            scope_description="scopeDescription",
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
        scope_name: builtins.str,
        scope_configuration: typing.Optional[builtins.str] = None,
        scope_description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::NetworkSecurityManager::Scope``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param scope_name: The name of the scope.
        :param scope_configuration: The scope configuration as a JSON string.
        :param scope_description: A description of the scope.
        :param tags: The tags associated with the scope.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6ff7bb85df05bd1b20a1ba7b9a465f9472332e6d25fbb133ba336f35b8825e55)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnScopeProps(
            scope_name=scope_name,
            scope_configuration=scope_configuration,
            scope_description=scope_description,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForScope")
    @builtins.classmethod
    def arn_for_scope(
        cls,
        resource: "_aws_networksecuritymanager_a06671e9.IScopeRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__31d9de14da44a82e409492351f9aa60ffdc92347568e428989f2a1ea6c199e9f)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForScope", [resource]))

    @jsii.member(jsii_name="isCfnScope")
    @builtins.classmethod
    def is_cfn_scope(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnScope.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__15580df2a43c40cf612f27e7d91c01a77896c3e299fd3110e9492612d9ba8258)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnScope", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d00c9339a4f4728adbc4bd35dd1eee92d4c53a899be282066fa4e9cf82f191a4)
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
            type_hints = cached_type_hints(_typecheckingstub__a20d894a78d83a296727b143ba17cf342f55da62ac0903093d79bf43070852b5)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    @builtins.classmethod
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrScopeArn")
    def attr_scope_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the scope.

        :cloudformationAttribute: ScopeArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrScopeArn"))

    @builtins.property
    @jsii.member(jsii_name="attrScopeId")
    def attr_scope_id(self) -> builtins.str:
        '''The unique identifier of the scope.

        :cloudformationAttribute: ScopeId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrScopeId"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The status of the scope.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdatedAt")
    def attr_updated_at(self) -> builtins.str:
        '''An ISO 8601 timestamp indicating when the scope was last modified.

        :cloudformationAttribute: UpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrVersion")
    def attr_version(self) -> builtins.str:
        '''The version number of the scope.

        :cloudformationAttribute: Version
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVersion"))

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
    @jsii.member(jsii_name="scopeRef")
    def scope_ref(self) -> "_aws_networksecuritymanager_a06671e9.ScopeReference":
        '''A reference to a Scope resource.'''
        return typing.cast("_aws_networksecuritymanager_a06671e9.ScopeReference", jsii.get(self, "scopeRef"))

    @builtins.property
    @jsii.member(jsii_name="scopeName")
    def scope_name(self) -> builtins.str:
        '''The name of the scope.'''
        return typing.cast(builtins.str, jsii.get(self, "scopeName"))

    @scope_name.setter
    def scope_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__7a5c321d572293b3b2a7c44ab17a1578b1d6052ae7506a96abb08537af6193c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopeName", value)

    @builtins.property
    @jsii.member(jsii_name="scopeConfiguration")
    def scope_configuration(self) -> typing.Optional[builtins.str]:
        '''The scope configuration as a JSON string.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeConfiguration"))

    @scope_configuration.setter
    def scope_configuration(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a2243f1477c8466a10a54a8ed6fbb01af21b835af3f5d8e82d1bca969d54cc6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopeConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="scopeDescription")
    def scope_description(self) -> typing.Optional[builtins.str]:
        '''A description of the scope.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeDescription"))

    @scope_description.setter
    def scope_description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__04e59f1583d51cf224b47084e3f1a795e053f50c8cc5ea498b39ebc519f97baf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopeDescription", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''The tags associated with the scope.'''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__fd451be1a7a080c7556ac3b33ed96b676f841f386c8d2dc1c93313b979d6db97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_networksecuritymanager.CfnScopeProps",
    jsii_struct_bases=[],
    name_mapping={
        "scope_name": "scopeName",
        "scope_configuration": "scopeConfiguration",
        "scope_description": "scopeDescription",
        "tags": "tags",
    },
)
class CfnScopeProps:
    def __init__(
        self,
        *,
        scope_name: builtins.str,
        scope_configuration: typing.Optional[builtins.str] = None,
        scope_description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnScope``.

        :param scope_name: The name of the scope.
        :param scope_configuration: The scope configuration as a JSON string.
        :param scope_description: A description of the scope.
        :param tags: The tags associated with the scope.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-scope.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_networksecuritymanager as networksecuritymanager
            
            cfn_scope_props = networksecuritymanager.CfnScopeProps(
                scope_name="scopeName",
            
                # the properties below are optional
                scope_configuration="scopeConfiguration",
                scope_description="scopeDescription",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__9a7ef147523135464ed18edd8315a6add25a41f78c6e60685bd3c2de15e44d63)
            check_type(argname="argument scope_name", value=scope_name, expected_type=type_hints["scope_name"])
            check_type(argname="argument scope_configuration", value=scope_configuration, expected_type=type_hints["scope_configuration"])
            check_type(argname="argument scope_description", value=scope_description, expected_type=type_hints["scope_description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "scope_name": scope_name,
        }
        if scope_configuration is not None:
            self._values["scope_configuration"] = scope_configuration
        if scope_description is not None:
            self._values["scope_description"] = scope_description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def scope_name(self) -> builtins.str:
        '''The name of the scope.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-scope.html#cfn-networksecuritymanager-scope-scopename
        '''
        result = self._values.get("scope_name")
        assert result is not None, "Required property 'scope_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scope_configuration(self) -> typing.Optional[builtins.str]:
        '''The scope configuration as a JSON string.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-scope.html#cfn-networksecuritymanager-scope-scopeconfiguration
        '''
        result = self._values.get("scope_configuration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scope_description(self) -> typing.Optional[builtins.str]:
        '''A description of the scope.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-scope.html#cfn-networksecuritymanager-scope-scopedescription
        '''
        result = self._values.get("scope_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''The tags associated with the scope.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-scope.html#cfn-networksecuritymanager-scope-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnScopeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_networksecuritymanager_a06671e9.ITemplateRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnTemplate(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_networksecuritymanager.CfnTemplate",
):
    '''Resource Type definition for AWS::NetworkSecurityManager::Template.

    Creates and manages a Network Security Manager template.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-template.html
    :cloudformationResource: AWS::NetworkSecurityManager::Template
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_networksecuritymanager as networksecuritymanager
        
        cfn_template = networksecuritymanager.CfnTemplate(self, "MyCfnTemplate",
            template_name="templateName",
        
            # the properties below are optional
            associated_rule_list=[networksecuritymanager.CfnTemplate.AssociatedRuleProperty(
                rule_arn="ruleArn"
            )],
            firewall_type="firewallType",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            template_description="templateDescription"
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        template_name: builtins.str,
        associated_rule_list: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Sequence[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnTemplate.AssociatedRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        firewall_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
        template_description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::NetworkSecurityManager::Template``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param template_name: The name of the template.
        :param associated_rule_list: List of rules associated with this template.
        :param firewall_type: The type of firewall.
        :param tags: The tags associated with the template.
        :param template_description: A description of the template.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__0c45b73e844b488d41ca7273ff603c14fcfad688de835808f99dd6483f815b48)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnTemplateProps(
            template_name=template_name,
            associated_rule_list=associated_rule_list,
            firewall_type=firewall_type,
            tags=tags,
            template_description=template_description,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForTemplate")
    @builtins.classmethod
    def arn_for_template(
        cls,
        resource: "_aws_networksecuritymanager_a06671e9.ITemplateRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e0828644ab8c0f2604ce8d6398cc2710eec23d33d8ad8ae653cca846d8c564b5)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForTemplate", [resource]))

    @jsii.member(jsii_name="isCfnTemplate")
    @builtins.classmethod
    def is_cfn_template(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnTemplate.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b5acb8f409ef1efc522b27cd344c8f16f8838363f0976cb420b2697b509051db)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnTemplate", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__11a3509b944d93c31fd0d81fe6885405f9a9cc3b49daea7473faf6c561a590e4)
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
            type_hints = cached_type_hints(_typecheckingstub__26d479a23512531247e99b9e25dee9bad80992ec81e4393e378980f4b5d836ca)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    @builtins.classmethod
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The status of the template.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrTemplateArn")
    def attr_template_arn(self) -> builtins.str:
        '''The ARN of the template.

        :cloudformationAttribute: TemplateArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrTemplateArn"))

    @builtins.property
    @jsii.member(jsii_name="attrTemplateId")
    def attr_template_id(self) -> builtins.str:
        '''The unique identifier of the template.

        :cloudformationAttribute: TemplateId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrTemplateId"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdatedAt")
    def attr_updated_at(self) -> builtins.str:
        '''An ISO 8601 timestamp indicating when the template was last modified.

        :cloudformationAttribute: UpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrVersion")
    def attr_version(self) -> builtins.str:
        '''The version number.

        :cloudformationAttribute: Version
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVersion"))

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
    @jsii.member(jsii_name="templateRef")
    def template_ref(self) -> "_aws_networksecuritymanager_a06671e9.TemplateReference":
        '''A reference to a Template resource.'''
        return typing.cast("_aws_networksecuritymanager_a06671e9.TemplateReference", jsii.get(self, "templateRef"))

    @builtins.property
    @jsii.member(jsii_name="templateName")
    def template_name(self) -> builtins.str:
        '''The name of the template.'''
        return typing.cast(builtins.str, jsii.get(self, "templateName"))

    @template_name.setter
    def template_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__fc678d067e5f0af8c7519abc790e7201d87b2cc1fa9f6db6ed8cd2e915ba9ba0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateName", value)

    @builtins.property
    @jsii.member(jsii_name="associatedRuleList")
    def associated_rule_list(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnTemplate.AssociatedRuleProperty"]]]]:
        '''List of rules associated with this template.'''
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnTemplate.AssociatedRuleProperty"]]]], jsii.get(self, "associatedRuleList"))

    @associated_rule_list.setter
    def associated_rule_list(
        self,
        value: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnTemplate.AssociatedRuleProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3a96894b91813f8ca08a0d30b91c940aa34db5ecb1ad92334d215ae65bc7b7a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "associatedRuleList", value)

    @builtins.property
    @jsii.member(jsii_name="firewallType")
    def firewall_type(self) -> typing.Optional[builtins.str]:
        '''The type of firewall.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firewallType"))

    @firewall_type.setter
    def firewall_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__211cdee9376d35dc1019eef01550d190f1cd674fb9207893006f1de36ef5f600)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firewallType", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''The tags associated with the template.'''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6c7c0f4368f756739ae05dcb501e7d5e7c134f144a71caca9bf13851125f6d64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="templateDescription")
    def template_description(self) -> typing.Optional[builtins.str]:
        '''A description of the template.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateDescription"))

    @template_description.setter
    def template_description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a40afd00719dc578f1db0479377e93548e49eb7a41df547f02c99ff0410595a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateDescription", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_networksecuritymanager.CfnTemplate.AssociatedRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"rule_arn": "ruleArn"},
    )
    class AssociatedRuleProperty:
        def __init__(self, *, rule_arn: builtins.str) -> None:
            '''An association between a template and a rule.

            :param rule_arn: ARN of the associated rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networksecuritymanager-template-associatedrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_networksecuritymanager as networksecuritymanager
                
                associated_rule_property = networksecuritymanager.CfnTemplate.AssociatedRuleProperty(
                    rule_arn="ruleArn"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__549726b5c72d5be6197f09a158c14ae1cb4140a399b3743b572135fafc58743a)
                check_type(argname="argument rule_arn", value=rule_arn, expected_type=type_hints["rule_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "rule_arn": rule_arn,
            }

        @builtins.property
        def rule_arn(self) -> builtins.str:
            '''ARN of the associated rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networksecuritymanager-template-associatedrule.html#cfn-networksecuritymanager-template-associatedrule-rulearn
            '''
            result = self._values.get("rule_arn")
            assert result is not None, "Required property 'rule_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssociatedRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_networksecuritymanager.CfnTemplateProps",
    jsii_struct_bases=[],
    name_mapping={
        "template_name": "templateName",
        "associated_rule_list": "associatedRuleList",
        "firewall_type": "firewallType",
        "tags": "tags",
        "template_description": "templateDescription",
    },
)
class CfnTemplateProps:
    def __init__(
        self,
        *,
        template_name: builtins.str,
        associated_rule_list: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Sequence[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnTemplate.AssociatedRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        firewall_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
        template_description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnTemplate``.

        :param template_name: The name of the template.
        :param associated_rule_list: List of rules associated with this template.
        :param firewall_type: The type of firewall.
        :param tags: The tags associated with the template.
        :param template_description: A description of the template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-template.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_networksecuritymanager as networksecuritymanager
            
            cfn_template_props = networksecuritymanager.CfnTemplateProps(
                template_name="templateName",
            
                # the properties below are optional
                associated_rule_list=[networksecuritymanager.CfnTemplate.AssociatedRuleProperty(
                    rule_arn="ruleArn"
                )],
                firewall_type="firewallType",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                template_description="templateDescription"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__2776f80fbca707335f11ecf6f07155e86a0c3ad72cb62047b94710724f9ec69f)
            check_type(argname="argument template_name", value=template_name, expected_type=type_hints["template_name"])
            check_type(argname="argument associated_rule_list", value=associated_rule_list, expected_type=type_hints["associated_rule_list"])
            check_type(argname="argument firewall_type", value=firewall_type, expected_type=type_hints["firewall_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument template_description", value=template_description, expected_type=type_hints["template_description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "template_name": template_name,
        }
        if associated_rule_list is not None:
            self._values["associated_rule_list"] = associated_rule_list
        if firewall_type is not None:
            self._values["firewall_type"] = firewall_type
        if tags is not None:
            self._values["tags"] = tags
        if template_description is not None:
            self._values["template_description"] = template_description

    @builtins.property
    def template_name(self) -> builtins.str:
        '''The name of the template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-template.html#cfn-networksecuritymanager-template-templatename
        '''
        result = self._values.get("template_name")
        assert result is not None, "Required property 'template_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def associated_rule_list(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnTemplate.AssociatedRuleProperty"]]]]:
        '''List of rules associated with this template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-template.html#cfn-networksecuritymanager-template-associatedrulelist
        '''
        result = self._values.get("associated_rule_list")
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnTemplate.AssociatedRuleProperty"]]]], result)

    @builtins.property
    def firewall_type(self) -> typing.Optional[builtins.str]:
        '''The type of firewall.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-template.html#cfn-networksecuritymanager-template-firewalltype
        '''
        result = self._values.get("firewall_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''The tags associated with the template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-template.html#cfn-networksecuritymanager-template-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    @builtins.property
    def template_description(self) -> typing.Optional[builtins.str]:
        '''A description of the template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networksecuritymanager-template.html#cfn-networksecuritymanager-template-templatedescription
        '''
        result = self._values.get("template_description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTemplateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnDeployment",
    "CfnDeploymentProps",
    "CfnPolicy",
    "CfnPolicyProps",
    "CfnRule",
    "CfnRuleProps",
    "CfnScope",
    "CfnScopeProps",
    "CfnTemplate",
    "CfnTemplateProps",
]

publication.publish()

def _typecheckingstub__3f39c840c5df17b618e9ab668273d1bd2d8972453214cbe27e1af6e7fbb8f9bb(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    deployment_name: builtins.str,
    associated_policy_list: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Sequence[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnDeployment.AssociatedPolicyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    associated_scope_list: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Sequence[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnDeployment.AssociatedScopeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    deployment_configuration: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnDeployment.DeploymentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    deployment_description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb9100d3f5ecd518543c9d7b93315dde93e21ae8404648129d590e480c750995(
    resource: _aws_networksecuritymanager_a06671e9.IDeploymentRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d691846db836794178f9fdaf83029f3da5a6788b39e33ca4a528a7c7fbc94ed3(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a18c344f16e32e6fc04a52409866551333f2aae35e5fdb02fe8698711a0a930(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49514bf67a86289b947047b4446045f46656df1034b4d9170cd84bec275fc852(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5c0ceaaf5ade36cecdae6b388f0f5c91426589cd41c0c3f20404bc2afc55022(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4df5ae837ad9251c88e4e7f89160d3a9790f05e0ac86ae1f6748b4456affd9b4(
    value: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.List[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnDeployment.AssociatedPolicyProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__502611450f2185f1516eac85bb373d188a6d7503e22974b812058d51af2a61fa(
    value: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.List[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnDeployment.AssociatedScopeProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8583c77943e2827a47d4b8fbf4a9a60dfe18af98963360ea172a35248acaa61(
    value: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnDeployment.DeploymentConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d46f859371b9b0fc92538e0eb745d6bee7f3d1a0a3da83c19f68f3e0628e594(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e95b757f6b39d96c49bd92fc69c053bf092805e3bb9adc257a23ad77288655f0(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__306f7d4eae62b640a3ba14c5adc2e413887bb96f70feb8796939ef73d8dfd75f(
    *,
    policy_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a584b4b537b5cb33cf1acf514ac44cd26e97863965f05c7005638fd73417392d(
    *,
    scope_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__154eba5468d601ce94ae486b9a13246a28745f5bb16fe814194910e16ef2eca0(
    *,
    enable_cross_account_visibility: typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4da69db68df96fa3214f35b58941f59f95df427e723ef1e2e8933c6e744114cd(
    *,
    deployment_name: builtins.str,
    associated_policy_list: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Sequence[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnDeployment.AssociatedPolicyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    associated_scope_list: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Sequence[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnDeployment.AssociatedScopeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    deployment_configuration: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnDeployment.DeploymentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    deployment_description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e455d8af87a638174f344d9a93d7603b20ba5eb09596bb904ec2fd74cc5ce3d3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    firewall_type: builtins.str,
    policy_configuration: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnPolicy.PolicyConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
    policy_name: builtins.str,
    priority: jsii.Number,
    associated_template_and_rule_list: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Sequence[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnPolicy.AssociatedTemplateAndRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    policy_description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b095f3e022eeefa5110592d7571739da7549a8be5f0b8f265c1d56889317f795(
    resource: _aws_networksecuritymanager_a06671e9.IPolicyRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81843608d40596bdfec2ed93e7c070999c60ed3e2284da5ff4b6c29cc53a6c21(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6081c17a0ed16f1abac4add790966f09c5b4b231547e20dd99297f1697845f8c(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__556b5797c35eb8b15df7dc91407356bbde61e40e66a67ad5e88c22a5f93e6962(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3689b76c694f1cbcb15847ed12fcc71fc4de945907b84ec480460ddd342006b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85fe1123c733f774b5881dc32e28c60085600f5f2e10cb5b3f86b0fff3a71536(
    value: typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnPolicy.PolicyConfigurationProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d056ce533e7118a721b0fd7f581ee6faad5d0ab568d8a8407a8a3ab7c926ad8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af51aaf48b615b9d972230f14ae3e9998750105fde8b6cf6a663950a85eea6c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d6d0649064408e9f07375e685a9c0f377b816a338cedfde7d5ad3ba47b631dc(
    value: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.List[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnPolicy.AssociatedTemplateAndRuleProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__146edd331f95c9894b839e912f3c5e3c9e5db99b266e9f6c120c8877f57a54d3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__317966e71a07d6489f5a99a868ec2bf13dae386c29fc0f76d96a686f90b0de86(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22f88dff79c8071f59256fe33147daa14194ec6b52ee1ee0552d8d7b1587e6f0(
    *,
    rule_arn: typing.Optional[builtins.str] = None,
    template_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__759ff63568a360d5f4dd2fd4ebfa70ddb6c3ad174bf1a984add0075380b24d7a(
    *,
    remediation_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    resources_clean_up: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    waf_config: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnPolicy.WafConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9462811bb77e5368b20d6847fd3b99806812e7301d7f6f435c3011ad7ce461c(
    *,
    conflict_resolution: builtins.str,
    existing_customer_web_acl_resolution: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95fd24ed0adaea48b3049483dea0605c0cf80984e5a6644c8acad0107be40dab(
    *,
    firewall_type: builtins.str,
    policy_configuration: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnPolicy.PolicyConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
    policy_name: builtins.str,
    priority: jsii.Number,
    associated_template_and_rule_list: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Sequence[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnPolicy.AssociatedTemplateAndRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    policy_description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2716c7d1e1667ee98281c864647c62bedb2a3856518c5b49b4b64d2b03117bb3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    rule_name: builtins.str,
    configuration: typing.Optional[builtins.str] = None,
    firewall_type: typing.Optional[builtins.str] = None,
    rule_description: typing.Optional[builtins.str] = None,
    rule_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__968497cacd3bfcce9914185b71a22f6aeac91cba762f60aef64a3e8678bad0b0(
    resource: _aws_networksecuritymanager_a06671e9.IRuleRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05d810eba079d645808d4f22c1c81561467660a11101cf122e8c15605c787b93(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73bf706e6d76e5428c3c75a15b1eda84c5967f81ab730e4b2f06aa60dad424cf(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50747cd301706f253311f65d580d9414c3b4a6eb12812cac86f2387e527335c6(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5bc020521222a5c1bfda6525d9478e8e64e9707acfbd4444ad3a651f6c79eed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d323b436fd9bf671018c23056e19303c59a72ba02490533874d6d16ce476a081(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dee95fc3c8f91d6e887a537403721e63e95c0cf5b83abb23aa94ede31adf854(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c920a9da597c2ecf6b87408f27d7bc8c5191b52e03956f1e30e7f58fb605f2f2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__948f67cd8b5aff3074e2a11607ff71cfcc7e3d6e797089711b815b7c7bfd7d56(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c73d645bfdfd294e1df04bcfabe18c5a155ffcf6c301bb3f15a63422896edbcc(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38ab3ccfcbc66c618c0bd8b626a1750feb6c7069578175566e38016e733d9789(
    *,
    rule_name: builtins.str,
    configuration: typing.Optional[builtins.str] = None,
    firewall_type: typing.Optional[builtins.str] = None,
    rule_description: typing.Optional[builtins.str] = None,
    rule_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ff7bb85df05bd1b20a1ba7b9a465f9472332e6d25fbb133ba336f35b8825e55(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    scope_name: builtins.str,
    scope_configuration: typing.Optional[builtins.str] = None,
    scope_description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31d9de14da44a82e409492351f9aa60ffdc92347568e428989f2a1ea6c199e9f(
    resource: _aws_networksecuritymanager_a06671e9.IScopeRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15580df2a43c40cf612f27e7d91c01a77896c3e299fd3110e9492612d9ba8258(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d00c9339a4f4728adbc4bd35dd1eee92d4c53a899be282066fa4e9cf82f191a4(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a20d894a78d83a296727b143ba17cf342f55da62ac0903093d79bf43070852b5(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a5c321d572293b3b2a7c44ab17a1578b1d6052ae7506a96abb08537af6193c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2243f1477c8466a10a54a8ed6fbb01af21b835af3f5d8e82d1bca969d54cc6a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04e59f1583d51cf224b47084e3f1a795e053f50c8cc5ea498b39ebc519f97baf(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd451be1a7a080c7556ac3b33ed96b676f841f386c8d2dc1c93313b979d6db97(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a7ef147523135464ed18edd8315a6add25a41f78c6e60685bd3c2de15e44d63(
    *,
    scope_name: builtins.str,
    scope_configuration: typing.Optional[builtins.str] = None,
    scope_description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c45b73e844b488d41ca7273ff603c14fcfad688de835808f99dd6483f815b48(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    template_name: builtins.str,
    associated_rule_list: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Sequence[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnTemplate.AssociatedRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    firewall_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    template_description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0828644ab8c0f2604ce8d6398cc2710eec23d33d8ad8ae653cca846d8c564b5(
    resource: _aws_networksecuritymanager_a06671e9.ITemplateRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5acb8f409ef1efc522b27cd344c8f16f8838363f0976cb420b2697b509051db(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11a3509b944d93c31fd0d81fe6885405f9a9cc3b49daea7473faf6c561a590e4(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26d479a23512531247e99b9e25dee9bad80992ec81e4393e378980f4b5d836ca(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc678d067e5f0af8c7519abc790e7201d87b2cc1fa9f6db6ed8cd2e915ba9ba0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a96894b91813f8ca08a0d30b91c940aa34db5ecb1ad92334d215ae65bc7b7a6(
    value: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.List[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnTemplate.AssociatedRuleProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__211cdee9376d35dc1019eef01550d190f1cd674fb9207893006f1de36ef5f600(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c7c0f4368f756739ae05dcb501e7d5e7c134f144a71caca9bf13851125f6d64(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a40afd00719dc578f1db0479377e93548e49eb7a41df547f02c99ff0410595a4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__549726b5c72d5be6197f09a158c14ae1cb4140a399b3743b572135fafc58743a(
    *,
    rule_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2776f80fbca707335f11ecf6f07155e86a0c3ad72cb62047b94710724f9ec69f(
    *,
    template_name: builtins.str,
    associated_rule_list: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Sequence[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnTemplate.AssociatedRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    firewall_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    template_description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
