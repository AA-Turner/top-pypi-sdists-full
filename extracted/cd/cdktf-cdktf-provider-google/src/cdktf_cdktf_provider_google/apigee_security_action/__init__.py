r'''
# `google_apigee_security_action`

Refer to the Terraform Registry for docs: [`google_apigee_security_action`](https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action).
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


class ApigeeSecurityAction(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeSecurityAction.ApigeeSecurityAction",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action google_apigee_security_action}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        condition_config: typing.Union["ApigeeSecurityActionConditionConfig", typing.Dict[builtins.str, typing.Any]],
        env_id: builtins.str,
        org_id: builtins.str,
        security_action_id: builtins.str,
        state: builtins.str,
        allow: typing.Optional[typing.Union["ApigeeSecurityActionAllow", typing.Dict[builtins.str, typing.Any]]] = None,
        api_proxies: typing.Optional[typing.Sequence[builtins.str]] = None,
        deny: typing.Optional[typing.Union["ApigeeSecurityActionDeny", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        expire_time: typing.Optional[builtins.str] = None,
        flag: typing.Optional[typing.Union["ApigeeSecurityActionFlag", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ApigeeSecurityActionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        ttl: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action google_apigee_security_action} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param condition_config: condition_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#condition_config ApigeeSecurityAction#condition_config}
        :param env_id: The Apigee environment that this security action applies to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#env_id ApigeeSecurityAction#env_id}
        :param org_id: The organization that this security action applies to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#org_id ApigeeSecurityAction#org_id}
        :param security_action_id: The ID to use for the SecurityAction, which will become the final component of the action's resource name. This value should be 0-61 characters, and valid format is (^a-z?$). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#security_action_id ApigeeSecurityAction#security_action_id}
        :param state: Only an ENABLED SecurityAction is enforced. An ENABLED SecurityAction past its expiration time will not be enforced. Possible values: ["ENABLED", "DISABLED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#state ApigeeSecurityAction#state}
        :param allow: allow block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#allow ApigeeSecurityAction#allow}
        :param api_proxies: If unset, this would apply to all proxies in the environment. If set, this action is enforced only if at least one proxy in the repeated list is deployed at the time of enforcement. If set, several restrictions are enforced on SecurityActions. There can be at most 100 enabled actions with proxies set in an env. Several other restrictions apply on conditions and are detailed later. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#api_proxies ApigeeSecurityAction#api_proxies}
        :param deny: deny block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#deny ApigeeSecurityAction#deny}
        :param description: An optional user provided description of the SecurityAction. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#description ApigeeSecurityAction#description}
        :param expire_time: The expiration for this SecurityAction. Uses RFC 3339, where generated output will always be Z-normalized and uses 0, 3, 6 or 9 fractional digits. Offsets other than "Z" are also accepted. Examples: "2014-10-02T15:01:23Z", "2014-10-02T15:01:23.045123456Z" or "2014-10-02T15:01:23+05:30". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#expire_time ApigeeSecurityAction#expire_time}
        :param flag: flag block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#flag ApigeeSecurityAction#flag}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#id ApigeeSecurityAction#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#timeouts ApigeeSecurityAction#timeouts}
        :param ttl: The TTL for this SecurityAction. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#ttl ApigeeSecurityAction#ttl}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fe5237d0b8ce1e99bbf712442b3cb247ca8fb78cb5c30605e27718cd9c9ff80)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApigeeSecurityActionConfig(
            condition_config=condition_config,
            env_id=env_id,
            org_id=org_id,
            security_action_id=security_action_id,
            state=state,
            allow=allow,
            api_proxies=api_proxies,
            deny=deny,
            description=description,
            expire_time=expire_time,
            flag=flag,
            id=id,
            timeouts=timeouts,
            ttl=ttl,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a ApigeeSecurityAction resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ApigeeSecurityAction to import.
        :param import_from_id: The id of the existing ApigeeSecurityAction that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ApigeeSecurityAction to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b48722c9d7f76d59fb0247954ae20fbc3474e2c6bb4835beba7ca4bdcf6c114f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAllow")
    def put_allow(self) -> None:
        value = ApigeeSecurityActionAllow()

        return typing.cast(None, jsii.invoke(self, "putAllow", [value]))

    @jsii.member(jsii_name="putConditionConfig")
    def put_condition_config(
        self,
        *,
        access_tokens: typing.Optional[typing.Sequence[builtins.str]] = None,
        api_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        api_products: typing.Optional[typing.Sequence[builtins.str]] = None,
        asns: typing.Optional[typing.Sequence[builtins.str]] = None,
        bot_reasons: typing.Optional[typing.Sequence[builtins.str]] = None,
        developer_apps: typing.Optional[typing.Sequence[builtins.str]] = None,
        developers: typing.Optional[typing.Sequence[builtins.str]] = None,
        http_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
        ip_address_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_agents: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param access_tokens: A list of accessTokens. Limit 1000 per action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#access_tokens ApigeeSecurityAction#access_tokens}
        :param api_keys: A list of API keys. Limit 1000 per action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#api_keys ApigeeSecurityAction#api_keys}
        :param api_products: A list of API Products. Limit 1000 per action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#api_products ApigeeSecurityAction#api_products}
        :param asns: A list of ASN numbers to act on, e.g. 23. https://en.wikipedia.org/wiki/Autonomous_system_(Internet) This uses int64 instead of uint32 because of https://linter.aip.dev/141/forbidden-types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#asns ApigeeSecurityAction#asns}
        :param bot_reasons: A list of Bot Reasons. Current options: Flooder, Brute Guessor, Static Content Scraper, OAuth Abuser, Robot Abuser, TorListRule, Advanced Anomaly Detection, Advanced API Scraper, Search Engine Crawlers, Public Clouds, Public Cloud AWS, Public Cloud Azure, and Public Cloud Google. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#bot_reasons ApigeeSecurityAction#bot_reasons}
        :param developer_apps: A list of developer apps. Limit 1000 per action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#developer_apps ApigeeSecurityAction#developer_apps}
        :param developers: A list of developers. Limit 1000 per action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#developers ApigeeSecurityAction#developers}
        :param http_methods: Act only on particular HTTP methods. E.g. A read-only API can block POST/PUT/DELETE methods. Accepted values are: GET, HEAD, POST, PUT, DELETE, CONNECT, OPTIONS, TRACE and PATCH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#http_methods ApigeeSecurityAction#http_methods}
        :param ip_address_ranges: A list of IP addresses. This could be either IPv4 or IPv6. Limited to 100 per action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#ip_address_ranges ApigeeSecurityAction#ip_address_ranges}
        :param region_codes: A list of countries/region codes to act on, e.g. US. This follows https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#region_codes ApigeeSecurityAction#region_codes}
        :param user_agents: A list of user agents to deny. We look for exact matches. Limit 50 per action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#user_agents ApigeeSecurityAction#user_agents}
        '''
        value = ApigeeSecurityActionConditionConfig(
            access_tokens=access_tokens,
            api_keys=api_keys,
            api_products=api_products,
            asns=asns,
            bot_reasons=bot_reasons,
            developer_apps=developer_apps,
            developers=developers,
            http_methods=http_methods,
            ip_address_ranges=ip_address_ranges,
            region_codes=region_codes,
            user_agents=user_agents,
        )

        return typing.cast(None, jsii.invoke(self, "putConditionConfig", [value]))

    @jsii.member(jsii_name="putDeny")
    def put_deny(self, *, response_code: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param response_code: The HTTP response code if the Action = DENY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#response_code ApigeeSecurityAction#response_code}
        '''
        value = ApigeeSecurityActionDeny(response_code=response_code)

        return typing.cast(None, jsii.invoke(self, "putDeny", [value]))

    @jsii.member(jsii_name="putFlag")
    def put_flag(
        self,
        *,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigeeSecurityActionFlagHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param headers: headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#headers ApigeeSecurityAction#headers}
        '''
        value = ApigeeSecurityActionFlag(headers=headers)

        return typing.cast(None, jsii.invoke(self, "putFlag", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#create ApigeeSecurityAction#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#delete ApigeeSecurityAction#delete}.
        '''
        value = ApigeeSecurityActionTimeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAllow")
    def reset_allow(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllow", []))

    @jsii.member(jsii_name="resetApiProxies")
    def reset_api_proxies(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiProxies", []))

    @jsii.member(jsii_name="resetDeny")
    def reset_deny(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeny", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetExpireTime")
    def reset_expire_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpireTime", []))

    @jsii.member(jsii_name="resetFlag")
    def reset_flag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFlag", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTtl")
    def reset_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTtl", []))

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
    @jsii.member(jsii_name="allow")
    def allow(self) -> "ApigeeSecurityActionAllowOutputReference":
        return typing.cast("ApigeeSecurityActionAllowOutputReference", jsii.get(self, "allow"))

    @builtins.property
    @jsii.member(jsii_name="conditionConfig")
    def condition_config(self) -> "ApigeeSecurityActionConditionConfigOutputReference":
        return typing.cast("ApigeeSecurityActionConditionConfigOutputReference", jsii.get(self, "conditionConfig"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="deny")
    def deny(self) -> "ApigeeSecurityActionDenyOutputReference":
        return typing.cast("ApigeeSecurityActionDenyOutputReference", jsii.get(self, "deny"))

    @builtins.property
    @jsii.member(jsii_name="flag")
    def flag(self) -> "ApigeeSecurityActionFlagOutputReference":
        return typing.cast("ApigeeSecurityActionFlagOutputReference", jsii.get(self, "flag"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ApigeeSecurityActionTimeoutsOutputReference":
        return typing.cast("ApigeeSecurityActionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="allowInput")
    def allow_input(self) -> typing.Optional["ApigeeSecurityActionAllow"]:
        return typing.cast(typing.Optional["ApigeeSecurityActionAllow"], jsii.get(self, "allowInput"))

    @builtins.property
    @jsii.member(jsii_name="apiProxiesInput")
    def api_proxies_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "apiProxiesInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionConfigInput")
    def condition_config_input(
        self,
    ) -> typing.Optional["ApigeeSecurityActionConditionConfig"]:
        return typing.cast(typing.Optional["ApigeeSecurityActionConditionConfig"], jsii.get(self, "conditionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="denyInput")
    def deny_input(self) -> typing.Optional["ApigeeSecurityActionDeny"]:
        return typing.cast(typing.Optional["ApigeeSecurityActionDeny"], jsii.get(self, "denyInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="envIdInput")
    def env_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "envIdInput"))

    @builtins.property
    @jsii.member(jsii_name="expireTimeInput")
    def expire_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expireTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="flagInput")
    def flag_input(self) -> typing.Optional["ApigeeSecurityActionFlag"]:
        return typing.cast(typing.Optional["ApigeeSecurityActionFlag"], jsii.get(self, "flagInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="orgIdInput")
    def org_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgIdInput"))

    @builtins.property
    @jsii.member(jsii_name="securityActionIdInput")
    def security_action_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityActionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApigeeSecurityActionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApigeeSecurityActionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="ttlInput")
    def ttl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ttlInput"))

    @builtins.property
    @jsii.member(jsii_name="apiProxies")
    def api_proxies(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "apiProxies"))

    @api_proxies.setter
    def api_proxies(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d76cb8a82c9dc237d261f7ed35e8e714cf33337747be1b69656bb1e9ba2af7e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiProxies", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce4ab2ebcba1798058eb9f58c91542d7e849fd8d4036d4c8003fb37265adc5be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="envId")
    def env_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "envId"))

    @env_id.setter
    def env_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50af45e6d6e84eb8ee9e1daa442a19f474d81338b044197c35cda54bb46ea65a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "envId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expireTime")
    def expire_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expireTime"))

    @expire_time.setter
    def expire_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1677ab90ab71e2598ec104857335d63b4f3d18fade160bd9044372075c03948a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expireTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1247a3b3fbbf411cd82271f7312fc268429700177b55a3bf6d0ae4a5d4494331)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="orgId")
    def org_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orgId"))

    @org_id.setter
    def org_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05f1b91a87036bcb9af8548b7dac50adbc72c627c89aa92f0efda139f06c9fed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orgId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityActionId")
    def security_action_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityActionId"))

    @security_action_id.setter
    def security_action_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc1787aef55e6feaf7c7ac116ea8176505ea67ad200b404b45a9734ed115a84e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityActionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbfd51e73f27af88e8ca02e69d9c27d3f559f9a44629b3b97689b97cb8393f36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ttl"))

    @ttl.setter
    def ttl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b5cffa20a68934a9dd46082f8d8c719f9185f5e2504c0d4464fc384c8c46d5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ttl", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeSecurityAction.ApigeeSecurityActionAllow",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApigeeSecurityActionAllow:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeSecurityActionAllow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigeeSecurityActionAllowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeSecurityAction.ApigeeSecurityActionAllowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ecd4653bb76145e0be2d548aa2a55fd6cffe88319a434792100929666910914)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApigeeSecurityActionAllow]:
        return typing.cast(typing.Optional[ApigeeSecurityActionAllow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ApigeeSecurityActionAllow]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f31ea0d3149018fa169048af96a21f1918e8e64ed0d85f7bc859d78dc77c9794)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeSecurityAction.ApigeeSecurityActionConditionConfig",
    jsii_struct_bases=[],
    name_mapping={
        "access_tokens": "accessTokens",
        "api_keys": "apiKeys",
        "api_products": "apiProducts",
        "asns": "asns",
        "bot_reasons": "botReasons",
        "developer_apps": "developerApps",
        "developers": "developers",
        "http_methods": "httpMethods",
        "ip_address_ranges": "ipAddressRanges",
        "region_codes": "regionCodes",
        "user_agents": "userAgents",
    },
)
class ApigeeSecurityActionConditionConfig:
    def __init__(
        self,
        *,
        access_tokens: typing.Optional[typing.Sequence[builtins.str]] = None,
        api_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        api_products: typing.Optional[typing.Sequence[builtins.str]] = None,
        asns: typing.Optional[typing.Sequence[builtins.str]] = None,
        bot_reasons: typing.Optional[typing.Sequence[builtins.str]] = None,
        developer_apps: typing.Optional[typing.Sequence[builtins.str]] = None,
        developers: typing.Optional[typing.Sequence[builtins.str]] = None,
        http_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
        ip_address_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_agents: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param access_tokens: A list of accessTokens. Limit 1000 per action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#access_tokens ApigeeSecurityAction#access_tokens}
        :param api_keys: A list of API keys. Limit 1000 per action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#api_keys ApigeeSecurityAction#api_keys}
        :param api_products: A list of API Products. Limit 1000 per action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#api_products ApigeeSecurityAction#api_products}
        :param asns: A list of ASN numbers to act on, e.g. 23. https://en.wikipedia.org/wiki/Autonomous_system_(Internet) This uses int64 instead of uint32 because of https://linter.aip.dev/141/forbidden-types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#asns ApigeeSecurityAction#asns}
        :param bot_reasons: A list of Bot Reasons. Current options: Flooder, Brute Guessor, Static Content Scraper, OAuth Abuser, Robot Abuser, TorListRule, Advanced Anomaly Detection, Advanced API Scraper, Search Engine Crawlers, Public Clouds, Public Cloud AWS, Public Cloud Azure, and Public Cloud Google. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#bot_reasons ApigeeSecurityAction#bot_reasons}
        :param developer_apps: A list of developer apps. Limit 1000 per action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#developer_apps ApigeeSecurityAction#developer_apps}
        :param developers: A list of developers. Limit 1000 per action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#developers ApigeeSecurityAction#developers}
        :param http_methods: Act only on particular HTTP methods. E.g. A read-only API can block POST/PUT/DELETE methods. Accepted values are: GET, HEAD, POST, PUT, DELETE, CONNECT, OPTIONS, TRACE and PATCH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#http_methods ApigeeSecurityAction#http_methods}
        :param ip_address_ranges: A list of IP addresses. This could be either IPv4 or IPv6. Limited to 100 per action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#ip_address_ranges ApigeeSecurityAction#ip_address_ranges}
        :param region_codes: A list of countries/region codes to act on, e.g. US. This follows https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#region_codes ApigeeSecurityAction#region_codes}
        :param user_agents: A list of user agents to deny. We look for exact matches. Limit 50 per action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#user_agents ApigeeSecurityAction#user_agents}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5585f29ff88d80bfd681eb63541a70f18c203cb27724d5624949ba293ec2e3d0)
            check_type(argname="argument access_tokens", value=access_tokens, expected_type=type_hints["access_tokens"])
            check_type(argname="argument api_keys", value=api_keys, expected_type=type_hints["api_keys"])
            check_type(argname="argument api_products", value=api_products, expected_type=type_hints["api_products"])
            check_type(argname="argument asns", value=asns, expected_type=type_hints["asns"])
            check_type(argname="argument bot_reasons", value=bot_reasons, expected_type=type_hints["bot_reasons"])
            check_type(argname="argument developer_apps", value=developer_apps, expected_type=type_hints["developer_apps"])
            check_type(argname="argument developers", value=developers, expected_type=type_hints["developers"])
            check_type(argname="argument http_methods", value=http_methods, expected_type=type_hints["http_methods"])
            check_type(argname="argument ip_address_ranges", value=ip_address_ranges, expected_type=type_hints["ip_address_ranges"])
            check_type(argname="argument region_codes", value=region_codes, expected_type=type_hints["region_codes"])
            check_type(argname="argument user_agents", value=user_agents, expected_type=type_hints["user_agents"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_tokens is not None:
            self._values["access_tokens"] = access_tokens
        if api_keys is not None:
            self._values["api_keys"] = api_keys
        if api_products is not None:
            self._values["api_products"] = api_products
        if asns is not None:
            self._values["asns"] = asns
        if bot_reasons is not None:
            self._values["bot_reasons"] = bot_reasons
        if developer_apps is not None:
            self._values["developer_apps"] = developer_apps
        if developers is not None:
            self._values["developers"] = developers
        if http_methods is not None:
            self._values["http_methods"] = http_methods
        if ip_address_ranges is not None:
            self._values["ip_address_ranges"] = ip_address_ranges
        if region_codes is not None:
            self._values["region_codes"] = region_codes
        if user_agents is not None:
            self._values["user_agents"] = user_agents

    @builtins.property
    def access_tokens(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of accessTokens. Limit 1000 per action.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#access_tokens ApigeeSecurityAction#access_tokens}
        '''
        result = self._values.get("access_tokens")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def api_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of API keys. Limit 1000 per action.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#api_keys ApigeeSecurityAction#api_keys}
        '''
        result = self._values.get("api_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def api_products(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of API Products. Limit 1000 per action.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#api_products ApigeeSecurityAction#api_products}
        '''
        result = self._values.get("api_products")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def asns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of ASN numbers to act on, e.g. 23. https://en.wikipedia.org/wiki/Autonomous_system_(Internet) This uses int64 instead of uint32 because of https://linter.aip.dev/141/forbidden-types.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#asns ApigeeSecurityAction#asns}
        '''
        result = self._values.get("asns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def bot_reasons(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Bot Reasons.

        Current options: Flooder, Brute Guessor, Static Content Scraper,
        OAuth Abuser, Robot Abuser, TorListRule, Advanced Anomaly Detection, Advanced API Scraper,
        Search Engine Crawlers, Public Clouds, Public Cloud AWS, Public Cloud Azure, and Public Cloud Google.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#bot_reasons ApigeeSecurityAction#bot_reasons}
        '''
        result = self._values.get("bot_reasons")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def developer_apps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of developer apps. Limit 1000 per action.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#developer_apps ApigeeSecurityAction#developer_apps}
        '''
        result = self._values.get("developer_apps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def developers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of developers. Limit 1000 per action.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#developers ApigeeSecurityAction#developers}
        '''
        result = self._values.get("developers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def http_methods(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Act only on particular HTTP methods.

        E.g. A read-only API can block POST/PUT/DELETE methods.
        Accepted values are: GET, HEAD, POST, PUT, DELETE, CONNECT, OPTIONS, TRACE and PATCH.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#http_methods ApigeeSecurityAction#http_methods}
        '''
        result = self._values.get("http_methods")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ip_address_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of IP addresses. This could be either IPv4 or IPv6. Limited to 100 per action.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#ip_address_ranges ApigeeSecurityAction#ip_address_ranges}
        '''
        result = self._values.get("ip_address_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def region_codes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of countries/region codes to act on, e.g. US. This follows https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#region_codes ApigeeSecurityAction#region_codes}
        '''
        result = self._values.get("region_codes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def user_agents(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of user agents to deny. We look for exact matches. Limit 50 per action.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#user_agents ApigeeSecurityAction#user_agents}
        '''
        result = self._values.get("user_agents")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeSecurityActionConditionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigeeSecurityActionConditionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeSecurityAction.ApigeeSecurityActionConditionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2b4fbaae41fa72a25262dfed6507c5b8b82a3588e57dba3ca817099e70f8b4d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAccessTokens")
    def reset_access_tokens(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessTokens", []))

    @jsii.member(jsii_name="resetApiKeys")
    def reset_api_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiKeys", []))

    @jsii.member(jsii_name="resetApiProducts")
    def reset_api_products(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiProducts", []))

    @jsii.member(jsii_name="resetAsns")
    def reset_asns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAsns", []))

    @jsii.member(jsii_name="resetBotReasons")
    def reset_bot_reasons(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBotReasons", []))

    @jsii.member(jsii_name="resetDeveloperApps")
    def reset_developer_apps(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeveloperApps", []))

    @jsii.member(jsii_name="resetDevelopers")
    def reset_developers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDevelopers", []))

    @jsii.member(jsii_name="resetHttpMethods")
    def reset_http_methods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpMethods", []))

    @jsii.member(jsii_name="resetIpAddressRanges")
    def reset_ip_address_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddressRanges", []))

    @jsii.member(jsii_name="resetRegionCodes")
    def reset_region_codes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegionCodes", []))

    @jsii.member(jsii_name="resetUserAgents")
    def reset_user_agents(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserAgents", []))

    @builtins.property
    @jsii.member(jsii_name="accessTokensInput")
    def access_tokens_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accessTokensInput"))

    @builtins.property
    @jsii.member(jsii_name="apiKeysInput")
    def api_keys_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "apiKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="apiProductsInput")
    def api_products_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "apiProductsInput"))

    @builtins.property
    @jsii.member(jsii_name="asnsInput")
    def asns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "asnsInput"))

    @builtins.property
    @jsii.member(jsii_name="botReasonsInput")
    def bot_reasons_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "botReasonsInput"))

    @builtins.property
    @jsii.member(jsii_name="developerAppsInput")
    def developer_apps_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "developerAppsInput"))

    @builtins.property
    @jsii.member(jsii_name="developersInput")
    def developers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "developersInput"))

    @builtins.property
    @jsii.member(jsii_name="httpMethodsInput")
    def http_methods_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "httpMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressRangesInput")
    def ip_address_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipAddressRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="regionCodesInput")
    def region_codes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "regionCodesInput"))

    @builtins.property
    @jsii.member(jsii_name="userAgentsInput")
    def user_agents_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "userAgentsInput"))

    @builtins.property
    @jsii.member(jsii_name="accessTokens")
    def access_tokens(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accessTokens"))

    @access_tokens.setter
    def access_tokens(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5181514bf1e1ad61333e2b7305f5127debfe6c327eca47fd66948c7f9dcad04b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessTokens", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiKeys")
    def api_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "apiKeys"))

    @api_keys.setter
    def api_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bbc56a8f276de96fb46aab676a0552d18c9139911c6eda723f57c4073983a1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiProducts")
    def api_products(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "apiProducts"))

    @api_products.setter
    def api_products(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a5e4e7740a87f39cbdb09ff2f11f1af2b62960cf791feef1bdddcea4023ec80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiProducts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="asns")
    def asns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "asns"))

    @asns.setter
    def asns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e9a85940147d90afde588003d1c674a277163f8275ccb565d452e43e755a100)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "asns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="botReasons")
    def bot_reasons(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "botReasons"))

    @bot_reasons.setter
    def bot_reasons(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fb1075936c998c221780f6f079c6fbd26192fa669159148e2233860aa3b1643)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "botReasons", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="developerApps")
    def developer_apps(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "developerApps"))

    @developer_apps.setter
    def developer_apps(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71837fb1f932a2790ee375f8c05ad4644b9a4c1519f81d827f832e6fd4b29439)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "developerApps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="developers")
    def developers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "developers"))

    @developers.setter
    def developers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__434e5d52aaef47d35cca29dcebfaa284d693bbfe449197970275bf306adeb1f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "developers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpMethods")
    def http_methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "httpMethods"))

    @http_methods.setter
    def http_methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e13d616c25ccd9004171b5435d20e9fa779ce5395ba0e73ba4b9f127d65c49a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpMethods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddressRanges")
    def ip_address_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipAddressRanges"))

    @ip_address_ranges.setter
    def ip_address_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb78057f69ef376a9e5c3f8c314644cd1efd67fa25b256db4d1f4dcb518f3ae5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddressRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regionCodes")
    def region_codes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "regionCodes"))

    @region_codes.setter
    def region_codes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43f1068df3f321d631a93a133324dd97ac9c54d686b7e88ef574d7bcfda0e82d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regionCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userAgents")
    def user_agents(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "userAgents"))

    @user_agents.setter
    def user_agents(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6e5c95f19cc1e0d51813be7bddccae327a658ade8e5d03740e045c36eeba032)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userAgents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApigeeSecurityActionConditionConfig]:
        return typing.cast(typing.Optional[ApigeeSecurityActionConditionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApigeeSecurityActionConditionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b205cb97d7c914c8d1e5e6b8daabf6907593104b8ff8721c92523ba60d69ea68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeSecurityAction.ApigeeSecurityActionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "condition_config": "conditionConfig",
        "env_id": "envId",
        "org_id": "orgId",
        "security_action_id": "securityActionId",
        "state": "state",
        "allow": "allow",
        "api_proxies": "apiProxies",
        "deny": "deny",
        "description": "description",
        "expire_time": "expireTime",
        "flag": "flag",
        "id": "id",
        "timeouts": "timeouts",
        "ttl": "ttl",
    },
)
class ApigeeSecurityActionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        condition_config: typing.Union[ApigeeSecurityActionConditionConfig, typing.Dict[builtins.str, typing.Any]],
        env_id: builtins.str,
        org_id: builtins.str,
        security_action_id: builtins.str,
        state: builtins.str,
        allow: typing.Optional[typing.Union[ApigeeSecurityActionAllow, typing.Dict[builtins.str, typing.Any]]] = None,
        api_proxies: typing.Optional[typing.Sequence[builtins.str]] = None,
        deny: typing.Optional[typing.Union["ApigeeSecurityActionDeny", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        expire_time: typing.Optional[builtins.str] = None,
        flag: typing.Optional[typing.Union["ApigeeSecurityActionFlag", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ApigeeSecurityActionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        ttl: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param condition_config: condition_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#condition_config ApigeeSecurityAction#condition_config}
        :param env_id: The Apigee environment that this security action applies to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#env_id ApigeeSecurityAction#env_id}
        :param org_id: The organization that this security action applies to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#org_id ApigeeSecurityAction#org_id}
        :param security_action_id: The ID to use for the SecurityAction, which will become the final component of the action's resource name. This value should be 0-61 characters, and valid format is (^a-z?$). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#security_action_id ApigeeSecurityAction#security_action_id}
        :param state: Only an ENABLED SecurityAction is enforced. An ENABLED SecurityAction past its expiration time will not be enforced. Possible values: ["ENABLED", "DISABLED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#state ApigeeSecurityAction#state}
        :param allow: allow block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#allow ApigeeSecurityAction#allow}
        :param api_proxies: If unset, this would apply to all proxies in the environment. If set, this action is enforced only if at least one proxy in the repeated list is deployed at the time of enforcement. If set, several restrictions are enforced on SecurityActions. There can be at most 100 enabled actions with proxies set in an env. Several other restrictions apply on conditions and are detailed later. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#api_proxies ApigeeSecurityAction#api_proxies}
        :param deny: deny block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#deny ApigeeSecurityAction#deny}
        :param description: An optional user provided description of the SecurityAction. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#description ApigeeSecurityAction#description}
        :param expire_time: The expiration for this SecurityAction. Uses RFC 3339, where generated output will always be Z-normalized and uses 0, 3, 6 or 9 fractional digits. Offsets other than "Z" are also accepted. Examples: "2014-10-02T15:01:23Z", "2014-10-02T15:01:23.045123456Z" or "2014-10-02T15:01:23+05:30". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#expire_time ApigeeSecurityAction#expire_time}
        :param flag: flag block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#flag ApigeeSecurityAction#flag}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#id ApigeeSecurityAction#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#timeouts ApigeeSecurityAction#timeouts}
        :param ttl: The TTL for this SecurityAction. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#ttl ApigeeSecurityAction#ttl}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(condition_config, dict):
            condition_config = ApigeeSecurityActionConditionConfig(**condition_config)
        if isinstance(allow, dict):
            allow = ApigeeSecurityActionAllow(**allow)
        if isinstance(deny, dict):
            deny = ApigeeSecurityActionDeny(**deny)
        if isinstance(flag, dict):
            flag = ApigeeSecurityActionFlag(**flag)
        if isinstance(timeouts, dict):
            timeouts = ApigeeSecurityActionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d2bb02dbc1d054ea00c0fdd7816925f04c5b8bb2a1d5e74d051614a4b96fea2)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument condition_config", value=condition_config, expected_type=type_hints["condition_config"])
            check_type(argname="argument env_id", value=env_id, expected_type=type_hints["env_id"])
            check_type(argname="argument org_id", value=org_id, expected_type=type_hints["org_id"])
            check_type(argname="argument security_action_id", value=security_action_id, expected_type=type_hints["security_action_id"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument allow", value=allow, expected_type=type_hints["allow"])
            check_type(argname="argument api_proxies", value=api_proxies, expected_type=type_hints["api_proxies"])
            check_type(argname="argument deny", value=deny, expected_type=type_hints["deny"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument expire_time", value=expire_time, expected_type=type_hints["expire_time"])
            check_type(argname="argument flag", value=flag, expected_type=type_hints["flag"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "condition_config": condition_config,
            "env_id": env_id,
            "org_id": org_id,
            "security_action_id": security_action_id,
            "state": state,
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
        if allow is not None:
            self._values["allow"] = allow
        if api_proxies is not None:
            self._values["api_proxies"] = api_proxies
        if deny is not None:
            self._values["deny"] = deny
        if description is not None:
            self._values["description"] = description
        if expire_time is not None:
            self._values["expire_time"] = expire_time
        if flag is not None:
            self._values["flag"] = flag
        if id is not None:
            self._values["id"] = id
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if ttl is not None:
            self._values["ttl"] = ttl

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
    def condition_config(self) -> ApigeeSecurityActionConditionConfig:
        '''condition_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#condition_config ApigeeSecurityAction#condition_config}
        '''
        result = self._values.get("condition_config")
        assert result is not None, "Required property 'condition_config' is missing"
        return typing.cast(ApigeeSecurityActionConditionConfig, result)

    @builtins.property
    def env_id(self) -> builtins.str:
        '''The Apigee environment that this security action applies to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#env_id ApigeeSecurityAction#env_id}
        '''
        result = self._values.get("env_id")
        assert result is not None, "Required property 'env_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def org_id(self) -> builtins.str:
        '''The organization that this security action applies to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#org_id ApigeeSecurityAction#org_id}
        '''
        result = self._values.get("org_id")
        assert result is not None, "Required property 'org_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def security_action_id(self) -> builtins.str:
        '''The ID to use for the SecurityAction, which will become the final component of the action's resource name.

        This value should be 0-61 characters, and valid format is (^a-z?$).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#security_action_id ApigeeSecurityAction#security_action_id}
        '''
        result = self._values.get("security_action_id")
        assert result is not None, "Required property 'security_action_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def state(self) -> builtins.str:
        '''Only an ENABLED SecurityAction is enforced.

        An ENABLED SecurityAction past its expiration time will not be enforced. Possible values: ["ENABLED", "DISABLED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#state ApigeeSecurityAction#state}
        '''
        result = self._values.get("state")
        assert result is not None, "Required property 'state' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow(self) -> typing.Optional[ApigeeSecurityActionAllow]:
        '''allow block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#allow ApigeeSecurityAction#allow}
        '''
        result = self._values.get("allow")
        return typing.cast(typing.Optional[ApigeeSecurityActionAllow], result)

    @builtins.property
    def api_proxies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''If unset, this would apply to all proxies in the environment.

        If set, this action is enforced only if at least one proxy in the repeated
        list is deployed at the time of enforcement. If set, several restrictions are enforced on SecurityActions.
        There can be at most 100 enabled actions with proxies set in an env.
        Several other restrictions apply on conditions and are detailed later.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#api_proxies ApigeeSecurityAction#api_proxies}
        '''
        result = self._values.get("api_proxies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def deny(self) -> typing.Optional["ApigeeSecurityActionDeny"]:
        '''deny block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#deny ApigeeSecurityAction#deny}
        '''
        result = self._values.get("deny")
        return typing.cast(typing.Optional["ApigeeSecurityActionDeny"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional user provided description of the SecurityAction.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#description ApigeeSecurityAction#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expire_time(self) -> typing.Optional[builtins.str]:
        '''The expiration for this SecurityAction.

        Uses RFC 3339, where generated output will always be Z-normalized and uses 0, 3, 6 or 9
        fractional digits. Offsets other than "Z" are also accepted.
        Examples: "2014-10-02T15:01:23Z", "2014-10-02T15:01:23.045123456Z" or "2014-10-02T15:01:23+05:30".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#expire_time ApigeeSecurityAction#expire_time}
        '''
        result = self._values.get("expire_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def flag(self) -> typing.Optional["ApigeeSecurityActionFlag"]:
        '''flag block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#flag ApigeeSecurityAction#flag}
        '''
        result = self._values.get("flag")
        return typing.cast(typing.Optional["ApigeeSecurityActionFlag"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#id ApigeeSecurityAction#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ApigeeSecurityActionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#timeouts ApigeeSecurityAction#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ApigeeSecurityActionTimeouts"], result)

    @builtins.property
    def ttl(self) -> typing.Optional[builtins.str]:
        '''The TTL for this SecurityAction. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#ttl ApigeeSecurityAction#ttl}
        '''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeSecurityActionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeSecurityAction.ApigeeSecurityActionDeny",
    jsii_struct_bases=[],
    name_mapping={"response_code": "responseCode"},
)
class ApigeeSecurityActionDeny:
    def __init__(self, *, response_code: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param response_code: The HTTP response code if the Action = DENY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#response_code ApigeeSecurityAction#response_code}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__003c458d89b692d1fabf84a5f871e4a20f70db6d24262841b2d244039bb3faed)
            check_type(argname="argument response_code", value=response_code, expected_type=type_hints["response_code"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if response_code is not None:
            self._values["response_code"] = response_code

    @builtins.property
    def response_code(self) -> typing.Optional[jsii.Number]:
        '''The HTTP response code if the Action = DENY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#response_code ApigeeSecurityAction#response_code}
        '''
        result = self._values.get("response_code")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeSecurityActionDeny(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigeeSecurityActionDenyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeSecurityAction.ApigeeSecurityActionDenyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1c72f556f3ccf78a28f1b730242ef58637b1757ba9e29fc8c6dc78c711fa7e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetResponseCode")
    def reset_response_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponseCode", []))

    @builtins.property
    @jsii.member(jsii_name="responseCodeInput")
    def response_code_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "responseCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="responseCode")
    def response_code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "responseCode"))

    @response_code.setter
    def response_code(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02857db4f82b400907d0c089f9e8f9e00f8e3c6405f6e4d6f0696a66d3d58d96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApigeeSecurityActionDeny]:
        return typing.cast(typing.Optional[ApigeeSecurityActionDeny], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ApigeeSecurityActionDeny]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc5b6763a5243a0f33839cc47d85b902305a71704dc6ae39789113808ad2784e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeSecurityAction.ApigeeSecurityActionFlag",
    jsii_struct_bases=[],
    name_mapping={"headers": "headers"},
)
class ApigeeSecurityActionFlag:
    def __init__(
        self,
        *,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigeeSecurityActionFlagHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param headers: headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#headers ApigeeSecurityAction#headers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e5de675f48ffb97d9cd251efe19f8f8a6efc2c4f94ef34b3c41560324035842)
            check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if headers is not None:
            self._values["headers"] = headers

    @builtins.property
    def headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigeeSecurityActionFlagHeaders"]]]:
        '''headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#headers ApigeeSecurityAction#headers}
        '''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigeeSecurityActionFlagHeaders"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeSecurityActionFlag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeSecurityAction.ApigeeSecurityActionFlagHeaders",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class ApigeeSecurityActionFlagHeaders:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The header name to be sent to the target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#name ApigeeSecurityAction#name}
        :param value: The header value to be sent to the target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#value ApigeeSecurityAction#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07ddb2d8efae2fd8026e9f3815ff7c53fafb151d7c8cd5c39eb0bf7fb6b3619a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The header name to be sent to the target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#name ApigeeSecurityAction#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The header value to be sent to the target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#value ApigeeSecurityAction#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeSecurityActionFlagHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigeeSecurityActionFlagHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeSecurityAction.ApigeeSecurityActionFlagHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7e74aad2ff48af0229f01c9b14847d2453cda93a7f8ea29243238b97c49df0e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApigeeSecurityActionFlagHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60ca0d57faeea4e10579b0592c153240560d34106bb9d16f701873cd109e6b25)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApigeeSecurityActionFlagHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3a47f22c6271e8d4dd722bf5d5ddb8572fe6554436ef6fb6034463a7c4ed8a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a814a8ed4c4f10a371af15e641256a6e9fe3380da0bc9ee3896317ef749a632)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd942bde24b7b52bae8f2396415174e9bbf71da5956ffd76c524e8978669c899)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeSecurityActionFlagHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeSecurityActionFlagHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeSecurityActionFlagHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__847bfd07152ce6e66c25d464ac02328106e23a3f444054579f63241a694c1bb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigeeSecurityActionFlagHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeSecurityAction.ApigeeSecurityActionFlagHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea576b90adebaff042c3eabda53219e5ba593ed19e202a420b46f10855e59cea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac16b542ab5aabd843831387c7ac8a1c51c322e395bc792d9c919cb072152b83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e4fbc891183bcaec63115a704ba0837b3b0d53cd4c3b56c8fc95e14cdfb3e9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeSecurityActionFlagHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeSecurityActionFlagHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeSecurityActionFlagHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__207429772e822508ce0ab75ee2239bdf5b8e558fe72dbb485c373124de47267e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigeeSecurityActionFlagOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeSecurityAction.ApigeeSecurityActionFlagOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__044261018126d9c013629656a1199b6a4cd7541c1dc09163d2c55704ee300773)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHeaders")
    def put_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeSecurityActionFlagHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dffa19bf49400a0f715bd727928702a6a451e3388f62a12f186a8843028da18a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeaders", [value]))

    @jsii.member(jsii_name="resetHeaders")
    def reset_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaders", []))

    @builtins.property
    @jsii.member(jsii_name="headers")
    def headers(self) -> ApigeeSecurityActionFlagHeadersList:
        return typing.cast(ApigeeSecurityActionFlagHeadersList, jsii.get(self, "headers"))

    @builtins.property
    @jsii.member(jsii_name="headersInput")
    def headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeSecurityActionFlagHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeSecurityActionFlagHeaders]]], jsii.get(self, "headersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApigeeSecurityActionFlag]:
        return typing.cast(typing.Optional[ApigeeSecurityActionFlag], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ApigeeSecurityActionFlag]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__349c21f192c4411575be715f6ea6afcacb98c73e650fe28d359b6b279396b311)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeSecurityAction.ApigeeSecurityActionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class ApigeeSecurityActionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#create ApigeeSecurityAction#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#delete ApigeeSecurityAction#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bedb62276b266027de3b4f1d9b56766c54724d7708570f30b1ef31e5db01851e)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#create ApigeeSecurityAction#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.49.3/docs/resources/apigee_security_action#delete ApigeeSecurityAction#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeSecurityActionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigeeSecurityActionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeSecurityAction.ApigeeSecurityActionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6d40492a133d5d464c06935b1d4e864f068eae856e500da0cf8e7b8f3fbec38)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c682a7e28b3f39dd6b8695a5b4f0db95195587b9eda53b99be97cfb0b0abc7b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bff8d524d7e1f6571cb76509ce32cae24fd17c79a990680ab412fbbc5841845)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeSecurityActionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeSecurityActionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeSecurityActionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b06c048697238b9ea64b2feff59c3c3d066064a3d8964d40fc9741eef2664e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ApigeeSecurityAction",
    "ApigeeSecurityActionAllow",
    "ApigeeSecurityActionAllowOutputReference",
    "ApigeeSecurityActionConditionConfig",
    "ApigeeSecurityActionConditionConfigOutputReference",
    "ApigeeSecurityActionConfig",
    "ApigeeSecurityActionDeny",
    "ApigeeSecurityActionDenyOutputReference",
    "ApigeeSecurityActionFlag",
    "ApigeeSecurityActionFlagHeaders",
    "ApigeeSecurityActionFlagHeadersList",
    "ApigeeSecurityActionFlagHeadersOutputReference",
    "ApigeeSecurityActionFlagOutputReference",
    "ApigeeSecurityActionTimeouts",
    "ApigeeSecurityActionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__9fe5237d0b8ce1e99bbf712442b3cb247ca8fb78cb5c30605e27718cd9c9ff80(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    condition_config: typing.Union[ApigeeSecurityActionConditionConfig, typing.Dict[builtins.str, typing.Any]],
    env_id: builtins.str,
    org_id: builtins.str,
    security_action_id: builtins.str,
    state: builtins.str,
    allow: typing.Optional[typing.Union[ApigeeSecurityActionAllow, typing.Dict[builtins.str, typing.Any]]] = None,
    api_proxies: typing.Optional[typing.Sequence[builtins.str]] = None,
    deny: typing.Optional[typing.Union[ApigeeSecurityActionDeny, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    expire_time: typing.Optional[builtins.str] = None,
    flag: typing.Optional[typing.Union[ApigeeSecurityActionFlag, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ApigeeSecurityActionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    ttl: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__b48722c9d7f76d59fb0247954ae20fbc3474e2c6bb4835beba7ca4bdcf6c114f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d76cb8a82c9dc237d261f7ed35e8e714cf33337747be1b69656bb1e9ba2af7e2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce4ab2ebcba1798058eb9f58c91542d7e849fd8d4036d4c8003fb37265adc5be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50af45e6d6e84eb8ee9e1daa442a19f474d81338b044197c35cda54bb46ea65a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1677ab90ab71e2598ec104857335d63b4f3d18fade160bd9044372075c03948a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1247a3b3fbbf411cd82271f7312fc268429700177b55a3bf6d0ae4a5d4494331(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05f1b91a87036bcb9af8548b7dac50adbc72c627c89aa92f0efda139f06c9fed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc1787aef55e6feaf7c7ac116ea8176505ea67ad200b404b45a9734ed115a84e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbfd51e73f27af88e8ca02e69d9c27d3f559f9a44629b3b97689b97cb8393f36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b5cffa20a68934a9dd46082f8d8c719f9185f5e2504c0d4464fc384c8c46d5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ecd4653bb76145e0be2d548aa2a55fd6cffe88319a434792100929666910914(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f31ea0d3149018fa169048af96a21f1918e8e64ed0d85f7bc859d78dc77c9794(
    value: typing.Optional[ApigeeSecurityActionAllow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5585f29ff88d80bfd681eb63541a70f18c203cb27724d5624949ba293ec2e3d0(
    *,
    access_tokens: typing.Optional[typing.Sequence[builtins.str]] = None,
    api_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    api_products: typing.Optional[typing.Sequence[builtins.str]] = None,
    asns: typing.Optional[typing.Sequence[builtins.str]] = None,
    bot_reasons: typing.Optional[typing.Sequence[builtins.str]] = None,
    developer_apps: typing.Optional[typing.Sequence[builtins.str]] = None,
    developers: typing.Optional[typing.Sequence[builtins.str]] = None,
    http_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
    ip_address_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_agents: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2b4fbaae41fa72a25262dfed6507c5b8b82a3588e57dba3ca817099e70f8b4d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5181514bf1e1ad61333e2b7305f5127debfe6c327eca47fd66948c7f9dcad04b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bbc56a8f276de96fb46aab676a0552d18c9139911c6eda723f57c4073983a1f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a5e4e7740a87f39cbdb09ff2f11f1af2b62960cf791feef1bdddcea4023ec80(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e9a85940147d90afde588003d1c674a277163f8275ccb565d452e43e755a100(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fb1075936c998c221780f6f079c6fbd26192fa669159148e2233860aa3b1643(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71837fb1f932a2790ee375f8c05ad4644b9a4c1519f81d827f832e6fd4b29439(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__434e5d52aaef47d35cca29dcebfaa284d693bbfe449197970275bf306adeb1f4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e13d616c25ccd9004171b5435d20e9fa779ce5395ba0e73ba4b9f127d65c49a3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb78057f69ef376a9e5c3f8c314644cd1efd67fa25b256db4d1f4dcb518f3ae5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43f1068df3f321d631a93a133324dd97ac9c54d686b7e88ef574d7bcfda0e82d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6e5c95f19cc1e0d51813be7bddccae327a658ade8e5d03740e045c36eeba032(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b205cb97d7c914c8d1e5e6b8daabf6907593104b8ff8721c92523ba60d69ea68(
    value: typing.Optional[ApigeeSecurityActionConditionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d2bb02dbc1d054ea00c0fdd7816925f04c5b8bb2a1d5e74d051614a4b96fea2(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    condition_config: typing.Union[ApigeeSecurityActionConditionConfig, typing.Dict[builtins.str, typing.Any]],
    env_id: builtins.str,
    org_id: builtins.str,
    security_action_id: builtins.str,
    state: builtins.str,
    allow: typing.Optional[typing.Union[ApigeeSecurityActionAllow, typing.Dict[builtins.str, typing.Any]]] = None,
    api_proxies: typing.Optional[typing.Sequence[builtins.str]] = None,
    deny: typing.Optional[typing.Union[ApigeeSecurityActionDeny, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    expire_time: typing.Optional[builtins.str] = None,
    flag: typing.Optional[typing.Union[ApigeeSecurityActionFlag, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ApigeeSecurityActionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    ttl: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__003c458d89b692d1fabf84a5f871e4a20f70db6d24262841b2d244039bb3faed(
    *,
    response_code: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1c72f556f3ccf78a28f1b730242ef58637b1757ba9e29fc8c6dc78c711fa7e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02857db4f82b400907d0c089f9e8f9e00f8e3c6405f6e4d6f0696a66d3d58d96(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc5b6763a5243a0f33839cc47d85b902305a71704dc6ae39789113808ad2784e(
    value: typing.Optional[ApigeeSecurityActionDeny],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e5de675f48ffb97d9cd251efe19f8f8a6efc2c4f94ef34b3c41560324035842(
    *,
    headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeSecurityActionFlagHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07ddb2d8efae2fd8026e9f3815ff7c53fafb151d7c8cd5c39eb0bf7fb6b3619a(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7e74aad2ff48af0229f01c9b14847d2453cda93a7f8ea29243238b97c49df0e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60ca0d57faeea4e10579b0592c153240560d34106bb9d16f701873cd109e6b25(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3a47f22c6271e8d4dd722bf5d5ddb8572fe6554436ef6fb6034463a7c4ed8a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a814a8ed4c4f10a371af15e641256a6e9fe3380da0bc9ee3896317ef749a632(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd942bde24b7b52bae8f2396415174e9bbf71da5956ffd76c524e8978669c899(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__847bfd07152ce6e66c25d464ac02328106e23a3f444054579f63241a694c1bb1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeSecurityActionFlagHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea576b90adebaff042c3eabda53219e5ba593ed19e202a420b46f10855e59cea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac16b542ab5aabd843831387c7ac8a1c51c322e395bc792d9c919cb072152b83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e4fbc891183bcaec63115a704ba0837b3b0d53cd4c3b56c8fc95e14cdfb3e9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__207429772e822508ce0ab75ee2239bdf5b8e558fe72dbb485c373124de47267e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeSecurityActionFlagHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__044261018126d9c013629656a1199b6a4cd7541c1dc09163d2c55704ee300773(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dffa19bf49400a0f715bd727928702a6a451e3388f62a12f186a8843028da18a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeSecurityActionFlagHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__349c21f192c4411575be715f6ea6afcacb98c73e650fe28d359b6b279396b311(
    value: typing.Optional[ApigeeSecurityActionFlag],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bedb62276b266027de3b4f1d9b56766c54724d7708570f30b1ef31e5db01851e(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6d40492a133d5d464c06935b1d4e864f068eae856e500da0cf8e7b8f3fbec38(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c682a7e28b3f39dd6b8695a5b4f0db95195587b9eda53b99be97cfb0b0abc7b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bff8d524d7e1f6571cb76509ce32cae24fd17c79a990680ab412fbbc5841845(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b06c048697238b9ea64b2feff59c3c3d066064a3d8964d40fc9741eef2664e4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeSecurityActionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
