r'''
<!--
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0
-->

# cdk-nag

[![PyPI version](https://img.shields.io/pypi/v/cdk-nag)](https://pypi.org/project/cdk-nag/)
[![npm version](https://img.shields.io/npm/v/cdk-nag)](https://www.npmjs.com/package/cdk-nag)
[![Maven version](https://img.shields.io/maven-central/v/io.github.cdklabs/cdknag)](https://search.maven.org/search?q=a:cdknag)
[![NuGet version](https://img.shields.io/nuget/v/Cdklabs.CdkNag)](https://www.nuget.org/packages/Cdklabs.CdkNag)
[![Go version](https://img.shields.io/github/go-mod/go-version/cdklabs/cdk-nag-go?color=blue&filename=cdknag%2Fgo.mod)](https://github.com/cdklabs/cdk-nag-go)

[![View on Construct Hub](https://constructs.dev/badge?package=cdk-nag)](https://constructs.dev/packages/cdk-nag)

Check CDK applications or [CloudFormation templates](#using-on-cloudformation-templates) for best practices using a combination of available rule packs. Inspired by [cfn_nag](https://github.com/stelligent/cfn_nag).

Check out [this blog post](https://aws.amazon.com/blogs/devops/manage-application-security-and-compliance-with-the-aws-cloud-development-kit-and-cdk-nag/) for a guided overview!

![demo](cdk_nag.gif)

## Available Rules and Packs

See [RULES](./RULES.md) for more information on all the available packs.

1. [AWS Solutions](./RULES.md#awssolutions)
2. [HIPAA Security](./RULES.md#hipaa-security)
3. [NIST 800-53 rev 4](./RULES.md#nist-800-53-rev-4)
4. [NIST 800-53 rev 5](./RULES.md#nist-800-53-rev-5)
5. [PCI DSS 3.2.1](./RULES.md#pci-dss-321)
6. [Serverless](./RULES.md#serverless)

[RULES](./RULES.md) also includes a collection of [additional rules](./RULES.md#additional-rules) that are not currently included in any of the pre-built NagPacks, but are still available for inclusion in custom NagPacks.

Read the [NagPack developer docs](./docs/NagPack.md) if you are interested in creating your own pack.

## Usage

For a full list of options See `NagPackProps` in the [API.md](./API.md#struct-nagpackprops)

<details>
<summary>Including in an application</summary>

```python
from aws_cdk import App, Validations
from cdk_nag import AwsSolutionsChecks, NIST80053R5Checks

# CdkTestStack: Any

app = App()
CdkTestStack(app, "CdkNagDemo")
# Simple rule informational messages using the AWS Solutions Rule pack
Validations.of(app).add_plugins(AwsSolutionsChecks(app))
# Multiple rule packs can be run against the same app
Validations.of(app).add_plugins(NIST80053R5Checks(app))
```

</details>

## Acknowledging a Rule

Use CDK's native `Validations.of()` API to acknowledge (suppress) rule violations on specific constructs.

<details>
  <summary>Example 1) Acknowledging a rule on a construct</summary>

```python
from aws_cdk.aws_ec2 import SecurityGroup, Vpc, Peer, Port
from aws_cdk import Stack, StackProps, Validations
from constructs import Construct

class CdkTestStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, notificationArns=None, synthesizer=None, terminationProtection=None, analyticsReporting=None, crossRegionReferences=None, permissionsBoundary=None, suppressTemplateIndentation=None, propertyInjectors=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, notificationArns=notificationArns, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting, crossRegionReferences=crossRegionReferences, permissionsBoundary=permissionsBoundary, suppressTemplateIndentation=suppressTemplateIndentation, propertyInjectors=propertyInjectors)
        test = SecurityGroup(self, "test",
            vpc=Vpc(self, "vpc")
        )
        test.add_ingress_rule(Peer.any_ipv4(), Port.all_traffic())
        Validations.of(test).acknowledge(
            id="AwsSolutions-EC23",
            reason="This security group is used for internal testing only."
        )
```

</details><details>
  <summary>Example 2) Acknowledging a rule on a stack</summary>

```python
from aws_cdk import App, Validations
from cdk_nag import AwsSolutionsChecks

# CdkTestStack: Any

app = App()
stack = CdkTestStack(app, "CdkNagDemo")
Validations.of(app).add_plugins(AwsSolutionsChecks(app))
Validations.of(stack).acknowledge(
    id="AwsSolutions-EC23",
    reason="All security groups in this stack are internal only."
)
```

</details><details>
  <summary>Example 3) Acknowledging a specific finding</summary>

Certain rules report multiple findings per resource (e.g., IAM wildcard permissions). Each finding has its own ID in the format `RuleId[FindingId]`.

If you received the following errors on synth/deploy:

```bash
[Error at /StackName/rUser/DefaultPolicy/Resource] AwsSolutions-IAM5[Action::s3:*]: The IAM entity contains wildcard permissions.
[Error at /StackName/rUser/DefaultPolicy/Resource] AwsSolutions-IAM5[Resource::*]: The IAM entity contains wildcard permissions.
```

You can acknowledge a specific finding:

```python
from aws_cdk.aws_iam import User, PolicyStatement
from aws_cdk import Stack, StackProps, Validations
from constructs import Construct

class CdkTestStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, notificationArns=None, synthesizer=None, terminationProtection=None, analyticsReporting=None, crossRegionReferences=None, permissionsBoundary=None, suppressTemplateIndentation=None, propertyInjectors=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, notificationArns=notificationArns, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting, crossRegionReferences=crossRegionReferences, permissionsBoundary=permissionsBoundary, suppressTemplateIndentation=suppressTemplateIndentation, propertyInjectors=propertyInjectors)
        user = User(self, "rUser")
        user.add_to_policy(
            PolicyStatement(
                actions=["s3:*"],
                resources=["*"]
            ))
        # Only acknowledge the s3:* action — Resource::* still triggers
        Validations.of(user).acknowledge(
            id="AwsSolutions-IAM5[Action::s3:*]",
            reason="Need s3:* for cross-account replication."
        )
```

</details>

## Rules and Property Overrides

In some cases L2 Constructs do not have a native option to remediate an issue and must be fixed via [Raw Overrides](https://docs.aws.amazon.com/cdk/latest/guide/cfn_layer.html#cfn_layer_raw). Since raw overrides take place after template synthesis these fixes are not caught by cdk-nag. In this case you should remediate the issue and acknowledge the rule.

<details>
  <summary>Example) Property Overrides</summary>

```python
from aws_cdk.aws_ec2 import Instance, InstanceType, InstanceClass, MachineImage, Vpc, CfnInstance
from aws_cdk import Stack, StackProps, Validations
from constructs import Construct

class CdkTestStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, notificationArns=None, synthesizer=None, terminationProtection=None, analyticsReporting=None, crossRegionReferences=None, permissionsBoundary=None, suppressTemplateIndentation=None, propertyInjectors=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, notificationArns=notificationArns, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting, crossRegionReferences=crossRegionReferences, permissionsBoundary=permissionsBoundary, suppressTemplateIndentation=suppressTemplateIndentation, propertyInjectors=propertyInjectors)
        instance = Instance(self, "rInstance",
            vpc=Vpc(self, "rVpc"),
            instance_type=InstanceType(InstanceClass.T3),
            machine_image=MachineImage.latest_amazon_linux()
        )
        cfn_ins = instance.node.default_child
        cfn_ins.add_property_override("DisableApiTermination", True)
        Validations.of(instance).acknowledge(
            id="AwsSolutions-EC29",
            reason="Remediated through property override."
        )
```

</details>

## Audit Trail: CloudFormation Metadata

By default, cdk-nag writes violations to CDK's `policy-validation-report.json` in the cloud assembly. If you need the v2-compatible `cdk_nag` metadata block in your synthesized CloudFormation templates (for existing compliance tooling), enable `writeSuppressionsToCloudFormation`:

```python
from aws_cdk import App, Validations
from cdk_nag import AwsSolutionsChecks

app = App()
# Writes acknowledged rules into CfnResource Metadata as cdk_nag: { rules_to_suppress: [...] }
Validations.of(app).add_plugins(AwsSolutionsChecks(app, write_suppressions_to_cloud_formation=True))
```

This registers a `WriteNagSuppressionsToCloudFormationAspect` that runs during synthesis and copies `Validations.of().acknowledge()` data into the CloudFormation template Metadata section, preserving the same format as cdk-nag v2.

## Using on CloudFormation templates

You can use cdk-nag on existing CloudFormation templates by using the [cloudformation-include](https://docs.aws.amazon.com/cdk/latest/guide/use-cfn-template.html#use-cfn-template-import) module.

<details>
  <summary>Example) CloudFormation template</summary>

Sample App

```python
from aws_cdk import App, Validations
from cdk_nag import AwsSolutionsChecks

# CdkTestStack: Any

app = App()
CdkTestStack(app, "CdkNagDemo")
Validations.of(app).add_plugins(AwsSolutionsChecks(app))
```

Sample Stack with imported template

```python
from aws_cdk.cloudformation_include import CfnInclude
from aws_cdk import Stack, StackProps, Validations
from constructs import Construct

class CdkTestStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, notificationArns=None, synthesizer=None, terminationProtection=None, analyticsReporting=None, crossRegionReferences=None, permissionsBoundary=None, suppressTemplateIndentation=None, propertyInjectors=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, notificationArns=notificationArns, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting, crossRegionReferences=crossRegionReferences, permissionsBoundary=permissionsBoundary, suppressTemplateIndentation=suppressTemplateIndentation, propertyInjectors=propertyInjectors)
        template = CfnInclude(self, "Template",
            template_file="my-template.json"
        )
        # Acknowledge rules on imported resources
        bucket = template.get_resource("rBucket")
        Validations.of(bucket).acknowledge(
            id="AwsSolutions-S1",
            reason="Logging not required for this bucket."
        )
```

</details>

## Migrating from v2

cdk-nag v3 replaces the custom `NagSuppressions` API with CDK's native `Validations.of().acknowledge()` mechanism.

| v2 | v3 |
|---|---|
| `NagSuppressions.addResourceSuppressions(construct, [{ id, reason }])` | `Validations.of(construct).acknowledge({ id, reason })` |
| `NagSuppressions.addStackSuppressions(stack, [{ id, reason }])` | `Validations.of(stack).acknowledge({ id, reason })` |
| `NagSuppressions.addResourceSuppressionsByPath(stack, path, [...])` | `Validations.of(construct).acknowledge({ id, reason })` |
| `appliesTo: ['Action::s3:*']` | `id: 'AwsSolutions-IAM5[Action::s3:*]'` |
| `{ id: 'CdkNagValidationFailure', reason: '...' }` | `Validations.of(construct).acknowledge({ id: 'RuleId', reason: '...' })` |

**Note on bulk suppression:** In v2, suppressing a rule without `appliesTo` would suppress all findings for that rule on the construct. In v3, each finding must be acknowledged individually (e.g., `AwsSolutions-IAM5[Action::s3:*]` and `AwsSolutions-IAM5[Resource::*]` are separate acknowledgments). Prefix matching (acknowledging `AwsSolutions-IAM5` to suppress all findings) is not yet supported — tracked via [issue link].

**Removed APIs:**

* `NagSuppressions` (use `Validations.of().acknowledge()`)
* `INagSuppressionIgnore` and all condition classes
* `NagPackSuppression` interface
* `CdkNagValidationFailure` concept
* `logIgnores` and `suppressionIgnoreCondition` props

## Contributing

See [CONTRIBUTING](./CONTRIBUTING.md) for more information.

## License

This project is licensed under the Apache-2.0 License.
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


from ._jsii import *

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

    import aws_cdk as _aws_cdk_ceddda9d
    import constructs as _constructs_77d1e7e8
else:

    _aws_cdk_ceddda9d = _LazyImport("aws_cdk")
    _constructs_77d1e7e8 = _LazyImport("constructs")


@jsii.interface(jsii_type="cdk-nag.IApplyRule")
class IApplyRule(typing_extensions.Protocol):
    '''(experimental) Interface for JSII interoperability for passing parameters and the Rule Callback to.

    :stability: experimental
    :applyRule: method.
    '''

    @builtins.property
    @jsii.member(jsii_name="explanation")
    def explanation(self) -> builtins.str:
        '''(experimental) Why the rule exists.

        :stability: experimental
        '''
        ...

    @explanation.setter
    def explanation(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="info")
    def info(self) -> builtins.str:
        '''(experimental) Why the rule was triggered.

        :stability: experimental
        '''
        ...

    @info.setter
    def info(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> "NagMessageLevel":
        '''(experimental) The annotations message level to apply to the rule if triggered.

        :stability: experimental
        '''
        ...

    @level.setter
    def level(self, value: "NagMessageLevel") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="node")
    def node(self) -> "_aws_cdk_ceddda9d.CfnResource":
        '''(experimental) The CfnResource to check.

        :stability: experimental
        '''
        ...

    @node.setter
    def node(self, value: "_aws_cdk_ceddda9d.CfnResource") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="ruleSuffixOverride")
    def rule_suffix_override(self) -> typing.Optional[builtins.str]:
        '''(experimental) Override for the suffix of the Rule ID for this rule.

        :stability: experimental
        '''
        ...

    @rule_suffix_override.setter
    def rule_suffix_override(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @jsii.member(jsii_name="rule")
    def rule(
        self,
        node: "_aws_cdk_ceddda9d.CfnResource",
    ) -> typing.Union["NagRuleCompliance", typing.List[builtins.str]]:
        '''(experimental) The callback to the rule.

        :param node: The CfnResource to check.

        :stability: experimental
        '''
        ...


class _IApplyRuleProxy:
    '''(experimental) Interface for JSII interoperability for passing parameters and the Rule Callback to.

    :stability: experimental
    :applyRule: method.
    '''

    __jsii_type__: typing.ClassVar[str] = "cdk-nag.IApplyRule"

    @builtins.property
    @jsii.member(jsii_name="explanation")
    def explanation(self) -> builtins.str:
        '''(experimental) Why the rule exists.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "explanation"))

    @explanation.setter
    def explanation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6a23651ea44768b1af733a2b9cef46eced1602c3bca3849419b685c2c8fcba15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "explanation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="info")
    def info(self) -> builtins.str:
        '''(experimental) Why the rule was triggered.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "info"))

    @info.setter
    def info(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__5b0a9865d3a20bd3ed9f672903366f8e8197ef53dddebf5ab545d1e84de2ca16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "info", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> "NagMessageLevel":
        '''(experimental) The annotations message level to apply to the rule if triggered.

        :stability: experimental
        '''
        return typing.cast("NagMessageLevel", jsii.get(self, "level"))

    @level.setter
    def level(self, value: "NagMessageLevel") -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__fca6380ef48764f27214931f0c5bf28e44b41d002da53939e9265879e403ff9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "level", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="node")
    def node(self) -> "_aws_cdk_ceddda9d.CfnResource":
        '''(experimental) The CfnResource to check.

        :stability: experimental
        '''
        return typing.cast("_aws_cdk_ceddda9d.CfnResource", jsii.get(self, "node"))

    @node.setter
    def node(self, value: "_aws_cdk_ceddda9d.CfnResource") -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__123173a6ce5be62d3f85f1d78609032a82004c4807c1cc883736375dfa93eb62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "node", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ruleSuffixOverride")
    def rule_suffix_override(self) -> typing.Optional[builtins.str]:
        '''(experimental) Override for the suffix of the Rule ID for this rule.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleSuffixOverride"))

    @rule_suffix_override.setter
    def rule_suffix_override(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__333cce877f5798931df373ac5d819b402e92f9ac723cf0184c1db35694ca67a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleSuffixOverride", value) # pyright: ignore[reportArgumentType]

    @jsii.member(jsii_name="rule")
    def rule(
        self,
        node: "_aws_cdk_ceddda9d.CfnResource",
    ) -> typing.Union["NagRuleCompliance", typing.List[builtins.str]]:
        '''(experimental) The callback to the rule.

        :param node: The CfnResource to check.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__735fc03a45b618e514165f2e218d73e8b7084a45ea15b931267f19e67ef9e8c0)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(typing.Union["NagRuleCompliance", typing.List[builtins.str]], jsii.invoke(self, "rule", [node]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IApplyRule).__jsii_proxy_class__ = lambda : _IApplyRuleProxy


@jsii.interface(jsii_type="cdk-nag.INagValidationContext")
class INagValidationContext(
    _aws_cdk_ceddda9d.IPolicyValidationContext,
    typing_extensions.Protocol,
):
    '''(experimental) Extended validation context that includes the construct tree.

    Requires CDK core change to populate ``appConstruct`` during plugin validation.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="appConstruct")
    def app_construct(self) -> "_constructs_77d1e7e8.IConstruct":
        '''
        :stability: experimental
        '''
        ...


