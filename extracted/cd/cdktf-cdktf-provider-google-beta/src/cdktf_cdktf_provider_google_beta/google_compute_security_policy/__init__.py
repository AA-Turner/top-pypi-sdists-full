r'''
# `google_compute_security_policy`

Refer to the Terraform Registry for docs: [`google_compute_security_policy`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy).
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


class GoogleComputeSecurityPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy google_compute_security_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        adaptive_protection_config: typing.Optional[typing.Union["GoogleComputeSecurityPolicyAdaptiveProtectionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        advanced_options_config: typing.Optional[typing.Union["GoogleComputeSecurityPolicyAdvancedOptionsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        recaptcha_options_config: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRecaptchaOptionsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeSecurityPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy google_compute_security_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name of the security policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#name GoogleComputeSecurityPolicy#name}
        :param adaptive_protection_config: adaptive_protection_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#adaptive_protection_config GoogleComputeSecurityPolicy#adaptive_protection_config}
        :param advanced_options_config: advanced_options_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#advanced_options_config GoogleComputeSecurityPolicy#advanced_options_config}
        :param description: An optional description of this security policy. Max size is 2048. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#description GoogleComputeSecurityPolicy#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#id GoogleComputeSecurityPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: The project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#project GoogleComputeSecurityPolicy#project}
        :param recaptcha_options_config: recaptcha_options_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#recaptcha_options_config GoogleComputeSecurityPolicy#recaptcha_options_config}
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#rule GoogleComputeSecurityPolicy#rule}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#timeouts GoogleComputeSecurityPolicy#timeouts}
        :param type: The type indicates the intended use of the security policy. CLOUD_ARMOR - Cloud Armor backend security policies can be configured to filter incoming HTTP requests targeting backend services. They filter requests before they hit the origin servers. CLOUD_ARMOR_EDGE - Cloud Armor edge security policies can be configured to filter incoming HTTP requests targeting backend services (including Cloud CDN-enabled) as well as backend buckets (Cloud Storage). They filter requests before the request is served from Google's cache. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#type GoogleComputeSecurityPolicy#type}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fecc710847eadb6bb10f3f5ab244e929151509b547744cc5a42abff4762b2b7f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleComputeSecurityPolicyConfig(
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
        '''Generates CDKTF code for importing a GoogleComputeSecurityPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleComputeSecurityPolicy to import.
        :param import_from_id: The id of the existing GoogleComputeSecurityPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleComputeSecurityPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f85a1251d1be34e96d8514cb40a5186e53f4e80997c70a620c9497712c206cc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAdaptiveProtectionConfig")
    def put_adaptive_protection_config(
        self,
        *,
        auto_deploy_config: typing.Optional[typing.Union["GoogleComputeSecurityPolicyAdaptiveProtectionConfigAutoDeployConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        layer7_ddos_defense_config: typing.Optional[typing.Union["GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param auto_deploy_config: auto_deploy_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#auto_deploy_config GoogleComputeSecurityPolicy#auto_deploy_config}
        :param layer7_ddos_defense_config: layer_7_ddos_defense_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#layer_7_ddos_defense_config GoogleComputeSecurityPolicy#layer_7_ddos_defense_config}
        '''
        value = GoogleComputeSecurityPolicyAdaptiveProtectionConfig(
            auto_deploy_config=auto_deploy_config,
            layer7_ddos_defense_config=layer7_ddos_defense_config,
        )

        return typing.cast(None, jsii.invoke(self, "putAdaptiveProtectionConfig", [value]))

    @jsii.member(jsii_name="putAdvancedOptionsConfig")
    def put_advanced_options_config(
        self,
        *,
        json_custom_config: typing.Optional[typing.Union["GoogleComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        json_parsing: typing.Optional[builtins.str] = None,
        log_level: typing.Optional[builtins.str] = None,
        user_ip_request_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param json_custom_config: json_custom_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#json_custom_config GoogleComputeSecurityPolicy#json_custom_config}
        :param json_parsing: JSON body parsing. Supported values include: "DISABLED", "STANDARD". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#json_parsing GoogleComputeSecurityPolicy#json_parsing}
        :param log_level: Logging level. Supported values include: "NORMAL", "VERBOSE". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#log_level GoogleComputeSecurityPolicy#log_level}
        :param user_ip_request_headers: An optional list of case-insensitive request header names to use for resolving the callers client IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#user_ip_request_headers GoogleComputeSecurityPolicy#user_ip_request_headers}
        '''
        value = GoogleComputeSecurityPolicyAdvancedOptionsConfig(
            json_custom_config=json_custom_config,
            json_parsing=json_parsing,
            log_level=log_level,
            user_ip_request_headers=user_ip_request_headers,
        )

        return typing.cast(None, jsii.invoke(self, "putAdvancedOptionsConfig", [value]))

    @jsii.member(jsii_name="putRecaptchaOptionsConfig")
    def put_recaptcha_options_config(self, *, redirect_site_key: builtins.str) -> None:
        '''
        :param redirect_site_key: A field to supply a reCAPTCHA site key to be used for all the rules using the redirect action with the type of GOOGLE_RECAPTCHA under the security policy. The specified site key needs to be created from the reCAPTCHA API. The user is responsible for the validity of the specified site key. If not specified, a Google-managed site key is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#redirect_site_key GoogleComputeSecurityPolicy#redirect_site_key}
        '''
        value = GoogleComputeSecurityPolicyRecaptchaOptionsConfig(
            redirect_site_key=redirect_site_key
        )

        return typing.cast(None, jsii.invoke(self, "putRecaptchaOptionsConfig", [value]))

    @jsii.member(jsii_name="putRule")
    def put_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__252ba1039fcb14988ce91252c90820570f7cf04fbeec8b98109ad4d9ae8bd3de)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#create GoogleComputeSecurityPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#delete GoogleComputeSecurityPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#update GoogleComputeSecurityPolicy#update}.
        '''
        value = GoogleComputeSecurityPolicyTimeouts(
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
    ) -> "GoogleComputeSecurityPolicyAdaptiveProtectionConfigOutputReference":
        return typing.cast("GoogleComputeSecurityPolicyAdaptiveProtectionConfigOutputReference", jsii.get(self, "adaptiveProtectionConfig"))

    @builtins.property
    @jsii.member(jsii_name="advancedOptionsConfig")
    def advanced_options_config(
        self,
    ) -> "GoogleComputeSecurityPolicyAdvancedOptionsConfigOutputReference":
        return typing.cast("GoogleComputeSecurityPolicyAdvancedOptionsConfigOutputReference", jsii.get(self, "advancedOptionsConfig"))

    @builtins.property
    @jsii.member(jsii_name="fingerprint")
    def fingerprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fingerprint"))

    @builtins.property
    @jsii.member(jsii_name="recaptchaOptionsConfig")
    def recaptcha_options_config(
        self,
    ) -> "GoogleComputeSecurityPolicyRecaptchaOptionsConfigOutputReference":
        return typing.cast("GoogleComputeSecurityPolicyRecaptchaOptionsConfigOutputReference", jsii.get(self, "recaptchaOptionsConfig"))

    @builtins.property
    @jsii.member(jsii_name="rule")
    def rule(self) -> "GoogleComputeSecurityPolicyRuleList":
        return typing.cast("GoogleComputeSecurityPolicyRuleList", jsii.get(self, "rule"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleComputeSecurityPolicyTimeoutsOutputReference":
        return typing.cast("GoogleComputeSecurityPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="adaptiveProtectionConfigInput")
    def adaptive_protection_config_input(
        self,
    ) -> typing.Optional["GoogleComputeSecurityPolicyAdaptiveProtectionConfig"]:
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyAdaptiveProtectionConfig"], jsii.get(self, "adaptiveProtectionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="advancedOptionsConfigInput")
    def advanced_options_config_input(
        self,
    ) -> typing.Optional["GoogleComputeSecurityPolicyAdvancedOptionsConfig"]:
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyAdvancedOptionsConfig"], jsii.get(self, "advancedOptionsConfigInput"))

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
    ) -> typing.Optional["GoogleComputeSecurityPolicyRecaptchaOptionsConfig"]:
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRecaptchaOptionsConfig"], jsii.get(self, "recaptchaOptionsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleInput")
    def rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRule"]]], jsii.get(self, "ruleInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeSecurityPolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeSecurityPolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__5143e872f87b646bd1c6787c3e1339db86e7cd3e67ad945a77880bed487c949d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab39ace6afd00a35167c0a1ad7646361a60cd52bf32dbe65c005d22644b4a22b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__940e5de3fbc03eaef3e00ddb1394ef38bc0b5ce2cd1ecf69eb0fa2cf622afd34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ca7baabdc9215d67c5cb275bd32a295a6a4a868250e21095b423d4922fb6d3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d40370e34426fc44054bb6092a3ea30994af31d17e3020ee1cd56cb0b10168d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyAdaptiveProtectionConfig",
    jsii_struct_bases=[],
    name_mapping={
        "auto_deploy_config": "autoDeployConfig",
        "layer7_ddos_defense_config": "layer7DdosDefenseConfig",
    },
)
class GoogleComputeSecurityPolicyAdaptiveProtectionConfig:
    def __init__(
        self,
        *,
        auto_deploy_config: typing.Optional[typing.Union["GoogleComputeSecurityPolicyAdaptiveProtectionConfigAutoDeployConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        layer7_ddos_defense_config: typing.Optional[typing.Union["GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param auto_deploy_config: auto_deploy_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#auto_deploy_config GoogleComputeSecurityPolicy#auto_deploy_config}
        :param layer7_ddos_defense_config: layer_7_ddos_defense_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#layer_7_ddos_defense_config GoogleComputeSecurityPolicy#layer_7_ddos_defense_config}
        '''
        if isinstance(auto_deploy_config, dict):
            auto_deploy_config = GoogleComputeSecurityPolicyAdaptiveProtectionConfigAutoDeployConfig(**auto_deploy_config)
        if isinstance(layer7_ddos_defense_config, dict):
            layer7_ddos_defense_config = GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig(**layer7_ddos_defense_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d0dc85030e330c94b918e458e23d5871b399522566e8cb8453cca40e76a1964)
            check_type(argname="argument auto_deploy_config", value=auto_deploy_config, expected_type=type_hints["auto_deploy_config"])
            check_type(argname="argument layer7_ddos_defense_config", value=layer7_ddos_defense_config, expected_type=type_hints["layer7_ddos_defense_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_deploy_config is not None:
            self._values["auto_deploy_config"] = auto_deploy_config
        if layer7_ddos_defense_config is not None:
            self._values["layer7_ddos_defense_config"] = layer7_ddos_defense_config

    @builtins.property
    def auto_deploy_config(
        self,
    ) -> typing.Optional["GoogleComputeSecurityPolicyAdaptiveProtectionConfigAutoDeployConfig"]:
        '''auto_deploy_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#auto_deploy_config GoogleComputeSecurityPolicy#auto_deploy_config}
        '''
        result = self._values.get("auto_deploy_config")
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyAdaptiveProtectionConfigAutoDeployConfig"], result)

    @builtins.property
    def layer7_ddos_defense_config(
        self,
    ) -> typing.Optional["GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig"]:
        '''layer_7_ddos_defense_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#layer_7_ddos_defense_config GoogleComputeSecurityPolicy#layer_7_ddos_defense_config}
        '''
        result = self._values.get("layer7_ddos_defense_config")
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyAdaptiveProtectionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyAdaptiveProtectionConfigAutoDeployConfig",
    jsii_struct_bases=[],
    name_mapping={
        "confidence_threshold": "confidenceThreshold",
        "expiration_sec": "expirationSec",
        "impacted_baseline_threshold": "impactedBaselineThreshold",
        "load_threshold": "loadThreshold",
    },
)
class GoogleComputeSecurityPolicyAdaptiveProtectionConfigAutoDeployConfig:
    def __init__(
        self,
        *,
        confidence_threshold: typing.Optional[jsii.Number] = None,
        expiration_sec: typing.Optional[jsii.Number] = None,
        impacted_baseline_threshold: typing.Optional[jsii.Number] = None,
        load_threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param confidence_threshold: Rules are only automatically deployed for alerts on potential attacks with confidence scores greater than this threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#confidence_threshold GoogleComputeSecurityPolicy#confidence_threshold}
        :param expiration_sec: Google Cloud Armor stops applying the action in the automatically deployed rule to an identified attacker after this duration. The rule continues to operate against new requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#expiration_sec GoogleComputeSecurityPolicy#expiration_sec}
        :param impacted_baseline_threshold: Rules are only automatically deployed when the estimated impact to baseline traffic from the suggested mitigation is below this threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#impacted_baseline_threshold GoogleComputeSecurityPolicy#impacted_baseline_threshold}
        :param load_threshold: Identifies new attackers only when the load to the backend service that is under attack exceeds this threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#load_threshold GoogleComputeSecurityPolicy#load_threshold}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a0d3d057bfc44767b9f79e5d70a436d9691b380586648fb28b6acb1e62e6a1a)
            check_type(argname="argument confidence_threshold", value=confidence_threshold, expected_type=type_hints["confidence_threshold"])
            check_type(argname="argument expiration_sec", value=expiration_sec, expected_type=type_hints["expiration_sec"])
            check_type(argname="argument impacted_baseline_threshold", value=impacted_baseline_threshold, expected_type=type_hints["impacted_baseline_threshold"])
            check_type(argname="argument load_threshold", value=load_threshold, expected_type=type_hints["load_threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if confidence_threshold is not None:
            self._values["confidence_threshold"] = confidence_threshold
        if expiration_sec is not None:
            self._values["expiration_sec"] = expiration_sec
        if impacted_baseline_threshold is not None:
            self._values["impacted_baseline_threshold"] = impacted_baseline_threshold
        if load_threshold is not None:
            self._values["load_threshold"] = load_threshold

    @builtins.property
    def confidence_threshold(self) -> typing.Optional[jsii.Number]:
        '''Rules are only automatically deployed for alerts on potential attacks with confidence scores greater than this threshold.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#confidence_threshold GoogleComputeSecurityPolicy#confidence_threshold}
        '''
        result = self._values.get("confidence_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def expiration_sec(self) -> typing.Optional[jsii.Number]:
        '''Google Cloud Armor stops applying the action in the automatically deployed rule to an identified attacker after this duration.

        The rule continues to operate against new requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#expiration_sec GoogleComputeSecurityPolicy#expiration_sec}
        '''
        result = self._values.get("expiration_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def impacted_baseline_threshold(self) -> typing.Optional[jsii.Number]:
        '''Rules are only automatically deployed when the estimated impact to baseline traffic from the suggested mitigation is below this threshold.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#impacted_baseline_threshold GoogleComputeSecurityPolicy#impacted_baseline_threshold}
        '''
        result = self._values.get("impacted_baseline_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def load_threshold(self) -> typing.Optional[jsii.Number]:
        '''Identifies new attackers only when the load to the backend service that is under attack exceeds this threshold.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#load_threshold GoogleComputeSecurityPolicy#load_threshold}
        '''
        result = self._values.get("load_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyAdaptiveProtectionConfigAutoDeployConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyAdaptiveProtectionConfigAutoDeployConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyAdaptiveProtectionConfigAutoDeployConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ceedd3ff5bb1c19f8c4c7103d0a15a1e8a32fe2b8acc06c48f9250f8aa212cf4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetConfidenceThreshold")
    def reset_confidence_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfidenceThreshold", []))

    @jsii.member(jsii_name="resetExpirationSec")
    def reset_expiration_sec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpirationSec", []))

    @jsii.member(jsii_name="resetImpactedBaselineThreshold")
    def reset_impacted_baseline_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImpactedBaselineThreshold", []))

    @jsii.member(jsii_name="resetLoadThreshold")
    def reset_load_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadThreshold", []))

    @builtins.property
    @jsii.member(jsii_name="confidenceThresholdInput")
    def confidence_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "confidenceThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="expirationSecInput")
    def expiration_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "expirationSecInput"))

    @builtins.property
    @jsii.member(jsii_name="impactedBaselineThresholdInput")
    def impacted_baseline_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "impactedBaselineThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="loadThresholdInput")
    def load_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "loadThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="confidenceThreshold")
    def confidence_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "confidenceThreshold"))

    @confidence_threshold.setter
    def confidence_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eb6fa2b1afa426b6837bb7082ffb329b2259d5c74df95ce14289c37dbcae256)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "confidenceThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expirationSec")
    def expiration_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "expirationSec"))

    @expiration_sec.setter
    def expiration_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5cf8e099c8bc867f0b22a4e56fda63d4684965ac03c6066fb4fd4037ab6efd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expirationSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="impactedBaselineThreshold")
    def impacted_baseline_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "impactedBaselineThreshold"))

    @impacted_baseline_threshold.setter
    def impacted_baseline_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf8de267f0eff5efe0f4c0278a746a5f90dcf8c45c042e70a0862792f8986651)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "impactedBaselineThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadThreshold")
    def load_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "loadThreshold"))

    @load_threshold.setter
    def load_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52dac5ce159b846008a1e74b393fb5af79d0f8231a0ae9de173b2656cf00da3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeSecurityPolicyAdaptiveProtectionConfigAutoDeployConfig]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyAdaptiveProtectionConfigAutoDeployConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeSecurityPolicyAdaptiveProtectionConfigAutoDeployConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd67dba8b1a94508998a063513fed4078f39f17b8ffae3b7fba795551e12b0c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable": "enable",
        "rule_visibility": "ruleVisibility",
        "threshold_configs": "thresholdConfigs",
    },
)
class GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig:
    def __init__(
        self,
        *,
        enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rule_visibility: typing.Optional[builtins.str] = None,
        threshold_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enable: If set to true, enables CAAP for L7 DDoS detection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#enable GoogleComputeSecurityPolicy#enable}
        :param rule_visibility: Rule visibility. Supported values include: "STANDARD", "PREMIUM". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#rule_visibility GoogleComputeSecurityPolicy#rule_visibility}
        :param threshold_configs: threshold_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#threshold_configs GoogleComputeSecurityPolicy#threshold_configs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87a062d5d581c037f6158f794f46f40ae9bb0a86e2b7ab6f82d5815b072c247a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#enable GoogleComputeSecurityPolicy#enable}
        '''
        result = self._values.get("enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def rule_visibility(self) -> typing.Optional[builtins.str]:
        '''Rule visibility. Supported values include: "STANDARD", "PREMIUM".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#rule_visibility GoogleComputeSecurityPolicy#rule_visibility}
        '''
        result = self._values.get("rule_visibility")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def threshold_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs"]]]:
        '''threshold_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#threshold_configs GoogleComputeSecurityPolicy#threshold_configs}
        '''
        result = self._values.get("threshold_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9fa0b83569bf6a8a8c709b1c41cd3a914ed074426047b442cda1c91dedbf21d0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putThresholdConfigs")
    def put_threshold_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__887b137107aaf4399361b67d580813d021d1ae175b95c8ff9e5cd63b354daae0)
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
    ) -> "GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsList":
        return typing.cast("GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsList", jsii.get(self, "thresholdConfigs"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs"]]], jsii.get(self, "thresholdConfigsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__87fdcab022f06430539baaf30110061bf911f331798060ec239c717406178610)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ruleVisibility")
    def rule_visibility(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleVisibility"))

    @rule_visibility.setter
    def rule_visibility(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a81b284843829f29538e90c53bf4fdd87eaedaf3594ecd2088ec857663fd006)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleVisibility", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45eb42a967d8b0ccc1f0e0dce330875de5db155cb2aac831c30c8bee34ba75d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs",
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
class GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs:
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
        traffic_granularity_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name: The name must be 1-63 characters long, and comply with RFC1035. The name must be unique within the security policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#name GoogleComputeSecurityPolicy#name}
        :param auto_deploy_confidence_threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#auto_deploy_confidence_threshold GoogleComputeSecurityPolicy#auto_deploy_confidence_threshold}.
        :param auto_deploy_expiration_sec: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#auto_deploy_expiration_sec GoogleComputeSecurityPolicy#auto_deploy_expiration_sec}.
        :param auto_deploy_impacted_baseline_threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#auto_deploy_impacted_baseline_threshold GoogleComputeSecurityPolicy#auto_deploy_impacted_baseline_threshold}.
        :param auto_deploy_load_threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#auto_deploy_load_threshold GoogleComputeSecurityPolicy#auto_deploy_load_threshold}.
        :param detection_absolute_qps: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#detection_absolute_qps GoogleComputeSecurityPolicy#detection_absolute_qps}.
        :param detection_load_threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#detection_load_threshold GoogleComputeSecurityPolicy#detection_load_threshold}.
        :param detection_relative_to_baseline_qps: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#detection_relative_to_baseline_qps GoogleComputeSecurityPolicy#detection_relative_to_baseline_qps}.
        :param traffic_granularity_configs: traffic_granularity_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#traffic_granularity_configs GoogleComputeSecurityPolicy#traffic_granularity_configs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c06249d0dfd6d8b44076c3789b154d09a8b9722cc285d2c7fec897633b46f332)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#name GoogleComputeSecurityPolicy#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_deploy_confidence_threshold(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#auto_deploy_confidence_threshold GoogleComputeSecurityPolicy#auto_deploy_confidence_threshold}.'''
        result = self._values.get("auto_deploy_confidence_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def auto_deploy_expiration_sec(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#auto_deploy_expiration_sec GoogleComputeSecurityPolicy#auto_deploy_expiration_sec}.'''
        result = self._values.get("auto_deploy_expiration_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def auto_deploy_impacted_baseline_threshold(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#auto_deploy_impacted_baseline_threshold GoogleComputeSecurityPolicy#auto_deploy_impacted_baseline_threshold}.'''
        result = self._values.get("auto_deploy_impacted_baseline_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def auto_deploy_load_threshold(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#auto_deploy_load_threshold GoogleComputeSecurityPolicy#auto_deploy_load_threshold}.'''
        result = self._values.get("auto_deploy_load_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def detection_absolute_qps(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#detection_absolute_qps GoogleComputeSecurityPolicy#detection_absolute_qps}.'''
        result = self._values.get("detection_absolute_qps")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def detection_load_threshold(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#detection_load_threshold GoogleComputeSecurityPolicy#detection_load_threshold}.'''
        result = self._values.get("detection_load_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def detection_relative_to_baseline_qps(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#detection_relative_to_baseline_qps GoogleComputeSecurityPolicy#detection_relative_to_baseline_qps}.'''
        result = self._values.get("detection_relative_to_baseline_qps")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def traffic_granularity_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs"]]]:
        '''traffic_granularity_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#traffic_granularity_configs GoogleComputeSecurityPolicy#traffic_granularity_configs}
        '''
        result = self._values.get("traffic_granularity_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfd3ccd1693b5449d534682b31c00b82bb9c841386c83eafb5fbafe90f726738)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aadc527c4de746b3d924629a831411276f647b73c1d193848deacc700de00b1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0e45d3f807dea3cf8aefd9856e6537773317f46f20a8c04213ac0b0f86f560e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1347bd1888c11e1c42e0b0c6e7916a0f8055c1b5458e52cafb44ca9a4a2d9deb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a58ea1c8bfda7cda500d5f537f9955adb8ac06fe15ce4267d6c36e7074d68a35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a63e2c0ca3a66af2906e250909708ae45b0ef22c84dc601f537078120a2eee8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__acb9fe3bd5795f41ceaa837a094e5e225de04a793b0754fe39edb3bf8bfa6919)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putTrafficGranularityConfigs")
    def put_traffic_granularity_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d7d9213d460836bfa84c3f016b04226650ae384db341bc24634363752baa14e)
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
    ) -> "GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigsList":
        return typing.cast("GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigsList", jsii.get(self, "trafficGranularityConfigs"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs"]]], jsii.get(self, "trafficGranularityConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="autoDeployConfidenceThreshold")
    def auto_deploy_confidence_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "autoDeployConfidenceThreshold"))

    @auto_deploy_confidence_threshold.setter
    def auto_deploy_confidence_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d7c73f8c0476009039cf3a370bf1d2f9821a88a83c1aa6ba12ce4127ef81c07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoDeployConfidenceThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoDeployExpirationSec")
    def auto_deploy_expiration_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "autoDeployExpirationSec"))

    @auto_deploy_expiration_sec.setter
    def auto_deploy_expiration_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42541018cb27f62f5f48dc1d8261ed7bb56b4ef153bb6451a5a1699863a6c6cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoDeployExpirationSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoDeployImpactedBaselineThreshold")
    def auto_deploy_impacted_baseline_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "autoDeployImpactedBaselineThreshold"))

    @auto_deploy_impacted_baseline_threshold.setter
    def auto_deploy_impacted_baseline_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40fd428f73db95641efc4c124a67d761d5b05285aaf2c29410b52366a083daf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoDeployImpactedBaselineThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoDeployLoadThreshold")
    def auto_deploy_load_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "autoDeployLoadThreshold"))

    @auto_deploy_load_threshold.setter
    def auto_deploy_load_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc6b74178bd20ab5ecca0830ffdfddc95f043d68faa1b1b86d528536ee80ccf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoDeployLoadThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="detectionAbsoluteQps")
    def detection_absolute_qps(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "detectionAbsoluteQps"))

    @detection_absolute_qps.setter
    def detection_absolute_qps(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c804afb367a039deb8b52e9d482268c45d18f88b354c31bf4b49a78d37c7c192)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "detectionAbsoluteQps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="detectionLoadThreshold")
    def detection_load_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "detectionLoadThreshold"))

    @detection_load_threshold.setter
    def detection_load_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18d4f1eab9e6a03d1c86b03c97d890cbf97d9f1a436e27b32ed41a4b06e39239)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "detectionLoadThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="detectionRelativeToBaselineQps")
    def detection_relative_to_baseline_qps(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "detectionRelativeToBaselineQps"))

    @detection_relative_to_baseline_qps.setter
    def detection_relative_to_baseline_qps(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63a29e6da705b883cde7bd853f3a664c10218112c5ac7c1753caea5a777ae2e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "detectionRelativeToBaselineQps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3498c05bb2fb6d7bead05e021ac4f214463aaf02f7b15716dc39bcf697d1f3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3187954075d1e14ef0444093f7559454bde69bb5e2efc994efae2de1ecc67488)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "enable_each_unique_value": "enableEachUniqueValue",
        "value": "value",
    },
)
class GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs:
    def __init__(
        self,
        *,
        type: builtins.str,
        enable_each_unique_value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Type of this configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#type GoogleComputeSecurityPolicy#type}
        :param enable_each_unique_value: If enabled, traffic matching each unique value for the specified type constitutes a separate traffic unit. It can only be set to true if value is empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#enable_each_unique_value GoogleComputeSecurityPolicy#enable_each_unique_value}
        :param value: Requests that match this value constitute a granular traffic unit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#value GoogleComputeSecurityPolicy#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65f2dc7b8aa667ede9ab58bd42dd90eebf61da0514b2ed5429739ee3f33d8faf)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#type GoogleComputeSecurityPolicy#type}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#enable_each_unique_value GoogleComputeSecurityPolicy#enable_each_unique_value}
        '''
        result = self._values.get("enable_each_unique_value")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Requests that match this value constitute a granular traffic unit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#value GoogleComputeSecurityPolicy#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8d15324a65e15f6c31f1ccd7fb7e89fb84bb04976acd80ca76ac95cb2c4b3b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db6f697cc5a10be9650e7d898ddf6fb6eb100945ca332899d2bcc28a8d67a405)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__266d14bf5b1fe31d968e8544f30c44fbe099b1b840946247363b510409783961)
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
            type_hints = typing.get_type_hints(_typecheckingstub__365991e21558633c8840d9e3c79e6b52d105d179c824842065842be7e8eeec8f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a95a107dc258eaff8f83e0403355df9022d26e558d97a2cecf739d7e29f0515)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2603af767830dd3f521a3e7cfac10acceae66ac9c6b86acb96fd5e6895f936ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1200e377e558e6f307fb3376e25e23ddca6cb24edc097f5cd7b47e39333507c9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0ec7891a72d5253123cbc266dd380409fb744eca94220ed562b931361f6f211)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableEachUniqueValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8117e9eb19f2aa8adf828c764b76d3a848b4e4121a0e8680586c277d8ed08f51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7585e8a68fb90d33b6b777c4ebc524363ab9e4fd425a0032d8a08bb72c8a4a83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f11434a16ad03f4d5de0532d7b7a5c6e48d2bdc9f33f65ef26f0623b14c2652)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeSecurityPolicyAdaptiveProtectionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyAdaptiveProtectionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4de4862fe71de53f8a8d6bceb5a9f0e531defedc1478c965d77be0bc9c6e5d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutoDeployConfig")
    def put_auto_deploy_config(
        self,
        *,
        confidence_threshold: typing.Optional[jsii.Number] = None,
        expiration_sec: typing.Optional[jsii.Number] = None,
        impacted_baseline_threshold: typing.Optional[jsii.Number] = None,
        load_threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param confidence_threshold: Rules are only automatically deployed for alerts on potential attacks with confidence scores greater than this threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#confidence_threshold GoogleComputeSecurityPolicy#confidence_threshold}
        :param expiration_sec: Google Cloud Armor stops applying the action in the automatically deployed rule to an identified attacker after this duration. The rule continues to operate against new requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#expiration_sec GoogleComputeSecurityPolicy#expiration_sec}
        :param impacted_baseline_threshold: Rules are only automatically deployed when the estimated impact to baseline traffic from the suggested mitigation is below this threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#impacted_baseline_threshold GoogleComputeSecurityPolicy#impacted_baseline_threshold}
        :param load_threshold: Identifies new attackers only when the load to the backend service that is under attack exceeds this threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#load_threshold GoogleComputeSecurityPolicy#load_threshold}
        '''
        value = GoogleComputeSecurityPolicyAdaptiveProtectionConfigAutoDeployConfig(
            confidence_threshold=confidence_threshold,
            expiration_sec=expiration_sec,
            impacted_baseline_threshold=impacted_baseline_threshold,
            load_threshold=load_threshold,
        )

        return typing.cast(None, jsii.invoke(self, "putAutoDeployConfig", [value]))

    @jsii.member(jsii_name="putLayer7DdosDefenseConfig")
    def put_layer7_ddos_defense_config(
        self,
        *,
        enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rule_visibility: typing.Optional[builtins.str] = None,
        threshold_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enable: If set to true, enables CAAP for L7 DDoS detection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#enable GoogleComputeSecurityPolicy#enable}
        :param rule_visibility: Rule visibility. Supported values include: "STANDARD", "PREMIUM". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#rule_visibility GoogleComputeSecurityPolicy#rule_visibility}
        :param threshold_configs: threshold_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#threshold_configs GoogleComputeSecurityPolicy#threshold_configs}
        '''
        value = GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig(
            enable=enable,
            rule_visibility=rule_visibility,
            threshold_configs=threshold_configs,
        )

        return typing.cast(None, jsii.invoke(self, "putLayer7DdosDefenseConfig", [value]))

    @jsii.member(jsii_name="resetAutoDeployConfig")
    def reset_auto_deploy_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoDeployConfig", []))

    @jsii.member(jsii_name="resetLayer7DdosDefenseConfig")
    def reset_layer7_ddos_defense_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLayer7DdosDefenseConfig", []))

    @builtins.property
    @jsii.member(jsii_name="autoDeployConfig")
    def auto_deploy_config(
        self,
    ) -> GoogleComputeSecurityPolicyAdaptiveProtectionConfigAutoDeployConfigOutputReference:
        return typing.cast(GoogleComputeSecurityPolicyAdaptiveProtectionConfigAutoDeployConfigOutputReference, jsii.get(self, "autoDeployConfig"))

    @builtins.property
    @jsii.member(jsii_name="layer7DdosDefenseConfig")
    def layer7_ddos_defense_config(
        self,
    ) -> GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigOutputReference:
        return typing.cast(GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigOutputReference, jsii.get(self, "layer7DdosDefenseConfig"))

    @builtins.property
    @jsii.member(jsii_name="autoDeployConfigInput")
    def auto_deploy_config_input(
        self,
    ) -> typing.Optional[GoogleComputeSecurityPolicyAdaptiveProtectionConfigAutoDeployConfig]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyAdaptiveProtectionConfigAutoDeployConfig], jsii.get(self, "autoDeployConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="layer7DdosDefenseConfigInput")
    def layer7_ddos_defense_config_input(
        self,
    ) -> typing.Optional[GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig], jsii.get(self, "layer7DdosDefenseConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeSecurityPolicyAdaptiveProtectionConfig]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyAdaptiveProtectionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeSecurityPolicyAdaptiveProtectionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3ceb9ee5a4129460d66008195c3dafd334e2fc36dda0cccbedb3bf0bea2ba1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyAdvancedOptionsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "json_custom_config": "jsonCustomConfig",
        "json_parsing": "jsonParsing",
        "log_level": "logLevel",
        "user_ip_request_headers": "userIpRequestHeaders",
    },
)
class GoogleComputeSecurityPolicyAdvancedOptionsConfig:
    def __init__(
        self,
        *,
        json_custom_config: typing.Optional[typing.Union["GoogleComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        json_parsing: typing.Optional[builtins.str] = None,
        log_level: typing.Optional[builtins.str] = None,
        user_ip_request_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param json_custom_config: json_custom_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#json_custom_config GoogleComputeSecurityPolicy#json_custom_config}
        :param json_parsing: JSON body parsing. Supported values include: "DISABLED", "STANDARD". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#json_parsing GoogleComputeSecurityPolicy#json_parsing}
        :param log_level: Logging level. Supported values include: "NORMAL", "VERBOSE". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#log_level GoogleComputeSecurityPolicy#log_level}
        :param user_ip_request_headers: An optional list of case-insensitive request header names to use for resolving the callers client IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#user_ip_request_headers GoogleComputeSecurityPolicy#user_ip_request_headers}
        '''
        if isinstance(json_custom_config, dict):
            json_custom_config = GoogleComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfig(**json_custom_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d08e1b21aa07e83c12c3482555db70c56c5529e4ebacde9506d07134ccd49a2d)
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
    ) -> typing.Optional["GoogleComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfig"]:
        '''json_custom_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#json_custom_config GoogleComputeSecurityPolicy#json_custom_config}
        '''
        result = self._values.get("json_custom_config")
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfig"], result)

    @builtins.property
    def json_parsing(self) -> typing.Optional[builtins.str]:
        '''JSON body parsing. Supported values include: "DISABLED", "STANDARD".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#json_parsing GoogleComputeSecurityPolicy#json_parsing}
        '''
        result = self._values.get("json_parsing")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_level(self) -> typing.Optional[builtins.str]:
        '''Logging level. Supported values include: "NORMAL", "VERBOSE".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#log_level GoogleComputeSecurityPolicy#log_level}
        '''
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_ip_request_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An optional list of case-insensitive request header names to use for resolving the callers client IP address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#user_ip_request_headers GoogleComputeSecurityPolicy#user_ip_request_headers}
        '''
        result = self._values.get("user_ip_request_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyAdvancedOptionsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfig",
    jsii_struct_bases=[],
    name_mapping={"content_types": "contentTypes"},
)
class GoogleComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfig:
    def __init__(self, *, content_types: typing.Sequence[builtins.str]) -> None:
        '''
        :param content_types: A list of custom Content-Type header values to apply the JSON parsing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#content_types GoogleComputeSecurityPolicy#content_types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__979a982845e7c8b234d8c5bd4307b82cc6f28269b1fc39cd14c1e59cbcc525e2)
            check_type(argname="argument content_types", value=content_types, expected_type=type_hints["content_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content_types": content_types,
        }

    @builtins.property
    def content_types(self) -> typing.List[builtins.str]:
        '''A list of custom Content-Type header values to apply the JSON parsing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#content_types GoogleComputeSecurityPolicy#content_types}
        '''
        result = self._values.get("content_types")
        assert result is not None, "Required property 'content_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bc8b00a868e0f33831554ec0941d29edbe732a21ba7c0505188b3350d0c4841)
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
            type_hints = typing.get_type_hints(_typecheckingstub__515b4b6e8566a142cc38461449b131cea3804504026c26e3105caf34724a75ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfig]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d82f1004af00b3bc5412009922d96ef13424714db7add4fef7e74ee85efd309a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeSecurityPolicyAdvancedOptionsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyAdvancedOptionsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cbe0e1799b4ea99698e93f0704b11030c4d7680adc1f43d19e89dc70f80f8b37)
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
        :param content_types: A list of custom Content-Type header values to apply the JSON parsing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#content_types GoogleComputeSecurityPolicy#content_types}
        '''
        value = GoogleComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfig(
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
    ) -> GoogleComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfigOutputReference:
        return typing.cast(GoogleComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfigOutputReference, jsii.get(self, "jsonCustomConfig"))

    @builtins.property
    @jsii.member(jsii_name="jsonCustomConfigInput")
    def json_custom_config_input(
        self,
    ) -> typing.Optional[GoogleComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfig]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfig], jsii.get(self, "jsonCustomConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__aafec473825455b8b802ce94675b32bbcb65fccd8a8266c02e34fd43524440fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jsonParsing", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logLevel")
    def log_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logLevel"))

    @log_level.setter
    def log_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33eacee6aa1d0602453f47c78b887c11f78514d09967bca0608d0d944fa4e9be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userIpRequestHeaders")
    def user_ip_request_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "userIpRequestHeaders"))

    @user_ip_request_headers.setter
    def user_ip_request_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73fbb1c9ae571af11bdf44015f39f1e9f1294026ae96b6b878273cee691596b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userIpRequestHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeSecurityPolicyAdvancedOptionsConfig]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyAdvancedOptionsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeSecurityPolicyAdvancedOptionsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d88a6f7512f3f3d335212b703f6e47fc13d00efa61aad9fe793c44ac1f95eacd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyConfig",
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
class GoogleComputeSecurityPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        adaptive_protection_config: typing.Optional[typing.Union[GoogleComputeSecurityPolicyAdaptiveProtectionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        advanced_options_config: typing.Optional[typing.Union[GoogleComputeSecurityPolicyAdvancedOptionsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        recaptcha_options_config: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRecaptchaOptionsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeSecurityPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param name: The name of the security policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#name GoogleComputeSecurityPolicy#name}
        :param adaptive_protection_config: adaptive_protection_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#adaptive_protection_config GoogleComputeSecurityPolicy#adaptive_protection_config}
        :param advanced_options_config: advanced_options_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#advanced_options_config GoogleComputeSecurityPolicy#advanced_options_config}
        :param description: An optional description of this security policy. Max size is 2048. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#description GoogleComputeSecurityPolicy#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#id GoogleComputeSecurityPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: The project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#project GoogleComputeSecurityPolicy#project}
        :param recaptcha_options_config: recaptcha_options_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#recaptcha_options_config GoogleComputeSecurityPolicy#recaptcha_options_config}
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#rule GoogleComputeSecurityPolicy#rule}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#timeouts GoogleComputeSecurityPolicy#timeouts}
        :param type: The type indicates the intended use of the security policy. CLOUD_ARMOR - Cloud Armor backend security policies can be configured to filter incoming HTTP requests targeting backend services. They filter requests before they hit the origin servers. CLOUD_ARMOR_EDGE - Cloud Armor edge security policies can be configured to filter incoming HTTP requests targeting backend services (including Cloud CDN-enabled) as well as backend buckets (Cloud Storage). They filter requests before the request is served from Google's cache. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#type GoogleComputeSecurityPolicy#type}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(adaptive_protection_config, dict):
            adaptive_protection_config = GoogleComputeSecurityPolicyAdaptiveProtectionConfig(**adaptive_protection_config)
        if isinstance(advanced_options_config, dict):
            advanced_options_config = GoogleComputeSecurityPolicyAdvancedOptionsConfig(**advanced_options_config)
        if isinstance(recaptcha_options_config, dict):
            recaptcha_options_config = GoogleComputeSecurityPolicyRecaptchaOptionsConfig(**recaptcha_options_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleComputeSecurityPolicyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f94a14b5a30d02e46fd24a5a69aec67870e98e9e9d5b45192bfb3d0fd4ef7197)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#name GoogleComputeSecurityPolicy#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def adaptive_protection_config(
        self,
    ) -> typing.Optional[GoogleComputeSecurityPolicyAdaptiveProtectionConfig]:
        '''adaptive_protection_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#adaptive_protection_config GoogleComputeSecurityPolicy#adaptive_protection_config}
        '''
        result = self._values.get("adaptive_protection_config")
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyAdaptiveProtectionConfig], result)

    @builtins.property
    def advanced_options_config(
        self,
    ) -> typing.Optional[GoogleComputeSecurityPolicyAdvancedOptionsConfig]:
        '''advanced_options_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#advanced_options_config GoogleComputeSecurityPolicy#advanced_options_config}
        '''
        result = self._values.get("advanced_options_config")
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyAdvancedOptionsConfig], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this security policy. Max size is 2048.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#description GoogleComputeSecurityPolicy#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#id GoogleComputeSecurityPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The project in which the resource belongs. If it is not provided, the provider project is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#project GoogleComputeSecurityPolicy#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recaptcha_options_config(
        self,
    ) -> typing.Optional["GoogleComputeSecurityPolicyRecaptchaOptionsConfig"]:
        '''recaptcha_options_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#recaptcha_options_config GoogleComputeSecurityPolicy#recaptcha_options_config}
        '''
        result = self._values.get("recaptcha_options_config")
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRecaptchaOptionsConfig"], result)

    @builtins.property
    def rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRule"]]]:
        '''rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#rule GoogleComputeSecurityPolicy#rule}
        '''
        result = self._values.get("rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRule"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleComputeSecurityPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#timeouts GoogleComputeSecurityPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyTimeouts"], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type indicates the intended use of the security policy.

        CLOUD_ARMOR - Cloud Armor backend security policies can be configured to filter incoming HTTP requests targeting backend services. They filter requests before they hit the origin servers. CLOUD_ARMOR_EDGE - Cloud Armor edge security policies can be configured to filter incoming HTTP requests targeting backend services (including Cloud CDN-enabled) as well as backend buckets (Cloud Storage). They filter requests before the request is served from Google's cache.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#type GoogleComputeSecurityPolicy#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRecaptchaOptionsConfig",
    jsii_struct_bases=[],
    name_mapping={"redirect_site_key": "redirectSiteKey"},
)
class GoogleComputeSecurityPolicyRecaptchaOptionsConfig:
    def __init__(self, *, redirect_site_key: builtins.str) -> None:
        '''
        :param redirect_site_key: A field to supply a reCAPTCHA site key to be used for all the rules using the redirect action with the type of GOOGLE_RECAPTCHA under the security policy. The specified site key needs to be created from the reCAPTCHA API. The user is responsible for the validity of the specified site key. If not specified, a Google-managed site key is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#redirect_site_key GoogleComputeSecurityPolicy#redirect_site_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d07cd13260fe19a18e5736a8014d3fb646b1f95586c7c991268002efaa1cefe)
            check_type(argname="argument redirect_site_key", value=redirect_site_key, expected_type=type_hints["redirect_site_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "redirect_site_key": redirect_site_key,
        }

    @builtins.property
    def redirect_site_key(self) -> builtins.str:
        '''A field to supply a reCAPTCHA site key to be used for all the rules using the redirect action with the type of GOOGLE_RECAPTCHA under the security policy.

        The specified site key needs to be created from the reCAPTCHA API. The user is responsible for the validity of the specified site key. If not specified, a Google-managed site key is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#redirect_site_key GoogleComputeSecurityPolicy#redirect_site_key}
        '''
        result = self._values.get("redirect_site_key")
        assert result is not None, "Required property 'redirect_site_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRecaptchaOptionsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyRecaptchaOptionsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRecaptchaOptionsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4e2861f9f0cc8301bb1a018423d890ba94816d768e097b1970262682bbeca24)
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
            type_hints = typing.get_type_hints(_typecheckingstub__730768aba2ea22e04197a3aac784d732cd78141b8933681525b090c4364cf36e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectSiteKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeSecurityPolicyRecaptchaOptionsConfig]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyRecaptchaOptionsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeSecurityPolicyRecaptchaOptionsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba936aff49894da7c1bf7819b1672c2fb28e1dffbf3a833ddc3b27c6de690b94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRule",
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
class GoogleComputeSecurityPolicyRule:
    def __init__(
        self,
        *,
        action: builtins.str,
        match: typing.Union["GoogleComputeSecurityPolicyRuleMatch", typing.Dict[builtins.str, typing.Any]],
        priority: jsii.Number,
        description: typing.Optional[builtins.str] = None,
        header_action: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRuleHeaderAction", typing.Dict[builtins.str, typing.Any]]] = None,
        preconfigured_waf_config: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRulePreconfiguredWafConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        preview: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rate_limit_options: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRuleRateLimitOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        redirect_options: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRuleRedirectOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param action: Action to take when match matches the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#action GoogleComputeSecurityPolicy#action}
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#match GoogleComputeSecurityPolicy#match}
        :param priority: An unique positive integer indicating the priority of evaluation for a rule. Rules are evaluated from highest priority (lowest numerically) to lowest priority (highest numerically) in order. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#priority GoogleComputeSecurityPolicy#priority}
        :param description: An optional description of this rule. Max size is 64. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#description GoogleComputeSecurityPolicy#description}
        :param header_action: header_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#header_action GoogleComputeSecurityPolicy#header_action}
        :param preconfigured_waf_config: preconfigured_waf_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#preconfigured_waf_config GoogleComputeSecurityPolicy#preconfigured_waf_config}
        :param preview: When set to true, the action specified above is not enforced. Stackdriver logs for requests that trigger a preview action are annotated as such. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#preview GoogleComputeSecurityPolicy#preview}
        :param rate_limit_options: rate_limit_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#rate_limit_options GoogleComputeSecurityPolicy#rate_limit_options}
        :param redirect_options: redirect_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#redirect_options GoogleComputeSecurityPolicy#redirect_options}
        '''
        if isinstance(match, dict):
            match = GoogleComputeSecurityPolicyRuleMatch(**match)
        if isinstance(header_action, dict):
            header_action = GoogleComputeSecurityPolicyRuleHeaderAction(**header_action)
        if isinstance(preconfigured_waf_config, dict):
            preconfigured_waf_config = GoogleComputeSecurityPolicyRulePreconfiguredWafConfig(**preconfigured_waf_config)
        if isinstance(rate_limit_options, dict):
            rate_limit_options = GoogleComputeSecurityPolicyRuleRateLimitOptions(**rate_limit_options)
        if isinstance(redirect_options, dict):
            redirect_options = GoogleComputeSecurityPolicyRuleRedirectOptions(**redirect_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abcfa6af206f57a464098d5caf35404e7c2e8b1403f6ffcc325760875350dafc)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#action GoogleComputeSecurityPolicy#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def match(self) -> "GoogleComputeSecurityPolicyRuleMatch":
        '''match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#match GoogleComputeSecurityPolicy#match}
        '''
        result = self._values.get("match")
        assert result is not None, "Required property 'match' is missing"
        return typing.cast("GoogleComputeSecurityPolicyRuleMatch", result)

    @builtins.property
    def priority(self) -> jsii.Number:
        '''An unique positive integer indicating the priority of evaluation for a rule.

        Rules are evaluated from highest priority (lowest numerically) to lowest priority (highest numerically) in order.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#priority GoogleComputeSecurityPolicy#priority}
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this rule. Max size is 64.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#description GoogleComputeSecurityPolicy#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def header_action(
        self,
    ) -> typing.Optional["GoogleComputeSecurityPolicyRuleHeaderAction"]:
        '''header_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#header_action GoogleComputeSecurityPolicy#header_action}
        '''
        result = self._values.get("header_action")
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRuleHeaderAction"], result)

    @builtins.property
    def preconfigured_waf_config(
        self,
    ) -> typing.Optional["GoogleComputeSecurityPolicyRulePreconfiguredWafConfig"]:
        '''preconfigured_waf_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#preconfigured_waf_config GoogleComputeSecurityPolicy#preconfigured_waf_config}
        '''
        result = self._values.get("preconfigured_waf_config")
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRulePreconfiguredWafConfig"], result)

    @builtins.property
    def preview(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When set to true, the action specified above is not enforced.

        Stackdriver logs for requests that trigger a preview action are annotated as such.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#preview GoogleComputeSecurityPolicy#preview}
        '''
        result = self._values.get("preview")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def rate_limit_options(
        self,
    ) -> typing.Optional["GoogleComputeSecurityPolicyRuleRateLimitOptions"]:
        '''rate_limit_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#rate_limit_options GoogleComputeSecurityPolicy#rate_limit_options}
        '''
        result = self._values.get("rate_limit_options")
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRuleRateLimitOptions"], result)

    @builtins.property
    def redirect_options(
        self,
    ) -> typing.Optional["GoogleComputeSecurityPolicyRuleRedirectOptions"]:
        '''redirect_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#redirect_options GoogleComputeSecurityPolicy#redirect_options}
        '''
        result = self._values.get("redirect_options")
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRuleRedirectOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRuleHeaderAction",
    jsii_struct_bases=[],
    name_mapping={"request_headers_to_adds": "requestHeadersToAdds"},
)
class GoogleComputeSecurityPolicyRuleHeaderAction:
    def __init__(
        self,
        *,
        request_headers_to_adds: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param request_headers_to_adds: request_headers_to_adds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#request_headers_to_adds GoogleComputeSecurityPolicy#request_headers_to_adds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5da920f72ed90831dc957cc807d18e2f9723fd74c9a630aea324d97e0246963)
            check_type(argname="argument request_headers_to_adds", value=request_headers_to_adds, expected_type=type_hints["request_headers_to_adds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "request_headers_to_adds": request_headers_to_adds,
        }

    @builtins.property
    def request_headers_to_adds(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds"]]:
        '''request_headers_to_adds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#request_headers_to_adds GoogleComputeSecurityPolicy#request_headers_to_adds}
        '''
        result = self._values.get("request_headers_to_adds")
        assert result is not None, "Required property 'request_headers_to_adds' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRuleHeaderAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyRuleHeaderActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRuleHeaderActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d441994c2bae89150655c6763c2499777eabe23760577ab8ae9bd20ae39707d1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRequestHeadersToAdds")
    def put_request_headers_to_adds(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccc37b1b522c966d5867a33e04a147d248b89a189aa145fee2a8f4ddb4e6159b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestHeadersToAdds", [value]))

    @builtins.property
    @jsii.member(jsii_name="requestHeadersToAdds")
    def request_headers_to_adds(
        self,
    ) -> "GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsList":
        return typing.cast("GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsList", jsii.get(self, "requestHeadersToAdds"))

    @builtins.property
    @jsii.member(jsii_name="requestHeadersToAddsInput")
    def request_headers_to_adds_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds"]]], jsii.get(self, "requestHeadersToAddsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeSecurityPolicyRuleHeaderAction]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyRuleHeaderAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeSecurityPolicyRuleHeaderAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df8a552d4f9f4b647b61dc6c22f83d1402e2dd2a621b25ef544baa6edcf7a831)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds",
    jsii_struct_bases=[],
    name_mapping={"header_name": "headerName", "header_value": "headerValue"},
)
class GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds:
    def __init__(
        self,
        *,
        header_name: builtins.str,
        header_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param header_name: The name of the header to set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#header_name GoogleComputeSecurityPolicy#header_name}
        :param header_value: The value to set the named header to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#header_value GoogleComputeSecurityPolicy#header_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3329dcde84146078ed8c76c010ace4bfce84d4a2e7a01ef61bfc9839eff89ff)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#header_name GoogleComputeSecurityPolicy#header_name}
        '''
        result = self._values.get("header_name")
        assert result is not None, "Required property 'header_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def header_value(self) -> typing.Optional[builtins.str]:
        '''The value to set the named header to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#header_value GoogleComputeSecurityPolicy#header_value}
        '''
        result = self._values.get("header_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ef944215780ebf3a0e562df2041163d1a749f6e414b7d9c3207b2d0ec9a6350)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46425823e6c9f9d68fb99d13dbfbfbfce918acdf9aa0e294be02765b3bf35e63)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9f926cf5df3c921316c71be7dfeb2ee76a3da3b83e71e40cb277537a9360365)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cad8a4f3077a054b255cdb89e70e7fe5f9295dab1658913fdaecb6c3b6543a66)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5f77f941568c54a6f5dca3b58cabf55c1a0eeb82cfb0c53ae81946ac722a5dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7315344c024e362e7d0dae04f87a18d9b6dd5ae9560c9b5401620d7e2addc699)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__15e8a2a5368c6010431c57961d3dfa06c8a6f29e30a2837bf915d3baf3dbac28)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c407700bc2f730bd581620d1092565afaf2b3680350305cdc4702aa07cf949c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headerValue")
    def header_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerValue"))

    @header_value.setter
    def header_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6db60d9c8f4562c2940f9ebbc98d22ae960d7695401a479e81c964b507c85125)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30758ed5067e492ded8e5f3999e3fe1693aa1196177d6b8799c45b73205e0276)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeSecurityPolicyRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__12b14466b9772aa9043eb5de6cda463fc491ab2e6667a953fbed94f754133c53)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeSecurityPolicyRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08d140dff9d37026d4ae9832bfae4966146bf090160ab8c1f8b5fd2490d4f770)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeSecurityPolicyRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__debfc15b0e99eb08b287740961e59d2b16f6211f750fdf00940bffb4b03d6fd7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__79cafc75f9429257f81a381c261ec1a75eca7b9fc0d5784afbd14b281bd35a6c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__67b78893a1758b9a265e8378cbb683d3fd651261ccd66d355d988d47d287f791)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1711dd7340a30d4e7a49fdcc2190c898f7ede92ddf0362c612a851afa8993c86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRuleMatch",
    jsii_struct_bases=[],
    name_mapping={
        "config": "config",
        "expr": "expr",
        "expr_options": "exprOptions",
        "versioned_expr": "versionedExpr",
    },
)
class GoogleComputeSecurityPolicyRuleMatch:
    def __init__(
        self,
        *,
        config: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRuleMatchConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        expr: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRuleMatchExpr", typing.Dict[builtins.str, typing.Any]]] = None,
        expr_options: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRuleMatchExprOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        versioned_expr: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#config GoogleComputeSecurityPolicy#config}
        :param expr: expr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#expr GoogleComputeSecurityPolicy#expr}
        :param expr_options: expr_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#expr_options GoogleComputeSecurityPolicy#expr_options}
        :param versioned_expr: Predefined rule expression. If this field is specified, config must also be specified. Available options: SRC_IPS_V1: Must specify the corresponding src_ip_ranges field in config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#versioned_expr GoogleComputeSecurityPolicy#versioned_expr}
        '''
        if isinstance(config, dict):
            config = GoogleComputeSecurityPolicyRuleMatchConfig(**config)
        if isinstance(expr, dict):
            expr = GoogleComputeSecurityPolicyRuleMatchExpr(**expr)
        if isinstance(expr_options, dict):
            expr_options = GoogleComputeSecurityPolicyRuleMatchExprOptions(**expr_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c21af780107c072c9dc5f33f4b40fa1772387e904f273558e9d2ad571e1f738)
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
    def config(self) -> typing.Optional["GoogleComputeSecurityPolicyRuleMatchConfig"]:
        '''config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#config GoogleComputeSecurityPolicy#config}
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRuleMatchConfig"], result)

    @builtins.property
    def expr(self) -> typing.Optional["GoogleComputeSecurityPolicyRuleMatchExpr"]:
        '''expr block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#expr GoogleComputeSecurityPolicy#expr}
        '''
        result = self._values.get("expr")
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRuleMatchExpr"], result)

    @builtins.property
    def expr_options(
        self,
    ) -> typing.Optional["GoogleComputeSecurityPolicyRuleMatchExprOptions"]:
        '''expr_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#expr_options GoogleComputeSecurityPolicy#expr_options}
        '''
        result = self._values.get("expr_options")
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRuleMatchExprOptions"], result)

    @builtins.property
    def versioned_expr(self) -> typing.Optional[builtins.str]:
        '''Predefined rule expression.

        If this field is specified, config must also be specified. Available options:   SRC_IPS_V1: Must specify the corresponding src_ip_ranges field in config.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#versioned_expr GoogleComputeSecurityPolicy#versioned_expr}
        '''
        result = self._values.get("versioned_expr")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRuleMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRuleMatchConfig",
    jsii_struct_bases=[],
    name_mapping={"src_ip_ranges": "srcIpRanges"},
)
class GoogleComputeSecurityPolicyRuleMatchConfig:
    def __init__(self, *, src_ip_ranges: typing.Sequence[builtins.str]) -> None:
        '''
        :param src_ip_ranges: Set of IP addresses or ranges (IPV4 or IPV6) in CIDR notation to match against inbound traffic. There is a limit of 10 IP ranges per rule. A value of '*' matches all IPs (can be used to override the default behavior). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#src_ip_ranges GoogleComputeSecurityPolicy#src_ip_ranges}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04ba0095e022217308d00a45fa46d98738cb824f7f8a02f94745b1f839801bbf)
            check_type(argname="argument src_ip_ranges", value=src_ip_ranges, expected_type=type_hints["src_ip_ranges"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "src_ip_ranges": src_ip_ranges,
        }

    @builtins.property
    def src_ip_ranges(self) -> typing.List[builtins.str]:
        '''Set of IP addresses or ranges (IPV4 or IPV6) in CIDR notation to match against inbound traffic.

        There is a limit of 10 IP ranges per rule. A value of '*' matches all IPs (can be used to override the default behavior).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#src_ip_ranges GoogleComputeSecurityPolicy#src_ip_ranges}
        '''
        result = self._values.get("src_ip_ranges")
        assert result is not None, "Required property 'src_ip_ranges' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRuleMatchConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyRuleMatchConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRuleMatchConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3075ad5f2c2a1a84b79221ccf69322f7f10422cf34a026f6c4a2c15833711b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa0ff852250c7db9365809e666156841f18416eaf0a0391e124846f741dad9b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcIpRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeSecurityPolicyRuleMatchConfig]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyRuleMatchConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeSecurityPolicyRuleMatchConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ea6fd84ff2c1867cf43100e38588a64bc226264f0681a10f1874e68ab9f9490)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRuleMatchExpr",
    jsii_struct_bases=[],
    name_mapping={"expression": "expression"},
)
class GoogleComputeSecurityPolicyRuleMatchExpr:
    def __init__(self, *, expression: builtins.str) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. The application context of the containing message determines which well-known feature set of CEL is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#expression GoogleComputeSecurityPolicy#expression}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af0af65207d2b36fb903b34a971a88cc7988cce0feab65ffef71b19c847e99cb)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "expression": expression,
        }

    @builtins.property
    def expression(self) -> builtins.str:
        '''Textual representation of an expression in Common Expression Language syntax.

        The application context of the containing message determines which well-known feature set of CEL is supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#expression GoogleComputeSecurityPolicy#expression}
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRuleMatchExpr(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRuleMatchExprOptions",
    jsii_struct_bases=[],
    name_mapping={"recaptcha_options": "recaptchaOptions"},
)
class GoogleComputeSecurityPolicyRuleMatchExprOptions:
    def __init__(
        self,
        *,
        recaptcha_options: typing.Union["GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptions", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param recaptcha_options: recaptcha_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#recaptcha_options GoogleComputeSecurityPolicy#recaptcha_options}
        '''
        if isinstance(recaptcha_options, dict):
            recaptcha_options = GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptions(**recaptcha_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70d1457febdc9e144aeefa0adab72086c9a724af5ad9255e40264cbed39c6846)
            check_type(argname="argument recaptcha_options", value=recaptcha_options, expected_type=type_hints["recaptcha_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "recaptcha_options": recaptcha_options,
        }

    @builtins.property
    def recaptcha_options(
        self,
    ) -> "GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptions":
        '''recaptcha_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#recaptcha_options GoogleComputeSecurityPolicy#recaptcha_options}
        '''
        result = self._values.get("recaptcha_options")
        assert result is not None, "Required property 'recaptcha_options' is missing"
        return typing.cast("GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptions", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRuleMatchExprOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyRuleMatchExprOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRuleMatchExprOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a8d32584107bbb90d3e45778ead0153e3a941198aa840c26cc36da887338c37)
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
        :param action_token_site_keys: A list of site keys to be used during the validation of reCAPTCHA action-tokens. The provided site keys need to be created from reCAPTCHA API under the same project where the security policy is created Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#action_token_site_keys GoogleComputeSecurityPolicy#action_token_site_keys}
        :param session_token_site_keys: A list of site keys to be used during the validation of reCAPTCHA session-tokens. The provided site keys need to be created from reCAPTCHA API under the same project where the security policy is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#session_token_site_keys GoogleComputeSecurityPolicy#session_token_site_keys}
        '''
        value = GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptions(
            action_token_site_keys=action_token_site_keys,
            session_token_site_keys=session_token_site_keys,
        )

        return typing.cast(None, jsii.invoke(self, "putRecaptchaOptions", [value]))

    @builtins.property
    @jsii.member(jsii_name="recaptchaOptions")
    def recaptcha_options(
        self,
    ) -> "GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsOutputReference":
        return typing.cast("GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsOutputReference", jsii.get(self, "recaptchaOptions"))

    @builtins.property
    @jsii.member(jsii_name="recaptchaOptionsInput")
    def recaptcha_options_input(
        self,
    ) -> typing.Optional["GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptions"]:
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptions"], jsii.get(self, "recaptchaOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeSecurityPolicyRuleMatchExprOptions]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyRuleMatchExprOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeSecurityPolicyRuleMatchExprOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a575a85cf6e483dafb7eb651cf9cfa3a5c14b55b2ca16577efc6d9aed4ad56ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptions",
    jsii_struct_bases=[],
    name_mapping={
        "action_token_site_keys": "actionTokenSiteKeys",
        "session_token_site_keys": "sessionTokenSiteKeys",
    },
)
class GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptions:
    def __init__(
        self,
        *,
        action_token_site_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        session_token_site_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param action_token_site_keys: A list of site keys to be used during the validation of reCAPTCHA action-tokens. The provided site keys need to be created from reCAPTCHA API under the same project where the security policy is created Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#action_token_site_keys GoogleComputeSecurityPolicy#action_token_site_keys}
        :param session_token_site_keys: A list of site keys to be used during the validation of reCAPTCHA session-tokens. The provided site keys need to be created from reCAPTCHA API under the same project where the security policy is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#session_token_site_keys GoogleComputeSecurityPolicy#session_token_site_keys}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76d7f396001dd3bb52d45a14c94312b17ae0345ca149ee385e27fe8bef3a3fe3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#action_token_site_keys GoogleComputeSecurityPolicy#action_token_site_keys}
        '''
        result = self._values.get("action_token_site_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def session_token_site_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of site keys to be used during the validation of reCAPTCHA session-tokens.

        The provided site keys need to be created from reCAPTCHA API under the same project where the security policy is created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#session_token_site_keys GoogleComputeSecurityPolicy#session_token_site_keys}
        '''
        result = self._values.get("session_token_site_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f16c9f199557884ad4ca93589a05a3d26076a8cbee5f064f549518cfe2725af8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__581aec377c5564f108875964de64729054598e23a2eee6b7c6b87b6e992713a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionTokenSiteKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionTokenSiteKeys")
    def session_token_site_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sessionTokenSiteKeys"))

    @session_token_site_keys.setter
    def session_token_site_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba7996df80acbd539661efa1716ce3ffa6b3c3744ccfbd4edeb159c2a16b660c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionTokenSiteKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptions]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9cb7a6b3c6d3100b387b2b0faf067b504af3515339f31ad19cb282126a9a225)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeSecurityPolicyRuleMatchExprOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRuleMatchExprOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b91f49ec75ed996317e4e0f95ba5ebb1ac96cc60693a259991e6e30faadece9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea4ff4d5b27d892c0fccc291a2c0d0e01de08f87d32146e164fb0bce4e483edd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeSecurityPolicyRuleMatchExpr]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyRuleMatchExpr], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeSecurityPolicyRuleMatchExpr],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8f30af3987a016697d5d41039ce5518eed9a64ccb709db94486c6601402bedb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeSecurityPolicyRuleMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRuleMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5a301cf202e61ab89c21a83226ba20e7eea4f41b4571763c6f08f51efadb6d0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConfig")
    def put_config(self, *, src_ip_ranges: typing.Sequence[builtins.str]) -> None:
        '''
        :param src_ip_ranges: Set of IP addresses or ranges (IPV4 or IPV6) in CIDR notation to match against inbound traffic. There is a limit of 10 IP ranges per rule. A value of '*' matches all IPs (can be used to override the default behavior). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#src_ip_ranges GoogleComputeSecurityPolicy#src_ip_ranges}
        '''
        value = GoogleComputeSecurityPolicyRuleMatchConfig(src_ip_ranges=src_ip_ranges)

        return typing.cast(None, jsii.invoke(self, "putConfig", [value]))

    @jsii.member(jsii_name="putExpr")
    def put_expr(self, *, expression: builtins.str) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. The application context of the containing message determines which well-known feature set of CEL is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#expression GoogleComputeSecurityPolicy#expression}
        '''
        value = GoogleComputeSecurityPolicyRuleMatchExpr(expression=expression)

        return typing.cast(None, jsii.invoke(self, "putExpr", [value]))

    @jsii.member(jsii_name="putExprOptions")
    def put_expr_options(
        self,
        *,
        recaptcha_options: typing.Union[GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptions, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param recaptcha_options: recaptcha_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#recaptcha_options GoogleComputeSecurityPolicy#recaptcha_options}
        '''
        value = GoogleComputeSecurityPolicyRuleMatchExprOptions(
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
    def config(self) -> GoogleComputeSecurityPolicyRuleMatchConfigOutputReference:
        return typing.cast(GoogleComputeSecurityPolicyRuleMatchConfigOutputReference, jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="expr")
    def expr(self) -> GoogleComputeSecurityPolicyRuleMatchExprOutputReference:
        return typing.cast(GoogleComputeSecurityPolicyRuleMatchExprOutputReference, jsii.get(self, "expr"))

    @builtins.property
    @jsii.member(jsii_name="exprOptions")
    def expr_options(
        self,
    ) -> GoogleComputeSecurityPolicyRuleMatchExprOptionsOutputReference:
        return typing.cast(GoogleComputeSecurityPolicyRuleMatchExprOptionsOutputReference, jsii.get(self, "exprOptions"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(
        self,
    ) -> typing.Optional[GoogleComputeSecurityPolicyRuleMatchConfig]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyRuleMatchConfig], jsii.get(self, "configInput"))

    @builtins.property
    @jsii.member(jsii_name="exprInput")
    def expr_input(self) -> typing.Optional[GoogleComputeSecurityPolicyRuleMatchExpr]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyRuleMatchExpr], jsii.get(self, "exprInput"))

    @builtins.property
    @jsii.member(jsii_name="exprOptionsInput")
    def expr_options_input(
        self,
    ) -> typing.Optional[GoogleComputeSecurityPolicyRuleMatchExprOptions]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyRuleMatchExprOptions], jsii.get(self, "exprOptionsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__f1ad32435cf1d5625eb86b9fab5ecaf24221b2958fe1d9f7dd5c776ef635e921)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionedExpr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleComputeSecurityPolicyRuleMatch]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyRuleMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeSecurityPolicyRuleMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db37ccde8887c16a16b511862af60cb4a46d7bf7dd7cab07c36df0c160b8c25f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeSecurityPolicyRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b2303cfddf8901d1bf1a6bf56f1fabbc003302cfd12de03dc6db6729c46c191)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHeaderAction")
    def put_header_action(
        self,
        *,
        request_headers_to_adds: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param request_headers_to_adds: request_headers_to_adds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#request_headers_to_adds GoogleComputeSecurityPolicy#request_headers_to_adds}
        '''
        value = GoogleComputeSecurityPolicyRuleHeaderAction(
            request_headers_to_adds=request_headers_to_adds
        )

        return typing.cast(None, jsii.invoke(self, "putHeaderAction", [value]))

    @jsii.member(jsii_name="putMatch")
    def put_match(
        self,
        *,
        config: typing.Optional[typing.Union[GoogleComputeSecurityPolicyRuleMatchConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        expr: typing.Optional[typing.Union[GoogleComputeSecurityPolicyRuleMatchExpr, typing.Dict[builtins.str, typing.Any]]] = None,
        expr_options: typing.Optional[typing.Union[GoogleComputeSecurityPolicyRuleMatchExprOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        versioned_expr: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#config GoogleComputeSecurityPolicy#config}
        :param expr: expr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#expr GoogleComputeSecurityPolicy#expr}
        :param expr_options: expr_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#expr_options GoogleComputeSecurityPolicy#expr_options}
        :param versioned_expr: Predefined rule expression. If this field is specified, config must also be specified. Available options: SRC_IPS_V1: Must specify the corresponding src_ip_ranges field in config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#versioned_expr GoogleComputeSecurityPolicy#versioned_expr}
        '''
        value = GoogleComputeSecurityPolicyRuleMatch(
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
        exclusion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusion", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param exclusion: exclusion block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#exclusion GoogleComputeSecurityPolicy#exclusion}
        '''
        value = GoogleComputeSecurityPolicyRulePreconfiguredWafConfig(
            exclusion=exclusion
        )

        return typing.cast(None, jsii.invoke(self, "putPreconfiguredWafConfig", [value]))

    @jsii.member(jsii_name="putRateLimitOptions")
    def put_rate_limit_options(
        self,
        *,
        conform_action: builtins.str,
        exceed_action: builtins.str,
        rate_limit_threshold: typing.Union["GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThreshold", typing.Dict[builtins.str, typing.Any]],
        ban_duration_sec: typing.Optional[jsii.Number] = None,
        ban_threshold: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThreshold", typing.Dict[builtins.str, typing.Any]]] = None,
        enforce_on_key: typing.Optional[builtins.str] = None,
        enforce_on_key_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enforce_on_key_name: typing.Optional[builtins.str] = None,
        exceed_redirect_options: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param conform_action: Action to take for requests that are under the configured rate limit threshold. Valid option is "allow" only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#conform_action GoogleComputeSecurityPolicy#conform_action}
        :param exceed_action: Action to take for requests that are above the configured rate limit threshold, to either deny with a specified HTTP response code, or redirect to a different endpoint. Valid options are "deny()" where valid values for status are 403, 404, 429, and 502, and "redirect" where the redirect parameters come from exceedRedirectOptions below. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#exceed_action GoogleComputeSecurityPolicy#exceed_action}
        :param rate_limit_threshold: rate_limit_threshold block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#rate_limit_threshold GoogleComputeSecurityPolicy#rate_limit_threshold}
        :param ban_duration_sec: Can only be specified if the action for the rule is "rate_based_ban". If specified, determines the time (in seconds) the traffic will continue to be banned by the rate limit after the rate falls below the threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#ban_duration_sec GoogleComputeSecurityPolicy#ban_duration_sec}
        :param ban_threshold: ban_threshold block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#ban_threshold GoogleComputeSecurityPolicy#ban_threshold}
        :param enforce_on_key: Determines the key to enforce the rateLimitThreshold on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#enforce_on_key GoogleComputeSecurityPolicy#enforce_on_key}
        :param enforce_on_key_configs: enforce_on_key_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#enforce_on_key_configs GoogleComputeSecurityPolicy#enforce_on_key_configs}
        :param enforce_on_key_name: Rate limit key name applicable only for the following key types: HTTP_HEADER -- Name of the HTTP header whose value is taken as the key value. HTTP_COOKIE -- Name of the HTTP cookie whose value is taken as the key value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#enforce_on_key_name GoogleComputeSecurityPolicy#enforce_on_key_name}
        :param exceed_redirect_options: exceed_redirect_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#exceed_redirect_options GoogleComputeSecurityPolicy#exceed_redirect_options}
        '''
        value = GoogleComputeSecurityPolicyRuleRateLimitOptions(
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
        :param type: Type of the redirect action. Available options: EXTERNAL_302: Must specify the corresponding target field in config. GOOGLE_RECAPTCHA: Cannot specify target field in config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#type GoogleComputeSecurityPolicy#type}
        :param target: Target for the redirect action. This is required if the type is EXTERNAL_302 and cannot be specified for GOOGLE_RECAPTCHA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#target GoogleComputeSecurityPolicy#target}
        '''
        value = GoogleComputeSecurityPolicyRuleRedirectOptions(
            type=type, target=target
        )

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
    def header_action(
        self,
    ) -> GoogleComputeSecurityPolicyRuleHeaderActionOutputReference:
        return typing.cast(GoogleComputeSecurityPolicyRuleHeaderActionOutputReference, jsii.get(self, "headerAction"))

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> GoogleComputeSecurityPolicyRuleMatchOutputReference:
        return typing.cast(GoogleComputeSecurityPolicyRuleMatchOutputReference, jsii.get(self, "match"))

    @builtins.property
    @jsii.member(jsii_name="preconfiguredWafConfig")
    def preconfigured_waf_config(
        self,
    ) -> "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigOutputReference":
        return typing.cast("GoogleComputeSecurityPolicyRulePreconfiguredWafConfigOutputReference", jsii.get(self, "preconfiguredWafConfig"))

    @builtins.property
    @jsii.member(jsii_name="rateLimitOptions")
    def rate_limit_options(
        self,
    ) -> "GoogleComputeSecurityPolicyRuleRateLimitOptionsOutputReference":
        return typing.cast("GoogleComputeSecurityPolicyRuleRateLimitOptionsOutputReference", jsii.get(self, "rateLimitOptions"))

    @builtins.property
    @jsii.member(jsii_name="redirectOptions")
    def redirect_options(
        self,
    ) -> "GoogleComputeSecurityPolicyRuleRedirectOptionsOutputReference":
        return typing.cast("GoogleComputeSecurityPolicyRuleRedirectOptionsOutputReference", jsii.get(self, "redirectOptions"))

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
    ) -> typing.Optional[GoogleComputeSecurityPolicyRuleHeaderAction]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyRuleHeaderAction], jsii.get(self, "headerActionInput"))

    @builtins.property
    @jsii.member(jsii_name="matchInput")
    def match_input(self) -> typing.Optional[GoogleComputeSecurityPolicyRuleMatch]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyRuleMatch], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="preconfiguredWafConfigInput")
    def preconfigured_waf_config_input(
        self,
    ) -> typing.Optional["GoogleComputeSecurityPolicyRulePreconfiguredWafConfig"]:
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRulePreconfiguredWafConfig"], jsii.get(self, "preconfiguredWafConfigInput"))

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
    ) -> typing.Optional["GoogleComputeSecurityPolicyRuleRateLimitOptions"]:
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRuleRateLimitOptions"], jsii.get(self, "rateLimitOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectOptionsInput")
    def redirect_options_input(
        self,
    ) -> typing.Optional["GoogleComputeSecurityPolicyRuleRedirectOptions"]:
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRuleRedirectOptions"], jsii.get(self, "redirectOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3f82f9661442dcd2b4a6f02f69945c951793ff9128054a441932a9ab7294855)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29d79d87d1d96a7c970055672bc5d73de83d83371446c1762b189e4979d91ede)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aaf6e774974c8dcb4eb6e373f96faf78972f3fcc822568cf49cb892bb381f2e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preview", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56016f8b58f8bb68bca5ebd25df7559aa8a3f4cdd8845572da4af7e7efafaddc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__230faa2e5d6bf63f5c661c9cc511e9f760001bc09b36f39f6d7f372511b9b494)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRulePreconfiguredWafConfig",
    jsii_struct_bases=[],
    name_mapping={"exclusion": "exclusion"},
)
class GoogleComputeSecurityPolicyRulePreconfiguredWafConfig:
    def __init__(
        self,
        *,
        exclusion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusion", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param exclusion: exclusion block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#exclusion GoogleComputeSecurityPolicy#exclusion}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a438bc303dfd9697392dd922ed1a27a86c9c2563bc23215dc431fb0c1c585543)
            check_type(argname="argument exclusion", value=exclusion, expected_type=type_hints["exclusion"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclusion is not None:
            self._values["exclusion"] = exclusion

    @builtins.property
    def exclusion(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusion"]]]:
        '''exclusion block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#exclusion GoogleComputeSecurityPolicy#exclusion}
        '''
        result = self._values.get("exclusion")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusion"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRulePreconfiguredWafConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusion",
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
class GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusion:
    def __init__(
        self,
        *,
        target_rule_set: builtins.str,
        request_cookie: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_query_param: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_uri: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_rule_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param target_rule_set: Target WAF rule set to apply the preconfigured WAF exclusion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#target_rule_set GoogleComputeSecurityPolicy#target_rule_set}
        :param request_cookie: request_cookie block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#request_cookie GoogleComputeSecurityPolicy#request_cookie}
        :param request_header: request_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#request_header GoogleComputeSecurityPolicy#request_header}
        :param request_query_param: request_query_param block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#request_query_param GoogleComputeSecurityPolicy#request_query_param}
        :param request_uri: request_uri block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#request_uri GoogleComputeSecurityPolicy#request_uri}
        :param target_rule_ids: A list of target rule IDs under the WAF rule set to apply the preconfigured WAF exclusion. If omitted, it refers to all the rule IDs under the WAF rule set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#target_rule_ids GoogleComputeSecurityPolicy#target_rule_ids}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f3278dfa6bcd504280d5b941c9a492c0038b56846f8dd0c8ad3bf4abae9dde2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#target_rule_set GoogleComputeSecurityPolicy#target_rule_set}
        '''
        result = self._values.get("target_rule_set")
        assert result is not None, "Required property 'target_rule_set' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def request_cookie(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie"]]]:
        '''request_cookie block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#request_cookie GoogleComputeSecurityPolicy#request_cookie}
        '''
        result = self._values.get("request_cookie")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie"]]], result)

    @builtins.property
    def request_header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader"]]]:
        '''request_header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#request_header GoogleComputeSecurityPolicy#request_header}
        '''
        result = self._values.get("request_header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader"]]], result)

    @builtins.property
    def request_query_param(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam"]]]:
        '''request_query_param block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#request_query_param GoogleComputeSecurityPolicy#request_query_param}
        '''
        result = self._values.get("request_query_param")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam"]]], result)

    @builtins.property
    def request_uri(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri"]]]:
        '''request_uri block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#request_uri GoogleComputeSecurityPolicy#request_uri}
        '''
        result = self._values.get("request_uri")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri"]]], result)

    @builtins.property
    def target_rule_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of target rule IDs under the WAF rule set to apply the preconfigured WAF exclusion.

        If omitted, it refers to all the rule IDs under the WAF rule set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#target_rule_ids GoogleComputeSecurityPolicy#target_rule_ids}
        '''
        result = self._values.get("target_rule_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e454804142d1055cfefa5a4c04a18fb1977fb4ba1bcaf68322b60c61c6e3bac4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad628ba34c70fb8b05648043f9c72110fa3a5f6159a812d59ae7d16e6193c291)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dacef77ec1e33230bc0416c6369d93aed28b0a4231819b491deae86711e36c73)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aeab7121295cf9e5d0325579f14ff0626670a4ab019f95843b154b878f19e4f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f39e2fbfc8dc8c9e95b81615b048b83634f903bd09b366a646c568478ecaa84f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusion]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusion]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusion]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1446af13c369360584df2d61d8a3e13a14c633ad869e184d42a8892c0b27542)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd9209795f94e7794a2e08429ec1b8d7e0cba58fa0184d634b48e7ad2b500cce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putRequestCookie")
    def put_request_cookie(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87a359c988150d836d65ddc9d7e74f0a2385d2ede2149dd65932dde1ab68eba3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestCookie", [value]))

    @jsii.member(jsii_name="putRequestHeader")
    def put_request_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__636e8aed5fb97968c783e358dbea343e0b0cde0253b7dd9777a5d455f05b3bbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestHeader", [value]))

    @jsii.member(jsii_name="putRequestQueryParam")
    def put_request_query_param(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39c4507265fd7c1f8e50e6c5e2c3139e4a54cf9ab1f12df4ca3296d691f8a72f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestQueryParam", [value]))

    @jsii.member(jsii_name="putRequestUri")
    def put_request_uri(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d4b2ffcb928723c323300690549c82813c6ce5875db5bd49af53bc925e04bbb)
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
    ) -> "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieList":
        return typing.cast("GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieList", jsii.get(self, "requestCookie"))

    @builtins.property
    @jsii.member(jsii_name="requestHeader")
    def request_header(
        self,
    ) -> "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderList":
        return typing.cast("GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderList", jsii.get(self, "requestHeader"))

    @builtins.property
    @jsii.member(jsii_name="requestQueryParam")
    def request_query_param(
        self,
    ) -> "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamList":
        return typing.cast("GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamList", jsii.get(self, "requestQueryParam"))

    @builtins.property
    @jsii.member(jsii_name="requestUri")
    def request_uri(
        self,
    ) -> "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriList":
        return typing.cast("GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriList", jsii.get(self, "requestUri"))

    @builtins.property
    @jsii.member(jsii_name="requestCookieInput")
    def request_cookie_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie"]]], jsii.get(self, "requestCookieInput"))

    @builtins.property
    @jsii.member(jsii_name="requestHeaderInput")
    def request_header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader"]]], jsii.get(self, "requestHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="requestQueryParamInput")
    def request_query_param_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam"]]], jsii.get(self, "requestQueryParamInput"))

    @builtins.property
    @jsii.member(jsii_name="requestUriInput")
    def request_uri_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri"]]], jsii.get(self, "requestUriInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__1ff4f105e378e1c5f863c01d9573a5e10f42b159f2d2f8694e40623f51c01adb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetRuleIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetRuleSet")
    def target_rule_set(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetRuleSet"))

    @target_rule_set.setter
    def target_rule_set(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ac896d73f9be8900150e93a1e21bc6f4489d06dd05a4907c860ec6d2e7e3c1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetRuleSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusion]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusion]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusion]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41b720dd05089a6d3f8b89709e312617282a47f9a29ed5009894ef266522c7b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "value": "value"},
)
class GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie:
    def __init__(
        self,
        *,
        operator: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operator: You can specify an exact match or a partial match by using a field operator and a field value. Available options: EQUALS: The operator matches if the field value equals the specified value. STARTS_WITH: The operator matches if the field value starts with the specified value. ENDS_WITH: The operator matches if the field value ends with the specified value. CONTAINS: The operator matches if the field value contains the specified value. EQUALS_ANY: The operator matches if the field value is any value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#operator GoogleComputeSecurityPolicy#operator}
        :param value: A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation. The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#value GoogleComputeSecurityPolicy#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__534a36ebca31702f7e450898fcb8188de0699721ce4be1886f5e66d9f20ef903)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#operator GoogleComputeSecurityPolicy#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation.

        The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#value GoogleComputeSecurityPolicy#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df0ac8b0577ce9a4d6c8147f9a3a00909c20b11cf4058e48b3aacbaf146d656e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d96487b2dc97e751640d89d730bb8a6199512eb18cfe83b8aec7aa405567ea2f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b26e4b23b005b728bcbfdeeeb5494a230420de84d81ca3a813bb578266389e9f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a61d7ea0af3cdd170ed553de4df0377756004bf295da6143b57320b49ff0e2c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__957983506659beb9756b3ebc15d7116d333038f09ade9f045e8bf8e61c2699fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4d85c8dc7bbeb2fc0e6a7d198c6130d6f9b4123731f8eceddafa5b9ddcd8d46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__36f2ec8ccd24cd6aaa4812d22959950e2711acf6eaa2a291760d2b619817f5bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__22093c6e7d34f7c911ab9e32f27603654c7d61a588250cbe4199e28dc89ba2e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e8d6d46ae1869fddc6482b4e3dbf40f0cfe67c681b8c5f720551ce7bf26912f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__474dc1b775d12a73b6e4f2d229b809da92ee477902c6e594d692e09dc5209c2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "value": "value"},
)
class GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader:
    def __init__(
        self,
        *,
        operator: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operator: You can specify an exact match or a partial match by using a field operator and a field value. Available options: EQUALS: The operator matches if the field value equals the specified value. STARTS_WITH: The operator matches if the field value starts with the specified value. ENDS_WITH: The operator matches if the field value ends with the specified value. CONTAINS: The operator matches if the field value contains the specified value. EQUALS_ANY: The operator matches if the field value is any value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#operator GoogleComputeSecurityPolicy#operator}
        :param value: A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation. The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#value GoogleComputeSecurityPolicy#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c1f82ee6561f7f2dc59c15ec07b7feb8dfff2372200cb16f8f6bf27be98bd3b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#operator GoogleComputeSecurityPolicy#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation.

        The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#value GoogleComputeSecurityPolicy#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__78ba9d36e4073137b23f5be8df39341965aa97bba0ddc58ac93b84d82299eba1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84b8104a78d84f7a5fc4554d32d52ff637f665301ca8c394b7f262ec5d4e4c9b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e332585d59ce27f2117a73be6d41bc8b2303bd5f51197cdf54ca0412c8c17c8b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e56e7f27cd7a521ddd7bb73e73c568d344cfcfd402d0c5d59c8ac277afb6a73)
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
            type_hints = typing.get_type_hints(_typecheckingstub__81741fb16315414ac97839b23c6a7b11f37c9c44b0da167ce776098afb19ba3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c84be9ee0b224e96f2ad99ef89ceda6fd3d69422e9c2f45d70a94735d68595fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__660fb38678e24ffb5d4276074ffb473f5e674157f121f19647fe7d1a47a237d5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8379a5297f67dab9682e7b40c3c2bf438809852d01e03af8ceb78e96a803d9c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c654bb9953424b0d2dee5ed647a362a4b93c506fa99d7e96ef1f72f27340f63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dae7381d26fc958bddae97319ce801b1bead1d4bd3eecb9fb66f1b336efc61d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "value": "value"},
)
class GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam:
    def __init__(
        self,
        *,
        operator: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operator: You can specify an exact match or a partial match by using a field operator and a field value. Available options: EQUALS: The operator matches if the field value equals the specified value. STARTS_WITH: The operator matches if the field value starts with the specified value. ENDS_WITH: The operator matches if the field value ends with the specified value. CONTAINS: The operator matches if the field value contains the specified value. EQUALS_ANY: The operator matches if the field value is any value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#operator GoogleComputeSecurityPolicy#operator}
        :param value: A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation. The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#value GoogleComputeSecurityPolicy#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f33c259cbcd1982862dcfe632e518cc3d5758f6ba1d3cd4817a21430cc99155)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#operator GoogleComputeSecurityPolicy#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation.

        The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#value GoogleComputeSecurityPolicy#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__714fc1f257c2dd4e0dcecaca4f8538889878a79c18ea0e8213cbb0db6cbb019e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1344b0d524a3c60c5da2d6b456be867ea1ac9f1faa4085efe8e44e9a1fdf6ed)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28be2054fc9b9859ccf49291ace04ce9e6253997aa28305d99ee6dd72d46e15c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__27aeadc0b1919b55d048fc8d3483f93408ed45956f2e236919b1e319a218b7a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8a07fccbfbc65b641ad9efd9ae8a17d5e86e5217b0e717faa30d8e3643bb529)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeea22e9686bcc04de62db647799afdad03753446e51c07c5f3a87f7aa0c3114)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fae45065f5a122fd317b4afa415c94f509c96e5f301b6e6adc2c6feb12a5791)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b58e90e196626c43c196bd75f50a4fe44ffc6da4fc1dc484a110bf7260bb71fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f773bf4fc2a11427936b1e9e04b5a782c5521ea35146ee8bcddfb4e1ee85fa9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ffd483de994ae7b984c66de1001b8d2063e8cb18f4e47096830cfcd9ca9797a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "value": "value"},
)
class GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri:
    def __init__(
        self,
        *,
        operator: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operator: You can specify an exact match or a partial match by using a field operator and a field value. Available options: EQUALS: The operator matches if the field value equals the specified value. STARTS_WITH: The operator matches if the field value starts with the specified value. ENDS_WITH: The operator matches if the field value ends with the specified value. CONTAINS: The operator matches if the field value contains the specified value. EQUALS_ANY: The operator matches if the field value is any value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#operator GoogleComputeSecurityPolicy#operator}
        :param value: A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation. The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#value GoogleComputeSecurityPolicy#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5a2792490abccde26248cd4fd216a5a033a027eb69f5183128bd918a7a80ace)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#operator GoogleComputeSecurityPolicy#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation.

        The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#value GoogleComputeSecurityPolicy#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b1cce0a4444f71efd0ead54f12014d2946f8ed09b5813cb288479c392a9f36a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ead12dcf804eeb1e9128d0a5975570f08cd866c8095eacad78ce6f45749d0463)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c890c0b4fd2122bcd185c9d9ea8241d69050d738f25b934aa74251c0bafe6679)
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
            type_hints = typing.get_type_hints(_typecheckingstub__02ddff115c45ab67106f265f744971a838996a71f5580cfdce3ee36a22299445)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c768b6bfec2aa4b9632218d6a3e152821427b66ce743654f1d42cf3de115c81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2eee321c157d54b2e00c484f249c239ecbfa8251db0f89d5c03993fb85fdc2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__841a7290f70cbd5d4e2c7a4b45111814604f990f1a288ffc60271c7db97085ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c2b5c3b72777dbad5c7491331df08d20c65b89a4519e85db83b8bb5ef21fb7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e47adade75302acb5c87efbdde29e1f50d19ca857d8d683a98099386066fe47f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc909dee9818049e6ba692001a0314c49e253cc5ce8a48881ab2b3228acd44b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeSecurityPolicyRulePreconfiguredWafConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRulePreconfiguredWafConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__83db2451b262456936b48e234be9fdc695050b1cae8dc8a4fd4d608a5dbbcebc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExclusion")
    def put_exclusion(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusion, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5082be1b73a03aa798d1368ceaffb70ebe2b3767c12dce515ab6d52b47f21f74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExclusion", [value]))

    @jsii.member(jsii_name="resetExclusion")
    def reset_exclusion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusion", []))

    @builtins.property
    @jsii.member(jsii_name="exclusion")
    def exclusion(
        self,
    ) -> GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionList:
        return typing.cast(GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionList, jsii.get(self, "exclusion"))

    @builtins.property
    @jsii.member(jsii_name="exclusionInput")
    def exclusion_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusion]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusion]]], jsii.get(self, "exclusionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeSecurityPolicyRulePreconfiguredWafConfig]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyRulePreconfiguredWafConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeSecurityPolicyRulePreconfiguredWafConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91ed987741a619465b58015289ee9be5e8978f0a69a072a78ce6c7e340f121b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRuleRateLimitOptions",
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
class GoogleComputeSecurityPolicyRuleRateLimitOptions:
    def __init__(
        self,
        *,
        conform_action: builtins.str,
        exceed_action: builtins.str,
        rate_limit_threshold: typing.Union["GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThreshold", typing.Dict[builtins.str, typing.Any]],
        ban_duration_sec: typing.Optional[jsii.Number] = None,
        ban_threshold: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThreshold", typing.Dict[builtins.str, typing.Any]]] = None,
        enforce_on_key: typing.Optional[builtins.str] = None,
        enforce_on_key_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enforce_on_key_name: typing.Optional[builtins.str] = None,
        exceed_redirect_options: typing.Optional[typing.Union["GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param conform_action: Action to take for requests that are under the configured rate limit threshold. Valid option is "allow" only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#conform_action GoogleComputeSecurityPolicy#conform_action}
        :param exceed_action: Action to take for requests that are above the configured rate limit threshold, to either deny with a specified HTTP response code, or redirect to a different endpoint. Valid options are "deny()" where valid values for status are 403, 404, 429, and 502, and "redirect" where the redirect parameters come from exceedRedirectOptions below. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#exceed_action GoogleComputeSecurityPolicy#exceed_action}
        :param rate_limit_threshold: rate_limit_threshold block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#rate_limit_threshold GoogleComputeSecurityPolicy#rate_limit_threshold}
        :param ban_duration_sec: Can only be specified if the action for the rule is "rate_based_ban". If specified, determines the time (in seconds) the traffic will continue to be banned by the rate limit after the rate falls below the threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#ban_duration_sec GoogleComputeSecurityPolicy#ban_duration_sec}
        :param ban_threshold: ban_threshold block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#ban_threshold GoogleComputeSecurityPolicy#ban_threshold}
        :param enforce_on_key: Determines the key to enforce the rateLimitThreshold on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#enforce_on_key GoogleComputeSecurityPolicy#enforce_on_key}
        :param enforce_on_key_configs: enforce_on_key_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#enforce_on_key_configs GoogleComputeSecurityPolicy#enforce_on_key_configs}
        :param enforce_on_key_name: Rate limit key name applicable only for the following key types: HTTP_HEADER -- Name of the HTTP header whose value is taken as the key value. HTTP_COOKIE -- Name of the HTTP cookie whose value is taken as the key value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#enforce_on_key_name GoogleComputeSecurityPolicy#enforce_on_key_name}
        :param exceed_redirect_options: exceed_redirect_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#exceed_redirect_options GoogleComputeSecurityPolicy#exceed_redirect_options}
        '''
        if isinstance(rate_limit_threshold, dict):
            rate_limit_threshold = GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThreshold(**rate_limit_threshold)
        if isinstance(ban_threshold, dict):
            ban_threshold = GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThreshold(**ban_threshold)
        if isinstance(exceed_redirect_options, dict):
            exceed_redirect_options = GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptions(**exceed_redirect_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bddb22cba872f779e2bb6162c2413c6f6b2a00c7591f832dc0de1f79ef70a2ac)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#conform_action GoogleComputeSecurityPolicy#conform_action}
        '''
        result = self._values.get("conform_action")
        assert result is not None, "Required property 'conform_action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def exceed_action(self) -> builtins.str:
        '''Action to take for requests that are above the configured rate limit threshold, to either deny with a specified HTTP response code, or redirect to a different endpoint.

        Valid options are "deny()" where valid values for status are 403, 404, 429, and 502, and "redirect" where the redirect parameters come from exceedRedirectOptions below.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#exceed_action GoogleComputeSecurityPolicy#exceed_action}
        '''
        result = self._values.get("exceed_action")
        assert result is not None, "Required property 'exceed_action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rate_limit_threshold(
        self,
    ) -> "GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThreshold":
        '''rate_limit_threshold block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#rate_limit_threshold GoogleComputeSecurityPolicy#rate_limit_threshold}
        '''
        result = self._values.get("rate_limit_threshold")
        assert result is not None, "Required property 'rate_limit_threshold' is missing"
        return typing.cast("GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThreshold", result)

    @builtins.property
    def ban_duration_sec(self) -> typing.Optional[jsii.Number]:
        '''Can only be specified if the action for the rule is "rate_based_ban".

        If specified, determines the time (in seconds) the traffic will continue to be banned by the rate limit after the rate falls below the threshold.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#ban_duration_sec GoogleComputeSecurityPolicy#ban_duration_sec}
        '''
        result = self._values.get("ban_duration_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ban_threshold(
        self,
    ) -> typing.Optional["GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThreshold"]:
        '''ban_threshold block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#ban_threshold GoogleComputeSecurityPolicy#ban_threshold}
        '''
        result = self._values.get("ban_threshold")
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThreshold"], result)

    @builtins.property
    def enforce_on_key(self) -> typing.Optional[builtins.str]:
        '''Determines the key to enforce the rateLimitThreshold on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#enforce_on_key GoogleComputeSecurityPolicy#enforce_on_key}
        '''
        result = self._values.get("enforce_on_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enforce_on_key_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs"]]]:
        '''enforce_on_key_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#enforce_on_key_configs GoogleComputeSecurityPolicy#enforce_on_key_configs}
        '''
        result = self._values.get("enforce_on_key_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs"]]], result)

    @builtins.property
    def enforce_on_key_name(self) -> typing.Optional[builtins.str]:
        '''Rate limit key name applicable only for the following key types: HTTP_HEADER -- Name of the HTTP header whose value is taken as the key value.

        HTTP_COOKIE -- Name of the HTTP cookie whose value is taken as the key value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#enforce_on_key_name GoogleComputeSecurityPolicy#enforce_on_key_name}
        '''
        result = self._values.get("enforce_on_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exceed_redirect_options(
        self,
    ) -> typing.Optional["GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptions"]:
        '''exceed_redirect_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#exceed_redirect_options GoogleComputeSecurityPolicy#exceed_redirect_options}
        '''
        result = self._values.get("exceed_redirect_options")
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRuleRateLimitOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThreshold",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "interval_sec": "intervalSec"},
)
class GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThreshold:
    def __init__(self, *, count: jsii.Number, interval_sec: jsii.Number) -> None:
        '''
        :param count: Number of HTTP(S) requests for calculating the threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#count GoogleComputeSecurityPolicy#count}
        :param interval_sec: Interval over which the threshold is computed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#interval_sec GoogleComputeSecurityPolicy#interval_sec}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19895f1e8b24c3d4ee60ea397999f8721837ffdb54b424807a4bd96a050a7be5)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument interval_sec", value=interval_sec, expected_type=type_hints["interval_sec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "count": count,
            "interval_sec": interval_sec,
        }

    @builtins.property
    def count(self) -> jsii.Number:
        '''Number of HTTP(S) requests for calculating the threshold.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#count GoogleComputeSecurityPolicy#count}
        '''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def interval_sec(self) -> jsii.Number:
        '''Interval over which the threshold is computed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#interval_sec GoogleComputeSecurityPolicy#interval_sec}
        '''
        result = self._values.get("interval_sec")
        assert result is not None, "Required property 'interval_sec' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThreshold(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThresholdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThresholdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3c8c0ea288e27d763fc0e7d99ffe2f15dbc830897724174dcb6e31131495ddb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8a54b90668f7d36fce6dd90f869ced750dd31d670c669ae115e817e316b4b7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalSec")
    def interval_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "intervalSec"))

    @interval_sec.setter
    def interval_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc57404079dedf1fa751b9d61c635ac3dacfacbb103e1427c3ceed70ce17a773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThreshold]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThreshold], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThreshold],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4475f1e47900239d182dbb58a8b0a556637da3e8f64b089acd4bdd0a3f2d561)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "enforce_on_key_name": "enforceOnKeyName",
        "enforce_on_key_type": "enforceOnKeyType",
    },
)
class GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs:
    def __init__(
        self,
        *,
        enforce_on_key_name: typing.Optional[builtins.str] = None,
        enforce_on_key_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enforce_on_key_name: Rate limit key name applicable only for the following key types: HTTP_HEADER -- Name of the HTTP header whose value is taken as the key value. HTTP_COOKIE -- Name of the HTTP cookie whose value is taken as the key value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#enforce_on_key_name GoogleComputeSecurityPolicy#enforce_on_key_name}
        :param enforce_on_key_type: Determines the key to enforce the rate_limit_threshold on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#enforce_on_key_type GoogleComputeSecurityPolicy#enforce_on_key_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28c7ee59853bad73400945b5bc7085de52c4e17b60269016eea11af4b1eafc07)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#enforce_on_key_name GoogleComputeSecurityPolicy#enforce_on_key_name}
        '''
        result = self._values.get("enforce_on_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enforce_on_key_type(self) -> typing.Optional[builtins.str]:
        '''Determines the key to enforce the rate_limit_threshold on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#enforce_on_key_type GoogleComputeSecurityPolicy#enforce_on_key_type}
        '''
        result = self._values.get("enforce_on_key_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__53845ff5ff4f3a4e68ede7b1fdb9ed63792bca29bdb21958804501a4bcc4289f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__947b274a352889cbe48fd668d0bd6d0ead195975cf1097640519eff1e8c0c58d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54184cb6e9ec1288eff3e69f968b907dd1ca9946807b2ddb8395660f63ddf782)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc67b0adf54b8a8039643bb280518246f6cae7600d98569cc8c7fc1540840870)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a74744b2fbaa26d16bdc81a356d4424cc5d0d6d4d04ffea8cbff53535f906a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a3970d2fe72b46b19a8927ba0e353ebdc657ee71edd116f839ada8e2e7b6139)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__02c3f38598adb7551a5c6b25544ebbf97993840499288cdb9fe27b27c55190ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__286c407b165fe08f2e0e02c2653071390b0b0d0af7b5f8f27df60031c2d718b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforceOnKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforceOnKeyType")
    def enforce_on_key_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enforceOnKeyType"))

    @enforce_on_key_type.setter
    def enforce_on_key_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0696c4263bca164554bde1d42640bcb265f4cce9140211093841e97c5896359)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforceOnKeyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41dce5118256ac0146ae91793b13dea4247de9b64fec475194d4920b0327548a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptions",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "target": "target"},
)
class GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptions:
    def __init__(
        self,
        *,
        type: builtins.str,
        target: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Type of the redirect action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#type GoogleComputeSecurityPolicy#type}
        :param target: Target for the redirect action. This is required if the type is EXTERNAL_302 and cannot be specified for GOOGLE_RECAPTCHA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#target GoogleComputeSecurityPolicy#target}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87b60b8c5d367ea335b5a0747b34bc20dccb17f82f03512db87aa92d7942959e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#type GoogleComputeSecurityPolicy#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''Target for the redirect action. This is required if the type is EXTERNAL_302 and cannot be specified for GOOGLE_RECAPTCHA.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#target GoogleComputeSecurityPolicy#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f859aee14d56c31f108d9d74537a92e5b9483b571321771249074b4f07927e41)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d67eb0e071838ed35fb5c4e59b3ee0b7aaab86cc616703270dcd66a750668391)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89f2196b5c6f08695df7febab7243ace41732c5ac1501d02e6e9ae08fece0eb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptions]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c6c08689e84a4670f319b6910c070fc0d8ce67b7de2df04b9a1021201e22612)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeSecurityPolicyRuleRateLimitOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRuleRateLimitOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fa54a63d73efe7063e473a610af38e6d8b03f2116564b705aa2cad94ae804f2)
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
        :param count: Number of HTTP(S) requests for calculating the threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#count GoogleComputeSecurityPolicy#count}
        :param interval_sec: Interval over which the threshold is computed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#interval_sec GoogleComputeSecurityPolicy#interval_sec}
        '''
        value = GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThreshold(
            count=count, interval_sec=interval_sec
        )

        return typing.cast(None, jsii.invoke(self, "putBanThreshold", [value]))

    @jsii.member(jsii_name="putEnforceOnKeyConfigs")
    def put_enforce_on_key_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0e14c1d8b48a9393dbe6c7e816138b7e6c9ce36464886f6fefe9ce6ce7f0ed5)
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
        :param type: Type of the redirect action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#type GoogleComputeSecurityPolicy#type}
        :param target: Target for the redirect action. This is required if the type is EXTERNAL_302 and cannot be specified for GOOGLE_RECAPTCHA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#target GoogleComputeSecurityPolicy#target}
        '''
        value = GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptions(
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
        :param count: Number of HTTP(S) requests for calculating the threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#count GoogleComputeSecurityPolicy#count}
        :param interval_sec: Interval over which the threshold is computed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#interval_sec GoogleComputeSecurityPolicy#interval_sec}
        '''
        value = GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThreshold(
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
    ) -> GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThresholdOutputReference:
        return typing.cast(GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThresholdOutputReference, jsii.get(self, "banThreshold"))

    @builtins.property
    @jsii.member(jsii_name="enforceOnKeyConfigs")
    def enforce_on_key_configs(
        self,
    ) -> GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsList:
        return typing.cast(GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsList, jsii.get(self, "enforceOnKeyConfigs"))

    @builtins.property
    @jsii.member(jsii_name="exceedRedirectOptions")
    def exceed_redirect_options(
        self,
    ) -> GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsOutputReference:
        return typing.cast(GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsOutputReference, jsii.get(self, "exceedRedirectOptions"))

    @builtins.property
    @jsii.member(jsii_name="rateLimitThreshold")
    def rate_limit_threshold(
        self,
    ) -> "GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdOutputReference":
        return typing.cast("GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdOutputReference", jsii.get(self, "rateLimitThreshold"))

    @builtins.property
    @jsii.member(jsii_name="banDurationSecInput")
    def ban_duration_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "banDurationSecInput"))

    @builtins.property
    @jsii.member(jsii_name="banThresholdInput")
    def ban_threshold_input(
        self,
    ) -> typing.Optional[GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThreshold]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThreshold], jsii.get(self, "banThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="conformActionInput")
    def conform_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conformActionInput"))

    @builtins.property
    @jsii.member(jsii_name="enforceOnKeyConfigsInput")
    def enforce_on_key_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs]]], jsii.get(self, "enforceOnKeyConfigsInput"))

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
    ) -> typing.Optional[GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptions]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptions], jsii.get(self, "exceedRedirectOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="rateLimitThresholdInput")
    def rate_limit_threshold_input(
        self,
    ) -> typing.Optional["GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThreshold"]:
        return typing.cast(typing.Optional["GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThreshold"], jsii.get(self, "rateLimitThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="banDurationSec")
    def ban_duration_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "banDurationSec"))

    @ban_duration_sec.setter
    def ban_duration_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0a961b2c99df18ab9440eea40721706b65e8a41042d4c9f1383f18345ff0503)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "banDurationSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="conformAction")
    def conform_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "conformAction"))

    @conform_action.setter
    def conform_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8acc7e5ed3dbf6189b74262c842ef0fab90ee40ba6bc29e3f352bd4a30a1b822)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "conformAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforceOnKey")
    def enforce_on_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enforceOnKey"))

    @enforce_on_key.setter
    def enforce_on_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50da3ed6fd955eadc6ca3cee3e324c40cd26890eff27eb94cf996a3de4cc3803)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforceOnKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforceOnKeyName")
    def enforce_on_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enforceOnKeyName"))

    @enforce_on_key_name.setter
    def enforce_on_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e013dd464ba0574fda50eb7c3ffa66eaef1782ff68a91a89c0892c2d3d4fbba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforceOnKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exceedAction")
    def exceed_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exceedAction"))

    @exceed_action.setter
    def exceed_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__988c3cff8a1866851b3a1e16476398011ac190ab737e7d7810c51acab73d8578)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exceedAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeSecurityPolicyRuleRateLimitOptions]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyRuleRateLimitOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeSecurityPolicyRuleRateLimitOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5a1d418a42f782f42bae1c0b1a15a82fe57c1784ae01f451436c8f18c493f81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThreshold",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "interval_sec": "intervalSec"},
)
class GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThreshold:
    def __init__(self, *, count: jsii.Number, interval_sec: jsii.Number) -> None:
        '''
        :param count: Number of HTTP(S) requests for calculating the threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#count GoogleComputeSecurityPolicy#count}
        :param interval_sec: Interval over which the threshold is computed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#interval_sec GoogleComputeSecurityPolicy#interval_sec}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3556ea60e636f31235d54af776bccaae1573194241ffae6fed818759ddca9c47)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument interval_sec", value=interval_sec, expected_type=type_hints["interval_sec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "count": count,
            "interval_sec": interval_sec,
        }

    @builtins.property
    def count(self) -> jsii.Number:
        '''Number of HTTP(S) requests for calculating the threshold.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#count GoogleComputeSecurityPolicy#count}
        '''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def interval_sec(self) -> jsii.Number:
        '''Interval over which the threshold is computed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#interval_sec GoogleComputeSecurityPolicy#interval_sec}
        '''
        result = self._values.get("interval_sec")
        assert result is not None, "Required property 'interval_sec' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThreshold(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7721b3df0a089e8ca43bd73a30ef5aedd66487a59697708e3709f3674af50d7c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4983fed5838a3ba9996b44fd6ade6b1cd73214012b5b9bb511210b38d4a2dc04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalSec")
    def interval_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "intervalSec"))

    @interval_sec.setter
    def interval_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f564a099526798e153095ec53a0213f110f6d50f805865757f8afa7b35b7ddf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThreshold]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThreshold], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThreshold],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f032c3ff18616f9d60680981878d6e9b2deb7387ade5e49814f09d93ebf50d7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRuleRedirectOptions",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "target": "target"},
)
class GoogleComputeSecurityPolicyRuleRedirectOptions:
    def __init__(
        self,
        *,
        type: builtins.str,
        target: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Type of the redirect action. Available options: EXTERNAL_302: Must specify the corresponding target field in config. GOOGLE_RECAPTCHA: Cannot specify target field in config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#type GoogleComputeSecurityPolicy#type}
        :param target: Target for the redirect action. This is required if the type is EXTERNAL_302 and cannot be specified for GOOGLE_RECAPTCHA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#target GoogleComputeSecurityPolicy#target}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3d9b9e41a85394b95ac4498438fff4872407605c8c7ba2f5463f5ec10623fdf)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#type GoogleComputeSecurityPolicy#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''Target for the redirect action. This is required if the type is EXTERNAL_302 and cannot be specified for GOOGLE_RECAPTCHA.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#target GoogleComputeSecurityPolicy#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyRuleRedirectOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyRuleRedirectOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyRuleRedirectOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6dca066264f78de5728eb6d3102bb6677827f06a6dd37efebdc63a86c650df14)
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
            type_hints = typing.get_type_hints(_typecheckingstub__206fcc5fbdcbc01d657fcde5f75ec29d512b99bb32f0656d29870dc00754a4b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af7e225e07e070a35162c67a169264d218345818fb0efddffd1e33783f68b965)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeSecurityPolicyRuleRedirectOptions]:
        return typing.cast(typing.Optional[GoogleComputeSecurityPolicyRuleRedirectOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeSecurityPolicyRuleRedirectOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff7e13ec867b31389abda12d617e01e96544a775c283a78e80a0895c2b4e3db8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleComputeSecurityPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#create GoogleComputeSecurityPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#delete GoogleComputeSecurityPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#update GoogleComputeSecurityPolicy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10e1e2a83e5ef55e734f1e1c9a5ab0698dcbb08b25d1d57c8c27bdbc68f60d18)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#create GoogleComputeSecurityPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#delete GoogleComputeSecurityPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_security_policy#update GoogleComputeSecurityPolicy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSecurityPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSecurityPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSecurityPolicy.GoogleComputeSecurityPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41f5b804392b0264b9042fa07680e9400443c13146d421a77f839ee439f8a1e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__189d73e0f1a90c461eefb69d13d4755389911fa7dc89f8375de263c52a8b87c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dad7bb59569d14ff6fcc538bc1b43c53f57fdb1dc9c876c156c5748f2042d09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76b1b0e8241e2655d41b032c79f5518b9e2cf4ac2c876fc7c3bfa2ddf357fbd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1875b5065acfddeada91c45bf1d33c809d9b99e283baf47dc99baef397592680)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleComputeSecurityPolicy",
    "GoogleComputeSecurityPolicyAdaptiveProtectionConfig",
    "GoogleComputeSecurityPolicyAdaptiveProtectionConfigAutoDeployConfig",
    "GoogleComputeSecurityPolicyAdaptiveProtectionConfigAutoDeployConfigOutputReference",
    "GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig",
    "GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigOutputReference",
    "GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs",
    "GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsList",
    "GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsOutputReference",
    "GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs",
    "GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigsList",
    "GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigsOutputReference",
    "GoogleComputeSecurityPolicyAdaptiveProtectionConfigOutputReference",
    "GoogleComputeSecurityPolicyAdvancedOptionsConfig",
    "GoogleComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfig",
    "GoogleComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfigOutputReference",
    "GoogleComputeSecurityPolicyAdvancedOptionsConfigOutputReference",
    "GoogleComputeSecurityPolicyConfig",
    "GoogleComputeSecurityPolicyRecaptchaOptionsConfig",
    "GoogleComputeSecurityPolicyRecaptchaOptionsConfigOutputReference",
    "GoogleComputeSecurityPolicyRule",
    "GoogleComputeSecurityPolicyRuleHeaderAction",
    "GoogleComputeSecurityPolicyRuleHeaderActionOutputReference",
    "GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds",
    "GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsList",
    "GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAddsOutputReference",
    "GoogleComputeSecurityPolicyRuleList",
    "GoogleComputeSecurityPolicyRuleMatch",
    "GoogleComputeSecurityPolicyRuleMatchConfig",
    "GoogleComputeSecurityPolicyRuleMatchConfigOutputReference",
    "GoogleComputeSecurityPolicyRuleMatchExpr",
    "GoogleComputeSecurityPolicyRuleMatchExprOptions",
    "GoogleComputeSecurityPolicyRuleMatchExprOptionsOutputReference",
    "GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptions",
    "GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptionsOutputReference",
    "GoogleComputeSecurityPolicyRuleMatchExprOutputReference",
    "GoogleComputeSecurityPolicyRuleMatchOutputReference",
    "GoogleComputeSecurityPolicyRuleOutputReference",
    "GoogleComputeSecurityPolicyRulePreconfiguredWafConfig",
    "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusion",
    "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionList",
    "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionOutputReference",
    "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie",
    "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieList",
    "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookieOutputReference",
    "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader",
    "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderList",
    "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeaderOutputReference",
    "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam",
    "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamList",
    "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParamOutputReference",
    "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri",
    "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriList",
    "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUriOutputReference",
    "GoogleComputeSecurityPolicyRulePreconfiguredWafConfigOutputReference",
    "GoogleComputeSecurityPolicyRuleRateLimitOptions",
    "GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThreshold",
    "GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThresholdOutputReference",
    "GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs",
    "GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsList",
    "GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigsOutputReference",
    "GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptions",
    "GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptionsOutputReference",
    "GoogleComputeSecurityPolicyRuleRateLimitOptionsOutputReference",
    "GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThreshold",
    "GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThresholdOutputReference",
    "GoogleComputeSecurityPolicyRuleRedirectOptions",
    "GoogleComputeSecurityPolicyRuleRedirectOptionsOutputReference",
    "GoogleComputeSecurityPolicyTimeouts",
    "GoogleComputeSecurityPolicyTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__fecc710847eadb6bb10f3f5ab244e929151509b547744cc5a42abff4762b2b7f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    adaptive_protection_config: typing.Optional[typing.Union[GoogleComputeSecurityPolicyAdaptiveProtectionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    advanced_options_config: typing.Optional[typing.Union[GoogleComputeSecurityPolicyAdvancedOptionsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    recaptcha_options_config: typing.Optional[typing.Union[GoogleComputeSecurityPolicyRecaptchaOptionsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeSecurityPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__3f85a1251d1be34e96d8514cb40a5186e53f4e80997c70a620c9497712c206cc(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__252ba1039fcb14988ce91252c90820570f7cf04fbeec8b98109ad4d9ae8bd3de(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5143e872f87b646bd1c6787c3e1339db86e7cd3e67ad945a77880bed487c949d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab39ace6afd00a35167c0a1ad7646361a60cd52bf32dbe65c005d22644b4a22b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__940e5de3fbc03eaef3e00ddb1394ef38bc0b5ce2cd1ecf69eb0fa2cf622afd34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ca7baabdc9215d67c5cb275bd32a295a6a4a868250e21095b423d4922fb6d3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d40370e34426fc44054bb6092a3ea30994af31d17e3020ee1cd56cb0b10168d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d0dc85030e330c94b918e458e23d5871b399522566e8cb8453cca40e76a1964(
    *,
    auto_deploy_config: typing.Optional[typing.Union[GoogleComputeSecurityPolicyAdaptiveProtectionConfigAutoDeployConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    layer7_ddos_defense_config: typing.Optional[typing.Union[GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a0d3d057bfc44767b9f79e5d70a436d9691b380586648fb28b6acb1e62e6a1a(
    *,
    confidence_threshold: typing.Optional[jsii.Number] = None,
    expiration_sec: typing.Optional[jsii.Number] = None,
    impacted_baseline_threshold: typing.Optional[jsii.Number] = None,
    load_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceedd3ff5bb1c19f8c4c7103d0a15a1e8a32fe2b8acc06c48f9250f8aa212cf4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eb6fa2b1afa426b6837bb7082ffb329b2259d5c74df95ce14289c37dbcae256(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5cf8e099c8bc867f0b22a4e56fda63d4684965ac03c6066fb4fd4037ab6efd4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf8de267f0eff5efe0f4c0278a746a5f90dcf8c45c042e70a0862792f8986651(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52dac5ce159b846008a1e74b393fb5af79d0f8231a0ae9de173b2656cf00da3c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd67dba8b1a94508998a063513fed4078f39f17b8ffae3b7fba795551e12b0c4(
    value: typing.Optional[GoogleComputeSecurityPolicyAdaptiveProtectionConfigAutoDeployConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87a062d5d581c037f6158f794f46f40ae9bb0a86e2b7ab6f82d5815b072c247a(
    *,
    enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    rule_visibility: typing.Optional[builtins.str] = None,
    threshold_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fa0b83569bf6a8a8c709b1c41cd3a914ed074426047b442cda1c91dedbf21d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__887b137107aaf4399361b67d580813d021d1ae175b95c8ff9e5cd63b354daae0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87fdcab022f06430539baaf30110061bf911f331798060ec239c717406178610(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a81b284843829f29538e90c53bf4fdd87eaedaf3594ecd2088ec857663fd006(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45eb42a967d8b0ccc1f0e0dce330875de5db155cb2aac831c30c8bee34ba75d8(
    value: typing.Optional[GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c06249d0dfd6d8b44076c3789b154d09a8b9722cc285d2c7fec897633b46f332(
    *,
    name: builtins.str,
    auto_deploy_confidence_threshold: typing.Optional[jsii.Number] = None,
    auto_deploy_expiration_sec: typing.Optional[jsii.Number] = None,
    auto_deploy_impacted_baseline_threshold: typing.Optional[jsii.Number] = None,
    auto_deploy_load_threshold: typing.Optional[jsii.Number] = None,
    detection_absolute_qps: typing.Optional[jsii.Number] = None,
    detection_load_threshold: typing.Optional[jsii.Number] = None,
    detection_relative_to_baseline_qps: typing.Optional[jsii.Number] = None,
    traffic_granularity_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfd3ccd1693b5449d534682b31c00b82bb9c841386c83eafb5fbafe90f726738(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aadc527c4de746b3d924629a831411276f647b73c1d193848deacc700de00b1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0e45d3f807dea3cf8aefd9856e6537773317f46f20a8c04213ac0b0f86f560e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1347bd1888c11e1c42e0b0c6e7916a0f8055c1b5458e52cafb44ca9a4a2d9deb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a58ea1c8bfda7cda500d5f537f9955adb8ac06fe15ce4267d6c36e7074d68a35(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a63e2c0ca3a66af2906e250909708ae45b0ef22c84dc601f537078120a2eee8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acb9fe3bd5795f41ceaa837a094e5e225de04a793b0754fe39edb3bf8bfa6919(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d7d9213d460836bfa84c3f016b04226650ae384db341bc24634363752baa14e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d7c73f8c0476009039cf3a370bf1d2f9821a88a83c1aa6ba12ce4127ef81c07(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42541018cb27f62f5f48dc1d8261ed7bb56b4ef153bb6451a5a1699863a6c6cc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40fd428f73db95641efc4c124a67d761d5b05285aaf2c29410b52366a083daf6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc6b74178bd20ab5ecca0830ffdfddc95f043d68faa1b1b86d528536ee80ccf6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c804afb367a039deb8b52e9d482268c45d18f88b354c31bf4b49a78d37c7c192(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18d4f1eab9e6a03d1c86b03c97d890cbf97d9f1a436e27b32ed41a4b06e39239(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63a29e6da705b883cde7bd853f3a664c10218112c5ac7c1753caea5a777ae2e7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3498c05bb2fb6d7bead05e021ac4f214463aaf02f7b15716dc39bcf697d1f3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3187954075d1e14ef0444093f7559454bde69bb5e2efc994efae2de1ecc67488(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65f2dc7b8aa667ede9ab58bd42dd90eebf61da0514b2ed5429739ee3f33d8faf(
    *,
    type: builtins.str,
    enable_each_unique_value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8d15324a65e15f6c31f1ccd7fb7e89fb84bb04976acd80ca76ac95cb2c4b3b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db6f697cc5a10be9650e7d898ddf6fb6eb100945ca332899d2bcc28a8d67a405(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__266d14bf5b1fe31d968e8544f30c44fbe099b1b840946247363b510409783961(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__365991e21558633c8840d9e3c79e6b52d105d179c824842065842be7e8eeec8f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a95a107dc258eaff8f83e0403355df9022d26e558d97a2cecf739d7e29f0515(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2603af767830dd3f521a3e7cfac10acceae66ac9c6b86acb96fd5e6895f936ed(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1200e377e558e6f307fb3376e25e23ddca6cb24edc097f5cd7b47e39333507c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0ec7891a72d5253123cbc266dd380409fb744eca94220ed562b931361f6f211(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8117e9eb19f2aa8adf828c764b76d3a848b4e4121a0e8680586c277d8ed08f51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7585e8a68fb90d33b6b777c4ebc524363ab9e4fd425a0032d8a08bb72c8a4a83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f11434a16ad03f4d5de0532d7b7a5c6e48d2bdc9f33f65ef26f0623b14c2652(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyAdaptiveProtectionConfigLayer7DdosDefenseConfigThresholdConfigsTrafficGranularityConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4de4862fe71de53f8a8d6bceb5a9f0e531defedc1478c965d77be0bc9c6e5d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3ceb9ee5a4129460d66008195c3dafd334e2fc36dda0cccbedb3bf0bea2ba1f(
    value: typing.Optional[GoogleComputeSecurityPolicyAdaptiveProtectionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d08e1b21aa07e83c12c3482555db70c56c5529e4ebacde9506d07134ccd49a2d(
    *,
    json_custom_config: typing.Optional[typing.Union[GoogleComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    json_parsing: typing.Optional[builtins.str] = None,
    log_level: typing.Optional[builtins.str] = None,
    user_ip_request_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__979a982845e7c8b234d8c5bd4307b82cc6f28269b1fc39cd14c1e59cbcc525e2(
    *,
    content_types: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bc8b00a868e0f33831554ec0941d29edbe732a21ba7c0505188b3350d0c4841(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__515b4b6e8566a142cc38461449b131cea3804504026c26e3105caf34724a75ab(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d82f1004af00b3bc5412009922d96ef13424714db7add4fef7e74ee85efd309a(
    value: typing.Optional[GoogleComputeSecurityPolicyAdvancedOptionsConfigJsonCustomConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbe0e1799b4ea99698e93f0704b11030c4d7680adc1f43d19e89dc70f80f8b37(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aafec473825455b8b802ce94675b32bbcb65fccd8a8266c02e34fd43524440fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33eacee6aa1d0602453f47c78b887c11f78514d09967bca0608d0d944fa4e9be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73fbb1c9ae571af11bdf44015f39f1e9f1294026ae96b6b878273cee691596b0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d88a6f7512f3f3d335212b703f6e47fc13d00efa61aad9fe793c44ac1f95eacd(
    value: typing.Optional[GoogleComputeSecurityPolicyAdvancedOptionsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f94a14b5a30d02e46fd24a5a69aec67870e98e9e9d5b45192bfb3d0fd4ef7197(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    adaptive_protection_config: typing.Optional[typing.Union[GoogleComputeSecurityPolicyAdaptiveProtectionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    advanced_options_config: typing.Optional[typing.Union[GoogleComputeSecurityPolicyAdvancedOptionsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    recaptcha_options_config: typing.Optional[typing.Union[GoogleComputeSecurityPolicyRecaptchaOptionsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeSecurityPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d07cd13260fe19a18e5736a8014d3fb646b1f95586c7c991268002efaa1cefe(
    *,
    redirect_site_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4e2861f9f0cc8301bb1a018423d890ba94816d768e097b1970262682bbeca24(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__730768aba2ea22e04197a3aac784d732cd78141b8933681525b090c4364cf36e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba936aff49894da7c1bf7819b1672c2fb28e1dffbf3a833ddc3b27c6de690b94(
    value: typing.Optional[GoogleComputeSecurityPolicyRecaptchaOptionsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abcfa6af206f57a464098d5caf35404e7c2e8b1403f6ffcc325760875350dafc(
    *,
    action: builtins.str,
    match: typing.Union[GoogleComputeSecurityPolicyRuleMatch, typing.Dict[builtins.str, typing.Any]],
    priority: jsii.Number,
    description: typing.Optional[builtins.str] = None,
    header_action: typing.Optional[typing.Union[GoogleComputeSecurityPolicyRuleHeaderAction, typing.Dict[builtins.str, typing.Any]]] = None,
    preconfigured_waf_config: typing.Optional[typing.Union[GoogleComputeSecurityPolicyRulePreconfiguredWafConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    preview: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    rate_limit_options: typing.Optional[typing.Union[GoogleComputeSecurityPolicyRuleRateLimitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    redirect_options: typing.Optional[typing.Union[GoogleComputeSecurityPolicyRuleRedirectOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5da920f72ed90831dc957cc807d18e2f9723fd74c9a630aea324d97e0246963(
    *,
    request_headers_to_adds: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d441994c2bae89150655c6763c2499777eabe23760577ab8ae9bd20ae39707d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccc37b1b522c966d5867a33e04a147d248b89a189aa145fee2a8f4ddb4e6159b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df8a552d4f9f4b647b61dc6c22f83d1402e2dd2a621b25ef544baa6edcf7a831(
    value: typing.Optional[GoogleComputeSecurityPolicyRuleHeaderAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3329dcde84146078ed8c76c010ace4bfce84d4a2e7a01ef61bfc9839eff89ff(
    *,
    header_name: builtins.str,
    header_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ef944215780ebf3a0e562df2041163d1a749f6e414b7d9c3207b2d0ec9a6350(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46425823e6c9f9d68fb99d13dbfbfbfce918acdf9aa0e294be02765b3bf35e63(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9f926cf5df3c921316c71be7dfeb2ee76a3da3b83e71e40cb277537a9360365(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cad8a4f3077a054b255cdb89e70e7fe5f9295dab1658913fdaecb6c3b6543a66(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5f77f941568c54a6f5dca3b58cabf55c1a0eeb82cfb0c53ae81946ac722a5dc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7315344c024e362e7d0dae04f87a18d9b6dd5ae9560c9b5401620d7e2addc699(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15e8a2a5368c6010431c57961d3dfa06c8a6f29e30a2837bf915d3baf3dbac28(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c407700bc2f730bd581620d1092565afaf2b3680350305cdc4702aa07cf949c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6db60d9c8f4562c2940f9ebbc98d22ae960d7695401a479e81c964b507c85125(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30758ed5067e492ded8e5f3999e3fe1693aa1196177d6b8799c45b73205e0276(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRuleHeaderActionRequestHeadersToAdds]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12b14466b9772aa9043eb5de6cda463fc491ab2e6667a953fbed94f754133c53(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08d140dff9d37026d4ae9832bfae4966146bf090160ab8c1f8b5fd2490d4f770(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__debfc15b0e99eb08b287740961e59d2b16f6211f750fdf00940bffb4b03d6fd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79cafc75f9429257f81a381c261ec1a75eca7b9fc0d5784afbd14b281bd35a6c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67b78893a1758b9a265e8378cbb683d3fd651261ccd66d355d988d47d287f791(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1711dd7340a30d4e7a49fdcc2190c898f7ede92ddf0362c612a851afa8993c86(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c21af780107c072c9dc5f33f4b40fa1772387e904f273558e9d2ad571e1f738(
    *,
    config: typing.Optional[typing.Union[GoogleComputeSecurityPolicyRuleMatchConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    expr: typing.Optional[typing.Union[GoogleComputeSecurityPolicyRuleMatchExpr, typing.Dict[builtins.str, typing.Any]]] = None,
    expr_options: typing.Optional[typing.Union[GoogleComputeSecurityPolicyRuleMatchExprOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    versioned_expr: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04ba0095e022217308d00a45fa46d98738cb824f7f8a02f94745b1f839801bbf(
    *,
    src_ip_ranges: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3075ad5f2c2a1a84b79221ccf69322f7f10422cf34a026f6c4a2c15833711b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa0ff852250c7db9365809e666156841f18416eaf0a0391e124846f741dad9b9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ea6fd84ff2c1867cf43100e38588a64bc226264f0681a10f1874e68ab9f9490(
    value: typing.Optional[GoogleComputeSecurityPolicyRuleMatchConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af0af65207d2b36fb903b34a971a88cc7988cce0feab65ffef71b19c847e99cb(
    *,
    expression: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70d1457febdc9e144aeefa0adab72086c9a724af5ad9255e40264cbed39c6846(
    *,
    recaptcha_options: typing.Union[GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptions, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a8d32584107bbb90d3e45778ead0153e3a941198aa840c26cc36da887338c37(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a575a85cf6e483dafb7eb651cf9cfa3a5c14b55b2ca16577efc6d9aed4ad56ce(
    value: typing.Optional[GoogleComputeSecurityPolicyRuleMatchExprOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76d7f396001dd3bb52d45a14c94312b17ae0345ca149ee385e27fe8bef3a3fe3(
    *,
    action_token_site_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    session_token_site_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f16c9f199557884ad4ca93589a05a3d26076a8cbee5f064f549518cfe2725af8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__581aec377c5564f108875964de64729054598e23a2eee6b7c6b87b6e992713a2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba7996df80acbd539661efa1716ce3ffa6b3c3744ccfbd4edeb159c2a16b660c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9cb7a6b3c6d3100b387b2b0faf067b504af3515339f31ad19cb282126a9a225(
    value: typing.Optional[GoogleComputeSecurityPolicyRuleMatchExprOptionsRecaptchaOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b91f49ec75ed996317e4e0f95ba5ebb1ac96cc60693a259991e6e30faadece9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea4ff4d5b27d892c0fccc291a2c0d0e01de08f87d32146e164fb0bce4e483edd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8f30af3987a016697d5d41039ce5518eed9a64ccb709db94486c6601402bedb(
    value: typing.Optional[GoogleComputeSecurityPolicyRuleMatchExpr],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5a301cf202e61ab89c21a83226ba20e7eea4f41b4571763c6f08f51efadb6d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1ad32435cf1d5625eb86b9fab5ecaf24221b2958fe1d9f7dd5c776ef635e921(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db37ccde8887c16a16b511862af60cb4a46d7bf7dd7cab07c36df0c160b8c25f(
    value: typing.Optional[GoogleComputeSecurityPolicyRuleMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b2303cfddf8901d1bf1a6bf56f1fabbc003302cfd12de03dc6db6729c46c191(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3f82f9661442dcd2b4a6f02f69945c951793ff9128054a441932a9ab7294855(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29d79d87d1d96a7c970055672bc5d73de83d83371446c1762b189e4979d91ede(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaf6e774974c8dcb4eb6e373f96faf78972f3fcc822568cf49cb892bb381f2e7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56016f8b58f8bb68bca5ebd25df7559aa8a3f4cdd8845572da4af7e7efafaddc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__230faa2e5d6bf63f5c661c9cc511e9f760001bc09b36f39f6d7f372511b9b494(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a438bc303dfd9697392dd922ed1a27a86c9c2563bc23215dc431fb0c1c585543(
    *,
    exclusion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusion, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f3278dfa6bcd504280d5b941c9a492c0038b56846f8dd0c8ad3bf4abae9dde2(
    *,
    target_rule_set: builtins.str,
    request_cookie: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie, typing.Dict[builtins.str, typing.Any]]]]] = None,
    request_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    request_query_param: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam, typing.Dict[builtins.str, typing.Any]]]]] = None,
    request_uri: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_rule_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e454804142d1055cfefa5a4c04a18fb1977fb4ba1bcaf68322b60c61c6e3bac4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad628ba34c70fb8b05648043f9c72110fa3a5f6159a812d59ae7d16e6193c291(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dacef77ec1e33230bc0416c6369d93aed28b0a4231819b491deae86711e36c73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeab7121295cf9e5d0325579f14ff0626670a4ab019f95843b154b878f19e4f5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f39e2fbfc8dc8c9e95b81615b048b83634f903bd09b366a646c568478ecaa84f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1446af13c369360584df2d61d8a3e13a14c633ad869e184d42a8892c0b27542(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusion]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd9209795f94e7794a2e08429ec1b8d7e0cba58fa0184d634b48e7ad2b500cce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87a359c988150d836d65ddc9d7e74f0a2385d2ede2149dd65932dde1ab68eba3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__636e8aed5fb97968c783e358dbea343e0b0cde0253b7dd9777a5d455f05b3bbb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39c4507265fd7c1f8e50e6c5e2c3139e4a54cf9ab1f12df4ca3296d691f8a72f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d4b2ffcb928723c323300690549c82813c6ce5875db5bd49af53bc925e04bbb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ff4f105e378e1c5f863c01d9573a5e10f42b159f2d2f8694e40623f51c01adb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ac896d73f9be8900150e93a1e21bc6f4489d06dd05a4907c860ec6d2e7e3c1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41b720dd05089a6d3f8b89709e312617282a47f9a29ed5009894ef266522c7b0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusion]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__534a36ebca31702f7e450898fcb8188de0699721ce4be1886f5e66d9f20ef903(
    *,
    operator: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df0ac8b0577ce9a4d6c8147f9a3a00909c20b11cf4058e48b3aacbaf146d656e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d96487b2dc97e751640d89d730bb8a6199512eb18cfe83b8aec7aa405567ea2f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b26e4b23b005b728bcbfdeeeb5494a230420de84d81ca3a813bb578266389e9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a61d7ea0af3cdd170ed553de4df0377756004bf295da6143b57320b49ff0e2c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__957983506659beb9756b3ebc15d7116d333038f09ade9f045e8bf8e61c2699fb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4d85c8dc7bbeb2fc0e6a7d198c6130d6f9b4123731f8eceddafa5b9ddcd8d46(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36f2ec8ccd24cd6aaa4812d22959950e2711acf6eaa2a291760d2b619817f5bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22093c6e7d34f7c911ab9e32f27603654c7d61a588250cbe4199e28dc89ba2e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e8d6d46ae1869fddc6482b4e3dbf40f0cfe67c681b8c5f720551ce7bf26912f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__474dc1b775d12a73b6e4f2d229b809da92ee477902c6e594d692e09dc5209c2f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestCookie]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c1f82ee6561f7f2dc59c15ec07b7feb8dfff2372200cb16f8f6bf27be98bd3b(
    *,
    operator: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78ba9d36e4073137b23f5be8df39341965aa97bba0ddc58ac93b84d82299eba1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84b8104a78d84f7a5fc4554d32d52ff637f665301ca8c394b7f262ec5d4e4c9b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e332585d59ce27f2117a73be6d41bc8b2303bd5f51197cdf54ca0412c8c17c8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e56e7f27cd7a521ddd7bb73e73c568d344cfcfd402d0c5d59c8ac277afb6a73(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81741fb16315414ac97839b23c6a7b11f37c9c44b0da167ce776098afb19ba3d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c84be9ee0b224e96f2ad99ef89ceda6fd3d69422e9c2f45d70a94735d68595fd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__660fb38678e24ffb5d4276074ffb473f5e674157f121f19647fe7d1a47a237d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8379a5297f67dab9682e7b40c3c2bf438809852d01e03af8ceb78e96a803d9c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c654bb9953424b0d2dee5ed647a362a4b93c506fa99d7e96ef1f72f27340f63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dae7381d26fc958bddae97319ce801b1bead1d4bd3eecb9fb66f1b336efc61d9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f33c259cbcd1982862dcfe632e518cc3d5758f6ba1d3cd4817a21430cc99155(
    *,
    operator: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__714fc1f257c2dd4e0dcecaca4f8538889878a79c18ea0e8213cbb0db6cbb019e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1344b0d524a3c60c5da2d6b456be867ea1ac9f1faa4085efe8e44e9a1fdf6ed(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28be2054fc9b9859ccf49291ace04ce9e6253997aa28305d99ee6dd72d46e15c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27aeadc0b1919b55d048fc8d3483f93408ed45956f2e236919b1e319a218b7a5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8a07fccbfbc65b641ad9efd9ae8a17d5e86e5217b0e717faa30d8e3643bb529(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeea22e9686bcc04de62db647799afdad03753446e51c07c5f3a87f7aa0c3114(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fae45065f5a122fd317b4afa415c94f509c96e5f301b6e6adc2c6feb12a5791(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b58e90e196626c43c196bd75f50a4fe44ffc6da4fc1dc484a110bf7260bb71fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f773bf4fc2a11427936b1e9e04b5a782c5521ea35146ee8bcddfb4e1ee85fa9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ffd483de994ae7b984c66de1001b8d2063e8cb18f4e47096830cfcd9ca9797a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestQueryParam]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5a2792490abccde26248cd4fd216a5a033a027eb69f5183128bd918a7a80ace(
    *,
    operator: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b1cce0a4444f71efd0ead54f12014d2946f8ed09b5813cb288479c392a9f36a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ead12dcf804eeb1e9128d0a5975570f08cd866c8095eacad78ce6f45749d0463(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c890c0b4fd2122bcd185c9d9ea8241d69050d738f25b934aa74251c0bafe6679(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02ddff115c45ab67106f265f744971a838996a71f5580cfdce3ee36a22299445(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c768b6bfec2aa4b9632218d6a3e152821427b66ce743654f1d42cf3de115c81(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2eee321c157d54b2e00c484f249c239ecbfa8251db0f89d5c03993fb85fdc2c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__841a7290f70cbd5d4e2c7a4b45111814604f990f1a288ffc60271c7db97085ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c2b5c3b72777dbad5c7491331df08d20c65b89a4519e85db83b8bb5ef21fb7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e47adade75302acb5c87efbdde29e1f50d19ca857d8d683a98099386066fe47f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc909dee9818049e6ba692001a0314c49e253cc5ce8a48881ab2b3228acd44b7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusionRequestUri]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83db2451b262456936b48e234be9fdc695050b1cae8dc8a4fd4d608a5dbbcebc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5082be1b73a03aa798d1368ceaffb70ebe2b3767c12dce515ab6d52b47f21f74(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyRulePreconfiguredWafConfigExclusion, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91ed987741a619465b58015289ee9be5e8978f0a69a072a78ce6c7e340f121b9(
    value: typing.Optional[GoogleComputeSecurityPolicyRulePreconfiguredWafConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bddb22cba872f779e2bb6162c2413c6f6b2a00c7591f832dc0de1f79ef70a2ac(
    *,
    conform_action: builtins.str,
    exceed_action: builtins.str,
    rate_limit_threshold: typing.Union[GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThreshold, typing.Dict[builtins.str, typing.Any]],
    ban_duration_sec: typing.Optional[jsii.Number] = None,
    ban_threshold: typing.Optional[typing.Union[GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThreshold, typing.Dict[builtins.str, typing.Any]]] = None,
    enforce_on_key: typing.Optional[builtins.str] = None,
    enforce_on_key_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enforce_on_key_name: typing.Optional[builtins.str] = None,
    exceed_redirect_options: typing.Optional[typing.Union[GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19895f1e8b24c3d4ee60ea397999f8721837ffdb54b424807a4bd96a050a7be5(
    *,
    count: jsii.Number,
    interval_sec: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3c8c0ea288e27d763fc0e7d99ffe2f15dbc830897724174dcb6e31131495ddb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8a54b90668f7d36fce6dd90f869ced750dd31d670c669ae115e817e316b4b7b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc57404079dedf1fa751b9d61c635ac3dacfacbb103e1427c3ceed70ce17a773(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4475f1e47900239d182dbb58a8b0a556637da3e8f64b089acd4bdd0a3f2d561(
    value: typing.Optional[GoogleComputeSecurityPolicyRuleRateLimitOptionsBanThreshold],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28c7ee59853bad73400945b5bc7085de52c4e17b60269016eea11af4b1eafc07(
    *,
    enforce_on_key_name: typing.Optional[builtins.str] = None,
    enforce_on_key_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53845ff5ff4f3a4e68ede7b1fdb9ed63792bca29bdb21958804501a4bcc4289f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__947b274a352889cbe48fd668d0bd6d0ead195975cf1097640519eff1e8c0c58d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54184cb6e9ec1288eff3e69f968b907dd1ca9946807b2ddb8395660f63ddf782(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc67b0adf54b8a8039643bb280518246f6cae7600d98569cc8c7fc1540840870(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a74744b2fbaa26d16bdc81a356d4424cc5d0d6d4d04ffea8cbff53535f906a9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a3970d2fe72b46b19a8927ba0e353ebdc657ee71edd116f839ada8e2e7b6139(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02c3f38598adb7551a5c6b25544ebbf97993840499288cdb9fe27b27c55190ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__286c407b165fe08f2e0e02c2653071390b0b0d0af7b5f8f27df60031c2d718b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0696c4263bca164554bde1d42640bcb265f4cce9140211093841e97c5896359(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41dce5118256ac0146ae91793b13dea4247de9b64fec475194d4920b0327548a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87b60b8c5d367ea335b5a0747b34bc20dccb17f82f03512db87aa92d7942959e(
    *,
    type: builtins.str,
    target: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f859aee14d56c31f108d9d74537a92e5b9483b571321771249074b4f07927e41(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d67eb0e071838ed35fb5c4e59b3ee0b7aaab86cc616703270dcd66a750668391(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89f2196b5c6f08695df7febab7243ace41732c5ac1501d02e6e9ae08fece0eb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c6c08689e84a4670f319b6910c070fc0d8ce67b7de2df04b9a1021201e22612(
    value: typing.Optional[GoogleComputeSecurityPolicyRuleRateLimitOptionsExceedRedirectOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fa54a63d73efe7063e473a610af38e6d8b03f2116564b705aa2cad94ae804f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0e14c1d8b48a9393dbe6c7e816138b7e6c9ce36464886f6fefe9ce6ce7f0ed5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSecurityPolicyRuleRateLimitOptionsEnforceOnKeyConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0a961b2c99df18ab9440eea40721706b65e8a41042d4c9f1383f18345ff0503(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8acc7e5ed3dbf6189b74262c842ef0fab90ee40ba6bc29e3f352bd4a30a1b822(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50da3ed6fd955eadc6ca3cee3e324c40cd26890eff27eb94cf996a3de4cc3803(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e013dd464ba0574fda50eb7c3ffa66eaef1782ff68a91a89c0892c2d3d4fbba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__988c3cff8a1866851b3a1e16476398011ac190ab737e7d7810c51acab73d8578(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5a1d418a42f782f42bae1c0b1a15a82fe57c1784ae01f451436c8f18c493f81(
    value: typing.Optional[GoogleComputeSecurityPolicyRuleRateLimitOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3556ea60e636f31235d54af776bccaae1573194241ffae6fed818759ddca9c47(
    *,
    count: jsii.Number,
    interval_sec: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7721b3df0a089e8ca43bd73a30ef5aedd66487a59697708e3709f3674af50d7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4983fed5838a3ba9996b44fd6ade6b1cd73214012b5b9bb511210b38d4a2dc04(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f564a099526798e153095ec53a0213f110f6d50f805865757f8afa7b35b7ddf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f032c3ff18616f9d60680981878d6e9b2deb7387ade5e49814f09d93ebf50d7a(
    value: typing.Optional[GoogleComputeSecurityPolicyRuleRateLimitOptionsRateLimitThreshold],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3d9b9e41a85394b95ac4498438fff4872407605c8c7ba2f5463f5ec10623fdf(
    *,
    type: builtins.str,
    target: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dca066264f78de5728eb6d3102bb6677827f06a6dd37efebdc63a86c650df14(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__206fcc5fbdcbc01d657fcde5f75ec29d512b99bb32f0656d29870dc00754a4b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af7e225e07e070a35162c67a169264d218345818fb0efddffd1e33783f68b965(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff7e13ec867b31389abda12d617e01e96544a775c283a78e80a0895c2b4e3db8(
    value: typing.Optional[GoogleComputeSecurityPolicyRuleRedirectOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10e1e2a83e5ef55e734f1e1c9a5ab0698dcbb08b25d1d57c8c27bdbc68f60d18(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41f5b804392b0264b9042fa07680e9400443c13146d421a77f839ee439f8a1e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__189d73e0f1a90c461eefb69d13d4755389911fa7dc89f8375de263c52a8b87c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dad7bb59569d14ff6fcc538bc1b43c53f57fdb1dc9c876c156c5748f2042d09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76b1b0e8241e2655d41b032c79f5518b9e2cf4ac2c876fc7c3bfa2ddf357fbd5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1875b5065acfddeada91c45bf1d33c809d9b99e283baf47dc99baef397592680(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSecurityPolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
