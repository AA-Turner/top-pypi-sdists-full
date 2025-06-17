r'''
# `pagerduty_jira_cloud_account_mapping_rule`

Refer to the Terraform Registry for docs: [`pagerduty_jira_cloud_account_mapping_rule`](https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule).
'''
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

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class JiraCloudAccountMappingRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.jiraCloudAccountMappingRule.JiraCloudAccountMappingRule",
):
    '''Represents a {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule pagerduty_jira_cloud_account_mapping_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account_mapping: builtins.str,
        name: builtins.str,
        config: typing.Optional[typing.Union["JiraCloudAccountMappingRuleConfigA", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule pagerduty_jira_cloud_account_mapping_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_mapping: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#account_mapping JiraCloudAccountMappingRule#account_mapping}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#name JiraCloudAccountMappingRule#name}.
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#config JiraCloudAccountMappingRule#config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afb506592aab04542eeba94fad9980f8722b05c5ead54c17e81ffc5f011766d5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config_ = JiraCloudAccountMappingRuleConfig(
            account_mapping=account_mapping,
            name=name,
            config=config,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config_])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a JiraCloudAccountMappingRule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the JiraCloudAccountMappingRule to import.
        :param import_from_id: The id of the existing JiraCloudAccountMappingRule that should be imported. Refer to the {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the JiraCloudAccountMappingRule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a39d3a40dac458599e0cdbae10045d2667bed4da31bc875d42731c5ada8bf702)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putConfig")
    def put_config(
        self,
        *,
        service: builtins.str,
        jira: typing.Optional[typing.Union["JiraCloudAccountMappingRuleConfigJira", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param service: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#service JiraCloudAccountMappingRule#service}.
        :param jira: jira block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#jira JiraCloudAccountMappingRule#jira}
        '''
        value = JiraCloudAccountMappingRuleConfigA(service=service, jira=jira)

        return typing.cast(None, jsii.invoke(self, "putConfig", [value]))

    @jsii.member(jsii_name="resetConfig")
    def reset_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfig", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="autocreateJqlDisabledReason")
    def autocreate_jql_disabled_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autocreateJqlDisabledReason"))

    @builtins.property
    @jsii.member(jsii_name="autocreateJqlDisabledUntil")
    def autocreate_jql_disabled_until(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autocreateJqlDisabledUntil"))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> "JiraCloudAccountMappingRuleConfigAOutputReference":
        return typing.cast("JiraCloudAccountMappingRuleConfigAOutputReference", jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="accountMappingInput")
    def account_mapping_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountMappingInput"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "JiraCloudAccountMappingRuleConfigA"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "JiraCloudAccountMappingRuleConfigA"]], jsii.get(self, "configInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="accountMapping")
    def account_mapping(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountMapping"))

    @account_mapping.setter
    def account_mapping(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b4a98c4e119426d4b92e43d09f219dbd9d06e322581dfd2300858e37d9aa61b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountMapping", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__494f780c921e1a15a4e8e54e47b5a5174950da7e587c2d18e7156e481dd93b66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.jiraCloudAccountMappingRule.JiraCloudAccountMappingRuleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "account_mapping": "accountMapping",
        "name": "name",
        "config": "config",
    },
)
class JiraCloudAccountMappingRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        account_mapping: builtins.str,
        name: builtins.str,
        config: typing.Optional[typing.Union["JiraCloudAccountMappingRuleConfigA", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param account_mapping: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#account_mapping JiraCloudAccountMappingRule#account_mapping}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#name JiraCloudAccountMappingRule#name}.
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#config JiraCloudAccountMappingRule#config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(config, dict):
            config = JiraCloudAccountMappingRuleConfigA(**config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a4485e15c0e1d1b8c578751b283cf1a0fc196866c77daedb975549f5dc26022)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument account_mapping", value=account_mapping, expected_type=type_hints["account_mapping"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_mapping": account_mapping,
            "name": name,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if config is not None:
            self._values["config"] = config

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def account_mapping(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#account_mapping JiraCloudAccountMappingRule#account_mapping}.'''
        result = self._values.get("account_mapping")
        assert result is not None, "Required property 'account_mapping' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#name JiraCloudAccountMappingRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def config(self) -> typing.Optional["JiraCloudAccountMappingRuleConfigA"]:
        '''config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#config JiraCloudAccountMappingRule#config}
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional["JiraCloudAccountMappingRuleConfigA"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JiraCloudAccountMappingRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.jiraCloudAccountMappingRule.JiraCloudAccountMappingRuleConfigA",
    jsii_struct_bases=[],
    name_mapping={"service": "service", "jira": "jira"},
)
class JiraCloudAccountMappingRuleConfigA:
    def __init__(
        self,
        *,
        service: builtins.str,
        jira: typing.Optional[typing.Union["JiraCloudAccountMappingRuleConfigJira", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param service: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#service JiraCloudAccountMappingRule#service}.
        :param jira: jira block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#jira JiraCloudAccountMappingRule#jira}
        '''
        if isinstance(jira, dict):
            jira = JiraCloudAccountMappingRuleConfigJira(**jira)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f34ccb50de9de421d723002c9619ed94f416c8f90b267f2ea55fa97c2ffc330c)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument jira", value=jira, expected_type=type_hints["jira"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service": service,
        }
        if jira is not None:
            self._values["jira"] = jira

    @builtins.property
    def service(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#service JiraCloudAccountMappingRule#service}.'''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def jira(self) -> typing.Optional["JiraCloudAccountMappingRuleConfigJira"]:
        '''jira block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#jira JiraCloudAccountMappingRule#jira}
        '''
        result = self._values.get("jira")
        return typing.cast(typing.Optional["JiraCloudAccountMappingRuleConfigJira"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JiraCloudAccountMappingRuleConfigA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class JiraCloudAccountMappingRuleConfigAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.jiraCloudAccountMappingRule.JiraCloudAccountMappingRuleConfigAOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__715a1df3264e416b5855b7fbbabd836c4acb51d18e4f9187c7b43985a0d2052f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putJira")
    def put_jira(
        self,
        *,
        issue_type: typing.Union["JiraCloudAccountMappingRuleConfigJiraIssueType", typing.Dict[builtins.str, typing.Any]],
        project: typing.Union["JiraCloudAccountMappingRuleConfigJiraProject", typing.Dict[builtins.str, typing.Any]],
        autocreate_jql: typing.Optional[builtins.str] = None,
        create_issue_on_incident_trigger: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        custom_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["JiraCloudAccountMappingRuleConfigJiraCustomFields", typing.Dict[builtins.str, typing.Any]]]]] = None,
        priorities: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["JiraCloudAccountMappingRuleConfigJiraPriorities", typing.Dict[builtins.str, typing.Any]]]]] = None,
        status_mapping: typing.Optional[typing.Union["JiraCloudAccountMappingRuleConfigJiraStatusMapping", typing.Dict[builtins.str, typing.Any]]] = None,
        sync_notes_user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param issue_type: issue_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#issue_type JiraCloudAccountMappingRule#issue_type}
        :param project: project block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#project JiraCloudAccountMappingRule#project}
        :param autocreate_jql: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#autocreate_jql JiraCloudAccountMappingRule#autocreate_jql}.
        :param create_issue_on_incident_trigger: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#create_issue_on_incident_trigger JiraCloudAccountMappingRule#create_issue_on_incident_trigger}.
        :param custom_fields: custom_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#custom_fields JiraCloudAccountMappingRule#custom_fields}
        :param priorities: priorities block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#priorities JiraCloudAccountMappingRule#priorities}
        :param status_mapping: status_mapping block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#status_mapping JiraCloudAccountMappingRule#status_mapping}
        :param sync_notes_user: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#sync_notes_user JiraCloudAccountMappingRule#sync_notes_user}.
        '''
        value = JiraCloudAccountMappingRuleConfigJira(
            issue_type=issue_type,
            project=project,
            autocreate_jql=autocreate_jql,
            create_issue_on_incident_trigger=create_issue_on_incident_trigger,
            custom_fields=custom_fields,
            priorities=priorities,
            status_mapping=status_mapping,
            sync_notes_user=sync_notes_user,
        )

        return typing.cast(None, jsii.invoke(self, "putJira", [value]))

    @jsii.member(jsii_name="resetJira")
    def reset_jira(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJira", []))

    @builtins.property
    @jsii.member(jsii_name="jira")
    def jira(self) -> "JiraCloudAccountMappingRuleConfigJiraOutputReference":
        return typing.cast("JiraCloudAccountMappingRuleConfigJiraOutputReference", jsii.get(self, "jira"))

    @builtins.property
    @jsii.member(jsii_name="jiraInput")
    def jira_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "JiraCloudAccountMappingRuleConfigJira"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "JiraCloudAccountMappingRuleConfigJira"]], jsii.get(self, "jiraInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5263d0c1a2eded6d235c9a48bca6c6e59ac6f3a770edad1c67e179447552f384)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigA]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigA]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigA]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a365cf19b76617e33405e399b208a72d90beb9c8bb8580ddfa1d89dac6d850a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.jiraCloudAccountMappingRule.JiraCloudAccountMappingRuleConfigJira",
    jsii_struct_bases=[],
    name_mapping={
        "issue_type": "issueType",
        "project": "project",
        "autocreate_jql": "autocreateJql",
        "create_issue_on_incident_trigger": "createIssueOnIncidentTrigger",
        "custom_fields": "customFields",
        "priorities": "priorities",
        "status_mapping": "statusMapping",
        "sync_notes_user": "syncNotesUser",
    },
)
class JiraCloudAccountMappingRuleConfigJira:
    def __init__(
        self,
        *,
        issue_type: typing.Union["JiraCloudAccountMappingRuleConfigJiraIssueType", typing.Dict[builtins.str, typing.Any]],
        project: typing.Union["JiraCloudAccountMappingRuleConfigJiraProject", typing.Dict[builtins.str, typing.Any]],
        autocreate_jql: typing.Optional[builtins.str] = None,
        create_issue_on_incident_trigger: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        custom_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["JiraCloudAccountMappingRuleConfigJiraCustomFields", typing.Dict[builtins.str, typing.Any]]]]] = None,
        priorities: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["JiraCloudAccountMappingRuleConfigJiraPriorities", typing.Dict[builtins.str, typing.Any]]]]] = None,
        status_mapping: typing.Optional[typing.Union["JiraCloudAccountMappingRuleConfigJiraStatusMapping", typing.Dict[builtins.str, typing.Any]]] = None,
        sync_notes_user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param issue_type: issue_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#issue_type JiraCloudAccountMappingRule#issue_type}
        :param project: project block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#project JiraCloudAccountMappingRule#project}
        :param autocreate_jql: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#autocreate_jql JiraCloudAccountMappingRule#autocreate_jql}.
        :param create_issue_on_incident_trigger: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#create_issue_on_incident_trigger JiraCloudAccountMappingRule#create_issue_on_incident_trigger}.
        :param custom_fields: custom_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#custom_fields JiraCloudAccountMappingRule#custom_fields}
        :param priorities: priorities block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#priorities JiraCloudAccountMappingRule#priorities}
        :param status_mapping: status_mapping block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#status_mapping JiraCloudAccountMappingRule#status_mapping}
        :param sync_notes_user: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#sync_notes_user JiraCloudAccountMappingRule#sync_notes_user}.
        '''
        if isinstance(issue_type, dict):
            issue_type = JiraCloudAccountMappingRuleConfigJiraIssueType(**issue_type)
        if isinstance(project, dict):
            project = JiraCloudAccountMappingRuleConfigJiraProject(**project)
        if isinstance(status_mapping, dict):
            status_mapping = JiraCloudAccountMappingRuleConfigJiraStatusMapping(**status_mapping)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edf4a70d34cb948fa2b1ceb5d86be813c7689dc0d412af3533d8e45950584b1c)
            check_type(argname="argument issue_type", value=issue_type, expected_type=type_hints["issue_type"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument autocreate_jql", value=autocreate_jql, expected_type=type_hints["autocreate_jql"])
            check_type(argname="argument create_issue_on_incident_trigger", value=create_issue_on_incident_trigger, expected_type=type_hints["create_issue_on_incident_trigger"])
            check_type(argname="argument custom_fields", value=custom_fields, expected_type=type_hints["custom_fields"])
            check_type(argname="argument priorities", value=priorities, expected_type=type_hints["priorities"])
            check_type(argname="argument status_mapping", value=status_mapping, expected_type=type_hints["status_mapping"])
            check_type(argname="argument sync_notes_user", value=sync_notes_user, expected_type=type_hints["sync_notes_user"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "issue_type": issue_type,
            "project": project,
        }
        if autocreate_jql is not None:
            self._values["autocreate_jql"] = autocreate_jql
        if create_issue_on_incident_trigger is not None:
            self._values["create_issue_on_incident_trigger"] = create_issue_on_incident_trigger
        if custom_fields is not None:
            self._values["custom_fields"] = custom_fields
        if priorities is not None:
            self._values["priorities"] = priorities
        if status_mapping is not None:
            self._values["status_mapping"] = status_mapping
        if sync_notes_user is not None:
            self._values["sync_notes_user"] = sync_notes_user

    @builtins.property
    def issue_type(self) -> "JiraCloudAccountMappingRuleConfigJiraIssueType":
        '''issue_type block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#issue_type JiraCloudAccountMappingRule#issue_type}
        '''
        result = self._values.get("issue_type")
        assert result is not None, "Required property 'issue_type' is missing"
        return typing.cast("JiraCloudAccountMappingRuleConfigJiraIssueType", result)

    @builtins.property
    def project(self) -> "JiraCloudAccountMappingRuleConfigJiraProject":
        '''project block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#project JiraCloudAccountMappingRule#project}
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast("JiraCloudAccountMappingRuleConfigJiraProject", result)

    @builtins.property
    def autocreate_jql(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#autocreate_jql JiraCloudAccountMappingRule#autocreate_jql}.'''
        result = self._values.get("autocreate_jql")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def create_issue_on_incident_trigger(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#create_issue_on_incident_trigger JiraCloudAccountMappingRule#create_issue_on_incident_trigger}.'''
        result = self._values.get("create_issue_on_incident_trigger")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def custom_fields(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["JiraCloudAccountMappingRuleConfigJiraCustomFields"]]]:
        '''custom_fields block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#custom_fields JiraCloudAccountMappingRule#custom_fields}
        '''
        result = self._values.get("custom_fields")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["JiraCloudAccountMappingRuleConfigJiraCustomFields"]]], result)

    @builtins.property
    def priorities(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["JiraCloudAccountMappingRuleConfigJiraPriorities"]]]:
        '''priorities block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#priorities JiraCloudAccountMappingRule#priorities}
        '''
        result = self._values.get("priorities")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["JiraCloudAccountMappingRuleConfigJiraPriorities"]]], result)

    @builtins.property
    def status_mapping(
        self,
    ) -> typing.Optional["JiraCloudAccountMappingRuleConfigJiraStatusMapping"]:
        '''status_mapping block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#status_mapping JiraCloudAccountMappingRule#status_mapping}
        '''
        result = self._values.get("status_mapping")
        return typing.cast(typing.Optional["JiraCloudAccountMappingRuleConfigJiraStatusMapping"], result)

    @builtins.property
    def sync_notes_user(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#sync_notes_user JiraCloudAccountMappingRule#sync_notes_user}.'''
        result = self._values.get("sync_notes_user")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JiraCloudAccountMappingRuleConfigJira(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.jiraCloudAccountMappingRule.JiraCloudAccountMappingRuleConfigJiraCustomFields",
    jsii_struct_bases=[],
    name_mapping={
        "target_issue_field": "targetIssueField",
        "target_issue_field_name": "targetIssueFieldName",
        "type": "type",
        "source_incident_field": "sourceIncidentField",
        "value": "value",
    },
)
class JiraCloudAccountMappingRuleConfigJiraCustomFields:
    def __init__(
        self,
        *,
        target_issue_field: builtins.str,
        target_issue_field_name: builtins.str,
        type: builtins.str,
        source_incident_field: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target_issue_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#target_issue_field JiraCloudAccountMappingRule#target_issue_field}.
        :param target_issue_field_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#target_issue_field_name JiraCloudAccountMappingRule#target_issue_field_name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#type JiraCloudAccountMappingRule#type}.
        :param source_incident_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#source_incident_field JiraCloudAccountMappingRule#source_incident_field}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#value JiraCloudAccountMappingRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84c9a93370e770133f7f52bab7e5fa55ab5fe386edc4ac4314f4cd918cdd99ac)
            check_type(argname="argument target_issue_field", value=target_issue_field, expected_type=type_hints["target_issue_field"])
            check_type(argname="argument target_issue_field_name", value=target_issue_field_name, expected_type=type_hints["target_issue_field_name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument source_incident_field", value=source_incident_field, expected_type=type_hints["source_incident_field"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_issue_field": target_issue_field,
            "target_issue_field_name": target_issue_field_name,
            "type": type,
        }
        if source_incident_field is not None:
            self._values["source_incident_field"] = source_incident_field
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def target_issue_field(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#target_issue_field JiraCloudAccountMappingRule#target_issue_field}.'''
        result = self._values.get("target_issue_field")
        assert result is not None, "Required property 'target_issue_field' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_issue_field_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#target_issue_field_name JiraCloudAccountMappingRule#target_issue_field_name}.'''
        result = self._values.get("target_issue_field_name")
        assert result is not None, "Required property 'target_issue_field_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#type JiraCloudAccountMappingRule#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_incident_field(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#source_incident_field JiraCloudAccountMappingRule#source_incident_field}.'''
        result = self._values.get("source_incident_field")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#value JiraCloudAccountMappingRule#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JiraCloudAccountMappingRuleConfigJiraCustomFields(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class JiraCloudAccountMappingRuleConfigJiraCustomFieldsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.jiraCloudAccountMappingRule.JiraCloudAccountMappingRuleConfigJiraCustomFieldsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bb21863a8762e7be964032c143c278f06a34a5dd2bdde2eb3bc21a4f49ef1e0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "JiraCloudAccountMappingRuleConfigJiraCustomFieldsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2f38334666379bb610e190b45644d65735bc3bb4e762c20a49f2b5b8110d4fe)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("JiraCloudAccountMappingRuleConfigJiraCustomFieldsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14866d57c8e3f7150aed9e4901a01b945f7cebc2552979981b2d897458d48e13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbe4a1c7ee825bc811edbf01c9346f29f32a9a8333dfd5748b64f7b2b606492d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0584cfc9947fd855c3a790a1aae2334de2031ee5cb6aa608fe562ef4a9d10db6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[JiraCloudAccountMappingRuleConfigJiraCustomFields]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[JiraCloudAccountMappingRuleConfigJiraCustomFields]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[JiraCloudAccountMappingRuleConfigJiraCustomFields]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29fcd84179a0797073e1d02b28150fb5127a6bd37559d9efbd3ffb23cc4207c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class JiraCloudAccountMappingRuleConfigJiraCustomFieldsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.jiraCloudAccountMappingRule.JiraCloudAccountMappingRuleConfigJiraCustomFieldsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a948c09b429258d3b3d6fbca86d1957fa2ea948c475bab33271771fcf81f0b0a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSourceIncidentField")
    def reset_source_incident_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceIncidentField", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="sourceIncidentFieldInput")
    def source_incident_field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceIncidentFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="targetIssueFieldInput")
    def target_issue_field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetIssueFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="targetIssueFieldNameInput")
    def target_issue_field_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetIssueFieldNameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceIncidentField")
    def source_incident_field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceIncidentField"))

    @source_incident_field.setter
    def source_incident_field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b895a26672249820648b48bfe821c2f51e7488f0a5168d190e9e263057ad361)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceIncidentField", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetIssueField")
    def target_issue_field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetIssueField"))

    @target_issue_field.setter
    def target_issue_field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d0ca17ab91d434caa69c45f06fdd11e17bdc98738628f11bd063db058b56d08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetIssueField", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetIssueFieldName")
    def target_issue_field_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetIssueFieldName"))

    @target_issue_field_name.setter
    def target_issue_field_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ddf891fae2adeeec9be57d4f3e7643175f1a0f45594156e07ac76eea05d51e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetIssueFieldName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad4c1f3394d17f432e3e700960d3180d7a3d1672d2c806aca34fdd70677c709e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67a6787aa2d0c7d8c680909af37fdfceba32b94c917e4ae2d1ea29315d0fb918)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJiraCustomFields]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJiraCustomFields]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJiraCustomFields]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95fc839b47f15a0376242beecda9a056418e4cb8d3070b8d95dc2544bb985188)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.jiraCloudAccountMappingRule.JiraCloudAccountMappingRuleConfigJiraIssueType",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "name": "name"},
)
class JiraCloudAccountMappingRuleConfigJiraIssueType:
    def __init__(self, *, id: builtins.str, name: builtins.str) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#id JiraCloudAccountMappingRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#name JiraCloudAccountMappingRule#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f5c45e0473724f72edbe36061578d7a309b64651bf7f4494653966ec7b80e91)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "name": name,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#id JiraCloudAccountMappingRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#name JiraCloudAccountMappingRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JiraCloudAccountMappingRuleConfigJiraIssueType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class JiraCloudAccountMappingRuleConfigJiraIssueTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.jiraCloudAccountMappingRule.JiraCloudAccountMappingRuleConfigJiraIssueTypeOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8bf69be5756d7429ff00bedf954ce10b79918ee21077b9ef8c99548ab586a3d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fd693885cbab30c70abc298ba9365d550f882af171fc414f1dd5f82370f26ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6684d0f839687d92b8fa0d67ca01bd5ffa64eab9c07843871e68aed6d53bdf51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJiraIssueType]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJiraIssueType]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJiraIssueType]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6afa47abb5806c8ae3b827ee884532f7cc27f4d75df331be4543ce7cb9252bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class JiraCloudAccountMappingRuleConfigJiraOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.jiraCloudAccountMappingRule.JiraCloudAccountMappingRuleConfigJiraOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7290abbf180f3e6f203a5bcef74cb560a82d0f63df85a66e47e5b89f3e34387)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomFields")
    def put_custom_fields(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[JiraCloudAccountMappingRuleConfigJiraCustomFields, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07c241c0df5d7171b6ec8d20f76264b8ebe9e6644bcac0675443d69227276eea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomFields", [value]))

    @jsii.member(jsii_name="putIssueType")
    def put_issue_type(self, *, id: builtins.str, name: builtins.str) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#id JiraCloudAccountMappingRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#name JiraCloudAccountMappingRule#name}.
        '''
        value = JiraCloudAccountMappingRuleConfigJiraIssueType(id=id, name=name)

        return typing.cast(None, jsii.invoke(self, "putIssueType", [value]))

    @jsii.member(jsii_name="putPriorities")
    def put_priorities(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["JiraCloudAccountMappingRuleConfigJiraPriorities", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__437c272306b1ddb850aaead9c7e35fcdb1a97d1477fa2d6f5361adf079791fe8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPriorities", [value]))

    @jsii.member(jsii_name="putProject")
    def put_project(
        self,
        *,
        id: builtins.str,
        key: builtins.str,
        name: builtins.str,
    ) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#id JiraCloudAccountMappingRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#key JiraCloudAccountMappingRule#key}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#name JiraCloudAccountMappingRule#name}.
        '''
        value = JiraCloudAccountMappingRuleConfigJiraProject(id=id, key=key, name=name)

        return typing.cast(None, jsii.invoke(self, "putProject", [value]))

    @jsii.member(jsii_name="putStatusMapping")
    def put_status_mapping(
        self,
        *,
        triggered: typing.Union["JiraCloudAccountMappingRuleConfigJiraStatusMappingTriggered", typing.Dict[builtins.str, typing.Any]],
        acknowledged: typing.Optional[typing.Union["JiraCloudAccountMappingRuleConfigJiraStatusMappingAcknowledged", typing.Dict[builtins.str, typing.Any]]] = None,
        resolved: typing.Optional[typing.Union["JiraCloudAccountMappingRuleConfigJiraStatusMappingResolved", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param triggered: triggered block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#triggered JiraCloudAccountMappingRule#triggered}
        :param acknowledged: acknowledged block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#acknowledged JiraCloudAccountMappingRule#acknowledged}
        :param resolved: resolved block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#resolved JiraCloudAccountMappingRule#resolved}
        '''
        value = JiraCloudAccountMappingRuleConfigJiraStatusMapping(
            triggered=triggered, acknowledged=acknowledged, resolved=resolved
        )

        return typing.cast(None, jsii.invoke(self, "putStatusMapping", [value]))

    @jsii.member(jsii_name="resetAutocreateJql")
    def reset_autocreate_jql(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutocreateJql", []))

    @jsii.member(jsii_name="resetCreateIssueOnIncidentTrigger")
    def reset_create_issue_on_incident_trigger(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateIssueOnIncidentTrigger", []))

    @jsii.member(jsii_name="resetCustomFields")
    def reset_custom_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomFields", []))

    @jsii.member(jsii_name="resetPriorities")
    def reset_priorities(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriorities", []))

    @jsii.member(jsii_name="resetStatusMapping")
    def reset_status_mapping(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatusMapping", []))

    @jsii.member(jsii_name="resetSyncNotesUser")
    def reset_sync_notes_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncNotesUser", []))

    @builtins.property
    @jsii.member(jsii_name="customFields")
    def custom_fields(self) -> JiraCloudAccountMappingRuleConfigJiraCustomFieldsList:
        return typing.cast(JiraCloudAccountMappingRuleConfigJiraCustomFieldsList, jsii.get(self, "customFields"))

    @builtins.property
    @jsii.member(jsii_name="issueType")
    def issue_type(
        self,
    ) -> JiraCloudAccountMappingRuleConfigJiraIssueTypeOutputReference:
        return typing.cast(JiraCloudAccountMappingRuleConfigJiraIssueTypeOutputReference, jsii.get(self, "issueType"))

    @builtins.property
    @jsii.member(jsii_name="priorities")
    def priorities(self) -> "JiraCloudAccountMappingRuleConfigJiraPrioritiesList":
        return typing.cast("JiraCloudAccountMappingRuleConfigJiraPrioritiesList", jsii.get(self, "priorities"))

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> "JiraCloudAccountMappingRuleConfigJiraProjectOutputReference":
        return typing.cast("JiraCloudAccountMappingRuleConfigJiraProjectOutputReference", jsii.get(self, "project"))

    @builtins.property
    @jsii.member(jsii_name="statusMapping")
    def status_mapping(
        self,
    ) -> "JiraCloudAccountMappingRuleConfigJiraStatusMappingOutputReference":
        return typing.cast("JiraCloudAccountMappingRuleConfigJiraStatusMappingOutputReference", jsii.get(self, "statusMapping"))

    @builtins.property
    @jsii.member(jsii_name="autocreateJqlInput")
    def autocreate_jql_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autocreateJqlInput"))

    @builtins.property
    @jsii.member(jsii_name="createIssueOnIncidentTriggerInput")
    def create_issue_on_incident_trigger_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "createIssueOnIncidentTriggerInput"))

    @builtins.property
    @jsii.member(jsii_name="customFieldsInput")
    def custom_fields_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[JiraCloudAccountMappingRuleConfigJiraCustomFields]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[JiraCloudAccountMappingRuleConfigJiraCustomFields]]], jsii.get(self, "customFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="issueTypeInput")
    def issue_type_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJiraIssueType]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJiraIssueType]], jsii.get(self, "issueTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="prioritiesInput")
    def priorities_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["JiraCloudAccountMappingRuleConfigJiraPriorities"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["JiraCloudAccountMappingRuleConfigJiraPriorities"]]], jsii.get(self, "prioritiesInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "JiraCloudAccountMappingRuleConfigJiraProject"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "JiraCloudAccountMappingRuleConfigJiraProject"]], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="statusMappingInput")
    def status_mapping_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "JiraCloudAccountMappingRuleConfigJiraStatusMapping"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "JiraCloudAccountMappingRuleConfigJiraStatusMapping"]], jsii.get(self, "statusMappingInput"))

    @builtins.property
    @jsii.member(jsii_name="syncNotesUserInput")
    def sync_notes_user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "syncNotesUserInput"))

    @builtins.property
    @jsii.member(jsii_name="autocreateJql")
    def autocreate_jql(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autocreateJql"))

    @autocreate_jql.setter
    def autocreate_jql(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ee9518b4cb466bb9e395a4b6c532730511b33e33bb8fa38ce659652f67e7ee7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autocreateJql", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createIssueOnIncidentTrigger")
    def create_issue_on_incident_trigger(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "createIssueOnIncidentTrigger"))

    @create_issue_on_incident_trigger.setter
    def create_issue_on_incident_trigger(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a12006567f582e2e0967dcb7edb6c75a4641859729ebce9f6f723d30a0650868)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createIssueOnIncidentTrigger", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncNotesUser")
    def sync_notes_user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncNotesUser"))

    @sync_notes_user.setter
    def sync_notes_user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1abea1f1aed169385c22cc56f53f2a8d19a8ace24f94965a0345c8ed0634978)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncNotesUser", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJira]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJira]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJira]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58947de24fb8c5b487a445da9e841a11eec426b854fac4d7d7cfa96c2bcb257c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.jiraCloudAccountMappingRule.JiraCloudAccountMappingRuleConfigJiraPriorities",
    jsii_struct_bases=[],
    name_mapping={"jira_id": "jiraId", "pagerduty_id": "pagerdutyId"},
)
class JiraCloudAccountMappingRuleConfigJiraPriorities:
    def __init__(self, *, jira_id: builtins.str, pagerduty_id: builtins.str) -> None:
        '''
        :param jira_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#jira_id JiraCloudAccountMappingRule#jira_id}.
        :param pagerduty_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#pagerduty_id JiraCloudAccountMappingRule#pagerduty_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0733d63cf21e384e198f10eaf1b97c133ae536e0f541a777055ef3a5b66fcdbf)
            check_type(argname="argument jira_id", value=jira_id, expected_type=type_hints["jira_id"])
            check_type(argname="argument pagerduty_id", value=pagerduty_id, expected_type=type_hints["pagerduty_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "jira_id": jira_id,
            "pagerduty_id": pagerduty_id,
        }

    @builtins.property
    def jira_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#jira_id JiraCloudAccountMappingRule#jira_id}.'''
        result = self._values.get("jira_id")
        assert result is not None, "Required property 'jira_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pagerduty_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#pagerduty_id JiraCloudAccountMappingRule#pagerduty_id}.'''
        result = self._values.get("pagerduty_id")
        assert result is not None, "Required property 'pagerduty_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JiraCloudAccountMappingRuleConfigJiraPriorities(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class JiraCloudAccountMappingRuleConfigJiraPrioritiesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.jiraCloudAccountMappingRule.JiraCloudAccountMappingRuleConfigJiraPrioritiesList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9496b6d55fd7a97ebe394acbc1d9c751821237b09628ad4a6385868184c9cb70)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "JiraCloudAccountMappingRuleConfigJiraPrioritiesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73034a13924afc61f8a57ea354b43487b15a80f83e27ca7b2e65a0a839c19779)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("JiraCloudAccountMappingRuleConfigJiraPrioritiesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb0a052559776d07d9e5c27c791be750a7767f4b4b4105b2d283bccea01dd1f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1ef80c7f9cd7d87256d8a406cae0fade692f070c3bb8576f11f08fb55880d33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b835dc7ad78ec176e62de7f6d61f2337b56db005133346aebc2f5eb075c588b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[JiraCloudAccountMappingRuleConfigJiraPriorities]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[JiraCloudAccountMappingRuleConfigJiraPriorities]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[JiraCloudAccountMappingRuleConfigJiraPriorities]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cff635e5607cdff4ff062cd8574a62d5acc0fdb6d52f1567edf5e784ef03b93b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class JiraCloudAccountMappingRuleConfigJiraPrioritiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.jiraCloudAccountMappingRule.JiraCloudAccountMappingRuleConfigJiraPrioritiesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__404121d86a987231b469ddceb74d772b7c13c41c4d8a198bb6d2c9b5c5c450be)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="jiraIdInput")
    def jira_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jiraIdInput"))

    @builtins.property
    @jsii.member(jsii_name="pagerdutyIdInput")
    def pagerduty_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pagerdutyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="jiraId")
    def jira_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jiraId"))

    @jira_id.setter
    def jira_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1b386f0cef8081ea776504d1558c356f80acd20d944490d7d25ed9b53b7d2b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jiraId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pagerdutyId")
    def pagerduty_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pagerdutyId"))

    @pagerduty_id.setter
    def pagerduty_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe3435d8e9e1beb24d7bfc7af769fb8c858547ad7fb14487c6bb55ba930419d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pagerdutyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJiraPriorities]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJiraPriorities]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJiraPriorities]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c170971948474f21dfc4177a8153843b9880ff83fc6b889d0e7d3596ed9160a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.jiraCloudAccountMappingRule.JiraCloudAccountMappingRuleConfigJiraProject",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "key": "key", "name": "name"},
)
class JiraCloudAccountMappingRuleConfigJiraProject:
    def __init__(
        self,
        *,
        id: builtins.str,
        key: builtins.str,
        name: builtins.str,
    ) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#id JiraCloudAccountMappingRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#key JiraCloudAccountMappingRule#key}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#name JiraCloudAccountMappingRule#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__684f7553a6e9ccb2001a581719388b0fc067b2835b3b5595f075ff6438a61467)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "key": key,
            "name": name,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#id JiraCloudAccountMappingRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#key JiraCloudAccountMappingRule#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#name JiraCloudAccountMappingRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JiraCloudAccountMappingRuleConfigJiraProject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class JiraCloudAccountMappingRuleConfigJiraProjectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.jiraCloudAccountMappingRule.JiraCloudAccountMappingRuleConfigJiraProjectOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da7e52485114978834df18a73b747eb56581f7a7490e68de807e5a313bdcf017)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cda1b22f13f4440ffe1ed53cdc09b615ad0062e3fd94a6f0c0a808d935d9900e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92000673927ac7708661e4b547016de37e5ac4bf1ac2e15a420f5af4183e8041)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0a88accb27de448c323722b779ebc74caec47b7a9f1ed2f81ee163726f09119)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJiraProject]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJiraProject]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJiraProject]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__265d85f9718b6fd28d60f153c199e2c3623552ad08be947ce41e91215f88fe28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.jiraCloudAccountMappingRule.JiraCloudAccountMappingRuleConfigJiraStatusMapping",
    jsii_struct_bases=[],
    name_mapping={
        "triggered": "triggered",
        "acknowledged": "acknowledged",
        "resolved": "resolved",
    },
)
class JiraCloudAccountMappingRuleConfigJiraStatusMapping:
    def __init__(
        self,
        *,
        triggered: typing.Union["JiraCloudAccountMappingRuleConfigJiraStatusMappingTriggered", typing.Dict[builtins.str, typing.Any]],
        acknowledged: typing.Optional[typing.Union["JiraCloudAccountMappingRuleConfigJiraStatusMappingAcknowledged", typing.Dict[builtins.str, typing.Any]]] = None,
        resolved: typing.Optional[typing.Union["JiraCloudAccountMappingRuleConfigJiraStatusMappingResolved", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param triggered: triggered block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#triggered JiraCloudAccountMappingRule#triggered}
        :param acknowledged: acknowledged block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#acknowledged JiraCloudAccountMappingRule#acknowledged}
        :param resolved: resolved block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#resolved JiraCloudAccountMappingRule#resolved}
        '''
        if isinstance(triggered, dict):
            triggered = JiraCloudAccountMappingRuleConfigJiraStatusMappingTriggered(**triggered)
        if isinstance(acknowledged, dict):
            acknowledged = JiraCloudAccountMappingRuleConfigJiraStatusMappingAcknowledged(**acknowledged)
        if isinstance(resolved, dict):
            resolved = JiraCloudAccountMappingRuleConfigJiraStatusMappingResolved(**resolved)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__748c89713060e14400c7929f1d6252c44bcff90d52c90f9eba193af743963d7b)
            check_type(argname="argument triggered", value=triggered, expected_type=type_hints["triggered"])
            check_type(argname="argument acknowledged", value=acknowledged, expected_type=type_hints["acknowledged"])
            check_type(argname="argument resolved", value=resolved, expected_type=type_hints["resolved"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "triggered": triggered,
        }
        if acknowledged is not None:
            self._values["acknowledged"] = acknowledged
        if resolved is not None:
            self._values["resolved"] = resolved

    @builtins.property
    def triggered(
        self,
    ) -> "JiraCloudAccountMappingRuleConfigJiraStatusMappingTriggered":
        '''triggered block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#triggered JiraCloudAccountMappingRule#triggered}
        '''
        result = self._values.get("triggered")
        assert result is not None, "Required property 'triggered' is missing"
        return typing.cast("JiraCloudAccountMappingRuleConfigJiraStatusMappingTriggered", result)

    @builtins.property
    def acknowledged(
        self,
    ) -> typing.Optional["JiraCloudAccountMappingRuleConfigJiraStatusMappingAcknowledged"]:
        '''acknowledged block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#acknowledged JiraCloudAccountMappingRule#acknowledged}
        '''
        result = self._values.get("acknowledged")
        return typing.cast(typing.Optional["JiraCloudAccountMappingRuleConfigJiraStatusMappingAcknowledged"], result)

    @builtins.property
    def resolved(
        self,
    ) -> typing.Optional["JiraCloudAccountMappingRuleConfigJiraStatusMappingResolved"]:
        '''resolved block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#resolved JiraCloudAccountMappingRule#resolved}
        '''
        result = self._values.get("resolved")
        return typing.cast(typing.Optional["JiraCloudAccountMappingRuleConfigJiraStatusMappingResolved"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JiraCloudAccountMappingRuleConfigJiraStatusMapping(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.jiraCloudAccountMappingRule.JiraCloudAccountMappingRuleConfigJiraStatusMappingAcknowledged",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "name": "name"},
)
class JiraCloudAccountMappingRuleConfigJiraStatusMappingAcknowledged:
    def __init__(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#id JiraCloudAccountMappingRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#name JiraCloudAccountMappingRule#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d4ec115cb589218441cd42ead87581fc1af479242d96b9ada3d00db4080fb4b)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if id is not None:
            self._values["id"] = id
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#id JiraCloudAccountMappingRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#name JiraCloudAccountMappingRule#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JiraCloudAccountMappingRuleConfigJiraStatusMappingAcknowledged(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class JiraCloudAccountMappingRuleConfigJiraStatusMappingAcknowledgedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.jiraCloudAccountMappingRule.JiraCloudAccountMappingRuleConfigJiraStatusMappingAcknowledgedOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d48c3bb47c4bbfc333b18d2a29f96465e2be958562dbb761223088b494cd3c3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f987c534b0c3440dfb1a5689852b0dbc6fe128938ceeb4a70d70adbb6ba59dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c80badc2283f323a4159f89da738404077eef7cb5bdcbf29b2516d1e79427009)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJiraStatusMappingAcknowledged]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJiraStatusMappingAcknowledged]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJiraStatusMappingAcknowledged]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b0cbbf44435b69afa341c336ff9353baee28fae7f1fb4b69949ea2a8eff5982)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class JiraCloudAccountMappingRuleConfigJiraStatusMappingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.jiraCloudAccountMappingRule.JiraCloudAccountMappingRuleConfigJiraStatusMappingOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__349f6e6bfea37c68931bf906e462d6709f9c988a362bc81eb331505152c52858)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAcknowledged")
    def put_acknowledged(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#id JiraCloudAccountMappingRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#name JiraCloudAccountMappingRule#name}.
        '''
        value = JiraCloudAccountMappingRuleConfigJiraStatusMappingAcknowledged(
            id=id, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putAcknowledged", [value]))

    @jsii.member(jsii_name="putResolved")
    def put_resolved(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#id JiraCloudAccountMappingRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#name JiraCloudAccountMappingRule#name}.
        '''
        value = JiraCloudAccountMappingRuleConfigJiraStatusMappingResolved(
            id=id, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putResolved", [value]))

    @jsii.member(jsii_name="putTriggered")
    def put_triggered(self, *, id: builtins.str, name: builtins.str) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#id JiraCloudAccountMappingRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#name JiraCloudAccountMappingRule#name}.
        '''
        value = JiraCloudAccountMappingRuleConfigJiraStatusMappingTriggered(
            id=id, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putTriggered", [value]))

    @jsii.member(jsii_name="resetAcknowledged")
    def reset_acknowledged(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcknowledged", []))

    @jsii.member(jsii_name="resetResolved")
    def reset_resolved(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResolved", []))

    @builtins.property
    @jsii.member(jsii_name="acknowledged")
    def acknowledged(
        self,
    ) -> JiraCloudAccountMappingRuleConfigJiraStatusMappingAcknowledgedOutputReference:
        return typing.cast(JiraCloudAccountMappingRuleConfigJiraStatusMappingAcknowledgedOutputReference, jsii.get(self, "acknowledged"))

    @builtins.property
    @jsii.member(jsii_name="resolved")
    def resolved(
        self,
    ) -> "JiraCloudAccountMappingRuleConfigJiraStatusMappingResolvedOutputReference":
        return typing.cast("JiraCloudAccountMappingRuleConfigJiraStatusMappingResolvedOutputReference", jsii.get(self, "resolved"))

    @builtins.property
    @jsii.member(jsii_name="triggered")
    def triggered(
        self,
    ) -> "JiraCloudAccountMappingRuleConfigJiraStatusMappingTriggeredOutputReference":
        return typing.cast("JiraCloudAccountMappingRuleConfigJiraStatusMappingTriggeredOutputReference", jsii.get(self, "triggered"))

    @builtins.property
    @jsii.member(jsii_name="acknowledgedInput")
    def acknowledged_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJiraStatusMappingAcknowledged]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJiraStatusMappingAcknowledged]], jsii.get(self, "acknowledgedInput"))

    @builtins.property
    @jsii.member(jsii_name="resolvedInput")
    def resolved_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "JiraCloudAccountMappingRuleConfigJiraStatusMappingResolved"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "JiraCloudAccountMappingRuleConfigJiraStatusMappingResolved"]], jsii.get(self, "resolvedInput"))

    @builtins.property
    @jsii.member(jsii_name="triggeredInput")
    def triggered_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "JiraCloudAccountMappingRuleConfigJiraStatusMappingTriggered"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "JiraCloudAccountMappingRuleConfigJiraStatusMappingTriggered"]], jsii.get(self, "triggeredInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJiraStatusMapping]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJiraStatusMapping]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJiraStatusMapping]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a26a3ea0723300f3f53bb8502b2bce8a83c179fe80727534905aa30862888e17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.jiraCloudAccountMappingRule.JiraCloudAccountMappingRuleConfigJiraStatusMappingResolved",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "name": "name"},
)
class JiraCloudAccountMappingRuleConfigJiraStatusMappingResolved:
    def __init__(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#id JiraCloudAccountMappingRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#name JiraCloudAccountMappingRule#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be3d2bf640a9f3c4a707b6c1ea364219099db8cf5935c2756173792b555c9b58)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if id is not None:
            self._values["id"] = id
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#id JiraCloudAccountMappingRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#name JiraCloudAccountMappingRule#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JiraCloudAccountMappingRuleConfigJiraStatusMappingResolved(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class JiraCloudAccountMappingRuleConfigJiraStatusMappingResolvedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.jiraCloudAccountMappingRule.JiraCloudAccountMappingRuleConfigJiraStatusMappingResolvedOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3561f47fe29a5deb4aef55092cb58f8f36a7aa199da21d6020d88965946cdb23)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44dd67a7a43a123028b65f5e6542157188fd4d4cd85e6b5c39fe0394394f2f2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d59c69ae62ed793acf249dc40b42381f6168d8f7ef2fdf7d6f8ebb51ca94d94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJiraStatusMappingResolved]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJiraStatusMappingResolved]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJiraStatusMappingResolved]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a73bc339ed97d76699496a7cd281abda2bcd492cb68cd5923b76d261e953682)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.jiraCloudAccountMappingRule.JiraCloudAccountMappingRuleConfigJiraStatusMappingTriggered",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "name": "name"},
)
class JiraCloudAccountMappingRuleConfigJiraStatusMappingTriggered:
    def __init__(self, *, id: builtins.str, name: builtins.str) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#id JiraCloudAccountMappingRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#name JiraCloudAccountMappingRule#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f564d993273e63cd13be12b4a58d0f211cb15be1fa20f1bfc1026fc964f3116)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "name": name,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#id JiraCloudAccountMappingRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/jira_cloud_account_mapping_rule#name JiraCloudAccountMappingRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JiraCloudAccountMappingRuleConfigJiraStatusMappingTriggered(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class JiraCloudAccountMappingRuleConfigJiraStatusMappingTriggeredOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.jiraCloudAccountMappingRule.JiraCloudAccountMappingRuleConfigJiraStatusMappingTriggeredOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2db66d38419faccde1e197c9fea46302eb1452ebe0bbe4f8a041cb2565eb304b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ff300203805b7870abfbdf5e7a8c78b8d37236ffacbfe38db50d1e26e0061ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__479fdc01d2fde2ea3fdfb64a761ed0210978740ca4a3915c9ed609671e3aa1ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJiraStatusMappingTriggered]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJiraStatusMappingTriggered]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJiraStatusMappingTriggered]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b43687a6100289ded9787117b715889fcd3a6840ef15cdea2cdfb0373f2cf1b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "JiraCloudAccountMappingRule",
    "JiraCloudAccountMappingRuleConfig",
    "JiraCloudAccountMappingRuleConfigA",
    "JiraCloudAccountMappingRuleConfigAOutputReference",
    "JiraCloudAccountMappingRuleConfigJira",
    "JiraCloudAccountMappingRuleConfigJiraCustomFields",
    "JiraCloudAccountMappingRuleConfigJiraCustomFieldsList",
    "JiraCloudAccountMappingRuleConfigJiraCustomFieldsOutputReference",
    "JiraCloudAccountMappingRuleConfigJiraIssueType",
    "JiraCloudAccountMappingRuleConfigJiraIssueTypeOutputReference",
    "JiraCloudAccountMappingRuleConfigJiraOutputReference",
    "JiraCloudAccountMappingRuleConfigJiraPriorities",
    "JiraCloudAccountMappingRuleConfigJiraPrioritiesList",
    "JiraCloudAccountMappingRuleConfigJiraPrioritiesOutputReference",
    "JiraCloudAccountMappingRuleConfigJiraProject",
    "JiraCloudAccountMappingRuleConfigJiraProjectOutputReference",
    "JiraCloudAccountMappingRuleConfigJiraStatusMapping",
    "JiraCloudAccountMappingRuleConfigJiraStatusMappingAcknowledged",
    "JiraCloudAccountMappingRuleConfigJiraStatusMappingAcknowledgedOutputReference",
    "JiraCloudAccountMappingRuleConfigJiraStatusMappingOutputReference",
    "JiraCloudAccountMappingRuleConfigJiraStatusMappingResolved",
    "JiraCloudAccountMappingRuleConfigJiraStatusMappingResolvedOutputReference",
    "JiraCloudAccountMappingRuleConfigJiraStatusMappingTriggered",
    "JiraCloudAccountMappingRuleConfigJiraStatusMappingTriggeredOutputReference",
]

