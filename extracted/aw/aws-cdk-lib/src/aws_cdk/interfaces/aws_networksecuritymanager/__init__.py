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


from ..._jsii import *

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

    import aws_cdk.interfaces as _interfaces_8ca7e747
    import constructs as _constructs_77d1e7e8
else:

    _constructs_77d1e7e8 = _LazyImport("constructs")
    _interfaces_8ca7e747 = _LazyImport("aws_cdk.interfaces")


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_networksecuritymanager.DeploymentReference",
    jsii_struct_bases=[],
    name_mapping={"deployment_arn": "deploymentArn"},
)
class DeploymentReference:
    def __init__(self, *, deployment_arn: builtins.str) -> None:
        '''A reference to a Deployment resource.

        :param deployment_arn: The DeploymentArn of the Deployment resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_networksecuritymanager as interfaces_networksecuritymanager
            
            deployment_reference = interfaces_networksecuritymanager.DeploymentReference(
                deployment_arn="deploymentArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__24c6213f84de176ff34df43d0c3ff94f9d83676ebd6ff19ebea93a2216dae4ba)
            check_type(argname="argument deployment_arn", value=deployment_arn, expected_type=type_hints["deployment_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "deployment_arn": deployment_arn,
        }

    @builtins.property
    def deployment_arn(self) -> builtins.str:
        '''The DeploymentArn of the Deployment resource.'''
        result = self._values.get("deployment_arn")
        assert result is not None, "Required property 'deployment_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeploymentReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(
    jsii_type="aws-cdk-lib.interfaces.aws_networksecuritymanager.IDeploymentRef"
)
class IDeploymentRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a Deployment.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="deploymentRef")
    def deployment_ref(self) -> "DeploymentReference":
        '''(experimental) A reference to a Deployment resource.

        :stability: experimental
        '''
        ...


class _IDeploymentRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a Deployment.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_networksecuritymanager.IDeploymentRef"

    @builtins.property
    @jsii.member(jsii_name="deploymentRef")
    def deployment_ref(self) -> "DeploymentReference":
        '''(experimental) A reference to a Deployment resource.

        :stability: experimental
        '''
        return typing.cast("DeploymentReference", jsii.get(self, "deploymentRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDeploymentRef).__jsii_proxy_class__ = lambda : _IDeploymentRefProxy


@jsii.interface(
    jsii_type="aws-cdk-lib.interfaces.aws_networksecuritymanager.IPolicyRef"
)
class IPolicyRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a Policy.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="policyRef")
    def policy_ref(self) -> "PolicyReference":
        '''(experimental) A reference to a Policy resource.

        :stability: experimental
        '''
        ...


class _IPolicyRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a Policy.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_networksecuritymanager.IPolicyRef"

    @builtins.property
    @jsii.member(jsii_name="policyRef")
    def policy_ref(self) -> "PolicyReference":
        '''(experimental) A reference to a Policy resource.

        :stability: experimental
        '''
        return typing.cast("PolicyReference", jsii.get(self, "policyRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPolicyRef).__jsii_proxy_class__ = lambda : _IPolicyRefProxy


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_networksecuritymanager.IRuleRef")
class IRuleRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a Rule.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="ruleRef")
    def rule_ref(self) -> "RuleReference":
        '''(experimental) A reference to a Rule resource.

        :stability: experimental
        '''
        ...


class _IRuleRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a Rule.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_networksecuritymanager.IRuleRef"

    @builtins.property
    @jsii.member(jsii_name="ruleRef")
    def rule_ref(self) -> "RuleReference":
        '''(experimental) A reference to a Rule resource.

        :stability: experimental
        '''
        return typing.cast("RuleReference", jsii.get(self, "ruleRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRuleRef).__jsii_proxy_class__ = lambda : _IRuleRefProxy


@jsii.interface(
    jsii_type="aws-cdk-lib.interfaces.aws_networksecuritymanager.IScopeRef"
)
class IScopeRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a Scope.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="scopeRef")
    def scope_ref(self) -> "ScopeReference":
        '''(experimental) A reference to a Scope resource.

        :stability: experimental
        '''
        ...


class _IScopeRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a Scope.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_networksecuritymanager.IScopeRef"

    @builtins.property
    @jsii.member(jsii_name="scopeRef")
    def scope_ref(self) -> "ScopeReference":
        '''(experimental) A reference to a Scope resource.

        :stability: experimental
        '''
        return typing.cast("ScopeReference", jsii.get(self, "scopeRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IScopeRef).__jsii_proxy_class__ = lambda : _IScopeRefProxy


@jsii.interface(
    jsii_type="aws-cdk-lib.interfaces.aws_networksecuritymanager.ITemplateRef"
)
class ITemplateRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a Template.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="templateRef")
    def template_ref(self) -> "TemplateReference":
        '''(experimental) A reference to a Template resource.

        :stability: experimental
        '''
        ...


class _ITemplateRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a Template.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_networksecuritymanager.ITemplateRef"

    @builtins.property
    @jsii.member(jsii_name="templateRef")
    def template_ref(self) -> "TemplateReference":
        '''(experimental) A reference to a Template resource.

        :stability: experimental
        '''
        return typing.cast("TemplateReference", jsii.get(self, "templateRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITemplateRef).__jsii_proxy_class__ = lambda : _ITemplateRefProxy


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_networksecuritymanager.PolicyReference",
    jsii_struct_bases=[],
    name_mapping={"policy_arn": "policyArn"},
)
class PolicyReference:
    def __init__(self, *, policy_arn: builtins.str) -> None:
        '''A reference to a Policy resource.

        :param policy_arn: The PolicyArn of the Policy resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_networksecuritymanager as interfaces_networksecuritymanager
            
            policy_reference = interfaces_networksecuritymanager.PolicyReference(
                policy_arn="policyArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__17b7e7a25a5bf94973e9f230377fa887539b3fbec244eec168aeaaae8f5bc088)
            check_type(argname="argument policy_arn", value=policy_arn, expected_type=type_hints["policy_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy_arn": policy_arn,
        }

    @builtins.property
    def policy_arn(self) -> builtins.str:
        '''The PolicyArn of the Policy resource.'''
        result = self._values.get("policy_arn")
        assert result is not None, "Required property 'policy_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolicyReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_networksecuritymanager.RuleReference",
    jsii_struct_bases=[],
    name_mapping={"rule_arn": "ruleArn"},
)
class RuleReference:
    def __init__(self, *, rule_arn: builtins.str) -> None:
        '''A reference to a Rule resource.

        :param rule_arn: The RuleArn of the Rule resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_networksecuritymanager as interfaces_networksecuritymanager
            
            rule_reference = interfaces_networksecuritymanager.RuleReference(
                rule_arn="ruleArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f85f9439db939717ec82680c69f6449d6a04ebb27a368143a9a527d574bbd710)
            check_type(argname="argument rule_arn", value=rule_arn, expected_type=type_hints["rule_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rule_arn": rule_arn,
        }

    @builtins.property
    def rule_arn(self) -> builtins.str:
        '''The RuleArn of the Rule resource.'''
        result = self._values.get("rule_arn")
        assert result is not None, "Required property 'rule_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RuleReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_networksecuritymanager.ScopeReference",
    jsii_struct_bases=[],
    name_mapping={"scope_arn": "scopeArn"},
)
class ScopeReference:
    def __init__(self, *, scope_arn: builtins.str) -> None:
        '''A reference to a Scope resource.

        :param scope_arn: The ScopeArn of the Scope resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_networksecuritymanager as interfaces_networksecuritymanager
            
            scope_reference = interfaces_networksecuritymanager.ScopeReference(
                scope_arn="scopeArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__7b2c857fa029abe7aadce73c4bed17838908126f72fa25e4c65ad8fdcd9c55bb)
            check_type(argname="argument scope_arn", value=scope_arn, expected_type=type_hints["scope_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "scope_arn": scope_arn,
        }

    @builtins.property
    def scope_arn(self) -> builtins.str:
        '''The ScopeArn of the Scope resource.'''
        result = self._values.get("scope_arn")
        assert result is not None, "Required property 'scope_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScopeReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_networksecuritymanager.TemplateReference",
    jsii_struct_bases=[],
    name_mapping={"template_arn": "templateArn"},
)
class TemplateReference:
    def __init__(self, *, template_arn: builtins.str) -> None:
        '''A reference to a Template resource.

        :param template_arn: The TemplateArn of the Template resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_networksecuritymanager as interfaces_networksecuritymanager
            
            template_reference = interfaces_networksecuritymanager.TemplateReference(
                template_arn="templateArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__12450cbae07b20c4f3f4c0e65cd96692f766aca21277513ce5d06c5e9f70a9e1)
            check_type(argname="argument template_arn", value=template_arn, expected_type=type_hints["template_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "template_arn": template_arn,
        }

    @builtins.property
    def template_arn(self) -> builtins.str:
        '''The TemplateArn of the Template resource.'''
        result = self._values.get("template_arn")
        assert result is not None, "Required property 'template_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TemplateReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DeploymentReference",
    "IDeploymentRef",
    "IPolicyRef",
    "IRuleRef",
    "IScopeRef",
    "ITemplateRef",
    "PolicyReference",
    "RuleReference",
    "ScopeReference",
    "TemplateReference",
]

publication.publish()

def _typecheckingstub__24c6213f84de176ff34df43d0c3ff94f9d83676ebd6ff19ebea93a2216dae4ba(
    *,
    deployment_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17b7e7a25a5bf94973e9f230377fa887539b3fbec244eec168aeaaae8f5bc088(
    *,
    policy_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f85f9439db939717ec82680c69f6449d6a04ebb27a368143a9a527d574bbd710(
    *,
    rule_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b2c857fa029abe7aadce73c4bed17838908126f72fa25e4c65ad8fdcd9c55bb(
    *,
    scope_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12450cbae07b20c4f3f4c0e65cd96692f766aca21277513ce5d06c5e9f70a9e1(
    *,
    template_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

for cls in [IDeploymentRef, IPolicyRef, IRuleRef, IScopeRef, ITemplateRef]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