class _INagValidationContextProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IPolicyValidationContext), # type: ignore[misc]
):
    '''(experimental) Extended validation context that includes the construct tree.

    Requires CDK core change to populate ``appConstruct`` during plugin validation.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdk-nag.INagValidationContext"

    @builtins.property
    @jsii.member(jsii_name="appConstruct")
    def app_construct(self) -> "_constructs_77d1e7e8.IConstruct":
        '''
        :stability: experimental
        '''
        return typing.cast("_constructs_77d1e7e8.IConstruct", jsii.get(self, "appConstruct"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INagValidationContext).__jsii_proxy_class__ = lambda : _INagValidationContextProxy


@jsii.enum(jsii_type="cdk-nag.NagMessageLevel")
class NagMessageLevel(enum.Enum):
    '''(experimental) The severity level of the rule.

    :stability: experimental
    '''

    WARN = "WARN"
    '''
    :stability: experimental
    '''
    ERROR = "ERROR"
    '''
    :stability: experimental
    '''
    INFO = "INFO"
    '''
    :stability: experimental
    '''


@jsii.implements(_aws_cdk_ceddda9d.IPolicyValidationPlugin)
class NagPack(metaclass=jsii.JSIIAbstractClass, jsii_type="cdk-nag.NagPack"):
    '''(experimental) Base class for all rule packs.

    Implements IPolicyValidationPlugin so that
    packs are registered via ``Validations.of(app).addPlugins(new MyPack(app))``
    instead of ``Aspects.of(app).add(...)``.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: typing.Optional["_constructs_77d1e7e8.IConstruct"] = None,
        *,
        verbose: typing.Optional[builtins.bool] = None,
        write_suppressions_to_cloud_formation: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param verbose: (experimental) Whether or not to enable extended explanatory descriptions on warning, error, and logged ignore messages (default: false).
        :param write_suppressions_to_cloud_formation: (experimental) Whether to write acknowledged rules into CfnResource CloudFormation Metadata as ``cdk_nag: { rules_to_suppress: [...] }`` for backwards compatibility with v2 audit trail tooling (default: false).

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3017bec3b325642a7f017efcaa8f3e15a21609195066e1d9d84ad8398f1774dd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        props = NagPackProps(
            verbose=verbose,
            write_suppressions_to_cloud_formation=write_suppressions_to_cloud_formation,
        )

        jsii.create(self.__class__, self, [scope, props])

    @jsii.member(jsii_name="applyRule")
    def _apply_rule(self, params: "IApplyRule") -> None:
        '''(experimental) Create a rule to be used in the NagPack.

        :param params: The.

        :stability: experimental
        :IApplyRule: interface with rule details.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f3628e5213d5585ace3e16109c26f8af64546c343c9014c7c1f61edad43c259e)
            check_type(argname="argument params", value=params, expected_type=type_hints["params"])
        return typing.cast(None, jsii.invoke(self, "applyRule", [params]))

    @jsii.member(jsii_name="checkResource")
    @abc.abstractmethod
    def _check_resource(self, node: "_aws_cdk_ceddda9d.CfnResource") -> None:
        '''(experimental) Subclasses implement this to apply rules to each CfnResource.

        :param node: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="validate")
    def validate(
        self,
        context: "_aws_cdk_ceddda9d.IPolicyValidationContext",
    ) -> "_aws_cdk_ceddda9d.PolicyValidationPluginReport":
        '''(experimental) Entry point called by the CDK validation framework.

        Requires ``appConstruct`` to be present on the context (CDK core change).
        For testing or direct invocation, use ``validateScope(scope)``.

        :param context: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__0e2d68c6332428b542b671a5db7d792e33667aab3e08db3145e98ebce4d22528)
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
        return typing.cast("_aws_cdk_ceddda9d.PolicyValidationPluginReport", jsii.invoke(self, "validate", [context]))

    @jsii.member(jsii_name="validateScope")
    def validate_scope(
        self,
        scope: "_constructs_77d1e7e8.IConstruct",
    ) -> "_aws_cdk_ceddda9d.PolicyValidationPluginReport":
        '''(experimental) Validate a construct tree directly.

        This is the primary entry point
        for testing and for CDK versions that do not yet provide ``appConstruct`` on
        ``IPolicyValidationContext``.

        :param scope: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ec1e978998b866e1f0cf9b5507693090d004d680485682bafc3b9491680ab041)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast("_aws_cdk_ceddda9d.PolicyValidationPluginReport", jsii.invoke(self, "validateScope", [scope]))

    @builtins.property
    @jsii.member(jsii_name="name")
    @abc.abstractmethod
    def name(self) -> builtins.str:
        '''(experimental) The name of the plugin that will be displayed in the validation report.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="readPackName")
    def read_pack_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "readPackName"))

    @builtins.property
    @jsii.member(jsii_name="ruleIds")
    def rule_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The list of rule IDs that the plugin will evaluate.

        Used for analytics
        purposes.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ruleIds"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of the plugin, following the Semantic Versioning specification (see https://semver.org/). This version is used for analytics purposes, to measure the usage of different plugins and different versions. The value of this property should be kept in sync with the actual version of the software package. If the version is not provided or is not a valid semantic version, it will be reported as ``0.0.0``.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="packName")
    def _pack_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "packName"))

    @_pack_name.setter
    def _pack_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__18633cd3423c88500a3be3035af0c083c9c2a61e7358e09d541efac11ba04ecf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packName", value) # pyright: ignore[reportArgumentType]


class _NagPackProxy(NagPack):
    @jsii.member(jsii_name="checkResource")
    def _check_resource(self, node: "_aws_cdk_ceddda9d.CfnResource") -> None:
        '''(experimental) Subclasses implement this to apply rules to each CfnResource.

        :param node: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f430411ab22d637c2bb7899d2fa75de3d7035a2affe70f9e393e020a84d1dd36)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "checkResource", [node]))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The name of the plugin that will be displayed in the validation report.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, NagPack).__jsii_proxy_class__ = lambda : _NagPackProxy


