r'''
# `datadog_action_connection`

Refer to the Terraform Registry for docs: [`datadog_action_connection`](https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection).
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


class ActionConnection(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.actionConnection.ActionConnection",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection datadog_action_connection}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        aws: typing.Optional[typing.Union["ActionConnectionAws", typing.Dict[builtins.str, typing.Any]]] = None,
        http: typing.Optional[typing.Union["ActionConnectionHttp", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection datadog_action_connection} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#name ActionConnection#name}
        :param aws: aws block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#aws ActionConnection#aws}
        :param http: http block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#http ActionConnection#http}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__529edb8862c892350021822a3cb1af453ed1456a2b30d430f82abe40f80328c7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = ActionConnectionConfig(
            name=name,
            aws=aws,
            http=http,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a ActionConnection resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ActionConnection to import.
        :param import_from_id: The id of the existing ActionConnection that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ActionConnection to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06b3755f4c10317ad23600a7d45f8221df1db416e0137e4874741ce050d61d95)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAws")
    def put_aws(
        self,
        *,
        assume_role: typing.Optional[typing.Union["ActionConnectionAwsAssumeRole", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param assume_role: assume_role block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#assume_role ActionConnection#assume_role}
        '''
        value = ActionConnectionAws(assume_role=assume_role)

        return typing.cast(None, jsii.invoke(self, "putAws", [value]))

    @jsii.member(jsii_name="putHttp")
    def put_http(
        self,
        *,
        base_url: typing.Optional[builtins.str] = None,
        token_auth: typing.Optional[typing.Union["ActionConnectionHttpTokenAuth", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param base_url: Base HTTP url for the integration. String length must be at least 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#base_url ActionConnection#base_url}
        :param token_auth: token_auth block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#token_auth ActionConnection#token_auth}
        '''
        value = ActionConnectionHttp(base_url=base_url, token_auth=token_auth)

        return typing.cast(None, jsii.invoke(self, "putHttp", [value]))

    @jsii.member(jsii_name="resetAws")
    def reset_aws(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAws", []))

    @jsii.member(jsii_name="resetHttp")
    def reset_http(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttp", []))

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
    @jsii.member(jsii_name="aws")
    def aws(self) -> "ActionConnectionAwsOutputReference":
        return typing.cast("ActionConnectionAwsOutputReference", jsii.get(self, "aws"))

    @builtins.property
    @jsii.member(jsii_name="http")
    def http(self) -> "ActionConnectionHttpOutputReference":
        return typing.cast("ActionConnectionHttpOutputReference", jsii.get(self, "http"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="awsInput")
    def aws_input(
        self,
    ) -> typing.Optional[typing.Union["ActionConnectionAws", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["ActionConnectionAws", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "awsInput"))

    @builtins.property
    @jsii.member(jsii_name="httpInput")
    def http_input(
        self,
    ) -> typing.Optional[typing.Union["ActionConnectionHttp", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["ActionConnectionHttp", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "httpInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b10eeb2f3c9147091aefb0554a2a1117efe39e367f0b82608c76ddfafc091b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.actionConnection.ActionConnectionAws",
    jsii_struct_bases=[],
    name_mapping={"assume_role": "assumeRole"},
)
class ActionConnectionAws:
    def __init__(
        self,
        *,
        assume_role: typing.Optional[typing.Union["ActionConnectionAwsAssumeRole", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param assume_role: assume_role block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#assume_role ActionConnection#assume_role}
        '''
        if isinstance(assume_role, dict):
            assume_role = ActionConnectionAwsAssumeRole(**assume_role)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f25da154ba2fb59eafbbbf353fb5947a69d863fe3393a4d3e63f4ea9e8acdab5)
            check_type(argname="argument assume_role", value=assume_role, expected_type=type_hints["assume_role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if assume_role is not None:
            self._values["assume_role"] = assume_role

    @builtins.property
    def assume_role(self) -> typing.Optional["ActionConnectionAwsAssumeRole"]:
        '''assume_role block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#assume_role ActionConnection#assume_role}
        '''
        result = self._values.get("assume_role")
        return typing.cast(typing.Optional["ActionConnectionAwsAssumeRole"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionConnectionAws(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.actionConnection.ActionConnectionAwsAssumeRole",
    jsii_struct_bases=[],
    name_mapping={"account_id": "accountId", "role": "role"},
)
class ActionConnectionAwsAssumeRole:
    def __init__(
        self,
        *,
        account_id: typing.Optional[builtins.str] = None,
        role: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account_id: AWS account that the connection is created for. String length must be at least 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#account_id ActionConnection#account_id}
        :param role: Role to assume. String length must be at least 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#role ActionConnection#role}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46762c6ecae4849cdeddffca1d9f39adc1c839417658264821ca7a6cac579a58)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account_id is not None:
            self._values["account_id"] = account_id
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def account_id(self) -> typing.Optional[builtins.str]:
        '''AWS account that the connection is created for. String length must be at least 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#account_id ActionConnection#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[builtins.str]:
        '''Role to assume. String length must be at least 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#role ActionConnection#role}
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionConnectionAwsAssumeRole(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ActionConnectionAwsAssumeRoleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.actionConnection.ActionConnectionAwsAssumeRoleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__39e35f5fd8d04dbfa5ae916ec421decfcec0f5464a3d93dc77363d279f3ff1b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @jsii.member(jsii_name="resetRole")
    def reset_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRole", []))

    @builtins.property
    @jsii.member(jsii_name="externalId")
    def external_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalId"))

    @builtins.property
    @jsii.member(jsii_name="principalId")
    def principal_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principalId"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="roleInput")
    def role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f267de337c5e565014c5560768923b24c85404d6bd9d8ff76a1f87c52a12bed5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @role.setter
    def role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87f5366d282cf980e283671a6bbb00e0fd132891e202d42cffda496335d8a3c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "role", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ActionConnectionAwsAssumeRole, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ActionConnectionAwsAssumeRole, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ActionConnectionAwsAssumeRole, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b63ace98318e1c518159321c3fca45893e41c4aca1a867a7c87ece16f634e5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ActionConnectionAwsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.actionConnection.ActionConnectionAwsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3dd18f049a61e0b2afcb0dd891ce8b32e21acd1e8ceb4398bd581da714dcfdc7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAssumeRole")
    def put_assume_role(
        self,
        *,
        account_id: typing.Optional[builtins.str] = None,
        role: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account_id: AWS account that the connection is created for. String length must be at least 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#account_id ActionConnection#account_id}
        :param role: Role to assume. String length must be at least 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#role ActionConnection#role}
        '''
        value = ActionConnectionAwsAssumeRole(account_id=account_id, role=role)

        return typing.cast(None, jsii.invoke(self, "putAssumeRole", [value]))

    @jsii.member(jsii_name="resetAssumeRole")
    def reset_assume_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssumeRole", []))

    @builtins.property
    @jsii.member(jsii_name="assumeRole")
    def assume_role(self) -> ActionConnectionAwsAssumeRoleOutputReference:
        return typing.cast(ActionConnectionAwsAssumeRoleOutputReference, jsii.get(self, "assumeRole"))

    @builtins.property
    @jsii.member(jsii_name="assumeRoleInput")
    def assume_role_input(
        self,
    ) -> typing.Optional[typing.Union[ActionConnectionAwsAssumeRole, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ActionConnectionAwsAssumeRole, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "assumeRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ActionConnectionAws, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ActionConnectionAws, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ActionConnectionAws, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e11dfde9238bb48c6dcc5bea8903549cdf066293740e57e23581350348910f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.actionConnection.ActionConnectionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "aws": "aws",
        "http": "http",
    },
)
class ActionConnectionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        aws: typing.Optional[typing.Union[ActionConnectionAws, typing.Dict[builtins.str, typing.Any]]] = None,
        http: typing.Optional[typing.Union["ActionConnectionHttp", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#name ActionConnection#name}
        :param aws: aws block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#aws ActionConnection#aws}
        :param http: http block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#http ActionConnection#http}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(aws, dict):
            aws = ActionConnectionAws(**aws)
        if isinstance(http, dict):
            http = ActionConnectionHttp(**http)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63752c5ec5c01ac27d871f4e4a5b9482425473f7f789bc408a21d91d52cd8f8f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument aws", value=aws, expected_type=type_hints["aws"])
            check_type(argname="argument http", value=http, expected_type=type_hints["http"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if aws is not None:
            self._values["aws"] = aws
        if http is not None:
            self._values["http"] = http

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
    def name(self) -> builtins.str:
        '''Name of the connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#name ActionConnection#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aws(self) -> typing.Optional[ActionConnectionAws]:
        '''aws block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#aws ActionConnection#aws}
        '''
        result = self._values.get("aws")
        return typing.cast(typing.Optional[ActionConnectionAws], result)

    @builtins.property
    def http(self) -> typing.Optional["ActionConnectionHttp"]:
        '''http block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#http ActionConnection#http}
        '''
        result = self._values.get("http")
        return typing.cast(typing.Optional["ActionConnectionHttp"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionConnectionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.actionConnection.ActionConnectionHttp",
    jsii_struct_bases=[],
    name_mapping={"base_url": "baseUrl", "token_auth": "tokenAuth"},
)
class ActionConnectionHttp:
    def __init__(
        self,
        *,
        base_url: typing.Optional[builtins.str] = None,
        token_auth: typing.Optional[typing.Union["ActionConnectionHttpTokenAuth", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param base_url: Base HTTP url for the integration. String length must be at least 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#base_url ActionConnection#base_url}
        :param token_auth: token_auth block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#token_auth ActionConnection#token_auth}
        '''
        if isinstance(token_auth, dict):
            token_auth = ActionConnectionHttpTokenAuth(**token_auth)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9f89e62962a63aa44470d224036b9149865a993765db78d3bbb85c41177dc75)
            check_type(argname="argument base_url", value=base_url, expected_type=type_hints["base_url"])
            check_type(argname="argument token_auth", value=token_auth, expected_type=type_hints["token_auth"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if base_url is not None:
            self._values["base_url"] = base_url
        if token_auth is not None:
            self._values["token_auth"] = token_auth

    @builtins.property
    def base_url(self) -> typing.Optional[builtins.str]:
        '''Base HTTP url for the integration. String length must be at least 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#base_url ActionConnection#base_url}
        '''
        result = self._values.get("base_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_auth(self) -> typing.Optional["ActionConnectionHttpTokenAuth"]:
        '''token_auth block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#token_auth ActionConnection#token_auth}
        '''
        result = self._values.get("token_auth")
        return typing.cast(typing.Optional["ActionConnectionHttpTokenAuth"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionConnectionHttp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ActionConnectionHttpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.actionConnection.ActionConnectionHttpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__56d8b79b4f356607b0b8466722ca98ba51a93af443c4b1f2693a002a1c32c733)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTokenAuth")
    def put_token_auth(
        self,
        *,
        body: typing.Optional[typing.Union["ActionConnectionHttpTokenAuthBody", typing.Dict[builtins.str, typing.Any]]] = None,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ActionConnectionHttpTokenAuthHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        token: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ActionConnectionHttpTokenAuthToken", typing.Dict[builtins.str, typing.Any]]]]] = None,
        url_parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ActionConnectionHttpTokenAuthUrlParameter", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param body: body block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#body ActionConnection#body}
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#header ActionConnection#header}
        :param token: token block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#token ActionConnection#token}
        :param url_parameter: url_parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#url_parameter ActionConnection#url_parameter}
        '''
        value = ActionConnectionHttpTokenAuth(
            body=body, header=header, token=token, url_parameter=url_parameter
        )

        return typing.cast(None, jsii.invoke(self, "putTokenAuth", [value]))

    @jsii.member(jsii_name="resetBaseUrl")
    def reset_base_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBaseUrl", []))

    @jsii.member(jsii_name="resetTokenAuth")
    def reset_token_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTokenAuth", []))

    @builtins.property
    @jsii.member(jsii_name="tokenAuth")
    def token_auth(self) -> "ActionConnectionHttpTokenAuthOutputReference":
        return typing.cast("ActionConnectionHttpTokenAuthOutputReference", jsii.get(self, "tokenAuth"))

    @builtins.property
    @jsii.member(jsii_name="baseUrlInput")
    def base_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "baseUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenAuthInput")
    def token_auth_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ActionConnectionHttpTokenAuth"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ActionConnectionHttpTokenAuth"]], jsii.get(self, "tokenAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="baseUrl")
    def base_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "baseUrl"))

    @base_url.setter
    def base_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a66ec497642e0b4a6737615f6cfd1674b3e4606165bdb57e0e4808f7cddba08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ActionConnectionHttp, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ActionConnectionHttp, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ActionConnectionHttp, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a510182737e2090c0350645e31f7f6ed1a048a24895319564dc6fd5164a1b9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.actionConnection.ActionConnectionHttpTokenAuth",
    jsii_struct_bases=[],
    name_mapping={
        "body": "body",
        "header": "header",
        "token": "token",
        "url_parameter": "urlParameter",
    },
)
class ActionConnectionHttpTokenAuth:
    def __init__(
        self,
        *,
        body: typing.Optional[typing.Union["ActionConnectionHttpTokenAuthBody", typing.Dict[builtins.str, typing.Any]]] = None,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ActionConnectionHttpTokenAuthHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        token: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ActionConnectionHttpTokenAuthToken", typing.Dict[builtins.str, typing.Any]]]]] = None,
        url_parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ActionConnectionHttpTokenAuthUrlParameter", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param body: body block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#body ActionConnection#body}
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#header ActionConnection#header}
        :param token: token block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#token ActionConnection#token}
        :param url_parameter: url_parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#url_parameter ActionConnection#url_parameter}
        '''
        if isinstance(body, dict):
            body = ActionConnectionHttpTokenAuthBody(**body)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04d732816dcc1fd92afbd455569f6d6fa9d458c0c445748fb04dd25cb924c833)
            check_type(argname="argument body", value=body, expected_type=type_hints["body"])
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
            check_type(argname="argument url_parameter", value=url_parameter, expected_type=type_hints["url_parameter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if body is not None:
            self._values["body"] = body
        if header is not None:
            self._values["header"] = header
        if token is not None:
            self._values["token"] = token
        if url_parameter is not None:
            self._values["url_parameter"] = url_parameter

    @builtins.property
    def body(self) -> typing.Optional["ActionConnectionHttpTokenAuthBody"]:
        '''body block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#body ActionConnection#body}
        '''
        result = self._values.get("body")
        return typing.cast(typing.Optional["ActionConnectionHttpTokenAuthBody"], result)

    @builtins.property
    def header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ActionConnectionHttpTokenAuthHeader"]]]:
        '''header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#header ActionConnection#header}
        '''
        result = self._values.get("header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ActionConnectionHttpTokenAuthHeader"]]], result)

    @builtins.property
    def token(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ActionConnectionHttpTokenAuthToken"]]]:
        '''token block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#token ActionConnection#token}
        '''
        result = self._values.get("token")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ActionConnectionHttpTokenAuthToken"]]], result)

    @builtins.property
    def url_parameter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ActionConnectionHttpTokenAuthUrlParameter"]]]:
        '''url_parameter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#url_parameter ActionConnection#url_parameter}
        '''
        result = self._values.get("url_parameter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ActionConnectionHttpTokenAuthUrlParameter"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionConnectionHttpTokenAuth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.actionConnection.ActionConnectionHttpTokenAuthBody",
    jsii_struct_bases=[],
    name_mapping={"content": "content", "content_type": "contentType"},
)
class ActionConnectionHttpTokenAuthBody:
    def __init__(
        self,
        *,
        content: typing.Optional[builtins.str] = None,
        content_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param content: Serialized body content. String length must be at least 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#content ActionConnection#content}
        :param content_type: Content type of the body. String length must be at least 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#content_type ActionConnection#content_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86ca630442e327b336aa1bdb3bfd22dd977aa3a34155cff688f556d6c9a1540d)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if content is not None:
            self._values["content"] = content
        if content_type is not None:
            self._values["content_type"] = content_type

    @builtins.property
    def content(self) -> typing.Optional[builtins.str]:
        '''Serialized body content. String length must be at least 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#content ActionConnection#content}
        '''
        result = self._values.get("content")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_type(self) -> typing.Optional[builtins.str]:
        '''Content type of the body. String length must be at least 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#content_type ActionConnection#content_type}
        '''
        result = self._values.get("content_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionConnectionHttpTokenAuthBody(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ActionConnectionHttpTokenAuthBodyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.actionConnection.ActionConnectionHttpTokenAuthBodyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b6e700c624d605df01b6f9ca0e6599d5d078a8835e407723881a0f32a884782)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetContent")
    def reset_content(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContent", []))

    @jsii.member(jsii_name="resetContentType")
    def reset_content_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentType", []))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="contentTypeInput")
    def content_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48e99f8f9cf3ddb2357d0d3b58166d2465e74eafd803fc24a0d355b4d77b82b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentType")
    def content_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentType"))

    @content_type.setter
    def content_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97fb071e5475e47dd90b0feada67b87e3602702fc651b3041e0dbb961b3f8339)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ActionConnectionHttpTokenAuthBody]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ActionConnectionHttpTokenAuthBody]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ActionConnectionHttpTokenAuthBody]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c80cd7b1e3a6109bb1512f997ccc1b99d726884948f907f41d3086abdb1267b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.actionConnection.ActionConnectionHttpTokenAuthHeader",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class ActionConnectionHttpTokenAuthHeader:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Header name. String length must be at least 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#name ActionConnection#name}
        :param value: String length must be at least 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#value ActionConnection#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34cb02e5fc2a376610267fbcf33fcf2cb55ecf37fa0aa48430e68a577161a995)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Header name. String length must be at least 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#name ActionConnection#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''String length must be at least 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#value ActionConnection#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionConnectionHttpTokenAuthHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ActionConnectionHttpTokenAuthHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.actionConnection.ActionConnectionHttpTokenAuthHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c912fcc03875ec45695ccaf4476423dc2a865aa7c70092dee28b5effb6e6134b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ActionConnectionHttpTokenAuthHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b8a22f2c59c9da1ece3f0b4c45932713c31f552edaa31c9b0277a4be5f8a702)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ActionConnectionHttpTokenAuthHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1e9d132d061338ace3f3afa2f9e654800448023f7508b33e908a08e449d4a89)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3505c908fc7111ec79bd39214dc2f16143a799846574e87a219a3287b03ba16b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__32aba910475c1e71839ab45cb65b1920f0475bf60c16739cdcdd147499394f89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ActionConnectionHttpTokenAuthHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ActionConnectionHttpTokenAuthHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ActionConnectionHttpTokenAuthHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e474ce69012d90c8a741588fd64fa6b10686856285fd2b67934656fadc3b3d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ActionConnectionHttpTokenAuthHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.actionConnection.ActionConnectionHttpTokenAuthHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8adc6a22ee9bd3b741078e1f1af164e6c270f5077fd739f8e5dd79d0c085dabc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9514f9df418cc4e3d2f7721315f0fdd2814555e5a032aad71620e5d28e69e7e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f42094b1f84334d32e2cf03e787ae12af975c89a5e4643031b3894ac6baef3db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ActionConnectionHttpTokenAuthHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ActionConnectionHttpTokenAuthHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ActionConnectionHttpTokenAuthHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86472a8cf9501f80e37a7b4c8ae76e426b390bfadb570a4fa812a4e6ef4dcc7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ActionConnectionHttpTokenAuthOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.actionConnection.ActionConnectionHttpTokenAuthOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cff68bd6bf6a4878bf4bb633b851b57f2ac8a7a860eda153d20473ad487f70c6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBody")
    def put_body(
        self,
        *,
        content: typing.Optional[builtins.str] = None,
        content_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param content: Serialized body content. String length must be at least 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#content ActionConnection#content}
        :param content_type: Content type of the body. String length must be at least 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#content_type ActionConnection#content_type}
        '''
        value = ActionConnectionHttpTokenAuthBody(
            content=content, content_type=content_type
        )

        return typing.cast(None, jsii.invoke(self, "putBody", [value]))

    @jsii.member(jsii_name="putHeader")
    def put_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ActionConnectionHttpTokenAuthHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aba1a85d9fdd819ce7adcd8065da595ac31654fbd5a33e2c8a442976c8e4658)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeader", [value]))

    @jsii.member(jsii_name="putToken")
    def put_token(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ActionConnectionHttpTokenAuthToken", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0468a2b05f8e7a512664bcb4b9b0687c66af183ba1681d0de1f4b186f9d0ab7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putToken", [value]))

    @jsii.member(jsii_name="putUrlParameter")
    def put_url_parameter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ActionConnectionHttpTokenAuthUrlParameter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc14c075225c769e6e345a97cdca986fc74a2662f7ffb141ffa926049dd0dc1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUrlParameter", [value]))

    @jsii.member(jsii_name="resetBody")
    def reset_body(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBody", []))

    @jsii.member(jsii_name="resetHeader")
    def reset_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeader", []))

    @jsii.member(jsii_name="resetToken")
    def reset_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetToken", []))

    @jsii.member(jsii_name="resetUrlParameter")
    def reset_url_parameter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrlParameter", []))

    @builtins.property
    @jsii.member(jsii_name="body")
    def body(self) -> ActionConnectionHttpTokenAuthBodyOutputReference:
        return typing.cast(ActionConnectionHttpTokenAuthBodyOutputReference, jsii.get(self, "body"))

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(self) -> ActionConnectionHttpTokenAuthHeaderList:
        return typing.cast(ActionConnectionHttpTokenAuthHeaderList, jsii.get(self, "header"))

    @builtins.property
    @jsii.member(jsii_name="token")
    def token(self) -> "ActionConnectionHttpTokenAuthTokenList":
        return typing.cast("ActionConnectionHttpTokenAuthTokenList", jsii.get(self, "token"))

    @builtins.property
    @jsii.member(jsii_name="urlParameter")
    def url_parameter(self) -> "ActionConnectionHttpTokenAuthUrlParameterList":
        return typing.cast("ActionConnectionHttpTokenAuthUrlParameterList", jsii.get(self, "urlParameter"))

    @builtins.property
    @jsii.member(jsii_name="bodyInput")
    def body_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ActionConnectionHttpTokenAuthBody]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ActionConnectionHttpTokenAuthBody]], jsii.get(self, "bodyInput"))

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ActionConnectionHttpTokenAuthHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ActionConnectionHttpTokenAuthHeader]]], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenInput")
    def token_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ActionConnectionHttpTokenAuthToken"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ActionConnectionHttpTokenAuthToken"]]], jsii.get(self, "tokenInput"))

    @builtins.property
    @jsii.member(jsii_name="urlParameterInput")
    def url_parameter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ActionConnectionHttpTokenAuthUrlParameter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ActionConnectionHttpTokenAuthUrlParameter"]]], jsii.get(self, "urlParameterInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ActionConnectionHttpTokenAuth]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ActionConnectionHttpTokenAuth]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ActionConnectionHttpTokenAuth]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2572c02d68a308cee59c9161904acedbaf4680bd1b8b98ea04f6ab69b5a8daac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.actionConnection.ActionConnectionHttpTokenAuthToken",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "type": "type", "value": "value"},
)
class ActionConnectionHttpTokenAuthToken:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Token name. String length must be at least 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#name ActionConnection#name}
        :param type: Token type Valid values are ``SECRET``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#type ActionConnection#type}
        :param value: Token value. String length must be at least 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#value ActionConnection#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1a340979827a96ac531b7efe576c6e6f6802e933697adce2767bf4f331ade7b)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if type is not None:
            self._values["type"] = type
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Token name. String length must be at least 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#name ActionConnection#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Token type Valid values are ``SECRET``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#type ActionConnection#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Token value. String length must be at least 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#value ActionConnection#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionConnectionHttpTokenAuthToken(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ActionConnectionHttpTokenAuthTokenList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.actionConnection.ActionConnectionHttpTokenAuthTokenList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c52833791d70922c4fc87e32d3c39279d9847bf019d4f19517ae3f4460e42ac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ActionConnectionHttpTokenAuthTokenOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b6cba876552b9037c7e79d600de69b4299300c704d6e9b301c3e7151b3abd97)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ActionConnectionHttpTokenAuthTokenOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13419e81aee779b02bddb63b2005cc0ab08f15ae6522a55f3c8baeace5f7ebd2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f4a2828c792a8e30618575877110e932ddac97a9e071f02820b5fe74ee96e1f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__707a1d115c3024ecb97394087fba7ff58dac74148795f4bc971767d9a64e1d32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ActionConnectionHttpTokenAuthToken]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ActionConnectionHttpTokenAuthToken]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ActionConnectionHttpTokenAuthToken]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27fd2e810c3198c21d20be447426ffd707563b8ef487a7457dd649b793826f97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ActionConnectionHttpTokenAuthTokenOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.actionConnection.ActionConnectionHttpTokenAuthTokenOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46ac87abf08c82fa61eada87e29142d195f2b46b5ed61195694c30a112afae60)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__947c1b57a45b6da7df1aa94f0f9e800c42e42ba3f391c4236c6c25c158ee9a66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cda5d442265d23437c90576c92ed1f8330592765501153201eec779eced37568)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aa230d56045490f5889dc559374d11bc8bf09593c6c332861c8397ce813c433)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ActionConnectionHttpTokenAuthToken]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ActionConnectionHttpTokenAuthToken]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ActionConnectionHttpTokenAuthToken]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb396a6edb45ebb0d42f52aa68ab7e25ec1cb057d320fbf3a596c854db32deac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.actionConnection.ActionConnectionHttpTokenAuthUrlParameter",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class ActionConnectionHttpTokenAuthUrlParameter:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: URL parameter name. String length must be at least 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#name ActionConnection#name}
        :param value: URL parameter value. String length must be at least 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#value ActionConnection#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adf868f6095df1cfa5ce166ee70e0c1877607ae81b3716f9a0a2a1e371c79933)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''URL parameter name. String length must be at least 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#name ActionConnection#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''URL parameter value. String length must be at least 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/action_connection#value ActionConnection#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionConnectionHttpTokenAuthUrlParameter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ActionConnectionHttpTokenAuthUrlParameterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.actionConnection.ActionConnectionHttpTokenAuthUrlParameterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3398fe8768c9e4b85acd5b2b99c09c514802295e82bf7ef23b544faa84d21e48)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ActionConnectionHttpTokenAuthUrlParameterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44e2be608f3f406684966beb15c8eb3e72b13d11e1eb4c522590482006d2bc8e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ActionConnectionHttpTokenAuthUrlParameterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e0c19ba9d39f2e6e571e6aa2a1594611b6827d0de5cd25edc1aaf815bc2b3bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3428a77460865b362d0ce1384b3aab15f67023eb927a837081a071b09221ed20)
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
            type_hints = typing.get_type_hints(_typecheckingstub__494c1eee1cf7c8ba5081a98ff4fcacecb070783fa69440370fea3dba9dae4833)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ActionConnectionHttpTokenAuthUrlParameter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ActionConnectionHttpTokenAuthUrlParameter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ActionConnectionHttpTokenAuthUrlParameter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e47af171a0d606fcf84e422fd25262e6b734f4c7be9b72012a22da45493d935)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ActionConnectionHttpTokenAuthUrlParameterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.actionConnection.ActionConnectionHttpTokenAuthUrlParameterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e06a24bca5f15d2b4f887b5ab774a4d115024ea231025e21beb42dfd1ae4554)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e1ac1e901653f7be5c8fdc250d4e42ef740cd9a3505439185691288608e2a3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61b8d10bf9163c127837b8b391af4c77e471aaaadab82f9a07b22fa14b5fb20c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ActionConnectionHttpTokenAuthUrlParameter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ActionConnectionHttpTokenAuthUrlParameter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ActionConnectionHttpTokenAuthUrlParameter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dcc1b2ecc95883e602f1583f81301b1610489ed9d2ae9ea2d76a97447d155fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ActionConnection",
    "ActionConnectionAws",
    "ActionConnectionAwsAssumeRole",
    "ActionConnectionAwsAssumeRoleOutputReference",
    "ActionConnectionAwsOutputReference",
    "ActionConnectionConfig",
    "ActionConnectionHttp",
    "ActionConnectionHttpOutputReference",
    "ActionConnectionHttpTokenAuth",
    "ActionConnectionHttpTokenAuthBody",
    "ActionConnectionHttpTokenAuthBodyOutputReference",
    "ActionConnectionHttpTokenAuthHeader",
    "ActionConnectionHttpTokenAuthHeaderList",
    "ActionConnectionHttpTokenAuthHeaderOutputReference",
    "ActionConnectionHttpTokenAuthOutputReference",
    "ActionConnectionHttpTokenAuthToken",
    "ActionConnectionHttpTokenAuthTokenList",
    "ActionConnectionHttpTokenAuthTokenOutputReference",
    "ActionConnectionHttpTokenAuthUrlParameter",
    "ActionConnectionHttpTokenAuthUrlParameterList",
    "ActionConnectionHttpTokenAuthUrlParameterOutputReference",
]

