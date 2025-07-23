r'''
# `google_binary_authorization_policy`

Refer to the Terraform Registry for docs: [`google_binary_authorization_policy`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy).
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


class BinaryAuthorizationPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.binaryAuthorizationPolicy.BinaryAuthorizationPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy google_binary_authorization_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        default_admission_rule: typing.Union["BinaryAuthorizationPolicyDefaultAdmissionRule", typing.Dict[builtins.str, typing.Any]],
        admission_whitelist_patterns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BinaryAuthorizationPolicyAdmissionWhitelistPatterns", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cluster_admission_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BinaryAuthorizationPolicyClusterAdmissionRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        global_policy_evaluation_mode: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BinaryAuthorizationPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy google_binary_authorization_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param default_admission_rule: default_admission_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#default_admission_rule BinaryAuthorizationPolicy#default_admission_rule}
        :param admission_whitelist_patterns: admission_whitelist_patterns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#admission_whitelist_patterns BinaryAuthorizationPolicy#admission_whitelist_patterns}
        :param cluster_admission_rules: cluster_admission_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#cluster_admission_rules BinaryAuthorizationPolicy#cluster_admission_rules}
        :param description: A descriptive comment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#description BinaryAuthorizationPolicy#description}
        :param global_policy_evaluation_mode: Controls the evaluation of a Google-maintained global admission policy for common system-level images. Images not covered by the global policy will be subject to the project admission policy. Possible values: ["ENABLE", "DISABLE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#global_policy_evaluation_mode BinaryAuthorizationPolicy#global_policy_evaluation_mode}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#id BinaryAuthorizationPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#project BinaryAuthorizationPolicy#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#timeouts BinaryAuthorizationPolicy#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56f27d08df74208f3d42509af466b0f4424d30f4c9726c6a72e57abd69066809)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BinaryAuthorizationPolicyConfig(
            default_admission_rule=default_admission_rule,
            admission_whitelist_patterns=admission_whitelist_patterns,
            cluster_admission_rules=cluster_admission_rules,
            description=description,
            global_policy_evaluation_mode=global_policy_evaluation_mode,
            id=id,
            project=project,
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
        '''Generates CDKTF code for importing a BinaryAuthorizationPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BinaryAuthorizationPolicy to import.
        :param import_from_id: The id of the existing BinaryAuthorizationPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BinaryAuthorizationPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc2b07bbdd6cb5ca67652ef422a7b918482631cc1cf6710cd9668452b33bbf45)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAdmissionWhitelistPatterns")
    def put_admission_whitelist_patterns(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BinaryAuthorizationPolicyAdmissionWhitelistPatterns", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1417e6a0d0c565ed2607f409b297c9b895f867c1819921a58dda7c7c7d331268)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdmissionWhitelistPatterns", [value]))

    @jsii.member(jsii_name="putClusterAdmissionRules")
    def put_cluster_admission_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BinaryAuthorizationPolicyClusterAdmissionRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__479faa2ecb48bd60212d2a556493be3b7b8052fae2393ccf4b9ac28419a3c430)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putClusterAdmissionRules", [value]))

    @jsii.member(jsii_name="putDefaultAdmissionRule")
    def put_default_admission_rule(
        self,
        *,
        enforcement_mode: builtins.str,
        evaluation_mode: builtins.str,
        require_attestations_by: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param enforcement_mode: The action when a pod creation is denied by the admission rule. Possible values: ["ENFORCED_BLOCK_AND_AUDIT_LOG", "DRYRUN_AUDIT_LOG_ONLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#enforcement_mode BinaryAuthorizationPolicy#enforcement_mode}
        :param evaluation_mode: How this admission rule will be evaluated. Possible values: ["ALWAYS_ALLOW", "REQUIRE_ATTESTATION", "ALWAYS_DENY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#evaluation_mode BinaryAuthorizationPolicy#evaluation_mode}
        :param require_attestations_by: The resource names of the attestors that must attest to a container image. If the attestor is in a different project from the policy, it should be specified in the format 'projects/* /attestors/*'. Each attestor must exist before a policy can reference it. To add an attestor to a policy the principal issuing the policy change request must be able to read the attestor resource. Note: this field must be non-empty when the evaluation_mode field specifies REQUIRE_ATTESTATION, otherwise it must be empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#require_attestations_by BinaryAuthorizationPolicy#require_attestations_by} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = BinaryAuthorizationPolicyDefaultAdmissionRule(
            enforcement_mode=enforcement_mode,
            evaluation_mode=evaluation_mode,
            require_attestations_by=require_attestations_by,
        )

        return typing.cast(None, jsii.invoke(self, "putDefaultAdmissionRule", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#create BinaryAuthorizationPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#delete BinaryAuthorizationPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#update BinaryAuthorizationPolicy#update}.
        '''
        value = BinaryAuthorizationPolicyTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAdmissionWhitelistPatterns")
    def reset_admission_whitelist_patterns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdmissionWhitelistPatterns", []))

    @jsii.member(jsii_name="resetClusterAdmissionRules")
    def reset_cluster_admission_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterAdmissionRules", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetGlobalPolicyEvaluationMode")
    def reset_global_policy_evaluation_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGlobalPolicyEvaluationMode", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

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
    @jsii.member(jsii_name="admissionWhitelistPatterns")
    def admission_whitelist_patterns(
        self,
    ) -> "BinaryAuthorizationPolicyAdmissionWhitelistPatternsList":
        return typing.cast("BinaryAuthorizationPolicyAdmissionWhitelistPatternsList", jsii.get(self, "admissionWhitelistPatterns"))

    @builtins.property
    @jsii.member(jsii_name="clusterAdmissionRules")
    def cluster_admission_rules(
        self,
    ) -> "BinaryAuthorizationPolicyClusterAdmissionRulesList":
        return typing.cast("BinaryAuthorizationPolicyClusterAdmissionRulesList", jsii.get(self, "clusterAdmissionRules"))

    @builtins.property
    @jsii.member(jsii_name="defaultAdmissionRule")
    def default_admission_rule(
        self,
    ) -> "BinaryAuthorizationPolicyDefaultAdmissionRuleOutputReference":
        return typing.cast("BinaryAuthorizationPolicyDefaultAdmissionRuleOutputReference", jsii.get(self, "defaultAdmissionRule"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "BinaryAuthorizationPolicyTimeoutsOutputReference":
        return typing.cast("BinaryAuthorizationPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="admissionWhitelistPatternsInput")
    def admission_whitelist_patterns_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BinaryAuthorizationPolicyAdmissionWhitelistPatterns"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BinaryAuthorizationPolicyAdmissionWhitelistPatterns"]]], jsii.get(self, "admissionWhitelistPatternsInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterAdmissionRulesInput")
    def cluster_admission_rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BinaryAuthorizationPolicyClusterAdmissionRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BinaryAuthorizationPolicyClusterAdmissionRules"]]], jsii.get(self, "clusterAdmissionRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultAdmissionRuleInput")
    def default_admission_rule_input(
        self,
    ) -> typing.Optional["BinaryAuthorizationPolicyDefaultAdmissionRule"]:
        return typing.cast(typing.Optional["BinaryAuthorizationPolicyDefaultAdmissionRule"], jsii.get(self, "defaultAdmissionRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="globalPolicyEvaluationModeInput")
    def global_policy_evaluation_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "globalPolicyEvaluationModeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BinaryAuthorizationPolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BinaryAuthorizationPolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1c3e4a74226957e28af5c6cd87e15ea6731a9dd40ef6e8db6b75966d9778120)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="globalPolicyEvaluationMode")
    def global_policy_evaluation_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "globalPolicyEvaluationMode"))

    @global_policy_evaluation_mode.setter
    def global_policy_evaluation_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ad1d4ae7c6d5ea90353f0d1df52420938bc479d51a1d06f3a997eab2bef8741)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "globalPolicyEvaluationMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c41952953d983e2ca443d00a077e7afa9b664e56ab9a52fef5076736b562e4d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e7feed5cf4dce331a3965e6ca09e72305e1e63d08572a055f5ac27af563897a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.binaryAuthorizationPolicy.BinaryAuthorizationPolicyAdmissionWhitelistPatterns",
    jsii_struct_bases=[],
    name_mapping={"name_pattern": "namePattern"},
)
class BinaryAuthorizationPolicyAdmissionWhitelistPatterns:
    def __init__(self, *, name_pattern: builtins.str) -> None:
        '''
        :param name_pattern: An image name pattern to whitelist, in the form 'registry/path/to/image'. This supports a trailing * as a wildcard, but this is allowed only in text after the registry/ part. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#name_pattern BinaryAuthorizationPolicy#name_pattern}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ca8565e71f5bb795188633f3143268e63f30774646cc2ca1a6dbc2f16075bb6)
            check_type(argname="argument name_pattern", value=name_pattern, expected_type=type_hints["name_pattern"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name_pattern": name_pattern,
        }

    @builtins.property
    def name_pattern(self) -> builtins.str:
        '''An image name pattern to whitelist, in the form 'registry/path/to/image'.

        This supports a trailing * as a
        wildcard, but this is allowed only in text after the registry/
        part.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#name_pattern BinaryAuthorizationPolicy#name_pattern}
        '''
        result = self._values.get("name_pattern")
        assert result is not None, "Required property 'name_pattern' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BinaryAuthorizationPolicyAdmissionWhitelistPatterns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BinaryAuthorizationPolicyAdmissionWhitelistPatternsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.binaryAuthorizationPolicy.BinaryAuthorizationPolicyAdmissionWhitelistPatternsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6723a104a959995da923acab7dfce85b43e81b95090b921bbf3c48499261dc3a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BinaryAuthorizationPolicyAdmissionWhitelistPatternsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb61fa9583d324736df7dcd30c9ae94e8203cfc8e3edf71c16fabd9ac2e5cac3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BinaryAuthorizationPolicyAdmissionWhitelistPatternsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d5f14b2ed6b195c0e6dec3f21d84cbf4a697d37f387c9894dc7efa60da47370)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a20db54ec2dc98a81c4ae0f52791a651ca6d4eefeed03b0cb71960f13abcead)
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
            type_hints = typing.get_type_hints(_typecheckingstub__909cc6ae5233b3323f68eaef85209ad85faf6e5a4a3f8fc8f61a952b166cf39f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BinaryAuthorizationPolicyAdmissionWhitelistPatterns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BinaryAuthorizationPolicyAdmissionWhitelistPatterns]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BinaryAuthorizationPolicyAdmissionWhitelistPatterns]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89541ea40f771cae45c12bba1119a04b0cfd81d2efe6d0d8fb654c173877fb01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BinaryAuthorizationPolicyAdmissionWhitelistPatternsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.binaryAuthorizationPolicy.BinaryAuthorizationPolicyAdmissionWhitelistPatternsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db9abc5a3ade2ad5efe89e0a80712f8d5bbe3bb76a1835a5f67e66fcc86ca6b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="namePatternInput")
    def name_pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namePatternInput"))

    @builtins.property
    @jsii.member(jsii_name="namePattern")
    def name_pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namePattern"))

    @name_pattern.setter
    def name_pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78477a3a3a76422d127225001bf82da49d7a7a8f97bee54bc28849a243cf6773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namePattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BinaryAuthorizationPolicyAdmissionWhitelistPatterns]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BinaryAuthorizationPolicyAdmissionWhitelistPatterns]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BinaryAuthorizationPolicyAdmissionWhitelistPatterns]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e8f415db83caafc678bf5d4424c559da94ac8d32c921668295550717d125d11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.binaryAuthorizationPolicy.BinaryAuthorizationPolicyClusterAdmissionRules",
    jsii_struct_bases=[],
    name_mapping={
        "cluster": "cluster",
        "enforcement_mode": "enforcementMode",
        "evaluation_mode": "evaluationMode",
        "require_attestations_by": "requireAttestationsBy",
    },
)
class BinaryAuthorizationPolicyClusterAdmissionRules:
    def __init__(
        self,
        *,
        cluster: builtins.str,
        enforcement_mode: builtins.str,
        evaluation_mode: builtins.str,
        require_attestations_by: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param cluster: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#cluster BinaryAuthorizationPolicy#cluster}.
        :param enforcement_mode: The action when a pod creation is denied by the admission rule. Possible values: ["ENFORCED_BLOCK_AND_AUDIT_LOG", "DRYRUN_AUDIT_LOG_ONLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#enforcement_mode BinaryAuthorizationPolicy#enforcement_mode}
        :param evaluation_mode: How this admission rule will be evaluated. Possible values: ["ALWAYS_ALLOW", "REQUIRE_ATTESTATION", "ALWAYS_DENY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#evaluation_mode BinaryAuthorizationPolicy#evaluation_mode}
        :param require_attestations_by: The resource names of the attestors that must attest to a container image. If the attestor is in a different project from the policy, it should be specified in the format 'projects/* /attestors/*'. Each attestor must exist before a policy can reference it. To add an attestor to a policy the principal issuing the policy change request must be able to read the attestor resource. Note: this field must be non-empty when the evaluation_mode field specifies REQUIRE_ATTESTATION, otherwise it must be empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#require_attestations_by BinaryAuthorizationPolicy#require_attestations_by} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c8aa7c694919a370114660f80cd8afb8d1a78bafe0ede84f0b4b87bc05254f3)
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument enforcement_mode", value=enforcement_mode, expected_type=type_hints["enforcement_mode"])
            check_type(argname="argument evaluation_mode", value=evaluation_mode, expected_type=type_hints["evaluation_mode"])
            check_type(argname="argument require_attestations_by", value=require_attestations_by, expected_type=type_hints["require_attestations_by"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster": cluster,
            "enforcement_mode": enforcement_mode,
            "evaluation_mode": evaluation_mode,
        }
        if require_attestations_by is not None:
            self._values["require_attestations_by"] = require_attestations_by

    @builtins.property
    def cluster(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#cluster BinaryAuthorizationPolicy#cluster}.'''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enforcement_mode(self) -> builtins.str:
        '''The action when a pod creation is denied by the admission rule. Possible values: ["ENFORCED_BLOCK_AND_AUDIT_LOG", "DRYRUN_AUDIT_LOG_ONLY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#enforcement_mode BinaryAuthorizationPolicy#enforcement_mode}
        '''
        result = self._values.get("enforcement_mode")
        assert result is not None, "Required property 'enforcement_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def evaluation_mode(self) -> builtins.str:
        '''How this admission rule will be evaluated. Possible values: ["ALWAYS_ALLOW", "REQUIRE_ATTESTATION", "ALWAYS_DENY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#evaluation_mode BinaryAuthorizationPolicy#evaluation_mode}
        '''
        result = self._values.get("evaluation_mode")
        assert result is not None, "Required property 'evaluation_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def require_attestations_by(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The resource names of the attestors that must attest to a container image.

        If the attestor is in a different project from the
        policy, it should be specified in the format 'projects/* /attestors/*'.
        Each attestor must exist before a policy can reference it. To add an
        attestor to a policy the principal issuing the policy change
        request must be able to read the attestor resource.

        Note: this field must be non-empty when the evaluation_mode field
        specifies REQUIRE_ATTESTATION, otherwise it must be empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#require_attestations_by BinaryAuthorizationPolicy#require_attestations_by}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("require_attestations_by")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BinaryAuthorizationPolicyClusterAdmissionRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BinaryAuthorizationPolicyClusterAdmissionRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.binaryAuthorizationPolicy.BinaryAuthorizationPolicyClusterAdmissionRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0e41fd1593c912ce49f5c0919dfa0db7eef9162306f9a1c46ee323787961b9c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BinaryAuthorizationPolicyClusterAdmissionRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edc5a94ba2d98443324e0d16ec5f14104301f83d99ddafb9b5366f14f624be44)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BinaryAuthorizationPolicyClusterAdmissionRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e97c9af5fa59964af4578971eab783a12a94ec1ba69b0993775d216c210eb186)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c402edbe6959bc02f3c6b23cce43835ebf2d489d10fcd62ad700e2ecbd7799d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__749d21f9bea1be47c5ed71d2e61c8f0060ef7130015b902b9e56fcdc821da0d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BinaryAuthorizationPolicyClusterAdmissionRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BinaryAuthorizationPolicyClusterAdmissionRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BinaryAuthorizationPolicyClusterAdmissionRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6da19e1317b79bb7b63935ac15e637ed56c87898a70ce4d560d86723ac28f303)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BinaryAuthorizationPolicyClusterAdmissionRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.binaryAuthorizationPolicy.BinaryAuthorizationPolicyClusterAdmissionRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__87590698a3ae41221b9516b0d983277b799f2f0ace56d98e31378b96ce4eaaab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetRequireAttestationsBy")
    def reset_require_attestations_by(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireAttestationsBy", []))

    @builtins.property
    @jsii.member(jsii_name="clusterInput")
    def cluster_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterInput"))

    @builtins.property
    @jsii.member(jsii_name="enforcementModeInput")
    def enforcement_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enforcementModeInput"))

    @builtins.property
    @jsii.member(jsii_name="evaluationModeInput")
    def evaluation_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "evaluationModeInput"))

    @builtins.property
    @jsii.member(jsii_name="requireAttestationsByInput")
    def require_attestations_by_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "requireAttestationsByInput"))

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cluster"))

    @cluster.setter
    def cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d27337a1c0c93f4c6e7ddeac833ed1adaf87b215760b225471f6a79404f9250)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforcementMode")
    def enforcement_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enforcementMode"))

    @enforcement_mode.setter
    def enforcement_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00f3e9bb65996c2e717296dad7e6b55d986eb546eb453617f1beec3d33ecd2ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforcementMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="evaluationMode")
    def evaluation_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "evaluationMode"))

    @evaluation_mode.setter
    def evaluation_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a804c89ee55ec418fb6897169f173413f344fda03000b1dadddedba181e49f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "evaluationMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireAttestationsBy")
    def require_attestations_by(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "requireAttestationsBy"))

    @require_attestations_by.setter
    def require_attestations_by(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4e6be9bbe6b70064a851f44cd14e310a3aa67ed5fcb61001f0c64a7a41ae065)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireAttestationsBy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BinaryAuthorizationPolicyClusterAdmissionRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BinaryAuthorizationPolicyClusterAdmissionRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BinaryAuthorizationPolicyClusterAdmissionRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92bbdf6b84a65b9a2766dae2d8fe14d65e21676a3123fef1736aa217d3ad317c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.binaryAuthorizationPolicy.BinaryAuthorizationPolicyConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "default_admission_rule": "defaultAdmissionRule",
        "admission_whitelist_patterns": "admissionWhitelistPatterns",
        "cluster_admission_rules": "clusterAdmissionRules",
        "description": "description",
        "global_policy_evaluation_mode": "globalPolicyEvaluationMode",
        "id": "id",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class BinaryAuthorizationPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        default_admission_rule: typing.Union["BinaryAuthorizationPolicyDefaultAdmissionRule", typing.Dict[builtins.str, typing.Any]],
        admission_whitelist_patterns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BinaryAuthorizationPolicyAdmissionWhitelistPatterns, typing.Dict[builtins.str, typing.Any]]]]] = None,
        cluster_admission_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BinaryAuthorizationPolicyClusterAdmissionRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        global_policy_evaluation_mode: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BinaryAuthorizationPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param default_admission_rule: default_admission_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#default_admission_rule BinaryAuthorizationPolicy#default_admission_rule}
        :param admission_whitelist_patterns: admission_whitelist_patterns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#admission_whitelist_patterns BinaryAuthorizationPolicy#admission_whitelist_patterns}
        :param cluster_admission_rules: cluster_admission_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#cluster_admission_rules BinaryAuthorizationPolicy#cluster_admission_rules}
        :param description: A descriptive comment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#description BinaryAuthorizationPolicy#description}
        :param global_policy_evaluation_mode: Controls the evaluation of a Google-maintained global admission policy for common system-level images. Images not covered by the global policy will be subject to the project admission policy. Possible values: ["ENABLE", "DISABLE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#global_policy_evaluation_mode BinaryAuthorizationPolicy#global_policy_evaluation_mode}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#id BinaryAuthorizationPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#project BinaryAuthorizationPolicy#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#timeouts BinaryAuthorizationPolicy#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(default_admission_rule, dict):
            default_admission_rule = BinaryAuthorizationPolicyDefaultAdmissionRule(**default_admission_rule)
        if isinstance(timeouts, dict):
            timeouts = BinaryAuthorizationPolicyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1561fd3bc8681a5e4810109217dd14205d26f7e381d9d04bf461de10f3c6aa7d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument default_admission_rule", value=default_admission_rule, expected_type=type_hints["default_admission_rule"])
            check_type(argname="argument admission_whitelist_patterns", value=admission_whitelist_patterns, expected_type=type_hints["admission_whitelist_patterns"])
            check_type(argname="argument cluster_admission_rules", value=cluster_admission_rules, expected_type=type_hints["cluster_admission_rules"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument global_policy_evaluation_mode", value=global_policy_evaluation_mode, expected_type=type_hints["global_policy_evaluation_mode"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_admission_rule": default_admission_rule,
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
        if admission_whitelist_patterns is not None:
            self._values["admission_whitelist_patterns"] = admission_whitelist_patterns
        if cluster_admission_rules is not None:
            self._values["cluster_admission_rules"] = cluster_admission_rules
        if description is not None:
            self._values["description"] = description
        if global_policy_evaluation_mode is not None:
            self._values["global_policy_evaluation_mode"] = global_policy_evaluation_mode
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
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
    def default_admission_rule(self) -> "BinaryAuthorizationPolicyDefaultAdmissionRule":
        '''default_admission_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#default_admission_rule BinaryAuthorizationPolicy#default_admission_rule}
        '''
        result = self._values.get("default_admission_rule")
        assert result is not None, "Required property 'default_admission_rule' is missing"
        return typing.cast("BinaryAuthorizationPolicyDefaultAdmissionRule", result)

    @builtins.property
    def admission_whitelist_patterns(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BinaryAuthorizationPolicyAdmissionWhitelistPatterns]]]:
        '''admission_whitelist_patterns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#admission_whitelist_patterns BinaryAuthorizationPolicy#admission_whitelist_patterns}
        '''
        result = self._values.get("admission_whitelist_patterns")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BinaryAuthorizationPolicyAdmissionWhitelistPatterns]]], result)

    @builtins.property
    def cluster_admission_rules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BinaryAuthorizationPolicyClusterAdmissionRules]]]:
        '''cluster_admission_rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#cluster_admission_rules BinaryAuthorizationPolicy#cluster_admission_rules}
        '''
        result = self._values.get("cluster_admission_rules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BinaryAuthorizationPolicyClusterAdmissionRules]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A descriptive comment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#description BinaryAuthorizationPolicy#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def global_policy_evaluation_mode(self) -> typing.Optional[builtins.str]:
        '''Controls the evaluation of a Google-maintained global admission policy for common system-level images.

        Images not covered by the global
        policy will be subject to the project admission policy. Possible values: ["ENABLE", "DISABLE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#global_policy_evaluation_mode BinaryAuthorizationPolicy#global_policy_evaluation_mode}
        '''
        result = self._values.get("global_policy_evaluation_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#id BinaryAuthorizationPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#project BinaryAuthorizationPolicy#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["BinaryAuthorizationPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#timeouts BinaryAuthorizationPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["BinaryAuthorizationPolicyTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BinaryAuthorizationPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.binaryAuthorizationPolicy.BinaryAuthorizationPolicyDefaultAdmissionRule",
    jsii_struct_bases=[],
    name_mapping={
        "enforcement_mode": "enforcementMode",
        "evaluation_mode": "evaluationMode",
        "require_attestations_by": "requireAttestationsBy",
    },
)
class BinaryAuthorizationPolicyDefaultAdmissionRule:
    def __init__(
        self,
        *,
        enforcement_mode: builtins.str,
        evaluation_mode: builtins.str,
        require_attestations_by: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param enforcement_mode: The action when a pod creation is denied by the admission rule. Possible values: ["ENFORCED_BLOCK_AND_AUDIT_LOG", "DRYRUN_AUDIT_LOG_ONLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#enforcement_mode BinaryAuthorizationPolicy#enforcement_mode}
        :param evaluation_mode: How this admission rule will be evaluated. Possible values: ["ALWAYS_ALLOW", "REQUIRE_ATTESTATION", "ALWAYS_DENY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#evaluation_mode BinaryAuthorizationPolicy#evaluation_mode}
        :param require_attestations_by: The resource names of the attestors that must attest to a container image. If the attestor is in a different project from the policy, it should be specified in the format 'projects/* /attestors/*'. Each attestor must exist before a policy can reference it. To add an attestor to a policy the principal issuing the policy change request must be able to read the attestor resource. Note: this field must be non-empty when the evaluation_mode field specifies REQUIRE_ATTESTATION, otherwise it must be empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#require_attestations_by BinaryAuthorizationPolicy#require_attestations_by} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e1652c545fc81d3313cdd8c48f72768e75cefa42fd2c7f55576d9041454ea12)
            check_type(argname="argument enforcement_mode", value=enforcement_mode, expected_type=type_hints["enforcement_mode"])
            check_type(argname="argument evaluation_mode", value=evaluation_mode, expected_type=type_hints["evaluation_mode"])
            check_type(argname="argument require_attestations_by", value=require_attestations_by, expected_type=type_hints["require_attestations_by"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enforcement_mode": enforcement_mode,
            "evaluation_mode": evaluation_mode,
        }
        if require_attestations_by is not None:
            self._values["require_attestations_by"] = require_attestations_by

    @builtins.property
    def enforcement_mode(self) -> builtins.str:
        '''The action when a pod creation is denied by the admission rule. Possible values: ["ENFORCED_BLOCK_AND_AUDIT_LOG", "DRYRUN_AUDIT_LOG_ONLY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#enforcement_mode BinaryAuthorizationPolicy#enforcement_mode}
        '''
        result = self._values.get("enforcement_mode")
        assert result is not None, "Required property 'enforcement_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def evaluation_mode(self) -> builtins.str:
        '''How this admission rule will be evaluated. Possible values: ["ALWAYS_ALLOW", "REQUIRE_ATTESTATION", "ALWAYS_DENY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#evaluation_mode BinaryAuthorizationPolicy#evaluation_mode}
        '''
        result = self._values.get("evaluation_mode")
        assert result is not None, "Required property 'evaluation_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def require_attestations_by(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The resource names of the attestors that must attest to a container image.

        If the attestor is in a different project from the
        policy, it should be specified in the format 'projects/* /attestors/*'.
        Each attestor must exist before a policy can reference it. To add an
        attestor to a policy the principal issuing the policy change
        request must be able to read the attestor resource.

        Note: this field must be non-empty when the evaluation_mode field
        specifies REQUIRE_ATTESTATION, otherwise it must be empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#require_attestations_by BinaryAuthorizationPolicy#require_attestations_by}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("require_attestations_by")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BinaryAuthorizationPolicyDefaultAdmissionRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BinaryAuthorizationPolicyDefaultAdmissionRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.binaryAuthorizationPolicy.BinaryAuthorizationPolicyDefaultAdmissionRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb52e7b655a4a924d142e9d343b7639afff827d2c8ab4e6d1d091e45ec66e547)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRequireAttestationsBy")
    def reset_require_attestations_by(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireAttestationsBy", []))

    @builtins.property
    @jsii.member(jsii_name="enforcementModeInput")
    def enforcement_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enforcementModeInput"))

    @builtins.property
    @jsii.member(jsii_name="evaluationModeInput")
    def evaluation_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "evaluationModeInput"))

    @builtins.property
    @jsii.member(jsii_name="requireAttestationsByInput")
    def require_attestations_by_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "requireAttestationsByInput"))

    @builtins.property
    @jsii.member(jsii_name="enforcementMode")
    def enforcement_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enforcementMode"))

    @enforcement_mode.setter
    def enforcement_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a51d55ef0b36e095ad313fedbc893aa184e220221d9e8e59ac70e40ac96ca90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforcementMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="evaluationMode")
    def evaluation_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "evaluationMode"))

    @evaluation_mode.setter
    def evaluation_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a71022b376a86a39c3e585d75632dad12e4158b0bff275774cdb97e721a116c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "evaluationMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireAttestationsBy")
    def require_attestations_by(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "requireAttestationsBy"))

    @require_attestations_by.setter
    def require_attestations_by(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8c0dcdaa68d34a06f45afe98870807e85901c98435d1789dfb05d79999e8e80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireAttestationsBy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BinaryAuthorizationPolicyDefaultAdmissionRule]:
        return typing.cast(typing.Optional[BinaryAuthorizationPolicyDefaultAdmissionRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BinaryAuthorizationPolicyDefaultAdmissionRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0946d7043f8b4583d5db82e8e035598264d6c560d61e136cc628bcd6dfbf9589)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.binaryAuthorizationPolicy.BinaryAuthorizationPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class BinaryAuthorizationPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#create BinaryAuthorizationPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#delete BinaryAuthorizationPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#update BinaryAuthorizationPolicy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52452c27a0658ebb40e71befc8a071f072a0ea899235280905b4bfca573c3f95)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#create BinaryAuthorizationPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#delete BinaryAuthorizationPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_policy#update BinaryAuthorizationPolicy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BinaryAuthorizationPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BinaryAuthorizationPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.binaryAuthorizationPolicy.BinaryAuthorizationPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__869ebeb86c78c41d21dc208c8a42734948e751868290a12f17857fbd43e4ee4b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ce96c72b12d798a0a2708a303ead4289325570d1b5d5996bd22654f32843767)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f658b4e8c23cc26042655bae43fe8265ea225c9364ea9b47e15ef0449707bd1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abc2e38bef2b92ec6afd2fc8562736af00318de10dc3e644e84d381b59918682)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BinaryAuthorizationPolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BinaryAuthorizationPolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BinaryAuthorizationPolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6b0aef0a766ee512e9e4cb8a96887ccfb42ccea579566bf42ffad9b76be78e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BinaryAuthorizationPolicy",
    "BinaryAuthorizationPolicyAdmissionWhitelistPatterns",
    "BinaryAuthorizationPolicyAdmissionWhitelistPatternsList",
    "BinaryAuthorizationPolicyAdmissionWhitelistPatternsOutputReference",
    "BinaryAuthorizationPolicyClusterAdmissionRules",
    "BinaryAuthorizationPolicyClusterAdmissionRulesList",
    "BinaryAuthorizationPolicyClusterAdmissionRulesOutputReference",
    "BinaryAuthorizationPolicyConfig",
    "BinaryAuthorizationPolicyDefaultAdmissionRule",
    "BinaryAuthorizationPolicyDefaultAdmissionRuleOutputReference",
    "BinaryAuthorizationPolicyTimeouts",
    "BinaryAuthorizationPolicyTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__56f27d08df74208f3d42509af466b0f4424d30f4c9726c6a72e57abd69066809(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    default_admission_rule: typing.Union[BinaryAuthorizationPolicyDefaultAdmissionRule, typing.Dict[builtins.str, typing.Any]],
    admission_whitelist_patterns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BinaryAuthorizationPolicyAdmissionWhitelistPatterns, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cluster_admission_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BinaryAuthorizationPolicyClusterAdmissionRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    global_policy_evaluation_mode: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[BinaryAuthorizationPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__bc2b07bbdd6cb5ca67652ef422a7b918482631cc1cf6710cd9668452b33bbf45(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1417e6a0d0c565ed2607f409b297c9b895f867c1819921a58dda7c7c7d331268(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BinaryAuthorizationPolicyAdmissionWhitelistPatterns, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__479faa2ecb48bd60212d2a556493be3b7b8052fae2393ccf4b9ac28419a3c430(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BinaryAuthorizationPolicyClusterAdmissionRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1c3e4a74226957e28af5c6cd87e15ea6731a9dd40ef6e8db6b75966d9778120(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ad1d4ae7c6d5ea90353f0d1df52420938bc479d51a1d06f3a997eab2bef8741(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c41952953d983e2ca443d00a077e7afa9b664e56ab9a52fef5076736b562e4d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e7feed5cf4dce331a3965e6ca09e72305e1e63d08572a055f5ac27af563897a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ca8565e71f5bb795188633f3143268e63f30774646cc2ca1a6dbc2f16075bb6(
    *,
    name_pattern: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6723a104a959995da923acab7dfce85b43e81b95090b921bbf3c48499261dc3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb61fa9583d324736df7dcd30c9ae94e8203cfc8e3edf71c16fabd9ac2e5cac3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d5f14b2ed6b195c0e6dec3f21d84cbf4a697d37f387c9894dc7efa60da47370(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a20db54ec2dc98a81c4ae0f52791a651ca6d4eefeed03b0cb71960f13abcead(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__909cc6ae5233b3323f68eaef85209ad85faf6e5a4a3f8fc8f61a952b166cf39f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89541ea40f771cae45c12bba1119a04b0cfd81d2efe6d0d8fb654c173877fb01(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BinaryAuthorizationPolicyAdmissionWhitelistPatterns]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db9abc5a3ade2ad5efe89e0a80712f8d5bbe3bb76a1835a5f67e66fcc86ca6b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78477a3a3a76422d127225001bf82da49d7a7a8f97bee54bc28849a243cf6773(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e8f415db83caafc678bf5d4424c559da94ac8d32c921668295550717d125d11(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BinaryAuthorizationPolicyAdmissionWhitelistPatterns]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c8aa7c694919a370114660f80cd8afb8d1a78bafe0ede84f0b4b87bc05254f3(
    *,
    cluster: builtins.str,
    enforcement_mode: builtins.str,
    evaluation_mode: builtins.str,
    require_attestations_by: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0e41fd1593c912ce49f5c0919dfa0db7eef9162306f9a1c46ee323787961b9c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edc5a94ba2d98443324e0d16ec5f14104301f83d99ddafb9b5366f14f624be44(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e97c9af5fa59964af4578971eab783a12a94ec1ba69b0993775d216c210eb186(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c402edbe6959bc02f3c6b23cce43835ebf2d489d10fcd62ad700e2ecbd7799d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__749d21f9bea1be47c5ed71d2e61c8f0060ef7130015b902b9e56fcdc821da0d9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6da19e1317b79bb7b63935ac15e637ed56c87898a70ce4d560d86723ac28f303(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BinaryAuthorizationPolicyClusterAdmissionRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87590698a3ae41221b9516b0d983277b799f2f0ace56d98e31378b96ce4eaaab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d27337a1c0c93f4c6e7ddeac833ed1adaf87b215760b225471f6a79404f9250(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00f3e9bb65996c2e717296dad7e6b55d986eb546eb453617f1beec3d33ecd2ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a804c89ee55ec418fb6897169f173413f344fda03000b1dadddedba181e49f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4e6be9bbe6b70064a851f44cd14e310a3aa67ed5fcb61001f0c64a7a41ae065(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92bbdf6b84a65b9a2766dae2d8fe14d65e21676a3123fef1736aa217d3ad317c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BinaryAuthorizationPolicyClusterAdmissionRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1561fd3bc8681a5e4810109217dd14205d26f7e381d9d04bf461de10f3c6aa7d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_admission_rule: typing.Union[BinaryAuthorizationPolicyDefaultAdmissionRule, typing.Dict[builtins.str, typing.Any]],
    admission_whitelist_patterns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BinaryAuthorizationPolicyAdmissionWhitelistPatterns, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cluster_admission_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BinaryAuthorizationPolicyClusterAdmissionRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    global_policy_evaluation_mode: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[BinaryAuthorizationPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e1652c545fc81d3313cdd8c48f72768e75cefa42fd2c7f55576d9041454ea12(
    *,
    enforcement_mode: builtins.str,
    evaluation_mode: builtins.str,
    require_attestations_by: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb52e7b655a4a924d142e9d343b7639afff827d2c8ab4e6d1d091e45ec66e547(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a51d55ef0b36e095ad313fedbc893aa184e220221d9e8e59ac70e40ac96ca90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a71022b376a86a39c3e585d75632dad12e4158b0bff275774cdb97e721a116c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8c0dcdaa68d34a06f45afe98870807e85901c98435d1789dfb05d79999e8e80(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0946d7043f8b4583d5db82e8e035598264d6c560d61e136cc628bcd6dfbf9589(
    value: typing.Optional[BinaryAuthorizationPolicyDefaultAdmissionRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52452c27a0658ebb40e71befc8a071f072a0ea899235280905b4bfca573c3f95(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__869ebeb86c78c41d21dc208c8a42734948e751868290a12f17857fbd43e4ee4b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ce96c72b12d798a0a2708a303ead4289325570d1b5d5996bd22654f32843767(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f658b4e8c23cc26042655bae43fe8265ea225c9364ea9b47e15ef0449707bd1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abc2e38bef2b92ec6afd2fc8562736af00318de10dc3e644e84d381b59918682(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6b0aef0a766ee512e9e4cb8a96887ccfb42ccea579566bf42ffad9b76be78e6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BinaryAuthorizationPolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