@jsii.data_type(
    jsii_type="cdk-nag.NagPackProps",
    jsii_struct_bases=[],
    name_mapping={
        "verbose": "verbose",
        "write_suppressions_to_cloud_formation": "writeSuppressionsToCloudFormation",
    },
)
class NagPackProps:
    def __init__(
        self,
        *,
        verbose: typing.Optional[builtins.bool] = None,
        write_suppressions_to_cloud_formation: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Interface for creating a NagPack.

        :param verbose: (experimental) Whether or not to enable extended explanatory descriptions on warning, error, and logged ignore messages (default: false).
        :param write_suppressions_to_cloud_formation: (experimental) Whether to write acknowledged rules into CfnResource CloudFormation Metadata as ``cdk_nag: { rules_to_suppress: [...] }`` for backwards compatibility with v2 audit trail tooling (default: false).

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__83a83ce3fdb1cb0ca96a59694799f0ed3b0090f7d4e437681d969d4c74e7ddab)
            check_type(argname="argument verbose", value=verbose, expected_type=type_hints["verbose"])
            check_type(argname="argument write_suppressions_to_cloud_formation", value=write_suppressions_to_cloud_formation, expected_type=type_hints["write_suppressions_to_cloud_formation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if verbose is not None:
            self._values["verbose"] = verbose
        if write_suppressions_to_cloud_formation is not None:
            self._values["write_suppressions_to_cloud_formation"] = write_suppressions_to_cloud_formation

    @builtins.property
    def verbose(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not to enable extended explanatory descriptions on warning, error, and logged ignore messages (default: false).

        :stability: experimental
        '''
        result = self._values.get("verbose")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def write_suppressions_to_cloud_formation(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to write acknowledged rules into CfnResource CloudFormation Metadata as ``cdk_nag: { rules_to_suppress: [...] }`` for backwards compatibility with v2 audit trail tooling (default: false).

        :stability: experimental
        '''
        result = self._values.get("write_suppressions_to_cloud_formation")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NagPackProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-nag.NagReportFormat")
class NagReportFormat(enum.Enum):
    '''(experimental) Possible output formats of the NagReport.

    :stability: experimental
    '''

    CSV = "CSV"
    '''
    :stability: experimental
    '''
    JSON = "JSON"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="cdk-nag.NagReportLine",
    jsii_struct_bases=[],
    name_mapping={
        "compliance": "compliance",
        "resource_id": "resourceId",
        "rule_id": "ruleId",
        "rule_info": "ruleInfo",
        "rule_level": "ruleLevel",
    },
)
class NagReportLine:
    def __init__(
        self,
        *,
        compliance: builtins.str,
        resource_id: builtins.str,
        rule_id: builtins.str,
        rule_info: builtins.str,
        rule_level: builtins.str,
    ) -> None:
        '''(experimental) A single line in a NagReport.

        :param compliance: 
        :param resource_id: 
        :param rule_id: 
        :param rule_info: 
        :param rule_level: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__4c6b6029bff770690f88c877bee0f2885b7bc043157258be4815d22b42c13364)
            check_type(argname="argument compliance", value=compliance, expected_type=type_hints["compliance"])
            check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
            check_type(argname="argument rule_id", value=rule_id, expected_type=type_hints["rule_id"])
            check_type(argname="argument rule_info", value=rule_info, expected_type=type_hints["rule_info"])
            check_type(argname="argument rule_level", value=rule_level, expected_type=type_hints["rule_level"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "compliance": compliance,
            "resource_id": resource_id,
            "rule_id": rule_id,
            "rule_info": rule_info,
            "rule_level": rule_level,
        }

    @builtins.property
    def compliance(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("compliance")
        assert result is not None, "Required property 'compliance' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("resource_id")
        assert result is not None, "Required property 'resource_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("rule_id")
        assert result is not None, "Required property 'rule_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule_info(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("rule_info")
        assert result is not None, "Required property 'rule_info' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule_level(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("rule_level")
        assert result is not None, "Required property 'rule_level' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NagReportLine(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-nag.NagReportSchema",
    jsii_struct_bases=[],
    name_mapping={"lines": "lines"},
)
class NagReportSchema:
    def __init__(
        self,
        *,
        lines: typing.Sequence[typing.Union["NagReportLine", typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''(experimental) Schema for the NagReport output.

        :param lines: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1d13606a383c679c37ca15873660037b156e8491412ee339c74a414fb2061d8d)
            check_type(argname="argument lines", value=lines, expected_type=type_hints["lines"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "lines": lines,
        }

    @builtins.property
    def lines(self) -> typing.List["NagReportLine"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lines")
        assert result is not None, "Required property 'lines' is missing"
        return typing.cast(typing.List["NagReportLine"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NagReportSchema(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-nag.NagRuleCompliance")
class NagRuleCompliance(enum.Enum):
    '''(experimental) The compliance level of a resource in relation to a rule.

    :stability: experimental
    '''

    COMPLIANT = "COMPLIANT"
    '''
    :stability: experimental
    '''
    NON_COMPLIANT = "NON_COMPLIANT"
    '''
    :stability: experimental
    '''
    NOT_APPLICABLE = "NOT_APPLICABLE"
    '''
    :stability: experimental
    '''


@jsii.enum(jsii_type="cdk-nag.NagRulePostValidationStates")
class NagRulePostValidationStates(enum.Enum):
    '''(experimental) Additional states a rule can be in post compliance validation.

    :stability: experimental
    '''

    UNKNOWN = "UNKNOWN"
    '''
    :stability: experimental
    '''


class NagRules(metaclass=jsii.JSIIMeta, jsii_type="cdk-nag.NagRules"):
    '''(experimental) Helper class with methods for rule creation.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="resolveIfPrimitive")
    @builtins.classmethod
    def resolve_if_primitive(
        cls,
        node: "_aws_cdk_ceddda9d.CfnResource",
        parameter: typing.Any,
    ) -> typing.Any:
        '''(experimental) Use in cases where a primitive value must be known to pass a rule.

        https://developer.mozilla.org/en-US/docs/Glossary/Primitive

        :param node: The CfnResource to check.
        :param parameter: The value to attempt to resolve.

        :return: Return a value if resolves to a primitive data type, otherwise throw an error.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a8817c32270238bf0dfc84f6218e16b587420567b5bc41a280c177f7ee6cd79f)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
            check_type(argname="argument parameter", value=parameter, expected_type=type_hints["parameter"])
        return typing.cast(typing.Any, jsii.sinvoke(cls, "resolveIfPrimitive", [node, parameter]))

    @jsii.member(jsii_name="resolveResourceFromInstrinsic")
    @builtins.classmethod
    def resolve_resource_from_instrinsic(
        cls,
        node: "_aws_cdk_ceddda9d.CfnResource",
        parameter: typing.Any,
    ) -> typing.Any:
        '''
        :param node: The CfnResource to check.
        :param parameter: The value to attempt to resolve.

        :return: Return the Logical resource Id if resolves to a intrinsic function, otherwise the resolved provided value.

        :deprecated:

        Use resolveResourceFromIntrinsic instead

        Use in cases where a token resolves to an intrinsic function and the referenced resource must be known to pass a rule.

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b2af31e0e8c775eabad30b7da777a2689dbf22e8f31976bf4840dbd2cbbbf939)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
            check_type(argname="argument parameter", value=parameter, expected_type=type_hints["parameter"])
        return typing.cast(typing.Any, jsii.sinvoke(cls, "resolveResourceFromInstrinsic", [node, parameter]))

    @jsii.member(jsii_name="resolveResourceFromIntrinsic")
    @builtins.classmethod
    def resolve_resource_from_intrinsic(
        cls,
        node: "_aws_cdk_ceddda9d.CfnResource",
        parameter: typing.Any,
    ) -> typing.Any:
        '''(experimental) Use in cases where a token resolves to an intrinsic function and the referenced resource must be known to pass a rule.

        :param node: The CfnResource to check.
        :param parameter: The value to attempt to resolve.

        :return: Return the Logical resource Id if resolves to a intrinsic function, otherwise the resolved provided value.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__31cd67cca34b4963ea5b427552d0ed8190cf2265f4659708bb7d899d8e5fc6cb)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
            check_type(argname="argument parameter", value=parameter, expected_type=type_hints["parameter"])
        return typing.cast(typing.Any, jsii.sinvoke(cls, "resolveResourceFromIntrinsic", [node, parameter]))


class PCIDSS321Checks(
    NagPack,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-nag.PCIDSS321Checks",
):
    '''(experimental) Check for PCI DSS 3.2.1 compliance. Based on the PCI DSS 3.2.1 AWS operational best practices: https://docs.aws.amazon.com/config/latest/developerguide/operational-best-practices-for-pci-dss.html.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: typing.Optional["_constructs_77d1e7e8.IConstruct"] = None,
        *,
        verbose: typing.Optional[builtins.bool] = None,
        write_suppressions_to_cloud_formation: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param verbose: (experimental) Whether or not to enable extended explanatory descriptions on warning, error, and logged ignore messages (default: false).
        :param write_suppressions_to_cloud_formation: (experimental) Whether to write acknowledged rules into CfnResource CloudFormation Metadata as ``cdk_nag: { rules_to_suppress: [...] }`` for backwards compatibility with v2 audit trail tooling (default: false).

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__0cc46ecacf7df9181e9567c7b72fb36ba1959bfc351922f773f88c7525850fd5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        props = NagPackProps(
            verbose=verbose,
            write_suppressions_to_cloud_formation=write_suppressions_to_cloud_formation,
        )

        jsii.create(self.__class__, self, [scope, props])

    @jsii.member(jsii_name="checkResource")
    def _check_resource(self, node: "_aws_cdk_ceddda9d.CfnResource") -> None:
        '''(experimental) Subclasses implement this to apply rules to each CfnResource.

        :param node: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__71a8dce28af0aa91d1a25f141fdb97110a125246cb08236c3343190a9f176e8c)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "checkResource", [node]))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The name of the plugin that will be displayed in the validation report.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))


class ServerlessChecks(
    NagPack,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-nag.ServerlessChecks",
):
    '''(experimental) Serverless Checks are a compilation of rules to validate infrastructure-as-code template against recommended practices.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: typing.Optional["_constructs_77d1e7e8.IConstruct"] = None,
        *,
        verbose: typing.Optional[builtins.bool] = None,
        write_suppressions_to_cloud_formation: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param verbose: (experimental) Whether or not to enable extended explanatory descriptions on warning, error, and logged ignore messages (default: false).
        :param write_suppressions_to_cloud_formation: (experimental) Whether to write acknowledged rules into CfnResource CloudFormation Metadata as ``cdk_nag: { rules_to_suppress: [...] }`` for backwards compatibility with v2 audit trail tooling (default: false).

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f31b6fe87b5ee4f0b0ce0058a22fe72920f64a122756a75b670ced8ac39c82c7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        props = NagPackProps(
            verbose=verbose,
            write_suppressions_to_cloud_formation=write_suppressions_to_cloud_formation,
        )

        jsii.create(self.__class__, self, [scope, props])

    @jsii.member(jsii_name="checkResource")
    def _check_resource(self, node: "_aws_cdk_ceddda9d.CfnResource") -> None:
        '''(experimental) Subclasses implement this to apply rules to each CfnResource.

        :param node: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b782b306305e1d03c2a388cfcc90b66e8c5e5551fbc2060cede17ff43a8e7049)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "checkResource", [node]))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The name of the plugin that will be displayed in the validation report.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))


@jsii.implements(_aws_cdk_ceddda9d.IAspect)
class WriteNagSuppressionsToCloudFormationAspect(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-nag.WriteNagSuppressionsToCloudFormationAspect",
):
    '''(experimental) An IAspect that reads acknowledged rules from construct metadata and writes them into the CfnResource's CloudFormation Metadata for audit trail persistence in the synthesized template.

    Preserves the v2 ``cdk_nag``
    metadata format.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="visit")
    def visit(self, node: "_constructs_77d1e7e8.IConstruct") -> None:
        '''(experimental) All aspects can visit an IConstruct.

        :param node: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__32b5cbcbfb40ab453835409abb88c9f37fe966b387077de2bc63ec203bdd8590)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


class AwsSolutionsChecks(
    NagPack,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-nag.AwsSolutionsChecks",
):
    '''(experimental) Check Best practices based on AWS Solutions Security Matrix.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: typing.Optional["_constructs_77d1e7e8.IConstruct"] = None,
        *,
        verbose: typing.Optional[builtins.bool] = None,
        write_suppressions_to_cloud_formation: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param verbose: (experimental) Whether or not to enable extended explanatory descriptions on warning, error, and logged ignore messages (default: false).
        :param write_suppressions_to_cloud_formation: (experimental) Whether to write acknowledged rules into CfnResource CloudFormation Metadata as ``cdk_nag: { rules_to_suppress: [...] }`` for backwards compatibility with v2 audit trail tooling (default: false).

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ed3fdd64fd69f6c1132c8a1cba92e2661a89ce0f017c503e0bca7f221e3d1b38)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        props = NagPackProps(
            verbose=verbose,
            write_suppressions_to_cloud_formation=write_suppressions_to_cloud_formation,
        )

        jsii.create(self.__class__, self, [scope, props])

    @jsii.member(jsii_name="checkResource")
    def _check_resource(self, node: "_aws_cdk_ceddda9d.CfnResource") -> None:
        '''(experimental) Subclasses implement this to apply rules to each CfnResource.

        :param node: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d147812c742450618f7becf9ad71174cbebb6b13704701c3691b5de11d29f110)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "checkResource", [node]))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The name of the plugin that will be displayed in the validation report.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))


class HIPAASecurityChecks(
    NagPack,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-nag.HIPAASecurityChecks",
):
    '''(experimental) Check for HIPAA Security compliance.

    Based on the HIPAA Security AWS operational best practices: https://docs.aws.amazon.com/config/latest/developerguide/operational-best-practices-for-hipaa_security.html

    :stability: experimental
    '''

    def __init__(
        self,
        scope: typing.Optional["_constructs_77d1e7e8.IConstruct"] = None,
        *,
        verbose: typing.Optional[builtins.bool] = None,
        write_suppressions_to_cloud_formation: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param verbose: (experimental) Whether or not to enable extended explanatory descriptions on warning, error, and logged ignore messages (default: false).
        :param write_suppressions_to_cloud_formation: (experimental) Whether to write acknowledged rules into CfnResource CloudFormation Metadata as ``cdk_nag: { rules_to_suppress: [...] }`` for backwards compatibility with v2 audit trail tooling (default: false).

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6c8d54058510ca74dacc7d9eace3b0662165082781c44ddd1376dfa8493a5591)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        props = NagPackProps(
            verbose=verbose,
            write_suppressions_to_cloud_formation=write_suppressions_to_cloud_formation,
        )

        jsii.create(self.__class__, self, [scope, props])

    @jsii.member(jsii_name="checkResource")
    def _check_resource(self, node: "_aws_cdk_ceddda9d.CfnResource") -> None:
        '''(experimental) Subclasses implement this to apply rules to each CfnResource.

        :param node: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__96bd49c3468e34d61bd11381266e3b72071a66df475891ab572c446cb5dd8df6)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "checkResource", [node]))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The name of the plugin that will be displayed in the validation report.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))


