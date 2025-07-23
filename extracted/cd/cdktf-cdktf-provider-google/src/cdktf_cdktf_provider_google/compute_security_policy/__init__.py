r'''
# `google_compute_security_policy`

Refer to the Terraform Registry for docs: [`google_compute_security_policy`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy).
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


class ComputeSecurityPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy google_compute_security_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        adaptive_protection_config: typing.Optional[typing.Union["ComputeSecurityPolicyAdaptiveProtectionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        advanced_options_config: typing.Optional[typing.Union["ComputeSecurityPolicyAdvancedOptionsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        recaptcha_options_config: typing.Optional[typing.Union["ComputeSecurityPolicyRecaptchaOptionsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["ComputeSecurityPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy google_compute_security_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name of the security policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#name ComputeSecurityPolicy#name}
        :param adaptive_protection_config: adaptive_protection_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#adaptive_protection_config ComputeSecurityPolicy#adaptive_protection_config}
        :param advanced_options_config: advanced_options_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#advanced_options_config ComputeSecurityPolicy#advanced_options_config}
        :param description: An optional description of this security policy. Max size is 2048. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#description ComputeSecurityPolicy#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#id ComputeSecurityPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: The project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#project ComputeSecurityPolicy#project}
        :param recaptcha_options_config: recaptcha_options_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#recaptcha_options_config ComputeSecurityPolicy#recaptcha_options_config}
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#rule ComputeSecurityPolicy#rule}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#timeouts ComputeSecurityPolicy#timeouts}
        :param type: The type indicates the intended use of the security policy. CLOUD_ARMOR - Cloud Armor backend security policies can be configured to filter incoming HTTP requests targeting backend services. They filter requests before they hit the origin servers. CLOUD_ARMOR_EDGE - Cloud Armor edge security policies can be configured to filter incoming HTTP requests targeting backend services (including Cloud CDN-enabled) as well as backend buckets (Cloud Storage). They filter requests before the request is served from Google's cache. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#type ComputeSecurityPolicy#type}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a59c3318fbcecbddc8ed7d1ff918bb9920ef120f8bb784e7180855dd88b8270)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeSecurityPolicyConfig(
            name=name,
            adaptive_protection_config=adaptive_protection_config,
            advanced_options_config=advanced_options_config,
            description=description,
            id=id,
            project=project,
            recaptcha_options_config=recaptcha_options_config,
            rule=rule,
            timeouts=timeouts,
            type=type,
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
        '''Generates CDKTF code for importing a ComputeSecurityPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeSecurityPolicy to import.
        :param import_from_id: The id of the existing ComputeSecurityPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeSecurityPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__376dbaec45717e998256b914a5be300a09c18fc5905d5125ca2b736090e6ab20)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAdaptiveProtectionConfig")
    def put_adaptive_protection_config(
        self,
        *,
        layer7_ddos_defense_config: typing.Optional[typing.Union["ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param layer7_ddos_defense_config: layer_7_ddos_defense_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#layer_7_ddos_defense_config ComputeSecurityPolicy#layer_7_ddos_defense_config}
        '''
        value = ComputeSecurityPolicyAdaptiveProtectionConfig(
            layer7_ddos_defense_config=layer7_ddos_defense_config
        )

        return typing.cast(None, jsii.invoke(self, "putAdaptiveProtectionConfig", [value]))

    @jsii.member(jsii_name="putAdvancedOptionsConfig")
    def put_advanced_options_config(
        self,
        *,
        json_custom_config: typing.Optional[typing.Union["ComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        json_parsing: typing.Optional[builtins.str] = None,
        log_level: typing.Optional[builtins.str] = None,
        user_ip_request_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param json_custom_config: json_custom_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#json_custom_config ComputeSecurityPolicy#json_custom_config}
        :param json_parsing: JSON body parsing. Supported values include: "DISABLED", "STANDARD". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#json_parsing ComputeSecurityPolicy#json_parsing}
        :param log_level: Logging level. Supported values include: "NORMAL", "VERBOSE". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#log_level ComputeSecurityPolicy#log_level}
        :param user_ip_request_headers: An optional list of case-insensitive request header names to use for resolving the callers client IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#user_ip_request_headers ComputeSecurityPolicy#user_ip_request_headers}
        '''
        value = ComputeSecurityPolicyAdvancedOptionsConfig(
            json_custom_config=json_custom_config,
            json_parsing=json_parsing,
            log_level=log_level,
            user_ip_request_headers=user_ip_request_headers,
        )

        return typing.cast(None, jsii.invoke(self, "putAdvancedOptionsConfig", [value]))

    @jsii.member(jsii_name="putRecaptchaOptionsConfig")
    def put_recaptcha_options_config(self, *, redirect_site_key: builtins.str) -> None:
        '''
        :param redirect_site_key: A field to supply a reCAPTCHA site key to be used for all the rules using the redirect action with the type of GOOGLE_RECAPTCHA under the security policy. The specified site key needs to be created from the reCAPTCHA API. The user is responsible for the validity of the specified site key. If not specified, a Google-managed site key is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#redirect_site_key ComputeSecurityPolicy#redirect_site_key}
        '''
        value = ComputeSecurityPolicyRecaptchaOptionsConfig(
            redirect_site_key=redirect_site_key
        )

        return typing.cast(None, jsii.invoke(self, "putRecaptchaOptionsConfig", [value]))

    @jsii.member(jsii_name="putRule")
    def put_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d631794c35e30e47ee1690f99a283477b2609e883e8ae8bbf7e1a4b1fda0b55b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRule", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#create ComputeSecurityPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#delete ComputeSecurityPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#update ComputeSecurityPolicy#update}.
        '''
        value = ComputeSecurityPolicyTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAdaptiveProtectionConfig")
    def reset_adaptive_protection_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdaptiveProtectionConfig", []))

    @jsii.member(jsii_name="resetAdvancedOptionsConfig")
    def reset_advanced_options_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvancedOptionsConfig", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRecaptchaOptionsConfig")
    def reset_recaptcha_options_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecaptchaOptionsConfig", []))

    @jsii.member(jsii_name="resetRule")
    def reset_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRule", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

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
    @jsii.member(jsii_name="adaptiveProtectionConfig")
    def adaptive_protection_config(
        self,
    ) -> "ComputeSecurityPolicyAdaptiveProtectionConfigOutputReference":
        return typing.cast("ComputeSecurityPolicyAdaptiveProtectionConfigOutputReference", jsii.get(self, "adaptiveProtectionConfig"))

    @builtins.property
    @jsii.member(jsii_name="advancedOptionsConfig")
    def advanced_options_config(
        self,
    ) -> "ComputeSecurityPolicyAdvancedOptionsConfigOutputReference":
        return typing.cast("ComputeSecurityPolicyAdvancedOptionsConfigOutputReference", jsii.get(self, "advancedOptionsConfig"))

    @builtins.property
    @jsii.member(jsii_name="fingerprint")
    def fingerprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fingerprint"))

    @builtins.property
    @jsii.member(jsii_name="recaptchaOptionsConfig")
    def recaptcha_options_config(
        self,
    ) -> "ComputeSecurityPolicyRecaptchaOptionsConfigOutputReference":
        return typing.cast("ComputeSecurityPolicyRecaptchaOptionsConfigOutputReference", jsii.get(self, "recaptchaOptionsConfig"))

    @builtins.property
    @jsii.member(jsii_name="rule")
    def rule(self) -> "ComputeSecurityPolicyRuleList":
        return typing.cast("ComputeSecurityPolicyRuleList", jsii.get(self, "rule"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeSecurityPolicyTimeoutsOutputReference":
        return typing.cast("ComputeSecurityPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="adaptiveProtectionConfigInput")
    def adaptive_protection_config_input(
        self,
    ) -> typing.Optional["ComputeSecurityPolicyAdaptiveProtectionConfig"]:
        return typing.cast(typing.Optional["ComputeSecurityPolicyAdaptiveProtectionConfig"], jsii.get(self, "adaptiveProtectionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="advancedOptionsConfigInput")
    def advanced_options_config_input(
        self,
    ) -> typing.Optional["ComputeSecurityPolicyAdvancedOptionsConfig"]:
        return typing.cast(typing.Optional["ComputeSecurityPolicyAdvancedOptionsConfig"], jsii.get(self, "advancedOptionsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="recaptchaOptionsConfigInput")
    def recaptcha_options_config_input(
        self,
    ) -> typing.Optional["ComputeSecurityPolicyRecaptchaOptionsConfig"]:
        return typing.cast(typing.Optional["ComputeSecurityPolicyRecaptchaOptionsConfig"], jsii.get(self, "recaptchaOptionsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleInput")
    def rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRule"]]], jsii.get(self, "ruleInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeSecurityPolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeSecurityPolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ae4bcb1126273705e87c758eea02ed4783812a2edf3c30dc6db70b77d6f8407)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b31848e8093121060dd26c52739477cf0908de5e29bc756209af58e599ad720)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fad7748849f59d44af2052aa0e487d98e58302bcee482eca7bfa1a891258c86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9823743ae42e9de223bf84137402ea28e19eb9a04f62cdb8a73ac86d55f5c81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4840c1149449708bd5bc5284f5ce54485f810f2748b484baf14846cbc2a4dbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyAdaptiveProtectionConfig",
    jsii_struct_bases=[],
    name_mapping={"layer7_ddos_defense_config": "layer7DdosDefenseConfig"},
)
class ComputeSecurityPolicyAdaptiveProtectionConfig:
    def __init__(
        self,
        *,
        layer7_ddos_defense_config: typing.Optional[typing.Union["ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param layer7_ddos_defense_config: layer_7_ddos_defense_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#layer_7_ddos_defense_config ComputeSecurityPolicy#layer_7_ddos_defense_config}
        '''
        if isinstance(layer7_ddos_defense_config, dict):
            layer7_ddos_defense_config = ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig(**layer7_ddos_defense_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__199704435de57e2755e400ffaa603c7f9ce1ae9baf0a0adde2d5822dfb8a31fd)
            check_type(argname="argument layer7_ddos_defense_config", value=layer7_ddos_defense_config, expected_type=type_hints["layer7_ddos_defense_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if layer7_ddos_defense_config is not None:
            self._values["layer7_ddos_defense_config"] = layer7_ddos_defense_config

    @builtins.property
    def layer7_ddos_defense_config(
        self,
    ) -> typing.Optional["ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig"]:
        '''layer_7_ddos_defense_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#layer_7_ddos_defense_config ComputeSecurityPolicy#layer_7_ddos_defense_config}
        '''
        result = self._values.get("layer7_ddos_defense_config")
        return typing.cast(typing.Optional["ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyAdaptiveProtectionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable": "enable",
        "rule_visibility": "ruleVisibility",
        "threshold_configs": "thresholdConfigs",
    },
)
class ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig:
    def __init__(
        self,
        *,
        enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rule_visibility: typing.Optional[builtins.str] = None,
        threshold_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enable: If set to true, enables CAAP for L7 DDoS detection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#enable ComputeSecurityPolicy#enable}
        :param rule_visibility: Rule visibility. Supported values include: "STANDARD", "PREMIUM". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#rule_visibility ComputeSecurityPolicy#rule_visibility}
        :param threshold_configs: threshold_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#threshold_configs ComputeSecurityPolicy#threshold_configs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19d3926c3cd50d957efe608297568fd1dcbaaa1415e53efd71d5e2c0c352bfcc)
            check_type(argname="argument enable", value=enable, expected_type=type_hints["enable"])
            check_type(argname="argument rule_visibility", value=rule_visibility, expected_type=type_hints["rule_visibility"])
            check_type(argname="argument threshold_configs", value=threshold_configs, expected_type=type_hints["threshold_configs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable is not None:
            self._values["enable"] = enable
        if rule_visibility is not None:
            self._values["rule_visibility"] = rule_visibility
        if threshold_configs is not None:
            self._values["threshold_configs"] = threshold_configs

    @builtins.property
    def enable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, enables CAAP for L7 DDoS detection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#enable ComputeSecurityPolicy#enable}
        '''
        result = self._values.get("enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def rule_visibility(self) -> typing.Optional[builtins.str]:
        '''Rule visibility. Supported values include: "STANDARD", "PREMIUM".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#rule_visibility ComputeSecurityPolicy#rule_visibility}
        '''
        result = self._values.get("rule_visibility")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def threshold_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs"]]]:
        '''threshold_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#threshold_configs ComputeSecurityPolicy#threshold_configs}
        '''
        result = self._values.get("threshold_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9087537101729c145175bc05883f2de193515395d9667b4b9f19d8e48447de5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putThresholdConfigs")
    def put_threshold_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e09c15b8b612b635a7aa735cfd549ed7d00d9d81e7c1f0a51e9f4fd715b11358)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putThresholdConfigs", [value]))

    @jsii.member(jsii_name="resetEnable")
    def reset_enable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnable", []))

    @jsii.member(jsii_name="resetRuleVisibility")
    def reset_rule_visibility(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuleVisibility", []))

    @jsii.member(jsii_name="resetThresholdConfigs")
    def reset_threshold_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThresholdConfigs", []))

    @builtins.property
    @jsii.member(jsii_name="thresholdConfigs")
    def threshold_configs(
        self,
    ) -> "ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsList":
        return typing.cast("ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsList", jsii.get(self, "thresholdConfigs"))

    @builtins.property
    @jsii.member(jsii_name="enableInput")
    def enable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleVisibilityInput")
    def rule_visibility_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleVisibilityInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdConfigsInput")
    def threshold_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs"]]], jsii.get(self, "thresholdConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="enable")
    def enable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enable"))

    @enable.setter
    def enable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb51d815c9cac78b84228b45742cbf34e4cd2575de44443e52ea689d5d7be103)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ruleVisibility")
    def rule_visibility(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleVisibility"))

    @rule_visibility.setter
    def rule_visibility(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a1531ed536f49c5632cc07bfa883bf96625b8916ac863b3753b27ff65ffef62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleVisibility", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c870525dc44efdeab738313f85626c47dabd8201c1e53a5669809a2fff085a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "auto_deploy_confidence_threshold": "autoDeployConfidenceThreshold",
        "auto_deploy_expiration_sec": "autoDeployExpirationSec",
        "auto_deploy_impacted_baseline_threshold": "autoDeployImpactedBaselineThreshold",
        "auto_deploy_load_threshold": "autoDeployLoadThreshold",
        "detection_absolute_qps": "detectionAbsoluteQps",
        "detection_load_threshold": "detectionLoadThreshold",
        "detection_relative_to_baseline_qps": "detectionRelativeToBaselineQps",
        "traffic_granularity_configs": "trafficGranularityConfigs",
    },
)
class ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs:
    def __init__(
        self,
        *,
        name: builtins.str,
        auto_deploy_confidence_threshold: typing.Optional[jsii.Number] = None,
        auto_deploy_expiration_sec: typing.Optional[jsii.Number] = None,
        auto_deploy_impacted_baseline_threshold: typing.Optional[jsii.Number] = None,
        auto_deploy_load_threshold: typing.Optional[jsii.Number] = None,
        detection_absolute_qps: typing.Optional[jsii.Number] = None,
        detection_load_threshold: typing.Optional[jsii.Number] = None,
        detection_relative_to_baseline_qps: typing.Optional[jsii.Number] = None,
        traffic_granularity_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name: The name must be 1-63 characters long, and comply with RFC1035. The name must be unique within the security policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#name ComputeSecurityPolicy#name}
        :param auto_deploy_confidence_threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#auto_deploy_confidence_threshold ComputeSecurityPolicy#auto_deploy_confidence_threshold}.
        :param auto_deploy_expiration_sec: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#auto_deploy_expiration_sec ComputeSecurityPolicy#auto_deploy_expiration_sec}.
        :param auto_deploy_impacted_baseline_threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#auto_deploy_impacted_baseline_threshold ComputeSecurityPolicy#auto_deploy_impacted_baseline_threshold}.
        :param auto_deploy_load_threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#auto_deploy_load_threshold ComputeSecurityPolicy#auto_deploy_load_threshold}.
        :param detection_absolute_qps: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#detection_absolute_qps ComputeSecurityPolicy#detection_absolute_qps}.
        :param detection_load_threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#detection_load_threshold ComputeSecurityPolicy#detection_load_threshold}.
        :param detection_relative_to_baseline_qps: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#detection_relative_to_baseline_qps ComputeSecurityPolicy#detection_relative_to_baseline_qps}.
        :param traffic_granularity_configs: traffic_granularity_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#traffic_granularity_configs ComputeSecurityPolicy#traffic_granularity_configs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83e155f3cebd7f21fb13c04667217cff67c2e6f15a4cab87f292e62b36024e6e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument auto_deploy_confidence_threshold", value=auto_deploy_confidence_threshold, expected_type=type_hints["auto_deploy_confidence_threshold"])
            check_type(argname="argument auto_deploy_expiration_sec", value=auto_deploy_expiration_sec, expected_type=type_hints["auto_deploy_expiration_sec"])
            check_type(argname="argument auto_deploy_impacted_baseline_threshold", value=auto_deploy_impacted_baseline_threshold, expected_type=type_hints["auto_deploy_impacted_baseline_threshold"])
            check_type(argname="argument auto_deploy_load_threshold", value=auto_deploy_load_threshold, expected_type=type_hints["auto_deploy_load_threshold"])
            check_type(argname="argument detection_absolute_qps", value=detection_absolute_qps, expected_type=type_hints["detection_absolute_qps"])
            check_type(argname="argument detection_load_threshold", value=detection_load_threshold, expected_type=type_hints["detection_load_threshold"])
            check_type(argname="argument detection_relative_to_baseline_qps", value=detection_relative_to_baseline_qps, expected_type=type_hints["detection_relative_to_baseline_qps"])
            check_type(argname="argument traffic_granularity_configs", value=traffic_granularity_configs, expected_type=type_hints["traffic_granularity_configs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if auto_deploy_confidence_threshold is not None:
            self._values["auto_deploy_confidence_threshold"] = auto_deploy_confidence_threshold
        if auto_deploy_expiration_sec is not None:
            self._values["auto_deploy_expiration_sec"] = auto_deploy_expiration_sec
        if auto_deploy_impacted_baseline_threshold is not None:
            self._values["auto_deploy_impacted_baseline_threshold"] = auto_deploy_impacted_baseline_threshold
        if auto_deploy_load_threshold is not None:
            self._values["auto_deploy_load_threshold"] = auto_deploy_load_threshold
        if detection_absolute_qps is not None:
            self._values["detection_absolute_qps"] = detection_absolute_qps
        if detection_load_threshold is not None:
            self._values["detection_load_threshold"] = detection_load_threshold
        if detection_relative_to_baseline_qps is not None:
            self._values["detection_relative_to_baseline_qps"] = detection_relative_to_baseline_qps
        if traffic_granularity_configs is not None:
            self._values["traffic_granularity_configs"] = traffic_granularity_configs

    @builtins.property
    def name(self) -> builtins.str:
        '''The name must be 1-63 characters long, and comply with RFC1035.

        The name must be unique within the security policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#name ComputeSecurityPolicy#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_deploy_confidence_threshold(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#auto_deploy_confidence_threshold ComputeSecurityPolicy#auto_deploy_confidence_threshold}.'''
        result = self._values.get("auto_deploy_confidence_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def auto_deploy_expiration_sec(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#auto_deploy_expiration_sec ComputeSecurityPolicy#auto_deploy_expiration_sec}.'''
        result = self._values.get("auto_deploy_expiration_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def auto_deploy_impacted_baseline_threshold(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#auto_deploy_impacted_baseline_threshold ComputeSecurityPolicy#auto_deploy_impacted_baseline_threshold}.'''
        result = self._values.get("auto_deploy_impacted_baseline_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def auto_deploy_load_threshold(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#auto_deploy_load_threshold ComputeSecurityPolicy#auto_deploy_load_threshold}.'''
        result = self._values.get("auto_deploy_load_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def detection_absolute_qps(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#detection_absolute_qps ComputeSecurityPolicy#detection_absolute_qps}.'''
        result = self._values.get("detection_absolute_qps")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def detection_load_threshold(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#detection_load_threshold ComputeSecurityPolicy#detection_load_threshold}.'''
        result = self._values.get("detection_load_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def detection_relative_to_baseline_qps(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#detection_relative_to_baseline_qps ComputeSecurityPolicy#detection_relative_to_baseline_qps}.'''
        result = self._values.get("detection_relative_to_baseline_qps")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def traffic_granularity_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs"]]]:
        '''traffic_granularity_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#traffic_granularity_configs ComputeSecurityPolicy#traffic_granularity_configs}
        '''
        result = self._values.get("traffic_granularity_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__34963b99ca2fe6e857b2365d7141ed5185a2a2003674222d97271528906cc8b1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e0860ec128d10fc51f9f8bcc3112f5db25609f9a60d488790ca8c488a226b1d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14b794550a4a2717d507697c7a026affae798e1a6851d102c3b9e2b51a1c4d31)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8490e0edc9b7cf092a715be71e8fa4c489f865b936ea884dd0f83e89190ffd1f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7513af91bcee546f05902756afaa33c3c9ffee948dacf12056614a131ad6a9a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c89aaa1bdd27b577084e3c27c2f18128754bf11bc20e6565b6ace5b1c7472385)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e670a4eab1a311a49c4299c3111f5119cdb0f22dc6c3e4b3029cfdf919939b9f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putTrafficGranularityConfigs")
    def put_traffic_granularity_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc4eec2d2f262894385732609256a0e63db9028e51aefe973c61a496bee73d98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTrafficGranularityConfigs", [value]))

    @jsii.member(jsii_name="resetAutoDeployConfidenceThreshold")
    def reset_auto_deploy_confidence_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoDeployConfidenceThreshold", []))

    @jsii.member(jsii_name="resetAutoDeployExpirationSec")
    def reset_auto_deploy_expiration_sec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoDeployExpirationSec", []))

    @jsii.member(jsii_name="resetAutoDeployImpactedBaselineThreshold")
    def reset_auto_deploy_impacted_baseline_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoDeployImpactedBaselineThreshold", []))

    @jsii.member(jsii_name="resetAutoDeployLoadThreshold")
    def reset_auto_deploy_load_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoDeployLoadThreshold", []))

    @jsii.member(jsii_name="resetDetectionAbsoluteQps")
    def reset_detection_absolute_qps(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDetectionAbsoluteQps", []))

    @jsii.member(jsii_name="resetDetectionLoadThreshold")
    def reset_detection_load_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDetectionLoadThreshold", []))

    @jsii.member(jsii_name="resetDetectionRelativeToBaselineQps")
    def reset_detection_relative_to_baseline_qps(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDetectionRelativeToBaselineQps", []))

    @jsii.member(jsii_name="resetTrafficGranularityConfigs")
    def reset_traffic_granularity_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrafficGranularityConfigs", []))

    @builtins.property
    @jsii.member(jsii_name="trafficGranularityConfigs")
    def traffic_granularity_configs(
        self,
    ) -> "ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigsList":
        return typing.cast("ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigsList", jsii.get(self, "trafficGranularityConfigs"))

    @builtins.property
    @jsii.member(jsii_name="autoDeployConfidenceThresholdInput")
    def auto_deploy_confidence_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "autoDeployConfidenceThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="autoDeployExpirationSecInput")
    def auto_deploy_expiration_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "autoDeployExpirationSecInput"))

    @builtins.property
    @jsii.member(jsii_name="autoDeployImpactedBaselineThresholdInput")
    def auto_deploy_impacted_baseline_threshold_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "autoDeployImpactedBaselineThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="autoDeployLoadThresholdInput")
    def auto_deploy_load_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "autoDeployLoadThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="detectionAbsoluteQpsInput")
    def detection_absolute_qps_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "detectionAbsoluteQpsInput"))

    @builtins.property
    @jsii.member(jsii_name="detectionLoadThresholdInput")
    def detection_load_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "detectionLoadThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="detectionRelativeToBaselineQpsInput")
    def detection_relative_to_baseline_qps_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "detectionRelativeToBaselineQpsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="trafficGranularityConfigsInput")
    def traffic_granularity_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs"]]], jsii.get(self, "trafficGranularityConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="autoDeployConfidenceThreshold")
    def auto_deploy_confidence_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "autoDeployConfidenceThreshold"))

    @auto_deploy_confidence_threshold.setter
    def auto_deploy_confidence_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e767b41278222e2265a1c12f7e9bdccbf4767a65e5453d5242e6523b837e7038)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoDeployConfidenceThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoDeployExpirationSec")
    def auto_deploy_expiration_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "autoDeployExpirationSec"))

    @auto_deploy_expiration_sec.setter
    def auto_deploy_expiration_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44354cc2a8ecb693c0cf897dc309965b25113f23c2676cee0cee18ae14add58a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoDeployExpirationSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoDeployImpactedBaselineThreshold")
    def auto_deploy_impacted_baseline_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "autoDeployImpactedBaselineThreshold"))

    @auto_deploy_impacted_baseline_threshold.setter
    def auto_deploy_impacted_baseline_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a357626efc3992798d03fcbb56b280ffbf2d80de4b3dba6f11befb73cee53eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoDeployImpactedBaselineThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoDeployLoadThreshold")
    def auto_deploy_load_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "autoDeployLoadThreshold"))

    @auto_deploy_load_threshold.setter
    def auto_deploy_load_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__279fb3ef974e07947dc5b56df3d58998b8fe261f24808f7cb97b1aee14f33ace)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoDeployLoadThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="detectionAbsoluteQps")
    def detection_absolute_qps(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "detectionAbsoluteQps"))

    @detection_absolute_qps.setter
    def detection_absolute_qps(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d974eecae6c9f355cbec6f814d512b407e3b2daa5af9fd829313e1738200efd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "detectionAbsoluteQps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="detectionLoadThreshold")
    def detection_load_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "detectionLoadThreshold"))

    @detection_load_threshold.setter
    def detection_load_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f05137315c8c3a056e4ae7274fbf930ef955bd1e1ba46e98f915ee744e9f98e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "detectionLoadThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="detectionRelativeToBaselineQps")
    def detection_relative_to_baseline_qps(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "detectionRelativeToBaselineQps"))

    @detection_relative_to_baseline_qps.setter
    def detection_relative_to_baseline_qps(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5640825b89c28ec82d2ea16fd423306a65720cd8be9f34bf95c743f094a23b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "detectionRelativeToBaselineQps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d972c10364066640686ce7ff36bf2f1d46069eff3fdb02b89fbb11a214679e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73f09ed01a6462299a5b0ca7044993b263ff46407ff248877d205b2b7fe4ec06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "enable_each_unique_value": "enableEachUniqueValue",
        "value": "value",
    },
)
class ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs:
    def __init__(
        self,
        *,
        type: builtins.str,
        enable_each_unique_value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Type of this configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#type ComputeSecurityPolicy#type}
        :param enable_each_unique_value: If enabled, traffic matching each unique value for the specified type constitutes a separate traffic unit. It can only be set to true if value is empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#enable_each_unique_value ComputeSecurityPolicy#enable_each_unique_value}
        :param value: Requests that match this value constitute a granular traffic unit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#value ComputeSecurityPolicy#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8a3bc8f1deeaba37a1e783c90958f3175c5b82aebd6d3baf6bd9e9dc665c477)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument enable_each_unique_value", value=enable_each_unique_value, expected_type=type_hints["enable_each_unique_value"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if enable_each_unique_value is not None:
            self._values["enable_each_unique_value"] = enable_each_unique_value
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def type(self) -> builtins.str:
        '''Type of this configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#type ComputeSecurityPolicy#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enable_each_unique_value(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If enabled, traffic matching each unique value for the specified type constitutes a separate traffic unit.

        It can only be set to true if value is empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#enable_each_unique_value ComputeSecurityPolicy#enable_each_unique_value}
        '''
        result = self._values.get("enable_each_unique_value")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Requests that match this value constitute a granular traffic unit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#value ComputeSecurityPolicy#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79cb202ac0f9010f99df83d4a488383c6ea80c1567598d8bccd7ed1148a7dc7f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80b9dfe8706c435713cac484c1f08d5a76a170f8814b7b8b561b1cba9f96b429)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f3708309b2d1f11981820494883e0b87b01058cb4fb21b0cdf25967b003768f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fe2dc0ed4b4f81e67a137266739a4f1926e0d6cb1a3781ef012c15684db10ed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62e899c0054021862a268a576f50600aed9f017a9638d902921823877ff60319)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a13007df156d186a02850b3a393d6304031c74a791e80e9d9958f09952cec62c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__134a8da58323e8bef745e1d0ec96a4e630a951ee8e8193889045daa1df3aec49)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEnableEachUniqueValue")
    def reset_enable_each_unique_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableEachUniqueValue", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="enableEachUniqueValueInput")
    def enable_each_unique_value_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableEachUniqueValueInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="enableEachUniqueValue")
    def enable_each_unique_value(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableEachUniqueValue"))

    @enable_each_unique_value.setter
    def enable_each_unique_value(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__510e99207755b7a2e935e8df7a5bc3f7b5cdb29ee7cc0ad14e80499e776a0106)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableEachUniqueValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__143415ec9e0a578ec6fbcd6519c3d91901a4d6bd372a3adb03fcc495c0d101cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__748e2102ce3372413b71767839361cd43f4fada9aca2b46f9acc800e13591dc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__978ecdf9cf8f35141c0db87ac2f1b26628630d1279a5991950b89476aec769dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeSecurityPolicyAdaptiveProtectionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyAdaptiveProtectionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eea86d03a5ab8e02ed798f7ca216655049cd4d5c8f1b54940b6ad2697d9e47ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLayer7DdosDefenseConfig")
    def put_layer7_ddos_defense_config(
        self,
        *,
        enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rule_visibility: typing.Optional[builtins.str] = None,
        threshold_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enable: If set to true, enables CAAP for L7 DDoS detection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#enable ComputeSecurityPolicy#enable}
        :param rule_visibility: Rule visibility. Supported values include: "STANDARD", "PREMIUM". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#rule_visibility ComputeSecurityPolicy#rule_visibility}
        :param threshold_configs: threshold_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#threshold_configs ComputeSecurityPolicy#threshold_configs}
        '''
        value = ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig(
            enable=enable,
            rule_visibility=rule_visibility,
            threshold_configs=threshold_configs,
        )

        return typing.cast(None, jsii.invoke(self, "putLayer7DdosDefenseConfig", [value]))

    @jsii.member(jsii_name="resetLayer7DdosDefenseConfig")
    def reset_layer7_ddos_defense_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLayer7DdosDefenseConfig", []))

    @builtins.property
    @jsii.member(jsii_name="layer7DdosDefenseConfig")
    def layer7_ddos_defense_config(
        self,
    ) -> ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigOutputReference:
        return typing.cast(ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigOutputReference, jsii.get(self, "layer7DdosDefenseConfig"))

    @builtins.property
    @jsii.member(jsii_name="layer7DdosDefenseConfigInput")
    def layer7_ddos_defense_config_input(
        self,
    ) -> typing.Optional[ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig], jsii.get(self, "layer7DdosDefenseConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeSecurityPolicyAdaptiveProtectionConfig]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyAdaptiveProtectionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeSecurityPolicyAdaptiveProtectionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84b19164a502b37dc7384a73488fd8c4300fe71ddbfbc0398be0babb55bb29ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyAdvancedOptionsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "json_custom_config": "jsonCustomConfig",
        "json_parsing": "jsonParsing",
        "log_level": "logLevel",
        "user_ip_request_headers": "userIpRequestHeaders",
    },
)
class ComputeSecurityPolicyAdvancedOptionsConfig:
    def __init__(
        self,
        *,
        json_custom_config: typing.Optional[typing.Union["ComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        json_parsing: typing.Optional[builtins.str] = None,
        log_level: typing.Optional[builtins.str] = None,
        user_ip_request_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param json_custom_config: json_custom_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#json_custom_config ComputeSecurityPolicy#json_custom_config}
        :param json_parsing: JSON body parsing. Supported values include: "DISABLED", "STANDARD". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#json_parsing ComputeSecurityPolicy#json_parsing}
        :param log_level: Logging level. Supported values include: "NORMAL", "VERBOSE". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#log_level ComputeSecurityPolicy#log_level}
        :param user_ip_request_headers: An optional list of case-insensitive request header names to use for resolving the callers client IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#user_ip_request_headers ComputeSecurityPolicy#user_ip_request_headers}
        '''
        if isinstance(json_custom_config, dict):
            json_custom_config = ComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfig(**json_custom_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__500d086d3b46d5cd93122d7b3e2eb9fc4cb8d5eeb24beffd2d04a9280c109cb6)
            check_type(argname="argument json_custom_config", value=json_custom_config, expected_type=type_hints["json_custom_config"])
            check_type(argname="argument json_parsing", value=json_parsing, expected_type=type_hints["json_parsing"])
            check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
            check_type(argname="argument user_ip_request_headers", value=user_ip_request_headers, expected_type=type_hints["user_ip_request_headers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if json_custom_config is not None:
            self._values["json_custom_config"] = json_custom_config
        if json_parsing is not None:
            self._values["json_parsing"] = json_parsing
        if log_level is not None:
            self._values["log_level"] = log_level
        if user_ip_request_headers is not None:
            self._values["user_ip_request_headers"] = user_ip_request_headers

    @builtins.property
    def json_custom_config(
        self,
    ) -> typing.Optional["ComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfig"]:
        '''json_custom_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#json_custom_config ComputeSecurityPolicy#json_custom_config}
        '''
        result = self._values.get("json_custom_config")
        return typing.cast(typing.Optional["ComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfig"], result)

    @builtins.property
    def json_parsing(self) -> typing.Optional[builtins.str]:
        '''JSON body parsing. Supported values include: "DISABLED", "STANDARD".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#json_parsing ComputeSecurityPolicy#json_parsing}
        '''
        result = self._values.get("json_parsing")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_level(self) -> typing.Optional[builtins.str]:
        '''Logging level. Supported values include: "NORMAL", "VERBOSE".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#log_level ComputeSecurityPolicy#log_level}
        '''
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_ip_request_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An optional list of case-insensitive request header names to use for resolving the callers client IP address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#user_ip_request_headers ComputeSecurityPolicy#user_ip_request_headers}
        '''
        result = self._values.get("user_ip_request_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyAdvancedOptionsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfig",
    jsii_struct_bases=[],
    name_mapping={"content_types": "contentTypes"},
)
class ComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfig:
    def __init__(self, *, content_types: typing.Sequence[builtins.str]) -> None:
        '''
        :param content_types: A list of custom Content-Type header values to apply the JSON parsing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#content_types ComputeSecurityPolicy#content_types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb438a3770599a7060e8985213810cf127f624adf96f5f8c7892cb4ccf8be8c9)
            check_type(argname="argument content_types", value=content_types, expected_type=type_hints["content_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content_types": content_types,
        }

    @builtins.property
    def content_types(self) -> typing.List[builtins.str]:
        '''A list of custom Content-Type header values to apply the JSON parsing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#content_types ComputeSecurityPolicy#content_types}
        '''
        result = self._values.get("content_types")
        assert result is not None, "Required property 'content_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50adcd9096cba16307f01484481b6548777d3fab8d75f42fd6f430c74c7f2f6b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="contentTypesInput")
    def content_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "contentTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="contentTypes")
    def content_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "contentTypes"))

    @content_types.setter
    def content_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9320d9243e5054f17188c72ca115d9d6f1f110750661e74b4aa2968e15f30f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfig]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__180cb74e067673d5caa2c518e8ed741d7d573a49cc9d83be7e01802068bc6d78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeSecurityPolicyAdvancedOptionsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyAdvancedOptionsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ce4bc4833a72106db1abbb69fa2d44a78065af930dd1b2c97f21ec140e2ca41)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putJsonCustomConfig")
    def put_json_custom_config(
        self,
        *,
        content_types: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param content_types: A list of custom Content-Type header values to apply the JSON parsing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#content_types ComputeSecurityPolicy#content_types}
        '''
        value = ComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfig(
            content_types=content_types
        )

        return typing.cast(None, jsii.invoke(self, "putJsonCustomConfig", [value]))

    @jsii.member(jsii_name="resetJsonCustomConfig")
    def reset_json_custom_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJsonCustomConfig", []))

    @jsii.member(jsii_name="resetJsonParsing")
    def reset_json_parsing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJsonParsing", []))

    @jsii.member(jsii_name="resetLogLevel")
    def reset_log_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogLevel", []))

    @jsii.member(jsii_name="resetUserIpRequestHeaders")
    def reset_user_ip_request_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserIpRequestHeaders", []))

    @builtins.property
    @jsii.member(jsii_name="jsonCustomConfig")
    def json_custom_config(
        self,
    ) -> ComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfigOutputReference:
        return typing.cast(ComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfigOutputReference, jsii.get(self, "jsonCustomConfig"))

    @builtins.property
    @jsii.member(jsii_name="jsonCustomConfigInput")
    def json_custom_config_input(
        self,
    ) -> typing.Optional[ComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfig]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfig], jsii.get(self, "jsonCustomConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="jsonParsingInput")
    def json_parsing_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jsonParsingInput"))

    @builtins.property
    @jsii.member(jsii_name="logLevelInput")
    def log_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="userIpRequestHeadersInput")
    def user_ip_request_headers_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "userIpRequestHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="jsonParsing")
    def json_parsing(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jsonParsing"))

    @json_parsing.setter
    def json_parsing(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08c2a9933288e7f5e5c08bffc64c081e2fb1915a7dfd5260c61bcd25b2e8e9d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jsonParsing", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logLevel")
    def log_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logLevel"))

    @log_level.setter
    def log_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c650944ee4f47f7d8179f3768e9ece58fa0b2ef5e5b3749a853aaf2829e3e04d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userIpRequestHeaders")
    def user_ip_request_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "userIpRequestHeaders"))

    @user_ip_request_headers.setter
    def user_ip_request_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b728edb0b9c2f2fe38b376e9253365ac391b2871979c79c742d582cad4fe07e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userIpRequestHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeSecurityPolicyAdvancedOptionsConfig]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyAdvancedOptionsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeSecurityPolicyAdvancedOptionsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d87de7ea9e0db2366eba14f6d191c15740f0bd1023a1d97d0805225f8055f2ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyConfig",
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
        "adaptive_protection_config": "adaptiveProtectionConfig",
        "advanced_options_config": "advancedOptionsConfig",
        "description": "description",
        "id": "id",
        "project": "project",
        "recaptcha_options_config": "recaptchaOptionsConfig",
        "rule": "rule",
        "timeouts": "timeouts",
        "type": "type",
    },
)
class ComputeSecurityPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        adaptive_protection_config: typing.Optional[typing.Union[ComputeSecurityPolicyAdaptiveProtectionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        advanced_options_config: typing.Optional[typing.Union[ComputeSecurityPolicyAdvancedOptionsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        recaptcha_options_config: typing.Optional[typing.Union["ComputeSecurityPolicyRecaptchaOptionsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["ComputeSecurityPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The name of the security policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#name ComputeSecurityPolicy#name}
        :param adaptive_protection_config: adaptive_protection_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#adaptive_protection_config ComputeSecurityPolicy#adaptive_protection_config}
        :param advanced_options_config: advanced_options_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#advanced_options_config ComputeSecurityPolicy#advanced_options_config}
        :param description: An optional description of this security policy. Max size is 2048. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#description ComputeSecurityPolicy#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#id ComputeSecurityPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: The project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#project ComputeSecurityPolicy#project}
        :param recaptcha_options_config: recaptcha_options_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#recaptcha_options_config ComputeSecurityPolicy#recaptcha_options_config}
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#rule ComputeSecurityPolicy#rule}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#timeouts ComputeSecurityPolicy#timeouts}
        :param type: The type indicates the intended use of the security policy. CLOUD_ARMOR - Cloud Armor backend security policies can be configured to filter incoming HTTP requests targeting backend services. They filter requests before they hit the origin servers. CLOUD_ARMOR_EDGE - Cloud Armor edge security policies can be configured to filter incoming HTTP requests targeting backend services (including Cloud CDN-enabled) as well as backend buckets (Cloud Storage). They filter requests before the request is served from Google's cache. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#type ComputeSecurityPolicy#type}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(adaptive_protection_config, dict):
            adaptive_protection_config = ComputeSecurityPolicyAdaptiveProtectionConfig(**adaptive_protection_config)
        if isinstance(advanced_options_config, dict):
            advanced_options_config = ComputeSecurityPolicyAdvancedOptionsConfig(**advanced_options_config)
        if isinstance(recaptcha_options_config, dict):
            recaptcha_options_config = ComputeSecurityPolicyRecaptchaOptionsConfig(**recaptcha_options_config)
        if isinstance(timeouts, dict):
            timeouts = ComputeSecurityPolicyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c97d006ac70967c06c652a6605bacecfa15cfcba384633db1ceb0256c7b9150)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument adaptive_protection_config", value=adaptive_protection_config, expected_type=type_hints["adaptive_protection_config"])
            check_type(argname="argument advanced_options_config", value=advanced_options_config, expected_type=type_hints["advanced_options_config"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument recaptcha_options_config", value=recaptcha_options_config, expected_type=type_hints["recaptcha_options_config"])
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
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
        if adaptive_protection_config is not None:
            self._values["adaptive_protection_config"] = adaptive_protection_config
        if advanced_options_config is not None:
            self._values["advanced_options_config"] = advanced_options_config
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
        if recaptcha_options_config is not None:
            self._values["recaptcha_options_config"] = recaptcha_options_config
        if rule is not None:
            self._values["rule"] = rule
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if type is not None:
            self._values["type"] = type

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
        '''The name of the security policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#name ComputeSecurityPolicy#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def adaptive_protection_config(
        self,
    ) -> typing.Optional[ComputeSecurityPolicyAdaptiveProtectionConfig]:
        '''adaptive_protection_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#adaptive_protection_config ComputeSecurityPolicy#adaptive_protection_config}
        '''
        result = self._values.get("adaptive_protection_config")
        return typing.cast(typing.Optional[ComputeSecurityPolicyAdaptiveProtectionConfig], result)

    @builtins.property
    def advanced_options_config(
        self,
    ) -> typing.Optional[ComputeSecurityPolicyAdvancedOptionsConfig]:
        '''advanced_options_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#advanced_options_config ComputeSecurityPolicy#advanced_options_config}
        '''
        result = self._values.get("advanced_options_config")
        return typing.cast(typing.Optional[ComputeSecurityPolicyAdvancedOptionsConfig], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this security policy. Max size is 2048.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#description ComputeSecurityPolicy#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#id ComputeSecurityPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The project in which the resource belongs. If it is not provided, the provider project is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#project ComputeSecurityPolicy#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recaptcha_options_config(
        self,
    ) -> typing.Optional["ComputeSecurityPolicyRecaptchaOptionsConfig"]:
        '''recaptcha_options_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#recaptcha_options_config ComputeSecurityPolicy#recaptcha_options_config}
        '''
        result = self._values.get("recaptcha_options_config")
        return typing.cast(typing.Optional["ComputeSecurityPolicyRecaptchaOptionsConfig"], result)

    @builtins.property
    def rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRule"]]]:
        '''rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#rule ComputeSecurityPolicy#rule}
        '''
        result = self._values.get("rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRule"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeSecurityPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#timeouts ComputeSecurityPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeSecurityPolicyTimeouts"], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type indicates the intended use of the security policy.

        CLOUD_ARMOR - Cloud Armor backend security policies can be configured to filter incoming HTTP requests targeting backend services. They filter requests before they hit the origin servers. CLOUD_ARMOR_EDGE - Cloud Armor edge security policies can be configured to filter incoming HTTP requests targeting backend services (including Cloud CDN-enabled) as well as backend buckets (Cloud Storage). They filter requests before the request is served from Google's cache.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#type ComputeSecurityPolicy#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRecaptchaOptionsConfig",
    jsii_struct_bases=[],
    name_mapping={"redirect_site_key": "redirectSiteKey"},
)
class ComputeSecurityPolicyRecaptchaOptionsConfig:
    def __init__(self, *, redirect_site_key: builtins.str) -> None:
        '''
        :param redirect_site_key: A field to supply a reCAPTCHA site key to be used for all the rules using the redirect action with the type of GOOGLE_RECAPTCHA under the security policy. The specified site key needs to be created from the reCAPTCHA API. The user is responsible for the validity of the specified site key. If not specified, a Google-managed site key is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#redirect_site_key ComputeSecurityPolicy#redirect_site_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b068fe9b98a44fb6a6aa907fd051099b34f7e8d1352488cff62bcfeae8b0c84e)
            check_type(argname="argument redirect_site_key", value=redirect_site_key, expected_type=type_hints["redirect_site_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "redirect_site_key": redirect_site_key,
        }

    @builtins.property
    def redirect_site_key(self) -> builtins.str:
        '''A field to supply a reCAPTCHA site key to be used for all the rules using the redirect action with the type of GOOGLE_RECAPTCHA under the security policy.

        The specified site key needs to be created from the reCAPTCHA API. The user is responsible for the validity of the specified site key. If not specified, a Google-managed site key is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#redirect_site_key ComputeSecurityPolicy#redirect_site_key}
        '''
        result = self._values.get("redirect_site_key")
        assert result is not None, "Required property 'redirect_site_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRecaptchaOptionsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyRecaptchaOptionsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRecaptchaOptionsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__885be4404a8b5093ce256dd04ce73b756036913abe822d6d5b90e80df0a435b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="redirectSiteKeyInput")
    def redirect_site_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectSiteKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectSiteKey")
    def redirect_site_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectSiteKey"))

    @redirect_site_key.setter
    def redirect_site_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__496efa2250c8d2f1ee3c2bf14725ee4e46cfcd3ebd5b7272488353f583e38d9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectSiteKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeSecurityPolicyRecaptchaOptionsConfig]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyRecaptchaOptionsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeSecurityPolicyRecaptchaOptionsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c22e4d3904a31ad4e81c4bac230c381597419f12bb1a54f906089ec239b16e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRule",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "match": "match",
        "priority": "priority",
        "description": "description",
        "header_action": "headerAction",
        "preconfigured_waf_config": "preconfiguredWafConfig",
        "preview": "preview",
        "rate_limit_options": "rateLimitOptions",
        "redirect_options": "redirectOptions",
    },
)
class ComputeSecurityPolicyRule:
    def __init__(
        self,
        *,
        action: builtins.str,
        match: typing.Union["ComputeSecurityPolicyRuleMatch", typing.Dict[builtins.str, typing.Any]],
        priority: jsii.Number,
        description: typing.Optional[builtins.str] = None,
        header_action: typing.Optional[typing.Union["ComputeSecurityPolicyRuleHeaderAction", typing.Dict[builtins.str, typing.Any]]] = None,
        preconfigured_waf_config: typing.Optional[typing.Union["ComputeSecurityPolicyRulePreconfiguredWafConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        preview: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rate_limit_options: typing.Optional[typing.Union["ComputeSecurityPolicyRuleRateLimitOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        redirect_options: typing.Optional[typing.Union["ComputeSecurityPolicyRuleRedirectOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param action: Action to take when match matches the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#action ComputeSecurityPolicy#action}
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#match ComputeSecurityPolicy#match}
        :param priority: An unique positive integer indicating the priority of evaluation for a rule. Rules are evaluated from highest priority (lowest numerically) to lowest priority (highest numerically) in order. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#priority ComputeSecurityPolicy#priority}
        :param description: An optional description of this rule. Max size is 64. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#description ComputeSecurityPolicy#description}
        :param header_action: header_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#header_action ComputeSecurityPolicy#header_action}
        :param preconfigured_waf_config: preconfigured_waf_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#preconfigured_waf_config ComputeSecurityPolicy#preconfigured_waf_config}
        :param preview: When set to true, the action specified above is not enforced. Stackdriver logs for requests that trigger a preview action are annotated as such. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#preview ComputeSecurityPolicy#preview}
        :param rate_limit_options: rate_limit_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#rate_limit_options ComputeSecurityPolicy#rate_limit_options}
        :param redirect_options: redirect_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#redirect_options ComputeSecurityPolicy#redirect_options}
        '''
        if isinstance(match, dict):
            match = ComputeSecurityPolicyRuleMatch(**match)
        if isinstance(header_action, dict):
            header_action = ComputeSecurityPolicyRuleHeaderAction(**header_action)
        if isinstance(preconfigured_waf_config, dict):
            preconfigured_waf_config = ComputeSecurityPolicyRulePreconfiguredWafConfig(**preconfigured_waf_config)
        if isinstance(rate_limit_options, dict):
            rate_limit_options = ComputeSecurityPolicyRuleRateLimitOptions(**rate_limit_options)
        if isinstance(redirect_options, dict):
            redirect_options = ComputeSecurityPolicyRuleRedirectOptions(**redirect_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae0fcd526221b8cb2a77e91ef8175c0230c3eabcfed66475e14cb40aba3a579d)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument header_action", value=header_action, expected_type=type_hints["header_action"])
            check_type(argname="argument preconfigured_waf_config", value=preconfigured_waf_config, expected_type=type_hints["preconfigured_waf_config"])
            check_type(argname="argument preview", value=preview, expected_type=type_hints["preview"])
            check_type(argname="argument rate_limit_options", value=rate_limit_options, expected_type=type_hints["rate_limit_options"])
            check_type(argname="argument redirect_options", value=redirect_options, expected_type=type_hints["redirect_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "match": match,
            "priority": priority,
        }
        if description is not None:
            self._values["description"] = description
        if header_action is not None:
            self._values["header_action"] = header_action
        if preconfigured_waf_config is not None:
            self._values["preconfigured_waf_config"] = preconfigured_waf_config
        if preview is not None:
            self._values["preview"] = preview
        if rate_limit_options is not None:
            self._values["rate_limit_options"] = rate_limit_options
        if redirect_options is not None:
            self._values["redirect_options"] = redirect_options

    @builtins.property
    def action(self) -> builtins.str:
        '''Action to take when match matches the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#action ComputeSecurityPolicy#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def match(self) -> "ComputeSecurityPolicyRuleMatch":
        '''match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#match ComputeSecurityPolicy#match}
        '''
        result = self._values.get("match")
        assert result is not None, "Required property 'match' is missing"
        return typing.cast("ComputeSecurityPolicyRuleMatch", result)

    @builtins.property
    def priority(self) -> jsii.Number:
        '''An unique positive integer indicating the priority of evaluation for a rule.

        Rules are evaluated from highest priority (lowest numerically) to lowest priority (highest numerically) in order.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#priority ComputeSecurityPolicy#priority}
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this rule. Max size is 64.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#description ComputeSecurityPolicy#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def header_action(self) -> typing.Optional["ComputeSecurityPolicyRuleHeaderAction"]:
        '''header_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#header_action ComputeSecurityPolicy#header_action}
        '''
        result = self._values.get("header_action")
        return typing.cast(typing.Optional["ComputeSecurityPolicyRuleHeaderAction"], result)

    @builtins.property
    def preconfigured_waf_config(
        self,
    ) -> typing.Optional["ComputeSecurityPolicyRulePreconfiguredWafConfig"]:
        '''preconfigured_waf_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#preconfigured_waf_config ComputeSecurityPolicy#preconfigured_waf_config}
        '''
        result = self._values.get("preconfigured_waf_config")
        return typing.cast(typing.Optional["ComputeSecurityPolicyRulePreconfiguredWafConfig"], result)

    @builtins.property
    def preview(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When set to true, the action specified above is not enforced.

        Stackdriver logs for requests that trigger a preview action are annotated as such.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#preview ComputeSecurityPolicy#preview}
        '''
        result = self._values.get("preview")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def rate_limit_options(
        self,
    ) -> typing.Optional["ComputeSecurityPolicyRuleRateLimitOptions"]:
        '''rate_limit_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#rate_limit_options ComputeSecurityPolicy#rate_limit_options}
        '''
        result = self._values.get("rate_limit_options")
        return typing.cast(typing.Optional["ComputeSecurityPolicyRuleRateLimitOptions"], result)

    @builtins.property
    def redirect_options(
        self,
    ) -> typing.Optional["ComputeSecurityPolicyRuleRedirectOptions"]:
        '''redirect_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#redirect_options ComputeSecurityPolicy#redirect_options}
        '''
        result = self._values.get("redirect_options")
        return typing.cast(typing.Optional["ComputeSecurityPolicyRuleRedirectOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRuleHeaderAction",
    jsii_struct_bases=[],
    name_mapping={"request_headers_to_adds": "requestHeadersToAdds"},
)
class ComputeSecurityPolicyRuleHeaderAction:
    def __init__(
        self,
        *,
        request_headers_to_adds: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param request_headers_to_adds: request_headers_to_adds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#request_headers_to_adds ComputeSecurityPolicy#request_headers_to_adds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6e5af6a32266044b5ce1b2973a8f8a74429cbf3cc1ec110764d8575ec3bc4bd)
            check_type(argname="argument request_headers_to_adds", value=request_headers_to_adds, expected_type=type_hints["request_headers_to_adds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "request_headers_to_adds": request_headers_to_adds,
        }

    @builtins.property
    def request_headers_to_adds(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds"]]:
        '''request_headers_to_adds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#request_headers_to_adds ComputeSecurityPolicy#request_headers_to_adds}
        '''
        result = self._values.get("request_headers_to_adds")
        assert result is not None, "Required property 'request_headers_to_adds' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRuleHeaderAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyRuleHeaderActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRuleHeaderActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f6161c2b3dd3a49183d4e0f49c02a02cf5606a8be30066bdb102b325287cc88)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRequestHeadersToAdds")
    def put_request_headers_to_adds(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10a217310dc7342aee447c93826cc16903e230c24e0313a9b9415949a259f56f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestHeadersToAdds", [value]))

    @builtins.property
    @jsii.member(jsii_name="requestHeadersToAdds")
    def request_headers_to_adds(
        self,
    ) -> "ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsList":
        return typing.cast("ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsList", jsii.get(self, "requestHeadersToAdds"))

    @builtins.property
    @jsii.member(jsii_name="requestHeadersToAddsInput")
    def request_headers_to_adds_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds"]]], jsii.get(self, "requestHeadersToAddsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeSecurityPolicyRuleHeaderAction]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyRuleHeaderAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeSecurityPolicyRuleHeaderAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4f94582f2f528842e2a2c32ebea9a79fcd34d3fdbebe881b3390c6ab5e9599e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds",
    jsii_struct_bases=[],
    name_mapping={"header_name": "headerName", "header_value": "headerValue"},
)
class ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds:
    def __init__(
        self,
        *,
        header_name: builtins.str,
        header_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param header_name: The name of the header to set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#header_name ComputeSecurityPolicy#header_name}
        :param header_value: The value to set the named header to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#header_value ComputeSecurityPolicy#header_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a27d30e52936fe3622e42e0df85c5fd9ab5a91eeefc5373a0b73231f176060d)
            check_type(argname="argument header_name", value=header_name, expected_type=type_hints["header_name"])
            check_type(argname="argument header_value", value=header_value, expected_type=type_hints["header_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "header_name": header_name,
        }
        if header_value is not None:
            self._values["header_value"] = header_value

    @builtins.property
    def header_name(self) -> builtins.str:
        '''The name of the header to set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#header_name ComputeSecurityPolicy#header_name}
        '''
        result = self._values.get("header_name")
        assert result is not None, "Required property 'header_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def header_value(self) -> typing.Optional[builtins.str]:
        '''The value to set the named header to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#header_value ComputeSecurityPolicy#header_value}
        '''
        result = self._values.get("header_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6212324e258068ee60834543691245f0e9f03033eeec524161391d3c667c536)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68fdf236a66e51328c08444ffccb239137dccf86e49163ba25b91f1b79aa78d1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6545aee55fb954e1e8bdc46d3b707e24924e516ff1f9ec4c1119da465abff801)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b14c5c98cf86ef621ae03ce4f72d86afd2738e2ce1a54b04544f4850243f258f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf52dee9f6b3049130c9661274c9f6c199744ee3484b525bacaf07631b9f84e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38ff1e2ff5bfb420e41cd853d478d9e9a2d6bcbc60b0c29f250d97c16d969d44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5fa0c8b079e0d34f2a4819ba77536445247203c85a7b22586fc454a714a225d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetHeaderValue")
    def reset_header_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaderValue", []))

    @builtins.property
    @jsii.member(jsii_name="headerNameInput")
    def header_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "headerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="headerValueInput")
    def header_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "headerValueInput"))

    @builtins.property
    @jsii.member(jsii_name="headerName")
    def header_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerName"))

    @header_name.setter
    def header_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d433e9e3b4f472ae17b94477ee2d4c7e1b1f8065057ce9d279e4593fc735b0de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headerValue")
    def header_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerValue"))

    @header_value.setter
    def header_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a45104a09e4fd126dd94b0ea426b8294b45e58ac24b29f600597909010dec0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8270828ab9c7623cb48ae480aea52630e8d9779007ba2344bc3ea62c2969569b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeSecurityPolicyRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__231e3b1ac9dd65130f8f5bc56dcb2797fa5d5cb217b9b23d9b7d4620028d987d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ComputeSecurityPolicyRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71d3b75a58ab15d230d71101cf3a1507fbd1293ec5687dd1c32e07a8a2919cd2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeSecurityPolicyRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a50034553ab2b2a917c8389a7c3b3083119cc43da37649381af5f6a300e57b0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__10be10a2e22ba09a432818a8ebea01395fbee1d3c9961e547515d15092706bcc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5023f4d00bf38d78b323a963c5784fa035a7f1cbce40e43cbec203dfdbfe83a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bae9bd7f692d4e917b34319df5f5fdc581837e21c17795159eceb1e30c7ee4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRuleMatch",
    jsii_struct_bases=[],
    name_mapping={
        "config": "config",
        "expr": "expr",
        "expr_options": "exprOptions",
        "versioned_expr": "versionedExpr",
    },
)
class ComputeSecurityPolicyRuleMatch:
    def __init__(
        self,
        *,
        config: typing.Optional[typing.Union["ComputeSecurityPolicyRuleMatchConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        expr: typing.Optional[typing.Union["ComputeSecurityPolicyRuleMatchExpr", typing.Dict[builtins.str, typing.Any]]] = None,
        expr_options: typing.Optional[typing.Union["ComputeSecurityPolicyRuleMatchExprOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        versioned_expr: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#config ComputeSecurityPolicy#config}
        :param expr: expr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#expr ComputeSecurityPolicy#expr}
        :param expr_options: expr_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#expr_options ComputeSecurityPolicy#expr_options}
        :param versioned_expr: Predefined rule expression. If this field is specified, config must also be specified. Available options: SRC_IPS_V1: Must specify the corresponding src_ip_ranges field in config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#versioned_expr ComputeSecurityPolicy#versioned_expr}
        '''
        if isinstance(config, dict):
            config = ComputeSecurityPolicyRuleMatchConfig(**config)
        if isinstance(expr, dict):
            expr = ComputeSecurityPolicyRuleMatchExpr(**expr)
        if isinstance(expr_options, dict):
            expr_options = ComputeSecurityPolicyRuleMatchExprOptions(**expr_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5c17b5f190a675920cf8b7ed3aeb1ac1b5d30e311ee6b3ceb46042dddfc1bf2)
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument expr", value=expr, expected_type=type_hints["expr"])
            check_type(argname="argument expr_options", value=expr_options, expected_type=type_hints["expr_options"])
            check_type(argname="argument versioned_expr", value=versioned_expr, expected_type=type_hints["versioned_expr"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if config is not None:
            self._values["config"] = config
        if expr is not None:
            self._values["expr"] = expr
        if expr_options is not None:
            self._values["expr_options"] = expr_options
        if versioned_expr is not None:
            self._values["versioned_expr"] = versioned_expr

    @builtins.property
    def config(self) -> typing.Optional["ComputeSecurityPolicyRuleMatchConfig"]:
        '''config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#config ComputeSecurityPolicy#config}
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional["ComputeSecurityPolicyRuleMatchConfig"], result)

    @builtins.property
    def expr(self) -> typing.Optional["ComputeSecurityPolicyRuleMatchExpr"]:
        '''expr block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#expr ComputeSecurityPolicy#expr}
        '''
        result = self._values.get("expr")
        return typing.cast(typing.Optional["ComputeSecurityPolicyRuleMatchExpr"], result)

    @builtins.property
    def expr_options(
        self,
    ) -> typing.Optional["ComputeSecurityPolicyRuleMatchExprOptions"]:
        '''expr_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#expr_options ComputeSecurityPolicy#expr_options}
        '''
        result = self._values.get("expr_options")
        return typing.cast(typing.Optional["ComputeSecurityPolicyRuleMatchExprOptions"], result)

    @builtins.property
    def versioned_expr(self) -> typing.Optional[builtins.str]:
        '''Predefined rule expression.

        If this field is specified, config must also be specified. Available options:   SRC_IPS_V1: Must specify the corresponding src_ip_ranges field in config.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#versioned_expr ComputeSecurityPolicy#versioned_expr}
        '''
        result = self._values.get("versioned_expr")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRuleMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRuleMatchConfig",
    jsii_struct_bases=[],
    name_mapping={"src_ip_ranges": "srcIpRanges"},
)
class ComputeSecurityPolicyRuleMatchConfig:
    def __init__(self, *, src_ip_ranges: typing.Sequence[builtins.str]) -> None:
        '''
        :param src_ip_ranges: Set of IP addresses or ranges (IPV4 or IPV6) in CIDR notation to match against inbound traffic. There is a limit of 10 IP ranges per rule. A value of '*' matches all IPs (can be used to override the default behavior). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#src_ip_ranges ComputeSecurityPolicy#src_ip_ranges}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7f0131dcc111c41d2dc494a82ab9e7a9ed28d4c8daf78f24f5d4f6b362d5486)
            check_type(argname="argument src_ip_ranges", value=src_ip_ranges, expected_type=type_hints["src_ip_ranges"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "src_ip_ranges": src_ip_ranges,
        }

    @builtins.property
    def src_ip_ranges(self) -> typing.List[builtins.str]:
        '''Set of IP addresses or ranges (IPV4 or IPV6) in CIDR notation to match against inbound traffic.

        There is a limit of 10 IP ranges per rule. A value of '*' matches all IPs (can be used to override the default behavior).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#src_ip_ranges ComputeSecurityPolicy#src_ip_ranges}
        '''
        result = self._values.get("src_ip_ranges")
        assert result is not None, "Required property 'src_ip_ranges' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRuleMatchConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyRuleMatchConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRuleMatchConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__170e7681e03cd93ea3b9e85df3ec1220d1ce3ee46021dd9c2e5f04a376a77a01)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="srcIpRangesInput")
    def src_ip_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "srcIpRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="srcIpRanges")
    def src_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcIpRanges"))

    @src_ip_ranges.setter
    def src_ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b04947e950a256ae1a5f76bd2253d7d6a2318ce736f9af4f73c5403b759e342)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcIpRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeSecurityPolicyRuleMatchConfig]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyRuleMatchConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeSecurityPolicyRuleMatchConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd9faf10aad162e9024c8a541c911939d30f9f8e8b4adfadbfeaa1efe2ae5b1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRuleMatchExpr",
    jsii_struct_bases=[],
    name_mapping={"expression": "expression"},
)
class ComputeSecurityPolicyRuleMatchExpr:
    def __init__(self, *, expression: builtins.str) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. The application context of the containing message determines which well-known feature set of CEL is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#expression ComputeSecurityPolicy#expression}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37c7b584a5b111ec379bd0db55777d6bbfebe64b4c2d60dfa57f90fd8fac28fb)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "expression": expression,
        }

    @builtins.property
    def expression(self) -> builtins.str:
        '''Textual representation of an expression in Common Expression Language syntax.

        The application context of the containing message determines which well-known feature set of CEL is supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#expression ComputeSecurityPolicy#expression}
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRuleMatchExpr(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRuleMatchExprOptions",
    jsii_struct_bases=[],
    name_mapping={"recaptcha_options": "recaptchaOptions"},
)
class ComputeSecurityPolicyRuleMatchExprOptions:
    def __init__(
        self,
        *,
        recaptcha_options: typing.Union["ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptions", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param recaptcha_options: recaptcha_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#recaptcha_options ComputeSecurityPolicy#recaptcha_options}
        '''
        if isinstance(recaptcha_options, dict):
            recaptcha_options = ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptions(**recaptcha_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8742467b22d0f6d459645ccdf1507ee48250585c97cf2a4bd2ee3d054b6edd5b)
            check_type(argname="argument recaptcha_options", value=recaptcha_options, expected_type=type_hints["recaptcha_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "recaptcha_options": recaptcha_options,
        }

    @builtins.property
    def recaptcha_options(
        self,
    ) -> "ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptions":
        '''recaptcha_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#recaptcha_options ComputeSecurityPolicy#recaptcha_options}
        '''
        result = self._values.get("recaptcha_options")
        assert result is not None, "Required property 'recaptcha_options' is missing"
        return typing.cast("ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptions", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRuleMatchExprOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyRuleMatchExprOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRuleMatchExprOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e99f5efc8d6bae82f8b3a80b23df2112fbf3363461ef8ea6832daf7b0354e56d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRecaptchaOptions")
    def put_recaptcha_options(
        self,
        *,
        action_token_site_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        session_token_site_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param action_token_site_keys: A list of site keys to be used during the validation of reCAPTCHA action-tokens. The provided site keys need to be created from reCAPTCHA API under the same project where the security policy is created Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#action_token_site_keys ComputeSecurityPolicy#action_token_site_keys}
        :param session_token_site_keys: A list of site keys to be used during the validation of reCAPTCHA session-tokens. The provided site keys need to be created from reCAPTCHA API under the same project where the security policy is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#session_token_site_keys ComputeSecurityPolicy#session_token_site_keys}
        '''
        value = ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptions(
            action_token_site_keys=action_token_site_keys,
            session_token_site_keys=session_token_site_keys,
        )

        return typing.cast(None, jsii.invoke(self, "putRecaptchaOptions", [value]))

    @builtins.property
    @jsii.member(jsii_name="recaptchaOptions")
    def recaptcha_options(
        self,
    ) -> "ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsOutputReference":
        return typing.cast("ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsOutputReference", jsii.get(self, "recaptchaOptions"))

    @builtins.property
    @jsii.member(jsii_name="recaptchaOptionsInput")
    def recaptcha_options_input(
        self,
    ) -> typing.Optional["ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptions"]:
        return typing.cast(typing.Optional["ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptions"], jsii.get(self, "recaptchaOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeSecurityPolicyRuleMatchExprOptions]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyRuleMatchExprOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeSecurityPolicyRuleMatchExprOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31309abf56b081f47344740cd0de955007dca6d675a20a82d91b84ab608be3d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptions",
    jsii_struct_bases=[],
    name_mapping={
        "action_token_site_keys": "actionTokenSiteKeys",
        "session_token_site_keys": "sessionTokenSiteKeys",
    },
)
class ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptions:
    def __init__(
        self,
        *,
        action_token_site_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        session_token_site_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param action_token_site_keys: A list of site keys to be used during the validation of reCAPTCHA action-tokens. The provided site keys need to be created from reCAPTCHA API under the same project where the security policy is created Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#action_token_site_keys ComputeSecurityPolicy#action_token_site_keys}
        :param session_token_site_keys: A list of site keys to be used during the validation of reCAPTCHA session-tokens. The provided site keys need to be created from reCAPTCHA API under the same project where the security policy is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#session_token_site_keys ComputeSecurityPolicy#session_token_site_keys}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4768378bf15b08167c79d4634a54081d43ee99cecff751b629e051879767972)
            check_type(argname="argument action_token_site_keys", value=action_token_site_keys, expected_type=type_hints["action_token_site_keys"])
            check_type(argname="argument session_token_site_keys", value=session_token_site_keys, expected_type=type_hints["session_token_site_keys"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action_token_site_keys is not None:
            self._values["action_token_site_keys"] = action_token_site_keys
        if session_token_site_keys is not None:
            self._values["session_token_site_keys"] = session_token_site_keys

    @builtins.property
    def action_token_site_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of site keys to be used during the validation of reCAPTCHA action-tokens.

        The provided site keys need to be created from reCAPTCHA API under the same project where the security policy is created

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#action_token_site_keys ComputeSecurityPolicy#action_token_site_keys}
        '''
        result = self._values.get("action_token_site_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def session_token_site_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of site keys to be used during the validation of reCAPTCHA session-tokens.

        The provided site keys need to be created from reCAPTCHA API under the same project where the security policy is created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#session_token_site_keys ComputeSecurityPolicy#session_token_site_keys}
        '''
        result = self._values.get("session_token_site_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__effaa0f12d053f180cdd5faff5b7e6ae42e0571c23424af213702acab6a7757c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetActionTokenSiteKeys")
    def reset_action_token_site_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActionTokenSiteKeys", []))

    @jsii.member(jsii_name="resetSessionTokenSiteKeys")
    def reset_session_token_site_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionTokenSiteKeys", []))

    @builtins.property
    @jsii.member(jsii_name="actionTokenSiteKeysInput")
    def action_token_site_keys_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "actionTokenSiteKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionTokenSiteKeysInput")
    def session_token_site_keys_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sessionTokenSiteKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="actionTokenSiteKeys")
    def action_token_site_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "actionTokenSiteKeys"))

    @action_token_site_keys.setter
    def action_token_site_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b7aa4e0cf7be4bd25d112151fb0baea83893654de849703d54589dbb02ffd9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionTokenSiteKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionTokenSiteKeys")
    def session_token_site_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sessionTokenSiteKeys"))

    @session_token_site_keys.setter
    def session_token_site_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a956149f51ea33679cbcbdc93133f6c93901fb6708328416b6df94ab822cac19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionTokenSiteKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptions]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20cfd09c41e73ad847b0e374b2ba5d98d8209bedcefeefb20b93754aac08ccee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeSecurityPolicyRuleMatchExprOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRuleMatchExprOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f58206deb22370e0d9c1788f567955151d87180f8e965c916aa6a1dd5d553e9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="expressionInput")
    def expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expressionInput"))

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d000fb75d3f4849b7c747250befb6ebfbcdc732d26fc676fdd6fe4088296530f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeSecurityPolicyRuleMatchExpr]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyRuleMatchExpr], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeSecurityPolicyRuleMatchExpr],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90f0c7dd308c0d7fc522c9aec4f8e177084053ace12ddaf8bc80da6e95e73ab7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeSecurityPolicyRuleMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRuleMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea77cb7ed8f08dbd809970e821556edd5e8ba302a974decb960d2f67a7cb84a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConfig")
    def put_config(self, *, src_ip_ranges: typing.Sequence[builtins.str]) -> None:
        '''
        :param src_ip_ranges: Set of IP addresses or ranges (IPV4 or IPV6) in CIDR notation to match against inbound traffic. There is a limit of 10 IP ranges per rule. A value of '*' matches all IPs (can be used to override the default behavior). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#src_ip_ranges ComputeSecurityPolicy#src_ip_ranges}
        '''
        value = ComputeSecurityPolicyRuleMatchConfig(src_ip_ranges=src_ip_ranges)

        return typing.cast(None, jsii.invoke(self, "putConfig", [value]))

    @jsii.member(jsii_name="putExpr")
    def put_expr(self, *, expression: builtins.str) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. The application context of the containing message determines which well-known feature set of CEL is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#expression ComputeSecurityPolicy#expression}
        '''
        value = ComputeSecurityPolicyRuleMatchExpr(expression=expression)

        return typing.cast(None, jsii.invoke(self, "putExpr", [value]))

    @jsii.member(jsii_name="putExprOptions")
    def put_expr_options(
        self,
        *,
        recaptcha_options: typing.Union[ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptions, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param recaptcha_options: recaptcha_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#recaptcha_options ComputeSecurityPolicy#recaptcha_options}
        '''
        value = ComputeSecurityPolicyRuleMatchExprOptions(
            recaptcha_options=recaptcha_options
        )

        return typing.cast(None, jsii.invoke(self, "putExprOptions", [value]))

    @jsii.member(jsii_name="resetConfig")
    def reset_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfig", []))

    @jsii.member(jsii_name="resetExpr")
    def reset_expr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpr", []))

    @jsii.member(jsii_name="resetExprOptions")
    def reset_expr_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExprOptions", []))

    @jsii.member(jsii_name="resetVersionedExpr")
    def reset_versioned_expr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersionedExpr", []))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> ComputeSecurityPolicyRuleMatchConfigOutputReference:
        return typing.cast(ComputeSecurityPolicyRuleMatchConfigOutputReference, jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="expr")
    def expr(self) -> ComputeSecurityPolicyRuleMatchExprOutputReference:
        return typing.cast(ComputeSecurityPolicyRuleMatchExprOutputReference, jsii.get(self, "expr"))

    @builtins.property
    @jsii.member(jsii_name="exprOptions")
    def expr_options(self) -> ComputeSecurityPolicyRuleMatchExprOptionsOutputReference:
        return typing.cast(ComputeSecurityPolicyRuleMatchExprOptionsOutputReference, jsii.get(self, "exprOptions"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(self) -> typing.Optional[ComputeSecurityPolicyRuleMatchConfig]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyRuleMatchConfig], jsii.get(self, "configInput"))

    @builtins.property
    @jsii.member(jsii_name="exprInput")
    def expr_input(self) -> typing.Optional[ComputeSecurityPolicyRuleMatchExpr]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyRuleMatchExpr], jsii.get(self, "exprInput"))

    @builtins.property
    @jsii.member(jsii_name="exprOptionsInput")
    def expr_options_input(
        self,
    ) -> typing.Optional[ComputeSecurityPolicyRuleMatchExprOptions]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyRuleMatchExprOptions], jsii.get(self, "exprOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="versionedExprInput")
    def versioned_expr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionedExprInput"))

    @builtins.property
    @jsii.member(jsii_name="versionedExpr")
    def versioned_expr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "versionedExpr"))

    @versioned_expr.setter
    def versioned_expr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca3e66969f8e5fbe6a87752d2df17d2bd816c93502d3b450187d317c30de6d4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionedExpr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeSecurityPolicyRuleMatch]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyRuleMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeSecurityPolicyRuleMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0305920f4fca2b9227d4bd65ca9c8a151501f6dc7e1a70a42903070ff0cf7a58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeSecurityPolicyRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__211c25e6f8065efa28bc11230aeb136ace2c1f49a018eb9e07cc7c2b1d56702b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHeaderAction")
    def put_header_action(
        self,
        *,
        request_headers_to_adds: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param request_headers_to_adds: request_headers_to_adds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#request_headers_to_adds ComputeSecurityPolicy#request_headers_to_adds}
        '''
        value = ComputeSecurityPolicyRuleHeaderAction(
            request_headers_to_adds=request_headers_to_adds
        )

        return typing.cast(None, jsii.invoke(self, "putHeaderAction", [value]))

    @jsii.member(jsii_name="putMatch")
    def put_match(
        self,
        *,
        config: typing.Optional[typing.Union[ComputeSecurityPolicyRuleMatchConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        expr: typing.Optional[typing.Union[ComputeSecurityPolicyRuleMatchExpr, typing.Dict[builtins.str, typing.Any]]] = None,
        expr_options: typing.Optional[typing.Union[ComputeSecurityPolicyRuleMatchExprOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        versioned_expr: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#config ComputeSecurityPolicy#config}
        :param expr: expr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#expr ComputeSecurityPolicy#expr}
        :param expr_options: expr_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#expr_options ComputeSecurityPolicy#expr_options}
        :param versioned_expr: Predefined rule expression. If this field is specified, config must also be specified. Available options: SRC_IPS_V1: Must specify the corresponding src_ip_ranges field in config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#versioned_expr ComputeSecurityPolicy#versioned_expr}
        '''
        value = ComputeSecurityPolicyRuleMatch(
            config=config,
            expr=expr,
            expr_options=expr_options,
            versioned_expr=versioned_expr,
        )

        return typing.cast(None, jsii.invoke(self, "putMatch", [value]))

    @jsii.member(jsii_name="putPreconfiguredWafConfig")
    def put_preconfigured_waf_config(
        self,
        *,
        exclusion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusion", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param exclusion: exclusion block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#exclusion ComputeSecurityPolicy#exclusion}
        '''
        value = ComputeSecurityPolicyRulePreconfiguredWafConfig(exclusion=exclusion)

        return typing.cast(None, jsii.invoke(self, "putPreconfiguredWafConfig", [value]))

    @jsii.member(jsii_name="putRateLimitOptions")
    def put_rate_limit_options(
        self,
        *,
        conform_action: builtins.str,
        exceed_action: builtins.str,
        rate_limit_threshold: typing.Union["ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThreshold", typing.Dict[builtins.str, typing.Any]],
        ban_duration_sec: typing.Optional[jsii.Number] = None,
        ban_threshold: typing.Optional[typing.Union["ComputeSecurityPolicyRuleRateLimitOptionsBanThreshold", typing.Dict[builtins.str, typing.Any]]] = None,
        enforce_on_key: typing.Optional[builtins.str] = None,
        enforce_on_key_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enforce_on_key_name: typing.Optional[builtins.str] = None,
        exceed_redirect_options: typing.Optional[typing.Union["ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param conform_action: Action to take for requests that are under the configured rate limit threshold. Valid option is "allow" only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#conform_action ComputeSecurityPolicy#conform_action}
        :param exceed_action: Action to take for requests that are above the configured rate limit threshold, to either deny with a specified HTTP response code, or redirect to a different endpoint. Valid options are "deny()" where valid values for status are 403, 404, 429, and 502, and "redirect" where the redirect parameters come from exceedRedirectOptions below. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#exceed_action ComputeSecurityPolicy#exceed_action}
        :param rate_limit_threshold: rate_limit_threshold block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#rate_limit_threshold ComputeSecurityPolicy#rate_limit_threshold}
        :param ban_duration_sec: Can only be specified if the action for the rule is "rate_based_ban". If specified, determines the time (in seconds) the traffic will continue to be banned by the rate limit after the rate falls below the threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#ban_duration_sec ComputeSecurityPolicy#ban_duration_sec}
        :param ban_threshold: ban_threshold block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#ban_threshold ComputeSecurityPolicy#ban_threshold}
        :param enforce_on_key: Determines the key to enforce the rateLimitThreshold on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#enforce_on_key ComputeSecurityPolicy#enforce_on_key}
        :param enforce_on_key_configs: enforce_on_key_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#enforce_on_key_configs ComputeSecurityPolicy#enforce_on_key_configs}
        :param enforce_on_key_name: Rate limit key name applicable only for the following key types: HTTP_HEADER -- Name of the HTTP header whose value is taken as the key value. HTTP_COOKIE -- Name of the HTTP cookie whose value is taken as the key value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#enforce_on_key_name ComputeSecurityPolicy#enforce_on_key_name}
        :param exceed_redirect_options: exceed_redirect_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#exceed_redirect_options ComputeSecurityPolicy#exceed_redirect_options}
        '''
        value = ComputeSecurityPolicyRuleRateLimitOptions(
            conform_action=conform_action,
            exceed_action=exceed_action,
            rate_limit_threshold=rate_limit_threshold,
            ban_duration_sec=ban_duration_sec,
            ban_threshold=ban_threshold,
            enforce_on_key=enforce_on_key,
            enforce_on_key_configs=enforce_on_key_configs,
            enforce_on_key_name=enforce_on_key_name,
            exceed_redirect_options=exceed_redirect_options,
        )

        return typing.cast(None, jsii.invoke(self, "putRateLimitOptions", [value]))

    @jsii.member(jsii_name="putRedirectOptions")
    def put_redirect_options(
        self,
        *,
        type: builtins.str,
        target: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Type of the redirect action. Available options: EXTERNAL_302: Must specify the corresponding target field in config. GOOGLE_RECAPTCHA: Cannot specify target field in config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#type ComputeSecurityPolicy#type}
        :param target: Target for the redirect action. This is required if the type is EXTERNAL_302 and cannot be specified for GOOGLE_RECAPTCHA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#target ComputeSecurityPolicy#target}
        '''
        value = ComputeSecurityPolicyRuleRedirectOptions(type=type, target=target)

        return typing.cast(None, jsii.invoke(self, "putRedirectOptions", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetHeaderAction")
    def reset_header_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaderAction", []))

    @jsii.member(jsii_name="resetPreconfiguredWafConfig")
    def reset_preconfigured_waf_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreconfiguredWafConfig", []))

    @jsii.member(jsii_name="resetPreview")
    def reset_preview(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreview", []))

    @jsii.member(jsii_name="resetRateLimitOptions")
    def reset_rate_limit_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRateLimitOptions", []))

    @jsii.member(jsii_name="resetRedirectOptions")
    def reset_redirect_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectOptions", []))

    @builtins.property
    @jsii.member(jsii_name="headerAction")
    def header_action(self) -> ComputeSecurityPolicyRuleHeaderActionOutputReference:
        return typing.cast(ComputeSecurityPolicyRuleHeaderActionOutputReference, jsii.get(self, "headerAction"))

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> ComputeSecurityPolicyRuleMatchOutputReference:
        return typing.cast(ComputeSecurityPolicyRuleMatchOutputReference, jsii.get(self, "match"))

    @builtins.property
    @jsii.member(jsii_name="preconfiguredWafConfig")
    def preconfigured_waf_config(
        self,
    ) -> "ComputeSecurityPolicyRulePreconfiguredWafConfigOutputReference":
        return typing.cast("ComputeSecurityPolicyRulePreconfiguredWafConfigOutputReference", jsii.get(self, "preconfiguredWafConfig"))

    @builtins.property
    @jsii.member(jsii_name="rateLimitOptions")
    def rate_limit_options(
        self,
    ) -> "ComputeSecurityPolicyRuleRateLimitOptionsOutputReference":
        return typing.cast("ComputeSecurityPolicyRuleRateLimitOptionsOutputReference", jsii.get(self, "rateLimitOptions"))

    @builtins.property
    @jsii.member(jsii_name="redirectOptions")
    def redirect_options(
        self,
    ) -> "ComputeSecurityPolicyRuleRedirectOptionsOutputReference":
        return typing.cast("ComputeSecurityPolicyRuleRedirectOptionsOutputReference", jsii.get(self, "redirectOptions"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="headerActionInput")
    def header_action_input(
        self,
    ) -> typing.Optional[ComputeSecurityPolicyRuleHeaderAction]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyRuleHeaderAction], jsii.get(self, "headerActionInput"))

    @builtins.property
    @jsii.member(jsii_name="matchInput")
    def match_input(self) -> typing.Optional[ComputeSecurityPolicyRuleMatch]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyRuleMatch], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="preconfiguredWafConfigInput")
    def preconfigured_waf_config_input(
        self,
    ) -> typing.Optional["ComputeSecurityPolicyRulePreconfiguredWafConfig"]:
        return typing.cast(typing.Optional["ComputeSecurityPolicyRulePreconfiguredWafConfig"], jsii.get(self, "preconfiguredWafConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="previewInput")
    def preview_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "previewInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="rateLimitOptionsInput")
    def rate_limit_options_input(
        self,
    ) -> typing.Optional["ComputeSecurityPolicyRuleRateLimitOptions"]:
        return typing.cast(typing.Optional["ComputeSecurityPolicyRuleRateLimitOptions"], jsii.get(self, "rateLimitOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectOptionsInput")
    def redirect_options_input(
        self,
    ) -> typing.Optional["ComputeSecurityPolicyRuleRedirectOptions"]:
        return typing.cast(typing.Optional["ComputeSecurityPolicyRuleRedirectOptions"], jsii.get(self, "redirectOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f7aa3eaa2127247714caf3bc80cee8b767fe6b2004f8f136b4ec78fda852085)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce3eb1838890d3a0f8636b6b1231b157aff90ab9bec13c831446b92307e31329)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preview")
    def preview(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preview"))

    @preview.setter
    def preview(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f060c8190ec8192ed3dee6a1c3e1213a176fd6da323b5cccc232bad7405cfdfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preview", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7a6f0c9dec2247e20c0780bdae134e9f7059923ada7272594b1018b7eb137db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6d0ac6bafb0510f527f4bef0865f853099122e3565073190464356b5855a6d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRulePreconfiguredWafConfig",
    jsii_struct_bases=[],
    name_mapping={"exclusion": "exclusion"},
)
class ComputeSecurityPolicyRulePreconfiguredWafConfig:
    def __init__(
        self,
        *,
        exclusion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusion", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param exclusion: exclusion block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#exclusion ComputeSecurityPolicy#exclusion}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89e68fa66f026a04ed275fd0c3ae77c197ec191878c2e470787692f467b2816a)
            check_type(argname="argument exclusion", value=exclusion, expected_type=type_hints["exclusion"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclusion is not None:
            self._values["exclusion"] = exclusion

    @builtins.property
    def exclusion(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusion"]]]:
        '''exclusion block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#exclusion ComputeSecurityPolicy#exclusion}
        '''
        result = self._values.get("exclusion")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusion"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRulePreconfiguredWafConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRulePreconfiguredWafConfigExclusion",
    jsii_struct_bases=[],
    name_mapping={
        "target_rule_set": "targetRuleSet",
        "request_cookie": "requestCookie",
        "request_header": "requestHeader",
        "request_query_param": "requestQueryParam",
        "request_uri": "requestUri",
        "target_rule_ids": "targetRuleIds",
    },
)
class ComputeSecurityPolicyRulePreconfiguredWafConfigExclusion:
    def __init__(
        self,
        *,
        target_rule_set: builtins.str,
        request_cookie: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_query_param: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_uri: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_rule_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param target_rule_set: Target WAF rule set to apply the preconfigured WAF exclusion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#target_rule_set ComputeSecurityPolicy#target_rule_set}
        :param request_cookie: request_cookie block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#request_cookie ComputeSecurityPolicy#request_cookie}
        :param request_header: request_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#request_header ComputeSecurityPolicy#request_header}
        :param request_query_param: request_query_param block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#request_query_param ComputeSecurityPolicy#request_query_param}
        :param request_uri: request_uri block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#request_uri ComputeSecurityPolicy#request_uri}
        :param target_rule_ids: A list of target rule IDs under the WAF rule set to apply the preconfigured WAF exclusion. If omitted, it refers to all the rule IDs under the WAF rule set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#target_rule_ids ComputeSecurityPolicy#target_rule_ids}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e4e5d4a6704be27a7f995946a3cd9f75941b3ac6eb875140efa6eef6bbfd082)
            check_type(argname="argument target_rule_set", value=target_rule_set, expected_type=type_hints["target_rule_set"])
            check_type(argname="argument request_cookie", value=request_cookie, expected_type=type_hints["request_cookie"])
            check_type(argname="argument request_header", value=request_header, expected_type=type_hints["request_header"])
            check_type(argname="argument request_query_param", value=request_query_param, expected_type=type_hints["request_query_param"])
            check_type(argname="argument request_uri", value=request_uri, expected_type=type_hints["request_uri"])
            check_type(argname="argument target_rule_ids", value=target_rule_ids, expected_type=type_hints["target_rule_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_rule_set": target_rule_set,
        }
        if request_cookie is not None:
            self._values["request_cookie"] = request_cookie
        if request_header is not None:
            self._values["request_header"] = request_header
        if request_query_param is not None:
            self._values["request_query_param"] = request_query_param
        if request_uri is not None:
            self._values["request_uri"] = request_uri
        if target_rule_ids is not None:
            self._values["target_rule_ids"] = target_rule_ids

    @builtins.property
    def target_rule_set(self) -> builtins.str:
        '''Target WAF rule set to apply the preconfigured WAF exclusion.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#target_rule_set ComputeSecurityPolicy#target_rule_set}
        '''
        result = self._values.get("target_rule_set")
        assert result is not None, "Required property 'target_rule_set' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def request_cookie(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie"]]]:
        '''request_cookie block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#request_cookie ComputeSecurityPolicy#request_cookie}
        '''
        result = self._values.get("request_cookie")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie"]]], result)

    @builtins.property
    def request_header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader"]]]:
        '''request_header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#request_header ComputeSecurityPolicy#request_header}
        '''
        result = self._values.get("request_header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader"]]], result)

    @builtins.property
    def request_query_param(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam"]]]:
        '''request_query_param block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#request_query_param ComputeSecurityPolicy#request_query_param}
        '''
        result = self._values.get("request_query_param")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam"]]], result)

    @builtins.property
    def request_uri(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri"]]]:
        '''request_uri block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#request_uri ComputeSecurityPolicy#request_uri}
        '''
        result = self._values.get("request_uri")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri"]]], result)

    @builtins.property
    def target_rule_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of target rule IDs under the WAF rule set to apply the preconfigured WAF exclusion.

        If omitted, it refers to all the rule IDs under the WAF rule set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#target_rule_ids ComputeSecurityPolicy#target_rule_ids}
        '''
        result = self._values.get("target_rule_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9878a4c043e46f2be35a4948e7b81eb65a34d17496051269c103b11ec604d9d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ec15b8507b94760f54d7e6b64a720617c23bf6090cc2e45c5587f60e7021f22)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ffa3c2d9f45f048301a28df3d218b62e465ab493f21d9907a306fa03e16a709)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d638dcf3d1d08cd1bda7e5e2c39c19cacab3cdaaea4c5c8453b977edcaaf049)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4b8476bafdccf44c9bdff1d8088fa1e8f442f9cf4e1e743b32c47e4a1f3f33f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusion]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusion]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusion]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7402b55b8a967b80b63143b7726ec3b74ed9e68ba5f52e5bbe8d1db9140bc8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__448eced29ccad4f77981255e4576a800c29dc7e165f3d9db2a5a9f4e2fe24683)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putRequestCookie")
    def put_request_cookie(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1d29f7d48dc5aec07877aaf52ddeefe6e2e73d480b4c50ce2acdb13c9495894)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestCookie", [value]))

    @jsii.member(jsii_name="putRequestHeader")
    def put_request_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4380a7b83c47c31e8009f622e6c9a0aafdca9e591e7af44daeee32d603c0b759)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestHeader", [value]))

    @jsii.member(jsii_name="putRequestQueryParam")
    def put_request_query_param(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00554e93734baa6df94c817f54fbf0a01d863464d94459f37589772d8f9b0c90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestQueryParam", [value]))

    @jsii.member(jsii_name="putRequestUri")
    def put_request_uri(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8935a3c8a067b19ca2422dbc62648bb660f1257c2ead4329f7b48af2907dee20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestUri", [value]))

    @jsii.member(jsii_name="resetRequestCookie")
    def reset_request_cookie(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestCookie", []))

    @jsii.member(jsii_name="resetRequestHeader")
    def reset_request_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestHeader", []))

    @jsii.member(jsii_name="resetRequestQueryParam")
    def reset_request_query_param(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestQueryParam", []))

    @jsii.member(jsii_name="resetRequestUri")
    def reset_request_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestUri", []))

    @jsii.member(jsii_name="resetTargetRuleIds")
    def reset_target_rule_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetRuleIds", []))

    @builtins.property
    @jsii.member(jsii_name="requestCookie")
    def request_cookie(
        self,
    ) -> "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieList":
        return typing.cast("ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieList", jsii.get(self, "requestCookie"))

    @builtins.property
    @jsii.member(jsii_name="requestHeader")
    def request_header(
        self,
    ) -> "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderList":
        return typing.cast("ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderList", jsii.get(self, "requestHeader"))

    @builtins.property
    @jsii.member(jsii_name="requestQueryParam")
    def request_query_param(
        self,
    ) -> "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamList":
        return typing.cast("ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamList", jsii.get(self, "requestQueryParam"))

    @builtins.property
    @jsii.member(jsii_name="requestUri")
    def request_uri(
        self,
    ) -> "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriList":
        return typing.cast("ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriList", jsii.get(self, "requestUri"))

    @builtins.property
    @jsii.member(jsii_name="requestCookieInput")
    def request_cookie_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie"]]], jsii.get(self, "requestCookieInput"))

    @builtins.property
    @jsii.member(jsii_name="requestHeaderInput")
    def request_header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader"]]], jsii.get(self, "requestHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="requestQueryParamInput")
    def request_query_param_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam"]]], jsii.get(self, "requestQueryParamInput"))

    @builtins.property
    @jsii.member(jsii_name="requestUriInput")
    def request_uri_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri"]]], jsii.get(self, "requestUriInput"))

    @builtins.property
    @jsii.member(jsii_name="targetRuleIdsInput")
    def target_rule_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "targetRuleIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="targetRuleSetInput")
    def target_rule_set_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetRuleSetInput"))

    @builtins.property
    @jsii.member(jsii_name="targetRuleIds")
    def target_rule_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "targetRuleIds"))

    @target_rule_ids.setter
    def target_rule_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a3d0615f978aae667964187dca9fbb17e21376d58b3c4349c14196eec21ff85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetRuleIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetRuleSet")
    def target_rule_set(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetRuleSet"))

    @target_rule_set.setter
    def target_rule_set(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__608caf0ef6978f5b6f6d96b68ca06bda170e947d5ebbba1fbf6af41992f6cc53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetRuleSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusion]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusion]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusion]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12cf0f4c5d2c13ece9fcda63f6f494300d7e5d4adf0b57bdd8db6ae8c9198e73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "value": "value"},
)
class ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie:
    def __init__(
        self,
        *,
        operator: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operator: You can specify an exact match or a partial match by using a field operator and a field value. Available options: EQUALS: The operator matches if the field value equals the specified value. STARTS_WITH: The operator matches if the field value starts with the specified value. ENDS_WITH: The operator matches if the field value ends with the specified value. CONTAINS: The operator matches if the field value contains the specified value. EQUALS_ANY: The operator matches if the field value is any value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#operator ComputeSecurityPolicy#operator}
        :param value: A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation. The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#value ComputeSecurityPolicy#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__566fcf96d097daa1fd78723f1dc343a05867273e01ba77d710190b7a8104a4ae)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
        }
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def operator(self) -> builtins.str:
        '''You can specify an exact match or a partial match by using a field operator and a field value.

        Available options: EQUALS: The operator matches if the field value equals the specified value. STARTS_WITH: The operator matches if the field value starts with the specified value. ENDS_WITH: The operator matches if the field value ends with the specified value. CONTAINS: The operator matches if the field value contains the specified value. EQUALS_ANY: The operator matches if the field value is any value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#operator ComputeSecurityPolicy#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation.

        The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#value ComputeSecurityPolicy#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__622a9d498b969761fc8afb0a1f450e226272f0458dc5f2bc9877b0c423908f29)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87a3c1437323dcb3004e977e5d1de289403e233259735034762249409ce5e4c5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b55cdec1c587776e2b59f1cf191d5516128a97f4546faccc1ff8db4a77030cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__11711aa012758e34e7603c7ab08807f8c8816a407111f84646f3701465fc804a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b46575d737412682e85d8d4103467956f0d0fd1271338ead0021d9cc5cc2acb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e4322b3d339fe9a61f55e5a37834dfa2a2cd97b6ec2f3a2ac30fa5ad2514ca1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__40afa676cfd7f5f8669c551c947086424347bb5b70a2eb2923cdbcf031bdec59)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fa3caffb871402b04a217720ddbd0c28addc8f4382d2e73dc06a5695896bad5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__603c14b3bc4e4397d8b43ad9320bcdd3ccc50a6db99b0b4840b3242872253bc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__201e35b7e33c3234a3bffdebfb79fde00d2c08299c237635bb3be3b3c281071a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "value": "value"},
)
class ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader:
    def __init__(
        self,
        *,
        operator: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operator: You can specify an exact match or a partial match by using a field operator and a field value. Available options: EQUALS: The operator matches if the field value equals the specified value. STARTS_WITH: The operator matches if the field value starts with the specified value. ENDS_WITH: The operator matches if the field value ends with the specified value. CONTAINS: The operator matches if the field value contains the specified value. EQUALS_ANY: The operator matches if the field value is any value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#operator ComputeSecurityPolicy#operator}
        :param value: A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation. The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#value ComputeSecurityPolicy#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42fb9c46f07606b327504f47c438a9706425d54a3e905a7c0afc65ca29c2b17e)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
        }
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def operator(self) -> builtins.str:
        '''You can specify an exact match or a partial match by using a field operator and a field value.

        Available options: EQUALS: The operator matches if the field value equals the specified value. STARTS_WITH: The operator matches if the field value starts with the specified value. ENDS_WITH: The operator matches if the field value ends with the specified value. CONTAINS: The operator matches if the field value contains the specified value. EQUALS_ANY: The operator matches if the field value is any value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#operator ComputeSecurityPolicy#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation.

        The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#value ComputeSecurityPolicy#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__accceca5e04b92bf62fd7f4c79c43c8c3f5502ac19ccdfb666240f6fc531a3b8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__182a75d34b195ae3ea57246363874fd596c55f0cf9777b77f5596060fbe5656e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cd80ef91236a2de5a7a381b473fd3d25d91595cf6a996d091598af6c137cde7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__50b501737d13d1b34afbb77f57613c2270a60ea52a4f616cad4f9a985c28b9c8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1520a96e72f6a7181a387c0e1a9204891fad1464a75b8b14cda11cd2cadd52b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6a7f61d9b857b5c5c6f17370c4bbe5ee60f29500274815decf7403fa11a759d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__acfb268b94b005d0be0edc97c42b1bec0fe973e5d77bc9e5d771343f54acd237)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0154beb0926c7e8588bfc4f4a0784fd66c1f0c8c9a62acde5b1e28943a7e8c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c711c115b7bba62167eee98e4c14e88cfb8a7df259008c4b8ca6f46e0a2dd99a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17ef1886fe99c02ef33ef6fff553aa492f6e9cd2103e705ba332541bfa92ac12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "value": "value"},
)
class ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam:
    def __init__(
        self,
        *,
        operator: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operator: You can specify an exact match or a partial match by using a field operator and a field value. Available options: EQUALS: The operator matches if the field value equals the specified value. STARTS_WITH: The operator matches if the field value starts with the specified value. ENDS_WITH: The operator matches if the field value ends with the specified value. CONTAINS: The operator matches if the field value contains the specified value. EQUALS_ANY: The operator matches if the field value is any value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#operator ComputeSecurityPolicy#operator}
        :param value: A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation. The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#value ComputeSecurityPolicy#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d75914f78158edc5ee8e4e6ddb1bef4c8544e98a581242b02e0c98b1840f80d)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
        }
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def operator(self) -> builtins.str:
        '''You can specify an exact match or a partial match by using a field operator and a field value.

        Available options: EQUALS: The operator matches if the field value equals the specified value. STARTS_WITH: The operator matches if the field value starts with the specified value. ENDS_WITH: The operator matches if the field value ends with the specified value. CONTAINS: The operator matches if the field value contains the specified value. EQUALS_ANY: The operator matches if the field value is any value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#operator ComputeSecurityPolicy#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation.

        The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#value ComputeSecurityPolicy#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c002751015b88ef8e078e11685d90bb1bcda525e428863bdde21cea629b7ad9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__407c9a345bc21af7d13c76c8cfe5ad8e009c0cce518502ba677e0e27d9281560)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07dffbd8b024d5a149468967a0a94cbf3c0ca541cd1a546615a5fb086a1c19b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be94ecb9309a5a7c4957a37a5675e248684d5f03acbebd5f4b1ae0e92b57f099)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b7976050fcf8a3526d11bcb34a5f9996e4043ff24b4525e163235bf2767f013)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2c5caae8933ab8b0c35f6fbddc7ebabeeb7cddcf70945cbc0b0ff08a4c09fe7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dec8919a18360cc32defad77ce81e52a0d59ee977d5333d960ba04ce8c1d75f5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0be4a6ea69964b419ce934250c8f036dc746beb342ba110e9fd50667c2f2c8ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1317274df5369f1bd3e83bf93e9ec9756e9b033b39675a3cfaeb81da8ff61e3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__136496b79285d30bdbb5b4c4f66dba1b6a696765aaeb228e0de4fb7fd8e208cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "value": "value"},
)
class ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri:
    def __init__(
        self,
        *,
        operator: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operator: You can specify an exact match or a partial match by using a field operator and a field value. Available options: EQUALS: The operator matches if the field value equals the specified value. STARTS_WITH: The operator matches if the field value starts with the specified value. ENDS_WITH: The operator matches if the field value ends with the specified value. CONTAINS: The operator matches if the field value contains the specified value. EQUALS_ANY: The operator matches if the field value is any value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#operator ComputeSecurityPolicy#operator}
        :param value: A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation. The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#value ComputeSecurityPolicy#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11d205aaa4638bcb3efc89d860d5aeaf78f5064f4d6e00e6f86709c298250abd)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
        }
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def operator(self) -> builtins.str:
        '''You can specify an exact match or a partial match by using a field operator and a field value.

        Available options: EQUALS: The operator matches if the field value equals the specified value. STARTS_WITH: The operator matches if the field value starts with the specified value. ENDS_WITH: The operator matches if the field value ends with the specified value. CONTAINS: The operator matches if the field value contains the specified value. EQUALS_ANY: The operator matches if the field value is any value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#operator ComputeSecurityPolicy#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation.

        The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#value ComputeSecurityPolicy#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c7659036c05d1bf595cba9a954bd224e2bf8989ae8d0396cfcfbe8f663248cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f65653f409ae0efe0c13b05ee843b986fdfbc397524f55f662d058caf9afe6e9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__641c6f51907ff52c4dbc45556fbbb0736ea54d817b58dce5e8514d65ea1bea01)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9aeb60da934a10179cd8601656bc10c6a87710643a14f08bd7b6d77a88ee589f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__65e15a1d4efe56a7b3d84ee71ccd9452032c3d479a8a8de09a926afb3b3fc995)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc2b81b47626eecf3b69aa570022962490435ed2d7cb1af8a3861e3d71389950)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__06033ad544ed20e54997e0a6d72243452822e72809970191854e41099a0e4e32)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f40b5618673c603d6391983642c50cf841edf699e10fe2cee8950869472dc86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4658c7a6b90b451ad1d8b7475ff80a8209495e75849cb6779ded0a96f1c621c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6832546d2d5a79062535a70575954f53875a4163d285996561140a59105d2b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeSecurityPolicyRulePreconfiguredWafConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRulePreconfiguredWafConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__888a683b089acbdceaed7bc5b65c71e76fbd761bde575968d95c569b5aa7c85f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExclusion")
    def put_exclusion(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusion, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c56f6126242ff8c4f75819246994ac6137997a41214f87c467e57782ebcc8090)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExclusion", [value]))

    @jsii.member(jsii_name="resetExclusion")
    def reset_exclusion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusion", []))

    @builtins.property
    @jsii.member(jsii_name="exclusion")
    def exclusion(self) -> ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionList:
        return typing.cast(ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionList, jsii.get(self, "exclusion"))

    @builtins.property
    @jsii.member(jsii_name="exclusionInput")
    def exclusion_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusion]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusion]]], jsii.get(self, "exclusionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeSecurityPolicyRulePreconfiguredWafConfig]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyRulePreconfiguredWafConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeSecurityPolicyRulePreconfiguredWafConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ae88ef482544cb04b659e6f2cf8682e291f394b8efbeb7ef6f49087bbd0ebf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRuleRateLimitOptions",
    jsii_struct_bases=[],
    name_mapping={
        "conform_action": "conformAction",
        "exceed_action": "exceedAction",
        "rate_limit_threshold": "rateLimitThreshold",
        "ban_duration_sec": "banDurationSec",
        "ban_threshold": "banThreshold",
        "enforce_on_key": "enforceOnKey",
        "enforce_on_key_configs": "enforceOnKeyConfigs",
        "enforce_on_key_name": "enforceOnKeyName",
        "exceed_redirect_options": "exceedRedirectOptions",
    },
)
class ComputeSecurityPolicyRuleRateLimitOptions:
    def __init__(
        self,
        *,
        conform_action: builtins.str,
        exceed_action: builtins.str,
        rate_limit_threshold: typing.Union["ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThreshold", typing.Dict[builtins.str, typing.Any]],
        ban_duration_sec: typing.Optional[jsii.Number] = None,
        ban_threshold: typing.Optional[typing.Union["ComputeSecurityPolicyRuleRateLimitOptionsBanThreshold", typing.Dict[builtins.str, typing.Any]]] = None,
        enforce_on_key: typing.Optional[builtins.str] = None,
        enforce_on_key_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enforce_on_key_name: typing.Optional[builtins.str] = None,
        exceed_redirect_options: typing.Optional[typing.Union["ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param conform_action: Action to take for requests that are under the configured rate limit threshold. Valid option is "allow" only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#conform_action ComputeSecurityPolicy#conform_action}
        :param exceed_action: Action to take for requests that are above the configured rate limit threshold, to either deny with a specified HTTP response code, or redirect to a different endpoint. Valid options are "deny()" where valid values for status are 403, 404, 429, and 502, and "redirect" where the redirect parameters come from exceedRedirectOptions below. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#exceed_action ComputeSecurityPolicy#exceed_action}
        :param rate_limit_threshold: rate_limit_threshold block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#rate_limit_threshold ComputeSecurityPolicy#rate_limit_threshold}
        :param ban_duration_sec: Can only be specified if the action for the rule is "rate_based_ban". If specified, determines the time (in seconds) the traffic will continue to be banned by the rate limit after the rate falls below the threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#ban_duration_sec ComputeSecurityPolicy#ban_duration_sec}
        :param ban_threshold: ban_threshold block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#ban_threshold ComputeSecurityPolicy#ban_threshold}
        :param enforce_on_key: Determines the key to enforce the rateLimitThreshold on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#enforce_on_key ComputeSecurityPolicy#enforce_on_key}
        :param enforce_on_key_configs: enforce_on_key_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#enforce_on_key_configs ComputeSecurityPolicy#enforce_on_key_configs}
        :param enforce_on_key_name: Rate limit key name applicable only for the following key types: HTTP_HEADER -- Name of the HTTP header whose value is taken as the key value. HTTP_COOKIE -- Name of the HTTP cookie whose value is taken as the key value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#enforce_on_key_name ComputeSecurityPolicy#enforce_on_key_name}
        :param exceed_redirect_options: exceed_redirect_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#exceed_redirect_options ComputeSecurityPolicy#exceed_redirect_options}
        '''
        if isinstance(rate_limit_threshold, dict):
            rate_limit_threshold = ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThreshold(**rate_limit_threshold)
        if isinstance(ban_threshold, dict):
            ban_threshold = ComputeSecurityPolicyRuleRateLimitOptionsBanThreshold(**ban_threshold)
        if isinstance(exceed_redirect_options, dict):
            exceed_redirect_options = ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptions(**exceed_redirect_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8964420ef94d2ee7d1a8fee257f6e49399859e20a032775b33de9622f9b9a1f5)
            check_type(argname="argument conform_action", value=conform_action, expected_type=type_hints["conform_action"])
            check_type(argname="argument exceed_action", value=exceed_action, expected_type=type_hints["exceed_action"])
            check_type(argname="argument rate_limit_threshold", value=rate_limit_threshold, expected_type=type_hints["rate_limit_threshold"])
            check_type(argname="argument ban_duration_sec", value=ban_duration_sec, expected_type=type_hints["ban_duration_sec"])
            check_type(argname="argument ban_threshold", value=ban_threshold, expected_type=type_hints["ban_threshold"])
            check_type(argname="argument enforce_on_key", value=enforce_on_key, expected_type=type_hints["enforce_on_key"])
            check_type(argname="argument enforce_on_key_configs", value=enforce_on_key_configs, expected_type=type_hints["enforce_on_key_configs"])
            check_type(argname="argument enforce_on_key_name", value=enforce_on_key_name, expected_type=type_hints["enforce_on_key_name"])
            check_type(argname="argument exceed_redirect_options", value=exceed_redirect_options, expected_type=type_hints["exceed_redirect_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "conform_action": conform_action,
            "exceed_action": exceed_action,
            "rate_limit_threshold": rate_limit_threshold,
        }
        if ban_duration_sec is not None:
            self._values["ban_duration_sec"] = ban_duration_sec
        if ban_threshold is not None:
            self._values["ban_threshold"] = ban_threshold
        if enforce_on_key is not None:
            self._values["enforce_on_key"] = enforce_on_key
        if enforce_on_key_configs is not None:
            self._values["enforce_on_key_configs"] = enforce_on_key_configs
        if enforce_on_key_name is not None:
            self._values["enforce_on_key_name"] = enforce_on_key_name
        if exceed_redirect_options is not None:
            self._values["exceed_redirect_options"] = exceed_redirect_options

    @builtins.property
    def conform_action(self) -> builtins.str:
        '''Action to take for requests that are under the configured rate limit threshold. Valid option is "allow" only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#conform_action ComputeSecurityPolicy#conform_action}
        '''
        result = self._values.get("conform_action")
        assert result is not None, "Required property 'conform_action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def exceed_action(self) -> builtins.str:
        '''Action to take for requests that are above the configured rate limit threshold, to either deny with a specified HTTP response code, or redirect to a different endpoint.

        Valid options are "deny()" where valid values for status are 403, 404, 429, and 502, and "redirect" where the redirect parameters come from exceedRedirectOptions below.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#exceed_action ComputeSecurityPolicy#exceed_action}
        '''
        result = self._values.get("exceed_action")
        assert result is not None, "Required property 'exceed_action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rate_limit_threshold(
        self,
    ) -> "ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThreshold":
        '''rate_limit_threshold block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#rate_limit_threshold ComputeSecurityPolicy#rate_limit_threshold}
        '''
        result = self._values.get("rate_limit_threshold")
        assert result is not None, "Required property 'rate_limit_threshold' is missing"
        return typing.cast("ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThreshold", result)

    @builtins.property
    def ban_duration_sec(self) -> typing.Optional[jsii.Number]:
        '''Can only be specified if the action for the rule is "rate_based_ban".

        If specified, determines the time (in seconds) the traffic will continue to be banned by the rate limit after the rate falls below the threshold.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#ban_duration_sec ComputeSecurityPolicy#ban_duration_sec}
        '''
        result = self._values.get("ban_duration_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ban_threshold(
        self,
    ) -> typing.Optional["ComputeSecurityPolicyRuleRateLimitOptionsBanThreshold"]:
        '''ban_threshold block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#ban_threshold ComputeSecurityPolicy#ban_threshold}
        '''
        result = self._values.get("ban_threshold")
        return typing.cast(typing.Optional["ComputeSecurityPolicyRuleRateLimitOptionsBanThreshold"], result)

    @builtins.property
    def enforce_on_key(self) -> typing.Optional[builtins.str]:
        '''Determines the key to enforce the rateLimitThreshold on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#enforce_on_key ComputeSecurityPolicy#enforce_on_key}
        '''
        result = self._values.get("enforce_on_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enforce_on_key_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs"]]]:
        '''enforce_on_key_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#enforce_on_key_configs ComputeSecurityPolicy#enforce_on_key_configs}
        '''
        result = self._values.get("enforce_on_key_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs"]]], result)

    @builtins.property
    def enforce_on_key_name(self) -> typing.Optional[builtins.str]:
        '''Rate limit key name applicable only for the following key types: HTTP_HEADER -- Name of the HTTP header whose value is taken as the key value.

        HTTP_COOKIE -- Name of the HTTP cookie whose value is taken as the key value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#enforce_on_key_name ComputeSecurityPolicy#enforce_on_key_name}
        '''
        result = self._values.get("enforce_on_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exceed_redirect_options(
        self,
    ) -> typing.Optional["ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptions"]:
        '''exceed_redirect_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#exceed_redirect_options ComputeSecurityPolicy#exceed_redirect_options}
        '''
        result = self._values.get("exceed_redirect_options")
        return typing.cast(typing.Optional["ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRuleRateLimitOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRuleRateLimitOptionsBanThreshold",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "interval_sec": "intervalSec"},
)
class ComputeSecurityPolicyRuleRateLimitOptionsBanThreshold:
    def __init__(self, *, count: jsii.Number, interval_sec: jsii.Number) -> None:
        '''
        :param count: Number of HTTP(S) requests for calculating the threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#count ComputeSecurityPolicy#count}
        :param interval_sec: Interval over which the threshold is computed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#interval_sec ComputeSecurityPolicy#interval_sec}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbf526eca30c6b0f5bce336280236cfb750b870c91f436d0c2f88d03d3beb9b4)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument interval_sec", value=interval_sec, expected_type=type_hints["interval_sec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "count": count,
            "interval_sec": interval_sec,
        }

    @builtins.property
    def count(self) -> jsii.Number:
        '''Number of HTTP(S) requests for calculating the threshold.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#count ComputeSecurityPolicy#count}
        '''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def interval_sec(self) -> jsii.Number:
        '''Interval over which the threshold is computed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#interval_sec ComputeSecurityPolicy#interval_sec}
        '''
        result = self._values.get("interval_sec")
        assert result is not None, "Required property 'interval_sec' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRuleRateLimitOptionsBanThreshold(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyRuleRateLimitOptionsBanThresholdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRuleRateLimitOptionsBanThresholdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__026cc302ef58180b8ba186963cf29af6e377aa949042ead69d12106594a9ca5c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalSecInput")
    def interval_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalSecInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebca3ab5137f57cc3f5366c9fbd35f63cb26e64743a0cb247520b3fdeb343f68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalSec")
    def interval_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "intervalSec"))

    @interval_sec.setter
    def interval_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85877065a916deed9b1829d47a1629c4fd3d5fefdd8f0dd16a69794939a19522)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeSecurityPolicyRuleRateLimitOptionsBanThreshold]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyRuleRateLimitOptionsBanThreshold], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeSecurityPolicyRuleRateLimitOptionsBanThreshold],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f6b4172af51d85b092252583003c0568665f8ad806ef9c0dcbe50772cd95762)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "enforce_on_key_name": "enforceOnKeyName",
        "enforce_on_key_type": "enforceOnKeyType",
    },
)
class ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs:
    def __init__(
        self,
        *,
        enforce_on_key_name: typing.Optional[builtins.str] = None,
        enforce_on_key_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enforce_on_key_name: Rate limit key name applicable only for the following key types: HTTP_HEADER -- Name of the HTTP header whose value is taken as the key value. HTTP_COOKIE -- Name of the HTTP cookie whose value is taken as the key value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#enforce_on_key_name ComputeSecurityPolicy#enforce_on_key_name}
        :param enforce_on_key_type: Determines the key to enforce the rate_limit_threshold on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#enforce_on_key_type ComputeSecurityPolicy#enforce_on_key_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efbf44ceeeedc5236a8ac0a88aa5780e34c8f8cf423af99953ec7e144d4503c9)
            check_type(argname="argument enforce_on_key_name", value=enforce_on_key_name, expected_type=type_hints["enforce_on_key_name"])
            check_type(argname="argument enforce_on_key_type", value=enforce_on_key_type, expected_type=type_hints["enforce_on_key_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enforce_on_key_name is not None:
            self._values["enforce_on_key_name"] = enforce_on_key_name
        if enforce_on_key_type is not None:
            self._values["enforce_on_key_type"] = enforce_on_key_type

    @builtins.property
    def enforce_on_key_name(self) -> typing.Optional[builtins.str]:
        '''Rate limit key name applicable only for the following key types: HTTP_HEADER -- Name of the HTTP header whose value is taken as the key value.

        HTTP_COOKIE -- Name of the HTTP cookie whose value is taken as the key value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#enforce_on_key_name ComputeSecurityPolicy#enforce_on_key_name}
        '''
        result = self._values.get("enforce_on_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enforce_on_key_type(self) -> typing.Optional[builtins.str]:
        '''Determines the key to enforce the rate_limit_threshold on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#enforce_on_key_type ComputeSecurityPolicy#enforce_on_key_type}
        '''
        result = self._values.get("enforce_on_key_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74f3bb6e05084f5b5d45d3e04c9d755ea41885058788a1b0de211eb51926b633)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15d252f9e5b2ede120a826b3b873df2f18fc9787b0d93a047823d97239b81b9d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c6b1f930ceb4967c3a90f78aa503e01dd31c7ce4882255339821b48e261159a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__211885d4cad2d72df47b6a983fe335fb5e4d3d8442f899b7648c1dedc4df10a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__819f2f14141baf659fa079010b61f96270ce853b86f2c208dd081dc336c33c7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c5de3faf3aeaaa998664b31cbb4bac59dda3fba3db1f888eec3ddb5dd433e16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a94cf952db1e9a64f1300cd09168336d0f1f307bf230a56ad0e7d054e684d8a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEnforceOnKeyName")
    def reset_enforce_on_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforceOnKeyName", []))

    @jsii.member(jsii_name="resetEnforceOnKeyType")
    def reset_enforce_on_key_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforceOnKeyType", []))

    @builtins.property
    @jsii.member(jsii_name="enforceOnKeyNameInput")
    def enforce_on_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enforceOnKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="enforceOnKeyTypeInput")
    def enforce_on_key_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enforceOnKeyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="enforceOnKeyName")
    def enforce_on_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enforceOnKeyName"))

    @enforce_on_key_name.setter
    def enforce_on_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cbb83b86add9aaca532bd5d4abe13d8feefa911e9b261dabb1332323665ae5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforceOnKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforceOnKeyType")
    def enforce_on_key_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enforceOnKeyType"))

    @enforce_on_key_type.setter
    def enforce_on_key_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__472b844b40ffc31964df72b1f8e88144440615a5ce59f9c2e73c5e8ac96886fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforceOnKeyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7646c181e46fdb43d9368625d69e591ee4a2ffc4d98bd0fb0093e72383b04c86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptions",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "target": "target"},
)
class ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptions:
    def __init__(
        self,
        *,
        type: builtins.str,
        target: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Type of the redirect action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#type ComputeSecurityPolicy#type}
        :param target: Target for the redirect action. This is required if the type is EXTERNAL_302 and cannot be specified for GOOGLE_RECAPTCHA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#target ComputeSecurityPolicy#target}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91f662a0ffdac86f09124fdd5771e3d7b96af3fcd647e82226c6b988f52d14a7)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def type(self) -> builtins.str:
        '''Type of the redirect action.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#type ComputeSecurityPolicy#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''Target for the redirect action. This is required if the type is EXTERNAL_302 and cannot be specified for GOOGLE_RECAPTCHA.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#target ComputeSecurityPolicy#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6465aff36ac8c6401e1b5cfa8e5c0c4ac8c222332f7ce7da0af07525cf5829a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c977bcba01e97c68c9979f32763300b8f48de3c6cc9fb9636c5639f6a3bdb6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eab928f76a4c4696994a8e9acaf198bc60b8c3810e15a5266474ee03c8c6fd24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptions]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36c802e3d3350be0836665440810dd1c27c073584683f92b2c2ce50d4785f61d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeSecurityPolicyRuleRateLimitOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRuleRateLimitOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a2ac183b8d66193ae0f3235cf1acb4f4f4f3824ce9bb7f3077a6df57b6f77e2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBanThreshold")
    def put_ban_threshold(
        self,
        *,
        count: jsii.Number,
        interval_sec: jsii.Number,
    ) -> None:
        '''
        :param count: Number of HTTP(S) requests for calculating the threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#count ComputeSecurityPolicy#count}
        :param interval_sec: Interval over which the threshold is computed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#interval_sec ComputeSecurityPolicy#interval_sec}
        '''
        value = ComputeSecurityPolicyRuleRateLimitOptionsBanThreshold(
            count=count, interval_sec=interval_sec
        )

        return typing.cast(None, jsii.invoke(self, "putBanThreshold", [value]))

    @jsii.member(jsii_name="putEnforceOnKeyConfigs")
    def put_enforce_on_key_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca20df3a58d8cafd3570753cc5d94fd63735854aaf0847870b4dd348609eb74f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEnforceOnKeyConfigs", [value]))

    @jsii.member(jsii_name="putExceedRedirectOptions")
    def put_exceed_redirect_options(
        self,
        *,
        type: builtins.str,
        target: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Type of the redirect action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#type ComputeSecurityPolicy#type}
        :param target: Target for the redirect action. This is required if the type is EXTERNAL_302 and cannot be specified for GOOGLE_RECAPTCHA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#target ComputeSecurityPolicy#target}
        '''
        value = ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptions(
            type=type, target=target
        )

        return typing.cast(None, jsii.invoke(self, "putExceedRedirectOptions", [value]))

    @jsii.member(jsii_name="putRateLimitThreshold")
    def put_rate_limit_threshold(
        self,
        *,
        count: jsii.Number,
        interval_sec: jsii.Number,
    ) -> None:
        '''
        :param count: Number of HTTP(S) requests for calculating the threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#count ComputeSecurityPolicy#count}
        :param interval_sec: Interval over which the threshold is computed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#interval_sec ComputeSecurityPolicy#interval_sec}
        '''
        value = ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThreshold(
            count=count, interval_sec=interval_sec
        )

        return typing.cast(None, jsii.invoke(self, "putRateLimitThreshold", [value]))

    @jsii.member(jsii_name="resetBanDurationSec")
    def reset_ban_duration_sec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBanDurationSec", []))

    @jsii.member(jsii_name="resetBanThreshold")
    def reset_ban_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBanThreshold", []))

    @jsii.member(jsii_name="resetEnforceOnKey")
    def reset_enforce_on_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforceOnKey", []))

    @jsii.member(jsii_name="resetEnforceOnKeyConfigs")
    def reset_enforce_on_key_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforceOnKeyConfigs", []))

    @jsii.member(jsii_name="resetEnforceOnKeyName")
    def reset_enforce_on_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforceOnKeyName", []))

    @jsii.member(jsii_name="resetExceedRedirectOptions")
    def reset_exceed_redirect_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExceedRedirectOptions", []))

    @builtins.property
    @jsii.member(jsii_name="banThreshold")
    def ban_threshold(
        self,
    ) -> ComputeSecurityPolicyRuleRateLimitOptionsBanThresholdOutputReference:
        return typing.cast(ComputeSecurityPolicyRuleRateLimitOptionsBanThresholdOutputReference, jsii.get(self, "banThreshold"))

    @builtins.property
    @jsii.member(jsii_name="enforceOnKeyConfigs")
    def enforce_on_key_configs(
        self,
    ) -> ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsList:
        return typing.cast(ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsList, jsii.get(self, "enforceOnKeyConfigs"))

    @builtins.property
    @jsii.member(jsii_name="exceedRedirectOptions")
    def exceed_redirect_options(
        self,
    ) -> ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsOutputReference:
        return typing.cast(ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsOutputReference, jsii.get(self, "exceedRedirectOptions"))

    @builtins.property
    @jsii.member(jsii_name="rateLimitThreshold")
    def rate_limit_threshold(
        self,
    ) -> "ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdOutputReference":
        return typing.cast("ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdOutputReference", jsii.get(self, "rateLimitThreshold"))

    @builtins.property
    @jsii.member(jsii_name="banDurationSecInput")
    def ban_duration_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "banDurationSecInput"))

    @builtins.property
    @jsii.member(jsii_name="banThresholdInput")
    def ban_threshold_input(
        self,
    ) -> typing.Optional[ComputeSecurityPolicyRuleRateLimitOptionsBanThreshold]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyRuleRateLimitOptionsBanThreshold], jsii.get(self, "banThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="conformActionInput")
    def conform_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conformActionInput"))

    @builtins.property
    @jsii.member(jsii_name="enforceOnKeyConfigsInput")
    def enforce_on_key_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs]]], jsii.get(self, "enforceOnKeyConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="enforceOnKeyInput")
    def enforce_on_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enforceOnKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="enforceOnKeyNameInput")
    def enforce_on_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enforceOnKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="exceedActionInput")
    def exceed_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exceedActionInput"))

    @builtins.property
    @jsii.member(jsii_name="exceedRedirectOptionsInput")
    def exceed_redirect_options_input(
        self,
    ) -> typing.Optional[ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptions]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptions], jsii.get(self, "exceedRedirectOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="rateLimitThresholdInput")
    def rate_limit_threshold_input(
        self,
    ) -> typing.Optional["ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThreshold"]:
        return typing.cast(typing.Optional["ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThreshold"], jsii.get(self, "rateLimitThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="banDurationSec")
    def ban_duration_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "banDurationSec"))

    @ban_duration_sec.setter
    def ban_duration_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1ab3be979613f0f79565fda941c2fb7235bbdf7f029567904cf0724d50d5c2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "banDurationSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="conformAction")
    def conform_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "conformAction"))

    @conform_action.setter
    def conform_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__761d92b700239734ac7ef4b940496cf91dd10d811e2b36a8c64f6554d7b9aebd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "conformAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforceOnKey")
    def enforce_on_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enforceOnKey"))

    @enforce_on_key.setter
    def enforce_on_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9d0f00bec5df1be16273c70d4a27b7af4342f348756680ee715b1e002f25464)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforceOnKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforceOnKeyName")
    def enforce_on_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enforceOnKeyName"))

    @enforce_on_key_name.setter
    def enforce_on_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8feb4ed2a4d85a192758bf4a79a2d1eab20c2c16c9eba86a8b20947f204c4a7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforceOnKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exceedAction")
    def exceed_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exceedAction"))

    @exceed_action.setter
    def exceed_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b589c87d548a19aeb1c5373ee1c2dcdf44f20973ebccf2da32bd7cb3e7e7f556)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exceedAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeSecurityPolicyRuleRateLimitOptions]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyRuleRateLimitOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeSecurityPolicyRuleRateLimitOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdb62f553ee1bf9d3eed4bf979fe2ceaecd399328410e9843e36d18cec81b82e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThreshold",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "interval_sec": "intervalSec"},
)
class ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThreshold:
    def __init__(self, *, count: jsii.Number, interval_sec: jsii.Number) -> None:
        '''
        :param count: Number of HTTP(S) requests for calculating the threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#count ComputeSecurityPolicy#count}
        :param interval_sec: Interval over which the threshold is computed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#interval_sec ComputeSecurityPolicy#interval_sec}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__627a8fa941a20f4d26571249e9004f9eb22d682c1854dc8142c5955c1a8ff2fe)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument interval_sec", value=interval_sec, expected_type=type_hints["interval_sec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "count": count,
            "interval_sec": interval_sec,
        }

    @builtins.property
    def count(self) -> jsii.Number:
        '''Number of HTTP(S) requests for calculating the threshold.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#count ComputeSecurityPolicy#count}
        '''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def interval_sec(self) -> jsii.Number:
        '''Interval over which the threshold is computed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#interval_sec ComputeSecurityPolicy#interval_sec}
        '''
        result = self._values.get("interval_sec")
        assert result is not None, "Required property 'interval_sec' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThreshold(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9eaf37dd4aa2efa247cc290bf0857acb60cd039315dc6fb4816c8f1f9285578b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalSecInput")
    def interval_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalSecInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6082b8f2cb35af7198fa1b7d366c80128aefca8dcb667658551dd0d7e6487f04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalSec")
    def interval_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "intervalSec"))

    @interval_sec.setter
    def interval_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06b8e02a62e0d3743b0fb803ee4acaf78125dae8ebd16d7ee0439e2629a6c824)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThreshold]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThreshold], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThreshold],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__727cf41fdb4d2931b370f37b65f73fa7b0f21c359251b9f0487ba29f75b279a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRuleRedirectOptions",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "target": "target"},
)
class ComputeSecurityPolicyRuleRedirectOptions:
    def __init__(
        self,
        *,
        type: builtins.str,
        target: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Type of the redirect action. Available options: EXTERNAL_302: Must specify the corresponding target field in config. GOOGLE_RECAPTCHA: Cannot specify target field in config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#type ComputeSecurityPolicy#type}
        :param target: Target for the redirect action. This is required if the type is EXTERNAL_302 and cannot be specified for GOOGLE_RECAPTCHA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#target ComputeSecurityPolicy#target}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aac13f1b4905ddf26ddbb8453a3057f859fe57c84d0e1a6e0f14fb5eae4abad)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def type(self) -> builtins.str:
        '''Type of the redirect action.

        Available options: EXTERNAL_302: Must specify the corresponding target field in config. GOOGLE_RECAPTCHA: Cannot specify target field in config.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#type ComputeSecurityPolicy#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''Target for the redirect action. This is required if the type is EXTERNAL_302 and cannot be specified for GOOGLE_RECAPTCHA.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#target ComputeSecurityPolicy#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyRuleRedirectOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyRuleRedirectOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyRuleRedirectOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f0aaade5768d1f861a1fd7bb46e48e208728d212621f0a16b87f91488bf5235)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c666b5c3904f0628d16cbe185df350c6546b4a9d4872bbd9f61d63b1ad66ce2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e12b945bb1aab569cc6726879123655348d0c14bf97ee8cec2ca1c77d306e9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeSecurityPolicyRuleRedirectOptions]:
        return typing.cast(typing.Optional[ComputeSecurityPolicyRuleRedirectOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeSecurityPolicyRuleRedirectOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f53d180910dc419c7db74a348b930cb0db2c0b31d8e37c0770e99b3479aebf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeSecurityPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#create ComputeSecurityPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#delete ComputeSecurityPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#update ComputeSecurityPolicy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8efc9556a6a0b01e405855ae88e02148f377321c7ff8218d5da02325a7016364)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#create ComputeSecurityPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#delete ComputeSecurityPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_security_policy#update ComputeSecurityPolicy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSecurityPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSecurityPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSecurityPolicy.ComputeSecurityPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1bb462b4b40f85ca0a3d8806322316b73204e16ecf12a7855362e2b25459815e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53ac3466e0b3a7b1f7355c7771d64794f6f45d51a63f52e9754e4bba05aeeb52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3db610b63e76611c9ca1b2026e28f6e5fcdde22da5020bbdfd18526a790e3574)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26b944ecd7ead4abf448c2013f75e606b344e350cc0a483e82fe664922a0f71c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc45ed2e0cfb524349fd8a399c940319534e76e92aa46125552023370c50d243)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeSecurityPolicy",
    "ComputeSecurityPolicyAdaptiveProtectionConfig",
    "ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig",
    "ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigOutputReference",
    "ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs",
    "ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsList",
    "ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsOutputReference",
    "ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs",
    "ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigsList",
    "ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigsOutputReference",
    "ComputeSecurityPolicyAdaptiveProtectionConfigOutputReference",
    "ComputeSecurityPolicyAdvancedOptionsConfig",
    "ComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfig",
    "ComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfigOutputReference",
    "ComputeSecurityPolicyAdvancedOptionsConfigOutputReference",
    "ComputeSecurityPolicyConfig",
    "ComputeSecurityPolicyRecaptchaOptionsConfig",
    "ComputeSecurityPolicyRecaptchaOptionsConfigOutputReference",
    "ComputeSecurityPolicyRule",
    "ComputeSecurityPolicyRuleHeaderAction",
    "ComputeSecurityPolicyRuleHeaderActionOutputReference",
    "ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds",
    "ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsList",
    "ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsOutputReference",
    "ComputeSecurityPolicyRuleList",
    "ComputeSecurityPolicyRuleMatch",
    "ComputeSecurityPolicyRuleMatchConfig",
    "ComputeSecurityPolicyRuleMatchConfigOutputReference",
    "ComputeSecurityPolicyRuleMatchExpr",
    "ComputeSecurityPolicyRuleMatchExprOptions",
    "ComputeSecurityPolicyRuleMatchExprOptionsOutputReference",
    "ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptions",
    "ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsOutputReference",
    "ComputeSecurityPolicyRuleMatchExprOutputReference",
    "ComputeSecurityPolicyRuleMatchOutputReference",
    "ComputeSecurityPolicyRuleOutputReference",
    "ComputeSecurityPolicyRulePreconfiguredWafConfig",
    "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusion",
    "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionList",
    "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionOutputReference",
    "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie",
    "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieList",
    "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieOutputReference",
    "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader",
    "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderList",
    "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderOutputReference",
    "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam",
    "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamList",
    "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamOutputReference",
    "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri",
    "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriList",
    "ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriOutputReference",
    "ComputeSecurityPolicyRulePreconfiguredWafConfigOutputReference",
    "ComputeSecurityPolicyRuleRateLimitOptions",
    "ComputeSecurityPolicyRuleRateLimitOptionsBanThreshold",
    "ComputeSecurityPolicyRuleRateLimitOptionsBanThresholdOutputReference",
    "ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs",
    "ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsList",
    "ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsOutputReference",
    "ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptions",
    "ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsOutputReference",
    "ComputeSecurityPolicyRuleRateLimitOptionsOutputReference",
    "ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThreshold",
    "ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdOutputReference",
    "ComputeSecurityPolicyRuleRedirectOptions",
    "ComputeSecurityPolicyRuleRedirectOptionsOutputReference",
    "ComputeSecurityPolicyTimeouts",
    "ComputeSecurityPolicyTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__7a59c3318fbcecbddc8ed7d1ff918bb9920ef120f8bb784e7180855dd88b8270(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    adaptive_protection_config: typing.Optional[typing.Union[ComputeSecurityPolicyAdaptiveProtectionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    advanced_options_config: typing.Optional[typing.Union[ComputeSecurityPolicyAdvancedOptionsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    recaptcha_options_config: typing.Optional[typing.Union[ComputeSecurityPolicyRecaptchaOptionsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[ComputeSecurityPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__376dbaec45717e998256b914a5be300a09c18fc5905d5125ca2b736090e6ab20(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d631794c35e30e47ee1690f99a283477b2609e883e8ae8bbf7e1a4b1fda0b55b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ae4bcb1126273705e87c758eea02ed4783812a2edf3c30dc6db70b77d6f8407(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b31848e8093121060dd26c52739477cf0908de5e29bc756209af58e599ad720(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fad7748849f59d44af2052aa0e487d98e58302bcee482eca7bfa1a891258c86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9823743ae42e9de223bf84137402ea28e19eb9a04f62cdb8a73ac86d55f5c81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4840c1149449708bd5bc5284f5ce54485f810f2748b484baf14846cbc2a4dbb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__199704435de57e2755e400ffaa603c7f9ce1ae9baf0a0adde2d5822dfb8a31fd(
    *,
    layer7_ddos_defense_config: typing.Optional[typing.Union[ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19d3926c3cd50d957efe608297568fd1dcbaaa1415e53efd71d5e2c0c352bfcc(
    *,
    enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    rule_visibility: typing.Optional[builtins.str] = None,
    threshold_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9087537101729c145175bc05883f2de193515395d9667b4b9f19d8e48447de5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e09c15b8b612b635a7aa735cfd549ed7d00d9d81e7c1f0a51e9f4fd715b11358(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb51d815c9cac78b84228b45742cbf34e4cd2575de44443e52ea689d5d7be103(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a1531ed536f49c5632cc07bfa883bf96625b8916ac863b3753b27ff65ffef62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c870525dc44efdeab738313f85626c47dabd8201c1e53a5669809a2fff085a2(
    value: typing.Optional[ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83e155f3cebd7f21fb13c04667217cff67c2e6f15a4cab87f292e62b36024e6e(
    *,
    name: builtins.str,
    auto_deploy_confidence_threshold: typing.Optional[jsii.Number] = None,
    auto_deploy_expiration_sec: typing.Optional[jsii.Number] = None,
    auto_deploy_impacted_baseline_threshold: typing.Optional[jsii.Number] = None,
    auto_deploy_load_threshold: typing.Optional[jsii.Number] = None,
    detection_absolute_qps: typing.Optional[jsii.Number] = None,
    detection_load_threshold: typing.Optional[jsii.Number] = None,
    detection_relative_to_baseline_qps: typing.Optional[jsii.Number] = None,
    traffic_granularity_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34963b99ca2fe6e857b2365d7141ed5185a2a2003674222d97271528906cc8b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e0860ec128d10fc51f9f8bcc3112f5db25609f9a60d488790ca8c488a226b1d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14b794550a4a2717d507697c7a026affae798e1a6851d102c3b9e2b51a1c4d31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8490e0edc9b7cf092a715be71e8fa4c489f865b936ea884dd0f83e89190ffd1f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7513af91bcee546f05902756afaa33c3c9ffee948dacf12056614a131ad6a9a6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c89aaa1bdd27b577084e3c27c2f18128754bf11bc20e6565b6ace5b1c7472385(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e670a4eab1a311a49c4299c3111f5119cdb0f22dc6c3e4b3029cfdf919939b9f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc4eec2d2f262894385732609256a0e63db9028e51aefe973c61a496bee73d98(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e767b41278222e2265a1c12f7e9bdccbf4767a65e5453d5242e6523b837e7038(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44354cc2a8ecb693c0cf897dc309965b25113f23c2676cee0cee18ae14add58a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a357626efc3992798d03fcbb56b280ffbf2d80de4b3dba6f11befb73cee53eb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__279fb3ef974e07947dc5b56df3d58998b8fe261f24808f7cb97b1aee14f33ace(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d974eecae6c9f355cbec6f814d512b407e3b2daa5af9fd829313e1738200efd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f05137315c8c3a056e4ae7274fbf930ef955bd1e1ba46e98f915ee744e9f98e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5640825b89c28ec82d2ea16fd423306a65720cd8be9f34bf95c743f094a23b3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d972c10364066640686ce7ff36bf2f1d46069eff3fdb02b89fbb11a214679e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73f09ed01a6462299a5b0ca7044993b263ff46407ff248877d205b2b7fe4ec06(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8a3bc8f1deeaba37a1e783c90958f3175c5b82aebd6d3baf6bd9e9dc665c477(
    *,
    type: builtins.str,
    enable_each_unique_value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79cb202ac0f9010f99df83d4a488383c6ea80c1567598d8bccd7ed1148a7dc7f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80b9dfe8706c435713cac484c1f08d5a76a170f8814b7b8b561b1cba9f96b429(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f3708309b2d1f11981820494883e0b87b01058cb4fb21b0cdf25967b003768f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fe2dc0ed4b4f81e67a137266739a4f1926e0d6cb1a3781ef012c15684db10ed(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62e899c0054021862a268a576f50600aed9f017a9638d902921823877ff60319(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a13007df156d186a02850b3a393d6304031c74a791e80e9d9958f09952cec62c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__134a8da58323e8bef745e1d0ec96a4e630a951ee8e8193889045daa1df3aec49(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__510e99207755b7a2e935e8df7a5bc3f7b5cdb29ee7cc0ad14e80499e776a0106(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__143415ec9e0a578ec6fbcd6519c3d91901a4d6bd372a3adb03fcc495c0d101cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__748e2102ce3372413b71767839361cd43f4fada9aca2b46f9acc800e13591dc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__978ecdf9cf8f35141c0db87ac2f1b26628630d1279a5991950b89476aec769dc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eea86d03a5ab8e02ed798f7ca216655049cd4d5c8f1b54940b6ad2697d9e47ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84b19164a502b37dc7384a73488fd8c4300fe71ddbfbc0398be0babb55bb29ad(
    value: typing.Optional[ComputeSecurityPolicyAdaptiveProtectionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__500d086d3b46d5cd93122d7b3e2eb9fc4cb8d5eeb24beffd2d04a9280c109cb6(
    *,
    json_custom_config: typing.Optional[typing.Union[ComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    json_parsing: typing.Optional[builtins.str] = None,
    log_level: typing.Optional[builtins.str] = None,
    user_ip_request_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb438a3770599a7060e8985213810cf127f624adf96f5f8c7892cb4ccf8be8c9(
    *,
    content_types: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50adcd9096cba16307f01484481b6548777d3fab8d75f42fd6f430c74c7f2f6b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9320d9243e5054f17188c72ca115d9d6f1f110750661e74b4aa2968e15f30f6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__180cb74e067673d5caa2c518e8ed741d7d573a49cc9d83be7e01802068bc6d78(
    value: typing.Optional[ComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ce4bc4833a72106db1abbb69fa2d44a78065af930dd1b2c97f21ec140e2ca41(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08c2a9933288e7f5e5c08bffc64c081e2fb1915a7dfd5260c61bcd25b2e8e9d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c650944ee4f47f7d8179f3768e9ece58fa0b2ef5e5b3749a853aaf2829e3e04d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b728edb0b9c2f2fe38b376e9253365ac391b2871979c79c742d582cad4fe07e5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d87de7ea9e0db2366eba14f6d191c15740f0bd1023a1d97d0805225f8055f2ae(
    value: typing.Optional[ComputeSecurityPolicyAdvancedOptionsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c97d006ac70967c06c652a6605bacecfa15cfcba384633db1ceb0256c7b9150(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    adaptive_protection_config: typing.Optional[typing.Union[ComputeSecurityPolicyAdaptiveProtectionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    advanced_options_config: typing.Optional[typing.Union[ComputeSecurityPolicyAdvancedOptionsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    recaptcha_options_config: typing.Optional[typing.Union[ComputeSecurityPolicyRecaptchaOptionsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[ComputeSecurityPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b068fe9b98a44fb6a6aa907fd051099b34f7e8d1352488cff62bcfeae8b0c84e(
    *,
    redirect_site_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__885be4404a8b5093ce256dd04ce73b756036913abe822d6d5b90e80df0a435b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__496efa2250c8d2f1ee3c2bf14725ee4e46cfcd3ebd5b7272488353f583e38d9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c22e4d3904a31ad4e81c4bac230c381597419f12bb1a54f906089ec239b16e8(
    value: typing.Optional[ComputeSecurityPolicyRecaptchaOptionsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae0fcd526221b8cb2a77e91ef8175c0230c3eabcfed66475e14cb40aba3a579d(
    *,
    action: builtins.str,
    match: typing.Union[ComputeSecurityPolicyRuleMatch, typing.Dict[builtins.str, typing.Any]],
    priority: jsii.Number,
    description: typing.Optional[builtins.str] = None,
    header_action: typing.Optional[typing.Union[ComputeSecurityPolicyRuleHeaderAction, typing.Dict[builtins.str, typing.Any]]] = None,
    preconfigured_waf_config: typing.Optional[typing.Union[ComputeSecurityPolicyRulePreconfiguredWafConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    preview: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    rate_limit_options: typing.Optional[typing.Union[ComputeSecurityPolicyRuleRateLimitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    redirect_options: typing.Optional[typing.Union[ComputeSecurityPolicyRuleRedirectOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6e5af6a32266044b5ce1b2973a8f8a74429cbf3cc1ec110764d8575ec3bc4bd(
    *,
    request_headers_to_adds: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f6161c2b3dd3a49183d4e0f49c02a02cf5606a8be30066bdb102b325287cc88(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10a217310dc7342aee447c93826cc16903e230c24e0313a9b9415949a259f56f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4f94582f2f528842e2a2c32ebea9a79fcd34d3fdbebe881b3390c6ab5e9599e(
    value: typing.Optional[ComputeSecurityPolicyRuleHeaderAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a27d30e52936fe3622e42e0df85c5fd9ab5a91eeefc5373a0b73231f176060d(
    *,
    header_name: builtins.str,
    header_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6212324e258068ee60834543691245f0e9f03033eeec524161391d3c667c536(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68fdf236a66e51328c08444ffccb239137dccf86e49163ba25b91f1b79aa78d1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6545aee55fb954e1e8bdc46d3b707e24924e516ff1f9ec4c1119da465abff801(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b14c5c98cf86ef621ae03ce4f72d86afd2738e2ce1a54b04544f4850243f258f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf52dee9f6b3049130c9661274c9f6c199744ee3484b525bacaf07631b9f84e1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38ff1e2ff5bfb420e41cd853d478d9e9a2d6bcbc60b0c29f250d97c16d969d44(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5fa0c8b079e0d34f2a4819ba77536445247203c85a7b22586fc454a714a225d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d433e9e3b4f472ae17b94477ee2d4c7e1b1f8065057ce9d279e4593fc735b0de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a45104a09e4fd126dd94b0ea426b8294b45e58ac24b29f600597909010dec0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8270828ab9c7623cb48ae480aea52630e8d9779007ba2344bc3ea62c2969569b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__231e3b1ac9dd65130f8f5bc56dcb2797fa5d5cb217b9b23d9b7d4620028d987d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71d3b75a58ab15d230d71101cf3a1507fbd1293ec5687dd1c32e07a8a2919cd2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a50034553ab2b2a917c8389a7c3b3083119cc43da37649381af5f6a300e57b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10be10a2e22ba09a432818a8ebea01395fbee1d3c9961e547515d15092706bcc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5023f4d00bf38d78b323a963c5784fa035a7f1cbce40e43cbec203dfdbfe83a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bae9bd7f692d4e917b34319df5f5fdc581837e21c17795159eceb1e30c7ee4c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5c17b5f190a675920cf8b7ed3aeb1ac1b5d30e311ee6b3ceb46042dddfc1bf2(
    *,
    config: typing.Optional[typing.Union[ComputeSecurityPolicyRuleMatchConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    expr: typing.Optional[typing.Union[ComputeSecurityPolicyRuleMatchExpr, typing.Dict[builtins.str, typing.Any]]] = None,
    expr_options: typing.Optional[typing.Union[ComputeSecurityPolicyRuleMatchExprOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    versioned_expr: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7f0131dcc111c41d2dc494a82ab9e7a9ed28d4c8daf78f24f5d4f6b362d5486(
    *,
    src_ip_ranges: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__170e7681e03cd93ea3b9e85df3ec1220d1ce3ee46021dd9c2e5f04a376a77a01(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b04947e950a256ae1a5f76bd2253d7d6a2318ce736f9af4f73c5403b759e342(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd9faf10aad162e9024c8a541c911939d30f9f8e8b4adfadbfeaa1efe2ae5b1d(
    value: typing.Optional[ComputeSecurityPolicyRuleMatchConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37c7b584a5b111ec379bd0db55777d6bbfebe64b4c2d60dfa57f90fd8fac28fb(
    *,
    expression: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8742467b22d0f6d459645ccdf1507ee48250585c97cf2a4bd2ee3d054b6edd5b(
    *,
    recaptcha_options: typing.Union[ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptions, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e99f5efc8d6bae82f8b3a80b23df2112fbf3363461ef8ea6832daf7b0354e56d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31309abf56b081f47344740cd0de955007dca6d675a20a82d91b84ab608be3d5(
    value: typing.Optional[ComputeSecurityPolicyRuleMatchExprOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4768378bf15b08167c79d4634a54081d43ee99cecff751b629e051879767972(
    *,
    action_token_site_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    session_token_site_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__effaa0f12d053f180cdd5faff5b7e6ae42e0571c23424af213702acab6a7757c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b7aa4e0cf7be4bd25d112151fb0baea83893654de849703d54589dbb02ffd9a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a956149f51ea33679cbcbdc93133f6c93901fb6708328416b6df94ab822cac19(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20cfd09c41e73ad847b0e374b2ba5d98d8209bedcefeefb20b93754aac08ccee(
    value: typing.Optional[ComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f58206deb22370e0d9c1788f567955151d87180f8e965c916aa6a1dd5d553e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d000fb75d3f4849b7c747250befb6ebfbcdc732d26fc676fdd6fe4088296530f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90f0c7dd308c0d7fc522c9aec4f8e177084053ace12ddaf8bc80da6e95e73ab7(
    value: typing.Optional[ComputeSecurityPolicyRuleMatchExpr],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea77cb7ed8f08dbd809970e821556edd5e8ba302a974decb960d2f67a7cb84a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca3e66969f8e5fbe6a87752d2df17d2bd816c93502d3b450187d317c30de6d4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0305920f4fca2b9227d4bd65ca9c8a151501f6dc7e1a70a42903070ff0cf7a58(
    value: typing.Optional[ComputeSecurityPolicyRuleMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__211c25e6f8065efa28bc11230aeb136ace2c1f49a018eb9e07cc7c2b1d56702b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f7aa3eaa2127247714caf3bc80cee8b767fe6b2004f8f136b4ec78fda852085(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce3eb1838890d3a0f8636b6b1231b157aff90ab9bec13c831446b92307e31329(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f060c8190ec8192ed3dee6a1c3e1213a176fd6da323b5cccc232bad7405cfdfe(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7a6f0c9dec2247e20c0780bdae134e9f7059923ada7272594b1018b7eb137db(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6d0ac6bafb0510f527f4bef0865f853099122e3565073190464356b5855a6d5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89e68fa66f026a04ed275fd0c3ae77c197ec191878c2e470787692f467b2816a(
    *,
    exclusion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusion, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e4e5d4a6704be27a7f995946a3cd9f75941b3ac6eb875140efa6eef6bbfd082(
    *,
    target_rule_set: builtins.str,
    request_cookie: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie, typing.Dict[builtins.str, typing.Any]]]]] = None,
    request_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    request_query_param: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam, typing.Dict[builtins.str, typing.Any]]]]] = None,
    request_uri: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_rule_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9878a4c043e46f2be35a4948e7b81eb65a34d17496051269c103b11ec604d9d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ec15b8507b94760f54d7e6b64a720617c23bf6090cc2e45c5587f60e7021f22(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ffa3c2d9f45f048301a28df3d218b62e465ab493f21d9907a306fa03e16a709(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d638dcf3d1d08cd1bda7e5e2c39c19cacab3cdaaea4c5c8453b977edcaaf049(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4b8476bafdccf44c9bdff1d8088fa1e8f442f9cf4e1e743b32c47e4a1f3f33f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7402b55b8a967b80b63143b7726ec3b74ed9e68ba5f52e5bbe8d1db9140bc8e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusion]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__448eced29ccad4f77981255e4576a800c29dc7e165f3d9db2a5a9f4e2fe24683(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1d29f7d48dc5aec07877aaf52ddeefe6e2e73d480b4c50ce2acdb13c9495894(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4380a7b83c47c31e8009f622e6c9a0aafdca9e591e7af44daeee32d603c0b759(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00554e93734baa6df94c817f54fbf0a01d863464d94459f37589772d8f9b0c90(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8935a3c8a067b19ca2422dbc62648bb660f1257c2ead4329f7b48af2907dee20(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a3d0615f978aae667964187dca9fbb17e21376d58b3c4349c14196eec21ff85(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__608caf0ef6978f5b6f6d96b68ca06bda170e947d5ebbba1fbf6af41992f6cc53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12cf0f4c5d2c13ece9fcda63f6f494300d7e5d4adf0b57bdd8db6ae8c9198e73(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusion]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__566fcf96d097daa1fd78723f1dc343a05867273e01ba77d710190b7a8104a4ae(
    *,
    operator: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__622a9d498b969761fc8afb0a1f450e226272f0458dc5f2bc9877b0c423908f29(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87a3c1437323dcb3004e977e5d1de289403e233259735034762249409ce5e4c5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b55cdec1c587776e2b59f1cf191d5516128a97f4546faccc1ff8db4a77030cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11711aa012758e34e7603c7ab08807f8c8816a407111f84646f3701465fc804a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b46575d737412682e85d8d4103467956f0d0fd1271338ead0021d9cc5cc2acb1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e4322b3d339fe9a61f55e5a37834dfa2a2cd97b6ec2f3a2ac30fa5ad2514ca1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40afa676cfd7f5f8669c551c947086424347bb5b70a2eb2923cdbcf031bdec59(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fa3caffb871402b04a217720ddbd0c28addc8f4382d2e73dc06a5695896bad5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__603c14b3bc4e4397d8b43ad9320bcdd3ccc50a6db99b0b4840b3242872253bc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__201e35b7e33c3234a3bffdebfb79fde00d2c08299c237635bb3be3b3c281071a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42fb9c46f07606b327504f47c438a9706425d54a3e905a7c0afc65ca29c2b17e(
    *,
    operator: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__accceca5e04b92bf62fd7f4c79c43c8c3f5502ac19ccdfb666240f6fc531a3b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__182a75d34b195ae3ea57246363874fd596c55f0cf9777b77f5596060fbe5656e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cd80ef91236a2de5a7a381b473fd3d25d91595cf6a996d091598af6c137cde7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50b501737d13d1b34afbb77f57613c2270a60ea52a4f616cad4f9a985c28b9c8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1520a96e72f6a7181a387c0e1a9204891fad1464a75b8b14cda11cd2cadd52b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6a7f61d9b857b5c5c6f17370c4bbe5ee60f29500274815decf7403fa11a759d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acfb268b94b005d0be0edc97c42b1bec0fe973e5d77bc9e5d771343f54acd237(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0154beb0926c7e8588bfc4f4a0784fd66c1f0c8c9a62acde5b1e28943a7e8c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c711c115b7bba62167eee98e4c14e88cfb8a7df259008c4b8ca6f46e0a2dd99a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17ef1886fe99c02ef33ef6fff553aa492f6e9cd2103e705ba332541bfa92ac12(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d75914f78158edc5ee8e4e6ddb1bef4c8544e98a581242b02e0c98b1840f80d(
    *,
    operator: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c002751015b88ef8e078e11685d90bb1bcda525e428863bdde21cea629b7ad9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__407c9a345bc21af7d13c76c8cfe5ad8e009c0cce518502ba677e0e27d9281560(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07dffbd8b024d5a149468967a0a94cbf3c0ca541cd1a546615a5fb086a1c19b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be94ecb9309a5a7c4957a37a5675e248684d5f03acbebd5f4b1ae0e92b57f099(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b7976050fcf8a3526d11bcb34a5f9996e4043ff24b4525e163235bf2767f013(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2c5caae8933ab8b0c35f6fbddc7ebabeeb7cddcf70945cbc0b0ff08a4c09fe7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dec8919a18360cc32defad77ce81e52a0d59ee977d5333d960ba04ce8c1d75f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0be4a6ea69964b419ce934250c8f036dc746beb342ba110e9fd50667c2f2c8ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1317274df5369f1bd3e83bf93e9ec9756e9b033b39675a3cfaeb81da8ff61e3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__136496b79285d30bdbb5b4c4f66dba1b6a696765aaeb228e0de4fb7fd8e208cc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11d205aaa4638bcb3efc89d860d5aeaf78f5064f4d6e00e6f86709c298250abd(
    *,
    operator: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c7659036c05d1bf595cba9a954bd224e2bf8989ae8d0396cfcfbe8f663248cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f65653f409ae0efe0c13b05ee843b986fdfbc397524f55f662d058caf9afe6e9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__641c6f51907ff52c4dbc45556fbbb0736ea54d817b58dce5e8514d65ea1bea01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aeb60da934a10179cd8601656bc10c6a87710643a14f08bd7b6d77a88ee589f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65e15a1d4efe56a7b3d84ee71ccd9452032c3d479a8a8de09a926afb3b3fc995(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc2b81b47626eecf3b69aa570022962490435ed2d7cb1af8a3861e3d71389950(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06033ad544ed20e54997e0a6d72243452822e72809970191854e41099a0e4e32(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f40b5618673c603d6391983642c50cf841edf699e10fe2cee8950869472dc86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4658c7a6b90b451ad1d8b7475ff80a8209495e75849cb6779ded0a96f1c621c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6832546d2d5a79062535a70575954f53875a4163d285996561140a59105d2b7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__888a683b089acbdceaed7bc5b65c71e76fbd761bde575968d95c569b5aa7c85f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c56f6126242ff8c4f75819246994ac6137997a41214f87c467e57782ebcc8090(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyRulePreconfiguredWafConfigExclusion, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ae88ef482544cb04b659e6f2cf8682e291f394b8efbeb7ef6f49087bbd0ebf6(
    value: typing.Optional[ComputeSecurityPolicyRulePreconfiguredWafConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8964420ef94d2ee7d1a8fee257f6e49399859e20a032775b33de9622f9b9a1f5(
    *,
    conform_action: builtins.str,
    exceed_action: builtins.str,
    rate_limit_threshold: typing.Union[ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThreshold, typing.Dict[builtins.str, typing.Any]],
    ban_duration_sec: typing.Optional[jsii.Number] = None,
    ban_threshold: typing.Optional[typing.Union[ComputeSecurityPolicyRuleRateLimitOptionsBanThreshold, typing.Dict[builtins.str, typing.Any]]] = None,
    enforce_on_key: typing.Optional[builtins.str] = None,
    enforce_on_key_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enforce_on_key_name: typing.Optional[builtins.str] = None,
    exceed_redirect_options: typing.Optional[typing.Union[ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbf526eca30c6b0f5bce336280236cfb750b870c91f436d0c2f88d03d3beb9b4(
    *,
    count: jsii.Number,
    interval_sec: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__026cc302ef58180b8ba186963cf29af6e377aa949042ead69d12106594a9ca5c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebca3ab5137f57cc3f5366c9fbd35f63cb26e64743a0cb247520b3fdeb343f68(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85877065a916deed9b1829d47a1629c4fd3d5fefdd8f0dd16a69794939a19522(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f6b4172af51d85b092252583003c0568665f8ad806ef9c0dcbe50772cd95762(
    value: typing.Optional[ComputeSecurityPolicyRuleRateLimitOptionsBanThreshold],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efbf44ceeeedc5236a8ac0a88aa5780e34c8f8cf423af99953ec7e144d4503c9(
    *,
    enforce_on_key_name: typing.Optional[builtins.str] = None,
    enforce_on_key_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74f3bb6e05084f5b5d45d3e04c9d755ea41885058788a1b0de211eb51926b633(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15d252f9e5b2ede120a826b3b873df2f18fc9787b0d93a047823d97239b81b9d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c6b1f930ceb4967c3a90f78aa503e01dd31c7ce4882255339821b48e261159a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__211885d4cad2d72df47b6a983fe335fb5e4d3d8442f899b7648c1dedc4df10a5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__819f2f14141baf659fa079010b61f96270ce853b86f2c208dd081dc336c33c7f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c5de3faf3aeaaa998664b31cbb4bac59dda3fba3db1f888eec3ddb5dd433e16(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a94cf952db1e9a64f1300cd09168336d0f1f307bf230a56ad0e7d054e684d8a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cbb83b86add9aaca532bd5d4abe13d8feefa911e9b261dabb1332323665ae5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__472b844b40ffc31964df72b1f8e88144440615a5ce59f9c2e73c5e8ac96886fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7646c181e46fdb43d9368625d69e591ee4a2ffc4d98bd0fb0093e72383b04c86(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91f662a0ffdac86f09124fdd5771e3d7b96af3fcd647e82226c6b988f52d14a7(
    *,
    type: builtins.str,
    target: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6465aff36ac8c6401e1b5cfa8e5c0c4ac8c222332f7ce7da0af07525cf5829a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c977bcba01e97c68c9979f32763300b8f48de3c6cc9fb9636c5639f6a3bdb6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eab928f76a4c4696994a8e9acaf198bc60b8c3810e15a5266474ee03c8c6fd24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36c802e3d3350be0836665440810dd1c27c073584683f92b2c2ce50d4785f61d(
    value: typing.Optional[ComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a2ac183b8d66193ae0f3235cf1acb4f4f4f3824ce9bb7f3077a6df57b6f77e2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca20df3a58d8cafd3570753cc5d94fd63735854aaf0847870b4dd348609eb74f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1ab3be979613f0f79565fda941c2fb7235bbdf7f029567904cf0724d50d5c2d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__761d92b700239734ac7ef4b940496cf91dd10d811e2b36a8c64f6554d7b9aebd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9d0f00bec5df1be16273c70d4a27b7af4342f348756680ee715b1e002f25464(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8feb4ed2a4d85a192758bf4a79a2d1eab20c2c16c9eba86a8b20947f204c4a7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b589c87d548a19aeb1c5373ee1c2dcdf44f20973ebccf2da32bd7cb3e7e7f556(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdb62f553ee1bf9d3eed4bf979fe2ceaecd399328410e9843e36d18cec81b82e(
    value: typing.Optional[ComputeSecurityPolicyRuleRateLimitOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__627a8fa941a20f4d26571249e9004f9eb22d682c1854dc8142c5955c1a8ff2fe(
    *,
    count: jsii.Number,
    interval_sec: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eaf37dd4aa2efa247cc290bf0857acb60cd039315dc6fb4816c8f1f9285578b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6082b8f2cb35af7198fa1b7d366c80128aefca8dcb667658551dd0d7e6487f04(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06b8e02a62e0d3743b0fb803ee4acaf78125dae8ebd16d7ee0439e2629a6c824(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__727cf41fdb4d2931b370f37b65f73fa7b0f21c359251b9f0487ba29f75b279a8(
    value: typing.Optional[ComputeSecurityPolicyRuleRateLimitOptionsRateLimitThreshold],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aac13f1b4905ddf26ddbb8453a3057f859fe57c84d0e1a6e0f14fb5eae4abad(
    *,
    type: builtins.str,
    target: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f0aaade5768d1f861a1fd7bb46e48e208728d212621f0a16b87f91488bf5235(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c666b5c3904f0628d16cbe185df350c6546b4a9d4872bbd9f61d63b1ad66ce2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e12b945bb1aab569cc6726879123655348d0c14bf97ee8cec2ca1c77d306e9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f53d180910dc419c7db74a348b930cb0db2c0b31d8e37c0770e99b3479aebf2(
    value: typing.Optional[ComputeSecurityPolicyRuleRedirectOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8efc9556a6a0b01e405855ae88e02148f377321c7ff8218d5da02325a7016364(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bb462b4b40f85ca0a3d8806322316b73204e16ecf12a7855362e2b25459815e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53ac3466e0b3a7b1f7355c7771d64794f6f45d51a63f52e9754e4bba05aeeb52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3db610b63e76611c9ca1b2026e28f6e5fcdde22da5020bbdfd18526a790e3574(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26b944ecd7ead4abf448c2013f75e606b344e350cc0a483e82fe664922a0f71c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc45ed2e0cfb524349fd8a399c940319534e76e92aa46125552023370c50d243(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSecurityPolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
