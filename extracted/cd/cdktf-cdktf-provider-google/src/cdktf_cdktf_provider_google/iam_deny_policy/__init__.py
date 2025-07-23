r'''
# `google_iam_deny_policy`

Refer to the Terraform Registry for docs: [`google_iam_deny_policy`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy).
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


class IamDenyPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iamDenyPolicy.IamDenyPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy google_iam_deny_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        parent: builtins.str,
        rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IamDenyPolicyRules", typing.Dict[builtins.str, typing.Any]]]],
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["IamDenyPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy google_iam_deny_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name of the policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#name IamDenyPolicy#name}
        :param parent: The attachment point is identified by its URL-encoded full resource name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#parent IamDenyPolicy#parent}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#rules IamDenyPolicy#rules}
        :param display_name: The display name of the rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#display_name IamDenyPolicy#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#id IamDenyPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#timeouts IamDenyPolicy#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebf9653c0bbd860e4eee0e23f036c0debb5196a3d7fc2f133602b300fcee35e9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = IamDenyPolicyConfig(
            name=name,
            parent=parent,
            rules=rules,
            display_name=display_name,
            id=id,
            timeouts=timeouts,
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
        '''Generates CDKTF code for importing a IamDenyPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the IamDenyPolicy to import.
        :param import_from_id: The id of the existing IamDenyPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the IamDenyPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00ae8ab2c34288ab648b837efe83e362e1ddbcd2a7c15a81a97e49f1e465811b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRules")
    def put_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IamDenyPolicyRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9869b230e4ff255cdf79fc2e01268b32735dbd90a0dbea0d719ff85223613a1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRules", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#create IamDenyPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#delete IamDenyPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#update IamDenyPolicy#update}.
        '''
        value = IamDenyPolicyTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

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
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> "IamDenyPolicyRulesList":
        return typing.cast("IamDenyPolicyRulesList", jsii.get(self, "rules"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "IamDenyPolicyTimeoutsOutputReference":
        return typing.cast("IamDenyPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parentInput")
    def parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentInput"))

    @builtins.property
    @jsii.member(jsii_name="rulesInput")
    def rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IamDenyPolicyRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IamDenyPolicyRules"]]], jsii.get(self, "rulesInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IamDenyPolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IamDenyPolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d02b10c3928ca537b8de6d6628af18e1a647f5881933ba690a463bd927fc139f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd322092d66bf6a2fcfad55d7b55ef23eb08fc0203a189dfc6f34e4b78fad9b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54d9ccf6c337532b1d82566497a6ded187ae72122afb0c8c081811e879422650)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dee2769d2e553745052ea9388d6a71df8218f915f1746288db9d2445f69c36f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iamDenyPolicy.IamDenyPolicyConfig",
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
        "parent": "parent",
        "rules": "rules",
        "display_name": "displayName",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class IamDenyPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        parent: builtins.str,
        rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IamDenyPolicyRules", typing.Dict[builtins.str, typing.Any]]]],
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["IamDenyPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The name of the policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#name IamDenyPolicy#name}
        :param parent: The attachment point is identified by its URL-encoded full resource name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#parent IamDenyPolicy#parent}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#rules IamDenyPolicy#rules}
        :param display_name: The display name of the rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#display_name IamDenyPolicy#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#id IamDenyPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#timeouts IamDenyPolicy#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = IamDenyPolicyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cec96f37a0d4450b4149e1d397c1366a80fecbeee7d1f4fc48e13b30bfcf0faf)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "parent": parent,
            "rules": rules,
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
        if display_name is not None:
            self._values["display_name"] = display_name
        if id is not None:
            self._values["id"] = id
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
        '''The name of the policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#name IamDenyPolicy#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parent(self) -> builtins.str:
        '''The attachment point is identified by its URL-encoded full resource name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#parent IamDenyPolicy#parent}
        '''
        result = self._values.get("parent")
        assert result is not None, "Required property 'parent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rules(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IamDenyPolicyRules"]]:
        '''rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#rules IamDenyPolicy#rules}
        '''
        result = self._values.get("rules")
        assert result is not None, "Required property 'rules' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IamDenyPolicyRules"]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#display_name IamDenyPolicy#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#id IamDenyPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["IamDenyPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#timeouts IamDenyPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["IamDenyPolicyTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamDenyPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iamDenyPolicy.IamDenyPolicyRules",
    jsii_struct_bases=[],
    name_mapping={"deny_rule": "denyRule", "description": "description"},
)
class IamDenyPolicyRules:
    def __init__(
        self,
        *,
        deny_rule: typing.Optional[typing.Union["IamDenyPolicyRulesDenyRule", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param deny_rule: deny_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#deny_rule IamDenyPolicy#deny_rule}
        :param description: The description of the rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#description IamDenyPolicy#description}
        '''
        if isinstance(deny_rule, dict):
            deny_rule = IamDenyPolicyRulesDenyRule(**deny_rule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd8843d9a58922d231b2a1b1da359adfc6fa77657acdf3e920d7b8cdec4489cb)
            check_type(argname="argument deny_rule", value=deny_rule, expected_type=type_hints["deny_rule"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if deny_rule is not None:
            self._values["deny_rule"] = deny_rule
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def deny_rule(self) -> typing.Optional["IamDenyPolicyRulesDenyRule"]:
        '''deny_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#deny_rule IamDenyPolicy#deny_rule}
        '''
        result = self._values.get("deny_rule")
        return typing.cast(typing.Optional["IamDenyPolicyRulesDenyRule"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#description IamDenyPolicy#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamDenyPolicyRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iamDenyPolicy.IamDenyPolicyRulesDenyRule",
    jsii_struct_bases=[],
    name_mapping={
        "denial_condition": "denialCondition",
        "denied_permissions": "deniedPermissions",
        "denied_principals": "deniedPrincipals",
        "exception_permissions": "exceptionPermissions",
        "exception_principals": "exceptionPrincipals",
    },
)
class IamDenyPolicyRulesDenyRule:
    def __init__(
        self,
        *,
        denial_condition: typing.Optional[typing.Union["IamDenyPolicyRulesDenyRuleDenialCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        denied_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
        denied_principals: typing.Optional[typing.Sequence[builtins.str]] = None,
        exception_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
        exception_principals: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param denial_condition: denial_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#denial_condition IamDenyPolicy#denial_condition}
        :param denied_permissions: The permissions that are explicitly denied by this rule. Each permission uses the format '{service-fqdn}/{resource}.{verb}', where '{service-fqdn}' is the fully qualified domain name for the service. For example, 'iam.googleapis.com/roles.list'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#denied_permissions IamDenyPolicy#denied_permissions}
        :param denied_principals: The identities that are prevented from using one or more permissions on Google Cloud resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#denied_principals IamDenyPolicy#denied_principals}
        :param exception_permissions: Specifies the permissions that this rule excludes from the set of denied permissions given by deniedPermissions. If a permission appears in deniedPermissions and in exceptionPermissions then it will not be denied. The excluded permissions can be specified using the same syntax as deniedPermissions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#exception_permissions IamDenyPolicy#exception_permissions}
        :param exception_principals: The identities that are excluded from the deny rule, even if they are listed in the deniedPrincipals. For example, you could add a Google group to the deniedPrincipals, then exclude specific users who belong to that group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#exception_principals IamDenyPolicy#exception_principals}
        '''
        if isinstance(denial_condition, dict):
            denial_condition = IamDenyPolicyRulesDenyRuleDenialCondition(**denial_condition)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91f8412a495d38643b485b8acf673e63efd66bb7ab8ad818987edbb0e8c91f74)
            check_type(argname="argument denial_condition", value=denial_condition, expected_type=type_hints["denial_condition"])
            check_type(argname="argument denied_permissions", value=denied_permissions, expected_type=type_hints["denied_permissions"])
            check_type(argname="argument denied_principals", value=denied_principals, expected_type=type_hints["denied_principals"])
            check_type(argname="argument exception_permissions", value=exception_permissions, expected_type=type_hints["exception_permissions"])
            check_type(argname="argument exception_principals", value=exception_principals, expected_type=type_hints["exception_principals"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if denial_condition is not None:
            self._values["denial_condition"] = denial_condition
        if denied_permissions is not None:
            self._values["denied_permissions"] = denied_permissions
        if denied_principals is not None:
            self._values["denied_principals"] = denied_principals
        if exception_permissions is not None:
            self._values["exception_permissions"] = exception_permissions
        if exception_principals is not None:
            self._values["exception_principals"] = exception_principals

    @builtins.property
    def denial_condition(
        self,
    ) -> typing.Optional["IamDenyPolicyRulesDenyRuleDenialCondition"]:
        '''denial_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#denial_condition IamDenyPolicy#denial_condition}
        '''
        result = self._values.get("denial_condition")
        return typing.cast(typing.Optional["IamDenyPolicyRulesDenyRuleDenialCondition"], result)

    @builtins.property
    def denied_permissions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The permissions that are explicitly denied by this rule.

        Each permission uses the format '{service-fqdn}/{resource}.{verb}',
        where '{service-fqdn}' is the fully qualified domain name for the service. For example, 'iam.googleapis.com/roles.list'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#denied_permissions IamDenyPolicy#denied_permissions}
        '''
        result = self._values.get("denied_permissions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def denied_principals(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The identities that are prevented from using one or more permissions on Google Cloud resources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#denied_principals IamDenyPolicy#denied_principals}
        '''
        result = self._values.get("denied_principals")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def exception_permissions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the permissions that this rule excludes from the set of denied permissions given by deniedPermissions.

        If a permission appears in deniedPermissions and in exceptionPermissions then it will not be denied.
        The excluded permissions can be specified using the same syntax as deniedPermissions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#exception_permissions IamDenyPolicy#exception_permissions}
        '''
        result = self._values.get("exception_permissions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def exception_principals(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The identities that are excluded from the deny rule, even if they are listed in the deniedPrincipals.

        For example, you could add a Google group to the deniedPrincipals, then exclude specific users who belong to that group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#exception_principals IamDenyPolicy#exception_principals}
        '''
        result = self._values.get("exception_principals")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamDenyPolicyRulesDenyRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iamDenyPolicy.IamDenyPolicyRulesDenyRuleDenialCondition",
    jsii_struct_bases=[],
    name_mapping={
        "expression": "expression",
        "description": "description",
        "location": "location",
        "title": "title",
    },
)
class IamDenyPolicyRulesDenyRuleDenialCondition:
    def __init__(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#expression IamDenyPolicy#expression}
        :param description: Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#description IamDenyPolicy#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#location IamDenyPolicy#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#title IamDenyPolicy#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c99e48017abadfdcf6e02a7e030484e30d67a716715835c8d280348e727d2c2)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "expression": expression,
        }
        if description is not None:
            self._values["description"] = description
        if location is not None:
            self._values["location"] = location
        if title is not None:
            self._values["title"] = title

    @builtins.property
    def expression(self) -> builtins.str:
        '''Textual representation of an expression in Common Expression Language syntax.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#expression IamDenyPolicy#expression}
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the expression.

        This is a longer text which describes the expression,
        e.g. when hovered over it in a UI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#description IamDenyPolicy#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#location IamDenyPolicy#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#title IamDenyPolicy#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamDenyPolicyRulesDenyRuleDenialCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IamDenyPolicyRulesDenyRuleDenialConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iamDenyPolicy.IamDenyPolicyRulesDenyRuleDenialConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2325f89965a68ff0406f8ccd4ef6078797f1b4847973c1994b14f3d74b3c528e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetTitle")
    def reset_title(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTitle", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="expressionInput")
    def expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expressionInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46e56ecdd45693cd603a7958d9040550e3ecb950ee2cb7827358b4dce409a9b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c49cba96a886da56c7e77b464af9e7d931ad09f4f1b9da121e2e527b99cdbf20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77a2429399b6664c5c69d5abcfde75e687d125f343ff8d7252a67582a8f60724)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1af11da8676a6683835d29f2f455c599bf59c133abcfe4b1b35f33067a6dade1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IamDenyPolicyRulesDenyRuleDenialCondition]:
        return typing.cast(typing.Optional[IamDenyPolicyRulesDenyRuleDenialCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IamDenyPolicyRulesDenyRuleDenialCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b98d7f484dc1ac1a7963d0d0431631e65f4a88c6db78e796429605933d47822)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IamDenyPolicyRulesDenyRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iamDenyPolicy.IamDenyPolicyRulesDenyRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd897a7820d0490df0c731797cc53da89186b7a7ff2fcac2de5a8233f0f2726a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDenialCondition")
    def put_denial_condition(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#expression IamDenyPolicy#expression}
        :param description: Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#description IamDenyPolicy#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#location IamDenyPolicy#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#title IamDenyPolicy#title}
        '''
        value = IamDenyPolicyRulesDenyRuleDenialCondition(
            expression=expression,
            description=description,
            location=location,
            title=title,
        )

        return typing.cast(None, jsii.invoke(self, "putDenialCondition", [value]))

    @jsii.member(jsii_name="resetDenialCondition")
    def reset_denial_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDenialCondition", []))

    @jsii.member(jsii_name="resetDeniedPermissions")
    def reset_denied_permissions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeniedPermissions", []))

    @jsii.member(jsii_name="resetDeniedPrincipals")
    def reset_denied_principals(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeniedPrincipals", []))

    @jsii.member(jsii_name="resetExceptionPermissions")
    def reset_exception_permissions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExceptionPermissions", []))

    @jsii.member(jsii_name="resetExceptionPrincipals")
    def reset_exception_principals(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExceptionPrincipals", []))

    @builtins.property
    @jsii.member(jsii_name="denialCondition")
    def denial_condition(
        self,
    ) -> IamDenyPolicyRulesDenyRuleDenialConditionOutputReference:
        return typing.cast(IamDenyPolicyRulesDenyRuleDenialConditionOutputReference, jsii.get(self, "denialCondition"))

    @builtins.property
    @jsii.member(jsii_name="denialConditionInput")
    def denial_condition_input(
        self,
    ) -> typing.Optional[IamDenyPolicyRulesDenyRuleDenialCondition]:
        return typing.cast(typing.Optional[IamDenyPolicyRulesDenyRuleDenialCondition], jsii.get(self, "denialConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="deniedPermissionsInput")
    def denied_permissions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "deniedPermissionsInput"))

    @builtins.property
    @jsii.member(jsii_name="deniedPrincipalsInput")
    def denied_principals_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "deniedPrincipalsInput"))

    @builtins.property
    @jsii.member(jsii_name="exceptionPermissionsInput")
    def exception_permissions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exceptionPermissionsInput"))

    @builtins.property
    @jsii.member(jsii_name="exceptionPrincipalsInput")
    def exception_principals_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exceptionPrincipalsInput"))

    @builtins.property
    @jsii.member(jsii_name="deniedPermissions")
    def denied_permissions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "deniedPermissions"))

    @denied_permissions.setter
    def denied_permissions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4894c27315a29fcb5277ced982ad07fcd58aecdaa2b5a6a7dd06d92185bfbfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deniedPermissions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deniedPrincipals")
    def denied_principals(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "deniedPrincipals"))

    @denied_principals.setter
    def denied_principals(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fe1c0226ddb922e088219dd798f21321c0b8df74390373e2943081085c5aecc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deniedPrincipals", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exceptionPermissions")
    def exception_permissions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exceptionPermissions"))

    @exception_permissions.setter
    def exception_permissions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d81247fc11267ab8bfb8b813871dc70d96ce0ca3720bde53b0b10ddbd4f7ed61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exceptionPermissions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exceptionPrincipals")
    def exception_principals(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exceptionPrincipals"))

    @exception_principals.setter
    def exception_principals(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28998a2255006357d4050437de21d824ea306c4ddc12774adb4f6d9511d1904e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exceptionPrincipals", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IamDenyPolicyRulesDenyRule]:
        return typing.cast(typing.Optional[IamDenyPolicyRulesDenyRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IamDenyPolicyRulesDenyRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80661dc50cb33fa7e004381847fee88c4c7423fa751bd9c6dcc3f20c8509c864)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IamDenyPolicyRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iamDenyPolicy.IamDenyPolicyRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ad51d401f36efe2a235a33e1683c4d68ce24627fff3de0fa51a53e6c6ad27ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IamDenyPolicyRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dac5729c9e4c11e43081395f8e310f46b4abb3e01f280e799b948e9ceca27d4c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IamDenyPolicyRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8531a8526fb9a603783021a1d3b222072765d1761dc392c8a31162d0699f065c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc67f21536a5717e9823f75e38acf0057c51988fe9c800be7271e1def8f87b89)
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
            type_hints = typing.get_type_hints(_typecheckingstub__33bcc306394eb2e3ac5e11f33f76fabbe83d99c9c61138f8f6b1fc87eb6d6241)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IamDenyPolicyRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IamDenyPolicyRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IamDenyPolicyRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ba1f802d1c27eb2707f6b2e5f8ecb6684f5bfe609276ff5d7e4b3cde680fa99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IamDenyPolicyRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iamDenyPolicy.IamDenyPolicyRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__86d1fd856f5d5c0d5c44d8fffb76637ae72e41747235004c08017ebd4ebe280e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDenyRule")
    def put_deny_rule(
        self,
        *,
        denial_condition: typing.Optional[typing.Union[IamDenyPolicyRulesDenyRuleDenialCondition, typing.Dict[builtins.str, typing.Any]]] = None,
        denied_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
        denied_principals: typing.Optional[typing.Sequence[builtins.str]] = None,
        exception_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
        exception_principals: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param denial_condition: denial_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#denial_condition IamDenyPolicy#denial_condition}
        :param denied_permissions: The permissions that are explicitly denied by this rule. Each permission uses the format '{service-fqdn}/{resource}.{verb}', where '{service-fqdn}' is the fully qualified domain name for the service. For example, 'iam.googleapis.com/roles.list'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#denied_permissions IamDenyPolicy#denied_permissions}
        :param denied_principals: The identities that are prevented from using one or more permissions on Google Cloud resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#denied_principals IamDenyPolicy#denied_principals}
        :param exception_permissions: Specifies the permissions that this rule excludes from the set of denied permissions given by deniedPermissions. If a permission appears in deniedPermissions and in exceptionPermissions then it will not be denied. The excluded permissions can be specified using the same syntax as deniedPermissions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#exception_permissions IamDenyPolicy#exception_permissions}
        :param exception_principals: The identities that are excluded from the deny rule, even if they are listed in the deniedPrincipals. For example, you could add a Google group to the deniedPrincipals, then exclude specific users who belong to that group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#exception_principals IamDenyPolicy#exception_principals}
        '''
        value = IamDenyPolicyRulesDenyRule(
            denial_condition=denial_condition,
            denied_permissions=denied_permissions,
            denied_principals=denied_principals,
            exception_permissions=exception_permissions,
            exception_principals=exception_principals,
        )

        return typing.cast(None, jsii.invoke(self, "putDenyRule", [value]))

    @jsii.member(jsii_name="resetDenyRule")
    def reset_deny_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDenyRule", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @builtins.property
    @jsii.member(jsii_name="denyRule")
    def deny_rule(self) -> IamDenyPolicyRulesDenyRuleOutputReference:
        return typing.cast(IamDenyPolicyRulesDenyRuleOutputReference, jsii.get(self, "denyRule"))

    @builtins.property
    @jsii.member(jsii_name="denyRuleInput")
    def deny_rule_input(self) -> typing.Optional[IamDenyPolicyRulesDenyRule]:
        return typing.cast(typing.Optional[IamDenyPolicyRulesDenyRule], jsii.get(self, "denyRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f11f18ef7f62da9bbbe5a1bd7e6aac512d449ce0abf44e14f1b90c6e722c5b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IamDenyPolicyRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IamDenyPolicyRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IamDenyPolicyRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__344f75dac0443e1a9147b5e267e57fcf5d2f9684068979cb731e5bd8edfe37ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iamDenyPolicy.IamDenyPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class IamDenyPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#create IamDenyPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#delete IamDenyPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#update IamDenyPolicy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__976d9690f11e51eb09ea61e978de515ad127f437ab76afa83239047d595a62a1)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#create IamDenyPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#delete IamDenyPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_deny_policy#update IamDenyPolicy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamDenyPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IamDenyPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iamDenyPolicy.IamDenyPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4c46f02821b74c92de9b6603753a60a6060b71da9a221945e030a2dde8aadd6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__469c40cac9aacce04e644370f33c1726428643c24db936a7f3ba08e11576198c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80d0e2cbdab540c8dc810fe587d35b9481ef1833c9d1710cc69fa8ce8b0cb504)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2f35eeb5a63e7481d6be21b17eb039190d460307cae09b5339c44abd8d7b15c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IamDenyPolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IamDenyPolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IamDenyPolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aea9d351705f42b522497f0432148d90a1fecce31fd1124c0e384246d2687139)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "IamDenyPolicy",
    "IamDenyPolicyConfig",
    "IamDenyPolicyRules",
    "IamDenyPolicyRulesDenyRule",
    "IamDenyPolicyRulesDenyRuleDenialCondition",
    "IamDenyPolicyRulesDenyRuleDenialConditionOutputReference",
    "IamDenyPolicyRulesDenyRuleOutputReference",
    "IamDenyPolicyRulesList",
    "IamDenyPolicyRulesOutputReference",
    "IamDenyPolicyTimeouts",
    "IamDenyPolicyTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__ebf9653c0bbd860e4eee0e23f036c0debb5196a3d7fc2f133602b300fcee35e9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    parent: builtins.str,
    rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IamDenyPolicyRules, typing.Dict[builtins.str, typing.Any]]]],
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[IamDenyPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__00ae8ab2c34288ab648b837efe83e362e1ddbcd2a7c15a81a97e49f1e465811b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9869b230e4ff255cdf79fc2e01268b32735dbd90a0dbea0d719ff85223613a1b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IamDenyPolicyRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d02b10c3928ca537b8de6d6628af18e1a647f5881933ba690a463bd927fc139f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd322092d66bf6a2fcfad55d7b55ef23eb08fc0203a189dfc6f34e4b78fad9b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54d9ccf6c337532b1d82566497a6ded187ae72122afb0c8c081811e879422650(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dee2769d2e553745052ea9388d6a71df8218f915f1746288db9d2445f69c36f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cec96f37a0d4450b4149e1d397c1366a80fecbeee7d1f4fc48e13b30bfcf0faf(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    parent: builtins.str,
    rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IamDenyPolicyRules, typing.Dict[builtins.str, typing.Any]]]],
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[IamDenyPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd8843d9a58922d231b2a1b1da359adfc6fa77657acdf3e920d7b8cdec4489cb(
    *,
    deny_rule: typing.Optional[typing.Union[IamDenyPolicyRulesDenyRule, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91f8412a495d38643b485b8acf673e63efd66bb7ab8ad818987edbb0e8c91f74(
    *,
    denial_condition: typing.Optional[typing.Union[IamDenyPolicyRulesDenyRuleDenialCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    denied_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
    denied_principals: typing.Optional[typing.Sequence[builtins.str]] = None,
    exception_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
    exception_principals: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c99e48017abadfdcf6e02a7e030484e30d67a716715835c8d280348e727d2c2(
    *,
    expression: builtins.str,
    description: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2325f89965a68ff0406f8ccd4ef6078797f1b4847973c1994b14f3d74b3c528e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46e56ecdd45693cd603a7958d9040550e3ecb950ee2cb7827358b4dce409a9b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c49cba96a886da56c7e77b464af9e7d931ad09f4f1b9da121e2e527b99cdbf20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77a2429399b6664c5c69d5abcfde75e687d125f343ff8d7252a67582a8f60724(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1af11da8676a6683835d29f2f455c599bf59c133abcfe4b1b35f33067a6dade1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b98d7f484dc1ac1a7963d0d0431631e65f4a88c6db78e796429605933d47822(
    value: typing.Optional[IamDenyPolicyRulesDenyRuleDenialCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd897a7820d0490df0c731797cc53da89186b7a7ff2fcac2de5a8233f0f2726a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4894c27315a29fcb5277ced982ad07fcd58aecdaa2b5a6a7dd06d92185bfbfb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fe1c0226ddb922e088219dd798f21321c0b8df74390373e2943081085c5aecc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d81247fc11267ab8bfb8b813871dc70d96ce0ca3720bde53b0b10ddbd4f7ed61(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28998a2255006357d4050437de21d824ea306c4ddc12774adb4f6d9511d1904e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80661dc50cb33fa7e004381847fee88c4c7423fa751bd9c6dcc3f20c8509c864(
    value: typing.Optional[IamDenyPolicyRulesDenyRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ad51d401f36efe2a235a33e1683c4d68ce24627fff3de0fa51a53e6c6ad27ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dac5729c9e4c11e43081395f8e310f46b4abb3e01f280e799b948e9ceca27d4c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8531a8526fb9a603783021a1d3b222072765d1761dc392c8a31162d0699f065c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc67f21536a5717e9823f75e38acf0057c51988fe9c800be7271e1def8f87b89(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33bcc306394eb2e3ac5e11f33f76fabbe83d99c9c61138f8f6b1fc87eb6d6241(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ba1f802d1c27eb2707f6b2e5f8ecb6684f5bfe609276ff5d7e4b3cde680fa99(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IamDenyPolicyRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86d1fd856f5d5c0d5c44d8fffb76637ae72e41747235004c08017ebd4ebe280e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f11f18ef7f62da9bbbe5a1bd7e6aac512d449ce0abf44e14f1b90c6e722c5b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__344f75dac0443e1a9147b5e267e57fcf5d2f9684068979cb731e5bd8edfe37ba(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IamDenyPolicyRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__976d9690f11e51eb09ea61e978de515ad127f437ab76afa83239047d595a62a1(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4c46f02821b74c92de9b6603753a60a6060b71da9a221945e030a2dde8aadd6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__469c40cac9aacce04e644370f33c1726428643c24db936a7f3ba08e11576198c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80d0e2cbdab540c8dc810fe587d35b9481ef1833c9d1710cc69fa8ce8b0cb504(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2f35eeb5a63e7481d6be21b17eb039190d460307cae09b5339c44abd8d7b15c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aea9d351705f42b522497f0432148d90a1fecce31fd1124c0e384246d2687139(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IamDenyPolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