class NIST80053R4Checks(
    NagPack,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-nag.NIST80053R4Checks",
):
    '''(experimental) Check for NIST 800-53 rev 4 compliance.

    Based on the NIST 800-53 rev 4 AWS operational best practices: https://docs.aws.amazon.com/config/latest/developerguide/operational-best-practices-for-nist-800-53_rev_4.html

    :stability: experimental
    '''

    def __init__(
        self,
        scope: typing.Optional["_constructs_77d1e7e8.IConstruct"] = None,
        *,
        verbose: typing.Optional[builtins.bool] = None,
        write_suppressions_to_cloud_formation: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param verbose: (experimental) Whether or not to enable extended explanatory descriptions on warning, error, and logged ignore messages (default: false).
        :param write_suppressions_to_cloud_formation: (experimental) Whether to write acknowledged rules into CfnResource CloudFormation Metadata as ``cdk_nag: { rules_to_suppress: [...] }`` for backwards compatibility with v2 audit trail tooling (default: false).

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__62fcbcacb1da6c78228604ef0803b448884fe3a3036295b1f48263e44334e07e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        props = NagPackProps(
            verbose=verbose,
            write_suppressions_to_cloud_formation=write_suppressions_to_cloud_formation,
        )

        jsii.create(self.__class__, self, [scope, props])

    @jsii.member(jsii_name="checkResource")
    def _check_resource(self, node: "_aws_cdk_ceddda9d.CfnResource") -> None:
        '''(experimental) Subclasses implement this to apply rules to each CfnResource.

        :param node: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__50ead95dfab8dd5759ca4e395f7da0761c36dad5d3a38e455542554fe5b1030c)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "checkResource", [node]))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The name of the plugin that will be displayed in the validation report.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))


class NIST80053R5Checks(
    NagPack,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-nag.NIST80053R5Checks",
):
    '''(experimental) Check for NIST 800-53 rev 5 compliance.

    Based on the NIST 800-53 rev 5 AWS operational best practices: https://docs.aws.amazon.com/config/latest/developerguide/operational-best-practices-for-nist-800-53_rev_5.html

    :stability: experimental
    '''

    def __init__(
        self,
        scope: typing.Optional["_constructs_77d1e7e8.IConstruct"] = None,
        *,
        verbose: typing.Optional[builtins.bool] = None,
        write_suppressions_to_cloud_formation: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param verbose: (experimental) Whether or not to enable extended explanatory descriptions on warning, error, and logged ignore messages (default: false).
        :param write_suppressions_to_cloud_formation: (experimental) Whether to write acknowledged rules into CfnResource CloudFormation Metadata as ``cdk_nag: { rules_to_suppress: [...] }`` for backwards compatibility with v2 audit trail tooling (default: false).

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3836ef55144e761b4b39324b693b0a70aa6270333ba84be0c748d88290d8f534)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        props = NagPackProps(
            verbose=verbose,
            write_suppressions_to_cloud_formation=write_suppressions_to_cloud_formation,
        )

        jsii.create(self.__class__, self, [scope, props])

    @jsii.member(jsii_name="checkResource")
    def _check_resource(self, node: "_aws_cdk_ceddda9d.CfnResource") -> None:
        '''(experimental) Subclasses implement this to apply rules to each CfnResource.

        :param node: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__48341372ba0221aae88ec766b1ef50ee63dca3abf31a5ccb00eb1494ea8584c0)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "checkResource", [node]))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The name of the plugin that will be displayed in the validation report.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))


