r'''
# `google_apigee_security_action`

Refer to the Terraform Registry for docs: [`google_apigee_security_action`](https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action).
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


class GoogleApigeeSecurityAction(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeSecurityAction.GoogleApigeeSecurityAction",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action google_apigee_security_action}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        condition_config: typing.Union["GoogleApigeeSecurityActionConditionConfig", typing.Dict[builtins.str, typing.Any]],
        env_id: builtins.str,
        org_id: builtins.str,
        security_action_id: builtins.str,
        state: builtins.str,
        allow: typing.Optional[typing.Union["GoogleApigeeSecurityActionAllow", typing.Dict[builtins.str, typing.Any]]] = None,
        api_proxies: typing.Optional[typing.Sequence[builtins.str]] = None,
        deny: typing.Optional[typing.Union["GoogleApigeeSecurityActionDeny", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        expire_time: typing.Optional[builtins.str] = None,
        flag: typing.Optional[typing.Union["GoogleApigeeSecurityActionFlag", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleApigeeSecurityActionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        ttl: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action google_apigee_security_action} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param condition_config: condition_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#condition_config GoogleApigeeSecurityAction#condition_config}
        :param env_id: The Apigee environment that this security action applies to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#env_id GoogleApigeeSecurityAction#env_id}
        :param org_id: The organization that this security action applies to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#org_id GoogleApigeeSecurityAction#org_id}
        :param security_action_id: The ID to use for the SecurityAction, which will become the final component of the action's resource name. This value should be 0-61 characters, and valid format is (^a-z?$). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#security_action_id GoogleApigeeSecurityAction#security_action_id}
        :param state: Only an ENABLED SecurityAction is enforced. An ENABLED SecurityAction past its expiration time will not be enforced. Possible values: ["ENABLED", "DISABLED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#state GoogleApigeeSecurityAction#state}
        :param allow: allow block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#allow GoogleApigeeSecurityAction#allow}
        :param api_proxies: If unset, this would apply to all proxies in the environment. If set, this action is enforced only if at least one proxy in the repeated list is deployed at the time of enforcement. If set, several restrictions are enforced on SecurityActions. There can be at most 100 enabled actions with proxies set in an env. Several other restrictions apply on conditions and are detailed later. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#api_proxies GoogleApigeeSecurityAction#api_proxies}
        :param deny: deny block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#deny GoogleApigeeSecurityAction#deny}
        :param description: An optional user provided description of the SecurityAction. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#description GoogleApigeeSecurityAction#description}
        :param expire_time: The expiration for this SecurityAction. Uses RFC 3339, where generated output will always be Z-normalized and uses 0, 3, 6 or 9 fractional digits. Offsets other than "Z" are also accepted. Examples: "2014-10-02T15:01:23Z", "2014-10-02T15:01:23.045123456Z" or "2014-10-02T15:01:23+05:30". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#expire_time GoogleApigeeSecurityAction#expire_time}
        :param flag: flag block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#flag GoogleApigeeSecurityAction#flag}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#id GoogleApigeeSecurityAction#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#timeouts GoogleApigeeSecurityAction#timeouts}
        :param ttl: The TTL for this SecurityAction. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#ttl GoogleApigeeSecurityAction#ttl}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe60952e6ea68fd0c068bf066c65885d824f406e0b9935ef396cedc4819fa32e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleApigeeSecurityActionConfig(
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
        '''Generates CDKTF code for importing a GoogleApigeeSecurityAction resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleApigeeSecurityAction to import.
        :param import_from_id: The id of the existing GoogleApigeeSecurityAction that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleApigeeSecurityAction to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__852320f414122553dc9a2776680d4583b110387a7be4050dd6b049d10bceb297)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAllow")
    def put_allow(self) -> None:
        value = GoogleApigeeSecurityActionAllow()

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
        :param access_tokens: A list of accessTokens. Limit 1000 per action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#access_tokens GoogleApigeeSecurityAction#access_tokens}
        :param api_keys: A list of API keys. Limit 1000 per action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#api_keys GoogleApigeeSecurityAction#api_keys}
        :param api_products: A list of API Products. Limit 1000 per action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#api_products GoogleApigeeSecurityAction#api_products}
        :param asns: A list of ASN numbers to act on, e.g. 23. https://en.wikipedia.org/wiki/Autonomous_system_(Internet) This uses int64 instead of uint32 because of https://linter.aip.dev/141/forbidden-types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#asns GoogleApigeeSecurityAction#asns}
        :param bot_reasons: A list of Bot Reasons. Current options: Flooder, Brute Guessor, Static Content Scraper, OAuth Abuser, Robot Abuser, TorListRule, Advanced Anomaly Detection, Advanced API Scraper, Search Engine Crawlers, Public Clouds, Public Cloud AWS, Public Cloud Azure, and Public Cloud Google. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#bot_reasons GoogleApigeeSecurityAction#bot_reasons}
        :param developer_apps: A list of developer apps. Limit 1000 per action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#developer_apps GoogleApigeeSecurityAction#developer_apps}
        :param developers: A list of developers. Limit 1000 per action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#developers GoogleApigeeSecurityAction#developers}
        :param http_methods: Act only on particular HTTP methods. E.g. A read-only API can block POST/PUT/DELETE methods. Accepted values are: GET, HEAD, POST, PUT, DELETE, CONNECT, OPTIONS, TRACE and PATCH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#http_methods GoogleApigeeSecurityAction#http_methods}
        :param ip_address_ranges: A list of IP addresses. This could be either IPv4 or IPv6. Limited to 100 per action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#ip_address_ranges GoogleApigeeSecurityAction#ip_address_ranges}
        :param region_codes: A list of countries/region codes to act on, e.g. US. This follows https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#region_codes GoogleApigeeSecurityAction#region_codes}
        :param user_agents: A list of user agents to deny. We look for exact matches. Limit 50 per action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#user_agents GoogleApigeeSecurityAction#user_agents}
        '''
        value = GoogleApigeeSecurityActionConditionConfig(
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
        :param response_code: The HTTP response code if the Action = DENY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#response_code GoogleApigeeSecurityAction#response_code}
        '''
        value = GoogleApigeeSecurityActionDeny(response_code=response_code)

        return typing.cast(None, jsii.invoke(self, "putDeny", [value]))

    @jsii.member(jsii_name="putFlag")
    def put_flag(
        self,
        *,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApigeeSecurityActionFlagHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param headers: headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#headers GoogleApigeeSecurityAction#headers}
        '''
        value = GoogleApigeeSecurityActionFlag(headers=headers)

        return typing.cast(None, jsii.invoke(self, "putFlag", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#create GoogleApigeeSecurityAction#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#delete GoogleApigeeSecurityAction#delete}.
        '''
        value = GoogleApigeeSecurityActionTimeouts(create=create, delete=delete)

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
    def allow(self) -> "GoogleApigeeSecurityActionAllowOutputReference":
        return typing.cast("GoogleApigeeSecurityActionAllowOutputReference", jsii.get(self, "allow"))

    @builtins.property
    @jsii.member(jsii_name="conditionConfig")
    def condition_config(
        self,
    ) -> "GoogleApigeeSecurityActionConditionConfigOutputReference":
        return typing.cast("GoogleApigeeSecurityActionConditionConfigOutputReference", jsii.get(self, "conditionConfig"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="deny")
    def deny(self) -> "GoogleApigeeSecurityActionDenyOutputReference":
        return typing.cast("GoogleApigeeSecurityActionDenyOutputReference", jsii.get(self, "deny"))

    @builtins.property
    @jsii.member(jsii_name="flag")
    def flag(self) -> "GoogleApigeeSecurityActionFlagOutputReference":
        return typing.cast("GoogleApigeeSecurityActionFlagOutputReference", jsii.get(self, "flag"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleApigeeSecurityActionTimeoutsOutputReference":
        return typing.cast("GoogleApigeeSecurityActionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="allowInput")
    def allow_input(self) -> typing.Optional["GoogleApigeeSecurityActionAllow"]:
        return typing.cast(typing.Optional["GoogleApigeeSecurityActionAllow"], jsii.get(self, "allowInput"))

    @builtins.property
    @jsii.member(jsii_name="apiProxiesInput")
    def api_proxies_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "apiProxiesInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionConfigInput")
    def condition_config_input(
        self,
    ) -> typing.Optional["GoogleApigeeSecurityActionConditionConfig"]:
        return typing.cast(typing.Optional["GoogleApigeeSecurityActionConditionConfig"], jsii.get(self, "conditionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="denyInput")
    def deny_input(self) -> typing.Optional["GoogleApigeeSecurityActionDeny"]:
        return typing.cast(typing.Optional["GoogleApigeeSecurityActionDeny"], jsii.get(self, "denyInput"))

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
    def flag_input(self) -> typing.Optional["GoogleApigeeSecurityActionFlag"]:
        return typing.cast(typing.Optional["GoogleApigeeSecurityActionFlag"], jsii.get(self, "flagInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleApigeeSecurityActionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleApigeeSecurityActionTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ff399e57d58388fc0876e3c34985abd3707ed8a91c1d6ab387e70fc8503febe1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiProxies", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0240b13805c31e889a6b136328bd2648863e9afae64b974d258e263c139b303c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="envId")
    def env_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "envId"))

    @env_id.setter
    def env_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3ff8fcb294d114d11e1629816e3f3de3516e61264cc6558378099ecde42b115)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "envId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expireTime")
    def expire_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expireTime"))

    @expire_time.setter
    def expire_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31ff7c9c308cbe9484fcea30244357c7eee4a90cee50369dfb19ae3c96bf0ef4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expireTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c596d7b696b251bd8b2f1c22006f9c105d2a4eddefd2550ccf4b65bd7e89468)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="orgId")
    def org_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orgId"))

    @org_id.setter
    def org_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1d708a92e0be85a54dd0ebf0a73805de7975c037d1ff2988dcd009ceba90406)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orgId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityActionId")
    def security_action_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityActionId"))

    @security_action_id.setter
    def security_action_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e128238f3baf3c00f762a47bd1eb97be10092e01a45daaf5dca9777e01ccbb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityActionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4285b9864596520fe090a7ffbcf7ce514e37d2c60a05e3f143689cfa33c55e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ttl"))

    @ttl.setter
    def ttl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__158c149ef98cac34ea5431e35294402a58fd7500c31e88a6237d5db78e078633)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ttl", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeSecurityAction.GoogleApigeeSecurityActionAllow",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleApigeeSecurityActionAllow:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeSecurityActionAllow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApigeeSecurityActionAllowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeSecurityAction.GoogleApigeeSecurityActionAllowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__16c3b58a9a43fdf162cf9545aca83c2cfe183a4b4cc0dfff76ac5cb5561eb367)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleApigeeSecurityActionAllow]:
        return typing.cast(typing.Optional[GoogleApigeeSecurityActionAllow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApigeeSecurityActionAllow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c898f641ddfc5a3db90e79eb032fd168b6638b186b9387206ce5d9e182c1ec2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeSecurityAction.GoogleApigeeSecurityActionConditionConfig",
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
class GoogleApigeeSecurityActionConditionConfig:
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
        :param access_tokens: A list of accessTokens. Limit 1000 per action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#access_tokens GoogleApigeeSecurityAction#access_tokens}
        :param api_keys: A list of API keys. Limit 1000 per action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#api_keys GoogleApigeeSecurityAction#api_keys}
        :param api_products: A list of API Products. Limit 1000 per action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#api_products GoogleApigeeSecurityAction#api_products}
        :param asns: A list of ASN numbers to act on, e.g. 23. https://en.wikipedia.org/wiki/Autonomous_system_(Internet) This uses int64 instead of uint32 because of https://linter.aip.dev/141/forbidden-types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#asns GoogleApigeeSecurityAction#asns}
        :param bot_reasons: A list of Bot Reasons. Current options: Flooder, Brute Guessor, Static Content Scraper, OAuth Abuser, Robot Abuser, TorListRule, Advanced Anomaly Detection, Advanced API Scraper, Search Engine Crawlers, Public Clouds, Public Cloud AWS, Public Cloud Azure, and Public Cloud Google. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#bot_reasons GoogleApigeeSecurityAction#bot_reasons}
        :param developer_apps: A list of developer apps. Limit 1000 per action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#developer_apps GoogleApigeeSecurityAction#developer_apps}
        :param developers: A list of developers. Limit 1000 per action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#developers GoogleApigeeSecurityAction#developers}
        :param http_methods: Act only on particular HTTP methods. E.g. A read-only API can block POST/PUT/DELETE methods. Accepted values are: GET, HEAD, POST, PUT, DELETE, CONNECT, OPTIONS, TRACE and PATCH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#http_methods GoogleApigeeSecurityAction#http_methods}
        :param ip_address_ranges: A list of IP addresses. This could be either IPv4 or IPv6. Limited to 100 per action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#ip_address_ranges GoogleApigeeSecurityAction#ip_address_ranges}
        :param region_codes: A list of countries/region codes to act on, e.g. US. This follows https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#region_codes GoogleApigeeSecurityAction#region_codes}
        :param user_agents: A list of user agents to deny. We look for exact matches. Limit 50 per action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#user_agents GoogleApigeeSecurityAction#user_agents}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__105f5626ce17284b4bd26af1005de395b7c4ecc6560c4a3e72f485c9ca02a896)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#access_tokens GoogleApigeeSecurityAction#access_tokens}
        '''
        result = self._values.get("access_tokens")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def api_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of API keys. Limit 1000 per action.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#api_keys GoogleApigeeSecurityAction#api_keys}
        '''
        result = self._values.get("api_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def api_products(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of API Products. Limit 1000 per action.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#api_products GoogleApigeeSecurityAction#api_products}
        '''
        result = self._values.get("api_products")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def asns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of ASN numbers to act on, e.g. 23. https://en.wikipedia.org/wiki/Autonomous_system_(Internet) This uses int64 instead of uint32 because of https://linter.aip.dev/141/forbidden-types.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#asns GoogleApigeeSecurityAction#asns}
        '''
        result = self._values.get("asns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def bot_reasons(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Bot Reasons.

        Current options: Flooder, Brute Guessor, Static Content Scraper,
        OAuth Abuser, Robot Abuser, TorListRule, Advanced Anomaly Detection, Advanced API Scraper,
        Search Engine Crawlers, Public Clouds, Public Cloud AWS, Public Cloud Azure, and Public Cloud Google.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#bot_reasons GoogleApigeeSecurityAction#bot_reasons}
        '''
        result = self._values.get("bot_reasons")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def developer_apps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of developer apps. Limit 1000 per action.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#developer_apps GoogleApigeeSecurityAction#developer_apps}
        '''
        result = self._values.get("developer_apps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def developers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of developers. Limit 1000 per action.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#developers GoogleApigeeSecurityAction#developers}
        '''
        result = self._values.get("developers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def http_methods(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Act only on particular HTTP methods.

        E.g. A read-only API can block POST/PUT/DELETE methods.
        Accepted values are: GET, HEAD, POST, PUT, DELETE, CONNECT, OPTIONS, TRACE and PATCH.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#http_methods GoogleApigeeSecurityAction#http_methods}
        '''
        result = self._values.get("http_methods")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ip_address_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of IP addresses. This could be either IPv4 or IPv6. Limited to 100 per action.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#ip_address_ranges GoogleApigeeSecurityAction#ip_address_ranges}
        '''
        result = self._values.get("ip_address_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def region_codes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of countries/region codes to act on, e.g. US. This follows https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#region_codes GoogleApigeeSecurityAction#region_codes}
        '''
        result = self._values.get("region_codes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def user_agents(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of user agents to deny. We look for exact matches. Limit 50 per action.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#user_agents GoogleApigeeSecurityAction#user_agents}
        '''
        result = self._values.get("user_agents")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeSecurityActionConditionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApigeeSecurityActionConditionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeSecurityAction.GoogleApigeeSecurityActionConditionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__983543985fcbcb892ea117ee31460e7eaddb485b951f5c8104cf81bfe54e7721)
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
            type_hints = typing.get_type_hints(_typecheckingstub__10550c73646d4784a6ff91bd09d063682ebcbfb7b452c0167f8e1ad235a6174a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessTokens", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiKeys")
    def api_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "apiKeys"))

    @api_keys.setter
    def api_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__714e87921fe6fae6cda6cbb63167bc1dafc7f2214b6bbd0d78428029f489949f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiProducts")
    def api_products(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "apiProducts"))

    @api_products.setter
    def api_products(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93528a581733958602359e4f147b74192365832aac39894bc0bc2186787e8e4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiProducts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="asns")
    def asns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "asns"))

    @asns.setter
    def asns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8efcb2c5e6c768572a24cb1a3f4970756b68a5eeb3d786fd087bd0bd7086be5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "asns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="botReasons")
    def bot_reasons(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "botReasons"))

    @bot_reasons.setter
    def bot_reasons(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e94156f283693f07c97f57a95ce6513b7bc0d28d91af4eee324619b346f78b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "botReasons", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="developerApps")
    def developer_apps(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "developerApps"))

    @developer_apps.setter
    def developer_apps(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84f90480cb6bf7bfa3e06fcf3d30b4481b65a7baed3b35b6f25f7b5d6bcae4fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "developerApps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="developers")
    def developers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "developers"))

    @developers.setter
    def developers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afea04a035e479414390172378ccea8c36eb926749c575d44b58d614499ffce1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "developers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpMethods")
    def http_methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "httpMethods"))

    @http_methods.setter
    def http_methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75ad3da8ab036b78fecf16bd50b0fa020e1282414397bc320bf55bf7175e6854)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpMethods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddressRanges")
    def ip_address_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipAddressRanges"))

    @ip_address_ranges.setter
    def ip_address_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81899fa0f02df030f5256c9009fbcb0cdbcae5c86a86ba25716e0c5ae42419c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddressRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regionCodes")
    def region_codes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "regionCodes"))

    @region_codes.setter
    def region_codes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d29b2062cf77406421879158a28ec04f61151aac8590190de00fb20f3783e304)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regionCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userAgents")
    def user_agents(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "userAgents"))

    @user_agents.setter
    def user_agents(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11fc98a90104e18cc8c27f3e8d8b77d73fa3388f0a3f9989e0d572466fa69c76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userAgents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleApigeeSecurityActionConditionConfig]:
        return typing.cast(typing.Optional[GoogleApigeeSecurityActionConditionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApigeeSecurityActionConditionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__595b3e465acf7e887ae10ac4abd329623bfdb545789c377900d2ef523147c9d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeSecurityAction.GoogleApigeeSecurityActionConfig",
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
class GoogleApigeeSecurityActionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        condition_config: typing.Union[GoogleApigeeSecurityActionConditionConfig, typing.Dict[builtins.str, typing.Any]],
        env_id: builtins.str,
        org_id: builtins.str,
        security_action_id: builtins.str,
        state: builtins.str,
        allow: typing.Optional[typing.Union[GoogleApigeeSecurityActionAllow, typing.Dict[builtins.str, typing.Any]]] = None,
        api_proxies: typing.Optional[typing.Sequence[builtins.str]] = None,
        deny: typing.Optional[typing.Union["GoogleApigeeSecurityActionDeny", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        expire_time: typing.Optional[builtins.str] = None,
        flag: typing.Optional[typing.Union["GoogleApigeeSecurityActionFlag", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleApigeeSecurityActionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param condition_config: condition_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#condition_config GoogleApigeeSecurityAction#condition_config}
        :param env_id: The Apigee environment that this security action applies to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#env_id GoogleApigeeSecurityAction#env_id}
        :param org_id: The organization that this security action applies to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#org_id GoogleApigeeSecurityAction#org_id}
        :param security_action_id: The ID to use for the SecurityAction, which will become the final component of the action's resource name. This value should be 0-61 characters, and valid format is (^a-z?$). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#security_action_id GoogleApigeeSecurityAction#security_action_id}
        :param state: Only an ENABLED SecurityAction is enforced. An ENABLED SecurityAction past its expiration time will not be enforced. Possible values: ["ENABLED", "DISABLED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#state GoogleApigeeSecurityAction#state}
        :param allow: allow block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#allow GoogleApigeeSecurityAction#allow}
        :param api_proxies: If unset, this would apply to all proxies in the environment. If set, this action is enforced only if at least one proxy in the repeated list is deployed at the time of enforcement. If set, several restrictions are enforced on SecurityActions. There can be at most 100 enabled actions with proxies set in an env. Several other restrictions apply on conditions and are detailed later. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#api_proxies GoogleApigeeSecurityAction#api_proxies}
        :param deny: deny block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#deny GoogleApigeeSecurityAction#deny}
        :param description: An optional user provided description of the SecurityAction. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#description GoogleApigeeSecurityAction#description}
        :param expire_time: The expiration for this SecurityAction. Uses RFC 3339, where generated output will always be Z-normalized and uses 0, 3, 6 or 9 fractional digits. Offsets other than "Z" are also accepted. Examples: "2014-10-02T15:01:23Z", "2014-10-02T15:01:23.045123456Z" or "2014-10-02T15:01:23+05:30". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#expire_time GoogleApigeeSecurityAction#expire_time}
        :param flag: flag block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#flag GoogleApigeeSecurityAction#flag}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#id GoogleApigeeSecurityAction#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#timeouts GoogleApigeeSecurityAction#timeouts}
        :param ttl: The TTL for this SecurityAction. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#ttl GoogleApigeeSecurityAction#ttl}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(condition_config, dict):
            condition_config = GoogleApigeeSecurityActionConditionConfig(**condition_config)
        if isinstance(allow, dict):
            allow = GoogleApigeeSecurityActionAllow(**allow)
        if isinstance(deny, dict):
            deny = GoogleApigeeSecurityActionDeny(**deny)
        if isinstance(flag, dict):
            flag = GoogleApigeeSecurityActionFlag(**flag)
        if isinstance(timeouts, dict):
            timeouts = GoogleApigeeSecurityActionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c7badf34c692000a7a346850cd56663e2e05d9873c1d0039441b86d72538d1b)
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
    def condition_config(self) -> GoogleApigeeSecurityActionConditionConfig:
        '''condition_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#condition_config GoogleApigeeSecurityAction#condition_config}
        '''
        result = self._values.get("condition_config")
        assert result is not None, "Required property 'condition_config' is missing"
        return typing.cast(GoogleApigeeSecurityActionConditionConfig, result)

    @builtins.property
    def env_id(self) -> builtins.str:
        '''The Apigee environment that this security action applies to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#env_id GoogleApigeeSecurityAction#env_id}
        '''
        result = self._values.get("env_id")
        assert result is not None, "Required property 'env_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def org_id(self) -> builtins.str:
        '''The organization that this security action applies to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#org_id GoogleApigeeSecurityAction#org_id}
        '''
        result = self._values.get("org_id")
        assert result is not None, "Required property 'org_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def security_action_id(self) -> builtins.str:
        '''The ID to use for the SecurityAction, which will become the final component of the action's resource name.

        This value should be 0-61 characters, and valid format is (^a-z?$).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#security_action_id GoogleApigeeSecurityAction#security_action_id}
        '''
        result = self._values.get("security_action_id")
        assert result is not None, "Required property 'security_action_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def state(self) -> builtins.str:
        '''Only an ENABLED SecurityAction is enforced.

        An ENABLED SecurityAction past its expiration time will not be enforced. Possible values: ["ENABLED", "DISABLED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#state GoogleApigeeSecurityAction#state}
        '''
        result = self._values.get("state")
        assert result is not None, "Required property 'state' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow(self) -> typing.Optional[GoogleApigeeSecurityActionAllow]:
        '''allow block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#allow GoogleApigeeSecurityAction#allow}
        '''
        result = self._values.get("allow")
        return typing.cast(typing.Optional[GoogleApigeeSecurityActionAllow], result)

    @builtins.property
    def api_proxies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''If unset, this would apply to all proxies in the environment.

        If set, this action is enforced only if at least one proxy in the repeated
        list is deployed at the time of enforcement. If set, several restrictions are enforced on SecurityActions.
        There can be at most 100 enabled actions with proxies set in an env.
        Several other restrictions apply on conditions and are detailed later.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#api_proxies GoogleApigeeSecurityAction#api_proxies}
        '''
        result = self._values.get("api_proxies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def deny(self) -> typing.Optional["GoogleApigeeSecurityActionDeny"]:
        '''deny block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#deny GoogleApigeeSecurityAction#deny}
        '''
        result = self._values.get("deny")
        return typing.cast(typing.Optional["GoogleApigeeSecurityActionDeny"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional user provided description of the SecurityAction.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#description GoogleApigeeSecurityAction#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expire_time(self) -> typing.Optional[builtins.str]:
        '''The expiration for this SecurityAction.

        Uses RFC 3339, where generated output will always be Z-normalized and uses 0, 3, 6 or 9
        fractional digits. Offsets other than "Z" are also accepted.
        Examples: "2014-10-02T15:01:23Z", "2014-10-02T15:01:23.045123456Z" or "2014-10-02T15:01:23+05:30".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#expire_time GoogleApigeeSecurityAction#expire_time}
        '''
        result = self._values.get("expire_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def flag(self) -> typing.Optional["GoogleApigeeSecurityActionFlag"]:
        '''flag block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#flag GoogleApigeeSecurityAction#flag}
        '''
        result = self._values.get("flag")
        return typing.cast(typing.Optional["GoogleApigeeSecurityActionFlag"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#id GoogleApigeeSecurityAction#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleApigeeSecurityActionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#timeouts GoogleApigeeSecurityAction#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleApigeeSecurityActionTimeouts"], result)

    @builtins.property
    def ttl(self) -> typing.Optional[builtins.str]:
        '''The TTL for this SecurityAction. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#ttl GoogleApigeeSecurityAction#ttl}
        '''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeSecurityActionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeSecurityAction.GoogleApigeeSecurityActionDeny",
    jsii_struct_bases=[],
    name_mapping={"response_code": "responseCode"},
)
class GoogleApigeeSecurityActionDeny:
    def __init__(self, *, response_code: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param response_code: The HTTP response code if the Action = DENY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#response_code GoogleApigeeSecurityAction#response_code}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1631cca3f88d1cb0e0b5fb7abc8d5956ac83398bd2babd7a117e1419e26665f)
            check_type(argname="argument response_code", value=response_code, expected_type=type_hints["response_code"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if response_code is not None:
            self._values["response_code"] = response_code

    @builtins.property
    def response_code(self) -> typing.Optional[jsii.Number]:
        '''The HTTP response code if the Action = DENY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#response_code GoogleApigeeSecurityAction#response_code}
        '''
        result = self._values.get("response_code")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeSecurityActionDeny(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApigeeSecurityActionDenyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeSecurityAction.GoogleApigeeSecurityActionDenyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f872e88d80c48653b63a631d3661d787d27996979621de182aed8b03f338ec74)
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
            type_hints = typing.get_type_hints(_typecheckingstub__74fc0f587b0737aeb44bb86a3a21bec7639e7c770e19a7a165a128d8d3ed2503)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleApigeeSecurityActionDeny]:
        return typing.cast(typing.Optional[GoogleApigeeSecurityActionDeny], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApigeeSecurityActionDeny],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa7c1c54758606aeda36489f3fb3c2c4b2d1e98f4788e922cead9888993a0813)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeSecurityAction.GoogleApigeeSecurityActionFlag",
    jsii_struct_bases=[],
    name_mapping={"headers": "headers"},
)
class GoogleApigeeSecurityActionFlag:
    def __init__(
        self,
        *,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApigeeSecurityActionFlagHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param headers: headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#headers GoogleApigeeSecurityAction#headers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0055f69b251b8bc38550b68953885f42ec8ae5c4085e7df69a2e266fa1ab2f1b)
            check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if headers is not None:
            self._values["headers"] = headers

    @builtins.property
    def headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApigeeSecurityActionFlagHeaders"]]]:
        '''headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#headers GoogleApigeeSecurityAction#headers}
        '''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApigeeSecurityActionFlagHeaders"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeSecurityActionFlag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeSecurityAction.GoogleApigeeSecurityActionFlagHeaders",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class GoogleApigeeSecurityActionFlagHeaders:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The header name to be sent to the target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#name GoogleApigeeSecurityAction#name}
        :param value: The header value to be sent to the target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#value GoogleApigeeSecurityAction#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d92e15ae4650088f8d622dc0b1323d3c567f6e5f61357c15cce3de442ddef6e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#name GoogleApigeeSecurityAction#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The header value to be sent to the target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#value GoogleApigeeSecurityAction#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeSecurityActionFlagHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApigeeSecurityActionFlagHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeSecurityAction.GoogleApigeeSecurityActionFlagHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c3d177bae6cc802cda9dd0e527bf36e5bd255b614e2ebd03d8422fbfbcc5cfc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleApigeeSecurityActionFlagHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f382b4b27e3c36b94b7029a9504b7ba01ba0a9d89f1e1d32f788db3d116565df)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleApigeeSecurityActionFlagHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__041f5999a6006758ce5027040a9682f0a9d9e6b3eb27cb7c5e6a66c17e090f8d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4da281b3fc315a98cc091c25dfa326db121c5e47c9ff75d70104ab6944a6738e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__14f50ec6cc76c1f8bd8b723a183b27fcd240e5ae840aa146d865f0f1372ec4b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeSecurityActionFlagHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeSecurityActionFlagHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeSecurityActionFlagHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30b543af8035dfed196dd518f5c3ab532b46ba6df1e0f0fdbbb8776503db3607)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApigeeSecurityActionFlagHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeSecurityAction.GoogleApigeeSecurityActionFlagHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__30ea13d39278495a085f718d95fa11a9b7d10881234cf459ebf81238c2beecbe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__879d65656719b38a0a3fda0bc60209cbf4142a54ff0ad51fbbdf0c4eb20040dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b57000b5359b945747b63824ee66a832598cd369cd17e8ae1fc114a2d70f26d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeSecurityActionFlagHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeSecurityActionFlagHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeSecurityActionFlagHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1e90dd212a4b191dfe5f6ce916fb8bbfec8762cb55d93799e2a4d5b9aecbd74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApigeeSecurityActionFlagOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeSecurityAction.GoogleApigeeSecurityActionFlagOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e8e78d4d0c7ac6ec5c4714459b542eb17a380a90f4de5f2bccfa3b782424a55)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHeaders")
    def put_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeSecurityActionFlagHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12c5ab5dca9cf3ceb877c3c253c6b42d7046fb2d9c27895d213251a4d7be4850)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeaders", [value]))

    @jsii.member(jsii_name="resetHeaders")
    def reset_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaders", []))

    @builtins.property
    @jsii.member(jsii_name="headers")
    def headers(self) -> GoogleApigeeSecurityActionFlagHeadersList:
        return typing.cast(GoogleApigeeSecurityActionFlagHeadersList, jsii.get(self, "headers"))

    @builtins.property
    @jsii.member(jsii_name="headersInput")
    def headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeSecurityActionFlagHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeSecurityActionFlagHeaders]]], jsii.get(self, "headersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleApigeeSecurityActionFlag]:
        return typing.cast(typing.Optional[GoogleApigeeSecurityActionFlag], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApigeeSecurityActionFlag],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b0bd91f724d8b5cae8689d664eb95f07619afec3f9811bd209113f375ffdfc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeSecurityAction.GoogleApigeeSecurityActionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class GoogleApigeeSecurityActionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#create GoogleApigeeSecurityAction#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#delete GoogleApigeeSecurityAction#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ae3ff2fc04fd4b679de14917af547c7d76a84c4a57adf062e474969dd0a6486)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#create GoogleApigeeSecurityAction#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_apigee_security_action#delete GoogleApigeeSecurityAction#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeSecurityActionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApigeeSecurityActionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeSecurityAction.GoogleApigeeSecurityActionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6804c212dc6d6d5569c6831dcd7968c216df2cb767bd93751e73278a6f286aac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b252a4bc882bb1d8ba0674349c76eede3ee90ca86cce2248bffc5555161cbf31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7985bcd0a8e2324e6ce8b5bb1d7a787b112099cbb5c2748d8ea4f36403dff5f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeSecurityActionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeSecurityActionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeSecurityActionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__490dd237c21266ab5f162765d417c7790820019a11087212a8e1179fc437a590)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleApigeeSecurityAction",
    "GoogleApigeeSecurityActionAllow",
    "GoogleApigeeSecurityActionAllowOutputReference",
    "GoogleApigeeSecurityActionConditionConfig",
    "GoogleApigeeSecurityActionConditionConfigOutputReference",
    "GoogleApigeeSecurityActionConfig",
    "GoogleApigeeSecurityActionDeny",
    "GoogleApigeeSecurityActionDenyOutputReference",
    "GoogleApigeeSecurityActionFlag",
    "GoogleApigeeSecurityActionFlagHeaders",
    "GoogleApigeeSecurityActionFlagHeadersList",
    "GoogleApigeeSecurityActionFlagHeadersOutputReference",
    "GoogleApigeeSecurityActionFlagOutputReference",
    "GoogleApigeeSecurityActionTimeouts",
    "GoogleApigeeSecurityActionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__fe60952e6ea68fd0c068bf066c65885d824f406e0b9935ef396cedc4819fa32e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    condition_config: typing.Union[GoogleApigeeSecurityActionConditionConfig, typing.Dict[builtins.str, typing.Any]],
    env_id: builtins.str,
    org_id: builtins.str,
    security_action_id: builtins.str,
    state: builtins.str,
    allow: typing.Optional[typing.Union[GoogleApigeeSecurityActionAllow, typing.Dict[builtins.str, typing.Any]]] = None,
    api_proxies: typing.Optional[typing.Sequence[builtins.str]] = None,
    deny: typing.Optional[typing.Union[GoogleApigeeSecurityActionDeny, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    expire_time: typing.Optional[builtins.str] = None,
    flag: typing.Optional[typing.Union[GoogleApigeeSecurityActionFlag, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleApigeeSecurityActionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__852320f414122553dc9a2776680d4583b110387a7be4050dd6b049d10bceb297(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff399e57d58388fc0876e3c34985abd3707ed8a91c1d6ab387e70fc8503febe1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0240b13805c31e889a6b136328bd2648863e9afae64b974d258e263c139b303c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3ff8fcb294d114d11e1629816e3f3de3516e61264cc6558378099ecde42b115(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31ff7c9c308cbe9484fcea30244357c7eee4a90cee50369dfb19ae3c96bf0ef4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c596d7b696b251bd8b2f1c22006f9c105d2a4eddefd2550ccf4b65bd7e89468(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1d708a92e0be85a54dd0ebf0a73805de7975c037d1ff2988dcd009ceba90406(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e128238f3baf3c00f762a47bd1eb97be10092e01a45daaf5dca9777e01ccbb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4285b9864596520fe090a7ffbcf7ce514e37d2c60a05e3f143689cfa33c55e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__158c149ef98cac34ea5431e35294402a58fd7500c31e88a6237d5db78e078633(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16c3b58a9a43fdf162cf9545aca83c2cfe183a4b4cc0dfff76ac5cb5561eb367(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c898f641ddfc5a3db90e79eb032fd168b6638b186b9387206ce5d9e182c1ec2c(
    value: typing.Optional[GoogleApigeeSecurityActionAllow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__105f5626ce17284b4bd26af1005de395b7c4ecc6560c4a3e72f485c9ca02a896(
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

def _typecheckingstub__983543985fcbcb892ea117ee31460e7eaddb485b951f5c8104cf81bfe54e7721(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10550c73646d4784a6ff91bd09d063682ebcbfb7b452c0167f8e1ad235a6174a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__714e87921fe6fae6cda6cbb63167bc1dafc7f2214b6bbd0d78428029f489949f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93528a581733958602359e4f147b74192365832aac39894bc0bc2186787e8e4d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8efcb2c5e6c768572a24cb1a3f4970756b68a5eeb3d786fd087bd0bd7086be5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e94156f283693f07c97f57a95ce6513b7bc0d28d91af4eee324619b346f78b8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84f90480cb6bf7bfa3e06fcf3d30b4481b65a7baed3b35b6f25f7b5d6bcae4fd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afea04a035e479414390172378ccea8c36eb926749c575d44b58d614499ffce1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75ad3da8ab036b78fecf16bd50b0fa020e1282414397bc320bf55bf7175e6854(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81899fa0f02df030f5256c9009fbcb0cdbcae5c86a86ba25716e0c5ae42419c4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d29b2062cf77406421879158a28ec04f61151aac8590190de00fb20f3783e304(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11fc98a90104e18cc8c27f3e8d8b77d73fa3388f0a3f9989e0d572466fa69c76(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__595b3e465acf7e887ae10ac4abd329623bfdb545789c377900d2ef523147c9d7(
    value: typing.Optional[GoogleApigeeSecurityActionConditionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c7badf34c692000a7a346850cd56663e2e05d9873c1d0039441b86d72538d1b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    condition_config: typing.Union[GoogleApigeeSecurityActionConditionConfig, typing.Dict[builtins.str, typing.Any]],
    env_id: builtins.str,
    org_id: builtins.str,
    security_action_id: builtins.str,
    state: builtins.str,
    allow: typing.Optional[typing.Union[GoogleApigeeSecurityActionAllow, typing.Dict[builtins.str, typing.Any]]] = None,
    api_proxies: typing.Optional[typing.Sequence[builtins.str]] = None,
    deny: typing.Optional[typing.Union[GoogleApigeeSecurityActionDeny, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    expire_time: typing.Optional[builtins.str] = None,
    flag: typing.Optional[typing.Union[GoogleApigeeSecurityActionFlag, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleApigeeSecurityActionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    ttl: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1631cca3f88d1cb0e0b5fb7abc8d5956ac83398bd2babd7a117e1419e26665f(
    *,
    response_code: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f872e88d80c48653b63a631d3661d787d27996979621de182aed8b03f338ec74(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74fc0f587b0737aeb44bb86a3a21bec7639e7c770e19a7a165a128d8d3ed2503(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa7c1c54758606aeda36489f3fb3c2c4b2d1e98f4788e922cead9888993a0813(
    value: typing.Optional[GoogleApigeeSecurityActionDeny],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0055f69b251b8bc38550b68953885f42ec8ae5c4085e7df69a2e266fa1ab2f1b(
    *,
    headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeSecurityActionFlagHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d92e15ae4650088f8d622dc0b1323d3c567f6e5f61357c15cce3de442ddef6e(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c3d177bae6cc802cda9dd0e527bf36e5bd255b614e2ebd03d8422fbfbcc5cfc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f382b4b27e3c36b94b7029a9504b7ba01ba0a9d89f1e1d32f788db3d116565df(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__041f5999a6006758ce5027040a9682f0a9d9e6b3eb27cb7c5e6a66c17e090f8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4da281b3fc315a98cc091c25dfa326db121c5e47c9ff75d70104ab6944a6738e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14f50ec6cc76c1f8bd8b723a183b27fcd240e5ae840aa146d865f0f1372ec4b4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30b543af8035dfed196dd518f5c3ab532b46ba6df1e0f0fdbbb8776503db3607(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeSecurityActionFlagHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30ea13d39278495a085f718d95fa11a9b7d10881234cf459ebf81238c2beecbe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__879d65656719b38a0a3fda0bc60209cbf4142a54ff0ad51fbbdf0c4eb20040dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b57000b5359b945747b63824ee66a832598cd369cd17e8ae1fc114a2d70f26d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1e90dd212a4b191dfe5f6ce916fb8bbfec8762cb55d93799e2a4d5b9aecbd74(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeSecurityActionFlagHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e8e78d4d0c7ac6ec5c4714459b542eb17a380a90f4de5f2bccfa3b782424a55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12c5ab5dca9cf3ceb877c3c253c6b42d7046fb2d9c27895d213251a4d7be4850(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeSecurityActionFlagHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b0bd91f724d8b5cae8689d664eb95f07619afec3f9811bd209113f375ffdfc6(
    value: typing.Optional[GoogleApigeeSecurityActionFlag],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ae3ff2fc04fd4b679de14917af547c7d76a84c4a57adf062e474969dd0a6486(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6804c212dc6d6d5569c6831dcd7968c216df2cb767bd93751e73278a6f286aac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b252a4bc882bb1d8ba0674349c76eede3ee90ca86cce2248bffc5555161cbf31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7985bcd0a8e2324e6ce8b5bb1d7a787b112099cbb5c2748d8ea4f36403dff5f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__490dd237c21266ab5f162765d417c7790820019a11087212a8e1179fc437a590(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeSecurityActionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
