r'''
# Amazon Route53 Resolver Construct Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

## DNS Firewall

With Route 53 Resolver DNS Firewall, you can filter and regulate outbound DNS traffic for your
virtual private connections (VPCs). To do this, you create reusable collections of filtering rules
in DNS Firewall rule groups and associate the rule groups to your VPC.

DNS Firewall provides protection for outbound DNS requests from your VPCs. These requests route
through Resolver for domain name resolution. A primary use of DNS Firewall protections is to help
prevent DNS exfiltration of your data. DNS exfiltration can happen when a bad actor compromises
an application instance in your VPC and then uses DNS lookup to send data out of the VPC to a domain
that they control. With DNS Firewall, you can monitor and control the domains that your applications
can query. You can deny access to the domains that you know to be bad and allow all other queries
to pass through. Alternately, you can deny access to all domains except for the ones that you
explicitly trust.

### Domain lists

Domain lists can be created using a list of strings, a text file stored in Amazon S3 or a local
text file:

```python
block_list = route53resolver.FirewallDomainList(self, "BlockList",
    domains=route53resolver.FirewallDomains.from_list(["bad-domain.com", "bot-domain.net"])
)

s3_list = route53resolver.FirewallDomainList(self, "S3List",
    domains=route53resolver.FirewallDomains.from_s3_url("s3://bucket/prefix/object")
)

asset_list = route53resolver.FirewallDomainList(self, "AssetList",
    domains=route53resolver.FirewallDomains.from_asset("/path/to/domains.txt")
)
```

The file must be a text file and must contain a single domain per line.

Use `FirewallDomainList.fromFirewallDomainListId()` to import an existing or [AWS managed domain list](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resolver-dns-firewall-managed-domain-lists.html):

```python
# AWSManagedDomainsMalwareDomainList in us-east-1
malware_list = route53resolver.FirewallDomainList.from_firewall_domain_list_id(self, "Malware", "rslvr-fdl-2c46f2ecbfec4dcc")
```

### Rule group

Create a rule group:

```python
# my_block_list: route53resolver.FirewallDomainList

route53resolver.FirewallRuleGroup(self, "RuleGroup",
    rules=[route53resolver.FirewallRule(
        priority=10,
        firewall_domain_list=my_block_list,
        # block and reply with NODATA
        action=route53resolver.FirewallRuleAction.block()
    )
    ]
)
```

Rules can be added at construction time or using `addRule()`:

```python
# my_block_list: route53resolver.FirewallDomainList
# rule_group: route53resolver.FirewallRuleGroup


rule_group.add_rule(
    priority=10,
    firewall_domain_list=my_block_list,
    # block and reply with NXDOMAIN
    action=route53resolver.FirewallRuleAction.block(route53resolver.DnsBlockResponse.nx_domain())
)

rule_group.add_rule(
    priority=20,
    firewall_domain_list=my_block_list,
    # block and override DNS response with a custom domain
    action=route53resolver.FirewallRuleAction.block(route53resolver.DnsBlockResponse.override("amazon.com"))
)
```

Use `associate()` to associate a rule group with a VPC:

```python
import aws_cdk.aws_ec2 as ec2

# rule_group: route53resolver.FirewallRuleGroup
# my_vpc: ec2.Vpc


rule_group.associate("Association",
    priority=101,
    vpc=my_vpc
)
```
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
    import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
    import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
    import constructs as _constructs_77d1e7e8
else:

    _aws_cdk_aws_ec2_ceddda9d = _LazyImport("aws_cdk.aws_ec2")
    _aws_cdk_aws_s3_ceddda9d = _LazyImport("aws_cdk.aws_s3")
    _aws_cdk_ceddda9d = _LazyImport("aws_cdk")
    _constructs_77d1e7e8 = _LazyImport("constructs")


class DnsBlockResponse(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-route53resolver-alpha.DnsBlockResponse",
):
    '''(experimental) The way that you want DNS Firewall to block the request.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # my_block_list: route53resolver.FirewallDomainList
        # rule_group: route53resolver.FirewallRuleGroup
        
        
        rule_group.add_rule(
            priority=10,
            firewall_domain_list=my_block_list,
            # block and reply with NXDOMAIN
            action=route53resolver.FirewallRuleAction.block(route53resolver.DnsBlockResponse.nx_domain())
        )
        
        rule_group.add_rule(
            priority=20,
            firewall_domain_list=my_block_list,
            # block and override DNS response with a custom domain
            action=route53resolver.FirewallRuleAction.block(route53resolver.DnsBlockResponse.override("amazon.com"))
        )
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="noData")
    @builtins.classmethod
    def no_data(cls) -> "DnsBlockResponse":
        '''(experimental) Respond indicating that the query was successful, but no response is available for it.

        :stability: experimental
        '''
        return typing.cast("DnsBlockResponse", jsii.sinvoke(cls, "noData", []))

    @jsii.member(jsii_name="nxDomain")
    @builtins.classmethod
    def nx_domain(cls) -> "DnsBlockResponse":
        '''(experimental) Respond indicating that the domain name that's in the query doesn't exist.

        :stability: experimental
        '''
        return typing.cast("DnsBlockResponse", jsii.sinvoke(cls, "nxDomain", []))

    @jsii.member(jsii_name="override")
    @builtins.classmethod
    def override(
        cls,
        domain: builtins.str,
        ttl: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
    ) -> "DnsBlockResponse":
        '''(experimental) Provides a custom override response to the query.

        :param domain: The custom DNS record to send back in response to the query.
        :param ttl: The recommended amount of time for the DNS resolver or web browser to cache the provided override record.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__bcc6e5cbcbf161b026004146d290f4c2c5203dd60e43bb296ae451b7ea8afb50)
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
        return typing.cast("DnsBlockResponse", jsii.sinvoke(cls, "override", [domain, ttl]))

    @builtins.property
    @jsii.member(jsii_name="blockOverrideDnsType")
    @abc.abstractmethod
    def block_override_dns_type(self) -> typing.Optional[builtins.str]:
        '''(experimental) The DNS record's type.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="blockOverrideDomain")
    @abc.abstractmethod
    def block_override_domain(self) -> typing.Optional[builtins.str]:
        '''(experimental) The custom DNS record to send back in response to the query.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="blockOverrideTtl")
    @abc.abstractmethod
    def block_override_ttl(self) -> typing.Optional["_aws_cdk_ceddda9d.Duration"]:
        '''(experimental) The recommended amount of time for the DNS resolver or web browser to cache the provided override record.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="blockResponse")
    @abc.abstractmethod
    def block_response(self) -> typing.Optional[builtins.str]:
        '''(experimental) The way that you want DNS Firewall to block the request.

        :stability: experimental
        '''
        ...


