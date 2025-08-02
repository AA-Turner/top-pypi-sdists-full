r'''
# `opentelekomcloud_lb_policy_v3`

Refer to the Terraform Registry for docs: [`opentelekomcloud_lb_policy_v3`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3).
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


class LbPolicyV3(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.lbPolicyV3.LbPolicyV3",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3 opentelekomcloud_lb_policy_v3}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        action: builtins.str,
        listener_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        fixed_response_config: typing.Optional[typing.Union["LbPolicyV3FixedResponseConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        position: typing.Optional[jsii.Number] = None,
        priority: typing.Optional[jsii.Number] = None,
        project_id: typing.Optional[builtins.str] = None,
        redirect_listener_id: typing.Optional[builtins.str] = None,
        redirect_pool_id: typing.Optional[builtins.str] = None,
        redirect_pools_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LbPolicyV3RedirectPoolsConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        redirect_url: typing.Optional[builtins.str] = None,
        redirect_url_config: typing.Optional[typing.Union["LbPolicyV3RedirectUrlConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LbPolicyV3Rules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3 opentelekomcloud_lb_policy_v3} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#action LbPolicyV3#action}.
        :param listener_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#listener_id LbPolicyV3#listener_id}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#description LbPolicyV3#description}.
        :param fixed_response_config: fixed_response_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#fixed_response_config LbPolicyV3#fixed_response_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#id LbPolicyV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#name LbPolicyV3#name}.
        :param position: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#position LbPolicyV3#position}.
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#priority LbPolicyV3#priority}.
        :param project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#project_id LbPolicyV3#project_id}.
        :param redirect_listener_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#redirect_listener_id LbPolicyV3#redirect_listener_id}.
        :param redirect_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#redirect_pool_id LbPolicyV3#redirect_pool_id}.
        :param redirect_pools_config: redirect_pools_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#redirect_pools_config LbPolicyV3#redirect_pools_config}
        :param redirect_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#redirect_url LbPolicyV3#redirect_url}.
        :param redirect_url_config: redirect_url_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#redirect_url_config LbPolicyV3#redirect_url_config}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#rules LbPolicyV3#rules}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c8a9260b90fb20208dd659368b33b4c0f0b8e2f6225a26d091b7816d143b507)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LbPolicyV3Config(
            action=action,
            listener_id=listener_id,
            description=description,
            fixed_response_config=fixed_response_config,
            id=id,
            name=name,
            position=position,
            priority=priority,
            project_id=project_id,
            redirect_listener_id=redirect_listener_id,
            redirect_pool_id=redirect_pool_id,
            redirect_pools_config=redirect_pools_config,
            redirect_url=redirect_url,
            redirect_url_config=redirect_url_config,
            rules=rules,
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
        '''Generates CDKTF code for importing a LbPolicyV3 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the LbPolicyV3 to import.
        :param import_from_id: The id of the existing LbPolicyV3 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the LbPolicyV3 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52ae74f742082f3befa76046b1efd0e9691a5ed9c3659f55e9521f4a5d8701eb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putFixedResponseConfig")
    def put_fixed_response_config(
        self,
        *,
        status_code: builtins.str,
        content_type: typing.Optional[builtins.str] = None,
        message_body: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param status_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#status_code LbPolicyV3#status_code}.
        :param content_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#content_type LbPolicyV3#content_type}.
        :param message_body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#message_body LbPolicyV3#message_body}.
        '''
        value = LbPolicyV3FixedResponseConfig(
            status_code=status_code,
            content_type=content_type,
            message_body=message_body,
        )

        return typing.cast(None, jsii.invoke(self, "putFixedResponseConfig", [value]))

    @jsii.member(jsii_name="putRedirectPoolsConfig")
    def put_redirect_pools_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LbPolicyV3RedirectPoolsConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bdb9a9b285064b3eb80305ef074442b4f175cafeaf507689afc68dd007bab17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRedirectPoolsConfig", [value]))

    @jsii.member(jsii_name="putRedirectUrlConfig")
    def put_redirect_url_config(
        self,
        *,
        status_code: builtins.str,
        host: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        query: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param status_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#status_code LbPolicyV3#status_code}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#host LbPolicyV3#host}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#path LbPolicyV3#path}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#port LbPolicyV3#port}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#protocol LbPolicyV3#protocol}.
        :param query: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#query LbPolicyV3#query}.
        '''
        value = LbPolicyV3RedirectUrlConfig(
            status_code=status_code,
            host=host,
            path=path,
            port=port,
            protocol=protocol,
            query=query,
        )

        return typing.cast(None, jsii.invoke(self, "putRedirectUrlConfig", [value]))

    @jsii.member(jsii_name="putRules")
    def put_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LbPolicyV3Rules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a8ff68649bba6c49f180ac9602f56b1917b8d899595f7d13af4e22e4d385071)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRules", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetFixedResponseConfig")
    def reset_fixed_response_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFixedResponseConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPosition")
    def reset_position(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPosition", []))

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

    @jsii.member(jsii_name="resetRedirectListenerId")
    def reset_redirect_listener_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectListenerId", []))

    @jsii.member(jsii_name="resetRedirectPoolId")
    def reset_redirect_pool_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectPoolId", []))

    @jsii.member(jsii_name="resetRedirectPoolsConfig")
    def reset_redirect_pools_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectPoolsConfig", []))

    @jsii.member(jsii_name="resetRedirectUrl")
    def reset_redirect_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectUrl", []))

    @jsii.member(jsii_name="resetRedirectUrlConfig")
    def reset_redirect_url_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectUrlConfig", []))

    @jsii.member(jsii_name="resetRules")
    def reset_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRules", []))

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
    @jsii.member(jsii_name="fixedResponseConfig")
    def fixed_response_config(self) -> "LbPolicyV3FixedResponseConfigOutputReference":
        return typing.cast("LbPolicyV3FixedResponseConfigOutputReference", jsii.get(self, "fixedResponseConfig"))

    @builtins.property
    @jsii.member(jsii_name="redirectPoolsConfig")
    def redirect_pools_config(self) -> "LbPolicyV3RedirectPoolsConfigList":
        return typing.cast("LbPolicyV3RedirectPoolsConfigList", jsii.get(self, "redirectPoolsConfig"))

    @builtins.property
    @jsii.member(jsii_name="redirectUrlConfig")
    def redirect_url_config(self) -> "LbPolicyV3RedirectUrlConfigOutputReference":
        return typing.cast("LbPolicyV3RedirectUrlConfigOutputReference", jsii.get(self, "redirectUrlConfig"))

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> "LbPolicyV3RulesList":
        return typing.cast("LbPolicyV3RulesList", jsii.get(self, "rules"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="fixedResponseConfigInput")
    def fixed_response_config_input(
        self,
    ) -> typing.Optional["LbPolicyV3FixedResponseConfig"]:
        return typing.cast(typing.Optional["LbPolicyV3FixedResponseConfig"], jsii.get(self, "fixedResponseConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="listenerIdInput")
    def listener_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "listenerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="positionInput")
    def position_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "positionInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectListenerIdInput")
    def redirect_listener_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectListenerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectPoolIdInput")
    def redirect_pool_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectPoolIdInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectPoolsConfigInput")
    def redirect_pools_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LbPolicyV3RedirectPoolsConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LbPolicyV3RedirectPoolsConfig"]]], jsii.get(self, "redirectPoolsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectUrlConfigInput")
    def redirect_url_config_input(
        self,
    ) -> typing.Optional["LbPolicyV3RedirectUrlConfig"]:
        return typing.cast(typing.Optional["LbPolicyV3RedirectUrlConfig"], jsii.get(self, "redirectUrlConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectUrlInput")
    def redirect_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="rulesInput")
    def rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LbPolicyV3Rules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LbPolicyV3Rules"]]], jsii.get(self, "rulesInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5ab6b603b32eb6cc062a59c467c17151a30352389ed3e279b43759953a5d035)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d310015c0cb20d3191374217d01be2cb7d04a1649ae8fed59a76ee4306dcca64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85c1ccc1debcd03d6fa6b27bc699f50fe1ef4ed89ba16e9344ee9fff5b52b266)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="listenerId")
    def listener_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "listenerId"))

    @listener_id.setter
    def listener_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35ae3f9d0af07d4dd58a26f172c46e3ed4ad11b13a8843edcb197e626d6a20c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "listenerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__972f5d52d10cb224cadeeef27cd7a058699889a9b9ca8090d9d04e44ef837c8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="position")
    def position(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "position"))

    @position.setter
    def position(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8e0b1353b9f7a76a197b7b07e979947eb01bfe3ebdc3dd9c2b359c53c0ec2f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "position", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__799f0e49c0655cd9e6eaf098825e79f8677cfae59af967dff54fc9b3ee7d205a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9946f7539291363c6be57c4712686c46273f8ce8209b32c622415de3c7c0e3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectListenerId")
    def redirect_listener_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectListenerId"))

    @redirect_listener_id.setter
    def redirect_listener_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d0b01d35b085c79783d88bba427d7eb9e4655927cc2cad048b88fbb1c57dec7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectListenerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectPoolId")
    def redirect_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectPoolId"))

    @redirect_pool_id.setter
    def redirect_pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b898423c99cf90984287f78465d270ea7c4568ca7fee4ad452e36de25ba0980)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectPoolId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectUrl")
    def redirect_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectUrl"))

    @redirect_url.setter
    def redirect_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94a56fb69dba1d04d4bc5477cd86f7b141fc1f565b4877e38a2a26b2c3975c8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectUrl", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.lbPolicyV3.LbPolicyV3Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "action": "action",
        "listener_id": "listenerId",
        "description": "description",
        "fixed_response_config": "fixedResponseConfig",
        "id": "id",
        "name": "name",
        "position": "position",
        "priority": "priority",
        "project_id": "projectId",
        "redirect_listener_id": "redirectListenerId",
        "redirect_pool_id": "redirectPoolId",
        "redirect_pools_config": "redirectPoolsConfig",
        "redirect_url": "redirectUrl",
        "redirect_url_config": "redirectUrlConfig",
        "rules": "rules",
    },
)
class LbPolicyV3Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        action: builtins.str,
        listener_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        fixed_response_config: typing.Optional[typing.Union["LbPolicyV3FixedResponseConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        position: typing.Optional[jsii.Number] = None,
        priority: typing.Optional[jsii.Number] = None,
        project_id: typing.Optional[builtins.str] = None,
        redirect_listener_id: typing.Optional[builtins.str] = None,
        redirect_pool_id: typing.Optional[builtins.str] = None,
        redirect_pools_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LbPolicyV3RedirectPoolsConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        redirect_url: typing.Optional[builtins.str] = None,
        redirect_url_config: typing.Optional[typing.Union["LbPolicyV3RedirectUrlConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LbPolicyV3Rules", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#action LbPolicyV3#action}.
        :param listener_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#listener_id LbPolicyV3#listener_id}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#description LbPolicyV3#description}.
        :param fixed_response_config: fixed_response_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#fixed_response_config LbPolicyV3#fixed_response_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#id LbPolicyV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#name LbPolicyV3#name}.
        :param position: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#position LbPolicyV3#position}.
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#priority LbPolicyV3#priority}.
        :param project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#project_id LbPolicyV3#project_id}.
        :param redirect_listener_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#redirect_listener_id LbPolicyV3#redirect_listener_id}.
        :param redirect_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#redirect_pool_id LbPolicyV3#redirect_pool_id}.
        :param redirect_pools_config: redirect_pools_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#redirect_pools_config LbPolicyV3#redirect_pools_config}
        :param redirect_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#redirect_url LbPolicyV3#redirect_url}.
        :param redirect_url_config: redirect_url_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#redirect_url_config LbPolicyV3#redirect_url_config}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#rules LbPolicyV3#rules}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(fixed_response_config, dict):
            fixed_response_config = LbPolicyV3FixedResponseConfig(**fixed_response_config)
        if isinstance(redirect_url_config, dict):
            redirect_url_config = LbPolicyV3RedirectUrlConfig(**redirect_url_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fe6412a28b8a4025829bcf047b513164862fcd0b4dafb3461d6ea3c6e27eab8)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument listener_id", value=listener_id, expected_type=type_hints["listener_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument fixed_response_config", value=fixed_response_config, expected_type=type_hints["fixed_response_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument position", value=position, expected_type=type_hints["position"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument redirect_listener_id", value=redirect_listener_id, expected_type=type_hints["redirect_listener_id"])
            check_type(argname="argument redirect_pool_id", value=redirect_pool_id, expected_type=type_hints["redirect_pool_id"])
            check_type(argname="argument redirect_pools_config", value=redirect_pools_config, expected_type=type_hints["redirect_pools_config"])
            check_type(argname="argument redirect_url", value=redirect_url, expected_type=type_hints["redirect_url"])
            check_type(argname="argument redirect_url_config", value=redirect_url_config, expected_type=type_hints["redirect_url_config"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "listener_id": listener_id,
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
        if description is not None:
            self._values["description"] = description
        if fixed_response_config is not None:
            self._values["fixed_response_config"] = fixed_response_config
        if id is not None:
            self._values["id"] = id
        if name is not None:
            self._values["name"] = name
        if position is not None:
            self._values["position"] = position
        if priority is not None:
            self._values["priority"] = priority
        if project_id is not None:
            self._values["project_id"] = project_id
        if redirect_listener_id is not None:
            self._values["redirect_listener_id"] = redirect_listener_id
        if redirect_pool_id is not None:
            self._values["redirect_pool_id"] = redirect_pool_id
        if redirect_pools_config is not None:
            self._values["redirect_pools_config"] = redirect_pools_config
        if redirect_url is not None:
            self._values["redirect_url"] = redirect_url
        if redirect_url_config is not None:
            self._values["redirect_url_config"] = redirect_url_config
        if rules is not None:
            self._values["rules"] = rules

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
    def action(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#action LbPolicyV3#action}.'''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def listener_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#listener_id LbPolicyV3#listener_id}.'''
        result = self._values.get("listener_id")
        assert result is not None, "Required property 'listener_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#description LbPolicyV3#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fixed_response_config(self) -> typing.Optional["LbPolicyV3FixedResponseConfig"]:
        '''fixed_response_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#fixed_response_config LbPolicyV3#fixed_response_config}
        '''
        result = self._values.get("fixed_response_config")
        return typing.cast(typing.Optional["LbPolicyV3FixedResponseConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#id LbPolicyV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#name LbPolicyV3#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def position(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#position LbPolicyV3#position}.'''
        result = self._values.get("position")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#priority LbPolicyV3#priority}.'''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#project_id LbPolicyV3#project_id}.'''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_listener_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#redirect_listener_id LbPolicyV3#redirect_listener_id}.'''
        result = self._values.get("redirect_listener_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_pool_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#redirect_pool_id LbPolicyV3#redirect_pool_id}.'''
        result = self._values.get("redirect_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_pools_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LbPolicyV3RedirectPoolsConfig"]]]:
        '''redirect_pools_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#redirect_pools_config LbPolicyV3#redirect_pools_config}
        '''
        result = self._values.get("redirect_pools_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LbPolicyV3RedirectPoolsConfig"]]], result)

    @builtins.property
    def redirect_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#redirect_url LbPolicyV3#redirect_url}.'''
        result = self._values.get("redirect_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_url_config(self) -> typing.Optional["LbPolicyV3RedirectUrlConfig"]:
        '''redirect_url_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#redirect_url_config LbPolicyV3#redirect_url_config}
        '''
        result = self._values.get("redirect_url_config")
        return typing.cast(typing.Optional["LbPolicyV3RedirectUrlConfig"], result)

    @builtins.property
    def rules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LbPolicyV3Rules"]]]:
        '''rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#rules LbPolicyV3#rules}
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LbPolicyV3Rules"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LbPolicyV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.lbPolicyV3.LbPolicyV3FixedResponseConfig",
    jsii_struct_bases=[],
    name_mapping={
        "status_code": "statusCode",
        "content_type": "contentType",
        "message_body": "messageBody",
    },
)
class LbPolicyV3FixedResponseConfig:
    def __init__(
        self,
        *,
        status_code: builtins.str,
        content_type: typing.Optional[builtins.str] = None,
        message_body: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param status_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#status_code LbPolicyV3#status_code}.
        :param content_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#content_type LbPolicyV3#content_type}.
        :param message_body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#message_body LbPolicyV3#message_body}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d64a9c1038e4705d9f4e0d95aa5bd9ebbbcb7d4796b418105f464d4e3afcea42)
            check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
            check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
            check_type(argname="argument message_body", value=message_body, expected_type=type_hints["message_body"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "status_code": status_code,
        }
        if content_type is not None:
            self._values["content_type"] = content_type
        if message_body is not None:
            self._values["message_body"] = message_body

    @builtins.property
    def status_code(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#status_code LbPolicyV3#status_code}.'''
        result = self._values.get("status_code")
        assert result is not None, "Required property 'status_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#content_type LbPolicyV3#content_type}.'''
        result = self._values.get("content_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def message_body(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#message_body LbPolicyV3#message_body}.'''
        result = self._values.get("message_body")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LbPolicyV3FixedResponseConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LbPolicyV3FixedResponseConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.lbPolicyV3.LbPolicyV3FixedResponseConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecab2c3139edd9d481ce1c35b81fb4ba9557b87762acc34bc22d58eafc4c2c05)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetContentType")
    def reset_content_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentType", []))

    @jsii.member(jsii_name="resetMessageBody")
    def reset_message_body(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageBody", []))

    @builtins.property
    @jsii.member(jsii_name="contentTypeInput")
    def content_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="messageBodyInput")
    def message_body_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageBodyInput"))

    @builtins.property
    @jsii.member(jsii_name="statusCodeInput")
    def status_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="contentType")
    def content_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentType"))

    @content_type.setter
    def content_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62271393826da96d4529d5e76c8ba2079de4158866c4494441e30d92b594f2dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="messageBody")
    def message_body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "messageBody"))

    @message_body.setter
    def message_body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d83f6dd0743e46a3dc387ab29c14e16ad7db701b6c0071db82ff2988a997d726)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageBody", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statusCode")
    def status_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statusCode"))

    @status_code.setter
    def status_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__049a8fa0e072eebec16f61cdf3e6f7323328de27b05b49e359a242087777eb05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statusCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LbPolicyV3FixedResponseConfig]:
        return typing.cast(typing.Optional[LbPolicyV3FixedResponseConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LbPolicyV3FixedResponseConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2405e8fd0d6b1710b23b001237e5c88dd3dd0139aa9014d9e29c5758f40d2123)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.lbPolicyV3.LbPolicyV3RedirectPoolsConfig",
    jsii_struct_bases=[],
    name_mapping={"pool_id": "poolId", "weight": "weight"},
)
class LbPolicyV3RedirectPoolsConfig:
    def __init__(self, *, pool_id: builtins.str, weight: jsii.Number) -> None:
        '''
        :param pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#pool_id LbPolicyV3#pool_id}.
        :param weight: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#weight LbPolicyV3#weight}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b660187cccd0fd876f9de8a3a965f185e91bf74f8289edae56d2e015042b799)
            check_type(argname="argument pool_id", value=pool_id, expected_type=type_hints["pool_id"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pool_id": pool_id,
            "weight": weight,
        }

    @builtins.property
    def pool_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#pool_id LbPolicyV3#pool_id}.'''
        result = self._values.get("pool_id")
        assert result is not None, "Required property 'pool_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def weight(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#weight LbPolicyV3#weight}.'''
        result = self._values.get("weight")
        assert result is not None, "Required property 'weight' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LbPolicyV3RedirectPoolsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LbPolicyV3RedirectPoolsConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.lbPolicyV3.LbPolicyV3RedirectPoolsConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__294f2a1ab520213640660b88ef633b95be6c6e770ec8de645d520d5d32f92f2a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "LbPolicyV3RedirectPoolsConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8dfbb0c8025a7dce4a0c9fd8010e014c7de2b826f39be638770c3fc04e5d336)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LbPolicyV3RedirectPoolsConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72ec084c1b5073e349b9149c119f2b015a7380f1c3cc1c346be6b230729ab2cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d90224c954d3efa960adaeff52b41105aa496c82e367b73c27f9c05af386ada0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c8be3ed5a0a895c407284fe6853cda1f44028557168449aa56bd9ece02ea498)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LbPolicyV3RedirectPoolsConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LbPolicyV3RedirectPoolsConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LbPolicyV3RedirectPoolsConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6548161b028acf01039b21b439ddbd9a6edb19c02aef23b63cc89104bbe4cfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LbPolicyV3RedirectPoolsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.lbPolicyV3.LbPolicyV3RedirectPoolsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d56bde18c9c2f328ec95bb765138e8e78ea57d97496fa8fe745b533426f7edc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="poolIdInput")
    def pool_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "poolIdInput"))

    @builtins.property
    @jsii.member(jsii_name="weightInput")
    def weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weightInput"))

    @builtins.property
    @jsii.member(jsii_name="poolId")
    def pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "poolId"))

    @pool_id.setter
    def pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60fef61ac957115a10a235b06edfa2d14a914a024e16514715b361e4b1f85d7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "poolId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @weight.setter
    def weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea0eff9946cc2f2aabf765c69e9696a67259f44dc60bf2ce3285ed69b7ad04de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weight", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LbPolicyV3RedirectPoolsConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LbPolicyV3RedirectPoolsConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LbPolicyV3RedirectPoolsConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b33299b8ec8679508592ecc92c011bb0822cfd5a77cd07e63d9829e81d9ffe30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.lbPolicyV3.LbPolicyV3RedirectUrlConfig",
    jsii_struct_bases=[],
    name_mapping={
        "status_code": "statusCode",
        "host": "host",
        "path": "path",
        "port": "port",
        "protocol": "protocol",
        "query": "query",
    },
)
class LbPolicyV3RedirectUrlConfig:
    def __init__(
        self,
        *,
        status_code: builtins.str,
        host: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        query: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param status_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#status_code LbPolicyV3#status_code}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#host LbPolicyV3#host}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#path LbPolicyV3#path}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#port LbPolicyV3#port}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#protocol LbPolicyV3#protocol}.
        :param query: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#query LbPolicyV3#query}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88b1227f49c4a3297d99b6c9d21772a4bd2030ab636c1a6b7c8cfbc29735e59f)
            check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "status_code": status_code,
        }
        if host is not None:
            self._values["host"] = host
        if path is not None:
            self._values["path"] = path
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if query is not None:
            self._values["query"] = query

    @builtins.property
    def status_code(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#status_code LbPolicyV3#status_code}.'''
        result = self._values.get("status_code")
        assert result is not None, "Required property 'status_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#host LbPolicyV3#host}.'''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#path LbPolicyV3#path}.'''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#port LbPolicyV3#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#protocol LbPolicyV3#protocol}.'''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#query LbPolicyV3#query}.'''
        result = self._values.get("query")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LbPolicyV3RedirectUrlConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LbPolicyV3RedirectUrlConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.lbPolicyV3.LbPolicyV3RedirectUrlConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__404125ba284763372498290605c7c0012be68b11c143831a067935acddcdfbe1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetProtocol")
    def reset_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocol", []))

    @jsii.member(jsii_name="resetQuery")
    def reset_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuery", []))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="statusCodeInput")
    def status_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98da50e3f22efaf8ead594ba018d8a31e4dbf7ad2aa26c62621dd75176045756)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3562ab9e5dd6d9bcf5ef97ff2fdefb4351863c0c5957a8fa40801f5623e94b72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "port"))

    @port.setter
    def port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6d6e7caf9b359550f3bb16dddcb8d28737692309af273cb5a462b0aeb31010a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77a8b6c6ee8632287dfdf40bc29d5b3086b4b2485a78a37c0f4f725475c69293)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d025d0be07cbf1a38b44b54109fa70ab6027b95b565a527474d086b9840ae24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statusCode")
    def status_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statusCode"))

    @status_code.setter
    def status_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81b943a7a2b35591f7dfe3cfd3b84756656d41e9da84457e9cc947e45c3a6a00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statusCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LbPolicyV3RedirectUrlConfig]:
        return typing.cast(typing.Optional[LbPolicyV3RedirectUrlConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LbPolicyV3RedirectUrlConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e922384a1c7fe455454b8331aef02350568863fedafe014c21552785075c4ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.lbPolicyV3.LbPolicyV3Rules",
    jsii_struct_bases=[],
    name_mapping={"compare_type": "compareType", "type": "type", "value": "value"},
)
class LbPolicyV3Rules:
    def __init__(
        self,
        *,
        compare_type: builtins.str,
        type: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param compare_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#compare_type LbPolicyV3#compare_type}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#type LbPolicyV3#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#value LbPolicyV3#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a7dd89d4d33b6357b92371a6d52e69d3f1ead88651847cca1345f18b1dd839d)
            check_type(argname="argument compare_type", value=compare_type, expected_type=type_hints["compare_type"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "compare_type": compare_type,
            "type": type,
            "value": value,
        }

    @builtins.property
    def compare_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#compare_type LbPolicyV3#compare_type}.'''
        result = self._values.get("compare_type")
        assert result is not None, "Required property 'compare_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#type LbPolicyV3#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_policy_v3#value LbPolicyV3#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LbPolicyV3Rules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LbPolicyV3RulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.lbPolicyV3.LbPolicyV3RulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__333c25b3f2a3dfa56546d34f7a226c5c16cb9afb432695679979d96f1184e49d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "LbPolicyV3RulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ceb102389c020e887917248f869a78ef0e0e022c5918be35110b934df793c2ef)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LbPolicyV3RulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da1d6d778aedd5567feffc9661bd60c1be07307a945430b5fe585e1f95ec06fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd38499568bab4b702afa69ee2ccedd02af6759997bbdfdaa50cb53a3a2842a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc394e6607dbfbd8ab196b43a7f122b0c8b5141c442b2bdb534964ea4c7fd61d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LbPolicyV3Rules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LbPolicyV3Rules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LbPolicyV3Rules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7da58dc2787aba4c50bb07ef42f05cc41f444bf83cf28a9f80b31b8829172f9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LbPolicyV3RulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.lbPolicyV3.LbPolicyV3RulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cbeca56556bbd6aaf582b9d1a708f36a610dc6817136f9d71a996967edcfa7f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="compareTypeInput")
    def compare_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "compareTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="compareType")
    def compare_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "compareType"))

    @compare_type.setter
    def compare_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__866567dd50a835ad76bdc91cea0eb5c5c1ecaee40a26fcf983c6937cf83b4bdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compareType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa3b6ba656111eb28c161756d9bfb771dba6316886e0b99002939b6bd4285bc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12969ff17061a66e152f9ee2a74c1095e9f03bc0891058a6dab81e8cdb678dcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LbPolicyV3Rules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LbPolicyV3Rules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LbPolicyV3Rules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__433dbd3b910ba083f49627046de29d55a3e5d3718350d8b8c8a4df2a40f380b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "LbPolicyV3",
    "LbPolicyV3Config",
    "LbPolicyV3FixedResponseConfig",
    "LbPolicyV3FixedResponseConfigOutputReference",
    "LbPolicyV3RedirectPoolsConfig",
    "LbPolicyV3RedirectPoolsConfigList",
    "LbPolicyV3RedirectPoolsConfigOutputReference",
    "LbPolicyV3RedirectUrlConfig",
    "LbPolicyV3RedirectUrlConfigOutputReference",
    "LbPolicyV3Rules",
    "LbPolicyV3RulesList",
    "LbPolicyV3RulesOutputReference",
]