__all__ = [
    "AwsSolutionsChecks",
    "HIPAASecurityChecks",
    "IApplyRule",
    "INagValidationContext",
    "NIST80053R4Checks",
    "NIST80053R5Checks",
    "NagMessageLevel",
    "NagPack",
    "NagPackProps",
    "NagReportFormat",
    "NagReportLine",
    "NagReportSchema",
    "NagRuleCompliance",
    "NagRulePostValidationStates",
    "NagRules",
    "PCIDSS321Checks",
    "ServerlessChecks",
    "WriteNagSuppressionsToCloudFormationAspect",
]

publication.publish()

def _typecheckingstub__6a23651ea44768b1af733a2b9cef46eced1602c3bca3849419b685c2c8fcba15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b0a9865d3a20bd3ed9f672903366f8e8197ef53dddebf5ab545d1e84de2ca16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fca6380ef48764f27214931f0c5bf28e44b41d002da53939e9265879e403ff9e(
    value: NagMessageLevel,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__123173a6ce5be62d3f85f1d78609032a82004c4807c1cc883736375dfa93eb62(
    value: _aws_cdk_ceddda9d.CfnResource,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__333cce877f5798931df373ac5d819b402e92f9ac723cf0184c1db35694ca67a9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__735fc03a45b618e514165f2e218d73e8b7084a45ea15b931267f19e67ef9e8c0(
    node: _aws_cdk_ceddda9d.CfnResource,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3017bec3b325642a7f017efcaa8f3e15a21609195066e1d9d84ad8398f1774dd(
    scope: typing.Optional[_constructs_77d1e7e8.IConstruct] = None,
    *,
    verbose: typing.Optional[builtins.bool] = None,
    write_suppressions_to_cloud_formation: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3628e5213d5585ace3e16109c26f8af64546c343c9014c7c1f61edad43c259e(
    params: IApplyRule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e2d68c6332428b542b671a5db7d792e33667aab3e08db3145e98ebce4d22528(
    context: _aws_cdk_ceddda9d.IPolicyValidationContext,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec1e978998b866e1f0cf9b5507693090d004d680485682bafc3b9491680ab041(
    scope: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18633cd3423c88500a3be3035af0c083c9c2a61e7358e09d541efac11ba04ecf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f430411ab22d637c2bb7899d2fa75de3d7035a2affe70f9e393e020a84d1dd36(
    node: _aws_cdk_ceddda9d.CfnResource,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83a83ce3fdb1cb0ca96a59694799f0ed3b0090f7d4e437681d969d4c74e7ddab(
    *,
    verbose: typing.Optional[builtins.bool] = None,
    write_suppressions_to_cloud_formation: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c6b6029bff770690f88c877bee0f2885b7bc043157258be4815d22b42c13364(
    *,
    compliance: builtins.str,
    resource_id: builtins.str,
    rule_id: builtins.str,
    rule_info: builtins.str,
    rule_level: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d13606a383c679c37ca15873660037b156e8491412ee339c74a414fb2061d8d(
    *,
    lines: typing.Sequence[typing.Union[NagReportLine, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8817c32270238bf0dfc84f6218e16b587420567b5bc41a280c177f7ee6cd79f(
    node: _aws_cdk_ceddda9d.CfnResource,
    parameter: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2af31e0e8c775eabad30b7da777a2689dbf22e8f31976bf4840dbd2cbbbf939(
    node: _aws_cdk_ceddda9d.CfnResource,
    parameter: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31cd67cca34b4963ea5b427552d0ed8190cf2265f4659708bb7d899d8e5fc6cb(
    node: _aws_cdk_ceddda9d.CfnResource,
    parameter: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cc46ecacf7df9181e9567c7b72fb36ba1959bfc351922f773f88c7525850fd5(
    scope: typing.Optional[_constructs_77d1e7e8.IConstruct] = None,
    *,
    verbose: typing.Optional[builtins.bool] = None,
    write_suppressions_to_cloud_formation: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71a8dce28af0aa91d1a25f141fdb97110a125246cb08236c3343190a9f176e8c(
    node: _aws_cdk_ceddda9d.CfnResource,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f31b6fe87b5ee4f0b0ce0058a22fe72920f64a122756a75b670ced8ac39c82c7(
    scope: typing.Optional[_constructs_77d1e7e8.IConstruct] = None,
    *,
    verbose: typing.Optional[builtins.bool] = None,
    write_suppressions_to_cloud_formation: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b782b306305e1d03c2a388cfcc90b66e8c5e5551fbc2060cede17ff43a8e7049(
    node: _aws_cdk_ceddda9d.CfnResource,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32b5cbcbfb40ab453835409abb88c9f37fe966b387077de2bc63ec203bdd8590(
    node: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed3fdd64fd69f6c1132c8a1cba92e2661a89ce0f017c503e0bca7f221e3d1b38(
    scope: typing.Optional[_constructs_77d1e7e8.IConstruct] = None,
    *,
    verbose: typing.Optional[builtins.bool] = None,
    write_suppressions_to_cloud_formation: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d147812c742450618f7becf9ad71174cbebb6b13704701c3691b5de11d29f110(
    node: _aws_cdk_ceddda9d.CfnResource,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c8d54058510ca74dacc7d9eace3b0662165082781c44ddd1376dfa8493a5591(
    scope: typing.Optional[_constructs_77d1e7e8.IConstruct] = None,
    *,
    verbose: typing.Optional[builtins.bool] = None,
    write_suppressions_to_cloud_formation: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96bd49c3468e34d61bd11381266e3b72071a66df475891ab572c446cb5dd8df6(
    node: _aws_cdk_ceddda9d.CfnResource,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62fcbcacb1da6c78228604ef0803b448884fe3a3036295b1f48263e44334e07e(
    scope: typing.Optional[_constructs_77d1e7e8.IConstruct] = None,
    *,
    verbose: typing.Optional[builtins.bool] = None,
    write_suppressions_to_cloud_formation: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50ead95dfab8dd5759ca4e395f7da0761c36dad5d3a38e455542554fe5b1030c(
    node: _aws_cdk_ceddda9d.CfnResource,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3836ef55144e761b4b39324b693b0a70aa6270333ba84be0c748d88290d8f534(
    scope: typing.Optional[_constructs_77d1e7e8.IConstruct] = None,
    *,
    verbose: typing.Optional[builtins.bool] = None,
    write_suppressions_to_cloud_formation: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48341372ba0221aae88ec766b1ef50ee63dca3abf31a5ccb00eb1494ea8584c0(
    node: _aws_cdk_ceddda9d.CfnResource,
) -> None:
    """Type checking stubs"""
    pass

for cls in [IApplyRule, INagValidationContext]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