class _DnsBlockResponseProxy(DnsBlockResponse):
    @builtins.property
    @jsii.member(jsii_name="blockOverrideDnsType")
    def block_override_dns_type(self) -> typing.Optional[builtins.str]:
        '''(experimental) The DNS record's type.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "blockOverrideDnsType"))

    @builtins.property
    @jsii.member(jsii_name="blockOverrideDomain")
    def block_override_domain(self) -> typing.Optional[builtins.str]:
        '''(experimental) The custom DNS record to send back in response to the query.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "blockOverrideDomain"))

    @builtins.property
    @jsii.member(jsii_name="blockOverrideTtl")
    def block_override_ttl(self) -> typing.Optional["_aws_cdk_ceddda9d.Duration"]:
        '''(experimental) The recommended amount of time for the DNS resolver or web browser to cache the provided override record.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["_aws_cdk_ceddda9d.Duration"], jsii.get(self, "blockOverrideTtl"))

    @builtins.property
    @jsii.member(jsii_name="blockResponse")
    def block_response(self) -> typing.Optional[builtins.str]:
        '''(experimental) The way that you want DNS Firewall to block the request.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "blockResponse"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, DnsBlockResponse).__jsii_proxy_class__ = lambda : _DnsBlockResponseProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-route53resolver-alpha.DomainsConfig",
    jsii_struct_bases=[],
    name_mapping={"domain_file_url": "domainFileUrl", "domains": "domains"},
)
class DomainsConfig:
    def __init__(
        self,
        *,
        domain_file_url: typing.Optional[builtins.str] = None,
        domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Domains configuration.

        :param domain_file_url: (experimental) The fully qualified URL or URI of the file stored in Amazon S3 that contains the list of domains to import. The file must be a text file and must contain a single domain per line. The content type of the S3 object must be ``plain/text``. Default: - use ``domains``
        :param domains: (experimental) A list of domains. Default: - use ``domainFileUrl``

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_route53resolver_alpha as route53resolver_alpha
            
            domains_config = route53resolver_alpha.DomainsConfig(
                domain_file_url="domainFileUrl",
                domains=["domains"]
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__efcc739bead6cd1e2f6028bbf509537b88cdaab217e4ad29abcb83010af732aa)
            check_type(argname="argument domain_file_url", value=domain_file_url, expected_type=type_hints["domain_file_url"])
            check_type(argname="argument domains", value=domains, expected_type=type_hints["domains"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if domain_file_url is not None:
            self._values["domain_file_url"] = domain_file_url
        if domains is not None:
            self._values["domains"] = domains

    @builtins.property
    def domain_file_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) The fully qualified URL or URI of the file stored in Amazon S3 that contains the list of domains to import.

        The file must be a text file and must contain
        a single domain per line. The content type of the S3 object must be ``plain/text``.

        :default: - use ``domains``

        :stability: experimental
        '''
        result = self._values.get("domain_file_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domains(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of domains.

        :default: - use ``domainFileUrl``

        :stability: experimental
        '''
        result = self._values.get("domains")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DomainsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-route53resolver-alpha.FirewallDomainListProps",
    jsii_struct_bases=[],
    name_mapping={"domains": "domains", "name": "name"},
)
class FirewallDomainListProps:
    def __init__(
        self,
        *,
        domains: "FirewallDomains",
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for a Firewall Domain List.

        :param domains: (experimental) A list of domains.
        :param name: (experimental) A name for the domain list. Default: - a CloudFormation generated name

        :stability: experimental
        :exampleMetadata: infused

        Example::

            block_list = route53resolver.FirewallDomainList(self, "BlockList",
                domains=route53resolver.FirewallDomains.from_list(["bad-domain.com", "bot-domain.net"])
            )
            
            s3_list = route53resolver.FirewallDomainList(self, "S3List",
                domains=route53resolver.FirewallDomains.from_s3_url("s3://bucket/prefix/object")
            )
            
            asset_list = route53resolver.FirewallDomainList(self, "AssetList",
                domains=route53resolver.FirewallDomains.from_asset("/path/to/domains.txt")
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e2694ecc77bbdf59285a53d044c17b801083d48fd6d9cf26c5798be8ef83cfd4)
            check_type(argname="argument domains", value=domains, expected_type=type_hints["domains"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domains": domains,
        }
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def domains(self) -> "FirewallDomains":
        '''(experimental) A list of domains.

        :stability: experimental
        '''
        result = self._values.get("domains")
        assert result is not None, "Required property 'domains' is missing"
        return typing.cast("FirewallDomains", result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the domain list.

        :default: - a CloudFormation generated name

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirewallDomainListProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirewallDomains(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-route53resolver-alpha.FirewallDomains",
):
    '''(experimental) A list of domains.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        block_list = route53resolver.FirewallDomainList(self, "BlockList",
            domains=route53resolver.FirewallDomains.from_list(["bad-domain.com", "bot-domain.net"])
        )
        
        s3_list = route53resolver.FirewallDomainList(self, "S3List",
            domains=route53resolver.FirewallDomains.from_s3_url("s3://bucket/prefix/object")
        )
        
        asset_list = route53resolver.FirewallDomainList(self, "AssetList",
            domains=route53resolver.FirewallDomains.from_asset("/path/to/domains.txt")
        )
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromAsset")
    @builtins.classmethod
    def from_asset(cls, asset_path: builtins.str) -> "FirewallDomains":
        '''(experimental) Firewall domains created from a local disk path to a text file.

        The file must be a text file (``.txt`` extension) and must contain a single
        domain per line. It will be uploaded to S3.

        :param asset_path: path to the text file.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a7b0d1079af5d8eb8466e6719de93c31cc9a02bfc3b4b058593e609db394d240)
            check_type(argname="argument asset_path", value=asset_path, expected_type=type_hints["asset_path"])
        return typing.cast("FirewallDomains", jsii.sinvoke(cls, "fromAsset", [asset_path]))

    @jsii.member(jsii_name="fromList")
    @builtins.classmethod
    def from_list(cls, list: typing.Sequence[builtins.str]) -> "FirewallDomains":
        '''(experimental) Firewall domains created from a list of domains.

        :param list: the list of domains.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__4db439b64de98348184f5457d37416fdf39df7bfa653f43e5546f736c932c7ba)
            check_type(argname="argument list", value=list, expected_type=type_hints["list"])
        return typing.cast("FirewallDomains", jsii.sinvoke(cls, "fromList", [list]))

    @jsii.member(jsii_name="fromS3")
    @builtins.classmethod
    def from_s3(
        cls,
        bucket: "_aws_cdk_aws_s3_ceddda9d.IBucket",
        key: builtins.str,
    ) -> "FirewallDomains":
        '''(experimental) Firewall domains created from a file stored in Amazon S3.

        The file must be a text file and must contain a single domain per line.
        The content type of the S3 object must be ``plain/text``.

        :param bucket: S3 bucket.
        :param key: S3 key.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__9123f4606e1c6eda8fc3b706939d87b0209c2bea457af92c0af2a946a6684d64)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast("FirewallDomains", jsii.sinvoke(cls, "fromS3", [bucket, key]))

    @jsii.member(jsii_name="fromS3Url")
    @builtins.classmethod
    def from_s3_url(cls, url: builtins.str) -> "FirewallDomains":
        '''(experimental) Firewall domains created from the URL of a file stored in Amazon S3.

        The file must be a text file and must contain a single domain per line.
        The content type of the S3 object must be ``plain/text``.

        :param url: S3 bucket url (s3://bucket/prefix/objet).

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__9f74514d1763b172a7f7f23feabbb8360b780c1b88c0e33c8dd934f2542a42db)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        return typing.cast("FirewallDomains", jsii.sinvoke(cls, "fromS3Url", [url]))

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, scope: "_constructs_77d1e7e8.Construct") -> "DomainsConfig":
        '''(experimental) Binds the domains to a domain list.

        :param scope: -

        :stability: experimental
        '''
        ...


class _FirewallDomainsProxy(FirewallDomains):
    @jsii.member(jsii_name="bind")
    def bind(self, scope: "_constructs_77d1e7e8.Construct") -> "DomainsConfig":
        '''(experimental) Binds the domains to a domain list.

        :param scope: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__beee843294402bd0b4634b78a18a987c0d888a0afb182d42637c4bf1d18c0908)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast("DomainsConfig", jsii.invoke(self, "bind", [scope]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, FirewallDomains).__jsii_proxy_class__ = lambda : _FirewallDomainsProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-route53resolver-alpha.FirewallRule",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "firewall_domain_list": "firewallDomainList",
        "priority": "priority",
    },
)
class FirewallRule:
    def __init__(
        self,
        *,
        action: "FirewallRuleAction",
        firewall_domain_list: "IFirewallDomainList",
        priority: jsii.Number,
    ) -> None:
        '''(experimental) A Firewall Rule.

        :param action: (experimental) The action for this rule.
        :param firewall_domain_list: (experimental) The domain list for this rule.
        :param priority: (experimental) The priority of the rule in the rule group. This value must be unique within the rule group.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # my_block_list: route53resolver.FirewallDomainList
            # rule_group: route53resolver.FirewallRuleGroup
            
            
            rule_group.add_rule(
                priority=10,
                firewall_domain_list=my_block_list,
                # block and reply with NXDOMAIN
                action=route53resolver.FirewallRuleAction.block(route53resolver.DnsBlockResponse.nx_domain())
            )
            
            rule_group.add_rule(
                priority=20,
                firewall_domain_list=my_block_list,
                # block and override DNS response with a custom domain
                action=route53resolver.FirewallRuleAction.block(route53resolver.DnsBlockResponse.override("amazon.com"))
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c842a13b2d3ff276f74958de9ce814eafca72f45f15296caa8cf78d6ad8c39a5)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument firewall_domain_list", value=firewall_domain_list, expected_type=type_hints["firewall_domain_list"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "firewall_domain_list": firewall_domain_list,
            "priority": priority,
        }

    @builtins.property
    def action(self) -> "FirewallRuleAction":
        '''(experimental) The action for this rule.

        :stability: experimental
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast("FirewallRuleAction", result)

    @builtins.property
    def firewall_domain_list(self) -> "IFirewallDomainList":
        '''(experimental) The domain list for this rule.

        :stability: experimental
        '''
        result = self._values.get("firewall_domain_list")
        assert result is not None, "Required property 'firewall_domain_list' is missing"
        return typing.cast("IFirewallDomainList", result)

    @builtins.property
    def priority(self) -> jsii.Number:
        '''(experimental) The priority of the rule in the rule group.

        This value must be unique within
        the rule group.

        :stability: experimental
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirewallRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirewallRuleAction(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-route53resolver-alpha.FirewallRuleAction",
):
    '''(experimental) A Firewall Rule.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # my_block_list: route53resolver.FirewallDomainList
        
        route53resolver.FirewallRuleGroup(self, "RuleGroup",
            rules=[route53resolver.FirewallRule(
                priority=10,
                firewall_domain_list=my_block_list,
                # block and reply with NODATA
                action=route53resolver.FirewallRuleAction.block()
            )
            ]
        )
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="alert")
    @builtins.classmethod
    def alert(cls) -> "FirewallRuleAction":
        '''(experimental) Permit the request to go through but send an alert to the logs.

        :stability: experimental
        '''
        return typing.cast("FirewallRuleAction", jsii.sinvoke(cls, "alert", []))

    @jsii.member(jsii_name="allow")
    @builtins.classmethod
    def allow(cls) -> "FirewallRuleAction":
        '''(experimental) Permit the request to go through.

        :stability: experimental
        '''
        return typing.cast("FirewallRuleAction", jsii.sinvoke(cls, "allow", []))

    @jsii.member(jsii_name="block")
    @builtins.classmethod
    def block(
        cls,
        response: typing.Optional["DnsBlockResponse"] = None,
    ) -> "FirewallRuleAction":
        '''(experimental) Disallow the request.

        :param response: The way that you want DNS Firewall to block the request.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__908212340f1ac128d44306136d4c2b8737eeff37eab2b68c781cfb8d7345f036)
            check_type(argname="argument response", value=response, expected_type=type_hints["response"])
        return typing.cast("FirewallRuleAction", jsii.sinvoke(cls, "block", [response]))

    @builtins.property
    @jsii.member(jsii_name="action")
    @abc.abstractmethod
    def action(self) -> builtins.str:
        '''(experimental) The action that DNS Firewall should take on a DNS query when it matches one of the domains in the rule's domain list.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="blockResponse")
    @abc.abstractmethod
    def block_response(self) -> typing.Optional["DnsBlockResponse"]:
        '''(experimental) The way that you want DNS Firewall to block the request.

        :stability: experimental
        '''
        ...


