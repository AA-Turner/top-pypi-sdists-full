r'''
# `google_org_policy_policy`

Refer to the Terraform Registry for docs: [`google_org_policy_policy`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy).
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


class OrgPolicyPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.orgPolicyPolicy.OrgPolicyPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy google_org_policy_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        parent: builtins.str,
        dry_run_spec: typing.Optional[typing.Union["OrgPolicyPolicyDryRunSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        spec: typing.Optional[typing.Union["OrgPolicyPolicySpec", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["OrgPolicyPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy google_org_policy_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Immutable. The resource name of the Policy. Must be one of the following forms, where constraint_name is the name of the constraint which this Policy configures: * 'projects/{project_number}/policies/{constraint_name}' * 'folders/{folder_id}/policies/{constraint_name}' * 'organizations/{organization_id}/policies/{constraint_name}' For example, "projects/123/policies/compute.disableSerialPortAccess". Note: 'projects/{project_id}/policies/{constraint_name}' is also an acceptable name for API requests, but responses will return the name using the equivalent project number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#name OrgPolicyPolicy#name}
        :param parent: The parent of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#parent OrgPolicyPolicy#parent}
        :param dry_run_spec: dry_run_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#dry_run_spec OrgPolicyPolicy#dry_run_spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#id OrgPolicyPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#spec OrgPolicyPolicy#spec}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#timeouts OrgPolicyPolicy#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cb420ea32b7efe362b61251b8e864613dce0f018955bce2e6f41850097aec4a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = OrgPolicyPolicyConfig(
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
        '''Generates CDKTF code for importing a OrgPolicyPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the OrgPolicyPolicy to import.
        :param import_from_id: The id of the existing OrgPolicyPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the OrgPolicyPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d6385d9bc8804bbcfca688a3d6b0da6dc113ffcd3d93c28def37975bde259b2)
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
        rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrgPolicyPolicyDryRunSpecRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param inherit_from_parent: Determines the inheritance behavior for this policy. If 'inherit_from_parent' is true, policy rules set higher up in the hierarchy (up to the closest root) are inherited and present in the effective policy. If it is false, then no rules are inherited, and this policy becomes the new root for evaluation. This field can be set only for policies which configure list constraints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#inherit_from_parent OrgPolicyPolicy#inherit_from_parent}
        :param reset: Ignores policies set above this resource and restores the 'constraint_default' enforcement behavior of the specific constraint at this resource. This field can be set in policies for either list or boolean constraints. If set, 'rules' must be empty and 'inherit_from_parent' must be set to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#reset OrgPolicyPolicy#reset}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#rules OrgPolicyPolicy#rules}
        '''
        value = OrgPolicyPolicyDryRunSpec(
            inherit_from_parent=inherit_from_parent, reset=reset, rules=rules
        )

        return typing.cast(None, jsii.invoke(self, "putDryRunSpec", [value]))

    @jsii.member(jsii_name="putSpec")
    def put_spec(
        self,
        *,
        inherit_from_parent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        reset: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrgPolicyPolicySpecRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param inherit_from_parent: Determines the inheritance behavior for this 'Policy'. If 'inherit_from_parent' is true, PolicyRules set higher up in the hierarchy (up to the closest root) are inherited and present in the effective policy. If it is false, then no rules are inherited, and this Policy becomes the new root for evaluation. This field can be set only for Policies which configure list constraints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#inherit_from_parent OrgPolicyPolicy#inherit_from_parent}
        :param reset: Ignores policies set above this resource and restores the 'constraint_default' enforcement behavior of the specific 'Constraint' at this resource. This field can be set in policies for either list or boolean constraints. If set, 'rules' must be empty and 'inherit_from_parent' must be set to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#reset OrgPolicyPolicy#reset}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#rules OrgPolicyPolicy#rules}
        '''
        value = OrgPolicyPolicySpec(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#create OrgPolicyPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#delete OrgPolicyPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#update OrgPolicyPolicy#update}.
        '''
        value = OrgPolicyPolicyTimeouts(create=create, delete=delete, update=update)

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
    def dry_run_spec(self) -> "OrgPolicyPolicyDryRunSpecOutputReference":
        return typing.cast("OrgPolicyPolicyDryRunSpecOutputReference", jsii.get(self, "dryRunSpec"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="spec")
    def spec(self) -> "OrgPolicyPolicySpecOutputReference":
        return typing.cast("OrgPolicyPolicySpecOutputReference", jsii.get(self, "spec"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "OrgPolicyPolicyTimeoutsOutputReference":
        return typing.cast("OrgPolicyPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="dryRunSpecInput")
    def dry_run_spec_input(self) -> typing.Optional["OrgPolicyPolicyDryRunSpec"]:
        return typing.cast(typing.Optional["OrgPolicyPolicyDryRunSpec"], jsii.get(self, "dryRunSpecInput"))

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
    def spec_input(self) -> typing.Optional["OrgPolicyPolicySpec"]:
        return typing.cast(typing.Optional["OrgPolicyPolicySpec"], jsii.get(self, "specInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "OrgPolicyPolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "OrgPolicyPolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50d4c6dc8c743ab894e559bc1cc826381087950dcebd4c5bf52c59211eac5074)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6b2cbcef0e39cccf8409a3b92752f9254f7b64cd4fbad16c9ebb71fd24ca6a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f5841f878711d6d3568bdad87aba456b6a3906595a3fda1c1a0e8eb6ebf316c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.orgPolicyPolicy.OrgPolicyPolicyConfig",
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
class OrgPolicyPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        dry_run_spec: typing.Optional[typing.Union["OrgPolicyPolicyDryRunSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        spec: typing.Optional[typing.Union["OrgPolicyPolicySpec", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["OrgPolicyPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Immutable. The resource name of the Policy. Must be one of the following forms, where constraint_name is the name of the constraint which this Policy configures: * 'projects/{project_number}/policies/{constraint_name}' * 'folders/{folder_id}/policies/{constraint_name}' * 'organizations/{organization_id}/policies/{constraint_name}' For example, "projects/123/policies/compute.disableSerialPortAccess". Note: 'projects/{project_id}/policies/{constraint_name}' is also an acceptable name for API requests, but responses will return the name using the equivalent project number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#name OrgPolicyPolicy#name}
        :param parent: The parent of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#parent OrgPolicyPolicy#parent}
        :param dry_run_spec: dry_run_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#dry_run_spec OrgPolicyPolicy#dry_run_spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#id OrgPolicyPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#spec OrgPolicyPolicy#spec}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#timeouts OrgPolicyPolicy#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(dry_run_spec, dict):
            dry_run_spec = OrgPolicyPolicyDryRunSpec(**dry_run_spec)
        if isinstance(spec, dict):
            spec = OrgPolicyPolicySpec(**spec)
        if isinstance(timeouts, dict):
            timeouts = OrgPolicyPolicyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f167db329a1f404dde4b6d65f2198c7d69be8a31ceb80d5ace385a1142b6efd9)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#name OrgPolicyPolicy#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parent(self) -> builtins.str:
        '''The parent of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#parent OrgPolicyPolicy#parent}
        '''
        result = self._values.get("parent")
        assert result is not None, "Required property 'parent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dry_run_spec(self) -> typing.Optional["OrgPolicyPolicyDryRunSpec"]:
        '''dry_run_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#dry_run_spec OrgPolicyPolicy#dry_run_spec}
        '''
        result = self._values.get("dry_run_spec")
        return typing.cast(typing.Optional["OrgPolicyPolicyDryRunSpec"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#id OrgPolicyPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spec(self) -> typing.Optional["OrgPolicyPolicySpec"]:
        '''spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#spec OrgPolicyPolicy#spec}
        '''
        result = self._values.get("spec")
        return typing.cast(typing.Optional["OrgPolicyPolicySpec"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["OrgPolicyPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#timeouts OrgPolicyPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["OrgPolicyPolicyTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgPolicyPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.orgPolicyPolicy.OrgPolicyPolicyDryRunSpec",
    jsii_struct_bases=[],
    name_mapping={
        "inherit_from_parent": "inheritFromParent",
        "reset": "reset",
        "rules": "rules",
    },
)
class OrgPolicyPolicyDryRunSpec:
    def __init__(
        self,
        *,
        inherit_from_parent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        reset: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrgPolicyPolicyDryRunSpecRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param inherit_from_parent: Determines the inheritance behavior for this policy. If 'inherit_from_parent' is true, policy rules set higher up in the hierarchy (up to the closest root) are inherited and present in the effective policy. If it is false, then no rules are inherited, and this policy becomes the new root for evaluation. This field can be set only for policies which configure list constraints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#inherit_from_parent OrgPolicyPolicy#inherit_from_parent}
        :param reset: Ignores policies set above this resource and restores the 'constraint_default' enforcement behavior of the specific constraint at this resource. This field can be set in policies for either list or boolean constraints. If set, 'rules' must be empty and 'inherit_from_parent' must be set to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#reset OrgPolicyPolicy#reset}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#rules OrgPolicyPolicy#rules}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1af08a49d6a20d8c242a8c29046815a3c4bfb9ee54722720b73b5d0c357e511)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#inherit_from_parent OrgPolicyPolicy#inherit_from_parent}
        '''
        result = self._values.get("inherit_from_parent")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def reset(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Ignores policies set above this resource and restores the 'constraint_default' enforcement behavior of the specific constraint at this resource.

        This field can be set in policies for either list or boolean constraints. If set, 'rules' must be empty and 'inherit_from_parent' must be set to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#reset OrgPolicyPolicy#reset}
        '''
        result = self._values.get("reset")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def rules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrgPolicyPolicyDryRunSpecRules"]]]:
        '''rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#rules OrgPolicyPolicy#rules}
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrgPolicyPolicyDryRunSpecRules"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgPolicyPolicyDryRunSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrgPolicyPolicyDryRunSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.orgPolicyPolicy.OrgPolicyPolicyDryRunSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__89343746d428fed962786d6690a758791dcbfd5c603f1c3ad6d14236eefe4fe9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRules")
    def put_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrgPolicyPolicyDryRunSpecRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5fcea140ed69bf4ddb2f1d966bd3bbed98f5a6ff9cae66ece80484ea751e4e8)
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
    def rules(self) -> "OrgPolicyPolicyDryRunSpecRulesList":
        return typing.cast("OrgPolicyPolicyDryRunSpecRulesList", jsii.get(self, "rules"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrgPolicyPolicyDryRunSpecRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrgPolicyPolicyDryRunSpecRules"]]], jsii.get(self, "rulesInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2d5a61eb6416d80033a93a0160cc207687d922c90f7f97c1450cdbacad8d87b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d553f8ece5b740fe28d07fe297aa0bb3479df62c12e45b84fbd85db04c417aeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OrgPolicyPolicyDryRunSpec]:
        return typing.cast(typing.Optional[OrgPolicyPolicyDryRunSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[OrgPolicyPolicyDryRunSpec]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__124db6cda09dab6b502dd846fc5c76a89dddbb499c37edc4401b3edf56227676)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.orgPolicyPolicy.OrgPolicyPolicyDryRunSpecRules",
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
class OrgPolicyPolicyDryRunSpecRules:
    def __init__(
        self,
        *,
        allow_all: typing.Optional[builtins.str] = None,
        condition: typing.Optional[typing.Union["OrgPolicyPolicyDryRunSpecRulesCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        deny_all: typing.Optional[builtins.str] = None,
        enforce: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Union["OrgPolicyPolicyDryRunSpecRulesValues", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_all: Setting this to '"TRUE"' means that all values are allowed. This field can be set only in Policies for list constraints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#allow_all OrgPolicyPolicy#allow_all}
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#condition OrgPolicyPolicy#condition}
        :param deny_all: Setting this to '"TRUE"' means that all values are denied. This field can be set only in Policies for list constraints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#deny_all OrgPolicyPolicy#deny_all}
        :param enforce: If '"TRUE"', then the 'Policy' is enforced. If '"FALSE"', then any configuration is acceptable. This field can be set only in Policies for boolean constraints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#enforce OrgPolicyPolicy#enforce}
        :param parameters: Optional. Required for Managed Constraints if parameters defined in constraints. Pass parameter values when policy enforcement is enabled. Ensure that parameter value types match those defined in the constraint definition. For example: { "allowedLocations" : ["us-east1", "us-west1"], "allowAll" : true } Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#parameters OrgPolicyPolicy#parameters}
        :param values: values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#values OrgPolicyPolicy#values}
        '''
        if isinstance(condition, dict):
            condition = OrgPolicyPolicyDryRunSpecRulesCondition(**condition)
        if isinstance(values, dict):
            values = OrgPolicyPolicyDryRunSpecRulesValues(**values)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16d5cc38c5c82d0dd1800c218eb9459f9d678fcb9b0249b9cfc74b3693a53ad4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#allow_all OrgPolicyPolicy#allow_all}
        '''
        result = self._values.get("allow_all")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def condition(self) -> typing.Optional["OrgPolicyPolicyDryRunSpecRulesCondition"]:
        '''condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#condition OrgPolicyPolicy#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional["OrgPolicyPolicyDryRunSpecRulesCondition"], result)

    @builtins.property
    def deny_all(self) -> typing.Optional[builtins.str]:
        '''Setting this to '"TRUE"' means that all values are denied.

        This field can be set only in Policies for list constraints.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#deny_all OrgPolicyPolicy#deny_all}
        '''
        result = self._values.get("deny_all")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enforce(self) -> typing.Optional[builtins.str]:
        '''If '"TRUE"', then the 'Policy' is enforced.

        If '"FALSE"', then any configuration is acceptable. This field can be set only in Policies for boolean constraints.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#enforce OrgPolicyPolicy#enforce}
        '''
        result = self._values.get("enforce")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Required for Managed Constraints if parameters defined in constraints. Pass parameter values when policy enforcement is enabled. Ensure that parameter value types match those defined in the constraint definition. For example: { "allowedLocations" : ["us-east1", "us-west1"], "allowAll" : true }

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#parameters OrgPolicyPolicy#parameters}
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional["OrgPolicyPolicyDryRunSpecRulesValues"]:
        '''values block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#values OrgPolicyPolicy#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional["OrgPolicyPolicyDryRunSpecRulesValues"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgPolicyPolicyDryRunSpecRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.orgPolicyPolicy.OrgPolicyPolicyDryRunSpecRulesCondition",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "expression": "expression",
        "location": "location",
        "title": "title",
    },
)
class OrgPolicyPolicyDryRunSpecRulesCondition:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        expression: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param description: Optional. Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#description OrgPolicyPolicy#description}
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#expression OrgPolicyPolicy#expression}
        :param location: Optional. String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#location OrgPolicyPolicy#location}
        :param title: Optional. Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#title OrgPolicyPolicy#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5edc41838bdef7879d525e6883475261a396442b5d0daec93f47c3d5462ee91f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#description OrgPolicyPolicy#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expression(self) -> typing.Optional[builtins.str]:
        '''Textual representation of an expression in Common Expression Language syntax.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#expression OrgPolicyPolicy#expression}
        '''
        result = self._values.get("expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''Optional.

        String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#location OrgPolicyPolicy#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#title OrgPolicyPolicy#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgPolicyPolicyDryRunSpecRulesCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrgPolicyPolicyDryRunSpecRulesConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.orgPolicyPolicy.OrgPolicyPolicyDryRunSpecRulesConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfc3adcfb6be04ee9814af7466d96e89af9e71930b1b97ad8559b3ef8c3e10d3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3be4fb08f74585bf19f8a40c1dcdca954d26766102452af47e7f3e662147b155)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64106aac88e39736444280089c8d4cb8c1dba7e60eb2745c8cfadc99c5446ef6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e6e1c5e1ae858176c2a9baaca44efac4e4a6216c40077461d3739ae9beebcd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e56f091f8cdd1f8f9e8b180c30f503678d51a8c3ad67a495d9b4b3338e3f496)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OrgPolicyPolicyDryRunSpecRulesCondition]:
        return typing.cast(typing.Optional[OrgPolicyPolicyDryRunSpecRulesCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrgPolicyPolicyDryRunSpecRulesCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f52e5d00ed95a843a00413aeb8ff0c421ab55917f571380fde5c262e051ef15d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OrgPolicyPolicyDryRunSpecRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.orgPolicyPolicy.OrgPolicyPolicyDryRunSpecRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7387491aca5a3846126a15da4b7154c19f48ca76351bb9fd42512b8c9d9bdf54)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OrgPolicyPolicyDryRunSpecRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39e9764f1b4c1ba70129e23dc4ccafbbec9e84e64e863519711040899b6e7b75)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OrgPolicyPolicyDryRunSpecRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d96a828a01dad33d00c5047d13ddb42d79765254698fc54b88e5d5c73a1e1833)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdd2a1bb7ce3a5883de4ee29e3051076320ecd03405983725824d1b353790516)
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
            type_hints = typing.get_type_hints(_typecheckingstub__292868eceb2ab74777e299d7e0c1100768fb6bcc5c65a7c88c383b67cfd9ff82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrgPolicyPolicyDryRunSpecRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrgPolicyPolicyDryRunSpecRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrgPolicyPolicyDryRunSpecRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f003ed77c86784738cc08bfb1733557dac041535ce3e35b1ecb5bd00e8462a0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OrgPolicyPolicyDryRunSpecRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.orgPolicyPolicy.OrgPolicyPolicyDryRunSpecRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__672f6744acd7e30322de73370f8b43778b7f0583b4c1d8d11caffd86bc4e60d4)
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
        :param description: Optional. Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#description OrgPolicyPolicy#description}
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#expression OrgPolicyPolicy#expression}
        :param location: Optional. String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#location OrgPolicyPolicy#location}
        :param title: Optional. Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#title OrgPolicyPolicy#title}
        '''
        value = OrgPolicyPolicyDryRunSpecRulesCondition(
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
        :param allowed_values: List of values allowed at this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#allowed_values OrgPolicyPolicy#allowed_values}
        :param denied_values: List of values denied at this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#denied_values OrgPolicyPolicy#denied_values}
        '''
        value = OrgPolicyPolicyDryRunSpecRulesValues(
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
    def condition(self) -> OrgPolicyPolicyDryRunSpecRulesConditionOutputReference:
        return typing.cast(OrgPolicyPolicyDryRunSpecRulesConditionOutputReference, jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> "OrgPolicyPolicyDryRunSpecRulesValuesOutputReference":
        return typing.cast("OrgPolicyPolicyDryRunSpecRulesValuesOutputReference", jsii.get(self, "values"))

    @builtins.property
    @jsii.member(jsii_name="allowAllInput")
    def allow_all_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "allowAllInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(
        self,
    ) -> typing.Optional[OrgPolicyPolicyDryRunSpecRulesCondition]:
        return typing.cast(typing.Optional[OrgPolicyPolicyDryRunSpecRulesCondition], jsii.get(self, "conditionInput"))

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
    def values_input(self) -> typing.Optional["OrgPolicyPolicyDryRunSpecRulesValues"]:
        return typing.cast(typing.Optional["OrgPolicyPolicyDryRunSpecRulesValues"], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowAll")
    def allow_all(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "allowAll"))

    @allow_all.setter
    def allow_all(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc925ea0e57d1d4fc02b00aeedbef2fb8f0560d8c6f10e6d1dd7a91131e48325)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="denyAll")
    def deny_all(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "denyAll"))

    @deny_all.setter
    def deny_all(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e7d60349c4b90ec5979eb8af6dc7ce5a5954e1b0c91c19d90ecd7073babbf69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "denyAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforce")
    def enforce(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enforce"))

    @enforce.setter
    def enforce(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c760d5923ced0fbb8f4642c570cbfbf678a147ea6972b1a1e6215f8ad112352)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforce", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b900ffe3a74b755c135e8341ee831787741c4ead00084ce8720f7f3fe683627)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrgPolicyPolicyDryRunSpecRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrgPolicyPolicyDryRunSpecRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrgPolicyPolicyDryRunSpecRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64fd808271b28714f75076c45909fdb8f629d7bb4b17830482234188d2956ca3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.orgPolicyPolicy.OrgPolicyPolicyDryRunSpecRulesValues",
    jsii_struct_bases=[],
    name_mapping={"allowed_values": "allowedValues", "denied_values": "deniedValues"},
)
class OrgPolicyPolicyDryRunSpecRulesValues:
    def __init__(
        self,
        *,
        allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        denied_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_values: List of values allowed at this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#allowed_values OrgPolicyPolicy#allowed_values}
        :param denied_values: List of values denied at this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#denied_values OrgPolicyPolicy#denied_values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6072c9be1ae8b808df3f4c04a4409f76840acf0613eb56ca84f9a2dab9fbabb)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#allowed_values OrgPolicyPolicy#allowed_values}
        '''
        result = self._values.get("allowed_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def denied_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of values denied at this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#denied_values OrgPolicyPolicy#denied_values}
        '''
        result = self._values.get("denied_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgPolicyPolicyDryRunSpecRulesValues(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrgPolicyPolicyDryRunSpecRulesValuesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.orgPolicyPolicy.OrgPolicyPolicyDryRunSpecRulesValuesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0fb563c623afdd58e7e1e1dcff56f350ea15028fd2c7aa4829ae0e8bea9af0c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a3649c1fc6fcadd19a941d7c79bc082268183eec27eb89b4bc3c54fac817c50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deniedValues")
    def denied_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "deniedValues"))

    @denied_values.setter
    def denied_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8370ba6baaf00219538eb74bfdd5940b537ebb21ebb0d69f9856ea97d164c38e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deniedValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OrgPolicyPolicyDryRunSpecRulesValues]:
        return typing.cast(typing.Optional[OrgPolicyPolicyDryRunSpecRulesValues], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrgPolicyPolicyDryRunSpecRulesValues],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cd553078807478a29bbb9076d06825f0f675bfdf8260f23c852e9c448a2b888)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.orgPolicyPolicy.OrgPolicyPolicySpec",
    jsii_struct_bases=[],
    name_mapping={
        "inherit_from_parent": "inheritFromParent",
        "reset": "reset",
        "rules": "rules",
    },
)
class OrgPolicyPolicySpec:
    def __init__(
        self,
        *,
        inherit_from_parent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        reset: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrgPolicyPolicySpecRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param inherit_from_parent: Determines the inheritance behavior for this 'Policy'. If 'inherit_from_parent' is true, PolicyRules set higher up in the hierarchy (up to the closest root) are inherited and present in the effective policy. If it is false, then no rules are inherited, and this Policy becomes the new root for evaluation. This field can be set only for Policies which configure list constraints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#inherit_from_parent OrgPolicyPolicy#inherit_from_parent}
        :param reset: Ignores policies set above this resource and restores the 'constraint_default' enforcement behavior of the specific 'Constraint' at this resource. This field can be set in policies for either list or boolean constraints. If set, 'rules' must be empty and 'inherit_from_parent' must be set to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#reset OrgPolicyPolicy#reset}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#rules OrgPolicyPolicy#rules}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21b56320ff38a215e9cd5d7fa04e70409e5b8744c7c495869e9861c973b416da)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#inherit_from_parent OrgPolicyPolicy#inherit_from_parent}
        '''
        result = self._values.get("inherit_from_parent")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def reset(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Ignores policies set above this resource and restores the 'constraint_default' enforcement behavior of the specific 'Constraint' at this resource.

        This field can be set in policies for either list or boolean constraints. If set, 'rules' must be empty and 'inherit_from_parent' must be set to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#reset OrgPolicyPolicy#reset}
        '''
        result = self._values.get("reset")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def rules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrgPolicyPolicySpecRules"]]]:
        '''rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#rules OrgPolicyPolicy#rules}
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrgPolicyPolicySpecRules"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgPolicyPolicySpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrgPolicyPolicySpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.orgPolicyPolicy.OrgPolicyPolicySpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ddb07da617f2cc87cb636ac81a096981dfdceba15b6f92de18c5729a6f721dee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRules")
    def put_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrgPolicyPolicySpecRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0ee326139b88ff7f50f886f778ffa95a4c0513c3b1bc5b59241f5d112cf1229)
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
    def rules(self) -> "OrgPolicyPolicySpecRulesList":
        return typing.cast("OrgPolicyPolicySpecRulesList", jsii.get(self, "rules"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrgPolicyPolicySpecRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrgPolicyPolicySpecRules"]]], jsii.get(self, "rulesInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__3fd02d0a3f746d92bc09f17712585879f6112921f6d2f202ab98cf791c65c502)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b463bed25ba5d36229195236153dcbe65b12b48496e283d574fea03b6a3dc666)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OrgPolicyPolicySpec]:
        return typing.cast(typing.Optional[OrgPolicyPolicySpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[OrgPolicyPolicySpec]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea02ee2a2eef1d8ec2c75f50485944e39d8f7a6041c77444297dadafc7380d08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.orgPolicyPolicy.OrgPolicyPolicySpecRules",
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
class OrgPolicyPolicySpecRules:
    def __init__(
        self,
        *,
        allow_all: typing.Optional[builtins.str] = None,
        condition: typing.Optional[typing.Union["OrgPolicyPolicySpecRulesCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        deny_all: typing.Optional[builtins.str] = None,
        enforce: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Union["OrgPolicyPolicySpecRulesValues", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_all: Setting this to '"TRUE"' means that all values are allowed. This field can be set only in Policies for list constraints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#allow_all OrgPolicyPolicy#allow_all}
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#condition OrgPolicyPolicy#condition}
        :param deny_all: Setting this to '"TRUE"' means that all values are denied. This field can be set only in Policies for list constraints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#deny_all OrgPolicyPolicy#deny_all}
        :param enforce: If '"TRUE"', then the 'Policy' is enforced. If '"FALSE"', then any configuration is acceptable. This field can be set only in Policies for boolean constraints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#enforce OrgPolicyPolicy#enforce}
        :param parameters: Optional. Required for Managed Constraints if parameters defined in constraints. Pass parameter values when policy enforcement is enabled. Ensure that parameter value types match those defined in the constraint definition. For example: { "allowedLocations" : ["us-east1", "us-west1"], "allowAll" : true } Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#parameters OrgPolicyPolicy#parameters}
        :param values: values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#values OrgPolicyPolicy#values}
        '''
        if isinstance(condition, dict):
            condition = OrgPolicyPolicySpecRulesCondition(**condition)
        if isinstance(values, dict):
            values = OrgPolicyPolicySpecRulesValues(**values)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49b82ba79f6ace37456eef93057ed699b0f881abe835506661de58836f5f1e08)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#allow_all OrgPolicyPolicy#allow_all}
        '''
        result = self._values.get("allow_all")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def condition(self) -> typing.Optional["OrgPolicyPolicySpecRulesCondition"]:
        '''condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#condition OrgPolicyPolicy#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional["OrgPolicyPolicySpecRulesCondition"], result)

    @builtins.property
    def deny_all(self) -> typing.Optional[builtins.str]:
        '''Setting this to '"TRUE"' means that all values are denied.

        This field can be set only in Policies for list constraints.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#deny_all OrgPolicyPolicy#deny_all}
        '''
        result = self._values.get("deny_all")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enforce(self) -> typing.Optional[builtins.str]:
        '''If '"TRUE"', then the 'Policy' is enforced.

        If '"FALSE"', then any configuration is acceptable. This field can be set only in Policies for boolean constraints.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#enforce OrgPolicyPolicy#enforce}
        '''
        result = self._values.get("enforce")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Required for Managed Constraints if parameters defined in constraints. Pass parameter values when policy enforcement is enabled. Ensure that parameter value types match those defined in the constraint definition. For example: { "allowedLocations" : ["us-east1", "us-west1"], "allowAll" : true }

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#parameters OrgPolicyPolicy#parameters}
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional["OrgPolicyPolicySpecRulesValues"]:
        '''values block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#values OrgPolicyPolicy#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional["OrgPolicyPolicySpecRulesValues"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgPolicyPolicySpecRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.orgPolicyPolicy.OrgPolicyPolicySpecRulesCondition",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "expression": "expression",
        "location": "location",
        "title": "title",
    },
)
class OrgPolicyPolicySpecRulesCondition:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        expression: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param description: Optional. Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#description OrgPolicyPolicy#description}
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#expression OrgPolicyPolicy#expression}
        :param location: Optional. String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#location OrgPolicyPolicy#location}
        :param title: Optional. Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#title OrgPolicyPolicy#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bafea799a9852424a8b6474db5e94615a2be57bf8bf69423c4e25fda83210d9)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#description OrgPolicyPolicy#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expression(self) -> typing.Optional[builtins.str]:
        '''Textual representation of an expression in Common Expression Language syntax.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#expression OrgPolicyPolicy#expression}
        '''
        result = self._values.get("expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''Optional.

        String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#location OrgPolicyPolicy#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#title OrgPolicyPolicy#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgPolicyPolicySpecRulesCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrgPolicyPolicySpecRulesConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.orgPolicyPolicy.OrgPolicyPolicySpecRulesConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d632d22acaa005d559c4fc062c90603c709e841fa5984915748dcb71fc9df41a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f76e1c845ce28a8e2c363abd5515076fb94cd76a56efd593e51adceecdcf6582)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3481657cac54fa6aaf3e67151c66e4a62bcf3483c08d6e2b82219d96c353abd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08b23573b5b3f5a521ba5839589a67c4d4c3507ccc52056d5bcd21d1d608ea48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dcf5705cf8254cee25f2941a4a810e606a02597c427f2e9d4c9aa6671f3391b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OrgPolicyPolicySpecRulesCondition]:
        return typing.cast(typing.Optional[OrgPolicyPolicySpecRulesCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrgPolicyPolicySpecRulesCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd80cbb1becee5ba15abc3aac8515e03bcac9d0eca51124d057694ab085e0a3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OrgPolicyPolicySpecRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.orgPolicyPolicy.OrgPolicyPolicySpecRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5ebb0ae3ad125b2275c766bba6478509d86e14e19fa7ca83e1bd60cace2ab2c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OrgPolicyPolicySpecRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aeb1c91da8ed87f4905f374a11b0d406ed4c94a1b15e32c3b9829aa768b28ab)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OrgPolicyPolicySpecRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbcc04acca85c24094893e4ec18be1765d21a0b1b2fa920b674dfc4a57033641)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6489d58baa00f47518e0eded4376cc042ba33b4e538993531a8f41cf2d067962)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e062f2fabf09af1a6e6a49a02048963c595418b6dfb3b9a086e06f14633d5b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrgPolicyPolicySpecRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrgPolicyPolicySpecRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrgPolicyPolicySpecRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0429670686c492347752203bb5c888e2647cce3cb9d27479ef3e33284ca206d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OrgPolicyPolicySpecRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.orgPolicyPolicy.OrgPolicyPolicySpecRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ebdbf8465a50e47169dea02e1111fe3b0a218ad7bc7b1ac567acc1a7c1b8b2e)
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
        :param description: Optional. Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#description OrgPolicyPolicy#description}
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#expression OrgPolicyPolicy#expression}
        :param location: Optional. String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#location OrgPolicyPolicy#location}
        :param title: Optional. Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#title OrgPolicyPolicy#title}
        '''
        value = OrgPolicyPolicySpecRulesCondition(
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
        :param allowed_values: List of values allowed at this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#allowed_values OrgPolicyPolicy#allowed_values}
        :param denied_values: List of values denied at this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#denied_values OrgPolicyPolicy#denied_values}
        '''
        value = OrgPolicyPolicySpecRulesValues(
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
    def condition(self) -> OrgPolicyPolicySpecRulesConditionOutputReference:
        return typing.cast(OrgPolicyPolicySpecRulesConditionOutputReference, jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> "OrgPolicyPolicySpecRulesValuesOutputReference":
        return typing.cast("OrgPolicyPolicySpecRulesValuesOutputReference", jsii.get(self, "values"))

    @builtins.property
    @jsii.member(jsii_name="allowAllInput")
    def allow_all_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "allowAllInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(self) -> typing.Optional[OrgPolicyPolicySpecRulesCondition]:
        return typing.cast(typing.Optional[OrgPolicyPolicySpecRulesCondition], jsii.get(self, "conditionInput"))

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
    def values_input(self) -> typing.Optional["OrgPolicyPolicySpecRulesValues"]:
        return typing.cast(typing.Optional["OrgPolicyPolicySpecRulesValues"], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowAll")
    def allow_all(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "allowAll"))

    @allow_all.setter
    def allow_all(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f69a0cdf3663360d6f6e61dfeae83baeb8bf48b09a27cf5ed438594270e35b10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="denyAll")
    def deny_all(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "denyAll"))

    @deny_all.setter
    def deny_all(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e763800f8deebb49fe07a5bd25b01044ed289eeb7b92428b03949ab00979f7fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "denyAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforce")
    def enforce(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enforce"))

    @enforce.setter
    def enforce(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8176eab81064a71c8d37139f7b7b5565d4d4e584edc6d9fc5007b88d70955a51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforce", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95598abbbf51a7571555df2269428a437337b7f0a039c111fad145982cecde00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrgPolicyPolicySpecRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrgPolicyPolicySpecRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrgPolicyPolicySpecRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3baf05f28a7868b69dd2165aba0a3ec03df0c6168312c31b99e5cdc009cb1b9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.orgPolicyPolicy.OrgPolicyPolicySpecRulesValues",
    jsii_struct_bases=[],
    name_mapping={"allowed_values": "allowedValues", "denied_values": "deniedValues"},
)
class OrgPolicyPolicySpecRulesValues:
    def __init__(
        self,
        *,
        allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        denied_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_values: List of values allowed at this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#allowed_values OrgPolicyPolicy#allowed_values}
        :param denied_values: List of values denied at this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#denied_values OrgPolicyPolicy#denied_values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccb0ca968f946c1cedcea81e3b8b63d04e2d445d1d344f8b1825c2a80413a2a8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#allowed_values OrgPolicyPolicy#allowed_values}
        '''
        result = self._values.get("allowed_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def denied_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of values denied at this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#denied_values OrgPolicyPolicy#denied_values}
        '''
        result = self._values.get("denied_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgPolicyPolicySpecRulesValues(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrgPolicyPolicySpecRulesValuesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.orgPolicyPolicy.OrgPolicyPolicySpecRulesValuesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f0ff6ba4d5524e490539726aa50de07e38e2fb5f05779ea62b8d1b9342e55ff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f782a3e3b76632462af233dd6a3c4564f3cd8c4f208481d5f47c761ce473d00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deniedValues")
    def denied_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "deniedValues"))

    @denied_values.setter
    def denied_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1022751e132f4945603a1630d18a605a6c6019d00881288ec4431798da0a56bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deniedValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OrgPolicyPolicySpecRulesValues]:
        return typing.cast(typing.Optional[OrgPolicyPolicySpecRulesValues], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrgPolicyPolicySpecRulesValues],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b102b43b0262313c0d63f0f53a5c336d1fc2b0c2830e192934b3055f7f62930)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.orgPolicyPolicy.OrgPolicyPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class OrgPolicyPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#create OrgPolicyPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#delete OrgPolicyPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#update OrgPolicyPolicy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__806c60ad99258d7048cb931403c2f954076638317f1c744104d44ba7833b381b)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#create OrgPolicyPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#delete OrgPolicyPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/org_policy_policy#update OrgPolicyPolicy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgPolicyPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrgPolicyPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.orgPolicyPolicy.OrgPolicyPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0c31ba141fe21b6a73a679d281ae863c2c12fdf07f155a269247ce749b6f84f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a5f16bab8463136d8549846937c030dad6f1e814f98bfd07230dbeb654cee7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd45fa0c7818f888db0b5327f506e1190288dd997ef4f10f2856d6c8850984c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35312249f301a6d7be319a2dfa0da15fa229660838718adec17caa4b0bcf879e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrgPolicyPolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrgPolicyPolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrgPolicyPolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91ee61e1bacec1f713dc1849d88d5c09af8ec9944fde76168254f6f82e688ac4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "OrgPolicyPolicy",
    "OrgPolicyPolicyConfig",
    "OrgPolicyPolicyDryRunSpec",
    "OrgPolicyPolicyDryRunSpecOutputReference",
    "OrgPolicyPolicyDryRunSpecRules",
    "OrgPolicyPolicyDryRunSpecRulesCondition",
    "OrgPolicyPolicyDryRunSpecRulesConditionOutputReference",
    "OrgPolicyPolicyDryRunSpecRulesList",
    "OrgPolicyPolicyDryRunSpecRulesOutputReference",
    "OrgPolicyPolicyDryRunSpecRulesValues",
    "OrgPolicyPolicyDryRunSpecRulesValuesOutputReference",
    "OrgPolicyPolicySpec",
    "OrgPolicyPolicySpecOutputReference",
    "OrgPolicyPolicySpecRules",
    "OrgPolicyPolicySpecRulesCondition",
    "OrgPolicyPolicySpecRulesConditionOutputReference",
    "OrgPolicyPolicySpecRulesList",
    "OrgPolicyPolicySpecRulesOutputReference",
    "OrgPolicyPolicySpecRulesValues",
    "OrgPolicyPolicySpecRulesValuesOutputReference",
    "OrgPolicyPolicyTimeouts",
    "OrgPolicyPolicyTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__3cb420ea32b7efe362b61251b8e864613dce0f018955bce2e6f41850097aec4a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    parent: builtins.str,
    dry_run_spec: typing.Optional[typing.Union[OrgPolicyPolicyDryRunSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    spec: typing.Optional[typing.Union[OrgPolicyPolicySpec, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[OrgPolicyPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__9d6385d9bc8804bbcfca688a3d6b0da6dc113ffcd3d93c28def37975bde259b2(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50d4c6dc8c743ab894e559bc1cc826381087950dcebd4c5bf52c59211eac5074(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6b2cbcef0e39cccf8409a3b92752f9254f7b64cd4fbad16c9ebb71fd24ca6a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f5841f878711d6d3568bdad87aba456b6a3906595a3fda1c1a0e8eb6ebf316c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f167db329a1f404dde4b6d65f2198c7d69be8a31ceb80d5ace385a1142b6efd9(
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
    dry_run_spec: typing.Optional[typing.Union[OrgPolicyPolicyDryRunSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    spec: typing.Optional[typing.Union[OrgPolicyPolicySpec, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[OrgPolicyPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1af08a49d6a20d8c242a8c29046815a3c4bfb9ee54722720b73b5d0c357e511(
    *,
    inherit_from_parent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    reset: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrgPolicyPolicyDryRunSpecRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89343746d428fed962786d6690a758791dcbfd5c603f1c3ad6d14236eefe4fe9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5fcea140ed69bf4ddb2f1d966bd3bbed98f5a6ff9cae66ece80484ea751e4e8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrgPolicyPolicyDryRunSpecRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d5a61eb6416d80033a93a0160cc207687d922c90f7f97c1450cdbacad8d87b1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d553f8ece5b740fe28d07fe297aa0bb3479df62c12e45b84fbd85db04c417aeb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__124db6cda09dab6b502dd846fc5c76a89dddbb499c37edc4401b3edf56227676(
    value: typing.Optional[OrgPolicyPolicyDryRunSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16d5cc38c5c82d0dd1800c218eb9459f9d678fcb9b0249b9cfc74b3693a53ad4(
    *,
    allow_all: typing.Optional[builtins.str] = None,
    condition: typing.Optional[typing.Union[OrgPolicyPolicyDryRunSpecRulesCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    deny_all: typing.Optional[builtins.str] = None,
    enforce: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Union[OrgPolicyPolicyDryRunSpecRulesValues, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5edc41838bdef7879d525e6883475261a396442b5d0daec93f47c3d5462ee91f(
    *,
    description: typing.Optional[builtins.str] = None,
    expression: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfc3adcfb6be04ee9814af7466d96e89af9e71930b1b97ad8559b3ef8c3e10d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3be4fb08f74585bf19f8a40c1dcdca954d26766102452af47e7f3e662147b155(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64106aac88e39736444280089c8d4cb8c1dba7e60eb2745c8cfadc99c5446ef6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e6e1c5e1ae858176c2a9baaca44efac4e4a6216c40077461d3739ae9beebcd6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e56f091f8cdd1f8f9e8b180c30f503678d51a8c3ad67a495d9b4b3338e3f496(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f52e5d00ed95a843a00413aeb8ff0c421ab55917f571380fde5c262e051ef15d(
    value: typing.Optional[OrgPolicyPolicyDryRunSpecRulesCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7387491aca5a3846126a15da4b7154c19f48ca76351bb9fd42512b8c9d9bdf54(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39e9764f1b4c1ba70129e23dc4ccafbbec9e84e64e863519711040899b6e7b75(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d96a828a01dad33d00c5047d13ddb42d79765254698fc54b88e5d5c73a1e1833(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdd2a1bb7ce3a5883de4ee29e3051076320ecd03405983725824d1b353790516(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__292868eceb2ab74777e299d7e0c1100768fb6bcc5c65a7c88c383b67cfd9ff82(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f003ed77c86784738cc08bfb1733557dac041535ce3e35b1ecb5bd00e8462a0c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrgPolicyPolicyDryRunSpecRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__672f6744acd7e30322de73370f8b43778b7f0583b4c1d8d11caffd86bc4e60d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc925ea0e57d1d4fc02b00aeedbef2fb8f0560d8c6f10e6d1dd7a91131e48325(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e7d60349c4b90ec5979eb8af6dc7ce5a5954e1b0c91c19d90ecd7073babbf69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c760d5923ced0fbb8f4642c570cbfbf678a147ea6972b1a1e6215f8ad112352(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b900ffe3a74b755c135e8341ee831787741c4ead00084ce8720f7f3fe683627(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64fd808271b28714f75076c45909fdb8f629d7bb4b17830482234188d2956ca3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrgPolicyPolicyDryRunSpecRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6072c9be1ae8b808df3f4c04a4409f76840acf0613eb56ca84f9a2dab9fbabb(
    *,
    allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    denied_values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0fb563c623afdd58e7e1e1dcff56f350ea15028fd2c7aa4829ae0e8bea9af0c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a3649c1fc6fcadd19a941d7c79bc082268183eec27eb89b4bc3c54fac817c50(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8370ba6baaf00219538eb74bfdd5940b537ebb21ebb0d69f9856ea97d164c38e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cd553078807478a29bbb9076d06825f0f675bfdf8260f23c852e9c448a2b888(
    value: typing.Optional[OrgPolicyPolicyDryRunSpecRulesValues],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21b56320ff38a215e9cd5d7fa04e70409e5b8744c7c495869e9861c973b416da(
    *,
    inherit_from_parent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    reset: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrgPolicyPolicySpecRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddb07da617f2cc87cb636ac81a096981dfdceba15b6f92de18c5729a6f721dee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0ee326139b88ff7f50f886f778ffa95a4c0513c3b1bc5b59241f5d112cf1229(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrgPolicyPolicySpecRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fd02d0a3f746d92bc09f17712585879f6112921f6d2f202ab98cf791c65c502(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b463bed25ba5d36229195236153dcbe65b12b48496e283d574fea03b6a3dc666(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea02ee2a2eef1d8ec2c75f50485944e39d8f7a6041c77444297dadafc7380d08(
    value: typing.Optional[OrgPolicyPolicySpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49b82ba79f6ace37456eef93057ed699b0f881abe835506661de58836f5f1e08(
    *,
    allow_all: typing.Optional[builtins.str] = None,
    condition: typing.Optional[typing.Union[OrgPolicyPolicySpecRulesCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    deny_all: typing.Optional[builtins.str] = None,
    enforce: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Union[OrgPolicyPolicySpecRulesValues, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bafea799a9852424a8b6474db5e94615a2be57bf8bf69423c4e25fda83210d9(
    *,
    description: typing.Optional[builtins.str] = None,
    expression: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d632d22acaa005d559c4fc062c90603c709e841fa5984915748dcb71fc9df41a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f76e1c845ce28a8e2c363abd5515076fb94cd76a56efd593e51adceecdcf6582(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3481657cac54fa6aaf3e67151c66e4a62bcf3483c08d6e2b82219d96c353abd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08b23573b5b3f5a521ba5839589a67c4d4c3507ccc52056d5bcd21d1d608ea48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dcf5705cf8254cee25f2941a4a810e606a02597c427f2e9d4c9aa6671f3391b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd80cbb1becee5ba15abc3aac8515e03bcac9d0eca51124d057694ab085e0a3a(
    value: typing.Optional[OrgPolicyPolicySpecRulesCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5ebb0ae3ad125b2275c766bba6478509d86e14e19fa7ca83e1bd60cace2ab2c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aeb1c91da8ed87f4905f374a11b0d406ed4c94a1b15e32c3b9829aa768b28ab(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbcc04acca85c24094893e4ec18be1765d21a0b1b2fa920b674dfc4a57033641(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6489d58baa00f47518e0eded4376cc042ba33b4e538993531a8f41cf2d067962(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e062f2fabf09af1a6e6a49a02048963c595418b6dfb3b9a086e06f14633d5b0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0429670686c492347752203bb5c888e2647cce3cb9d27479ef3e33284ca206d2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrgPolicyPolicySpecRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ebdbf8465a50e47169dea02e1111fe3b0a218ad7bc7b1ac567acc1a7c1b8b2e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f69a0cdf3663360d6f6e61dfeae83baeb8bf48b09a27cf5ed438594270e35b10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e763800f8deebb49fe07a5bd25b01044ed289eeb7b92428b03949ab00979f7fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8176eab81064a71c8d37139f7b7b5565d4d4e584edc6d9fc5007b88d70955a51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95598abbbf51a7571555df2269428a437337b7f0a039c111fad145982cecde00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3baf05f28a7868b69dd2165aba0a3ec03df0c6168312c31b99e5cdc009cb1b9d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrgPolicyPolicySpecRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccb0ca968f946c1cedcea81e3b8b63d04e2d445d1d344f8b1825c2a80413a2a8(
    *,
    allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    denied_values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f0ff6ba4d5524e490539726aa50de07e38e2fb5f05779ea62b8d1b9342e55ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f782a3e3b76632462af233dd6a3c4564f3cd8c4f208481d5f47c761ce473d00(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1022751e132f4945603a1630d18a605a6c6019d00881288ec4431798da0a56bc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b102b43b0262313c0d63f0f53a5c336d1fc2b0c2830e192934b3055f7f62930(
    value: typing.Optional[OrgPolicyPolicySpecRulesValues],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__806c60ad99258d7048cb931403c2f954076638317f1c744104d44ba7833b381b(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0c31ba141fe21b6a73a679d281ae863c2c12fdf07f155a269247ce749b6f84f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a5f16bab8463136d8549846937c030dad6f1e814f98bfd07230dbeb654cee7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd45fa0c7818f888db0b5327f506e1190288dd997ef4f10f2856d6c8850984c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35312249f301a6d7be319a2dfa0da15fa229660838718adec17caa4b0bcf879e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91ee61e1bacec1f713dc1849d88d5c09af8ec9944fde76168254f6f82e688ac4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrgPolicyPolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