publication.publish()

def _typecheckingstub__3c8a9260b90fb20208dd659368b33b4c0f0b8e2f6225a26d091b7816d143b507(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    action: builtins.str,
    listener_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    fixed_response_config: typing.Optional[typing.Union[LbPolicyV3FixedResponseConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    position: typing.Optional[jsii.Number] = None,
    priority: typing.Optional[jsii.Number] = None,
    project_id: typing.Optional[builtins.str] = None,
    redirect_listener_id: typing.Optional[builtins.str] = None,
    redirect_pool_id: typing.Optional[builtins.str] = None,
    redirect_pools_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LbPolicyV3RedirectPoolsConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    redirect_url: typing.Optional[builtins.str] = None,
    redirect_url_config: typing.Optional[typing.Union[LbPolicyV3RedirectUrlConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LbPolicyV3Rules, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__52ae74f742082f3befa76046b1efd0e9691a5ed9c3659f55e9521f4a5d8701eb(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bdb9a9b285064b3eb80305ef074442b4f175cafeaf507689afc68dd007bab17(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LbPolicyV3RedirectPoolsConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a8ff68649bba6c49f180ac9602f56b1917b8d899595f7d13af4e22e4d385071(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LbPolicyV3Rules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5ab6b603b32eb6cc062a59c467c17151a30352389ed3e279b43759953a5d035(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d310015c0cb20d3191374217d01be2cb7d04a1649ae8fed59a76ee4306dcca64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85c1ccc1debcd03d6fa6b27bc699f50fe1ef4ed89ba16e9344ee9fff5b52b266(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35ae3f9d0af07d4dd58a26f172c46e3ed4ad11b13a8843edcb197e626d6a20c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__972f5d52d10cb224cadeeef27cd7a058699889a9b9ca8090d9d04e44ef837c8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8e0b1353b9f7a76a197b7b07e979947eb01bfe3ebdc3dd9c2b359c53c0ec2f4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__799f0e49c0655cd9e6eaf098825e79f8677cfae59af967dff54fc9b3ee7d205a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9946f7539291363c6be57c4712686c46273f8ce8209b32c622415de3c7c0e3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d0b01d35b085c79783d88bba427d7eb9e4655927cc2cad048b88fbb1c57dec7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b898423c99cf90984287f78465d270ea7c4568ca7fee4ad452e36de25ba0980(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94a56fb69dba1d04d4bc5477cd86f7b141fc1f565b4877e38a2a26b2c3975c8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fe6412a28b8a4025829bcf047b513164862fcd0b4dafb3461d6ea3c6e27eab8(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    action: builtins.str,
    listener_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    fixed_response_config: typing.Optional[typing.Union[LbPolicyV3FixedResponseConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    position: typing.Optional[jsii.Number] = None,
    priority: typing.Optional[jsii.Number] = None,
    project_id: typing.Optional[builtins.str] = None,
    redirect_listener_id: typing.Optional[builtins.str] = None,
    redirect_pool_id: typing.Optional[builtins.str] = None,
    redirect_pools_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LbPolicyV3RedirectPoolsConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    redirect_url: typing.Optional[builtins.str] = None,
    redirect_url_config: typing.Optional[typing.Union[LbPolicyV3RedirectUrlConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LbPolicyV3Rules, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d64a9c1038e4705d9f4e0d95aa5bd9ebbbcb7d4796b418105f464d4e3afcea42(
    *,
    status_code: builtins.str,
    content_type: typing.Optional[builtins.str] = None,
    message_body: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecab2c3139edd9d481ce1c35b81fb4ba9557b87762acc34bc22d58eafc4c2c05(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62271393826da96d4529d5e76c8ba2079de4158866c4494441e30d92b594f2dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d83f6dd0743e46a3dc387ab29c14e16ad7db701b6c0071db82ff2988a997d726(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__049a8fa0e072eebec16f61cdf3e6f7323328de27b05b49e359a242087777eb05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2405e8fd0d6b1710b23b001237e5c88dd3dd0139aa9014d9e29c5758f40d2123(
    value: typing.Optional[LbPolicyV3FixedResponseConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b660187cccd0fd876f9de8a3a965f185e91bf74f8289edae56d2e015042b799(
    *,
    pool_id: builtins.str,
    weight: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__294f2a1ab520213640660b88ef633b95be6c6e770ec8de645d520d5d32f92f2a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8dfbb0c8025a7dce4a0c9fd8010e014c7de2b826f39be638770c3fc04e5d336(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72ec084c1b5073e349b9149c119f2b015a7380f1c3cc1c346be6b230729ab2cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d90224c954d3efa960adaeff52b41105aa496c82e367b73c27f9c05af386ada0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c8be3ed5a0a895c407284fe6853cda1f44028557168449aa56bd9ece02ea498(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6548161b028acf01039b21b439ddbd9a6edb19c02aef23b63cc89104bbe4cfa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LbPolicyV3RedirectPoolsConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d56bde18c9c2f328ec95bb765138e8e78ea57d97496fa8fe745b533426f7edc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60fef61ac957115a10a235b06edfa2d14a914a024e16514715b361e4b1f85d7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea0eff9946cc2f2aabf765c69e9696a67259f44dc60bf2ce3285ed69b7ad04de(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b33299b8ec8679508592ecc92c011bb0822cfd5a77cd07e63d9829e81d9ffe30(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LbPolicyV3RedirectPoolsConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88b1227f49c4a3297d99b6c9d21772a4bd2030ab636c1a6b7c8cfbc29735e59f(
    *,
    status_code: builtins.str,
    host: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    port: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    query: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__404125ba284763372498290605c7c0012be68b11c143831a067935acddcdfbe1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98da50e3f22efaf8ead594ba018d8a31e4dbf7ad2aa26c62621dd75176045756(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3562ab9e5dd6d9bcf5ef97ff2fdefb4351863c0c5957a8fa40801f5623e94b72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6d6e7caf9b359550f3bb16dddcb8d28737692309af273cb5a462b0aeb31010a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77a8b6c6ee8632287dfdf40bc29d5b3086b4b2485a78a37c0f4f725475c69293(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d025d0be07cbf1a38b44b54109fa70ab6027b95b565a527474d086b9840ae24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81b943a7a2b35591f7dfe3cfd3b84756656d41e9da84457e9cc947e45c3a6a00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e922384a1c7fe455454b8331aef02350568863fedafe014c21552785075c4ac(
    value: typing.Optional[LbPolicyV3RedirectUrlConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a7dd89d4d33b6357b92371a6d52e69d3f1ead88651847cca1345f18b1dd839d(
    *,
    compare_type: builtins.str,
    type: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__333c25b3f2a3dfa56546d34f7a226c5c16cb9afb432695679979d96f1184e49d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceb102389c020e887917248f869a78ef0e0e022c5918be35110b934df793c2ef(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da1d6d778aedd5567feffc9661bd60c1be07307a945430b5fe585e1f95ec06fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd38499568bab4b702afa69ee2ccedd02af6759997bbdfdaa50cb53a3a2842a1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc394e6607dbfbd8ab196b43a7f122b0c8b5141c442b2bdb534964ea4c7fd61d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7da58dc2787aba4c50bb07ef42f05cc41f444bf83cf28a9f80b31b8829172f9a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LbPolicyV3Rules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbeca56556bbd6aaf582b9d1a708f36a610dc6817136f9d71a996967edcfa7f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__866567dd50a835ad76bdc91cea0eb5c5c1ecaee40a26fcf983c6937cf83b4bdd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa3b6ba656111eb28c161756d9bfb771dba6316886e0b99002939b6bd4285bc5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12969ff17061a66e152f9ee2a74c1095e9f03bc0891058a6dab81e8cdb678dcd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__433dbd3b910ba083f49627046de29d55a3e5d3718350d8b8c8a4df2a40f380b5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LbPolicyV3Rules]],
) -> None:
    """Type checking stubs"""
    pass