class _FirewallRuleActionProxy(FirewallRuleAction):
    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        '''(experimental) The action that DNS Firewall should take on a DNS query when it matches one of the domains in the rule's domain list.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="blockResponse")
    def block_response(self) -> typing.Optional["DnsBlockResponse"]:
        '''(experimental) The way that you want DNS Firewall to block the request.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["DnsBlockResponse"], jsii.get(self, "blockResponse"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, FirewallRuleAction).__jsii_proxy_class__ = lambda : _FirewallRuleActionProxy


class FirewallRuleGroupAssociation(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-route53resolver-alpha.FirewallRuleGroupAssociation",
):
    '''(experimental) A Firewall Rule Group Association.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_route53resolver_alpha as route53resolver_alpha
        from aws_cdk import aws_ec2 as ec2
        
        # firewall_rule_group: route53resolver_alpha.FirewallRuleGroup
        # vpc: ec2.Vpc
        
        firewall_rule_group_association = route53resolver_alpha.FirewallRuleGroupAssociation(self, "MyFirewallRuleGroupAssociation",
            firewall_rule_group=firewall_rule_group,
            priority=123,
            vpc=vpc,
        
            # the properties below are optional
            mutation_protection=False,
            name="name"
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        firewall_rule_group: "IFirewallRuleGroup",
        priority: jsii.Number,
        vpc: "_aws_cdk_aws_ec2_ceddda9d.IVpc",
        mutation_protection: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param firewall_rule_group: (experimental) The firewall rule group which must be associated.
        :param priority: (experimental) The setting that determines the processing order of the rule group among the rule groups that are associated with a single VPC. DNS Firewall filters VPC traffic starting from rule group with the lowest numeric priority setting. This value must be greater than 100 and less than 9,000
        :param vpc: (experimental) The VPC that to associate with the rule group.
        :param mutation_protection: (experimental) If enabled, this setting disallows modification or removal of the association, to help prevent against accidentally altering DNS firewall protections. Default: true
        :param name: (experimental) The name of the association. Default: - a CloudFormation generated name

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__66db44623853cec6127559e80b1ff37cd188ae6bb06e46d5500ca10c786695ec)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FirewallRuleGroupAssociationProps(
            firewall_rule_group=firewall_rule_group,
            priority=priority,
            vpc=vpc,
            mutation_protection=mutation_protection,
            name=name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupAssociationArn")
    def firewall_rule_group_association_arn(self) -> builtins.str:
        '''(experimental) The ARN (Amazon Resource Name) of the association.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupAssociationArn"))

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupAssociationCreationTime")
    def firewall_rule_group_association_creation_time(self) -> builtins.str:
        '''(experimental) The date and time that the association was created.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupAssociationCreationTime"))

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupAssociationCreatorRequestId")
    def firewall_rule_group_association_creator_request_id(self) -> builtins.str:
        '''(experimental) The creator request ID.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupAssociationCreatorRequestId"))

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupAssociationId")
    def firewall_rule_group_association_id(self) -> builtins.str:
        '''(experimental) The ID of the association.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupAssociationId"))

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupAssociationManagedOwnerName")
    def firewall_rule_group_association_managed_owner_name(self) -> builtins.str:
        '''(experimental) The owner of the association, used only for lists that are not managed by you.

        If you use AWS Firewall Manager to manage your firewalls from DNS Firewall,
        then this reports Firewall Manager as the managed owner.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupAssociationManagedOwnerName"))

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupAssociationModificationTime")
    def firewall_rule_group_association_modification_time(self) -> builtins.str:
        '''(experimental) The date and time that the association was last modified.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupAssociationModificationTime"))

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupAssociationStatus")
    def firewall_rule_group_association_status(self) -> builtins.str:
        '''(experimental) The status of the association.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupAssociationStatus"))

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupAssociationStatusMessage")
    def firewall_rule_group_association_status_message(self) -> builtins.str:
        '''(experimental) Additional information about the status of the association.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupAssociationStatusMessage"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-route53resolver-alpha.FirewallRuleGroupAssociationOptions",
    jsii_struct_bases=[],
    name_mapping={
        "priority": "priority",
        "vpc": "vpc",
        "mutation_protection": "mutationProtection",
        "name": "name",
    },
)
class FirewallRuleGroupAssociationOptions:
    def __init__(
        self,
        *,
        priority: jsii.Number,
        vpc: "_aws_cdk_aws_ec2_ceddda9d.IVpc",
        mutation_protection: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for a Firewall Rule Group Association.

        :param priority: (experimental) The setting that determines the processing order of the rule group among the rule groups that are associated with a single VPC. DNS Firewall filters VPC traffic starting from rule group with the lowest numeric priority setting. This value must be greater than 100 and less than 9,000
        :param vpc: (experimental) The VPC that to associate with the rule group.
        :param mutation_protection: (experimental) If enabled, this setting disallows modification or removal of the association, to help prevent against accidentally altering DNS firewall protections. Default: true
        :param name: (experimental) The name of the association. Default: - a CloudFormation generated name

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_ec2 as ec2
            
            # rule_group: route53resolver.FirewallRuleGroup
            # my_vpc: ec2.Vpc
            
            
            rule_group.associate("Association",
                priority=101,
                vpc=my_vpc
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d760432d87440f1d9d763a89518f2699a8f5ebc2f80e4eee0cad66fb9d945d0e)
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument mutation_protection", value=mutation_protection, expected_type=type_hints["mutation_protection"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "priority": priority,
            "vpc": vpc,
        }
        if mutation_protection is not None:
            self._values["mutation_protection"] = mutation_protection
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def priority(self) -> jsii.Number:
        '''(experimental) The setting that determines the processing order of the rule group among the rule groups that are associated with a single VPC.

        DNS Firewall filters VPC
        traffic starting from rule group with the lowest numeric priority setting.

        This value must be greater than 100 and less than 9,000

        :stability: experimental
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def vpc(self) -> "_aws_cdk_aws_ec2_ceddda9d.IVpc":
        '''(experimental) The VPC that to associate with the rule group.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast("_aws_cdk_aws_ec2_ceddda9d.IVpc", result)

    @builtins.property
    def mutation_protection(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If enabled, this setting disallows modification or removal of the association, to help prevent against accidentally altering DNS firewall protections.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("mutation_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the association.

        :default: - a CloudFormation generated name

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirewallRuleGroupAssociationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-route53resolver-alpha.FirewallRuleGroupAssociationProps",
    jsii_struct_bases=[FirewallRuleGroupAssociationOptions],
    name_mapping={
        "priority": "priority",
        "vpc": "vpc",
        "mutation_protection": "mutationProtection",
        "name": "name",
        "firewall_rule_group": "firewallRuleGroup",
    },
)
class FirewallRuleGroupAssociationProps(FirewallRuleGroupAssociationOptions):
    def __init__(
        self,
        *,
        priority: jsii.Number,
        vpc: "_aws_cdk_aws_ec2_ceddda9d.IVpc",
        mutation_protection: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        firewall_rule_group: "IFirewallRuleGroup",
    ) -> None:
        '''(experimental) Properties for a Firewall Rule Group Association.

        :param priority: (experimental) The setting that determines the processing order of the rule group among the rule groups that are associated with a single VPC. DNS Firewall filters VPC traffic starting from rule group with the lowest numeric priority setting. This value must be greater than 100 and less than 9,000
        :param vpc: (experimental) The VPC that to associate with the rule group.
        :param mutation_protection: (experimental) If enabled, this setting disallows modification or removal of the association, to help prevent against accidentally altering DNS firewall protections. Default: true
        :param name: (experimental) The name of the association. Default: - a CloudFormation generated name
        :param firewall_rule_group: (experimental) The firewall rule group which must be associated.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_route53resolver_alpha as route53resolver_alpha
            from aws_cdk import aws_ec2 as ec2
            
            # firewall_rule_group: route53resolver_alpha.FirewallRuleGroup
            # vpc: ec2.Vpc
            
            firewall_rule_group_association_props = route53resolver_alpha.FirewallRuleGroupAssociationProps(
                firewall_rule_group=firewall_rule_group,
                priority=123,
                vpc=vpc,
            
                # the properties below are optional
                mutation_protection=False,
                name="name"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__83da411f10ecd4b598d0ba8241ed0a5eb15f93d3bedcf56bea32403113edff28)
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument mutation_protection", value=mutation_protection, expected_type=type_hints["mutation_protection"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument firewall_rule_group", value=firewall_rule_group, expected_type=type_hints["firewall_rule_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "priority": priority,
            "vpc": vpc,
            "firewall_rule_group": firewall_rule_group,
        }
        if mutation_protection is not None:
            self._values["mutation_protection"] = mutation_protection
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def priority(self) -> jsii.Number:
        '''(experimental) The setting that determines the processing order of the rule group among the rule groups that are associated with a single VPC.

        DNS Firewall filters VPC
        traffic starting from rule group with the lowest numeric priority setting.

        This value must be greater than 100 and less than 9,000

        :stability: experimental
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def vpc(self) -> "_aws_cdk_aws_ec2_ceddda9d.IVpc":
        '''(experimental) The VPC that to associate with the rule group.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast("_aws_cdk_aws_ec2_ceddda9d.IVpc", result)

    @builtins.property
    def mutation_protection(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If enabled, this setting disallows modification or removal of the association, to help prevent against accidentally altering DNS firewall protections.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("mutation_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the association.

        :default: - a CloudFormation generated name

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firewall_rule_group(self) -> "IFirewallRuleGroup":
        '''(experimental) The firewall rule group which must be associated.

        :stability: experimental
        '''
        result = self._values.get("firewall_rule_group")
        assert result is not None, "Required property 'firewall_rule_group' is missing"
        return typing.cast("IFirewallRuleGroup", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirewallRuleGroupAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-route53resolver-alpha.FirewallRuleGroupProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "rules": "rules"},
)
class FirewallRuleGroupProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        rules: typing.Optional[typing.Sequence[typing.Union["FirewallRule", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Properties for a Firewall Rule Group.

        :param name: (experimental) The name of the rule group. Default: - a CloudFormation generated name
        :param rules: (experimental) A list of rules for this group. Default: - no rules

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # my_block_list: route53resolver.FirewallDomainList
            
            route53resolver.FirewallRuleGroup(self, "RuleGroup",
                rules=[route53resolver.FirewallRule(
                    priority=10,
                    firewall_domain_list=my_block_list,
                    # block and reply with NODATA
                    action=route53resolver.FirewallRuleAction.block()
                )
                ]
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__7bcc990fe1d7f82a8c07b96a7a276e0306150596cdae07e9a310ee5702d9e9dd)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if rules is not None:
            self._values["rules"] = rules

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the rule group.

        :default: - a CloudFormation generated name

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rules(self) -> typing.Optional[typing.List["FirewallRule"]]:
        '''(experimental) A list of rules for this group.

        :default: - no rules

        :stability: experimental
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.List["FirewallRule"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirewallRuleGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-route53resolver-alpha.IFirewallDomainList")
class IFirewallDomainList(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) A Firewall Domain List.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="firewallDomainListId")
    def firewall_domain_list_id(self) -> builtins.str:
        '''(experimental) The ID of the domain list.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IFirewallDomainListProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) A Firewall Domain List.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-route53resolver-alpha.IFirewallDomainList"

    @builtins.property
    @jsii.member(jsii_name="firewallDomainListId")
    def firewall_domain_list_id(self) -> builtins.str:
        '''(experimental) The ID of the domain list.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallDomainListId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFirewallDomainList).__jsii_proxy_class__ = lambda : _IFirewallDomainListProxy


@jsii.interface(jsii_type="@aws-cdk/aws-route53resolver-alpha.IFirewallRuleGroup")
class IFirewallRuleGroup(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) A Firewall Rule Group.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupId")
    def firewall_rule_group_id(self) -> builtins.str:
        '''(experimental) The ID of the rule group.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IFirewallRuleGroupProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) A Firewall Rule Group.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-route53resolver-alpha.IFirewallRuleGroup"

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupId")
    def firewall_rule_group_id(self) -> builtins.str:
        '''(experimental) The ID of the rule group.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFirewallRuleGroup).__jsii_proxy_class__ = lambda : _IFirewallRuleGroupProxy


@jsii.implements(IFirewallDomainList)
class FirewallDomainList(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-route53resolver-alpha.FirewallDomainList",
):
    '''(experimental) A Firewall Domain List.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        block_list = route53resolver.FirewallDomainList(self, "BlockList",
            domains=route53resolver.FirewallDomains.from_list(["bad-domain.com", "bot-domain.net"])
        )
        
        s3_list = route53resolver.FirewallDomainList(self, "S3List",
            domains=route53resolver.FirewallDomains.from_s3_url("s3://bucket/prefix/object")
        )
        
        asset_list = route53resolver.FirewallDomainList(self, "AssetList",
            domains=route53resolver.FirewallDomains.from_asset("/path/to/domains.txt")
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        domains: "FirewallDomains",
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param domains: (experimental) A list of domains.
        :param name: (experimental) A name for the domain list. Default: - a CloudFormation generated name

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d88ae2f1abdd515eaaf6c8c66d5625be7fdc658b36001fd0e165ea83b038320a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FirewallDomainListProps(domains=domains, name=name)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromFirewallDomainListId")
    @builtins.classmethod
    def from_firewall_domain_list_id(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        firewall_domain_list_id: builtins.str,
    ) -> "IFirewallDomainList":
        '''(experimental) Import an existing Firewall Rule Group.

        :param scope: -
        :param id: -
        :param firewall_domain_list_id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__9fac64f1151d9c654325fa60b63a3266f027fcfdd0f27cfc7dd25dca3626062d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument firewall_domain_list_id", value=firewall_domain_list_id, expected_type=type_hints["firewall_domain_list_id"])
        return typing.cast("IFirewallDomainList", jsii.sinvoke(cls, "fromFirewallDomainListId", [scope, id, firewall_domain_list_id]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="firewallDomainListArn")
    def firewall_domain_list_arn(self) -> builtins.str:
        '''(experimental) The ARN (Amazon Resource Name) of the domain list.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallDomainListArn"))

    @builtins.property
    @jsii.member(jsii_name="firewallDomainListCreationTime")
    def firewall_domain_list_creation_time(self) -> builtins.str:
        '''(experimental) The date and time that the domain list was created.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallDomainListCreationTime"))

    @builtins.property
    @jsii.member(jsii_name="firewallDomainListCreatorRequestId")
    def firewall_domain_list_creator_request_id(self) -> builtins.str:
        '''(experimental) The creator request ID.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallDomainListCreatorRequestId"))

    @builtins.property
    @jsii.member(jsii_name="firewallDomainListDomainCount")
    def firewall_domain_list_domain_count(self) -> jsii.Number:
        '''(experimental) The number of domains in the list.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(jsii.Number, jsii.get(self, "firewallDomainListDomainCount"))

    @builtins.property
    @jsii.member(jsii_name="firewallDomainListId")
    def firewall_domain_list_id(self) -> builtins.str:
        '''(experimental) The ID of the domain list.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallDomainListId"))

    @builtins.property
    @jsii.member(jsii_name="firewallDomainListManagedOwnerName")
    def firewall_domain_list_managed_owner_name(self) -> builtins.str:
        '''(experimental) The owner of the list, used only for lists that are not managed by you.

        For example, the managed domain list ``AWSManagedDomainsMalwareDomainList``
        has the managed owner name ``Route 53 Resolver DNS Firewall``.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallDomainListManagedOwnerName"))

    @builtins.property
    @jsii.member(jsii_name="firewallDomainListModificationTime")
    def firewall_domain_list_modification_time(self) -> builtins.str:
        '''(experimental) The date and time that the domain list was last modified.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallDomainListModificationTime"))

    @builtins.property
    @jsii.member(jsii_name="firewallDomainListStatus")
    def firewall_domain_list_status(self) -> builtins.str:
        '''(experimental) The status of the domain list.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallDomainListStatus"))

    @builtins.property
    @jsii.member(jsii_name="firewallDomainListStatusMessage")
    def firewall_domain_list_status_message(self) -> builtins.str:
        '''(experimental) Additional information about the status of the rule group.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallDomainListStatusMessage"))


@jsii.implements(IFirewallRuleGroup)
class FirewallRuleGroup(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-route53resolver-alpha.FirewallRuleGroup",
):
    '''(experimental) A Firewall Rule Group.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # my_block_list: route53resolver.FirewallDomainList
        
        route53resolver.FirewallRuleGroup(self, "RuleGroup",
            rules=[route53resolver.FirewallRule(
                priority=10,
                firewall_domain_list=my_block_list,
                # block and reply with NODATA
                action=route53resolver.FirewallRuleAction.block()
            )
            ]
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        name: typing.Optional[builtins.str] = None,
        rules: typing.Optional[typing.Sequence[typing.Union["FirewallRule", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param name: (experimental) The name of the rule group. Default: - a CloudFormation generated name
        :param rules: (experimental) A list of rules for this group. Default: - no rules

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1cb24fa06a6d2f6631fd2f617858f3d92eba8ac1220751022ff38d3f87a6db20)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FirewallRuleGroupProps(name=name, rules=rules)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromFirewallRuleGroupId")
    @builtins.classmethod
    def from_firewall_rule_group_id(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        firewall_rule_group_id: builtins.str,
    ) -> "IFirewallRuleGroup":
        '''(experimental) Import an existing Firewall Rule Group.

        :param scope: -
        :param id: -
        :param firewall_rule_group_id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6af1f0d9981b2568b1050e7796f1a1b81df83547efa007299f4de89a58871c08)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument firewall_rule_group_id", value=firewall_rule_group_id, expected_type=type_hints["firewall_rule_group_id"])
        return typing.cast("IFirewallRuleGroup", jsii.sinvoke(cls, "fromFirewallRuleGroupId", [scope, id, firewall_rule_group_id]))

    @jsii.member(jsii_name="addRule")
    def add_rule(
        self,
        *,
        action: "FirewallRuleAction",
        firewall_domain_list: "IFirewallDomainList",
        priority: jsii.Number,
    ) -> "FirewallRuleGroup":
        '''(experimental) Adds a rule to this group.

        :param action: (experimental) The action for this rule.
        :param firewall_domain_list: (experimental) The domain list for this rule.
        :param priority: (experimental) The priority of the rule in the rule group. This value must be unique within the rule group.

        :stability: experimental
        '''
        rule = FirewallRule(
            action=action, firewall_domain_list=firewall_domain_list, priority=priority
        )

        return typing.cast("FirewallRuleGroup", jsii.invoke(self, "addRule", [rule]))

    @jsii.member(jsii_name="associate")
    def associate(
        self,
        id: builtins.str,
        *,
        priority: jsii.Number,
        vpc: "_aws_cdk_aws_ec2_ceddda9d.IVpc",
        mutation_protection: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> "FirewallRuleGroupAssociation":
        '''(experimental) Associates this Firewall Rule Group with a VPC.

        :param id: -
        :param priority: (experimental) The setting that determines the processing order of the rule group among the rule groups that are associated with a single VPC. DNS Firewall filters VPC traffic starting from rule group with the lowest numeric priority setting. This value must be greater than 100 and less than 9,000
        :param vpc: (experimental) The VPC that to associate with the rule group.
        :param mutation_protection: (experimental) If enabled, this setting disallows modification or removal of the association, to help prevent against accidentally altering DNS firewall protections. Default: true
        :param name: (experimental) The name of the association. Default: - a CloudFormation generated name

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__2c7f8452576eb937895dbebdfe9c7ae375ecabfafd5e215cbfec8b69ad2074d2)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FirewallRuleGroupAssociationOptions(
            priority=priority,
            vpc=vpc,
            mutation_protection=mutation_protection,
            name=name,
        )

        return typing.cast("FirewallRuleGroupAssociation", jsii.invoke(self, "associate", [id, props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupArn")
    def firewall_rule_group_arn(self) -> builtins.str:
        '''(experimental) The ARN (Amazon Resource Name) of the rule group.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupCreationTime")
    def firewall_rule_group_creation_time(self) -> builtins.str:
        '''(experimental) The date and time that the rule group was created.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupCreationTime"))

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupCreatorRequestId")
    def firewall_rule_group_creator_request_id(self) -> builtins.str:
        '''(experimental) The creator request ID.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupCreatorRequestId"))

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupId")
    def firewall_rule_group_id(self) -> builtins.str:
        '''(experimental) The ID of the rule group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupId"))

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupModificationTime")
    def firewall_rule_group_modification_time(self) -> builtins.str:
        '''(experimental) The date and time that the rule group was last modified.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupModificationTime"))

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupOwnerId")
    def firewall_rule_group_owner_id(self) -> builtins.str:
        '''(experimental) The AWS account ID for the account that created the rule group.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupOwnerId"))

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupRuleCount")
    def firewall_rule_group_rule_count(self) -> jsii.Number:
        '''(experimental) The number of rules in the rule group.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(jsii.Number, jsii.get(self, "firewallRuleGroupRuleCount"))

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupShareStatus")
    def firewall_rule_group_share_status(self) -> builtins.str:
        '''(experimental) Whether the rule group is shared with other AWS accounts, or was shared with the current account by another AWS account.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupShareStatus"))

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupStatus")
    def firewall_rule_group_status(self) -> builtins.str:
        '''(experimental) The status of the rule group.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupStatus"))

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupStatusMessage")
    def firewall_rule_group_status_message(self) -> builtins.str:
        '''(experimental) Additional information about the status of the rule group.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupStatusMessage"))


__all__ = [
    "DnsBlockResponse",
    "DomainsConfig",
    "FirewallDomainList",
    "FirewallDomainListProps",
    "FirewallDomains",
    "FirewallRule",
    "FirewallRuleAction",
    "FirewallRuleGroup",
    "FirewallRuleGroupAssociation",
    "FirewallRuleGroupAssociationOptions",
    "FirewallRuleGroupAssociationProps",
    "FirewallRuleGroupProps",
    "IFirewallDomainList",
    "IFirewallRuleGroup",
]

publication.publish()

def _typecheckingstub__bcc6e5cbcbf161b026004146d290f4c2c5203dd60e43bb296ae451b7ea8afb50(
    domain: builtins.str,
    ttl: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efcc739bead6cd1e2f6028bbf509537b88cdaab217e4ad29abcb83010af732aa(
    *,
    domain_file_url: typing.Optional[builtins.str] = None,
    domains: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2694ecc77bbdf59285a53d044c17b801083d48fd6d9cf26c5798be8ef83cfd4(
    *,
    domains: FirewallDomains,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7b0d1079af5d8eb8466e6719de93c31cc9a02bfc3b4b058593e609db394d240(
    asset_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4db439b64de98348184f5457d37416fdf39df7bfa653f43e5546f736c932c7ba(
    list: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9123f4606e1c6eda8fc3b706939d87b0209c2bea457af92c0af2a946a6684d64(
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f74514d1763b172a7f7f23feabbb8360b780c1b88c0e33c8dd934f2542a42db(
    url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beee843294402bd0b4634b78a18a987c0d888a0afb182d42637c4bf1d18c0908(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c842a13b2d3ff276f74958de9ce814eafca72f45f15296caa8cf78d6ad8c39a5(
    *,
    action: FirewallRuleAction,
    firewall_domain_list: IFirewallDomainList,
    priority: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__908212340f1ac128d44306136d4c2b8737eeff37eab2b68c781cfb8d7345f036(
    response: typing.Optional[DnsBlockResponse] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66db44623853cec6127559e80b1ff37cd188ae6bb06e46d5500ca10c786695ec(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    firewall_rule_group: IFirewallRuleGroup,
    priority: jsii.Number,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    mutation_protection: typing.Optional[builtins.bool] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d760432d87440f1d9d763a89518f2699a8f5ebc2f80e4eee0cad66fb9d945d0e(
    *,
    priority: jsii.Number,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    mutation_protection: typing.Optional[builtins.bool] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83da411f10ecd4b598d0ba8241ed0a5eb15f93d3bedcf56bea32403113edff28(
    *,
    priority: jsii.Number,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    mutation_protection: typing.Optional[builtins.bool] = None,
    name: typing.Optional[builtins.str] = None,
    firewall_rule_group: IFirewallRuleGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bcc990fe1d7f82a8c07b96a7a276e0306150596cdae07e9a310ee5702d9e9dd(
    *,
    name: typing.Optional[builtins.str] = None,
    rules: typing.Optional[typing.Sequence[typing.Union[FirewallRule, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d88ae2f1abdd515eaaf6c8c66d5625be7fdc658b36001fd0e165ea83b038320a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    domains: FirewallDomains,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fac64f1151d9c654325fa60b63a3266f027fcfdd0f27cfc7dd25dca3626062d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    firewall_domain_list_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cb24fa06a6d2f6631fd2f617858f3d92eba8ac1220751022ff38d3f87a6db20(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: typing.Optional[builtins.str] = None,
    rules: typing.Optional[typing.Sequence[typing.Union[FirewallRule, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6af1f0d9981b2568b1050e7796f1a1b81df83547efa007299f4de89a58871c08(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    firewall_rule_group_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c7f8452576eb937895dbebdfe9c7ae375ecabfafd5e215cbfec8b69ad2074d2(
    id: builtins.str,
    *,
    priority: jsii.Number,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    mutation_protection: typing.Optional[builtins.bool] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

for cls in [IFirewallDomainList, IFirewallRuleGroup]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
