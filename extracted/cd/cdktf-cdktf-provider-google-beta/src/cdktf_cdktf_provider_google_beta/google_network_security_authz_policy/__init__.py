r'''
# `google_network_security_authz_policy`

Refer to the Terraform Registry for docs: [`google_network_security_authz_policy`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy).
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


class GoogleNetworkSecurityAuthzPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy google_network_security_authz_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        action: builtins.str,
        location: builtins.str,
        name: builtins.str,
        target: typing.Union["GoogleNetworkSecurityAuthzPolicyTarget", typing.Dict[builtins.str, typing.Any]],
        custom_provider: typing.Optional[typing.Union["GoogleNetworkSecurityAuthzPolicyCustomProvider", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        http_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecurityAuthzPolicyHttpRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleNetworkSecurityAuthzPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy google_network_security_authz_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param action: When the action is CUSTOM, customProvider must be specified. When the action is ALLOW, only requests matching the policy will be allowed. When the action is DENY, only requests matching the policy will be denied. When a request arrives, the policies are evaluated in the following order: 1. If there is a CUSTOM policy that matches the request, the CUSTOM policy is evaluated using the custom authorization providers and the request is denied if the provider rejects the request. 2. If there are any DENY policies that match the request, the request is denied. 3. If there are no ALLOW policies for the resource or if any of the ALLOW policies match the request, the request is allowed. 4. Else the request is denied by default if none of the configured AuthzPolicies with ALLOW action match the request. Possible values: ["ALLOW", "DENY", "CUSTOM"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#action GoogleNetworkSecurityAuthzPolicy#action}
        :param location: The location of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#location GoogleNetworkSecurityAuthzPolicy#location}
        :param name: Identifier. Name of the AuthzPolicy resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#name GoogleNetworkSecurityAuthzPolicy#name}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#target GoogleNetworkSecurityAuthzPolicy#target}
        :param custom_provider: custom_provider block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#custom_provider GoogleNetworkSecurityAuthzPolicy#custom_provider}
        :param description: A human-readable description of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#description GoogleNetworkSecurityAuthzPolicy#description}
        :param http_rules: http_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#http_rules GoogleNetworkSecurityAuthzPolicy#http_rules}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#id GoogleNetworkSecurityAuthzPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of labels associated with the AuthzExtension resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#labels GoogleNetworkSecurityAuthzPolicy#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#project GoogleNetworkSecurityAuthzPolicy#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#timeouts GoogleNetworkSecurityAuthzPolicy#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76a2aa2eb7227adfdef29cdff4b51285116747de715ccece05afbbc6b321117b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleNetworkSecurityAuthzPolicyConfig(
            action=action,
            location=location,
            name=name,
            target=target,
            custom_provider=custom_provider,
            description=description,
            http_rules=http_rules,
            id=id,
            labels=labels,
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
        '''Generates CDKTF code for importing a GoogleNetworkSecurityAuthzPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleNetworkSecurityAuthzPolicy to import.
        :param import_from_id: The id of the existing GoogleNetworkSecurityAuthzPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleNetworkSecurityAuthzPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0597f9421c357f0784759cb117b624ddfeb58dc31bb7e1a57b7d057844be6b0f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCustomProvider")
    def put_custom_provider(
        self,
        *,
        authz_extension: typing.Optional[typing.Union["GoogleNetworkSecurityAuthzPolicyCustomProviderAuthzExtension", typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_iap: typing.Optional[typing.Union["GoogleNetworkSecurityAuthzPolicyCustomProviderCloudIap", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param authz_extension: authz_extension block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#authz_extension GoogleNetworkSecurityAuthzPolicy#authz_extension}
        :param cloud_iap: cloud_iap block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#cloud_iap GoogleNetworkSecurityAuthzPolicy#cloud_iap}
        '''
        value = GoogleNetworkSecurityAuthzPolicyCustomProvider(
            authz_extension=authz_extension, cloud_iap=cloud_iap
        )

        return typing.cast(None, jsii.invoke(self, "putCustomProvider", [value]))

    @jsii.member(jsii_name="putHttpRules")
    def put_http_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecurityAuthzPolicyHttpRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5b4eecf27f62da30739e7f703e8e111376ecf9bb43cfe9316424a13ebc05c68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHttpRules", [value]))

    @jsii.member(jsii_name="putTarget")
    def put_target(
        self,
        *,
        load_balancing_scheme: builtins.str,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param load_balancing_scheme: All gateways and forwarding rules referenced by this policy and extensions must share the same load balancing scheme. For more information, refer to `Backend services overview <https://cloud.google.com/load-balancing/docs/backend-service>`_. Possible values: ["INTERNAL_MANAGED", "EXTERNAL_MANAGED", "INTERNAL_SELF_MANAGED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#load_balancing_scheme GoogleNetworkSecurityAuthzPolicy#load_balancing_scheme}
        :param resources: A list of references to the Forwarding Rules on which this policy will be applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#resources GoogleNetworkSecurityAuthzPolicy#resources}
        '''
        value = GoogleNetworkSecurityAuthzPolicyTarget(
            load_balancing_scheme=load_balancing_scheme, resources=resources
        )

        return typing.cast(None, jsii.invoke(self, "putTarget", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#create GoogleNetworkSecurityAuthzPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#delete GoogleNetworkSecurityAuthzPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#update GoogleNetworkSecurityAuthzPolicy#update}.
        '''
        value = GoogleNetworkSecurityAuthzPolicyTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCustomProvider")
    def reset_custom_provider(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomProvider", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetHttpRules")
    def reset_http_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpRules", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="customProvider")
    def custom_provider(
        self,
    ) -> "GoogleNetworkSecurityAuthzPolicyCustomProviderOutputReference":
        return typing.cast("GoogleNetworkSecurityAuthzPolicyCustomProviderOutputReference", jsii.get(self, "customProvider"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="httpRules")
    def http_rules(self) -> "GoogleNetworkSecurityAuthzPolicyHttpRulesList":
        return typing.cast("GoogleNetworkSecurityAuthzPolicyHttpRulesList", jsii.get(self, "httpRules"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "GoogleNetworkSecurityAuthzPolicyTargetOutputReference":
        return typing.cast("GoogleNetworkSecurityAuthzPolicyTargetOutputReference", jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleNetworkSecurityAuthzPolicyTimeoutsOutputReference":
        return typing.cast("GoogleNetworkSecurityAuthzPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="customProviderInput")
    def custom_provider_input(
        self,
    ) -> typing.Optional["GoogleNetworkSecurityAuthzPolicyCustomProvider"]:
        return typing.cast(typing.Optional["GoogleNetworkSecurityAuthzPolicyCustomProvider"], jsii.get(self, "customProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="httpRulesInput")
    def http_rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRules"]]], jsii.get(self, "httpRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional["GoogleNetworkSecurityAuthzPolicyTarget"]:
        return typing.cast(typing.Optional["GoogleNetworkSecurityAuthzPolicyTarget"], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleNetworkSecurityAuthzPolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleNetworkSecurityAuthzPolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc34ae11e0f873dc2f6a5f41eec4f0e7767d91242d476d97c85113da0e200ba5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5d42fd24c85696d4d2e4173fac2412a87f4cfc74c7024461e029321d062c137)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb4cb2d1d3a1ed67a13328e69fc9a6be35abef468267a8ab3ea7a1b105f7a969)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aff62bd4f6210e6fc003709543767a31d9d2a71792d4c9252fc01a0d1cf6d1a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__872d6281dc075dcc577ce9cabec802da2cea997bc054ca8fdb0668849630e5a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fc70c06f193fb38e4e6d90249e8bd62e097d893ab4c70af050228d2a5ed9cb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f66d17fb53c64c3f165818fa382c8a9e949004ab3c4543b72c9a29e4c52c566)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyConfig",
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
        "location": "location",
        "name": "name",
        "target": "target",
        "custom_provider": "customProvider",
        "description": "description",
        "http_rules": "httpRules",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class GoogleNetworkSecurityAuthzPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        name: builtins.str,
        target: typing.Union["GoogleNetworkSecurityAuthzPolicyTarget", typing.Dict[builtins.str, typing.Any]],
        custom_provider: typing.Optional[typing.Union["GoogleNetworkSecurityAuthzPolicyCustomProvider", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        http_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecurityAuthzPolicyHttpRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleNetworkSecurityAuthzPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param action: When the action is CUSTOM, customProvider must be specified. When the action is ALLOW, only requests matching the policy will be allowed. When the action is DENY, only requests matching the policy will be denied. When a request arrives, the policies are evaluated in the following order: 1. If there is a CUSTOM policy that matches the request, the CUSTOM policy is evaluated using the custom authorization providers and the request is denied if the provider rejects the request. 2. If there are any DENY policies that match the request, the request is denied. 3. If there are no ALLOW policies for the resource or if any of the ALLOW policies match the request, the request is allowed. 4. Else the request is denied by default if none of the configured AuthzPolicies with ALLOW action match the request. Possible values: ["ALLOW", "DENY", "CUSTOM"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#action GoogleNetworkSecurityAuthzPolicy#action}
        :param location: The location of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#location GoogleNetworkSecurityAuthzPolicy#location}
        :param name: Identifier. Name of the AuthzPolicy resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#name GoogleNetworkSecurityAuthzPolicy#name}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#target GoogleNetworkSecurityAuthzPolicy#target}
        :param custom_provider: custom_provider block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#custom_provider GoogleNetworkSecurityAuthzPolicy#custom_provider}
        :param description: A human-readable description of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#description GoogleNetworkSecurityAuthzPolicy#description}
        :param http_rules: http_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#http_rules GoogleNetworkSecurityAuthzPolicy#http_rules}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#id GoogleNetworkSecurityAuthzPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of labels associated with the AuthzExtension resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#labels GoogleNetworkSecurityAuthzPolicy#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#project GoogleNetworkSecurityAuthzPolicy#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#timeouts GoogleNetworkSecurityAuthzPolicy#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(target, dict):
            target = GoogleNetworkSecurityAuthzPolicyTarget(**target)
        if isinstance(custom_provider, dict):
            custom_provider = GoogleNetworkSecurityAuthzPolicyCustomProvider(**custom_provider)
        if isinstance(timeouts, dict):
            timeouts = GoogleNetworkSecurityAuthzPolicyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__965967f19aeecd0bc8438c35c0da171aff0717847a6d55819b4d59293e87beae)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument custom_provider", value=custom_provider, expected_type=type_hints["custom_provider"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument http_rules", value=http_rules, expected_type=type_hints["http_rules"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "location": location,
            "name": name,
            "target": target,
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
        if custom_provider is not None:
            self._values["custom_provider"] = custom_provider
        if description is not None:
            self._values["description"] = description
        if http_rules is not None:
            self._values["http_rules"] = http_rules
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
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
    def action(self) -> builtins.str:
        '''When the action is CUSTOM, customProvider must be specified.

        When the action is ALLOW, only requests matching the policy will be allowed.
        When the action is DENY, only requests matching the policy will be denied.

        When a request arrives, the policies are evaluated in the following order:

        1. If there is a CUSTOM policy that matches the request, the CUSTOM policy is evaluated using the custom authorization providers and the request is denied if the provider rejects the request.
        2. If there are any DENY policies that match the request, the request is denied.
        3. If there are no ALLOW policies for the resource or if any of the ALLOW policies match the request, the request is allowed.
        4. Else the request is denied by default if none of the configured AuthzPolicies with ALLOW action match the request. Possible values: ["ALLOW", "DENY", "CUSTOM"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#action GoogleNetworkSecurityAuthzPolicy#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#location GoogleNetworkSecurityAuthzPolicy#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Identifier. Name of the AuthzPolicy resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#name GoogleNetworkSecurityAuthzPolicy#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> "GoogleNetworkSecurityAuthzPolicyTarget":
        '''target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#target GoogleNetworkSecurityAuthzPolicy#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast("GoogleNetworkSecurityAuthzPolicyTarget", result)

    @builtins.property
    def custom_provider(
        self,
    ) -> typing.Optional["GoogleNetworkSecurityAuthzPolicyCustomProvider"]:
        '''custom_provider block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#custom_provider GoogleNetworkSecurityAuthzPolicy#custom_provider}
        '''
        result = self._values.get("custom_provider")
        return typing.cast(typing.Optional["GoogleNetworkSecurityAuthzPolicyCustomProvider"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-readable description of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#description GoogleNetworkSecurityAuthzPolicy#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_rules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRules"]]]:
        '''http_rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#http_rules GoogleNetworkSecurityAuthzPolicy#http_rules}
        '''
        result = self._values.get("http_rules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRules"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#id GoogleNetworkSecurityAuthzPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Set of labels associated with the AuthzExtension resource.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#labels GoogleNetworkSecurityAuthzPolicy#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#project GoogleNetworkSecurityAuthzPolicy#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleNetworkSecurityAuthzPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#timeouts GoogleNetworkSecurityAuthzPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleNetworkSecurityAuthzPolicyTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityAuthzPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyCustomProvider",
    jsii_struct_bases=[],
    name_mapping={"authz_extension": "authzExtension", "cloud_iap": "cloudIap"},
)
class GoogleNetworkSecurityAuthzPolicyCustomProvider:
    def __init__(
        self,
        *,
        authz_extension: typing.Optional[typing.Union["GoogleNetworkSecurityAuthzPolicyCustomProviderAuthzExtension", typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_iap: typing.Optional[typing.Union["GoogleNetworkSecurityAuthzPolicyCustomProviderCloudIap", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param authz_extension: authz_extension block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#authz_extension GoogleNetworkSecurityAuthzPolicy#authz_extension}
        :param cloud_iap: cloud_iap block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#cloud_iap GoogleNetworkSecurityAuthzPolicy#cloud_iap}
        '''
        if isinstance(authz_extension, dict):
            authz_extension = GoogleNetworkSecurityAuthzPolicyCustomProviderAuthzExtension(**authz_extension)
        if isinstance(cloud_iap, dict):
            cloud_iap = GoogleNetworkSecurityAuthzPolicyCustomProviderCloudIap(**cloud_iap)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7a3e33662399748bed801374c1e9f01aa38416e412e397e571a25aebe56faf0)
            check_type(argname="argument authz_extension", value=authz_extension, expected_type=type_hints["authz_extension"])
            check_type(argname="argument cloud_iap", value=cloud_iap, expected_type=type_hints["cloud_iap"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authz_extension is not None:
            self._values["authz_extension"] = authz_extension
        if cloud_iap is not None:
            self._values["cloud_iap"] = cloud_iap

    @builtins.property
    def authz_extension(
        self,
    ) -> typing.Optional["GoogleNetworkSecurityAuthzPolicyCustomProviderAuthzExtension"]:
        '''authz_extension block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#authz_extension GoogleNetworkSecurityAuthzPolicy#authz_extension}
        '''
        result = self._values.get("authz_extension")
        return typing.cast(typing.Optional["GoogleNetworkSecurityAuthzPolicyCustomProviderAuthzExtension"], result)

    @builtins.property
    def cloud_iap(
        self,
    ) -> typing.Optional["GoogleNetworkSecurityAuthzPolicyCustomProviderCloudIap"]:
        '''cloud_iap block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#cloud_iap GoogleNetworkSecurityAuthzPolicy#cloud_iap}
        '''
        result = self._values.get("cloud_iap")
        return typing.cast(typing.Optional["GoogleNetworkSecurityAuthzPolicyCustomProviderCloudIap"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityAuthzPolicyCustomProvider(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyCustomProviderAuthzExtension",
    jsii_struct_bases=[],
    name_mapping={"resources": "resources"},
)
class GoogleNetworkSecurityAuthzPolicyCustomProviderAuthzExtension:
    def __init__(self, *, resources: typing.Sequence[builtins.str]) -> None:
        '''
        :param resources: A list of references to authorization extensions that will be invoked for requests matching this policy. Limited to 1 custom provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#resources GoogleNetworkSecurityAuthzPolicy#resources}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b81cb563f1b7e6422b9a3563594739bf480fdafc648d9611bb0fbccadaca7b8)
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resources": resources,
        }

    @builtins.property
    def resources(self) -> typing.List[builtins.str]:
        '''A list of references to authorization extensions that will be invoked for requests matching this policy.

        Limited to 1 custom provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#resources GoogleNetworkSecurityAuthzPolicy#resources}
        '''
        result = self._values.get("resources")
        assert result is not None, "Required property 'resources' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityAuthzPolicyCustomProviderAuthzExtension(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkSecurityAuthzPolicyCustomProviderAuthzExtensionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyCustomProviderAuthzExtensionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8261726fe405cc41ad2284fea9543bf9360ec9a18e5345492ee5125d4f3c6665)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resources"))

    @resources.setter
    def resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5407b814a6e84d825070a8c8873c66fb6e72935f4efe4f30cc8e04f755beb7e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityAuthzPolicyCustomProviderAuthzExtension]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityAuthzPolicyCustomProviderAuthzExtension], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkSecurityAuthzPolicyCustomProviderAuthzExtension],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc26b3655e0783f1d5e9f4e338ba0a7851e2ac272c1830b9f6fcd636b29a1327)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyCustomProviderCloudIap",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleNetworkSecurityAuthzPolicyCustomProviderCloudIap:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Enable Cloud IAP at the AuthzPolicy level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#enabled GoogleNetworkSecurityAuthzPolicy#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e3baead72eef489eeebacbb277094f933803e9e28656c44a492d9371435ab08)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Enable Cloud IAP at the AuthzPolicy level.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#enabled GoogleNetworkSecurityAuthzPolicy#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityAuthzPolicyCustomProviderCloudIap(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkSecurityAuthzPolicyCustomProviderCloudIapOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyCustomProviderCloudIapOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__14927affea671bc1c296ca35aa06801c01185716ea0f7ee51126ebd1c3a49d38)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6715d7d2072650ee8cf6c59a4306e97c16fe18a62c78754762a282c4e4fe50e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityAuthzPolicyCustomProviderCloudIap]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityAuthzPolicyCustomProviderCloudIap], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkSecurityAuthzPolicyCustomProviderCloudIap],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cca588f91b93513e73b802c6f16874fc25377b745fd2f1790de68140b4c9541)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkSecurityAuthzPolicyCustomProviderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyCustomProviderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27d9b27d974b320c36ca729a00082c2e10b90758118d0fc1f8b52b7bf72df12b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuthzExtension")
    def put_authz_extension(self, *, resources: typing.Sequence[builtins.str]) -> None:
        '''
        :param resources: A list of references to authorization extensions that will be invoked for requests matching this policy. Limited to 1 custom provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#resources GoogleNetworkSecurityAuthzPolicy#resources}
        '''
        value = GoogleNetworkSecurityAuthzPolicyCustomProviderAuthzExtension(
            resources=resources
        )

        return typing.cast(None, jsii.invoke(self, "putAuthzExtension", [value]))

    @jsii.member(jsii_name="putCloudIap")
    def put_cloud_iap(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Enable Cloud IAP at the AuthzPolicy level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#enabled GoogleNetworkSecurityAuthzPolicy#enabled}
        '''
        value = GoogleNetworkSecurityAuthzPolicyCustomProviderCloudIap(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putCloudIap", [value]))

    @jsii.member(jsii_name="resetAuthzExtension")
    def reset_authz_extension(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthzExtension", []))

    @jsii.member(jsii_name="resetCloudIap")
    def reset_cloud_iap(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudIap", []))

    @builtins.property
    @jsii.member(jsii_name="authzExtension")
    def authz_extension(
        self,
    ) -> GoogleNetworkSecurityAuthzPolicyCustomProviderAuthzExtensionOutputReference:
        return typing.cast(GoogleNetworkSecurityAuthzPolicyCustomProviderAuthzExtensionOutputReference, jsii.get(self, "authzExtension"))

    @builtins.property
    @jsii.member(jsii_name="cloudIap")
    def cloud_iap(
        self,
    ) -> GoogleNetworkSecurityAuthzPolicyCustomProviderCloudIapOutputReference:
        return typing.cast(GoogleNetworkSecurityAuthzPolicyCustomProviderCloudIapOutputReference, jsii.get(self, "cloudIap"))

    @builtins.property
    @jsii.member(jsii_name="authzExtensionInput")
    def authz_extension_input(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityAuthzPolicyCustomProviderAuthzExtension]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityAuthzPolicyCustomProviderAuthzExtension], jsii.get(self, "authzExtensionInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudIapInput")
    def cloud_iap_input(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityAuthzPolicyCustomProviderCloudIap]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityAuthzPolicyCustomProviderCloudIap], jsii.get(self, "cloudIapInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityAuthzPolicyCustomProvider]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityAuthzPolicyCustomProvider], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkSecurityAuthzPolicyCustomProvider],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b9b333cfbfe6ee0c22e04bca2020347f62e84ba0655f6f7cfab29de71846661)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRules",
    jsii_struct_bases=[],
    name_mapping={"from_": "from", "to": "to", "when": "when"},
)
class GoogleNetworkSecurityAuthzPolicyHttpRules:
    def __init__(
        self,
        *,
        from_: typing.Optional[typing.Union["GoogleNetworkSecurityAuthzPolicyHttpRulesFrom", typing.Dict[builtins.str, typing.Any]]] = None,
        to: typing.Optional[typing.Union["GoogleNetworkSecurityAuthzPolicyHttpRulesTo", typing.Dict[builtins.str, typing.Any]]] = None,
        when: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param from_: from block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#from GoogleNetworkSecurityAuthzPolicy#from}
        :param to: to block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#to GoogleNetworkSecurityAuthzPolicy#to}
        :param when: CEL expression that describes the conditions to be satisfied for the action. The result of the CEL expression is ANDed with the from and to. Refer to the CEL language reference for a list of available attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#when GoogleNetworkSecurityAuthzPolicy#when}
        '''
        if isinstance(from_, dict):
            from_ = GoogleNetworkSecurityAuthzPolicyHttpRulesFrom(**from_)
        if isinstance(to, dict):
            to = GoogleNetworkSecurityAuthzPolicyHttpRulesTo(**to)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fac68984474e7339179fd0531d76f76e8ba93c84eac2b82bc9b5079f80e8eef)
            check_type(argname="argument from_", value=from_, expected_type=type_hints["from_"])
            check_type(argname="argument to", value=to, expected_type=type_hints["to"])
            check_type(argname="argument when", value=when, expected_type=type_hints["when"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if from_ is not None:
            self._values["from_"] = from_
        if to is not None:
            self._values["to"] = to
        if when is not None:
            self._values["when"] = when

    @builtins.property
    def from_(self) -> typing.Optional["GoogleNetworkSecurityAuthzPolicyHttpRulesFrom"]:
        '''from block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#from GoogleNetworkSecurityAuthzPolicy#from}
        '''
        result = self._values.get("from_")
        return typing.cast(typing.Optional["GoogleNetworkSecurityAuthzPolicyHttpRulesFrom"], result)

    @builtins.property
    def to(self) -> typing.Optional["GoogleNetworkSecurityAuthzPolicyHttpRulesTo"]:
        '''to block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#to GoogleNetworkSecurityAuthzPolicy#to}
        '''
        result = self._values.get("to")
        return typing.cast(typing.Optional["GoogleNetworkSecurityAuthzPolicyHttpRulesTo"], result)

    @builtins.property
    def when(self) -> typing.Optional[builtins.str]:
        '''CEL expression that describes the conditions to be satisfied for the action.

        The result of the CEL expression is ANDed with the from and to. Refer to the CEL language reference for a list of available attributes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#when GoogleNetworkSecurityAuthzPolicy#when}
        '''
        result = self._values.get("when")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityAuthzPolicyHttpRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesFrom",
    jsii_struct_bases=[],
    name_mapping={"not_sources": "notSources", "sources": "sources"},
)
class GoogleNetworkSecurityAuthzPolicyHttpRulesFrom:
    def __init__(
        self,
        *,
        not_sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSources", typing.Dict[builtins.str, typing.Any]]]]] = None,
        sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecurityAuthzPolicyHttpRulesFromSources", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param not_sources: not_sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#not_sources GoogleNetworkSecurityAuthzPolicy#not_sources}
        :param sources: sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#sources GoogleNetworkSecurityAuthzPolicy#sources}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__938438547a41462aff0ffb5c14b87a30a27cdc0b10f824240bdb0e0197640d4f)
            check_type(argname="argument not_sources", value=not_sources, expected_type=type_hints["not_sources"])
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if not_sources is not None:
            self._values["not_sources"] = not_sources
        if sources is not None:
            self._values["sources"] = sources

    @builtins.property
    def not_sources(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSources"]]]:
        '''not_sources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#not_sources GoogleNetworkSecurityAuthzPolicy#not_sources}
        '''
        result = self._values.get("not_sources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSources"]]], result)

    @builtins.property
    def sources(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesFromSources"]]]:
        '''sources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#sources GoogleNetworkSecurityAuthzPolicy#sources}
        '''
        result = self._values.get("sources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesFromSources"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityAuthzPolicyHttpRulesFrom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSources",
    jsii_struct_bases=[],
    name_mapping={"principals": "principals", "resources": "resources"},
)
class GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSources:
    def __init__(
        self,
        *,
        principals: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param principals: principals block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#principals GoogleNetworkSecurityAuthzPolicy#principals}
        :param resources: resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#resources GoogleNetworkSecurityAuthzPolicy#resources}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7aa458c07a7714e32a0fb8484bbad3fa5d931c84089a2c600e046cbb45b86ee)
            check_type(argname="argument principals", value=principals, expected_type=type_hints["principals"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if principals is not None:
            self._values["principals"] = principals
        if resources is not None:
            self._values["resources"] = resources

    @builtins.property
    def principals(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals"]]]:
        '''principals block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#principals GoogleNetworkSecurityAuthzPolicy#principals}
        '''
        result = self._values.get("principals")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals"]]], result)

    @builtins.property
    def resources(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources"]]]:
        '''resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#resources GoogleNetworkSecurityAuthzPolicy#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bba00a33d9a497362ec71fae8e22df0a05dc98b3627aed55c5cca1f49e2fae41)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71208460ca486315b21748a23e8b62dd27b38e99e2b1e60ddb0fd2c416fc27bb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b634f4c2ecc3c64e910a757986c7a6df5984e4f96ec230855523c1003d03b4f0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__26fd81604d8ff7628382f4a36c3b46258f885dce34dfea6ae51089d8ed4278d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__45468619c08ef13054c31a167c3858df4a6894d0d88caf2c32d08e3903ac7d9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fadab3f967a32e79e9054c87da9b80212596ae70e5168b6a71f853bb6d5b5fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7688d7f9a69da207414930006f51b6cc02d70306f7d1a4b302632270efbd03b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPrincipals")
    def put_principals(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a2333e781f45581d8d7692f982760d1defb718e8fd4c1bc6ce27d7de3431881)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPrincipals", [value]))

    @jsii.member(jsii_name="putResources")
    def put_resources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8297536b1310013081bcf66e81ff8e24155475eab950832b6be8f58361425ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResources", [value]))

    @jsii.member(jsii_name="resetPrincipals")
    def reset_principals(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrincipals", []))

    @jsii.member(jsii_name="resetResources")
    def reset_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResources", []))

    @builtins.property
    @jsii.member(jsii_name="principals")
    def principals(
        self,
    ) -> "GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipalsList":
        return typing.cast("GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipalsList", jsii.get(self, "principals"))

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(
        self,
    ) -> "GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesList":
        return typing.cast("GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesList", jsii.get(self, "resources"))

    @builtins.property
    @jsii.member(jsii_name="principalsInput")
    def principals_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals"]]], jsii.get(self, "principalsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources"]]], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed3aa5b39c6f1d8957808775e005c66db0a6ba72f7873beace6e9c943bf6b62a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals",
    jsii_struct_bases=[],
    name_mapping={
        "contains": "contains",
        "exact": "exact",
        "ignore_case": "ignoreCase",
        "prefix": "prefix",
        "suffix": "suffix",
    },
)
class GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals:
    def __init__(
        self,
        *,
        contains: typing.Optional[builtins.str] = None,
        exact: typing.Optional[builtins.str] = None,
        ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prefix: typing.Optional[builtins.str] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param contains: The input string must have the substring specified here. Note: empty contains match is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc.def Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#contains GoogleNetworkSecurityAuthzPolicy#contains}
        :param exact: The input string must match exactly the string specified here. Examples: * abc only matches the value abc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#exact GoogleNetworkSecurityAuthzPolicy#exact}
        :param ignore_case: If true, indicates the exact/prefix/suffix/contains matching should be case insensitive. For example, the matcher data will match both input string Data and data if set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#ignore_case GoogleNetworkSecurityAuthzPolicy#ignore_case}
        :param prefix: The input string must have the prefix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value abc.xyz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#prefix GoogleNetworkSecurityAuthzPolicy#prefix}
        :param suffix: The input string must have the suffix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#suffix GoogleNetworkSecurityAuthzPolicy#suffix}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12f3580c1115e434184a00145c8a2912f56a0b154385f35d566e050e9bb6a899)
            check_type(argname="argument contains", value=contains, expected_type=type_hints["contains"])
            check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
            check_type(argname="argument ignore_case", value=ignore_case, expected_type=type_hints["ignore_case"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument suffix", value=suffix, expected_type=type_hints["suffix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if contains is not None:
            self._values["contains"] = contains
        if exact is not None:
            self._values["exact"] = exact
        if ignore_case is not None:
            self._values["ignore_case"] = ignore_case
        if prefix is not None:
            self._values["prefix"] = prefix
        if suffix is not None:
            self._values["suffix"] = suffix

    @builtins.property
    def contains(self) -> typing.Optional[builtins.str]:
        '''The input string must have the substring specified here.

        Note: empty contains match is not allowed, please use regex instead.
        Examples:

        - abc matches the value xyz.abc.def

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#contains GoogleNetworkSecurityAuthzPolicy#contains}
        '''
        result = self._values.get("contains")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exact(self) -> typing.Optional[builtins.str]:
        '''The input string must match exactly the string specified here. Examples: * abc only matches the value abc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#exact GoogleNetworkSecurityAuthzPolicy#exact}
        '''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, indicates the exact/prefix/suffix/contains matching should be case insensitive.

        For example, the matcher data will match both input string Data and data if set to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#ignore_case GoogleNetworkSecurityAuthzPolicy#ignore_case}
        '''
        result = self._values.get("ignore_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the prefix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value abc.xyz

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#prefix GoogleNetworkSecurityAuthzPolicy#prefix}
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suffix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the suffix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value xyz.abc

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#suffix GoogleNetworkSecurityAuthzPolicy#suffix}
        '''
        result = self._values.get("suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipalsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipalsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af2f23e2d51a18c595ef2fff1da7d4a3a9db4c5cf97aaff3b9cc812b059dc62d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipalsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f39f8a2750b63786991c0e0e11f73aab6f7b3721a6e00bbaae215124147efbe)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipalsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d51f4120ba051a7c308f969a1808cbd148b23f5f61618f12d4671ad73b28af3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__36f9fd813a7eb06b95edddad0b0a8e637c04985a58700854f9f1cdd231c53c2b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1edc5ef65fa68599b9330644409211842da2fbcf1c4b09769f762dbb6ee8674c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0dd47067ac2c634e3bf5395adb2bdf83410604b8cc6b4f66ec054047e7a1d31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipalsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipalsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9875645e013be612878f586911f692f436bc5743d01d7ab3afc6bc38958d73f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetContains")
    def reset_contains(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContains", []))

    @jsii.member(jsii_name="resetExact")
    def reset_exact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExact", []))

    @jsii.member(jsii_name="resetIgnoreCase")
    def reset_ignore_case(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreCase", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @jsii.member(jsii_name="resetSuffix")
    def reset_suffix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuffix", []))

    @builtins.property
    @jsii.member(jsii_name="containsInput")
    def contains_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containsInput"))

    @builtins.property
    @jsii.member(jsii_name="exactInput")
    def exact_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exactInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreCaseInput")
    def ignore_case_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreCaseInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="suffixInput")
    def suffix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "suffixInput"))

    @builtins.property
    @jsii.member(jsii_name="contains")
    def contains(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contains"))

    @contains.setter
    def contains(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7928dab76ef2fb51e2a40962baaf6ba78c059efa8c3b458ce1129fd36cc32539)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exact")
    def exact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exact"))

    @exact.setter
    def exact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44ec3e8e44ccaa64849eaf440d754f101ed35c485198df7e531f8770c5d5c3b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreCase")
    def ignore_case(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreCase"))

    @ignore_case.setter
    def ignore_case(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fca23b87cb961a5560ea96be7db5981009aca58b8cc95ccbc8bebea2c9f9a7f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreCase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef4fcfb87d72d791d699b1c0930abfa139ac8e1cf4b34488ca5a62706b06b877)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suffix")
    def suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suffix"))

    @suffix.setter
    def suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d919d58691c223cba556a00591ce453ff7058b0a852e3c57796bdb6593e0cf58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53bb62878d3043a0ad95c9c3ac47b35cd93e4714233851f7848dbe7588215e29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources",
    jsii_struct_bases=[],
    name_mapping={
        "iam_service_account": "iamServiceAccount",
        "tag_value_id_set": "tagValueIdSet",
    },
)
class GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources:
    def __init__(
        self,
        *,
        iam_service_account: typing.Optional[typing.Union["GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccount", typing.Dict[builtins.str, typing.Any]]] = None,
        tag_value_id_set: typing.Optional[typing.Union["GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSet", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param iam_service_account: iam_service_account block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#iam_service_account GoogleNetworkSecurityAuthzPolicy#iam_service_account}
        :param tag_value_id_set: tag_value_id_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#tag_value_id_set GoogleNetworkSecurityAuthzPolicy#tag_value_id_set}
        '''
        if isinstance(iam_service_account, dict):
            iam_service_account = GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccount(**iam_service_account)
        if isinstance(tag_value_id_set, dict):
            tag_value_id_set = GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSet(**tag_value_id_set)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deeeb29bfcf1ff3d515e90aef13abe2c21c64901ad69e826cef9389bd613f46a)
            check_type(argname="argument iam_service_account", value=iam_service_account, expected_type=type_hints["iam_service_account"])
            check_type(argname="argument tag_value_id_set", value=tag_value_id_set, expected_type=type_hints["tag_value_id_set"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if iam_service_account is not None:
            self._values["iam_service_account"] = iam_service_account
        if tag_value_id_set is not None:
            self._values["tag_value_id_set"] = tag_value_id_set

    @builtins.property
    def iam_service_account(
        self,
    ) -> typing.Optional["GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccount"]:
        '''iam_service_account block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#iam_service_account GoogleNetworkSecurityAuthzPolicy#iam_service_account}
        '''
        result = self._values.get("iam_service_account")
        return typing.cast(typing.Optional["GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccount"], result)

    @builtins.property
    def tag_value_id_set(
        self,
    ) -> typing.Optional["GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSet"]:
        '''tag_value_id_set block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#tag_value_id_set GoogleNetworkSecurityAuthzPolicy#tag_value_id_set}
        '''
        result = self._values.get("tag_value_id_set")
        return typing.cast(typing.Optional["GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSet"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccount",
    jsii_struct_bases=[],
    name_mapping={
        "contains": "contains",
        "exact": "exact",
        "ignore_case": "ignoreCase",
        "prefix": "prefix",
        "suffix": "suffix",
    },
)
class GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccount:
    def __init__(
        self,
        *,
        contains: typing.Optional[builtins.str] = None,
        exact: typing.Optional[builtins.str] = None,
        ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prefix: typing.Optional[builtins.str] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param contains: The input string must have the substring specified here. Note: empty contains match is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc.def Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#contains GoogleNetworkSecurityAuthzPolicy#contains}
        :param exact: The input string must match exactly the string specified here. Examples: * abc only matches the value abc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#exact GoogleNetworkSecurityAuthzPolicy#exact}
        :param ignore_case: If true, indicates the exact/prefix/suffix/contains matching should be case insensitive. For example, the matcher data will match both input string Data and data if set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#ignore_case GoogleNetworkSecurityAuthzPolicy#ignore_case}
        :param prefix: The input string must have the prefix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value abc.xyz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#prefix GoogleNetworkSecurityAuthzPolicy#prefix}
        :param suffix: The input string must have the suffix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#suffix GoogleNetworkSecurityAuthzPolicy#suffix}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d8104bdcdcff3c3ff6df871842dd05a3df8aa24a809748e50430e6dc7e81ed2)
            check_type(argname="argument contains", value=contains, expected_type=type_hints["contains"])
            check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
            check_type(argname="argument ignore_case", value=ignore_case, expected_type=type_hints["ignore_case"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument suffix", value=suffix, expected_type=type_hints["suffix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if contains is not None:
            self._values["contains"] = contains
        if exact is not None:
            self._values["exact"] = exact
        if ignore_case is not None:
            self._values["ignore_case"] = ignore_case
        if prefix is not None:
            self._values["prefix"] = prefix
        if suffix is not None:
            self._values["suffix"] = suffix

    @builtins.property
    def contains(self) -> typing.Optional[builtins.str]:
        '''The input string must have the substring specified here.

        Note: empty contains match is not allowed, please use regex instead.
        Examples:

        - abc matches the value xyz.abc.def

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#contains GoogleNetworkSecurityAuthzPolicy#contains}
        '''
        result = self._values.get("contains")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exact(self) -> typing.Optional[builtins.str]:
        '''The input string must match exactly the string specified here. Examples: * abc only matches the value abc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#exact GoogleNetworkSecurityAuthzPolicy#exact}
        '''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, indicates the exact/prefix/suffix/contains matching should be case insensitive.

        For example, the matcher data will match both input string Data and data if set to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#ignore_case GoogleNetworkSecurityAuthzPolicy#ignore_case}
        '''
        result = self._values.get("ignore_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the prefix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value abc.xyz

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#prefix GoogleNetworkSecurityAuthzPolicy#prefix}
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suffix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the suffix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value xyz.abc

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#suffix GoogleNetworkSecurityAuthzPolicy#suffix}
        '''
        result = self._values.get("suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ed26d0559cefc22861a7f1fd433f949a978df7f95cee5c766a3798659ec0db9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetContains")
    def reset_contains(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContains", []))

    @jsii.member(jsii_name="resetExact")
    def reset_exact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExact", []))

    @jsii.member(jsii_name="resetIgnoreCase")
    def reset_ignore_case(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreCase", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @jsii.member(jsii_name="resetSuffix")
    def reset_suffix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuffix", []))

    @builtins.property
    @jsii.member(jsii_name="containsInput")
    def contains_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containsInput"))

    @builtins.property
    @jsii.member(jsii_name="exactInput")
    def exact_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exactInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreCaseInput")
    def ignore_case_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreCaseInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="suffixInput")
    def suffix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "suffixInput"))

    @builtins.property
    @jsii.member(jsii_name="contains")
    def contains(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contains"))

    @contains.setter
    def contains(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81557a31d85994d4e1e1458337aad9c9de8efa5e581fa70ba23f8259c774e5cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exact")
    def exact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exact"))

    @exact.setter
    def exact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__710d09b3391acf0ebf4989da05f94633698f4173258a0c77760393ebfeff7350)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreCase")
    def ignore_case(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreCase"))

    @ignore_case.setter
    def ignore_case(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d53c5ea5f1ac18c3ec4b8b0c4402f73f4c1aa08fa3843df35eab8762f76b4a22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreCase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e427ccd47067b13f6c51cc59b20d4a4c7e284f0db0c0e3483429f6adb29e6aaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suffix")
    def suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suffix"))

    @suffix.setter
    def suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d34abdf6b402940537dbf5cfe175f7a37daee6ee7f52baebc221e89326c24464)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccount]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccount], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccount],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4de7d94812c15b9dde9a1b86a47665ecf0bd051f10172c02044dcdc1a1bfb85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__15071da1982a848f6b35a7ffae7a18b04f56eb22b576d13dab7adc202b023b20)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb8cd7a91a369ec9faa78a423844a704c8d6d02872a919a74a926cd800f5b72e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3fa13b9c809e7d2593dff002408ffe729fa585eb94fd8ffb4d591c5902d76c2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b7d9c2b3cb5209ad695c111e95422c3b1c7711d3b5efaedcfbbcc02fa3b987a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad4cfa97ab9650ae4dac43d46c8ae3a7f486d3af1624f0d7e587816129607790)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__757dfbe215d08d3d733f868ddb5489d773e46ab3d19d29512d2aac88f0c3a25c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ac61e151e756220969c61fc5fbd5d7bdc46a9752fb35bb2835ac99be3d5a4ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putIamServiceAccount")
    def put_iam_service_account(
        self,
        *,
        contains: typing.Optional[builtins.str] = None,
        exact: typing.Optional[builtins.str] = None,
        ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prefix: typing.Optional[builtins.str] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param contains: The input string must have the substring specified here. Note: empty contains match is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc.def Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#contains GoogleNetworkSecurityAuthzPolicy#contains}
        :param exact: The input string must match exactly the string specified here. Examples: * abc only matches the value abc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#exact GoogleNetworkSecurityAuthzPolicy#exact}
        :param ignore_case: If true, indicates the exact/prefix/suffix/contains matching should be case insensitive. For example, the matcher data will match both input string Data and data if set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#ignore_case GoogleNetworkSecurityAuthzPolicy#ignore_case}
        :param prefix: The input string must have the prefix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value abc.xyz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#prefix GoogleNetworkSecurityAuthzPolicy#prefix}
        :param suffix: The input string must have the suffix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#suffix GoogleNetworkSecurityAuthzPolicy#suffix}
        '''
        value = GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccount(
            contains=contains,
            exact=exact,
            ignore_case=ignore_case,
            prefix=prefix,
            suffix=suffix,
        )

        return typing.cast(None, jsii.invoke(self, "putIamServiceAccount", [value]))

    @jsii.member(jsii_name="putTagValueIdSet")
    def put_tag_value_id_set(
        self,
        *,
        ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param ids: A list of resource tag value permanent IDs to match against the resource manager tags value associated with the source VM of a request. The match follows AND semantics which means all the ids must match. Limited to 5 matches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#ids GoogleNetworkSecurityAuthzPolicy#ids}
        '''
        value = GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSet(
            ids=ids
        )

        return typing.cast(None, jsii.invoke(self, "putTagValueIdSet", [value]))

    @jsii.member(jsii_name="resetIamServiceAccount")
    def reset_iam_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIamServiceAccount", []))

    @jsii.member(jsii_name="resetTagValueIdSet")
    def reset_tag_value_id_set(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagValueIdSet", []))

    @builtins.property
    @jsii.member(jsii_name="iamServiceAccount")
    def iam_service_account(
        self,
    ) -> GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccountOutputReference:
        return typing.cast(GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccountOutputReference, jsii.get(self, "iamServiceAccount"))

    @builtins.property
    @jsii.member(jsii_name="tagValueIdSet")
    def tag_value_id_set(
        self,
    ) -> "GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSetOutputReference":
        return typing.cast("GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSetOutputReference", jsii.get(self, "tagValueIdSet"))

    @builtins.property
    @jsii.member(jsii_name="iamServiceAccountInput")
    def iam_service_account_input(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccount]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccount], jsii.get(self, "iamServiceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="tagValueIdSetInput")
    def tag_value_id_set_input(
        self,
    ) -> typing.Optional["GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSet"]:
        return typing.cast(typing.Optional["GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSet"], jsii.get(self, "tagValueIdSetInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3086c9ecc197aa99e6b2012d800b3360029ad4347140d03baa5f5e48d60a46c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSet",
    jsii_struct_bases=[],
    name_mapping={"ids": "ids"},
)
class GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSet:
    def __init__(
        self,
        *,
        ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param ids: A list of resource tag value permanent IDs to match against the resource manager tags value associated with the source VM of a request. The match follows AND semantics which means all the ids must match. Limited to 5 matches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#ids GoogleNetworkSecurityAuthzPolicy#ids}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f49909c16f382fb49c0f0fe5f5deec09556caf604bd21931e487291c3efa1f8e)
            check_type(argname="argument ids", value=ids, expected_type=type_hints["ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ids is not None:
            self._values["ids"] = ids

    @builtins.property
    def ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of resource tag value permanent IDs to match against the resource manager tags value associated with the source VM of a request.

        The match follows AND semantics which means all the ids must match.
        Limited to 5 matches.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#ids GoogleNetworkSecurityAuthzPolicy#ids}
        '''
        result = self._values.get("ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df0bba9b389404f873745060460b839b2d524f4e8fea939d189a5c330379fbc0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIds")
    def reset_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIds", []))

    @builtins.property
    @jsii.member(jsii_name="idsInput")
    def ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "idsInput"))

    @builtins.property
    @jsii.member(jsii_name="ids")
    def ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ids"))

    @ids.setter
    def ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2679520bbf00eb79abbfebbef42787d169ab5c4960300d6ff98ff14b7b214aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ids", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSet]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f732371c0e2628dc17c7b8c6ae7ef8a88f682652e633ee3e87da6da81db8620b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkSecurityAuthzPolicyHttpRulesFromOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesFromOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__459f431fd8af9ad647d06ef8e611df6f2a93695a89a28e078819345a7769b58b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNotSources")
    def put_not_sources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSources, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86cdbbe7bf4df9de5e7a0bf91b3747091601316a47bd205c95aa8330bcdcd09d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNotSources", [value]))

    @jsii.member(jsii_name="putSources")
    def put_sources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecurityAuthzPolicyHttpRulesFromSources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e019253b86dfbaa2fa445528832864e2b7f0ed8d212cb2d48af68536ee010d88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSources", [value]))

    @jsii.member(jsii_name="resetNotSources")
    def reset_not_sources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotSources", []))

    @jsii.member(jsii_name="resetSources")
    def reset_sources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSources", []))

    @builtins.property
    @jsii.member(jsii_name="notSources")
    def not_sources(
        self,
    ) -> GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesList:
        return typing.cast(GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesList, jsii.get(self, "notSources"))

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(self) -> "GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesList":
        return typing.cast("GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesList", jsii.get(self, "sources"))

    @builtins.property
    @jsii.member(jsii_name="notSourcesInput")
    def not_sources_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSources]]], jsii.get(self, "notSourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcesInput")
    def sources_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesFromSources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesFromSources"]]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesFrom]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesFrom], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesFrom],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e6f79de503399bc7a93ff4799c5a9d4b515afc339bd15328bbfaadba7b5b098)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesFromSources",
    jsii_struct_bases=[],
    name_mapping={"principals": "principals", "resources": "resources"},
)
class GoogleNetworkSecurityAuthzPolicyHttpRulesFromSources:
    def __init__(
        self,
        *,
        principals: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResources", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param principals: principals block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#principals GoogleNetworkSecurityAuthzPolicy#principals}
        :param resources: resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#resources GoogleNetworkSecurityAuthzPolicy#resources}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2bbf812bf0e8c6d6af9a69a54600141869e8fc3fdff649cb0903fe34f45a256)
            check_type(argname="argument principals", value=principals, expected_type=type_hints["principals"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if principals is not None:
            self._values["principals"] = principals
        if resources is not None:
            self._values["resources"] = resources

    @builtins.property
    def principals(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals"]]]:
        '''principals block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#principals GoogleNetworkSecurityAuthzPolicy#principals}
        '''
        result = self._values.get("principals")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals"]]], result)

    @builtins.property
    def resources(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResources"]]]:
        '''resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#resources GoogleNetworkSecurityAuthzPolicy#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResources"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityAuthzPolicyHttpRulesFromSources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ab3c168df2ba81e86ac3d2c327ef91d143f7c739f351de7f7a8899d9381cb34)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9da4f2936283164c56bf0bb3174af8886a7b792c5a8f01316a018ee390bfc951)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__579da74c65fb705f6865f3f7936cc88b360e9d74d0030905b5a426a0be06931e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a591cf2510a681939067abef855ab3ebc1c3b58318dcf3e7dca70a65d5ab0e6c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__093d82598c9640e300436eb42966800b32c40b08f300b2e8accbac59a2bbd218)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesFromSources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesFromSources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesFromSources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb94fa6a02f2db03f4c53587bd1ba62f4b88439cab30930b37f3d4116ac03513)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d861ebbbf1e2f080710562ce41ec01a635c14de936bd673521284254c83aeb7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPrincipals")
    def put_principals(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a03dcee5b3f3475d75501ba5dce8df566c83279eac83e2f0da9f6730dd14c27a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPrincipals", [value]))

    @jsii.member(jsii_name="putResources")
    def put_resources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dab8aa70ae2e859229085feec2321640bf390b87df9f8099f9d8c1ef08dc703)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResources", [value]))

    @jsii.member(jsii_name="resetPrincipals")
    def reset_principals(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrincipals", []))

    @jsii.member(jsii_name="resetResources")
    def reset_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResources", []))

    @builtins.property
    @jsii.member(jsii_name="principals")
    def principals(
        self,
    ) -> "GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipalsList":
        return typing.cast("GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipalsList", jsii.get(self, "principals"))

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(
        self,
    ) -> "GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesList":
        return typing.cast("GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesList", jsii.get(self, "resources"))

    @builtins.property
    @jsii.member(jsii_name="principalsInput")
    def principals_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals"]]], jsii.get(self, "principalsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResources"]]], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesFromSources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesFromSources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesFromSources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bc9eafa7e3691d60146d2177270187f31775b13b9c556f9c08a482c5973e05e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals",
    jsii_struct_bases=[],
    name_mapping={
        "contains": "contains",
        "exact": "exact",
        "ignore_case": "ignoreCase",
        "prefix": "prefix",
        "suffix": "suffix",
    },
)
class GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals:
    def __init__(
        self,
        *,
        contains: typing.Optional[builtins.str] = None,
        exact: typing.Optional[builtins.str] = None,
        ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prefix: typing.Optional[builtins.str] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param contains: The input string must have the substring specified here. Note: empty contains match is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc.def Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#contains GoogleNetworkSecurityAuthzPolicy#contains}
        :param exact: The input string must match exactly the string specified here. Examples: * abc only matches the value abc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#exact GoogleNetworkSecurityAuthzPolicy#exact}
        :param ignore_case: If true, indicates the exact/prefix/suffix/contains matching should be case insensitive. For example, the matcher data will match both input string Data and data if set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#ignore_case GoogleNetworkSecurityAuthzPolicy#ignore_case}
        :param prefix: The input string must have the prefix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value abc.xyz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#prefix GoogleNetworkSecurityAuthzPolicy#prefix}
        :param suffix: The input string must have the suffix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#suffix GoogleNetworkSecurityAuthzPolicy#suffix}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__725d5aa6c2f5ee0d1a0ab5812fdf074f123d52fb7619168e660c756b604fc9c8)
            check_type(argname="argument contains", value=contains, expected_type=type_hints["contains"])
            check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
            check_type(argname="argument ignore_case", value=ignore_case, expected_type=type_hints["ignore_case"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument suffix", value=suffix, expected_type=type_hints["suffix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if contains is not None:
            self._values["contains"] = contains
        if exact is not None:
            self._values["exact"] = exact
        if ignore_case is not None:
            self._values["ignore_case"] = ignore_case
        if prefix is not None:
            self._values["prefix"] = prefix
        if suffix is not None:
            self._values["suffix"] = suffix

    @builtins.property
    def contains(self) -> typing.Optional[builtins.str]:
        '''The input string must have the substring specified here.

        Note: empty contains match is not allowed, please use regex instead.
        Examples:

        - abc matches the value xyz.abc.def

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#contains GoogleNetworkSecurityAuthzPolicy#contains}
        '''
        result = self._values.get("contains")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exact(self) -> typing.Optional[builtins.str]:
        '''The input string must match exactly the string specified here. Examples: * abc only matches the value abc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#exact GoogleNetworkSecurityAuthzPolicy#exact}
        '''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, indicates the exact/prefix/suffix/contains matching should be case insensitive.

        For example, the matcher data will match both input string Data and data if set to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#ignore_case GoogleNetworkSecurityAuthzPolicy#ignore_case}
        '''
        result = self._values.get("ignore_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the prefix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value abc.xyz

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#prefix GoogleNetworkSecurityAuthzPolicy#prefix}
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suffix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the suffix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value xyz.abc

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#suffix GoogleNetworkSecurityAuthzPolicy#suffix}
        '''
        result = self._values.get("suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipalsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipalsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d12d445d7db8d1ed0d03e345cd0d4ba6cff45e476f2b53c0714bf50e43d4932e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipalsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0941cc1f0248c7681fbf2df26585e06077a8e5301adec89a6a6d2b80dcfc030f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipalsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7a7124756d86e966969f8ca3833bf677a45d42ab3c5af9b1e5c87febb3bb64b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b2d1ffd693d6e1842d0b079711728179980c8f7819880bc08fe7880a70caca5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9f4816a699b58515fc7b31b3c106470f8b2734a6c5273951b806693852b283d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0b5ae02d1e017a73682c191a8fcfe3baa3e2be81ae35d37484abcf564365058)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipalsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipalsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__21dafd9c449443d10b0b6de42ef0faedc348e9c2e76eec6cb5d325d64f32f679)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetContains")
    def reset_contains(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContains", []))

    @jsii.member(jsii_name="resetExact")
    def reset_exact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExact", []))

    @jsii.member(jsii_name="resetIgnoreCase")
    def reset_ignore_case(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreCase", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @jsii.member(jsii_name="resetSuffix")
    def reset_suffix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuffix", []))

    @builtins.property
    @jsii.member(jsii_name="containsInput")
    def contains_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containsInput"))

    @builtins.property
    @jsii.member(jsii_name="exactInput")
    def exact_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exactInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreCaseInput")
    def ignore_case_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreCaseInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="suffixInput")
    def suffix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "suffixInput"))

    @builtins.property
    @jsii.member(jsii_name="contains")
    def contains(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contains"))

    @contains.setter
    def contains(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03a6bac6204af27b7291c21d7df9260f044a5450e771cc193456e21b9ff2a918)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exact")
    def exact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exact"))

    @exact.setter
    def exact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__909afd0296248d23e192d4eafadb7608af8151f2e1b62e351f6e0142aaa5f637)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreCase")
    def ignore_case(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreCase"))

    @ignore_case.setter
    def ignore_case(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d93568d1f9cb312e506a5559176914401e9c360798c8a97b4149a3441acf0b74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreCase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d611f1f3adef8ef477db00a2db5fea03eb1e2edf55669f88660cc3ea2d253f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suffix")
    def suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suffix"))

    @suffix.setter
    def suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be94b2868b9ed935467c4eeae1a69375d674acdb7e4fcb7fc7c7edd38ac12d60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12ceaafe63df24c877872d7c4ce4b0e6c2cd7de9fcbfd99b56f82d153be61507)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResources",
    jsii_struct_bases=[],
    name_mapping={
        "iam_service_account": "iamServiceAccount",
        "tag_value_id_set": "tagValueIdSet",
    },
)
class GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResources:
    def __init__(
        self,
        *,
        iam_service_account: typing.Optional[typing.Union["GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccount", typing.Dict[builtins.str, typing.Any]]] = None,
        tag_value_id_set: typing.Optional[typing.Union["GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSet", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param iam_service_account: iam_service_account block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#iam_service_account GoogleNetworkSecurityAuthzPolicy#iam_service_account}
        :param tag_value_id_set: tag_value_id_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#tag_value_id_set GoogleNetworkSecurityAuthzPolicy#tag_value_id_set}
        '''
        if isinstance(iam_service_account, dict):
            iam_service_account = GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccount(**iam_service_account)
        if isinstance(tag_value_id_set, dict):
            tag_value_id_set = GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSet(**tag_value_id_set)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a0c4e83d72ac978f8976597ffe2229d4232be66827881cff069a2176ce17836)
            check_type(argname="argument iam_service_account", value=iam_service_account, expected_type=type_hints["iam_service_account"])
            check_type(argname="argument tag_value_id_set", value=tag_value_id_set, expected_type=type_hints["tag_value_id_set"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if iam_service_account is not None:
            self._values["iam_service_account"] = iam_service_account
        if tag_value_id_set is not None:
            self._values["tag_value_id_set"] = tag_value_id_set

    @builtins.property
    def iam_service_account(
        self,
    ) -> typing.Optional["GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccount"]:
        '''iam_service_account block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#iam_service_account GoogleNetworkSecurityAuthzPolicy#iam_service_account}
        '''
        result = self._values.get("iam_service_account")
        return typing.cast(typing.Optional["GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccount"], result)

    @builtins.property
    def tag_value_id_set(
        self,
    ) -> typing.Optional["GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSet"]:
        '''tag_value_id_set block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#tag_value_id_set GoogleNetworkSecurityAuthzPolicy#tag_value_id_set}
        '''
        result = self._values.get("tag_value_id_set")
        return typing.cast(typing.Optional["GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSet"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccount",
    jsii_struct_bases=[],
    name_mapping={
        "contains": "contains",
        "exact": "exact",
        "ignore_case": "ignoreCase",
        "prefix": "prefix",
        "suffix": "suffix",
    },
)
class GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccount:
    def __init__(
        self,
        *,
        contains: typing.Optional[builtins.str] = None,
        exact: typing.Optional[builtins.str] = None,
        ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prefix: typing.Optional[builtins.str] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param contains: The input string must have the substring specified here. Note: empty contains match is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc.def Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#contains GoogleNetworkSecurityAuthzPolicy#contains}
        :param exact: The input string must match exactly the string specified here. Examples: * abc only matches the value abc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#exact GoogleNetworkSecurityAuthzPolicy#exact}
        :param ignore_case: If true, indicates the exact/prefix/suffix/contains matching should be case insensitive. For example, the matcher data will match both input string Data and data if set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#ignore_case GoogleNetworkSecurityAuthzPolicy#ignore_case}
        :param prefix: The input string must have the prefix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value abc.xyz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#prefix GoogleNetworkSecurityAuthzPolicy#prefix}
        :param suffix: The input string must have the suffix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#suffix GoogleNetworkSecurityAuthzPolicy#suffix}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad33bd4ec9679e9c03cca6fa844c70e50b848aa266929bc054523a8185292aa4)
            check_type(argname="argument contains", value=contains, expected_type=type_hints["contains"])
            check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
            check_type(argname="argument ignore_case", value=ignore_case, expected_type=type_hints["ignore_case"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument suffix", value=suffix, expected_type=type_hints["suffix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if contains is not None:
            self._values["contains"] = contains
        if exact is not None:
            self._values["exact"] = exact
        if ignore_case is not None:
            self._values["ignore_case"] = ignore_case
        if prefix is not None:
            self._values["prefix"] = prefix
        if suffix is not None:
            self._values["suffix"] = suffix

    @builtins.property
    def contains(self) -> typing.Optional[builtins.str]:
        '''The input string must have the substring specified here.

        Note: empty contains match is not allowed, please use regex instead.
        Examples:

        - abc matches the value xyz.abc.def

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#contains GoogleNetworkSecurityAuthzPolicy#contains}
        '''
        result = self._values.get("contains")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exact(self) -> typing.Optional[builtins.str]:
        '''The input string must match exactly the string specified here. Examples: * abc only matches the value abc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#exact GoogleNetworkSecurityAuthzPolicy#exact}
        '''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, indicates the exact/prefix/suffix/contains matching should be case insensitive.

        For example, the matcher data will match both input string Data and data if set to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#ignore_case GoogleNetworkSecurityAuthzPolicy#ignore_case}
        '''
        result = self._values.get("ignore_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the prefix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value abc.xyz

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#prefix GoogleNetworkSecurityAuthzPolicy#prefix}
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suffix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the suffix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value xyz.abc

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#suffix GoogleNetworkSecurityAuthzPolicy#suffix}
        '''
        result = self._values.get("suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__294dd5068b4bc7173afff2e25effc738f96d885123504f106d3f0be6061384cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetContains")
    def reset_contains(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContains", []))

    @jsii.member(jsii_name="resetExact")
    def reset_exact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExact", []))

    @jsii.member(jsii_name="resetIgnoreCase")
    def reset_ignore_case(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreCase", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @jsii.member(jsii_name="resetSuffix")
    def reset_suffix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuffix", []))

    @builtins.property
    @jsii.member(jsii_name="containsInput")
    def contains_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containsInput"))

    @builtins.property
    @jsii.member(jsii_name="exactInput")
    def exact_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exactInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreCaseInput")
    def ignore_case_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreCaseInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="suffixInput")
    def suffix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "suffixInput"))

    @builtins.property
    @jsii.member(jsii_name="contains")
    def contains(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contains"))

    @contains.setter
    def contains(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24b5046e44a23234ae2df1ee46659afc84f2bb65bd9fcdceb6337e95b975a51b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exact")
    def exact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exact"))

    @exact.setter
    def exact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e674e0afe8d18d1ea58d42aac46ba4f506551cd05a18e160f8131a461ad12287)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreCase")
    def ignore_case(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreCase"))

    @ignore_case.setter
    def ignore_case(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54635b1f5af3c5ed5ae30c91ec03635b35b421b5a86d474ad88bd88c227d18ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreCase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1badd1c2099ff9dec4a99758141fb341335861d19fcf63948f2636accf781ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suffix")
    def suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suffix"))

    @suffix.setter
    def suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68e70ea6756e9b71b1f9d2f18468bd05be92aed9c9e185800b82dff69441ae7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccount]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccount], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccount],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__740a8344b590d2a2c2000c7b8d50cd7804370f6e94650ceb97739512b12edcbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd04521cecacb4cb79cfafefb45b69f20534e9f5564288128c9fb26a7b99a9b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__827e500ca289014a5dec09e4d65ed55d5a13cac269e64f239bdbe65b8756cb77)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__249dbd4142562752381ea37b280d3d0678cda420ed7a28728c57974fab49b673)
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
            type_hints = typing.get_type_hints(_typecheckingstub__69258a71c1fc69737b7e13807e0d0a181960f8651e7314c02a85c537de880b6e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f3630870146ea88dd17e304767d1bed5f212128e931c99b6ffb466af779489c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c899d4e9c5257a9c8adc23fcd72ef264fbd0dc1f51d9d2d283b7607cebbc34d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6ce1c2799beba56cac031ad4b8d23736488130ee0c39885b58e9ae93590dc90)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putIamServiceAccount")
    def put_iam_service_account(
        self,
        *,
        contains: typing.Optional[builtins.str] = None,
        exact: typing.Optional[builtins.str] = None,
        ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prefix: typing.Optional[builtins.str] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param contains: The input string must have the substring specified here. Note: empty contains match is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc.def Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#contains GoogleNetworkSecurityAuthzPolicy#contains}
        :param exact: The input string must match exactly the string specified here. Examples: * abc only matches the value abc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#exact GoogleNetworkSecurityAuthzPolicy#exact}
        :param ignore_case: If true, indicates the exact/prefix/suffix/contains matching should be case insensitive. For example, the matcher data will match both input string Data and data if set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#ignore_case GoogleNetworkSecurityAuthzPolicy#ignore_case}
        :param prefix: The input string must have the prefix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value abc.xyz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#prefix GoogleNetworkSecurityAuthzPolicy#prefix}
        :param suffix: The input string must have the suffix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#suffix GoogleNetworkSecurityAuthzPolicy#suffix}
        '''
        value = GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccount(
            contains=contains,
            exact=exact,
            ignore_case=ignore_case,
            prefix=prefix,
            suffix=suffix,
        )

        return typing.cast(None, jsii.invoke(self, "putIamServiceAccount", [value]))

    @jsii.member(jsii_name="putTagValueIdSet")
    def put_tag_value_id_set(
        self,
        *,
        ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param ids: A list of resource tag value permanent IDs to match against the resource manager tags value associated with the source VM of a request. The match follows AND semantics which means all the ids must match. Limited to 5 matches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#ids GoogleNetworkSecurityAuthzPolicy#ids}
        '''
        value = GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSet(
            ids=ids
        )

        return typing.cast(None, jsii.invoke(self, "putTagValueIdSet", [value]))

    @jsii.member(jsii_name="resetIamServiceAccount")
    def reset_iam_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIamServiceAccount", []))

    @jsii.member(jsii_name="resetTagValueIdSet")
    def reset_tag_value_id_set(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagValueIdSet", []))

    @builtins.property
    @jsii.member(jsii_name="iamServiceAccount")
    def iam_service_account(
        self,
    ) -> GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccountOutputReference:
        return typing.cast(GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccountOutputReference, jsii.get(self, "iamServiceAccount"))

    @builtins.property
    @jsii.member(jsii_name="tagValueIdSet")
    def tag_value_id_set(
        self,
    ) -> "GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSetOutputReference":
        return typing.cast("GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSetOutputReference", jsii.get(self, "tagValueIdSet"))

    @builtins.property
    @jsii.member(jsii_name="iamServiceAccountInput")
    def iam_service_account_input(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccount]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccount], jsii.get(self, "iamServiceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="tagValueIdSetInput")
    def tag_value_id_set_input(
        self,
    ) -> typing.Optional["GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSet"]:
        return typing.cast(typing.Optional["GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSet"], jsii.get(self, "tagValueIdSetInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c29738df5ead3141eb2c39522bd85405290f043fd5e5da46389deb1b987ed81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSet",
    jsii_struct_bases=[],
    name_mapping={"ids": "ids"},
)
class GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSet:
    def __init__(
        self,
        *,
        ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param ids: A list of resource tag value permanent IDs to match against the resource manager tags value associated with the source VM of a request. The match follows AND semantics which means all the ids must match. Limited to 5 matches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#ids GoogleNetworkSecurityAuthzPolicy#ids}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4be2d603c7c3c395056b714d31d68f2567c6e3afe8dc250ae08afd297439866)
            check_type(argname="argument ids", value=ids, expected_type=type_hints["ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ids is not None:
            self._values["ids"] = ids

    @builtins.property
    def ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of resource tag value permanent IDs to match against the resource manager tags value associated with the source VM of a request.

        The match follows AND semantics which means all the ids must match.
        Limited to 5 matches.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#ids GoogleNetworkSecurityAuthzPolicy#ids}
        '''
        result = self._values.get("ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__70a8be01c87dea9274720dcbc0196323cfc9920a9b96a283ae1214268c84ebf6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIds")
    def reset_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIds", []))

    @builtins.property
    @jsii.member(jsii_name="idsInput")
    def ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "idsInput"))

    @builtins.property
    @jsii.member(jsii_name="ids")
    def ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ids"))

    @ids.setter
    def ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d508056e6e609d5f872a4f8b45e0a3c1597f26766401aa7d2715c8022ad6aba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ids", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSet]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c903f60e2af2e99ee78bed983121b9740783cbbb354d5960c16258f224056fd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkSecurityAuthzPolicyHttpRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__68f14568ef055854cd138a9f56e72033e609b6f5442f299e1fcbecbfa46dfde0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkSecurityAuthzPolicyHttpRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c33988e2843c2dfae2de16b34f289f7603139450dfef12cee518c42dfefbf0fa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkSecurityAuthzPolicyHttpRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f1efcf024c211d91252c31a3ba12fdc5b4f10779ddda123a3db50f72aa4b0b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed14ded10b09906356d238ad1cedac9978587776cbac9135e9857ecd84fc5326)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d37c4fc535176a94e72b53bd8c6a41aca427e5e50a1ae5e8a5554023a2e5920c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__373a77f901dfca73a538ed3bfaf87c5673a19a115bf719070a8ba10348e737fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkSecurityAuthzPolicyHttpRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5568f5a03507e04ad508d48d152140bb431edbb4d081e9a69d3952a57e971c37)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putFrom")
    def put_from(
        self,
        *,
        not_sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
        sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesFromSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param not_sources: not_sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#not_sources GoogleNetworkSecurityAuthzPolicy#not_sources}
        :param sources: sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#sources GoogleNetworkSecurityAuthzPolicy#sources}
        '''
        value = GoogleNetworkSecurityAuthzPolicyHttpRulesFrom(
            not_sources=not_sources, sources=sources
        )

        return typing.cast(None, jsii.invoke(self, "putFrom", [value]))

    @jsii.member(jsii_name="putTo")
    def put_to(
        self,
        *,
        not_operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecurityAuthzPolicyHttpRulesToOperations", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param not_operations: not_operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#not_operations GoogleNetworkSecurityAuthzPolicy#not_operations}
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#operations GoogleNetworkSecurityAuthzPolicy#operations}
        '''
        value = GoogleNetworkSecurityAuthzPolicyHttpRulesTo(
            not_operations=not_operations, operations=operations
        )

        return typing.cast(None, jsii.invoke(self, "putTo", [value]))

    @jsii.member(jsii_name="resetFrom")
    def reset_from(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFrom", []))

    @jsii.member(jsii_name="resetTo")
    def reset_to(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTo", []))

    @jsii.member(jsii_name="resetWhen")
    def reset_when(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWhen", []))

    @builtins.property
    @jsii.member(jsii_name="from")
    def from_(self) -> GoogleNetworkSecurityAuthzPolicyHttpRulesFromOutputReference:
        return typing.cast(GoogleNetworkSecurityAuthzPolicyHttpRulesFromOutputReference, jsii.get(self, "from"))

    @builtins.property
    @jsii.member(jsii_name="to")
    def to(self) -> "GoogleNetworkSecurityAuthzPolicyHttpRulesToOutputReference":
        return typing.cast("GoogleNetworkSecurityAuthzPolicyHttpRulesToOutputReference", jsii.get(self, "to"))

    @builtins.property
    @jsii.member(jsii_name="fromInput")
    def from_input(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesFrom]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesFrom], jsii.get(self, "fromInput"))

    @builtins.property
    @jsii.member(jsii_name="toInput")
    def to_input(
        self,
    ) -> typing.Optional["GoogleNetworkSecurityAuthzPolicyHttpRulesTo"]:
        return typing.cast(typing.Optional["GoogleNetworkSecurityAuthzPolicyHttpRulesTo"], jsii.get(self, "toInput"))

    @builtins.property
    @jsii.member(jsii_name="whenInput")
    def when_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "whenInput"))

    @builtins.property
    @jsii.member(jsii_name="when")
    def when(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "when"))

    @when.setter
    def when(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__743b952e8156c7add892967339ec83426a361e06fe7fee655c1269ebf6d70889)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "when", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fb91823d37697b5eda0a5c5ff1865f013899796addab136bfa0474795717da2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesTo",
    jsii_struct_bases=[],
    name_mapping={"not_operations": "notOperations", "operations": "operations"},
)
class GoogleNetworkSecurityAuthzPolicyHttpRulesTo:
    def __init__(
        self,
        *,
        not_operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecurityAuthzPolicyHttpRulesToOperations", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param not_operations: not_operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#not_operations GoogleNetworkSecurityAuthzPolicy#not_operations}
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#operations GoogleNetworkSecurityAuthzPolicy#operations}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b78ae971647bfa85500c2c71aa498e07c93bb3eff02ef8220896146ba1dbc13f)
            check_type(argname="argument not_operations", value=not_operations, expected_type=type_hints["not_operations"])
            check_type(argname="argument operations", value=operations, expected_type=type_hints["operations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if not_operations is not None:
            self._values["not_operations"] = not_operations
        if operations is not None:
            self._values["operations"] = operations

    @builtins.property
    def not_operations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperations"]]]:
        '''not_operations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#not_operations GoogleNetworkSecurityAuthzPolicy#not_operations}
        '''
        result = self._values.get("not_operations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperations"]]], result)

    @builtins.property
    def operations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesToOperations"]]]:
        '''operations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#operations GoogleNetworkSecurityAuthzPolicy#operations}
        '''
        result = self._values.get("operations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesToOperations"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityAuthzPolicyHttpRulesTo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperations",
    jsii_struct_bases=[],
    name_mapping={
        "header_set": "headerSet",
        "hosts": "hosts",
        "methods": "methods",
        "paths": "paths",
    },
)
class GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperations:
    def __init__(
        self,
        *,
        header_set: typing.Optional[typing.Union["GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSet", typing.Dict[builtins.str, typing.Any]]] = None,
        hosts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        methods: typing.Optional[typing.Sequence[builtins.str]] = None,
        paths: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param header_set: header_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#header_set GoogleNetworkSecurityAuthzPolicy#header_set}
        :param hosts: hosts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#hosts GoogleNetworkSecurityAuthzPolicy#hosts}
        :param methods: A list of HTTP methods to match against. Each entry must be a valid HTTP method name (GET, PUT, POST, HEAD, PATCH, DELETE, OPTIONS). It only allows exact match and is always case sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#methods GoogleNetworkSecurityAuthzPolicy#methods}
        :param paths: paths block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#paths GoogleNetworkSecurityAuthzPolicy#paths}
        '''
        if isinstance(header_set, dict):
            header_set = GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSet(**header_set)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a7ff6f1a36f8610724675d895716e79b7a5639eb9a9a7b27eb8b9f9ea26e508)
            check_type(argname="argument header_set", value=header_set, expected_type=type_hints["header_set"])
            check_type(argname="argument hosts", value=hosts, expected_type=type_hints["hosts"])
            check_type(argname="argument methods", value=methods, expected_type=type_hints["methods"])
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if header_set is not None:
            self._values["header_set"] = header_set
        if hosts is not None:
            self._values["hosts"] = hosts
        if methods is not None:
            self._values["methods"] = methods
        if paths is not None:
            self._values["paths"] = paths

    @builtins.property
    def header_set(
        self,
    ) -> typing.Optional["GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSet"]:
        '''header_set block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#header_set GoogleNetworkSecurityAuthzPolicy#header_set}
        '''
        result = self._values.get("header_set")
        return typing.cast(typing.Optional["GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSet"], result)

    @builtins.property
    def hosts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts"]]]:
        '''hosts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#hosts GoogleNetworkSecurityAuthzPolicy#hosts}
        '''
        result = self._values.get("hosts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts"]]], result)

    @builtins.property
    def methods(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of HTTP methods to match against.

        Each entry must be a valid HTTP method name (GET, PUT, POST, HEAD, PATCH, DELETE, OPTIONS). It only allows exact match and is always case sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#methods GoogleNetworkSecurityAuthzPolicy#methods}
        '''
        result = self._values.get("methods")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def paths(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths"]]]:
        '''paths block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#paths GoogleNetworkSecurityAuthzPolicy#paths}
        '''
        result = self._values.get("paths")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSet",
    jsii_struct_bases=[],
    name_mapping={"headers": "headers"},
)
class GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSet:
    def __init__(
        self,
        *,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param headers: headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#headers GoogleNetworkSecurityAuthzPolicy#headers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41cde4e7dbeb2e6def23570c123bfe374f26c90d35bb6d4fe7ca91de86946eeb)
            check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if headers is not None:
            self._values["headers"] = headers

    @builtins.property
    def headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders"]]]:
        '''headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#headers GoogleNetworkSecurityAuthzPolicy#headers}
        '''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[typing.Union["GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValue", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Specifies the name of the header in the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#name GoogleNetworkSecurityAuthzPolicy#name}
        :param value: value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#value GoogleNetworkSecurityAuthzPolicy#value}
        '''
        if isinstance(value, dict):
            value = GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValue(**value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74bab4fb574aad29b395ecff9c6e72c70c6e209eed07bd5a69385da01a55ff98)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the header in the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#name GoogleNetworkSecurityAuthzPolicy#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(
        self,
    ) -> typing.Optional["GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValue"]:
        '''value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#value GoogleNetworkSecurityAuthzPolicy#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional["GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValue"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c42cc3faa1d3843d8f2f6de511f516c9e708ca28c5587f4b5966c1173d37340b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38865e0b5f111c5d7d2345e2ff574d743b1838c69e97a5cc671ad1cd5c2463b8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85a8b0cc34d649956cf6464a04234240feb25569b8948cf28c4999c3225e4fbf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d10c3fba8df75f8a882d69f70c91e7b3eab14f04cbc06ce0a0d52900085de52)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4d66dd792aff2cf97e458e48fc674ae384219da4ce95382540470da567003a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e39dd56a4d7fe9a8632828d51b4f03fb62aff4305c710bf0f7e0ef56f5c7f59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__befe9d2fc507b8f583155f4a1aaf491407699b85112022713ee0a99808121fa1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putValue")
    def put_value(
        self,
        *,
        contains: typing.Optional[builtins.str] = None,
        exact: typing.Optional[builtins.str] = None,
        ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prefix: typing.Optional[builtins.str] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param contains: The input string must have the substring specified here. Note: empty contains match is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc.def Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#contains GoogleNetworkSecurityAuthzPolicy#contains}
        :param exact: The input string must match exactly the string specified here. Examples: * abc only matches the value abc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#exact GoogleNetworkSecurityAuthzPolicy#exact}
        :param ignore_case: If true, indicates the exact/prefix/suffix/contains matching should be case insensitive. For example, the matcher data will match both input string Data and data if set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#ignore_case GoogleNetworkSecurityAuthzPolicy#ignore_case}
        :param prefix: The input string must have the prefix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value abc.xyz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#prefix GoogleNetworkSecurityAuthzPolicy#prefix}
        :param suffix: The input string must have the suffix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#suffix GoogleNetworkSecurityAuthzPolicy#suffix}
        '''
        value = GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValue(
            contains=contains,
            exact=exact,
            ignore_case=ignore_case,
            prefix=prefix,
            suffix=suffix,
        )

        return typing.cast(None, jsii.invoke(self, "putValue", [value]))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(
        self,
    ) -> "GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValueOutputReference":
        return typing.cast("GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValueOutputReference", jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(
        self,
    ) -> typing.Optional["GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValue"]:
        return typing.cast(typing.Optional["GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValue"], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64540500fc484b75bba493b0672b2230b954507b63446670841503932d1b0b1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__944b85ec830e06db7f98837d74a19c2bf130081ba511b36ebdc9c2c8b642e483)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValue",
    jsii_struct_bases=[],
    name_mapping={
        "contains": "contains",
        "exact": "exact",
        "ignore_case": "ignoreCase",
        "prefix": "prefix",
        "suffix": "suffix",
    },
)
class GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValue:
    def __init__(
        self,
        *,
        contains: typing.Optional[builtins.str] = None,
        exact: typing.Optional[builtins.str] = None,
        ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prefix: typing.Optional[builtins.str] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param contains: The input string must have the substring specified here. Note: empty contains match is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc.def Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#contains GoogleNetworkSecurityAuthzPolicy#contains}
        :param exact: The input string must match exactly the string specified here. Examples: * abc only matches the value abc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#exact GoogleNetworkSecurityAuthzPolicy#exact}
        :param ignore_case: If true, indicates the exact/prefix/suffix/contains matching should be case insensitive. For example, the matcher data will match both input string Data and data if set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#ignore_case GoogleNetworkSecurityAuthzPolicy#ignore_case}
        :param prefix: The input string must have the prefix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value abc.xyz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#prefix GoogleNetworkSecurityAuthzPolicy#prefix}
        :param suffix: The input string must have the suffix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#suffix GoogleNetworkSecurityAuthzPolicy#suffix}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6bd7f114e68f63d746fb69aaa5dea73c59a83d8c159369c6e3f52a9d97ee836)
            check_type(argname="argument contains", value=contains, expected_type=type_hints["contains"])
            check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
            check_type(argname="argument ignore_case", value=ignore_case, expected_type=type_hints["ignore_case"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument suffix", value=suffix, expected_type=type_hints["suffix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if contains is not None:
            self._values["contains"] = contains
        if exact is not None:
            self._values["exact"] = exact
        if ignore_case is not None:
            self._values["ignore_case"] = ignore_case
        if prefix is not None:
            self._values["prefix"] = prefix
        if suffix is not None:
            self._values["suffix"] = suffix

    @builtins.property
    def contains(self) -> typing.Optional[builtins.str]:
        '''The input string must have the substring specified here.

        Note: empty contains match is not allowed, please use regex instead.
        Examples:

        - abc matches the value xyz.abc.def

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#contains GoogleNetworkSecurityAuthzPolicy#contains}
        '''
        result = self._values.get("contains")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exact(self) -> typing.Optional[builtins.str]:
        '''The input string must match exactly the string specified here. Examples: * abc only matches the value abc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#exact GoogleNetworkSecurityAuthzPolicy#exact}
        '''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, indicates the exact/prefix/suffix/contains matching should be case insensitive.

        For example, the matcher data will match both input string Data and data if set to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#ignore_case GoogleNetworkSecurityAuthzPolicy#ignore_case}
        '''
        result = self._values.get("ignore_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the prefix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value abc.xyz

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#prefix GoogleNetworkSecurityAuthzPolicy#prefix}
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suffix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the suffix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value xyz.abc

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#suffix GoogleNetworkSecurityAuthzPolicy#suffix}
        '''
        result = self._values.get("suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb8e3d9ff254c45ac776545708499f5f77bcc1e9313e65d0985748f94708a33b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetContains")
    def reset_contains(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContains", []))

    @jsii.member(jsii_name="resetExact")
    def reset_exact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExact", []))

    @jsii.member(jsii_name="resetIgnoreCase")
    def reset_ignore_case(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreCase", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @jsii.member(jsii_name="resetSuffix")
    def reset_suffix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuffix", []))

    @builtins.property
    @jsii.member(jsii_name="containsInput")
    def contains_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containsInput"))

    @builtins.property
    @jsii.member(jsii_name="exactInput")
    def exact_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exactInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreCaseInput")
    def ignore_case_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreCaseInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="suffixInput")
    def suffix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "suffixInput"))

    @builtins.property
    @jsii.member(jsii_name="contains")
    def contains(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contains"))

    @contains.setter
    def contains(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8adce1710680d4c35a3409366ce8648812f4545272a926ffaa21fd77b4029f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exact")
    def exact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exact"))

    @exact.setter
    def exact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__962b8ad37687efa4e544581fe8fe03e641e04d42691c738f1270ad8e3fb660f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreCase")
    def ignore_case(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreCase"))

    @ignore_case.setter
    def ignore_case(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04c715c769fd016e6b939662a2b3caaf8065bd70bd53f699a7b2b8d2b987c8fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreCase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38eff95ee58a493b54c3fcaef35ce2d68d42818e6100728ec9b5a913381a29ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suffix")
    def suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suffix"))

    @suffix.setter
    def suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c0643829289921cf49f36fea4e913ddace56e6787ad7da938dfa88657278e1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValue]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d668069558ac4219bf2dff3016fe6eca2d276ad227f7df3c7d31a4d8b16c201)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fa8f6b0a4c73786ea65df51e60491b7f26571a60e5c832c99a89d93e28b739c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHeaders")
    def put_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e09836f59b468a07ff0f4d4863c6623778d0c989216148937a19b3eaf113593)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeaders", [value]))

    @jsii.member(jsii_name="resetHeaders")
    def reset_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaders", []))

    @builtins.property
    @jsii.member(jsii_name="headers")
    def headers(
        self,
    ) -> GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersList:
        return typing.cast(GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersList, jsii.get(self, "headers"))

    @builtins.property
    @jsii.member(jsii_name="headersInput")
    def headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders]]], jsii.get(self, "headersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSet]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f24d653ee7bdcad4540b0ad0aba28ec2aa0ae4299892e7f6bb8a96d9d5da36a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts",
    jsii_struct_bases=[],
    name_mapping={
        "contains": "contains",
        "exact": "exact",
        "ignore_case": "ignoreCase",
        "prefix": "prefix",
        "suffix": "suffix",
    },
)
class GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts:
    def __init__(
        self,
        *,
        contains: typing.Optional[builtins.str] = None,
        exact: typing.Optional[builtins.str] = None,
        ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prefix: typing.Optional[builtins.str] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param contains: The input string must have the substring specified here. Note: empty contains match is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc.def Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#contains GoogleNetworkSecurityAuthzPolicy#contains}
        :param exact: The input string must match exactly the string specified here. Examples: * abc only matches the value abc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#exact GoogleNetworkSecurityAuthzPolicy#exact}
        :param ignore_case: If true, indicates the exact/prefix/suffix/contains matching should be case insensitive. For example, the matcher data will match both input string Data and data if set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#ignore_case GoogleNetworkSecurityAuthzPolicy#ignore_case}
        :param prefix: The input string must have the prefix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value abc.xyz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#prefix GoogleNetworkSecurityAuthzPolicy#prefix}
        :param suffix: The input string must have the suffix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#suffix GoogleNetworkSecurityAuthzPolicy#suffix}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8fd6f24f2f95b866bfb8208137e6ed4c4068c442cf3e7ce451796ca64686b4b)
            check_type(argname="argument contains", value=contains, expected_type=type_hints["contains"])
            check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
            check_type(argname="argument ignore_case", value=ignore_case, expected_type=type_hints["ignore_case"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument suffix", value=suffix, expected_type=type_hints["suffix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if contains is not None:
            self._values["contains"] = contains
        if exact is not None:
            self._values["exact"] = exact
        if ignore_case is not None:
            self._values["ignore_case"] = ignore_case
        if prefix is not None:
            self._values["prefix"] = prefix
        if suffix is not None:
            self._values["suffix"] = suffix

    @builtins.property
    def contains(self) -> typing.Optional[builtins.str]:
        '''The input string must have the substring specified here.

        Note: empty contains match is not allowed, please use regex instead.
        Examples:

        - abc matches the value xyz.abc.def

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#contains GoogleNetworkSecurityAuthzPolicy#contains}
        '''
        result = self._values.get("contains")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exact(self) -> typing.Optional[builtins.str]:
        '''The input string must match exactly the string specified here. Examples: * abc only matches the value abc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#exact GoogleNetworkSecurityAuthzPolicy#exact}
        '''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, indicates the exact/prefix/suffix/contains matching should be case insensitive.

        For example, the matcher data will match both input string Data and data if set to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#ignore_case GoogleNetworkSecurityAuthzPolicy#ignore_case}
        '''
        result = self._values.get("ignore_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the prefix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value abc.xyz

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#prefix GoogleNetworkSecurityAuthzPolicy#prefix}
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suffix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the suffix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value xyz.abc

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#suffix GoogleNetworkSecurityAuthzPolicy#suffix}
        '''
        result = self._values.get("suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHostsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHostsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__048e830e11b73d64d88d5b2981506c1496a6f32cada18e77243346719454c6cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHostsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e04203f6588e2aa2aae7f69f8a78e8faa89b6827fd7269a113c45526a4c47c9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHostsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b64c71670e73a5b83015f53ba39af4ed89a3ef1c65910d0cdaa494e2dfbeb644)
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
            type_hints = typing.get_type_hints(_typecheckingstub__091d8a25b883c6cf8bce100c50821b89b77f83e3603476859a5174c78b096e14)
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
            type_hints = typing.get_type_hints(_typecheckingstub__168ef3d8e423ad6407f45ceb1bbde51659a9aef0a3d2ed79c88c6de8424c5374)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6565f7d707cc676491b611f0f3041d93af53dbfceb102a94a389c526876ff78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHostsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHostsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50eb0a061332afae9902ca82461d810a5f528565b8d60abc942b36b3cb2509a9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetContains")
    def reset_contains(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContains", []))

    @jsii.member(jsii_name="resetExact")
    def reset_exact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExact", []))

    @jsii.member(jsii_name="resetIgnoreCase")
    def reset_ignore_case(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreCase", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @jsii.member(jsii_name="resetSuffix")
    def reset_suffix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuffix", []))

    @builtins.property
    @jsii.member(jsii_name="containsInput")
    def contains_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containsInput"))

    @builtins.property
    @jsii.member(jsii_name="exactInput")
    def exact_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exactInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreCaseInput")
    def ignore_case_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreCaseInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="suffixInput")
    def suffix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "suffixInput"))

    @builtins.property
    @jsii.member(jsii_name="contains")
    def contains(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contains"))

    @contains.setter
    def contains(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71c1be95af96d40b19dd238b42791bb03f14cf9cd6a6d265146a9b6d483d7bd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exact")
    def exact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exact"))

    @exact.setter
    def exact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84e5fc72b846668b6086c3742b92ca23888df4c502326d28300624c6edc21ef0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreCase")
    def ignore_case(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreCase"))

    @ignore_case.setter
    def ignore_case(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dac188eada7f07b4d93cc550b1b9453f2cfea80ecf1f7469d39e8fedeb29833f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreCase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed2be711df6f59cd704d1f39a5fc5bd31c56e85748f925c13951608c7d3fb874)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suffix")
    def suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suffix"))

    @suffix.setter
    def suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1324c9fbcb6f3b758b433d0508d310872b12b6f6d326bba83b4f54eda89a618)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba76abc9d8b2ea6490987e6eae1192d6475a1d598ebfa1511c7585124e91ae23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__56fc22dbaa5bacd499a2eb7237e94cbea6dacb0a683ac12d1015ea3de56d24cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e85a4bba93eb460de5e59f16b8950d83ba9922e3ae4f2a7c47a7ea10c43a5ab)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeee71a4e2f98c29e121e7945db986074773495554d0b6e1d35d23f3f6523625)
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
            type_hints = typing.get_type_hints(_typecheckingstub__16b17c092a16ffbb453870b458c89ddc7cbc50af2e1c99e5624559bd37345ba0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0df0eef045eb61a4d12fa1083748ebb99784f2a14ecf9398c78c37503294b13d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5d2e85035fddfefe222b8468bae32e3ffb49a1dfe719392ebb9640f0586305c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d20bc351b50934c2568c35c154351205a86d48ed904c032db7939f0212cba679)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHeaderSet")
    def put_header_set(
        self,
        *,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param headers: headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#headers GoogleNetworkSecurityAuthzPolicy#headers}
        '''
        value = GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSet(
            headers=headers
        )

        return typing.cast(None, jsii.invoke(self, "putHeaderSet", [value]))

    @jsii.member(jsii_name="putHosts")
    def put_hosts(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d93682f7951feb54092ba2741d940bf77a8edc70365f0ded38c38b162c6892df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHosts", [value]))

    @jsii.member(jsii_name="putPaths")
    def put_paths(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7165351fc5ecacfed275a6874db0768b8e0fb37ae38986bb9d3fe401390723c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPaths", [value]))

    @jsii.member(jsii_name="resetHeaderSet")
    def reset_header_set(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaderSet", []))

    @jsii.member(jsii_name="resetHosts")
    def reset_hosts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHosts", []))

    @jsii.member(jsii_name="resetMethods")
    def reset_methods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethods", []))

    @jsii.member(jsii_name="resetPaths")
    def reset_paths(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPaths", []))

    @builtins.property
    @jsii.member(jsii_name="headerSet")
    def header_set(
        self,
    ) -> GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetOutputReference:
        return typing.cast(GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetOutputReference, jsii.get(self, "headerSet"))

    @builtins.property
    @jsii.member(jsii_name="hosts")
    def hosts(
        self,
    ) -> GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHostsList:
        return typing.cast(GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHostsList, jsii.get(self, "hosts"))

    @builtins.property
    @jsii.member(jsii_name="paths")
    def paths(
        self,
    ) -> "GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsPathsList":
        return typing.cast("GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsPathsList", jsii.get(self, "paths"))

    @builtins.property
    @jsii.member(jsii_name="headerSetInput")
    def header_set_input(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSet]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSet], jsii.get(self, "headerSetInput"))

    @builtins.property
    @jsii.member(jsii_name="hostsInput")
    def hosts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts]]], jsii.get(self, "hostsInput"))

    @builtins.property
    @jsii.member(jsii_name="methodsInput")
    def methods_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "methodsInput"))

    @builtins.property
    @jsii.member(jsii_name="pathsInput")
    def paths_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths"]]], jsii.get(self, "pathsInput"))

    @builtins.property
    @jsii.member(jsii_name="methods")
    def methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "methods"))

    @methods.setter
    def methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32cc49dcad2f542b1634db6680e6b14d0952e15e7c3f6c0e167abce9627fadda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "methods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be1d31c2b51a2a0893949603afb98140b9a4bcb9ba767aa959c86465760ae5a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths",
    jsii_struct_bases=[],
    name_mapping={
        "contains": "contains",
        "exact": "exact",
        "ignore_case": "ignoreCase",
        "prefix": "prefix",
        "suffix": "suffix",
    },
)
class GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths:
    def __init__(
        self,
        *,
        contains: typing.Optional[builtins.str] = None,
        exact: typing.Optional[builtins.str] = None,
        ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prefix: typing.Optional[builtins.str] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param contains: The input string must have the substring specified here. Note: empty contains match is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc.def Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#contains GoogleNetworkSecurityAuthzPolicy#contains}
        :param exact: The input string must match exactly the string specified here. Examples: * abc only matches the value abc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#exact GoogleNetworkSecurityAuthzPolicy#exact}
        :param ignore_case: If true, indicates the exact/prefix/suffix/contains matching should be case insensitive. For example, the matcher data will match both input string Data and data if set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#ignore_case GoogleNetworkSecurityAuthzPolicy#ignore_case}
        :param prefix: The input string must have the prefix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value abc.xyz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#prefix GoogleNetworkSecurityAuthzPolicy#prefix}
        :param suffix: The input string must have the suffix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#suffix GoogleNetworkSecurityAuthzPolicy#suffix}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efd7af60d8299925c6e0bdc7b3afd7cc4c1bd1787955b913efbfea614cd65dac)
            check_type(argname="argument contains", value=contains, expected_type=type_hints["contains"])
            check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
            check_type(argname="argument ignore_case", value=ignore_case, expected_type=type_hints["ignore_case"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument suffix", value=suffix, expected_type=type_hints["suffix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if contains is not None:
            self._values["contains"] = contains
        if exact is not None:
            self._values["exact"] = exact
        if ignore_case is not None:
            self._values["ignore_case"] = ignore_case
        if prefix is not None:
            self._values["prefix"] = prefix
        if suffix is not None:
            self._values["suffix"] = suffix

    @builtins.property
    def contains(self) -> typing.Optional[builtins.str]:
        '''The input string must have the substring specified here.

        Note: empty contains match is not allowed, please use regex instead.
        Examples:

        - abc matches the value xyz.abc.def

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#contains GoogleNetworkSecurityAuthzPolicy#contains}
        '''
        result = self._values.get("contains")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exact(self) -> typing.Optional[builtins.str]:
        '''The input string must match exactly the string specified here. Examples: * abc only matches the value abc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#exact GoogleNetworkSecurityAuthzPolicy#exact}
        '''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, indicates the exact/prefix/suffix/contains matching should be case insensitive.

        For example, the matcher data will match both input string Data and data if set to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#ignore_case GoogleNetworkSecurityAuthzPolicy#ignore_case}
        '''
        result = self._values.get("ignore_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the prefix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value abc.xyz

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#prefix GoogleNetworkSecurityAuthzPolicy#prefix}
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suffix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the suffix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value xyz.abc

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#suffix GoogleNetworkSecurityAuthzPolicy#suffix}
        '''
        result = self._values.get("suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsPathsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsPathsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__408382a44dfa304d04ed16f83a813b03f55f6b7e24ae8a9d8f577414e69b06b9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsPathsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a3f041d5f5051b35cde3fa5137548058854a11c7c7c3372ccbc0dc99110a5e3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsPathsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5811c06ddf0d65dfaf01c767c975df06d5f0a8f124c4b9efe14596955b9db97)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3584ec13dddf764e11e2141ba06c324126e8deaaf775590ac8eee512b71f0089)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ceec877722e5f525a314c92507e6eaeabb460a7b7d02d36141ac352062fac90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7801c114e57cbcf515a6d12f9d6424a303af0d088e2831c0567dc86f59920212)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsPathsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsPathsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__94e92f6f2e07e5cca7820fdc16322b7e6fe991fe6b018c75b7c7ca470593b746)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetContains")
    def reset_contains(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContains", []))

    @jsii.member(jsii_name="resetExact")
    def reset_exact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExact", []))

    @jsii.member(jsii_name="resetIgnoreCase")
    def reset_ignore_case(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreCase", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @jsii.member(jsii_name="resetSuffix")
    def reset_suffix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuffix", []))

    @builtins.property
    @jsii.member(jsii_name="containsInput")
    def contains_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containsInput"))

    @builtins.property
    @jsii.member(jsii_name="exactInput")
    def exact_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exactInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreCaseInput")
    def ignore_case_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreCaseInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="suffixInput")
    def suffix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "suffixInput"))

    @builtins.property
    @jsii.member(jsii_name="contains")
    def contains(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contains"))

    @contains.setter
    def contains(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37458a288afa8d859f7ed0dac59f780103293097c2b60d2280db67116dee3da7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exact")
    def exact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exact"))

    @exact.setter
    def exact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__023b160078941155ade0b2d982c11728699c300f942e6cabebfa7f0426bd1a18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreCase")
    def ignore_case(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreCase"))

    @ignore_case.setter
    def ignore_case(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d869641dc1a47ec5fe3ad78b1189a32d1bdc0873c21d41eb4c8ff1725601b34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreCase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a378baf6e7d4cf32f33331a685ac6758829e3b1a03f50a7545e743b36bf9cfbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suffix")
    def suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suffix"))

    @suffix.setter
    def suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4345cb572416a6ff1935a916c0989ec644f462730e9db3bf4b2725560284cff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__626380b862474f627997150e35ed3dae6bfc8c1ecd72ef3785bfbf204ef59e78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesToOperations",
    jsii_struct_bases=[],
    name_mapping={
        "header_set": "headerSet",
        "hosts": "hosts",
        "methods": "methods",
        "paths": "paths",
    },
)
class GoogleNetworkSecurityAuthzPolicyHttpRulesToOperations:
    def __init__(
        self,
        *,
        header_set: typing.Optional[typing.Union["GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSet", typing.Dict[builtins.str, typing.Any]]] = None,
        hosts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHosts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        methods: typing.Optional[typing.Sequence[builtins.str]] = None,
        paths: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsPaths", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param header_set: header_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#header_set GoogleNetworkSecurityAuthzPolicy#header_set}
        :param hosts: hosts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#hosts GoogleNetworkSecurityAuthzPolicy#hosts}
        :param methods: A list of HTTP methods to match against. Each entry must be a valid HTTP method name (GET, PUT, POST, HEAD, PATCH, DELETE, OPTIONS). It only allows exact match and is always case sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#methods GoogleNetworkSecurityAuthzPolicy#methods}
        :param paths: paths block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#paths GoogleNetworkSecurityAuthzPolicy#paths}
        '''
        if isinstance(header_set, dict):
            header_set = GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSet(**header_set)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c4269c9f8aca0158964aa088909a289f99fb9fdbadbc27c4e70ddfc5c745a1a)
            check_type(argname="argument header_set", value=header_set, expected_type=type_hints["header_set"])
            check_type(argname="argument hosts", value=hosts, expected_type=type_hints["hosts"])
            check_type(argname="argument methods", value=methods, expected_type=type_hints["methods"])
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if header_set is not None:
            self._values["header_set"] = header_set
        if hosts is not None:
            self._values["hosts"] = hosts
        if methods is not None:
            self._values["methods"] = methods
        if paths is not None:
            self._values["paths"] = paths

    @builtins.property
    def header_set(
        self,
    ) -> typing.Optional["GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSet"]:
        '''header_set block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#header_set GoogleNetworkSecurityAuthzPolicy#header_set}
        '''
        result = self._values.get("header_set")
        return typing.cast(typing.Optional["GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSet"], result)

    @builtins.property
    def hosts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHosts"]]]:
        '''hosts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#hosts GoogleNetworkSecurityAuthzPolicy#hosts}
        '''
        result = self._values.get("hosts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHosts"]]], result)

    @builtins.property
    def methods(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of HTTP methods to match against.

        Each entry must be a valid HTTP method name (GET, PUT, POST, HEAD, PATCH, DELETE, OPTIONS). It only allows exact match and is always case sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#methods GoogleNetworkSecurityAuthzPolicy#methods}
        '''
        result = self._values.get("methods")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def paths(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsPaths"]]]:
        '''paths block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#paths GoogleNetworkSecurityAuthzPolicy#paths}
        '''
        result = self._values.get("paths")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsPaths"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityAuthzPolicyHttpRulesToOperations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSet",
    jsii_struct_bases=[],
    name_mapping={"headers": "headers"},
)
class GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSet:
    def __init__(
        self,
        *,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param headers: headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#headers GoogleNetworkSecurityAuthzPolicy#headers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ceb715d4fa6ecd15613aae45c76e251533be5dcf328c6d45b11d4d96b881283)
            check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if headers is not None:
            self._values["headers"] = headers

    @builtins.property
    def headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders"]]]:
        '''headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#headers GoogleNetworkSecurityAuthzPolicy#headers}
        '''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[typing.Union["GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValue", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Specifies the name of the header in the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#name GoogleNetworkSecurityAuthzPolicy#name}
        :param value: value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#value GoogleNetworkSecurityAuthzPolicy#value}
        '''
        if isinstance(value, dict):
            value = GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValue(**value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a74ca3302aa27748c0b222da9466b1c7d78861d2c6810841a1f7cdbcea92551)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the header in the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#name GoogleNetworkSecurityAuthzPolicy#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(
        self,
    ) -> typing.Optional["GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValue"]:
        '''value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#value GoogleNetworkSecurityAuthzPolicy#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional["GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValue"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a3f3099aea3cfdd2e5bae29523faca8efe118ca13ae2a7a03cc70ee7eea1763)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89435e08edefaefd04d9d01401d062acd5d6bb31420bf4b421c01391c68ad17a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__114db9623b29ecdca98d9a97e10d12a484b3d5873aa1703618aad9ee2455147e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bacd42563a8548d434a80d14712b4e131e5ac44739e073893000c3c5a30d3b77)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4367e8789361b2bdc548ac42cc8cd42556d86c2a5f1ef5f127160bbbe6f4be61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10d406da9e37dea2af0a6db68a7702a276761ee54635a206806b74e8642055f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__49976ba01dab0c26a9649b8984f5e35e528eae5cde9ae4e0370e23545691d98d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putValue")
    def put_value(
        self,
        *,
        contains: typing.Optional[builtins.str] = None,
        exact: typing.Optional[builtins.str] = None,
        ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prefix: typing.Optional[builtins.str] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param contains: The input string must have the substring specified here. Note: empty contains match is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc.def Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#contains GoogleNetworkSecurityAuthzPolicy#contains}
        :param exact: The input string must match exactly the string specified here. Examples: * abc only matches the value abc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#exact GoogleNetworkSecurityAuthzPolicy#exact}
        :param ignore_case: If true, indicates the exact/prefix/suffix/contains matching should be case insensitive. For example, the matcher data will match both input string Data and data if set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#ignore_case GoogleNetworkSecurityAuthzPolicy#ignore_case}
        :param prefix: The input string must have the prefix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value abc.xyz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#prefix GoogleNetworkSecurityAuthzPolicy#prefix}
        :param suffix: The input string must have the suffix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#suffix GoogleNetworkSecurityAuthzPolicy#suffix}
        '''
        value = GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValue(
            contains=contains,
            exact=exact,
            ignore_case=ignore_case,
            prefix=prefix,
            suffix=suffix,
        )

        return typing.cast(None, jsii.invoke(self, "putValue", [value]))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(
        self,
    ) -> "GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValueOutputReference":
        return typing.cast("GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValueOutputReference", jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(
        self,
    ) -> typing.Optional["GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValue"]:
        return typing.cast(typing.Optional["GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValue"], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3463c24fa049b07a9ad8d090cb12cbda992e1c875398bd7b2a1006c99286ac3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9155da548c367c2daf6a598c92f2c2bc549c159efc1818915e3ce5ba9ef1d5b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValue",
    jsii_struct_bases=[],
    name_mapping={
        "contains": "contains",
        "exact": "exact",
        "ignore_case": "ignoreCase",
        "prefix": "prefix",
        "suffix": "suffix",
    },
)
class GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValue:
    def __init__(
        self,
        *,
        contains: typing.Optional[builtins.str] = None,
        exact: typing.Optional[builtins.str] = None,
        ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prefix: typing.Optional[builtins.str] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param contains: The input string must have the substring specified here. Note: empty contains match is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc.def Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#contains GoogleNetworkSecurityAuthzPolicy#contains}
        :param exact: The input string must match exactly the string specified here. Examples: * abc only matches the value abc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#exact GoogleNetworkSecurityAuthzPolicy#exact}
        :param ignore_case: If true, indicates the exact/prefix/suffix/contains matching should be case insensitive. For example, the matcher data will match both input string Data and data if set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#ignore_case GoogleNetworkSecurityAuthzPolicy#ignore_case}
        :param prefix: The input string must have the prefix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value abc.xyz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#prefix GoogleNetworkSecurityAuthzPolicy#prefix}
        :param suffix: The input string must have the suffix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#suffix GoogleNetworkSecurityAuthzPolicy#suffix}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c192deaedd018376faa42d985c4f7bd1300fdd168d5476bdaac1d52467b684f4)
            check_type(argname="argument contains", value=contains, expected_type=type_hints["contains"])
            check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
            check_type(argname="argument ignore_case", value=ignore_case, expected_type=type_hints["ignore_case"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument suffix", value=suffix, expected_type=type_hints["suffix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if contains is not None:
            self._values["contains"] = contains
        if exact is not None:
            self._values["exact"] = exact
        if ignore_case is not None:
            self._values["ignore_case"] = ignore_case
        if prefix is not None:
            self._values["prefix"] = prefix
        if suffix is not None:
            self._values["suffix"] = suffix

    @builtins.property
    def contains(self) -> typing.Optional[builtins.str]:
        '''The input string must have the substring specified here.

        Note: empty contains match is not allowed, please use regex instead.
        Examples:

        - abc matches the value xyz.abc.def

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#contains GoogleNetworkSecurityAuthzPolicy#contains}
        '''
        result = self._values.get("contains")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exact(self) -> typing.Optional[builtins.str]:
        '''The input string must match exactly the string specified here. Examples: * abc only matches the value abc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#exact GoogleNetworkSecurityAuthzPolicy#exact}
        '''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, indicates the exact/prefix/suffix/contains matching should be case insensitive.

        For example, the matcher data will match both input string Data and data if set to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#ignore_case GoogleNetworkSecurityAuthzPolicy#ignore_case}
        '''
        result = self._values.get("ignore_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the prefix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value abc.xyz

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#prefix GoogleNetworkSecurityAuthzPolicy#prefix}
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suffix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the suffix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value xyz.abc

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#suffix GoogleNetworkSecurityAuthzPolicy#suffix}
        '''
        result = self._values.get("suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c44ec3d0e6b6909f8df1e0af7e8f429bf50829197a7f9e721fe3a966a4471c2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetContains")
    def reset_contains(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContains", []))

    @jsii.member(jsii_name="resetExact")
    def reset_exact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExact", []))

    @jsii.member(jsii_name="resetIgnoreCase")
    def reset_ignore_case(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreCase", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @jsii.member(jsii_name="resetSuffix")
    def reset_suffix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuffix", []))

    @builtins.property
    @jsii.member(jsii_name="containsInput")
    def contains_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containsInput"))

    @builtins.property
    @jsii.member(jsii_name="exactInput")
    def exact_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exactInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreCaseInput")
    def ignore_case_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreCaseInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="suffixInput")
    def suffix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "suffixInput"))

    @builtins.property
    @jsii.member(jsii_name="contains")
    def contains(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contains"))

    @contains.setter
    def contains(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0359d4ae030192f106566d15ec80a4587e1aa5ea2914bd564fb9578508b6590b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exact")
    def exact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exact"))

    @exact.setter
    def exact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feffe525edd6dcc5de26f90551e5db2dde8818cc5772390c7ee5f581e89aee93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreCase")
    def ignore_case(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreCase"))

    @ignore_case.setter
    def ignore_case(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aa03897f6ffeca4e8a3f4f32ec5565e3c57e2a7f3d44beb480a4a353190c363)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreCase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22aabaac4ded3058771a0f3bf2d18ceeae5885f5495bab29be3e818bc39f1160)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suffix")
    def suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suffix"))

    @suffix.setter
    def suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c691f9348ef075a3f617acbbcea11a7ed1d6581be9809538e2d598d46aa6610)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValue]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35701f652825f5d06bfae788c2432d827579ae154e267666fa088b8f266f8d16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__75e11971b6b364d619cd2c2af77cf60e7990bacc53fe267c67cc5aaafbd11f2c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHeaders")
    def put_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c1ad549f2b4a73ba69430edf19249a7a3a1cb585951122f831da474cc638c42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeaders", [value]))

    @jsii.member(jsii_name="resetHeaders")
    def reset_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaders", []))

    @builtins.property
    @jsii.member(jsii_name="headers")
    def headers(
        self,
    ) -> GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersList:
        return typing.cast(GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersList, jsii.get(self, "headers"))

    @builtins.property
    @jsii.member(jsii_name="headersInput")
    def headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders]]], jsii.get(self, "headersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSet]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8bd62e645cc74adb8bf2fd8f68191701274c2785ec53487b59741372635bdec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHosts",
    jsii_struct_bases=[],
    name_mapping={
        "contains": "contains",
        "exact": "exact",
        "ignore_case": "ignoreCase",
        "prefix": "prefix",
        "suffix": "suffix",
    },
)
class GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHosts:
    def __init__(
        self,
        *,
        contains: typing.Optional[builtins.str] = None,
        exact: typing.Optional[builtins.str] = None,
        ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prefix: typing.Optional[builtins.str] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param contains: The input string must have the substring specified here. Note: empty contains match is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc.def Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#contains GoogleNetworkSecurityAuthzPolicy#contains}
        :param exact: The input string must match exactly the string specified here. Examples: * abc only matches the value abc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#exact GoogleNetworkSecurityAuthzPolicy#exact}
        :param ignore_case: If true, indicates the exact/prefix/suffix/contains matching should be case insensitive. For example, the matcher data will match both input string Data and data if set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#ignore_case GoogleNetworkSecurityAuthzPolicy#ignore_case}
        :param prefix: The input string must have the prefix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value abc.xyz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#prefix GoogleNetworkSecurityAuthzPolicy#prefix}
        :param suffix: The input string must have the suffix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#suffix GoogleNetworkSecurityAuthzPolicy#suffix}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1522f7c58d5f6dcb631380ebe13e3f16cb61782e85bd73f3719a3b102a1767f1)
            check_type(argname="argument contains", value=contains, expected_type=type_hints["contains"])
            check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
            check_type(argname="argument ignore_case", value=ignore_case, expected_type=type_hints["ignore_case"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument suffix", value=suffix, expected_type=type_hints["suffix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if contains is not None:
            self._values["contains"] = contains
        if exact is not None:
            self._values["exact"] = exact
        if ignore_case is not None:
            self._values["ignore_case"] = ignore_case
        if prefix is not None:
            self._values["prefix"] = prefix
        if suffix is not None:
            self._values["suffix"] = suffix

    @builtins.property
    def contains(self) -> typing.Optional[builtins.str]:
        '''The input string must have the substring specified here.

        Note: empty contains match is not allowed, please use regex instead.
        Examples:

        - abc matches the value xyz.abc.def

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#contains GoogleNetworkSecurityAuthzPolicy#contains}
        '''
        result = self._values.get("contains")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exact(self) -> typing.Optional[builtins.str]:
        '''The input string must match exactly the string specified here. Examples: * abc only matches the value abc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#exact GoogleNetworkSecurityAuthzPolicy#exact}
        '''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, indicates the exact/prefix/suffix/contains matching should be case insensitive.

        For example, the matcher data will match both input string Data and data if set to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#ignore_case GoogleNetworkSecurityAuthzPolicy#ignore_case}
        '''
        result = self._values.get("ignore_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the prefix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value abc.xyz

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#prefix GoogleNetworkSecurityAuthzPolicy#prefix}
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suffix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the suffix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value xyz.abc

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#suffix GoogleNetworkSecurityAuthzPolicy#suffix}
        '''
        result = self._values.get("suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHosts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHostsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHostsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbe4091822296aa96a70d7d682705cafe75cf9aa37af833a119ac7564cf692a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHostsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6efa705ac5b6f555e505b3f986f2ff5a9237cde2c07ebdac4b8c245223e09fc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHostsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09ddea738e3c0b400ec6bd80431bbfe074d9f061161cb69ab243327fdc54c96f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e84ef21e978b7f99ba9f36a86cff494834847fbe5088513f714e8e9e7d5490f6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c91223aea87c92312be46e9984e3946d81543d9d1dc41f20c8e824ce1644d588)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHosts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHosts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHosts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78f98209c777812271ea37f2a34601560f14bf4c1ca428cca524eebdf3c042a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHostsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHostsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbd65406d8aa9a1749db6db3828b1ec934543af52e506095dc635796e3256b7a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetContains")
    def reset_contains(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContains", []))

    @jsii.member(jsii_name="resetExact")
    def reset_exact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExact", []))

    @jsii.member(jsii_name="resetIgnoreCase")
    def reset_ignore_case(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreCase", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @jsii.member(jsii_name="resetSuffix")
    def reset_suffix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuffix", []))

    @builtins.property
    @jsii.member(jsii_name="containsInput")
    def contains_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containsInput"))

    @builtins.property
    @jsii.member(jsii_name="exactInput")
    def exact_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exactInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreCaseInput")
    def ignore_case_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreCaseInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="suffixInput")
    def suffix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "suffixInput"))

    @builtins.property
    @jsii.member(jsii_name="contains")
    def contains(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contains"))

    @contains.setter
    def contains(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__016a9c79637a47ce177667666b0b45bcc856749dc1e18c74526e291ca4e95609)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exact")
    def exact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exact"))

    @exact.setter
    def exact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__817cf86b5a5d7c8999052b0e8cb1fe234de6e65911301befae3179f991abd905)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreCase")
    def ignore_case(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreCase"))

    @ignore_case.setter
    def ignore_case(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e422774485cc02e3848e59a14bed34e2cdcc1946a1f3ae5ddff0e4dc66a57c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreCase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7384e42914169afe96eae2665cda85ec87c818fba6ec7e2350d1bc432cc17803)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suffix")
    def suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suffix"))

    @suffix.setter
    def suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d3074144f666578d0ac35b812016e6cf5371c32e33d7c7c04d91fe78056c477)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHosts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHosts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHosts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bebe6c7100d193952dcf9012a5e89f4ad9b6d8b83545f135785f8d75632d45e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__47c29075073af7306616a7468836a0b150315f5fc415ab53a36b8a5c3533e222)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e71681ca6e3239f510ee0a68d7ea9627f5318d267c83f570d7eeb8f0e491fb53)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03383a8e3fad1ff4a977c2f098bf8a83af9fbd9233731c2e6ef5140b5e34dc66)
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
            type_hints = typing.get_type_hints(_typecheckingstub__98968dbb1e28500430eba634c44cad2b1835c2c6ec78798db7f7af8cfbb66b07)
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
            type_hints = typing.get_type_hints(_typecheckingstub__651b18bae8e0ec066531d1ae1c4c695168a92c420a73b95ba311bcf56b8076fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d319a8ce289915b7dc695cd544c74e62433fde0069ba6ce110ced1bca91be17c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f8081b796159dfd7b037c18f1d572a25cc1bdbad71f6ca4dc34ae44cb46a787)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHeaderSet")
    def put_header_set(
        self,
        *,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param headers: headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#headers GoogleNetworkSecurityAuthzPolicy#headers}
        '''
        value = GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSet(
            headers=headers
        )

        return typing.cast(None, jsii.invoke(self, "putHeaderSet", [value]))

    @jsii.member(jsii_name="putHosts")
    def put_hosts(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHosts, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0389c5d2b1dd6f86729a510a488d4bb79a28863c970472792718495d87db406d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHosts", [value]))

    @jsii.member(jsii_name="putPaths")
    def put_paths(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsPaths", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8abe0edf8e3bb1daf3e7c26a2ca38c61ac1e482de10312b8b482529c74b5a239)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPaths", [value]))

    @jsii.member(jsii_name="resetHeaderSet")
    def reset_header_set(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaderSet", []))

    @jsii.member(jsii_name="resetHosts")
    def reset_hosts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHosts", []))

    @jsii.member(jsii_name="resetMethods")
    def reset_methods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethods", []))

    @jsii.member(jsii_name="resetPaths")
    def reset_paths(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPaths", []))

    @builtins.property
    @jsii.member(jsii_name="headerSet")
    def header_set(
        self,
    ) -> GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetOutputReference:
        return typing.cast(GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetOutputReference, jsii.get(self, "headerSet"))

    @builtins.property
    @jsii.member(jsii_name="hosts")
    def hosts(self) -> GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHostsList:
        return typing.cast(GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHostsList, jsii.get(self, "hosts"))

    @builtins.property
    @jsii.member(jsii_name="paths")
    def paths(self) -> "GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsPathsList":
        return typing.cast("GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsPathsList", jsii.get(self, "paths"))

    @builtins.property
    @jsii.member(jsii_name="headerSetInput")
    def header_set_input(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSet]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSet], jsii.get(self, "headerSetInput"))

    @builtins.property
    @jsii.member(jsii_name="hostsInput")
    def hosts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHosts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHosts]]], jsii.get(self, "hostsInput"))

    @builtins.property
    @jsii.member(jsii_name="methodsInput")
    def methods_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "methodsInput"))

    @builtins.property
    @jsii.member(jsii_name="pathsInput")
    def paths_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsPaths"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsPaths"]]], jsii.get(self, "pathsInput"))

    @builtins.property
    @jsii.member(jsii_name="methods")
    def methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "methods"))

    @methods.setter
    def methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcd5f5eb12d5cf4a3e0e4b447a61f65e565ffcbb880ef3b5ffdd18e667f06d2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "methods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesToOperations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesToOperations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesToOperations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45ce23dd4f1c263962c689a9fe9d6646af026816eba26fc7281c9b5da28a0517)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsPaths",
    jsii_struct_bases=[],
    name_mapping={
        "contains": "contains",
        "exact": "exact",
        "ignore_case": "ignoreCase",
        "prefix": "prefix",
        "suffix": "suffix",
    },
)
class GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsPaths:
    def __init__(
        self,
        *,
        contains: typing.Optional[builtins.str] = None,
        exact: typing.Optional[builtins.str] = None,
        ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prefix: typing.Optional[builtins.str] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param contains: The input string must have the substring specified here. Note: empty contains match is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc.def Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#contains GoogleNetworkSecurityAuthzPolicy#contains}
        :param exact: The input string must match exactly the string specified here. Examples: * abc only matches the value abc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#exact GoogleNetworkSecurityAuthzPolicy#exact}
        :param ignore_case: If true, indicates the exact/prefix/suffix/contains matching should be case insensitive. For example, the matcher data will match both input string Data and data if set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#ignore_case GoogleNetworkSecurityAuthzPolicy#ignore_case}
        :param prefix: The input string must have the prefix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value abc.xyz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#prefix GoogleNetworkSecurityAuthzPolicy#prefix}
        :param suffix: The input string must have the suffix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#suffix GoogleNetworkSecurityAuthzPolicy#suffix}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6efb307002b1341ad75102adc7fe927e1de2828d87d8e355d7f0d33bc3da0511)
            check_type(argname="argument contains", value=contains, expected_type=type_hints["contains"])
            check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
            check_type(argname="argument ignore_case", value=ignore_case, expected_type=type_hints["ignore_case"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument suffix", value=suffix, expected_type=type_hints["suffix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if contains is not None:
            self._values["contains"] = contains
        if exact is not None:
            self._values["exact"] = exact
        if ignore_case is not None:
            self._values["ignore_case"] = ignore_case
        if prefix is not None:
            self._values["prefix"] = prefix
        if suffix is not None:
            self._values["suffix"] = suffix

    @builtins.property
    def contains(self) -> typing.Optional[builtins.str]:
        '''The input string must have the substring specified here.

        Note: empty contains match is not allowed, please use regex instead.
        Examples:

        - abc matches the value xyz.abc.def

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#contains GoogleNetworkSecurityAuthzPolicy#contains}
        '''
        result = self._values.get("contains")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exact(self) -> typing.Optional[builtins.str]:
        '''The input string must match exactly the string specified here. Examples: * abc only matches the value abc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#exact GoogleNetworkSecurityAuthzPolicy#exact}
        '''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, indicates the exact/prefix/suffix/contains matching should be case insensitive.

        For example, the matcher data will match both input string Data and data if set to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#ignore_case GoogleNetworkSecurityAuthzPolicy#ignore_case}
        '''
        result = self._values.get("ignore_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the prefix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value abc.xyz

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#prefix GoogleNetworkSecurityAuthzPolicy#prefix}
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suffix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the suffix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value xyz.abc

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#suffix GoogleNetworkSecurityAuthzPolicy#suffix}
        '''
        result = self._values.get("suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsPaths(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsPathsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsPathsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__495fbc6392fd85135439f981c74ae7a04c743b5acf1a2c82ed59e14cc7502d11)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsPathsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e72c42f667b6b9e64a94ac568974ae9e4f90cf1cb8ce69ee15eae8de189cbce)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsPathsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ff9ad0d32041e02d9a12afd5064c5c7360441805df078060a3de864ca12c2d5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f875fbe3ae8e6875678923ff30a3a01718b20a388dc3f425789ff1014dcdcdd1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6ad6acf7c1362b76459d5407def3cf04b85c57fb87d517901814646172e983b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsPaths]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsPaths]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsPaths]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27c0d73da59f28f5411caaf4b7cb3da3b78a1ffd3cc0c9380402ac455d3bb9fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsPathsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsPathsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4be58b5ff8f334d4335531b8c46f953187abfc487ef01d8f2ac147e62cb24e7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetContains")
    def reset_contains(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContains", []))

    @jsii.member(jsii_name="resetExact")
    def reset_exact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExact", []))

    @jsii.member(jsii_name="resetIgnoreCase")
    def reset_ignore_case(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreCase", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @jsii.member(jsii_name="resetSuffix")
    def reset_suffix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuffix", []))

    @builtins.property
    @jsii.member(jsii_name="containsInput")
    def contains_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containsInput"))

    @builtins.property
    @jsii.member(jsii_name="exactInput")
    def exact_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exactInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreCaseInput")
    def ignore_case_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreCaseInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="suffixInput")
    def suffix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "suffixInput"))

    @builtins.property
    @jsii.member(jsii_name="contains")
    def contains(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contains"))

    @contains.setter
    def contains(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04a4732c1d81926d8b834fbd6b6407ff18a2eb424addd9b875425462a8ff5ed8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exact")
    def exact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exact"))

    @exact.setter
    def exact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d4a432c804fa6f8da06aad66c57877d1a352c0c2778910b99183b469da211e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreCase")
    def ignore_case(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreCase"))

    @ignore_case.setter
    def ignore_case(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e48e419487947cf727d3e278af35890577609bab63a3d709ce9b8a3fd1e848b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreCase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52b0d29b021bbfb8ff40e55f6f5f25620b9f48eee7008141df6796b8df5a974a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suffix")
    def suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suffix"))

    @suffix.setter
    def suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35ea892b2c7391384da6b9d156f8878f6b9da7f574b741dc29ae60d93fe3d058)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsPaths]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsPaths]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsPaths]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__359b2e0ccde4ee5bcd6d378ee2a08efd076acdcd592131e68820bd0ba5053401)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkSecurityAuthzPolicyHttpRulesToOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyHttpRulesToOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d29c879af7ada699266f14d95e53c9b068933b52e1b3846000cd4fdc8dc69c95)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNotOperations")
    def put_not_operations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee791553eaa844b6bd0cf75e4d6f331d34c0b2a5eafbb107418bf9095c9190f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNotOperations", [value]))

    @jsii.member(jsii_name="putOperations")
    def put_operations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e31abb8f166be7dad98ab8ca3440e62e29af2425e687ed3c6194668ee05006a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOperations", [value]))

    @jsii.member(jsii_name="resetNotOperations")
    def reset_not_operations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotOperations", []))

    @jsii.member(jsii_name="resetOperations")
    def reset_operations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperations", []))

    @builtins.property
    @jsii.member(jsii_name="notOperations")
    def not_operations(
        self,
    ) -> GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsList:
        return typing.cast(GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsList, jsii.get(self, "notOperations"))

    @builtins.property
    @jsii.member(jsii_name="operations")
    def operations(self) -> GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsList:
        return typing.cast(GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsList, jsii.get(self, "operations"))

    @builtins.property
    @jsii.member(jsii_name="notOperationsInput")
    def not_operations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperations]]], jsii.get(self, "notOperationsInput"))

    @builtins.property
    @jsii.member(jsii_name="operationsInput")
    def operations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperations]]], jsii.get(self, "operationsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesTo]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesTo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesTo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22a21f11ffa1675ddbd2979cb6225dfe224e8beadd716b4db9fdbad03ea444b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyTarget",
    jsii_struct_bases=[],
    name_mapping={
        "load_balancing_scheme": "loadBalancingScheme",
        "resources": "resources",
    },
)
class GoogleNetworkSecurityAuthzPolicyTarget:
    def __init__(
        self,
        *,
        load_balancing_scheme: builtins.str,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param load_balancing_scheme: All gateways and forwarding rules referenced by this policy and extensions must share the same load balancing scheme. For more information, refer to `Backend services overview <https://cloud.google.com/load-balancing/docs/backend-service>`_. Possible values: ["INTERNAL_MANAGED", "EXTERNAL_MANAGED", "INTERNAL_SELF_MANAGED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#load_balancing_scheme GoogleNetworkSecurityAuthzPolicy#load_balancing_scheme}
        :param resources: A list of references to the Forwarding Rules on which this policy will be applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#resources GoogleNetworkSecurityAuthzPolicy#resources}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__295e4974fd6d0a4b2a1ff31575427af97b6cb86a1a34ed0ccf8548831843a49a)
            check_type(argname="argument load_balancing_scheme", value=load_balancing_scheme, expected_type=type_hints["load_balancing_scheme"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "load_balancing_scheme": load_balancing_scheme,
        }
        if resources is not None:
            self._values["resources"] = resources

    @builtins.property
    def load_balancing_scheme(self) -> builtins.str:
        '''All gateways and forwarding rules referenced by this policy and extensions must share the same load balancing scheme.

        For more information, refer to `Backend services overview <https://cloud.google.com/load-balancing/docs/backend-service>`_. Possible values: ["INTERNAL_MANAGED", "EXTERNAL_MANAGED", "INTERNAL_SELF_MANAGED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#load_balancing_scheme GoogleNetworkSecurityAuthzPolicy#load_balancing_scheme}
        '''
        result = self._values.get("load_balancing_scheme")
        assert result is not None, "Required property 'load_balancing_scheme' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of references to the Forwarding Rules on which this policy will be applied.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#resources GoogleNetworkSecurityAuthzPolicy#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityAuthzPolicyTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkSecurityAuthzPolicyTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6711b053320bd4db558d7428aa614714324ac5fc8ee59a534417a1d234bbeebb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetResources")
    def reset_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResources", []))

    @builtins.property
    @jsii.member(jsii_name="loadBalancingSchemeInput")
    def load_balancing_scheme_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loadBalancingSchemeInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancingScheme")
    def load_balancing_scheme(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancingScheme"))

    @load_balancing_scheme.setter
    def load_balancing_scheme(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c036f3b8353c4dc6b891a8b7e59a84711b2dfa17cb4a478393eaf986bc8f45d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancingScheme", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resources"))

    @resources.setter
    def resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a1909b207dfd985fcdaafdcee6206b61bab36552f5b67336bd509da5b813760)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleNetworkSecurityAuthzPolicyTarget]:
        return typing.cast(typing.Optional[GoogleNetworkSecurityAuthzPolicyTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkSecurityAuthzPolicyTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__992bb4f414d383e127db3d123901099d49d5c7944d1777143e96d18c156f1ec5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleNetworkSecurityAuthzPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#create GoogleNetworkSecurityAuthzPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#delete GoogleNetworkSecurityAuthzPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#update GoogleNetworkSecurityAuthzPolicy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26442eda2c8cfb4eea492562f589ec4aa52e44fa3c14e145901621db4eb03833)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#create GoogleNetworkSecurityAuthzPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#delete GoogleNetworkSecurityAuthzPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_authz_policy#update GoogleNetworkSecurityAuthzPolicy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecurityAuthzPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkSecurityAuthzPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecurityAuthzPolicy.GoogleNetworkSecurityAuthzPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5937d4d92901fc50b69998ba77ee10257d0cba3437401d934bbe198a4070f5cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e428494ecbf5009f33af79fce4ad8d7a8dc9b6ab3bf0a54c11e2649222ad9fba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76b0b7223beccea0496ff0e95970c3432a556db49527cebd0a2f7dfcf27eb6d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37b5e534feb51f423e39d6974625e7d08e179a88ca8a3fdd7cc26f7fb6426d6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed25794152a217087d168388d2d04475a38bcad8111937675777f266a48928c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleNetworkSecurityAuthzPolicy",
    "GoogleNetworkSecurityAuthzPolicyConfig",
    "GoogleNetworkSecurityAuthzPolicyCustomProvider",
    "GoogleNetworkSecurityAuthzPolicyCustomProviderAuthzExtension",
    "GoogleNetworkSecurityAuthzPolicyCustomProviderAuthzExtensionOutputReference",
    "GoogleNetworkSecurityAuthzPolicyCustomProviderCloudIap",
    "GoogleNetworkSecurityAuthzPolicyCustomProviderCloudIapOutputReference",
    "GoogleNetworkSecurityAuthzPolicyCustomProviderOutputReference",
    "GoogleNetworkSecurityAuthzPolicyHttpRules",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesFrom",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSources",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesList",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesOutputReference",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipalsList",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipalsOutputReference",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccount",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccountOutputReference",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesList",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesOutputReference",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSet",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSetOutputReference",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesFromOutputReference",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesFromSources",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesList",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesOutputReference",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipalsList",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipalsOutputReference",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResources",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccount",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccountOutputReference",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesList",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesOutputReference",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSet",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSetOutputReference",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesList",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesOutputReference",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesTo",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperations",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSet",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersList",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersOutputReference",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValue",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValueOutputReference",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetOutputReference",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHostsList",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHostsOutputReference",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsList",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsOutputReference",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsPathsList",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsPathsOutputReference",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesToOperations",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSet",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersList",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersOutputReference",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValue",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValueOutputReference",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetOutputReference",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHosts",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHostsList",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHostsOutputReference",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsList",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsOutputReference",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsPaths",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsPathsList",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsPathsOutputReference",
    "GoogleNetworkSecurityAuthzPolicyHttpRulesToOutputReference",
    "GoogleNetworkSecurityAuthzPolicyTarget",
    "GoogleNetworkSecurityAuthzPolicyTargetOutputReference",
    "GoogleNetworkSecurityAuthzPolicyTimeouts",
    "GoogleNetworkSecurityAuthzPolicyTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__76a2aa2eb7227adfdef29cdff4b51285116747de715ccece05afbbc6b321117b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    action: builtins.str,
    location: builtins.str,
    name: builtins.str,
    target: typing.Union[GoogleNetworkSecurityAuthzPolicyTarget, typing.Dict[builtins.str, typing.Any]],
    custom_provider: typing.Optional[typing.Union[GoogleNetworkSecurityAuthzPolicyCustomProvider, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    http_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleNetworkSecurityAuthzPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__0597f9421c357f0784759cb117b624ddfeb58dc31bb7e1a57b7d057844be6b0f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5b4eecf27f62da30739e7f703e8e111376ecf9bb43cfe9316424a13ebc05c68(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc34ae11e0f873dc2f6a5f41eec4f0e7767d91242d476d97c85113da0e200ba5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5d42fd24c85696d4d2e4173fac2412a87f4cfc74c7024461e029321d062c137(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb4cb2d1d3a1ed67a13328e69fc9a6be35abef468267a8ab3ea7a1b105f7a969(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aff62bd4f6210e6fc003709543767a31d9d2a71792d4c9252fc01a0d1cf6d1a8(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__872d6281dc075dcc577ce9cabec802da2cea997bc054ca8fdb0668849630e5a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fc70c06f193fb38e4e6d90249e8bd62e097d893ab4c70af050228d2a5ed9cb1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f66d17fb53c64c3f165818fa382c8a9e949004ab3c4543b72c9a29e4c52c566(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__965967f19aeecd0bc8438c35c0da171aff0717847a6d55819b4d59293e87beae(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    action: builtins.str,
    location: builtins.str,
    name: builtins.str,
    target: typing.Union[GoogleNetworkSecurityAuthzPolicyTarget, typing.Dict[builtins.str, typing.Any]],
    custom_provider: typing.Optional[typing.Union[GoogleNetworkSecurityAuthzPolicyCustomProvider, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    http_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleNetworkSecurityAuthzPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7a3e33662399748bed801374c1e9f01aa38416e412e397e571a25aebe56faf0(
    *,
    authz_extension: typing.Optional[typing.Union[GoogleNetworkSecurityAuthzPolicyCustomProviderAuthzExtension, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_iap: typing.Optional[typing.Union[GoogleNetworkSecurityAuthzPolicyCustomProviderCloudIap, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b81cb563f1b7e6422b9a3563594739bf480fdafc648d9611bb0fbccadaca7b8(
    *,
    resources: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8261726fe405cc41ad2284fea9543bf9360ec9a18e5345492ee5125d4f3c6665(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5407b814a6e84d825070a8c8873c66fb6e72935f4efe4f30cc8e04f755beb7e4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc26b3655e0783f1d5e9f4e338ba0a7851e2ac272c1830b9f6fcd636b29a1327(
    value: typing.Optional[GoogleNetworkSecurityAuthzPolicyCustomProviderAuthzExtension],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e3baead72eef489eeebacbb277094f933803e9e28656c44a492d9371435ab08(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14927affea671bc1c296ca35aa06801c01185716ea0f7ee51126ebd1c3a49d38(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6715d7d2072650ee8cf6c59a4306e97c16fe18a62c78754762a282c4e4fe50e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cca588f91b93513e73b802c6f16874fc25377b745fd2f1790de68140b4c9541(
    value: typing.Optional[GoogleNetworkSecurityAuthzPolicyCustomProviderCloudIap],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27d9b27d974b320c36ca729a00082c2e10b90758118d0fc1f8b52b7bf72df12b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b9b333cfbfe6ee0c22e04bca2020347f62e84ba0655f6f7cfab29de71846661(
    value: typing.Optional[GoogleNetworkSecurityAuthzPolicyCustomProvider],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fac68984474e7339179fd0531d76f76e8ba93c84eac2b82bc9b5079f80e8eef(
    *,
    from_: typing.Optional[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesFrom, typing.Dict[builtins.str, typing.Any]]] = None,
    to: typing.Optional[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesTo, typing.Dict[builtins.str, typing.Any]]] = None,
    when: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__938438547a41462aff0ffb5c14b87a30a27cdc0b10f824240bdb0e0197640d4f(
    *,
    not_sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
    sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesFromSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7aa458c07a7714e32a0fb8484bbad3fa5d931c84089a2c600e046cbb45b86ee(
    *,
    principals: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bba00a33d9a497362ec71fae8e22df0a05dc98b3627aed55c5cca1f49e2fae41(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71208460ca486315b21748a23e8b62dd27b38e99e2b1e60ddb0fd2c416fc27bb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b634f4c2ecc3c64e910a757986c7a6df5984e4f96ec230855523c1003d03b4f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26fd81604d8ff7628382f4a36c3b46258f885dce34dfea6ae51089d8ed4278d7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45468619c08ef13054c31a167c3858df4a6894d0d88caf2c32d08e3903ac7d9e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fadab3f967a32e79e9054c87da9b80212596ae70e5168b6a71f853bb6d5b5fc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7688d7f9a69da207414930006f51b6cc02d70306f7d1a4b302632270efbd03b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a2333e781f45581d8d7692f982760d1defb718e8fd4c1bc6ce27d7de3431881(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8297536b1310013081bcf66e81ff8e24155475eab950832b6be8f58361425ef(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed3aa5b39c6f1d8957808775e005c66db0a6ba72f7873beace6e9c943bf6b62a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12f3580c1115e434184a00145c8a2912f56a0b154385f35d566e050e9bb6a899(
    *,
    contains: typing.Optional[builtins.str] = None,
    exact: typing.Optional[builtins.str] = None,
    ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prefix: typing.Optional[builtins.str] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af2f23e2d51a18c595ef2fff1da7d4a3a9db4c5cf97aaff3b9cc812b059dc62d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f39f8a2750b63786991c0e0e11f73aab6f7b3721a6e00bbaae215124147efbe(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d51f4120ba051a7c308f969a1808cbd148b23f5f61618f12d4671ad73b28af3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36f9fd813a7eb06b95edddad0b0a8e637c04985a58700854f9f1cdd231c53c2b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1edc5ef65fa68599b9330644409211842da2fbcf1c4b09769f762dbb6ee8674c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0dd47067ac2c634e3bf5395adb2bdf83410604b8cc6b4f66ec054047e7a1d31(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9875645e013be612878f586911f692f436bc5743d01d7ab3afc6bc38958d73f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7928dab76ef2fb51e2a40962baaf6ba78c059efa8c3b458ce1129fd36cc32539(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44ec3e8e44ccaa64849eaf440d754f101ed35c485198df7e531f8770c5d5c3b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fca23b87cb961a5560ea96be7db5981009aca58b8cc95ccbc8bebea2c9f9a7f8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef4fcfb87d72d791d699b1c0930abfa139ac8e1cf4b34488ca5a62706b06b877(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d919d58691c223cba556a00591ce453ff7058b0a852e3c57796bdb6593e0cf58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53bb62878d3043a0ad95c9c3ac47b35cd93e4714233851f7848dbe7588215e29(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deeeb29bfcf1ff3d515e90aef13abe2c21c64901ad69e826cef9389bd613f46a(
    *,
    iam_service_account: typing.Optional[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccount, typing.Dict[builtins.str, typing.Any]]] = None,
    tag_value_id_set: typing.Optional[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSet, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d8104bdcdcff3c3ff6df871842dd05a3df8aa24a809748e50430e6dc7e81ed2(
    *,
    contains: typing.Optional[builtins.str] = None,
    exact: typing.Optional[builtins.str] = None,
    ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prefix: typing.Optional[builtins.str] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ed26d0559cefc22861a7f1fd433f949a978df7f95cee5c766a3798659ec0db9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81557a31d85994d4e1e1458337aad9c9de8efa5e581fa70ba23f8259c774e5cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__710d09b3391acf0ebf4989da05f94633698f4173258a0c77760393ebfeff7350(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d53c5ea5f1ac18c3ec4b8b0c4402f73f4c1aa08fa3843df35eab8762f76b4a22(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e427ccd47067b13f6c51cc59b20d4a4c7e284f0db0c0e3483429f6adb29e6aaa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d34abdf6b402940537dbf5cfe175f7a37daee6ee7f52baebc221e89326c24464(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4de7d94812c15b9dde9a1b86a47665ecf0bd051f10172c02044dcdc1a1bfb85(
    value: typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccount],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15071da1982a848f6b35a7ffae7a18b04f56eb22b576d13dab7adc202b023b20(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb8cd7a91a369ec9faa78a423844a704c8d6d02872a919a74a926cd800f5b72e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3fa13b9c809e7d2593dff002408ffe729fa585eb94fd8ffb4d591c5902d76c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b7d9c2b3cb5209ad695c111e95422c3b1c7711d3b5efaedcfbbcc02fa3b987a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad4cfa97ab9650ae4dac43d46c8ae3a7f486d3af1624f0d7e587816129607790(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__757dfbe215d08d3d733f868ddb5489d773e46ab3d19d29512d2aac88f0c3a25c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ac61e151e756220969c61fc5fbd5d7bdc46a9752fb35bb2835ac99be3d5a4ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3086c9ecc197aa99e6b2012d800b3360029ad4347140d03baa5f5e48d60a46c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f49909c16f382fb49c0f0fe5f5deec09556caf604bd21931e487291c3efa1f8e(
    *,
    ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df0bba9b389404f873745060460b839b2d524f4e8fea939d189a5c330379fbc0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2679520bbf00eb79abbfebbef42787d169ab5c4960300d6ff98ff14b7b214aa(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f732371c0e2628dc17c7b8c6ae7ef8a88f682652e633ee3e87da6da81db8620b(
    value: typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__459f431fd8af9ad647d06ef8e611df6f2a93695a89a28e078819345a7769b58b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86cdbbe7bf4df9de5e7a0bf91b3747091601316a47bd205c95aa8330bcdcd09d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesFromNotSources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e019253b86dfbaa2fa445528832864e2b7f0ed8d212cb2d48af68536ee010d88(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesFromSources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e6f79de503399bc7a93ff4799c5a9d4b515afc339bd15328bbfaadba7b5b098(
    value: typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesFrom],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2bbf812bf0e8c6d6af9a69a54600141869e8fc3fdff649cb0903fe34f45a256(
    *,
    principals: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResources, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ab3c168df2ba81e86ac3d2c327ef91d143f7c739f351de7f7a8899d9381cb34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9da4f2936283164c56bf0bb3174af8886a7b792c5a8f01316a018ee390bfc951(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__579da74c65fb705f6865f3f7936cc88b360e9d74d0030905b5a426a0be06931e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a591cf2510a681939067abef855ab3ebc1c3b58318dcf3e7dca70a65d5ab0e6c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__093d82598c9640e300436eb42966800b32c40b08f300b2e8accbac59a2bbd218(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb94fa6a02f2db03f4c53587bd1ba62f4b88439cab30930b37f3d4116ac03513(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesFromSources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d861ebbbf1e2f080710562ce41ec01a635c14de936bd673521284254c83aeb7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a03dcee5b3f3475d75501ba5dce8df566c83279eac83e2f0da9f6730dd14c27a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dab8aa70ae2e859229085feec2321640bf390b87df9f8099f9d8c1ef08dc703(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bc9eafa7e3691d60146d2177270187f31775b13b9c556f9c08a482c5973e05e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesFromSources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__725d5aa6c2f5ee0d1a0ab5812fdf074f123d52fb7619168e660c756b604fc9c8(
    *,
    contains: typing.Optional[builtins.str] = None,
    exact: typing.Optional[builtins.str] = None,
    ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prefix: typing.Optional[builtins.str] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d12d445d7db8d1ed0d03e345cd0d4ba6cff45e476f2b53c0714bf50e43d4932e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0941cc1f0248c7681fbf2df26585e06077a8e5301adec89a6a6d2b80dcfc030f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7a7124756d86e966969f8ca3833bf677a45d42ab3c5af9b1e5c87febb3bb64b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b2d1ffd693d6e1842d0b079711728179980c8f7819880bc08fe7880a70caca5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9f4816a699b58515fc7b31b3c106470f8b2734a6c5273951b806693852b283d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0b5ae02d1e017a73682c191a8fcfe3baa3e2be81ae35d37484abcf564365058(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21dafd9c449443d10b0b6de42ef0faedc348e9c2e76eec6cb5d325d64f32f679(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03a6bac6204af27b7291c21d7df9260f044a5450e771cc193456e21b9ff2a918(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__909afd0296248d23e192d4eafadb7608af8151f2e1b62e351f6e0142aaa5f637(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d93568d1f9cb312e506a5559176914401e9c360798c8a97b4149a3441acf0b74(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d611f1f3adef8ef477db00a2db5fea03eb1e2edf55669f88660cc3ea2d253f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be94b2868b9ed935467c4eeae1a69375d674acdb7e4fcb7fc7c7edd38ac12d60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12ceaafe63df24c877872d7c4ce4b0e6c2cd7de9fcbfd99b56f82d153be61507(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a0c4e83d72ac978f8976597ffe2229d4232be66827881cff069a2176ce17836(
    *,
    iam_service_account: typing.Optional[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccount, typing.Dict[builtins.str, typing.Any]]] = None,
    tag_value_id_set: typing.Optional[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSet, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad33bd4ec9679e9c03cca6fa844c70e50b848aa266929bc054523a8185292aa4(
    *,
    contains: typing.Optional[builtins.str] = None,
    exact: typing.Optional[builtins.str] = None,
    ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prefix: typing.Optional[builtins.str] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__294dd5068b4bc7173afff2e25effc738f96d885123504f106d3f0be6061384cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24b5046e44a23234ae2df1ee46659afc84f2bb65bd9fcdceb6337e95b975a51b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e674e0afe8d18d1ea58d42aac46ba4f506551cd05a18e160f8131a461ad12287(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54635b1f5af3c5ed5ae30c91ec03635b35b421b5a86d474ad88bd88c227d18ec(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1badd1c2099ff9dec4a99758141fb341335861d19fcf63948f2636accf781ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68e70ea6756e9b71b1f9d2f18468bd05be92aed9c9e185800b82dff69441ae7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__740a8344b590d2a2c2000c7b8d50cd7804370f6e94650ceb97739512b12edcbe(
    value: typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccount],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd04521cecacb4cb79cfafefb45b69f20534e9f5564288128c9fb26a7b99a9b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__827e500ca289014a5dec09e4d65ed55d5a13cac269e64f239bdbe65b8756cb77(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__249dbd4142562752381ea37b280d3d0678cda420ed7a28728c57974fab49b673(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69258a71c1fc69737b7e13807e0d0a181960f8651e7314c02a85c537de880b6e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f3630870146ea88dd17e304767d1bed5f212128e931c99b6ffb466af779489c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c899d4e9c5257a9c8adc23fcd72ef264fbd0dc1f51d9d2d283b7607cebbc34d5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6ce1c2799beba56cac031ad4b8d23736488130ee0c39885b58e9ae93590dc90(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c29738df5ead3141eb2c39522bd85405290f043fd5e5da46389deb1b987ed81(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4be2d603c7c3c395056b714d31d68f2567c6e3afe8dc250ae08afd297439866(
    *,
    ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70a8be01c87dea9274720dcbc0196323cfc9920a9b96a283ae1214268c84ebf6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d508056e6e609d5f872a4f8b45e0a3c1597f26766401aa7d2715c8022ad6aba(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c903f60e2af2e99ee78bed983121b9740783cbbb354d5960c16258f224056fd0(
    value: typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68f14568ef055854cd138a9f56e72033e609b6f5442f299e1fcbecbfa46dfde0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c33988e2843c2dfae2de16b34f289f7603139450dfef12cee518c42dfefbf0fa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f1efcf024c211d91252c31a3ba12fdc5b4f10779ddda123a3db50f72aa4b0b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed14ded10b09906356d238ad1cedac9978587776cbac9135e9857ecd84fc5326(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d37c4fc535176a94e72b53bd8c6a41aca427e5e50a1ae5e8a5554023a2e5920c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__373a77f901dfca73a538ed3bfaf87c5673a19a115bf719070a8ba10348e737fc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5568f5a03507e04ad508d48d152140bb431edbb4d081e9a69d3952a57e971c37(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__743b952e8156c7add892967339ec83426a361e06fe7fee655c1269ebf6d70889(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fb91823d37697b5eda0a5c5ff1865f013899796addab136bfa0474795717da2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b78ae971647bfa85500c2c71aa498e07c93bb3eff02ef8220896146ba1dbc13f(
    *,
    not_operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperations, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a7ff6f1a36f8610724675d895716e79b7a5639eb9a9a7b27eb8b9f9ea26e508(
    *,
    header_set: typing.Optional[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSet, typing.Dict[builtins.str, typing.Any]]] = None,
    hosts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    methods: typing.Optional[typing.Sequence[builtins.str]] = None,
    paths: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41cde4e7dbeb2e6def23570c123bfe374f26c90d35bb6d4fe7ca91de86946eeb(
    *,
    headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74bab4fb574aad29b395ecff9c6e72c70c6e209eed07bd5a69385da01a55ff98(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValue, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c42cc3faa1d3843d8f2f6de511f516c9e708ca28c5587f4b5966c1173d37340b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38865e0b5f111c5d7d2345e2ff574d743b1838c69e97a5cc671ad1cd5c2463b8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85a8b0cc34d649956cf6464a04234240feb25569b8948cf28c4999c3225e4fbf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d10c3fba8df75f8a882d69f70c91e7b3eab14f04cbc06ce0a0d52900085de52(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4d66dd792aff2cf97e458e48fc674ae384219da4ce95382540470da567003a8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e39dd56a4d7fe9a8632828d51b4f03fb62aff4305c710bf0f7e0ef56f5c7f59(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__befe9d2fc507b8f583155f4a1aaf491407699b85112022713ee0a99808121fa1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64540500fc484b75bba493b0672b2230b954507b63446670841503932d1b0b1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__944b85ec830e06db7f98837d74a19c2bf130081ba511b36ebdc9c2c8b642e483(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6bd7f114e68f63d746fb69aaa5dea73c59a83d8c159369c6e3f52a9d97ee836(
    *,
    contains: typing.Optional[builtins.str] = None,
    exact: typing.Optional[builtins.str] = None,
    ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prefix: typing.Optional[builtins.str] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb8e3d9ff254c45ac776545708499f5f77bcc1e9313e65d0985748f94708a33b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8adce1710680d4c35a3409366ce8648812f4545272a926ffaa21fd77b4029f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__962b8ad37687efa4e544581fe8fe03e641e04d42691c738f1270ad8e3fb660f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c715c769fd016e6b939662a2b3caaf8065bd70bd53f699a7b2b8d2b987c8fc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38eff95ee58a493b54c3fcaef35ce2d68d42818e6100728ec9b5a913381a29ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c0643829289921cf49f36fea4e913ddace56e6787ad7da938dfa88657278e1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d668069558ac4219bf2dff3016fe6eca2d276ad227f7df3c7d31a4d8b16c201(
    value: typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fa8f6b0a4c73786ea65df51e60491b7f26571a60e5c832c99a89d93e28b739c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e09836f59b468a07ff0f4d4863c6623778d0c989216148937a19b3eaf113593(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f24d653ee7bdcad4540b0ad0aba28ec2aa0ae4299892e7f6bb8a96d9d5da36a2(
    value: typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8fd6f24f2f95b866bfb8208137e6ed4c4068c442cf3e7ce451796ca64686b4b(
    *,
    contains: typing.Optional[builtins.str] = None,
    exact: typing.Optional[builtins.str] = None,
    ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prefix: typing.Optional[builtins.str] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__048e830e11b73d64d88d5b2981506c1496a6f32cada18e77243346719454c6cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e04203f6588e2aa2aae7f69f8a78e8faa89b6827fd7269a113c45526a4c47c9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b64c71670e73a5b83015f53ba39af4ed89a3ef1c65910d0cdaa494e2dfbeb644(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__091d8a25b883c6cf8bce100c50821b89b77f83e3603476859a5174c78b096e14(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__168ef3d8e423ad6407f45ceb1bbde51659a9aef0a3d2ed79c88c6de8424c5374(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6565f7d707cc676491b611f0f3041d93af53dbfceb102a94a389c526876ff78(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50eb0a061332afae9902ca82461d810a5f528565b8d60abc942b36b3cb2509a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71c1be95af96d40b19dd238b42791bb03f14cf9cd6a6d265146a9b6d483d7bd9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84e5fc72b846668b6086c3742b92ca23888df4c502326d28300624c6edc21ef0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dac188eada7f07b4d93cc550b1b9453f2cfea80ecf1f7469d39e8fedeb29833f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed2be711df6f59cd704d1f39a5fc5bd31c56e85748f925c13951608c7d3fb874(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1324c9fbcb6f3b758b433d0508d310872b12b6f6d326bba83b4f54eda89a618(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba76abc9d8b2ea6490987e6eae1192d6475a1d598ebfa1511c7585124e91ae23(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56fc22dbaa5bacd499a2eb7237e94cbea6dacb0a683ac12d1015ea3de56d24cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e85a4bba93eb460de5e59f16b8950d83ba9922e3ae4f2a7c47a7ea10c43a5ab(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeee71a4e2f98c29e121e7945db986074773495554d0b6e1d35d23f3f6523625(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16b17c092a16ffbb453870b458c89ddc7cbc50af2e1c99e5624559bd37345ba0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0df0eef045eb61a4d12fa1083748ebb99784f2a14ecf9398c78c37503294b13d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5d2e85035fddfefe222b8468bae32e3ffb49a1dfe719392ebb9640f0586305c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d20bc351b50934c2568c35c154351205a86d48ed904c032db7939f0212cba679(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d93682f7951feb54092ba2741d940bf77a8edc70365f0ded38c38b162c6892df(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7165351fc5ecacfed275a6874db0768b8e0fb37ae38986bb9d3fe401390723c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32cc49dcad2f542b1634db6680e6b14d0952e15e7c3f6c0e167abce9627fadda(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be1d31c2b51a2a0893949603afb98140b9a4bcb9ba767aa959c86465760ae5a9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efd7af60d8299925c6e0bdc7b3afd7cc4c1bd1787955b913efbfea614cd65dac(
    *,
    contains: typing.Optional[builtins.str] = None,
    exact: typing.Optional[builtins.str] = None,
    ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prefix: typing.Optional[builtins.str] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__408382a44dfa304d04ed16f83a813b03f55f6b7e24ae8a9d8f577414e69b06b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a3f041d5f5051b35cde3fa5137548058854a11c7c7c3372ccbc0dc99110a5e3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5811c06ddf0d65dfaf01c767c975df06d5f0a8f124c4b9efe14596955b9db97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3584ec13dddf764e11e2141ba06c324126e8deaaf775590ac8eee512b71f0089(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ceec877722e5f525a314c92507e6eaeabb460a7b7d02d36141ac352062fac90(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7801c114e57cbcf515a6d12f9d6424a303af0d088e2831c0567dc86f59920212(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94e92f6f2e07e5cca7820fdc16322b7e6fe991fe6b018c75b7c7ca470593b746(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37458a288afa8d859f7ed0dac59f780103293097c2b60d2280db67116dee3da7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__023b160078941155ade0b2d982c11728699c300f942e6cabebfa7f0426bd1a18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d869641dc1a47ec5fe3ad78b1189a32d1bdc0873c21d41eb4c8ff1725601b34(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a378baf6e7d4cf32f33331a685ac6758829e3b1a03f50a7545e743b36bf9cfbc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4345cb572416a6ff1935a916c0989ec644f462730e9db3bf4b2725560284cff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__626380b862474f627997150e35ed3dae6bfc8c1ecd72ef3785bfbf204ef59e78(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c4269c9f8aca0158964aa088909a289f99fb9fdbadbc27c4e70ddfc5c745a1a(
    *,
    header_set: typing.Optional[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSet, typing.Dict[builtins.str, typing.Any]]] = None,
    hosts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHosts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    methods: typing.Optional[typing.Sequence[builtins.str]] = None,
    paths: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsPaths, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ceb715d4fa6ecd15613aae45c76e251533be5dcf328c6d45b11d4d96b881283(
    *,
    headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a74ca3302aa27748c0b222da9466b1c7d78861d2c6810841a1f7cdbcea92551(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValue, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a3f3099aea3cfdd2e5bae29523faca8efe118ca13ae2a7a03cc70ee7eea1763(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89435e08edefaefd04d9d01401d062acd5d6bb31420bf4b421c01391c68ad17a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__114db9623b29ecdca98d9a97e10d12a484b3d5873aa1703618aad9ee2455147e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bacd42563a8548d434a80d14712b4e131e5ac44739e073893000c3c5a30d3b77(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4367e8789361b2bdc548ac42cc8cd42556d86c2a5f1ef5f127160bbbe6f4be61(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10d406da9e37dea2af0a6db68a7702a276761ee54635a206806b74e8642055f6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49976ba01dab0c26a9649b8984f5e35e528eae5cde9ae4e0370e23545691d98d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3463c24fa049b07a9ad8d090cb12cbda992e1c875398bd7b2a1006c99286ac3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9155da548c367c2daf6a598c92f2c2bc549c159efc1818915e3ce5ba9ef1d5b0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c192deaedd018376faa42d985c4f7bd1300fdd168d5476bdaac1d52467b684f4(
    *,
    contains: typing.Optional[builtins.str] = None,
    exact: typing.Optional[builtins.str] = None,
    ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prefix: typing.Optional[builtins.str] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c44ec3d0e6b6909f8df1e0af7e8f429bf50829197a7f9e721fe3a966a4471c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0359d4ae030192f106566d15ec80a4587e1aa5ea2914bd564fb9578508b6590b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feffe525edd6dcc5de26f90551e5db2dde8818cc5772390c7ee5f581e89aee93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aa03897f6ffeca4e8a3f4f32ec5565e3c57e2a7f3d44beb480a4a353190c363(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22aabaac4ded3058771a0f3bf2d18ceeae5885f5495bab29be3e818bc39f1160(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c691f9348ef075a3f617acbbcea11a7ed1d6581be9809538e2d598d46aa6610(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35701f652825f5d06bfae788c2432d827579ae154e267666fa088b8f266f8d16(
    value: typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75e11971b6b364d619cd2c2af77cf60e7990bacc53fe267c67cc5aaafbd11f2c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c1ad549f2b4a73ba69430edf19249a7a3a1cb585951122f831da474cc638c42(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8bd62e645cc74adb8bf2fd8f68191701274c2785ec53487b59741372635bdec(
    value: typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1522f7c58d5f6dcb631380ebe13e3f16cb61782e85bd73f3719a3b102a1767f1(
    *,
    contains: typing.Optional[builtins.str] = None,
    exact: typing.Optional[builtins.str] = None,
    ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prefix: typing.Optional[builtins.str] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbe4091822296aa96a70d7d682705cafe75cf9aa37af833a119ac7564cf692a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6efa705ac5b6f555e505b3f986f2ff5a9237cde2c07ebdac4b8c245223e09fc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09ddea738e3c0b400ec6bd80431bbfe074d9f061161cb69ab243327fdc54c96f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e84ef21e978b7f99ba9f36a86cff494834847fbe5088513f714e8e9e7d5490f6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c91223aea87c92312be46e9984e3946d81543d9d1dc41f20c8e824ce1644d588(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78f98209c777812271ea37f2a34601560f14bf4c1ca428cca524eebdf3c042a5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHosts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbd65406d8aa9a1749db6db3828b1ec934543af52e506095dc635796e3256b7a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__016a9c79637a47ce177667666b0b45bcc856749dc1e18c74526e291ca4e95609(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__817cf86b5a5d7c8999052b0e8cb1fe234de6e65911301befae3179f991abd905(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e422774485cc02e3848e59a14bed34e2cdcc1946a1f3ae5ddff0e4dc66a57c9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7384e42914169afe96eae2665cda85ec87c818fba6ec7e2350d1bc432cc17803(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d3074144f666578d0ac35b812016e6cf5371c32e33d7c7c04d91fe78056c477(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bebe6c7100d193952dcf9012a5e89f4ad9b6d8b83545f135785f8d75632d45e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHosts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47c29075073af7306616a7468836a0b150315f5fc415ab53a36b8a5c3533e222(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e71681ca6e3239f510ee0a68d7ea9627f5318d267c83f570d7eeb8f0e491fb53(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03383a8e3fad1ff4a977c2f098bf8a83af9fbd9233731c2e6ef5140b5e34dc66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98968dbb1e28500430eba634c44cad2b1835c2c6ec78798db7f7af8cfbb66b07(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__651b18bae8e0ec066531d1ae1c4c695168a92c420a73b95ba311bcf56b8076fc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d319a8ce289915b7dc695cd544c74e62433fde0069ba6ce110ced1bca91be17c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f8081b796159dfd7b037c18f1d572a25cc1bdbad71f6ca4dc34ae44cb46a787(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0389c5d2b1dd6f86729a510a488d4bb79a28863c970472792718495d87db406d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsHosts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8abe0edf8e3bb1daf3e7c26a2ca38c61ac1e482de10312b8b482529c74b5a239(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsPaths, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcd5f5eb12d5cf4a3e0e4b447a61f65e565ffcbb880ef3b5ffdd18e667f06d2b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45ce23dd4f1c263962c689a9fe9d6646af026816eba26fc7281c9b5da28a0517(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesToOperations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6efb307002b1341ad75102adc7fe927e1de2828d87d8e355d7f0d33bc3da0511(
    *,
    contains: typing.Optional[builtins.str] = None,
    exact: typing.Optional[builtins.str] = None,
    ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prefix: typing.Optional[builtins.str] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__495fbc6392fd85135439f981c74ae7a04c743b5acf1a2c82ed59e14cc7502d11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e72c42f667b6b9e64a94ac568974ae9e4f90cf1cb8ce69ee15eae8de189cbce(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ff9ad0d32041e02d9a12afd5064c5c7360441805df078060a3de864ca12c2d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f875fbe3ae8e6875678923ff30a3a01718b20a388dc3f425789ff1014dcdcdd1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6ad6acf7c1362b76459d5407def3cf04b85c57fb87d517901814646172e983b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27c0d73da59f28f5411caaf4b7cb3da3b78a1ffd3cc0c9380402ac455d3bb9fa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsPaths]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4be58b5ff8f334d4335531b8c46f953187abfc487ef01d8f2ac147e62cb24e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04a4732c1d81926d8b834fbd6b6407ff18a2eb424addd9b875425462a8ff5ed8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d4a432c804fa6f8da06aad66c57877d1a352c0c2778910b99183b469da211e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e48e419487947cf727d3e278af35890577609bab63a3d709ce9b8a3fd1e848b9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52b0d29b021bbfb8ff40e55f6f5f25620b9f48eee7008141df6796b8df5a974a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35ea892b2c7391384da6b9d156f8878f6b9da7f574b741dc29ae60d93fe3d058(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__359b2e0ccde4ee5bcd6d378ee2a08efd076acdcd592131e68820bd0ba5053401(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyHttpRulesToOperationsPaths]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d29c879af7ada699266f14d95e53c9b068933b52e1b3846000cd4fdc8dc69c95(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee791553eaa844b6bd0cf75e4d6f331d34c0b2a5eafbb107418bf9095c9190f7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesToNotOperations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e31abb8f166be7dad98ab8ca3440e62e29af2425e687ed3c6194668ee05006a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecurityAuthzPolicyHttpRulesToOperations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22a21f11ffa1675ddbd2979cb6225dfe224e8beadd716b4db9fdbad03ea444b6(
    value: typing.Optional[GoogleNetworkSecurityAuthzPolicyHttpRulesTo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__295e4974fd6d0a4b2a1ff31575427af97b6cb86a1a34ed0ccf8548831843a49a(
    *,
    load_balancing_scheme: builtins.str,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6711b053320bd4db558d7428aa614714324ac5fc8ee59a534417a1d234bbeebb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c036f3b8353c4dc6b891a8b7e59a84711b2dfa17cb4a478393eaf986bc8f45d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a1909b207dfd985fcdaafdcee6206b61bab36552f5b67336bd509da5b813760(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__992bb4f414d383e127db3d123901099d49d5c7944d1777143e96d18c156f1ec5(
    value: typing.Optional[GoogleNetworkSecurityAuthzPolicyTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26442eda2c8cfb4eea492562f589ec4aa52e44fa3c14e145901621db4eb03833(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5937d4d92901fc50b69998ba77ee10257d0cba3437401d934bbe198a4070f5cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e428494ecbf5009f33af79fce4ad8d7a8dc9b6ab3bf0a54c11e2649222ad9fba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76b0b7223beccea0496ff0e95970c3432a556db49527cebd0a2f7dfcf27eb6d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37b5e534feb51f423e39d6974625e7d08e179a88ca8a3fdd7cc26f7fb6426d6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed25794152a217087d168388d2d04475a38bcad8111937675777f266a48928c9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecurityAuthzPolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