publication.publish()

def _typecheckingstub__afb506592aab04542eeba94fad9980f8722b05c5ead54c17e81ffc5f011766d5(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account_mapping: builtins.str,
    name: builtins.str,
    config: typing.Optional[typing.Union[JiraCloudAccountMappingRuleConfigA, typing.Dict[builtins.str, typing.Any]]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a39d3a40dac458599e0cdbae10045d2667bed4da31bc875d42731c5ada8bf702(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b4a98c4e119426d4b92e43d09f219dbd9d06e322581dfd2300858e37d9aa61b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__494f780c921e1a15a4e8e54e47b5a5174950da7e587c2d18e7156e481dd93b66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a4485e15c0e1d1b8c578751b283cf1a0fc196866c77daedb975549f5dc26022(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    account_mapping: builtins.str,
    name: builtins.str,
    config: typing.Optional[typing.Union[JiraCloudAccountMappingRuleConfigA, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f34ccb50de9de421d723002c9619ed94f416c8f90b267f2ea55fa97c2ffc330c(
    *,
    service: builtins.str,
    jira: typing.Optional[typing.Union[JiraCloudAccountMappingRuleConfigJira, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__715a1df3264e416b5855b7fbbabd836c4acb51d18e4f9187c7b43985a0d2052f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5263d0c1a2eded6d235c9a48bca6c6e59ac6f3a770edad1c67e179447552f384(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a365cf19b76617e33405e399b208a72d90beb9c8bb8580ddfa1d89dac6d850a0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigA]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edf4a70d34cb948fa2b1ceb5d86be813c7689dc0d412af3533d8e45950584b1c(
    *,
    issue_type: typing.Union[JiraCloudAccountMappingRuleConfigJiraIssueType, typing.Dict[builtins.str, typing.Any]],
    project: typing.Union[JiraCloudAccountMappingRuleConfigJiraProject, typing.Dict[builtins.str, typing.Any]],
    autocreate_jql: typing.Optional[builtins.str] = None,
    create_issue_on_incident_trigger: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    custom_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[JiraCloudAccountMappingRuleConfigJiraCustomFields, typing.Dict[builtins.str, typing.Any]]]]] = None,
    priorities: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[JiraCloudAccountMappingRuleConfigJiraPriorities, typing.Dict[builtins.str, typing.Any]]]]] = None,
    status_mapping: typing.Optional[typing.Union[JiraCloudAccountMappingRuleConfigJiraStatusMapping, typing.Dict[builtins.str, typing.Any]]] = None,
    sync_notes_user: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84c9a93370e770133f7f52bab7e5fa55ab5fe386edc4ac4314f4cd918cdd99ac(
    *,
    target_issue_field: builtins.str,
    target_issue_field_name: builtins.str,
    type: builtins.str,
    source_incident_field: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bb21863a8762e7be964032c143c278f06a34a5dd2bdde2eb3bc21a4f49ef1e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2f38334666379bb610e190b45644d65735bc3bb4e762c20a49f2b5b8110d4fe(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14866d57c8e3f7150aed9e4901a01b945f7cebc2552979981b2d897458d48e13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbe4a1c7ee825bc811edbf01c9346f29f32a9a8333dfd5748b64f7b2b606492d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0584cfc9947fd855c3a790a1aae2334de2031ee5cb6aa608fe562ef4a9d10db6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29fcd84179a0797073e1d02b28150fb5127a6bd37559d9efbd3ffb23cc4207c6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[JiraCloudAccountMappingRuleConfigJiraCustomFields]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a948c09b429258d3b3d6fbca86d1957fa2ea948c475bab33271771fcf81f0b0a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b895a26672249820648b48bfe821c2f51e7488f0a5168d190e9e263057ad361(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d0ca17ab91d434caa69c45f06fdd11e17bdc98738628f11bd063db058b56d08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ddf891fae2adeeec9be57d4f3e7643175f1a0f45594156e07ac76eea05d51e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad4c1f3394d17f432e3e700960d3180d7a3d1672d2c806aca34fdd70677c709e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67a6787aa2d0c7d8c680909af37fdfceba32b94c917e4ae2d1ea29315d0fb918(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95fc839b47f15a0376242beecda9a056418e4cb8d3070b8d95dc2544bb985188(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJiraCustomFields]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f5c45e0473724f72edbe36061578d7a309b64651bf7f4494653966ec7b80e91(
    *,
    id: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8bf69be5756d7429ff00bedf954ce10b79918ee21077b9ef8c99548ab586a3d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fd693885cbab30c70abc298ba9365d550f882af171fc414f1dd5f82370f26ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6684d0f839687d92b8fa0d67ca01bd5ffa64eab9c07843871e68aed6d53bdf51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6afa47abb5806c8ae3b827ee884532f7cc27f4d75df331be4543ce7cb9252bb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJiraIssueType]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7290abbf180f3e6f203a5bcef74cb560a82d0f63df85a66e47e5b89f3e34387(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07c241c0df5d7171b6ec8d20f76264b8ebe9e6644bcac0675443d69227276eea(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[JiraCloudAccountMappingRuleConfigJiraCustomFields, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__437c272306b1ddb850aaead9c7e35fcdb1a97d1477fa2d6f5361adf079791fe8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[JiraCloudAccountMappingRuleConfigJiraPriorities, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ee9518b4cb466bb9e395a4b6c532730511b33e33bb8fa38ce659652f67e7ee7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a12006567f582e2e0967dcb7edb6c75a4641859729ebce9f6f723d30a0650868(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1abea1f1aed169385c22cc56f53f2a8d19a8ace24f94965a0345c8ed0634978(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58947de24fb8c5b487a445da9e841a11eec426b854fac4d7d7cfa96c2bcb257c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJira]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0733d63cf21e384e198f10eaf1b97c133ae536e0f541a777055ef3a5b66fcdbf(
    *,
    jira_id: builtins.str,
    pagerduty_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9496b6d55fd7a97ebe394acbc1d9c751821237b09628ad4a6385868184c9cb70(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73034a13924afc61f8a57ea354b43487b15a80f83e27ca7b2e65a0a839c19779(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb0a052559776d07d9e5c27c791be750a7767f4b4b4105b2d283bccea01dd1f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1ef80c7f9cd7d87256d8a406cae0fade692f070c3bb8576f11f08fb55880d33(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b835dc7ad78ec176e62de7f6d61f2337b56db005133346aebc2f5eb075c588b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cff635e5607cdff4ff062cd8574a62d5acc0fdb6d52f1567edf5e784ef03b93b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[JiraCloudAccountMappingRuleConfigJiraPriorities]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__404121d86a987231b469ddceb74d772b7c13c41c4d8a198bb6d2c9b5c5c450be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1b386f0cef8081ea776504d1558c356f80acd20d944490d7d25ed9b53b7d2b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe3435d8e9e1beb24d7bfc7af769fb8c858547ad7fb14487c6bb55ba930419d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c170971948474f21dfc4177a8153843b9880ff83fc6b889d0e7d3596ed9160a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJiraPriorities]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__684f7553a6e9ccb2001a581719388b0fc067b2835b3b5595f075ff6438a61467(
    *,
    id: builtins.str,
    key: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da7e52485114978834df18a73b747eb56581f7a7490e68de807e5a313bdcf017(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cda1b22f13f4440ffe1ed53cdc09b615ad0062e3fd94a6f0c0a808d935d9900e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92000673927ac7708661e4b547016de37e5ac4bf1ac2e15a420f5af4183e8041(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0a88accb27de448c323722b779ebc74caec47b7a9f1ed2f81ee163726f09119(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__265d85f9718b6fd28d60f153c199e2c3623552ad08be947ce41e91215f88fe28(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJiraProject]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__748c89713060e14400c7929f1d6252c44bcff90d52c90f9eba193af743963d7b(
    *,
    triggered: typing.Union[JiraCloudAccountMappingRuleConfigJiraStatusMappingTriggered, typing.Dict[builtins.str, typing.Any]],
    acknowledged: typing.Optional[typing.Union[JiraCloudAccountMappingRuleConfigJiraStatusMappingAcknowledged, typing.Dict[builtins.str, typing.Any]]] = None,
    resolved: typing.Optional[typing.Union[JiraCloudAccountMappingRuleConfigJiraStatusMappingResolved, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d4ec115cb589218441cd42ead87581fc1af479242d96b9ada3d00db4080fb4b(
    *,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d48c3bb47c4bbfc333b18d2a29f96465e2be958562dbb761223088b494cd3c3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f987c534b0c3440dfb1a5689852b0dbc6fe128938ceeb4a70d70adbb6ba59dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c80badc2283f323a4159f89da738404077eef7cb5bdcbf29b2516d1e79427009(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b0cbbf44435b69afa341c336ff9353baee28fae7f1fb4b69949ea2a8eff5982(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJiraStatusMappingAcknowledged]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__349f6e6bfea37c68931bf906e462d6709f9c988a362bc81eb331505152c52858(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a26a3ea0723300f3f53bb8502b2bce8a83c179fe80727534905aa30862888e17(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJiraStatusMapping]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be3d2bf640a9f3c4a707b6c1ea364219099db8cf5935c2756173792b555c9b58(
    *,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3561f47fe29a5deb4aef55092cb58f8f36a7aa199da21d6020d88965946cdb23(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44dd67a7a43a123028b65f5e6542157188fd4d4cd85e6b5c39fe0394394f2f2e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d59c69ae62ed793acf249dc40b42381f6168d8f7ef2fdf7d6f8ebb51ca94d94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a73bc339ed97d76699496a7cd281abda2bcd492cb68cd5923b76d261e953682(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJiraStatusMappingResolved]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f564d993273e63cd13be12b4a58d0f211cb15be1fa20f1bfc1026fc964f3116(
    *,
    id: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2db66d38419faccde1e197c9fea46302eb1452ebe0bbe4f8a041cb2565eb304b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ff300203805b7870abfbdf5e7a8c78b8d37236ffacbfe38db50d1e26e0061ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__479fdc01d2fde2ea3fdfb64a761ed0210978740ca4a3915c9ed609671e3aa1ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b43687a6100289ded9787117b715889fcd3a6840ef15cdea2cdfb0373f2cf1b7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, JiraCloudAccountMappingRuleConfigJiraStatusMappingTriggered]],
) -> None:
    """Type checking stubs"""
    pass
