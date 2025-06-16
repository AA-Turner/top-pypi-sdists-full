r'''
# `google_binary_authorization_policy`

Refer to the Terraform Registry for docs: [`google_binary_authorization_policy`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy).
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


class GoogleBinaryAuthorizationPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBinaryAuthorizationPolicy.GoogleBinaryAuthorizationPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy google_binary_authorization_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        default_admission_rule: typing.Union["GoogleBinaryAuthorizationPolicyDefaultAdmissionRule", typing.Dict[builtins.str, typing.Any]],
        admission_whitelist_patterns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleBinaryAuthorizationPolicyAdmissionWhitelistPatterns", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cluster_admission_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleBinaryAuthorizationPolicyClusterAdmissionRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        global_policy_evaluation_mode: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleBinaryAuthorizationPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy google_binary_authorization_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param default_admission_rule: default_admission_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#default_admission_rule GoogleBinaryAuthorizationPolicy#default_admission_rule}
        :param admission_whitelist_patterns: admission_whitelist_patterns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#admission_whitelist_patterns GoogleBinaryAuthorizationPolicy#admission_whitelist_patterns}
        :param cluster_admission_rules: cluster_admission_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#cluster_admission_rules GoogleBinaryAuthorizationPolicy#cluster_admission_rules}
        :param description: A descriptive comment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#description GoogleBinaryAuthorizationPolicy#description}
        :param global_policy_evaluation_mode: Controls the evaluation of a Google-maintained global admission policy for common system-level images. Images not covered by the global policy will be subject to the project admission policy. Possible values: ["ENABLE", "DISABLE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#global_policy_evaluation_mode GoogleBinaryAuthorizationPolicy#global_policy_evaluation_mode}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#id GoogleBinaryAuthorizationPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#project GoogleBinaryAuthorizationPolicy#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#timeouts GoogleBinaryAuthorizationPolicy#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b044704c9cef5c3ba0d5e750f11c72f8125f8bc4797342c0f65e827f91e4c856)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleBinaryAuthorizationPolicyConfig(
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
        '''Generates CDKTF code for importing a GoogleBinaryAuthorizationPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleBinaryAuthorizationPolicy to import.
        :param import_from_id: The id of the existing GoogleBinaryAuthorizationPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleBinaryAuthorizationPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59fa213e394c7e5fe3c577d7be7132709ae7df6745c28c0aca8f28c1a87098db)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAdmissionWhitelistPatterns")
    def put_admission_whitelist_patterns(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleBinaryAuthorizationPolicyAdmissionWhitelistPatterns", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01f25f1dd26a47dfcd1cc104c1977474ff077ec75054af8c072c37d8db8788a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdmissionWhitelistPatterns", [value]))

    @jsii.member(jsii_name="putClusterAdmissionRules")
    def put_cluster_admission_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleBinaryAuthorizationPolicyClusterAdmissionRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba1096fcd2a41061ace198ff1840f4b9ce55575587f36a435ef3bad0fc4d1476)
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
        :param enforcement_mode: The action when a pod creation is denied by the admission rule. Possible values: ["ENFORCED_BLOCK_AND_AUDIT_LOG", "DRYRUN_AUDIT_LOG_ONLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#enforcement_mode GoogleBinaryAuthorizationPolicy#enforcement_mode}
        :param evaluation_mode: How this admission rule will be evaluated. Possible values: ["ALWAYS_ALLOW", "REQUIRE_ATTESTATION", "ALWAYS_DENY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#evaluation_mode GoogleBinaryAuthorizationPolicy#evaluation_mode}
        :param require_attestations_by: The resource names of the attestors that must attest to a container image. If the attestor is in a different project from the policy, it should be specified in the format 'projects/* /attestors/*'. Each attestor must exist before a policy can reference it. To add an attestor to a policy the principal issuing the policy change request must be able to read the attestor resource. Note: this field must be non-empty when the evaluation_mode field specifies REQUIRE_ATTESTATION, otherwise it must be empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#require_attestations_by GoogleBinaryAuthorizationPolicy#require_attestations_by} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleBinaryAuthorizationPolicyDefaultAdmissionRule(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#create GoogleBinaryAuthorizationPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#delete GoogleBinaryAuthorizationPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#update GoogleBinaryAuthorizationPolicy#update}.
        '''
        value = GoogleBinaryAuthorizationPolicyTimeouts(
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
    ) -> "GoogleBinaryAuthorizationPolicyAdmissionWhitelistPatternsList":
        return typing.cast("GoogleBinaryAuthorizationPolicyAdmissionWhitelistPatternsList", jsii.get(self, "admissionWhitelistPatterns"))

    @builtins.property
    @jsii.member(jsii_name="clusterAdmissionRules")
    def cluster_admission_rules(
        self,
    ) -> "GoogleBinaryAuthorizationPolicyClusterAdmissionRulesList":
        return typing.cast("GoogleBinaryAuthorizationPolicyClusterAdmissionRulesList", jsii.get(self, "clusterAdmissionRules"))

    @builtins.property
    @jsii.member(jsii_name="defaultAdmissionRule")
    def default_admission_rule(
        self,
    ) -> "GoogleBinaryAuthorizationPolicyDefaultAdmissionRuleOutputReference":
        return typing.cast("GoogleBinaryAuthorizationPolicyDefaultAdmissionRuleOutputReference", jsii.get(self, "defaultAdmissionRule"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleBinaryAuthorizationPolicyTimeoutsOutputReference":
        return typing.cast("GoogleBinaryAuthorizationPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="admissionWhitelistPatternsInput")
    def admission_whitelist_patterns_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBinaryAuthorizationPolicyAdmissionWhitelistPatterns"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBinaryAuthorizationPolicyAdmissionWhitelistPatterns"]]], jsii.get(self, "admissionWhitelistPatternsInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterAdmissionRulesInput")
    def cluster_admission_rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBinaryAuthorizationPolicyClusterAdmissionRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBinaryAuthorizationPolicyClusterAdmissionRules"]]], jsii.get(self, "clusterAdmissionRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultAdmissionRuleInput")
    def default_admission_rule_input(
        self,
    ) -> typing.Optional["GoogleBinaryAuthorizationPolicyDefaultAdmissionRule"]:
        return typing.cast(typing.Optional["GoogleBinaryAuthorizationPolicyDefaultAdmissionRule"], jsii.get(self, "defaultAdmissionRuleInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleBinaryAuthorizationPolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleBinaryAuthorizationPolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac849ef9cca4d388de8dbb179bb462694ade7c26109d084b2160ff43b3f21a38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="globalPolicyEvaluationMode")
    def global_policy_evaluation_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "globalPolicyEvaluationMode"))

    @global_policy_evaluation_mode.setter
    def global_policy_evaluation_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20f780b57de34211970e49aa4f39462bbdaff51134beb020ceca535682a8f9a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "globalPolicyEvaluationMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__168ad62fd53b72427c863f82aef831ad50132b77f5fc0e882f7acb2fa9892a7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ecb47d85dbb8b53799cb4078d503dc7f0a13bb4845cfcffc2696d1494b10684)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBinaryAuthorizationPolicy.GoogleBinaryAuthorizationPolicyAdmissionWhitelistPatterns",
    jsii_struct_bases=[],
    name_mapping={"name_pattern": "namePattern"},
)
class GoogleBinaryAuthorizationPolicyAdmissionWhitelistPatterns:
    def __init__(self, *, name_pattern: builtins.str) -> None:
        '''
        :param name_pattern: An image name pattern to whitelist, in the form 'registry/path/to/image'. This supports a trailing * as a wildcard, but this is allowed only in text after the registry/ part. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#name_pattern GoogleBinaryAuthorizationPolicy#name_pattern}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7394b1af30c809ac5eaf44a61d30b0ef4576163a287b498f7f9f2763370e002)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#name_pattern GoogleBinaryAuthorizationPolicy#name_pattern}
        '''
        result = self._values.get("name_pattern")
        assert result is not None, "Required property 'name_pattern' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBinaryAuthorizationPolicyAdmissionWhitelistPatterns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBinaryAuthorizationPolicyAdmissionWhitelistPatternsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBinaryAuthorizationPolicy.GoogleBinaryAuthorizationPolicyAdmissionWhitelistPatternsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__06925eb28360a8ae28838dd03312c097d31ef230bfd771793e05bdc94d3ecd79)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleBinaryAuthorizationPolicyAdmissionWhitelistPatternsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f737d39b25d175233fb8db291ba709da63c4c3b10922254613fad7edf449351)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleBinaryAuthorizationPolicyAdmissionWhitelistPatternsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65afcc2ff8c7aadbde06410cc941004163c2f243ddaa14e19acaf5c96aef616a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__180b14537ab44c5910c9fe5df3b5375951279c1a0fd4df5c875721065651bb86)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a27771ae0c16a2315854ccd4a328cdfa309a9f28b878edd0e694bf26dda4219)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBinaryAuthorizationPolicyAdmissionWhitelistPatterns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBinaryAuthorizationPolicyAdmissionWhitelistPatterns]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBinaryAuthorizationPolicyAdmissionWhitelistPatterns]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__694543fff2aa665b8819586b2354a995c953418b569e71033994118bf5fbfd78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleBinaryAuthorizationPolicyAdmissionWhitelistPatternsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBinaryAuthorizationPolicy.GoogleBinaryAuthorizationPolicyAdmissionWhitelistPatternsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__188217bd0d6502814878e808f9f14f24d55cbd9114645adaa31fd9c7d986fc1b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7a29bbae3f91de8257c15200a1834b82ef944f26c3c1d2941a316d6f0063d80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namePattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBinaryAuthorizationPolicyAdmissionWhitelistPatterns]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBinaryAuthorizationPolicyAdmissionWhitelistPatterns]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBinaryAuthorizationPolicyAdmissionWhitelistPatterns]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10920e3c9940cfaa9528f601c3e354b573bd61c5aeb95c4a214686b28309f6ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBinaryAuthorizationPolicy.GoogleBinaryAuthorizationPolicyClusterAdmissionRules",
    jsii_struct_bases=[],
    name_mapping={
        "cluster": "cluster",
        "enforcement_mode": "enforcementMode",
        "evaluation_mode": "evaluationMode",
        "require_attestations_by": "requireAttestationsBy",
    },
)
class GoogleBinaryAuthorizationPolicyClusterAdmissionRules:
    def __init__(
        self,
        *,
        cluster: builtins.str,
        enforcement_mode: builtins.str,
        evaluation_mode: builtins.str,
        require_attestations_by: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param cluster: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#cluster GoogleBinaryAuthorizationPolicy#cluster}.
        :param enforcement_mode: The action when a pod creation is denied by the admission rule. Possible values: ["ENFORCED_BLOCK_AND_AUDIT_LOG", "DRYRUN_AUDIT_LOG_ONLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#enforcement_mode GoogleBinaryAuthorizationPolicy#enforcement_mode}
        :param evaluation_mode: How this admission rule will be evaluated. Possible values: ["ALWAYS_ALLOW", "REQUIRE_ATTESTATION", "ALWAYS_DENY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#evaluation_mode GoogleBinaryAuthorizationPolicy#evaluation_mode}
        :param require_attestations_by: The resource names of the attestors that must attest to a container image. If the attestor is in a different project from the policy, it should be specified in the format 'projects/* /attestors/*'. Each attestor must exist before a policy can reference it. To add an attestor to a policy the principal issuing the policy change request must be able to read the attestor resource. Note: this field must be non-empty when the evaluation_mode field specifies REQUIRE_ATTESTATION, otherwise it must be empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#require_attestations_by GoogleBinaryAuthorizationPolicy#require_attestations_by} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f1183b160c8f9c9125a43848e96a5825c577a85be8693ec4c262f92c191edcc)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#cluster GoogleBinaryAuthorizationPolicy#cluster}.'''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enforcement_mode(self) -> builtins.str:
        '''The action when a pod creation is denied by the admission rule. Possible values: ["ENFORCED_BLOCK_AND_AUDIT_LOG", "DRYRUN_AUDIT_LOG_ONLY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#enforcement_mode GoogleBinaryAuthorizationPolicy#enforcement_mode}
        '''
        result = self._values.get("enforcement_mode")
        assert result is not None, "Required property 'enforcement_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def evaluation_mode(self) -> builtins.str:
        '''How this admission rule will be evaluated. Possible values: ["ALWAYS_ALLOW", "REQUIRE_ATTESTATION", "ALWAYS_DENY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#evaluation_mode GoogleBinaryAuthorizationPolicy#evaluation_mode}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#require_attestations_by GoogleBinaryAuthorizationPolicy#require_attestations_by}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("require_attestations_by")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBinaryAuthorizationPolicyClusterAdmissionRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBinaryAuthorizationPolicyClusterAdmissionRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBinaryAuthorizationPolicy.GoogleBinaryAuthorizationPolicyClusterAdmissionRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__64cba4a9bc7ff79c391b3e451737f93c7d1efed3636e6a423d43ac8f480a04cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleBinaryAuthorizationPolicyClusterAdmissionRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f65854e13cfa144d233775bc6a93f0cee6edb66588e05a01362a9d0456882f2f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleBinaryAuthorizationPolicyClusterAdmissionRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b6a80e19baab7dad3554bfa1bb13997980acc8e018862028964befc425e9ca7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae1a34330162e34e94bb253e7d0e799f6dd7b88de4513a252c4d985e71efc698)
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
            type_hints = typing.get_type_hints(_typecheckingstub__18b9cc6f3a62ca14bc6f7799a16ca7616eb8e61c8bbb4910f0ef5c096f496679)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBinaryAuthorizationPolicyClusterAdmissionRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBinaryAuthorizationPolicyClusterAdmissionRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBinaryAuthorizationPolicyClusterAdmissionRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cdaf239005188ea8149b22235f7cf66c60cca0bdbef9d004fe92916c605974f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleBinaryAuthorizationPolicyClusterAdmissionRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBinaryAuthorizationPolicy.GoogleBinaryAuthorizationPolicyClusterAdmissionRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__49fcfd3bbcf9549d8c0d8b5b9d8dd19c8733c64eef20592ef3d8fc3d30e87d9a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__164920a152e795ea4f1844709d3363984dd54f4b6df95676878fef6f4e5a847c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforcementMode")
    def enforcement_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enforcementMode"))

    @enforcement_mode.setter
    def enforcement_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b387bf79a05f55dd21aa29dd357306fffa18d7236f3c21b2f2795be92f7bd957)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforcementMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="evaluationMode")
    def evaluation_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "evaluationMode"))

    @evaluation_mode.setter
    def evaluation_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b446ba994903d3b674e92ee9c8fd994898ed27f9bcf80dc34f1586a9c30f1e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "evaluationMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireAttestationsBy")
    def require_attestations_by(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "requireAttestationsBy"))

    @require_attestations_by.setter
    def require_attestations_by(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe2dbeac5998c3319e058c4277a091dc274637da826c6ba93462eaea13631eff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireAttestationsBy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBinaryAuthorizationPolicyClusterAdmissionRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBinaryAuthorizationPolicyClusterAdmissionRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBinaryAuthorizationPolicyClusterAdmissionRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ddc59ec6094904751d71211fbbe388e0ebb4d840adbd3956ee610b1f1b064b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBinaryAuthorizationPolicy.GoogleBinaryAuthorizationPolicyConfig",
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
class GoogleBinaryAuthorizationPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        default_admission_rule: typing.Union["GoogleBinaryAuthorizationPolicyDefaultAdmissionRule", typing.Dict[builtins.str, typing.Any]],
        admission_whitelist_patterns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleBinaryAuthorizationPolicyAdmissionWhitelistPatterns, typing.Dict[builtins.str, typing.Any]]]]] = None,
        cluster_admission_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleBinaryAuthorizationPolicyClusterAdmissionRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        global_policy_evaluation_mode: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleBinaryAuthorizationPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param default_admission_rule: default_admission_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#default_admission_rule GoogleBinaryAuthorizationPolicy#default_admission_rule}
        :param admission_whitelist_patterns: admission_whitelist_patterns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#admission_whitelist_patterns GoogleBinaryAuthorizationPolicy#admission_whitelist_patterns}
        :param cluster_admission_rules: cluster_admission_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#cluster_admission_rules GoogleBinaryAuthorizationPolicy#cluster_admission_rules}
        :param description: A descriptive comment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#description GoogleBinaryAuthorizationPolicy#description}
        :param global_policy_evaluation_mode: Controls the evaluation of a Google-maintained global admission policy for common system-level images. Images not covered by the global policy will be subject to the project admission policy. Possible values: ["ENABLE", "DISABLE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#global_policy_evaluation_mode GoogleBinaryAuthorizationPolicy#global_policy_evaluation_mode}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#id GoogleBinaryAuthorizationPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#project GoogleBinaryAuthorizationPolicy#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#timeouts GoogleBinaryAuthorizationPolicy#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(default_admission_rule, dict):
            default_admission_rule = GoogleBinaryAuthorizationPolicyDefaultAdmissionRule(**default_admission_rule)
        if isinstance(timeouts, dict):
            timeouts = GoogleBinaryAuthorizationPolicyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a50563949c75d1cc1c2efc6912960b0545e939a0c9518990abe598ba8de3e77)
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
    def default_admission_rule(
        self,
    ) -> "GoogleBinaryAuthorizationPolicyDefaultAdmissionRule":
        '''default_admission_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#default_admission_rule GoogleBinaryAuthorizationPolicy#default_admission_rule}
        '''
        result = self._values.get("default_admission_rule")
        assert result is not None, "Required property 'default_admission_rule' is missing"
        return typing.cast("GoogleBinaryAuthorizationPolicyDefaultAdmissionRule", result)

    @builtins.property
    def admission_whitelist_patterns(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBinaryAuthorizationPolicyAdmissionWhitelistPatterns]]]:
        '''admission_whitelist_patterns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#admission_whitelist_patterns GoogleBinaryAuthorizationPolicy#admission_whitelist_patterns}
        '''
        result = self._values.get("admission_whitelist_patterns")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBinaryAuthorizationPolicyAdmissionWhitelistPatterns]]], result)

    @builtins.property
    def cluster_admission_rules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBinaryAuthorizationPolicyClusterAdmissionRules]]]:
        '''cluster_admission_rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#cluster_admission_rules GoogleBinaryAuthorizationPolicy#cluster_admission_rules}
        '''
        result = self._values.get("cluster_admission_rules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBinaryAuthorizationPolicyClusterAdmissionRules]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A descriptive comment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#description GoogleBinaryAuthorizationPolicy#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def global_policy_evaluation_mode(self) -> typing.Optional[builtins.str]:
        '''Controls the evaluation of a Google-maintained global admission policy for common system-level images.

        Images not covered by the global
        policy will be subject to the project admission policy. Possible values: ["ENABLE", "DISABLE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#global_policy_evaluation_mode GoogleBinaryAuthorizationPolicy#global_policy_evaluation_mode}
        '''
        result = self._values.get("global_policy_evaluation_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#id GoogleBinaryAuthorizationPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#project GoogleBinaryAuthorizationPolicy#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleBinaryAuthorizationPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#timeouts GoogleBinaryAuthorizationPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleBinaryAuthorizationPolicyTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBinaryAuthorizationPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBinaryAuthorizationPolicy.GoogleBinaryAuthorizationPolicyDefaultAdmissionRule",
    jsii_struct_bases=[],
    name_mapping={
        "enforcement_mode": "enforcementMode",
        "evaluation_mode": "evaluationMode",
        "require_attestations_by": "requireAttestationsBy",
    },
)
class GoogleBinaryAuthorizationPolicyDefaultAdmissionRule:
    def __init__(
        self,
        *,
        enforcement_mode: builtins.str,
        evaluation_mode: builtins.str,
        require_attestations_by: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param enforcement_mode: The action when a pod creation is denied by the admission rule. Possible values: ["ENFORCED_BLOCK_AND_AUDIT_LOG", "DRYRUN_AUDIT_LOG_ONLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#enforcement_mode GoogleBinaryAuthorizationPolicy#enforcement_mode}
        :param evaluation_mode: How this admission rule will be evaluated. Possible values: ["ALWAYS_ALLOW", "REQUIRE_ATTESTATION", "ALWAYS_DENY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#evaluation_mode GoogleBinaryAuthorizationPolicy#evaluation_mode}
        :param require_attestations_by: The resource names of the attestors that must attest to a container image. If the attestor is in a different project from the policy, it should be specified in the format 'projects/* /attestors/*'. Each attestor must exist before a policy can reference it. To add an attestor to a policy the principal issuing the policy change request must be able to read the attestor resource. Note: this field must be non-empty when the evaluation_mode field specifies REQUIRE_ATTESTATION, otherwise it must be empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#require_attestations_by GoogleBinaryAuthorizationPolicy#require_attestations_by} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93d5ec45925263ca141e505ae2e68c4f054d292bee91df053c10dc7e0615d175)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#enforcement_mode GoogleBinaryAuthorizationPolicy#enforcement_mode}
        '''
        result = self._values.get("enforcement_mode")
        assert result is not None, "Required property 'enforcement_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def evaluation_mode(self) -> builtins.str:
        '''How this admission rule will be evaluated. Possible values: ["ALWAYS_ALLOW", "REQUIRE_ATTESTATION", "ALWAYS_DENY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#evaluation_mode GoogleBinaryAuthorizationPolicy#evaluation_mode}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#require_attestations_by GoogleBinaryAuthorizationPolicy#require_attestations_by}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("require_attestations_by")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBinaryAuthorizationPolicyDefaultAdmissionRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBinaryAuthorizationPolicyDefaultAdmissionRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBinaryAuthorizationPolicy.GoogleBinaryAuthorizationPolicyDefaultAdmissionRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c96410cce0763e682cf2d98927890a39b87ede8b0d582045e5b1a11518baa93d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__79b3bdb74fe8fc6f8b29aee5df8c84519eaaaa0c2d74405350f52ce7142ef36e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforcementMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="evaluationMode")
    def evaluation_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "evaluationMode"))

    @evaluation_mode.setter
    def evaluation_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c52a5c479f66dabea0ef085d2288b761a0641da5e9cc50076850f46e2227cf9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "evaluationMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireAttestationsBy")
    def require_attestations_by(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "requireAttestationsBy"))

    @require_attestations_by.setter
    def require_attestations_by(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cc948b8407f2746f5e131d72cf3eccff72432420be96dbaa93aee3976963e79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireAttestationsBy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleBinaryAuthorizationPolicyDefaultAdmissionRule]:
        return typing.cast(typing.Optional[GoogleBinaryAuthorizationPolicyDefaultAdmissionRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBinaryAuthorizationPolicyDefaultAdmissionRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__390b068fd79329dff45ea733feee719771d9f438bf6f7c3f63c886ee568650a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBinaryAuthorizationPolicy.GoogleBinaryAuthorizationPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleBinaryAuthorizationPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#create GoogleBinaryAuthorizationPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#delete GoogleBinaryAuthorizationPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#update GoogleBinaryAuthorizationPolicy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dae0fe234afe7cf9c1659f361d62cc27fc86b05c17ed8504a6b5c03d65f0645)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#create GoogleBinaryAuthorizationPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#delete GoogleBinaryAuthorizationPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_policy#update GoogleBinaryAuthorizationPolicy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBinaryAuthorizationPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBinaryAuthorizationPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBinaryAuthorizationPolicy.GoogleBinaryAuthorizationPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3834ceba3d11fe6906a9dceacaf767c2cbba5f24effbf43ffebf53bb2f7459c4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__521421dca8c9f52d1ded13a204d487c32a126e28314f1767fe68ef0d2ee6d3dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__560505b0fb3272baed0e6f5199e12d527a3720eef1e54dbe6933b55f0d1af450)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aad6112c1fe9f6e0897be21638391a545eee11c17d1e983e787ece80ec999fd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBinaryAuthorizationPolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBinaryAuthorizationPolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBinaryAuthorizationPolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c872a02cdba2fa2715f3b06c4978f545a1dbaa227cd6a3835ad05f3771ceec6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleBinaryAuthorizationPolicy",
    "GoogleBinaryAuthorizationPolicyAdmissionWhitelistPatterns",
    "GoogleBinaryAuthorizationPolicyAdmissionWhitelistPatternsList",
    "GoogleBinaryAuthorizationPolicyAdmissionWhitelistPatternsOutputReference",
    "GoogleBinaryAuthorizationPolicyClusterAdmissionRules",
    "GoogleBinaryAuthorizationPolicyClusterAdmissionRulesList",
    "GoogleBinaryAuthorizationPolicyClusterAdmissionRulesOutputReference",
    "GoogleBinaryAuthorizationPolicyConfig",
    "GoogleBinaryAuthorizationPolicyDefaultAdmissionRule",
    "GoogleBinaryAuthorizationPolicyDefaultAdmissionRuleOutputReference",
    "GoogleBinaryAuthorizationPolicyTimeouts",
    "GoogleBinaryAuthorizationPolicyTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__b044704c9cef5c3ba0d5e750f11c72f8125f8bc4797342c0f65e827f91e4c856(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    default_admission_rule: typing.Union[GoogleBinaryAuthorizationPolicyDefaultAdmissionRule, typing.Dict[builtins.str, typing.Any]],
    admission_whitelist_patterns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleBinaryAuthorizationPolicyAdmissionWhitelistPatterns, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cluster_admission_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleBinaryAuthorizationPolicyClusterAdmissionRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    global_policy_evaluation_mode: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleBinaryAuthorizationPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__59fa213e394c7e5fe3c577d7be7132709ae7df6745c28c0aca8f28c1a87098db(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01f25f1dd26a47dfcd1cc104c1977474ff077ec75054af8c072c37d8db8788a0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleBinaryAuthorizationPolicyAdmissionWhitelistPatterns, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba1096fcd2a41061ace198ff1840f4b9ce55575587f36a435ef3bad0fc4d1476(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleBinaryAuthorizationPolicyClusterAdmissionRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac849ef9cca4d388de8dbb179bb462694ade7c26109d084b2160ff43b3f21a38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20f780b57de34211970e49aa4f39462bbdaff51134beb020ceca535682a8f9a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__168ad62fd53b72427c863f82aef831ad50132b77f5fc0e882f7acb2fa9892a7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ecb47d85dbb8b53799cb4078d503dc7f0a13bb4845cfcffc2696d1494b10684(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7394b1af30c809ac5eaf44a61d30b0ef4576163a287b498f7f9f2763370e002(
    *,
    name_pattern: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06925eb28360a8ae28838dd03312c097d31ef230bfd771793e05bdc94d3ecd79(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f737d39b25d175233fb8db291ba709da63c4c3b10922254613fad7edf449351(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65afcc2ff8c7aadbde06410cc941004163c2f243ddaa14e19acaf5c96aef616a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__180b14537ab44c5910c9fe5df3b5375951279c1a0fd4df5c875721065651bb86(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a27771ae0c16a2315854ccd4a328cdfa309a9f28b878edd0e694bf26dda4219(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__694543fff2aa665b8819586b2354a995c953418b569e71033994118bf5fbfd78(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBinaryAuthorizationPolicyAdmissionWhitelistPatterns]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__188217bd0d6502814878e808f9f14f24d55cbd9114645adaa31fd9c7d986fc1b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7a29bbae3f91de8257c15200a1834b82ef944f26c3c1d2941a316d6f0063d80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10920e3c9940cfaa9528f601c3e354b573bd61c5aeb95c4a214686b28309f6ec(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBinaryAuthorizationPolicyAdmissionWhitelistPatterns]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f1183b160c8f9c9125a43848e96a5825c577a85be8693ec4c262f92c191edcc(
    *,
    cluster: builtins.str,
    enforcement_mode: builtins.str,
    evaluation_mode: builtins.str,
    require_attestations_by: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64cba4a9bc7ff79c391b3e451737f93c7d1efed3636e6a423d43ac8f480a04cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f65854e13cfa144d233775bc6a93f0cee6edb66588e05a01362a9d0456882f2f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b6a80e19baab7dad3554bfa1bb13997980acc8e018862028964befc425e9ca7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae1a34330162e34e94bb253e7d0e799f6dd7b88de4513a252c4d985e71efc698(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18b9cc6f3a62ca14bc6f7799a16ca7616eb8e61c8bbb4910f0ef5c096f496679(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cdaf239005188ea8149b22235f7cf66c60cca0bdbef9d004fe92916c605974f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBinaryAuthorizationPolicyClusterAdmissionRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49fcfd3bbcf9549d8c0d8b5b9d8dd19c8733c64eef20592ef3d8fc3d30e87d9a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__164920a152e795ea4f1844709d3363984dd54f4b6df95676878fef6f4e5a847c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b387bf79a05f55dd21aa29dd357306fffa18d7236f3c21b2f2795be92f7bd957(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b446ba994903d3b674e92ee9c8fd994898ed27f9bcf80dc34f1586a9c30f1e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe2dbeac5998c3319e058c4277a091dc274637da826c6ba93462eaea13631eff(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ddc59ec6094904751d71211fbbe388e0ebb4d840adbd3956ee610b1f1b064b2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBinaryAuthorizationPolicyClusterAdmissionRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a50563949c75d1cc1c2efc6912960b0545e939a0c9518990abe598ba8de3e77(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_admission_rule: typing.Union[GoogleBinaryAuthorizationPolicyDefaultAdmissionRule, typing.Dict[builtins.str, typing.Any]],
    admission_whitelist_patterns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleBinaryAuthorizationPolicyAdmissionWhitelistPatterns, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cluster_admission_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleBinaryAuthorizationPolicyClusterAdmissionRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    global_policy_evaluation_mode: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleBinaryAuthorizationPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93d5ec45925263ca141e505ae2e68c4f054d292bee91df053c10dc7e0615d175(
    *,
    enforcement_mode: builtins.str,
    evaluation_mode: builtins.str,
    require_attestations_by: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c96410cce0763e682cf2d98927890a39b87ede8b0d582045e5b1a11518baa93d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79b3bdb74fe8fc6f8b29aee5df8c84519eaaaa0c2d74405350f52ce7142ef36e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c52a5c479f66dabea0ef085d2288b761a0641da5e9cc50076850f46e2227cf9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cc948b8407f2746f5e131d72cf3eccff72432420be96dbaa93aee3976963e79(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__390b068fd79329dff45ea733feee719771d9f438bf6f7c3f63c886ee568650a1(
    value: typing.Optional[GoogleBinaryAuthorizationPolicyDefaultAdmissionRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dae0fe234afe7cf9c1659f361d62cc27fc86b05c17ed8504a6b5c03d65f0645(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3834ceba3d11fe6906a9dceacaf767c2cbba5f24effbf43ffebf53bb2f7459c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__521421dca8c9f52d1ded13a204d487c32a126e28314f1767fe68ef0d2ee6d3dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__560505b0fb3272baed0e6f5199e12d527a3720eef1e54dbe6933b55f0d1af450(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aad6112c1fe9f6e0897be21638391a545eee11c17d1e983e787ece80ec999fd9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c872a02cdba2fa2715f3b06c4978f545a1dbaa227cd6a3835ad05f3771ceec6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBinaryAuthorizationPolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
