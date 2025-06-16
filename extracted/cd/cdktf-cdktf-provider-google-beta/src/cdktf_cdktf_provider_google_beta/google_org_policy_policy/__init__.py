r'''
# `google_org_policy_policy`

Refer to the Terraform Registry for docs: [`google_org_policy_policy`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy).
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


class GoogleOrgPolicyPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOrgPolicyPolicy.GoogleOrgPolicyPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy google_org_policy_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        parent: builtins.str,
        dry_run_spec: typing.Optional[typing.Union["GoogleOrgPolicyPolicyDryRunSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        spec: typing.Optional[typing.Union["GoogleOrgPolicyPolicySpec", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleOrgPolicyPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy google_org_policy_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Immutable. The resource name of the Policy. Must be one of the following forms, where constraint_name is the name of the constraint which this Policy configures: * 'projects/{project_number}/policies/{constraint_name}' * 'folders/{folder_id}/policies/{constraint_name}' * 'organizations/{organization_id}/policies/{constraint_name}' For example, "projects/123/policies/compute.disableSerialPortAccess". Note: 'projects/{project_id}/policies/{constraint_name}' is also an acceptable name for API requests, but responses will return the name using the equivalent project number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#name GoogleOrgPolicyPolicy#name}
        :param parent: The parent of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#parent GoogleOrgPolicyPolicy#parent}
        :param dry_run_spec: dry_run_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#dry_run_spec GoogleOrgPolicyPolicy#dry_run_spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#id GoogleOrgPolicyPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#spec GoogleOrgPolicyPolicy#spec}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#timeouts GoogleOrgPolicyPolicy#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e8a4ffd4accd1a6036c9980d0afa4ccf8a3cc4a9d7a2eaa87a976e1f3a4dd49)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleOrgPolicyPolicyConfig(
            name=name,
            parent=parent,
            dry_run_spec=dry_run_spec,
            id=id,
            spec=spec,
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
        '''Generates CDKTF code for importing a GoogleOrgPolicyPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleOrgPolicyPolicy to import.
        :param import_from_id: The id of the existing GoogleOrgPolicyPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleOrgPolicyPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__118a6023f15a27663098cd846959c688e78ca2fbc61c7dd22e3fa9e05164424a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDryRunSpec")
    def put_dry_run_spec(
        self,
        *,
        inherit_from_parent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        reset: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOrgPolicyPolicyDryRunSpecRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param inherit_from_parent: Determines the inheritance behavior for this policy. If 'inherit_from_parent' is true, policy rules set higher up in the hierarchy (up to the closest root) are inherited and present in the effective policy. If it is false, then no rules are inherited, and this policy becomes the new root for evaluation. This field can be set only for policies which configure list constraints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#inherit_from_parent GoogleOrgPolicyPolicy#inherit_from_parent}
        :param reset: Ignores policies set above this resource and restores the 'constraint_default' enforcement behavior of the specific constraint at this resource. This field can be set in policies for either list or boolean constraints. If set, 'rules' must be empty and 'inherit_from_parent' must be set to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#reset GoogleOrgPolicyPolicy#reset}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#rules GoogleOrgPolicyPolicy#rules}
        '''
        value = GoogleOrgPolicyPolicyDryRunSpec(
            inherit_from_parent=inherit_from_parent, reset=reset, rules=rules
        )

        return typing.cast(None, jsii.invoke(self, "putDryRunSpec", [value]))

    @jsii.member(jsii_name="putSpec")
    def put_spec(
        self,
        *,
        inherit_from_parent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        reset: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOrgPolicyPolicySpecRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param inherit_from_parent: Determines the inheritance behavior for this 'Policy'. If 'inherit_from_parent' is true, PolicyRules set higher up in the hierarchy (up to the closest root) are inherited and present in the effective policy. If it is false, then no rules are inherited, and this Policy becomes the new root for evaluation. This field can be set only for Policies which configure list constraints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#inherit_from_parent GoogleOrgPolicyPolicy#inherit_from_parent}
        :param reset: Ignores policies set above this resource and restores the 'constraint_default' enforcement behavior of the specific 'Constraint' at this resource. This field can be set in policies for either list or boolean constraints. If set, 'rules' must be empty and 'inherit_from_parent' must be set to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#reset GoogleOrgPolicyPolicy#reset}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#rules GoogleOrgPolicyPolicy#rules}
        '''
        value = GoogleOrgPolicyPolicySpec(
            inherit_from_parent=inherit_from_parent, reset=reset, rules=rules
        )

        return typing.cast(None, jsii.invoke(self, "putSpec", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#create GoogleOrgPolicyPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#delete GoogleOrgPolicyPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#update GoogleOrgPolicyPolicy#update}.
        '''
        value = GoogleOrgPolicyPolicyTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDryRunSpec")
    def reset_dry_run_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDryRunSpec", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetSpec")
    def reset_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpec", []))

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
    @jsii.member(jsii_name="dryRunSpec")
    def dry_run_spec(self) -> "GoogleOrgPolicyPolicyDryRunSpecOutputReference":
        return typing.cast("GoogleOrgPolicyPolicyDryRunSpecOutputReference", jsii.get(self, "dryRunSpec"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="spec")
    def spec(self) -> "GoogleOrgPolicyPolicySpecOutputReference":
        return typing.cast("GoogleOrgPolicyPolicySpecOutputReference", jsii.get(self, "spec"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleOrgPolicyPolicyTimeoutsOutputReference":
        return typing.cast("GoogleOrgPolicyPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="dryRunSpecInput")
    def dry_run_spec_input(self) -> typing.Optional["GoogleOrgPolicyPolicyDryRunSpec"]:
        return typing.cast(typing.Optional["GoogleOrgPolicyPolicyDryRunSpec"], jsii.get(self, "dryRunSpecInput"))

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
    @jsii.member(jsii_name="specInput")
    def spec_input(self) -> typing.Optional["GoogleOrgPolicyPolicySpec"]:
        return typing.cast(typing.Optional["GoogleOrgPolicyPolicySpec"], jsii.get(self, "specInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleOrgPolicyPolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleOrgPolicyPolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b8809e127e5f908bc9d8b809ec184e6b9971e01b2900c9a5a0bccd36820b46e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad5300fd2514a8578f316b324ae6ca54c23ce71ee22caf1606b13a79fa26ecd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ea75a4ee4445012862a7aed9ffb2a8d9dc09378a73130aeb85fbea274f593e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOrgPolicyPolicy.GoogleOrgPolicyPolicyConfig",
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
        "dry_run_spec": "dryRunSpec",
        "id": "id",
        "spec": "spec",
        "timeouts": "timeouts",
    },
)
class GoogleOrgPolicyPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        dry_run_spec: typing.Optional[typing.Union["GoogleOrgPolicyPolicyDryRunSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        spec: typing.Optional[typing.Union["GoogleOrgPolicyPolicySpec", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleOrgPolicyPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Immutable. The resource name of the Policy. Must be one of the following forms, where constraint_name is the name of the constraint which this Policy configures: * 'projects/{project_number}/policies/{constraint_name}' * 'folders/{folder_id}/policies/{constraint_name}' * 'organizations/{organization_id}/policies/{constraint_name}' For example, "projects/123/policies/compute.disableSerialPortAccess". Note: 'projects/{project_id}/policies/{constraint_name}' is also an acceptable name for API requests, but responses will return the name using the equivalent project number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#name GoogleOrgPolicyPolicy#name}
        :param parent: The parent of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#parent GoogleOrgPolicyPolicy#parent}
        :param dry_run_spec: dry_run_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#dry_run_spec GoogleOrgPolicyPolicy#dry_run_spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#id GoogleOrgPolicyPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#spec GoogleOrgPolicyPolicy#spec}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#timeouts GoogleOrgPolicyPolicy#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(dry_run_spec, dict):
            dry_run_spec = GoogleOrgPolicyPolicyDryRunSpec(**dry_run_spec)
        if isinstance(spec, dict):
            spec = GoogleOrgPolicyPolicySpec(**spec)
        if isinstance(timeouts, dict):
            timeouts = GoogleOrgPolicyPolicyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35024a10e3a8e9d3acbca50cc8c55ca2fa6ac5090802572308acb0f606124604)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument dry_run_spec", value=dry_run_spec, expected_type=type_hints["dry_run_spec"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument spec", value=spec, expected_type=type_hints["spec"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "parent": parent,
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
        if dry_run_spec is not None:
            self._values["dry_run_spec"] = dry_run_spec
        if id is not None:
            self._values["id"] = id
        if spec is not None:
            self._values["spec"] = spec
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
        '''Immutable.

        The resource name of the Policy. Must be one of the following forms, where constraint_name is the name of the constraint which this Policy configures: * 'projects/{project_number}/policies/{constraint_name}' * 'folders/{folder_id}/policies/{constraint_name}' * 'organizations/{organization_id}/policies/{constraint_name}' For example, "projects/123/policies/compute.disableSerialPortAccess". Note: 'projects/{project_id}/policies/{constraint_name}' is also an acceptable name for API requests, but responses will return the name using the equivalent project number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#name GoogleOrgPolicyPolicy#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parent(self) -> builtins.str:
        '''The parent of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#parent GoogleOrgPolicyPolicy#parent}
        '''
        result = self._values.get("parent")
        assert result is not None, "Required property 'parent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dry_run_spec(self) -> typing.Optional["GoogleOrgPolicyPolicyDryRunSpec"]:
        '''dry_run_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#dry_run_spec GoogleOrgPolicyPolicy#dry_run_spec}
        '''
        result = self._values.get("dry_run_spec")
        return typing.cast(typing.Optional["GoogleOrgPolicyPolicyDryRunSpec"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#id GoogleOrgPolicyPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spec(self) -> typing.Optional["GoogleOrgPolicyPolicySpec"]:
        '''spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#spec GoogleOrgPolicyPolicy#spec}
        '''
        result = self._values.get("spec")
        return typing.cast(typing.Optional["GoogleOrgPolicyPolicySpec"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleOrgPolicyPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#timeouts GoogleOrgPolicyPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleOrgPolicyPolicyTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOrgPolicyPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOrgPolicyPolicy.GoogleOrgPolicyPolicyDryRunSpec",
    jsii_struct_bases=[],
    name_mapping={
        "inherit_from_parent": "inheritFromParent",
        "reset": "reset",
        "rules": "rules",
    },
)
class GoogleOrgPolicyPolicyDryRunSpec:
    def __init__(
        self,
        *,
        inherit_from_parent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        reset: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOrgPolicyPolicyDryRunSpecRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param inherit_from_parent: Determines the inheritance behavior for this policy. If 'inherit_from_parent' is true, policy rules set higher up in the hierarchy (up to the closest root) are inherited and present in the effective policy. If it is false, then no rules are inherited, and this policy becomes the new root for evaluation. This field can be set only for policies which configure list constraints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#inherit_from_parent GoogleOrgPolicyPolicy#inherit_from_parent}
        :param reset: Ignores policies set above this resource and restores the 'constraint_default' enforcement behavior of the specific constraint at this resource. This field can be set in policies for either list or boolean constraints. If set, 'rules' must be empty and 'inherit_from_parent' must be set to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#reset GoogleOrgPolicyPolicy#reset}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#rules GoogleOrgPolicyPolicy#rules}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9ae33c3ddb9a789dc84216c4f9197c5021aa725de7956063ceae00823ace9b4)
            check_type(argname="argument inherit_from_parent", value=inherit_from_parent, expected_type=type_hints["inherit_from_parent"])
            check_type(argname="argument reset", value=reset, expected_type=type_hints["reset"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if inherit_from_parent is not None:
            self._values["inherit_from_parent"] = inherit_from_parent
        if reset is not None:
            self._values["reset"] = reset
        if rules is not None:
            self._values["rules"] = rules

    @builtins.property
    def inherit_from_parent(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines the inheritance behavior for this policy.

        If 'inherit_from_parent' is true, policy rules set higher up in the hierarchy (up to the closest root) are inherited and present in the effective policy. If it is false, then no rules are inherited, and this policy becomes the new root for evaluation. This field can be set only for policies which configure list constraints.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#inherit_from_parent GoogleOrgPolicyPolicy#inherit_from_parent}
        '''
        result = self._values.get("inherit_from_parent")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def reset(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Ignores policies set above this resource and restores the 'constraint_default' enforcement behavior of the specific constraint at this resource.

        This field can be set in policies for either list or boolean constraints. If set, 'rules' must be empty and 'inherit_from_parent' must be set to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#reset GoogleOrgPolicyPolicy#reset}
        '''
        result = self._values.get("reset")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def rules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOrgPolicyPolicyDryRunSpecRules"]]]:
        '''rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#rules GoogleOrgPolicyPolicy#rules}
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOrgPolicyPolicyDryRunSpecRules"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOrgPolicyPolicyDryRunSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOrgPolicyPolicyDryRunSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOrgPolicyPolicy.GoogleOrgPolicyPolicyDryRunSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__444ee0d70a83697c6154d3cb94e245ef5b6424b4f904d016b608227a0a167c2a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRules")
    def put_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOrgPolicyPolicyDryRunSpecRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12136a36af2b4b0823d9ad785d44545753c686cd2b3053f48140359051a0b704)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRules", [value]))

    @jsii.member(jsii_name="resetInheritFromParent")
    def reset_inherit_from_parent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInheritFromParent", []))

    @jsii.member(jsii_name="resetReset")
    def reset_reset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReset", []))

    @jsii.member(jsii_name="resetRules")
    def reset_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRules", []))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> "GoogleOrgPolicyPolicyDryRunSpecRulesList":
        return typing.cast("GoogleOrgPolicyPolicyDryRunSpecRulesList", jsii.get(self, "rules"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="inheritFromParentInput")
    def inherit_from_parent_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "inheritFromParentInput"))

    @builtins.property
    @jsii.member(jsii_name="resetInput")
    def reset_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "resetInput"))

    @builtins.property
    @jsii.member(jsii_name="rulesInput")
    def rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOrgPolicyPolicyDryRunSpecRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOrgPolicyPolicyDryRunSpecRules"]]], jsii.get(self, "rulesInput"))

    @builtins.property
    @jsii.member(jsii_name="inheritFromParent")
    def inherit_from_parent(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "inheritFromParent"))

    @inherit_from_parent.setter
    def inherit_from_parent(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48dd4fb7c5cdccb594ae895661995749b10a29728e2d1bb6afdf5d89bd741de1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inheritFromParent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reset")
    def reset(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "reset"))

    @reset.setter
    def reset(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e16f1ed62afaa6b7101e72cf016592f9289a2a9e59194cac32820f12ce276a9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleOrgPolicyPolicyDryRunSpec]:
        return typing.cast(typing.Optional[GoogleOrgPolicyPolicyDryRunSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOrgPolicyPolicyDryRunSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae912335eeb630a9a0699426786115d23eda50525b24fa0ac2dd5367294e8847)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOrgPolicyPolicy.GoogleOrgPolicyPolicyDryRunSpecRules",
    jsii_struct_bases=[],
    name_mapping={
        "allow_all": "allowAll",
        "condition": "condition",
        "deny_all": "denyAll",
        "enforce": "enforce",
        "parameters": "parameters",
        "values": "values",
    },
)
class GoogleOrgPolicyPolicyDryRunSpecRules:
    def __init__(
        self,
        *,
        allow_all: typing.Optional[builtins.str] = None,
        condition: typing.Optional[typing.Union["GoogleOrgPolicyPolicyDryRunSpecRulesCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        deny_all: typing.Optional[builtins.str] = None,
        enforce: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Union["GoogleOrgPolicyPolicyDryRunSpecRulesValues", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_all: Setting this to '"TRUE"' means that all values are allowed. This field can be set only in Policies for list constraints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#allow_all GoogleOrgPolicyPolicy#allow_all}
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#condition GoogleOrgPolicyPolicy#condition}
        :param deny_all: Setting this to '"TRUE"' means that all values are denied. This field can be set only in Policies for list constraints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#deny_all GoogleOrgPolicyPolicy#deny_all}
        :param enforce: If '"TRUE"', then the 'Policy' is enforced. If '"FALSE"', then any configuration is acceptable. This field can be set only in Policies for boolean constraints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#enforce GoogleOrgPolicyPolicy#enforce}
        :param parameters: Optional. Required for Managed Constraints if parameters defined in constraints. Pass parameter values when policy enforcement is enabled. Ensure that parameter value types match those defined in the constraint definition. For example: { "allowedLocations" : ["us-east1", "us-west1"], "allowAll" : true } Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#parameters GoogleOrgPolicyPolicy#parameters}
        :param values: values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#values GoogleOrgPolicyPolicy#values}
        '''
        if isinstance(condition, dict):
            condition = GoogleOrgPolicyPolicyDryRunSpecRulesCondition(**condition)
        if isinstance(values, dict):
            values = GoogleOrgPolicyPolicyDryRunSpecRulesValues(**values)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf21511e5eda3ca2880d5f69e836f796d5c05d325bd31d882cb48714fcac9e15)
            check_type(argname="argument allow_all", value=allow_all, expected_type=type_hints["allow_all"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument deny_all", value=deny_all, expected_type=type_hints["deny_all"])
            check_type(argname="argument enforce", value=enforce, expected_type=type_hints["enforce"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_all is not None:
            self._values["allow_all"] = allow_all
        if condition is not None:
            self._values["condition"] = condition
        if deny_all is not None:
            self._values["deny_all"] = deny_all
        if enforce is not None:
            self._values["enforce"] = enforce
        if parameters is not None:
            self._values["parameters"] = parameters
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def allow_all(self) -> typing.Optional[builtins.str]:
        '''Setting this to '"TRUE"' means that all values are allowed.

        This field can be set only in Policies for list constraints.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#allow_all GoogleOrgPolicyPolicy#allow_all}
        '''
        result = self._values.get("allow_all")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def condition(
        self,
    ) -> typing.Optional["GoogleOrgPolicyPolicyDryRunSpecRulesCondition"]:
        '''condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#condition GoogleOrgPolicyPolicy#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional["GoogleOrgPolicyPolicyDryRunSpecRulesCondition"], result)

    @builtins.property
    def deny_all(self) -> typing.Optional[builtins.str]:
        '''Setting this to '"TRUE"' means that all values are denied.

        This field can be set only in Policies for list constraints.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#deny_all GoogleOrgPolicyPolicy#deny_all}
        '''
        result = self._values.get("deny_all")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enforce(self) -> typing.Optional[builtins.str]:
        '''If '"TRUE"', then the 'Policy' is enforced.

        If '"FALSE"', then any configuration is acceptable. This field can be set only in Policies for boolean constraints.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#enforce GoogleOrgPolicyPolicy#enforce}
        '''
        result = self._values.get("enforce")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Required for Managed Constraints if parameters defined in constraints. Pass parameter values when policy enforcement is enabled. Ensure that parameter value types match those defined in the constraint definition. For example: { "allowedLocations" : ["us-east1", "us-west1"], "allowAll" : true }

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#parameters GoogleOrgPolicyPolicy#parameters}
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional["GoogleOrgPolicyPolicyDryRunSpecRulesValues"]:
        '''values block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#values GoogleOrgPolicyPolicy#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional["GoogleOrgPolicyPolicyDryRunSpecRulesValues"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOrgPolicyPolicyDryRunSpecRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOrgPolicyPolicy.GoogleOrgPolicyPolicyDryRunSpecRulesCondition",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "expression": "expression",
        "location": "location",
        "title": "title",
    },
)
class GoogleOrgPolicyPolicyDryRunSpecRulesCondition:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        expression: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param description: Optional. Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#description GoogleOrgPolicyPolicy#description}
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#expression GoogleOrgPolicyPolicy#expression}
        :param location: Optional. String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#location GoogleOrgPolicyPolicy#location}
        :param title: Optional. Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#title GoogleOrgPolicyPolicy#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0413f74ba647f0f3995fa0ffec067f41cd79c6f67a367e9786e42389c22228e5)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if expression is not None:
            self._values["expression"] = expression
        if location is not None:
            self._values["location"] = location
        if title is not None:
            self._values["title"] = title

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#description GoogleOrgPolicyPolicy#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expression(self) -> typing.Optional[builtins.str]:
        '''Textual representation of an expression in Common Expression Language syntax.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#expression GoogleOrgPolicyPolicy#expression}
        '''
        result = self._values.get("expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''Optional.

        String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#location GoogleOrgPolicyPolicy#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#title GoogleOrgPolicyPolicy#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOrgPolicyPolicyDryRunSpecRulesCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOrgPolicyPolicyDryRunSpecRulesConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOrgPolicyPolicy.GoogleOrgPolicyPolicyDryRunSpecRulesConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__769ca56bdaf23e57712a242d8d1d7b8f53ef222d80f8e3d494fda62afc755305)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetExpression")
    def reset_expression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpression", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__f7c2bce735c0edde2d6822d60f7b748c03bc06b1e8cb51a06c9a0597fed523a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8ad04837acdedaa527eb6a506c5feac4a1429d2f63b3cca2c63e271e104e3cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03546b83a821aaa84ddcaf86e926e8b491e6ce826f5ef11e168cca72a8204a6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e900f8c4efd97b709cb59bf9fea9521b0d9e071648590917798f8e3d2fb862eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOrgPolicyPolicyDryRunSpecRulesCondition]:
        return typing.cast(typing.Optional[GoogleOrgPolicyPolicyDryRunSpecRulesCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOrgPolicyPolicyDryRunSpecRulesCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fcaa782736c4c40501b5e22b991c339ec86fd84b85976a667aade92c3067e39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOrgPolicyPolicyDryRunSpecRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOrgPolicyPolicy.GoogleOrgPolicyPolicyDryRunSpecRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__75ea892bc12c68580dd055d78b8ba25d609fa639711fc67d386e8742d96bcbb5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOrgPolicyPolicyDryRunSpecRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__568eea8a121ee7bc217e72bc2fc7e519b091ddd6a863a7764c9eb601cf16217c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOrgPolicyPolicyDryRunSpecRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f944c39db616c7b323213c6b5bec0478240945791f4379cecbfb1f93a271291)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f18141a37f5c55b95ec94092a3ee7d31348b973def9534e63771347f587ebd02)
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
            type_hints = typing.get_type_hints(_typecheckingstub__978c0b88b5e5f53a68852aff17fa2dbc9c82cc2caf2d7e5d0dbb31c3efe0e8d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOrgPolicyPolicyDryRunSpecRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOrgPolicyPolicyDryRunSpecRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOrgPolicyPolicyDryRunSpecRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22d89de079e92b7b9bb281c0581fde036671c0ef39c5afcbba0b4fb291b8da33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOrgPolicyPolicyDryRunSpecRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOrgPolicyPolicy.GoogleOrgPolicyPolicyDryRunSpecRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__13b43baeae701ead2a5a9a2a32c0e4256286ece4e0e47d2ced6dbe73b5d28465)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCondition")
    def put_condition(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        expression: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param description: Optional. Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#description GoogleOrgPolicyPolicy#description}
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#expression GoogleOrgPolicyPolicy#expression}
        :param location: Optional. String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#location GoogleOrgPolicyPolicy#location}
        :param title: Optional. Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#title GoogleOrgPolicyPolicy#title}
        '''
        value = GoogleOrgPolicyPolicyDryRunSpecRulesCondition(
            description=description,
            expression=expression,
            location=location,
            title=title,
        )

        return typing.cast(None, jsii.invoke(self, "putCondition", [value]))

    @jsii.member(jsii_name="putValues")
    def put_values(
        self,
        *,
        allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        denied_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_values: List of values allowed at this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#allowed_values GoogleOrgPolicyPolicy#allowed_values}
        :param denied_values: List of values denied at this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#denied_values GoogleOrgPolicyPolicy#denied_values}
        '''
        value = GoogleOrgPolicyPolicyDryRunSpecRulesValues(
            allowed_values=allowed_values, denied_values=denied_values
        )

        return typing.cast(None, jsii.invoke(self, "putValues", [value]))

    @jsii.member(jsii_name="resetAllowAll")
    def reset_allow_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowAll", []))

    @jsii.member(jsii_name="resetCondition")
    def reset_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCondition", []))

    @jsii.member(jsii_name="resetDenyAll")
    def reset_deny_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDenyAll", []))

    @jsii.member(jsii_name="resetEnforce")
    def reset_enforce(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforce", []))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> GoogleOrgPolicyPolicyDryRunSpecRulesConditionOutputReference:
        return typing.cast(GoogleOrgPolicyPolicyDryRunSpecRulesConditionOutputReference, jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> "GoogleOrgPolicyPolicyDryRunSpecRulesValuesOutputReference":
        return typing.cast("GoogleOrgPolicyPolicyDryRunSpecRulesValuesOutputReference", jsii.get(self, "values"))

    @builtins.property
    @jsii.member(jsii_name="allowAllInput")
    def allow_all_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "allowAllInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(
        self,
    ) -> typing.Optional[GoogleOrgPolicyPolicyDryRunSpecRulesCondition]:
        return typing.cast(typing.Optional[GoogleOrgPolicyPolicyDryRunSpecRulesCondition], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="denyAllInput")
    def deny_all_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "denyAllInput"))

    @builtins.property
    @jsii.member(jsii_name="enforceInput")
    def enforce_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enforceInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(
        self,
    ) -> typing.Optional["GoogleOrgPolicyPolicyDryRunSpecRulesValues"]:
        return typing.cast(typing.Optional["GoogleOrgPolicyPolicyDryRunSpecRulesValues"], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowAll")
    def allow_all(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "allowAll"))

    @allow_all.setter
    def allow_all(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66ff5fcd07b0b1706b9a332ccb8e376e1a4d44eb51e860ca6561381d66c0ba29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="denyAll")
    def deny_all(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "denyAll"))

    @deny_all.setter
    def deny_all(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1af588d33945551a7e3bf153c67ad1358f24e2f8c010103a7d9ce0bba151fbda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "denyAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforce")
    def enforce(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enforce"))

    @enforce.setter
    def enforce(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4c5fdeb8be5062d5267660627bf8dc44b43aec138929288bc802d76a3778b55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforce", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea9184a4f2bdba15c7bf41b158837bf76e3e91fd5acd8e79a4dcd9512e04e00d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOrgPolicyPolicyDryRunSpecRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOrgPolicyPolicyDryRunSpecRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOrgPolicyPolicyDryRunSpecRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd48bdc3824358dbfa85551916d425442afbd61610746efdf9215425ee496c0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOrgPolicyPolicy.GoogleOrgPolicyPolicyDryRunSpecRulesValues",
    jsii_struct_bases=[],
    name_mapping={"allowed_values": "allowedValues", "denied_values": "deniedValues"},
)
class GoogleOrgPolicyPolicyDryRunSpecRulesValues:
    def __init__(
        self,
        *,
        allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        denied_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_values: List of values allowed at this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#allowed_values GoogleOrgPolicyPolicy#allowed_values}
        :param denied_values: List of values denied at this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#denied_values GoogleOrgPolicyPolicy#denied_values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bfe132586289788c59d6d89922cba5657fdbfd5e472d575b4893263acb536a5)
            check_type(argname="argument allowed_values", value=allowed_values, expected_type=type_hints["allowed_values"])
            check_type(argname="argument denied_values", value=denied_values, expected_type=type_hints["denied_values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_values is not None:
            self._values["allowed_values"] = allowed_values
        if denied_values is not None:
            self._values["denied_values"] = denied_values

    @builtins.property
    def allowed_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of values allowed at this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#allowed_values GoogleOrgPolicyPolicy#allowed_values}
        '''
        result = self._values.get("allowed_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def denied_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of values denied at this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#denied_values GoogleOrgPolicyPolicy#denied_values}
        '''
        result = self._values.get("denied_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOrgPolicyPolicyDryRunSpecRulesValues(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOrgPolicyPolicyDryRunSpecRulesValuesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOrgPolicyPolicy.GoogleOrgPolicyPolicyDryRunSpecRulesValuesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be3641eb85763cd4f2287634d25f38c5c98e47a7f55ff13a1d860ffaeb7d407a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedValues")
    def reset_allowed_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedValues", []))

    @jsii.member(jsii_name="resetDeniedValues")
    def reset_denied_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeniedValues", []))

    @builtins.property
    @jsii.member(jsii_name="allowedValuesInput")
    def allowed_values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="deniedValuesInput")
    def denied_values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "deniedValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedValues")
    def allowed_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedValues"))

    @allowed_values.setter
    def allowed_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc99ec16b1a14efcc5ebd62df3a408d61f822b7da42f78c4746cb6bed104185c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deniedValues")
    def denied_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "deniedValues"))

    @denied_values.setter
    def denied_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__938c06554a8a118c336834457354e6e0a07a6e389ab82d1e85cc498ddaeb6231)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deniedValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOrgPolicyPolicyDryRunSpecRulesValues]:
        return typing.cast(typing.Optional[GoogleOrgPolicyPolicyDryRunSpecRulesValues], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOrgPolicyPolicyDryRunSpecRulesValues],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a067605524d356f4b42bec41f58867211a6bc02ee00ea27ff9559f5620cf911)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOrgPolicyPolicy.GoogleOrgPolicyPolicySpec",
    jsii_struct_bases=[],
    name_mapping={
        "inherit_from_parent": "inheritFromParent",
        "reset": "reset",
        "rules": "rules",
    },
)
class GoogleOrgPolicyPolicySpec:
    def __init__(
        self,
        *,
        inherit_from_parent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        reset: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOrgPolicyPolicySpecRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param inherit_from_parent: Determines the inheritance behavior for this 'Policy'. If 'inherit_from_parent' is true, PolicyRules set higher up in the hierarchy (up to the closest root) are inherited and present in the effective policy. If it is false, then no rules are inherited, and this Policy becomes the new root for evaluation. This field can be set only for Policies which configure list constraints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#inherit_from_parent GoogleOrgPolicyPolicy#inherit_from_parent}
        :param reset: Ignores policies set above this resource and restores the 'constraint_default' enforcement behavior of the specific 'Constraint' at this resource. This field can be set in policies for either list or boolean constraints. If set, 'rules' must be empty and 'inherit_from_parent' must be set to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#reset GoogleOrgPolicyPolicy#reset}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#rules GoogleOrgPolicyPolicy#rules}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c904a253e5f1e46ade1397cb042e92b432b0a80210256d3f4e095c913514cb38)
            check_type(argname="argument inherit_from_parent", value=inherit_from_parent, expected_type=type_hints["inherit_from_parent"])
            check_type(argname="argument reset", value=reset, expected_type=type_hints["reset"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if inherit_from_parent is not None:
            self._values["inherit_from_parent"] = inherit_from_parent
        if reset is not None:
            self._values["reset"] = reset
        if rules is not None:
            self._values["rules"] = rules

    @builtins.property
    def inherit_from_parent(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines the inheritance behavior for this 'Policy'.

        If 'inherit_from_parent' is true, PolicyRules set higher up in the hierarchy (up to the closest root) are inherited and present in the effective policy. If it is false, then no rules are inherited, and this Policy becomes the new root for evaluation. This field can be set only for Policies which configure list constraints.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#inherit_from_parent GoogleOrgPolicyPolicy#inherit_from_parent}
        '''
        result = self._values.get("inherit_from_parent")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def reset(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Ignores policies set above this resource and restores the 'constraint_default' enforcement behavior of the specific 'Constraint' at this resource.

        This field can be set in policies for either list or boolean constraints. If set, 'rules' must be empty and 'inherit_from_parent' must be set to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#reset GoogleOrgPolicyPolicy#reset}
        '''
        result = self._values.get("reset")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def rules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOrgPolicyPolicySpecRules"]]]:
        '''rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#rules GoogleOrgPolicyPolicy#rules}
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOrgPolicyPolicySpecRules"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOrgPolicyPolicySpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOrgPolicyPolicySpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOrgPolicyPolicy.GoogleOrgPolicyPolicySpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b5ffdb1514c521b58541ca3c80dc04af9eeffa41d551c37efd11987dae4b230)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRules")
    def put_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOrgPolicyPolicySpecRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__015f1222d530805b7fe1936570dd1c710e152d8b355f0170bc43e3e919bf0f36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRules", [value]))

    @jsii.member(jsii_name="resetInheritFromParent")
    def reset_inherit_from_parent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInheritFromParent", []))

    @jsii.member(jsii_name="resetReset")
    def reset_reset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReset", []))

    @jsii.member(jsii_name="resetRules")
    def reset_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRules", []))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> "GoogleOrgPolicyPolicySpecRulesList":
        return typing.cast("GoogleOrgPolicyPolicySpecRulesList", jsii.get(self, "rules"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="inheritFromParentInput")
    def inherit_from_parent_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "inheritFromParentInput"))

    @builtins.property
    @jsii.member(jsii_name="resetInput")
    def reset_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "resetInput"))

    @builtins.property
    @jsii.member(jsii_name="rulesInput")
    def rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOrgPolicyPolicySpecRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOrgPolicyPolicySpecRules"]]], jsii.get(self, "rulesInput"))

    @builtins.property
    @jsii.member(jsii_name="inheritFromParent")
    def inherit_from_parent(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "inheritFromParent"))

    @inherit_from_parent.setter
    def inherit_from_parent(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7b47e1805a6aee471f9c1c2a81e0ea96c29a05ca9c307f56c2720260874acc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inheritFromParent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reset")
    def reset(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "reset"))

    @reset.setter
    def reset(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e50448cc1b35a527b7db8b7495799f44edc77e4543750ba3c0f777679b94f4f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleOrgPolicyPolicySpec]:
        return typing.cast(typing.Optional[GoogleOrgPolicyPolicySpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[GoogleOrgPolicyPolicySpec]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfe92539b4823ab3a3be25d0a3589bee45ba385056b65ece376ab19527ee33f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOrgPolicyPolicy.GoogleOrgPolicyPolicySpecRules",
    jsii_struct_bases=[],
    name_mapping={
        "allow_all": "allowAll",
        "condition": "condition",
        "deny_all": "denyAll",
        "enforce": "enforce",
        "parameters": "parameters",
        "values": "values",
    },
)
class GoogleOrgPolicyPolicySpecRules:
    def __init__(
        self,
        *,
        allow_all: typing.Optional[builtins.str] = None,
        condition: typing.Optional[typing.Union["GoogleOrgPolicyPolicySpecRulesCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        deny_all: typing.Optional[builtins.str] = None,
        enforce: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Union["GoogleOrgPolicyPolicySpecRulesValues", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_all: Setting this to '"TRUE"' means that all values are allowed. This field can be set only in Policies for list constraints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#allow_all GoogleOrgPolicyPolicy#allow_all}
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#condition GoogleOrgPolicyPolicy#condition}
        :param deny_all: Setting this to '"TRUE"' means that all values are denied. This field can be set only in Policies for list constraints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#deny_all GoogleOrgPolicyPolicy#deny_all}
        :param enforce: If '"TRUE"', then the 'Policy' is enforced. If '"FALSE"', then any configuration is acceptable. This field can be set only in Policies for boolean constraints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#enforce GoogleOrgPolicyPolicy#enforce}
        :param parameters: Optional. Required for Managed Constraints if parameters defined in constraints. Pass parameter values when policy enforcement is enabled. Ensure that parameter value types match those defined in the constraint definition. For example: { "allowedLocations" : ["us-east1", "us-west1"], "allowAll" : true } Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#parameters GoogleOrgPolicyPolicy#parameters}
        :param values: values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#values GoogleOrgPolicyPolicy#values}
        '''
        if isinstance(condition, dict):
            condition = GoogleOrgPolicyPolicySpecRulesCondition(**condition)
        if isinstance(values, dict):
            values = GoogleOrgPolicyPolicySpecRulesValues(**values)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fe2113a0b682ed3d0bc589eb1f3c77d7a5f1cb701f05aa110eb98f6cb804ea3)
            check_type(argname="argument allow_all", value=allow_all, expected_type=type_hints["allow_all"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument deny_all", value=deny_all, expected_type=type_hints["deny_all"])
            check_type(argname="argument enforce", value=enforce, expected_type=type_hints["enforce"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_all is not None:
            self._values["allow_all"] = allow_all
        if condition is not None:
            self._values["condition"] = condition
        if deny_all is not None:
            self._values["deny_all"] = deny_all
        if enforce is not None:
            self._values["enforce"] = enforce
        if parameters is not None:
            self._values["parameters"] = parameters
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def allow_all(self) -> typing.Optional[builtins.str]:
        '''Setting this to '"TRUE"' means that all values are allowed.

        This field can be set only in Policies for list constraints.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#allow_all GoogleOrgPolicyPolicy#allow_all}
        '''
        result = self._values.get("allow_all")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def condition(self) -> typing.Optional["GoogleOrgPolicyPolicySpecRulesCondition"]:
        '''condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#condition GoogleOrgPolicyPolicy#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional["GoogleOrgPolicyPolicySpecRulesCondition"], result)

    @builtins.property
    def deny_all(self) -> typing.Optional[builtins.str]:
        '''Setting this to '"TRUE"' means that all values are denied.

        This field can be set only in Policies for list constraints.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#deny_all GoogleOrgPolicyPolicy#deny_all}
        '''
        result = self._values.get("deny_all")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enforce(self) -> typing.Optional[builtins.str]:
        '''If '"TRUE"', then the 'Policy' is enforced.

        If '"FALSE"', then any configuration is acceptable. This field can be set only in Policies for boolean constraints.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#enforce GoogleOrgPolicyPolicy#enforce}
        '''
        result = self._values.get("enforce")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Required for Managed Constraints if parameters defined in constraints. Pass parameter values when policy enforcement is enabled. Ensure that parameter value types match those defined in the constraint definition. For example: { "allowedLocations" : ["us-east1", "us-west1"], "allowAll" : true }

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#parameters GoogleOrgPolicyPolicy#parameters}
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional["GoogleOrgPolicyPolicySpecRulesValues"]:
        '''values block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#values GoogleOrgPolicyPolicy#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional["GoogleOrgPolicyPolicySpecRulesValues"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOrgPolicyPolicySpecRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOrgPolicyPolicy.GoogleOrgPolicyPolicySpecRulesCondition",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "expression": "expression",
        "location": "location",
        "title": "title",
    },
)
class GoogleOrgPolicyPolicySpecRulesCondition:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        expression: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param description: Optional. Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#description GoogleOrgPolicyPolicy#description}
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#expression GoogleOrgPolicyPolicy#expression}
        :param location: Optional. String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#location GoogleOrgPolicyPolicy#location}
        :param title: Optional. Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#title GoogleOrgPolicyPolicy#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e6ce8600430530faf0eb1d7ad9b5c8afe688eed18ac53693c7353d14ec8c039)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if expression is not None:
            self._values["expression"] = expression
        if location is not None:
            self._values["location"] = location
        if title is not None:
            self._values["title"] = title

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#description GoogleOrgPolicyPolicy#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expression(self) -> typing.Optional[builtins.str]:
        '''Textual representation of an expression in Common Expression Language syntax.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#expression GoogleOrgPolicyPolicy#expression}
        '''
        result = self._values.get("expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''Optional.

        String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#location GoogleOrgPolicyPolicy#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#title GoogleOrgPolicyPolicy#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOrgPolicyPolicySpecRulesCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOrgPolicyPolicySpecRulesConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOrgPolicyPolicy.GoogleOrgPolicyPolicySpecRulesConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__14d7b3de31f6ddbd265714039be227ae23f34d161ef83d3a4a1aa2809f443695)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetExpression")
    def reset_expression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpression", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__7de7562af852666ef3c56848a6d92b42e99e5b14211f3cf37c10aae329619828)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3c5d4f3f301b673531073dd6890eb0b3ceea59de45e556d55a3b9a09ebb2da4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec55e1afa5594c276a19d8259d60e45a7439bd136faffb1de1197eb9eac356c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__545d2c8db6c479da895fab5384f4d5a013a09547683c58eec86ddcb5fa114216)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOrgPolicyPolicySpecRulesCondition]:
        return typing.cast(typing.Optional[GoogleOrgPolicyPolicySpecRulesCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOrgPolicyPolicySpecRulesCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f610afe8f547a254cfeaaec82321bb3d2bb4915a7fed963cfda9210dc11cf6c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOrgPolicyPolicySpecRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOrgPolicyPolicy.GoogleOrgPolicyPolicySpecRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5170ba2fa8d99090cc21910ce6a57e49661918c7b1a3157772f33527ba61a6c7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOrgPolicyPolicySpecRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c1491050d809cc0973d3a1f772fdb73634bc9d646b876d8aa96368c3784b08d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOrgPolicyPolicySpecRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50adeb98eada068b51f6aa13d267f3fd9baf6ae09849c0862d9a5d08b10a131d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d17b4777d10a67e6947dfdacac80d8ef3203be84c285c942e98eaabc97445c29)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebe32159dd4df247beb9db64a1aa5e4909b2264e252f8418f1909f5b7613165c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOrgPolicyPolicySpecRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOrgPolicyPolicySpecRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOrgPolicyPolicySpecRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb96e04ae4ad512e423070cf566034ee00de6cb7a08e27e9ebeeb9f14d7121ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOrgPolicyPolicySpecRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOrgPolicyPolicy.GoogleOrgPolicyPolicySpecRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0c7665d498bc6af49f6682f10ea0c28173e654bd049b1299222a0f3707bb027)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCondition")
    def put_condition(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        expression: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param description: Optional. Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#description GoogleOrgPolicyPolicy#description}
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#expression GoogleOrgPolicyPolicy#expression}
        :param location: Optional. String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#location GoogleOrgPolicyPolicy#location}
        :param title: Optional. Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#title GoogleOrgPolicyPolicy#title}
        '''
        value = GoogleOrgPolicyPolicySpecRulesCondition(
            description=description,
            expression=expression,
            location=location,
            title=title,
        )

        return typing.cast(None, jsii.invoke(self, "putCondition", [value]))

    @jsii.member(jsii_name="putValues")
    def put_values(
        self,
        *,
        allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        denied_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_values: List of values allowed at this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#allowed_values GoogleOrgPolicyPolicy#allowed_values}
        :param denied_values: List of values denied at this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#denied_values GoogleOrgPolicyPolicy#denied_values}
        '''
        value = GoogleOrgPolicyPolicySpecRulesValues(
            allowed_values=allowed_values, denied_values=denied_values
        )

        return typing.cast(None, jsii.invoke(self, "putValues", [value]))

    @jsii.member(jsii_name="resetAllowAll")
    def reset_allow_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowAll", []))

    @jsii.member(jsii_name="resetCondition")
    def reset_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCondition", []))

    @jsii.member(jsii_name="resetDenyAll")
    def reset_deny_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDenyAll", []))

    @jsii.member(jsii_name="resetEnforce")
    def reset_enforce(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforce", []))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> GoogleOrgPolicyPolicySpecRulesConditionOutputReference:
        return typing.cast(GoogleOrgPolicyPolicySpecRulesConditionOutputReference, jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> "GoogleOrgPolicyPolicySpecRulesValuesOutputReference":
        return typing.cast("GoogleOrgPolicyPolicySpecRulesValuesOutputReference", jsii.get(self, "values"))

    @builtins.property
    @jsii.member(jsii_name="allowAllInput")
    def allow_all_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "allowAllInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(
        self,
    ) -> typing.Optional[GoogleOrgPolicyPolicySpecRulesCondition]:
        return typing.cast(typing.Optional[GoogleOrgPolicyPolicySpecRulesCondition], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="denyAllInput")
    def deny_all_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "denyAllInput"))

    @builtins.property
    @jsii.member(jsii_name="enforceInput")
    def enforce_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enforceInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional["GoogleOrgPolicyPolicySpecRulesValues"]:
        return typing.cast(typing.Optional["GoogleOrgPolicyPolicySpecRulesValues"], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowAll")
    def allow_all(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "allowAll"))

    @allow_all.setter
    def allow_all(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c65dd863afa9c1d345b18038e33f5b0106325f096920df57a9e1745896729bfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="denyAll")
    def deny_all(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "denyAll"))

    @deny_all.setter
    def deny_all(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c16296ce1a3cfcf26202418306d6ddd51b04f421536913fc2e5368886a5ce55e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "denyAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforce")
    def enforce(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enforce"))

    @enforce.setter
    def enforce(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0576ffb813ebaee215e301c47c83982fa1d4191251650ceb160f4b198d1db979)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforce", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb77241a20da3be778fe070037149dc40ee362e722287d67c347fca483d2b3f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOrgPolicyPolicySpecRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOrgPolicyPolicySpecRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOrgPolicyPolicySpecRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d9d2afc7ccf91ab9ff49cb348234c146ecd8814e348adb2a6ab97c4f4447e0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOrgPolicyPolicy.GoogleOrgPolicyPolicySpecRulesValues",
    jsii_struct_bases=[],
    name_mapping={"allowed_values": "allowedValues", "denied_values": "deniedValues"},
)
class GoogleOrgPolicyPolicySpecRulesValues:
    def __init__(
        self,
        *,
        allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        denied_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_values: List of values allowed at this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#allowed_values GoogleOrgPolicyPolicy#allowed_values}
        :param denied_values: List of values denied at this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#denied_values GoogleOrgPolicyPolicy#denied_values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee688c720e517a66e1e8c5f2ea676d12accbe8813d035d949704c0a87818d58f)
            check_type(argname="argument allowed_values", value=allowed_values, expected_type=type_hints["allowed_values"])
            check_type(argname="argument denied_values", value=denied_values, expected_type=type_hints["denied_values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_values is not None:
            self._values["allowed_values"] = allowed_values
        if denied_values is not None:
            self._values["denied_values"] = denied_values

    @builtins.property
    def allowed_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of values allowed at this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#allowed_values GoogleOrgPolicyPolicy#allowed_values}
        '''
        result = self._values.get("allowed_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def denied_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of values denied at this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#denied_values GoogleOrgPolicyPolicy#denied_values}
        '''
        result = self._values.get("denied_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOrgPolicyPolicySpecRulesValues(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOrgPolicyPolicySpecRulesValuesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOrgPolicyPolicy.GoogleOrgPolicyPolicySpecRulesValuesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__199b28d2fc9b246f0a85ca43eb3c1d36844ab688dfee2fbca28e1a12e560d7a0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedValues")
    def reset_allowed_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedValues", []))

    @jsii.member(jsii_name="resetDeniedValues")
    def reset_denied_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeniedValues", []))

    @builtins.property
    @jsii.member(jsii_name="allowedValuesInput")
    def allowed_values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="deniedValuesInput")
    def denied_values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "deniedValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedValues")
    def allowed_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedValues"))

    @allowed_values.setter
    def allowed_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c00a1bcf6d61aea0bec8f89d5d3ebeab1a0a330a89f3bf6f8622cddaab255745)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deniedValues")
    def denied_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "deniedValues"))

    @denied_values.setter
    def denied_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e08afc919cb24a55c9469154be00c398064f612a050f636a94ab05ade519070c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deniedValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleOrgPolicyPolicySpecRulesValues]:
        return typing.cast(typing.Optional[GoogleOrgPolicyPolicySpecRulesValues], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOrgPolicyPolicySpecRulesValues],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__109243844ee4eb8d0eb1a9941747aa0b3022b75198a7c72fa16dbeb93e9de332)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOrgPolicyPolicy.GoogleOrgPolicyPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleOrgPolicyPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#create GoogleOrgPolicyPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#delete GoogleOrgPolicyPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#update GoogleOrgPolicyPolicy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a11f5008a53e1546ee646e55c33fc9ad3801c5b6c974f8fc4a0d0fa012aa6ac4)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#create GoogleOrgPolicyPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#delete GoogleOrgPolicyPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_org_policy_policy#update GoogleOrgPolicyPolicy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOrgPolicyPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOrgPolicyPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOrgPolicyPolicy.GoogleOrgPolicyPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2d0e222eb76dafa163dcfe09e09a994e7e5a1cc9f89163c8c7c98cc5f9af170)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcaaaa01f00d6296b17ea0aca745e2835b205c3b6bf9f4c8bb1338b5fe9cf6f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1816d16ed38eb15c17b28a956fdc205cd8199c1f1061ecd594e11da72d551355)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__228834498dc14c26abb5e0b51c1c9e8b75ec6449c6a1237b76e8a8f73fd2a1f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOrgPolicyPolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOrgPolicyPolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOrgPolicyPolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3d5d6b28a3ab6da4f47058ffd25da2e293d320a3b26771efe4e6b7c0b3b7d3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleOrgPolicyPolicy",
    "GoogleOrgPolicyPolicyConfig",
    "GoogleOrgPolicyPolicyDryRunSpec",
    "GoogleOrgPolicyPolicyDryRunSpecOutputReference",
    "GoogleOrgPolicyPolicyDryRunSpecRules",
    "GoogleOrgPolicyPolicyDryRunSpecRulesCondition",
    "GoogleOrgPolicyPolicyDryRunSpecRulesConditionOutputReference",
    "GoogleOrgPolicyPolicyDryRunSpecRulesList",
    "GoogleOrgPolicyPolicyDryRunSpecRulesOutputReference",
    "GoogleOrgPolicyPolicyDryRunSpecRulesValues",
    "GoogleOrgPolicyPolicyDryRunSpecRulesValuesOutputReference",
    "GoogleOrgPolicyPolicySpec",
    "GoogleOrgPolicyPolicySpecOutputReference",
    "GoogleOrgPolicyPolicySpecRules",
    "GoogleOrgPolicyPolicySpecRulesCondition",
    "GoogleOrgPolicyPolicySpecRulesConditionOutputReference",
    "GoogleOrgPolicyPolicySpecRulesList",
    "GoogleOrgPolicyPolicySpecRulesOutputReference",
    "GoogleOrgPolicyPolicySpecRulesValues",
    "GoogleOrgPolicyPolicySpecRulesValuesOutputReference",
    "GoogleOrgPolicyPolicyTimeouts",
    "GoogleOrgPolicyPolicyTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__4e8a4ffd4accd1a6036c9980d0afa4ccf8a3cc4a9d7a2eaa87a976e1f3a4dd49(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    parent: builtins.str,
    dry_run_spec: typing.Optional[typing.Union[GoogleOrgPolicyPolicyDryRunSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    spec: typing.Optional[typing.Union[GoogleOrgPolicyPolicySpec, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleOrgPolicyPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__118a6023f15a27663098cd846959c688e78ca2fbc61c7dd22e3fa9e05164424a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b8809e127e5f908bc9d8b809ec184e6b9971e01b2900c9a5a0bccd36820b46e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad5300fd2514a8578f316b324ae6ca54c23ce71ee22caf1606b13a79fa26ecd9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ea75a4ee4445012862a7aed9ffb2a8d9dc09378a73130aeb85fbea274f593e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35024a10e3a8e9d3acbca50cc8c55ca2fa6ac5090802572308acb0f606124604(
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
    dry_run_spec: typing.Optional[typing.Union[GoogleOrgPolicyPolicyDryRunSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    spec: typing.Optional[typing.Union[GoogleOrgPolicyPolicySpec, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleOrgPolicyPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9ae33c3ddb9a789dc84216c4f9197c5021aa725de7956063ceae00823ace9b4(
    *,
    inherit_from_parent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    reset: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOrgPolicyPolicyDryRunSpecRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__444ee0d70a83697c6154d3cb94e245ef5b6424b4f904d016b608227a0a167c2a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12136a36af2b4b0823d9ad785d44545753c686cd2b3053f48140359051a0b704(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOrgPolicyPolicyDryRunSpecRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48dd4fb7c5cdccb594ae895661995749b10a29728e2d1bb6afdf5d89bd741de1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e16f1ed62afaa6b7101e72cf016592f9289a2a9e59194cac32820f12ce276a9c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae912335eeb630a9a0699426786115d23eda50525b24fa0ac2dd5367294e8847(
    value: typing.Optional[GoogleOrgPolicyPolicyDryRunSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf21511e5eda3ca2880d5f69e836f796d5c05d325bd31d882cb48714fcac9e15(
    *,
    allow_all: typing.Optional[builtins.str] = None,
    condition: typing.Optional[typing.Union[GoogleOrgPolicyPolicyDryRunSpecRulesCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    deny_all: typing.Optional[builtins.str] = None,
    enforce: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Union[GoogleOrgPolicyPolicyDryRunSpecRulesValues, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0413f74ba647f0f3995fa0ffec067f41cd79c6f67a367e9786e42389c22228e5(
    *,
    description: typing.Optional[builtins.str] = None,
    expression: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__769ca56bdaf23e57712a242d8d1d7b8f53ef222d80f8e3d494fda62afc755305(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7c2bce735c0edde2d6822d60f7b748c03bc06b1e8cb51a06c9a0597fed523a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8ad04837acdedaa527eb6a506c5feac4a1429d2f63b3cca2c63e271e104e3cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03546b83a821aaa84ddcaf86e926e8b491e6ce826f5ef11e168cca72a8204a6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e900f8c4efd97b709cb59bf9fea9521b0d9e071648590917798f8e3d2fb862eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fcaa782736c4c40501b5e22b991c339ec86fd84b85976a667aade92c3067e39(
    value: typing.Optional[GoogleOrgPolicyPolicyDryRunSpecRulesCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75ea892bc12c68580dd055d78b8ba25d609fa639711fc67d386e8742d96bcbb5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__568eea8a121ee7bc217e72bc2fc7e519b091ddd6a863a7764c9eb601cf16217c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f944c39db616c7b323213c6b5bec0478240945791f4379cecbfb1f93a271291(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f18141a37f5c55b95ec94092a3ee7d31348b973def9534e63771347f587ebd02(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__978c0b88b5e5f53a68852aff17fa2dbc9c82cc2caf2d7e5d0dbb31c3efe0e8d5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22d89de079e92b7b9bb281c0581fde036671c0ef39c5afcbba0b4fb291b8da33(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOrgPolicyPolicyDryRunSpecRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13b43baeae701ead2a5a9a2a32c0e4256286ece4e0e47d2ced6dbe73b5d28465(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66ff5fcd07b0b1706b9a332ccb8e376e1a4d44eb51e860ca6561381d66c0ba29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1af588d33945551a7e3bf153c67ad1358f24e2f8c010103a7d9ce0bba151fbda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4c5fdeb8be5062d5267660627bf8dc44b43aec138929288bc802d76a3778b55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea9184a4f2bdba15c7bf41b158837bf76e3e91fd5acd8e79a4dcd9512e04e00d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd48bdc3824358dbfa85551916d425442afbd61610746efdf9215425ee496c0a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOrgPolicyPolicyDryRunSpecRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bfe132586289788c59d6d89922cba5657fdbfd5e472d575b4893263acb536a5(
    *,
    allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    denied_values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be3641eb85763cd4f2287634d25f38c5c98e47a7f55ff13a1d860ffaeb7d407a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc99ec16b1a14efcc5ebd62df3a408d61f822b7da42f78c4746cb6bed104185c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__938c06554a8a118c336834457354e6e0a07a6e389ab82d1e85cc498ddaeb6231(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a067605524d356f4b42bec41f58867211a6bc02ee00ea27ff9559f5620cf911(
    value: typing.Optional[GoogleOrgPolicyPolicyDryRunSpecRulesValues],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c904a253e5f1e46ade1397cb042e92b432b0a80210256d3f4e095c913514cb38(
    *,
    inherit_from_parent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    reset: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOrgPolicyPolicySpecRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b5ffdb1514c521b58541ca3c80dc04af9eeffa41d551c37efd11987dae4b230(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__015f1222d530805b7fe1936570dd1c710e152d8b355f0170bc43e3e919bf0f36(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOrgPolicyPolicySpecRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7b47e1805a6aee471f9c1c2a81e0ea96c29a05ca9c307f56c2720260874acc9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e50448cc1b35a527b7db8b7495799f44edc77e4543750ba3c0f777679b94f4f5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfe92539b4823ab3a3be25d0a3589bee45ba385056b65ece376ab19527ee33f0(
    value: typing.Optional[GoogleOrgPolicyPolicySpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fe2113a0b682ed3d0bc589eb1f3c77d7a5f1cb701f05aa110eb98f6cb804ea3(
    *,
    allow_all: typing.Optional[builtins.str] = None,
    condition: typing.Optional[typing.Union[GoogleOrgPolicyPolicySpecRulesCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    deny_all: typing.Optional[builtins.str] = None,
    enforce: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Union[GoogleOrgPolicyPolicySpecRulesValues, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e6ce8600430530faf0eb1d7ad9b5c8afe688eed18ac53693c7353d14ec8c039(
    *,
    description: typing.Optional[builtins.str] = None,
    expression: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14d7b3de31f6ddbd265714039be227ae23f34d161ef83d3a4a1aa2809f443695(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7de7562af852666ef3c56848a6d92b42e99e5b14211f3cf37c10aae329619828(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3c5d4f3f301b673531073dd6890eb0b3ceea59de45e556d55a3b9a09ebb2da4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec55e1afa5594c276a19d8259d60e45a7439bd136faffb1de1197eb9eac356c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__545d2c8db6c479da895fab5384f4d5a013a09547683c58eec86ddcb5fa114216(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f610afe8f547a254cfeaaec82321bb3d2bb4915a7fed963cfda9210dc11cf6c9(
    value: typing.Optional[GoogleOrgPolicyPolicySpecRulesCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5170ba2fa8d99090cc21910ce6a57e49661918c7b1a3157772f33527ba61a6c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c1491050d809cc0973d3a1f772fdb73634bc9d646b876d8aa96368c3784b08d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50adeb98eada068b51f6aa13d267f3fd9baf6ae09849c0862d9a5d08b10a131d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d17b4777d10a67e6947dfdacac80d8ef3203be84c285c942e98eaabc97445c29(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebe32159dd4df247beb9db64a1aa5e4909b2264e252f8418f1909f5b7613165c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb96e04ae4ad512e423070cf566034ee00de6cb7a08e27e9ebeeb9f14d7121ca(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOrgPolicyPolicySpecRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0c7665d498bc6af49f6682f10ea0c28173e654bd049b1299222a0f3707bb027(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c65dd863afa9c1d345b18038e33f5b0106325f096920df57a9e1745896729bfb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c16296ce1a3cfcf26202418306d6ddd51b04f421536913fc2e5368886a5ce55e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0576ffb813ebaee215e301c47c83982fa1d4191251650ceb160f4b198d1db979(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb77241a20da3be778fe070037149dc40ee362e722287d67c347fca483d2b3f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d9d2afc7ccf91ab9ff49cb348234c146ecd8814e348adb2a6ab97c4f4447e0f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOrgPolicyPolicySpecRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee688c720e517a66e1e8c5f2ea676d12accbe8813d035d949704c0a87818d58f(
    *,
    allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    denied_values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__199b28d2fc9b246f0a85ca43eb3c1d36844ab688dfee2fbca28e1a12e560d7a0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c00a1bcf6d61aea0bec8f89d5d3ebeab1a0a330a89f3bf6f8622cddaab255745(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e08afc919cb24a55c9469154be00c398064f612a050f636a94ab05ade519070c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__109243844ee4eb8d0eb1a9941747aa0b3022b75198a7c72fa16dbeb93e9de332(
    value: typing.Optional[GoogleOrgPolicyPolicySpecRulesValues],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a11f5008a53e1546ee646e55c33fc9ad3801c5b6c974f8fc4a0d0fa012aa6ac4(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2d0e222eb76dafa163dcfe09e09a994e7e5a1cc9f89163c8c7c98cc5f9af170(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcaaaa01f00d6296b17ea0aca745e2835b205c3b6bf9f4c8bb1338b5fe9cf6f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1816d16ed38eb15c17b28a956fdc205cd8199c1f1061ecd594e11da72d551355(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__228834498dc14c26abb5e0b51c1c9e8b75ec6449c6a1237b76e8a8f73fd2a1f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3d5d6b28a3ab6da4f47058ffd25da2e293d320a3b26771efe4e6b7c0b3b7d3a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOrgPolicyPolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