publication.publish()

def _typecheckingstub__529edb8862c892350021822a3cb1af453ed1456a2b30d430f82abe40f80328c7(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    aws: typing.Optional[typing.Union[ActionConnectionAws, typing.Dict[builtins.str, typing.Any]]] = None,
    http: typing.Optional[typing.Union[ActionConnectionHttp, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__06b3755f4c10317ad23600a7d45f8221df1db416e0137e4874741ce050d61d95(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b10eeb2f3c9147091aefb0554a2a1117efe39e367f0b82608c76ddfafc091b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f25da154ba2fb59eafbbbf353fb5947a69d863fe3393a4d3e63f4ea9e8acdab5(
    *,
    assume_role: typing.Optional[typing.Union[ActionConnectionAwsAssumeRole, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46762c6ecae4849cdeddffca1d9f39adc1c839417658264821ca7a6cac579a58(
    *,
    account_id: typing.Optional[builtins.str] = None,
    role: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39e35f5fd8d04dbfa5ae916ec421decfcec0f5464a3d93dc77363d279f3ff1b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f267de337c5e565014c5560768923b24c85404d6bd9d8ff76a1f87c52a12bed5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87f5366d282cf980e283671a6bbb00e0fd132891e202d42cffda496335d8a3c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b63ace98318e1c518159321c3fca45893e41c4aca1a867a7c87ece16f634e5c(
    value: typing.Optional[typing.Union[ActionConnectionAwsAssumeRole, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dd18f049a61e0b2afcb0dd891ce8b32e21acd1e8ceb4398bd581da714dcfdc7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e11dfde9238bb48c6dcc5bea8903549cdf066293740e57e23581350348910f4(
    value: typing.Optional[typing.Union[ActionConnectionAws, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63752c5ec5c01ac27d871f4e4a5b9482425473f7f789bc408a21d91d52cd8f8f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    aws: typing.Optional[typing.Union[ActionConnectionAws, typing.Dict[builtins.str, typing.Any]]] = None,
    http: typing.Optional[typing.Union[ActionConnectionHttp, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9f89e62962a63aa44470d224036b9149865a993765db78d3bbb85c41177dc75(
    *,
    base_url: typing.Optional[builtins.str] = None,
    token_auth: typing.Optional[typing.Union[ActionConnectionHttpTokenAuth, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56d8b79b4f356607b0b8466722ca98ba51a93af443c4b1f2693a002a1c32c733(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a66ec497642e0b4a6737615f6cfd1674b3e4606165bdb57e0e4808f7cddba08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a510182737e2090c0350645e31f7f6ed1a048a24895319564dc6fd5164a1b9b(
    value: typing.Optional[typing.Union[ActionConnectionHttp, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04d732816dcc1fd92afbd455569f6d6fa9d458c0c445748fb04dd25cb924c833(
    *,
    body: typing.Optional[typing.Union[ActionConnectionHttpTokenAuthBody, typing.Dict[builtins.str, typing.Any]]] = None,
    header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ActionConnectionHttpTokenAuthHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    token: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ActionConnectionHttpTokenAuthToken, typing.Dict[builtins.str, typing.Any]]]]] = None,
    url_parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ActionConnectionHttpTokenAuthUrlParameter, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86ca630442e327b336aa1bdb3bfd22dd977aa3a34155cff688f556d6c9a1540d(
    *,
    content: typing.Optional[builtins.str] = None,
    content_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b6e700c624d605df01b6f9ca0e6599d5d078a8835e407723881a0f32a884782(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48e99f8f9cf3ddb2357d0d3b58166d2465e74eafd803fc24a0d355b4d77b82b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97fb071e5475e47dd90b0feada67b87e3602702fc651b3041e0dbb961b3f8339(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c80cd7b1e3a6109bb1512f997ccc1b99d726884948f907f41d3086abdb1267b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ActionConnectionHttpTokenAuthBody]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34cb02e5fc2a376610267fbcf33fcf2cb55ecf37fa0aa48430e68a577161a995(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c912fcc03875ec45695ccaf4476423dc2a865aa7c70092dee28b5effb6e6134b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b8a22f2c59c9da1ece3f0b4c45932713c31f552edaa31c9b0277a4be5f8a702(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1e9d132d061338ace3f3afa2f9e654800448023f7508b33e908a08e449d4a89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3505c908fc7111ec79bd39214dc2f16143a799846574e87a219a3287b03ba16b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32aba910475c1e71839ab45cb65b1920f0475bf60c16739cdcdd147499394f89(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e474ce69012d90c8a741588fd64fa6b10686856285fd2b67934656fadc3b3d9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ActionConnectionHttpTokenAuthHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8adc6a22ee9bd3b741078e1f1af164e6c270f5077fd739f8e5dd79d0c085dabc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9514f9df418cc4e3d2f7721315f0fdd2814555e5a032aad71620e5d28e69e7e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f42094b1f84334d32e2cf03e787ae12af975c89a5e4643031b3894ac6baef3db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86472a8cf9501f80e37a7b4c8ae76e426b390bfadb570a4fa812a4e6ef4dcc7e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ActionConnectionHttpTokenAuthHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cff68bd6bf6a4878bf4bb633b851b57f2ac8a7a860eda153d20473ad487f70c6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aba1a85d9fdd819ce7adcd8065da595ac31654fbd5a33e2c8a442976c8e4658(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ActionConnectionHttpTokenAuthHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0468a2b05f8e7a512664bcb4b9b0687c66af183ba1681d0de1f4b186f9d0ab7c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ActionConnectionHttpTokenAuthToken, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc14c075225c769e6e345a97cdca986fc74a2662f7ffb141ffa926049dd0dc1c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ActionConnectionHttpTokenAuthUrlParameter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2572c02d68a308cee59c9161904acedbaf4680bd1b8b98ea04f6ab69b5a8daac(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ActionConnectionHttpTokenAuth]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1a340979827a96ac531b7efe576c6e6f6802e933697adce2767bf4f331ade7b(
    *,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c52833791d70922c4fc87e32d3c39279d9847bf019d4f19517ae3f4460e42ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b6cba876552b9037c7e79d600de69b4299300c704d6e9b301c3e7151b3abd97(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13419e81aee779b02bddb63b2005cc0ab08f15ae6522a55f3c8baeace5f7ebd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f4a2828c792a8e30618575877110e932ddac97a9e071f02820b5fe74ee96e1f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__707a1d115c3024ecb97394087fba7ff58dac74148795f4bc971767d9a64e1d32(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27fd2e810c3198c21d20be447426ffd707563b8ef487a7457dd649b793826f97(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ActionConnectionHttpTokenAuthToken]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46ac87abf08c82fa61eada87e29142d195f2b46b5ed61195694c30a112afae60(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__947c1b57a45b6da7df1aa94f0f9e800c42e42ba3f391c4236c6c25c158ee9a66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cda5d442265d23437c90576c92ed1f8330592765501153201eec779eced37568(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aa230d56045490f5889dc559374d11bc8bf09593c6c332861c8397ce813c433(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb396a6edb45ebb0d42f52aa68ab7e25ec1cb057d320fbf3a596c854db32deac(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ActionConnectionHttpTokenAuthToken]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adf868f6095df1cfa5ce166ee70e0c1877607ae81b3716f9a0a2a1e371c79933(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3398fe8768c9e4b85acd5b2b99c09c514802295e82bf7ef23b544faa84d21e48(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44e2be608f3f406684966beb15c8eb3e72b13d11e1eb4c522590482006d2bc8e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e0c19ba9d39f2e6e571e6aa2a1594611b6827d0de5cd25edc1aaf815bc2b3bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3428a77460865b362d0ce1384b3aab15f67023eb927a837081a071b09221ed20(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__494c1eee1cf7c8ba5081a98ff4fcacecb070783fa69440370fea3dba9dae4833(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e47af171a0d606fcf84e422fd25262e6b734f4c7be9b72012a22da45493d935(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ActionConnectionHttpTokenAuthUrlParameter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e06a24bca5f15d2b4f887b5ab774a4d115024ea231025e21beb42dfd1ae4554(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e1ac1e901653f7be5c8fdc250d4e42ef740cd9a3505439185691288608e2a3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61b8d10bf9163c127837b8b391af4c77e471aaaadab82f9a07b22fa14b5fb20c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dcc1b2ecc95883e602f1583f81301b1610489ed9d2ae9ea2d76a97447d155fa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ActionConnectionHttpTokenAuthUrlParameter]],
) -> None:
    """Type checking stubs"""
    pass
